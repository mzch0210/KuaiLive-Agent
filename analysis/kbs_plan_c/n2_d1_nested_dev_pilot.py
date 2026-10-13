#!/usr/bin/env python3
"""N2-D1: sealed-DEV-only nested comparison of direct vs two-stage fixed-expert utility.

Five outer user-disjoint folds; four inner user-disjoint folds calibrate each
pointwise score>=threshold policy under the original max-30%-DEV rule.
Never reads, scores or changes G5 TEST. Event-level output stays on User-host.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

from g3_fit_dev_gates import FAMILY_BASE_FEATURES, SHARED_FEATURES, prepare_family_data
from frozen_gate import select_threshold

EXPECTED_N = 50049
EXPECTED_FEATURES = 12
FAMILIES = ("sasrec", "gru4rec")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def estimator(seed: int, max_iter: int = 200, min_leaf: int = 50):
    return HistGradientBoostingRegressor(
        loss="squared_error",
        max_iter=max_iter,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=min_leaf,
        l2_regularization=1.0,
        early_stopping=False,
        random_state=seed,
    )


def validate_source(directory: Path):
    manifest_file = directory / "summary.json"
    csv_file = directory / "dev_full_active_pairs.csv"
    if not manifest_file.is_file() or not csv_file.is_file():
        raise FileNotFoundError("Original corrected DEV paired cache absent")
    meta = json.loads(manifest_file.read_text())
    if (meta.get("schema") != "kbs-plan-c-full-active-dev-paired-v2"
        or meta.get("n_scored") != EXPECTED_N
        or meta.get("memory_corrected_from_all_history") is not True
        or meta.get("test_file_accessed") is not False
        or meta.get("source_test_outcomes_inspected", False) is not False):
        raise ValueError("DEV-only canonical corrected provenance rejected")
    source_sha = sha256(csv_file)
    if source_sha != meta.get("event_csv_sha256"):
        raise ValueError("Source DEV paired CSV SHA mismatch")
    return csv_file, source_sha, meta


def validate_frame(frame: pd.DataFrame):
    if frame.empty or not frame["split"].eq("DEV").all():
        raise ValueError("Only DEV rows allowed; TEST forbidden")
    if len(frame) != EXPECTED_N or frame["event_id"].isna().any():
        raise ValueError("Invalid number or identity of DEV events")
    if frame.event_id.duplicated().any() or frame.user_id.isna().any():
        raise ValueError("Invalid DEV identities")
    if frame.user_id.nunique() < 10:
        raise ValueError("Not enough users for nested GroupKFold")
    return frame


def cluster_ci(differences, users, n_boot=2000, seed=20261013):
    unique, inverse = np.unique(users.astype(str), return_inverse=True)
    sums = np.bincount(inverse, weights=differences, minlength=len(unique))
    counts = np.bincount(inverse, minlength=len(unique))
    rng = np.random.default_rng(seed)
    samples = np.empty(n_boot, dtype=float)
    for j in range(n_boot):
        sel = rng.integers(0, len(unique), size=len(unique))
        samples[j] = sums[sel].sum() / counts[sel].sum()
    return [float(q) for q in np.quantile(samples, [0.025, 0.975])]


def nested_compare(
    frame: pd.DataFrame, family: str, *,
    n_outer=5, n_inner=4, max_iter=200, min_leaf=50, n_boot=2000,
):
    if family not in FAMILIES:
        raise ValueError("Unsupported family")
    feature_cols = sorted(c for c in frame if c.startswith("x_"))
    if len(feature_cols) != EXPECTED_FEATURES:
        raise ValueError("Exactly 12 pre-outcome features required")
    if any("target" in c or "ndcg" in c or "label" in c for c in feature_cols):
        raise ValueError("Outcome leakage through features")
    X = frame[feature_cols].to_numpy(dtype=float)
    by = frame.base_ndcg10.to_numpy(dtype=float)
    my = frame.memory_ndcg10.to_numpy(dtype=float)
    delta = my - by
    groups = frame.user_id.astype(str).to_numpy()
    if not np.isfinite(X).all() or not np.isfinite(by).all() or not np.isfinite(my).all():
        raise ValueError("Nonfinite predictor or label")
    if np.any(by < 0) or np.any(my < 0) or np.any(by > 1) or np.any(my > 1):
        raise ValueError("NDCG values must be [0,1]")
    masks = {name: np.zeros(len(frame), dtype=bool) for name in ("direct", "two_stage")}
    seen = np.zeros(len(frame), dtype=np.uint8)
    outer_reports = []
    started = time.perf_counter()
    for outer, (tr, va) in enumerate(GroupKFold(n_splits=n_outer).split(X, groups=groups)):
        if set(groups[tr]) & set(groups[va]):
            raise AssertionError("Outer user overlap")
        inner_oof = {name: np.full(len(tr), np.nan) for name in
                     ("direct", "base", "memory")}
        inner_splits = GroupKFold(n_splits=n_inner).split(X[tr], groups=groups[tr])
        for inner, (itr, iva) in enumerate(inner_splits):
            if set(groups[tr][itr]) & set(groups[tr][iva]):
                raise AssertionError("Inner user overlap")
            local_targets = {
                "direct": delta[tr][itr],
                "base": by[tr][itr],
                "memory": my[tr][itr],
            }
            for name, target in local_targets.items():
                reg = estimator(20261012 + inner, max_iter=max_iter, min_leaf=min_leaf)
                reg.fit(X[tr][itr], target)
                inner_oof[name][iva] = reg.predict(X[tr][iva])
        if any(not np.isfinite(a).all() for a in inner_oof.values()):
            raise ValueError("Incomplete inner OOF estimates")
        inner_scores = {
            "direct": inner_oof["direct"],
            "two_stage": inner_oof["memory"] - inner_oof["base"],
        }
        thresholds = {
            name: select_threshold(inner_scores[name].tolist(), delta[tr].tolist(), 0.30)
            for name in ("direct", "two_stage")
        }
        final_predictions = {}
        for name, target in (("direct", delta[tr]), ("base", by[tr]), ("memory", my[tr])):
            reg = estimator(20261012, max_iter=max_iter, min_leaf=min_leaf)
            reg.fit(X[tr], target)
            final_predictions[name] = reg.predict(X[va])
        outer_scores = {
            "direct": final_predictions["direct"],
            "two_stage": final_predictions["memory"] - final_predictions["base"],
        }
        fold_summary = {"outer_fold": outer + 1, "n_train": len(tr), "n_valid": len(va),
                        "n_valid_users": len(set(groups[va])), "results": {}}
        for name, scores in outer_scores.items():
            threshold = thresholds[name]["threshold"]
            mask = np.zeros(len(va), dtype=bool) if threshold is None else scores >= threshold
            masks[name][va] = mask
            fold_summary["results"][name] = {
                "inner_oof_selection_rate": thresholds[name]["dev_oof_call_rate"],
                "outer_call_rate": float(mask.mean()),
                "outer_ndcg10": float(np.mean(by[va] + mask * delta[va])),
                "outer_delta_vs_base": float(np.mean(mask * delta[va])),
            }
        seen[va] += 1
        outer_reports.append(fold_summary)
    if not np.all(seen == 1):
        raise AssertionError("Every DEV event must occur once in outer holdout")
    quality = {name: by + masks[name] * delta for name in masks}
    diff = quality["direct"] - quality["two_stage"]
    metrics = {
        name: {"ndcg10": float(np.mean(quality[name])),
               "gain_over_base": float(np.mean(quality[name] - by)),
               "memory_calls": int(masks[name].sum()),
               "memory_call_rate": float(masks[name].mean())}
        for name in masks
    }
    return {
        "family": family, "evidence_tier": "POST_G5_EXPLORATORY_NESTED_DEV",
        "n_events": len(frame), "n_users": len(set(groups)),
        "outer_folds": n_outer, "inner_folds": n_inner,
        "n_features": len(feature_cols), "max_dev_call_fraction": 0.30,
        "always_base_ndcg10": float(by.mean()),
        "always_memory_ndcg10": float(my.mean()),
        "methods": metrics, "direct_minus_two_stage_ndcg10": float(diff.mean()),
        "direct_minus_two_stage_user_cluster_boot_ci95":
            cluster_ci(diff, groups, n_boot=n_boot),
        "elapsed_cpu_seconds": float(time.perf_counter() - started),
        "folds": outer_reports, "test_accessed": False,
        "not_full_neurips_l2d_replication": True,
        "not_confirmatory_g5": True,
    }


def run(source: Path, out: Path):
    infile, file_hash, meta = validate_source(source)
    if out.exists():
        raise FileExistsError("Refuse to overwrite DEV pilot outputs")
    raw = pd.read_csv(infile)
    verify = {}
    for fam in FAMILIES:
        fam_frame = validate_frame(prepare_family_data(raw, fam))
        verify[fam] = nested_compare(fam_frame, fam)
        print(json.dumps({"completed_family": fam, "results": verify[fam]["methods"],
                          "n_events": verify[fam]["n_events"]}), flush=True)
    result = {
        "schema": "kbs-n2-d1-two-stage-pilot-dev-only-v1",
        "source_dev_sha256": file_hash,
        "source_manifest_sha256": sha256(source / "summary.json"),
        "source_base_checkpoint_sha": meta.get("base_checkpoint_sha"),
        "source_g1_protocol_sha256": meta.get("g1_protocol_sha256"),
        "main_seed": 20261012, "training_data_scope": "DEV_ONLY",
        "scientific_status": "EXPLORATORY_AFTER_G5",
        "G5_TEST_opened": False, "G5_policy_changed": False,
        "n_dev": EXPECTED_N, "families": verify,
    }
    out.mkdir(mode=0o700, parents=True)
    artifact = out / "summary.json"
    artifact.write_text(json.dumps(result, indent=2) + "\n")
    artifact.chmod(0o600)
    print(json.dumps({"status": "N2_D1_DEV_PILOT_COMPLETE", "summary_sha256": sha256(artifact),
                      "test_accessed": False}), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    run(args.source, args.out)
