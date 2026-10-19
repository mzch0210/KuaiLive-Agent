# N12-C8N | Scientific Novelty Reinforcement: Decision-Relevant Candidate-Regime Supervision

Date: 2026-10-19. **Execution addendum to C8 academic-argument revision.** C0–C7 archived PASS, C8 three-role referee simulation complete; C8 author/go-no-go remains pending. This document defines authorized **manuscript-only scholarly edits**; no new source labels, model fits, thresholds, TEST scoring, p-values, new experiments or external approvals. It is **not** a guarantee of journal novelty or peer-review acceptance.

## 1. New prior-art stress test: an additional relevant research tradition

- Krichene & Rendle (KDD 2020), *On Sampled Metrics for Item Recommendation*: sample-based top-K metrics may not preserve full-candidate ranker comparison; **already-known metric phenomenon**. https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Mao, Mohri & Zhong (ICML 2024), *Regression with Multi-Expert Deferral*: learning to choose a pretrained incumbent or external expert using losses and costs, with theoretical guarantees; **already-known expert selection mechanism**. https://proceedings.mlr.press/v235/mao24d.html
- Mandi et al. (JAIR 80, 2024), *Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities*, doi:10.1613/JAIR.1.15320: training for downstream decision quality rather than merely minimizing predictive error is **already established**. https://mlanthology.org/jair/2024/mandi2024jair-decisionfocused/
- Yuan et al. (arXiv September 2026), *Recommender System as Slow and Fast Thinkers*: fast/slow computationally conditioned recommendation selection under budgets, preprint. https://arxiv.org/abs/2609.02671
- Zhong et al. (KBS 2026), *Scene-aware memory discrimination*: scene-dependent retention/writing rather than incumbent-relative use-time selection. https://www.sciencedirect.com/science/article/pii/S0950705126002388
- Xie et al. (KBS 2026), *Fusing multi-head gating and focused-view contrastive learning*: learns KG multi-view representations and fusion; N12 Memory is a fixed count/decay specialist and **not** a new graph representation. https://www.sciencedirect.com/science/article/pii/S0950705126004132

**Editorial conclusion:** merely stating that sampled rankings are inconsistent, a gate is useful, or decision-focused supervision beats predictive accuracy is **not** a distinct scientific contribution. The paper's defensible advance is an *empirical protocol-specific demonstration* of candidate-regime supervision **propagating to the allocation of calls to a fixed relationship-evidence source**, with separately frozen full-candidate policy outcomes and a parallel authentic-history null test. No firstness/optimality theorem.

## 2. Stronger integrated scientific question

> When the same pre-event features are used to decide whether to invoke an already-fixed historical knowledge specialist, does evaluating the specialist's `Base-relative` top-K value on sampled rather than actual eligible candidates change **which requests** get the source, and what ranking utility follows from those choices?

This sharply separates:
- **Known sampled metric bias**: whether a *reported ranker comparison* changes between candidate sets;
- **Known expert deferral**: given a suitable conditional loss/value, whether to call an expert;
- **Known decision-focused training**: optimize downstream choices rather than accuracy alone;
- **N12 empirical target**: *which candidate-regime relative-value labels* are appropriate for an **already fixed and auditable knowledge source** and how regime mismatch shows up in **switch-level actual utility**.

The paper should not claim these four principles are individually new. Scope the conclusion to live recommender ranking with event-specific eligible candidates and the frozen policies tested.

## 3. Policy switch accounting: existing DEV evidence, no new effect estimation

Under the exact same full-candidate outcomes for an incumbent `B`, fixed `M` and binary policy `π`, define
`V_F(π)=E[u_F(B)+π(Z)Δ_F]`. Therefore
`V_F(π_F)−V_F(π_S)=E[(π_F−π_S)Δ_F]`, where the second expression can be grouped into positive terms for `π_F=1,π_S=0` and negative terms for `π_F=0,π_S=1`. This is an **algebraic identity**, not a novel theory or causal isolation. The following are **published post-G5 exploratory M3 DEV summary numbers** from `N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md`, not independent 30k TEST measurements:

| Base | DEV disagreement | F-only / S-only Memory calls | Mean Δ_F on F-only vs S-only | Full DEV NDCG contribution, + / − | Net F−S |
| --- | --- | --- | --- | --- | --- |
| SASRec | 10,672 / 50,049 (21.32%) | 5,350 / 5,322 | +.133417 / +.076194 | +.014262 / −.008102 | +.006159 |
| GRU4Rec | 11,517 / 50,049 (23.01%) | 5,639 / 5,878 | +.126600 / +.079135 | +.014264 / −.009294 | +.004970 |

**Crucial counterintuition:** on average both switched groups have **positive** true Memory−Base value. The gain is best interpreted as **reallocating limited calls toward higher-value requests**, *not* simply identifying calls that are harmful. Because calls differ (even if relatively similar on DEV), decomposition alone is not an equal-call causal experiment. 50,049 DEV and 30k additional target pools **must not be equated**.

The separate frozen 30,000 same-recording-period M3 F-evaluated H1 provides policy-level confirmation: SAS F−S +.005391 CI [.003646,.007174], GRU +.003585 CI [.001599,.005576], with natural Memory calls **8704/9105** and **8629/9168**. Calls differ by 1.337/1.797 percentage points, exceeding original near-equal allowance; **only complete frozen-policy outcomes are established**.

Parallel RQ3 4,096 nested historical-source original vs constrained null +.031145: source arrangement informative under fixed candidates, but original prereveal same-cohort TRAIN-popularity floor was **NOT VERIFIED**, null rewiring is composite and three seeds are not independent cohorts. This test does not isolate the RQ2 mechanism.

## 4. Manuscript change contract and exact stopping rules

Change **title (optional), abstract, Intro motivation/contribution bullets, Related Work**, one key RQ2 Results exposition paragraph, **Discussion and Conclusion**, and Highlights to make the decision-level empirical question explicit. Introduce verified JAIR decision-focused learning survey in BibTeX as a *novelty boundary*, not an invented baseline. Preserve:
- all 7 literal Results original tables and original Twitch diagnostic figure;
- all 9 original Methods + 2 Experimental Design math blocks, existing LaTeX refs/labels;
- every frozen metric, CI, p-value, test population, candidate regime and call count;
- all four S10.19 supporting source tables (17 rows/49 numeric cells); still checked by C7 auditor;
- adverse Always Memory unconditional accuracy and old Utility latency, same-period overlap, H2 nonverified floor.

The new on/off accounting in text is **existing exploratory DEV evidence**, not a new frozen H1 claim, not a new hypothesis family and not a proof of knowledge-source-specific causal mechanisms. Relevant source `experiments/kbs_plan_c/N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json`.

**Stop** if writing implies novel sampled-ranking theorem / first use of decision-oriented learning / strict equal-budget effect / causal change in semantic relation alone / verified new TEST / measured deployment savings. New H1 evidence would require a separately pre-specified future independent cohort; not needed just to submit the bounded paper.

## 5. Deliverables and gate

1. Manuscript/BibTeX/Highlights revision aligned to the scientific question and verified exact DEV switches.
2. Run existing C6 science contract and C7 full-table-cell auditor / 5 tests **again after edits**.
3. New stage-named dual-PDF CI, no overfull boxes, resolved refs and primary numbers visible in PDF; log exact run/commit/39? actual page counts (no assumed lengths).
4. Detailed QA note identifying changes and remaining originality objections, and record that C8 **human scientific Go/No-go, author identity and AI/funding/COI/data declaration are still open**. No automatic C8 overall PASS/merge/submission.

**Result intended**: stronger specificity and clearer chain of evidence, **not a fabricated methodological invention**.
