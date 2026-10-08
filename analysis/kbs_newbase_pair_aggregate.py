"""Paired KuaiLive diagnostic aggregation for fixed newly trained Dual-ID base.

Post-hoc assessment: statistics are descriptive, never used to select a new gate,
Base combination coefficient, or target-based calibration. NumPy / pandas only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

METRICS = ("ndcg10", "hr10")
STATES = ("represented", "recoverable", "unavailable")
BOOT_SEED = 20261008


def _bootstrap(x: np.ndarray, n_boot: int, seed: int) -> dict:
    v = np.asarray(x, dtype=np.float64)
    if v.ndim != 1 or not len(v) or not np.isfinite(v).all():
        raise ValueError("Bootstrap requires nonempty finite 1D values")
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=np.float64)
    for b in range(n_boot):
        means[b] = v[rng.integers(0, len(v), len(v))].mean()
    return {"mean": float(v.mean()), "ci95": [float(np.quantile(means, .025)),
                                             float(np.quantile(means, .975))],
            "n": len(v)}


def aggregate(df: pd.DataFrame, n_boot: int = 5000, seed: int = BOOT_SEED) -> dict:
    keys = ["user_id", "time", "target_item"]
    required = set(keys + ["state", "sampled_candidates", "full_candidates",
                           "target_metadata_active"])
    for metric in METRICS:
        for regime in ("sampled", "full"):
            for predictor in ("base", "memory"):
                required.add(f"{regime}_{predictor}_{metric}")
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if df[keys].isna().any().any() or df.duplicated(keys).any() or df.user_id.duplicated().any():
        raise ValueError("Each user–time–target must appear exactly once")
    if not (df.sampled_candidates == 575).all():
        raise ValueError("The frozen sampled candidate size is not 575")
    if not (df.full_candidates >= 1).all() or not (df.full_candidates > 0).all():
        raise ValueError("Empty full-active candidate set")
    if not df.state.isin(STATES).all():
        raise ValueError("Unknown evidence-state label")
    for metric in METRICS:
        for regime in ("sampled", "full"):
            for predictor in ("base", "memory"):
                a = df[f"{regime}_{predictor}_{metric}"].to_numpy(float)
                if not np.isfinite(a).all() or ((a < 0) | (a > 1)).any():
                    raise ValueError(f"Invalid ranking metric {regime}/{predictor}/{metric}")
    result = {
        "kind": "POSTHOC_NEW_FIXED_CHECKPOINT_CANDIDATE_REGIME",
        "paired_user_target_events": int(len(df)),
        "candidate_sizes": {
            "sampled": 575,
            "full_mean": float(df.full_candidates.mean()),
            "full_median": float(df.full_candidates.median()),
            "full_min": int(df.full_candidates.min()),
            "full_max": int(df.full_candidates.max()),
            "metadata_target_fallbacks": int((~df.target_metadata_active.astype(bool)).sum()),
        },
        "metrics": {},
        "confidence_intervals": "user-paired percentile bootstrap; descriptive post-hoc",
        "bootstraps": n_boot,
        "no_training_or_selection_on_test": True,
    }
    n = len(df)
    for metric in METRICS:
        sampled_base = df[f"sampled_base_{metric}"].to_numpy(float)
        sampled_memory = df[f"sampled_memory_{metric}"].to_numpy(float)
        full_base = df[f"full_base_{metric}"].to_numpy(float)
        full_memory = df[f"full_memory_{metric}"].to_numpy(float)
        db = full_base - sampled_base
        dm = full_memory - sampled_memory
        sampled = sampled_memory - sampled_base
        full = full_memory - full_base
        shift = full - sampled
        if not np.allclose(shift, dm - db, atol=1e-12, rtol=0):
            raise AssertionError("Base/Memory identity failed")
        global_stats = {
            "sampled_base": float(sampled_base.mean()),
            "sampled_memory": float(sampled_memory.mean()),
            "full_base": float(full_base.mean()),
            "full_memory": float(full_memory.mean()),
            "sampled_memory_minus_base": _bootstrap(sampled, n_boot, seed),
            "full_memory_minus_base": _bootstrap(full, n_boot, seed + 1),
            "full_minus_sampled_relative_utility": _bootstrap(shift, n_boot, seed + 2),
            "memory_full_minus_sampled": float(dm.mean()),
            "base_full_minus_sampled": float(db.mean()),
            "states": {},
        }
        reconstruction_sampled = 0.
        reconstruction_full = 0.
        reconstruction_shift = 0.
        for i, state in enumerate(STATES):
            take = (df.state.to_numpy() == state)
            if not take.any():
                global_stats["states"][state] = {"n": 0, "prevalence": 0.}
                continue
            p = float(take.mean())
            summary = {
                "n": int(take.sum()), "prevalence": p,
                "sampled": _bootstrap(sampled[take], n_boot, seed + 100 + i),
                "full": _bootstrap(full[take], n_boot, seed + 200 + i),
                "full_minus_sampled": _bootstrap(shift[take], n_boot, seed + 300 + i),
                "sampled_weighted_contribution": float(p * sampled[take].mean()),
                "full_weighted_contribution": float(p * full[take].mean()),
            }
            reconstruction_sampled += summary["sampled_weighted_contribution"]
            reconstruction_full += summary["full_weighted_contribution"]
            reconstruction_shift += p * shift[take].mean()
            global_stats["states"][state] = summary
        err = max(abs(reconstruction_sampled - sampled.mean()),
                  abs(reconstruction_full - full.mean()),
                  abs(reconstruction_shift - shift.mean()))
        if err > 1e-12:
            raise AssertionError(f"Weighted state decomposition error: {err}")
        global_stats["state_reconstruction_error"] = err
        result["metrics"][metric] = global_stats
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pairs", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--n-boot", type=int, default=5000)
    args = p.parse_args()
    if args.n_boot < 100 or args.n_boot > 20000:
        raise ValueError("n_boot must be 100..20000")
    df = pd.read_csv(args.pairs)
    out = aggregate(df, n_boot=args.n_boot)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"paired_users": out["paired_user_target_events"],
                      "delta_ndcg": out["metrics"]["ndcg10"]["full_minus_sampled_relative_utility"],
                      "decomposition_error": out["metrics"]["ndcg10"]["state_reconstruction_error"]}, indent=2))


if __name__ == "__main__":
    main()
