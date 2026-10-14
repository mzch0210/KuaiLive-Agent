#!/usr/bin/env python3
"""B4-A A2: four DEV-only final F/S gate models; OOF thresholds.

No G5/B4A TEST files are opened and no target-blind TEST predictions computed.
"""
from __future__ import annotations
import argparse, hashlib, json, math, time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold
from frozen_gate import select_threshold

N,USERS,SEED,FOLDS=50049,12628,20261012,4
EXPECTED="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
SHARED=("hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique",
        "memory_history_supported_share","candidate_log_count")
BASE=("base_margin","base_std","base_top_z","base_top_score","base_score_mean")
FAMILIES=("sasrec","gru4rec")
ARMS=("S_aligned","F_aligned")

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def reg(seed):
    return HistGradientBoostingRegressor(
        loss="squared_error",max_iter=120,learning_rate=.05,max_depth=3,
        min_samples_leaf=50,l2_regularization=1.0,
        early_stopping=False,random_state=int(seed))

def main(source,out):
    if out.exists():raise FileExistsError("A2 final model freeze is immutable")
    started=time.monotonic()
    meta=json.loads((source/"summary.json").read_text())
    csv=source/"dev_pair_candidate_labels.csv"
    if not(meta.get("schema")=="kbs-b1-full-dev-paired-candidate-labels-v1"
           and meta.get("status")=="PASS"
           and meta.get("n_dev_events")==N
           and meta.get("test_accessed") is False
           and meta.get("model_training") is False
           and sha(csv)==meta.get("private_event_source_csv_sha256")==EXPECTED):
        raise RuntimeError("DEV source B1 integrity failed")
    cols=["event_id","user_id","split","memory_ndcg10","sampled_memory_ndcg10"]
    for family in FAMILIES:
        cols.extend((family+"_ndcg10","sampled_"+family+"_ndcg10"))
    for name in SHARED:cols.append("x_"+name)
    for family in FAMILIES:
        for name in BASE:cols.append("x_"+family+"_"+name)
    data=pd.read_csv(csv,usecols=cols)
    if not(len(data)==N and data.event_id.is_unique
           and data.user_id.nunique()==USERS
           and data.split.eq("DEV").all()):
        raise RuntimeError("DEV rows invalid")
    users=data.user_id.astype(str).to_numpy()
    folds=list(GroupKFold(n_splits=FOLDS).split(
        np.zeros(N,dtype=np.int8),groups=users))
    for tr,va in folds:
        if np.intersect1d(users[tr],users[va]).size:
            raise RuntimeError("User overlap in OOF")
    result={"schema":"kbs-route-b-b4a-a2-dev-final-gates-v1",
        "status":"DEV_ONLY_GATE_MODELS_AND_THRESHOLDS_FROZEN",
        "n_dev_events":N,"n_dev_users":USERS,
        "dev_source_SHA256":EXPECTED,"training_seed":SEED,
        "group_oof_folds":FOLDS,"max_OOF_call_fraction":.30,
        "threshold_rule":"frozen_gate.select_threshold, OOF signed gain, tied scores indivisible",
        "model_family":"HistGradientBoostingRegressor",
        "test_labels_or_ranking_metrics_opened":False,
        "B4A_sample_read":False,"base_or_memory_retrained":False,
        "models":{}}
    out.mkdir(parents=True,mode=0o700)
    modeldir=out/"private_models"
    modeldir.mkdir(mode=0o700)
    for family in FAMILIES:
        features=["x_"+name for name in SHARED]+[
            "x_"+family+"_"+name for name in BASE]
        X=data[features].to_numpy(dtype=np.float64)
        m=data.memory_ndcg10.to_numpy(dtype=np.float64)
        sm=data.sampled_memory_ndcg10.to_numpy(dtype=np.float64)
        true_F=data[family+"_ndcg10"].to_numpy(dtype=np.float64)
        true_S=data["sampled_"+family+"_ndcg10"].to_numpy(dtype=np.float64)
        targets={"S_aligned":sm-true_S,"F_aligned":m-true_F}
        if not np.isfinite(X).all() or not all(
                np.isfinite(yy).all() for yy in targets.values()):
            raise RuntimeError("Nonfinite pretarget features/DEV utility")
        result["models"][family]={}
        oofs={}
        for arm,y in targets.items():
            score=np.full(N,np.nan,dtype=np.float64)
            for k,(tr,va) in enumerate(folds):
                model=reg(SEED+k)
                model.fit(X[tr],y[tr])
                score[va]=model.predict(X[va])
            if not np.isfinite(score).all():
                raise RuntimeError("Incomplete OOF score")
            frozen=select_threshold(score.tolist(),y.tolist(),.30)
            if frozen["dev_oof_call_rate"]>.3+1e-12:
                raise RuntimeError("OOF budget violated")
            final=reg(SEED)
            final.fit(X,y)
            saved=modeldir/(family+"_"+arm+"_HGB.joblib")
            joblib.dump(final,saved,compress=3)
            model_hash=sha(saved)
            fitted=final.predict(X)
            th=frozen["threshold"]
            fitted_calls=np.zeros(N,dtype=bool) if th is None else (fitted>=th)
            oof_calls=np.zeros(N,dtype=bool) if th is None else (score>=th)
            if oof_calls.sum()!=frozen["calls"]:
                raise RuntimeError("Frozen OOF threshold call mismatch")
            diag={"label_regime":"retrospective_sampled_target_retained_DEV"
                    if arm=="S_aligned" else "full_active_DEV",
                  "label_count":N,
                  "features":features,
                  "feature_count":len(features),
                  "model_name":saved.name,
                  "model_private_SHA256":model_hash,
                  "oof_threshold":th,
                  "oof_budget":frozen,
                  "final_model_fitted_DEV_call_rate_diagnostic":float(fitted_calls.mean()),
                  "oof_DEV_full_F_NDCG_diagnostic":float(
                      np.mean(true_F+oof_calls*(m-true_F))),
                  "oof_DEV_signed_label_gain_diagnostic":float(np.mean(oof_calls*y)),
                  "regressor_training_seed":SEED,
                  "oof_user_disjoint":True,
                  "training_sample_count":N,
                  "model_hyperparameters":{"max_iter":120,"learning_rate":.05,
                      "max_depth":3,"min_samples_leaf":50,"l2_regularization":1.,
                      "early_stopping":False}}
            result["models"][family][arm]=diag
            oofs[arm]=oof_calls
            print(json.dumps({"A2_DEV_MODEL":"FROZEN","family":family,"arm":arm,
                "OOF_call_rate":diag["oof_budget"]["dev_oof_call_rate"],
                "OOF_F_quality_diagnostic":diag["oof_DEV_full_F_NDCG_diagnostic"],
                "frozen_model_SHA256":model_hash},sort_keys=True),flush=True)
        result["models"][family]["OOF_decision_disagreement_fraction"]=float(
            np.mean(oofs["S_aligned"]!=oofs["F_aligned"]))
    result["elapsed_seconds"]=round(time.monotonic()-started,2)
    (out/"summary.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"A2_DEV":"FOUR_GATES_FROZEN","safe_summary":result},
                     sort_keys=True),flush=True)

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--source",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    args=a.parse_args()
    main(args.source,args.out)
