#!/usr/bin/env python3
"""N10-C2-B: DEV-only counterbalanced, source-matched expanded offline timing.

Original G4 is a 256-request warmed component replay. This adds a separately
reported source-history construction and full-active candidate-roster sweep
plus alternating entire Base/Memory/Gate outputs, with pretarget-only rosters.

No new TEST or original B4-A target IDs, ranks or labels. This is *not*
production online latency; cold-data source scans are offline batch costs,
not legitimate per-online-request costs.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,math,platform,resource,time
from pathlib import Path
import numpy as np,pyarrow.parquet as pq,torch,joblib
from g2_train_base import Encoder
from g3_replay_correct_memory import replay_all_history,corrected_memory_score
from g4_sparse_gate_features import sparse_history_support_share
from g5_unlabeled_test_score import active_rosters,stable_top10

EVENTS=256
REPEATS=3
G1_SCHEMA="kbs-plan-c-full-active-dev-paired-v2"
POLICIES=("base_only","memory_only","frozen_utility_selector")
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(8<<20),b""):h.update(c)
    return h.hexdigest()
def require(x,msg):
    if not x:raise RuntimeError("N10 C2B DEV: "+msg)
def summary(v):
    a=np.asarray(v,dtype=np.float64)
    return {"n":len(a),"mean_ms":round(float(a.mean()),5),
      "median_ms":round(float(np.median(a)),5),
      "p95_ms":round(float(np.percentile(a,95)),5),
      "p99_ms":round(float(np.percentile(a,99)),5)}
def cutoff_sort(candidates,scores):
    return stable_top10(candidates,scores).astype(np.int32)
@torch.inference_mode()
def base_scores(model,ctx,candidates):
    x=torch.as_tensor(ctx[None],device="cuda",dtype=torch.long)
    cand=torch.as_tensor(candidates,device="cuda",dtype=torch.long)
    vec=model(x)
    pred=torch.mv(model.item.weight[cand],vec[0]).cpu().numpy()
    torch.cuda.synchronize()
    return pred
def gate_features(columns,row,score,candidates,warm):
    top=np.partition(score,-2)[-2:];top.sort()
    mean=float(score.mean());std=float(score.std())
    values={
      "x_base_margin":float(top[-1]-top[-2]),
      "x_base_std":std,
      "x_base_top_z":float((top[-1]-mean)/max(std,1e-8)),
      "x_base_top_score":float(top[-1]),
      "x_base_score_mean":mean,
      "x_candidate_log_count":math.log1p(len(candidates)),
      "x_memory_history_supported_share":sparse_history_support_share(candidates,warm)}
    for name in columns:
        if name not in values:
            if name not in ("x_hist_event_count","x_hist_warm_count",
               "x_hist_distinct","x_hist_repeat_max","x_hist_short_unique"):
                raise RuntimeError("unregistered gate feature "+name)
            values[name]=float(row[name])
    arr=np.asarray([[values[c] for c in columns]],dtype=np.float64)
    require(arr.shape==(1,12) and np.isfinite(arr).all(),"DEV gate feature invalid")
    return arr

def main(a):
    out=a.out
    if out.exists():raise FileExistsError("C2-B private output already exists; no overwrite")
    origin=time.monotonic()
    require(torch.cuda.is_available(),"GPU/3090 required for model parity and CUDA synchronization")
    report=json.loads((a.corrected/"summary.json").read_text())
    require(report["schema"]==G1_SCHEMA and report["n_scored"]==50049
            and report["memory_corrected_from_all_history"]
            and report["test_file_accessed"] is False,
            "corrected frozen DEV source report")
    source=a.corrected/"dev_full_active_pairs.csv"
    require(sha(source)==report["event_csv_sha256"],"DEV original label/feature source SHA drift")
    with source.open(newline="") as f:
        by_id={int(r["event_id"]):r for r in csv.DictReader(f)}
    require(len(by_id)==50049,"DEV unique event count mismatch")
    ids=np.load(a.dev/"dev_source_event_ids.npy",allow_pickle=False)
    ctx=np.load(a.dev/"dev_contexts.npy",mmap_mode="r")
    require(len(ids)==len(ctx)==50049 and set(ids.tolist())==set(by_id),
            "DEV only cache / CSV identity mismatch")
    chosen=np.unique(np.linspace(0,len(ids)-1,EVENTS,dtype=np.int64))
    require(len(chosen)==EVENTS,"sample count")
    request_ids=ids[chosen].astype(np.int64)
    with pq.ParquetFile(a.g1/"dev_cohort.parquet") as pf if False else open(__file__) as _:
        pass
    dev=pq.read_table(a.g1/"dev_cohort.parquet",columns=["source_event_id","observed_at"])
    require(np.array_equal(dev.column("source_event_id").to_numpy(),ids),
            "DEV cohort identity/source order")
    clocks=dev.column("observed_at").to_pylist()
    selected_clock=[clocks[int(i)] for i in chosen]
    names=np.load(a.index/"authors.npy",mmap_mode="r")
    known={int(z):i+1 for i,z in enumerate(names)}
    size=len(names)
    counts=np.bincount(np.load(a.index/"sequence_ids.npy",mmap_mode="r"),
                       minlength=size+1).astype(np.float64)
    logs=np.log1p(counts);pop=np.zeros(len(logs),dtype=np.float64)
    pop[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    t=time.perf_counter_ns()
    histories, scanned=replay_all_history(a.g1/"causal_stream_sealed.parquet",request_ids,known)
    history_prep_ms=(time.perf_counter_ns()-t)/1e6
    t=time.perf_counter_ns()
    candidates=[None]*EVENTS
    for i,c in active_rosters(a.g1/"available_room_intervals.parquet",selected_clock,known):
        require(len(c)>=10,"less than 10 F candidates")
        candidates[i]=c
    roster_prep_ms=(time.perf_counter_ns()-t)/1e6
    require(all(c is not None for c in candidates),"missing F roster")
    for n,i in enumerate(chosen):
        require(len(candidates[n])==int(by_id[int(ids[i])]["candidate_count"]),
                "source candidate count disagrees with corrected DEV")
        sparse=sparse_history_support_share(candidates[n],histories[n][0])
        require(np.isclose(sparse,float(by_id[int(ids[i])]["x_memory_history_supported_share"]),
                           atol=1e-12,rtol=0),"real DEV gate sparse-feature parity")
    selected=json.loads(a.selected.read_text())["family_results"]["sasrec"]["selected"]
    ck=a.g2/"sasrec"/selected["checkpoint"]
    require(sha(ck)==selected["checkpoint_sha256"],"Base checkpoint SHA not frozen")
    model=Encoder(size,"sasrec")
    state=torch.load(ck,map_location="cpu",weights_only=False)
    model.load_state_dict(state["model_state"])
    model.cuda().eval()
    gate=a.e2/"sasrec"/"models"/"utility.joblib"
    m=joblib.load(gate)
    oof=json.loads((a.e2/"sasrec"/"models"/"oof_manifest.json").read_text())
    fields=oof["feature_columns"]
    frozen=json.loads((a.e2/"sasrec"/"frozen_thresholds.json").read_text())
    threshold=frozen["methods"]["utility"]["threshold"]
    require(len(fields)==12 and threshold is not None,"frozen gate contract")
    require(m.n_features_in_==12,"gate shape changed")
    torch.cuda.synchronize()
    lat={p:[] for p in POLICIES}
    components=collections.defaultdict(list)
    top_digest=hashlib.sha256()
    selected_count=0
    consistency=0
    gpu_info=torch.cuda.get_device_name()
    torch.cuda.reset_peak_memory_stats()
    prestart=time.perf_counter_ns()
    for n in range(min(16,EVENTS)):
        c=candidates[n];warm,recent,longmax=histories[n]
        _=base_scores(model,np.asarray(ctx[chosen[n]],dtype=np.int64),c)
        _=corrected_memory_score(c,pop,warm,recent,longmax)
    torch.cuda.synchronize()
    warmup_ms=(time.perf_counter_ns()-prestart)/1e6
    for rep in range(REPEATS):
        # Rotate order across reps and request index; avoid systematically timing
        # one branch before another on warm CPU/GPU caches.
        for n in range(EVENTS):
            c=candidates[n]
            warm,recent,longmax=histories[n]
            seq=np.asarray(ctx[chosen[n]],dtype=np.int64)
            row=by_id[int(request_ids[n])]
            outputs={}
            base_out=None;mem_out=None
            for policy in [POLICIES[(n+rep+k)%3] for k in range(3)]:
                torch.cuda.synchronize()
                start=time.perf_counter_ns()
                if policy=="base_only":
                    score=base_scores(model,seq,c)
                    ranked=cutoff_sort(c,score)
                elif policy=="memory_only":
                    score=corrected_memory_score(c,pop,warm,recent,longmax)
                    ranked=cutoff_sort(c,score)
                else:
                    st=time.perf_counter_ns()
                    sc=base_scores(model,seq,c)
                    components["selected_base_ms"].append((time.perf_counter_ns()-st)/1e6)
                    st=time.perf_counter_ns()
                    features=gate_features(fields,row,sc,c,warm)
                    components["selected_feature_ms"].append((time.perf_counter_ns()-st)/1e6)
                    st=time.perf_counter_ns()
                    pred=float(m.predict(features)[0])
                    components["selected_gate_ms"].append((time.perf_counter_ns()-st)/1e6)
                    require(np.isfinite(pred),"nonfinite gate prediction")
                    choose=pred>=float(threshold)
                    selected_count+=int(choose)
                    if choose:
                        st=time.perf_counter_ns()
                        sc=corrected_memory_score(c,pop,warm,recent,longmax)
                        components["selected_memory_ms"].append((time.perf_counter_ns()-st)/1e6)
                    else:
                        components["selected_memory_ms"].append(0.)
                    ranked=cutoff_sort(c,sc)
                torch.cuda.synchronize()
                lat[policy].append((time.perf_counter_ns()-start)/1e6)
                outputs[policy]=ranked
            b=outputs["base_only"];mout=outputs["memory_only"];sel=outputs["frozen_utility_selector"]
            # DO NOT reveal or compute a relevant author / NDCG. Verify that
            # the selected Top-10 is one of the exact two designated outputs.
            require(np.array_equal(sel,b) or np.array_equal(sel,mout),
                    "selective output is neither Base nor Memory ranking")
            consistency+=1
            # Digest only, not user/creator/event IDs or raw private ranked lists.
            top_digest.update(sel.tobytes())
        print(json.dumps({"stage":"DEV_MATCHED_OFFLINE","completed_pass":rep+1,
             "passes":REPEATS,"n":EVENTS,"selected_calls":selected_count}),flush=True)
    nobs=EVENTS*REPEATS
    result={"schema":"kbs-n10-c2b-dev-matched-expanded-offline-v1",
      "status":"PASS_DEV_ONLY_NO_ONLINE_COST_CLAIM",
      "scope":"DEV_FIXED_256_REQUESTS_COUNTERBALANCED_WARMED_REPEATED_THREE_TIMES",
      "hardware":{"gpu":gpu_info,"torch":torch.__version__,"platform":platform.platform(),
           "cpu_ru_maxrss_kb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           "cuda_peak_allocated_bytes":torch.cuda.max_memory_allocated()},
      "sources":{"corrected_DEV_event_CSV_sha256":report["event_csv_sha256"],
           "G1_protocol_sha256":report["g1_protocol_sha256"],
           "Base_checkpoint_sha256":selected["checkpoint_sha256"],
           "frozen_primary_gate_path":"G3_E2_UTILITY_SASREC_DEV","threshold_regime":"DEV_OOF_NO_RETUNING"},
      "n_distinct_DEV_requests":EVENTS,"repeated_passes":REPEATS,
      "timed_request_path_invocations_per_policy":nobs,
      "history_replay_source_rows":int(scanned),
      "candidate_roster_allocation":["no target author passed to roster",
          "TRAIN-known live author interval sweep"],
      "setup_batch_ms":{"historical_full_source_batch_scan":round(history_prep_ms,3),
              "entire_interval_F_roster_batch_sweep":round(roster_prep_ms,3),
              "warmup_excluded":round(warmup_ms,3)},
      "warm_path_ms":{p:summary(v) for p,v in lat.items()},
      "selector_components_ms":{p:summary(v) for p,v in components.items()},
      "observed_selector_calls":int(selected_count),
      "observed_selector_call_rate":selected_count/nobs,
      "frozen_selector_output_parity_verified_n":consistency,
      "private_selection_digest_sha256_not_rank_export":top_digest.hexdigest(),
      "device_synchronized_before_and_after_each_branch":True,
      "run_path_counterbalanced_within_request":True,
      "data_scope":{"uses_DEV_only":True,"TEST_target_labels_loaded":False,
                    "B4A_labels_read":False,"A4_rerun":False,
                    "new_model_fit":False,"new_gate_threshold_tuned":False},
      "limit_not_measured":["live online incremental state maintenance",
        "network/queueing","production batching and concurrency",
        "data redistribution rights", "energy/cost in currency"],
      "interpretation":"Offline batch source construction is separately reported, not attributable as online latency per request. No claimed cost saving unless direct path measurement supports it.",
      "total_wall_seconds":round(time.monotonic()-origin,2)}
    if out.exists():raise FileExistsError("immutable output existed")
    out.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+"\n")
    print(json.dumps({"status":result["status"],"summaries":result["warm_path_ms"],
         "selector_call_frac":result["observed_selector_call_rate"],
         "B4A_rerun":False}),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("g1","index","dev","corrected","g2","selected","e2","out"):
        p.add_argument("--"+key,type=Path,required=True)
    a=p.parse_args();main(a)
