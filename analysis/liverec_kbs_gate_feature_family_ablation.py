from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_predict

SEED = 20260918
EXPECTED_N = 46878
FROZEN_K = 6563
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
FEATURE_SETS = {
    "state_only": STATE_FEATURES,
    "confidence_only": CONF_FEATURES,
    "full": STATE_FEATURES + CONF_FEATURES,
}


def hgb() -> HistGradientBoostingRegressor:
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
        key = (
            score,
            -float(use.mean()),
            float(th) if np.isfinite(th) else (1e99 if th > 0 else -1e99),
        )
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


def spearman_rank_corr(a: np.ndarray, b: np.ndarray) -> float:
    ra = pd.Series(np.asarray(a, dtype=float)).rank(method="average").to_numpy(float)
    rb = pd.Series(np.asarray(b, dtype=float)).rank(method="average").to_numpy(float)
    return float(np.corrcoef(ra, rb)[0, 1])


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-oof", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-jobs", type=int, default=-1)
    ap.add_argument("--n-boot", type=int, default=5000)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()

    dev = pd.read_csv(args.dev_oof)
    required = set(
        STATE_FEATURES
        + CONF_FEATURES
        + [
            "user_id",
            "base_ndcg10",
            "memory_ndcg10",
            "memory_delta_ndcg10",
            "utility_oof_pred",
            "difficulty_oof_pred",
            "use_utility",
        ]
    )
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"missing frozen DEV columns: {missing}")
    if len(dev) != EXPECTED_N or dev.user_id.duplicated().any():
        raise RuntimeError(f"unexpected frozen DEV shape/identity: n={len(dev)}")

    base = dev.base_ndcg10.to_numpy(float)
    memory = dev.memory_ndcg10.to_numpy(float)
    y_utility = dev.memory_delta_ndcg10.to_numpy(float)
    y_difficulty = 1.0 - base
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)

    predictions = {}
    summary_rows = []
    bootstrap_inputs = []
    bootstrap_labels = []

    for family, features in FEATURE_SETS.items():
        X = dev[features].to_numpy(float)
        if not np.isfinite(X).all():
            raise RuntimeError(f"non-finite features for {family}")

        utility_pred = cross_val_predict(
            hgb(), X, y_utility, cv=cv, method="predict", n_jobs=args.n_jobs
        )
        difficulty_pred = cross_val_predict(
            hgb(), X, y_difficulty, cv=cv, method="predict", n_jobs=args.n_jobs
        )
        predictions[family] = (utility_pred, difficulty_pred)

        threshold, use_opt, _ = choose_threshold(utility_pred, base, memory)
        k_opt = int(use_opt.sum())
        selected_opt = np.where(use_opt, memory, base)

        use_u_k = top_k_mask(utility_pred, FROZEN_K)
        use_d_k = top_k_mask(difficulty_pred, FROZEN_K)
        selected_u_k = np.where(use_u_k, memory, base)
        selected_d_k = np.where(use_d_k, memory, base)

        bootstrap_inputs.extend(
            [
                selected_u_k - base,
                selected_u_k - selected_d_k,
            ]
        )
        bootstrap_labels.extend(
            [
                (family, "utility_exact_k_vs_base"),
                (family, "utility_exact_k_vs_difficulty"),
            ]
        )

        summary_rows.append(
            {
                "feature_family": family,
                "n_features": len(features),
                "features": features,
                "oof_utility_spearman": spearman_rank_corr(utility_pred, y_utility),
                "optimal_threshold": float(threshold),
                "optimal_k": k_opt,
                "optimal_invocation_rate": float(use_opt.mean()),
                "optimal_ndcg10": float(selected_opt.mean()),
                "optimal_gain_vs_base": float((selected_opt - base).mean()),
                "exact_k": int(FROZEN_K),
                "utility_exact_k_ndcg10": float(selected_u_k.mean()),
                "utility_exact_k_gain_vs_base": float((selected_u_k - base).mean()),
                "difficulty_exact_k_ndcg10": float(selected_d_k.mean()),
                "difficulty_exact_k_gain_vs_base": float((selected_d_k - base).mean()),
                "utility_minus_difficulty_exact_k": float((selected_u_k - selected_d_k).mean()),
            }
        )

    # Amortize bootstrap index generation across all feature families/comparisons.
    diff_matrix = np.column_stack(bootstrap_inputs)
    cis = bootstrap_columns(diff_matrix, SEED + 100, n_boot=args.n_boot)
    ci_lookup = {label: ci for label, ci in zip(bootstrap_labels, cis)}
    for row in summary_rows:
        fam = row["feature_family"]
        a = ci_lookup[(fam, "utility_exact_k_vs_base")]
        b = ci_lookup[(fam, "utility_exact_k_vs_difficulty")]
        row["utility_exact_k_vs_base_ci95_low"] = a["ci95_low"]
        row["utility_exact_k_vs_base_ci95_high"] = a["ci95_high"]
        row["utility_minus_difficulty_exact_k_ci95_low"] = b["ci95_low"]
        row["utility_minus_difficulty_exact_k_ci95_high"] = b["ci95_high"]

    # Reproduce the original full-feature OOF evidence before interpreting ablations.
    full_u, full_d = predictions["full"]
    original_u = dev.utility_oof_pred.to_numpy(float)
    original_d = dev.difficulty_oof_pred.to_numpy(float)
    u_diff = np.abs(full_u - original_u)
    d_diff = np.abs(full_d - original_d)
    original_mask = dev.use_utility.to_numpy(bool)
    replay_threshold, replay_mask, _ = choose_threshold(full_u, base, memory)
    guard = {
        "full_utility_pred_max_abs_diff": float(u_diff.max()),
        "full_difficulty_pred_max_abs_diff": float(d_diff.max()),
        "full_utility_pred_mean_abs_diff": float(u_diff.mean()),
        "full_difficulty_pred_mean_abs_diff": float(d_diff.mean()),
        "full_utility_mask_mismatches": int(np.count_nonzero(replay_mask != original_mask)),
        "full_recomputed_threshold": float(replay_threshold),
        "frozen_original_k": int(original_mask.sum()),
    }
    if (
        guard["full_utility_pred_max_abs_diff"] > 1e-10
        or guard["full_difficulty_pred_max_abs_diff"] > 1e-10
        or guard["full_utility_mask_mismatches"] != 0
        or guard["frozen_original_k"] != FROZEN_K
    ):
        raise RuntimeError(f"full-feature frozen OOF replay guard failed: {guard}")

    pred_out = dev[
        ["user_id", "base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10"]
    ].copy()
    for family, (u, d) in predictions.items():
        pred_out[f"{family}_utility_oof_pred"] = u
        pred_out[f"{family}_difficulty_oof_pred"] = d
        pred_out[f"{family}_utility_exact_k"] = top_k_mask(u, FROZEN_K)
        pred_out[f"{family}_difficulty_exact_k"] = top_k_mask(d, FROZEN_K)
    pred_out.to_csv(args.out_dir / "kbs_gate_feature_family_oof.csv.gz", index=False, compression="gzip")

    table = pd.DataFrame(summary_rows)
    table.to_csv(args.out_dir / "kbs_gate_feature_family_ablation.csv", index=False)

    report = {
        "experiment": "kbs_utility_gate_feature_family_ablation_dev_only",
        "test_ranking_inspected": False,
        "n_dev": int(len(dev)),
        "frozen_exact_k": int(FROZEN_K),
        "gate": (
            "HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_depth=3, "
            "min_samples_leaf=50, l2_regularization=1.0, random_state=20260918)"
        ),
        "cv": "5-fold shuffled KFold, seed 20260918; OOF only",
        "feature_sets": FEATURE_SETS,
        "full_feature_replay_guard": guard,
        "results": summary_rows,
        "runtime_seconds": float(time.perf_counter() - t0),
        "interpretation_guardrail": (
            "DEV-only journal-strengthening analysis. Family-specific thresholds are descriptive OOF results; "
            "the frozen P1.3 policy/test is not changed. Exact-K=6563 is the primary apples-to-apples ablation."
        ),
    }
    (args.out_dir / "kbs_gate_feature_family_ablation.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n"
    )
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
