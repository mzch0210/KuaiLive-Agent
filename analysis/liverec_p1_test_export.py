from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from arguments import arg_parse
from data import SequenceDataset, get_sequences
from models import get_model_type
from p1_dev_memory_export import (
    EPS,
    MEMORY_WEIGHTS,
    SHORT_DECAY,
    SHORT_K,
    _Collator,
    batched_base_outputs,
    h10_from_rank0,
    load_data_with_availability_cache,
    memory_and_state_for_event,
    ndcg10_from_rank0,
    official_rank_list,
)

EXPECTED_COUNTS = {"dev": 46878, "test": 44221}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dev_reference_percentile(values: np.ndarray, sorted_ref: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    ref = np.asarray(sorted_ref, dtype=float)
    if ref.ndim != 1 or ref.size == 0 or not np.all(ref[:-1] <= ref[1:]):
        raise RuntimeError("Invalid frozen development ECDF")
    left = np.searchsorted(ref, values, side="left")
    right = np.searchsorted(ref, values, side="right")
    out = right.astype(np.float64) / float(ref.size)
    tied = right > left
    out[tied] = (left[tied] + right[tied] + 1.0) / (2.0 * float(ref.size))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--state-ecdf", required=True)
    ap.add_argument("--policy-manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--availability-cache", required=True)
    ap.add_argument("--split", choices=["dev", "test"], default="test")
    known, remaining = ap.parse_known_args()

    import sys
    sys.argv = [sys.argv[0]] + remaining
    args = arg_parse()
    args.device = torch.device(args.device)
    if args.device.type != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("P1.3 export requires CUDA")
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    split = known.split
    is_test = split == "test"
    state_ecdf_path = Path(known.state_ecdf)
    policy_manifest_path = Path(known.policy_manifest)
    manifest = json.loads(policy_manifest_path.read_text())
    ecdf = json.loads(state_ecdf_path.read_text())
    if manifest.get("test_ranking_inspected") is not False:
        raise RuntimeError("Policy preflight was not frozen before export")
    if manifest["source_p1_2"]["state_ecdf_sha256"] != sha256(state_ecdf_path):
        raise RuntimeError("Frozen development ECDF hash mismatch")
    mem_rule = manifest.get("memory_rule", {})
    if mem_rule.get("short_k") != SHORT_K or abs(float(mem_rule.get("short_decay")) - SHORT_DECAY) > 1e-15:
        raise RuntimeError("Frozen Memory short-term definition mismatch")
    if mem_rule.get("weights") != MEMORY_WEIGHTS:
        raise RuntimeError("Frozen Memory weights mismatch")

    out_dir = Path(known.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    data_fu = load_data_with_availability_cache(args, Path(known.availability_cache))
    if split == "dev":
        p1, p2 = args.pivot_1, args.pivot_2
    else:
        p1, p2 = args.pivot_2, args.max_step
    split_ds: SequenceDataset = get_sequences(data_fu, p1, p2, args)
    expected_n = EXPECTED_COUNTS[split]
    if len(split_ds) != expected_n:
        raise RuntimeError(f"Unexpected {split} target count: {len(split_ds)} != {expected_n}")

    split_loader = DataLoader(
        split_ds,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=_Collator(args.seq_len),
        num_workers=4,
        pin_memory=True,
        persistent_workers=True,
        prefetch_factor=2,
    )

    _, model_cls = get_model_type(args)
    model = model_cls(args).to(args.device)
    state = torch.load(known.checkpoint, map_location=args.device, weights_only=True)
    model.load_state_dict(state, strict=True)
    model.eval()

    # Verify optimized frozen-base evaluation against the pinned official scoring path.
    probe_batches = []
    it = iter(split_loader)
    for _ in range(2):
        probe_batches.append(next(it))
    official = official_rank_list(model, probe_batches, args)
    optimized = []
    with torch.inference_mode():
        for batch in probe_batches:
            optimized.extend(batched_base_outputs(model, batch, args)[0].tolist())
    if official != optimized:
        raise RuntimeError(f"P1.3 {split} batched base-rank optimization failed exact-equivalence guard")

    # The popularity component remains train-only, exactly as frozen in P1.2.
    train_raw = data_fu[data_fu.stop < args.pivot_1]
    counts = train_raw.groupby("streamer").size().astype(np.float64)
    logc = np.log1p(counts.to_numpy())
    pop_dense = np.zeros(args.N + 1, dtype=np.float64)
    if logc.size:
        lo, hi = float(logc.min()), float(logc.max())
        vals = np.zeros_like(logc) if hi <= lo + EPS else (logc - lo) / (hi - lo)
        pop_dense[counts.index.to_numpy(np.int64)] = vals

    split_users = set()
    for x in split_ds.data:
        u = x[4]
        nz = u[u != 0]
        if nz.numel():
            split_users.add(int(nz[-1].item()))
    raw_split = data_fu[data_fu.user.isin(split_users)].copy()
    rel_scratch = np.zeros(args.N + 1, dtype=np.float64)
    by_user = {int(uid): g for uid, g in raw_split.groupby("user", sort=False)}

    conf_names = [
        "base_score_std",
        "base_score_range",
        "base_margin12",
        "base_margin15",
        "base_margin1011",
        "base_top1_z",
        "base_entropy",
        "base_top10_mass",
    ]
    rows = []
    with torch.inference_mode():
        for data_cpu in split_loader:
            ranks, conf, steps, targets, inputs_np, pos_np = batched_base_outputs(model, data_cpu, args)
            users_np = data_cpu[:, :, 4].numpy()
            for b in range(data_cpu.shape[0]):
                uvals = users_np[b][users_np[b] != 0]
                if uvals.size == 0:
                    raise RuntimeError(f"{split} example has no user id")
                uid = int(uvals[-1])
                step = int(steps[b])
                target = int(targets[b])
                cands = np.asarray(args.ts[step], dtype=np.int64)
                mem = memory_and_state_for_event(by_user[uid], step, target, cands, pop_dense, rel_scratch)

                context = inputs_np[b]
                context = context[context != 0]
                recent_visible = bool(np.any(context == target))
                if recent_visible:
                    horizon = "recent_visible"
                elif mem["seen_before"]:
                    horizon = "long_horizon_only"
                else:
                    horizon = "unseen"

                prior_pos = pos_np[b, :-1]
                prior_pos = prior_pos[prior_pos != 0]
                official_repeat = bool(np.any(prior_pos == target))

                base_rank0 = int(ranks[b])
                mem_rank0 = int(mem.pop("memory_rank0"))
                row = {
                    "user_id": uid,
                    "target_step": step,
                    "target_streamer": target,
                    "candidate_count": int(len(cands)),
                    "official_repeat": official_repeat,
                    "relationship_horizon": horizon,
                    "base_rank0": base_rank0,
                    "memory_rank0": mem_rank0,
                    "base_ndcg10": ndcg10_from_rank0(base_rank0),
                    "memory_ndcg10": ndcg10_from_rank0(mem_rank0),
                    "base_h10": h10_from_rank0(base_rank0),
                    "memory_h10": h10_from_rank0(mem_rank0),
                    **mem,
                }
                row["memory_delta_ndcg10"] = row["memory_ndcg10"] - row["base_ndcg10"]
                row.update({name: float(conf[b, j]) for j, name in enumerate(conf_names)})
                rows.append(row)

    frame = pd.DataFrame(rows)
    if len(frame) != expected_n or len(frame) != len(split_ds):
        raise RuntimeError(f"P1.3 {split} row count mismatch: {len(frame)}")
    if frame.user_id.duplicated().any():
        raise RuntimeError(f"Expected one {split} target per user")
    if not np.isfinite(frame.select_dtypes(include=[np.number]).to_numpy()).all():
        raise RuntimeError(f"Non-finite numeric value in P1.3 {split} export")

    # Critical leakage guard: percentiles always use the frozen DEV reference.
    frame["preference_entropy_pct"] = dev_reference_percentile(
        frame.preference_entropy.to_numpy(float), np.asarray(ecdf["preference_entropy"], dtype=float)
    )
    frame["preference_drift_pct"] = dev_reference_percentile(
        frame.preference_drift.to_numpy(float), np.asarray(ecdf["preference_drift"], dtype=float)
    )
    frame["history_pct"] = dev_reference_percentile(
        frame.log_history_len.to_numpy(float), np.asarray(ecdf["log_history_len"], dtype=float)
    )
    frame["state_complexity"] = (
        0.4 * frame.preference_entropy_pct + 0.4 * frame.preference_drift_pct + 0.2 * frame.history_pct
    )

    if is_test:
        events_name = "p1_3_test_events.csv.gz"
        summary_name = "p1_3_test_export_summary.json"
        experiment = "liverec_twitch100k_p1_3_one_shot_test_export"
    else:
        events_name = "p1_3_dev_replay_events.csv.gz"
        summary_name = "p1_3_dev_replay_summary.json"
        experiment = "liverec_twitch100k_p1_3_pretest_dev_replay"

    frame.to_csv(out_dir / events_name, index=False, compression="gzip")
    summary = {
        "experiment": experiment,
        "split": split,
        "test_ranking_inspected": bool(is_test),
        "one_shot": bool(is_test),
        "n": int(len(frame)),
        "base": {
            "h1": float((frame.base_rank0 == 0).mean()),
            "ndcg10": float(frame.base_ndcg10.mean()),
            "h10": float(frame.base_h10.mean()),
        },
        "memory": {
            "ndcg10": float(frame.memory_ndcg10.mean()),
            "h10": float(frame.memory_h10.mean()),
        },
        "memory_minus_base_ndcg10": float(frame.memory_delta_ndcg10.mean()),
        "official_repeat_fraction": float(frame.official_repeat.mean()),
        "horizon_counts": {str(k): int(v) for k, v in frame.relationship_horizon.value_counts().to_dict().items()},
        "memory_definition": {
            "short_k": SHORT_K,
            "short_decay": SHORT_DECAY,
            "long": "count(streamer)/max_streamer_count over all strictly pre-target user interactions",
            "popularity": "train-only log1p streamer count, global min-max normalized",
            "weights": MEMORY_WEIGHTS,
            "tie_break": "higher score first; exact ties by lower factorized streamer id",
        },
        "state_transform": "frozen P1.2 development-reference ECDF; no split-distribution percentile fitting",
        "policy_manifest_sha256": sha256(policy_manifest_path),
        "base_rank_equivalence_guard": {"probe_batches": 2, "exact_match": True},
        "availability_cache_hit": bool(args._availability_cache_hit),
        "runtime_seconds": float(time.perf_counter() - t0),
        "guardrail": (
            "P1.3 one-shot untouched test; all policy components were frozen before export."
            if is_test
            else "Pre-test dev replay only; untouched test split is not constructed or inspected."
        ),
    }
    if is_test:
        summary["n_test"] = int(len(frame))
    else:
        summary["n_dev"] = int(len(frame))
    (out_dir / summary_name).write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
