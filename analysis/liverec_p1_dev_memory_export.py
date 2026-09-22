from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from arguments import arg_parse
from data import SequenceDataset, custom_collate, get_sequences
from models import get_model_type

EPS = 1e-12
MEMORY_WEIGHTS = {"short": 0.45, "long": 0.45, "popularity": 0.10}
SHORT_K = 10
SHORT_DECAY = 3.0


def ndcg10_from_rank0(rank0: int) -> float:
    return 0.0 if rank0 >= 10 else 1.0 / math.log2(rank0 + 2.0)


def h10_from_rank0(rank0: int) -> float:
    return float(rank0 < 10)


def norm_entropy(items: np.ndarray) -> float:
    n = int(items.size)
    if n <= 1:
        return 0.0
    _, counts = np.unique(items, return_counts=True)
    if counts.size <= 1:
        return 0.0
    p = counts.astype(np.float64) / float(n)
    return float(-(p * np.log(p)).sum() / math.log(counts.size))


def js_divergence(a: np.ndarray, b: np.ndarray) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0
    keys = np.union1d(a, b)
    ca = np.searchsorted(keys, a)
    cb = np.searchsorted(keys, b)
    pa = np.bincount(ca, minlength=len(keys)).astype(np.float64)
    pb = np.bincount(cb, minlength=len(keys)).astype(np.float64)
    pa /= max(pa.sum(), 1.0)
    pb /= max(pb.sum(), 1.0)
    m = 0.5 * (pa + pb)

    def kl(p, q):
        z = p > 0
        return float((p[z] * np.log2(p[z] / q[z])).sum())

    return 0.5 * kl(pa, m) + 0.5 * kl(pb, m)


def circular_regularity_steps(steps: np.ndarray) -> float:
    if steps.size == 0:
        return 0.0
    phase = (steps.astype(np.float64) % 144.0) / 144.0
    ang = 2.0 * np.pi * phase
    return float(np.hypot(np.cos(ang).mean(), np.sin(ang).mean()))


class _Collator:
    def __init__(self, args):
        self.args = args

    def __call__(self, batch):
        return custom_collate(batch, self.args)


def load_data_with_availability_cache(args, cache_path: Path) -> pd.DataFrame:
    """Official load_data semantics with an exact serialized availability cache."""
    infile = Path(args.dataset) / "100k.csv"
    cols = ["user", "stream", "streamer", "start", "stop"]
    data_fu = pd.read_csv(infile, header=None, names=cols)
    data_fu.user = pd.factorize(data_fu.user)[0] + 1
    data_fu["streamer_raw"] = data_fu.streamer
    data_fu.streamer = pd.factorize(data_fu.streamer)[0] + 1

    args.M = int(data_fu.user.max()) + 1
    args.N = int(data_fu.streamer.max()) + 2
    max_step = int(max(data_fu.start.max(), data_fu.stop.max()))
    args.max_step = max_step
    args.pivot_1 = max_step - 500
    args.pivot_2 = max_step - 250

    if cache_path.is_file():
        with cache_path.open("rb") as f:
            cached = pickle.load(f)
        if (
            cached.get("max_step") != args.max_step
            or cached.get("pivot_1") != args.pivot_1
            or cached.get("pivot_2") != args.pivot_2
        ):
            raise RuntimeError("Availability cache metadata mismatch")
        ts = cached["ts"]
        max_avail = int(cached["max_avail"])
        cache_hit = True
    else:
        ts = {}
        max_avail = 0
        for s in range(max_step + 1):
            all_av = data_fu[(data_fu.start <= s) & (data_fu.stop > s)].streamer.unique().tolist()
            ts[s] = all_av
            max_avail = max(max_avail, len(all_av))
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache_path.with_suffix(cache_path.suffix + ".tmp")
        with tmp.open("wb") as f:
            pickle.dump(
                {
                    "max_step": args.max_step,
                    "pivot_1": args.pivot_1,
                    "pivot_2": args.pivot_2,
                    "max_avail": max_avail,
                    "ts": ts,
                },
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
        os.replace(tmp, cache_path)
        cache_hit = False

    args.ts = ts
    args.max_avail = max_avail
    av_tens = torch.zeros(max_step + 1, max_avail, dtype=torch.long)
    for k, v in ts.items():
        av_tens[k, : len(v)] = torch.as_tensor(v, dtype=torch.long)
    args.av_tens = av_tens.to(args.device)
    args._availability_cache_hit = cache_hit
    return data_fu


def official_rank_list(model, batches, args) -> list[int]:
    """Exact pinned compute_rank scoring branch, retaining event order for guard."""
    ranks: list[int] = []
    model.eval()
    with torch.inference_mode():
        for data_cpu in batches:
            data = data_cpu.to(args.device)
            inputs = data[:, :, 3]
            pos = data[:, :, 5]
            xtsy = data[:, :, 6]
            feats = model(inputs)
            ctx, batch_inds = model.get_ctx_att(data, feats)
            for b in range(inputs.shape[0]):
                step = int(xtsy[b, -1].item())
                av = torch.LongTensor(args.ts[step]).to(args.device)
                ctx_expand = torch.zeros(args.av_tens.shape[1], args.K, device=args.device)
                ctx_expand[batch_inds[b, -1, :], :] = ctx[b, -1, :, :]
                scores = (feats[b, -1, :] * ctx_expand).sum(-1)[: len(av)]
                idx = torch.where(pos[b, -1] == av)[0]
                rank = torch.where(torch.argsort(scores, descending=True) == idx)[0]
                if rank.numel() != 1:
                    raise RuntimeError("official rank guard found non-unique target")
                ranks.append(int(rank.item()))
    return ranks


def batched_base_outputs(model, data_cpu, args):
    """Vectorized frozen-base ranks + confidence without changing score semantics."""
    data = data_cpu.to(args.device, non_blocking=bool(data_cpu.is_pinned()))
    inputs = data[:, :, 3]
    pos = data[:, :, 5]
    xtsy = data[:, :, 6]
    feats = model(inputs)
    ctx, batch_inds = model.get_ctx_att(data, feats)

    final_feat = feats[:, -1, :]
    final_ctx = ctx[:, -1, :, :]
    final_inds = batch_inds[:, -1, :]
    top_scores = (final_ctx * final_feat[:, None, :]).sum(-1)

    bsz = inputs.shape[0]
    max_av = args.av_tens.shape[1]
    scores = torch.zeros((bsz, max_av), dtype=top_scores.dtype, device=args.device)
    scores.scatter_(1, final_inds, top_scores)

    steps = xtsy[:, -1]
    lengths = torch.as_tensor([len(args.ts[int(x)]) for x in steps.detach().cpu().tolist()], device=args.device)
    ar = torch.arange(max_av, device=args.device).unsqueeze(0)
    valid = ar < lengths.unsqueeze(1)
    masked_scores = scores.masked_fill(~valid, -torch.inf)

    order = torch.argsort(masked_scores, dim=1, descending=True)
    av_rows = args.av_tens[steps, :]
    target_mask = av_rows == pos[:, -1].unsqueeze(1)
    target_pos = target_mask.to(torch.int64).argmax(dim=1)
    if not bool(target_mask.any(dim=1).all().item()):
        raise RuntimeError("At least one dev target is not in the legal active candidate set")
    ranks = (order == target_pos.unsqueeze(1)).to(torch.int64).argmax(dim=1)

    n = lengths.to(scores.dtype)
    s1 = scores.masked_fill(~valid, 0.0).sum(dim=1)
    s2 = scores.square().masked_fill(~valid, 0.0).sum(dim=1)
    mean = s1 / n
    var = torch.clamp(s2 / n - mean.square(), min=0.0)
    std = torch.sqrt(var)
    maxv = masked_scores.max(dim=1).values
    minv = scores.masked_fill(~valid, torch.inf).min(dim=1).values
    rng = maxv - minv
    top11 = torch.topk(masked_scores, k=11, dim=1).values

    shifted = masked_scores - maxv.unsqueeze(1)
    ex = torch.exp(torch.clamp(shifted, min=-60.0, max=0.0)).masked_fill(~valid, 0.0)
    z = ex.sum(dim=1, keepdim=True)
    prob = ex / z
    entropy = -(prob * torch.log(torch.clamp(prob, min=EPS))).sum(dim=1) / torch.log(n)
    top10_mass = torch.topk(prob, k=10, dim=1).values.sum(dim=1)

    conf = torch.stack(
        [
            std,
            rng,
            top11[:, 0] - top11[:, 1],
            top11[:, 0] - top11[:, 4],
            top11[:, 9] - top11[:, 10],
            (top11[:, 0] - mean) / torch.clamp(std, min=EPS),
            entropy,
            top10_mass,
        ],
        dim=1,
    )
    return (
        ranks.detach().cpu().numpy(),
        conf.detach().cpu().numpy(),
        steps.detach().cpu().numpy(),
        pos[:, -1].detach().cpu().numpy(),
        data_cpu[:, :, 3].numpy(),
        data_cpu[:, :, 5].numpy(),
    )


def memory_and_state_for_event(
    user_rows: pd.DataFrame,
    target_step: int,
    target_sid: int,
    candidates: np.ndarray,
    pop_dense: np.ndarray,
    rel_scratch: np.ndarray,
):
    hist = user_rows[user_rows.start < target_step].sort_values("start", kind="mergesort")
    sids = hist.streamer.to_numpy(np.int64)
    steps = hist.start.to_numpy(np.int64)
    n = int(sids.size)

    if n:
        uniq, counts = np.unique(sids, return_counts=True)
        maxc = int(counts.max())
        long_ids = uniq
        long_vals = counts.astype(np.float64) / float(maxc)
    else:
        long_ids = np.empty(0, dtype=np.int64)
        long_vals = np.empty(0, dtype=np.float64)

    short_map: dict[int, float] = {}
    for dist, sid in enumerate(reversed(sids[-SHORT_K:].tolist())):
        val = math.exp(-dist / SHORT_DECAY)
        sid = int(sid)
        if val > short_map.get(sid, 0.0):
            short_map[sid] = val

    touched = long_ids
    if long_ids.size:
        rel_scratch[long_ids] = MEMORY_WEIGHTS["long"] * long_vals
    if short_map:
        short_ids = np.fromiter(short_map.keys(), dtype=np.int64, count=len(short_map))
        short_vals = np.fromiter(short_map.values(), dtype=np.float64, count=len(short_map))
        rel_scratch[short_ids] += MEMORY_WEIGHTS["short"] * short_vals
        touched = np.union1d(long_ids, short_ids)

    score = (
        MEMORY_WEIGHTS["popularity"] * pop_dense[candidates]
        + rel_scratch[candidates]
    ).astype(np.float64, copy=False)
    if touched.size:
        rel_scratch[touched] = 0.0

    target_idx_arr = np.flatnonzero(candidates == target_sid)
    if target_idx_arr.size != 1:
        raise RuntimeError(f"target candidate multiplicity={target_idx_arr.size}")
    ti = int(target_idx_arr[0])
    ts = float(score[ti])
    rank0 = int(np.sum(score > ts + EPS) + np.sum((np.abs(score - ts) <= EPS) & (candidates < target_sid)))

    uniq_n = int(np.unique(sids).size) if n else 0
    repeat_rate = 1.0 - uniq_n / max(n, 1)
    pref_ent = norm_entropy(sids)
    recent_n = min(10, max(2, n // 3)) if n >= 3 else max(1, n // 2)
    old = sids[:-recent_n] if n > recent_n else sids[: max(1, n // 2)]
    recent = sids[-recent_n:] if recent_n else sids
    drift = js_divergence(old, recent) if old.size and recent.size else 0.0
    regularity = circular_regularity_steps(steps)

    return {
        "memory_rank0": rank0,
        "history_len": n,
        "log_history_len": math.log1p(n),
        "repeat_rate": repeat_rate,
        "preference_entropy": pref_ent,
        "preference_drift": drift,
        "time_regularity": regularity,
        "seen_before": bool(np.any(sids == target_sid)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--availability-cache", required=True)
    known, remaining = ap.parse_known_args()

    import sys
    sys.argv = [sys.argv[0]] + remaining
    args = arg_parse()
    args.device = torch.device(args.device)
    if args.device.type != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("P1.2 GPU export requires CUDA")
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    out_dir = Path(known.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    data_fu = load_data_with_availability_cache(args, Path(known.availability_cache))
    dev_ds: SequenceDataset = get_sequences(data_fu, args.pivot_1, args.pivot_2, args)
    val_loader = DataLoader(
        dev_ds,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=_Collator(args),
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

    probe_batches = []
    it = iter(val_loader)
    for _ in range(2):
        probe_batches.append(next(it))
    official = official_rank_list(model, probe_batches, args)
    optimized = []
    with torch.inference_mode():
        for batch in probe_batches:
            optimized.extend(batched_base_outputs(model, batch, args)[0].tolist())
    if official != optimized:
        raise RuntimeError("Batched base-rank optimization failed exact-equivalence guard")

    train_raw = data_fu[data_fu.stop < args.pivot_1]
    counts = train_raw.groupby("streamer").size().astype(np.float64)
    logc = np.log1p(counts.to_numpy())
    pop_dense = np.zeros(args.N + 1, dtype=np.float64)
    if logc.size:
        lo, hi = float(logc.min()), float(logc.max())
        vals = np.zeros_like(logc) if hi <= lo + EPS else (logc - lo) / (hi - lo)
        pop_dense[counts.index.to_numpy(np.int64)] = vals

    dev_users = set()
    for x in dev_ds.data:
        u = x[4]
        nz = u[u != 0]
        if nz.numel():
            dev_users.add(int(nz[-1].item()))
    raw_dev = data_fu[data_fu.user.isin(dev_users)].copy()
    rel_scratch = np.zeros(args.N + 1, dtype=np.float64)
    by_user = {int(uid): g for uid, g in raw_dev.groupby("user", sort=False)}

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
        for data_cpu in val_loader:
            ranks, conf, steps, targets, inputs_np, pos_np = batched_base_outputs(model, data_cpu, args)
            users_np = data_cpu[:, :, 4].numpy()
            for b in range(data_cpu.shape[0]):
                uvals = users_np[b][users_np[b] != 0]
                if uvals.size == 0:
                    raise RuntimeError("dev example has no user id")
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

    dev = pd.DataFrame(rows)
    if len(dev) != len(dev_ds):
        raise RuntimeError(f"row count mismatch: {len(dev)} != {len(dev_ds)}")
    if dev.user_id.duplicated().any():
        raise RuntimeError("Expected one dev target per user")
    if not np.isfinite(dev.select_dtypes(include=[np.number]).to_numpy()).all():
        raise RuntimeError("Non-finite numeric value in P1.2 dev export")

    dev["preference_entropy_pct"] = dev.preference_entropy.rank(pct=True, method="average")
    dev["preference_drift_pct"] = dev.preference_drift.rank(pct=True, method="average")
    dev["history_pct"] = dev.log_history_len.rank(pct=True, method="average")
    dev["state_complexity"] = (
        0.4 * dev.preference_entropy_pct + 0.4 * dev.preference_drift_pct + 0.2 * dev.history_pct
    )

    base_h1 = float((dev.base_rank0 == 0).mean())
    base_ndcg10 = float(dev.base_ndcg10.mean())
    if abs(base_h1 - 0.39299884807372326) > 5e-6:
        raise RuntimeError(f"Frozen-base H@1 mismatch: {base_h1}")
    if abs(base_ndcg10 - 0.5718533988252721) > 5e-6:
        raise RuntimeError(f"Frozen-base NDCG@10 mismatch: {base_ndcg10}")

    csv_path = out_dir / "p1_2_dev_events.csv.gz"
    dev.to_csv(csv_path, index=False, compression="gzip")
    ecdf = {
        "preference_entropy": np.sort(dev.preference_entropy.to_numpy(float)).tolist(),
        "preference_drift": np.sort(dev.preference_drift.to_numpy(float)).tolist(),
        "log_history_len": np.sort(dev.log_history_len.to_numpy(float)).tolist(),
    }
    (out_dir / "p1_2_state_ecdf.json").write_text(json.dumps(ecdf) + "\n")

    summary = {
        "experiment": "liverec_twitch100k_p1_2_dev_memory_export",
        "test_ranking_inspected": False,
        "n_dev": int(len(dev)),
        "base": {"h1": base_h1, "ndcg10": base_ndcg10, "h10": float(dev.base_h10.mean())},
        "memory": {"ndcg10": float(dev.memory_ndcg10.mean()), "h10": float(dev.memory_h10.mean())},
        "memory_minus_base_ndcg10": float(dev.memory_delta_ndcg10.mean()),
        "official_repeat_fraction": float(dev.official_repeat.mean()),
        "horizon_counts": {str(k): int(v) for k, v in dev.relationship_horizon.value_counts().to_dict().items()},
        "memory_definition": {
            "short_k": SHORT_K,
            "short_decay": SHORT_DECAY,
            "long": "count(streamer)/max_streamer_count over all strictly pre-target user interactions",
            "popularity": "train-only log1p streamer count, global min-max normalized",
            "weights": MEMORY_WEIGHTS,
            "tie_break": "higher score first; exact ties by lower factorized streamer id",
        },
        "base_rank_equivalence_guard": {"probe_batches": 2, "exact_match": True},
        "availability_cache_hit": bool(args._availability_cache_hit),
        "runtime_seconds": float(time.perf_counter() - t0),
        "guardrail": "Frozen LiveRec checkpoint is read-only; only dev sequences are materialized; test ranking is not constructed or inspected.",
    }
    (out_dir / "p1_2_dev_export_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
