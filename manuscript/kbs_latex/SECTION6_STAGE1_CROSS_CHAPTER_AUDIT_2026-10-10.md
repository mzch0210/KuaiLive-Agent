# KBS Section 6 — Stage 1 cross-chapter evidence and inference audit

**Date:** 2026-10-10  
**Scientific authority:** The approved C1–C3 novelty definition in the [submission-oriented outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md).  
**Canonical manuscript:** [main.tex](main.tex), Sections 3–6.  
**Machine-readable register:** [19-record claim-to-experiment CSV](SECTION6_STAGE1_CLAIM_EVIDENCE_LEDGER_2026-10-10.csv).  
**Status:** Stage-1 core claim and protocol audit executed. Complete archived SHA coverage and final S1–S9 publication packaging remain open. No training, extra TEST evaluation, threshold reselection or frozen model modification occurred.

## 1. Sources directly inspected

The primary Twitch [one-shot frozen TEST run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), job 106686133973, artifact 10684864297, was checked by opening the final report, TEST export summary and policy manifest. It reports n=44,221 and contains the actual fixed threshold, decisions, bootstrap confidence intervals and retrospective state results.

The Twitch [DEV strengthening run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), job 106700833375, artifact 10688746451, was checked by opening the actual three-row feature-family results, 20-row Memory-component results, JSON and accompanying hashes. Each analysis uses n=46,878 development events. The feature family compares 6, 8 and 14 predictors at the original combined-model-derived common 6,563-call operating count. The historical Memory component analysis reconstructs the fixed Full Memory ranking.

The KuaiLive [fixed-checkpoint P0/P1 factorial run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645), job 113226680691, artifact 11538678848, was checked by opening all three per-seed factorial JSON reports. Each contains n=10,222, room alpha 0.125, model SHA256s, matched TRAIN/DEV/TEST input SHA256s and verification guards, all reported TRUE: one target per user, sampled candidates nested within full, same raw Base scores, fixed alpha, exact factorial allocation, and group-weighted consistency. Three models on the same 10,222 users do NOT constitute independent dataset replication.

Historical KuaiLive native-policy evidence was directly inspected in [sampled-active run 35579466898](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35579466898), artifact 10629373430, and [full-active run 35581670479](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35581670479), artifact 10630557565. These are separately developed native policy protocols, NOT a single fixed-checkpoint paired comparison.

The KuaiLive alternative-gate [run 35571827672](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35571827672), artifacts 10626083783 and 10626432663, was checked through its accuracy report, actual three-replica latency aggregation, and environment records. The [formal efficiency run 35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758), artifact 10694941935, was checked through its complexity and footprint summary. The benchmark uses frozen route-mask replay even while timing actual gate inference.

Context-length, Memory sensitivity, recency and comparator-benchmark source logs and artifact existence were checked against the specialized [6.4 provenance](SECTION6_4_RESULTS_PROVENANCE_2026-10-09.md); not every archived per-user file and model byte was independently rehashed in this stage. Rows in the CSV distinguish direct primary-file verification from source-record-only verification.

## 2. Protocol disambiguation: results that must not be combined

| Provenance object | Reported Base NDCG@10 | Memory or strategy result | Identity and scientific role |
|---|---:|---|---|
| KuaiLive historical native sampled-active 575 | **0.6078439043** | Memory 0.5658874643, Utility HGB 0.6210175172 at 14.25% Memory calls | Native Dual-ID room/streamer fusion **0.1/0.9**, historical policy. |
| KuaiLive separate strong-Base benchmark | **0.6171415058** | Streamer-only 0.6099278 | Separate benchmark checkpoint and training/evaluation provenance. Not P0 Base. |
| KuaiLive exact paired 20260918 sampled SS | **0.60709** (manuscript rounded) | Memory 0.56589; relative utility **−0.04120411** | Paired checkpoint Room/Streamer scores, **0.125/0.875**, 575 sampled-active rooms. |
| Same paired checkpoint full FF | **0.38571** (manuscript rounded) | Memory 0.43202; relative utility **+0.04630669** | Same matched events and models as the preceding SS record; full candidates. |
| KuaiLive historical native full-active | **0.3983528756** | Memory 0.4320191095, native Utility 0.4518011415 at 64.44% Memory calls | Separately trained/developed native full-active base and policy; not the same P0 checkpoint. |

The common n=10,222 or a similar Memory mean does not establish Base checkpoint equivalence. The exact **within-event** Section 6.3 conclusion belongs exclusively to the fixed 20260918 seed (and matched seed-replication protocol), NOT to differences between native separately trained policy reports.

P0 base model SHA256 values (verified from original source JSON):

- Room: b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7
- Streamer: 82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945

P0/P1 exact shared data SHA256 across three model seeds:

- TRAIN: ad91413537175b9f6e9013c525a552b6004cc00e029b41360f08519e0735b5b4
- DEV: 46dd3081688468c89acf6366d36d87c122fa45850ddb69320c05da9de94a9f54
- TEST: 3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956

Seed 20260919 model SHA256s and seed 20260920 model SHA256s are stored individually in the claim ledger and original factorial reports.

The P0 original 2x2 mean utilities are SS −0.0412041108, SF −0.0414176046, FS +0.0476108486 and FF +0.0463066865. The same-user shift +0.0875107973 equals the descriptive membership allocation +0.0882696253 plus the normalization allocation −0.0007588280. This is a scoring-protocol allocation, NOT an isolated causal manipulation of candidate count, difficulty or user preference.

Across all three model seeds, the same retrospective-state counts are represented 4,589, recoverable 206, unavailable 5,427. The small recoverable state's contribution to the KuaiLive regime shift is negative. Do not impose a Twitch recoverable-history explanation on the KuaiLive candidate reversal.

## 3. Statistical and information-boundary checks

| Section / claim | Decision | Essential boundary checked |
|---|---|---|
| Section 3: marginal utility and the selector's information set | **PASS** | Observed target, realized ranks, realized utility and retrospective evidence states are OFFLINE labels/analyses, not pre-outcome gate features. |
| Sections 4–5: distinct Base models and frozen Memory rule | **PASS** | Same specialist coefficients; Room/Streamer Base architecture on KuaiLive versus LiveRec L16 on Twitch. Fusion weights and checkpoints are protocol-specific, NOT globally fixed across all studies. |
| Section 6.1: negative aggregate and positive recoverable group | **PASS** | Twitch TEST 44,221 events, observed-target state assignment, 5,000 paired one-event-per-user bootstrap replicates; DEV/TEST are windows of one platform, not two independent datasets. |
| Section 6.2: prospective Utility and matched-count Difficulty | **PASS** | Utility uses DEV-frozen pointwise rule with realized 6,650 calls; Difficulty retrospectively ranks entire TEST batch to select equal count. Equality of count is NOT equality of online budget behavior. |
| Section 6.2: Oracle and predictive limits | **PASS** | Oracle selects top 6,650 realized relative utilities for the SAME two rankings; no unrestricted optimum. Spearman approx 0.173 and only ~11.7% hindsight Oracle gain captured constrain claims. |
| Section 6.3: 2x2 candidate/reference and 3 seeds | **PASS** | Same raw scores, same users and eligible histories under sampled/full; paired bootstrap 3,000 within seed, across-seed SD separate; not causal attribution or TEST-confirmed transfer. |
| Section 6.4: feature-family comparison | **PASS** | Twitch DEV-only 46,878, common K 6,563 inherited from combined model; OOF bootstrap conditions on trained predictors/budget and no multiple-testing adjustment; not across-budget superiority. |
| Section 6.4: context length and recency | **PASS WITH LIMITS** | L8/L16/L32 Bases are independently retrained; invariant canonical Memory; target-relative selected group changes are not pure history-visibility intervention. Recency profile is nonmonotonic. |
| Section 5.5 vs Section 6.5: HGB parameter | **TECHNICAL WORDING CORRECTED** | max_iter=200 is a configured ceiling; 81 is the actual fitted tree/iteration count in a distinct auxiliary KuaiLive timing estimator. §5.5 now says *maximum* 200 iterations. |
| Section 6.5: cost vs call frequency | **PASS** | Twitch 15.04% calls are not measured Twitch latency. Separate warmed KuaiLive CPU benchmark at 14.25% HGB calls has Base 0.99058 ms and selective 2.00662 ms; no claimed speedup, production SLA, online latency or causal business lift. |
| Baseline competitiveness | **LIMITED / NOT A SOTA CLAIM** | The actual auxiliary alternative-model grids are constrained (Twitch small models trained for five epochs). Fixed platform-incumbent Base remains the object of relative valuation, not a universally best ranking model. |

No edits were warranted in Section 6.1–6.5 text at this stage; the existing individually reviewer-tightened Results passages make the essential inference boundaries explicit. Their **cross-section** integration and display tightening are a later scoped editorial pass after evidence reconciliation.

## 4. Edits performed and boundaries retained

1. Added the original-source backed 19-record CSV experiment ledger with direct source file, job, artifact, n, Base, candidate regime, classifier freeze semantics, CI meaning, evidence tier, exact P0 checkpoint SHAs and forbidden merges.
2. Updated ONLY one sentence in canonical manuscript §5.5: HGB was *configured with a maximum* of 200 boosting iterations; did not change a single Section 6 number, plot, theorem or experimental claim.
3. In the approved outline, corrected outdated editorial status lines asserting 6.5 was unwritten and 6.4 was still awaiting reviewer tightening. Replaced the ambiguous supplement destination language with S4 Memory components, S6 history/context, S7 selection, S5/S8 candidate regimes. Its scientific C1–C3 novelty, evidence interpretation, original experimental plans and section order were preserved.
4. Kept historical first-draft provenance logs unchanged as **time-specific source records**. In particular, the original §6.5 provenance document describes a four-pipeline main table later removed during independent reviewer tightening; it must not override the currently published canonical manuscript or [the revised 6.5 audit](SECTION6_5_KBS_REVIEWER_TIGHTENING_2026-10-09.md).

## 5. Outstanding checks — no fabrication of completion

**Open archival checks:** Historical native KuaiLive policy and comparator *exact model-byte hashes* and the primary Twitch original Base checkpoint bytes have not all been recovered in the directly reviewed result reports. The checkpoint identity **non-equivalence** is supported by differing protocols, but missing hashes are marked unresolved in the ledger. Completing comprehensive file-hash provenance is a future S2 archive task, not a reason to invent equivalence.

**Open source/package checks:** S1 original dataset mapping/eligibility and all component-specific checkpoint provenance need a single completed formal supplement. The S2 table must preserve artifact paths and split-specific training metadata. S1–S8 are not yet assembled as submission-ready documents; S9 is a staged efficiency audit awaiting its formal typesetting and source checks.

**Completed exact-source PDF gate:** the Section 5.5 correction commit [fb1be75a](https://github.com/mzch0210/KuaiLive-Agent/commit/fb1be75ad6caa43f7214e918ea4c16ae8f7e5d3c) triggered [successful Actions build 37956836331](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37956836331) with [artifact 11627494599](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37956836331/artifacts/11627494599). The 27-page PDF and LaTeX log were downloaded and checked: the corrected maximum-iteration wording appears on rendered page 16, §6.5 remains legible on page 23, References begins page 24, no undefined references are reported and no new overfull box was introduced. The single previously reported 5.51282-pt overfull line in Section 3 remains a later presentation-cleanup item.

**Stage boundaries:** No new DEV budget curve, Memory-component manuscript insertion, Gate-objective training, P2 negative-resampling run or extra strong-Base training was undertaken; those belong to later P1/optional phases. Discussion, Conclusion and Abstract remain unwritten.

## 6. G1 acceptance status

| Gate | Status |
|---|---|
| Central Twitch/KuaLive Section 6 claim → original source and split | **PASS for primary sources directly inspected** |
| C1–C3 and Sections 3–6 information/inference hierarchy | **PASS** |
| Detailed KuaiLive matched 2x2 and three-seed identities | **PASS** |
| One minor Section 5.5 parameter wording inconsistency | **CORRECTED** |
| Full historical and Twitch checkpoint-byte hashes | **OPEN** |
| Submission-ready complete S1–S9 | **OPEN** |
| Updated exact-source compiled PDF verification | **PASS** — build 37956836331, artifact 11627494599, rendered pages 16/23 reviewed |

**Interpretation:** The central Stage-1 audit and narrowly necessary text housekeeping have been executed. Do not describe the formal supplement package or archival fingerprint coverage as completed.
