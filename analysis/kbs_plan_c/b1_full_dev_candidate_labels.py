#!/usr/bin/env python3
"""B1-2 DEV-only: build sampled-candidate supervision reusing verified full F labels.

No G5 TEST, no training, no event-level export. Reconstruct one history and
one live-roster stream, batch sampled-only scores on frozen GPU encoders.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
import pyarrow.parquet as pq
import torch

from b1_fast_roster_dev_check import availability_vectorized
from g3_dev_full_active import load_models, representations, score_batch, ndcg
from g3_replay_correct_memory import replay_all_history, corrected_memory_score, rank as memory_rank
from b1_dev_regime_pilot import deterministic_sample, true_rank

N = 50049
SEED = 20261012

def digest(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(8<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def generate(root,out,batch):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("B1 output or unfinished stage already exists")
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Frozen B1 full DEV uses self-host RTX3090")
    if batch < 32 or batch > 1024:
        raise ValueError("Invalid sampled-candidate GPU batch")
    torch.backends.cuda.matmul.allow_tf32=False
    torch.set_float32_matmul_precision("highest")
    g1=root/"klm3_plan_c_g1_v1"
    index=root/"klm3_g2_train_index_v1"
    dev=root/"klm3_g2_dev_checkpoint_screen_v1"
    corr=root/"klm3_g3_dev_fullactive_base_memory_corrected_v1"
    models_root=root/"klm3_g2_seed20261012_epoch3_v1"
    selection=root/"klm3_g2_checkpoint_dev_selected_v1.json"
    srcm=json.loads((corr/"summary.json").read_text())
    im=json.loads((index/"index_manifest.json").read_text())
    gm=json.loads((g1/"manifest.json").read_text())
    dm=json.loads((dev/"manifest.json").read_text())
    selected=json.loads(selection.read_text())
    if not (srcm["schema"]=="kbs-plan-c-full-active-dev-paired-v2"
            and srcm.get("memory_corrected_from_all_history") is True
            and srcm.get("scope")=="DEV_ONLY"
            and srcm.get("test_file_accessed") is False
            and srcm.get("n_scored")==N
            and selected["test_data_opened"] is False
            and gm["protocol_sha256"]==im["g1_protocol_sha256"]==dm["g1_protocol_sha256"]):
        raise RuntimeError("Not the accepted DEV-only corrected source")
    source=corr/"dev_full_active_pairs.csv"
    if digest(source)!=srcm["event_csv_sha256"]:
        raise RuntimeError("Corrected full F DEV evidence SHA mismatch")
    with source.open(newline="") as f:
        reader=csv.DictReader(f)
        rows={int(x["event_id"]):x for x in reader}
    if len(rows)!=N:
        raise RuntimeError("Original DEV event identities incomplete")
    events=np.load(dev/"dev_source_event_ids.npy",mmap_mode="r")
    pos=np.load(dev/"dev_positive_author_tokens.npy",mmap_mode="r")
    contexts=np.load(dev/"dev_contexts.npy",mmap_mode="r")
    for name in ("dev_source_event_ids.npy","dev_positive_author_tokens.npy","dev_contexts.npy"):
        if digest(dev/name)!=dm["files_sha256"][name]:
            raise RuntimeError("G2 frozen DEV snapshot hash mismatch")
    times=pq.read_table(g1/"dev_cohort.parquet",
                        columns=["source_event_id","observed_at"])
    if not np.array_equal(times.column("source_event_id").to_numpy(),events):
        raise RuntimeError("G1/G2 source ordering differs")
    clocks=times.column("observed_at").to_pylist()
    author_ids=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):i+1 for i,a in enumerate(author_ids)}
    if len(events)!=N or any(int(e) not in rows for e in events):
        raise RuntimeError("Full original DEV event coverage required")
    start=time.monotonic()
    hist_started=time.monotonic()
    history,scanned=replay_all_history(g1/"causal_stream_sealed.parquet",
                                       events,known)
    hist_seconds=time.monotonic()-hist_started
    counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),
                       minlength=len(author_ids)+1).astype(np.float64)
    p=np.log1p(counts)
    popularity=np.zeros(len(counts),dtype=np.float64)
    popularity[1:]=(p[1:]-p[1:].min())/(p[1:].max()-p[1:].min())
    sampled=np.empty((N,575),dtype=np.int32)
    sampled_memory_ndcg=np.empty(N,dtype=np.float64)
    full_count=np.empty(N,dtype=np.int32)
    roster_started=time.monotonic()
    for j,cand,_ in availability_vectorized(
            g1/"available_room_intervals.parquet",clocks,pos,known,len(author_ids)):
        old=rows[int(events[j])]
        if len(cand)!=int(old["candidate_count"]):
            raise RuntimeError("Candidate universe differs from corrected F reference")
        f=deterministic_sample(cand,int(pos[j]),int(events[j]))
        sampled[j]=f
        warm,recent,longmax=history[j]
        mem=corrected_memory_score(f,popularity,warm,recent,longmax)
        sampled_memory_ndcg[j]=ndcg(memory_rank(f,mem,int(pos[j])))
        full_count[j]=len(cand)
    roster_seconds=time.monotonic()-roster_started
    del history
    model_started=time.monotonic()
    models=load_models(models_root,im,selected,"cuda")
    reps=representations(models,contexts,"cuda",batch=512)
    model_seconds=time.monotonic()-model_started
    eval_start=time.monotonic()
    sample_base={f:np.empty(N,dtype=np.float64) for f in ("sasrec","gru4rec")}
    torch.cuda.reset_peak_memory_stats()
    for b in range(0,N,batch):
        hi=min(b+batch,N)
        output=score_batch(models,reps,list(range(b,hi)),sampled[b:hi],"cuda")
        for family,scores in output.items():
            for local,j in enumerate(range(b,hi)):
                sample_base[family][j]=ndcg(true_rank(sampled[j],scores[local],int(pos[j])))
        if hi % 5000 < batch:
            print(json.dumps({"phase":"B1_sampled_DEV_scores","rows":hi,
                "elapsed_s":round(time.monotonic()-start,1)}),flush=True)
    torch.cuda.synchronize()
    eval_seconds=time.monotonic()-eval_start
    peak=float(torch.cuda.max_memory_allocated())/2**20
    stage=out.with_name(out.name+".incomplete")
    stage.mkdir(parents=True,mode=0o700)
    outcsv=stage/"dev_pair_candidate_labels.csv"
    maincols=list(next(iter(rows.values())).keys())
    added=["sampled_memory_ndcg10","sampled_sasrec_ndcg10",
           "sampled_gru4rec_ndcg10","b1_sampled_candidate_count"]
    if any(k in maincols for k in added):
        raise RuntimeError("B1 sampled columns collide with original DEV")
    with outcsv.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=maincols+added)
        writer.writeheader()
        for j,event in enumerate(events):
            d=dict(rows[int(event)])
            d.update(sampled_memory_ndcg10=repr(float(sampled_memory_ndcg[j])),
                     sampled_sasrec_ndcg10=repr(float(sample_base["sasrec"][j])),
                     sampled_gru4rec_ndcg10=repr(float(sample_base["gru4rec"][j])),
                     b1_sampled_candidate_count=575)
            writer.writerow(d)
    report={
        "schema":"kbs-b1-full-dev-paired-candidate-labels-v1",
        "status":"PASS",
        "scope":"DEV_ONLY_POST_G5_EXPLORATORY",
        "test_accessed":False,"model_training":False,
        "new_g5_confirmatory_inference":False,
        "event_level_uploaded":False,
        "n_dev_events":N,"n_users":len({x["user_id"] for x in rows.values()}),
        "checkpoint_count":2,"gpu_batch_size":batch,
        "full_candidate_count_min":int(full_count.min()),
        "full_candidate_count_max":int(full_count.max()),
        "sampled_candidate_count":575,
        "target_retained_sampling_offline_labels_only":True,
        "gate_feature_columns_unchanged_from_frozen_F":True,
        "corrected_F_source_sha256":srcm["event_csv_sha256"],
        "private_event_source_csv_sha256":digest(outcsv),
        "mean_frozen_full_NDCG":{k:float(np.mean([float(rows[int(e)][k+"_ndcg10"]) for e in events]))
                              for k in ("memory","sasrec","gru4rec")},
        "mean_new_sampled_NDCG":{
            "memory":float(sampled_memory_ndcg.mean()),
            **{k:float(v.mean()) for k,v in sample_base.items()}},
        "time_seconds":{"history_replay":round(hist_seconds,2),
            "roster_and_sampled_corrected_memory":round(roster_seconds,2),
            "checkpoint_and_context":round(model_seconds,2),
            "sampled_GPU_and_rank":round(eval_seconds,2),
            "overall":round(time.monotonic()-start,2)},
        "cuda_peak_memory_MiB":round(peak,1),
        "source_history_rows_scanned":int(scanned),
        "B1_nested_gate_fitted":False
    }
    (stage/"summary.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    stage.rename(out)
    # No private paths or ids in stdout.
    print(json.dumps({"B1_stage2":report["status"],"n_dev":N,
        "full_average":report["mean_frozen_full_NDCG"],
        "sampled_average":report["mean_new_sampled_NDCG"],
        "seconds":report["time_seconds"],
        "gpu_peak_MiB":report["cuda_peak_memory_MiB"]}),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--batch",type=int,default=512)
    a=p.parse_args()
    generate(a.root,a.output,a.batch)


if __name__=="__main__":
    main()
