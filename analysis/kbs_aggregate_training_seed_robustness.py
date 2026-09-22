from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for seed_dir in sorted(p for p in args.root.iterdir() if p.is_dir()):
        seed_txt = seed_dir.name.split("-")[-1]
        try:
            seed = int(seed_txt)
        except ValueError:
            continue
        dual_reports = list(seed_dir.rglob("dual_id_results/report.json"))
        closure_reports = list(seed_dir.rglob("seed_closure/report.json"))
        if len(dual_reports) != 1 or len(closure_reports) != 1:
            raise RuntimeError(f"seed {seed}: expected one dual and one closure report")
        dual = json.loads(dual_reports[0].read_text())
        clo = json.loads(closure_reports[0].read_text())
        mb = clo["matched_budget"]
        sel = float(dual["selective_minus_dual_delta"])
        utd = float(mb["utility_minus_difficulty"]["mean"])
        rows.append({
            "seed": seed,
            "alpha_room": float(dual["alpha_room"]),
            "base_test_ndcg10": float(dual["dual_id_test_ndcg10"]),
            "selective_test_ndcg10": float(dual["selective_dual_memory_test_ndcg10"]),
            "selective_minus_base": sel,
            "selective_ci95_low": float(dual["selective_minus_dual_ci95"][0]),
            "selective_ci95_high": float(dual["selective_minus_dual_ci95"][1]),
            "utility_minus_difficulty": utd,
            "utility_minus_difficulty_ci95_low": float(mb["utility_minus_difficulty"]["ci95_low"]),
            "utility_minus_difficulty_ci95_high": float(mb["utility_minus_difficulty"]["ci95_high"]),
            "invocation_rate": float(clo["frozen_invocation_rate"]),
        })

    df = pd.DataFrame(rows).sort_values("seed").reset_index(drop=True)
    if len(df) < 3:
        raise RuntimeError(f"expected at least 3 training seeds, found {len(df)}")
    df.to_csv(args.out_dir / "training_seed_results.csv", index=False)

    summary = {
        "experiment": "kbs_kuailive_training_seed_robustness",
        "n_seeds": int(len(df)),
        "seeds": df.seed.astype(int).tolist(),
        "selective_minus_base_mean": float(df.selective_minus_base.mean()),
        "selective_minus_base_std": float(df.selective_minus_base.std(ddof=1)),
        "selective_minus_base_min": float(df.selective_minus_base.min()),
        "selective_minus_base_all_positive": bool((df.selective_minus_base > 0).all()),
        "utility_minus_difficulty_mean": float(df.utility_minus_difficulty.mean()),
        "utility_minus_difficulty_std": float(df.utility_minus_difficulty.std(ddof=1)),
        "utility_minus_difficulty_min": float(df.utility_minus_difficulty.min()),
        "utility_minus_difficulty_all_positive": bool((df.utility_minus_difficulty > 0).all()),
        "all_selective_ci_lower_positive": bool((df.selective_ci95_low > 0).all()),
        "all_utility_vs_difficulty_ci_lower_positive": bool((df.utility_minus_difficulty_ci95_low > 0).all()),
        "claim_guardrail": "This check targets deep Base training randomness on KuaiLive. It is distinct from OOF-split, candidate-sampling, and bootstrap uncertainty.",
    }
    (args.out_dir / "training_seed_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(df.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
