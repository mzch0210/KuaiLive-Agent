#!/usr/bin/env python3
"""B1 DEV-only lossless active-author roster speedup test.

Replace repeated Python sorting of active author keys with numpy flatnonzero
over a fixed TRAIN-known token count vector. Must match frozen G3 exactly.
Never loads TEST, scores, labels beyond DEV eligibility or trains any model.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import heapq
import json
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq
from g3_dev_full_active import author_availability


def availability_vectorized(rooms_file, clock, positive, known, n_items):
    order = sorted(range(len(clock)), key=lambda i: (clock[i], i))
    pf = pq.ParquetFile(rooms_file)
    def room_events():
        for batch in pf.iter_batches(batch_size=131072,
                                     columns=["open_ts","close_ts","author_id"]):
            d = batch.to_pydict()
            yield from zip(d["open_ts"], d["close_ts"], d["author_id"])
    it = iter(room_events())
    ahead = next(it, None)
    active = np.zeros(n_items + 1, dtype=np.int32)
    heap = []
    max_rooms = 0
    for ix in order:
        t = clock[ix]
        while ahead is not None and ahead[0] <= t:
            _, end, aid = ahead
            token = known.get(int(aid))
            if token is not None and end > t:
                active[token] += 1
                heapq.heappush(heap, (end, token))
            ahead = next(it, None)
        while heap and heap[0][0] <= t:
            _, tok = heapq.heappop(heap)
            active[tok] -= 1
            if active[tok] < 0:
                raise RuntimeError("Negative active-room count")
        target = int(positive[ix])
        if active[target] == 0:
            raise RuntimeError("DEV target not active in vectorized roster")
        max_rooms = max(max_rooms, len(heap))
        yield ix, np.flatnonzero(active).astype(np.int32, copy=False), max_rooms


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=256)
    a = p.parse_args()
    if not 8 <= a.limit <= 512 or a.out.exists():
        raise RuntimeError("Invalid or overwritten B1 roster benchmark")
    root = a.root
    g1 = root / "klm3_plan_c_g1_v1"
    idx = root / "klm3_g2_train_index_v1"
    dev = root / "klm3_g2_dev_checkpoint_screen_v1"
    dd = json.loads((dev / "manifest.json").read_text())
    im = json.loads((idx / "index_manifest.json").read_text())
    gm = json.loads((g1 / "manifest.json").read_text())
    if not (gm["protocol_sha256"] == dd["g1_protocol_sha256"] == im["g1_protocol_sha256"]):
        raise RuntimeError("DEV source provenance mismatch")
    author_ids = np.load(idx / "authors.npy", mmap_mode="r")
    known = {int(author): k+1 for k, author in enumerate(author_ids)}
    positives = np.load(dev / "dev_positive_author_tokens.npy", mmap_mode="r")
    d = pq.read_table(g1 / "dev_cohort.parquet", columns=["observed_at"])
    clock = d.column("observed_at").to_pylist()
    if len(clock) != len(positives) or len(clock) != 50049:
        raise RuntimeError("DEV events misaligned")
    choose = np.unique(np.linspace(0, len(clock)-1, a.limit, dtype=np.int64))
    dates = [clock[i] for i in choose]
    y = np.asarray(positives[choose])
    roster_path = g1 / "available_room_intervals.parquet"

    start = time.monotonic()
    baseline = list(author_availability(roster_path, dates, y, known))
    baseline_seconds = time.monotonic() - start
    start = time.monotonic()
    improved = list(availability_vectorized(roster_path, dates, y, known, len(author_ids)))
    improved_seconds = time.monotonic() - start
    errors = 0
    for lhs, rhs in zip(baseline, improved):
        if lhs[0] != rhs[0] or lhs[2] != rhs[2] or not np.array_equal(lhs[1], rhs[1]):
            errors += 1
    if len(baseline) != a.limit or len(improved) != a.limit:
        raise RuntimeError("Benchmark roster count inconsistent")
    counts = [len(x[1]) for x in improved]
    report = {
        "schema":"kbs-b1-dev-vectorized-roster-benchmark-v1",
        "status":"PASS" if errors == 0 else "HOLD",
        "test_accessed":False,
        "train_fitted":False,
        "candidate_or_user_ids_exported":False,
        "dev_events":a.limit,
        "roster_identity_order_discrepancies":errors,
        "original_seconds":round(baseline_seconds,3),
        "vectorized_seconds":round(improved_seconds,3),
        "wall_speedup":round(baseline_seconds/max(improved_seconds,1e-9),3),
        "candidates_min":min(counts),"candidates_max":max(counts),
        "same_original_max_rooms_statistics":errors==0,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, sort_keys=True, indent=2)+"\n")
    print(json.dumps(report, sort_keys=True), flush=True)
    if errors:
        raise RuntimeError("Fast roster is not identical to frozen implementation")

if __name__ == "__main__":
    main()
