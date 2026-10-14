#!/usr/bin/env python3
"""B4-A A3 H2: original and per-seed null Top-10 on sealed 4096 requests.

No current target author is read as a ranking label. Author stream values are
used only AFTER each source event is observed; swaps from an hour are applied
only AFTER its hour has fully closed. No NDCG/HR/rank is computed here.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,time
from pathlib import Path
import numpy as np,pyarrow.parquet as pq
from g3_replay_correct_memory import corrected_memory_score
from g5_unlabeled_test_score import active_rosters,stable_top10

HOUR=3_600_000_000_000
SEEDS=(20261014,20261015,20261016)
MAIN_SHA="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
SUB_SHA="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for x in iter(lambda:f.read(8<<20),b""):h.update(x)
    return h.hexdigest()

class History:
    def __init__(self,known):
        self.raw=collections.Counter()
        self.warm=collections.Counter()
        self.recent=collections.deque(maxlen=10)
        self.max_raw=0
        self.known=known
    def add(self,author):
        raw=int(author)
        self.raw[raw]+=1
        self.max_raw=max(self.max_raw,self.raw[raw])
        tok=self.known.get(raw,0)
        self.recent.append(tok)
        if tok:self.warm[tok]+=1
    def snapshot_with_open_hour(self,buffer):
        # Buffered current-hour authors are always original, because their
        # swaps cannot be activated before this whole hour closes.
        w=self.warm.copy();r=collections.deque(self.recent,maxlen=10)
        raw=self.raw.copy();largest=self.max_raw
        for _,author in buffer:
            a=int(author);raw[a]+=1;largest=max(largest,raw[a])
            t=self.known.get(a,0);r.append(t)
            if t:w[t]+=1
        return dict(w),tuple(r),largest

def main(cache,g1,index,a1,source,h1,seed,out):
    if seed not in SEEDS:raise ValueError("unregistered H2 seed")
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("Immutable A3 H2 scorer output cannot be overwritten")
    started=time.monotonic()
    prior=json.loads((source/"summary.json").read_text())
    h1manifest=json.loads((h1/"manifest.json").read_text())
    if prior["status"]!="THREE_SOURCE_VALID_NULL_MAPS_PRIVATE_NO_RANKS":
        raise RuntimeError("H2 three-null structural SHA gate failed")
    if h1manifest["status"]!="H1_30000_FROZEN_PREDICTIONS_A4_HARD_HOLD":
        raise RuntimeError("H1 Top-10 must be sealed first")
    if prior["main_SHA256"]!=MAIN_SHA or prior["subset_SHA256"]!=SUB_SHA or (
            h1manifest["source_sample_SHA256"]!=MAIN_SHA):
        raise RuntimeError("H1/H2 sample identity changed")
    source_file=source/"H2_HISTORY_PRIVATE.npz"
    if sha(source_file)!=prior["private_history_sha256"]:
        raise RuntimeError("H2 preserved input history byte SHA mismatch")
    entry=next(x for x in prior["seed_results"] if x["seed"]==seed)
    map_file=source/f"null_seed_{seed}_PRIVATE.npz"
    if sha(map_file)!=entry["private_map_sha256"]:
        raise RuntimeError("H2 private null mapping SHA mismatch")
    m=np.load(map_file,allow_pickle=False)
    swap={int(e):int(a) for e,a in zip(m["source_event_ids"],m["swapped_author_ids"])}
    history=np.load(source_file,allow_pickle=False)
    E=history["source_event_ids"];U=history["user_ids"]
    A=history["author_ids"];T=history["source_time_ns"]
    if len(E)!=prior["source_history_rows"]:
        raise RuntimeError("stored causal source length mismatch")
    sub=a1/"B4A_IDENTITY_4096_PRIVATE.parquet"
    if sha(sub)!=SUB_SHA:raise RuntimeError("H2 frozen target list SHA mismatch")
    targets=pq.read_table(sub,columns=["source_event_id","user_id","observed_at"])
    ids=targets.column("source_event_id").to_numpy().astype(np.int64)
    users=targets.column("user_id").to_numpy().astype(np.int64)
    clocks=targets.column("observed_at").to_pylist()
    if len(ids)!=4096:raise RuntimeError("wrong H2 target size")
    wanted={int(e):i for i,e in enumerate(ids)}
    known_ids=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):i+1 for i,a in enumerate(known_ids)}
    n_auth=len(known_ids)
    counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),
                       minlength=n_auth+1).astype(np.float64)
    logs=np.log1p(counts);pop=np.zeros(len(logs),dtype=np.float64)
    pop[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    original=[None]*4096;altered=[None]*4096
    last_user=None;hour=None;buffer=[];received=set()
    realstate=None;nullstate=None;num_changed_source=0
    def close_hour():
        nonlocal buffer,num_changed_source
        for eid,raw in buffer:
            realstate.add(raw)
            a=swap.get(eid,raw)
            nullstate.add(a)
            num_changed_source+=int(a!=raw)
        buffer=[]
    for eid,u,raw,t in zip(E,U,A,T):
        eid=int(eid);u=int(u);raw=int(raw);t=int(t)
        if u!=last_user:
            if last_user is not None and buffer:close_hour()
            last_user=u;hour=None;buffer=[]
            realstate=History(known);nullstate=History(known)
        this_hour=t//HOUR
        if hour is not None and this_hour<hour:
            raise RuntimeError("causal source time went backward")
        if hour is not None and this_hour!=hour:
            close_hour()
        hour=this_hour
        k=wanted.get(eid)
        if k is not None:
            if k in received or u!=int(users[k]):
                raise RuntimeError("duplicate/incorrect H2 request")
            # Current author "raw" does not enter either snapshot here.
            original[k]=realstate.snapshot_with_open_hour(buffer)
            altered[k]=nullstate.snapshot_with_open_hour(buffer)
            received.add(k)
        buffer.append((eid,raw))
    if len(received)!=4096 or any(x is None for x in altered):
        raise RuntimeError("Missing A3 H2 snapshots")
    # Cross-check same original Full Memory top ten as already sealed H1.
    priorids=np.load(h1/"event_ids.npy",allow_pickle=False)
    prevtop=np.load(h1/"top10_base_and_memory_author_tokens.npy",allow_pickle=False)
    if sha(h1/"event_ids.npy")!=h1manifest["private_files_sha256"]["event_ids.npy"]:
        raise RuntimeError("H1 event SHA mismatch")
    if sha(h1/"top10_base_and_memory_author_tokens.npy")!=h1manifest["private_files_sha256"]["top10_base_and_memory_author_tokens.npy"]:
        raise RuntimeError("H1 predicted Memory SHA mismatch")
    lookup={int(e):i for i,e in enumerate(priorids)}
    if any(int(e) not in lookup for e in ids):
        raise RuntimeError("mechanism subset not covered by sealed H1")
    orig_top=np.empty((4096,10),dtype=np.int32)
    null_top=np.empty((4096,10),dtype=np.int32)
    active_counts=np.empty(4096,dtype=np.int32)
    for k,candidates in active_rosters(g1/"available_room_intervals.parquet",clocks,known):
        if len(candidates)<10:raise RuntimeError("invalid full F roster for H2")
        warm,recent,maximum=original[k]
        raw=corrected_memory_score(candidates,pop,warm,recent,maximum)
        orig_top[k]=stable_top10(candidates,raw)
        if not np.array_equal(orig_top[k],prevtop[lookup[int(ids[k])],2]):
            raise RuntimeError("H1 versus H2 original rank parity mismatch")
        warm,recent,maximum=altered[k]
        new=corrected_memory_score(candidates,pop,warm,recent,maximum)
        null_top[k]=stable_top10(candidates,new)
        active_counts[k]=len(candidates)
    if not np.all(active_counts>=10):raise RuntimeError("missing active roster")
    stage=out.with_name(out.name+".incomplete")
    stage.mkdir(parents=True,mode=0o700)
    for filename,arr in (("event_ids.npy",ids),("original_full_f_top10.npy",orig_top),
                         ("null_full_f_top10.npy",null_top)):
        np.save(stage/filename,arr,allow_pickle=False)
    summary={"schema":"kbs-b4a-a3-h2-one-null-target-blind-v1",
        "status":"H2_SEED_FROZEN_4096_UNLABELED_TOP10",
        "seed":seed,"n_events":4096,"source_sample_SHA256":SUB_SHA,
        "private_null_map_SHA256":sha(map_file),
        "H1_original_memory_top10_exact_match":True,
        "original_and_null_rankings_same_F_roster":True,
        "source_hour_rewire_applied_after_closed":True,
        "n_changed_completed_hour_historical_edges":num_changed_source,
        "target_author_from_same_request_as_prediction":False,
        "target_ndcg_rank_hr_computed":False,"A4_authorized":False,
        "files_sha256":{p.name:sha(p) for p in stage.glob("*.npy")},
        "wall_seconds":round(time.monotonic()-started,2)}
    (stage/"manifest.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    stage.rename(out)
    print(json.dumps({"status":summary["status"],"seed":seed,
                      "n_events":4096,"A4_authorized":False}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("cache","g1","index","a1","source","h1","out"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--seed",type=int,required=True)
    a=p.parse_args()
    main(a.cache,a.g1,a.index,a.a1,a.source,a.h1,a.seed,a.out)
