# N9 Route B — B1 audit report: zero top-10 support, candidate valuation and decision comparability

**2026-10-14 | B0 SHA/protocol PASS; B1A private source and user-bootstrap PASS; B1B public frozen aggregate audit PASS.** Author manuscript and S1–S10 remain unchanged. No original G5 TEST read or model retrained. This is a post-G5, **same-cohort exploratory DEV** audit, not a new prospective confirmation.

## B1A. Explicit nine-cell decomposition of fixed source×candidate valuation

Using the same 50,049 KuaiLive-M3 author-ranking DEV events / 12,628 users, frozen Full and Long-only fixed Memory sources, define `dF=u10(Full,F)-u10(Long,F)` and `dS=u10(Full,S)-u10(Long,S)`. Each event has one F sign and one S sign in {negative,zero,positive}, yielding nine mutually exhaustive cells.

The exact mean interaction is **+0.115381867910**, and the user-cluster 2,000-draw descriptive 95% interval (seed 20261014) is **[0.111573, 0.119111]**. It reproduces prior E3a aggregate +0.115382 and its source sign diagnostics. All nine signed contributions below are normalized by *all 50,049 events*, not conditional event-group means.

**Table B1.1. Contribution of exact utility sign status to the overall Full-minus-Long F-versus-S gap.**

| Sign dF | Sign dS | Events | Signed contribution to global interaction | 95% user-cluster CI |
|---|---|---:|---:|---|
| − | − | 1,927 | +0.010020 | [0.009324, 0.010737] |
| − | 0 | 10,542 | -0.050444 | [-0.051642, -0.049229] |
| − | + | 25 | -0.000248 | [-0.000351, -0.000152] |
| 0 | − | 8,524 | +0.104801 | [0.101638, 0.107850] |
| 0 | 0 | 18,728 | +0.000000 | [0.000000, 0.000000] |
| 0 | + | 1,101 | -0.009706 | [-0.010380, -0.009076] |
| + | − | 41 | +0.000457 | [0.000317, 0.000610] |
| + | 0 | 7,567 | +0.056234 | [0.054742, 0.057755] |
| + | + | 1,594 | +0.004268 | [0.003789, 0.004750] |

**Partition accounting:**
- **At least one source difference exactly zero:** 46462 events (92.83%), signed contribution **+0.100885**, or **87.44% of the net signed mean**. This is a net accounting share that can be altered by cancellation, not a fraction of all absolute effects.
- Both source differences nonzero: 3587 events, signed contribution **+0.014497** (net share 12.56%).
- Both exactly zero: 18728 events; only F zero: 9625; only S zero: 18109. **Only 66 events** have strictly opposite *nonzero* source-gap signs; their signed contribution is **+0.000209**, merely 0.182% of the net effect.
- Major countervailing terms: `F=0,S=negative` contributes +0.104801 and `F=positive,S=0` +0.056234, whereas `F=negative,S=0` contributes −0.050444. The observed net value depends on **zero-support transitions and signed cancellation**, not on widespread strict real source ordering reversal.

**Scientific interpretation:** The strong aggregate fixed-source×candidate interaction is statistically well-supported *within the explored DEV cohort*, but its net estimate is concentrated in whether a source gap is nonzero under one top-10 candidate regime. Such threshold/support behavior is consistent with known sampled-ranking metric incongruence; it does **not** identify a distinctive causal viewer–creator identity effect. Distinguish the *empirical transport of candidate metrics into source valuation and decisions* from claims about novel sampling theory. Reference: Krichene & Rendle, KDD 2020 (https://research.google/pubs/on-sampled-metrics-for-item-recommendation/).

## B1B. Decision comparability and information-entitlement audit

**GRU4REC:** S→F / F→F calls 15001/14762 (F−S -239; absolute difference 0.478 percentage points). Policy disagreement 23.01% (11517 events), and net F NDCG gain +0.004970 with paired user 95% CI [0.003550, 0.006369]. The F-only mean utility 0.126600 exceeds the S-only 0.079135; both are positive. An **illustrative only** one-action-per-net-imbalanced-call bound is 0.004775 (assuming |event Δ|≤1); this is not a valid equal-budget causal estimate because  11517 decisions changed identities and outer-test matching is not deployable. The prior shadow-price window is [0.083119, 0.104379] in hypothetical NDCG-equivalent call-cost units with gate overhead omitted.

**SASREC:** S→F / F→F calls 14988/15016 (F−S +28; absolute difference 0.056 percentage points). Policy disagreement 21.32% (10672 events), and net F NDCG gain +0.006159 with paired user 95% CI [0.004835, 0.007543]. The F-only mean utility 0.133417 exceeds the S-only 0.076194; both are positive. An **illustrative only** one-action-per-net-imbalanced-call bound is 0.000559 (assuming |event Δ|≤1); this is not a valid equal-budget causal estimate because  10672 decisions changed identities and outer-test matching is not deployable. The prior shadow-price window is [0.084516, 0.111321] in hypothetical NDCG-equivalent call-cost units with gate overhead omitted.


**Crucial distinction:** the observed 21–23% request reallocation is a robust descriptive policy difference after exact B1 refit parity. There are >10,000 bidirectional action changes, not merely the 28/239 *net* invocation differences. A bound based only on changing the net number of calls cannot formally prove the gain persists under a randomized equal-budget intervention, because which events are selected is the scientific quantity. Exact outer-observed call-count matching would use evaluation-sample information and is not a deployable original policy. Only inner-defined constrained rules can support a fair prospective-like sensitivity evaluation.

S→F trained with sampled *target-retained offline labels*; F→F trained with full-active labels. Adapted→F also uses full-active training labels. The Direct-versus-Two-stage controls compare different prediction estimators/head counts, not proof of new routing theory. The original nested 5×4 user-disjoint folds remain **same DEV**, not new chronological TEST. No valid sampled-only corrected top-10 estimator or per-candidate score parity has been identified; **Corrected-S remains HOLD**.

For E2, the shadow-price upper envelope is explicitly an **idealized linear value model**; actual specialist access cost, full gate-path latency and bootstrap switching-boundary uncertainty are unverified. Always Memory remains better in M3 when no incremental call cost is assumed.

## Consequences for Route B and manuscript editing

- **R1** more interpretable, **not solved**: explicit B1A reveals a quantitatively dominant zero/support component already anticipated by sampled-ranking results. Article should not claim a fundamentally new metric-related effect. The new scientific focus should be the **downstream request-level decision consequence under fixed specialist and decision information**.
- **R2** remains conditional and bounded: comparable total calls do not constitute strict equal-budget identification; any cost premise stays hypothetical. An inner-defined common-budget sensitivity is possible, not yet performed.
- **R3** requires a stronger historical relation identity comparator: B1A does not identify viewer–creator semantics. The prior 128-event co-active null is only a nonfloor pilot; conditional medium B2 must preserve causal time and author activity before making a stronger identity claim.
- **B2 eligibility:** continue with *metadata/algorithm/rights* review. Do not begin medium private-edge processing until temporal validity, prechosen sample, original-score parity, compute budget and author-approved data rights gates PASS. The B0 contract freezes 1,024 initial events, 2,048 ceiling and three null seeds. No TEST reopening, no opportunistic repeated placebo runs.
- **Manuscript:** do not change `main.tex`/S10 until B3 scientific verdict. If B2 is null/invalid, retain R1/R3 bounded conclusion and do not search for an algorithmic rescue.

## Reproducibility and provenance
B1A CI and cells: `experiments/kbs_plan_c/N9_B1A_NINE_CELL_SOURCE_CANDIDATE_PUBLIC_AGGREGATE_2026-10-14.json`, [GitHub Actions #38498422665](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38498422665), frozen implementation `analysis/kbs_plan_c/n9_route_b_b1_zero_mass_contributions_dev.py`. B1B source `experiments/kbs_plan_c/N9_B1B_DECISION_CALL_FAIRNESS_AUDIT_PUBLIC_2026-10-14.json`. Research freeze `N9_B0_ROUTE_B_PROTOCOL_FREEZE_2026-10-14.md`. Original TEST and private event/user IDs remain unchanged/unexported.

**B1 result: PASS for rigorous exploratory scientific audit, not a finding that all three KBS research risks have been resolved.**
