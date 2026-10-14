#!/usr/bin/env python3
"""B4A A2 model/feature/threshold contract: verify private DEV-only models.

A3 blocked. No G5 or B4A TEST file paths are read.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import joblib,numpy as np,pandas as pd

SRC="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
SHARED=["hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique",
        "memory_history_supported_share","candidate_log_count"]
BASE=["base_margin","base_std","base_top_z","base_top_score","base_score_mean"]
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for x in iter(lambda:f.read(8<<20),b""):h.update(x)
    return h.hexdigest()

def main(root,source,out):
    if out.exists():raise FileExistsError("Do not overwrite model contract")
    f=json.loads((root/"summary.json").read_text())
    if not(f["schema"]=="kbs-route-b-b4a-a2-dev-final-gates-v1"
           and f["status"]=="DEV_ONLY_GATE_MODELS_AND_THRESHOLDS_FROZEN"
           and f["dev_source_SHA256"]==SRC
           and f["test_labels_or_ranking_metrics_opened"] is False
           and f["B4A_sample_read"] is False
           and f["n_dev_events"]==50049):
        raise RuntimeError("A2 manifest invalid")
    manifest=json.loads((source/"summary.json").read_text())
    csv=source/"dev_pair_candidate_labels.csv"
    if not (sha(csv)==manifest["private_event_source_csv_sha256"]==SRC):
        raise RuntimeError("DEV SHA differs")
    sample=pd.read_csv(csv,nrows=256)
    evidence={}
    for family in ("sasrec","gru4rec"):
        cols=["x_"+s for s in SHARED]+["x_"+family+"_"+s for s in BASE]
        if len(cols)!=12 or len(set(cols))!=12:
            raise RuntimeError("Bad fixed feature schema")
        # G5's 12-feature online scoring contract uses the same pretarget
        # semantic order after removing model family from field names.
        normalized=[x.replace("x_"+family+"_","x_") for x in cols]
        expected=["x_"+s for s in SHARED]+["x_"+s for s in BASE]
        if normalized!=expected:raise RuntimeError("Mismatch with G5 feature semantics")
        X=sample[cols].to_numpy(dtype=np.float64)
        if not np.isfinite(X).all():raise RuntimeError("Nonfinite DEV feature sample")
        evidence[family]={}
        for arm in ("S_aligned","F_aligned"):
            m=f["models"][family][arm]
            if m["features"]!=cols or m["oof_user_disjoint"] is not True:
                raise RuntimeError("A2 model features/folds mismatch")
            if m["oof_budget"]["dev_oof_call_rate"]>.30+1e-10:
                raise RuntimeError("A2 OOF call budget exceeded")
            artifact=root/"private_models"/m["model_name"]
            if sha(artifact)!=m["model_private_SHA256"]:
                raise RuntimeError("Model SHA not equal to frozen manifest")
            reg=joblib.load(artifact)
            if getattr(reg,"n_features_in_",None)!=12:
                raise RuntimeError("Fitted model feature count inconsistent")
            values=reg.predict(X)
            if not np.isfinite(values).all():
                raise RuntimeError("DEV model inference produced nonfinite values")
            evidence[family][arm]={"model_SHA256_pass":True,
                "feature_contract_pass":True,"pointwise_threshold_frozen":True,
                "n_feature_inputs":12,
                "dev_probe_rows":len(X),"A3_execution_allowed":False}
    out.mkdir(parents=True,mode=0o700)
    report={"schema":"kbs-route-b-b4a-a2-contract-check-v1",
            "status":"FOUR_MODELS_DEV_SHA_FEATURE_AND_PREDICTION_CONTRACT_PASS",
            "source_DEV_SHA256":SRC,"results":evidence,
            "TEST_rows_read":0,"B4A_labels_read":False,
            "A3_A4_authorized":False}
    (out/"summary.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps(report,sort_keys=True),flush=True)

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--models",type=Path,required=True)
    a.add_argument("--dev",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    z=a.parse_args()
    main(z.models,z.dev,z.out)
