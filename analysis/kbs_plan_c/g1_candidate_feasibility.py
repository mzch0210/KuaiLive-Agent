#!/usr/bin/env python3
"""DEV-only G1 cost audit: count simultaneous unique TRAIN-known authors.

Uses the already frozen G1 Parquet cohort and room intervals. Never opens
TEST cohort or exports candidate identities.
"""
from __future__ import annotations
import argparse
import collections
import heapq
import json
import time
from pathlib import Path


def quantiles(seq):
    a = sorted(seq)
    if not a:
        return {"n": 0}
    return {"n": len(a), "min": a[0], "p10": a[(len(a)-1)//10],
            "median": a[(len(a)-1)//2], "p90": a[((len(a)-1)*9)//10],
            "max": a[-1]}


def active_author_counts(room_iter, known_authors, samples):
    samples = sorted(set(samples))
    pending = []
    active = collections.Counter()
    values = []
    i = 0
    n_rooms = 0

    def measure(t):
        while pending and pending[0][0] <= t:
            _, a = heapq.heappop(pending)
            active[a] -= 1
            if active[a] == 0:
                del active[a]
        return (len(pending), len(active))

    for start, end, author in room_iter:
        n_rooms += 1
        while i < len(samples) and samples[i] < start:
            values.append(measure(samples[i]))
            i += 1
        if i < len(samples) and author in known_authors and end > start:
            heapq.heappush(pending, (end, author))
            active[author] += 1
    while i < len(samples):
        values.append(measure(samples[i]))
        i += 1
    return {
        "sampled_dev_clock_instants": len(samples),
        "scanned_room_records": n_rooms,
        "known_author_active_room_distribution": quantiles([x[0] for x in values]),
        "distinct_known_author_candidate_distribution": quantiles([x[1] for x in values]),
        "all_sampled_instants_have_at_least_575_authors":
            bool(values) and all(x[1] >= 575 for x in values),
    }


def room_rows(path):
    import pyarrow.parquet as pq
    file = pq.ParquetFile(path)
    for batch in file.iter_batches(batch_size=131072,
                                   columns=["open_ts", "close_ts", "author_id"]):
        data = batch.to_pydict()
        yield from zip(data["open_ts"], data["close_ts"], data["author_id"])


def main():
    import pyarrow.parquet as pq
    p = argparse.ArgumentParser()
    p.add_argument("--g1", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    manifest = json.loads((args.g1/"manifest.json").read_text())
    if (manifest["schema"] != "kbs-plan-c-g1-derived-v1"
            or manifest["test_outcomes_inspected"] is not False):
        raise ValueError("Verified TEST-locked G1 required")
    known = set(pq.read_table(args.g1/"train_known_authors.parquet",
                              columns=["author_id"]).column("author_id").to_pylist())
    times = sorted(pq.read_table(args.g1/"dev_cohort.parquet",
                                 columns=["observed_at"]).column("observed_at").to_pylist())
    if len(times) < 1000:
        raise ValueError("Too few DEV events for stable candidate sampling")
    checkpoints = [times[(len(times)-1)*k//511] for k in range(512)]
    start = time.monotonic()
    distribution = active_author_counts(
        room_rows(args.g1/"available_room_intervals.parquet"), known, checkpoints)
    result = {
        "schema": "kbs-plan-c-g1-known-author-availability-v1",
        "source_protocol_sha256": manifest["protocol_sha256"],
        "train_known_authors": len(known),
        "sampling": "512 fixed order-statistic timestamps from DEV only",
        "distribution": distribution,
        "seconds": round(time.monotonic()-start, 2),
        "test_file_opened": False,
        "test_rankings_evaluated": False,
        "candidate_identifiers_exported": False,
        "models_trained": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
