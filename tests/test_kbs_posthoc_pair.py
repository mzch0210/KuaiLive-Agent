"""Synthetic data unit tests for post-hoc paired ranking inference."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))

import numpy as np
import pandas as pd

from kbs_newbase_pair_aggregate import aggregate


def toy():
    vals = [
        (1, "represented", 0.7, 0.6, 0.4, 0.5),
        (2, "represented", 0.3, 0.5, 0.2, 0.3),
        (3, "recoverable", 0.2, 0.9, 0.15, 0.8),
        (4, "unavailable", 0.8, 0.1, 0.4, 0.2),
    ]
    records = []
    for uid, state, sb, sm, fb, fm in vals:
        row = {
            "user_id": uid, "time": 1700000 + uid, "target_item": uid + 10,
            "state": state, "sampled_candidates": 575, "full_candidates": 800 + uid,
            "target_metadata_active": True,
        }
        for metric in ("ndcg10", "hr10"):
            for prefix, a, b in (("sampled", sb, sm), ("full", fb, fm)):
                row[f"{prefix}_base_{metric}"] = a
                row[f"{prefix}_memory_{metric}"] = b
        records.append(row)
    return pd.DataFrame(records)


def main():
    df = toy()
    a = aggregate(df, n_boot=100, seed=123)
    b = aggregate(df, n_boot=100, seed=123)
    assert a == b, "User bootstrap must be deterministic"
    x = a["metrics"]["ndcg10"]
    expected = (df.full_memory_ndcg10 - df.full_base_ndcg10) - (
        df.sampled_memory_ndcg10 - df.sampled_base_ndcg10)
    assert np.isclose(x["full_minus_sampled_relative_utility"]["mean"], expected.mean())
    assert x["state_reconstruction_error"] < 1e-12
    assert sum(z["n"] for z in x["states"].values()) == 4
    for broken in [pd.concat([df, df.iloc[[0]]], ignore_index=True),
                   df.assign(sampled_candidates=576),
                   df.assign(state="future")]:
        try:
            aggregate(broken, n_boot=100, seed=123)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid input was not rejected")
    print("KBS synthetic paired-aggregation test PASS")


if __name__ == "__main__":
    main()
