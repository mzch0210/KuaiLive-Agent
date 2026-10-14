#!/usr/bin/env python3
"""N9 Route B B2: 1024 M3 DEV original-vs-causally-valid coactive null ranking.

Three frozen seeds; private historical author substitutions only. TEST never
read. Scores and bootstrap are exported only as safe user-cluster aggregates.
"""
from __future__ import annotations
import argparse,collections,hashlib,heapq,json,math,time
from pathlib import Path
import numpy as np,pandas as pd,pyarrow.parquet as pq

HOUR=3600_000_000_000
SEEDS=(20261014,20261015,20261016)
EVENTS=1024
USERS=992
SAMPLE_SHA="6ad1a0753e181ac638636c278d226832b08d90d7d4867019910c61b96d7507da"
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()
def ndcg(k):
    return 1./math.log2(k+1) if k<=10 else 0.
def rank(c,s,true):
    i=int(np.searchsorted(c,true))
    if i==len(c) or c[i]!=true:raise RuntimeError("Frozen target absent from eligible F roster")
    v=s[i]
    return 1+int(np.count_nonzero((s>v+1e-12)|((np.abs(s-v)<=1e-12)&(c<true))))
def score(c,pop,warm,last,max_count,short=True,long=True):
    c=np.asarray(c,dtype=np.int32)
    z=.10*pop[c].astype(np.float64) if short else np.zeros(len(c),dtype=np.float64)
    if long and warm:
        if max_count<=0:raise RuntimeError("bad long maximum")
        ids=np.fromiter(warm,dtype=np.int32,count=len(warm))
        vals=np.fromiter(warm.values(),dtype=np.float64,count=len(warm))
        k=np.argsort(ids);ids=ids[k];vals=vals[k]
        ix=np.searchsorted(ids,c);hit=ix<len(ids)
        hit&=ids[np.minimum(ix,len(ids)-1)]==c
        z[hit]+=.45*vals[ix[hit]]/max_count
    if short and last:
        a={}
        for distance,tok in enumerate(reversed(last)):
            if tok:a[tok]=max(a.get(tok,0),math.exp(-distance/3))
        if a:
            ids=np.fromiter(sorted(a),dtype=np.int32)
            vals=np.array([a[t] for t in ids])
            ix=np.searchsorted(ids,c);hit=ix<len(ids)
            hit&=ids[np.minimum(ix,len(ids)-1)]==c
            z[hit]+=.45*vals[ix[hit]]
    return z
def active_rosters(path,clocks,truth,known):
    order=sorted(range(len(clocks)),key=lambda i:(clocks[i],i))
    def source():
        for b in pq.ParquetFile(path).iter_batches(batch_size=131072,
                                       columns=["open_ts","close_ts","author_id"]):
            rows=b.to_pydict()
            yield from zip(rows["open_ts"],rows["close_ts"],rows["author_id"])
    it=iter(source());ahead=next(it,None)
    heap=[];active=collections.Counter()
    for ix in order:
        t=clocks[ix]
        while ahead is not None and ahead[0]<=t:
            start,end,author=ahead
            token=known.get(int(author))
            if token is not None and end>t:
                active[token]+=1;heapq.heappush(heap,(end,token))
            ahead=next(it,None)
        while heap and heap[0][0]<=t:
            _,tok=heapq.heappop(heap);active[tok]-=1
            if not active[tok]:del active[tok]
        if int(truth[ix]) not in active:raise RuntimeError("Target absent from original F active roster")
        yield ix,np.fromiter(sorted(active),dtype=np.int32,count=len(active))
def paired_cluster_ci(d,user,n=2000,seed=20261014):
    ids,inv=np.unique(user,return_inverse=True)
    weights=np.bincount(inv,weights=d,minlength=len(ids))
    counts=np.bincount(inv,minlength=len(ids))
    rng=np.random.default_rng(seed)
    boot=np.empty(n)
    for k in range(n):
        ix=rng.integers(len(ids),size=len(ids))
        boot[k]=weights[ix].sum()/counts[ix].sum()
    return [float(v) for v in np.quantile(boot,[.025,.975])]
def snapshots_from_causal_stream(path,target_ids,target_users,target_times,
                                 null_mapping,known):
    requested={int(x):i for i,x in enumerate(target_ids)}
    allowed=set(int(x) for x in target_users)
    values=[None]*len(target_ids)
    seen=set();last_user=None;h=None
    raw_count=collections.Counter();warm=collections.Counter()
    recent=collections.deque(maxlen=10);max_raw=0
    buffer=[]
    replayed=0;checked=0;altered_used=set()
    def push(author):
        nonlocal max_raw
        raw_count[author]+=1
        max_raw=max(max_raw,raw_count[author])
        recent.append(known.get(author,0))
        tok=known.get(author,0)
        if tok:warm[tok]+=1
    def finalize():
        nonlocal buffer
        for e,raw,st in buffer:
            new=int(null_mapping.get(e,raw))
            if new!=raw:altered_used.add(e)
            push(new)
        buffer=[]
    for part in pq.ParquetFile(path).iter_batches(batch_size=262144,
          columns=["source_event_id","user_id","author_id","observed_at","split"]):
        d=part.to_pandas()
        d=d.loc[d.user_id.isin(allowed)&d.split.ne("TEST")]
        if d.empty:continue
        stamps=pd.to_datetime(d.observed_at,utc=True).dt.as_unit("ns").astype("int64").to_numpy()
        for eid,user,author,at,split in zip(d.source_event_id.to_numpy(),
                   d.user_id.to_numpy(),d.author_id.to_numpy(),stamps,d.split.to_numpy()):
            eid=int(eid);user=int(user);author=int(author);at=int(at)
            replayed+=1
            if user!=last_user:
                if user in seen:raise RuntimeError("user not contiguous in causal stream")
                seen.add(user);last_user=user;h=None
                raw_count.clear();warm.clear();recent.clear();max_raw=0;buffer=[]
            hour=at//HOUR
            if h is not None and hour<h:raise RuntimeError("history time backward")
            if h is not None and hour!=h:finalize()
            h=hour
            k=requested.get(eid)
            if k is not None:
                if split!="DEV" or values[k] is not None or user!=int(target_users[k]):
                    raise RuntimeError("wrong request ID/split/collision")
                if at!=int(target_times[k]):
                    raise RuntimeError("frozen request timestamp mismatched")
                c=raw_count.copy();w=warm.copy();l=collections.deque(recent,maxlen=10)
                max0=max_raw
                for _,original,_ in buffer:
                    c[original]+=1;max0=max(max0,c[original])
                    tok=known.get(original,0);l.append(tok)
                    if tok:w[tok]+=1
                values[k]=(dict(w),tuple(l),max0)
                checked+=1
            buffer.append((eid,author,at))
    if checked!=EVENTS or any(x is None for x in values):
        raise RuntimeError("missing DEV pretarget null snapshots")
    return values,replayed,len(altered_used)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--structural",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    q=p.parse_args()
    if q.out.exists():raise FileExistsError("Do not overwrite B2 scientific output")
    started=time.monotonic()
    root=q.root;g=root/"klm3_plan_c_g1_v1";idx=root/"klm3_g2_train_index_v1"
    dev=root/"klm3_g2_dev_checkpoint_screen_v1"
    sample=root/"klm3_n9_route_b_b2_pretarget_sample_v1"
    b2=root/"klm3_b2_full_dev_memory_source_ablation_seed20261013_v1"
    sm=json.loads((sample/"summary.json").read_text())
    struct=json.loads((q.structural/"summary.json").read_text())
    if not(sm["n_events"]==EVENTS and sm["n_users"]==USERS
           and sha(sample/"B2_MEDIUM_EVENTS_PRIVATE.npz")==SAMPLE_SHA
           and struct["n_target_events"]==EVENTS and struct["n_target_users"]==USERS
           and struct["source_sample_SHA256"]==SAMPLE_SHA
           and struct["source_hour_activated_after_close_only"] is True
           and struct["no_G5_TEST_read"] is True
           and [x["seed"] for x in struct["seed_results"]]==list(SEEDS)):
        raise RuntimeError("Missing correct frozen real null structure")
    bm=json.loads((b2/"summary.json").read_text())
    if not(bm["new_TEST_opened"] is False
           and sha(b2/"dev_memory_source_ablation_pairs.csv")==bm["private_event_source_csv_sha256"]
           and bm["full_memory_nDCG_mismatches"]=={"F":0,"S":0}):
        raise RuntimeError("B2 original scored source not verified")
    samp=np.load(sample/"B2_MEDIUM_EVENTS_PRIVATE.npz",allow_pickle=False)
    ids=samp["source_event_ids"].astype(np.int64)
    users=samp["user_ids"].astype(np.int64)
    targetns=samp["observed_at_ns"].astype(np.int64)
    if len(ids)!=EVENTS or len(np.unique(users))!=USERS:
        raise RuntimeError("B2 sample identity incorrect")
    devm=json.loads((dev/"manifest.json").read_text())
    for name in ("dev_source_event_ids.npy","dev_positive_author_tokens.npy"):
        if sha(dev/name)!=devm["files_sha256"][name]:raise RuntimeError("dev checkpoint altered")
    all_ids=np.load(dev/"dev_source_event_ids.npy",mmap_mode="r")
    target_tokens=np.load(dev/"dev_positive_author_tokens.npy",mmap_mode="r")
    byid={int(e):i for i,e in enumerate(all_ids)}
    chosen=np.array([byid[int(e)] for e in ids],dtype=np.int64)
    positive=target_tokens[chosen]
    clock=pq.read_table(g/"dev_cohort.parquet",
             columns=["source_event_id","user_id","observed_at"])
    if not np.array_equal(clock.column("source_event_id").to_numpy(),all_ids):
        raise RuntimeError("original G1 DEV time identity error")
    times=[clock.column("observed_at")[int(i)].as_py() for i in chosen]
    if not np.array_equal(clock.column("user_id").to_numpy()[chosen],users):
        raise RuntimeError("user identities misaligned")
    original=pd.read_csv(b2/"dev_memory_source_ablation_pairs.csv").set_index("event_id").loc[ids]
    if not original.split.eq("DEV").all():raise RuntimeError("non DEV entered")
    if not np.array_equal(original.user_id.to_numpy(dtype=np.int64),users):
        raise RuntimeError("original B2 user mismatch")
    knownids=np.load(idx/"authors.npy",mmap_mode="r")
    known={int(x):i+1 for i,x in enumerate(knownids)}
    counts=np.bincount(np.load(idx/"sequence_ids.npy",mmap_mode="r"),
                      minlength=len(knownids)+1).astype(np.float64)
    logs=np.log1p(counts);pop=np.zeros(len(logs),dtype=np.float64)
    pop[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    # Cache original real scorer qualities; each null is compared event-by-event.
    original_values={label:original[column].to_numpy(float) for label,column in [
        ("full_F","memory_ndcg10"),("full_S","sampled_memory_ndcg10"),
        ("long_F","b2_long_only_F_ndcg10"),("long_S","b2_long_only_S_ndcg10")]}
    rosters=[None]*EVENTS;sampled=[None]*EVENTS;select=[None]*EVENTS
    for k,c in active_rosters(g/"available_room_intervals.parquet",times,positive,known):
        true=int(positive[k]);rest=c[c!=true]
        if len(rest)<574:raise RuntimeError("S retrospective roster missing")
        S=np.sort(np.concatenate((np.random.default_rng(20261012+int(ids[k])).choice(
                    rest,size=574,replace=False),np.array([true],dtype=np.int32))))
        loc=np.searchsorted(c,S)
        if not np.array_equal(c[loc],S):raise RuntimeError("S candidate membership invalid")
        rosters[k]=c;sampled[k]=S;select[k]=loc
    result={"schema":"kbs-route-b-b2-m3-dev-1024-coactive-null-scores-v1",
        "evidence":"POST_G5_DEV_EXPLORATORY_SAME_1024_EVENTS_992_USERS",
        "n_events":EVENTS,"n_users":USERS,"null_seeds":list(SEEDS),
        "original_Full_Long_source_SHA256":bm["private_event_source_csv_sha256"],
        "frozen_DEV_sample_SHA256":SAMPLE_SHA,
        "G5_TEST_opened":False,"Base_models_retrained":False,
        "private_history_edges_exported":False,"seeds":[]}
    for n,seed in enumerate(SEEDS):
        private=q.structural/f"null_seed_{seed}_PRIVATE.npz"
        corresponding=struct["seed_results"][n]
        if sha(private)!=corresponding["private_changed_map_sha256"]:
            raise RuntimeError("structural null map digest mismatch")
        with np.load(private,allow_pickle=False) as change:
            altered_ids=change["source_event_ids"].astype(np.int64)
            altered_author=change["swapped_author_ids"].astype(np.int64)
            if len(altered_ids)!=corresponding["changed_edges"]:
                raise RuntimeError("changed edge count mismatches frozen null")
            mapping={int(e):int(a) for e,a in zip(altered_ids,altered_author)}
        if len(mapping)!=len(altered_ids):
            raise RuntimeError("duplicate changed source edge in null")
        states,replayed,changed_consumed=snapshots_from_causal_stream(
            g/"causal_stream_sealed.parquet",ids,users,targetns,mapping,known)
        scores={tag:np.empty(EVENTS,dtype=float) for tag in
                ("full_F","full_S","long_F","long_S","pop_F","pop_S")}
        for k,(warm,recent,den) in enumerate(states):
            c=rosters[k];S=sampled[k];loc=select[k];true=int(positive[k])
            full=score(c,pop,warm,recent,den)
            long=score(c,pop,warm,(),den,short=False)
            po=.10*pop[c]
            for label,cand,v in (("full_F",c,full),("full_S",S,full[loc]),
                                 ("long_F",c,long),("long_S",S,long[loc]),
                                 ("pop_F",c,po),("pop_S",S,po[loc])):
                scores[label][k]=ndcg(rank(cand,v,true))
        diffs={k:original_values[k]-scores[k] for k in original_values}
        baseline=float(scores["pop_F"].mean())
        nullF=float(scores["full_F"].mean())
        trueF=float(original_values["full_F"].mean())
        nonzero=int(np.count_nonzero(scores["full_F"]))
        # Frozen original 128 pilot's nonfloor diagnostic, suitably scaled.
        nonfloor=(nullF>=max(.10,.30*trueF)
                  and float(scores["full_S"].mean())>=.20
                  and nullF>=baseline+.02
                  and nonzero>=int(math.ceil(.10*EVENTS))
                  and corresponding["changed_fraction_of_selected_user_history"]>=.10)
        dF=diffs["full_F"];dS=diffs["full_S"]
        entry={"seed":seed,"private_map_SHA256":corresponding["private_changed_map_sha256"],
          "source_history_rows_scanned":replayed,
          "past_null_interventions_used_anywhere":changed_consumed,
          "structural_change_fraction":corresponding["changed_fraction_of_selected_user_history"],
          "n_requests_exposed_to_changed_pretarget_history":corresponding[
                      "target_requests_with_at_least_one_activated_null_edge"],
          "null_Full_F_NDCG":nullF,"original_Full_F_NDCG":trueF,
          "null_Full_S_NDCG":float(scores["full_S"].mean()),
          "original_Full_S_NDCG":float(original_values["full_S"].mean()),
          "null_Long_F_NDCG":float(scores["long_F"].mean()),
          "null_Long_S_NDCG":float(scores["long_S"].mean()),
          "popularity_only_F_NDCG":baseline,
          "null_Full_F_top10_positive_events":nonzero,
          "nonfloor_preset_diagnostic_pass":bool(nonfloor),
          "primary_real_minus_null_Full_F":float(dF.mean()),
          "primary_user_cluster_bootstrap_95":paired_cluster_ci(dF,users,seed=20261014),
          "secondary_real_minus_null_Full_S":float(dS.mean()),
          "secondary_user_cluster_bootstrap_95":paired_cluster_ci(dS,users,seed=20261015),
          "secondary_source_x_candidate_relation_interaction":float((dF-dS).mean()),
          "secondary_Long_original_minus_null_F":float(diffs["long_F"].mean())}
        result["seeds"].append(entry)
        print(json.dumps({"B2_NULL_SCORE":"ONE_SEED_DONE","safe_summary":entry},sort_keys=True),flush=True)
    avg=np.array([x["primary_real_minus_null_Full_F"] for x in result["seeds"]])
    result["across_null_seed_primary_mean"]=float(avg.mean())
    result["across_null_seed_primary_range"]=[float(avg.min()),float(avg.max())]
    result["all_null_arms_nonfloor"]=all(x["nonfloor_preset_diagnostic_pass"] for x in result["seeds"])
    result["runtime_seconds"]=round(time.monotonic()-started,2)
    q.out.mkdir(parents=True,mode=0o700)
    (q.out/"summary.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"B2_NULL_SCORE":"FINISHED","safe_summary":result},sort_keys=True),flush=True)
if __name__=="__main__":main()
