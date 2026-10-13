#!/usr/bin/env python3
"""B2-3 DEV-only nested selector ablation: matched variants, fixed Base, users.

Reuses B1 full F/S Base metrics, same 5x4 GroupKFold and frozen-HGB family.
Returns only global aggregates and user-bootstrap CIs. No G5 TEST.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from frozen_gate import select_threshold
from b1_nested_regime_transfer_dev import regressor, cluster_ci

N=50049
N_USERS=12628
VARIANTS=("full","long_only","short_only","popularity_only","relationship_shifted")
FAMILIES=("sasrec","gru4rec")
GROUPS=("all12","candidate_base_only")
SHARED=("hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique",
        "memory_history_supported_share","candidate_log_count")
BASE=("base_margin","base_std","base_top_z","base_top_score","base_score_mean")
OUTER=5
INNER=4
MAX_CALL=.30
SEED=20261012


def hash_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for x in iter(lambda:f.read(8<<20),b""):
            h.update(x)
    return h.hexdigest()


def run_one(df, family, variant, feature_set, splits):
    if variant not in VARIANTS or family not in FAMILIES or feature_set not in GROUPS:
        raise ValueError("Unexpected frozen B2 experiment arm")
    shared=SHARED if feature_set=="all12" else ("candidate_log_count",)
    features=["x_"+v for v in shared]+["x_"+family+"_"+v for v in BASE]
    if len(features)!=(12 if feature_set=="all12" else 6):
        raise RuntimeError("Invalid B2 pretarget feature dimension")
    if any(c not in df.columns for c in features):
        raise RuntimeError("Missing frozen full-active features")
    X=df[features].to_numpy(dtype=np.float64)
    f_base=df[family+"_ndcg10"].to_numpy(dtype=np.float64)
    s_base=df["sampled_"+family+"_ndcg10"].to_numpy(dtype=np.float64)
    fm_key=("memory_ndcg10" if variant=="full"
            else "b2_"+variant+"_F_ndcg10")
    sm_key=("sampled_memory_ndcg10" if variant=="full"
            else "b2_"+variant+"_S_ndcg10")
    f_mem=df[fm_key].to_numpy(dtype=np.float64)
    s_mem=df[sm_key].to_numpy(dtype=np.float64)
    dF=f_mem-f_base
    dS=s_mem-s_base
    if any(not np.isfinite(v).all() for v in (X,dF,dS)):
        raise RuntimeError("Nonfinite B2 DEV data")
    choose={arm:np.zeros(N,dtype=bool) for arm in ("S_to_F","F_to_F")}
    observed=np.zeros(N,dtype=np.uint8)
    counts=[]
    start=time.monotonic()
    for fold,(tr,val,inner) in enumerate(splits,1):
        oof={"S_to_F":np.full(len(tr),np.nan),
             "F_to_F":np.full(len(tr),np.nan)}
        for ii,(itr,iva) in enumerate(inner):
            for arm,target in (("S_to_F",dS),("F_to_F",dF)):
                model=regressor(SEED+ii)
                model.fit(X[tr[itr]],target[tr[itr]])
                oof[arm][iva]=model.predict(X[tr[iva]])
        if any(np.isnan(a).any() for a in oof.values()):
            raise RuntimeError("Inner user-disjoint OOF incomplete")
        report={"outer_fold":fold,"count":len(val)}
        for arm,target in (("S_to_F",dS),("F_to_F",dF)):
            frozen=select_threshold(oof[arm].tolist(),target[tr].tolist(),MAX_CALL)
            model=regressor(SEED)
            model.fit(X[tr],target[tr])
            predicted=model.predict(X[val])
            threshold=frozen["threshold"]
            mask=np.zeros(len(val),dtype=bool) if threshold is None else predicted>=threshold
            choose[arm][val]=mask
            report[arm+"_inner_rate"]=float(frozen["dev_oof_call_rate"])
            report[arm+"_outer_rate"]=float(mask.mean())
        observed[val]+=1
        counts.append(report)
    if not np.all(observed==1):
        raise RuntimeError("Outer DEV events not covered exactly once")
    q={arm:f_base+mask*dF for arm,mask in choose.items()}
    users=df.user_id.astype(str).to_numpy()
    regret=q["F_to_F"]-q["S_to_F"]
    return {
        "variant":variant,
        "feature_set":feature_set,
        "family":family,
        "n_events":N,
        "n_user_groups":len(set(users)),
        "always_base_F_NDCG10":float(f_base.mean()),
        "always_memory_F_NDCG10":float(f_mem.mean()),
        "sampled_memory_NDCG10":float(s_mem.mean()),
        "mean_regime_label_shift":float(np.mean(dF-dS)),
        "sign_category_change_rate":float(np.mean(np.sign(dF)!=np.sign(dS))),
        "arm_quality":{
            arm:{"F_NDCG10":float(v.mean()),
                 "F_gain_over_base":float(np.mean(v-f_base)),
                 "F_gain_over_best_fixed":float(v.mean()-max(f_base.mean(),f_mem.mean())),
                 "memory_calls":int(choose[arm].sum()),
                 "realized_memory_call_rate":float(choose[arm].mean())}
            for arm,v in q.items()},
        "regret_F_aligned_minus_S_mismatched":{
            "mean_F_NDCG10":float(regret.mean()),
            "user_bootstrap_CI95":cluster_ci(regret,users,reps=2000)},
        "folds":counts,
        "elapsed_CPU_seconds":round(time.monotonic()-start,2),
        "_private_regret":regret
    }


def outer_splits(groups):
    X=np.zeros((len(groups),1))
    res=[]
    for tr,v in GroupKFold(n_splits=OUTER).split(X,groups=groups):
        if set(groups[tr]) & set(groups[v]):
            raise RuntimeError("Outer user leakage")
        inner=[]
        for a,b in GroupKFold(n_splits=INNER).split(X[tr],groups=groups[tr]):
            if set(groups[tr[a]]) & set(groups[tr[b]]):
                raise RuntimeError("Inner user leakage")
            inner.append((a,b))
        res.append((tr,v,inner))
    return res


def run(source,out):
    if out.exists():
        raise FileExistsError("Do not overwrite B2 nested output")
    meta=json.loads((source/"summary.json").read_text())
    private=source/"dev_memory_source_ablation_pairs.csv"
    if not (meta["schema"]=="kbs-b2-dev-relationship-source-ablation-v1"
            and meta["scope"]=="POST_G5_DEV_EXPLORATORY"
            and meta["status"]=="PASS"
            and meta["is_full_cohort"] and meta["n_events"]==N
            and meta["n_users"]==N_USERS
            and meta["full_memory_nDCG_mismatches"]=={"F":0,"S":0}
            and not meta["new_TEST_opened"] and not meta["models_retrained"]
            and not meta["b2_nested_policy_fit"]
            and len(meta["private_event_source_csv_sha256"])==64
            and hash_file(private)==meta["private_event_source_csv_sha256"]):
        raise RuntimeError("B2 full Memory component paired DEV source not certified")
    data=pd.read_csv(private)
    if not (len(data)==N and data.event_id.is_unique and
            data.split.eq("DEV").all() and data.user_id.nunique()==N_USERS):
        raise RuntimeError("B2 matched DEV events/user groups invalid")
    groups=data.user_id.astype(str).to_numpy()
    splits=outer_splits(groups)
    result={}
    for feature_set in GROUPS:
        group_results={}
        for family in FAMILIES:
            fam={}
            regrets={}
            for variant in VARIANTS:
                report=run_one(data,family,variant,feature_set,splits)
                regrets[variant]=report.pop("_private_regret")
                fam[variant]=report
                print(json.dumps({"completed":True,"feature_set":feature_set,
                    "family":family,"variant":variant,
                    "regret":report["regret_F_aligned_minus_S_mismatched"]["mean_F_NDCG10"],
                    "F_to_F_NDCG":report["arm_quality"]["F_to_F"]["F_NDCG10"]}),flush=True)
            contrasts={}
            for control in ("long_only","short_only","popularity_only","relationship_shifted"):
                delta=regrets["full"]-regrets[control]
                contrasts["full_regret_minus_"+control+"_regret"]={
                    "paired_mean":float(delta.mean()),
                    "user_bootstrap_CI95":cluster_ci(delta,groups,reps=2000)}
            fam["_paired_source_specificity_regret_interactions"]=contrasts
            group_results[family]=fam
        result[feature_set]=group_results
    manifest={
        "schema":"kbs-b2-nested-user-group-knowledge-specificity-dev-v1",
        "scope":"POST_G5_EXPLORATORY_DEV_ONLY",
        "n_events":N,"n_users":N_USERS,
        "n_outer_folds":OUTER,"n_inner_folds":INNER,
        "max_inner_memory_calls":MAX_CALL,
        "source_b2_private_SHA256":meta["private_event_source_csv_sha256"],
        "src_B1_F_and_S_locked":True,
        "F_features_pretarget":True,
        "history_free_featureset_has_only_candidate_count_and_base_score_descriptors":True,
        "test_accessed":False,"base_retrained":False,
        "original_G5_test_unchanged":True,
        "any_claim_confirmatory":False,
        "fixed_hgb_max_iter":120,
        "bootstrap_user_cluster_draws":2000,
        "outcomes":result
    }
    out.mkdir(parents=True,mode=0o700)
    (out/"summary.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"B2_nested":"PASS","DEV":N,"variants":len(VARIANTS),
                      "feature_sets":len(GROUPS),"TEST_opened":False}),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    run(a.source,a.out)
