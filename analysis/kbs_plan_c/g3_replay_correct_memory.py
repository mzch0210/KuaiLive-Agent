#!/usr/bin/env python3
"""Exact DEV-only all-history Memory correction; reuse already-computed Base ranks.

Old Memory semantics count *every* prior user-author interaction (including
authors not present in TRAIN) for short-distance and global long denominator.
Only TRAIN-known active authors can be current ranking candidates. The previous
full-active GPU Base scores are reused byte-for-byte, never recomputed.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np

from g3_dev_full_active import author_availability,ndcg


def file_sha(file):
    h=hashlib.sha256()
    with file.open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def replay_all_history(stream_file,targets,known):
    """Same source-row order as G1; enforce earlier-before-target snapshots."""
    import pyarrow.parquet as pq
    requested={int(e):i for i,e in enumerate(targets)}
    result=[None]*len(targets)
    last_user=None
    warm_count=collections.Counter()
    all_count=collections.Counter()
    recent=collections.deque(maxlen=10)
    max_all=0
    processed=0
    captured=0
    for batch in pq.ParquetFile(stream_file).iter_batches(
            batch_size=262144,columns=["source_event_id","user_id","author_id","split"]):
        data=batch.to_pydict()
        for e,user,author,split in zip(data["source_event_id"],
                                       data["user_id"],data["author_id"],data["split"]):
            if split=="TEST":
                continue
            processed+=1
            if user!=last_user:
                last_user=user
                warm_count.clear()
                all_count.clear()
                recent.clear()
                max_all=0
            position=requested.get(int(e))
            if position is not None:
                if split!="DEV" or result[position] is not None:
                    raise ValueError("Wrong DEV identity or duplicate target")
                result[position]=(dict(warm_count),tuple(recent),max_all)
                captured+=1
            key=int(author)
            all_count[key]+=1
            max_all=max(max_all,all_count[key])
            token=known.get(key,0)
            # UNKNOWN authors consume recency slots: this is the important
            # exact-horizon difference from the provisional v1 scorer.
            recent.append(token)
            if token:
                warm_count[token]+=1
    if captured!=len(targets) or any(s is None for s in result):
        raise ValueError("DEV target snapshots missing from corrected causal history")
    return result,processed


def corrected_memory_score(tokens,pop,warm_counts,recent_with_zero,long_max):
    toks=np.asarray(tokens,dtype=np.int32)
    score=.10*pop[toks].astype(np.float64)
    if warm_counts:
        if long_max <= 0:
            raise ValueError("long horizon denominator must be positive")
        ids=np.fromiter(warm_counts,dtype=np.int32,count=len(warm_counts))
        vals=np.fromiter(warm_counts.values(),dtype=np.float64,count=len(warm_counts))
        order=np.argsort(ids)
        ids,vals=ids[order],vals[order]
        loc=np.searchsorted(ids,toks)
        selected=(loc<len(ids))
        selected &= ids[np.minimum(loc,len(ids)-1)]==toks
        score[selected]+=.45*vals[loc[selected]]/long_max
    if recent_with_zero:
        short={}
        for distance,token in enumerate(reversed(recent_with_zero)):
            if token:  # unknown authors still consume a distance step
                short[token]=max(short.get(token,0.),math.exp(-distance/3.0))
        if short:
            ids=np.fromiter(sorted(short),dtype=np.int32)
            vals=np.array([short[k] for k in ids],dtype=np.float64)
            loc=np.searchsorted(ids,toks)
            selected=(loc<len(ids))
            selected &= ids[np.minimum(loc,len(ids)-1)]==toks
            score[selected]+=.45*vals[loc[selected]]
    return score


def rank(toks,scores,true_id):
    p=np.searchsorted(toks,true_id)
    if p==len(toks) or toks[p]!=true_id:
        raise ValueError("True author must appear in available warm candidate set")
    val=scores[p]
    return 1+int(np.count_nonzero((scores>val+1e-12) |
              ((np.abs(scores-val)<=1e-12)&(toks<true_id))))


def main(g1,index,dev,provisional,out):
    import pyarrow.parquet as pq
    start=time.monotonic()
    if out.exists():
        raise FileExistsError("Never overwrite an existing Memory correction")
    stage=out.with_name(out.name+".incomplete")
    if stage.exists():
        raise FileExistsError("Pre-existing partial correction requires investigation")
    src_report=json.loads((provisional/"summary.json").read_text())
    if (src_report.get("schema")!="kbs-plan-c-full-active-dev-paired-v1"
        or src_report.get("scope")!="DEV_ONLY"
        or src_report.get("n_scored")!=50049
        or src_report.get("all_dev_scored") is not True
        or src_report.get("test_file_accessed") is not False):
        raise ValueError("Expected completed first-pass full-active DEV only")
    original=provisional/"dev_full_active_pairs.csv"
    if file_sha(original)!=src_report["event_csv_sha256"]:
        raise ValueError("Provisional file SHA mismatch")
    manifest=json.loads((g1/"manifest.json").read_text())
    idxm=json.loads((index/"index_manifest.json").read_text())
    if (manifest["schema"]!="kbs-plan-c-g1-derived-v1"
        or idxm["g1_protocol_sha256"]!=manifest["protocol_sha256"]
        or src_report["g1_protocol_sha256"]!=manifest["protocol_sha256"]):
        raise ValueError("Mismatched frozen source G1 identity")
    with original.open(newline="") as f:
        reader=csv.DictReader(f)
        fields=list(reader.fieldnames or [])
        rows=list(reader)
    if len(rows)!=50049 or len({x["event_id"] for x in rows})!=len(rows):
        raise ValueError("Expected exactly all unique DEV events")
    by_id={int(x["event_id"]):x for x in rows}
    ids=np.load(dev/"dev_source_event_ids.npy")
    targets=np.load(dev/"dev_positive_author_tokens.npy")
    if len(ids)!=50049 or set(ids.tolist())!=set(by_id):
        raise ValueError("Cannot match provisional Base results to all DEV target events")
    author_ids=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):j+1 for j,a in enumerate(author_ids)}
    times=pq.read_table(g1/"dev_cohort.parquet",
                        columns=["source_event_id","observed_at"])
    if not np.array_equal(np.asarray(times.column("source_event_id").to_numpy()),ids):
        raise ValueError("G1 DEV sample order mismatch")
    clocks=times.column("observed_at").to_pylist()
    snapshots,processed=replay_all_history(g1/"causal_stream_sealed.parquet",
                                            ids,known)
    counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),
                       minlength=len(author_ids)+1).astype(np.float64)
    logs=np.log1p(counts)
    pop=np.zeros(len(counts),dtype=np.float64)
    pop[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    n=0
    for i,cands,_ in author_availability(g1/"available_room_intervals.parquet",
                                        clocks,targets,known):
        e=int(ids[i])
        row=by_id[e]
        if int(row["candidate_count"])!=len(cands):
            raise ValueError("Cannot replay the exact original Base candidate universe")
        warm,recent,long_max=snapshots[i]
        scores=corrected_memory_score(cands,pop,warm,recent,long_max)
        m_rank=rank(cands,scores,int(targets[i]))
        row["memory_rank"]=str(m_rank)
        row["memory_ndcg10"]=repr(ndcg(m_rank))
        history_support=scores-.10*pop[cands]
        row["x_memory_history_supported_share"]=repr(float(np.mean(history_support>1e-12)))
        n+=1
        if n%1000==0:
            print(json.dumps({"phase":"DEV_correct_memory_replay",
                 "processed":n,"elapsed_s":round(time.monotonic()-start,1)}),flush=True)
    if n!=50049:
        raise ValueError("Incomplete exact author roster correction")
    stage.mkdir(parents=True,mode=0o700)
    out_file=stage/"dev_full_active_pairs.csv"
    with out_file.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    pairs_sha=file_sha(out_file)
    metrics={}
    for family in ("sasrec","gru4rec","memory"):
        vals=np.fromiter((float(r[family+"_ndcg10"]) for r in rows),
                         dtype=np.float64,count=n)
        ranks=np.fromiter((int(r[family+"_rank"]) for r in rows),
                          dtype=np.int32,count=n)
        metrics[family]={"ndcg10":float(vals.mean()),
                         "hr10":float(np.mean(ranks<=10))}
        if family!="memory":
            before=src_report["aggregate"][family]
            if not np.isclose(metrics[family]["ndcg10"],before["ndcg10"],atol=1e-12):
                raise ValueError("Base NDCG changed during Memory-only correction")
    m=np.fromiter((float(r["memory_ndcg10"]) for r in rows),dtype=np.float64,count=n)
    for base in ("sasrec","gru4rec"):
        b=np.fromiter((float(r[base+"_ndcg10"]) for r in rows),dtype=np.float64,count=n)
        metrics[base]["memory_minus_base_ndcg10"]=float(np.mean(m-b))
    summary=dict(src_report)
    summary.update({
        "schema":"kbs-plan-c-full-active-dev-paired-v2",
        "memory_corrected_from_all_history":True,
        "memory_definition":"0.10 TRAIN-normalized log popularity + 0.45 short last-10 ALL prior author events exp(-distance/3) + 0.45 long prior counts / max across ALL prior authors",
        "provisional_dev_pair_sha256":file_sha(original),
        "event_csv_sha256":pairs_sha,
        "historical_events_replayed":processed,
        "aggregate":metrics,
        "elapsed_seconds_memory_correction":round(time.monotonic()-start,1),
        "test_file_accessed":False,
        "source_test_outcomes_inspected":False,
        "gates_fit":False})
    (stage/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    stage.rename(out)
    print(json.dumps({"state":"DEV_PAIR_FULL_ACTIVE_MEMORY_CORRECTED",
        "n_events":n,"aggregate":metrics,"test_unseen":True}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--train-index",type=Path,required=True)
    p.add_argument("--dev",type=Path,required=True)
    p.add_argument("--provisional",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    main(a.g1,a.train_index,a.dev,a.provisional,a.out)
