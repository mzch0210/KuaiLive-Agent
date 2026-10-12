#!/usr/bin/env python3
"""Read-only bounded HTTP range probes for KLM3 transport. No data collection."""
from __future__ import annotations
import argparse
import json
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOSTS = ("huggingface.co", "cdn-lfs-us-1.hf.co", "cas-server.xethub.hf.co",
         "transfer.xethub.hf.co", "github.com", "api.github.com")
URLS = (
    ("hub-meta", "https://huggingface.co/api/datasets/imgkkk2004/KuaiLive-M3"),
    ("room", "https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3/resolve/138d213a23e261ed3094d27ed8a4b867fb9143fe/live_room_meta.parquet"),
    ("interaction", "https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3/resolve/138d213a23e261ed3094d27ed8a4b867fb9143fe/live_interaction.csv"),
)
def probe_url(label: str, url: str) -> dict:
    t = time.monotonic()
    req = urllib.request.Request(url, headers={
        "Range": "bytes=0-127", "User-Agent": "KBS-PlanC-TransportProbe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read(128)  # bounded; close even if server ignores Range
            return {"label": label, "ok": True, "http_status": resp.status,
                    "final_hostname": urllib.request.urlparse(resp.url).hostname,
                    "received_probe_bytes": len(data),
                    "elapsed_s": round(time.monotonic() - t, 3),
                    "no_raw_data_saved": True}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return {"label": label, "ok": False, "error": type(exc).__name__,
                "detail": str(exc)[:180], "elapsed_s": round(time.monotonic() - t, 3)}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    dns = {}
    for h in HOSTS:
        t = time.monotonic()
        try:
            records = socket.getaddrinfo(h, 443, type=socket.SOCK_STREAM)
            dns[h] = {"ok": True, "address_count": len(set(r[4][0] for r in records)),
                      "elapsed_s": round(time.monotonic() - t, 3)}
        except OSError as e:
            dns[h] = {"ok": False, "error": type(e).__name__}
    result = {"schema": "kbs-plan-c-hosted-transport-v1",
              "checked_utc": datetime.now(timezone.utc).isoformat(),
              "dns": dns,
              "probe": [probe_url(label, url) for label, url in URLS],
              "bytes_persisted_from_source": 0,
              "raw_data_uploaded": False, "test_labels_accessed": False}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"hosts": {h: v["ok"] for h, v in dns.items()},
                      "probe": [{"label": p["label"], "ok": p["ok"],
                                 "error": p.get("error")} for p in result["probe"]]}))
if __name__ == "__main__":
    main()
