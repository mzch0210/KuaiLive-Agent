#!/usr/bin/env python3
"""G3/E2: train all five DEV-only comparator gates from paired full-active scores.

The same locked per-event Base and Memory scores/candidates support every gate.
All user-level rows and fitted models stay on User-host; only aggregates export.
No TEST input, outcome, model tuning or file path is accepted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from train_gate_oof import fit_oof
from frozen_gate import freeze_dev, METHODS


FAMILY_BASE_FEATURES=("base_margin","base_std","base_top_z",
                       "base_top_score","base_score_mean")
SHARED_FEATURES=("hist_event_count","hist_warm_count","hist_distinct",
                 "hist_repeat_max","hist_short_unique",
                 "memory_history_supported_share","candidate_log_count")


def hash_path(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def prepare_family_data(src, family):
    if family not in ("sasrec","gru4rec"):
        raise ValueError("Only pretrained dual Base families allowed")
    cols=["event_id","user_id","split","memory_ndcg10",family+"_ndcg10"]
    cols += ["x_"+c for c in SHARED_FEATURES]
    cols += ["x_"+family+"_"+c for c in FAMILY_BASE_FEATURES]
    missing=set(cols)-set(src.columns)
    if missing:
        raise ValueError("Missing exactly-paired event features: "+repr(sorted(missing)))
    d=src[cols].copy()
    d=d.rename(columns={family+"_ndcg10":"base_ndcg10"})
    for name in FAMILY_BASE_FEATURES:
        d=d.rename(columns={"x_"+family+"_"+name:"x_"+name})
    if len(d)!=50049 or not d.split.eq("DEV").all():
        raise ValueError("Input must contain every one of 50,049 frozen DEV events")
    if d.event_id.duplicated().any() or d.user_id.isna().any():
        raise ValueError("DEV event identity invalid")
    if d.isna().any().any():
        raise ValueError("Missing feature/utility values")
    if len([c for c in d if c.startswith("x_")]) != len(FAMILY_BASE_FEATURES)+len(SHARED_FEATURES):
        raise ValueError("Unexpected Base/leaked cross-model feature")
    return d


def evaluate_oof(oof, frozen, base):
    b=oof.base_ndcg10.to_numpy(dtype=np.float64)
    m=oof.memory_ndcg10.to_numpy(dtype=np.float64)
    d=m-b
    metrics={
        "always_base_ndcg10":float(b.mean()),
        "always_memory_ndcg10":float(m.mean()),
        "always_memory_minus_base":float(d.mean()),
        "hindsight_oracle_ndcg10":float(np.maximum(b,m).mean()),
        "hindsight_oracle_gain":float(np.maximum(d,0).mean()),
        "methods":{}
    }
    for method in METHODS:
        t=frozen["methods"][method]["threshold"]
        scores=oof["score_"+method].to_numpy(dtype=np.float64)
        mask=scores>=t if t is not None else np.zeros(len(scores),dtype=bool)
        gain=float(d[mask].sum()/len(d))
        meth={
            "dev_frozen_threshold":None if t is None else float(t),
            "dev_oof_selected_events":int(mask.sum()),
            "dev_oof_call_rate":float(mask.mean()),
            "dev_oof_mean_ndcg10":float(b.mean()+gain),
            "dev_oof_gain_over_base":gain
        }
        if abs(gain-frozen["methods"][method]["dev_oof_gain"])>2e-8:
            raise ValueError("Threshold/utility mismatch for "+method)
        metrics["methods"][method]=meth
    metrics["utility_minus_difficulty_oof_gain"]=(
        metrics["methods"]["utility"]["dev_oof_gain_over_base"]-
        metrics["methods"]["difficulty"]["dev_oof_gain_over_base"])
    return metrics


def execute(pairs_dir:Path,out_dir:Path):
    manifest=json.loads((pairs_dir/"summary.json").read_text())
    src_file=pairs_dir/"dev_full_active_pairs.csv"
    if (manifest.get("schema")!="kbs-plan-c-full-active-dev-paired-v2"
        or manifest.get("scope")!="DEV_ONLY"
        or not manifest.get("all_dev_scored")
        or manifest.get("n_scored")!=50049
        or manifest.get("memory_corrected_from_all_history") is not True
        or manifest.get("test_file_accessed") is not False
        or hash_path(src_file)!=manifest["event_csv_sha256"]):
        raise ValueError("Requires fully paired DEV-only original source, byte verified")
    if out_dir.exists():
        raise FileExistsError("Existing DEV gate cache must not be overwritten")
    work=out_dir.with_name(out_dir.name+".incomplete")
    if work.exists():
        raise FileExistsError("Incomplete pre-existing gate run: inspect before retry")
    work.mkdir(parents=True,mode=0o700)
    src=pd.read_csv(src_file)
    if len(src)!=50049 or not src["split"].eq("DEV").all():
        raise ValueError("Full frozen DEV coverage required")
    root={"schema":"kbs-plan-c-g3-five-gates-dev-only-v1",
          "source_dev_pair_sha256":hash_path(src_file),
          "base_checkpoint_sha":manifest["base_checkpoint_sha"],
          "source_g1_protocol_sha256":manifest["g1_protocol_sha256"],
          "evaluation_scope":"DEV_OOF_POLICY_OPTIMIZATION",
          "selection":"five pointwise policies, each OOF budget<=0.30",
          "user_group_disjoint_fivefold":True,
          "target_quality_used_in_gate_features":False,
          "test_labels_inspected":False,
          "test_file_opened":False,
          "warning":"Optimized-on-DEV gate gains are discovery results; independent TEST confirmation remains locked.",
          "family":{}}
    for family in ("sasrec","gru4rec"):
        inp=prepare_family_data(src,family)
        directory=work/family
        directory.mkdir()
        inputfile=directory/"dev_features_with_dev_labels.csv"
        inp.to_csv(inputfile,index=False,float_format="%.12g")
        manifest_oof=fit_oof(inputfile,directory/"models",seed=20261012)
        path_oof=directory/"models"/"dev_oof.csv"
        oof_proof=directory/"models"/"oof_manifest.json"
        policy_path=directory/"frozen_thresholds.json"
        policy=freeze_dev(path_oof,oof_proof,policy_path,max_rate=.30)
        oof=pd.read_csv(path_oof)
        if not np.array_equal(oof.event_id.to_numpy(),inp.event_id.to_numpy()):
            raise ValueError("DEV OOF mismatched event order")
        eval_report=evaluate_oof(oof,policy,family)
        root["family"][family]={
            "n_events":len(oof),
            "n_users":int(inp.user_id.nunique()),
            "model_feature_columns":manifest_oof["feature_columns"],
            "OOF_model_sha256":manifest_oof["final_model_sha256"],
            "frozen_thresholds_sha256":hash_path(policy_path),
            "DEV_oof_sha256":hash_path(path_oof),
            "metrics":eval_report,
        }
        print(json.dumps({"family":family,"evaluation":"DEV OOF only",
                          "utility_gain":eval_report["methods"]["utility"]["dev_oof_gain_over_base"],
                          "difficulty_gain":eval_report["methods"]["difficulty"]["dev_oof_gain_over_base"],
                          "selected_pct":eval_report["methods"]["utility"]["dev_oof_call_rate"]}),flush=True)
    (work/"aggregate.json").write_text(json.dumps(root,indent=2)+"\n")
    work.rename(out_dir)
    print(json.dumps({"state":"DEV_OOF_FIVE_GATES_FROZEN",
                      "aggregate":{f:d["metrics"] for f,d in root["family"].items()},
                      "test_unseen":True}),flush=True)
    return root


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--paired",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    execute(args.paired,args.out)
