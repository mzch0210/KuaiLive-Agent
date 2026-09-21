from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_predict

from room_level_selective_agent import (
    CONF_FEATURES,
    USER_FEATURES,
    EPS,
    SEED,
    bootstrap_delta,
    choose_threshold,
    hgb,
)


def paired_ci(diff: np.ndarray, seed: int) -> dict:
    mean, lo, hi = bootstrap_delta(np.asarray(diff, float), seed=seed, n_boot=5000)
    return {"mean": float(mean), "ci95_low": float(lo), "ci95_high": float(hi)}


def topk_mask(score: np.ndarray, k: int) -> np.ndarray:
    score = np.asarray(score, float)
    k = int(np.clip(k, 0, len(score)))
    use = np.zeros(len(score), dtype=bool)
    if k:
        order = np.lexsort((np.arange(len(score)), -score))
        use[order[:k]] = True
    return use


def feature_matrix(df: pd.DataFrame, which: str) -> np.ndarray:
    if which == "state":
        return df[USER_FEATURES].to_numpy(float)
    if which == "confidence":
        return df[[f"native_{k}" for k in CONF_FEATURES]].to_numpy(float)
    if which == "combined":
        return np.column_stack([
            df[USER_FEATURES].to_numpy(float),
            df[[f"native_{k}" for k in CONF_FEATURES]].to_numpy(float),
        ])
    raise ValueError(which)


def fit_selective(d: pd.DataFrame, t: pd.DataFrame, which: str, seed_offset: int):
    Xd = feature_matrix(d, which)
    Xt = feature_matrix(t, which)
    yd = (d.memory_ndcg10 - d.native_base_ndcg10).to_numpy(float)
    base_d = d.native_base_ndcg10.to_numpy(float)
    mem_d = d.memory_ndcg10.to_numpy(float)
    base_t = t.native_base_ndcg10.to_numpy(float)
    mem_t = t.memory_ndcg10.to_numpy(float)
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(hgb(), Xd, yd, cv=cv, method="predict", n_jobs=1)
    th, use_d, dev_sel = choose_threshold(oof, base_d, mem_d)
    model = clone(hgb()).fit(Xd, yd)
    pred = model.predict(Xt)
    use_t = pred > th
    sel = np.where(use_t, mem_t, base_t)
    ci = paired_ci(sel - base_t, SEED + seed_offset)
    return {
        "name": f"{which}_HGB",
        "dev_oof_ndcg10": float(dev_sel),
        "threshold": float(th),
        "dev_invocation_rate": float(use_d.mean()),
        "test_ndcg10": float(sel.mean()),
        "delta_vs_base": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
        "test_invocation_rate": float(use_t.mean()),
        "selected_n": int(use_t.sum()),
    }


def history_threshold(d: pd.DataFrame, t: pd.DataFrame):
    base_d = d.native_base_ndcg10.to_numpy(float)
    mem_d = d.memory_ndcg10.to_numpy(float)
    base_t = t.native_base_ndcg10.to_numpy(float)
    mem_t = t.memory_ndcg10.to_numpy(float)
    pred_d = d.log_history_len.to_numpy(float)
    pred_t = t.log_history_len.to_numpy(float)
    th, use_d, dev_sel = choose_threshold(pred_d, base_d, mem_d)
    use_t = pred_t > th
    sel = np.where(use_t, mem_t, base_t)
    ci = paired_ci(sel - base_t, SEED + 1501)
    return {
        "name": "history_threshold",
        "dev_oof_ndcg10": float(dev_sel),
        "threshold": float(th),
        "dev_invocation_rate": float(use_d.mean()),
        "test_ndcg10": float(sel.mean()),
        "delta_vs_base": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
        "test_invocation_rate": float(use_t.mean()),
        "selected_n": int(use_t.sum()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-active-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    d = pd.read_csv(args.full_active_dir / "per_user_dev_full_active.csv.gz").sort_values("user_id").reset_index(drop=True)
    t = pd.read_csv(args.full_active_dir / "per_user_test_full_active.csv.gz").sort_values("user_id").reset_index(drop=True)
    primary_report = json.loads((args.full_active_dir / "report.json").read_text())

    base_t = t.native_base_ndcg10.to_numpy(float)
    mem_t = t.memory_ndcg10.to_numpy(float)
    realized = mem_t - base_t
    pred_utility = t.native_pred_delta.to_numpy(float)
    frozen_use = t.native_use_memory.astype(bool).to_numpy()
    frozen_sel = np.where(frozen_use, mem_t, base_t)
    k = int(frozen_use.sum())

    # Utility stratification.
    tmp = pd.DataFrame({
        "user_id": t.user_id.astype(int),
        "predicted_relative_utility": pred_utility,
        "realized_relative_utility": realized,
        "base_ndcg10": base_t,
        "memory_ndcg10": mem_t,
        "native_use_memory": frozen_use,
    })
    rank = pd.Series(pred_utility).rank(method="first")
    tmp["utility_decile"] = pd.qcut(rank, 10, labels=False) + 1
    deciles = tmp.groupby("utility_decile", as_index=False).agg(
        n=("user_id", "size"),
        predicted_utility_mean=("predicted_relative_utility", "mean"),
        realized_utility_mean=("realized_relative_utility", "mean"),
        positive_realized_fraction=("realized_relative_utility", lambda x: float((x > 0).mean())),
        base_ndcg10=("base_ndcg10", "mean"),
        memory_ndcg10=("memory_ndcg10", "mean"),
        invocation_fraction=("native_use_memory", "mean"),
    )
    deciles.to_csv(args.out_dir / "utility_deciles.csv", index=False)
    rho, rho_p = spearmanr(pred_utility, realized)

    # Difficulty comparator at exact native K.
    Xd = feature_matrix(d, "combined")
    Xt = feature_matrix(t, "combined")
    difficulty_target = 1.0 - d.native_base_ndcg10.to_numpy(float)
    difficulty_model = clone(hgb()).fit(Xd, difficulty_target)
    difficulty_pred = difficulty_model.predict(Xt)
    difficulty_use = topk_mask(difficulty_pred, k)
    difficulty_sel = np.where(difficulty_use, mem_t, base_t)
    difficulty_ci = paired_ci(difficulty_sel - base_t, SEED + 1601)
    utility_ci = paired_ci(frozen_sel - base_t, SEED + 1602)
    utility_vs_difficulty = paired_ci(frozen_sel - difficulty_sel, SEED + 1603)

    # Oracle exact-K and unrestricted.
    oracle_k_use = topk_mask(realized, k)
    oracle_k_sel = np.where(oracle_k_use, mem_t, base_t)
    oracle_k_gain = float((oracle_k_sel - base_t).mean())
    oracle_any_use = realized > 0
    oracle_any_sel = np.where(oracle_any_use, mem_t, base_t)
    oracle_any_gain = float((oracle_any_sel - base_t).mean())

    matched = pd.DataFrame([
        {"router": "full_active_native_utility_HGB", "k": k, "rate": k / len(t), "ndcg10": float(frozen_sel.mean()), "gain_vs_base": utility_ci["mean"]},
        {"router": "full_active_base_difficulty_HGB_exactK", "k": k, "rate": k / len(t), "ndcg10": float(difficulty_sel.mean()), "gain_vs_base": difficulty_ci["mean"]},
        {"router": "oracle_relative_utility_exactK", "k": k, "rate": k / len(t), "ndcg10": float(oracle_k_sel.mean()), "gain_vs_base": oracle_k_gain},
    ])
    matched.to_csv(args.out_dir / "matched_budget_routing.csv", index=False)

    # Budget curve.
    rows = []
    for frac in sorted(set([0.0, *np.linspace(0.05, 1.0, 20).tolist(), k / len(t), 1.0])):
        kk = int(round(frac * len(t)))
        um = topk_mask(pred_utility, kk)
        om = topk_mask(realized, kk)
        us = np.where(um, mem_t, base_t)
        os = np.where(om, mem_t, base_t)
        rows.append({
            "budget_fraction": kk / len(t), "k": kk,
            "utility_router_ndcg10": float(us.mean()),
            "utility_router_gain": float((us-base_t).mean()),
            "oracle_ndcg10": float(os.mean()),
            "oracle_gain": float((os-base_t).mean()),
        })
    pd.DataFrame(rows).drop_duplicates("k").sort_values("k").to_csv(args.out_dir / "utility_budget_oracle_curve.csv", index=False)

    # Information-source ablation under full-active native protocol.
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    ablations = [history_threshold(d, t)]
    ablations.append(fit_selective(d, t, "state", 1701))
    ablations.append(fit_selective(d, t, "confidence", 1702))
    ablations.append(fit_selective(d, t, "combined", 1703))
    ablations.append({
        "name": "combined_HGB_frozen_full_active_native",
        "dev_oof_ndcg10": float(primary_report["A2_full_active_native"]["dev_oof_selective_ndcg10"]),
        "threshold": float(primary_report["A2_full_active_native"]["threshold_dev_selected"]),
        "dev_invocation_rate": float(primary_report["A2_full_active_native"]["dev_oof_invocation_rate"]),
        "test_ndcg10": float(frozen_sel.mean()),
        "delta_vs_base": utility_ci["mean"],
        "ci95_low": utility_ci["ci95_low"],
        "ci95_high": utility_ci["ci95_high"],
        "test_invocation_rate": float(frozen_use.mean()),
        "selected_n": k,
    })
    pd.DataFrame(ablations).to_csv(args.out_dir / "full_active_information_ablation.csv", index=False)

    tmp["difficulty_pred"] = difficulty_pred
    tmp["difficulty_use_exactK"] = difficulty_use
    tmp["oracle_use_exactK"] = oracle_k_use
    tmp.to_csv(args.out_dir / "per_user_analysis.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "full_active_conditional_utility_closure",
        "users": int(len(t)),
        "base_ndcg10": float(base_t.mean()),
        "memory_ndcg10": float(mem_t.mean()),
        "selective_ndcg10": float(frozen_sel.mean()),
        "invocation_rate": float(k / len(t)),
        "calibration": {
            "spearman_predicted_vs_realized": float(rho),
            "spearman_pvalue": float(rho_p),
            "bottom_decile_realized_utility": float(deciles.iloc[0].realized_utility_mean),
            "top_decile_realized_utility": float(deciles.iloc[-1].realized_utility_mean),
            "bottom_decile_positive_fraction": float(deciles.iloc[0].positive_realized_fraction),
            "top_decile_positive_fraction": float(deciles.iloc[-1].positive_realized_fraction),
        },
        "matched_budget": {
            "k": k,
            "utility_router_gain_vs_base": utility_ci,
            "difficulty_router_gain_vs_base": difficulty_ci,
            "utility_minus_difficulty": utility_vs_difficulty,
            "oracle_exact_k_gain_vs_base": oracle_k_gain,
            "fraction_oracle_exact_k_gain_captured": float(utility_ci["mean"] / oracle_k_gain) if abs(oracle_k_gain) > EPS else None,
        },
        "oracle_unrestricted": {
            "positive_delta_fraction": float(oracle_any_use.mean()),
            "gain_vs_base": oracle_any_gain,
            "ndcg10": float(oracle_any_sel.mean()),
            "fraction_unrestricted_oracle_gain_captured": float(utility_ci["mean"] / oracle_any_gain) if abs(oracle_any_gain) > EPS else None,
        },
        "guardrail": "All full-active closure models are fit/thresholded from full-active dev only. The difficulty comparator uses the identical combined feature set and exact test invocation budget as the native utility router.",
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("\nInformation ablation:\n", pd.DataFrame(ablations).to_string(index=False))
    print("\nMatched budget:\n", matched.to_string(index=False))


if __name__ == "__main__":
    main()
