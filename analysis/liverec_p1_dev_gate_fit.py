from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict

SEED = 20260918
STATE_FEATURES = [
    "log_history_len",
    "repeat_rate",
    "preference_entropy",
    "preference_drift",
    "time_regularity",
    "state_complexity",
]
CONF_FEATURES = [
    "base_score_std",
    "base_score_range",
    "base_margin12",
    "base_margin15",
    "base_margin1011",
    "base_top1_z",
    "base_entropy",
    "base_top10_mass",
]
FEATURES = STATE_FEATURES + CONF_FEATURES


def hgb():
    return HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=50,
        l2_regularization=1.0,
        random_state=SEED,
    )


def choose_threshold(pred: np.ndarray, base: np.ndarray, memory: np.ndarray):
    pred = np.asarray(pred, dtype=float)
    qs = np.unique(np.quantile(pred, np.linspace(0.0, 1.0, 201)))
    thresholds = np.r_[np.inf, qs, -np.inf]
    best = None
    for th in thresholds:
        use = pred > th
        score = float(np.where(use, memory, base).mean())
        key = (score, -float(use.mean()), float(th) if np.isfinite(th) else (1e99 if th > 0 else -1e99))
        if best is None or key > best[0]:
            best = (key, float(th), use.copy())
    return best[1], best[2], float(best[0][0])


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


def paired_bootstrap(diff: np.ndarray, seed: int, n_boot: int = 5000):
    x = np.asarray(diff, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(x)
    means = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        means[i] = x[rng.integers(0, n, n)].mean()
    return {
        "mean": float(x.mean()),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "n": int(n),
        "n_boot": int(n_boot),
    }


def subgroup_table(df: pd.DataFrame, col: str) -> list[dict]:
    out = []
    for label, g in df.groupby(col, observed=True, sort=False):
        out.append(
            {
                "group": str(label),
                "n": int(len(g)),
                "base_ndcg10": float(g.base_ndcg10.mean()),
                "memory_ndcg10": float(g.memory_ndcg10.mean()),
                "memory_minus_base": float(g.memory_delta_ndcg10.mean()),
                "positive_memory_fraction": float((g.memory_delta_ndcg10 > 0).mean()),
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-events", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    dev = pd.read_csv(args.dev_events)
    required = set(FEATURES + ["base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10", "user_id"])
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"missing required columns: {missing}")
    if dev.user_id.duplicated().any():
        raise RuntimeError("Expected one dev event per user for paired user bootstrap")
    if not np.isfinite(dev[FEATURES + ["base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10"]].to_numpy(float)).all():
        raise RuntimeError("Non-finite input to P1.2 gate fitting")

    X = dev[FEATURES].to_numpy(float)
    y_utility = dev.memory_delta_ndcg10.to_numpy(float)
    y_difficulty = 1.0 - dev.base_ndcg10.to_numpy(float)
    base = dev.base_ndcg10.to_numpy(float)
    memory = dev.memory_ndcg10.to_numpy(float)

    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    utility_oof = cross_val_predict(hgb(), X, y_utility, cv=cv, method="predict", n_jobs=-1)
    difficulty_oof = cross_val_predict(hgb(), X, y_difficulty, cv=cv, method="predict", n_jobs=-1)

    threshold, use_utility, utility_score = choose_threshold(utility_oof, base, memory)
    k = int(use_utility.sum())
    use_difficulty = top_k_mask(difficulty_oof, k)
    use_oracle = top_k_mask(y_utility, k)

    selected_utility = np.where(use_utility, memory, base)
    selected_difficulty = np.where(use_difficulty, memory, base)
    selected_oracle = np.where(use_oracle, memory, base)

    utility_vs_base = paired_bootstrap(selected_utility - base, SEED + 1)
    utility_vs_difficulty = paired_bootstrap(selected_utility - selected_difficulty, SEED + 2)
    memory_vs_base = paired_bootstrap(memory - base, SEED + 3)

    pred_rank = pd.Series(utility_oof).rank(method="average").to_numpy(float)
    real_rank = pd.Series(y_utility).rank(method="average").to_numpy(float)
    spearman = float(np.corrcoef(pred_rank, real_rank)[0, 1])

    dev_out = dev.copy()
    dev_out["utility_oof_pred"] = utility_oof
    dev_out["difficulty_oof_pred"] = difficulty_oof
    dev_out["use_utility"] = use_utility
    dev_out["use_difficulty"] = use_difficulty
    dev_out["use_oracle_exact_k"] = use_oracle
    dev_out["selective_utility_ndcg10"] = selected_utility
    dev_out["selective_difficulty_ndcg10"] = selected_difficulty

    try:
        dev_out["utility_decile"] = pd.qcut(
            dev_out.utility_oof_pred, 10, labels=[f"D{i}" for i in range(1, 11)], duplicates="drop"
        )
    except ValueError:
        dev_out["utility_decile"] = "all"
    strata = []
    for label, g in dev_out.groupby("utility_decile", observed=True, sort=False):
        strata.append(
            {
                "stratum": str(label),
                "n": int(len(g)),
                "predicted_delta_mean": float(g.utility_oof_pred.mean()),
                "realized_delta_mean": float(g.memory_delta_ndcg10.mean()),
                "positive_memory_fraction": float((g.memory_delta_ndcg10 > 0).mean()),
            }
        )

    final_model = hgb().fit(X, y_utility)
    joblib.dump(
        {
            "model": final_model,
            "features": FEATURES,
            "threshold": float(threshold),
            "invocation_k_on_dev": k,
            "dev_n": int(len(dev)),
            "seed": SEED,
        },
        args.out_dir / "p1_2_frozen_utility_gate.joblib",
        compress=3,
    )

    dev_out.to_csv(args.out_dir / "p1_2_dev_oof_predictions.csv.gz", index=False, compression="gzip")
    report = {
        "experiment": "liverec_twitch100k_p1_2_dev_gate_freeze",
        "test_ranking_inspected": False,
        "features": FEATURES,
        "gate": "HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_depth=3, min_samples_leaf=50, l2_regularization=1.0)",
        "cv": "5-fold shuffled KFold, seed 20260918; all policy estimates below use OOF predictions",
        "base_ndcg10": float(base.mean()),
        "always_memory_ndcg10": float(memory.mean()),
        "memory_minus_base": memory_vs_base,
        "utility_router": {
            "threshold": float(threshold),
            "k": k,
            "invocation_rate": float(use_utility.mean()),
            "ndcg10": float(selected_utility.mean()),
            "vs_base": utility_vs_base,
        },
        "difficulty_router_exact_k": {
            "k": k,
            "invocation_rate": float(use_difficulty.mean()),
            "ndcg10": float(selected_difficulty.mean()),
        },
        "utility_minus_difficulty_exact_k": utility_vs_difficulty,
        "oracle_exact_k": {
            "ndcg10": float(selected_oracle.mean()),
            "gain_vs_base": float((selected_oracle - base).mean()),
        },
        "predicted_vs_realized_utility_spearman": spearman,
        "relationship_horizon": subgroup_table(dev_out, "relationship_horizon"),
        "repeat_novel": subgroup_table(dev_out.assign(repeat_label=np.where(dev_out.official_repeat, "repeat", "novel")), "repeat_label"),
        "utility_strata": strata,
        "freeze_rule": "Do not alter MemoryFusion weights, gate family/features, threshold rule, or matched-budget control after this dev-only freeze. P1.3 test remains one-shot.",
    }
    (args.out_dir / "p1_2_dev_gate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
