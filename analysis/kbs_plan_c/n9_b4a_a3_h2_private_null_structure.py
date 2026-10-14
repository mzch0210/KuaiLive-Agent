#!/usr/bin/env python3
"""B4-A A3 H2: create three real-historical, closed-hour source swaps before outcomes.

Private TEST-period history may include previously observed authors; no ranking,
current-label lookup, target ranks or NDCG are performed by this script.
Each hour gets its random seed from frozen seed+hour alone; a swap becomes
visible to predictions only after its source hour ends. Never publish maps.
"""
from __future__ import annotations
import argparse,hashlib,json,random,time
from pathlib import Path
import numpy as np,pandas as pd,pyarrow.parquet as pq

HOUR=3_600_000_000_000
SEEDS=(20261014,20261015,20261016)
MAIN_SHA="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
SUB_SHA="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def ns(v):
    a=pd.to_datetime(pd.Series(v),utc=True)
    if a.isna().any():raise ValueError("missing clock")
    return a.dt.as_unit("ns").astype("int64").to_numpy()

def main(a1,g1,preflight,out):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("Original H2 null structure immutable")
    t0=time.monotonic()
    report=json.loads((preflight/"summary.json").read_text())
    if report["status"]!="PASS_INPUT_ONLY_NOT_PRODUCTION_SCORER":
        raise RuntimeError("A3 metadata preflight missing")
    sample=a1/"B4A_IDENTITY_4096_PRIVATE.parquet"
    if sha(sample)!=SUB_SHA or sha(a1/"B4A_MAIN_30000_PRIVATE.parquet")!=MAIN_SHA:
        raise RuntimeError("A1 frozen sample changed")
    s=pq.read_table(sample,columns=["source_event_id","user_id","observed_at"])
    selected_id=s.column("source_event_id").to_numpy().astype(np.int64)
    selected_user=s.column("user_id").to_numpy().astype(np.int64)
    target_time=ns(s.column("observed_at").to_pylist())
    if len(selected_id)!=4096 or len(np.unique(selected_id))!=4096:
        raise RuntimeError("invalid H2 target ID list")
    last_by_user={}
    for u,t in zip(selected_user,target_time):
        last_by_user[int(u)]=max(last_by_user.get(int(u),-1),int(t))
    allowed=set(last_by_user)
    # Extract the observed stream for target users only, through their last
    # selected request. Reading an edge's historical author is required for
    # later causal histories; the same edge cannot affect its own prediction.
    Es=[];Us=[];As=[];Ts=[]
    previous=None;last_time=None;observed_users=set()
    for batch in pq.ParquetFile(g1/"causal_stream_sealed.parquet").iter_batches(
            batch_size=262144,
            columns=["source_event_id","user_id","author_id","observed_at"]):
        d=batch.to_pandas()
        d=d.loc[d.user_id.isin(allowed)]
        if d.empty:continue
        times=ns(d.observed_at)
        m=np.fromiter((tt<=last_by_user[int(u)] for u,tt in
                       zip(d.user_id.to_numpy(),times)),dtype=bool,count=len(d))
        d=d.loc[m];times=times[m]
        if d.empty:continue
        Es.append(d.source_event_id.to_numpy(dtype=np.int64))
        Us.append(d.user_id.to_numpy(dtype=np.int64))
        As.append(d.author_id.to_numpy(dtype=np.int64))
        Ts.append(times)
    if not Es:raise RuntimeError("No causal history for frozen H2 users")
    E=np.concatenate(Es);U=np.concatenate(Us);A=np.concatenate(As);T=np.concatenate(Ts)
    if len(set(E.tolist()))!=len(E):raise RuntimeError("repeated causal source event IDs")
    boundary=np.r_[0,np.flatnonzero(U[1:]!=U[:-1])+1,len(E)]
    if len(boundary)-1!=len(allowed) or len(set(U[boundary[:-1]].tolist()))!=len(allowed):
        raise RuntimeError("source stream not contiguous per frozen H2 users")
    for lo,hi in zip(boundary[:-1],boundary[1:]):
        if np.any(np.diff(T[lo:hi])<0):raise RuntimeError("within-user clock backwards")
    # All H2 events must actually occur in this source stream at their A1
    # time; a target may be included in a source stream for *later* requests.
    idx={int(e):i for i,e in enumerate(E)}
    if any(int(e) not in idx or int(U[idx[int(e)]])!=int(u) or
           int(T[idx[int(e)]])!=int(t) for e,u,t in
           zip(selected_id,selected_user,target_time)):
        raise RuntimeError("frozen H2 target source identity/clock mismatch")
    authors=set(A.tolist())
    intervals=[]
    for batch in pq.ParquetFile(g1/"available_room_intervals.parquet").iter_batches(
            batch_size=262144,columns=["author_id","open_ts","close_ts"]):
        d=batch.to_pandas();d=d.loc[d.author_id.isin(authors)]
        if len(d):intervals.append(d)
    if not intervals:raise RuntimeError("source author active intervals unavailable")
    f=pd.concat(intervals,ignore_index=True)
    begin=ns(f.open_ts);end=ns(f.close_ts)
    good=end>begin
    actor=f.author_id.to_numpy(np.int64)[good];begin=begin[good];end=end[good]
    order=np.lexsort((begin,actor))
    actor=actor[order];begin=begin[order];end=end[order]
    segments=np.r_[0,np.flatnonzero(actor[1:]!=actor[:-1])+1,len(actor)]
    intervals_by_author={}
    for lo,hi in zip(segments[:-1],segments[1:]):
        intervals_by_author[int(actor[lo])]=(begin[lo:hi],np.maximum.accumulate(end[lo:hi]))
    def active(author,t):
        v=intervals_by_author.get(int(author))
        if v is None:return False
        j=int(np.searchsorted(v[0],t,side="right"))-1
        return j>=0 and v[1][j]>t
    hours=T//HOUR
    order=np.argsort(hours,kind="stable")
    sorted_hours=hours[order]
    borders=np.r_[0,np.flatnonzero(sorted_hours[1:]!=sorted_hours[:-1])+1,len(E)]
    staging=out.with_name(out.name+".incomplete")
    staging.mkdir(parents=True,mode=0o700)
    # Private causal-history rows allow all three H2 scoring passes to reuse
    # one audited source extraction rather than repeatedly scan the full M3 file.
    np.savez_compressed(staging/"H2_HISTORY_PRIVATE.npz",
                        source_event_ids=E,user_ids=U,author_ids=A,source_time_ns=T)
    history_sha=sha(staging/"H2_HISTORY_PRIVATE.npz")
    results=[]
    try:
        for seed in SEEDS:
            revised=A.copy();changed=np.zeros(len(E),dtype=bool)
            attempts=0;swaps=0
            for lo,hi in zip(borders[:-1],borders[1:]):
                chunk=order[lo:hi];size=len(chunk)
                if size<2:continue
                hour=int(sorted_hours[lo])
                raw=f"n9-route-b-null-v1:{seed}:{hour}".encode("ascii")
                rng=random.Random(int.from_bytes(hashlib.blake2b(raw,digest_size=8).digest(),"little"))
                occupied=set()
                for _ in range(min(size*3,75000)):
                    if len(occupied)>=size-1:break
                    i=rng.randrange(size);j=rng.randrange(size-1)
                    if j>=i:j+=1
                    x=int(chunk[i]);y=int(chunk[j]);attempts+=1
                    if i in occupied or j in occupied or U[x]==U[y] or A[x]==A[y]:continue
                    if not(active(A[x],int(T[x])) and active(A[y],int(T[y]))
                           and active(A[y],int(T[x])) and active(A[x],int(T[y]))):continue
                    revised[x]=A[y];revised[y]=A[x]
                    changed[x]=changed[y]=True
                    occupied.add(i);occupied.add(j);swaps+=1
            if swaps==0 or np.count_nonzero(changed)!=2*swaps:
                raise RuntimeError("invalid or empty null pair changes")
            # Author/hour count marginals, excluding unchanged edges as they
            # cancel exactly from the before/after difference.
            b=pd.DataFrame({"h":hours[changed],"a":A[changed]}).groupby(["h","a"]).size()
            c=pd.DataFrame({"h":hours[changed],"a":revised[changed]}).groupby(["h","a"]).size()
            if not b.equals(c):raise RuntimeError("hourly author activity marginals changed")
            if not all(active(revised[i],int(T[i])) for i in np.flatnonzero(changed)):
                raise RuntimeError("ineligible source-time swapped author")
            filename=f"null_seed_{seed}_PRIVATE.npz"
            np.savez_compressed(staging/filename,
                source_event_ids=E[changed],swapped_author_ids=revised[changed])
            results.append({"seed":seed,"swap_pairs":swaps,
                "changed_edges":int(changed.sum()),
                "source_histories_examined":int(len(E)),
                "fraction_changed":float(changed.mean()),
                "marginal_and_source_availability_preserved":True,
                "strict_source_hour_closure_required_during_scoring":True,
                "private_map_sha256":sha(staging/filename)})
            print(json.dumps({"H2_NULL_SOURCE_PASS_SEED":seed,
                    "changed_fraction":round(float(changed.mean()),4)}),flush=True)
        manifest={"schema":"kbs-b4a-a3-h2-three-null-structure-v1",
             "status":"THREE_SOURCE_VALID_NULL_MAPS_PRIVATE_NO_RANKS",
             "main_SHA256":MAIN_SHA,"subset_SHA256":SUB_SHA,
             "n_targets":4096,"n_users":len(allowed),
             "source_history_rows":len(E),
             "private_history_sha256":history_sha,
             "null_seed_registry":SEEDS,"seed_results":results,
             "target_NDCG_ranks_labels_read":False,
             "target_blind_top10_completed":False,
             "A4_authorized":False,
             "wall_seconds":round(time.monotonic()-t0,1)}
        (staging/"summary.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
        staging.rename(out)
    except Exception:
        # Preserve incomplete private staging to prevent silent do-over.
        raise
    print(json.dumps({"status":manifest["status"],"n_targets":4096,
                      "A4_authorized":False}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("a1","g1","preflight","out"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args();main(a.a1,a.g1,a.preflight,a.out)
