#!/usr/bin/env python3
"""G2 E1: S→F vs F→F fitted-decision switch accounting; B1-compatible DEV only."""
from __future__ import annotations
import argparse,hashlib,json,time,math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold
N=50049;USERS=12628;SEED=20261012;CAP=.30;BOOT=2000
SHARED=("hist_event_count","hist_warm_count","hist_distinct",
        "hist_repeat_max","hist_short_unique","memory_history_supported_share",
        "candidate_log_count")
BASE=("base_margin","base_std","base_top_z","base_top_score","base_score_mean")
EXPECTED={"sasrec":{"S":(.296499,14988),"F":(.3026580312702608,15016)},
          "gru4rec":{"S":(.298123,15001),"F":(.3030931582511879,14762)}}
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()
def reg(seed):
    return HistGradientBoostingRegressor(loss="squared_error",max_iter=120,
        learning_rate=.05,max_depth=3,min_samples_leaf=50,
        l2_regularization=1.0,early_stopping=False,random_state=seed)
def threshold(scores,delta,cap=CAP):
    # Identical to frozen_gate.select_threshold, matching B1/A1 original semantics.
    order=sorted(zip(scores,delta),key=lambda x:x[0],reverse=True)
    n=len(order);maximum=math.floor(n*cap);best=None;gain=0.;cum=0.;i=0
    while i<n:
        j=i
        while j<n and order[j][0]==order[i][0]:
            cum+=order[j][1];j+=1
        new=cum/n
        if j<=maximum and new>gain+1e-14:
            gain=new;best=order[i][0]
        i=j
    return best
def cluster_ci(delta,user,reps=BOOT,seed=20261013):
    uid,inv=np.unique(user,return_inverse=True)
    num=np.bincount(inv,weights=delta,minlength=len(uid))
    den=np.bincount(inv,minlength=len(uid))
    rng=np.random.default_rng(seed)
    draws=np.empty(reps)
    for i in range(reps):
        idx=rng.integers(len(uid),size=len(uid))
        draws[i]=num[idx].sum()/den[idx].sum()
    return [float(v) for v in np.quantile(draws,[.025,.975])]
def run(df,family):
    features=["x_"+s for s in SHARED]+["x_"+family+"_"+s for s in BASE]
    if len(features)!=12 or not set(features).issubset(df.columns):
        raise RuntimeError("missing original B1 features")
    X=df[features].to_numpy(dtype=float)
    user=df.user_id.astype(str).to_numpy()
    dF=df.memory_ndcg10.to_numpy(dtype=float)-df[family+"_ndcg10"].to_numpy(dtype=float)
    dS=df.sampled_memory_ndcg10.to_numpy(dtype=float)-df["sampled_"+family+"_ndcg10"].to_numpy(dtype=float)
    base=df[family+"_ndcg10"].to_numpy(dtype=float)
    if not all(np.isfinite(a).all() for a in (X,dF,dS,base)):
        raise RuntimeError("nonfinite B1 F/S input")
    mS=np.zeros(N,dtype=bool);mF=np.zeros(N,dtype=bool);seen=np.zeros(N,dtype=np.uint8)
    folds=[]
    for oi,(tr,va) in enumerate(GroupKFold(n_splits=5).split(X,groups=user),1):
        if set(user[tr])&set(user[va]):raise RuntimeError("outer GroupKFold leak")
        scS=np.full(len(tr),np.nan);scF=np.full(len(tr),np.nan)
        for ii,(fi,vi) in enumerate(GroupKFold(n_splits=4).split(X[tr],groups=user[tr])):
            t=tr[fi];v=tr[vi]
            if set(user[t])&set(user[v]):raise RuntimeError("inner GroupKFold leak")
            for y,scores in [(dS,scS),(dF,scF)]:
                model=reg(SEED+ii);model.fit(X[t],y[t]);scores[vi]=model.predict(X[v])
        if not(np.isfinite(scS).all() and np.isfinite(scF).all()):
            raise RuntimeError("OOF incomplete")
        tS=threshold(scS.tolist(),dS[tr].tolist())
        tF=threshold(scF.tolist(),dF[tr].tolist())
        fitS=reg(SEED);fitF=reg(SEED)
        fitS.fit(X[tr],dS[tr]);fitF.fit(X[tr],dF[tr])
        mS[va]=False if tS is None else (fitS.predict(X[va])>=tS)
        mF[va]=False if tF is None else (fitF.predict(X[va])>=tF)
        seen[va]+=1
        folds.append({"outer_fold":oi,"events":int(len(va)),"users":int(len(set(user[va]))),
            "S_calls":int(mS[va].sum()),"F_calls":int(mF[va].sum())})
        print(json.dumps({"family":family,"outer_fold_complete":oi,"heldout_events":len(va)}),flush=True)
    if not np.all(seen==1):raise RuntimeError("incomplete B1 held-out event coverage")
    qualityS=base+mS*dF;qualityF=base+mF*dF
    expected=EXPECTED[family]
    for name,q,mask in [("S",qualityS,mS),("F",qualityF,mF)]:
        y,c=expected[name]
        if abs(q.mean()-y)>3e-6 or int(mask.sum())!=c:
            raise RuntimeError("B1 primary 30% original NDCG/call parity failed "+family+" "+name)
    on=mF & ~mS;off=mS & ~mF;same=mF==mS
    regret=qualityF-qualityS
    identity=(mF.astype(int)-mS.astype(int))*dF
    if not np.allclose(regret,identity,rtol=0,atol=1e-14):
        raise RuntimeError("E1 decision contribution accounting failed")
    source_label_sign=np.sign(dS);target_label_sign=np.sign(dF)
    res={"n_events":N,"n_users":USERS,"family":family,
        "original_B1_30pct_S_F_parity":True,
        "S_to_F":{"NDCG":float(qualityS.mean()),"Memory_calls":int(mS.sum()),"actual_rate":float(mS.mean())},
        "F_to_F":{"NDCG":float(qualityF.mean()),"Memory_calls":int(mF.sum()),"actual_rate":float(mF.mean())},
        "policy_disagreement":{"events":int((~same).sum()),"rate":float((~same).mean()),
          "switch_on_F":int(on.sum()),"switch_off_F":int(off.sum()),
          "F_delta_on_switch_on":float(dF[on].mean()) if on.any() else None,
          "F_delta_on_switch_off":float(dF[off].mean()) if off.any() else None,
          "net_gain_on_switch_on_event_avg":float(np.sum(dF[on])/N),
          "net_gain_from_switch_off_event_avg":float(-np.sum(dF[off])/N),
          "total_exact_F_policy_gain":float(regret.mean()),
          "gain_cluster_user_CI95":cluster_ci(regret,user),
          "disagreement_event_quality_impact":float(regret[~same].mean()) if (~same).any() else None,
          "switch_on_nonzero_utility":int((dF[on]!=0).sum()),
          "switch_off_nonzero_utility":int((dF[off]!=0).sum())},
        "supervision_label_sign":{"three_class_difference_including_zero":int((source_label_sign!=target_label_sign).sum()),
           "strict_nonzero_opposite":int((source_label_sign*target_label_sign<0).sum())},
        "outer_fold_metadata":folds}
    return res
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    x=ap.parse_args()
    if x.out.exists():raise FileExistsError("Never overwrite exploratory report")
    meta=json.loads((x.source/"summary.json").read_text())
    source=x.source/"dev_pair_candidate_labels.csv"
    if not(meta.get("schema")=="kbs-b1-full-dev-paired-candidate-labels-v1"
      and meta.get("status")=="PASS" and meta.get("n_dev_events")==N
      and meta.get("n_users")==USERS
      and meta.get("scope")=="DEV_ONLY_POST_G5_EXPLORATORY"
      and meta.get("target_retained_sampling_offline_labels_only") is True
      and meta.get("test_accessed") is False and meta.get("model_training") is False
      and sha(source)=="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
      and sha(source)==meta.get("private_event_source_csv_sha256")):
        raise RuntimeError("E1 invalid private paired DEV data source")
    df=pd.read_csv(source)
    if not(len(df)==N and df.event_id.is_unique and df.split.eq("DEV").all()
       and df.user_id.nunique()==USERS):raise RuntimeError("DEV row identity mismatched")
    begin=time.perf_counter()
    results={f:run(df,f) for f in ["sasrec","gru4rec"]}
    o={"schema":"kbs-n9-g2-e1-decision-switches-dev-v1",
       "scope":"POST_G5_EXPLORATORY_DEV_ONLY","n_events":N,"n_users":USERS,
       "source_SHA256":meta["private_event_source_csv_sha256"],"test_accessed":False,
       "updated_G5_family":False,"bootstrap_draws":BOOT,
       "corrected_S_estimator":"NOT_FITTED_METHOD_ELIGIBILITY_UNRESOLVED",
       "sampled_target_retain_online":False,"families":results,
       "CPU_wall_seconds":round(time.perf_counter()-begin,2)}
    x.out.mkdir(parents=True,mode=0o700)
    (x.out/"summary.json").write_text(json.dumps(o,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"E1":"PASS_B1_PARITY","families":results,"G5_TEST":False},sort_keys=True),flush=True)
if __name__=="__main__":
    main()
