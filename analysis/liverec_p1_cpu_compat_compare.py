from __future__ import annotations

import argparse
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
STATE_TOL = 1e-12
CONF_TOL = 1e-5
MAX_RECOMMENDED_EXPORT_SECONDS = 4.5 * 60.0 * 60.0


def hgb() -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=50,
        l2_regularization=1.0,
        random_state=SEED,
    )


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


def mismatch_count(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.count_nonzero(np.asarray(a) != np.asarray(b)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cpu-dev-events", type=Path, required=True)
    ap.add_argument("--cpu-summary", type=Path, required=True)
    ap.add_argument("--gpu-dev-oof", type=Path, required=True)
    ap.add_argument("--utility-gate", type=Path, required=True)
    ap.add_argument("--gate-report", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    cpu = pd.read_csv(args.cpu_dev_events)
    gpu = pd.read_csv(args.gpu_dev_oof)
    summary = json.loads(args.cpu_summary.read_text())
    gate_report = json.loads(args.gate_report.read_text())
    utility_bundle = joblib.load(args.utility_gate)

    if summary.get("split") != "dev" or summary.get("test_ranking_inspected") is not False:
        raise RuntimeError("CPU compatibility input must be dev-only")
    if str(summary.get("execution_device")) != "cpu":
        raise RuntimeError(f"Expected CPU dev export, got {summary.get('execution_device')!r}")
    if len(cpu) != 46878 or len(gpu) != 46878:
        raise RuntimeError(f"Unexpected dev row counts: CPU={len(cpu)}, GPU={len(gpu)}")
    if utility_bundle.get("features") != FEATURES or gate_report.get("features") != FEATURES:
        raise RuntimeError("Frozen utility feature order mismatch")

    identity_cols = ["user_id", "target_step", "target_streamer", "candidate_count"]
    discrete_cols = identity_cols + [
        "official_repeat",
        "relationship_horizon",
        "base_rank0",
        "memory_rank0",
        "base_h10",
        "memory_h10",
    ]
    missing = sorted(set(discrete_cols + FEATURES + ["base_ndcg10", "memory_ndcg10"]) - set(cpu.columns))
    missing += [f"gpu:{c}" for c in sorted(set(discrete_cols + FEATURES + ["base_ndcg10", "memory_ndcg10"]) - set(gpu.columns))]
    if missing:
        raise RuntimeError(f"Missing compatibility columns: {missing}")

    identity_mismatches = {c: mismatch_count(cpu[c].to_numpy(), gpu[c].to_numpy()) for c in identity_cols}
    if any(identity_mismatches.values()):
        raise RuntimeError(f"CPU/GPU event alignment mismatch: {identity_mismatches}")

    discrete_mismatches = {c: mismatch_count(cpu[c].to_numpy(), gpu[c].to_numpy()) for c in discrete_cols}

    feature_rows = []
    state_close = True
    conf_close = True
    for c in FEATURES:
        a = cpu[c].to_numpy(float)
        b = gpu[c].to_numpy(float)
        d = np.abs(a - b)
        row = {
            "feature": c,
            "max_abs_diff": float(d.max()),
            "mean_abs_diff": float(d.mean()),
            "p99_abs_diff": float(np.quantile(d, 0.99)),
            "n_nonzero_diff": int(np.count_nonzero(d)),
        }
        feature_rows.append(row)
        if c in STATE_FEATURES:
            state_close = state_close and row["max_abs_diff"] <= STATE_TOL
        else:
            conf_close = conf_close and row["max_abs_diff"] <= CONF_TOL

    feature_df = pd.DataFrame(feature_rows)
    feature_df.to_csv(args.out_dir / "p1_3_cpu_compat_feature_diffs.csv", index=False)

    X_gpu = gpu[FEATURES].to_numpy(float)
    X_cpu = cpu[FEATURES].to_numpy(float)
    utility_model = utility_bundle["model"]
    threshold = float(utility_bundle["threshold"])
    pred_gpu = np.asarray(utility_model.predict(X_gpu), dtype=float)
    pred_cpu = np.asarray(utility_model.predict(X_cpu), dtype=float)
    use_gpu = pred_gpu > threshold
    use_cpu = pred_cpu > threshold
    utility_mask_mismatches = mismatch_count(use_gpu, use_cpu)

    y_difficulty = 1.0 - gpu.base_ndcg10.to_numpy(float)
    difficulty_model = hgb().fit(X_gpu, y_difficulty)
    difficulty_gpu = np.asarray(difficulty_model.predict(X_gpu), dtype=float)
    difficulty_cpu = np.asarray(difficulty_model.predict(X_cpu), dtype=float)
    k_gpu = int(use_gpu.sum())
    k_cpu = int(use_cpu.sum())
    difficulty_mask_gpu = top_k_mask(difficulty_gpu, k_gpu)
    difficulty_mask_cpu = top_k_mask(difficulty_cpu, k_cpu)
    difficulty_mask_mismatches = mismatch_count(difficulty_mask_gpu, difficulty_mask_cpu)

    utility_pred_diff = np.abs(pred_gpu - pred_cpu)
    difficulty_pred_diff = np.abs(difficulty_gpu - difficulty_cpu)
    base_ndcg_diff = abs(float(cpu.base_ndcg10.mean()) - float(gpu.base_ndcg10.mean()))
    memory_ndcg_diff = abs(float(cpu.memory_ndcg10.mean()) - float(gpu.memory_ndcg10.mean()))

    policy_compatible = bool(
        all(v == 0 for v in discrete_mismatches.values())
        and utility_mask_mismatches == 0
        and difficulty_mask_mismatches == 0
        and k_gpu == k_cpu
    )
    numerically_close = bool(state_close and conf_close)
    runtime_seconds = float(summary["runtime_seconds"])
    runtime_fits = runtime_seconds < MAX_RECOMMENDED_EXPORT_SECONDS
    recommended_for_hosted_test = bool(policy_compatible and numerically_close and runtime_fits)

    report = {
        "experiment": "liverec_twitch100k_p1_3_hosted_cpu_dev_compatibility",
        "test_ranking_inspected": False,
        "n_dev": int(len(cpu)),
        "cpu_export": {
            "runtime_seconds": runtime_seconds,
            "max_recommended_export_seconds": MAX_RECOMMENDED_EXPORT_SECONDS,
            "runtime_fits_with_margin": runtime_fits,
            "num_workers": int(summary.get("num_workers", -1)),
        },
        "identity_mismatches": identity_mismatches,
        "discrete_mismatches": discrete_mismatches,
        "feature_tolerances": {
            "state_features_max_abs": STATE_TOL,
            "base_confidence_features_max_abs": CONF_TOL,
            "state_features_within_tolerance": bool(state_close),
            "base_confidence_features_within_tolerance": bool(conf_close),
        },
        "utility_policy": {
            "threshold": threshold,
            "gpu_dev_final_model_k": k_gpu,
            "cpu_dev_final_model_k": k_cpu,
            "invocation_mask_mismatches": utility_mask_mismatches,
            "prediction_max_abs_diff": float(utility_pred_diff.max()),
            "prediction_mean_abs_diff": float(utility_pred_diff.mean()),
        },
        "difficulty_policy": {
            "budget_k_gpu": k_gpu,
            "budget_k_cpu": k_cpu,
            "exact_k_mask_mismatches": difficulty_mask_mismatches,
            "prediction_max_abs_diff": float(difficulty_pred_diff.max()),
            "prediction_mean_abs_diff": float(difficulty_pred_diff.mean()),
        },
        "aggregate_metric_abs_diff": {
            "base_ndcg10": base_ndcg_diff,
            "memory_ndcg10": memory_ndcg_diff,
        },
        "policy_compatible": policy_compatible,
        "numerically_close": numerically_close,
        "recommended_for_hosted_cpu_p1_3": recommended_for_hosted_test,
        "decision_rule": (
            "Hosted CPU P1.3 is recommended only if dev event/rank/policy decisions are identical, "
            "state features agree within 1e-12, base-confidence features within 1e-5, and the full dev export finishes under 4.5 hours."
        ),
    }
    (args.out_dir / "p1_3_cpu_compat_report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report, indent=2, allow_nan=False))

    # Fail closed, but only on DEV compatibility. No test has been constructed or inspected.
    if not recommended_for_hosted_test:
        raise SystemExit("Hosted CPU compatibility criteria not met; keep P1.3 on the frozen CUDA path.")


if __name__ == "__main__":
    main()
