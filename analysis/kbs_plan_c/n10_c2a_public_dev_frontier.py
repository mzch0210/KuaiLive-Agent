#!/usr/bin/env python3
"""N10 C2-A: public frozen DEV quality-vs-observed-Memory-call frontier only.

This audit does not load any event/author row, private metrics, model, or TEST label.
It is not a new matched-budget policy fit, and its idealized lambda is NOT ms or $.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
SOURCE="experiments/kbs_plan_c/N9_G1_E2_SHADOW_PRICE_ENVELOPE_PUBLIC_AGGREGATE_2026-10-13.json"
SOURCE_BLOB="047411dfd4b6554e0601c60bf5787dac249da7c3"

def sha(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def require(v,msg):
    if not v:raise AssertionError("C2-A public DEV: "+msg)

def calc(root):
    path=root/SOURCE
    require(sha(path)==SOURCE_BLOB,"DEV frozen source aggregate changed")
    data=json.loads(path.read_text())
    require(data["cohort_events"]==50049 and data["cohort_users"]==12628,
            "DEV cohort size mismatch")
    ass=data["assumptions"]
    require(ass["G5_TEST_accessed"] is False and ass["gate_overhead"]=="idealized zero",
            "public-only zero-overhead assumption")
    require("NDCG" in ass["lambda_unit"] and "not currency or ms" in ass["lambda_unit"],
            "lambda unit is not ms/currency")
    result={}
    for family in ("sasrec","gru4rec"):
        policies=data["families"][family]["all_policies"]
        assert len(policies)>=9
        for x in policies:
            require(0<=x["q"]<=1 and 0<=x["V"]<=1,"policy fractions or outcomes")
            require(x["calls"]>=0 and abs(x["q"]-x["calls"]/50049)<1e-12,
                    "observed q != calls/DEV count")
        by_name={v["policy"]:v for v in policies}
        always_base=by_name["Always Base"];always_mem=by_name["Always Memory"]
        min30=by_name["max_inner_0.3"]
        require(always_mem["q"]==1. and always_base["q"]==0.,"full endpoint calls")
        require(min30["V"]<always_mem["V"],"Memory quality counterexample missing")
        require(min30["q"]>0 and min30["q"]<1,"bounded calls missing")
        # Pairwise Pareto over archived policy endpoints, without refitting/selecting TEST.
        nondom=[]
        for x in policies:
            if not any(
                    y["q"]<=x["q"]+1e-12 and y["V"]>=x["V"]-1e-12
                    and (y["q"]<x["q"]-1e-12 or y["V"]>x["V"]+1e-12)
                    for y in policies):
                nondom.append({"policy":x["policy"],
                    "calls":int(x["calls"]),"q":round(x["q"],9),
                    "full_F_DEV_ndcg":round(x["V"],9)})
        estimate= (always_mem["V"]-min30["V"])/(1-min30["q"])
        old=data["families"][family]["break_even_30_vs_always_memory"]
        require(abs(estimate-old)<1e-10,"published symbolic shadow price breakpoint drift")
        result[family]={"always_memory_DEV_F_NDCG":always_mem["V"],
          "fixed_30_inner_DEV_F_NDCG":min30["V"],
          "30_inner_actual_calls":min30["calls"],
          "30_inner_actual_q":min30["q"],
          "full_memory_minus_30_quality":always_mem["V"]-min30["V"],
          "break_even_lambda_ndcg_per_memory_call":old,
          "quality_vs_calls_pareto_archived_policies":nondom}
    return {"status":"C2A_PUBLIC_DEV_FRONTIER_READ_ONLY_PASS",
      "input_public_blob":SOURCE_BLOB,"n_DEV":50049,"n_users":12628,
      "inference_scope":"post_G5_DEV_exploratory_archived_policy_comparison",
      "no_new_model_or_thresholds":True,
      "new_TEST_event_or_author_labels_read":False,
      "B4A_reopened":False,
      "production_latency_or_cost_measured":False,
      "shadow_price_unit":"hypothetical_NDCG_per_memory_call_not_ms_or_currency",
      "gate_overhead_assumed_zero_in_source":True,
      "families":result}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    a=p.parse_args()
    print(json.dumps(calc(a.repo_root),indent=2,sort_keys=True))
