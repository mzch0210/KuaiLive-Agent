#!/usr/bin/env python3
"""Plan C DEV-only full-active paired Base/Memory scoring with a single room sweep.

All event-level artifacts remain in the User-host cache. Never read a TEST file.
Follows G0F weights: train-only normalized log popularity (0.10),
last-ten exponential short history (0.45), all-prior count/max long history (0.45).
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import heapq
import json
import math
import os
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch

from g2_train_base import Encoder

SHORT_K = 10
SHORT_DECAY = 3.0
WEIGHTS = (0.10, 0.45, 0.45)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8*1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def score_history(candidates, popularity, prior_map, recent):
    """Fixed target-blind Memory scores in token order (token reflects raw ID)."""
    candidates = np.asarray(candidates, dtype=np.int32)
    score = 0.10 * popularity[candidates].astype(np.float64)
    if prior_map:
        keys = np.fromiter(prior_map.keys(), dtype=np.int32, count=len(prior_map))
        cnt = np.fromiter(prior_map.values(), dtype=np.float64, count=len(prior_map))
        order = np.argsort(keys)
        keys, cnt = keys[order], cnt[order]
        ix = np.searchsorted(keys, candidates)
        valid = ix < len(keys)
        valid[valid] &= keys[ix[valid]] == candidates[valid]
        score[valid] += 0.45 * cnt[ix[valid]] / cnt.max()
    if recent:
        vals = {}
        for dist, author in enumerate(reversed(recent)):
            score_t = math.exp(-dist/SHORT_DECAY)
            vals[author] = max(vals.get(author, 0.), score_t)
        keys = np.array(sorted(vals), dtype=np.int32)
        strengths = np.array([vals[k] for k in keys], dtype=np.float64)
        ix = np.searchsorted(keys, candidates)
        valid = ix < len(keys)
        valid[valid] &= keys[ix[valid]] == candidates[valid]
        score[valid] += 0.45 * strengths[ix[valid]]
    return score


def memory_rank(candidates, scores, true_id):
    """Target rank with deterministic author-ID tie break, zero-based 0 is best."""
    i = np.flatnonzero(candidates == true_id)
    if len(i) != 1:
        raise ValueError("target must occur once in the exact eligible roster")
    ref = float(scores[i[0]])
    return 1 + int(np.count_nonzero((scores > ref + 1e-12) |
                  ((np.abs(scores-ref) <= 1e-12) & (candidates < true_id))))


def ndcg(rank):
    return float(1.0/math.log2(rank+1)) if rank <= 10 else 0.0


def build_dev_histories(stream_path, dev_event_ids, known_to_index, stride=2000000):
    """Replay TRAIN + previous DEV in sorted user-time order; never consume TEST."""
    import pyarrow.parquet as pq
    indices = {int(x):i for i,x in enumerate(dev_event_ids)}
    histories=[None]*len(indices)
    features=[None]*len(indices)
    last_user=None
    count=collections.Counter()
    recent=collections.deque(maxlen=SHORT_K)
    warm_hist_total=0
    all_hist_total=0
    processed=0
    captured=0
    reader=pq.ParquetFile(stream_path)
    for block in reader.iter_batches(batch_size=262144,
              columns=["source_event_id","user_id","author_id","split"]):
        d=block.to_pydict()
        for e,u,author,split in zip(d["source_event_id"],d["user_id"],
                                    d["author_id"],d["split"]):
            if split=="TEST":
                continue
            processed+=1
            if u != last_user:
                last_user=u
                count.clear()
                recent.clear()
                warm_hist_total=0
                all_hist_total=0
            j=indices.get(int(e))
            if j is not None:
                if split!="DEV" or histories[j] is not None:
                    raise ValueError("non-DEV history match or duplicate id")
                # Freeze counts and short horizon strictly before this event.
                histories[j]=(dict(count), tuple(recent))
                captured+=1
                features[j]={"hist_events_all":all_hist_total,
                             "hist_events_warm":warm_hist_total,
                             "hist_distinct_warm":len(count),
                             "hist_short_unique":len(set(recent)),
                             "hist_max_repeat":max(count.values()) if count else 0}
            token=known_to_index.get(int(author))
            all_hist_total+=1
            if token is not None:
                count[token]+=1
                recent.append(token)
                warm_hist_total+=1
            if stride and processed % stride==0:
                print(json.dumps({"phase":"memory_history_scan","events":processed,
                                  "dev_captured":captured}),flush=True)
    if any(x is None for x in histories):
        raise ValueError("Unable to capture all DEV target histories")
    return histories,features,processed


def author_availability(rooms_file, sample_times, token_targets, known_to_index):
    """Yield (row index, sorted active distinct known-author tokens) once in time order."""
    import pyarrow.parquet as pq
    order=sorted(range(len(sample_times)),key=lambda i:(sample_times[i],i))
    room_file=pq.ParquetFile(rooms_file)
    def rooms():
        for batch in room_file.iter_batches(batch_size=131072,
                    columns=["open_ts","close_ts","author_id"]):
            data=batch.to_pydict()
            yield from zip(data["open_ts"],data["close_ts"],data["author_id"])
    it=iter(rooms())
    ahead=next(it,None)
    heap=[]
    active=collections.Counter()
    max_rooms=0
    for ix in order:
        t=sample_times[ix]
        while ahead is not None and ahead[0] <= t:
            start,end,author=ahead
            token=known_to_index.get(int(author))
            if token is not None and end > t:
                active[token]+=1
                heapq.heappush(heap,(end,token))
            ahead=next(it,None)
        while heap and heap[0][0] <= t:
            _,token=heapq.heappop(heap)
            active[token]-=1
            if active[token]==0:
                del active[token]
        target=int(token_targets[ix])
        if target not in active:
            raise ValueError("frozen DEV target not available at pretarget clock")
        max_rooms=max(max_rooms,len(heap))
        yield ix,np.fromiter(sorted(active),dtype=np.int32,count=len(active)),max_rooms


def prepare(input_g1, train_idx, dev_cache, dev_select, seed=20261012, limit=None):
    import pyarrow.parquet as pq
    a=json.loads((input_g1/"manifest.json").read_text())
    i=json.loads((train_idx/"index_manifest.json").read_text())
    d=json.loads((dev_cache/"manifest.json").read_text())
    s=json.loads(dev_select.read_text())
    if (a["schema"]!="kbs-plan-c-g1-derived-v1"
            or d["schema"]!="kbs-plan-c-g2-dev-screen-v1"
            or s["schema"]!="kbs-plan-c-g2-checkpoint-selection-dev-only-v1"
            or a["protocol_sha256"]!=d["g1_protocol_sha256"]
            or a["protocol_sha256"]!=i["g1_protocol_sha256"]
            or s["test_data_opened"] is not False):
        raise ValueError("G1/G2 DEV-frozen provenance mismatch")
    for name in ("dev_contexts.npy","dev_positive_author_tokens.npy",
                 "dev_source_event_ids.npy"):
        if sha(dev_cache/name)!=d["files_sha256"][name]:
            raise ValueError("DEV snapshot SHA mismatch")
    events=np.load(dev_cache/"dev_source_event_ids.npy")
    positives=np.load(dev_cache/"dev_positive_author_tokens.npy")
    contexts=np.load(dev_cache/"dev_contexts.npy",mmap_mode="r")
    author_ids=np.load(train_idx/"authors.npy",mmap_mode="r")
    known={int(a):j+1 for j,a in enumerate(author_ids)}
    dev=pq.read_table(input_g1/"dev_cohort.parquet",
                      columns=["source_event_id","user_id","observed_at"])
    check=np.asarray(dev.column("source_event_id").to_numpy(),dtype=np.int64)
    if not np.array_equal(check,events):
        raise ValueError("DEV row order mismatch")
    clock=dev.column("observed_at").to_pylist()
    users=np.asarray(dev.column("user_id").to_numpy(),dtype=np.int64)
    if limit is not None:
        if not (0 < limit <= len(events)):
            raise ValueError("invalid DEV-only evaluation limit")
        # Selection is strictly independent of target/rank information.
        selected=np.unique(np.linspace(0,len(events)-1,limit,dtype=np.int64))
    else:
        selected=np.arange(len(events),dtype=np.int64)
    # Histories are built once for exactly the designated DEV events.
    hist,features,processed=build_dev_histories(
        input_g1/"causal_stream_sealed.parquet",events[selected],known)
    counts=np.bincount(np.load(train_idx/"sequence_ids.npy",mmap_mode="r"),
                       minlength=len(author_ids)+1).astype(np.float64)
    logpop=np.log1p(counts)
    pmin=np.min(logpop[1:])
    pmax=np.max(logpop[1:])
    if not pmax>pmin:
        raise ValueError("invalid train-only popularity")
    popularity=np.zeros(len(counts),dtype=np.float64)
    popularity[1:] = (logpop[1:]-pmin)/(pmax-pmin)
    return dict(g1=a,index=i,dev=d,selected=s,
                indices=selected,events=events,users=users,clock=clock,
                positives=positives,contexts=contexts,
                train_counts=counts,popularity=popularity,
                histories=hist,features=features,known=known,
                history_scanned=processed)


def load_models(training_root, index_manifest, dev_selected, device):
    models={}
    n=index_manifest["unique_train_authors"]
    for family in ("sasrec","gru4rec"):
        meta=dev_selected["family_results"][family]["selected"]
        ck=training_root/family/meta["checkpoint"]
        if sha(ck)!=meta["checkpoint_sha256"]:
            raise ValueError("DEV-selected checkpoint digest mismatch")
        cp=torch.load(ck,map_location="cpu",weights_only=False)
        if (cp["model_family"]!=family or cp["test_used"] is not False
                or cp["dev_selected"] is not False):
            raise ValueError("Unexpected checkpoint identity")
        m=Encoder(n,family)
        m.load_state_dict(cp["model_state"])
        m.to(device).eval()
        models[family]=m
        del cp
    return models


@torch.inference_mode()
def representations(models,context,device,batch=256):
    ans={}
    for family,model in models.items():
        outputs=[]
        for offset in range(0,len(context),batch):
            inp=torch.as_tensor(np.asarray(context[offset:offset+batch]),
                                dtype=torch.long,device=device)
            r=model(inp).detach().cpu().numpy().astype(np.float32)
            if not np.isfinite(r).all():
                raise FloatingPointError("invalid Base representation")
            outputs.append(r)
        ans[family]=np.concatenate(outputs)
    return ans


def score_batch(models, reps, context_ids, candidates, device):
    """Same candidates, different frozen Base checkpoints; zero TEST access."""
    array=np.asarray(candidates,dtype=np.int64)
    candidates_t=torch.as_tensor(array,device=device,dtype=torch.long)
    output={}
    for name,model in models.items():
        vec=torch.as_tensor(reps[name][context_ids],device=device)
        emb=model.item(candidates_t)
        pred=torch.einsum("bd,bkd->bk",vec,emb).cpu().numpy()
        if not np.isfinite(pred).all():
            raise FloatingPointError("nonfinite candidate scores")
        output[name]=pred
    return output


def full_dev_scoring(g1, train_idx, dev_cache, selection_file, train_root,
                     output, limit=None, block=12, progress=500):
    if output.exists():
        raise FileExistsError("Do not overwrite existing DEV evidence")
    t0=time.monotonic()
    prepared=prepare(g1,train_idx,dev_cache,selection_file,limit=limit)
    dev_idx=prepared["indices"]
    device="cuda"
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("User-host RTX3090 required")
    models=load_models(train_root,prepared["index"],prepared["selected"],device)
    reps=representations(models,prepared["contexts"][dev_idx],device)
    output.mkdir(parents=True,mode=0o700)
    rows=[]
    metrics=collections.defaultdict(lambda:collections.Counter())
    incoming=[]
    sample_time=[prepared["clock"][i] for i in dev_idx]
    for event_id,candidates,rooms in author_availability(
            g1/"available_room_intervals.parquet",
            sample_time,prepared["positives"][dev_idx],prepared["known"]):
        incoming.append((event_id,candidates,rooms))
        if len(incoming)<block:
            continue
        # Keep exact per-event candidates (may vary from 14k to >55k).
        rows.extend(score_work_block(incoming,models,reps,prepared,dev_idx,device))
        incoming.clear()
        if progress and len(rows)%progress < block:
            print(json.dumps({"stage":"DEV_full_active","rows":len(rows),
                "elapsed_s":round(time.monotonic()-t0,1)}),flush=True)
    if incoming:
        rows.extend(score_work_block(incoming,models,reps,prepared,dev_idx,device))
    if len(rows)!=len(dev_idx):
        raise ValueError("incomplete DEV event scoring")
    rows.sort(key=lambda x:int(x["event_id"]))
    columns=list(rows[0])
    out_csv=output/"dev_full_active_pairs.csv"
    with out_csv.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    summary={"schema":"kbs-plan-c-full-active-dev-paired-v1",
             "scope":"DEV_ONLY","n_scored":len(rows),
             "all_dev_scored":limit is None,
             "base_checkpoint_sha":{family:prepared["selected"]["family_results"][family]["selected"]["checkpoint_sha256"] for family in models},
             "g1_protocol_sha256":prepared["g1"]["protocol_sha256"],
             "event_csv_sha256":sha(out_csv),
             "source_test_outcomes_inspected":False,
             "test_file_accessed":False,
             "gates_fit":False,
             "memory_definition":"0.10 train-logpop + 0.45 exp(-distance/3) last10 + 0.45 prior-count/maxcount",
             "median_active_candidates":float(np.median([r["candidate_count"] for r in rows])),
             "history_events_scanned":prepared["history_scanned"],
             "elapsed_seconds":round(time.monotonic()-t0,1),
             "aggregate":{}}
    for label in ("sasrec","gru4rec","memory"):
        metric=np.asarray([float(r[label+"_ndcg10"]) for r in rows])
        summary["aggregate"][label]={"ndcg10":float(metric.mean()),
             "hr10":float(np.mean([int(r[label+"_rank"])<=10 for r in rows]))}
    for base in ("sasrec","gru4rec"):
        delta=np.asarray([float(r["memory_ndcg10"])-float(r[base+"_ndcg10"]) for r in rows])
        summary["aggregate"][base]["memory_minus_base_ndcg10"]=float(delta.mean())
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary),flush=True)
    return summary


def score_work_block(block, models, reps, state, selected, device):
    maxsize=max(len(x[1]) for x in block)
    padded=np.zeros((len(block),maxsize),dtype=np.int32)
    for j,(idx,vals,_) in enumerate(block):
        padded[j,:len(vals)]=vals
    raw=score_batch(models,reps,
                    [x[0] for x in block],padded,device)
    output=[]
    for j,(ix,candidate,rooms) in enumerate(block):
        original=int(selected[ix])
        uid=int(state["users"][original])
        true_id=int(state["positives"][original])
        past,recent=state["histories"][ix]
        mem=score_history(candidate,state["popularity"],past,recent)
        m_rank=memory_rank(candidate,mem,true_id)
        d={"event_id":int(state["events"][original]),"user_id":uid,
           "split":"DEV","candidate_count":len(candidate),
           "memory_rank":m_rank,"memory_ndcg10":ndcg(m_rank),
           "x_hist_event_count":float(state["features"][ix]["hist_events_all"]),
           "x_hist_warm_count":float(state["features"][ix]["hist_events_warm"]),
           "x_hist_distinct":float(state["features"][ix]["hist_distinct_warm"]),
           "x_hist_repeat_max":float(state["features"][ix]["hist_max_repeat"]),
           "x_hist_short_unique":float(state["features"][ix]["hist_short_unique"]),
           "x_memory_history_supported_share":float(np.mean((mem-0.10*state["popularity"][candidate])>1e-12)),
           "x_candidate_log_count":float(math.log1p(len(candidate)))}
        for model in ("sasrec","gru4rec"):
            scores=raw[model][j,:len(candidate)]
            true_score=float(scores[np.searchsorted(candidate,true_id)])
            outrank=(scores>true_score)|((scores==true_score)&(candidate<true_id))
            rank=1+int(np.count_nonzero(outrank))
            top=np.partition(scores,-min(11,len(scores)))[-min(11,len(scores)):]
            top.sort()
            top1=float(top[-1])
            top2=float(top[-2])
            mean=float(np.mean(scores))
            std=float(np.std(scores))
            d[model+"_rank"]=rank
            d[model+"_ndcg10"]=ndcg(rank)
            d["x_"+model+"_base_margin"]=top1-top2
            d["x_"+model+"_base_std"]=std
            d["x_"+model+"_base_top_z"]=(top1-mean)/max(std,1e-8)
            d["x_"+model+"_base_top_score"]=top1
            d["x_"+model+"_base_score_mean"]=mean
        output.append(d)
    return output


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--train-index",type=Path,required=True)
    p.add_argument("--dev",type=Path,required=True)
    p.add_argument("--selected",type=Path,required=True)
    p.add_argument("--train-root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--limit",type=int)
    p.add_argument("--block",type=int,default=12)
    a=p.parse_args()
    full_dev_scoring(a.g1,a.train_index,a.dev,a.selected,a.train_root,
                     a.out,limit=a.limit,block=a.block)


if __name__=="__main__":
    main()
