from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_val_predict

from dual_id_room_baseline import aligned_vectors, evaluate_vectors
from room_level_selective_agent import (
    CONF_FEATURES,
    USER_FEATURES,
    EPS,
    SEED,
    bootstrap_delta,
    choose_threshold,
    hgb,
    load_data,
    popularity_by_streamer,
    score_memory,
    user_features,
)


def paired_ci(diff: np.ndarray, seed: int) -> dict:
    mean, lo, hi = bootstrap_delta(np.asarray(diff, float), seed=seed, n_boot=5000)
    return {"mean": float(mean), "ci95_low": float(lo), "ci95_high": float(hi)}


def reconstruct_dev(args):
    train, dev, _test, item_to_streamer = load_data(args.room_data_dir, args.n_neg)
    streamer_map = pd.read_csv(args.streamer_data_dir / "streamer_item_map.tsv", sep="\t")
    streamer_to_item = dict(
        zip(streamer_map.streamer_id.astype(int), streamer_map.item_id.astype(int))
    )
    dv = aligned_vectors(
        dev,
        args.room_dev,
        args.streamer_dev,
        item_to_streamer,
        streamer_to_item,
        args.n_neg,
    )

    # Reproduce the frozen dev-only Dual-ID alpha selection.
    best = None
    for alpha in np.linspace(0.0, 1.0, 41):
        z = evaluate_vectors(dv, float(alpha), False)
        score = float(z.dual_score10.mean())
        key = (score, float(alpha))  # ties prefer more room weight, as in frozen run
        if best is None or key > best[0]:
            best = (key, float(alpha))
    alpha = best[1]
    base_dev = evaluate_vectors(dv, alpha, True)

    pop = popularity_by_streamer(train, item_to_streamer)
    mem_dev = score_memory(dev, train, pop, args.n_neg, item_to_streamer)
    feat_dev = user_features(train, item_to_streamer)
    d = base_dev.merge(mem_dev, on="user_id", validate="one_to_one").merge(
        feat_dev, on="user_id", validate="one_to_one"
    )
    d["MemoryFusion_delta"] = d.MemoryFusion_score10 - d.dual_score10
    return d.sort_values("user_id").reset_index(drop=True), alpha


def topk_mask(score: np.ndarray, k: int) -> np.ndarray:
    score = np.asarray(score, float)
    k = int(np.clip(k, 0, len(score)))
    use = np.zeros(len(score), dtype=bool)
    if k:
        order = np.lexsort((np.arange(len(score)), -score))
        use[order[:k]] = True
    return use


def eval_model_gate(name, d, t, features, cv, seed_offset):
    Xd = d[features].to_numpy(float)
    Xt = t[features].to_numpy(float)
    yd = d.MemoryFusion_delta.to_numpy(float)
    base_d = d.dual_score10.to_numpy(float)
    mem_d = d.MemoryFusion_score10.to_numpy(float)
    base_t = t.dual_score10.to_numpy(float)
    mem_t = t.MemoryFusion_score10.to_numpy(float)

    oof = cross_val_predict(hgb(), Xd, yd, cv=cv, method="predict", n_jobs=1)
    th, use_d, dev_score = choose_threshold(oof, base_d, mem_d)
    model = clone(hgb()).fit(Xd, yd)
    pred = model.predict(Xt)
    use_t = pred > th
    selected = np.where(use_t, mem_t, base_t)
    ci = paired_ci(selected - base_t, SEED + seed_offset)
    return {
        "name": name,
        "features": "+".join(features),
        "dev_oof_ndcg10": float(dev_score),
        "dev_invocation_rate": float(use_d.mean()),
        "threshold": float(th),
        "test_ndcg10": float(selected.mean()),
        "test_delta_vs_dual": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
        "test_invocation_rate": float(use_t.mean()),
        "selected_n": int(use_t.sum()),
    }


def history_threshold_gate(d, t):
    base_d = d.dual_score10.to_numpy(float)
    mem_d = d.MemoryFusion_score10.to_numpy(float)
    base_t = t.dual_score10.to_numpy(float)
    mem_t = t.MemoryFusion_score10.to_numpy(float)
    pdv = d.log_history_len.to_numpy(float)
    ptest = t.log_history_len.to_numpy(float)
    th, use_d, dev_score = choose_threshold(pdv, base_d, mem_d)
    use_t = ptest > th
    selected = np.where(use_t, mem_t, base_t)
    ci = paired_ci(selected - base_t, SEED + 811)
    return {
        "name": "history_threshold",
        "features": "log_history_len",
        "dev_oof_ndcg10": float(dev_score),
        "dev_invocation_rate": float(use_d.mean()),
        "threshold": float(th),
        "test_ndcg10": float(selected.mean()),
        "test_delta_vs_dual": ci["mean"],
        "ci95_low": ci["ci95_low"],
        "ci95_high": ci["ci95_high"],
        "test_invocation_rate": float(use_t.mean()),
        "selected_n": int(use_t.sum()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room-data-dir", type=Path, required=True)
    ap.add_argument("--streamer-data-dir", type=Path, required=True)
    ap.add_argument("--room-dev", type=Path, required=True)
    ap.add_argument("--streamer-dev", type=Path, required=True)
    ap.add_argument("--reference-report", type=Path, required=True)
    ap.add_argument("--reference-test", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--n-neg", type=int, default=574)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    d, alpha = reconstruct_dev(args)
    t = pd.read_csv(args.reference_test).sort_values("user_id").reset_index(drop=True)
    required = {
        "user_id", "dual_score10", "MemoryFusion_score10", "primary_pred_delta",
        "primary_use_memory", "selective_score10", *USER_FEATURES, *CONF_FEATURES,
    }
    missing = sorted(required - set(t.columns))
    if missing:
        raise ValueError(f"reference test missing columns: {missing}")

    ref = json.loads(args.reference_report.read_text())
    if abs(float(ref["alpha_room"]) - float(alpha)) > 1e-12:
        raise SystemExit(f"Dual-ID alpha reproduction failed: {alpha} vs {ref['alpha_room']}")

    base_t = t.dual_score10.to_numpy(float)
    mem_t = t.MemoryFusion_score10.to_numpy(float)
    realized = mem_t - base_t
    pred_utility = t.primary_pred_delta.to_numpy(float)
    frozen_use = t.primary_use_memory.astype(bool).to_numpy()
    frozen_selected = t.selective_score10.to_numpy(float)
    if not np.array_equal(np.where(frozen_use, mem_t, base_t), frozen_selected):
        raise SystemExit("Frozen HGB mask and selective score are inconsistent")

    # P0-B1: utility calibration / heterogeneity.
    tmp = pd.DataFrame({
        "user_id": t.user_id.astype(int),
        "predicted_relative_utility": pred_utility,
        "realized_relative_utility": realized,
        "base_ndcg10": base_t,
        "memory_ndcg10": mem_t,
        "frozen_use_memory": frozen_use,
    })
    # Rank-first gives deterministic equal-sized bins even when tree predictions tie.
    rank = pd.Series(pred_utility).rank(method="first")
    tmp["utility_decile"] = pd.qcut(rank, 10, labels=False) + 1
    deciles = tmp.groupby("utility_decile", as_index=False).agg(
        n=("user_id", "size"),
        predicted_utility_mean=("predicted_relative_utility", "mean"),
        realized_utility_mean=("realized_relative_utility", "mean"),
        positive_realized_fraction=("realized_relative_utility", lambda x: float((x > 0).mean())),
        base_ndcg10=("base_ndcg10", "mean"),
        memory_ndcg10=("memory_ndcg10", "mean"),
        frozen_invocation_fraction=("frozen_use_memory", "mean"),
    )
    deciles.to_csv(args.out_dir / "utility_deciles.csv", index=False)
    rho, rho_p = spearmanr(pred_utility, realized)

    # P0-B2: budget curves and oracle headroom.
    n = len(t)
    frozen_k = int(frozen_use.sum())
    budgets = sorted(set([0.0, *np.linspace(0.05, 1.0, 20).tolist(), frozen_k / n, 1.0]))
    curve_rows = []
    for frac in budgets:
        k = int(round(frac * n))
        util_mask = topk_mask(pred_utility, k)
        oracle_mask = topk_mask(realized, k)
        util_score = np.where(util_mask, mem_t, base_t)
        oracle_score = np.where(oracle_mask, mem_t, base_t)
        curve_rows.append({
            "budget_fraction": float(k / n),
            "k": int(k),
            "utility_router_ndcg10": float(util_score.mean()),
            "utility_router_gain": float((util_score - base_t).mean()),
            "oracle_exact_k_ndcg10": float(oracle_score.mean()),
            "oracle_exact_k_gain": float((oracle_score - base_t).mean()),
        })
    curve = pd.DataFrame(curve_rows).drop_duplicates("k").sort_values("k")
    curve.to_csv(args.out_dir / "utility_budget_oracle_curve.csv", index=False)

    unrestricted_oracle_mask = realized > 0
    unrestricted_oracle = np.where(unrestricted_oracle_mask, mem_t, base_t)
    frozen_gain = float((frozen_selected - base_t).mean())
    oracle_k_mask = topk_mask(realized, frozen_k)
    oracle_k = np.where(oracle_k_mask, mem_t, base_t)
    oracle_k_gain = float((oracle_k - base_t).mean())
    oracle_unrestricted_gain = float((unrestricted_oracle - base_t).mean())

    # P0-B3: generic base-difficulty routing at the exact frozen HGB invocation budget.
    feats = USER_FEATURES + CONF_FEATURES
    Xd = d[feats].to_numpy(float)
    Xt = t[feats].to_numpy(float)
    base_d = d.dual_score10.to_numpy(float)
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    difficulty_target = 1.0 - base_d
    difficulty_model = clone(hgb()).fit(Xd, difficulty_target)
    difficulty_pred = difficulty_model.predict(Xt)
    difficulty_use = topk_mask(difficulty_pred, frozen_k)
    difficulty_selected = np.where(difficulty_use, mem_t, base_t)
    diff_vs_base = paired_ci(difficulty_selected - base_t, SEED + 901)
    utility_vs_difficulty = paired_ci(frozen_selected - difficulty_selected, SEED + 902)

    matched_budget = pd.DataFrame([
        {
            "router": "frozen_relative_utility_HGB",
            "k": frozen_k,
            "invocation_rate": float(frozen_k / n),
            "ndcg10": float(frozen_selected.mean()),
            "gain_vs_base": float(frozen_gain),
        },
        {
            "router": "base_difficulty_HGB_exactK",
            "k": frozen_k,
            "invocation_rate": float(frozen_k / n),
            "ndcg10": float(difficulty_selected.mean()),
            "gain_vs_base": float(diff_vs_base["mean"]),
        },
        {
            "router": "oracle_relative_utility_exactK",
            "k": frozen_k,
            "invocation_rate": float(frozen_k / n),
            "ndcg10": float(oracle_k.mean()),
            "gain_vs_base": float(oracle_k_gain),
        },
    ])
    matched_budget.to_csv(args.out_dir / "matched_budget_routing.csv", index=False)

    # P0-C: information-source ablation under the final Dual-ID base.
    ablations = [history_threshold_gate(d, t)]
    ablations.append(eval_model_gate("state_only_HGB", d, t, USER_FEATURES, cv, 921))
    ablations.append(eval_model_gate("confidence_only_HGB", d, t, CONF_FEATURES, cv, 931))
    ablations.append(eval_model_gate("state_plus_confidence_HGB_reconstructed", d, t, feats, cv, 941))
    frozen_ci = paired_ci(frozen_selected - base_t, SEED + 951)
    ablations.append({
        "name": "state_plus_confidence_HGB_frozen_primary",
        "features": "+".join(feats),
        "dev_oof_ndcg10": float(ref["selective_dev_oof_ndcg10"]),
        "dev_invocation_rate": float(ref["dev_gate_rate"]),
        "threshold": np.nan,
        "test_ndcg10": float(frozen_selected.mean()),
        "test_delta_vs_dual": frozen_ci["mean"],
        "ci95_low": frozen_ci["ci95_low"],
        "ci95_high": frozen_ci["ci95_high"],
        "test_invocation_rate": float(frozen_use.mean()),
        "selected_n": frozen_k,
    })
    ablation_df = pd.DataFrame(ablations)
    ablation_df.to_csv(args.out_dir / "dual_id_information_ablation.csv", index=False)

    tmp["difficulty_pred"] = difficulty_pred
    tmp["difficulty_use_exactK"] = difficulty_use
    tmp["oracle_use_exactK"] = oracle_k_mask
    tmp.to_csv(args.out_dir / "per_user_utility_analysis.csv.gz", index=False, compression="gzip")

    report = {
        "experiment": "dual_id_conditional_utility_closure",
        "task": "next_live_room_sampled_active_575",
        "users": int(n),
        "alpha_room_reproduced": float(alpha),
        "base_test_ndcg10": float(base_t.mean()),
        "memory_test_ndcg10": float(mem_t.mean()),
        "frozen_selective_test_ndcg10": float(frozen_selected.mean()),
        "frozen_selective_gain_vs_base": frozen_ci,
        "frozen_invocation_rate": float(frozen_k / n),
        "calibration": {
            "spearman_predicted_vs_realized": float(rho),
            "spearman_pvalue": float(rho_p),
            "top_decile_realized_utility": float(deciles.iloc[-1].realized_utility_mean),
            "bottom_decile_realized_utility": float(deciles.iloc[0].realized_utility_mean),
            "top_decile_positive_fraction": float(deciles.iloc[-1].positive_realized_fraction),
            "bottom_decile_positive_fraction": float(deciles.iloc[0].positive_realized_fraction),
        },
        "matched_budget": {
            "k": frozen_k,
            "difficulty_router_gain_vs_base": diff_vs_base,
            "utility_router_gain_vs_base": frozen_ci,
            "utility_minus_difficulty": utility_vs_difficulty,
            "oracle_exact_k_gain_vs_base": float(oracle_k_gain),
            "fraction_oracle_exact_k_gain_captured": (
                float(frozen_gain / oracle_k_gain) if abs(oracle_k_gain) > EPS else None
            ),
        },
        "oracle_unrestricted": {
            "positive_delta_fraction": float(unrestricted_oracle_mask.mean()),
            "ndcg10": float(unrestricted_oracle.mean()),
            "gain_vs_base": float(oracle_unrestricted_gain),
            "fraction_unrestricted_oracle_gain_captured": (
                float(frozen_gain / oracle_unrestricted_gain)
                if abs(oracle_unrestricted_gain) > EPS else None
            ),
        },
        "interpretation_guardrail": (
            "The utility-vs-difficulty comparison is matched at the frozen HGB invocation budget. "
            "It tests whether specialist-minus-base prediction adds information beyond generic base difficulty; "
            "it is not a causal treatment-effect analysis."
        ),
    }
    (args.out_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("\nDual-ID information ablation:\n", ablation_df.to_string(index=False))
    print("\nMatched-budget routing:\n", matched_budget.to_string(index=False))


if __name__ == "__main__":
    main()
