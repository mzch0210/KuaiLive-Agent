#!/usr/bin/env python3
"""G2 DEV-only author context/candidate builder from sealed G1 provenance.

No TEST scoring or gate fitting. DEV evaluation rows/identities remain on User-host.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import heapq
import json
import math
import time
from pathlib import Path

import numpy as np

SELECT_N = 4096
NEG_N = 574


def sha(file: Path):
    h = hashlib.sha256()
    with file.open("rb") as f:
        for block in iter(lambda: f.read(8*1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def get_column(path, name):
    import pyarrow.parquet as pq
    return pq.read_table(path, columns=[name]).column(name).to_pylist()


def extract_dev_contexts(stream_file: Path, dev_file: Path, known_to_index, context_length=16):
    import pyarrow.parquet as pq
    dev_eids = get_column(dev_file, "source_event_id")
    n=len(dev_eids)
    positions={int(event):i for i,event in enumerate(dev_eids)}
    if len(positions)!=n:
        raise ValueError("DEV cohort contains duplicate event IDs")
    contexts=np.zeros((n,context_length),np.int32)
    seen=np.zeros(n,dtype=np.bool_)
    last_user=None
    hist=collections.deque(maxlen=context_length)
    parsed_events=0
    selected_events=0
    parquet=pq.ParquetFile(stream_file)
    for block in parquet.iter_batches(batch_size=131072,
                columns=["source_event_id","user_id","author_id","split"]):
        ids,users,authors,splits=block.to_pydict().values()
        for event,user,author,split in zip(ids,users,authors,splits):
            if split=="TEST":
                continue  # TEST identities never enter histories
            parsed_events+=1
            if last_user!=user:
                hist.clear()
                last_user=user
            i=positions.get(int(event))
            if i is not None:
                if split!="DEV" or seen[i]:
                    raise ValueError("DEV cohort not aligned with source chronology")
                if hist:
                    contexts[i,-len(hist):]=list(hist)
                selected_events+=1
                seen[i]=True
            token=known_to_index.get(int(author))
            if token is not None:
                hist.append(token)
    if not seen.all():
        raise ValueError("Missing DEV target contexts: " + str(n-int(seen.sum())))
    return contexts, {"n_dev_events":n,
                      "dev_contexts_nonempty":int(np.count_nonzero(contexts.any(axis=1))),
                      "dev_zero_warm_contexts":int(np.count_nonzero(~contexts.any(axis=1))),
                      "pretest_stream_events":parsed_events,
                      "target_contexts_found":selected_events,
                      "test_split_events_used_for_history":0}


def room_iterator(path: Path):
    import pyarrow.parquet as pq
    reader=pq.ParquetFile(path)
    for batch in reader.iter_batches(batch_size=131072,
              columns=["open_ts","close_ts","author_id"]):
        data=batch.to_pydict()
        yield from zip(data["open_ts"],data["close_ts"],data["author_id"])


def sample_active_author_sets(room_stream, observation_times, target_ids, source_events,
                              known_to_index, seed=20261012):
    if not (len(observation_times)==len(target_ids)==len(source_events)):
        raise ValueError("Misaligned target sample inputs")
    order=sorted(range(len(observation_times)),
                 key=lambda i:(observation_times[i],source_events[i]))
    n=len(order)
    arr=np.zeros((n,NEG_N+1),dtype=np.int32)
    active=collections.Counter()
    heap=[]
    stream=iter(room_stream)
    next_room=next(stream,None)
    n_processed=0
    mismatch=0
    counts=[]
    for ix in order:
        t=observation_times[ix]
        while next_room is not None and next_room[0]<=t:
            start,end,original_author=next_room
            token=known_to_index.get(int(original_author))
            if token is not None and end>start and end>t:
                active[token]+=1
                heapq.heappush(heap,(end,token))
            elif token is not None and end>start:
                # Room opened and finished between sampled timestamps:
                # skipping it is equivalent to enqueueing and expiring it.
                pass
            n_processed+=1
            next_room=next(stream,None)
        while heap and heap[0][0]<=t:
            _,token=heapq.heappop(heap)
            active[token]-=1
            if active[token]==0:
                del active[token]
        label=int(target_ids[ix])
        if label not in active:
            mismatch+=1
            continue
        pool=np.asarray(sorted(active),dtype=np.int32)
        pool=pool[pool!=label]
        counts.append(len(pool)+1)
        if len(pool)<NEG_N:
            raise ValueError("Insufficient DEV available warm authors")
        rng=np.random.default_rng(seed+int(source_events[ix]))
        sampled=rng.choice(pool,size=NEG_N,replace=False)
        arr[ix,0]=label
        arr[ix,1:]=sampled
    if mismatch:
        raise ValueError(str(mismatch)+" DEV target authors not active under frozen roster")
    return arr,{"selected_dev_events":n,
                "rooms_scanned_until_latest_sampled_time":n_processed,
                "DEV_roster_n_min":int(min(counts)),
                "DEV_roster_n_median":int(np.median(counts)),
                "DEV_roster_n_max":int(max(counts)),
                "sampled_candidate_count":int(arr.shape[1]),
                "warm_author_deduplicated":True,"targets_not_active":mismatch}


def run(g1:Path,index:Path,selection_protocol:Path,out:Path):
    import pyarrow.parquet as pq
    t0=time.monotonic()
    manifest=json.loads((g1/"manifest.json").read_text())
    index_manifest=json.loads((index/"index_manifest.json").read_text())
    spec=json.loads(selection_protocol.read_text())
    if (manifest.get("schema")!="kbs-plan-c-g1-derived-v1"
        or spec.get("status")!="PREDECLARED_BEFORE_DEV_CHECKPOINT_METRICS"
        or spec.get("g1_protocol_sha256")!=manifest.get("protocol_sha256")
        or index_manifest.get("g1_protocol_sha256")!=manifest["protocol_sha256"]):
        raise ValueError("G1, TRAIN index and DEV selection protocol are not identical")
    if out.exists():
        raise FileExistsError("DEV cache exists; never overwrite: "+str(out))
    tmp=out.with_name(out.name+".incomplete")
    if tmp.exists():
        raise FileExistsError("Interrupted DEV cache must be inspected first")
    tmp.mkdir(parents=True,mode=0o700)
    authors=np.load(index/"authors.npy",mmap_mode="r")
    known_to_index={int(a):i+1 for i,a in enumerate(authors)}
    dev_file=g1/"dev_cohort.parquet"
    dev=pq.read_table(dev_file,columns=[
        "source_event_id","author_id","observed_at"])
    event_ids=np.asarray(dev.column("source_event_id").to_numpy(),dtype=np.int64)
    author_original=np.asarray(dev.column("author_id").to_numpy(),dtype=np.int64)
    positive=np.asarray([known_to_index.get(int(a),0) for a in author_original],
                        dtype=np.int32)
    if np.any(positive==0):
        raise ValueError("Frozen DEV target unexpectedly contains an unseen author")
    context,alignment=extract_dev_contexts(
        g1/"causal_stream_sealed.parquet",dev_file,known_to_index)
    eval_indices=np.linspace(0,len(event_ids)-1,SELECT_N,dtype=np.int64)
    if len(np.unique(eval_indices))!=SELECT_N:
        raise ValueError("Insufficient unique DEV events for checkpoint screen")
    all_clock=dev.column("observed_at").to_pylist()
    times=[all_clock[i] for i in eval_indices]
    candidates,roster=sample_active_author_sets(
        room_iterator(g1/"available_room_intervals.parquet"),times,
        positive[eval_indices],event_ids[eval_indices],
        known_to_index,20261012)
    np.save(tmp/"dev_contexts.npy",context,allow_pickle=False)
    np.save(tmp/"dev_positive_author_tokens.npy",positive,allow_pickle=False)
    np.save(tmp/"dev_source_event_ids.npy",event_ids,allow_pickle=False)
    np.save(tmp/"checkpoint_dev_indices.npy",eval_indices,allow_pickle=False)
    np.save(tmp/"checkpoint_candidate_tokens.npy",candidates,allow_pickle=False)
    hashes={f.name:sha(f) for f in tmp.glob("*.npy")}
    summary={
        "schema":"kbs-plan-c-g2-dev-screen-v1",
        "selection_protocol_sha256":sha(selection_protocol),
        "g1_protocol_sha256":manifest["protocol_sha256"],
        "train_index_sha256":sha(index/"index_manifest.json"),
        "g1_dev_cohort_sha256":manifest["generated_files_sha256"]["dev_cohort.parquet"],
        "DEV_alignment":alignment,
        "DEV_active_author_candidates":roster,
        "files_sha256":hashes,"elapsed_s":round(time.monotonic()-t0,1),
        "target_labels_used":"DEV only",
        "test_cohort_file_opened":False,
        "test_metrics_calculated":False}
    (tmp/"manifest.json").write_text(json.dumps(summary,indent=2)+"\n")
    tmp.rename(out)
    print(json.dumps(summary),flush=True)
    return summary


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--index",type=Path,required=True)
    p.add_argument("--protocol",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    run(a.g1,a.index,a.protocol,a.out)
