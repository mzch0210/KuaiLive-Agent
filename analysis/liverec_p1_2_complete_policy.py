from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

SEED = 20260918


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oof", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--utility-gate", type=Path, required=True)
    ap.add_argument("--state-ecdf", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    report = json.loads(args.report.read_text())
    if report.get("test_ranking_inspected") is not False:
        raise RuntimeError("P1.2 report does not certify untouched test")
    if "Do not alter" not in report.get("freeze_rule", ""):
        raise RuntimeError("P1.2 freeze rule missing")

    frozen = joblib.load(args.utility_gate)
    features = list(frozen["features"])
    threshold = float(frozen["threshold"])
    if abs(threshold - float(report["utility_router"]["threshold"])) > 1e-15:
        raise RuntimeError("Frozen utility threshold mismatch")
    if int(frozen["dev_n"]) != int(report["memory_minus_base"]["n"]):
        raise RuntimeError("Frozen utility gate dev_n mismatch")
    if int(frozen["seed"]) != SEED:
        raise RuntimeError("Frozen utility gate seed mismatch")

    dev = pd.read_csv(args.oof)
    required = set(
        features
        + [
            "base_ndcg10",
            "memory_ndcg10",
            "memory_delta_ndcg10",
            "utility_oof_pred",
            "difficulty_oof_pred",
            "use_utility",
            "use_difficulty",
            "user_id",
        ]
    )
    missing = sorted(required - set(dev.columns))
    if missing:
        raise RuntimeError(f"P1.2 OOF file missing columns: {missing}")
    if len(dev) != int(frozen["dev_n"]) or dev.user_id.duplicated().any():
        raise RuntimeError("P1.2 OOF population mismatch")

    numeric = dev[features + ["base_ndcg10", "memory_ndcg10", "memory_delta_ndcg10", "utility_oof_pred", "difficulty_oof_pred"]].to_numpy(float)
    if not np.isfinite(numeric).all():
        raise RuntimeError("Non-finite P1.2 frozen dev values")

    X = dev[features].to_numpy(float)
    base = dev.base_ndcg10.to_numpy(float)
    memory = dev.memory_ndcg10.to_numpy(float)
    y_utility = dev.memory_delta_ndcg10.to_numpy(float)
    y_difficulty = 1.0 - base

    # Reproduce the frozen OOF policy exactly before adding the missing final
    # difficulty model. This is a protocol-completeness check, not retuning.
    use_utility = dev.utility_oof_pred.to_numpy(float) > threshold
    if not np.array_equal(use_utility, dev.use_utility.astype(bool).to_numpy()):
        raise RuntimeError("Frozen utility threshold no longer reproduces OOF use mask")
    k = int(use_utility.sum())
    if k != int(report["utility_router"]["k"]):
        raise RuntimeError("Frozen utility invocation count mismatch")

    use_difficulty = top_k_mask(dev.difficulty_oof_pred.to_numpy(float), k)
    if not np.array_equal(use_difficulty, dev.use_difficulty.astype(bool).to_numpy()):
        raise RuntimeError("Frozen exact-K difficulty mask mismatch")

    utility_score = float(np.where(use_utility, memory, base).mean())
    difficulty_score = float(np.where(use_difficulty, memory, base).mean())
    if abs(utility_score - float(report["utility_router"]["ndcg10"])) > 1e-12:
        raise RuntimeError("Frozen utility score mismatch")
    if abs(difficulty_score - float(report["difficulty_router_exact_k"]["ndcg10"])) > 1e-12:
        raise RuntimeError("Frozen difficulty score mismatch")

    # Verify that the persisted utility model is exactly reproducible from the
    # frozen family/features/target, then fit the missing final difficulty HGB.
    refit_utility = hgb().fit(X, y_utility)
    loaded_pred = np.asarray(frozen["model"].predict(X), dtype=float)
    refit_pred = np.asarray(refit_utility.predict(X), dtype=float)
    if not np.allclose(loaded_pred, refit_pred, rtol=0.0, atol=1e-12):
        raise RuntimeError("Persisted utility HGB is not reproducible from frozen dev inputs")

    final_difficulty = hgb().fit(X, y_difficulty)
    difficulty_pred = np.asarray(final_difficulty.predict(X), dtype=float)
    if not np.isfinite(difficulty_pred).all():
        raise RuntimeError("Non-finite final difficulty predictions")

    # Frozen dev OOF cut points are only for descriptive test strata. They do
    # not affect the routing decision.
    q = np.linspace(0.1, 0.9, 9)
    utility_decile_cutpoints = np.quantile(dev.utility_oof_pred.to_numpy(float), q).astype(float).tolist()

    policy = {
        "utility_model": frozen["model"],
        "difficulty_model": final_difficulty,
        "features": features,
        "utility_threshold": threshold,
        "dev_invocation_k": k,
        "dev_n": int(len(dev)),
        "seed": SEED,
        "utility_decile_cutpoints_oof": utility_decile_cutpoints,
        "difficulty_target": "1 - base_ndcg10",
        "matched_budget_rule": "On each evaluation split, Difficulty and Oracle use exactly K events where K is the frozen utility-threshold router's realized invocation count on that split.",
    }
    policy_path = args.out_dir / "p1_2_complete_policy.joblib"
    joblib.dump(policy, policy_path, compress=3)

    shutil.copy2(args.state_ecdf, args.out_dir / "p1_2_state_ecdf.json")
    shutil.copy2(args.report, args.out_dir / "p1_2_dev_gate_report.json")

    manifest = {
        "experiment": "liverec_twitch100k_p1_2_policy_completion",
        "test_ranking_inspected": False,
        "scientific_protocol_changed": False,
        "completion": "Persist final same-feature difficulty HGB and dev-OOF descriptive utility-strata cutpoints required by the already frozen P1.3 protocol.",
        "features": features,
        "utility_threshold": threshold,
        "dev_invocation_k": k,
        "dev_n": int(len(dev)),
        "utility_model_reproduction_max_abs_error": float(np.max(np.abs(loaded_pred - refit_pred))),
        "source_hashes": {
            "oof_sha256": sha256_file(args.oof),
            "report_sha256": sha256_file(args.report),
            "utility_gate_sha256": sha256_file(args.utility_gate),
            "state_ecdf_sha256": sha256_file(args.state_ecdf),
        },
        "output_policy_sha256": sha256_file(policy_path),
        "freeze_rule": "No changes to MemoryFusion, feature set, HGB family/hyperparameters, utility target, utility threshold, or matched-budget rule. P1.3 remains one-shot and test must not be used for rescue tuning.",
    }
    (args.out_dir / "p1_2_complete_policy_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
