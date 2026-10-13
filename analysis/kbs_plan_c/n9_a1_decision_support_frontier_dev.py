#!/usr/bin/env python3
"""N9-A1: nested DEV-only decision-quality / actual-call frontier.
Fixed decision-support thesis; no existing TEST read, Base training, or hindsight outer threshold.
"""
from __future__ import annotations
import argparse, hashlib, json, math, time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

N=50049
USERS=12628
SEED=20261012
OUTER=5
INNER=4
BUDGETS=(0.,.10,.20,.30,.50,.70,.90,1.0)
SHARED=("hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique","memory_history_supported_share",
        "candidate_log_count")
BASE=("base_margin","base_std","base_top_z","base_top_score","base_score_mean")

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda:f.read(8<<20),b''):
            h.update(part)
    return h.hexdigest()

def model(seed):
    return HistGradientBoostingRegressor(
        loss="squared_error",max_iter=120,learning_rate=.05,max_depth=3,
        min_samples_leaf=50,l2_regularization=1.0,early_stopping=False,
        random_state=seed)

def threshold(scores,labels,cap):
    """Exact original frozen_gate.select_threshold rule, including indivisible ties."""
    n=len(scores)
    if n==0 or len(labels)!=n or not 0<cap<=1:
        raise ValueError("invalid DEV threshold source")
    ordered=sorted(zip(scores,labels),key=lambda pair:pair[0],reverse=True)
    k=math.floor(cap*n)
    best={"threshold":None,"calls":0,"dev_oof_gain":0.}
    running=0.;i=0
    while i<n:
        j=i
        while j<n and ordered[j][0]==ordered[i][0]:
            running+=ordered[j][1];j+=1
        gain=running/n
        if j<=k and gain>best["dev_oof_gain"]+1e-14:
            best={"threshold":ordered[i][0],"calls":j,"dev_oof_gain":gain}
        i=j
    best["dev_oof_call_rate"]=best["calls"]/n
    return best

def ci_by_user(x,users,reps=2000):
    # Paired user-cluster percentile bootstrap; identical bootstrap stream
    # for different policy comparisons to make intervals directly comparable.
    uid,inv=np.unique(users,return_inverse=True)
    numer=np.bincount(inv,weights=x,minlength=len(uid))
    denom=np.bincount(inv,minlength=len(uid))
    rng=np.random.default_rng(20261013)
    draws=np.empty(reps,dtype=np.float64)
    for i in range(reps):
        ix=rng.integers(len(uid),size=len(uid))
        draws[i]=numer[ix].sum()/denom[ix].sum()
    return [float(v) for v in np.quantile(draws,[.025,.975])]

def run_family(data,family):
    names=["x_"+s for s in SHARED]+["x_"+family+"_"+b for b in BASE]
    if any(c not in data.columns for c in names):raise RuntimeError("F decision feature missing")
    X=data[names].to_numpy(dtype=np.float64)
    base=data[family+"_ndcg10"].to_numpy(dtype=np.float64)
    mem=data["memory_ndcg10"].to_numpy(dtype=np.float64)
    delta=mem-base
    user=data.user_id.astype(str).to_numpy()
    if not np.isfinite(X).all() or not np.isfinite(base).all() or not np.isfinite(mem).all():
        raise ValueError("nonfinite F decision context or utility")
    if np.any(base<0) or np.any(base>1) or np.any(mem<0) or np.any(mem>1):
        raise ValueError("out of range F rank utility")
    masks={cap:np.zeros(N,dtype=np.bool_) for cap in BUDGETS}
    seen=np.zeros(N,dtype=np.uint8)
    folds=[]
    t0=time.perf_counter()
    for oi,(tr,va) in enumerate(GroupKFold(n_splits=OUTER).split(X,groups=user),start=1):
        if set(user[tr]) & set(user[va]):raise RuntimeError("outer user leakage")
        pred_oof=np.full(len(tr),np.nan)
        for ii,(fit_idx,hold_idx) in enumerate(GroupKFold(n_splits=INNER).split(X[tr],groups=user[tr])):
            fit=tr[fit_idx]
            if set(user[fit]) & set(user[tr[hold_idx]]):raise RuntimeError("inner user leakage")
            pred=model(SEED+ii)
            pred.fit(X[fit],delta[fit])
            pred_oof[hold_idx]=pred.predict(X[tr[hold_idx]])
        if not np.isfinite(pred_oof).all():raise RuntimeError("incomplete OOF scores")
        final=model(SEED);final.fit(X[tr],delta[tr])
        held_score=final.predict(X[va])
        cap_summary=[]
        for cap in BUDGETS:
            if cap==0:
                mask=np.zeros(len(va),dtype=bool)
                inner_rate=0.
            else:
                th=threshold(pred_oof.tolist(),delta[tr].tolist(),cap)
                mask=np.zeros(len(va),dtype=bool) if th["threshold"] is None else held_score>=th["threshold"]
                inner_rate=th["dev_oof_call_rate"]
            masks[cap][va]=mask
            cap_summary.append({"maximum_inner_rate":cap,
                 "actual_outer_rate":float(mask.mean()),"inner_oof_rate":float(inner_rate)})
        seen[va]+=1
        folds.append({"fold":oi,"outer_events":len(va),"outer_users":len(set(user[va])),"budgets":cap_summary})
        print(json.dumps({"family":family,"outer_fold_complete":oi,
            "outer_events":len(va),"n_budget_rules":len(BUDGETS)},sort_keys=True),flush=True)
    if not np.all(seen==1):raise RuntimeError("outer DEV coverage is incomplete")
    frontier=[]
    best_fixed=float(max(base.mean(),mem.mean()))
    for cap in BUDGETS:
        mask=masks[cap]
        realized=base+mask*delta
        frontier.append({"inner_call_cap":cap,"outer_memory_calls":int(mask.sum()),
           "outer_realized_call_rate":float(mask.mean()),
           "F_outer_NDCG10":float(realized.mean()),
           "gain_over_always_base":float(realized.mean()-base.mean()),
           "quality_minus_best_fixed":float(realized.mean()-best_fixed),
           "paired_user_ci_gain_over_base":ci_by_user(realized-base,user),
           "paired_user_ci_difference_vs_always_memory":ci_by_user(realized-mem,user)})
    at30=frontier[BUDGETS.index(.30)]
    expected={"sasrec":(.3026580312702608,15016),
              "gru4rec":(.303093,14762)}
    quality, calls=expected[family]
    if abs(at30["F_outer_NDCG10"]-quality)>0.000002 or at30["outer_memory_calls"]!=calls:
        raise RuntimeError("30% baseline does not reproduce accepted B1 F-to-F experiment")
    max_quality=base+masks[1.]*delta
    thirty_quality=base+masks[.30]*delta
    return {"family":family,"n_events":N,"n_users":USERS,
       "always_base_F_NDCG10":float(base.mean()),"always_memory_F_NDCG10":float(mem.mean()),
       "baseline_30pct_reproduced":True,
       "no_cap_policy_minus_30pct_NDCG10":float(np.mean(max_quality-thirty_quality)),
       "no_cap_minus_30pct_user_cluster_ci95":ci_by_user(max_quality-thirty_quality,user),
       "frontier":frontier,"outer_fold_metadata":folds,
       "elapsed_cpu_seconds":round(time.perf_counter()-t0,2)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():raise FileExistsError("A1 results must never silently overwrite")
    meta=json.loads((args.source/"summary.json").read_text())
    csv_path=args.source/"dev_pair_candidate_labels.csv"
    if not (meta["schema"]=="kbs-b1-full-dev-paired-candidate-labels-v1" and
            meta["scope"]=="DEV_ONLY_POST_G5_EXPLORATORY" and
            meta["n_dev_events"]==N and meta["n_users"]==USERS and
            meta["test_accessed"] is False and meta["model_training"] is False and
            sha256(csv_path)==meta["private_event_source_csv_sha256"] and
            meta["private_event_source_csv_sha256"]=="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"):
        raise RuntimeError("A0 private DEV source identity gate failed")
    df=pd.read_csv(csv_path)
    if len(df)!=N or not df.split.eq("DEV").all() or df.event_id.duplicated().any() or df.user_id.nunique()!=USERS:
        raise RuntimeError("A1 source is not exact DEV cohort")
    results={fam:run_family(df,fam) for fam in ("sasrec","gru4rec")}
    summary={"schema":"kbs-n9-a1-decision-support-dev-frontier-v1",
         "evidence_tier":"POST_G5_EXPLORATORY_DEV_ONLY",
         "source_b1_private_sha256":meta["private_event_source_csv_sha256"],
         "n_events":N,"n_users":USERS,"outer_user_folds":OUTER,"inner_user_folds":INNER,
         "frozen_G5_TEST_accessed":False,"model_weights_retrained":False,
         "original_30pct_B1_reproduced":all(x["baseline_30pct_reproduced"] for x in results.values()),
         "threshold_tuned_on_outer_results":False,
         "call_caps_predeclared":list(BUDGETS),
         "memory_call_count_not_production_cost":True,
         "families":results}
    args.out.mkdir(parents=True,mode=0o700)
    (args.out/"summary.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"A1":"PASS","n_events":N,"n_users":USERS,"G5_TEST_used":False,
        "fixed_B1_30pct_reproduced":True,
        "families":{f:{"baseline_base":x["always_base_F_NDCG10"],
            "baseline_memory":x["always_memory_F_NDCG10"],
            "no_cap_minus_30pct":x["no_cap_policy_minus_30pct_NDCG10"],
            "no_cap_minus_30pct_ci":x["no_cap_minus_30pct_user_cluster_ci95"],
            "frontier":[{"cap":v["inner_call_cap"],"calls":v["outer_memory_calls"],
                 "realized_rate":v["outer_realized_call_rate"],
                 "ndcg":v["F_outer_NDCG10"],
                 "ci_gain_over_base":v["paired_user_ci_gain_over_base"]}
                 for v in x["frontier"]]}
                 for f,x in results.items()}},sort_keys=True),flush=True)

if __name__=="__main__":
    main()
