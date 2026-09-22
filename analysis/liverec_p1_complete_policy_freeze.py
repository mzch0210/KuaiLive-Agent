from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

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


def hgb() -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=50,
        l2_regularization=1.0,
        random_state=SEED,
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dev_reference_percentile(values: np.ndarray, sorted_ref: np.ndarray) -> np.ndarray:
    """Replay pandas rank(pct=True, method='average') for values seen in ref.

    For values not present in the development reference, use the ordinary right ECDF.
    This is a frozen, dev-reference transform; no test-distribution ranks are used.
    """
    values = np.asarray(values, dtype=float)
    ref = np.asarray(sorted_ref, dtype=float)
    if ref.ndim != 1 or ref.size == 0 or not np.all(ref[:-1] <= ref[1:]):
        raise RuntimeError("Invalid sorted development ECDF reference")
    left = np.searchsorted(ref, values, side="left")
    right = np.searchsorted(ref, values, side="right")
    out = right.astype(np.float64) / float(ref.size)
    tied = right > left
    out[tied] = (left[tied] + right[tied] + 1.0) / (2.0 * float(ref.size))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev-oof", type=Path, required=True)
    ap.add_argument("--utility-gate", type=Path, required=True)
    ap.add_argument("--gate-report", type=Path, required=True)
    ap.add_argument("--state-ecdf", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    dev = pd.read_csv(args.dev_oof)
    report = json.loads(args.gate_report.read_text())
    ecdf = json.loads(args.state_ecdf.read_text())
    utility_bundle = joblib.load(args.utility_gate)

    if report.get("test_ranking_inspected") is not False:
        raise RuntimeError("P1.2 source report is not dev-only")
    if utility_bundle.get("features") != FEATURES or report.get("features") != FEATURES:
        raise RuntimeError("Frozen utility feature ordering mismatch")
    if int(utility_bundle.get("seed")) != SEED or int(utility_bundle.get("dev_n")) != len(dev):
        raise RuntimeError("Frozen utility metadata mismatch")
    if abs(float(utility_bundle.get("threshold")) - float(report["utility_router"]["threshold"])) > 1e-15:
        raise RuntimeError("Frozen utility threshold mismatch")
    if int(utility_bundle.get("invocation_k_on_dev")) != int(report["utility_router"]["k"]):
        raise RuntimeError("Frozen utility dev invocation count mismatch")
    if dev.user_id.duplicated().any():
        raise RuntimeError("Expected one development target per user")

    required = set(FEATURES + [
        "base_ndcg10",
        "memory_ndcg10",
        "memory_delta_ndcg10",
        "utility_oof_pred",
        "preference_entropy_pct",
        "preference_drift_pct",
        "history_pct",
    ])
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"Missing frozen dev columns: {missing}")
    numeric = dev[list(required - {"user_id"})].select_dtypes(include=[np.number]).to_numpy(float)
    if not np.isfinite(numeric).all():
        raise RuntimeError("Non-finite frozen development values")

    # Freeze and verify the development-reference percentile transform needed at test time.
    mapping = {
        "preference_entropy": "preference_entropy_pct",
        "preference_drift": "preference_drift_pct",
        "log_history_len": "history_pct",
    }
    transform_max_abs_error = {}
    for raw_col, pct_col in mapping.items():
        ref = np.asarray(ecdf[raw_col], dtype=float)
        got = dev_reference_percentile(dev[raw_col].to_numpy(float), ref)
        want = dev[pct_col].to_numpy(float)
        err = float(np.max(np.abs(got - want)))
        transform_max_abs_error[raw_col] = err
        if err > 1e-12:
            raise RuntimeError(f"Development ECDF replay mismatch for {raw_col}: {err}")

    X = dev[FEATURES].to_numpy(float)
    y_difficulty = 1.0 - dev.base_ndcg10.to_numpy(float)
    difficulty_model = hgb().fit(X, y_difficulty)
    difficulty_bundle = {
        "model": difficulty_model,
        "features": FEATURES,
        "target": "1 - base_ndcg10",
        "budget_rule": "On test, select exactly K highest difficulty predictions, where K is the frozen utility-threshold invocation count on that test set; ties by stable row index.",
        "seed": SEED,
        "dev_n": int(len(dev)),
    }
    difficulty_path = args.out_dir / "p1_2_frozen_difficulty_gate.joblib"
    joblib.dump(difficulty_bundle, difficulty_path, compress=3)

    # Freeze display-only utility strata from P1.2 OOF predictions. These do not affect routing.
    _, qcut_bins = pd.qcut(
        dev.utility_oof_pred,
        10,
        retbins=True,
        duplicates="drop",
    )
    qcut_bins = np.asarray(qcut_bins, dtype=float)
    if qcut_bins.size != 11 or not np.all(np.diff(qcut_bins) > 0):
        raise RuntimeError(f"Expected 10 distinct frozen OOF utility strata, got {qcut_bins.tolist()}")
    internal_cutpoints = qcut_bins[1:-1]

    model = utility_bundle["model"]
    expected_params = {
        "max_iter": 200,
        "learning_rate": 0.05,
        "max_depth": 3,
        "min_samples_leaf": 50,
        "l2_regularization": 1.0,
        "random_state": SEED,
    }
    params = model.get_params()
    for key, value in expected_params.items():
        if params.get(key) != value:
            raise RuntimeError(f"Frozen utility HGB parameter mismatch: {key}={params.get(key)!r}")

    manifest = {
        "experiment": "liverec_twitch100k_p1_3_policy_preflight_freeze",
        "test_ranking_inspected": False,
        "source_p1_2": {
            "utility_gate_sha256": sha256(args.utility_gate),
            "gate_report_sha256": sha256(args.gate_report),
            "dev_oof_sha256": sha256(args.dev_oof),
            "state_ecdf_sha256": sha256(args.state_ecdf),
        },
        "features": FEATURES,
        "utility_rule": {
            "threshold": float(utility_bundle["threshold"]),
            "comparison": "predict(features) > threshold",
            "dev_invocation_k": int(utility_bundle["invocation_k_on_dev"]),
            "dev_n": int(utility_bundle["dev_n"]),
        },
        "difficulty_rule": {
            "target": "1 - base_ndcg10",
            "model": "HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_depth=3, min_samples_leaf=50, l2_regularization=1.0)",
            "budget": "exactly the utility router's realized test invocation count K",
            "tie_break": "stable test row index",
        },
        "oracle_rule": {
            "budget": "same realized test K",
            "ranking": "realized event-level Memory NDCG@10 - Base NDCG@10",
            "role": "analysis-only headroom",
        },
        "state_transform": {
            "reference": "P1.2 development ECDF only",
            "rule": "average-rank percentile for values tied to dev reference; right ECDF for values not present in dev reference",
            "state_complexity": "0.4*preference_entropy_pct + 0.4*preference_drift_pct + 0.2*history_pct",
            "dev_replay_max_abs_error": transform_max_abs_error,
        },
        "utility_strata": {
            "role": "display-only; never used for routing",
            "labels": [f"D{i}" for i in range(1, 11)],
            "internal_cutpoints": [float(x) for x in internal_cutpoints],
            "outer_intervals": "(-inf, first] and (last, +inf)",
        },
        "memory_rule": {
            "short_k": 10,
            "short_decay": 3.0,
            "weights": {"short": 0.45, "long": 0.45, "popularity": 0.10},
            "unchanged_from_p1_2": True,
        },
        "difficulty_gate_sha256": sha256(difficulty_path),
        "freeze_rule": "No Memory weights, feature set, HGB family/hyperparameters, utility threshold, state transform, difficulty budget rule, or test policy may change after this preflight. P1.3 is one-shot.",
    }
    (args.out_dir / "p1_3_policy_manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    print(json.dumps(manifest, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
