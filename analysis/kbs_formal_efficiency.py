from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def mib(n: int | float) -> float:
    return float(n) / (1024.0 ** 2)


def pick(df: pd.DataFrame, system: str) -> pd.Series:
    x = df[df.system == system]
    if len(x) != 1:
        raise RuntimeError(f"expected one row for {system}, got {len(x)}")
    return x.iloc[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-final-dir", type=Path, required=True)
    ap.add_argument("--gate-accuracy-dir", type=Path, required=True)
    ap.add_argument("--inference-final-dir", type=Path, required=True)
    ap.add_argument("--stack-probe", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    gate_latency_path = next(args.gate_final_dir.rglob("pooled_latency.csv"))
    gate_curve_path = next(args.gate_final_dir.rglob("accuracy_latency_summary.csv"))
    inference_path = next(args.inference_final_dir.rglob("pooled_summary.csv"))
    gate_report_path = next(args.gate_accuracy_dir.rglob("report.json"))
    hgb_path = next(args.gate_accuracy_dir.rglob("hgb_gate.joblib"))
    light_path = next(args.gate_accuracy_dir.rglob("light_gate_params.npz"))

    gl = pd.read_csv(gate_latency_path)
    curve = pd.read_csv(gate_curve_path)
    inf = pd.read_csv(inference_path)
    gate_report = json.loads(gate_report_path.read_text())
    stack = json.loads(args.stack_probe.read_text())

    hgb = joblib.load(hgb_path)
    light = np.load(light_path)
    n_features = int(len(gate_report["features"]))
    hgb_iters = int(getattr(hgb, "n_iter_", gate_report.get("hgb_n_iter", 200)))
    hgb_depth = 3

    ridge_bytes = int(sum(light[k].nbytes for k in ["ridge_mean", "ridge_scale", "ridge_coef", "ridge_intercept"]))
    mlp_bytes = int(sum(light[k].nbytes for k in ["mlp_mean", "mlp_scale", "mlp_w1", "mlp_b1", "mlp_w2", "mlp_b2"]))

    rows = []
    specs = [
        ("Dual-ID Base", "dual_id", "O(2·(L²d + Ld² + Cd))", "O(2·(Ld + L² + Cd))", stack["room_checkpoint_file_bytes"] + stack["streamer_checkpoint_file_bytes"], "two 1-layer SASRec encoders plus candidate scoring"),
        ("Memory lookup", "memory_fusion_cached", "O(C)", "O(R_u + C)", 0, "cached per-user relationship maps; no learned parameters"),
        ("HGB gate", "gate_hgb_predict_only", f"O(TD), T≈{hgb_iters}, D≤{hgb_depth}", "O(T)", int(hgb_path.stat().st_size), "tree traversal on 14 observable features"),
        ("Ridge gate", "gate_ridge_numpy_only", f"O(F), F={n_features}", "O(F)", ridge_bytes, "linear gate including scaler arrays"),
        ("Tiny-MLP gate", "gate_tiny_mlp_numpy_only", f"O(FH+H), F={n_features}, H=16", "O(F+H)", mlp_bytes, "14-16-1 MLP including scaler arrays"),
        ("Selective HGB", "selective_hgb", "Base + Gate + p·Memory", "Base working set + cached Memory", stack["room_checkpoint_file_bytes"] + stack["streamer_checkpoint_file_bytes"] + int(hgb_path.stat().st_size), "end-to-end selective stack"),
        ("Selective Ridge", "selective_ridge", "Base + Gate + p·Memory", "Base working set + cached Memory", stack["room_checkpoint_file_bytes"] + stack["streamer_checkpoint_file_bytes"] + ridge_bytes, "end-to-end selective stack"),
        ("Selective Tiny-MLP", "selective_tiny_mlp", "Base + Gate + p·Memory", "Base working set + cached Memory", stack["room_checkpoint_file_bytes"] + stack["streamer_checkpoint_file_bytes"] + mlp_bytes, "end-to-end selective stack"),
    ]
    for label, sys, tcomp, mcomp, size_bytes, note in specs:
        r = pick(gl, sys)
        mean_ms = float(r.mean_ms)
        rows.append({
            "component": label,
            "system_key": sys,
            "time_complexity": tcomp,
            "working_memory_complexity": mcomp,
            "mean_ms": mean_ms,
            "p50_ms": float(r.p50_ms),
            "p95_ms": float(r.p95_ms),
            "throughput_qps": float(1000.0 / mean_ms) if mean_ms > 0 else None,
            "model_or_gate_footprint_mib": mib(size_bytes),
            "note": note,
        })
    table = pd.DataFrame(rows)
    table.to_csv(args.out_dir / "formal_efficiency_table.csv", index=False)

    # Preserve the invocation/accuracy frontier already measured on the identical runner.
    frontier = curve.copy()
    frontier["throughput_qps"] = 1000.0 / frontier.selective_mean_ms
    frontier.to_csv(args.out_dir / "accuracy_efficiency_frontier.csv", index=False)

    # Cross-check legacy latency evidence and expose the frozen 14.25% budget row.
    frozen = inf[inf.system == "selective_frozen_14.25pct"].copy()
    if len(frozen) != 1:
        raise RuntimeError(f"expected frozen selective latency row, got {len(frozen)}")

    summary = {
        "experiment": "kbs_formal_complexity_efficiency",
        "candidate_count_C": 575,
        "history_length_L": 50,
        "embedding_dim_d": 64,
        "gate_features_F": n_features,
        "hgb_iterations_T": hgb_iters,
        "hgb_max_depth_D": hgb_depth,
        "loaded_stack_peak_rss_mb": float(stack["loaded_stack_peak_rss_mb"]),
        "memory_cache_serialized_mib": mib(stack["memory_cache_pickle_bytes"]),
        "dual_id_checkpoint_footprint_mib": mib(stack["room_checkpoint_file_bytes"] + stack["streamer_checkpoint_file_bytes"]),
        "hgb_gate_footprint_mib": mib(hgb_path.stat().st_size),
        "ridge_gate_array_footprint_mib": mib(ridge_bytes),
        "tiny_mlp_array_footprint_mib": mib(mlp_bytes),
        "frozen_selective_mean_ms_legacy": float(frozen.iloc[0].mean_ms),
        "frozen_selective_p50_ms_legacy": float(frozen.iloc[0].p50_ms),
        "frozen_selective_p95_ms_legacy": float(frozen.iloc[0].p95_ms),
        "measurement_scope": "single-query CPU steady-state latency on identical GitHub-hosted runners; model/data parsing excluded from latency; stack peak RSS measured separately during artifact/cache materialization",
        "complexity_guardrail": "Big-O expressions characterize the implemented serving path and should not be interpreted as hardware-independent wall-clock predictions.",
    }
    (args.out_dir / "formal_efficiency_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(table.to_string(index=False))
    print("\nAccuracy-efficiency frontier:\n", frontier.to_string(index=False))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
