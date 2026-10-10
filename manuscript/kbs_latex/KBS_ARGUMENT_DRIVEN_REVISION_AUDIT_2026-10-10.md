# KBS manuscript argument-first editorial review and completed P1/P2 revisions

**Date:** 2026-10-10  
**Work order:** [approved scoped plan](KBS_ARGUMENT_DRIVEN_REVISION_PLAN_2026-10-10.md)  
**Source:** [canonical elsarticle English manuscript](main.tex); [completed S1–S9 supplementary tables](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)  
**Frozen scientific target:** Original approved outline C1–C3, one-shot Twitch test policy, matched KuaiLive P0/P1/P2, finite DEV diagnostics and tested CPU overhead. **No new model fit, extra TEST policy selection, mutation of original result tables or C1–C3 novelty redefinition.**

## 1. Editorial diagnosis: why the six chapters initially read as several papers

The original Sections 1–6 contain a valid empirical contribution but emphasize **distinct workstreams rather than one scientific argument**. The initial Introduction previewed Twitch and KuaiLive as independent accomplishments; methods described operations (checkpoint matching, relative-Utility supervision, various frozen protocols); Results alternated between separate tables and preemptive validity defenses. This forced readers to infer the central research thesis, making a KBS contribution resemble a laboratory status report.

The appropriate unifying proposition is: **Relationship Memory has a decision-specific incremental ranking value relative to an existing recommender, conditioned on the historical state and candidate ranking context; part of this value can be predicted before the user outcome and used to select the better fixed ranking.** This is the C1–C3 novelty already fixed in the outline, not a newly invented general expert-gating objective or information-theoretic theorem.

**Chapter roles after the source revisions:**

| Main chapter | Scientific question it answers | Argumentative output |
|---|---|---|
| 1 Introduction | What decision about historical evidence is missing? | Define the Base-relative incremental value question and preview both complementary empirical strands |
| 2 Related Work | Why is relative value different from fusion and routing? | Locate the fixed expert–Base valuation question within existing evidence, information value, and deferral work |
| 3 Problem | What exactly is the decision quantity? | Event-level \(\Delta_M\), conditional value \(\eta_r\) and selective gain identity |
| 4 Framework | How is that quantity instantiated? | Transparent Memory, fixed sequential Base, observable pre-outcome Utility features |
| 5 Methods | Which empirical comparisons address the quantities? | Twitch frozen policy comparison; same-checkpoint post-hoc KuaiLive candidate diagnostics; specified uncertainty |
| 6 Results | What changes the specialist's value and does selecting help? | Heterogeneity → predictive decision value → candidate-regime boundaries → DEV mechanisms → CPU cost |

The Results subsections retain their approved original ordering: 6.1 C1/C2 state structure, 6.2 C3 decision selection, 6.3 C2 candidate dependence. The new Results roadmap makes that ordering argumentative without reshuffling all numerical material.

## 2. Why negative evidence and statistical boundaries belong in a scientific paper

Three kinds of originally negative-looking sentences must be separated:

1. **Scientific negative findings**: always-Memory is worse than Base overall on Twitch; sampled-active Memory is worse than Base on KuaiLive; the measured warm CPU selector adds roughly 1.016 ms. These are essential original findings and were **not** removed.
2. **Methodological boundary conditions**: target-defined groups are retrospective; KuaiLive TEST P2 is already inspected post-hoc; the exact-count Difficulty comparator is not an advance-known pointwise threshold; candidate size/composition vary together; 81-tree CPU gate is not identified as the Twitch frozen gate. These are **truth conditions** and remain visible near affected estimates/Methods.
3. **Rhetorically repetitive preemptive defenses**: multiple nearby "not independently held-out", "not causal", "not a new routing algorithm", "not an exhaustive SOTA comparison", combined with workflow archive/seed details. Repeating them without a new comparison reduces scientific information density and makes the paper sound reactive. These were selectively rewritten as **positive claims with precise conditions**, with full source/hyperparameter provenance retained in S1–S9.

Writing guidance: [Elsevier's official research paper Discussion guidance](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/) requires interpreting limitations and their practical effects, not erasing them. A general well-established reporting standard [ICMJE manuscript structure and Results/Discussion](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) recommends logical Results order, succinct text/table division, and discussion of implications and limitations. It is not claimed to be the KBS journal's binding guide. [KBS's official scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) emphasizes original artificial-intelligence research, decision support, and balanced method/application relevance.

## 3. Completed P1/P2 source edits

| Prior issue | Implemented source repair | Scientific audit |
|---|---|---|
| **P1-A, cross-subsection argument** | First Results paragraph now explicitly traces observed Memory heterogeneity → learned pre-outcome Utility selection → regime dependence → mechanism/cost diagnostics. Introduction, related-work gap, problem, framework, and methods introductions were rewritten around the same decision quantity. | C1–C3 contribution headings and order unchanged; no newly defined hypothesis or model claim |
| **P1-B, 6.2 direct selection value** | New paragraph reports **Utility-selected +0.05136**, **Utility-unselected -0.05890**, and equal-count **Difficulty-selected +0.00855** per-event realized Memory−Base NDCG@10. | These are algebraic restatements of original frozen TEST means and 6,650 calls, not retraining, source event rerouting or a new significance test |
| **P1-C, sampled prior-art positioning** | §6.3 foregrounds how original sampled-ranking inconsistency appears for a fixed relationship specialist versus designated Base, with an algebraic candidate membership/z-score reference allocation. | Prior sampled-metric order inconsistency belongs to Krichene and Rendle; no causal size-only effect or theorem claim |
| **P1-D, Full Memory composition** | §6.4 explicitly identifies Full Memory as fixed experimental specialist, contrasts recoverable Long-only 0.63890 versus Full 0.53298 and shows unavailable Long-only−Full −0.03208; overall Long-only 0.52761, Full 0.52170, Base 0.57185. | All source values in S4.1–S4.2; a post-target subgroup maximum is not substituted into primary policy |
| **P1-E, baseline and CPU fairness** | §5.2/§6.4 contextualize nonuniformly trained auxiliary baselines; §6.5 specifies the **separately benchmarked KuaiLive HGB** has 81 fitted trees (depth 3), distinct from the Twitch model's configured maximum 200 iterations. | No SOTA benchmark claim, no cross-checkpoint pooling, no production runtime savings claim |
| **P2, precise supplement reference and Results density** | New cross-references to **S4.1–S4.2, S5.2, S6.1, S6.4, S7.1 and S9.1**; P2 nine-draw table remains in S5; excess repeated caveats in core method/introduction/result transitions condensed. | Every cited table title/number exists in the unified S1–S9 source; no changed experiment or paired CI |

### 3.1 Derivation of newly displayed selected/nonselected conditional means

From the **original frozen Twitch TEST, n=44,221**:
- Base mean = 0.5821113853, always-Memory mean = 0.5397954318;
- Utility policy mean = 0.5898344192, matched-count Difficulty mean = 0.5833967726;
- Utility call count m = 6,650; noncalled events = 37571; call proportion p = 0.150381040682.

For a hard-routing choice with the same default Base ranking on unselected events:
\[
\overline\Delta_{\mathrm{Utility\ selected}} =
\frac{\overline u(\mathrm{Utility})-\overline u(B)}{p}
= +0.0513564334.
\]
The unselected Memory−Base diagnostic mean is:
\[
\overline\Delta_{\mathrm{Utility\ unselected}} =
\frac{\overline u(M)-\overline u(B)-[\overline u(\mathrm{Utility})-\overline u(B)]}{1-p}
= -0.0588957989.
\]
The retrospectively Difficulty-selected average gain, from its identical call count, is:
\[
\overline\Delta_{\mathrm{Difficulty\ selected}} =
\frac{\overline u(\mathrm{Difficulty})-\overline u(B)}{p}
= +0.0085475356.
\]
Checks: selected mean × p = the same +0.0077230 Utility−Base population gain; weighted selected+unselected = -0.0423159535 overall Memory−Base. The subgroup means **depend on distinct selection masks** and are observational summaries; their displayed difference does not constitute an additional paired inferential test. All original full-cohort paired bootstrap confidence intervals in §6.2 retain their meaning. Repeated rounding to five decimals explains a small reconstruction remainder.

## 4. Outstanding scientific/narrative risks and disciplined finishing strategy

### A. The manuscript still lacks its interpretive synthesis, not another Results table

Even after strengthening paragraphs in Sections 1–6, the case will not read like a fully complete academic article until an **actual Discussion** integrates what the results mean: Base-relative redundancy, dependence on candidate universe, noncausal group interpretation, limited success of observable selection, and distinct efficiency cost. The approved outline already specifies **7.1–7.5**; do not shift this interpretation into the Results merely to mask a missing Discussion.

### B. Preserve scientific negative findings, relocate repetitive “non-claims”

A single clearly placed methodological statement and a localized Discussion limitations analysis should carry the burden for cross-protocol and selection assumptions. Results paragraphs should lead with (1) positive/negative observed effect, (2) paired quantitative evidence, (3) *one* relevant inference boundary when needed. Full archival lineage belongs in S2/S5/S8/S9. Do not remove essential target-label leakage warnings, non-independent TEST labeling or unfair comparator limits.

### C. Honest unresolved evidence scope

- Primary C3 selection has one frozen Twitch TEST (44,221) and a **modest** Utility−Base +0.00772, versus an unattainable hindsight Oracle: 11.7% of the conditional two-ranking same-count bound recovered.
- Candidate-sample P2 nine draws use already inspected KuaiLive users and source pairs; user bootstrap, candidate RNG and three fitted-checkpoint seeds are distinct uncertainty levels.
- S3 auxiliary baseline tuning budgets remain unequal. Stronger published baselines have not been proven inferior under fully symmetric tuning.
- Cached KuaiLive CPU panel includes gate prediction but routing decisions use archived masks, and is not an independent Twitch deployment benchmark.

### D. Next full-paper authoring stages (not performed or implied complete)

Discussion §7, Conclusion §8, and Abstract remain absent in the canonical manuscript. Coauthor scientific review, formal author/declaration data, KBS-specific live guide verification, long-term source artifact archiving, and complete final-paper post-authoring typesetting remain separately required.

## 5. Acceptance and editorial gate

- Confirm only intended text changed and **no C1–C3 novelty redefinition** occurred.
- Recheck original n=44,221, m=6,650, n_unselected=37,571 and three new conditional mean identities.
- Confirm 23 S1–S9 extended tables and all **Sx.y** pointers align.
- Compile the exact GitHub `main.tex` revision; check missing citations, typography, float/table placement and the 6.5 versus References boundary. Matching run/verified artifact should be recorded **only when actually complete**.
- Preserve source and author-review distinction: a successful LaTeX build is a format validation, not a guarantee of KBS publication or acceptance.

**Editorial verdict:** This scoped round completes the requested P1/P2 modifications and materially improves the **argument-first organization of Sections 1–6**. The next major gains in paper coherence will come from disciplined Discussion/Conclusion synthesis, not from loosening verified scientific boundaries or adding a new algorithm competition.
