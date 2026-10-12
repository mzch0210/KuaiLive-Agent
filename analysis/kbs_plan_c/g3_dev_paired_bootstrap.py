#!/usr/bin/env python3
"""DEV-only user-cluster paired bootstrap for fixed OOF policies.

This is a *descriptive conditional DEV* uncertainty calculation, not a valid
independent TEST inference: threshold optimization reused these same OOF DEV
labels. Preserves that limitation verbatim in the exported report.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

METHODS=("utility","difficulty","specialist","uncertainty","history")
CONTRASTS=(
 ("memory_vs_base","memory","base"),
 ("utility_vs_base","utility","base"),
 ("utility_vs_difficulty","utility","difficulty"),
 ("utility_vs_uncertainty","utility","uncertainty"),
 ("utility_vs_specialist","utility","specialist"),
 ("utility_vs_history","utility","history"),
 ("utility_vs_always_memory","utility","memory"),
)


def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def compare_one_family(base,aggregate,seed=20261012,repetitions=5000):
    from collections import defaultdict
    source=base/"dev_features_with_dev_labels.csv"
    oof_path=base/"models"/"dev_oof.csv"
    policy_path=base/"frozen_thresholds.json"
    oof_manifest=json.loads((base/"models"/"oof_manifest.json").read_text())
    assert sha(source)==oof_manifest["source_dev_sha256"]
    assert sha(oof_path)==oof_manifest["provenance_sha256"]
    oof=pd.read_csv(oof_path)
    users=pd.read_csv(source,usecols=["event_id","user_id"])
    assert len(oof)==len(users)==50049
    assert np.array_equal(oof.event_id.values,users.event_id.values)
    assert oof.split.eq("DEV").all()
    p=json.loads(policy_path.read_text())
    assert p["schema"]=="kbs-plan-c-gates-v1" and p["state"]=="DEV_FROZEN_POINTWISE"
    assert p["oof_source_sha256"]==sha(oof_path)
    labels={
      "base":oof.base_ndcg10.to_numpy(np.float64),
      "memory":oof.memory_ndcg10.to_numpy(np.float64)
    }
    delta=labels["memory"]-labels["base"]
    for name in METHODS:
        threshold=p["methods"][name]["threshold"]
        scores=oof["score_"+name].to_numpy(np.float64)
        call=(scores>=float(threshold)) if threshold is not None else np.zeros(len(scores),bool)
        labels[name]=labels["base"]+call*delta
        assert abs(call.mean()-p["methods"][name]["dev_oof_call_rate"])<1e-10
    groups,inv=np.unique(users.user_id.to_numpy(),return_inverse=True)
    n=len(groups)
    sizes=np.bincount(inv,minlength=n)
    if n<1000:
        raise ValueError("Suspicious DEV user group count")
    rng=np.random.default_rng(seed)
    result={"n_events":len(oof),"n_users":n,
            "cluster_unit":"user_id","resamples":repetitions,
            "seed":seed,"method_dev_means":{k:float(v.mean()) for k,v in labels.items()},
            "comparisons":{}}
    # Avoid creating 5,000 x 50,000 row-level arrays: compress outcomes
    # to weighted user sums, then resample 12.6k user clusters.
    for label,positive,negative in CONTRASTS:
        diff=labels[positive]-labels[negative]
        sums=np.bincount(inv,weights=diff,minlength=n)
        mean=float(np.mean(diff))
        reps=np.empty(repetitions,np.float64)
        for k in range(0,repetitions,128):
            draws=rng.integers(0,n,size=(min(128,repetitions-k),n),dtype=np.int32)
            reps[k:k+len(draws)]=sums[draws].sum(axis=1)/sizes[draws].sum(axis=1)
        ci=np.percentile(reps,[2.5,97.5])
        p_one=float((1+np.count_nonzero(reps<=0))/(repetitions+1))
        result["comparisons"][label]={
          "paired_dev_mean":mean,"user_bootstrap_95ci":[float(ci[0]),float(ci[1])],
          "bootstrap_one_sided_tail_at_zero":p_one}
    # Selection of the thresholds was optimized using OOF DEV labels.
    # This bootstrap conditions on that selection and cannot eliminate optimism.
    result.update({
      "status":"DEV_ONLY_CONDITIONAL_UNCERTAINTY_NOT_TEST_CONFIRMATION",
      "threshold_selection_resampling_nested":False,
      "dev_threshold_optimization_bias_possible":True,
      "test_files_read":False,
      "test_outcomes_inspected":False})
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--e2-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--seed",type=int,default=20261012)
    p.add_argument("--reps",type=int,default=5000)
    args=p.parse_args()
    if args.out.exists():
        raise FileExistsError("Bootstrap report exists; no overwrite")
    agg=json.loads((args.e2_dir/"aggregate.json").read_text())
    if (agg["schema"]!="kbs-plan-c-g3-five-gates-dev-only-v1"
        or agg["evaluation_scope"]!="DEV_OOF_POLICY_OPTIMIZATION"
        or agg["test_file_opened"] is not False):
        raise ValueError("Only validated E2 DEV-only gate cache accepted")
    result={"schema":"kbs-plan-c-dev-user-bootstrap-v1",
            "source_e2_aggregate_sha256":sha(args.e2_dir/"aggregate.json"),
            "families":{}}
    for family in ("sasrec","gru4rec"):
        d=compare_one_family(args.e2_dir/family,agg,args.seed,args.reps)
        for method,score in d["method_dev_means"].items():
            expected=(agg["family"][family]["metrics"]["methods"][method]["dev_oof_mean_ndcg10"]
                      if method in METHODS
                      else agg["family"][family]["metrics"]["always_"+method+"_ndcg10"])
            if abs(score-expected)>1e-8:
                raise ValueError(f"{family}/{method}: mismatch with frozen E2 aggregate")
        result["families"][family]=d
        print(json.dumps({"family":family,"comparisons":d["comparisons"]}),flush=True)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"DEV_USER_BOOTSTRAP_COMPLETED",
                      "TEST_opened":False}),flush=True)


if __name__=="__main__":
    main()
