---
title: "Supplementary Information — N14"
subtitle: "Candidate-Aligned Knowledge Valuation for Selective Relationship Memory Routing in Live-Streaming Recommendation"
author: "Anonymous manuscript — Knowledge-Based Systems"
fontsize: 9pt
geometry: margin=0.76in
colorlinks: true
linkcolor: black
urlcolor: blue
toc: true
toc-depth: 1
header-includes:
  - \usepackage{microtype}
  - \setlength{\emergencystretch}{3em}
  - \sloppy
---

**Scope.** This document supports a **single research question**: whether the candidate regime used to label fixed Memory-minus-Base value changes frozen policies' allocation and full-candidate ranking outcomes. It contains the primary M3 evaluation protocol, exact aggregate result cells, development allocation accounting and original multiplicity/validity disclosure. It is **not** a repackaging of the original Twitch-selection, multi-seed selection, relationship-null or GPU-cost projects as additional independent contributions. Full historical tables and methods remain in the [N13 source-preserving archive](https://github.com/mzch0210/KuaiLive-Agent/tree/kbs-n14-single-question-scope-reset-20261023/manuscript/kbs_latex) and the unchanged companion document `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md`.

**Data availability boundary.** The public [KuaiLive dataset](https://zenodo.org/records/16565801) and the [companion repository](https://github.com/mzch0210/KuaiLive-Agent) provide upstream and method provenance. Derived event-level TEST predictions, processed bundles and model checkpoints are not represented as stable, unrestricted public deposits. Source access and derivative redistribution permissions require verification by the responsible author. A GitHub Actions artifact is not a persistent DOI.

---

# N14-S1. Candidates, ranking tasks and pretarget information

The retrospective KuaiLive **room** diagnostic contains **10,222 paired events** scored using fixed Base and Short--Long--Popularity Memory checkpoints under both a 575-candidate target-retained sampled regime and contemporaneous full-active room candidates. The ranking unit is a **room**, not a persistent creator; candidate identity, membership and competition change jointly. The paired diagnostic is not the M3 policy cohort.

M3 ranks persistent **author_id** identities eligible through active rooms. The original author-ranking TEST cohort consists of **47,575** events, while the independent *event-ID set* of **30,000** additional M3 author-ranking targets (10,387 users) was selected from the same **March 27–31, 2026** recording interval. Both policies receive the same full-active candidate roster and pretarget features. These are not newly recorded future-period observations and users may be shared.

The fixed specialist scores use 0.45 Short + 0.45 Long + 0.10 TRAIN-only popularity. The Base is fixed SASRec or GRU4Rec as applicable; the same fixed specialist applies within each event. The 12 M3 decision features consist of five Base-score statistics and seven history/candidate summaries, all computed from information available before the target outcome. The true current target can be retained in sampled **offline labels** but is not an input to the policy, candidate generator, historical source or threshold.

# N14-S2. Policy fitting, target freeze and inference

The two original sampled- and full-candidate supervision arms were **separately** trained and DEV-calibrated. S labels are the **uncorrected** 575-candidate target-retained Memory-minus-Base NDCG@10 increments; F labels are computed on the full-active roster. Both policy arms use identical **full-active** decision-time feature definitions. Four **user-disjoint DEV out-of-fold folds** define policy-calibration thresholds at nominal **30% DEV Memory calls**, and the final histogram-gradient-boosting policies use 120 iterations on all DEV. The additional 30k final policies are distinct from the earlier five-fold/200-iteration original M3 selector study.

The 30,000 target sample was frozen before labels were examined by five source dates × four pretarget-history quartiles, exactly **1,500 events per cell**, drawn from **4,723,652** eligible residual source events. Event-ID-seeded, label-blind selection excluded the original 47,575 TEST target IDs. The 20-cell eligible-population weight for a selected event in stratum h is $w_i=N_h/n_h$; reported weighted NDCG and Memory-call fractions use the same weights. Kish effective weighted sample size is **26,849.29**, not a count of independent users.

User-cluster paired percentile intervals use **5,000 bootstrap draws**. Frozen directional tests use 5,000 user-cluster sign randomizations under an approximate cluster sign-symmetry null. The original Holm family contains **exactly three** directional hypotheses: SASRec F−S, GRU4Rec F−S and a separately frozen nested authentic-history versus mean-null contrast. Removing the third from the main paper's research questions **does not permit retrospective two-test p-value adjustment**.

**Target-blind provenance:** [A3 H1 seal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517170015), [nested pre-outcome seal](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38517502835), [prereveal audit](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518563975), [A4 outcome read](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38518785650), [A5 numerical reconstruction](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38519174441). Sample SHA256 (30k): `be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14`. These are research provenance records, not a claim that derived private rows can be downloaded publicly.

# N14-S3. Primary frozen policy outcome and calls

**Table N14-S1. Additional M3 targets, fixed full-active F ranking, 20-cell natural population weighting (exact source: original Table S10.9).**

| Frozen policy | Weighted F NDCG@10 | Realized Memory calls | Unweighted call rate | Weighted call rate |
| --- | ---: | ---: | ---: | ---: |
| SASRec Always Base | 0.259307 | 0 | 0% | 0% |
| SASRec S-aligned | 0.300055 | 9,105 | 30.350% | 30.537% |
| SASRec F-aligned | **0.305446** | **8,704** | **29.013%** | **29.203%** |
| GRU4Rec Always Base | 0.260058 | 0 | 0% | 0% |
| GRU4Rec S-aligned | 0.300945 | 9,168 | 30.560% | 30.809% |
| GRU4Rec F-aligned | **0.304530** | **8,629** | **28.763%** | **29.008%** |
| Always Memory (shared) | **0.348744** | 30,000 | 100% | 100% |

The SASRec F-minus-S paired contrast is **+0.005391** (95% user-cluster CI **[+0.003646,+0.007174]**, three-test Holm-adjusted one-sided $p=0.000600$); GRU4Rec is **+0.003585** (CI **[+0.001599,+0.005576]**, adjusted $p=0.000800$). The F-aligned fixed gates make **401** and **539 fewer calls**, respectively. However, their realized unweighted call differences (**1.337** and **1.797 percentage points**) exceed the prespecified approximately equal-budget interpretation threshold of **1.0 pp**. Thus the evidence concerns quality and calls under **natural frozen-policy operation**, not a strict equal-call comparison. Always Memory remains more accurate at 100% specialist invocation. All five daily subgroup effects are descriptively positive, but shared users and one collection period prevent treating them as independent validation datasets. The DEV supervision labels also differ in available information, so the contrast does not isolate generic model architecture.

# N14-S4. Shared-DEV decision allocation (descriptive only)

**Table N14-S2. M3 exploratory DEV candidate-supervision transfer (50,049 author-ranking DEV events; 12,628 users; exact source: original Table S10.14).**

| Base | Training supervision → evaluation candidates | Full-F NDCG@10 | Realized Memory calls |
| --- | --- | ---: | ---: |
| SASRec | Sampled S → full F | 0.296499 | 14,988 |
| SASRec | Full F → full F | **0.302658** | 15,016 |
| SASRec | Full-label adapted → full F | 0.301847 | 14,954 |
| GRU4Rec | Sampled S → full F | 0.298123 | 15,001 |
| GRU4Rec | Full F → full F | **0.303093** | 14,762 |
| GRU4Rec | Full-label adapted → full F | 0.303000 | 14,989 |

The sampled S labels are constructed retrospectively by retaining the observed positive author on DEV; all real policy features are computed from full-F candidates and earlier information. The adapted condition uses full-F training labels on outer-fold training users rather than label-free adaptation. Actual outer-fold calls are not strictly equalized. The full-supervised gains over S-supervised are **+0.006159** (SASRec; paired 95% CI [+0.004835, +0.007543]) and **+0.004970** (GRU4Rec; [+0.003550, +0.006369]); 10,672/50,049 (21.32%) and 11,517/50,049 (23.01%) decisions disagree, respectively. This is an **exploratory DEV** analysis, not an independent held-out TEST or an additional prespecified hypothesis family. Additional DEV methodology and mechanism details remain in earlier S10 sections.

F-only and S-only calls: SASRec **5,350 vs 5,322**; GRU4Rec **5,639 vs 5,878**. Mean observed Memory-minus-Base value on F-only versus S-only events is **0.133417 vs 0.076194** (SASRec) and **0.126600 vs 0.079135** (GRU4Rec). Both displaced and newly invoked groups are beneficial on average. This is an algebraic description of one **50,049-request DEV** cohort, not a causal mediation of the held-out 30,000-target result, and not fractions of Memory calls.

# N14-S5. The third original Holm contrast and its incomplete prereveal acceptance check

The **third** originally prespecified directional comparison used **4,096** targets (3,059 users) nested in the additional 30k cohort and one fixed full-active candidate roster. Authentic Full Memory weighted NDCG@10 was **0.334942**; the per-event mean of three independently randomized but **same-cohort** constrained history nulls was **0.303797** (seeds **20261014/20261015/20261016**; individual scores **0.303905, 0.304689, 0.302796**). The authentic-minus-mean-null contrast was **+0.031145**, paired user-cluster 95% CI **[+0.027389,+0.035098]**, original Holm-adjusted one-sided **p=0.000600**. It is disclosed solely for the integrity of the prereveal multiplicity family and its archived source result. It is **not** presented as a second main research question or causal evidence that authentic historical relation structure mediates the primary policy comparison.

The constrained rewiring altered identity-specific repetitions **and** higher-order historical features. Rewiring checks, remaining positives and within-hour constraints were partially confirmed. **One prespecified acceptance diagnostic is NOT VERIFIED:** the nested cohort's **TRAIN-only Popularity** floor/margin for the three nulls was not measured and sealed before target-label revelation. A separate DEV popularity check cannot retroactively satisfy this original requirement. The three null seeds are not three independent cohorts. Original [S10.16 and S10.18](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md) preserve the full null generation and control details without altering the stated acceptance history.

# N14-S6. Adverse comparisons, measurement boundaries and full source archive

On the additional-target cohort, **Always Memory** weighted full-candidate NDCG@10 is **0.348744**, exceeding the selective F-aligned scores **0.305446** and **0.304530** at its unrestricted 100% call rate. In a separate warmed GPU DEV replay, the **old pointwise** Utility path averaged **1.76941 ms** versus **0.69165 ms** for Always Memory and **0.72759 ms** for Base. The later vectorized F-supervised online path has **not** been measured end to end. Lower specialist call fractions do **not** demonstrate serving speedups, RPC savings or monetary returns.

No scientifically accepted corrected sampled-only trained selector was evaluated. A valid corrected-S comparator could narrow the observed full-versus-sampled policy difference; sampled target-retention and the unequal realized call fractions remain relevant limitations. The empirical claims therefore concern separately frozen `F` and original `S` policies, not a pure equal-resource causal label effect. Source and result release constraints are unchanged.

The original full research record is preserved in:

- [N13 complete Results](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/manuscript/kbs_latex/N14_N13_COMPLETE_RESULTS_RESEARCH_ARCHIVE_2026-10-23.tex) (all seven original table blocks and diagnostic figure).
- [N13 complete Methods](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/manuscript/kbs_latex/N14_N13_COMPLETE_METHODS_PROTOCOL_ARCHIVE_2026-10-23.tex).
- [Original complete S1–S10.19 supplement](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/manuscript/kbs_latex/SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md) with original DEV, Twitch, M3, source-null, feature-ablation and original cost tables.
- [Scientific freeze fixture](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/analysis/kbs_plan_c/n12_c5_original_results_source_freeze.json) and [N14 archive-integrity validator](https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n14-single-question-scope-reset-20261023/analysis/kbs_plan_c/n14_p2_science_archive_contract.py).
