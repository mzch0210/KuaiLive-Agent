from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

EPS = 1e-12
SEED = 20260922
SHORT_K = 10
SHORT_DECAY = 3.0
VARIANTS = ("popularity_only", "short_only", "long_only", "short_long", "full_memory")
EXPECTED_N = 46878


def ndcg10(rank0: int) -> float:
    return 0.0 if rank0 >= 10 else 1.0 / math.log2(rank0 + 2.0)


def h10(rank0: int) -> float:
    return float(rank0 < 10)


def rank_from_score(candidates: np.ndarray, scores: np.ndarray, target_sid: int) -> int:
    idx = np.flatnonzero(candidates == target_sid)
    if idx.size != 1:
        raise RuntimeError(f"target candidate multiplicity={idx.size} for target={target_sid}")
    ts = float(scores[int(idx[0])])
    return int(
        np.count_nonzero(scores > ts + EPS)
        + np.count_nonzero((np.abs(scores - ts) <= EPS) & (candidates < target_sid))
    )


def bootstrap_columns(diff: np.ndarray, seed: int, n_boot: int = 5000, chunk: int = 32):
    x = np.asarray(diff, dtype=np.float64)
    if x.ndim == 1:
        x = x[:, None]
    n, d = x.shape
    rng = np.random.default_rng(seed)
    means = np.empty((n_boot, d), dtype=np.float64)
    out = 0
    while out < n_boot:
        b = min(chunk, n_boot - out)
        idx = rng.integers(0, n, size=(b, n), dtype=np.int32)
        means[out : out + b] = x[idx].mean(axis=1)
        out += b
    return [
        {
            "mean": float(x[:, j].mean()),
            "ci95_low": float(np.quantile(means[:, j], 0.025)),
            "ci95_high": float(np.quantile(means[:, j], 0.975)),
            "n": int(n),
            "n_boot": int(n_boot),
        }
        for j in range(d)
    ]


def build_active_matrix(
    starts: np.ndarray,
    stops: np.ndarray,
    streamers: np.ndarray,
    target_steps: np.ndarray,
    max_streamer: int,
) -> np.ndarray:
    """Active streamer counts only on DEV target steps; avoids max_step-wide tensors."""
    t = len(target_steps)
    diff = np.zeros((max_streamer + 1, t + 1), dtype=np.int32)
    left = np.searchsorted(target_steps, starts, side="left")
    right = np.searchsorted(target_steps, stops, side="left")
    m = (left < right) & (left < t)
    np.add.at(diff, (streamers[m], left[m]), 1)
    mr = m & (right < t)
    np.add.at(diff, (streamers[mr], right[mr]), -1)
    np.cumsum(diff[:, :t], axis=1, out=diff[:, :t])
    return diff[:, :t]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-oof", type=Path, required=True)
    ap.add_argument("--twitch-csv", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-boot", type=int, default=5000)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    dev = pd.read_csv(args.dev_oof)
    required = {
        "user_id", "target_step", "target_streamer", "candidate_count",
        "relationship_horizon", "base_ndcg10", "base_h10",
        "memory_rank0", "memory_ndcg10", "memory_h10", "history_len",
    }
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"missing frozen DEV columns: {missing}")
    if len(dev) != EXPECTED_N or dev.user_id.duplicated().any():
        raise RuntimeError(f"unexpected frozen DEV shape/identity: n={len(dev)}")
    if set(dev.relationship_horizon.unique()) != {"recent_visible", "long_horizon_only", "unseen"}:
        raise RuntimeError("unexpected relationship-horizon labels")

    cols = ["user", "stream", "streamer", "start", "stop"]
    raw = pd.read_csv(args.twitch_csv, header=None, names=cols)
    raw["row_id"] = np.arange(len(raw), dtype=np.int64)
    raw["user_id"] = pd.factorize(raw.user)[0].astype(np.int64) + 1
    raw["streamer_id"] = pd.factorize(raw.streamer)[0].astype(np.int64) + 1

    starts = raw.start.to_numpy(np.int64)
    stops = raw.stop.to_numpy(np.int64)
    users = raw.user_id.to_numpy(np.int64)
    sids = raw.streamer_id.to_numpy(np.int64)
    row_ids = raw.row_id.to_numpy(np.int64)
    max_step = int(max(starts.max(), stops.max()))
    pivot_1 = max_step - 500
    max_sid = int(sids.max())

    # Frozen train-only popularity.
    train_mask = stops < pivot_1
    pop_counts = np.bincount(sids[train_mask], minlength=max_sid + 1).astype(np.float64)
    pop_log = np.log1p(pop_counts)
    seen_train = pop_counts > 0
    pop = np.zeros(max_sid + 1, dtype=np.float64)
    if np.any(seen_train):
        lo = float(pop_log[seen_train].min())
        hi = float(pop_log[seen_train].max())
        if hi > lo + EPS:
            pop[seen_train] = (pop_log[seen_train] - lo) / (hi - lo)

    # Build active candidates only for target steps represented in frozen DEV.
    target_steps = np.sort(dev.target_step.unique().astype(np.int64))
    active_counts = build_active_matrix(starts, stops, sids, target_steps, max_sid)
    step_to_col = {int(s): i for i, s in enumerate(target_steps.tolist())}

    # Stable per-user history order: user, start, original row.
    order = np.lexsort((row_ids, starts, users))
    su = users[order]
    ss = starts[order]
    sid_sorted = sids[order]
    uniq_u, first, counts_u = np.unique(su, return_index=True, return_counts=True)
    bounds = {int(u): (int(a), int(a + c)) for u, a, c in zip(uniq_u, first, counts_u)}

    long_scratch = np.zeros(max_sid + 1, dtype=np.float64)
    short_scratch = np.zeros(max_sid + 1, dtype=np.float64)

    ranks = {v: np.empty(len(dev), dtype=np.int64) for v in VARIANTS}
    candidate_mismatch = 0
    history_mismatch = 0

    for i, row in enumerate(dev.itertuples(index=False)):
        uid = int(row.user_id)
        step = int(row.target_step)
        target = int(row.target_streamer)
        j = step_to_col[step]
        candidates = np.flatnonzero(active_counts[:, j] > 0).astype(np.int64, copy=False)
        if len(candidates) != int(row.candidate_count):
            candidate_mismatch += 1

        lo, hi = bounds[uid]
        n = int(np.searchsorted(ss[lo:hi], step, side="left"))
        hist = sid_sorted[lo : lo + n]
        if n != int(row.history_len):
            history_mismatch += 1

        if n:
            long_ids, long_counts = np.unique(hist, return_counts=True)
            long_scratch[long_ids] = long_counts.astype(np.float64) / float(long_counts.max())
        else:
            long_ids = np.empty(0, dtype=np.int64)

        short_map: dict[int, float] = {}
        for dist, sid in enumerate(reversed(hist[-SHORT_K:].tolist())):
            val = math.exp(-dist / SHORT_DECAY)
            sid = int(sid)
            if val > short_map.get(sid, 0.0):
                short_map[sid] = val
        if short_map:
            short_ids = np.fromiter(short_map.keys(), dtype=np.int64, count=len(short_map))
            short_vals = np.fromiter(short_map.values(), dtype=np.float64, count=len(short_map))
            short_scratch[short_ids] = short_vals
        else:
            short_ids = np.empty(0, dtype=np.int64)

        p = pop[candidates]
        s = short_scratch[candidates]
        l = long_scratch[candidates]
        score_map = {
            "popularity_only": p,
            "short_only": s,
            "long_only": l,
            # A common positive scaling does not affect ranking.
            "short_long": 0.5 * s + 0.5 * l,
            "full_memory": 0.10 * p + 0.45 * s + 0.45 * l,
        }
        for v in VARIANTS:
            ranks[v][i] = rank_from_score(candidates, score_map[v], target)

        if long_ids.size:
            long_scratch[long_ids] = 0.0
        if short_ids.size:
            short_scratch[short_ids] = 0.0

    full_rank_mismatch = int(np.count_nonzero(ranks["full_memory"] != dev.memory_rank0.to_numpy(np.int64)))
    full_ndcg = np.fromiter((ndcg10(int(r)) for r in ranks["full_memory"]), dtype=np.float64, count=len(dev))
    full_h = (ranks["full_memory"] < 10).astype(np.float64)
    full_ndcg_mismatch = int(np.count_nonzero(np.abs(full_ndcg - dev.memory_ndcg10.to_numpy(float)) > 1e-15))
    full_h_mismatch = int(np.count_nonzero(full_h != dev.memory_h10.to_numpy(float)))

    guards = {
        "candidate_count_mismatches": int(candidate_mismatch),
        "history_len_mismatches": int(history_mismatch),
        "full_memory_rank_mismatches": full_rank_mismatch,
        "full_memory_ndcg10_mismatches": full_ndcg_mismatch,
        "full_memory_h10_mismatches": full_h_mismatch,
    }
    if any(guards.values()):
        raise RuntimeError(f"frozen Memory reconstruction guard failed: {guards}")

    base_ndcg = dev.base_ndcg10.to_numpy(float)
    base_h = dev.base_h10.to_numpy(float)
    event_out = dev[["user_id", "target_step", "target_streamer", "relationship_horizon", "base_ndcg10", "base_h10"]].copy()

    variant_ndcg = {}
    variant_h = {}
    for v in VARIANTS:
        nd = np.fromiter((ndcg10(int(r)) for r in ranks[v]), dtype=np.float64, count=len(dev))
        hh = (ranks[v] < 10).astype(np.float64)
        variant_ndcg[v] = nd
        variant_h[v] = hh
        event_out[f"{v}_rank0"] = ranks[v]
        event_out[f"{v}_ndcg10"] = nd
        event_out[f"{v}_h10"] = hh

    groups = [("all", np.ones(len(dev), dtype=bool))]
    for h in ("recent_visible", "long_horizon_only", "unseen"):
        groups.append((h, dev.relationship_horizon.to_numpy() == h))

    rows = []
    ci_report = {}
    for gi, (gname, mask) in enumerate(groups):
        cols_diff = []
        labels = []
        for v in VARIANTS:
            cols_diff.append(variant_ndcg[v][mask] - base_ndcg[mask])
            labels.append((v, "ndcg10"))
            cols_diff.append(variant_h[v][mask] - base_h[mask])
            labels.append((v, "h10"))
        diff_matrix = np.column_stack(cols_diff)
        cis = bootstrap_columns(diff_matrix, SEED + gi, n_boot=args.n_boot)
        ci_report[gname] = {}
        for (v, metric), ci in zip(labels, cis):
            ci_report[gname].setdefault(v, {})[metric] = ci
        for v in VARIANTS:
            rows.append(
                {
                    "group": gname,
                    "n": int(mask.sum()),
                    "variant": v,
                    "ndcg10": float(variant_ndcg[v][mask].mean()),
                    "base_ndcg10": float(base_ndcg[mask].mean()),
                    "delta_ndcg10": float((variant_ndcg[v][mask] - base_ndcg[mask]).mean()),
                    "delta_ndcg10_ci95_low": ci_report[gname][v]["ndcg10"]["ci95_low"],
                    "delta_ndcg10_ci95_high": ci_report[gname][v]["ndcg10"]["ci95_high"],
                    "h10": float(variant_h[v][mask].mean()),
                    "base_h10": float(base_h[mask].mean()),
                    "delta_h10": float((variant_h[v][mask] - base_h[mask]).mean()),
                    "delta_h10_ci95_low": ci_report[gname][v]["h10"]["ci95_low"],
                    "delta_h10_ci95_high": ci_report[gname][v]["h10"]["ci95_high"],
                }
            )

    table = pd.DataFrame(rows)
    table.to_csv(args.out_dir / "kbs_memory_component_horizon_ablation.csv", index=False)
    event_out.to_csv(args.out_dir / "kbs_memory_component_dev_events.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "kbs_memory_component_by_relationship_horizon_dev_only",
        "test_ranking_inspected": False,
        "n_dev": int(len(dev)),
        "variants": {
            "popularity_only": "train-only normalized popularity",
            "short_only": "last-10 exp(-distance/3) relationship recurrence",
            "long_only": "strict pre-target count/max-count relationship strength",
            "short_long": "0.5*short + 0.5*long (ranking-equivalent to frozen 0.45+0.45 without popularity)",
            "full_memory": "0.10*popularity + 0.45*short + 0.45*long",
        },
        "reconstruction_guards": guards,
        "n_unique_dev_target_steps": int(len(target_steps)),
        "runtime_seconds": float(time.perf_counter() - t0),
        "results": rows,
        "interpretation_guardrail": (
            "DEV-only journal-strengthening analysis. It does not alter the frozen P1.3 Memory, gate, threshold, "
            "or untouched test results."
        ),
    }
    (args.out_dir / "kbs_memory_component_horizon_ablation.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n"
    )
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
