#!/usr/bin/env python3
"""NI-1c public synthetic: sampling reveals a top-10 rank flip iff its lone
distinguishing negative is sampled. No private data, policy fitting, or TEST.

World +: Memory full rank 10, Base full rank 11.
World -: Memory full rank 11, Base full rank 10.
Nine negatives outrank the target for both; one *additional* negative outranks
the target only for the worse expert. Both experts use the SAME n=574 sampled
non-targets. All other candidates rank below the target for both experts.
"""
from __future__ import annotations
from fractions import Fraction
from math import comb, log2
import json

SAMPLED_NEGATIVES = 574
TOP_K = 10
ROSTER_SIZES = (14022, 53762)
SHARED_AHEAD = 9


def full_ndcg(rank: int, k: int = TOP_K) -> float:
    return 1.0 / log2(rank + 1) if rank <= k else 0.0


def model(N: int, n: int = SAMPLED_NEGATIVES, repeats: int = 50) -> dict:
    if not (N >= SHARED_AHEAD + 2 and 1 <= n <= N - 1 and repeats >= 1):
        raise ValueError("invalid candidate, negative-sampling or repeat size")
    # Probability that the unique distinguishing negative enters the shared S.
    detected = Fraction(n, N - 1)
    undetected = 1 - detected
    # Conditional on selecting unique negative, choose n-1 from remaining N-2.
    # Nine common ahead-target candidates occupy a subset of N-2.
    denom = comb(N - 2, n - 1)
    conditional_expected_sampled_gap = 0.0
    pmf_total = Fraction()
    for h in range(SHARED_AHEAD + 1):
        if not (0 <= n - 1 - h <= N - 2 - SHARED_AHEAD):
            continue
        prob = Fraction(
            comb(SHARED_AHEAD, h) * comb(N - 2 - SHARED_AHEAD, n - 1 - h),
            denom,
        )
        pmf_total += prob
        # With unique sampled, better expert sampled rank h+1, worse h+2.
        conditional_expected_sampled_gap += float(prob) * (
            full_ndcg(h + 1) - full_ndcg(h + 2)
        )
    assert pmf_total == 1
    full_gap = full_ndcg(10) - full_ndcg(11)
    expected_sampled_gap = float(detected) * conditional_expected_sampled_gap
    # World +/- have identical mass on sampled-utility diagonal (no unique draw)
    # and *opposite disjoint* signed supports when unique is drawn:
    # exact total variation distance of observed (Y_M^S,Y_B^S) is detected.
    return {
        "N": N,
        "sampled_negatives": n,
        "world_plus_full_delta": full_gap,
        "world_minus_full_delta": -full_gap,
        "full_delta_world_separation": 2 * full_gap,
        "probability_of_observable_sampled_disagreement": float(detected),
        "exact_TV_joint_sample_observations": float(detected),
        "probability_of_sampled_agreement": float(undetected),
        "expected_sampled_delta_in_positive_world": expected_sampled_gap,
        "expected_sampled_delta_in_negative_world": -expected_sampled_gap,
        "probability_no_disagreement_in_independent_repeats": float(undetected ** repeats),
        "repeated_observations": repeats,
        "two_world_equal_prior_minimax_sign_error_lower_bound": float(undetected ** repeats / 2),
        "scope": "STRUCTURED_SYNTHETIC_NOT_ACTUAL_M3; no claims of estimator optimality",
    }


def main() -> None:
    print(json.dumps({
        "explanation": "Top10 vs top11 shared-negative one-candidate difference",
        "source": "B1 574-of-(N-1) target-retained sampling design",
        "cases": [model(N) for N in ROSTER_SIZES],
    }, indent=2))


if __name__ == "__main__":
    main()
