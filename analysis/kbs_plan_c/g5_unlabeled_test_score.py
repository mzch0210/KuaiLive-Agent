#!/usr/bin/env python3
"""G5-A: prequential, strictly pretarget, *unlabeled* frozen six-model TEST scoring.

The TEST cohort is opened ONLY for event ID/user/timestamp (not author label).
TEST stream prior observations are allowed as prequential history. Each
target's own author is appended only AFTER snapshot creation. All seven
rankers store target-blind top10 author-token IDs, not accuracy, target label,
rank or per-event NDCG. Frozen gate decisions are made from label-free data.
The independent G5-B action later reads the sealed target labels ONCE.
"""
from __future__ import annotations
import argparse,collections,hashlib,heapq,json,math,time
from pathlib import Path
import joblib,numpy as np,pyarrow.parquet as pq,torch
from g2_train_base import Encoder
from g3_replay_correct_memory import corrected_memory_score
from g4_sparse_gate_features import sparse_history_support_share

SEEDS=(20261012,20261013,20261014)
FAMILIES=("sasrec","gru4rec")
METHODS=("utility","difficulty","specialist","uncertainty","history")
MODEL_KEYS=tuple((seed,model) for seed in SEEDS for model in FAMILIES)
ROW_COUNT=47575
L=16

def sha(file):
    h=hashlib.sha256()
    with Path(file).open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def gate_path(cache,seed,family):
    root=cache/"klm3_g3_e2_five_gate_DEV_frozen_v1" if seed==20261012 else cache/f"klm3_g4_extra_seed{seed}_five_gate_DEV_frozen_v1"
    return root/family

def active_rosters(path,timestamps,known):
    # One causal sweep for all 47,575 events: no knowledge of observed target.
    order=sorted(range(len(timestamps)),key=lambda i:(timestamps[i],i))
    def rooms():
        pf=pq.ParquetFile(path)
        for block in pf.iter_batches(batch_size=131072,
                   columns=["open_ts","close_ts","author_id"]):
            d=block.to_pydict()
            yield from zip(d["open_ts"],d["close_ts"],d["author_id"])
    source=iter(rooms())
    ahead=next(source,None)
    expires=[]
    active=collections.Counter()
    for i in order:
        clock=timestamps[i]
        while ahead is not None and ahead[0]<=clock:
            begin,end,author=ahead
            token=known.get(int(author))
            if token and end>clock:
                active[token]+=1
                heapq.heappush(expires,(end,token))
            ahead=next(source,None)
        while expires and expires[0][0]<=clock:
            _,token=heapq.heappop(expires)
            active[token]-=1
            if not active[token]:
                del active[token]
        # Author-token order is raw author-ID order, frozen since G1.
        yield i,np.fromiter(sorted(active),dtype=np.int32,count=len(active))

def histories(stream,requested_ids,known):
    """All prior eligible TRAIN/DEV/TEST observations; no own/future event in row."""
    lookup={int(e):i for i,e in enumerate(requested_ids)}
    if len(lookup)!=len(requested_ids):
        raise ValueError("TEST repeated event IDs")
    snapshots=[None]*len(requested_ids)
    previous_user=None
    recent_all=collections.deque(maxlen=10)
    recent_warm=collections.deque(maxlen=10)
    last16=collections.deque(maxlen=L)
    all_count=collections.Counter()
    warm_count=collections.Counter()
    all_max=0
    total=0
    warm_total=0
    count=0
    seen=0
    for batch in pq.ParquetFile(stream).iter_batches(
            batch_size=262144,columns=["source_event_id","user_id","author_id","split"]):
        d=batch.to_pydict()
        for e,user,author,split in zip(d["source_event_id"],d["user_id"],
                                       d["author_id"],d["split"]):
            if previous_user!=user:
                previous_user=user
                recent_all.clear();recent_warm.clear();last16.clear()
                all_count.clear();warm_count.clear()
                all_max=0;total=0;warm_total=0
            i=lookup.get(int(e))
            if i is not None:
                if split!="TEST" or snapshots[i] is not None:
                    raise ValueError("Target identity/split mismatch")
                if total<2:
                    raise ValueError("TEST target violates min prior history")
                hist=np.zeros(L,dtype=np.int32)
                if last16:
                    hist[-len(last16):]=last16
                # Freeze only prior state at this point, before current author.
                features={
                 "x_hist_event_count":float(total),
                 "x_hist_warm_count":float(warm_total),
                 "x_hist_distinct":float(len(warm_count)),
                 "x_hist_repeat_max":float(max(warm_count.values()) if warm_count else 0),
                 "x_hist_short_unique":float(len(set(recent_warm)))}
                snapshots[i]=(hist,dict(warm_count),tuple(recent_all),
                              int(all_max),features)
                seen+=1
            # This observed event is now past relative to later user events,
            # including later TEST events, per frozen prequential G5 protocol.
            key=int(author)
            all_count[key]+=1
            all_max=max(all_max,all_count[key])
            total+=1
            token=known.get(key,0)
            recent_all.append(token)
            if token:
                warm_count[token]+=1
                recent_warm.append(token)
                last16.append(token)
                warm_total+=1
            count+=1
        if count%1000000<262144:
            print(json.dumps({"history_source_events":count,
                              "pretarget_TEST_snapshots":seen}),flush=True)
    if seen!=len(requested_ids) or any(s is None for s in snapshots):
        raise ValueError("Not all TEST pretarget contexts captured")
    return snapshots,count

def stable_top10(tokens,scores,k=10):
    """Exact score rank with ID tie break without sorting all 30k candidates."""
    tokens=np.asarray(tokens,dtype=np.int32)
    values=np.asarray(scores)
    if len(tokens)<k or not np.isfinite(values).all():
        raise ValueError("Invalid candidate scores")
    if np.any(tokens[1:]<=tokens[:-1]):
        raise ValueError("Candidate IDs not sorted uniquely")
    pivot=np.partition(values,len(values)-k)[len(values)-k]
    strictly=np.flatnonzero(values>pivot)
    tied=np.flatnonzero(values==pivot)
    wanted=k-len(strictly)
    if wanted<0 or wanted>len(tied):
        raise ValueError("top-k pivot mismatch")
    chosen=np.concatenate([strictly,tied[:wanted]])
    ordered=np.lexsort((tokens[chosen],-values[chosen]))
    return tokens[chosen][ordered]

@torch.inference_mode()
def score_block(models,reps,block):
    n=len(block)
    maxsize=max(len(r[1]) for r in block)
    padded=np.zeros((n,maxsize),np.int32)
    for pos,(_,candidates) in enumerate(block):
        padded[pos,:len(candidates)]=candidates
    item_ids=torch.as_tensor(padded,device="cuda",dtype=torch.long)
    best={}
    features={}
    for key,model in models.items():
        vecs=torch.as_tensor(reps[key][[i for i,_ in block]],
                             device="cuda",dtype=torch.float32)
        pred=(model.item(item_ids)*vecs[:,None,:]).sum(-1).cpu().numpy()
        for j,(_,candidates) in enumerate(block):
            sc=pred[j,:len(candidates)]
            top=np.partition(sc,-2)[-2:];top.sort()
            mean=float(sc.mean());std=float(sc.std())
            summary={"x_base_margin":float(top[-1]-top[-2]),
                "x_base_std":std,
                "x_base_top_z":float((top[-1]-mean)/max(std,1e-8)),
                "x_base_top_score":float(top[-1]),
                "x_base_score_mean":mean}
            best[(key,j)]=stable_top10(candidates,sc)
            features[(key,j)]=summary
    return best,features

def main(cache,g1,index,registry,preflight,out,block_size=16):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("G5-A one-shot cache already present; no overwrite")
    t0=time.monotonic()
    frozen=json.loads(registry.read_text())
    locked=json.loads(preflight.read_text())
    if (locked.get("status")!="ALL_SIX_CHECKPOINT_AND_POLICY_DIGESTS_VERIFIED"
       or locked["registry_sha256"]!=sha(registry)
       or locked["test_rows_opened"] is not False
       or frozen["target_test_events"]!=ROW_COUNT):
        raise ValueError("G5 immutable preflight must precede any TEST scoring")
    if sha(g1/"test_cohort_sealed.parquet")!=frozen["test_cohort_sha256"]:
        raise ValueError("TEST cohort byte digest mismatch")
    source=pq.read_table(g1/"test_cohort_sealed.parquet",
                         columns=["source_event_id","user_id","observed_at"])
    events=np.asarray(source.column("source_event_id").to_numpy(),np.int64)
    users=np.asarray(source.column("user_id").to_numpy(),np.int64)
    timestamps=source.column("observed_at").to_pylist()
    if len(events)!=ROW_COUNT or len(set(events.tolist()))!=len(events):
        raise ValueError("Frozen TEST event identity not intact")
    authors=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):i+1 for i,a in enumerate(authors)}
    snapshots,stream_events=histories(g1/"causal_stream_sealed.parquet",
                                      events,known)
    contexts=np.stack([x[0] for x in snapshots])
    n_authors=len(authors)
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Expected pre-authorized RTX 3090")
    models={}
    representations={}
    frozen_policies={}
    gates={}
    for seed,family in MODEL_KEYS:
        key=f"{seed}_{family}"
        doc=(cache/"klm3_g2_checkpoint_dev_selected_v1.json"
             if seed==20261012 else cache/f"klm3_g2_seed{seed}_dev_selected_v1.json")
        meta=json.loads(doc.read_text())["family_results"][family]["selected"]
        ck=cache/f"klm3_g2_seed{seed}_epoch3_v1"/family/meta["checkpoint"]
        if sha(ck)!=frozen["checkpoint_sha256"][str(seed)][family]:
            raise ValueError("G5-A selected Base model changed "+key)
        payload=torch.load(ck,map_location="cpu",weights_only=False)
        m=Encoder(n_authors,family)
        m.load_state_dict(payload["model_state"])
        m.cuda().eval()
        models[key]=m
        del payload
        all_vectors=[]
        with torch.inference_mode():
            for j in range(0,len(events),256):
                features=torch.as_tensor(contexts[j:j+256],device="cuda",dtype=torch.long)
                vectors=m(features).detach().cpu().numpy().astype(np.float32)
                if not np.isfinite(vectors).all():
                    raise FloatingPointError("Base representation invalid")
                all_vectors.append(vectors)
        representations[key]=np.concatenate(all_vectors)
        pdir=gate_path(cache,seed,family)
        threshold_file=pdir/"frozen_thresholds.json"
        if sha(threshold_file)!=frozen["policy_frozen_threshold_sha256"][str(seed)][family]:
            raise ValueError("G5-A policy file changed")
        p=json.loads(threshold_file.read_text())
        if p["state"]!="DEV_FROZEN_POINTWISE" or p["test_outcomes_seen"] is not False:
            raise ValueError("Bad DEV frozen policy")
        frozen_policies[key]=p
        mmanifest=json.loads((pdir/"models"/"oof_manifest.json").read_text())
        feats=mmanifest["feature_columns"]
        if len(feats)!=12:
            raise ValueError("Expected exact frozen 12 pretarget features")
        for obj in ("utility","difficulty","specialist"):
            path=pdir/"models"/(obj+".joblib")
            if sha(path)!=frozen["supervised_gate_model_sha256"][str(seed)][family][obj]:
                raise ValueError("Frozen HGB model file changed")
            gates[(key,obj)]=(joblib.load(path),feats)
    del authors
    counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),
                       minlength=n_authors+1).astype(np.float64)
    logs=np.log1p(counts)
    popularity=np.zeros(len(logs))
    popularity[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    npkeys=[f"{seed}_{family}" for seed,family in MODEL_KEYS]
    top10=np.empty((len(events),7,10),dtype=np.int32)
    feature_matrix=np.empty((len(events),6,12),dtype=np.float64)
    candidate_counts=np.empty(len(events),dtype=np.int32)
    incoming=[]
    count=0
    names=tuple(npkeys)
    feature_names=tuple(gates[(names[0],"utility")][1])
    if not all(tuple(gates[(key,obj)][1])==feature_names for key in names
       for obj in ("utility","difficulty","specialist")):
        raise ValueError("Frozen gate feature column order differs")
    def consume(block):
        nonlocal count
        ranks,score_feats=score_block(models,representations,block)
        for k,(i,candidate) in enumerate(block):
            seq,prior,recent,max_all,shared=snapshots[i]
            fixed=corrected_memory_score(candidate,popularity,prior,recent,max_all)
            top10[i,6]=stable_top10(candidate,fixed)
            support=sparse_history_support_share(candidate,prior)
            for m,key in enumerate(names):
                top10[i,m]=ranks[(key,k)]
                fields={**shared,**score_feats[(key,k)],
                        "x_memory_history_supported_share":support,
                        "x_candidate_log_count":math.log1p(len(candidate))}
                feature_matrix[i,m]=[fields[c] for c in feature_names]
            candidate_counts[i]=len(candidate)
        count+=len(block)
        if count%1000<block_size:
            print(json.dumps({"state":"G5_A_unlabeled_TEST_feature_scoring",
                              "n":count,"elapsed_s":round(time.monotonic()-t0,1)}),flush=True)
    for i,candidates in active_rosters(g1/"available_room_intervals.parquet",timestamps,known):
        if len(candidates)<10:
            raise ValueError("Empty/inadequate active warm author roster")
        incoming.append((i,candidates))
        if len(incoming)>=block_size:
            consume(incoming);incoming=[]
    if incoming: consume(incoming)
    if count!=ROW_COUNT or np.any(candidate_counts<10):
        raise ValueError("Incomplete TEST feature calculation")
    scores=np.empty((ROW_COUNT,6,5),dtype=np.float64)
    masks=np.empty((ROW_COUNT,6,5),dtype=np.bool_)
    for family_idx,key in enumerate(names):
        x=feature_matrix[:,family_idx]
        for method_idx,method in enumerate(METHODS):
            if method in ("utility","difficulty","specialist"):
                value=gates[(key,method)][0].predict(x)
            elif method=="uncertainty":
                value=-x[:,feature_names.index("x_base_margin")]
            else:
                value=x[:,feature_names.index("x_hist_event_count")]
            if not np.isfinite(value).all():
                raise ValueError("Nonfinite frozen TEST gate score")
            scores[:,family_idx,method_idx]=value
            threshold=frozen_policies[key]["methods"][method]["threshold"]
            masks[:,family_idx,method_idx]=(value>=threshold if threshold is not None
                                            else False)
    staging=out.with_name(out.name+".incomplete")
    staging.mkdir(parents=True,mode=0o700)
    for name,data in (("event_ids.npy",events),("user_ids.npy",users),
                      ("top10_author_tokens.npy",top10),
                      ("gate_score.npy",scores),("gate_calls.npy",masks),
                      ("candidate_counts.npy",candidate_counts)):
        np.save(staging/name,data,allow_pickle=False)
    manifest={
        "schema":"kbs-plan-c-g5-unlabeled-target-blind-test-v1",
        "status":"FROZEN_SIX_BASE_TEST_DECISIONS_BEFORE_OUTCOME_EVALUATION",
        "registry_sha256":sha(registry),
        "preflight_sha256":sha(preflight),
        "test_cohort_sha256":frozen["test_cohort_sha256"],
        "models":names,"methods":METHODS,
        "n_events":ROW_COUNT,
        "mean_active_warm_authors":float(candidate_counts.mean()),
        "median_active_warm_authors":float(np.median(candidate_counts)),
        "test_target_author_labels_loaded":False,
        "test_ranks_computed":False,
        "test_ndcg_computed":False,
        "unlabeled_prequential_prior_TEST_history_used":True,
        "no_TEST_model_or_threshold_fit":True,
        "file_sha256":{p.name:sha(p) for p in staging.glob("*.npy")},
        "elapsed_seconds":round(time.monotonic()-t0,1)}
    (staging/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    staging.rename(out)
    print(json.dumps({"status":manifest["status"],"n_events":ROW_COUNT,
       "elapsed_seconds":manifest["elapsed_seconds"],
       "test_metrics_computed":False}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for opt in ("cache","g1","index","registry","preflight","out"):
        p.add_argument("--"+opt,type=Path,required=True)
    p.add_argument("--block-size",type=int,default=16)
    a=p.parse_args()
    main(a.cache,a.g1,a.index,a.registry,a.preflight,a.out,a.block_size)
