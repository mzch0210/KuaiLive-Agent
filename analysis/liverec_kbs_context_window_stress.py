from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

EXPECTED_N = 46878
SEED = 20260922
SEQ_LEN_REF = 16
WINDOWS = (4, 8, 16, 32, 64, 128)


def bootstrap(x, seed, n_boot=3000, chunk=64):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n == 0:
        return {"mean": None, "ci95_low": None, "ci95_high": None, "n": 0}
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot, dtype=float)
    p = 0
    while p < n_boot:
        b = min(chunk, n_boot - p)
        idx = rng.integers(0, n, size=(b, n), dtype=np.int32)
        out[p:p+b] = x[idx].mean(axis=1)
        p += b
    return {
        "mean": float(x.mean()),
        "ci95_low": float(np.quantile(out, 0.025)),
        "ci95_high": float(np.quantile(out, 0.975)),
        "n": int(n),
    }


def summarize(mask, base, mem, seed, n_boot):
    idx = np.flatnonzero(mask)
    if len(idx) == 0:
        return {
            "n": 0,
            "base_ndcg10": None,
            "memory_ndcg10": None,
            "delta_vs_base": None,
            "ci95_low": None,
            "ci95_high": None,
        }
    ci = bootstrap(mem[idx] - base[idx], seed, n_boot)
    return {
        "n": int(len(idx)),
        "base_ndcg10": float(base[idx].mean()),
        "memory_ndcg10": float(mem[idx].mean()),
        "delta_vs_base": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-oof", type=Path, required=True)
    ap.add_argument("--twitch-csv", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-boot", type=int, default=3000)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)

    dev = pd.read_csv(a.dev_oof)
    req = {
        "user_id", "target_step", "target_streamer", "relationship_horizon",
        "history_len", "seen_before", "base_ndcg10", "memory_ndcg10",
    }
    miss = req - set(dev.columns)
    if miss or len(dev) != EXPECTED_N or dev.user_id.duplicated().any():
        raise RuntimeError(f"bad frozen DEV: missing={sorted(miss)}, n={len(dev)}")

    raw = pd.read_csv(
        a.twitch_csv,
        header=None,
        names=["user", "stream", "streamer", "start", "stop"],
    )
    raw["row"] = np.arange(len(raw), dtype=np.int64)
    raw["uid"] = pd.factorize(raw.user)[0] + 1
    raw["sid"] = pd.factorize(raw.streamer)[0] + 1

    users = raw.uid.to_numpy(np.int64)
    starts = raw.start.to_numpy(np.int64)
    sids = raw.sid.to_numpy(np.int64)
    rows = raw.row.to_numpy(np.int64)
    order = np.lexsort((rows, starts, users))
    su, ss, si = users[order], starts[order], sids[order]
    uu, first, counts = np.unique(su, return_index=True, return_counts=True)
    bounds = {int(u): (int(f), int(f+c)) for u, f, c in zip(uu, first, counts)}

    recency = np.full(len(dev), np.inf, dtype=float)
    hist_bad = 0
    seen_bad = 0
    horizon_bad = 0

    for i, r in enumerate(dev.itertuples(index=False)):
        lo, hi = bounds[int(r.user_id)]
        n = int(np.searchsorted(ss[lo:hi], int(r.target_step), side="left"))
        hist = si[lo:lo+n]
        if n != int(r.history_len):
            hist_bad += 1
        pos = np.flatnonzero(hist == int(r.target_streamer))
        seen = bool(pos.size)
        if seen != bool(r.seen_before):
            seen_bad += 1
        if seen:
            recency[i] = float(n - int(pos[-1]))
            if str(r.relationship_horizon) == "unseen":
                horizon_bad += 1
        elif str(r.relationship_horizon) != "unseen":
            horizon_bad += 1

    if hist_bad or seen_bad or horizon_bad:
        raise RuntimeError(
            f"reconstruction mismatch history={hist_bad} seen={seen_bad} horizon={horizon_bad}"
        )

    horizon = dev.relationship_horizon.astype(str).to_numpy()
    seen = np.isfinite(recency)
    frozen_recent = horizon == "recent_visible"
    frozen_long = horizon == "long_horizon_only"
    frozen_unseen = horizon == "unseen"

    cutoff_rows = []
    for w in range(1, 65):
        pred = seen & (recency <= w)
        mism = int(np.sum(pred != frozen_recent))
        cutoff_rows.append({"window": w, "mismatches": mism})
    best = min(cutoff_rows, key=lambda z: (z["mismatches"], abs(z["window"] - SEQ_LEN_REF)))
    ref_mism = next(z["mismatches"] for z in cutoff_rows if z["window"] == SEQ_LEN_REF)

    base = dev.base_ndcg10.to_numpy(float)
    mem = dev.memory_ndcg10.to_numpy(float)

    rows_out = []
    distance_specs = [
        ("1-4", seen & (recency >= 1) & (recency <= 4)),
        ("5-8", seen & (recency >= 5) & (recency <= 8)),
        ("9-16", seen & (recency >= 9) & (recency <= 16)),
        ("17-32", seen & (recency >= 17) & (recency <= 32)),
        ("33-64", seen & (recency >= 33) & (recency <= 64)),
        ("65+", seen & (recency >= 65)),
        ("unseen", ~seen),
    ]
    for j, (label, mask) in enumerate(distance_specs):
        s = summarize(mask, base, mem, SEED + j, a.n_boot)
        rows_out.append({"analysis": "last_seen_distance", "group": label, **s})

    window_rows = []
    for j, w in enumerate(WINDOWS):
        inside = seen & (recency <= w)
        outside = seen & (recency > w)
        s_in = summarize(inside, base, mem, SEED + 100 + 2*j, a.n_boot)
        s_out = summarize(outside, base, mem, SEED + 101 + 2*j, a.n_boot)
        row = {
            "window": int(w),
            "inside_n": s_in["n"],
            "inside_delta": s_in["delta_vs_base"],
            "inside_ci95_low": s_in["ci95_low"],
            "inside_ci95_high": s_in["ci95_high"],
            "outside_n": s_out["n"],
            "outside_delta": s_out["delta_vs_base"],
            "outside_ci95_low": s_out["ci95_low"],
            "outside_ci95_high": s_out["ci95_high"],
        }
        window_rows.append(row)

    frozen_rows = []
    for j, (label, mask) in enumerate(
        [("recent_visible", frozen_recent), ("long_horizon_only", frozen_long), ("unseen", frozen_unseen)]
    ):
        frozen_rows.append({"horizon": label, **summarize(mask, base, mem, SEED + 300 + j, a.n_boot)})

    pd.DataFrame(rows_out).to_csv(a.out_dir / "context_distance_bins.csv", index=False)
    pd.DataFrame(window_rows).to_csv(a.out_dir / "context_window_sweep.csv", index=False)
    pd.DataFrame(frozen_rows).to_csv(a.out_dir / "frozen_horizon_replay.csv", index=False)
    pd.DataFrame(cutoff_rows).to_csv(a.out_dir / "recent_visibility_cutoff_audit.csv", index=False)

    dtab = {r["group"]: r for r in rows_out}
    pre = [dtab[k]["delta_vs_base"] for k in ("1-4", "5-8", "9-16") if dtab[k]["n"] > 0]
    post = [dtab[k]["delta_vs_base"] for k in ("17-32", "33-64", "65+") if dtab[k]["n"] > 0]
    report = {
        "experiment": "KBS post-P1.3 DEV-only finite-context stress test",
        "test_ranking_inspected": False,
        "n_dev": int(len(dev)),
        "seq_len_reference": SEQ_LEN_REF,
        "history_mismatches": int(hist_bad),
        "seen_before_mismatches": int(seen_bad),
        "horizon_seen_unseen_mismatches": int(horizon_bad),
        "best_simple_visibility_cutoff": best,
        "seq_len_16_visibility_mismatches": int(ref_mism),
        "frozen_horizon_counts": {
            "recent_visible": int(frozen_recent.sum()),
            "long_horizon_only": int(frozen_long.sum()),
            "unseen": int(frozen_unseen.sum()),
        },
        "distance_bin_sign_pattern": {
            "all_1_to_16_negative": bool(pre and all(x < 0 for x in pre)),
            "all_17_plus_positive": bool(post and all(x > 0 for x in post)),
        },
        "window_16": next(r for r in window_rows if r["window"] == 16),
        "notes": [
            "All analyses use frozen DEV Base/Memory outcomes; no model or policy is retrained.",
            "Window sweeps are diagnostic relabelings by distance to the last prior target-streamer interaction.",
            "Frozen relationship-horizon labels remain authoritative and are not changed by this analysis.",
        ],
    }
    (a.out_dir / "context_window_stress_report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
