#!/usr/bin/env python3
"""G2 DEV-only selected checkpoint evaluation, with exact paired author candidates.

Ranks 4096 preregistered DEV events under an identical fixed 575-active-author
candidate panel for each checkpoint of SASRec and GRU4Rec. No TEST reads.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np
import torch

from g2_train_base import Encoder


def sha(file):
    h=hashlib.sha256()
    with open(file,"rb") as f:
        for block in iter(lambda:f.read(8*1024*1024),b""):
            h.update(block)
    return h.hexdigest()


@torch.inference_mode()
def evaluate(model,context,candidates,cdf,batch=128,device="cuda"):
    model.eval()
    num=len(context)
    if len(candidates)!=num or candidates.shape[1]!=575:
        raise ValueError("DEV panel/candidate shape mismatch")
    ndcg=np.zeros(num,dtype=np.float64)
    ranks=np.zeros(num,dtype=np.int32)
    probs=np.diff(np.concatenate(([0.0],cdf)))
    cold_count=0
    for i in range(0,num,batch):
        j=min(i+batch,num)
        hist=context[i:j]
        options=candidates[i:j]
        nonempty=np.any(hist!=0,axis=1)
        if nonempty.any():
            h=torch.as_tensor(hist[nonempty],device=device,dtype=torch.long)
            ids=torch.as_tensor(options[nonempty],device=device,dtype=torch.long)
            scores=model.score(h,ids)
            if not torch.isfinite(scores).all():
                raise FloatingPointError("Non-finite DEV checkpoint scores")
            positive_score=scores[:,0:1]
            outranks=(scores>positive_score)|((scores==positive_score)&
                     (ids<ids[:,0:1]))
            predicted=(1+outranks.sum(axis=1)).to("cpu").numpy()
            ranks[i:j][nonempty]=predicted
        if (~nonempty).any():
            cold_count+=int((~nonempty).sum())
            negs=options[~nonempty]
            s=probs[negs-1]
            a=s[:,0:1]
            predicted=1+((s>a)|((s==a)&(negs<negs[:,0:1]))).sum(axis=1)
            ranks[i:j][~nonempty]=predicted
    valid=(ranks>=1)&(ranks<=10)
    ndcg[valid]=1/np.log2(ranks[valid]+1)
    return {"ndcg10":float(np.mean(ndcg)),
            "hr10":float(np.mean(ranks<=10)),
            "n_eval":num,"zero_known_history_fallback_events":cold_count}


def select_checkpoint(train_root,dev_root,source_index,output):
    begin=time.monotonic()
    dev_manifest=json.loads((dev_root/"manifest.json").read_text())
    idx_manifest=json.loads((source_index/"index_manifest.json").read_text())
    if dev_manifest["schema"]!="kbs-plan-c-g2-dev-screen-v1":
        raise ValueError("Wrong DEV-only snapshot protocol")
    if dev_manifest["g1_protocol_sha256"]!=idx_manifest["g1_protocol_sha256"]:
        raise ValueError("Mismatched G1/DEV identity")
    for name,expected in dev_manifest["files_sha256"].items():
        if sha(dev_root/name)!=expected:
            raise ValueError("DEV candidate features SHA changed: "+name)
    indices=np.load(dev_root/"checkpoint_dev_indices.npy",allow_pickle=False)
    contexts=np.load(dev_root/"dev_contexts.npy",allow_pickle=False)[indices].astype(np.int64)
    candidates=np.load(dev_root/"checkpoint_candidate_tokens.npy",allow_pickle=False).astype(np.int64)
    positives=np.load(dev_root/"dev_positive_author_tokens.npy",allow_pickle=False)[indices]
    if not np.array_equal(candidates[:,0],positives):
        raise ValueError("Positive/candidate membership mismatch")
    cdf=np.load(source_index/"popularity_cdf.npy",allow_pickle=False)
    if not torch.cuda.is_available():
        raise RuntimeError("DEV comparison requires the designated 3090 CUDA host")
    results={}
    for family in ("sasrec","gru4rec"):
        root=train_root/family
        report=json.loads((root/(family+"_train_report.json")).read_text())
        if (report["status"]!="TRAIN_CHECKPOINTS_NOT_DEV_SELECTED" or
                len(report["train_records"])!=3 or
                report["index_manifest"]!=idx_manifest or
                report["test_outcomes_read"] is not False):
            raise ValueError("Training provenance or TEST isolation mismatch")
        performances=[]
        for record in report["train_records"]:
            cp=root/record["checkpoint"]
            if sha(cp)!=record["checkpoint_sha256"]:
                raise ValueError("checkpoint SHA mismatch")
            saved=torch.load(cp,map_location="cpu",weights_only=False)
            if saved.get("model_family")!=family or saved.get("test_used") is not False:
                raise ValueError("unexpected model family or TEST access")
            model=Encoder(idx_manifest["unique_train_authors"],family)
            model.load_state_dict(saved["model_state"])
            del saved
            model.to("cuda")
            torch.cuda.reset_peak_memory_stats()
            perf=evaluate(model,contexts,candidates,cdf,device="cuda")
            perf.update({"epoch":record["epoch"],"checkpoint":record["checkpoint"],
                         "checkpoint_sha256":record["checkpoint_sha256"],
                         "peak_cuda_gib":round(torch.cuda.max_memory_allocated()/1024**3,3)})
            performances.append(perf)
            print(json.dumps({"family":family,**perf}),flush=True)
            del model
            torch.cuda.empty_cache()
        # Deterministic DEV rule: earliest epoch wins exact metric ties.
        chosen=max(performances,key=lambda x:(x["ndcg10"],-x["epoch"]))
        results[family]={"epochs":performances,"selected":chosen}
    output.parent.mkdir(parents=True,exist_ok=True)
    result={"schema":"kbs-plan-c-g2-checkpoint-selection-dev-only-v1",
            "source_train_index_sha256":sha(source_index/"index_manifest.json"),
            "dev_snapshot_sha256":sha(dev_root/"manifest.json"),
            "selection_rule":"highest 4096-event DEV sampled-active NDCG@10; earliest-epoch tie",
            "family_results":results,
            "elapsed_seconds":round(time.monotonic()-begin,2),
            "test_data_opened":False,"test_rankings_calculated":False,
            "checkpoints_selected_by_train_loss":False}
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"G2_DEV_CHECKPOINT_SELECTED":{k:v["selected"] for k,v in results.items()},
                      "test_rankings_calculated":False}),flush=True)
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--train-root",type=Path,required=True)
    p.add_argument("--dev",type=Path,required=True)
    p.add_argument("--train-index",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    select_checkpoint(a.train_root,a.dev,a.train_index,a.out)
