#!/usr/bin/env python3
"""Read-only ORIGINAL 50,049-row B1 DEV label diagnostics for paired corrected-S.

This is a method-diagnostic using already existing F labels for retrospective
evaluation. It is NOT new model training, independent validation, a policy
experiment, nor a corrected-S estimator selected and approved for submission.
No raw event IDs/identifiers/rows are emitted or stored.
"""
from __future__ import annotations
import argparse
import csv
import functools
import hashlib
import json
import math
from pathlib import Path
from n12_c8v_v2a_corrected_s_rank_mapping_stress import (
    corrected_s_rank_expand_from_scalar,
    uniform_prior_posterior_from_scalar,
)
EXPECTED_N=50049
S_SHA="37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea"
F_SHA="e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f"
METHODS=("original_s","rank_expansion","uniform_prior_posterior")
FAMILIES=("sasrec","gru4rec")

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(4<<20),b""):
            h.update(chunk)
    return h.hexdigest()

@functools.lru_cache(maxsize=520000)
def correction(n:int,scalar:float,method:str)->float:
    if method=="original_s":
        return scalar
    if method=="rank_expansion":
        return corrected_s_rank_expand_from_scalar(scalar,n)
    if method=="uniform_prior_posterior":
        return uniform_prior_posterior_from_scalar(scalar,n)
    raise ValueError(method)

def accum():
    return {"n":0,"bias_sum":0.,"square_sum":0.,
            "sum_estimate":0.,"sum_full":0.,
            "positive_full":0,"positive_estimate":0,
            "false_positive_pref":0,"missed_positive_pref":0,
            "toy_allocation_regret_sum":0.,"sign_agreements":0}

def add(stats,truth,estimate):
    stats["n"]+=1
    delta=estimate-truth
    stats["bias_sum"]+=delta
    stats["square_sum"]+=delta*delta
    stats["sum_estimate"]+=estimate
    stats["sum_full"]+=truth
    use_memory=estimate>1e-12
    should_use=truth>1e-12
    stats["positive_full"]+=int(should_use)
    stats["positive_estimate"]+=int(use_memory)
    stats["false_positive_pref"]+=int(use_memory and not should_use)
    stats["missed_positive_pref"]+=int(not use_memory and should_use)
    stats["toy_allocation_regret_sum"]+=max(truth,0.)-(truth if use_memory else 0.)
    stats["sign_agreements"]+=int((estimate>1e-12)==(truth>1e-12))

def final(stats):
    n=stats["n"]
    return {"events":n,
            "joint_delta_bias":round(stats["bias_sum"]/n,9),
            "joint_delta_mse":round(stats["square_sum"]/n,9),
            "mean_estimated_delta":round(stats["sum_estimate"]/n,9),
            "mean_full_delta":round(stats["sum_full"]/n,9),
            "sign_agreement_rate":round(stats["sign_agreements"]/n,7),
            "positive_full_delta_events":stats["positive_full"],
            "estimated_positive_delta_events":stats["positive_estimate"],
            "false_positive_memory_preference_events":stats["false_positive_pref"],
            "missed_positive_memory_preference_events":stats["missed_positive_pref"],
            "toy_sign_gate_regret_mean":round(stats["toy_allocation_regret_sum"]/n,9)}

def audit(root:Path)->dict:
    origin=root/"klm3_b1_full_dev_candidate_labels_seed20261012_v1"
    reference=root/"klm3_g3_dev_fullactive_base_memory_corrected_v1"
    csv_file=origin/"dev_pair_candidate_labels.csv"
    reference_csv=reference/"dev_full_active_pairs.csv"
    sm=json.loads((origin/"summary.json").read_text())
    fm=json.loads((reference/"summary.json").read_text())
    if not (
        sm.get("schema")=="kbs-b1-full-dev-paired-candidate-labels-v1"
        and sm.get("scope")=="DEV_ONLY_POST_G5_EXPLORATORY"
        and sm.get("status")=="PASS"
        and sm.get("test_accessed") is False
        and sm.get("n_dev_events")==EXPECTED_N
        and sm.get("sampled_candidate_count")==575
        and sm.get("private_event_source_csv_sha256")==S_SHA
        and sm.get("corrected_F_source_sha256")==F_SHA
        and fm.get("schema")=="kbs-plan-c-full-active-dev-paired-v2"
        and fm.get("test_file_accessed") is False
        and fm.get("scope")=="DEV_ONLY"
        and fm.get("n_scored")==EXPECTED_N
        and fm.get("event_csv_sha256")==F_SHA
        and digest(csv_file)==S_SHA
        and digest(reference_csv)==F_SHA
    ):
        raise RuntimeError("Original DEV B1/F provenance or frozen SHA mismatch")
    groups={family:{method:accum() for method in METHODS} for family in FAMILIES}
    counts={"events":0,"full_candidate_min":10**9,"full_candidate_max":0,
            "full_candidates_below_585":0,
            "raw_sampled_support_violations":0,
            "all_source_rows_used_without_selection":True}
    with csv_file.open(newline="",encoding="utf-8") as f:
        rdr=csv.DictReader(f)
        needed={"candidate_count","sampled_memory_ndcg10","memory_ndcg10",
                "b1_sampled_candidate_count"} | {
                    key for family in FAMILIES for key in
                    (family+"_ndcg10","sampled_"+family+"_ndcg10")
                }
        if not needed.issubset(set(rdr.fieldnames or ())):
            raise RuntimeError("Required original B1 F/S paired labels missing")
        for row in rdr:
            n=int(row["candidate_count"])
            if not (575<=n<=200000) or int(row["b1_sampled_candidate_count"])!=575:
                raise RuntimeError("Unexpected candidate universe or S sampling")
            counts["events"]+=1
            counts["full_candidate_min"]=min(counts["full_candidate_min"],n)
            counts["full_candidate_max"]=max(counts["full_candidate_max"],n)
            counts["full_candidates_below_585"]+=int(n<585)
            def val(key):
                v=float(row[key])
                if not math.isfinite(v) or not -1e-12<=v<=1+1e-12:
                    raise RuntimeError("DEV rank label outside NDCG range")
                return v
            f_m,s_m=val("memory_ndcg10"),val("sampled_memory_ndcg10")
            # Because S is a subset of F for same frozen ranker, sampled
            # rank <= full rank, so sampled NDCG >= full NDCG.
            counts["raw_sampled_support_violations"]+=int(f_m>s_m+1e-10)
            method_m={method:correction(n,s_m,method) for method in METHODS}
            for family in FAMILIES:
                f_b,s_b=val(family+"_ndcg10"),val("sampled_"+family+"_ndcg10")
                counts["raw_sampled_support_violations"]+=int(f_b>s_b+1e-10)
                truth=f_m-f_b
                for method in METHODS:
                    estimate=method_m[method]-correction(n,s_b,method)
                    add(groups[family][method],truth,estimate)
    if (counts["events"]!=EXPECTED_N or counts["raw_sampled_support_violations"]!=0
        or counts["full_candidates_below_585"]!=0):
        raise RuntimeError("Original full event count, rank monotonicity or N invalid")
    for family in FAMILIES:
        for method in METHODS:
            if groups[family][method]["n"]!=EXPECTED_N:
                raise RuntimeError("Any post-hoc event selection is forbidden")
    return {"schema":"N12_C8V_V2A_EXISTING_DEV_PAIRED_LABEL_DIAGNOSTIC_V1",
            "status":"PASS_EXISTING_DEV_SOURCE_SHA_AND_PAIRED_DELTA_DIAGNOSTIC",
            "scope":"POST_G5_EXISTING_DEV_ONLY_ALL_ROWS_NO_MODEL_FITTING",
            "reference_labels":"archived original B1/F; original sampled candidate set shared by Base and Memory",
            "n_dev_events":counts["events"],
            "full_candidate_min":counts["full_candidate_min"],
            "full_candidate_max":counts["full_candidate_max"],
            "source_sha_verified":True,
            "same_original_source_event_population":True,
            "sampled_full_monotonicity_violations":counts["raw_sampled_support_violations"],
            "methods":list(METHODS),
            "results":{f:{m:final(groups[f][m]) for m in METHODS} for f in FAMILIES},
            "method_assumptions":{
                "rank_expansion":"rank-expectation plug-in, NOT full NDCG/unbiased conditional delta",
                "uniform_prior_posterior":"uniform true full-rank prior, NOT fit to DEV and not necessarily plausible",
                "original_s":"uncorrected historical target-retained sampled label"},
            "test_accessed":False,"new_training":False,"private_rows_exported":False,
            "new_policy_learned":False,"call_budget_established":False,
            "independent_confirmation":False,"v2b_authorized":False,
            "caveat":"All DEV full-F labels are used only for diagnostic evaluation, not to fit a correction or tune a policy. Toy oracle sign decision lacks capacity constraints and does not represent any B1 policy."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    a=parser.parse_args()
    if a.out.exists():
        raise FileExistsError("No overwrite of safe result")
    res=audit(a.root)
    a.out.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n")
    # Only schema and aggregated statistics (no identities/rows).
    print(json.dumps(res,sort_keys=True))
if __name__=="__main__":main()
