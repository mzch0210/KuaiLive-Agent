#!/usr/bin/env python3
"""Read-only Plan C G0-D full data audit; aggregate source quality only.

Does not train recommenders/gates, define a test split, or calculate ranking metrics.
The audit never exports event-level user/author/room identifiers.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import csv
import hashlib
import json
import math
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DAY_MS = 86400000
ROOM_COLS = ("live_id", "author_id", "start_timestamp", "end_timestamp")
EVENT_COLS = ("user_id", "author_id", "live_id", "live_play_start_timestamp",
              "live_play_end_timestamp")
SOURCE_SHA256 = {
    "live_interaction.csv": "2db0daab66ec18062d453cdbbc43cbb44f75559914ef53756dfd6635812ec653",
    "live_room_meta.parquet": "130986065f8fff7cb1146a7c6508979cf0df60f39a7d923f35003e1f29f0599a",
}


def number(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def timestamp_ms(v):
    """Decode real KLM3 ISO-8601 CSV and Arrow datetime[us] values as epoch ms.

    Original timestamps have no timezone suffix; assign UTC for consistent
    within-dataset comparisons. This is an analytical ordering convention,
    not a claim of documented physical UTC timezone.
    """
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        dt = v
    elif isinstance(v, (int, float)):
        return int(v)
    elif isinstance(v, str):
        clean = v.strip()
        if clean.isdigit():
            return int(clean)
        try:
            dt = datetime.fromisoformat(clean.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def sample_distribution(values):
    if not values:
        return {"n": 0}
    ordered = sorted(values)
    return {"n": len(ordered), "min": ordered[0],
            "p10": ordered[(len(ordered)-1)//10],
            "median": ordered[(len(ordered)-1)//2],
            "p90": ordered[((len(ordered)-1)*9)//10],
            "max": ordered[-1]}


def day_iso(epoch_day):
    return datetime.fromtimestamp(epoch_day*86400, tz=timezone.utc).strftime("%Y-%m-%d")


def time_quantiles(hour_hist):
    total = sum(hour_hist.values())
    if not total:
        return {}
    ordered = sorted(hour_hist.items())
    thresholds = [(name, math.ceil(total*p)) for name,p in
                  (("q70", .70), ("q85", .85))]
    result = {}
    cum = 0
    for hour,n in ordered:
        cum += n
        for name, target in thresholds:
            if name not in result and cum >= target:
                result[name] = {"utc_hour_start": datetime.fromtimestamp(
                    hour*3600, tz=timezone.utc).isoformat(),
                                "cumulative_event_fraction": round(cum/total, 6)}
    return result


def room_inventory(parquet_path, batch_size=200000):
    import pyarrow.parquet as pq
    metadata = pq.ParquetFile(parquet_path)
    missing = set(ROOM_COLS) - set(metadata.schema_arrow.names)
    if missing:
        raise ValueError("Room metadata missing fields: " + ", ".join(sorted(missing)))
    room_map = {}
    starts, ends = [], []
    counts = collections.Counter()
    for batch in metadata.iter_batches(columns=list(ROOM_COLS),
                                        batch_size=batch_size):
        col = [batch.column(i).to_pylist() for i in range(4)]
        for raw_room, raw_author, raw_start, raw_end in zip(*col):
            counts["rows"] += 1
            room = number(raw_room)
            author = number(raw_author)
            start = timestamp_ms(raw_start)
            end = timestamp_ms(raw_end)
            if None in (room, author, start, end):
                counts["missing_identity_or_time"] += 1
                continue
            if end <= start:
                counts["invalid_lifecycle"] += 1
                continue
            if room in room_map:
                counts["duplicate_room_id"] += 1
                old = room_map[room]
                if old != (author, start, end):
                    counts["conflicting_room_id"] += 1
                continue
            room_map[room] = (author, start, end)
            starts.append(start)
            ends.append(end)
    starts.sort()
    ends.sort()
    return room_map, starts, ends, dict(counts), metadata.metadata.num_rows


def audit_events(csv_path, room_map, starts, ends, report_stride=1000000,
                 sample_stride=2500, max_rows=None):
    count = collections.Counter()
    users = collections.Counter()
    authors = set()
    seen_pairs = set()
    per_user_authors = collections.Counter()
    daily = collections.Counter()
    hourly = collections.Counter()
    mins = {"event_ts": None, "event_end_ts": None}
    maxs = {"event_ts": None, "event_end_ts": None}
    prev_timestamp = None
    candidate_counts = []
    t0 = time.monotonic()
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        missing = set(EVENT_COLS) - set(header)
        if missing:
            raise ValueError("Interaction CSV missing fields: " + ", ".join(sorted(missing)))
        idx = {name: header.index(name) for name in EVENT_COLS}
        for line in reader:
            count["rows"] += 1
            k = count["rows"]
            if max_rows and k > max_rows:
                count["rows"] -= 1
                break
            if len(line) < len(header):
                count["truncated_csv_rows"] += 1
                continue
            user = number(line[idx["user_id"]])
            author = number(line[idx["author_id"]])
            room = number(line[idx["live_id"]])
            stamp = timestamp_ms(line[idx["live_play_start_timestamp"]])
            end_stamp = timestamp_ms(line[idx["live_play_end_timestamp"]])
            if None in (user, author, room, stamp):
                count["missing_required_values"] += 1
                continue
            if not 10**12 <= stamp < 10**14:
                count["timestamp_not_epoch_ms"] += 1
                continue
            if end_stamp is None:
                count["missing_event_end"] += 1
            elif end_stamp < stamp:
                count["event_end_before_start"] += 1
            users[user] += 1
            authors.add(author)
            pair = (user << 32) | author if 0 <= user < (1<<32) and 0 <= author < (1<<32) else (user,author)
            if pair in seen_pairs:
                count["pair_repeat_ever"] += 1
            else:
                seen_pairs.add(pair)
                per_user_authors[user] += 1
            day = stamp // DAY_MS
            daily[day] += 1
            hourly[stamp // 3600000] += 1
            if mins["event_ts"] is None or stamp < mins["event_ts"]:
                mins["event_ts"] = stamp
            if maxs["event_ts"] is None or stamp > maxs["event_ts"]:
                maxs["event_ts"] = stamp
            if end_stamp is not None:
                if mins["event_end_ts"] is None or end_stamp < mins["event_end_ts"]:
                    mins["event_end_ts"] = end_stamp
                if maxs["event_end_ts"] is None or end_stamp > maxs["event_end_ts"]:
                    maxs["event_end_ts"] = end_stamp
            if prev_timestamp is not None and stamp < prev_timestamp:
                count["raw_file_backward_time_steps"] += 1
            prev_timestamp = stamp
            entry = room_map.get(room)
            if entry is None:
                count["room_id_unmatched"] += 1
            else:
                count["room_id_matched"] += 1
                m_author, start, end = entry
                if m_author != author:
                    count["room_author_mismatch"] += 1
                if not start <= stamp < end:
                    count["entry_outside_room_lifecycle"] += 1
                if end_stamp is not None and end_stamp > end:
                    count["exit_after_room_end"] += 1
            if starts and k % sample_stride == 0:
                # Exact active *room* count at this timestamp, not active authors.
                available = bisect.bisect_right(starts, stamp) - bisect.bisect_right(ends, stamp)
                candidate_counts.append(available)
            if report_stride and k % report_stride == 0:
                print(json.dumps({"progress_events": k,
                    "elapsed_seconds": round(time.monotonic()-t0,1)}),flush=True)
    date_min = day_iso(min(daily)) if daily else None
    date_max = day_iso(max(daily)) if daily else None
    daily_json = {day_iso(day): n for day,n in sorted(daily.items())}
    n_users_ge = {str(k): sum(v >= k for v in users.values()) for k in (2,5,10,20)}
    n_author_ge = {str(k): sum(v >= k for v in per_user_authors.values()) for k in (2,5,10)}
    return {
        "events": dict(count), "unique_users": len(users),
        "unique_authors": len(authors),
        "unique_user_author_pairs": len(seen_pairs),
        "users_with_at_least_n_interactions": n_users_ge,
        "users_with_at_least_n_distinct_authors": n_author_ge,
        "per_user_event_count": sample_distribution(list(users.values())),
        "per_user_distinct_author_count": sample_distribution(list(per_user_authors.values())),
        "file_min_max_timestamp_ms": {"min": mins, "max": maxs},
        "utc_event_date_range": {"first": date_min, "last": date_max},
        "utc_daily_event_counts": daily_json,
        "global_count_based_hour_cutoff_proposals_not_frozen": time_quantiles(hourly),
        "sampled_exact_live_room_candidates": sample_distribution(candidate_counts),
        "sample_stride": sample_stride,
        "time_processing_seconds": round(time.monotonic()-t0,2),
        "interpretation": ("pair_repeat_ever is dataset-wide structural recurrence, "
                           "NOT a causal pre-target relationship classification; "
                           "sampled counts are live ROOMS, not unique authors; "
                           "global cutoff proposals are descriptive, NOT a frozen split."),
    }


def check_sha256(path, expected):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(8*1024*1024), b""):
            h.update(part)
    if h.hexdigest() != expected:
        raise ValueError("source digest mismatch for " + path.name)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--sample-stride", type=int, default=2500)
    p.add_argument("--skip-digest", action="store_true",
                   help="For tests ONLY: production workflow must not use.")
    a = p.parse_args()
    if a.sample_stride < 1:
        p.error("sample-stride must be positive")
    for name, sha in SOURCE_SHA256.items():
        if not (a.root / name).is_file():
            raise FileNotFoundError("Missing official source file: " + name)
        if not a.skip_digest:
            check_sha256(a.root / name, sha)
    rooms, starts, ends, room_counts, rows = room_inventory(
        a.root / "live_room_meta.parquet")
    print(json.dumps({"phase":"room_index_built",
                      "room_rows":rows,"valid_room_ids":len(rooms)}),flush=True)
    events = audit_events(a.root / "live_interaction.csv", rooms, starts, ends,
                          sample_stride=a.sample_stride)
    if not rooms or not events["unique_users"]:
        raise ValueError("G0-D INVALID: no valid room or user identities parsed")
    if events["events"].get("missing_required_values", 0) > 0.05 * events["events"]["rows"]:
        raise ValueError("G0-D INVALID: over 5% of events have missing required values")
    report = {
        "schema":"kbs-plan-c-g0d-full-aggregate-v2",
        "timestamp_parse_protocol":"ISO CSV and Arrow datetime[us] normalized to epoch ms; naive wall clock treated as UTC ordering convention",
        "source_revision":"138d213a23e261ed3094d27ed8a4b867fb9143fe",
        "source_sha256":SOURCE_SHA256,
        "sha256_reverified":not a.skip_digest,
        "room_meta_rows_from_footer":rows,
        "room_meta_audit":room_counts,
        "valid_room_ids":len(rooms),
        "streaming_interaction_audit":events,
        "original_kuailive_official_collection_dates":
            ["2025-05-05","2025-05-25"],
        "m3_official_collection_dates":["2026-03-04","2026-03-31"],
        "two_official_collection_windows_overlap":False,
        "cross_dataset_user_identity_overlap_verified":False,
        "no_user_id_equality_claim_across_anonymized_sources":True,
        "no_event_level_rows_exported":True,
        "no_test_ranking_metrics_computed":True,
        "no_model_trained":True,
        "decision":"PENDING_HUMAN_REVIEW_OF_ELIGIBILITY_AND_PROTOCOL_FREEZE",
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"stage":"complete","events":events["events"].get("rows"),
                      "users":events["unique_users"],"date_range":
                      events["utc_event_date_range"],"no_test_metrics":True}),flush=True)


if __name__=="__main__":
    main()
