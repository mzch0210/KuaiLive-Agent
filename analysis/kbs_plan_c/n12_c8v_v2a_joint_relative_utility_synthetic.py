#!/usr/bin/env python3
"""N12 V2a: paired Base/Memory sampled-candidate correction stress, DEV/TEST-free.

One EXACT SAME sampled negative set is shared by Base and Memory per event.
Full rank marginals and the overlap of ahead-of-target negatives fix a
synthetic four-cell joint population. Monte Carlo draws n=574 without
replacement from N-1 negatives, preserving the original B1 sampling law.

Outputs are fixed synthetic per-event relative utility prediction loss,
not a learned policy, a corrected-S empirical DEV experiment or evidence
of a new scientific mechanism.
"""
from __future__ import annotations

import json
import math
import random
import zlib

from n12_c8v_v2a_corrected_s_rank_mapping_stress import (
    DRAW, K, METHODS, N_RANGE, estimate, score
)

REPEATS = 4096
PAIRS = (
    ("memory_best", 11, 1),
    ("base_best", 1, 11),
    ("memory_boundary", 12, 7),
    ("base_boundary", 7, 12),
    ("base_better_top", 2, 8),
    ("memory_better_top", 8, 2),
    ("equal_rank_eight", 8, 8),
    ("both_beyond_top10", 30, 60),
)

def partition_counts(n_total: int, base_rank: int, memory_rank: int,
                     overlap: int) -> tuple[int,int,int,int]:
    a,b=base_rank-1,memory_rank-1
    if n_total < DRAW+1 or not 1<=base_rank<=n_total or not 1<=memory_rank<=n_total:
        raise ValueError("invalid N or full ranks")
    min_overlap=max(0,a+b-(n_total-1))
    max_overlap=min(a,b)
    if not min_overlap<=overlap<=max_overlap:
        raise ValueError("invalid shared ahead-set overlap")
    both=overlap
    base_only=a-overlap
    memory_only=b-overlap
    neither=n_total-1-(both+base_only+memory_only)
    assert min((both,base_only,memory_only,neither))>=0
    return both,base_only,memory_only,neither

def shared_outrank_counts(negatives,parts):
    both,b_only,m_only,_ =parts
    p=both
    q=p+b_only
    r=q+m_only
    b=m=0
    for idx in negatives:
        if idx<p:
            b+=1
            m+=1
        elif idx<q:
            b+=1
        elif idx<r:
            m+=1
    return b,m

def fixed_seed(*items)->int:
    # Same code and fixed public scenarios always regenerate the same draws.
    return zlib.crc32("|".join(map(str,items)).encode("utf-8")) & 0xffffffff

def cache_predictions(n_total:int):
    # x >= 10 -> sampled top-10 utility 0 -> full top-10 utility exactly 0.
    return {method:[estimate(x,n_total,method) for x in range(K)]+[0.0]
            for method in METHODS}

def rank_loss_scenario(n_total:int,base_rank:int,memory_rank:int,
                       overlap:int,repeats:int=REPEATS):
    parts=partition_counts(n_total,base_rank,memory_rank,overlap)
    rng=random.Random(fixed_seed("joint",n_total,base_rank,memory_rank,overlap,repeats))
    pred=cache_predictions(n_total)
    true_delta=score(memory_rank)-score(base_rank)
    metrics={method:{"bias":0.0,"mse":0.0,"false_memory_calls":0,
                     "lost_positive_calls":0,"toy_allocation_regret":0.0,
                     "memory_call_rate":0.0} for method in METHODS}
    covar={"error_base_mean":0., "error_memory_mean":0.,
           "error_base_memory_raw_cross":0.}
    # Marginal error covariance is calculated for raw sampled NDCG.
    for _ in range(repeats):
        draw=rng.sample(range(n_total-1),DRAW)
        xb,xm=shared_outrank_counts(draw,parts)
        # Off-top10 ranks only store the censored zero value.
        xb=min(K,xb)
        xm=min(K,xm)
        raw_b=pred["original_s"][xb]
        raw_m=pred["original_s"][xm]
        err_b=raw_b-score(base_rank)
        err_m=raw_m-score(memory_rank)
        covar["error_base_mean"]+=err_b
        covar["error_memory_mean"]+=err_m
        covar["error_base_memory_raw_cross"]+=err_b*err_m
        for method,vals in metrics.items():
            dhat=pred[method][xm]-pred[method][xb]
            err=dhat-true_delta
            vals["bias"]+=err
            vals["mse"]+=err*err
            # Toy oracle threshold: choose Memory iff predicted delta >0.
            # This is not a learned/deployable gate or quota comparison.
            call=dhat>1e-12
            vals["memory_call_rate"]+=int(call)
            vals["false_memory_calls"]+=int(call and true_delta<=0)
            vals["lost_positive_calls"]+=int(not call and true_delta>0)
            vals["toy_allocation_regret"]+=max(0.0,true_delta)-(true_delta if call else 0.)
    for vals in metrics.values():
        for key in vals:
            vals[key]=round(vals[key]/repeats,7)
    eb=covar["error_base_mean"]/repeats
    em=covar["error_memory_mean"]/repeats
    joint_cov=covar["error_base_memory_raw_cross"]/repeats-eb*em
    return {
        "N":n_total,"base_full_rank":base_rank,"memory_full_rank":memory_rank,
        "ahead_overlap":overlap,"joint_population_counts":list(parts),
        "true_delta_full_ndcg10":round(true_delta,7),
        "draws":repeats,
        "marginal_raw_error_covariance":round(joint_cov,7),
        "methods":metrics
    }

def independent_vs_shared_negative_control(n_total:int=14022,repeats:int=4096):
    # Base rank=2 (1 ahead), Memory rank=8 (7 ahead). Nested ahead sets.
    # Under SAME negatives, xm>=xb deterministically; sampled Memory utility
    # can never *exceed* sampled Base utility.
    ranks=(2,8)
    parts=partition_counts(n_total,*ranks,overlap=1)
    rng=random.Random(fixed_seed("negative_control",n_total,repeats))
    wrong_shared=wrong_independent=0
    nonzero_shared=nonzero_independent=0
    for _ in range(repeats):
        draw=rng.sample(range(n_total-1),DRAW)
        xb,xm=shared_outrank_counts(draw,parts)
        if xm<xb:
            raise AssertionError("Same-negative nested ranks reversed")
        ds=score(xm+1)-score(xb+1)
        wrong_shared+=int(ds>1e-12)
        nonzero_shared+=int(abs(ds)>1e-12)
        # Negative control ONLY: independent candidate samples for each scorer.
        # This is not what the real B1 protocol does.
        xb_ind,_=shared_outrank_counts(rng.sample(range(n_total-1),DRAW),parts)
        _,xm_ind=shared_outrank_counts(rng.sample(range(n_total-1),DRAW),parts)
        di=score(xm_ind+1)-score(xb_ind+1)
        wrong_independent+=int(di>1e-12)
        nonzero_independent+=int(abs(di)>1e-12)
    return {
        "N":n_total,"full_ranks_base_memory":list(ranks),"ahead_overlap":1,
        "synthetic_draws":repeats,
        "shared_false_memory_preference":wrong_shared,
        "independent_false_memory_preference":wrong_independent,
        "shared_nonzero_label_count":nonzero_shared,
        "independent_nonzero_label_count":nonzero_independent,
        "note":"The independent-sample arm violates the B1 actual shared-negative design and is a negative control, not a recommended estimator."
    }

def run():
    records=[]
    for n_total in N_RANGE:
        for name,b,m in PAIRS:
            low=max(0,b+m-2-(n_total-1))
            high=min(b-1,m-1)
            for overlap_tag,overlap in (("minimal",low),("nested",high)):
                r=rank_loss_scenario(n_total,b,m,overlap)
                r["scenario"]=name
                r["overlap_construction"]=overlap_tag
                records.append(r)
    negative=independent_vs_shared_negative_control()
    summary={}
    for method in METHODS:
        summary[method]={
            metric:round(sum(r["methods"][method][metric] for r in records)/len(records),7)
            for metric in ("bias","mse","toy_allocation_regret","memory_call_rate",
                           "false_memory_calls","lost_positive_calls")
        }
    # Pre-specified uniformly weighted synthetic scenario mean is NOT a DEV outcome.
    return {
        "schema":"N12_C8V_V2A_SHARED_NEGATIVE_JOINT_DELTA_SYNTHETIC_v1",
        "scope":"PUBLIC_SYNTHETIC_NO_DEV_OR_TEST_NO_FITTING",
        "source":"B1 target-retained uniform 574 negatives without replacement; exactly shared draw per Base/Memory pair",
        "N_values":list(N_RANGE),"sampled_negatives":DRAW,
        "draws_per_scenario":REPEATS,"scenario_count":len(records),
        "methods":list(METHODS),
        "summary_equal_synthetic_scenario_weight":summary,
        "wrong_independent_sampling_negative_control":negative,
        "scenarios":records,
        "limitations":"toy oracle delta>0 decision, not a trained policy; no DEV rank prior estimated; cannot establish corrected-S policy superiority, V2b remains not authorized"
    }

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
