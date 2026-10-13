#!/usr/bin/env python3
"""B1-3 candidate-supervision transfer: strictly nested user-disjoint DEV only.

S->F: S utility labels train and calibrate; F utility labels never used by this
arm until outer final evaluation. F->F and mixed/adapted F are separate arms.
All event-level predictions, user IDs and models stay on the private host.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

from frozen_gate import select_threshold

N=50049
SEED=20261012
OUTER=5
INNER=4
MAX_CALL=.30
ARMS=("sampled_to_full","full_to_full","regime_adapted_to_full")
SHARED=("hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique",
        "memory_history_supported_share","candidate_log_count")
BASE=("base_margin","base_std","base_top_z","base_top_score","base_score_mean")


def sha256(path):
    d=hashlib.sha256()
    with open(path,"rb") as f:
        for buf in iter(lambda:f.read(8<<20),b""):
            d.update(buf)
    return d.hexdigest()


def regressor(seed):
    return HistGradientBoostingRegressor(
        loss="squared_error",max_iter=120,learning_rate=.05,max_depth=3,
        min_samples_leaf=50,l2_regularization=1.0,early_stopping=False,
        random_state=seed)


def candidate_aware_X(X, feature_cols):
    # S label's sampled candidate count is known as a protocol constant, not
    # determined by the revealed positive; all remaining X are from F pretarget.
    if feature_cols.count("x_candidate_log_count") != 1:
        raise ValueError("Expected one pre-outcome candidate count feature")
    k=feature_cols.index("x_candidate_log_count")
    xs=X.copy()
    xs[:,k]=np.log1p(575)
    xf=X.copy()
    return np.column_stack([xs,np.zeros(len(xs))]),np.column_stack([xf,np.ones(len(xf))])


def mixed_fit_predict(Xs,Xf,ds,df,train,eval_idx,seed):
    reg=regressor(seed)
    reg.fit(np.concatenate((Xs[train],Xf[train])),
            np.concatenate((ds[train],df[train])))
    return reg.predict(Xf[eval_idx])


def cluster_ci(diff,users,reps=2000,seed=20261013):
    ids,inverse=np.unique(users.astype(str),return_inverse=True)
    total=np.bincount(inverse,weights=diff,minlength=len(ids))
    counts=np.bincount(inverse,minlength=len(ids))
    rng=np.random.default_rng(seed)
    draws=np.empty(reps,dtype=float)
    for k in range(reps):
        choice=rng.integers(len(ids),size=len(ids))
        draws[k]=total[choice].sum()/counts[choice].sum()
    return [float(v) for v in np.quantile(draws,[.025,.975])]


def run_family(data,family,boot=2000):
    if family not in ("sasrec","gru4rec"):
        raise ValueError("Unsupported family")
    feature_cols=["x_"+x for x in SHARED]+["x_"+family+"_"+x for x in BASE]
    if any(k not in data.columns for k in feature_cols):
        raise ValueError("Missing pre-outcome features")
    X=data[feature_cols].to_numpy(dtype=np.float64)
    features_norm=[
        x.replace("x_"+family+"_","x_") for x in feature_cols
    ]
    # x_candidate_log_count belongs to shared features.
    Xs,Xf=candidate_aware_X(X,features_norm)
    F_b=data[family+"_ndcg10"].to_numpy(dtype=np.float64)
    F_m=data["memory_ndcg10"].to_numpy(dtype=np.float64)
    S_b=data["sampled_"+family+"_ndcg10"].to_numpy(dtype=np.float64)
    S_m=data["sampled_memory_ndcg10"].to_numpy(dtype=np.float64)
    dF=F_m-F_b
    dS=S_m-S_b
    users=data.user_id.astype(str).to_numpy()
    if not np.isfinite(X).all() or not all(np.isfinite(x).all() for x in (dS,dF)):
        raise ValueError("NaN in B1 event utility or decision-time features")
    seen=np.zeros(N,dtype=np.uint8)
    masks={k:np.zeros(N,dtype=bool) for k in ARMS}
    per_fold=[]
    start=time.perf_counter()
    outer_cv=GroupKFold(n_splits=OUTER)
    for fold,(tr,va) in enumerate(outer_cv.split(X,groups=users),start=1):
        if set(users[tr]) & set(users[va]):
            raise RuntimeError("Outer user leakage")
        scores={k:np.full(len(tr),np.nan) for k in ARMS}
        for inner,(fit_idx,val_idx) in enumerate(GroupKFold(n_splits=INNER).split(X[tr],groups=users[tr])):
            t=tr[fit_idx]
            v=tr[val_idx]
            if set(users[t]) & set(users[v]):
                raise RuntimeError("Inner user overlap")
            for name,y in (("sampled_to_full",dS),("full_to_full",dF)):
                model=regressor(SEED+inner)
                model.fit(X[t],y[t])
                scores[name][val_idx]=model.predict(X[v])
            scores["regime_adapted_to_full"][val_idx]=mixed_fit_predict(
                Xs,Xf,dS,dF,t,v,SEED+inner)
        if any(np.isnan(z).any() for z in scores.values()):
            raise RuntimeError("Incomplete inner OOF")
        thresholds={}
        thresholds["sampled_to_full"]=select_threshold(
            scores["sampled_to_full"].tolist(),dS[tr].tolist(),MAX_CALL)
        thresholds["full_to_full"]=select_threshold(
            scores["full_to_full"].tolist(),dF[tr].tolist(),MAX_CALL)
        thresholds["regime_adapted_to_full"]=select_threshold(
            scores["regime_adapted_to_full"].tolist(),dF[tr].tolist(),MAX_CALL)
        final={}
        for name,yy in (("sampled_to_full",dS),("full_to_full",dF)):
            model=regressor(SEED)
            model.fit(X[tr],yy[tr])
            final[name]=model.predict(X[va])
        final["regime_adapted_to_full"]=mixed_fit_predict(
            Xs,Xf,dS,dF,tr,va,SEED)
        fold_out={"fold":fold,"n_train":len(tr),"n_val":len(va),
                  "n_val_users":len(set(users[va])),"arms":{}}
        for arm in ARMS:
            th=thresholds[arm]["threshold"]
            choose=np.zeros(len(va),dtype=bool) if th is None else final[arm]>=th
            masks[arm][va]=choose
            fold_out["arms"][arm]={
                "inner_call_rate":float(thresholds[arm]["dev_oof_call_rate"]),
                "outer_memory_call_rate":float(choose.mean()),
                "outer_full_ndcg10":float(np.mean(F_b[va]+choose*dF[va]))}
        seen[va]+=1
        per_fold.append(fold_out)
        print(json.dumps({"family":family,"completed_fold":fold,
            "fold_outer_quality":{k:v["outer_full_ndcg10"] for k,v in fold_out["arms"].items()}}),
            flush=True)
    if not np.all(seen==1):
        raise RuntimeError("Not every DEV event evaluated exactly once")
    quality={a:F_b+masks[a]*dF for a in ARMS}
    baseline=max(float(F_b.mean()),float(F_m.mean()))
    results={a:{"full_ndcg10":float(quality[a].mean()),
                "memory_calls":int(masks[a].sum()),
                "memory_call_rate":float(masks[a].mean()),
                "quality_minus_best_fixed":float(quality[a].mean()-baseline)}
             for a in ARMS}
    paired={
        "full_minus_sampled":quality["full_to_full"]-quality["sampled_to_full"],
        "adapted_minus_sampled":quality["regime_adapted_to_full"]-quality["sampled_to_full"],
        "adapted_minus_full":quality["regime_adapted_to_full"]-quality["full_to_full"],
    }
    contrasts={key:{"mean_ndcg10":float(v.mean()),
                    "user_cluster_bootstrap_95ci":cluster_ci(v,users,boot)}
              for key,v in paired.items()}
    return {
        "base":family,"n_events":N,"n_users":len(set(users)),
        "outer_group_folds":OUTER,"inner_group_folds":INNER,
        "n_decision_features":X.shape[1],
        "regime_adapted_features":Xs.shape[1],
        "max_inner_call_fraction":MAX_CALL,
        "always_base_F_ndcg10":float(F_b.mean()),
        "always_memory_F_ndcg10":float(F_m.mean()),
        "sampled_minus_full_value_mean":float(np.mean(dS-dF)),
        "sampled_full_value_sign_disagreement_rate":float(np.mean(np.sign(dS)!=np.sign(dF))),
        "arms":results,"contrasts":contrasts,"folds":per_fold,
        "elapsed_cpu_seconds":round(time.perf_counter()-start,2),
        "test_accessed":False,"G5_inference_unchanged":True,
        "not_full_L2D_or_DS_Frame_benchmark":True,
        "pure_S_to_F_no_full_labels_in_model_or_calibration":True,
        "regime_adapted_arm_uses_F_inner_training_labels":True
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Refuse to overwrite nested DEV results")
    meta=json.loads((args.source/"summary.json").read_text())
    input_csv=args.source/"dev_pair_candidate_labels.csv"
    if not (meta["schema"]=="kbs-b1-full-dev-paired-candidate-labels-v1"
            and meta["status"]=="PASS" and meta["n_dev_events"]==N
            and meta["test_accessed"] is False and meta["model_training"] is False
            and meta["B1_nested_gate_fitted"] is False
            and sha256(input_csv)==meta["private_event_source_csv_sha256"]):
        raise RuntimeError("B1 nested can only read frozen paired DEV source")
    df=pd.read_csv(input_csv)
    if len(df)!=N or not df.split.eq("DEV").all() or df.event_id.duplicated().any():
        raise RuntimeError("B1 DEV rows incomplete/invalid")
    if df.user_id.isna().any() or df.user_id.nunique()!=12628:
        raise RuntimeError("B1 author users differ from frozen source")
    results={}
    for family in ("sasrec","gru4rec"):
        results[family]=run_family(df,family)
    out={"schema":"kbs-b1-nested-regime-transfer-dev-v1",
         "scientific_scope":"POST_G5_EXPLORATORY_DEV_ONLY",
         "n_dev_events":N,"n_users":12628,
         "source_candidate_pair_sha256":meta["private_event_source_csv_sha256"],
         "n_original_TEST_used":0,"new_confirmatory_results":False,
         "families":results}
    args.out.mkdir(parents=True,mode=0o700)
    (args.out/"summary.json").write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"status":"B1_NESTED_DEV_EXPLORATORY_COMPLETED",
        "family_summary":{k:{"arms":v["arms"],"contrasts":v["contrasts"]}
                          for k,v in results.items()},"test_accessed":False}),flush=True)

if __name__=="__main__":
    main()
