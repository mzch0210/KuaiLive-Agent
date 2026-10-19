#!/usr/bin/env python3
"""DEV-free B1 sampled-rank information audit; not a corrected-S estimator.

Under target-retained uniform n-negative sampling without replacement:
X = sampled target rank - 1 ~ Hypergeom(N-1, R-1, n).
For fixed N and R, all E[g(X)] are polynomials in R of degree <= n.
When N >= n + K + 1, a universally design-unbiased one-sample estimator
of full top-K NDCG from sampled rank alone does not exist: the expectation
would need N-K >= n+1 zeros and a positive value at R=1.
This is a narrow impossibility claim, not a claim against approximate,
distribution-level, conditional or auxiliary-information-based corrections.
"""
from __future__ import annotations
import json
from math import comb, isclose, log2
from typing import Dict

NEGATIVES=574
TOP_K=10

def hypergeom_sample_outrank_pmf(total_candidates:int,full_rank:int,
                                sampled_negatives:int,k:int) -> float:
    n=sampled_negatives
    N=total_candidates
    R=full_rank
    if not (N>=2 and 1<=R<=N and 0<=n<=N-1):
        raise ValueError("invalid full-candidate size, rank or sample size")
    if k<0 or k>min(n,R-1) or n-k>N-R:
        return 0.0
    return comb(R-1,k)*comb(N-R,n-k)/comb(N-1,n)

def full_ndcg(rank:int,at:int=TOP_K)->float:
    return 1/log2(rank+1) if rank<=at else 0.0

def sampled_topk_probability(total_candidates:int,full_rank:int,
                             sampled_negatives:int=NEGATIVES,at:int=TOP_K)->float:
    return sum(hypergeom_sample_outrank_pmf(total_candidates,full_rank,
                    sampled_negatives,k) for k in range(at))

def expected_sampled_ndcg(total_candidates:int,full_rank:int,
                          sampled_negatives:int=NEGATIVES,at:int=TOP_K)->float:
    return sum(full_ndcg(k+1,at)*hypergeom_sample_outrank_pmf(
        total_candidates,full_rank,sampled_negatives,k) for k in range(at))

def no_universal_design_unbiased_from_sampled_rank(total_candidates:int,
                           sampled_negatives:int=NEGATIVES,at:int=TOP_K)->bool:
    """Sufficient impossibility condition, not an equivalence.

    The expectation of any function g(sampled_rank,N) is degree <=n in R;
    top-K full utility vanishes at each R in {K+1,...,N}. When there are
    at least n+1 such distinct roots it cannot also be positive at R=1.
    """
    if total_candidates < sampled_negatives+1:
        raise ValueError("cannot draw more negatives than the full non-target roster")
    return total_candidates-at >= sampled_negatives+1

def summary()->Dict:
    N=1000
    R=12
    return {
        "scope":"PUBLIC_SYNTHETIC_MATH_ONLY_NO_PRIVATE_DEV_OR_TEST",
        "N_synthetic":N,
        "full_rank_synthetic":R,
        "sampled_negatives":NEGATIVES,
        "full_ndcg10":full_ndcg(R),
        "P_sampled_rank_in_top10":sampled_topk_probability(N,R),
        "E_sampled_ndcg10":expected_sampled_ndcg(N,R),
        "threshold_N_for_sufficient_no_universal_unbiased_rank_only_estimator":
            NEGATIVES+TOP_K+1,
        "proof_condition_met_for_N_1000":
            no_universal_design_unbiased_from_sampled_rank(N),
        "warning":"Correction of population metrics or auxiliary-feature conditional estimates may still be useful; this audit did not identify or evaluate a corrected-S method."
    }

if __name__=="__main__":
    print(json.dumps(summary(),indent=2))
