#!/usr/bin/env python3
"""G4 limited warmed offline DEV replay serving-path latency microbenchmark.

Measures pre-gate sparse support, frozen HGB gate, Base full-roster ranking
and selected vs Memory-only paths on the *same* event/candidate roster.
Excludes dataset IO, initial offline chronology reconstruction, network,
GPU concurrency, persistent state construction and model-load overhead.
Never claims an actual production speedup without deployment validation.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,time
from pathlib import Path
import numpy as np
import torch
import joblib
import pyarrow.parquet as pq

from g2_train_base import Encoder
from g3_dev_full_active import author_availability, ndcg
from g3_replay_correct_memory import replay_all_history,corrected_memory_score
from g4_sparse_gate_features import sparse_history_support_share

N=256
def h(path):
    d=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b""):
            d.update(chunk)
    return d.hexdigest()

def med(values):
    x=np.asarray(values,dtype=np.float64)
    return {"n":len(x),"median_ms":round(float(np.median(x)),4),
            "p90_ms":round(float(np.percentile(x,90)),4),
            "p95_ms":round(float(np.percentile(x,95)),4),
            "mean_ms":round(float(np.mean(x)),4)}

@torch.inference_mode()
def base_score(model,seq,cands,device="cuda"):
    vec=model(torch.as_tensor(seq[None],device=device,dtype=torch.long))
    scores=torch.mv(model.item.weight[torch.as_tensor(cands,device=device,dtype=torch.long)],
                    vec[0]).cpu().numpy()
    # The actual top-k operational output is determined without target labels.
    _=np.argpartition(scores,-10)[-10:]
    torch.cuda.synchronize()
    return scores

def run(g1,index,dev_cache,corrected,g2_trained,selected,e2,out):
    if out.exists():
        raise FileExistsError("Existing cost audit is immutable")
    manifest=json.loads((corrected/"summary.json").read_text())
    if (manifest["schema"]!="kbs-plan-c-full-active-dev-paired-v2" or
        not manifest["memory_corrected_from_all_history"] or
        manifest["test_file_accessed"] is not False or
        manifest["n_scored"]!=50049):
        raise ValueError("Corrected DEV-only source required")
    with (corrected/"dev_full_active_pairs.csv").open(newline="") as f:
        old={int(row["event_id"]):row for row in csv.DictReader(f)}
    if h(corrected/"dev_full_active_pairs.csv")!=manifest["event_csv_sha256"]:
        raise ValueError("Corrected source file digest mismatch")
    ids=np.load(dev_cache/"dev_source_event_ids.npy")
    positives=np.load(dev_cache/"dev_positive_author_tokens.npy")
    contexts=np.load(dev_cache/"dev_contexts.npy",mmap_mode="r")
    indices=np.unique(np.linspace(0,len(ids)-1,N,dtype=np.int64))
    if len(indices)!=N:
        raise ValueError("Bad fixed event sampling")
    times=pq.read_table(g1/"dev_cohort.parquet",
                         columns=["source_event_id","observed_at"])
    if not np.array_equal(times.column("source_event_id").to_numpy(),ids):
        raise ValueError("DEV history alignment changed")
    clock=times.column("observed_at").to_pylist()
    author=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):i+1 for i,a in enumerate(author)}
    snapshots,replayed=replay_all_history(
        g1/"causal_stream_sealed.parquet",ids[indices],known)
    pop_counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),
                           minlength=len(author)+1).astype(np.float64)
    log=np.log1p(pop_counts)
    pop=np.zeros(len(log),dtype=np.float64)
    pop[1:]=(log[1:]-log[1:].min())/(log[1:].max()-log[1:].min())
    cp_meta=json.loads(selected.read_text())["family_results"]["sasrec"]["selected"]
    ck=g2_trained/"sasrec"/cp_meta["checkpoint"]
    if h(ck)!=cp_meta["checkpoint_sha256"]:
        raise ValueError("G2 Base checksum changed")
    data=torch.load(ck,map_location="cpu",weights_only=False)
    model=Encoder(len(author),"sasrec")
    model.load_state_dict(data["model_state"])
    model.cuda().eval()
    del data
    gate_file=e2/"sasrec"/"models"/"utility.joblib"
    gate=joblib.load(gate_file)
    oof=json.loads((e2/"sasrec"/"models"/"oof_manifest.json").read_text())
    feature_cols=oof["feature_columns"]
    policy=json.loads((e2/"sasrec"/"frozen_thresholds.json").read_text())
    threshold=policy["methods"]["utility"]["threshold"]
    if threshold is None:
        raise ValueError("Cannot time a policy that never invokes specialist")
    if len(feature_cols)!=12:
        raise ValueError("Frozen gate feature count mismatch")
    lat={"base_only":[],"memory_only":[],"selective_total":[],
         "base_in_selective":[],"sparse_feature":[],"gate_inference":[],
         "memory_when_selected":[]}
    mismatch=0
    calls=0
    durations=[]
    timer=time.perf_counter_ns
    for n,(i,candidates,_) in enumerate(author_availability(
        g1/"available_room_intervals.parquet",
        [clock[i] for i in indices],positives[indices],known)):
        srcidx=int(indices[i])
        event_id=int(ids[srcidx])
        old_row=old[event_id]
        if len(candidates)!=int(old_row["candidate_count"]):
            raise ValueError("Changed DEV author roster")
        warm,recent,longmax=snapshots[i]
        # Exact parity on real unseen-by-the-code DEV events, without target labels.
        sparse=sparse_history_support_share(candidates,warm)
        dense_ref=float(old_row["x_memory_history_supported_share"])
        if not np.isclose(sparse,dense_ref,atol=1e-12,rtol=0):
            mismatch+=1
        recent=tuple(recent)
        seq=np.asarray(contexts[srcidx],dtype=np.int64)
        # Timings are warmed same-machine replay. Two independent paths each
        # use their own model and state, and do not include source IO or state build.
        t0=timer()
        _=base_score(model,seq,candidates)
        base_ms=(timer()-t0)/1e6
        t0=timer()
        m=corrected_memory_score(candidates,pop,warm,recent,longmax)
        _=np.argpartition(m,-10)[-10:]
        memory_ms=(timer()-t0)/1e6
        # Real selective path starts with Base and recomputes the observable
        # score-summary features. No oracle or target rank enters gate inputs.
        t0=timer()
        scores=base_score(model,seq,candidates)
        b_ms=(timer()-t0)/1e6
        t0=timer()
        candidate_vals=np.partition(scores,-2)[-2:]
        candidate_vals.sort()
        mean=float(scores.mean())
        std=float(scores.std())
        derived={
            "x_base_margin":float(candidate_vals[-1]-candidate_vals[-2]),
            "x_base_std":std,
            "x_base_top_z":float((candidate_vals[-1]-mean)/max(std,1e-8)),
            "x_base_top_score":float(candidate_vals[-1]),
            "x_base_score_mean":mean,
            "x_candidate_log_count":math.log1p(len(candidates)),
            "x_memory_history_supported_share":sparse}
        # Other numerical pretarget history aggregates are maintained
        # as user-state counters; source read is outside timed serving path.
        for name in feature_cols:
            if name not in derived:
                derived[name]=float(old_row[name])
        feature_ms=(timer()-t0)/1e6
        t0=timer()
        gate_score=float(gate.predict(np.asarray(
            [[derived[name] for name in feature_cols]],dtype=np.float64))[0])
        gate_ms=(timer()-t0)/1e6
        take=gate_score>=float(threshold)
        selected_memory_ms=0.
        if take:
            t0=timer()
            ms=corrected_memory_score(candidates,pop,warm,recent,longmax)
            _=np.argpartition(ms,-10)[-10:]
            selected_memory_ms=(timer()-t0)/1e6
            calls+=1
        lat["base_only"].append(base_ms)
        lat["memory_only"].append(memory_ms)
        lat["base_in_selective"].append(b_ms)
        lat["sparse_feature"].append(feature_ms)
        lat["gate_inference"].append(gate_ms)
        lat["memory_when_selected"].append(selected_memory_ms)
        lat["selective_total"].append(b_ms+feature_ms+gate_ms+selected_memory_ms)
        if (n+1)%64==0:
            print(json.dumps({"events":n+1,"selected_calls":calls,
                              "median_selective_ms":float(np.median(lat["selective_total"]))}),flush=True)
    if mismatch:
        raise ValueError(f"Sparse feature real-DEV parity mismatches: {mismatch}")
    result={
        "schema":"kbs-plan-c-g4-warmed-dev-replay-cost-v1",
        "dataset":"M3 author ranking full-active warm candidates",
        "family":"sasrec","seed":20261012,"n_events":N,
        "g1_protocol_sha256":manifest["g1_protocol_sha256"],
        "source_corrected_memory_sha256":manifest["event_csv_sha256"],
        "base_checkpoint_sha256":cp_meta["checkpoint_sha256"],
        "DEV_frozen_utility_threshold":float(threshold),
        "selected_calls":calls,"actual_selected_fraction_on_sample":calls/N,
        "measured_ms":{k:med(v) for k,v in lat.items()},
        "corrected_memory_feature_real_parity":mismatch==0,
        "history_events_replayed_for_setup":replayed,
        "test_file_opened":False,
        "test_outcomes_inspected":False,
        "models_trained":False,
        "source_events_raw_ids_exported":False,
        "important_exclusions":["offline history reconstruction","incremental maintenance of user state",
            "candidate interval maintenance","input data loading","GPU contention",
            "batch serving optimization","network response time"],
        "scope":"WARMED_OFFLINE_DEV_REPLAY_MICROBENCHMARK_NOT_PRODUCTION_LATENCY"}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for opt in ("g1","index","dev","corrected","g2_trained","selected","e2","out"):
        p.add_argument("--"+opt.replace("_","-"),type=Path,required=True)
    a=p.parse_args()
    run(a.g1,a.index,a.dev,a.corrected,a.g2_trained,a.selected,a.e2,a.out)
