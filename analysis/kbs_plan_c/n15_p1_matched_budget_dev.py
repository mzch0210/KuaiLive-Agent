#!/usr/bin/env python3
"""N15 P1: exact-batch-call matched F-versus-S supervision, exploratory DEV only.

Never reads TEST, B4-A, or score files from in-sample fitted DEV final models.
Private per-request rows, labels, user IDs, predictions and models are not exported.
The result is a decision sensitivity analysis, not a new confirmatory experiment.
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
USERS = 12628
SEED = 20261012
SHA = "37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
PRIMARY_Q = 0.30
BUDGETS = (0.10, 0.20, 0.30, 0.40)
SHARED = (
    "hist_event_count", "hist_warm_count", "hist_distinct",
    "hist_repeat_max", "hist_short_unique", "memory_history_supported_share",
    "candidate_log_count",
)
BASE = ("base_margin", "base_std", "base_top_z", "base_top_score", "base_score_mean")
FAMILIES = ("sasrec", "gru4rec")


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
    """Select floor(q*n) highest scores with label-blind fixed tie resolution.

    The tie key is a seeded digest of the ORIGINAL row index of the frozen DEV
    CSV, not the positive target or any observed ranking label. The mask is
    indexed in local batch order, not full-dataset row order.
    """
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
        (
            int.from_bytes(
                hashlib.sha256(f"n15-batch|{SEED}|{int(i)}".encode()).digest()[:8],
                byteorder="big",
            )
            for i in row_index
        ),
        dtype=np.uint64, count=len(row_index),
    )
    order = np.lexsort((keys, -scores))
    chosen[order[:k]] = True
    if int(chosen.sum()) != k:
        raise RuntimeError("Exact call count invariant failed")
    return chosen


def user_cluster_ci(values: np.ndarray, users: np.ndarray, reps: int, seed: int) -> list[float]:
    """Exploratory user-cluster bootstrap; fixed actions, not policy refitting."""
    if reps < 0:
        raise ValueError("Negative bootstrap repeats")
    if reps == 0:
        return []
    _, inverse = np.unique(users, return_inverse=True)
    totals = np.bincount(inverse, weights=values)
    counts = np.bincount(inverse)
    rng = np.random.default_rng(seed)
    draws = np.empty(reps, dtype=np.float64)
    for i in range(reps):
        sampled = rng.integers(0, len(counts), size=len(counts))
        draws[i] = float(totals[sampled].sum() / counts[sampled].sum())
    return [float(a) for a in np.quantile(draws, [0.025, 0.975])]


def run_family(df: pd.DataFrame, family: str, reps: int) -> dict:
    features = ["x_" + x for x in SHARED] + ["x_" + family + "_" + x for x in BASE]
    if len(features) != 12 or not set(features).issubset(df.columns):
        raise ValueError("Original 12 pretarget features unavailable")
    x = df[features].to_numpy(dtype=np.float64)
    fb = df[family + "_ndcg10"].to_numpy(dtype=np.float64)
    fm = df["memory_ndcg10"].to_numpy(dtype=np.float64)
    sb = df["sampled_" + family + "_ndcg10"].to_numpy(dtype=np.float64)
    sm = df["sampled_memory_ndcg10"].to_numpy(dtype=np.float64)
    user = df["user_id"].astype(str).to_numpy()
    if not all(np.isfinite(a).all() for a in (x, fb, fm, sb, sm)):
        raise ValueError("Non-finite feature or ranking utility")
    if not all(((a >= 0) & (a <= 1)).all() for a in (fb, fm, sb, sm)):
        raise ValueError("NDCG outside [0,1]")
    dfull, dsampled = fm - fb, sm - sb
    masks = {q: {"F": np.zeros(N, dtype=bool), "S": np.zeros(N, dtype=bool)} for q in BUDGETS}
    seen = np.zeros(N, dtype=np.uint8)
    folds = []
    for fold_id, (train, val) in enumerate(GroupKFold(n_splits=5).split(x, groups=user), start=1):
        if not set(user[train]).isdisjoint(set(user[val])):
            raise RuntimeError("User overlap across train/evaluation")
        pred = {}
        for arm, labels in (("F", dfull), ("S", dsampled)):
            model = regressor()
            model.fit(x[train], labels[train])
            pred[arm] = model.predict(x[val])
        for q in BUDGETS:
            for arm in ("F", "S"):
                masks[q][arm][val] = exact_batch_topk(pred[arm], val, q)
        seen[val] += 1
        folds.append({
            "fold": fold_id,
            "n_events": int(len(val)),
            "n_users": int(len(np.unique(user[val]))),
            "calls_at_primary_quota": int(math.floor(PRIMARY_Q * len(val))),
        })
    if not np.all(seen == 1):
        raise RuntimeError("Exactly one held-out prediction per DEV event required")
    outcomes = {}
    for q in BUDGETS:
        maskf, masks_ = masks[q]["F"], masks[q]["S"]
        if int(maskf.sum()) != int(masks_.sum()):
            raise RuntimeError("F and S have unequal exact call counts")
        delta = (maskf.astype(np.int8) - masks_.astype(np.int8)) * dfull
        fquality = fb + maskf * dfull
        squality = fb + masks_ * dfull
        gain = float(delta.mean())
        if not np.allclose(fquality - squality, delta, atol=1e-14, rtol=0):
            raise RuntimeError("Allocation-value identity failed")
        f_only = maskf & ~masks_
        s_only = masks_ & ~maskf
        both = maskf & masks_
        neither = ~(maskf | masks_)
        if int(f_only.sum()) != int(s_only.sum()):
            raise RuntimeError("Matched-budget exchange counts differ")
        outcomes[f"{q:.2f}"] = {
            "budget": q,
            "calls_F": int(maskf.sum()),
            "calls_S": int(masks_.sum()),
            "raw_rate_F": float(maskf.mean()),
            "raw_rate_S": float(masks_.mean()),
            "full_F_ndcg_F": float(fquality.mean()),
            "full_F_ndcg_S": float(squality.mean()),
            "F_minus_S_full_F_ndcg": float(fquality.mean() - squality.mean()),
            "paired_allocation_value": gain,
            "paired_identity_error": float(abs(fquality.mean() - squality.mean() - gain)),
            "both_calls": int(both.sum()),
            "F_only": int(f_only.sum()),
            "S_only": int(s_only.sum()),
            "neither_calls": int(neither.sum()),
            "F_only_mean_full_increment": float(dfull[f_only].mean()) if f_only.any() else None,
            "S_only_mean_full_increment": float(dfull[s_only].mean()) if s_only.any() else None,
            "user_cluster_bootstrap_95ci_exploratory":
                user_cluster_ci(delta, user, reps, 20261027) if q == PRIMARY_Q else None,
        }
    return {
        "family": family, "events": N, "user_clusters": USERS,
        "always_base_full_F_ndcg": float(fb.mean()),
        "always_memory_full_F_ndcg": float(fm.mean()),
        "n_outer_user_folds": 5,
        "pretarget_feature_count": 12,
        "separate_F_and_S_supervised_model_fits": True,
        "matched_offline_batch_calls_not_live_online_policy": True,
        "folds": folds, "budgets": outcomes,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=2000)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError("Never overwrite a scientific exploratory result directory")
    if args.source.name != "klm3_b1_full_dev_candidate_labels_seed20261012_v1":
        raise RuntimeError("Only frozen B1 DEV source is eligible")
    meta = json.loads((args.source / "summary.json").read_text())
    csv = args.source / "dev_pair_candidate_labels.csv"
    if not (
        meta.get("schema") == "kbs-b1-full-dev-paired-candidate-labels-v1"
        and meta.get("status") == "PASS"
        and meta.get("scope") == "DEV_ONLY_POST_G5_EXPLORATORY"
        and meta.get("n_dev_events") == N
        and meta.get("n_users") == USERS
        and meta.get("target_retained_sampling_offline_labels_only") is True
        and meta.get("test_accessed") is False
        and meta.get("model_training") is False
        and sha256(csv) == SHA
        and meta.get("private_event_source_csv_sha256") == SHA
    ):
        raise RuntimeError("Frozen private B1 DEV source failed scientific provenance gate")
    columns = (
        ["event_id", "user_id", "split", "memory_ndcg10", "sampled_memory_ndcg10"]
        + [f + "_ndcg10" for f in FAMILIES]
        + ["sampled_" + f + "_ndcg10" for f in FAMILIES]
        + ["x_" + s for s in SHARED]
        + ["x_" + f + "_" + s for f in FAMILIES for s in BASE]
    )
    df = pd.read_csv(csv, usecols=columns)
    if not (
        len(df) == N and df.event_id.is_unique and df.split.eq("DEV").all()
        and df.user_id.notna().all() and df.user_id.nunique() == USERS
    ):
        raise RuntimeError("DEV user / event / split invariant failed")
    families = {f: run_family(df, f, args.bootstrap) for f in FAMILIES}
    summary = {
        "schema": "kbs-n15-p1-matched-budget-dev-v1",
        "status": "DEV_EXPLORATORY_ONLY",
        "n_events": N, "n_users": USERS,
        "source_sha256": SHA,
        "n_test_labels_accessed": 0,
        "n_original_test_events_used": 0,
        "prospective_confirmatory_result": False,
        "quota_policy": "offline_outer_fold_exact_top_k",
        "population_weights": "none; original unweighted DEV; NOT B4A population-weighted",
        "quota_main": PRIMARY_Q,
        "quotas": list(BUDGETS),
        "tie_rule": "seeded SHA256 original DEV row index; no outcome data",
        "families": families,
    }
    args.out.mkdir(mode=0o700, parents=True)
    output = args.out / "aggregate_only.json"
    output.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": summary["status"],
        "n_events": N,
        "matched_calls_main": {f: families[f]["budgets"]["0.30"]["calls_F"] for f in FAMILIES},
    }, sort_keys=True))


if __name__ == "__main__":
    main()
