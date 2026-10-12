#!/usr/bin/env python3
"""Budget-matched DEV diagnostics from already frozen E2 OOF events.

No new model fits, Base scores, Memory replay, TEST access or event upload.
Oracle@budget is hindsight-only, never deployable. Score-first top-k
frontiers are retrospective diagnostics, NOT DEV-frozen pointwise policies.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

METHODS=("utility","difficulty","specialist","uncertainty","history")
BUDGETS=(0.0,0.05,0.10,0.15,0.20,0.30,0.50,1.0)
RANDOM_SEEDS=tuple(range(20261012,20261032))


def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):
            h.update(b)
    return h.hexdigest()


def numbers(df, frozen, budget):
    n=len(df)
    k=math.floor(budget*n)
    base=df.base_ndcg10.to_numpy(dtype=np.float64)
    memory=df.memory_ndcg10.to_numpy(dtype=np.float64)
    delta=memory-base
    base_score=float(base.mean())
    # Exact *realized* hindsight upper bound for at most k non-negative-gain calls.
    best=np.sort(delta[delta>0])[::-1]
    oracle_gain=float(np.sum(best[:k])/n)
    random_expected=float(base_score+(k/n)*delta.mean())
    repeats=[]
    for seed in RANDOM_SEEDS:
        rng=np.random.default_rng(seed)
        if k:
            selected=rng.choice(n,size=k,replace=False)
            repeats.append(float(base_score+delta[selected].sum()/n))
        else:
            repeats.append(base_score)
    options={}
    tie=df.event_id.to_numpy(dtype=np.int64)
    for method in METHODS:
        scores=df["score_"+method].to_numpy(dtype=np.float64)
        if not np.isfinite(scores).all():
            raise ValueError("nonfinite score "+method)
        # Stable event-ID tie break, no label-dependent choice.
        ordered=np.lexsort((tie,-scores))
        top=ordered[:k]
        score_top=float(base_score+delta[top].sum()/n)
        # Compare previously selected DEV-frozen *pointwise* 30%-cap policy
        # separately; never pretend top-k equals a serving threshold.
        policy=frozen["methods"][method]
        threshold=policy["threshold"]
        fixed=None
        if abs(budget-.30)<1e-12:
            mask=scores>=float(threshold) if threshold is not None else np.zeros(n,bool)
            if mask.sum()>k:
                raise ValueError("DEV frozen threshold exceeds budget")
            fixed={"mean_ndcg10":float(base_score+delta[mask].sum()/n),
                   "actual_call_rate":float(mask.mean()),
                   "actual_calls":int(mask.sum()),
                   "threshold":None if threshold is None else float(threshold)}
            if abs(fixed["mean_ndcg10"]-(base_score+policy["dev_oof_gain"]))>1e-8:
                raise ValueError("frozen E2 summary does not match")
        options[method]={"score_ranked_topk_ndcg10":score_top,
                         "note":"posthoc exact-k score ordering; NOT a frozen policy"}
        if fixed is not None:
            options[method]["frozen_dev_30pct_policy"]=fixed
    return {"budget_max_rate":budget,"call_cap":k,
            "oracle_hindsight_at_most_k_ndcg10":base_score+oracle_gain,
            "oracle_hindsight_at_most_k_gain":oracle_gain,
            "oracle_calls":int(min(k,len(best))),
            "random_exact_k_expected_ndcg10":random_expected,
            "random_20_prespecified_draws_ndcg10":{
                 "n_seeds":len(RANDOM_SEEDS),
                 "mean":float(np.mean(repeats)),
                 "min":float(min(repeats)),
                 "max":float(max(repeats))},
            "methods":options}


def run(root:Path,out:Path):
    if out.exists():
        raise FileExistsError("Do not overwrite prior budget diagnostics")
    e2=json.loads((root/"aggregate.json").read_text())
    if (e2.get("schema")!="kbs-plan-c-g3-five-gates-dev-only-v1"
        or e2.get("evaluation_scope")!="DEV_OOF_POLICY_OPTIMIZATION"
        or e2.get("test_file_opened") is not False):
        raise ValueError("Requires frozen source E2 DEV OOF provenance")
    result={"schema":"kbs-plan-c-e2-dev-budget-matched-v1",
            "source_aggregate_sha256":digest(root/"aggregate.json"),
            "budgets":list(BUDGETS),
            "random_seeds":list(RANDOM_SEEDS),
            "family":{},
            "test_data_read":False,"test_metric_computed":False,
            "scope":"DEV_ONLY_DESCRIPTIVE_POSTHOC",
            "interpretation":"Oracle uses realized outcomes and is not deployable. "
                "Score top-k is not the frozen pointwise serving policy. "
                "DEV threshold was selected on OOF DEV labels, so no independent generalization inference."}
    for family in ("sasrec","gru4rec"):
        directory=root/family
        manifest=json.loads((directory/"models"/"oof_manifest.json").read_text())
        frozen=json.loads((directory/"frozen_thresholds.json").read_text())
        file=directory/"models"/"dev_oof.csv"
        if (digest(file)!=manifest["provenance_sha256"]
            or frozen["dev_source_sha256"]!=digest(file)
            or frozen["oof_source_sha256"]!=digest(directory/"models"/"oof_manifest.json")
            or not manifest["predictions_are_oof"] or not manifest["user_disjoint_across_folds"]):
            raise ValueError("OOF prediction / frozen threshold provenance mismatch")
        df=pd.read_csv(file)
        if len(df)!=50049 or not df.split.eq("DEV").all() or df.event_id.duplicated().any():
            raise ValueError("DEV cohort altered")
        curves=[numbers(df,frozen,b) for b in BUDGETS]
        o=curves[BUDGETS.index(.30)]
        baseline=e2["family"][family]["metrics"]
        for method in METHODS:
            observed=o["methods"][method]["frozen_dev_30pct_policy"]["mean_ndcg10"]
            expected=baseline["methods"][method]["dev_oof_mean_ndcg10"]
            if abs(observed-expected)>1e-8:
                raise ValueError("Nonidentical E2 frozen score "+method)
        result["family"][family]={
            "n_events":len(df),
            "baseline_ndcg10":float(df.base_ndcg10.mean()),
            "always_memory_ndcg10":float(df.memory_ndcg10.mean()),
            "budget_curve":curves,
            "at_30pct_oracle_vs_utility_headroom":float(
                 o["oracle_hindsight_at_most_k_ndcg10"]-
                 o["methods"]["utility"]["frozen_dev_30pct_policy"]["mean_ndcg10"]),
            "at_30pct_utility_gain_capture_of_budget_oracle":
                 float((o["methods"]["utility"]["frozen_dev_30pct_policy"]["mean_ndcg10"]-
                    df.base_ndcg10.mean()) /
                    max(o["oracle_hindsight_at_most_k_gain"],1e-12)),
        }
        print(json.dumps({"family":family,"at_30pct":o,
              "captured_budget_oracle":result["family"][family]["at_30pct_utility_gain_capture_of_budget_oracle"]}),
              flush=True)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"stage":"G3_BUDGET_REFERENCE_COMPLETE","test_unopened":True}))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--e2",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    run(a.e2,a.out)
