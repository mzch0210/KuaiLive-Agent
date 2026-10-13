#!/usr/bin/env python3
"""B2 DEV-only matched Memory evidence-ablation F/S outcome generator.

One pretarget causal history replay; one event-time active-author roster sweep.
No model fitting, GPU scoring, G5 TEST access or private row upload. B1 Base
outcomes reused byte-for-byte. full Memory must match canonical F and B1 S.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq

from b1_dev_regime_pilot import deterministic_sample
from b1_fast_roster_dev_check import availability_vectorized
from g3_dev_full_active import ndcg
from g3_replay_correct_memory import corrected_memory_score, replay_all_history, rank

FULL_N = 50049
VARIANTS = ("full", "long_only", "short_only", "popularity_only",
            "relationship_shifted")
SEED = 20261013


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def component_scores(candidate, pop, warm, recent, denom, source_event):
    """All columns reflect only histories preceding this DEV event."""
    zeros = np.zeros_like(pop)
    p = .10 * pop[candidate].astype(np.float64)
    # Use the original scorer for each component rather than a new definition.
    long = corrected_memory_score(candidate, zeros, warm, (), denom)
    short = corrected_memory_score(candidate, zeros, {}, recent, denom)
    full = (p + long) + short
    historical = long + short
    # Placebo preserves the per-event multiset of history-only scores
    # across eligible candidates while destroying alignment with author IDs.
    # The offset uses no target ID or outcome.
    shift = 1 + ((int(source_event) ^ SEED) % (len(candidate)-1))
    null = p + np.roll(historical, shift)
    return {
        "full": full,
        "long_only": long,
        "short_only": short,
        "popularity_only": p,
        "relationship_shifted": null,
    }


def run(root, out, limit):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("B2 never overwrites existing DEV artifacts")
    if limit is not None and not (16 <= limit <= 512):
        raise ValueError("B2 pilot bound must be 16 to 512")
    start = time.monotonic()
    g1 = root/"klm3_plan_c_g1_v1"
    idx = root/"klm3_g2_train_index_v1"
    dev = root/"klm3_g2_dev_checkpoint_screen_v1"
    b1 = root/"klm3_b1_full_dev_candidate_labels_seed20261012_v1"
    original = root/"klm3_g3_dev_fullactive_base_memory_corrected_v1"
    bm = json.loads((b1/"summary.json").read_text())
    om = json.loads((original/"summary.json").read_text())
    gm = json.loads((g1/"manifest.json").read_text())
    im = json.loads((idx/"index_manifest.json").read_text())
    dm = json.loads((dev/"manifest.json").read_text())
    if not (bm.get("schema") == "kbs-b1-full-dev-paired-candidate-labels-v1"
            and bm.get("status") == "PASS"
            and bm.get("scope") == "DEV_ONLY_POST_G5_EXPLORATORY"
            and not bm["test_accessed"]
            and om.get("schema") == "kbs-plan-c-full-active-dev-paired-v2"
            and om.get("memory_corrected_from_all_history") is True
            and not om["test_file_accessed"]
            and gm["protocol_sha256"] == im["g1_protocol_sha256"]
            == dm["g1_protocol_sha256"]):
        raise RuntimeError("Frozen DEV-only source provenance rejected")
    if (bm["corrected_F_source_sha256"] != om["event_csv_sha256"]
            or sha(b1/"dev_pair_candidate_labels.csv")
            != bm["private_event_source_csv_sha256"]):
        raise RuntimeError("B1 paired source SHA mismatch")
    events = np.load(dev/"dev_source_event_ids.npy", mmap_mode="r")
    targets = np.load(dev/"dev_positive_author_tokens.npy", mmap_mode="r")
    for file in ("dev_source_event_ids.npy", "dev_positive_author_tokens.npy"):
        if sha(dev/file) != dm["files_sha256"][file]:
            raise RuntimeError("DEV snapshot byte identity invalid")
    clocks_table = pq.read_table(g1/"dev_cohort.parquet",
                                  columns=["source_event_id","observed_at"])
    if not np.array_equal(clocks_table.column("source_event_id").to_numpy(),events):
        raise RuntimeError("G1 DEV row order mismatch")
    clocks = clocks_table.column("observed_at").to_pylist()
    if len(events) != FULL_N:
        raise RuntimeError("Incorrect original DEV size")
    author_ids = np.load(idx/"authors.npy",mmap_mode="r")
    known = {int(a):i+1 for i,a in enumerate(author_ids)}
    train_tokens = np.load(idx/"sequence_ids.npy", mmap_mode="r")
    counts = np.bincount(train_tokens,minlength=len(author_ids)+1)
    lp = np.log1p(counts.astype(np.float64))
    popularity = np.zeros(len(counts),dtype=np.float64)
    popularity[1:] = (lp[1:]-lp[1:].min())/(lp[1:].max()-lp[1:].min())

    with (b1/"dev_pair_candidate_labels.csv").open(newline="") as fh:
        reader = csv.DictReader(fh)
        input_columns = reader.fieldnames or []
        base_rows = {int(row["event_id"]):row for row in reader}
    if len(base_rows) != FULL_N or any(int(e) not in base_rows for e in events):
        raise RuntimeError("B1 matched cohort missing or duplicated")
    choose = (np.arange(FULL_N,dtype=np.int64) if limit is None
              else np.unique(np.linspace(0,FULL_N-1,limit,dtype=np.int64)))
    if limit is not None and len(choose) != limit:
        raise RuntimeError("Unexpected pilot subset")
    subset_events = np.asarray(events[choose],dtype=np.int64)
    replay_start = time.monotonic()
    snapshots, scanned = replay_all_history(
        g1/"causal_stream_sealed.parquet",subset_events,known)
    hist_elapsed = time.monotonic()-replay_start
    roster_start = time.monotonic()
    summaries = {k:{"f":[],"s":[]} for k in VARIANTS}
    ranks_mismatch = {"F":0,"S":0}
    rows_private = []
    missed = 0
    for ix,candidate,_ in availability_vectorized(
            g1/"available_room_intervals.parquet",
            [clocks[i] for i in choose],
            np.asarray(targets[choose]),known,len(author_ids)):
        full_id = int(choose[ix])
        event_id = int(events[full_id])
        y = int(targets[full_id])
        prev = base_rows[event_id]
        if int(prev["candidate_count"]) != len(candidate):
            raise RuntimeError("B2 full eligible author roster differs from B1")
        s = deterministic_sample(candidate,y,event_id)
        selected = np.searchsorted(candidate,s)
        if not np.array_equal(candidate[selected],s) or len(s)!=575:
            raise RuntimeError("Invalid deterministic sampled candidate subset")
        warm,recent,long_max = snapshots[ix]
        scores = component_scores(candidate,popularity,warm,recent,long_max,event_id)
        newrow = dict(prev) if limit is None else None
        for variant in VARIANTS:
            fullscores = scores[variant]
            f = ndcg(rank(candidate,fullscores,y))
            smallscores=fullscores[selected]
            sampled = ndcg(rank(s,smallscores,y))
            summaries[variant]["f"].append(f)
            summaries[variant]["s"].append(sampled)
            if variant == "full":
                if abs(f-float(prev["memory_ndcg10"])) > 1e-12:
                    ranks_mismatch["F"] += 1
                if abs(sampled-float(prev["sampled_memory_ndcg10"])) > 1e-12:
                    ranks_mismatch["S"] += 1
            if newrow is not None and variant != "full":
                newrow["b2_"+variant+"_F_ndcg10"]=repr(f)
                newrow["b2_"+variant+"_S_ndcg10"]=repr(sampled)
        if newrow is not None:
            rows_private.append(newrow)
        if (ix+1)%10000==0:
            print(json.dumps({"phase":"B2_memory_sources_DEV_only",
                              "checked":ix+1,"elapsed_seconds":round(time.monotonic()-start,2)}),flush=True)
    roster_elapsed = time.monotonic()-roster_start
    if limit is not None and ranks_mismatch["F"]+ranks_mismatch["S"]:
        raise RuntimeError("HARD STOP: full Memory must exactly reproduce original F and B1 S")
    if sum(len(x["f"]) for x in summaries.values())!=len(choose)*len(VARIANTS):
        raise RuntimeError("Partial B2 variant score coverage")
    report = {
        "schema":"kbs-b2-dev-relationship-source-ablation-v1",
        "scope":"POST_G5_DEV_EXPLORATORY",
        "status":"PASS" if not any(ranks_mismatch.values()) else "HOLD_PARITY",
        "new_TEST_opened":False,
        "models_retrained":False,
        "private_ids_exported":False,
        "candidate_labels_target_retained_offline_only":True,
        "sampled_size":575,
        "n_events":len(choose),
        "n_users":None if limit is not None else len({r["user_id"] for r in base_rows.values()}),
        "variants":list(VARIANTS),
        "full_memory_nDCG_mismatches":ranks_mismatch,
        "source_b1_pair_sha256":bm["private_event_source_csv_sha256"],
        "source_b1_original_F_sha256":om["event_csv_sha256"],
        "relations_placement_shift_seed":SEED,
        "relation_null_type":"within_event_nonzero_cyclic_history_score_rotation",
        "source_means":{k:{"F_memory_ndcg10":float(np.mean(a["f"])),
                           "S_memory_ndcg10":float(np.mean(a["s"]))}
                        for k,a in summaries.items()},
        "history_replay_events_scanned":int(scanned),
        "wall_seconds":{"historical_cpu":round(hist_elapsed,2),
                        "roster_and_five_source_scores_cpu":round(roster_elapsed,2),
                        "overall":round(time.monotonic()-start,2)},
        "b2_nested_policy_fit":False,
        "is_full_cohort":limit is None,
    }
    if limit is not None and not any(ranks_mismatch.values()):
        report["pilot_parity"]="PASS_FROZEN_F_AND_B1_S"
    if limit is None and not any(ranks_mismatch.values()):
        stage=out.with_name(out.name+".incomplete")
        stage.mkdir(parents=True,mode=0o700)
        destination=stage/"dev_memory_source_ablation_pairs.csv"
        newcols = [f"b2_{variant}_{regime}_ndcg10" for variant in VARIANTS
                   if variant!="full" for regime in ("F","S")]
        with destination.open("w",newline="") as fh:
            writer=csv.DictWriter(fh,fieldnames=input_columns+newcols)
            writer.writeheader()
            writer.writerows(rows_private)
        report["private_event_source_csv_sha256"]=sha(destination)
        (stage/"summary.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
        stage.rename(out)
    else:
        out.mkdir(parents=True,mode=0o700)
        (out/"summary.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":report["status"],"n_events":len(choose),
                      "parity":ranks_mismatch,"means":report["source_means"],
                      "elapsed":report["wall_seconds"]}),flush=True)
    if any(ranks_mismatch.values()):
        raise RuntimeError("B2 score parity mismatch; future B2 stages remain HOLD")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--limit",type=int)
    args=ap.parse_args()
    run(args.root,args.out,args.limit)


if __name__=="__main__":
    main()
