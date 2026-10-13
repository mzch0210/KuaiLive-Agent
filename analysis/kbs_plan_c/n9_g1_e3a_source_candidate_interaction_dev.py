#!/usr/bin/env python3
"""N9-G1 E3a. Matched fixed-source F/S interaction, DEV only, no model training."""
from __future__ import annotations
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np
import pandas as pd
N=50049
USERS=12628
REPS=2000
SEED=20261013

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8<<20),b""):h.update(b)
    return h.hexdigest()

def cluster_summary(vals,groups,seed=SEED,reps=REPS):
    u,inv=np.unique(groups,return_inverse=True)
    den=np.bincount(inv,minlength=len(u))
    vals=np.asarray(vals,dtype=float)
    num=np.bincount(inv,weights=vals,minlength=len(u))
    rng=np.random.default_rng(seed)
    draws=np.empty(reps,dtype=float)
    for i in range(reps):
        idx=rng.integers(len(u),size=len(u))
        draws[i]=num[idx].sum()/den[idx].sum()
    return {"mean":float(np.mean(vals)),
        "CI95":[float(v) for v in np.quantile(draws,[.025,.975])],
        "events":int(len(vals)),"users":int(len(u))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    if args.out.exists():raise FileExistsError("Refuse overwrite E3a")
    t=time.monotonic()
    meta=json.loads((args.source/"summary.json").read_text())
    file=args.source/"dev_memory_source_ablation_pairs.csv"
    if not (meta.get("schema")=="kbs-b2-dev-relationship-source-ablation-v1"
        and meta.get("scope")=="POST_G5_DEV_EXPLORATORY"
        and meta.get("status")=="PASS"
        and meta.get("is_full_cohort") is True
        and meta.get("n_events")==N and meta.get("n_users")==USERS
        and meta.get("full_memory_nDCG_mismatches")=={"F":0,"S":0}
        and meta.get("new_TEST_opened") is False
        and meta.get("models_retrained") is False
        and isinstance(meta.get("private_event_source_csv_sha256"),str)
        and len(meta["private_event_source_csv_sha256"])==64
        and sha(file)==meta["private_event_source_csv_sha256"]):
        raise RuntimeError("B2 private DEV origin/hash gate failed")
    df=pd.read_csv(file)
    need=["event_id","user_id","split","memory_ndcg10",
          "b2_long_only_F_ndcg10","sampled_memory_ndcg10",
          "b2_long_only_S_ndcg10"]
    if any(n not in df for n in need):raise RuntimeError("E3a missing matched source columns")
    if not(len(df)==N and df.event_id.is_unique and df.user_id.nunique()==USERS
          and df.split.eq("DEV").all()):raise RuntimeError("E3a DEV identity failed")
    data={k:df[k].to_numpy(dtype=float) for k in need[3:]}
    for k,a in data.items():
        if not (np.isfinite(a).all() and np.all(a>=0) and np.all(a<=1)):
            raise RuntimeError("Invalid NDCG source "+k)
    observed=[data["memory_ndcg10"].mean(),data["b2_long_only_F_ndcg10"].mean(),
              data["sampled_memory_ndcg10"].mean(),data["b2_long_only_S_ndcg10"].mean()]
    expected=[.343509,.333231,.668498,.773602]
    if any(abs(a-b)>3e-6 for a,b in zip(observed,expected)):
        raise RuntimeError("B2 published fixed-source mean parity FAILED")
    dF=data["memory_ndcg10"]-data["b2_long_only_F_ndcg10"]
    dS=data["sampled_memory_ndcg10"]-data["b2_long_only_S_ndcg10"]
    interaction=dF-dS
    if abs(float(interaction.mean())-.115382)>4e-6:
        raise RuntimeError("Source×candidate interaction public-point parity failed")
    users=df.user_id.astype(str).to_numpy()
    global_results={}
    # One joint user-resample stream for covariance-aware source contrasts.
    unique,inv=np.unique(users,return_inverse=True)
    den=np.bincount(inv,minlength=len(unique))
    sums=[np.bincount(inv,weights=v,minlength=len(unique)) for v in (dF,dS,interaction)]
    rng=np.random.default_rng(SEED)
    draws=np.empty((REPS,3),dtype=np.float64)
    for k in range(REPS):
        ix=rng.integers(len(unique),size=len(unique))
        n=den[ix].sum()
        for t0 in range(3):draws[k,t0]=sums[t0][ix].sum()/n
    for j,(name,a) in enumerate((("F_full_minus_long",dF),("S_full_minus_long",dS),("interaction_FminusS",interaction))):
        global_results[name]={"mean":float(a.mean()),"paired_user_bootstrap_CI95":[float(x) for x in np.quantile(draws[:,j],[.025,.975])]}
    sF=np.sign(dF);sS=np.sign(dS)
    signs={"positive_to_negative":int(((sS>0)&(sF<0)).sum()),
           "negative_to_positive":int(((sS<0)&(sF>0)).sum()),
           "zero_in_either":int(((sS==0)|(sF==0)).sum()),
           "opposite_nonzero":int(((sS*sF)<0).sum()),
           "all_sign_category_differences_including_zero":int((sS!=sF).sum())}
    fields=["x_hist_event_count","x_hist_distinct","x_hist_repeat_max",
            "x_candidate_log_count","x_sasrec_base_std"]
    strata={}
    for field in fields:
        if field not in df:continue
        values=pd.to_numeric(df[field],errors="coerce")
        if values.isna().any():raise RuntimeError("Nonfinite stratum "+field)
        # Preset quartile attempt; ties may legitimately collapse boundaries.
        bins=pd.qcut(values,q=4,duplicates="drop")
        rows=[]
        for k,c in enumerate(bins.cat.categories):
            mask=(bins==c).to_numpy()
            if mask.sum()<100:continue
            rows.append({"quartile_index":k+1,"interval":str(c),
                "n_events":int(mask.sum()),"n_users":int(len(np.unique(users[mask]))),
                "F_gap":float(dF[mask].mean()),"S_gap":float(dS[mask].mean()),
                "source_candidate_interaction":cluster_summary(interaction[mask],users[mask],seed=SEED+17+k)})
        strata[field]=rows
    result={"schema":"kbs-n9-g1-e3a-source-candidate-dev-v1",
        "evidence":"POST_G5_EXPLORATORY_DEV_ONLY",
        "n_events":N,"n_users":USERS,"source_SHA256":meta["private_event_source_csv_sha256"],
        "G5_TEST_opened":False,"base_retrained":False,"Memory_retrained":False,
        "user_bootstrap_draws":REPS,"bootstrap_seed":SEED,
        "original_source_mean_parity":True,"global":global_results,
        "nonzero_sign_category_counts":signs,"pretarget_quartile_strata":strata,
        "method_limit":"candidate count, candidate IDs and competition vary together; historical source effects are noncausal",
        "elapsed_seconds":round(time.monotonic()-t,2)}
    args.out.mkdir(parents=True,mode=0o700)
    (args.out/"summary.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"G1_E3a":"PASS","events":N,"users":USERS,
        "source_identity":"SHA_PASS","global":global_results,
        "sign_categories":signs,"strata":strata,
        "runtime_seconds":result["elapsed_seconds"],"no_TEST":True},sort_keys=True),flush=True)

if __name__=="__main__":
    main()
