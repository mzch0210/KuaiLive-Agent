#!/usr/bin/env python3
"""KBS Plan C: CPU-only, user-disjoint DEV OOF HGB comparison.

Inputs are pre-target numeric x_* features and paired DEV Base/Memory utility.
Outputs are aligned DEV OOF predictions + final DEV-fit model checkpoints.
No TEST data are accepted. This file does not choose a TEST threshold.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

TARGET_COLUMNS = ("base_ndcg10", "memory_ndcg10")
MODEL_METHODS = ("utility", "difficulty", "specialist")
ALL_METHODS = MODEL_METHODS + ("uncertainty", "history")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def validate_dev(df: pd.DataFrame):
    required = {"event_id", "user_id", "split", "x_base_margin",
                "x_hist_event_count"} | set(TARGET_COLUMNS)
    if not required.issubset(df.columns):
        raise ValueError("missing DEV identity/feature/utility fields")
    if df.empty or not df.split.eq("DEV").all():
        raise ValueError("DEV-only input: no TEST")
    if df.event_id.isna().any() or df.event_id.duplicated().any():
        raise ValueError("duplicate or missing event_id")
    if df.user_id.isna().any() or df.user_id.nunique() < 5:
        raise ValueError("at least 5 nonempty users needed for grouped 5-fold OOF")
    features = sorted(c for c in df if c.startswith("x_"))
    if not features or "x_base_margin" not in features or "x_hist_event_count" not in features:
        raise ValueError("required pre-outcome features missing")
    if any(c in features for c in TARGET_COLUMNS):
        raise ValueError("outcomes leaked into features")
    for col in features + list(TARGET_COLUMNS):
        values = pd.to_numeric(df[col], errors="raise").to_numpy(dtype=np.float64)
        if not np.isfinite(values).all():
            raise ValueError("NaN or Inf in " + col)
    if not ((df.base_ndcg10.between(0, 1) &
             df.memory_ndcg10.between(0, 1)).all()):
        raise ValueError("NDCG out of range")
    return features

def estimator(seed: int):
    return HistGradientBoostingRegressor(
        loss="squared_error", max_iter=200, learning_rate=0.05,
        max_depth=3, min_samples_leaf=50, l2_regularization=1.0,
        early_stopping=False, random_state=seed,
    )

def fit_oof(dev_file: Path, out_dir: Path, seed: int = 20260918):
    df = pd.read_csv(dev_file)
    features = validate_dev(df)
    X = df[features].to_numpy(dtype=np.float64)
    base = df.base_ndcg10.to_numpy(dtype=np.float64)
    memory = df.memory_ndcg10.to_numpy(dtype=np.float64)
    targets = {"utility": memory - base, "difficulty": -base,
               "specialist": memory}
    groups = df.user_id.astype(str).to_numpy()
    splits = list(GroupKFold(n_splits=5).split(X, groups=groups))
    for tr, va in splits:
        if set(groups[tr]) & set(groups[va]):
            raise RuntimeError("user leakage across OOF fold")
    out = df[["event_id", "split", *TARGET_COLUMNS]].copy()
    out["score_uncertainty"] = -df.x_base_margin.to_numpy(dtype=np.float64)
    out["score_history"] = df.x_hist_event_count.to_numpy(dtype=np.float64)
    out_dir.mkdir(parents=True, exist_ok=True)
    model_sha = {}
    for name, y in targets.items():
        pred = np.full(len(df), np.nan, dtype=np.float64)
        for fold, (tr, va) in enumerate(splits):
            model = estimator(seed + fold)
            model.fit(X[tr], y[tr])
            pred[va] = model.predict(X[va])
        if not np.isfinite(pred).all():
            raise RuntimeError("incomplete non-finite OOF predictions")
        out["score_" + name] = pred
        final_model = estimator(seed)
        final_model.fit(X, y)
        model_path = out_dir / (name + ".joblib")
        joblib.dump(final_model, model_path, compress=3)
        model_sha[name] = sha256(model_path)
    oof_csv = out_dir / "dev_oof.csv"
    out = out[["event_id", "split", *TARGET_COLUMNS] +
              ["score_" + m for m in ALL_METHODS]]
    out.to_csv(oof_csv, index=False, float_format="%.12g")
    manifest = {
        "schema": "kbs-plan-c-oof-v1",
        "phase": "DEV",
        "predictions_are_oof": True,
        "user_disjoint_across_folds": True,
        "n_splits": 5,
        "n_dev_events": len(df),
        "unique_dev_users": int(df.user_id.nunique()),
        "feature_columns": features,
        "user_group_key": "user_id",
        "source_dev_sha256": sha256(dev_file),
        "provenance_sha256": sha256(oof_csv),
        "final_model_sha256": model_sha,
        "estimator": "HistGradientBoostingRegressor max_iter=200 max_depth=3 min_samples_leaf=50",
        "test_outcomes_inspected": False,
    }
    (out_dir / "oof_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest

def predict_unlabeled(features_file: Path, model_dir: Path, out: Path):
    manifest = json.loads((model_dir / "oof_manifest.json").read_text())
    df = pd.read_csv(features_file)
    features = manifest["feature_columns"]
    if df.empty or not {"event_id", "split"}.issubset(df.columns):
        raise ValueError("missing unlabeled TEST keys")
    if not df.split.eq("TEST").all() or df.event_id.isna().any() or df.event_id.duplicated().any():
        raise ValueError("bad TEST identity or split")
    if any(x in df for x in TARGET_COLUMNS) or not set(features).issubset(df.columns):
        raise ValueError("TEST outcomes not allowed; required x_* features missing")
    X = df[features].to_numpy(dtype=np.float64)
    if not np.isfinite(X).all():
        raise ValueError("non-finite pre-outcome TEST features")
    scored = df[["event_id", "split"]].copy()
    scored["score_uncertainty"] = -df.x_base_margin
    scored["score_history"] = df.x_hist_event_count
    for name in MODEL_METHODS:
        file = model_dir / (name + ".joblib")
        if sha256(file) != manifest["final_model_sha256"][name]:
            raise ValueError("model file SHA mismatch")
        model = joblib.load(file)  # load only trusted, hash-matched own artifacts
        scored["score_" + name] = model.predict(X)
    out.parent.mkdir(parents=True, exist_ok=True)
    scored = scored[["event_id", "split"] + ["score_" + m for m in ALL_METHODS]]
    scored.to_csv(out, index=False, float_format="%.12g")
    return len(scored)

def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="mode", required=True)
    fit = sp.add_parser("fit-dev-oof")
    fit.add_argument("--dev", type=Path, required=True)
    fit.add_argument("--out-dir", type=Path, required=True)
    fit.add_argument("--seed", type=int, default=20260918)
    apply = sp.add_parser("predict-unlabeled-test")
    apply.add_argument("--test-features", type=Path, required=True)
    apply.add_argument("--model-dir", type=Path, required=True)
    apply.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.mode == "fit-dev-oof":
        print(json.dumps(fit_oof(a.dev, a.out_dir, a.seed)))
    else:
        print(json.dumps({"unlabeled_rows": predict_unlabeled(
            a.test_features, a.model_dir, a.out)}))
if __name__ == "__main__":
    main()
