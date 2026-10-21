#!/usr/bin/env python3
"""PUBLIC ONLY. Exact rank-mixture non-identification under B1-like 574 draws.

This construct is an abstract statistical counterexample, not an inference about
KuaiLive events, neural scores, identities, or a new corrected-S estimator.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb, log2

NEGATIVES = 574
K = 10
RANK_SUPPORT = (1, 3, 10, 11, 22, 40, 80, 100, 150, 200, 300, 1200)
CANDIDATE_SIZES = (14022, 53762)  # Verified range, not exact observed event samples.


def censored_emission_numerators(N: int, R: int, n: int = NEGATIVES) -> tuple[int, ...]:
    """Probabilities for X=0..9 and X>=10, denominator C(N-1,n)."""
    if not (N > n >= K and 1 <= R <= N):
        raise ValueError("invalid N, n, or R")
    denom = comb(N - 1, n)
    exact = tuple(
        comb(R - 1, k) * comb(N - R, n - k)
        if 0 <= k <= R - 1 and n - k <= N - R else 0
        for k in range(K)
    )
    out = exact + (denom - sum(exact),)
    assert len(out) == K + 1 and min(out) >= 0 and sum(out) == denom
    return out


def solve_kernel_vector(columns: list[tuple[int, ...]]) -> list[Fraction]:
    """Find nonzero signed v with sum_j v_j*P(Ys=i|Rj)=0 (exact)."""
    k = len(columns[0])
    if len(columns) != k + 1 or any(len(c) != k for c in columns):
        raise ValueError("require precisely one more rank than observed categories")
    a = [[Fraction(columns[j][i]) for j in range(k)] +
         [Fraction(-columns[k][i])] for i in range(k)]
    for pivot_col in range(k):
        pivot = next((row for row in range(pivot_col, k) if a[row][pivot_col]), None)
        if pivot is None:
            raise ArithmeticError("chosen rank support produces dependent columns")
        a[pivot_col], a[pivot] = a[pivot], a[pivot_col]
        scale = a[pivot_col][pivot_col]
        for c in range(pivot_col, k + 1):
            a[pivot_col][c] /= scale
        for row in range(k):
            if row == pivot_col or a[row][pivot_col] == 0:
                continue
            multiple = a[row][pivot_col]
            for c in range(pivot_col, k + 1):
                a[row][c] -= multiple * a[pivot_col][c]
    v = [a[i][k] for i in range(k)] + [Fraction(1)]
    assert all(sum(v[j] * columns[j][i] for j in range(k + 1)) == 0 for i in range(k))
    return v


def construct_worlds(N: int) -> dict:
    if N < max(RANK_SUPPORT) or N <= NEGATIVES:
        raise ValueError("full roster too small for support")
    ranks = RANK_SUPPORT
    cols = [censored_emission_numerators(N, R) for R in ranks]
    signed = solve_kernel_vector(cols)
    pos = sum((x for x in signed if x > 0), Fraction())
    neg = -sum((x for x in signed if x < 0), Fraction())
    assert pos == neg and pos > 0
    world_p = tuple(max(Fraction(), x) / pos for x in signed)
    world_q = tuple(max(Fraction(), -x) / neg for x in signed)
    assert sum(world_p) == sum(world_q) == 1
    assert all(sum((world_p[j] - world_q[j]) * cols[j][i] for j in range(len(ranks))) == 0
               for i in range(K + 1))
    # B always has full rank N => sampled X_B=574 => Y_B^S=0, full B utility=0.
    # B/M draw the same S negatives, so joint (Y_M^S,Y_B^S) distributions match.
    mean_p = sum(float(world_p[j]) / log2(R + 1) for j, R in enumerate(ranks) if R <= K)
    mean_q = sum(float(world_q[j]) / log2(R + 1) for j, R in enumerate(ranks) if R <= K)
    gap = abs(mean_p - mean_q)
    assert gap > 0.24
    return {
        "N": N, "negative_draws": NEGATIVES, "observed_joint_categories": K + 1,
        "support": list(ranks),
        "world_A": [{"rank": R, "probability": round(float(v), 9)} for R, v
                    in zip(ranks, world_p) if v],
        "world_B": [{"rank": R, "probability": round(float(v), 9)} for R, v
                    in zip(ranks, world_q) if v],
        "max_exact_probability_difference": "0 (verified with Fraction arithmetic)",
        "full_utility_world_A": round(mean_p, 9),
        "full_utility_world_B": round(mean_q, 9),
        "full_utility_absolute_gap": round(gap, 9),
        "matched_50_percent_call_budget_minimax_regret_lower_bound": round(gap / 4, 9),
        "warning": "Synthetic, deliberately unrestricted latent distributions; assumes "
                   "constant Z and B last. No claim that M3 ranks follow these worlds or "
                   "that corrections cannot work under additional assumptions."
    }


def main() -> None:
    print(json.dumps({
        "scope": "PUBLIC_SYNTHETIC_ONLY_NO_PRIVATE_DEV_TEST",
        "method": "EXACT_RATIONAL_NULLSPACE_CONSTRUCTION",
        "worlds": [construct_worlds(N) for N in CANDIDATE_SIZES]
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
