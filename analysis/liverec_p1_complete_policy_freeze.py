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
    """Average-rank percentile on exact dev-reference ties; right ECDF otherwise."""
    values = np.asarray(values, dtype=float)
    ref = np.asarray(sorted_ref, dtype=float)
    if ref.ndim != 1 or ref.size == 0 or not np.isfinite(ref).all() or not np.all(ref[:-1] <= ref[1:]):
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
        "user_id",
    ])
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"Missing frozen dev columns: {missing}")
    numeric_cols = [c for c in required if c != "user_id"]
    if not np.isfinite(dev[numeric_cols].to_numpy(float)).all():
        raise RuntimeError("Non-finite frozen development values")

    # The ECDF JSON was written from the original in-memory floats, while the CSV may
    # round some near-identical floats (e.g. values near 1.0). Validate the ECDF
    # against itself, not against re-parsed CSV raw values.
    ecdf_self_error = {}
    ecdf_lengths = {}
    for raw_col in ["preference_entropy", "preference_drift", "log_history_len"]:
        ref = np.asarray(ecdf[raw_col], dtype=float)
        if len(ref) != len(dev):
            raise RuntimeError(f"Frozen ECDF length mismatch for {raw_col}: {len(ref)} != {len(dev)}")
        got = dev_reference_percentile(ref, ref)
        want = pd.Series(ref).rank(pct=True, method="average").to_numpy(float)
        err = float(np.max(np.abs(got - want)))
        ecdf_self_error[raw_col] = err
        ecdf_lengths[raw_col] = int(len(ref))
        if err > 1e-15:
            raise RuntimeError(f"Frozen ECDF self-replay mismatch for {raw_col}: {err}")

    replayed_state_complexity = (
        0.4 * dev.preference_entropy_pct.to_numpy(float)
        + 0.4 * dev.preference_drift_pct.to_numpy(float)
        + 0.2 * dev.history_pct.to_numpy(float)
    )
    state_complexity_error = float(
        np.max(np.abs(replayed_state_complexity - dev.state_complexity.to_numpy(float)))
    )
    if state_complexity_error > 1e-12:
        raise RuntimeError(f"Frozen state-complexity formula mismatch: {state_complexity_error}")

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
            "reference": "P1.2 state_ecdf.json generated from original in-memory dev floats",
            "rule": "average-rank percentile for values tied to dev reference; right ECDF for values not present in dev reference",
            "state_complexity": "0.4*preference_entropy_pct + 0.4*preference_drift_pct + 0.2*history_pct",
            "ecdf_reference_lengths": ecdf_lengths,
            "ecdf_self_replay_max_abs_error": ecdf_self_error,
            "state_complexity_csv_replay_max_abs_error": state_complexity_error,
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
