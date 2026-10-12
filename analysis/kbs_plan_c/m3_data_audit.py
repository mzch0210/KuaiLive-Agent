#!/usr/bin/env python3
"""G0-D KLM3 field/schema audit; no split fitting, no ranking, no TEST utility."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

REQUIRED_INTERACTION = (
    "user_id", "author_id", "live_id", "live_play_start_timestamp"
)
REQUIRED_ROOM = ("live_id", "author_id", "start_timestamp", "end_timestamp")

def audit_interaction_header(path: Path, sample_rows: int = 5000) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        missing = sorted(set(REQUIRED_INTERACTION).difference(fields))
        if missing:
            raise ValueError("KLM3 live_interaction missing: " + ", ".join(missing))
        n = 0
        incomplete = 0
        for row in reader:
            n += 1
            if any(not row.get(k) for k in REQUIRED_INTERACTION):
                incomplete += 1
            if n >= sample_rows:
                break
    return {"expected_fields_present": True, "columns": fields,
            "audited_sample_rows": n, "required_values_missing_in_sample": incomplete,
            "full_file_scan": False}

def audit_room_footer(path: Path) -> dict:
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return {"footer_checked": False, "reason": "pyarrow_not_installed"}
    parquet = pq.ParquetFile(path)
    names = parquet.schema_arrow.names
    missing = sorted(set(REQUIRED_ROOM).difference(names))
    if missing:
        raise ValueError("KLM3 room metadata missing: " + ", ".join(missing))
    return {"footer_checked": True, "columns": names,
            "parquet_row_groups": parquet.metadata.num_row_groups,
            "metadata_row_count": parquet.metadata.num_rows,
            "all_rows_read": False}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    interaction = a.root / "live_interaction.csv"
    rooms = a.root / "live_room_meta.parquet"
    if not interaction.is_file() or not rooms.is_file():
        raise FileNotFoundError("expected exactly two pinned KLM3 live-domain files")
    result = {
        "stage": "KBS-PLAN-C-G0-D-FIELDS-ONLY",
        "interaction": audit_interaction_header(interaction),
        "room": audit_room_footer(rooms),
        "test_metrics_computed": False, "models_trained": False,
        "test_split_created": False, "candidate_policy_frozen": False,
        "data_gate": "HOLD_PENDING_FULL_TIME_CANDIDATE_OVERLAP_AUDIT",
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"stage": result["stage"], "interaction_sample_n":
                      result["interaction"]["audited_sample_rows"],
                      "room_footer_checked": result["room"]["footer_checked"],
                      "test_metrics_computed": False,
                      "data_gate": result["data_gate"]}))

if __name__ == "__main__":
    main()
