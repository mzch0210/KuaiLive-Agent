#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

RECORD_API = "https://zenodo.org/api/records/16565801"
TARGET_KEY = "KuaiLive.zip"


def urlopen_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "KuaiLive-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def stream_download(url: str, out: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "KuaiLive-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, out.open("wb") as f:
        shutil.copyfileobj(r, f, length=1024 * 1024)


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def locate_dataset(root: Path) -> Path:
    candidates = []
    for p in root.rglob("click.csv"):
        parent = p.parent
        if (parent / "room.csv").exists():
            candidates.append(parent)
    if not candidates:
        raise FileNotFoundError("Could not locate a directory containing both click.csv and room.csv after extraction")
    candidates.sort(key=lambda p: len(p.parts))
    return candidates[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", type=Path, default=Path("data"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    args.data_root.mkdir(parents=True, exist_ok=True)
    archive = args.data_root / TARGET_KEY
    extract_root = args.data_root / "raw"
    marker = args.data_root / "dataset_dir.txt"

    if marker.exists() and not args.force:
        p = Path(marker.read_text().strip())
        if (p / "click.csv").exists() and (p / "room.csv").exists():
            print(p)
            return

    meta = urlopen_json(RECORD_API)
    file_meta = next((f for f in meta.get("files", []) if f.get("key") == TARGET_KEY), None)
    if not file_meta:
        raise RuntimeError(f"{TARGET_KEY} not present in Zenodo record")
    expected_size = int(file_meta.get("size", 0))
    checksum = str(file_meta.get("checksum", ""))
    expected_md5 = checksum.split(":", 1)[1] if checksum.startswith("md5:") else None
    download_url = (file_meta.get("links") or {}).get("self") or (file_meta.get("links") or {}).get("content")
    if not download_url:
        raise RuntimeError("Zenodo metadata did not expose a download URL")

    need_download = args.force or not archive.exists() or archive.stat().st_size != expected_size
    if need_download:
        tmp = archive.with_suffix(".zip.part")
        tmp.unlink(missing_ok=True)
        print(f"Downloading {TARGET_KEY} ({expected_size/1024/1024:.1f} MiB) from Zenodo...", flush=True)
        stream_download(download_url, tmp)
        tmp.replace(archive)

    actual_size = archive.stat().st_size
    if expected_size and actual_size != expected_size:
        raise RuntimeError(f"Size mismatch: expected {expected_size}, got {actual_size}")
    if expected_md5:
        actual_md5 = md5_file(archive)
        if actual_md5.lower() != expected_md5.lower():
            raise RuntimeError(f"MD5 mismatch: expected {expected_md5}, got {actual_md5}")
        print(f"MD5 OK: {actual_md5}")

    if args.force and extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)
    if not any(extract_root.iterdir()):
        print("Extracting archive...", flush=True)
        with zipfile.ZipFile(archive) as zf:
            bad = zf.testzip()
            if bad:
                raise RuntimeError(f"Corrupt member in zip: {bad}")
            zf.extractall(extract_root)

    dataset_dir = locate_dataset(extract_root).resolve()
    marker.write_text(str(dataset_dir) + "\n")
    print(dataset_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
