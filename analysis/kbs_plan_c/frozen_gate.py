#!/usr/bin/env python3
"""CPU-only DEV OOF gate freezing and unlabeled TEST mask application.

Does not train Base models, read TEST outcomes, or calculate TEST quality.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

METHODS = ("utility", "difficulty", "specialist", "uncertainty", "history")
FORBIDDEN_TEST_COLUMNS = {"base_ndcg10", "memory_ndcg10", "delta_ndcg10",
                          "target_id", "target_item_id"}

def load_rows(file: Path):
    with file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV header required")
        return set(reader.fieldnames), list(reader)

def hash_file(file: Path):
    h = hashlib.sha256()
    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def numeric(value, name):
    try:
        x = float(value)
    except (TypeError, ValueError):
        raise ValueError("invalid " + name) from None
    if not math.isfinite(x):
        raise ValueError("nonfinite " + name)
    return x

def select_threshold(scores, deltas, max_rate=0.30):
    """OOF DEV optimization for *pointwise* score>=threshold, ties indivisible."""
    n = len(scores)
    if n == 0 or n != len(deltas) or not (0 < max_rate <= 1):
        raise ValueError("invalid score, target or budget input")
    if not all(math.isfinite(x) for x in scores + deltas):
        raise ValueError("nonfinite input")
    cap = math.floor(max_rate * n)
    order = sorted(zip(scores, deltas), key=lambda pair: pair[0], reverse=True)
    best = {"threshold": None, "calls": 0, "dev_oof_gain": 0.0}
    running = 0.0
    i = 0
    while i < n:
        j = i
        while j < n and order[j][0] == order[i][0]:
            running += order[j][1]
            j += 1
        gain = running / n
        if j <= cap and gain > best["dev_oof_gain"] + 1e-14:
            best = {"threshold": order[i][0], "calls": j,
                    "dev_oof_gain": gain}
        i = j
    best["dev_oof_call_rate"] = best["calls"] / n
    return best

def freeze_dev(dev_file: Path, oof_file: Path, out_file: Path, max_rate=0.30):
    oof = json.loads(oof_file.read_text(encoding="utf-8"))
    if (oof.get("phase") != "DEV" or
            oof.get("predictions_are_oof") is not True or
            oof.get("user_disjoint_across_folds") is not True or
            len(oof.get("provenance_sha256", "")) != 64):
        raise ValueError("DEV-only user-disjoint OOF provenance required")
    cols, rows = load_rows(dev_file)
    required = {"event_id", "split", "base_ndcg10", "memory_ndcg10"}
    required |= {"score_" + m for m in METHODS}
    if not rows or not required.issubset(cols):
        raise ValueError("missing required DEV fields")
    if any(r["split"] != "DEV" for r in rows):
        raise ValueError("TEST input forbidden during fitting")
    ids = [r["event_id"] for r in rows]
    if any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("DEV event ids must be nonempty and unique")
    base = [numeric(r["base_ndcg10"], "base") for r in rows]
    memory = [numeric(r["memory_ndcg10"], "memory") for r in rows]
    if any(not 0 <= x <= 1 for x in base + memory):
        raise ValueError("NDCG must be in [0,1]")
    deltas = [m - b for b, m in zip(base, memory)]
    thresholds = {name: select_threshold(
        [numeric(r["score_" + name], name) for r in rows], deltas, max_rate)
        for name in METHODS}
    policy = {
        "schema": "kbs-plan-c-gates-v1",
        "state": "DEV_FROZEN_POINTWISE",
        "oof_source_sha256": hash_file(oof_file),
        "dev_source_sha256": hash_file(dev_file),
        "oof_provenance_sha256": oof["provenance_sha256"],
        "n_dev_events": len(rows),
        "max_call_fraction": max_rate,
        "methods": thresholds,
        "test_outcomes_seen": False,
        "note": "TEST top-m is hindsight diagnostic, not this frozen serving policy.",
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
    return policy

def apply_unlabeled(policy_file: Path, features_file: Path, out_file: Path):
    policy = json.loads(policy_file.read_text(encoding="utf-8"))
    if (policy.get("schema") != "kbs-plan-c-gates-v1" or
            policy.get("state") != "DEV_FROZEN_POINTWISE" or
            policy.get("test_outcomes_seen") is not False):
        raise ValueError("not an authorized DEV-frozen policy")
    cols, rows = load_rows(features_file)
    required = {"event_id", "split"} | {"score_" + m for m in METHODS}
    if not required.issubset(cols) or FORBIDDEN_TEST_COLUMNS & cols:
        raise ValueError("TEST policy input must contain scores, not outcome labels")
    if not rows or any(r["split"] != "TEST" for r in rows):
        raise ValueError("unlabeled TEST feature rows required")
    ids = [r["event_id"] for r in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("invalid TEST event identities")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    cols_out = ["event_id"] + ["call_" + m for m in METHODS]
    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols_out)
        writer.writeheader()
        for row in rows:
            result = {"event_id": row["event_id"]}
            for m in METHODS:
                t = policy["methods"][m]["threshold"]
                s = numeric(row["score_" + m], m)
                result["call_" + m] = int(t is not None and s >= t)
            writer.writerow(result)
    return len(rows)

def main():
    ap = argparse.ArgumentParser()
    subs = ap.add_subparsers(dest="mode", required=True)
    fit = subs.add_parser("fit-dev")
    fit.add_argument("--dev", type=Path, required=True)
    fit.add_argument("--oof-manifest", type=Path, required=True)
    fit.add_argument("--out", type=Path, required=True)
    fit.add_argument("--max-call-fraction", type=float, default=0.30)
    apply = subs.add_parser("apply-unlabeled-test")
    apply.add_argument("--policy", type=Path, required=True)
    apply.add_argument("--features", type=Path, required=True)
    apply.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.mode == "fit-dev":
        p = freeze_dev(a.dev, a.oof_manifest, a.out, a.max_call_fraction)
        print(json.dumps({"state": p["state"], "methods": p["methods"]}))
    else:
        n = apply_unlabeled(a.policy, a.features, a.out)
        print(json.dumps({"state": "MASKS_ONLY", "events": n}))

if __name__ == "__main__":
    main()
