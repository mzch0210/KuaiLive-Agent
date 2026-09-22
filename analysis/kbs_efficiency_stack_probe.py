from __future__ import annotations

import argparse
import json
import pickle
import resource
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch

from room_level_selective_agent import histories, load_data, popularity_by_streamer


def tensor_bytes(state) -> int:
    total = 0
    for v in state.values():
        if torch.is_tensor(v):
            total += int(v.numel() * v.element_size())
    return total


def rss_mb() -> float:
    # Linux ru_maxrss is KiB.
    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--room-ckpt", type=Path, required=True)
    ap.add_argument("--streamer-ckpt", type=Path, required=True)
    ap.add_argument("--gate-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    stages = {"after_imports_peak_rss_mb": rss_mb()}
    room_state = torch.load(args.room_ckpt, map_location="cpu")
    stages["after_room_checkpoint_peak_rss_mb"] = rss_mb()
    streamer_state = torch.load(args.streamer_ckpt, map_location="cpu")
    stages["after_dual_checkpoints_peak_rss_mb"] = rss_mb()

    hgb_path = next(args.gate_dir.rglob("hgb_gate.joblib"))
    light_path = next(args.gate_dir.rglob("light_gate_params.npz"))
    _hgb = joblib.load(hgb_path)
    light = np.load(light_path)
    stages["after_gates_peak_rss_mb"] = rss_mb()

    train, dev, _test, item_to_streamer = load_data(args.data_dir, 574)
    pop = popularity_by_streamer(train, item_to_streamer)
    train_dev = pd.concat([train, dev[["user_id", "item_id", "time"]]], ignore_index=True)
    hist = histories(train_dev, item_to_streamer)
    memory_cache_bytes = len(pickle.dumps((pop, hist), protocol=pickle.HIGHEST_PROTOCOL))
    stages["after_memory_cache_peak_rss_mb"] = rss_mb()

    light_arrays_bytes = int(sum(light[k].nbytes for k in light.files))
    report = {
        "experiment": "kbs_efficiency_loaded_stack_memory_probe",
        "scope": "single-process materialization of both frozen Dual-ID checkpoints, all gate artifacts, and cached MemoryFusion relationship state",
        "room_checkpoint_file_bytes": int(args.room_ckpt.stat().st_size),
        "streamer_checkpoint_file_bytes": int(args.streamer_ckpt.stat().st_size),
        "room_state_tensor_bytes": tensor_bytes(room_state),
        "streamer_state_tensor_bytes": tensor_bytes(streamer_state),
        "hgb_joblib_bytes": int(hgb_path.stat().st_size),
        "light_gate_npz_file_bytes": int(light_path.stat().st_size),
        "light_gate_array_bytes": light_arrays_bytes,
        "memory_cache_pickle_bytes": int(memory_cache_bytes),
        "users_in_cached_history": int(len(hist)),
        "streamers_in_popularity_cache": int(len(pop)),
        "loaded_stack_peak_rss_mb": rss_mb(),
        "rss_stages": stages,
        "guardrail": "Peak RSS is a deployed-stack process-level measurement on the GitHub-hosted CPU runner, not a hardware-independent model-memory invariant. Serialized/tensor footprints are reported separately for portability.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
