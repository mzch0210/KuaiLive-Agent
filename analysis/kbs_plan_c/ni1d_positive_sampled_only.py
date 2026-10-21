#!/usr/bin/env python3
"""DEV-/TEST-free synthetic positive control for corrected sampled labels.

Under known *synthetic* rank support, each feature group contains two latent
states: (R_M,R_B)=(10,11) or (11,10). Both rankers share nine better
negatives; the worse ranker has one extra better negative. The SAME 574
negative candidates are sampled for Base and Memory.

This model is NOT validated for M3. Estimator learns mixing weights from
sampled S labels and known roster N only; full ranks are not training inputs.
"""
from __future__ import annotations
from fractions import Fraction
from math import comb, log2
import random
import json

N_SMALL, N_LARGE = 14022, 53762
DRAW = 574
K = 10
PI = (0.65, 0.85)
N_LIST = (N_SMALL, N_LARGE)
FULL_GAP = 1 / log2(11)


def u(rank: int) -> float:
    return 1 / log2(rank + 1) if rank <= K else 0.0


def conditional_common_ahead_probabilities(N: int, common_ahead: int = 9) -> list[float]:
    """H | special sampled ~ Hypergeom(N-2, common_ahead, DRAW-1)."""
    if N <= DRAW + 1 or not 0 <= common_ahead <= N - 2:
        raise ValueError("invalid candidate/structural parameters")
    denom = comb(N - 2, DRAW - 1)
    masses = [
        float(Fraction(comb(common_ahead, h) *
                       comb(N - 2 - common_ahead, DRAW - 1 - h), denom))
        if 0 <= DRAW - 1 - h <= N - 2 - common_ahead else 0.0
        for h in range(common_ahead + 1)
    ]
    assert abs(sum(masses) - 1) < 1e-12
    return masses


def mean_gap_if_detected(N: int, common_ahead: int = 9) -> float:
    return sum(w * (u(h + 1) - u(h + 2))
               for h, w in enumerate(conditional_common_ahead_probabilities(N, common_ahead)))


def analytic_raw_sampled_mean(N: int, pi: float, common_ahead: int = 9) -> float:
    return (2 * pi - 1) * (DRAW / (N - 1)) * mean_gap_if_detected(N, common_ahead)


def synthetic_training(N: int, pi: float, events: int, seed: int) -> dict:
    if not 0 <= pi <= 1 or events < 1 or N <= DRAW + 1:
        raise ValueError("invalid training parameters")
    r = random.Random(seed)
    pdet = DRAW / (N - 1)
    cdf = []
    acc = 0.0
    for w in conditional_common_ahead_probabilities(N):
        acc += w
        cdf.append(acc)
    positive = negative = 0
    raw = 0.0
    for _ in range(events):
        latent = 1 if r.random() < pi else -1  # generator only, NOT a predictor input
        if r.random() >= pdet:
            continue  # sampled paired NDCG equal; cannot determine latent sign
        positive += latent == 1
        negative += latent == -1
        roll = r.random()
        h = next(i for i, c in enumerate(cdf) if roll < c)
        raw += latent * (u(h + 1) - u(h + 2))
    detected = positive + negative
    # Known rank-10/11 support permits this S-only conditional MLE.
    corrected = (positive - negative) / detected * FULL_GAP if detected else 0.0
    return {
        "N": N, "n": events, "detected": detected,
        "positive_detected": positive, "negative_detected": negative,
        "raw_sample_mean": raw / events,
        "corrected_full_mean": corrected,
        "latent_pi_estimate": positive / detected if detected else None,
    }


def decisions(seed: int = 20261020, events: int = 50000,
              numbers: tuple[int, int] = N_LIST,
              probabilities: tuple[float, float] = PI) -> dict:
    if len(numbers) != 2 or len(probabilities) != 2:
        raise ValueError("exactly two groups")
    groups = [
        synthetic_training(N, pi, events, seed + 17 * i)
        for i, (N, pi) in enumerate(zip(numbers, probabilities))
    ]
    best_raw = max(range(2), key=lambda i: groups[i]["raw_sample_mean"])
    best_corrected = max(range(2), key=lambda i: groups[i]["corrected_full_mean"])
    true_vals = [(2 * pi - 1) * FULL_GAP for pi in probabilities]
    best_true = max(range(2), key=lambda i: true_vals[i])
    policies = {}
    for name, which in (("raw_s", best_raw), ("corrected_s", best_corrected),
                        ("full_oracle", best_true)):
        policies[name] = {
            "selected_group_index": which, "calls_per_2events": 1,
            "population_full_delta_gain": true_vals[which] / 2,
            "regret_vs_full_oracle": (true_vals[best_true] - true_vals[which]) / 2,
        }
    return {
        "training_samples_per_group": events, "seed": seed,
        "group_0": groups[0], "group_1": groups[1],
        "true_conditional_full_value": true_vals, "policies": policies,
    }


def run_experiment(replicates: int = 12, events: int = 50000) -> dict:
    runs = [decisions(seed=20261020 + i, events=events)
            for i in range(replicates)]
    counts = {
        name: sum(r["policies"][name]["selected_group_index"] == 1 for r in runs)
        for name in ("raw_s", "corrected_s", "full_oracle")
    }
    true_vals = [(2 * pi - 1) * FULL_GAP for pi in PI]
    return {
        "scope": "PUBLIC_SYNTHETIC_STRONGLY_ASSUMED_LATENT_10_11_RANKS_ONLY",
        "assumption": "Known full rank pair 10/11; unknown mixture probability",
        "pi_generator_only": PI, "N_groups": N_LIST,
        "analytic_raw_sampled_group_values": [
            analytic_raw_sampled_mean(N, pi) for N, pi in zip(N_LIST, PI)
        ],
        "analytic_full_conditional_value": true_vals,
        "ideal_fixed_50pct_call_budget_gap_if_wrong": (true_vals[1] - true_vals[0]) / 2,
        "simulation_replicates": replicates, "train_rows_per_group": events,
        "times_chose_true_best_group": counts,
        "example_first_rep": runs[0],
        "equal_N_negative_control_raw_ranks_correctly": (
            analytic_raw_sampled_mean(N_SMALL, PI[1]) >
            analytic_raw_sampled_mean(N_SMALL, PI[0])
        ),
        "misspecification_true_full_gap_rank9_vs10": u(9) - u(10),
        "incorrect_assumed_full_gap_rank10_vs11": FULL_GAP,
        "misspecification_magnitude_factor": FULL_GAP / (u(9) - u(10)),
        "interpretation": "Not an M3 estimator or a novelty claim; no private DEV/TEST.",
    }


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, ensure_ascii=False))
