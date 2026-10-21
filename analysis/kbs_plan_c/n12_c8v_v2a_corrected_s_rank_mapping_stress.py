#!/usr/bin/env python3
"""DEV-free correction candidates under original B1 target-retained S sampling.

These are illustrative *candidate estimators*, NOT proven per-event unbiased
NDCG estimators, and not policy experiments. The source sample label scalar
suffices because sampled positive top-K NDCG determines rank, and 0 sampled
top-K NDCG implies true full top-K NDCG=0.
"""
from __future__ import annotations

import json
import math

K = 10
DRAW = 574
N_RANGE = (14022,53762)
RANK_MIXTURES = {
    "synthetic_top_heavy": ((1,.24),(2,.18),(5,.15),(10,.12),(12,.11),(40,.10),(100,.10)),
    "synthetic_tail_heavy": ((1,.01),(2,.02),(5,.02),(10,.03),(12,.07),(40,.20),(100,.25),(1000,.40)),
}

def score(rank:float)->float:
    return 1.0/math.log2(rank+1) if rank <= K else 0.0

def sampled_scalar_from_outrank(x:int)->float:
    return score(x+1)

def decode_observed_sampled_scalar(value:float)->int|None:
    if not math.isfinite(value) or value<0 or value>1.0+1e-12:
        raise ValueError("bad NDCG scalar")
    if abs(value)<1e-15:
        return None   # sampled rank > 10; full rank >= sampled rank, so full utility = 0
    for x in range(K):
        if abs(value - score(x+1)) <= 1e-12:
            return x
    raise ValueError("not an original B1 single-positive NDCG@10 label")

def hypergeom_pmf(n_total:int, rank:int, n_draw:int, outrank:int)->float:
    if n_total < n_draw+1 or not 1<=rank<=n_total:
        raise ValueError("invalid full population or rank")
    x=outrank
    ahead=rank-1
    behind=n_total-rank
    if x<max(0,n_draw-behind) or x>min(n_draw,ahead):
        return 0.0
    # log(C(ahead,x) C(behind,n-x) / C(N-1,n)) to avoid enormous factorials.
    def logc(a,b):
        return math.lgamma(a+1)-math.lgamma(b+1)-math.lgamma(a-b+1)
    return math.exp(logc(ahead,x)+logc(behind,n_draw-x)-logc(n_total-1,n_draw))

def expanded_rank(n_total:int, x:int, n_draw:int=DRAW)->float:
    return 1.0+(n_total-1)*x/n_draw

def corrected_s_rank_expand_from_scalar(s_sample:float,n_total:int)->float:
    if n_total < DRAW+1:
        raise ValueError("candidate_count < sampled size")
    x=decode_observed_sampled_scalar(s_sample)
    if x is None:
        return 0.0
    return score(expanded_rank(n_total,x))

def uniform_prior_posterior_from_scalar(s_sample:float,n_total:int)->float:
    """Exact posterior E[full NDCG@10|sample rank] for prior R~Uniform(1,...,N).

    Marginal Pr(X=x)=1/(n+1) under the stated prior. This prior is NOT
    appropriate by default to model rank distributions in recommender logs.
    It is a sensitivity scenario, not an endorsed production correction.
    """
    if n_total<DRAW+1:
        raise ValueError("candidate_count < sampled size")
    x=decode_observed_sampled_scalar(s_sample)
    if x is None:
        return 0.0
    return (DRAW+1)/n_total * sum(
        score(r)*hypergeom_pmf(n_total,r,DRAW,x) for r in range(1,K+1))

def estimate(x:int,n_total:int,method:str)->float:
    value=sampled_scalar_from_outrank(x)
    if method=="original_s":
        return value
    if method=="rank_expansion":
        return corrected_s_rank_expand_from_scalar(value,n_total)
    if method=="uniform_prior_posterior":
        return uniform_prior_posterior_from_scalar(value,n_total)
    raise ValueError(method)

METHODS=("original_s","rank_expansion","uniform_prior_posterior")

def conditional_quality(n_total:int,full_rank:int)->dict:
    hi=min(DRAW,full_rank-1)
    lo=max(0,DRAW-(n_total-full_rank))
    output={m:{"mean":0.0,"mse":0.0} for m in METHODS}
    true=score(full_rank)
    norm=0.0
    for x in range(lo,hi+1):
        p=hypergeom_pmf(n_total,full_rank,DRAW,x)
        norm+=p
        for m in METHODS:
            v=estimate(x,n_total,m)
            output[m]["mean"] += p*v
            output[m]["mse"] += p*(v-true)**2
    if abs(norm-1)>1e-7:
        raise ArithmeticError(f"kernel not normalized N={n_total}, R={full_rank}: {norm}")
    for m in METHODS:
        output[m]["mean"]/=norm
        output[m]["mse"]/=norm
    return output

def synthetic_mixture(n_total:int,distribution)->dict:
    if abs(sum(w for _,w in distribution)-1.)>1e-12:
        raise ValueError("Synthetic mixture is not normalized")
    out={m:{"bias":0.0,"mse":0.0} for m in METHODS}
    truth=0.
    for rank,w in distribution:
        truth+=w*score(rank)
        q=conditional_quality(n_total,rank)
        for m in METHODS:
            out[m]["bias"]+=w*(q[m]["mean"]-score(rank))
            out[m]["mse"]+=w*q[m]["mse"]
    return {"true_mean":round(truth,6),
            "methods":{m:{k:round(v,6) for k,v in r.items()}
                       for m,r in out.items()}}

def run()->dict:
    return {"schema":"N12_C8V_V2A_CORRECTED_S_PUBLIC_SYNTHETIC_STRESS_V1",
            "source":"B1 original 574-negative uniform without-replacement target-retained S; no raw DEV read",
            "methods":{
                "original_s":"uncorrected sampled NDCG@10",
                "rank_expansion":"CIKM2024-inspired unbiased full rank estimator plugged into truncated NDCG (nonlinear, not unbiased metric)",
                "uniform_prior_posterior":"exact hypergeom Bayes posterior full NDCG under explicit uniform rank prior, not DEV-calibrated"
            },
            "censoring":"sampled_ndcg10=0 -> full_ndcg10=0 necessarily; positive sampled_ndcg10 recovers x=0..9",
            "selection":"fixed two synthetic rank priors, no calibration on original DEV or H1 TEST",
            "experiments":{
                str(n): {key:synthetic_mixture(n,dist) for key,dist in RANK_MIXTURES.items()}
                for n in N_RANGE
            },
            "limitations":"synthetic estimand stress only; rank-unbiased does not imply NDCG-unbiased, joint M/Base shared sample and downstream policy benefit untested; V2b not authorized"}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
