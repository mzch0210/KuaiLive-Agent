#!/usr/bin/env python3
"""G5-B ONE-SHOT sealed TEST label scoring and prespecified inferential contrasts.

Must execute only after G5-A immutable, outcome-free ranks/decisions manifest.
No threshold/model optimization, data-driven seed selection, or TEST-guided
revisions. Outputs aggregate evidence only, preserving event rows on User-host.
"""
from __future__ import annotations
import argparse,hashlib,json,math,time
from pathlib import Path
import numpy as np,pyarrow.parquet as pq

SEEDS=(20261012,20261013,20261014)
FAMILIES=("sasrec","gru4rec")
METHODS=("utility","difficulty","specialist","uncertainty","history")
PAIRS=tuple((seed,family) for seed in SEEDS for family in FAMILIES)
CONTRASTS=(("utility_minus_base","utility","base"),
           ("utility_minus_difficulty","utility","difficulty"),
           ("utility_minus_specialist","utility","specialist"))
B=5000

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for block in iter(lambda:f.read(8*1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def ndcg10(ranks):
    return np.where(ranks<=10,1.0/np.log2(ranks+1),0.0)

def holm3(pvalues):
    p=np.asarray(pvalues,dtype=np.float64)
    if p.shape!=(3,) or np.any(p<0) or np.any(p>1):
        raise ValueError("Only three preregistered Holm p values")
    ordered=np.argsort(p,kind="stable")
    adjusted=np.empty_like(p)
    acc=0.0
    for k,i in enumerate(ordered):
        acc=max(acc,min(1.,(3-k)*p[i]))
        adjusted[i]=acc
    return adjusted

def group_clustering(values,groups,seed,reps=5000):
    """One-sided cluster random-sign test and paired cluster bootstrap for 18 contrasts.

    Sign-flip inference assumes sign-symmetric *user-cluster* errors under H0,
    and is labeled explicitly; same test resample indices for all contrasts.
    """
    unique,inverse=np.unique(groups,return_inverse=True)
    n=len(unique)
    if n<1000:
        raise ValueError("Too few user clusters")
    weight=np.bincount(inverse,minlength=n)
    # Invariant target ordering: matrix is C x N observations.
    arr=np.asarray(values,dtype=np.float64)
    if arr.ndim!=2 or arr.shape[1]!=len(groups):
        raise ValueError("Cluster comparison shape mismatch")
    sums=np.vstack([np.bincount(inverse,weights=x,minlength=n) for x in arr])
    means=arr.mean(axis=1)
    boot=np.empty((reps,len(arr)),dtype=np.float64)
    perm=np.empty((reps,len(arr)),dtype=np.float64)
    rng=np.random.default_rng(seed)
    # chunk to bound memory; matrix products are CPU-only.
    for start in range(0,reps,40):
        k=min(40,reps-start)
        draws=rng.integers(0,n,size=(k,n),dtype=np.int32)
        b_sums=sums[:,draws].sum(axis=2).T
        b_weights=weight[draws].sum(axis=1)
        boot[start:start+k]=b_sums/b_weights[:,None]
        signs=rng.integers(0,2,size=(k,n),dtype=np.int8).astype(np.float64)*2-1
        perm[start:start+k]=signs @ sums.T/len(groups)
    lo,hi=np.percentile(boot,[2.5,97.5],axis=0)
    # H0: improvement <= 0; symmetric cluster sign randomization.
    pv=(1+np.sum(perm>=means[None,:],axis=0))/(reps+1)
    return unique.size,means,lo,hi,pv

def main(g1,unlabeled,registry,index,out,seed=20261012):
    if out.exists() or out.with_name(out.name+".incomplete").exists():
        raise FileExistsError("One-shot TEST output already exists: no overwrite/re-run")
    start=time.monotonic()
    registered=json.loads(registry.read_text())
    a=json.loads((unlabeled/"manifest.json").read_text())
    if (a["schema"]!="kbs-plan-c-g5-unlabeled-target-blind-test-v1"
        or a["status"]!="FROZEN_SIX_BASE_TEST_DECISIONS_BEFORE_OUTCOME_EVALUATION"
        or a["registry_sha256"]!=sha(registry)
        or a["test_target_author_labels_loaded"] is not False
        or a["test_ranks_computed"] is not False
        or a["test_ndcg_computed"] is not False
        or a["no_TEST_model_or_threshold_fit"] is not True
        or registered["test_performance_seen"] is not False):
        raise ValueError("Frozen G5-A pretarget, outcome-blind evidence required")
    for name,expected in a["file_sha256"].items():
        if sha(unlabeled/name)!=expected:
            raise ValueError("Frozen unlabeled predictions changed "+name)
    ids=np.load(unlabeled/"event_ids.npy",allow_pickle=False)
    users=np.load(unlabeled/"user_ids.npy",allow_pickle=False)
    top=np.load(unlabeled/"top10_author_tokens.npy",allow_pickle=False)
    calls=np.load(unlabeled/"gate_calls.npy",allow_pickle=False)
    candidates=np.load(unlabeled/"candidate_counts.npy",allow_pickle=False)
    if (len(ids)!=47575 or top.shape!=(len(ids),7,10)
        or calls.shape!=(len(ids),6,5)
        or not np.all(candidates>=10)
        or tuple(a["models"])!=tuple(f"{seed}_{fam}" for seed,fam in PAIRS)
        or tuple(a["methods"])!=METHODS):
        raise ValueError("Invalid G5-A frozen decisions shapes")
    # Only here, after frozen decisions and hashes, is the TEST target label
    # column opened. The label never appears in model input, thresholds or
    # active candidate lists.
    if sha(g1/"test_cohort_sealed.parquet")!=registered["test_cohort_sha256"]:
        raise ValueError("Actual heldout TEST source changed")
    targets=pq.read_table(g1/"test_cohort_sealed.parquet",
                          columns=["source_event_id","author_id","user_id"])
    if (not np.array_equal(targets.column("source_event_id").to_numpy(),ids)
        or not np.array_equal(targets.column("user_id").to_numpy(),users)):
        raise ValueError("Target-blind inference IDs and TEST labels not aligned")
    # TRAIN-index known authors: target author to token conversion from
    # read-only G1 manifest-controlled train authors; no target-based tuning.
    # Reuse original author embedding lookup only.
    authors=np.load(index/"authors.npy",mmap_mode="r")
    originals=np.asarray(targets.column("author_id").to_numpy(),np.int64)
    token=np.searchsorted(authors,originals)
    if np.any(token>=len(authors)) or np.any(authors[token]!=originals):
        raise ValueError("G1 TEST warm-target invariant violated")
    token=token+1
    matching=(top==token[:,None,None])
    # Every ranking is a strict top10 author list; no target can match twice.
    if np.any(matching.sum(axis=2)>1):
        raise ValueError("TEST top10 contains repeated target")
    r=np.where(matching.any(axis=2),matching.argmax(axis=2)+1,11)
    utilities=ndcg10(r)
    hits=(r<=10)
    measures={}
    contrasts=[]
    labels=[]
    for k,(train_seed,family) in enumerate(PAIRS):
        base=utilities[:,k]
        memory=utilities[:,6]
        gain=memory-base
        methods={name:base+calls[:,k,j]*gain for j,name in enumerate(METHODS)}
        methods["base"]=base
        methods["memory"]=memory
        means={}
        for name,vec in methods.items():
            if name in METHODS:
                mask=calls[:,k,METHODS.index(name)]
                hit=np.where(mask,hits[:,6],hits[:,k])
            elif name=="base":
                hit=hits[:,k]
            else:
                hit=hits[:,6]
            means[name]={"NDCG@10":float(vec.mean()),
                         "HR@10":float(np.mean(hit))}
        for name in METHODS:
            means[name]["call_count"]=int(calls[:,k,METHODS.index(name)].sum())
            means[name]["test_realized_call_fraction"]=float(
                 calls[:,k,METHODS.index(name)].mean())
        base_mean=means["base"]["NDCG@10"]
        oracle=base+np.maximum(gain,0)
        maxcalls=math.floor(.3*len(base))
        best=np.sort(gain[gain>0])[::-1]
        means["random30_conditional_expectation"]={
            "NDCG@10":float(base_mean+maxcalls/len(base)*gain.mean()),
            "note":"exact conditional expectation, not separately sampled actual policy"}
        means["hindsight_oracle30"]={
            "NDCG@10":float(base_mean+best[:maxcalls].sum()/len(base)),
            "calls":int(min(maxcalls,len(best))),
            "note":"nondeployable realized label-using upper bound"}
        means["hindsight_oracle_unlimited"]={
            "NDCG@10":float(oracle.mean()),
            "note":"nondeployable realized label-using upper bound"}
        measures[f"{train_seed}_{family}"]=means
        for title,p,q in CONTRASTS:
            labels.append((f"{train_seed}_{family}",title))
            contrasts.append(methods[p]-methods[q])
    nusers,means,lo,hi,pvalues=group_clustering(np.vstack(contrasts),users,seed,B)
    tests={}
    for k,(train_seed,family) in enumerate(PAIRS):
        name=f"{train_seed}_{family}"
        subset=[]
        pv=pvalues[k*3:(k+1)*3]
        adjusted=holm3(pv)
        for j,(title,p,q) in enumerate(CONTRASTS):
            pos=k*3+j
            subset.append({"contrast":title,
                "mean_paired_test_ndcg10_difference":float(means[pos]),
                "cluster_bootstrap_ci95":[float(lo[pos]),float(hi[pos])],
                "cluster_signflip_one_sided_p":float(pvalues[pos]),
                "holm3_adjusted_p":float(adjusted[j]),
                "reject_at_0_05":bool(adjusted[j]<.05)})
        tests[name]=subset
    stage=out.with_name(out.name+".incomplete")
    stage.mkdir(parents=True,mode=0o700)
    summary={
      "schema":"kbs-plan-c-g5-one-shot-heldout-test-v1",
      "status":"ONE_SHOT_HELDOUT_TEST_EVALUATION_COMPLETED",
      "source_registry_sha256":sha(registry),
      "source_unlabeled_manifest_sha256":sha(unlabeled/"manifest.json"),
      "test_cohort_sha256":registered["test_cohort_sha256"],
      "n_test_events":len(ids),"n_test_users":nusers,
      "base_ranking_models":list(a["models"]),
      "memory_fixed_across_all_models":True,
      "training_or_threshold_adjustments_after_TEST":False,
      "sequential_TEST_history_prior_only":True,
      "three_primary_comparisons_per_family_seed":list(x[0] for x in CONTRASTS),
      "primary_statistic":"per-event paired NDCG@10, user-cluster weighted",
      "inference":"5000 user-cluster paired bootstrap percentile CIs; 5000 one-sided cluster sign flips with Holm adjustment of three predeclared contrasts PER base/seed",
      "signflip_assumption":"approximately sign-symmetric user-cluster null errors; correlated seeds and no global familywise 18-test correction",
      "bootstrap_resamples":B,
      "seed":seed,
      "performance":measures,"primary_tests":tests,
      "all_models_and_thresholds_frozen":True,
      "realized_TEST_call_fraction_not_forced_to_DEV_budget":True,
      "not_net_computational_speedup_evidence":True,
      "elapsed_seconds":round(time.monotonic()-start,2)
    }
    (stage/"aggregate.json").write_text(json.dumps(summary,indent=2)+"\n")
    stage.rename(out)
    print(json.dumps({"status":summary["status"],"n_test_events":len(ids),
         "n_test_users":nusers,"mean_ndcg10":{
             k:{meth:v["NDCG@10"] for meth,v in meas.items()
                 if meth in ("base","memory","utility","difficulty","specialist")}
             for k,meas in measures.items()},
         "primary_holm_pass":{k:all(v["reject_at_0_05"] for v in tests[k])
                              for k in tests},
         "no_test_retraining":True}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for opt in ("g1","unlabeled","registry","index","out"):
        p.add_argument("--"+opt,type=Path,required=True)
    p.add_argument("--seed",type=int,default=20261012)
    args=p.parse_args()
    main(args.g1,args.unlabeled,args.registry,args.index,args.out,args.seed)
