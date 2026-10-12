#!/usr/bin/env python3
"""Plan C G0 read-only audit: no downloads, model fitting or TEST reads."""
from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CACHE_NAMES = (
    "dual-id-paired-20260918-574-v1",
    "dual-id-paired-20260918-model-v1",
    "factorial-sasrec-seed-20260919-source-c164ec43-data-ad914135-v1",
    "factorial-sasrec-seed-20260920-source-c164ec43-data-ad914135-v1",
)
M3_FILES = ("live_interaction.csv", "live_room_meta.parquet",
            "live_room_meta.csv", "events.parquet")

def file_inventory(root: Path) -> dict:
    return {
        "root_present": root.is_dir(),
        "present_named_files": [name for name in M3_FILES if (root / name).is_file()],
        "raw_live_present": (root / "live_interaction.csv").is_file(),
        "room_meta_present": any((root / p).is_file()
                                for p in ("live_room_meta.parquet", "live_room_meta.csv")),
    }

def memory_gib():
    p = Path("/proc/meminfo")
    if not p.is_file():
        return None
    for line in p.read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return round(int(line.split()[1]) / 1024**2, 2)
    return None

def gpu_probe(mode: str) -> dict:
    if mode == "hosted":
        return {"checked": False}
    out = {"checked": True}
    exe = shutil.which("nvidia-smi")
    if exe:
        try:
            p = subprocess.run(
                [exe, "--query-gpu=name,memory.total,driver_version",
                 "--format=csv,noheader,nounits"],
                check=True, text=True, capture_output=True, timeout=10)
            out["nvidia_smi"] = p.stdout.strip().splitlines()
        except (OSError, subprocess.SubprocessError) as exc:
            out["nvidia_smi_error"] = type(exc).__name__
    try:
        import torch
        out["torch_version"] = torch.__version__
        out["cuda_available"] = bool(torch.cuda.is_available())
        if out["cuda_available"]:
            out["device"] = torch.cuda.get_device_name(0)
            out["vram_gib"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1024**3, 2)
    except (ImportError, RuntimeError, OSError) as exc:
        out["torch_error"] = type(exc).__name__
        out["cuda_available"] = False
    out["gpu_ready"] = bool(out.get("cuda_available")
                            and "3090" in out.get("device", "")
                            and out.get("vram_gib", 0) >= 23)
    return out

def audit(mode: str, cache_root: Path, m3_root: Path) -> dict:
    usage = shutil.disk_usage(cache_root if cache_root.exists() else Path.home())
    cache = {name: {
        "present": (cache_root / name).is_dir(),
        "sha_manifest_present": (cache_root / name / "SHA256SUMS").is_file()
    } for name in CACHE_NAMES}
    gpu = gpu_probe(mode)
    return {
        "schema": "kbs-plan-c-g0-v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "hardware": {"platform": platform.platform(),
                     "python": sys.version.split()[0],
                     "available_ram_gib": memory_gib(),
                     "cache_disk_free_gib": round(usage.free / 1024**3, 2)},
        "original_kuailive_cache": cache,
        "m3_probe": file_inventory(m3_root),
        "gpu": gpu,
        "infrastructure_ready": bool(mode == "user-host" and gpu.get("gpu_ready")),
        "data_gate": "HOLD_LICENSE_TIME_OVERLAP_COHORT_CHECK",
        "test_accessed": False,
        "models_trained": False,
        "data_downloaded": False,
        "note": ("This is not proof of M3 absence if files are elsewhere. "
                 "This does not identify a valid independent evaluation cohort."),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("hosted", "user-host"), required=True)
    ap.add_argument("--cache-root", type=Path,
                    default=Path.home() / ".cache/kuailive-agent-kbs")
    ap.add_argument("--m3-root", type=Path,
                    default=Path(os.environ.get("KLM3_DATA_ROOT") or
                                 str(Path.home() / ".cache/kuailive-agent-kbs/klm3")))
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = audit(args.mode, args.cache_root, args.m3_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"mode": result["mode"],
                      "infrastructure_ready": result["infrastructure_ready"],
                      "m3_raw_present": result["m3_probe"]["raw_live_present"],
                      "test_accessed": result["test_accessed"],
                      "data_gate": result["data_gate"]}))

if __name__ == "__main__":
    main()
