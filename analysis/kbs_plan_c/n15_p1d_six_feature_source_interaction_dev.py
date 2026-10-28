#!/usr/bin/env python3
"""N15 P1-D: one-shot six-feature exact-call Full-vs-Long interaction.

Exploratory reused-DEV analysis only. Reads certified B1/B2 private DEV CSVs;
outputs aggregate metrics only. Never reads TEST, never exports event/user rows.
Uses the frozen six-descriptor B2 panel, the established HGB capacity and outer user folds; q=0.30 only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

N = 50049
N_USERS = 12628
SEED = 20261012
B1_SHA = "37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
BUDGETS = (0.30,)
PRIMARY_Q = 0.30
SOURCES = {
    "full": ("memory_ndcg10", "sampled_memory_ndcg10"),
    "long_only": ("b2_long_only_F_ndcg10", "b2_long_only_S_ndcg10"),
}
FAMILIES = ("sasrec", "gru4rec")
SHARED = (
    "hist_event_count", "hist_warm_count", "hist_distinct",
    "hist_repeat_max", "hist_short_unique", "memory_history_supported_share",
    "candidate_log_count",
)
BASE = ("base_margin", "base_std", "base_top_z", "base_top_score", "base_score_mean")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def regressor() -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        loss="squared_error", max_iter=120, learning_rate=0.05,
        max_depth=3, min_samples_leaf=50, l2_regularization=1.0,
        early_stopping=False, random_state=SEED,
    )


def exact_batch_topk(scores: np.ndarray, row_index: np.ndarray, q: float) -> np.ndarray:
    """Exactly floor(q*n) choices; score ties broken by protected row index hash."""
    scores = np.asarray(scores, dtype=np.float64)
    row_index = np.asarray(row_index, dtype=np.int64)
    if scores.ndim != 1 or row_index.ndim != 1 or len(scores) != len(row_index):
        raise ValueError("Scores/indices must be equally sized 1D arrays")
    if len(set(row_index.tolist())) != len(row_index):
        raise ValueError("Duplicate stable row indices")
    if not np.isfinite(scores).all() or not (0.0 <= q <= 1.0):
        raise ValueError("Invalid scores or quota")
    k = math.floor(q * len(scores))
    chosen = np.zeros(len(scores), dtype=bool)
    if k == 0:
        return chosen
    keys = np.fromiter(
        (int.from_bytes(hashlib.sha256(
            f"n15-batch|{SEED}|{int(i)}".encode()).digest()[:8], "big")
         for i in row_index),
        dtype=np.uint64, count=len(row_index),
    )
    order = np.lexsort((keys, -scores))
    chosen[order[:k]] = True
    if int(chosen.sum()) != k:
        raise RuntimeError("Exact call count invariant failed")
    return chosen


def user_cluster_ci(values: np.ndarray, users: np.ndarray, reps: int, seed: int) -> list[float]:
    """Descriptive user-cluster bootstrap of fixed-policy event-weighted mean."""
    if reps < 0:
        raise ValueError("Negative bootstrap repeats")
    if reps == 0:
        return []
    _, inverse = np.unique(users.astype(str), return_inverse=True)
    totals = np.bincount(inverse, weights=values)
    counts = np.bincount(inverse)
    rng = np.random.default_rng(seed)
    draws = np.empty(reps, dtype=np.float64)
    for i in range(reps):
        sampled = rng.integers(0, len(counts), size=len(counts))
        draws[i] = float(totals[sampled].sum() / counts[sampled].sum())
    return [float(v) for v in np.quantile(draws, [0.025, 0.975])]


def validate_sources(source_b2: Path, source_b1: Path) -> tuple[pd.DataFrame, str]:
    b2_meta = json.loads((source_b2 / "summary.json").read_text())
    b1_meta = json.loads((source_b1 / "summary.json").read_text())
    b2_csv = source_b2 / "dev_memory_source_ablation_pairs.csv"
    b1_csv = source_b1 / "dev_pair_candidate_labels.csv"
    if not (
        b1_meta.get("schema") == "kbs-b1-full-dev-paired-candidate-labels-v1"
        and b1_meta.get("status") == "PASS"
        and b1_meta.get("scope") == "DEV_ONLY_POST_G5_EXPLORATORY"
        and b1_meta.get("test_accessed") is False
        and b1_meta.get("n_dev_events") == N
        and b1_meta.get("n_users") == N_USERS
        and b1_meta.get("private_event_source_csv_sha256") == B1_SHA
        and sha256(b1_csv) == B1_SHA
    ):
        raise RuntimeError("Frozen B1 source provenance/hash gate failed")
    b2_sha = b2_meta.get("private_event_source_csv_sha256")
    if not (
        b2_meta.get("schema") == "kbs-b2-dev-relationship-source-ablation-v1"
        and b2_meta.get("scope") == "POST_G5_DEV_EXPLORATORY"
        and b2_meta.get("status") == "PASS"
        and b2_meta.get("is_full_cohort") is True
        and b2_meta.get("n_events") == N
        and b2_meta.get("n_users") == N_USERS
        and b2_meta.get("full_memory_nDCG_mismatches") == {"F": 0, "S": 0}
        and b2_meta.get("new_TEST_opened") is False
        and b2_meta.get("models_retrained") is False
        and b2_meta.get("b2_nested_policy_fit") is False
        and b2_meta.get("candidate_labels_target_retained_offline_only") is True
        and b2_meta.get("source_b1_pair_sha256") == B1_SHA
        and isinstance(b2_sha, str) and len(b2_sha) == 64
        and sha256(b2_csv) == b2_sha
    ):
        raise RuntimeError("Frozen B2 source provenance/hash gate failed")

    features = ["x_" + x for x in SHARED] + [
        "x_" + fam + "_" + x for fam in FAMILIES for x in BASE
    ]
    base_cols = ["event_id", "user_id", "split", "memory_ndcg10",
                 "sampled_memory_ndcg10"]
    for fam in FAMILIES:
        base_cols += [fam + "_ndcg10", "sampled_" + fam + "_ndcg10"]
    compare_cols = list(dict.fromkeys(base_cols + features))
    b1 = pd.read_csv(b1_csv, usecols=compare_cols)
    b2_cols = list(dict.fromkeys(compare_cols + [
        "b2_long_only_F_ndcg10", "b2_long_only_S_ndcg10"
    ]))
    data = pd.read_csv(b2_csv, usecols=b2_cols)
    if not (
        len(b1) == N and len(data) == N
        and b1.event_id.is_unique and data.event_id.is_unique
        and b1.split.eq("DEV").all() and data.split.eq("DEV").all()
        and b1.user_id.nunique() == N_USERS and data.user_id.nunique() == N_USERS
    ):
        raise RuntimeError("B1/B2 row, user, or split invariant failed")
    b1i = b1.set_index("event_id").sort_index()
    b2i = data.set_index("event_id").sort_index()
    if not b1i.index.equals(b2i.index):
        raise RuntimeError("B1/B2 event roster mismatch")
    if not np.array_equal(b1i.user_id.astype(str).to_numpy(), b2i.user_id.astype(str).to_numpy()):
        raise RuntimeError("B1/B2 user assignment mismatch")
    for col in compare_cols:
        if col in ("event_id", "user_id", "split"):
            continue
        a = pd.to_numeric(b1i[col], errors="raise").to_numpy(dtype=np.float64)
        b = pd.to_numeric(b2i[col], errors="raise").to_numpy(dtype=np.float64)
        if not np.isfinite(a).all() or not np.isfinite(b).all() or not np.allclose(a, b, atol=1e-12, rtol=0):
            raise RuntimeError("B1/B2 byte-source parity failed for " + col)
    for col in ("b2_long_only_F_ndcg10", "b2_long_only_S_ndcg10"):
        v = data[col].to_numpy(dtype=np.float64)
        if not np.isfinite(v).all() or not ((v >= 0) & (v <= 1)).all():
            raise RuntimeError("Invalid source-specific NDCG labels: " + col)
    if not data.event_id.is_unique:
        raise RuntimeError("Duplicate event id")
    return data, b2_sha


def run_family(data: pd.DataFrame, family: str, reps: int) -> dict:
    features = ["x_candidate_log_count"] + ["x_" + family + "_" + x for x in BASE]
    if len(features) != 6 or not set(features).issubset(data.columns):
        raise RuntimeError("Frozen six-feature B2 panel unavailable")
    X = data[features].to_numpy(dtype=np.float64)
    users = data.user_id.astype(str).to_numpy()
    if not np.isfinite(X).all():
        raise RuntimeError("Non-finite pretarget features")
    base_f = data[family + "_ndcg10"].to_numpy(dtype=np.float64)
    base_s = data["sampled_" + family + "_ndcg10"].to_numpy(dtype=np.float64)
    if not all(np.isfinite(x).all() and ((x >= 0) & (x <= 1)).all() for x in (base_f, base_s)):
        raise RuntimeError("Invalid Base ranking labels")

    targets = {}
    for source, (f_col, s_col) in SOURCES.items():
        mem_f = data[f_col].to_numpy(dtype=np.float64)
        mem_s = data[s_col].to_numpy(dtype=np.float64)
        if not all(np.isfinite(x).all() and ((x >= 0) & (x <= 1)).all() for x in (mem_f, mem_s)):
            raise RuntimeError("Invalid memory ranking labels for " + source)
        targets[source] = {"F": mem_f - base_f, "S": mem_s - base_s,
            "memory_f_mean": float(mem_f.mean()), "memory_s_mean": float(mem_s.mean())}

    masks = {src: {q: {arm: np.zeros(N, dtype=bool) for arm in ("F", "S")}
                   for q in BUDGETS} for src in SOURCES}
    seen = np.zeros(N, dtype=np.uint8)
    fold_summary = []
    split_iter = GroupKFold(n_splits=5).split(np.zeros((N, 1)), groups=users)
    for fold_id, (train, val) in enumerate(split_iter, start=1):
        if not set(users[train]).isdisjoint(set(users[val])):
            raise RuntimeError("Outer user leakage")
        predictions = {}
        for source in SOURCES:
            predictions[source] = {}
            for arm in ("F", "S"):
                y = targets[source][arm]
                model = regressor()
                model.fit(X[train], y[train])
                predictions[source][arm] = model.predict(X[val])
                if not np.isfinite(predictions[source][arm]).all():
                    raise RuntimeError("Nonfinite held-out predictions")
        for q in BUDGETS:
            for source in SOURCES:
                for arm in ("F", "S"):
                    masks[source][q][arm][val] = exact_batch_topk(predictions[source][arm], val, q)
        seen[val] += 1
        fold_summary.append({
            "fold": fold_id, "n_events": int(len(val)),
            "n_users": int(len(np.unique(users[val]))),
            "calls_per_arm_at_30pct": int(math.floor(PRIMARY_Q * len(val))),
        })
    if not np.all(seen == 1):
        raise RuntimeError("Every DEV request must have one held-out score")

    out = {
        "family": family, "n_events": N, "n_users": int(len(np.unique(users))),
        "outer_user_disjoint_folds": 5, "feature_count": 6,
        "source_quality_and_support": {},
        "budgets": {},
        "folds": fold_summary,
    }
    for source in SOURCES:
        d_f, d_s = targets[source]["F"], targets[source]["S"]
        out["source_quality_and_support"][source] = {
            "always_base_full_F_ndcg10": float(base_f.mean()),
            "always_memory_full_F_ndcg10": targets[source]["memory_f_mean"],
            "memory_sampled_S_ndcg10": targets[source]["memory_s_mean"],
            "mean_F_increment_over_base": float(d_f.mean()),
            "positive_F_increment_share": float(np.mean(d_f > 0)),
            "mean_S_increment_over_sampled_base": float(d_s.mean()),
            "positive_S_increment_share": float(np.mean(d_s > 0)),
            "F_vs_S_increment_sign_change_share": float(np.mean(np.sign(d_f) != np.sign(d_s))),
        }
    interaction_values = {}
    for q in BUDGETS:
        out["budgets"][f"{q:.2f}"] = {"by_source": {}}
        deltas = {}
        for source in SOURCES:
            mask_f, mask_s = masks[source][q]["F"], masks[source][q]["S"]
            if int(mask_f.sum()) != int(mask_s.sum()):
                raise RuntimeError("F/S source policies have unequal calls")
            d_f = targets[source]["F"]
            delta = (mask_f.astype(np.float64) - mask_s.astype(np.float64)) * d_f
            quality_f = base_f + mask_f * d_f
            quality_s = base_f + mask_s * d_f
            identity_error = float(abs((quality_f.mean() - quality_s.mean()) - delta.mean()))
            if identity_error >= 1e-12:
                raise RuntimeError("Source paired allocation identity failed")
            f_only, s_only = mask_f & ~mask_s, mask_s & ~mask_f
            both, neither = mask_f & mask_s, ~(mask_f | mask_s)
            if int(f_only.sum()) != int(s_only.sum()):
                raise RuntimeError("Exact quota switch counts differ")
            if int(both.sum() + f_only.sum() + s_only.sum() + neither.sum()) != N:
                raise RuntimeError("Source decision partition does not cover DEV")
            deltas[source] = delta
            out["budgets"][f"{q:.2f}"]["by_source"][source] = {
                "calls_F_supervised": int(mask_f.sum()),
                "calls_S_supervised": int(mask_s.sum()),
                "raw_call_rate": float(mask_f.mean()),
                "F_supervised_full_F_ndcg10": float(quality_f.mean()),
                "S_supervised_full_F_ndcg10": float(quality_s.mean()),
                "F_minus_S_full_F_ndcg10": float(quality_f.mean() - quality_s.mean()),
                "paired_allocation_value": float(delta.mean()),
                "paired_identity_error": identity_error,
                "user_cluster_bootstrap_95ci_descriptive":
                    user_cluster_ci(delta, users, reps, 20261028 + int(q*1000) + (0 if source == "full" else 100)),
                "both_calls": int(both.sum()), "F_only": int(f_only.sum()),
                "S_only": int(s_only.sum()), "neither_calls": int(neither.sum()),
                "F_only_mean_F_increment": float(d_f[f_only].mean()) if f_only.any() else None,
                "S_only_mean_F_increment": float(d_f[s_only].mean()) if s_only.any() else None,
            }
        interaction = deltas["full"] - deltas["long_only"]
        d_full = out["budgets"][f"{q:.2f}"]["by_source"]["full"]["paired_allocation_value"]
        d_long = out["budgets"][f"{q:.2f}"]["by_source"]["long_only"]["paired_allocation_value"]
        interaction_mean = float(interaction.mean())
        if abs(interaction_mean - (d_full - d_long)) >= 1e-12:
            raise RuntimeError("Source x supervision interaction identity failed")
        byq = out["budgets"][f"{q:.2f}"]
        byq["full_minus_long_interaction"] = {
            "estimand": "D_full_minus_D_long; D_source = F-supervised policy full-F NDCG minus S-supervised policy full-F NDCG",
            "mean": interaction_mean,
            "equals_difference_of_source_gaps": float(d_full - d_long),
            "identity_error": float(abs(interaction_mean - (d_full - d_long))),
            "user_cluster_bootstrap_95ci_descriptive":
                user_cluster_ci(interaction, users, reps, 20261128 + int(q*1000)),
        }
        interaction_values[q] = interaction
    out["primary_budget"] = PRIMARY_Q
    out["primary_interaction"] = out["budgets"][f"{PRIMARY_Q:.2f}"]["full_minus_long_interaction"]
    out["interpretation_guardrails"] = {\n        "feature_panel": "candidate count plus five Base-score descriptors; not a literal no-history panel",\n        "only_quota": 0.30,
        "offline_outer_fold_batch_top_k_not_online": True,
        "reused_post_G5_DEV_exploratory_only": True,
        "bootstrap_conditions_on_fitted_fold_policies": True,
        "F_vs_S_is_total_label_information_and_policy_comparison_not_label_only_causal_effect": True,
        "corrected_S_competitor_not_included": True,
        "independent_future_test_not_accessed": True,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-b2", type=Path, required=True)
    ap.add_argument("--source-b1", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=2000)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError("Never overwrite an existing N15 P1-D output")
    if args.bootstrap < 0:
        raise ValueError("Bootstrap repetitions must be nonnegative")
    data, b2_sha = validate_sources(args.source_b2, args.source_b1)
    family_results = {fam: run_family(data, fam, args.bootstrap) for fam in FAMILIES}
    summary = {
        "schema": "kbs-n15-p1d-six-feature-exact-budget-source-interaction-v1",
        "status": "DEV_EXPLORATORY_ONLY",
        "n_events": N, "n_users": N_USERS,
        "source_b1_sha256": B1_SHA, "source_b2_sha256": b2_sha,
        "n_test_labels_accessed": 0, "prospective_confirmatory_result": False,
        "quota_policy": "offline_outer_fold_exact_top_k",
        "quotas": list(BUDGETS), "primary_quota": PRIMARY_Q,
        "tie_rule": "seeded SHA256 of protected original B2 CSV row index; label blind",
        "population_weights": "none; unweighted original DEV",
        "families": family_results,
    }
    args.out.mkdir(mode=0o700, parents=True)
    (args.out / "aggregate_only.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    for fam, result in family_results.items():
        p = result["budgets"][f"{PRIMARY_Q:.2f}"]
        print("N15_P1D_SIX_FEATURE_SOURCE_INTERACTION_EXPLORATORY", json.dumps({
            "family": fam,
            "q": PRIMARY_Q,
            "full_D_F_minus_S": p["by_source"]["full"]["F_minus_S_full_F_ndcg10"],
            "long_D_F_minus_S": p["by_source"]["long_only"]["F_minus_S_full_F_ndcg10"],
            "full_minus_long_interaction": p["full_minus_long_interaction"]["mean"],
            "interaction_ci": p["full_minus_long_interaction"]["user_cluster_bootstrap_95ci_descriptive"],
            "calls_per_policy_source": p["by_source"]["full"]["calls_F_supervised"],
        }, sort_keys=True), flush=True)
    print(json.dumps({"status": summary["status"], "n_events": N, "n_users": N_USERS,
                      "b1_b2_source_parity": "PASS", "test_accessed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
