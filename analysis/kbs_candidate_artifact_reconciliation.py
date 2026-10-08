"""Read-only paired audit of previously frozen per-user scores (no new model evaluation).

Source scores may use DIFFERENT checkpoint pairs. This is provenance reconciliation,
NOT a fixed-checkpoint candidate manipulation or a new untouched test.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

def read_unique(path: Path, required: list[str]) -> pd.DataFrame:
    frame = pd.read_csv(path)
    absent = sorted(set(required) - set(frame.columns))
    if absent:
        raise ValueError(f"{path}: missing required columns {absent}")
    if frame.user_id.isna().any() or frame.user_id.duplicated().any():
        raise ValueError(f"{path}: nonunique or missing user_id")
    return frame.sort_values("user_id").reset_index(drop=True)

def profile(df: pd.DataFrame, b: str, m: str) -> dict:
    base = df[b].to_numpy(dtype=float)
    mem = df[m].to_numpy(dtype=float)
    if not (np.isfinite(base).all() and np.isfinite(mem).all()):
        raise ValueError("Nonfinite ranking scores")
    if not (np.logical_and(base >= 0, base <= 1).all() and
            np.logical_and(mem >= 0, mem <= 1).all()):
        raise ValueError("NDCG@10 outside [0,1]")
    return {
        "n": int(len(df)), "base_ndcg10": float(np.mean(base)),
        "memory_ndcg10": float(np.mean(mem)),
        "memory_minus_base": float(np.mean(mem - base)),
    }

def reconcile(seed: pd.DataFrame, full: pd.DataFrame) -> dict:
    seed = read_unique(seed, ["user_id", "dual_score10", "MemoryFusion_score10"])
    full = read_unique(full, [
        "user_id", "native_base_ndcg10", "transfer_base_ndcg10", "memory_ndcg10",
    ])
    ids0 = set(seed.user_id.tolist())
    ids1 = set(full.user_id.tolist())
    if ids0 != ids1:
        raise ValueError(
            f"Different user cohort: seed_only={len(ids0-ids1)} full_only={len(ids1-ids0)}"
        )
    z = seed[["user_id", "dual_score10", "MemoryFusion_score10"]].merge(
        full[["user_id", "native_base_ndcg10", "transfer_base_ndcg10", "memory_ndcg10"]],
        on="user_id", how="inner", validate="one_to_one"
    )
    d = z.MemoryFusion_score10.to_numpy(float) - z.memory_ndcg10.to_numpy(float)
    out = {
        "analysis_kind": "CROSS_CHECKPOINT_RECONCILIATION_NOT_FIXED_CHECKPOINT_EFFECT",
        "paired_users": int(len(z)),
        "seed_sampled": profile(z, "dual_score10", "MemoryFusion_score10"),
        "full_active_native": profile(z, "native_base_ndcg10", "memory_ndcg10"),
        "full_active_transfer": profile(z, "transfer_base_ndcg10", "memory_ndcg10"),
        "memory_score_comparability": {
            "max_absolute_paired_difference": float(np.max(np.abs(d))),
            "mean_signed_difference": float(np.mean(d)),
            "all_exactly_equal": bool(np.array_equal(
                z.MemoryFusion_score10.to_numpy(float), z.memory_ndcg10.to_numpy(float)
            )),
        },
        "provenance_constraint": (
            "Sampled seed and full-active Dual-ID outputs do not establish identical "
            "model checkpoint hashes. No paired difference here is a fixed-checkpoint "
            "candidate effect. Each comparison must retain its source run label."
        ),
        "sources": {
            "seed_sampled": "run 35729896175, artifact seed-20260918",
            "full_active": "run 35580324870, artifact full-active-dual-id-35580324870",
        },
    }
    return out

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed-csv",type=Path,required=True)
    ap.add_argument("--full-csv",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    res=reconcile(args.seed_csv,args.full_csv)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(res,indent=2)+"\n")
    print(json.dumps(res,indent=2))

if __name__=="__main__":
    main()
