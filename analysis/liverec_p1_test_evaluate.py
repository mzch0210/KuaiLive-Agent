from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

SEED = 20260918
N_BOOT = 5000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def top_k_mask(score: np.ndarray, k: int) -> np.ndarray:
    score = np.asarray(score, dtype=float)
    out = np.zeros(len(score), dtype=bool)
    if k <= 0:
        return out
    if k >= len(score):
        out[:] = True
        return out
    order = np.lexsort((np.arange(len(score)), -score))
    out[order[: int(k)]] = True
    return out


def paired_bootstrap(diff: np.ndarray, seed: int, n_boot: int = N_BOOT) -> dict:
    x = np.asarray(diff, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.isfinite(x).all():
        raise RuntimeError("Invalid bootstrap input")
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=float)
    chunk = 128
    cursor = 0
    while cursor < n_boot:
        m = min(chunk, n_boot - cursor)
        idx = rng.integers(0, len(x), size=(m, len(x)), dtype=np.int32)
        means[cursor : cursor + m] = x[idx].mean(axis=1)
        cursor += m
    return {
        "mean": float(x.mean()),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "n": int(len(x)),
        "n_boot": int(n_boot),
    }


def rank_spearman(a: np.ndarray, b: np.ndarray) -> float:
    ar = pd.Series(np.asarray(a, dtype=float)).rank(method="average").to_numpy(float)
    br = pd.Series(np.asarray(b, dtype=float)).rank(method="average").to_numpy(float)
    rho = float(np.corrcoef(ar, br)[0, 1])
    if not np.isfinite(rho):
        raise RuntimeError("Undefined frozen test utility Spearman correlation")
    return rho


def subgroup_rows(df: pd.DataFrame, col: str, seed_base: int) -> list[dict]:
    out = []
    for i, (label, g) in enumerate(df.groupby(col, observed=True, sort=False)):
        mem_diff = g.memory_ndcg10.to_numpy(float) - g.base_ndcg10.to_numpy(float)
        out.append(
            {
                "group": str(label),
                "n": int(len(g)),
                "base_ndcg10": float(g.base_ndcg10.mean()),
                "memory_ndcg10": float(g.memory_ndcg10.mean()),
                "selective_utility_ndcg10": float(g.selective_utility_ndcg10.mean()),
                "selective_difficulty_ndcg10": float(g.selective_difficulty_ndcg10.mean()),
                "memory_minus_base": paired_bootstrap(mem_diff, seed_base + i),
                "utility_invocation_rate": float(g.use_utility.mean()),
                "difficulty_invocation_rate": float(g.use_difficulty.mean()),
                "positive_memory_fraction": float((mem_diff > 0).mean()),
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-events", type=Path, required=True)
    ap.add_argument("--utility-gate", type=Path, required=True)
    ap.add_argument("--difficulty-gate", type=Path, required=True)
    ap.add_argument("--policy-manifest", type=Path, required=True)
    ap.add_argument("--test-export-summary", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    test = pd.read_csv(args.test_events)
    manifest = json.loads(args.policy_manifest.read_text())
    export_summary = json.loads(args.test_export_summary.read_text())

    if export_summary.get("policy_manifest_sha256") != sha256(args.policy_manifest):
        raise RuntimeError("Test export and evaluator policy manifest hashes differ")
    if manifest["source_p1_2"]["utility_gate_sha256"] != sha256(args.utility_gate):
        raise RuntimeError("Frozen utility gate hash mismatch")
    if manifest["difficulty_gate_sha256"] != sha256(args.difficulty_gate):
        raise RuntimeError("Frozen difficulty gate hash mismatch")

    utility_bundle = joblib.load(args.utility_gate)
    difficulty_bundle = joblib.load(args.difficulty_gate)

    if manifest.get("test_ranking_inspected") is not False:
        raise RuntimeError("Policy manifest must be frozen before test")
    if export_summary.get("test_ranking_inspected") is not True or export_summary.get("one_shot") is not True:
        raise RuntimeError("Input is not the declared one-shot P1.3 test export")
    if int(export_summary.get("n_test")) != len(test) or len(test) != 44221:
        raise RuntimeError("Unexpected P1.3 test size")
    if test.user_id.duplicated().any():
        raise RuntimeError("Expected one test target per user for paired user bootstrap")

    features = list(manifest["features"])
    if utility_bundle.get("features") != features or difficulty_bundle.get("features") != features:
        raise RuntimeError("Frozen gate feature order mismatch")
    missing = sorted(set(features + [
        "base_ndcg10",
        "memory_ndcg10",
        "base_h10",
        "memory_h10",
        "memory_delta_ndcg10",
        "relationship_horizon",
        "official_repeat",
    ]) - set(test.columns))
    if missing:
        raise RuntimeError(f"Missing P1.3 test columns: {missing}")
    if not np.isfinite(test[features + ["base_ndcg10", "memory_ndcg10", "base_h10", "memory_h10"]].to_numpy(float)).all():
        raise RuntimeError("Non-finite P1.3 evaluation inputs")

    X = test[features].to_numpy(float)
    base = test.base_ndcg10.to_numpy(float)
    memory = test.memory_ndcg10.to_numpy(float)
    base_h10 = test.base_h10.to_numpy(float)
    memory_h10 = test.memory_h10.to_numpy(float)
    realized_utility = memory - base

    utility_pred = np.asarray(utility_bundle["model"].predict(X), dtype=float)
    difficulty_pred = np.asarray(difficulty_bundle["model"].predict(X), dtype=float)
    if not np.isfinite(utility_pred).all() or not np.isfinite(difficulty_pred).all():
        raise RuntimeError("Non-finite frozen gate predictions")

    threshold = float(manifest["utility_rule"]["threshold"])
    if abs(threshold - float(utility_bundle["threshold"])) > 1e-15:
        raise RuntimeError("Utility threshold differs from frozen P1.2 bundle")
    use_utility = utility_pred > threshold
    k = int(use_utility.sum())
    use_difficulty = top_k_mask(difficulty_pred, k)
    use_oracle = top_k_mask(realized_utility, k)

    selective_utility = np.where(use_utility, memory, base)
    selective_difficulty = np.where(use_difficulty, memory, base)
    selective_oracle = np.where(use_oracle, memory, base)
    selective_utility_h10 = np.where(use_utility, memory_h10, base_h10)
    selective_difficulty_h10 = np.where(use_difficulty, memory_h10, base_h10)
    selective_oracle_h10 = np.where(use_oracle, memory_h10, base_h10)

    test_out = test.copy()
    test_out["utility_pred"] = utility_pred
    test_out["difficulty_pred"] = difficulty_pred
    test_out["use_utility"] = use_utility
    test_out["use_difficulty"] = use_difficulty
    test_out["use_oracle_exact_k"] = use_oracle
    test_out["selective_utility_ndcg10"] = selective_utility
    test_out["selective_difficulty_ndcg10"] = selective_difficulty
    test_out["selective_oracle_ndcg10"] = selective_oracle
    test_out["selective_utility_h10"] = selective_utility_h10
    test_out["selective_difficulty_h10"] = selective_difficulty_h10

    internal_edges = np.asarray(manifest["utility_strata"]["internal_cutpoints"], dtype=float)
    if internal_edges.size != 9 or not np.all(np.diff(internal_edges) > 0):
        raise RuntimeError("Invalid frozen utility-strata cutpoints")
    # qcut uses right-closed intervals; an exact cutpoint stays in the lower stratum.
    stratum_idx = np.searchsorted(internal_edges, utility_pred, side="left") + 1
    test_out["utility_stratum"] = [f"D{i}" for i in stratum_idx]

    ndcg_utility_vs_base = paired_bootstrap(selective_utility - base, SEED + 101)
    ndcg_utility_vs_difficulty = paired_bootstrap(selective_utility - selective_difficulty, SEED + 102)
    ndcg_memory_vs_base = paired_bootstrap(memory - base, SEED + 103)
    h10_utility_vs_base = paired_bootstrap(selective_utility_h10 - base_h10, SEED + 104)
    h10_utility_vs_difficulty = paired_bootstrap(selective_utility_h10 - selective_difficulty_h10, SEED + 105)

    repeat_label = np.where(test_out.official_repeat.to_numpy(bool), "repeat", "novel")
    test_out["repeat_label"] = repeat_label

    strata = []
    for label in [f"D{i}" for i in range(1, 11)]:
        g = test_out[test_out.utility_stratum == label]
        if g.empty:
            strata.append({"stratum": label, "n": 0})
            continue
        strata.append(
            {
                "stratum": label,
                "n": int(len(g)),
                "predicted_delta_mean": float(g.utility_pred.mean()),
                "realized_delta_mean": float(g.memory_delta_ndcg10.mean()),
                "base_ndcg10": float(g.base_ndcg10.mean()),
                "memory_ndcg10": float(g.memory_ndcg10.mean()),
                "selective_ndcg10": float(g.selective_utility_ndcg10.mean()),
                "positive_memory_fraction": float((g.memory_delta_ndcg10 > 0).mean()),
                "utility_invocation_rate": float(g.use_utility.mean()),
            }
        )

    base_ndcg = float(base.mean())
    memory_ndcg = float(memory.mean())
    utility_ndcg = float(selective_utility.mean())
    difficulty_ndcg = float(selective_difficulty.mean())
    oracle_ndcg = float(selective_oracle.mean())
    oracle_gain = oracle_ndcg - base_ndcg
    utility_gain = utility_ndcg - base_ndcg

    report = {
        "experiment": "liverec_twitch100k_p1_3_one_shot_test_final",
        "test_ranking_inspected": True,
        "one_shot": True,
        "n_test": int(len(test_out)),
        "policy": {
            "utility_threshold": threshold,
            "realized_test_k": k,
            "realized_invocation_rate": float(use_utility.mean()),
            "difficulty_budget_exact_match": bool(int(use_difficulty.sum()) == k),
            "oracle_budget_exact_match": bool(int(use_oracle.sum()) == k),
        },
        "ndcg10": {
            "base": base_ndcg,
            "always_memory": memory_ndcg,
            "selective_utility": utility_ndcg,
            "difficulty_exact_k": difficulty_ndcg,
            "oracle_exact_k": oracle_ndcg,
            "memory_vs_base": ndcg_memory_vs_base,
            "utility_vs_base": ndcg_utility_vs_base,
            "utility_vs_difficulty_exact_k": ndcg_utility_vs_difficulty,
        },
        "h10": {
            "base": float(base_h10.mean()),
            "always_memory": float(memory_h10.mean()),
            "selective_utility": float(selective_utility_h10.mean()),
            "difficulty_exact_k": float(selective_difficulty_h10.mean()),
            "oracle_exact_k": float(selective_oracle_h10.mean()),
            "utility_vs_base": h10_utility_vs_base,
            "utility_vs_difficulty_exact_k": h10_utility_vs_difficulty,
        },
        "oracle_headroom": {
            "gain_vs_base": float(oracle_gain),
            "utility_gain_vs_base": float(utility_gain),
            "fraction_captured": None if oracle_gain <= 0 else float(utility_gain / oracle_gain),
        },
        "predicted_vs_realized_utility_spearman": rank_spearman(utility_pred, realized_utility),
        "relationship_horizon": subgroup_rows(test_out, "relationship_horizon", SEED + 200),
        "repeat_novel": subgroup_rows(test_out, "repeat_label", SEED + 300),
        "utility_strata": strata,
        "primary_success": bool(ndcg_utility_vs_base["mean"] > 0 and ndcg_utility_vs_base["ci95_low"] > 0),
        "mechanism_replication": bool(
            ndcg_utility_vs_difficulty["mean"] > 0 and ndcg_utility_vs_difficulty["ci95_low"] > 0
        ),
        "freeze_statement": "This is the one-shot P1.3 test result. No test-based rescue tuning is permitted.",
    }

    test_out.to_csv(args.out_dir / "p1_3_test_predictions.csv.gz", index=False, compression="gzip")
    (args.out_dir / "p1_3_test_final_report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
