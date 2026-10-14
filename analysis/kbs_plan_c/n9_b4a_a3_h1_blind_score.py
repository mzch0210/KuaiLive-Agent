#!/usr/bin/env python3
"""B4-A A3 H1 target-blind 30,000 full-active requests, frozen F/S gate policies.

Reads only A1 event/user/clock metadata as *evaluation targets*. The causal
history stream has author IDs for events already observed; snapshots and
rankings for a request are assembled before its own author is incorporated.
No target labels, ranks, HR/NDCG or post-outcome decisions are generated.

A4 is NOT implemented here. H2 null predictions must be sealed separately
before any label reveal. Private .npy outputs must never be uploaded to GitHub.
"""
from __future__ import annotations
import argparse,hashlib,json,math,time
from pathlib import Path
import joblib,numpy as np,pyarrow.parquet as pq,torch
from g2_train_base import Encoder
from g3_replay_correct_memory import corrected_memory_score
from g4_sparse_gate_features import sparse_history_support_share
from g5_unlabeled_test_score import histories,active_rosters,score_block,stable_top10

EXPECTED_A1="be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14"
EXPECTED_SUB="40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059"
EXPECTED_DEV="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
SEED=20261012
FAMILIES=("sasrec","gru4rec")
ARMS=("S_aligned","F_aligned")
N=30000

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def require(condition,reason):
    if not condition:raise RuntimeError(reason)

def main(cache,g1,index,a1,a2,source_preflight,registry,out,batch_size=16):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("One-shot A3 H1 already present; immutable")
    start=time.monotonic()
    require(batch_size>=1 and batch_size<=64,"invalid GPU microbatch")
    report=json.loads((source_preflight/"summary.json").read_text())
    require(report["status"]=="PASS_INPUT_ONLY_NOT_PRODUCTION_SCORER"
            and report["main_sample_SHA256"]==EXPECTED_A1
            and not report["current_request_author_column_read"]
            and report["n_main_events"]==N
            and report["main_mechanism_nested_user_clock_identity"],
            "A3 source metadata preflight missing")
    selection=a1/"B4A_MAIN_30000_PRIVATE.parquet"
    nested=a1/"B4A_IDENTITY_4096_PRIVATE.parquet"
    frozen_a1=json.loads((a1/"summary.json").read_text())
    require(sha(selection)==frozen_a1["main_private_SHA256"]==EXPECTED_A1
            and sha(nested)==frozen_a1["mechanism_private_SHA256"]==EXPECTED_SUB,
            "A1 target ID SHA mismatch")
    a2meta=json.loads((a2/"summary.json").read_text())
    require(a2meta["status"]=="DEV_ONLY_GATE_MODELS_AND_THRESHOLDS_FROZEN"
            and a2meta["dev_source_SHA256"]==EXPECTED_DEV
            and not a2meta["test_labels_or_ranking_metrics_opened"],
            "A2 gate source not frozen")
    frozen=json.loads(registry.read_text())
    require(frozen["target_test_events"]==47575 and not frozen["test_performance_seen"],
            "original G5 source registry changed")
    old_ids=set(pq.read_table(g1/"test_cohort_sealed.parquet",columns=["source_event_id"]).column("source_event_id").to_numpy().tolist())
    data=pq.read_table(selection,columns=["source_event_id","user_id","observed_at"])
    events=np.asarray(data.column("source_event_id").to_numpy(),dtype=np.int64)
    users=np.asarray(data.column("user_id").to_numpy(),dtype=np.int64)
    clocks=data.column("observed_at").to_pylist()
    require(len(events)==N and len(set(events.tolist()))==N
            and not set(events.tolist()).intersection(old_ids),
            "target IDs invalid/old G5 overlap")
    nauthors=np.load(index/"authors.npy",mmap_mode="r")
    known={int(author):i+1 for i,author in enumerate(nauthors)}
    seq,history_rows=histories(g1/"causal_stream_sealed.parquet",events,known)
    contexts=np.stack([a[0] for a in seq])
    require(contexts.shape==(N,16),"Original G5 history length changed")
    require(torch.cuda.is_available(),"Fixed CUDA inference path unavailable")
    # Frozen two original Base checkpoints; NEVER retrain or reselect.
    models={};reps={}
    for family in FAMILIES:
        doc=json.loads((cache/"klm3_g2_checkpoint_dev_selected_v1.json").read_text())
        ckname=doc["family_results"][family]["selected"]["checkpoint"]
        ck=cache/f"klm3_g2_seed{SEED}_epoch3_v1"/family/ckname
        require(sha(ck)==frozen["checkpoint_sha256"][str(SEED)][family],
                "frozen G5 Base checkpoint SHA differs "+family)
        state=torch.load(ck,map_location="cpu",weights_only=False)
        model=Encoder(len(nauthors),family)
        model.load_state_dict(state["model_state"])
        model.cuda().eval()
        models[family]=model
        del state
        embeds=[]
        with torch.inference_mode():
            for i in range(0,N,256):
                x=torch.as_tensor(contexts[i:i+256],device="cuda",dtype=torch.long)
                em=model(x).detach().cpu().numpy().astype(np.float32)
                require(np.isfinite(em).all(),"Nonfinite Base vector")
                embeds.append(em)
        reps[family]=np.concatenate(embeds)
    counts=np.bincount(np.load(index/"sequence_ids.npy",mmap_mode="r"),minlength=len(nauthors)+1).astype(np.float64)
    logs=np.log1p(counts)
    popularity=np.zeros(len(logs),dtype=np.float64)
    popularity[1:]=(logs[1:]-logs[1:].min())/(logs[1:].max()-logs[1:].min())
    del nauthors
    # Only source G5 family score code, never labels or sampled-S TEST features.
    top=np.empty((N,3,10),dtype=np.int32)
    decisions=np.empty((N,2,2),dtype=np.bool_)
    predicted=np.empty((N,2,2),dtype=np.float64)
    ncand=np.empty(N,dtype=np.int32)
    gates={}
    for f in FAMILIES:
        for arm in ARMS:
            detail=a2meta["models"][f][arm]
            fp=a2/"private_models"/detail["model_name"]
            require(sha(fp)==detail["model_private_SHA256"],"model artifact changed "+f+arm)
            m=joblib.load(fp)
            require(m.n_features_in_==12 and detail["oof_user_disjoint"]
                    and detail["oof_budget"]["dev_oof_call_rate"]<=.3+1e-12,
                    "A2 feature count or frozen OOF threshold failed")
            gates[(f,arm)]=(m,detail["features"],detail["oof_threshold"])
    pending=[]
    processed=0
    def consume(block):
        nonlocal processed
        ranks,base_features=score_block(models,reps,block)
        for j,(i,candidates) in enumerate(block):
            rawseq,prior,recent,maxall,shared=seq[i]
            mscore=corrected_memory_score(candidates,popularity,prior,recent,maxall)
            top[i,2]=stable_top10(candidates,mscore)
            hist_support=sparse_history_support_share(candidates,prior)
            ncand[i]=len(candidates)
            for fi,family in enumerate(FAMILIES):
                top[i,fi]=ranks[(family,j)]
                fields={**shared,**base_features[(family,j)],
                        "x_memory_history_supported_share":hist_support,
                        "x_candidate_log_count":math.log1p(len(candidates))}
                # Same F regime, same 12 features for S-aligned/F-aligned arms.
                features={
                    "x_"+family+"_base_margin":fields["x_base_margin"],
                    "x_"+family+"_base_std":fields["x_base_std"],
                    "x_"+family+"_base_top_z":fields["x_base_top_z"],
                    "x_"+family+"_base_top_score":fields["x_base_top_score"],
                    "x_"+family+"_base_score_mean":fields["x_base_score_mean"]}
                features.update({key:value for key,value in fields.items() if key.startswith("x_") and key not in
                    {"x_base_margin","x_base_std","x_base_top_z","x_base_top_score","x_base_score_mean"}})
                for ai,arm in enumerate(ARMS):
                    reg,cols,threshold=gates[(family,arm)]
                    x=np.asarray([[features[k] for k in cols]],dtype=np.float64)
                    require(x.shape==(1,12) and np.isfinite(x).all(),
                            "nonfinite/misaligned Full-F A3 gate input")
                    val=float(reg.predict(x)[0])
                    require(math.isfinite(val),"A2 gate nonfinite TEST inference")
                    predicted[i,fi,ai]=val
                    decisions[i,fi,ai]=threshold is not None and val>=threshold
        processed+=len(block)
        if processed%2000<len(block):
            print(json.dumps({"phase":"A3_TARGET_BLIND_NO_METRICS",
                              "covered":processed,"elapsed_s":round(time.monotonic()-start,1)}),
                  flush=True)
    for i,c in active_rosters(g1/"available_room_intervals.parquet",clocks,known):
        require(len(c)>=10,"invalid active F roster")
        pending.append((i,c))
        if len(pending)>=batch_size:
            consume(pending);pending=[]
    if pending:consume(pending)
    require(processed==N and np.all(ncand>=10),"incomplete target-blind A3 scoring")
    # Race-safe immutable staging, without public private data artifacts.
    stage=out.with_name(out.name+".incomplete")
    stage.mkdir(parents=True,mode=0o700,exist_ok=False)
    for fname,arr in (("event_ids.npy",events),("user_ids.npy",users),
         ("top10_base_and_memory_author_tokens.npy",top),
         ("gate_calls.npy",decisions),("gate_predicted_utilities.npy",predicted),
         ("candidate_counts.npy",ncand)):
        np.save(stage/fname,arr,allow_pickle=False)
    manifest={"schema":"kbs-b4a-a3-h1-frozen-target-blind-v1",
        "status":"H1_30000_FROZEN_PREDICTIONS_A4_HARD_HOLD",
        "n_events":N,"model_seed":SEED,"base_families":FAMILIES,"gate_arms":ARMS,
        "source_sample_SHA256":EXPECTED_A1,"nested_H2_SHA256":EXPECTED_SUB,
        "frozen_A2_DEV_SHA256":EXPECTED_DEV,
        "original_G5_registry_SHA256":sha(registry),
        "frozen_checkpoint_SHA256":{f:frozen["checkpoint_sha256"][str(SEED)][f] for f in FAMILIES},
        "frozen_gate_model_SHA256":{f:{a:a2meta["models"][f][a]["model_private_SHA256"] for a in ARMS} for f in FAMILIES},
        "n_history_stream_rows":history_rows,
        "mean_active_candidates":float(ncand.mean()),
        "realized_call_fractions_unlabeled":{f:{a:float(decisions[:,fi,ai].mean()) for ai,a in enumerate(ARMS)} for fi,f in enumerate(FAMILIES)},
        "current_target_author_label_loaded_into_snapshot_or_scoring":False,
        "retrospective_target_retained_S_candidate_used":False,
        "test_rank_ndcg_hr_computed":False,"thresholds_recalibrated_on_TEST":False,
        "H2_nulls_scored":False,"A4_unseal_authorized":False,
        "private_files_sha256":{p.name:sha(p) for p in stage.glob("*.npy")},
        "wall_seconds":round(time.monotonic()-start,2)}
    (stage/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    stage.rename(out)
    print(json.dumps({"status":manifest["status"],"n_events":N,
        "A4_authorized":False,"NDCG_computed":False,"elapsed_s":manifest["wall_seconds"]}),
          flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("cache","g1","index","a1","a2","source-preflight","registry","out"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--batch-size",type=int,default=16)
    a=p.parse_args()
    main(a.cache,a.g1,a.index,a.a1,a.a2,a.source_preflight,a.registry,a.out,a.batch_size)
