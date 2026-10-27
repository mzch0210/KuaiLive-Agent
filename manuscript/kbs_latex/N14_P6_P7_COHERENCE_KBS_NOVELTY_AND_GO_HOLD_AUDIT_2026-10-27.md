# N14 P6–P7 — Cohesion, KBS novelty, and submission-decision audit

**Date:** 2026-10-27 | **Branch:** `kbs-n14-single-question-scope-reset-20261023` | **PR:** Draft #8

## P6: Whole-paper and journal-supplement coherence

The full N14 manuscript now has one research question and four Results subsections: paired room-regime diagnostic; frozen 30,000-author-target policy contrast; descriptive 50,049-DEV decision switches; adverse quality/cost/comparator boundaries. Earlier complete N13 Results, Methods, S1–S10.19 and the 11 original source tables remain unmodified research sources.

**Detected and corrected in P6:**
- Original fifth Highlight promoted the 4,096-event historical-source perturbation to a parallel contribution. The five current Highlights concern candidate-indexed supervision, full-candidate policy ranking, population-weighted calls, DEV switches and the non-matched-call causal limit. Each line is at most 85 characters.
- Several main-paper Methods and Results citations still named the historical S1–S10 archive as if it were the submitted journal Supplement. They now point to N14-S1/N14-S2, focused Table N14-S1/N14-S2 and, when necessary, explicitly to the complete original research archive.
- Focused supplement's two copied tables now use **N14-S1** and **N14-S2** as journal caption IDs, with exact original **S10.9** and **S10.14** source IDs preserved. Only caption text/links changed; result rows and numeric cells were retained.
- An independent `n14_p6_cross_document_consistency.py` verifies science-contract continuity, five Highlights, main-to-focused references, main/supplement key numeric facts, and original three-member Holm/H2 pre-reveal disclosure. The old 11-result-table and 49 migrated-cell contract is still executed first.

**P6 gate:** Source corrections completed. The final same-source dual-PDF and cross-document CI outcome must be read from its actual workflow run; a successful previous-source PDF is not sufficient. PDF visual spot checks and completeness are distinct from source-level/zero-overfull checks.

## P7: Nearest-prior-art novelty assessment

| Nearest published topic | Prior art already establishes | Residual contribution in N14 | Risk |
|---|---|---|---|
| Krichene and Rendle, KDD 2020, *On Sampled Metrics for Item Recommendation* ([Google Research](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)) | Sampled ranking metrics may not preserve full-ranking method order | Study the consequences of an **incremental fixed Memory-minus-Base supervision target** for downstream use decisions and identical full-F ranked outcomes | Substantial: plausible application of known inconsistency to a learned gate |
| Subbiah et al., CIKM 2024, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling* ([Google Research](https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/)) | Sampled rank-estimation corrections | Target-retained original S policy vs F policy demonstrates a bounded empirical difference; **does not refute corrected-S** | High: no valid corrected sampled-label gate trained/evaluated |
| Mao et al., ICML 2024, *Regression with Multi-Expert Deferral* ([PMLR](https://proceedings.mlr.press/v235/mao24d.html)) | Instance-dependent learned deferral and expert selection | Candidate-indexing of the **target used for deferral value estimation** under time-varying ranking candidates | High: no new deferral theorem or optimizer |
| Knowledge-aware memory and live recommendation studies | Historical relationship features, selective access and learned ranking are established | Same fixed Memory source and frozen ranker isolate an operational label-regime design question in live-ranking policy | Transfer to other domains / candidate regimes not established |

**Novelty verdict:** KBS topic/scope aligned; novelty still **HIGH-CONTESTABLE**. Narrower storytelling has removed multi-paper diffusion, but does not replace an untested corrected-S comparator, unequal realized call rates or independent future-period replication. This is a bounded empirical methodology insight, **not** a new ranking metric, learned-to-defer theory, or measured cost-saving design.

## Key scientific counterevidence retained

- Primary SASRec/GRU4Rec weighted F−S effects: **+0.005391 / +0.003585** under the original three-directional-comparison Holm family; policy call rates are unequal and the originally sampled labels are uncorrected and target-retained.
- Always Memory (weighted full-candidate NDCG **0.348744**) exceeds both selective F policies. The original pointwise Utility path (**1.76941 ms**) is slower than Always Memory (**0.69165 ms**) in separate DEV replay; the newer F policy end-to-end runtime is not measured.
- 30,000 targets are event-ID-disjoint but from the **same recording period**, not a later independent cohort.
- H2 remained a member of the original multiplicity family: authentic-minus-null **+0.031145**, but its same-cohort TRAIN-only Popularity prereveal acceptance subgate is **NOT VERIFIED**. It is not treated as causal support for H1.
- The original DEV 10,672/11,517 disagreements are counts of **50,049 requests**, not percentages of Memory calls; DEV accounting is not held-out TEST mediation.
- NI1g corrected-S training gate and audited KuaiRec external replication path remain **NO-GO**. No new experiment is claimed.

## GO / HOLD / REDIRECT

- **Technical source / science integrity:** conditional GO for internal manuscript QA after latest same-commit workflows finish. No overwrite of N13 research provenance.
- **KBS scientific originality / journal-submission decision: HOLD.** A scoped empirical contribution exists, but the corrected-S competition and deferral/sampling prior art make the incremental methodological value contestable. It is not justified to state KBS publication-ready on the basis of a successful PDF alone.
- **Author-owned formal submission: HOLD**, pending verified authorship/CRediT, relevant actual AI assistance disclosure, funding/conflict/ethics statements, rights for data and derivative files, journal anonymization and final guide-specific material rules. None should be fabricated or signed by automated work.
- **REDIRECT:** retain as a defensible fallback if authors judge the originality bar inadequate for KBS; no alternative journal is endorsed without a separate evidence-based fit check.

## P6–P7 final deliverable

The project now contains a focused manuscript, focused supplement and complete original science archive, and an additional source-level cross-document guard. PR #8 remains Draft. Last validation run must be checked and any failures fixed before technical acceptance; the scientific/author-owned HOLD survives even a technically green CI.
