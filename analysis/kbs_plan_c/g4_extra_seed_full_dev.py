#!/usr/bin/env python3
"""Plan C G4: reuse corrected DEV Memory and one live-author sweep for 4 new Bases.

Scientific lock: exactly the same 50,049 DEV events, candidate sets and
pretarget Memory, with independently trained 20261013/14 Base checkpoints.
No TEST files, model fitting, label-guided tuning or resampling occurs.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,time
from pathlib import Path
import numpy as np
import torch
import pyarrow.parquet as pq
from g2_train_base import Encoder
from g3_dev_full_active import author_availability,ndcg

SEEDS=(20261013,20261014)
FAMILIES=("sasrec","gru4rec")
N_EXPECTED=50049

def hash_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def checked_json(path):
    return json.loads(Path(path).read_text())

def prepare(g1,index,dev_cache,corrected,seed_root):
    g1m=checked_json(g1/"manifest.json")
    idxm=checked_json(index/"index_manifest.json")
    dm=checked_json(dev_cache/"manifest.json")
    mm=checked_json(corrected/"summary.json")
    if not (g1m["schema"]=="kbs-plan-c-g1-derived-v1"
       and dm["schema"]=="kbs-plan-c-g2-dev-screen-v1"
       and mm["schema"]=="kbs-plan-c-full-active-dev-paired-v2"
       and mm["memory_corrected_from_all_history"] is True
       and mm["scope"]=="DEV_ONLY" and mm["all_dev_scored"] is True
       and mm["n_scored"]==N_EXPECTED and mm["test_file_accessed"] is False
       and dm["g1_protocol_sha256"]==g1m["protocol_sha256"]
       and idxm["g1_protocol_sha256"]==g1m["protocol_sha256"]
       and mm["g1_protocol_sha256"]==g1m["protocol_sha256"]):
        raise ValueError("DEV-only G1/G2/G3 provenance mismatch")
    for name in ("dev_contexts.npy","dev_positive_author_tokens.npy","dev_source_event_ids.npy"):
        if hash_file(dev_cache/name)!=dm["files_sha256"][name]:
            raise ValueError("Modified frozen DEV feature: "+name)
    filename=corrected/"dev_full_active_pairs.csv"
    if hash_file(filename)!=mm["event_csv_sha256"]:
        raise ValueError("Modified corrected Memory paired file")
    with filename.open(newline="") as f:
        reader=csv.DictReader(f)
        original_columns=list(reader.fieldnames or [])
        old_rows=list(reader)
    by_event={int(r["event_id"]):r for r in old_rows}
    if len(old_rows)!=N_EXPECTED or len(by_event)!=N_EXPECTED:
        raise ValueError("Invalid corrected DEV pairs")
    ids=np.load(dev_cache/"dev_source_event_ids.npy",allow_pickle=False)
    pos=np.load(dev_cache/"dev_positive_author_tokens.npy",allow_pickle=False)
    ctx=np.load(dev_cache/"dev_contexts.npy",mmap_mode="r")
    if len(ids)!=N_EXPECTED or set(int(x) for x in ids)!=set(by_event):
        raise ValueError("DEV identity mismatch")
    tab=pq.read_table(g1/"dev_cohort.parquet",
                       columns=["source_event_id","observed_at","user_id"])
    if not np.array_equal(tab.column("source_event_id").to_numpy(),ids):
        raise ValueError("G1 DEV original cohort order changed")
    times=tab.column("observed_at").to_pylist()
    users=tab.column("user_id").to_numpy()
    authors=np.load(index/"authors.npy",mmap_mode="r")
    known={int(a):i+1 for i,a in enumerate(authors)}
    if len(known)!=idxm["unique_train_authors"]:
        raise ValueError("Author index not aligned")
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Expected dedicated user-host RTX 3090")
    models={}
    reps={}
    chosen={}
    for seed in SEEDS:
        doc=checked_json(seed_root/f"klm3_g2_seed{seed}_dev_selected_v1.json")
        if (doc["schema"]!="kbs-plan-c-g2-checkpoint-selection-dev-only-v1"
           or doc["test_data_opened"] is not False
           or doc["test_rankings_calculated"] is not False
           or doc["source_train_index_sha256"]!=hash_file(index/"index_manifest.json")
           or doc["dev_snapshot_sha256"]!=hash_file(dev_cache/"manifest.json")):
            raise ValueError("Wrong seed-specific DEV checkpoint provenance")
        for family in FAMILIES:
            meta=doc["family_results"][family]["selected"]
            ck=(seed_root/f"klm3_g2_seed{seed}_epoch3_v1"/family/meta["checkpoint"])
            if hash_file(ck)!=meta["checkpoint_sha256"]:
                raise ValueError(f"Selected checkpoint SHA changed: {seed}/{family}")
            data=torch.load(ck,map_location="cpu",weights_only=False)
            if (data.get("model_family")!=family or data.get("seed")!=seed
                or data.get("test_used") is not False
                or data.get("dev_selected") is not False):
                raise ValueError("Checkpoint family/seed/TEST misuse")
            model=Encoder(len(authors),family)
            model.load_state_dict(data["model_state"])
            model.to("cuda").eval()
            del data
            key=(seed,family)
            models[key]=model
            chosen[f"{seed}_{family}"]={"selected_epoch":meta["epoch"],
                  "checkpoint_sha256":meta["checkpoint_sha256"]}
            outputs=[]
            with torch.inference_mode():
                for offset in range(0,N_EXPECTED,256):
                    x=torch.as_tensor(np.asarray(ctx[offset:offset+256]),
                                      device="cuda",dtype=torch.long)
                    z=model(x).cpu().numpy()
                    if not np.isfinite(z).all():
                        raise FloatingPointError("Non-finite DEV representation")
                    outputs.append(z.astype(np.float32))
            reps[key]=np.concatenate(outputs)
    return {"g1m":g1m,"idxm":idxm,"mm":mm,"old_rows":by_event,
            "old_columns":original_columns,"id":ids,"pos":pos,
            "times":times,"users":users,"known":known,"models":models,
            "reps":reps,"chosen":chosen}

@torch.inference_mode()
def score_block(block,state):
    n=len(block)
    maxsize=max(len(c) for _,c in block)
    candidate=np.zeros((n,maxsize),dtype=np.int32)
    for k,(_,c) in enumerate(block):
        candidate[k,:len(c)]=c
    ids=torch.as_tensor(candidate,dtype=torch.long,device="cuda")
    out={seed:[None]*n for seed in SEEDS}
    for (seed,family),model in state["models"].items():
        reps=torch.as_tensor(state["reps"][(seed,family)][[i for i,_ in block]],
                             dtype=torch.float32,device="cuda")
        # No candidate × embedding dimensions saved to disk.
        scores=(model.item(ids)*reps[:,None,:]).sum(-1).cpu().numpy()
        if not np.isfinite(scores).all():
            raise FloatingPointError("Nonfinite full-active DEV Base score")
        for k,(i,options) in enumerate(block):
            score=scores[k,:len(options)]
            pos=int(state["pos"][i])
            target_idx=np.searchsorted(options,pos)
            if target_idx>=len(options) or options[target_idx]!=pos:
                raise ValueError("Target missing from candidate universe")
            val=score[target_idx]
            rank=1+int(np.count_nonzero((score>val) |
                    ((score==val)&(options<pos))))
            top=np.partition(score,-2)[-2:]
            top.sort()
            mean=float(score.mean())
            std=float(score.std())
            result={"rank":rank,"ndcg10":ndcg(rank),
                    "base_margin":float(top[-1]-top[-2]),
                    "base_std":std,
                    "base_top_z":float((top[-1]-mean)/max(std,1e-8)),
                    "base_top_score":float(top[-1]),
                    "base_score_mean":mean}
            old=state["old_rows"][int(state["id"][i])]
            if int(old["user_id"])!=int(state["users"][i]) or int(old["candidate_count"])!=len(options):
                raise ValueError("Base candidate panel deviates from corrected Memory")
            out[seed][k]=(out[seed][k] or {}) | {family:result}
    for seed in SEEDS:
        for k,(i,_) in enumerate(block):
            if set(out[seed][k])!=set(FAMILIES):
                raise ValueError("Missing one Base family")
    return out

def run(g1,index,dev,corrected,root,out_root,block_size=16):
    started=time.monotonic()
    for seed in SEEDS:
        if (out_root/f"seed{seed}").exists() or (out_root/f"seed{seed}.incomplete").exists():
            raise FileExistsError(f"Existing G4 seed{seed}; inspect before any retry")
    state=prepare(g1,index,dev,corrected,root)
    for seed in SEEDS:
        p=out_root/f"seed{seed}.incomplete"
        p.mkdir(parents=True,mode=0o700)
    retained={seed:[] for seed in SEEDS}
    pending=[]
    done=0
    def consume(block):
        nonlocal done
        scored=score_block(block,state)
        for seed in SEEDS:
            for k,(i,_) in enumerate(block):
                event_id=int(state["id"][i])
                row=state["old_rows"][event_id].copy()
                for family in FAMILIES:
                    for field,val in scored[seed][k][family].items():
                        if field in ("rank","ndcg10"):
                            col=f"{family}_{field}"
                        else:
                            col=f"x_{family}_{field}"
                        row[col]=val
                retained[seed].append(row)
        done+=len(block)
        if done%1000<block_size:
            print(json.dumps({"stage":"G4_four_models_one_roster",
                              "rows":done,"elapsed_seconds":round(time.monotonic()-started,1)}),flush=True)
    for i,c,room_count in author_availability(g1/"available_room_intervals.parquet",
                                              state["times"],state["pos"],state["known"]):
        pending.append((i,c))
        if len(pending)>=block_size:
            consume(pending)
            pending=[]
    if pending:
        consume(pending)
    if done!=N_EXPECTED:
        raise ValueError("Incomplete full DEV candidate sweep")
    reports={}
    for seed in SEEDS:
        rows=retained[seed]
        rows.sort(key=lambda r:int(r["event_id"]))
        path=out_root/f"seed{seed}.incomplete"
        filename=path/"dev_full_active_pairs.csv"
        with filename.open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=state["old_columns"])
            writer.writeheader()
            writer.writerows(rows)
        metrics={}
        for family in (*FAMILIES,"memory"):
            val=np.array([float(r[family+"_ndcg10"]) for r in rows])
            rank=np.array([int(r[family+"_rank"]) for r in rows])
            metrics[family]={"ndcg10":float(val.mean()),
                             "hr10":float(np.mean(rank<=10))}
            if family in FAMILIES:
                metrics[family]["memory_minus_base_ndcg10"]=float(
                   np.mean(np.array([float(r["memory_ndcg10"]) for r in rows])-val))
        if not math.isclose(metrics["memory"]["ndcg10"],
                             state["mm"]["aggregate"]["memory"]["ndcg10"],abs_tol=1e-12):
            raise ValueError("Memory changed in Base-only G4 evaluation")
        summary={"schema":"kbs-plan-c-full-active-dev-paired-v2",
                 "scope":"DEV_ONLY","n_scored":done,"all_dev_scored":True,
                 "seed":seed,
                 "base_checkpoint_sha":{family:state["chosen"][f"{seed}_{family}"]["checkpoint_sha256"]
                                        for family in FAMILIES},
                 "base_selected_epochs":{family:state["chosen"][f"{seed}_{family}"]["selected_epoch"]
                                         for family in FAMILIES},
                 "g1_protocol_sha256":state["g1m"]["protocol_sha256"],
                 "event_csv_sha256":hash_file(filename),
                 "original_corrected_memory_event_csv_sha256":state["mm"]["event_csv_sha256"],
                 "memory_corrected_from_all_history":True,
                 "memory_reused_not_retrained_or_recomputed":True,
                 "source_test_outcomes_inspected":False,"test_file_accessed":False,
                 "gates_fit":False,
                 "median_active_candidates":float(np.median([int(r["candidate_count"]) for r in rows])),
                 "elapsed_seconds":round(time.monotonic()-started,1),
                 "aggregate":metrics}
        (path/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
        reports[str(seed)]=summary
    for seed in SEEDS:
        (out_root/f"seed{seed}.incomplete").rename(out_root/f"seed{seed}")
    print(json.dumps({"status":"G4_EXTRA_SEED_FULL_ACTIVE_DEV_COMPLETE",
                      "aggregate":{s:v["aggregate"] for s,v in reports.items()},
                      "TEST_unseen":True}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--g1",type=Path,required=True)
    p.add_argument("--index",type=Path,required=True)
    p.add_argument("--dev",type=Path,required=True)
    p.add_argument("--corrected",type=Path,required=True)
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--out-root",type=Path,required=True)
    p.add_argument("--block-size",type=int,default=16)
    a=p.parse_args()
    run(a.g1,a.index,a.dev,a.corrected,a.root,a.out_root,a.block_size)
