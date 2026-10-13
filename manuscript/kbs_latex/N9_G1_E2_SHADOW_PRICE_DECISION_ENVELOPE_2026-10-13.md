# N9-G1 E2 — Specialist-call shadow-price decision envelope

**Status: completed from previously accepted A1 DEV public aggregates; no TEST or new models.** Source: `N9_A1_DECISION_FRONTIER_PUBLIC_AGGREGATE_2026-10-13.json`; exact complete-envelope JSON: `N9_G1_E2_SHADOW_PRICE_ENVELOPE_PUBLIC_AGGREGATE_2026-10-13.json`.

## Estimand and assumptions

For every A1 inner-call maximum (0/10/20/30/50/70/90/100%) plus Always Base and Always Memory, compare `J_lambda=V_F-lambda*q` using **realized outer-call q**, not a nominal 30% rate. Lambda is a *hypothetical* cost in expected NDCG@10 units per specialist invocation, with idealized zero incremental gate overhead; it is not an observed price, energy or latency measure. All estimates use the same original 50,049 M3 DEV author-ranking events (12,628 user clusters) and post-G5 exploratory protocol.

## Exact observed-policy upper envelope

At each positive cost interval, the named policy has the maximum observed estimated net quality among **all** enumerated A1/fixed policies. At interval boundaries policies tie.

### GRU4REC

| Shadow price λ from | λ to | Optimal observed policy | NDCG@10 | Actual Memory calls |
|---:|---:|---|---:|---:|
| 0.000000 | 0.025180 | Always Memory | 0.343509 | 50049 |
| 0.025180 | 0.043465 | max_inner_0.9 | 0.341051 | 45164 |
| 0.043465 | 0.060470 | max_inner_0.7 | 0.332078 | 34831 |
| 0.060470 | 0.083119 | max_inner_0.5 | 0.320478 | 25230 |
| 0.083119 | 0.104379 | max_inner_0.3 | 0.303093 | 14762 |
| 0.104379 | 0.142408 | max_inner_0.2 | 0.292962 | 9904 |
| 0.142408 | 0.200491 | max_inner_0.1 | 0.279025 | 5006 |
| 0.200491 | ∞ | max_inner_0 | 0.258971 | 0 |

The 30% inner-cap policy is optimal globally **only** for λ in [0.083119, 0.104379]. Its break-even shadow prices against Always Memory and Always Base *individually* are 0.057324 and 0.149590, respectively. Intermediate call policies narrow the optimum interval.

### SASREC

| Shadow price λ from | λ to | Optimal observed policy | NDCG@10 | Actual Memory calls |
|---:|---:|---|---:|---:|
| 0.000000 | 0.016315 | Always Memory | 0.343509 | 50049 |
| 0.016315 | 0.023455 | max_inner_1 | 0.343495 | 50006 |
| 0.023455 | 0.042674 | max_inner_0.9 | 0.341040 | 44768 |
| 0.042674 | 0.065931 | max_inner_0.7 | 0.332695 | 34980 |
| 0.065931 | 0.084516 | max_inner_0.5 | 0.319654 | 25081 |
| 0.084516 | 0.111321 | max_inner_0.3 | 0.302658 | 15016 |
| 0.111321 | 0.132766 | max_inner_0.2 | 0.291381 | 9946 |
| 0.132766 | 0.201117 | max_inner_0.1 | 0.278263 | 5001 |
| 0.201117 | ∞ | max_inner_0 | 0.258167 | 0 |

The 30% inner-cap policy is optimal globally **only** for λ in [0.084516, 0.111321]. Its break-even shadow prices against Always Memory and Always Base *individually* are 0.058361 and 0.148289, respectively. Intermediate call policies narrow the optimum interval.

## Scientific verdict and limits

When λ=0, Always Memory remains preferable in both M3 primary Base families. Under the *hypothesized* positive per-call disutility, the net-utility-maximizing observed policy changes along the quality–call-rate frontier; this is the operational condition under which forecasting incremental knowledge value can support allocation choices. The selection gate's complete-path processing burden is omitted and may overturn apparent economic advantage. **Therefore no real-world cost saving is established.**

No interval for estimated shadow-price switching thresholds is reported: the public A1 summaries do not contain the joint per-user covariance or outer policy decision vectors needed for a legitimate paired bootstrap. This calculation is fully identified as **exploratory DEV point-estimate sensitivity**; a private paired bootstrap can be added after verifying cached user-level source integrity, but confidence should not be fabricated from separate arm CIs.

**R2:** decision relevance within a hypothetical constraint is more clearly specified; real scarcity, permissions, production overhead and serving-cost advantage remain unverified. Manuscript edits deferred to G4/G5.
