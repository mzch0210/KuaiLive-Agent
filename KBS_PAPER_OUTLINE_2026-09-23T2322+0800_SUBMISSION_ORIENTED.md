# Submission-oriented manuscript outline for *Knowledge-Based Systems*

> **INDEPENDENT / NON-AUTHORITATIVE MANUSCRIPT OUTLINE**  
> This document is a paper-facing writing outline. It does not replace frozen experimental protocols, immutable test results, or prior authoritative experimental snapshots unless explicitly promoted by the authors.

**Updated:** 2026-09-25  
**Target journal:** *Knowledge-Based Systems*  
**Project:** `mzch0210/KuaiLive-Agent`

---

# Proposed title

## Preferred

> **When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation**

## Conservative alternative

> **Base-Relative Value of Relationship Memory in Live-Streaming Recommendation**

The title should foreground the scientific question and the Base-relative valuation concept rather than generic routing, gating, or memory architecture.

---

# Abstract

Structure the abstract around one scientific question, one mechanism result, one decision result, and one held-out validation result.

1. **Problem.** Strong sequential recommenders represent a bounded or compressed interaction history, while auxiliary historical evidence is not automatically useful because its marginal value depends on what the base already represents and on the operating recommendation regime.
2. **Operationalization.** Instantiate persistent relationship evidence through a transparent relationship-memory specialist and measure its event-level marginal ranking utility relative to a strong base recommender. Avoid implying that the measured quantity is an intrinsic, model-independent information value of history.
3. **Mechanism.** Characterize represented, recoverable-but-unrepresented, and unavailable relationship evidence; report pre-specified development analysis, untouched held-out test replication, and the context-capacity intervention showing that the same persistent evidence loses marginal value once a larger base context represents it.
4. **Decision.** Estimate conditional specialist-minus-base utility rather than generic base difficulty; show that Utility more strongly enriches recoverable events whereas Difficulty disproportionately selects unavailable events under the same invocation budget.
5. **Validation.** Report the KuaiLive regime reversal and the untouched Twitch/LiveRec held-out test result.
6. **Qualification.** State that evidence state structures but does not uniquely determine utility, the measured evidence value is operationalized through the fixed specialist, and substantial Oracle headroom remains.

Prioritize two quantitative anchors rather than a long result list:

- **Mechanism:** recoverable-to-represented transitions under context expansion reduce specialist-minus-base utility by approximately `0.42–0.45` NDCG@10 while canonical Memory is fixed.
- **Held-out decision:** on untouched Twitch/LiveRec TEST, Selective Utility improves over Base by `+0.00772` NDCG@10 and over exact-budget Difficulty by `+0.00644`.

Avoid introducing the paper as a new gating architecture, new Memory network, generic Learning-to-Defer method, or universal theory of information value.

---

# 1. Introduction

The formal manuscript Introduction is the canonical guide for this section. Do not reintroduce an explicit RQ list into the main text.

## 1.1 Motivation and scientific gap

Establish the following sequence:

1. Strong sequential recommenders represent recent or compressed interaction history.
2. Auxiliary evidence can be redundant, unavailable, or complementary relative to that representation.
3. Existing work extensively studies how heterogeneous evidence should be integrated, selected, denoised, or weighted; a distinct question is whether a fixed auxiliary specialist contributes positive marginal ranking utility relative to the current base for a specific event.
4. Persistent user–creator relationships in live-stream recommendation provide a transparent empirical setting in which target-specific evidence may already be represented, remain recoverable from older history, or be unavailable.
5. This motivates **Base-relative evidence valuation**, operationalized through a transparent fixed specialist rather than interpreted as intrinsic information value.

Use the central sentence:

> **The central problem is not whether more historical evidence improves recommendation, but whether that evidence is incremental relative to the information already represented by the base.**

## 1.2 Empirical motivation

Preview only three facts:

- aggregate specialist ordering reverses across KuaiLive candidate regimes;
- conditional evidence-state structure identified in pre-specified Twitch/LiveRec development analysis reproduces on untouched held-out test data;
- under a development-only context-capacity intervention, the same evidence loses approximately `0.42–0.45` NDCG@10 of specialist-minus-base utility when a larger base context comes to represent it.

Do not reproduce the full result matrix in the Introduction.

## 1.3 Contributions

Use exactly three headline contributions.

### C1 — Base-relative evidence valuation

> Operationalize the Base-relative value of persistent relationship evidence through the event-level marginal ranking utility of a transparent relationship-memory specialist relative to a strong base recommender, rather than standalone specialist performance or generic base difficulty.

### C2 — Relationship-evidence mechanism

> Characterize represented, recoverable-but-unrepresented, and unavailable evidence states; combine pre-specified development analysis with untouched held-out replication and a controlled base-context intervention; and show that evidence state structures, but does not deterministically fix, specialist utility across regimes.

### C3 — Conditional decision and validation

> Connect conditional specialist-minus-base utility to selective invocation and validate the decision principle across KuaiLive regimes, strong-base controls, independent training seeds, and an untouched second-platform held-out test.

End the Introduction with a scope sentence: the formulation can describe fixed auxiliary specialists more generally, but the empirical claims remain limited to the evaluated live-stream platforms, candidate protocols, and ranking outcomes.

Do **not** claim novelty for generic gating, mixture-of-experts, Learning-to-Defer, long/short-term modeling, evidence selection, multimodal fusion, or the weighted relationship-memory formula itself.

---

# 2. Related Work

Organize Related Work around nearest conceptual neighbors, using one concise positioning statement per subsection rather than repeated defensive contrasts.

## 2.1 Sequential and long-horizon recommendation

Cover strong sequential encoders and later work that broadens or enriches historical representation.

Positioning boundary:

> The contribution is not broader history encoding; it is the operational marginal value of a separately maintained relationship-evidence specialist relative to an already strong base representation.

## 2.2 Auxiliary evidence integration, selection, reliability, and harmful information

Cover:

- adaptive multi-source and long/short-term fusion;
- multimodal complementarity, redundancy suppression, and denoising;
- reliability-aware evidence modeling;
- preference-relevant evidence selection, including KAPER-style path evidence selection;
- conditional evidence gating;
- negative transfer / harmful auxiliary information;
- value-of-information as a decision-theoretic conceptual neighbor.

Positioning boundaries:

> Evidence integration or selection asks how information should be represented, filtered, or used downstream; **Base-relative evidence valuation asks what operational marginal ranking value a fixed auxiliary specialist contributes relative to a trained base.**

> Evidence reliability does not imply positive Base-relative marginal utility, and the current formulation does not claim model-independent intrinsic information value.

## 2.3 Expert routing, selective prediction, and Learning-to-Defer

Acknowledge post-hoc deferral, two-stage expert allocation, multiple-expert routing, and cost-sensitive decision making as established problems.

State explicitly:

> The paper does not propose new general deferral theory. It studies the conditional marginal ranking value of one transparent recommendation specialist and uses an estimator of that quantity for selective invocation.

Difficulty remains a **mechanistic control**, not a representative baseline for all L2D methods.

## 2.4 Live-streaming and repeat-aware recommendation

Cover dynamic availability, viewer–streamer interactions, repeated viewing, interaction decay, and richer viewer–channel relation modeling.

Positioning boundary:

> Live streaming supplies the empirical environment in which Base-relative relationship evidence can be studied; repeat modeling itself is not the methodological novelty.

## 2.5 Positioning summary table

Retain a compact three-column table:

| Research line | Primary objective | Difference in focus |
|---|---|---|
| Sequential / long-horizon recommendation | Encode broader history | Residual utility of a separate relationship-evidence specialist |
| Auxiliary fusion / evidence selection | Integrate, filter, or select evidence | Operational marginal ranking value relative to a trained base |
| Reliability / denoising | Estimate trustworthiness or informativeness | Reliable evidence may still be redundant relative to the base |
| Value of information | Quantify benefit of acquiring information | Ranking contribution of an already defined fixed specialist |
| L2D / expert routing | Assign instances to predictors/experts | Characterize the utility structure of one interpretable evidence specialist |
| Live-stream recommendation | Model dynamic availability and repeat behavior | Empirical setting for Base-relative evidence valuation |

The purpose is precise differentiation, not a claim that adjacent work is absent or inferior.

---

# 3. Problem Formulation

The current LaTeX manuscript is canonical for Section 3. Keep the section concise and avoid theorem inflation.

## 3.1 Recommendation setting and event-level ranking utility

Distinguish the pre-outcome decision context

\[
\xi=(u,t,\mathcal C_{u,t},\mathcal H_{u,t})
\]

from the evaluated event `x=(ξ,y)`. Models and selectors receive `ξ`, not the observed target `y`.

For one relevant target at cutoff `K`, define event-level NDCG utility:

\[
u_K(A,x)=
\begin{cases}
1/\log_2(r_A(y\mid\xi)+1), & r_A(y\mid\xi)\le K,\\
0, & r_A(y\mid\xi)>K.
\end{cases}
\]

Because rank utility is candidate-set relative, candidate construction can alter Base-relative specialist value even when underlying user–target history is unchanged.

## 3.2 Base-relative specialist utility

Define

\[
\Delta_m(x)=u_K(M,x)-u_K(B,x).
\]

Interpretation boundary:

> `Δ_m` is the **operational marginal value** of persistent relationship evidence as instantiated by fixed specialist `M` relative to fixed base `B`; it is not intrinsic or model-independent information value.

## 3.3 Conditional relative utility

For regime `r` and deployment-observable information `z`:

\[
\eta_r(z)=\mathbb E[\Delta_m(X)\mid Z=z,R=r].
\]

`R` indexes the event-generating/evaluation condition and need not be a selector feature. Analysis-only evidence-state labels, target `y`, realized ranks, and realized `Δ_m` are excluded from `Z`.

For a serving action `a`, define selective utility in prose or inline and retain the expected-gain identity:

\[
\mathbb E[u_K^{sel}-u_K(B)\mid R=r]
=
\mathbb E[a(Z)\eta_r(Z)\mid R=r].
\]

This is the decision rationale for predicting conditional relative utility rather than generic base difficulty.

## 3.4 Budget-constrained selective specialist use

Make **exact matched budget** the primary experimental decision formulation. For cardinality budget `m`, choose the `m` largest predicted `\hat\eta_r` values, with deterministic tie-breaking.

Key interpretation:

> Exact-budget evaluation depends on the ordering induced by `\hat\eta_r`, not on perfect absolute calibration.

Define the exact-budget Oracle by replacing predicted `\hat\eta_r` with realized offline `Δ_m`; Oracle is analysis-only.

Cost-sensitive thresholding is secondary deployment interpretation:

\[
a_r^*(z)=\mathbf 1[\eta_r(z)>\lambda\kappa_r(z)].
\]

At deployment, replace unobserved `η_r` with `\hatη_r`. Do not present this threshold as a new routing theorem.

## 3.5 Regime-level decomposition

Let `S` be a mutually exclusive and exhaustive partition of Base-relative evidence states. Then

\[
\mathbb E[\Delta_m\mid R=r]
=
\sum_sP(S=s\mid R=r)\,\mathbb E[\Delta_m\mid S=s,R=r].
\]

This separates evidence-state composition from state-specific specialist utility. Treat it as analytical decomposition, not causal theory.

---

# 4. Base-Relative Evidence Valuation Framework

Section 4 must instantiate Section 3 rather than redefine it. Reuse `B`, `M`, `Z`, `S`, `\hat\eta_r`, and the exact-budget action rule consistently.

## 4.1 Strong sequential base recommenders

Describe the two reference bases:

- KuaiLive identity-aware Dual-ID sequential base;
- official LiveRec availability-aware and repeat-aware base for Twitch.

Use same-protocol comparator results only to establish credible strong references. Avoid SOTA or leaderboard claims.

## 4.2 Transparent relationship-memory specialist

Use the frozen transferred specialist score:

\[
0.45\,Short+0.45\,Long+0.10\,Popularity.
\]

Explain each component and deterministic tie-breaking. State explicitly that this formula is an interpretable specialist instantiation, not the novelty claim and not an intrinsic measure of relationship evidence quality.

## 4.3 Base-relative relationship-evidence states

For base context length `L`, define:

- `V_L(x)=1` if the target creator appears in the base-visible input sequence;
- `H(x)=1` if the target creator exists in canonical pre-target history outside that visible sequence.

| Empirical state | `V_L(x)` | `H(x)` | Interpretation |
|---|---:|---:|---|
| recent-visible | 1 | any | represented evidence |
| long-horizon-only | 0 | 1 | recoverable but unrepresented evidence |
| unseen | 0 | 0 | unavailable target-specific evidence |

These states form a mutually exclusive and exhaustive analysis partition and are never selector features. Do not assign universal utility signs to them.

## 4.4 Observable features and conditional relative-utility estimator

Estimate `\hat\eta_r(z)` using only serving-observable user/history summaries, candidate descriptors where permitted, and base-confidence features. Do not include target labels, realized utility, relationship-state labels, or analysis-only context-distance variables.

The HGB implementation is operational rather than the source of novelty. Emphasize ranking quality under exact budget; absolute calibration matters only for explicit threshold/cost deployment.

## 4.5 Difficulty control, Oracle, and serving interpretation

- **Difficulty:** use the same observable information and matched model family where feasible; test whether base weakness alone identifies useful specialist invocation.
- **Oracle:** exact-budget selection using realized `Δ_m`; analysis upper bound only.
- **Serving interpretation:** report base cost + estimator overhead + invoked-specialist cost, latency/throughput, and memory/cache footprint. Do not imply that the paper directly optimizes a calibrated event-dependent cost model unless such an experiment is explicitly performed.

---

# 5. Experimental Design

## 5.1 Complementary roles of the two platforms

Treat the platforms as complementary experimental environments rather than interchangeable benchmarks.

### KuaiLive

Use for:

- candidate-regime reversal;
- temporal-regime effects;
- selective decision gains;
- fixed-composition state-specific candidate-regime decomposition.

### Twitch / LiveRec

Use for:

- credible official strong base;
- pre-specified development analysis and untouched held-out test validation;
- evidence-state replication;
- context-capacity intervention;
- Utility/Difficulty/Oracle selection-composition analysis.

## 5.2 Recommendation regimes

Describe sampled-active, full-active, standard temporal, and strict temporal regimes where applicable. Make candidate construction and temporal availability differences explicit because event-level rank utility is candidate-set relative.

## 5.3 Pre-specified held-out validation protocol

Main-text summary:

> **Development-only analysis and policy specification → policy freeze → untouched one-shot held-out TEST evaluation.**

Use `pre-specified`, `policy freeze`, and `untouched held-out test` in the manuscript. Keep immutable hashes, artifacts, chronology, and workflow provenance in reproducibility materials rather than the narrative Results text.

## 5.4 Metrics and statistical inference

Primary metric: NDCG@10.  
Secondary metric: H@10 / HR@10 as appropriate.

Use:

- paired user-level bootstrap intervals;
- exact matched invocation budgets;
- mean ± SD and sign consistency across independent base training seeds.

Do not reinterpret within-seed bootstrap intervals as across-seed confidence intervals.

## 5.5 Evidence hierarchy

### Primary confirmatory evidence

- pre-specified development relationship-state structure;
- untouched held-out TEST replication;
- untouched held-out selective-utility TEST result.

### Primary mechanistic strengthening

- development-only context-capacity intervention with canonical Memory held fixed;
- within-event recoverable→represented transitions;
- fixed-composition KuaiLive candidate-regime decomposition;
- Utility/Difficulty/Oracle selection composition under exact matched budgets.

### Secondary robustness and refinement

- component attribution;
- alternative-explanation stratification;
- positive-delta fractions;
- Memory-parameter sensitivity;
- context-distance consistency and fine recency bins;
- feature-family ablation;
- independent training seeds;
- strong-base comparator checks;
- complexity and efficiency.

This hierarchy should determine result order and claim strength.

---

# 6. Results

Use descriptive result headings rather than `RQ1`--`RQ4` labels in the manuscript.

## 6.1 Aggregate specialist value is regime-dependent

Begin with the paradox rather than the mechanism.

Key KuaiLive aggregate results:

- sampled-active: Base `0.60784`, Always Memory `0.56589`, Selective `0.62102`;
- full-active: Memory−Base approximately `+0.03367`, native Selective−Base approximately `+0.05345`;
- strict temporal: Selective−Base approximately `+0.07282` / `+0.09743`.

### Candidate-regime decomposition

For sampled-active versus full-active, use the same 10,222 events and show that evidence-state prevalence is identical while aggregate Memory−Base reverses from `−0.05125` to `+0.03367`.

| Base-relative state | Sampled Δ | Full-active Δ | Full−Sampled shift | 95% CI |
|---|---:|---:|---:|---:|
| represented | +0.11508 | +0.19261 | +0.07752 | [+0.07046,+0.08472] |
| recoverable-but-unrepresented | +0.17779 | +0.08049 | −0.09731 | [−0.14897,−0.04647] |
| unavailable | −0.20060 | −0.10251 | +0.09809 | [+0.08988,+0.10649] |

Conclusion:

> **Regime dependence is not reducible to changing state prevalence; candidate regime can change the operational marginal value of the same specialist within the same evidence state.**

Do not generalize this fixed-composition conclusion to temporal regimes without direct decomposition evidence.

## 6.2 Base-relative evidence state structures specialist utility

### Pre-specified development → untouched held-out test replication

| Evidence state | DEV Memory−Base | TEST Memory−Base |
|---|---:|---:|
| represented | −0.01995 | −0.01935 |
| recoverable-but-unrepresented | **+0.23097** | **+0.22045** |
| unavailable | −0.19562 | −0.18215 |

Interpret these as Twitch/LiveRec conditional patterns, not universal state signs.

### Context-capacity Base-visibility intervention

Keep canonical Memory fixed (`NDCG@10 = 0.52170`) while varying base context:

| Base context | Base NDCG@10 | Memory−Base | 95% CI |
|---:|---:|---:|---:|
| 8 | 0.52619 | −0.00450 | [−0.00756,−0.00127] |
| 16 | 0.57185 | −0.05016 | [−0.05307,−0.04731] |
| 32 | 0.59663 | −0.07493 | [−0.07766,−0.07227] |

Use within-event state transitions as the principal mechanism result:

| Transition | n | Δ before | Δ after | change | 95% CI |
|---|---:|---:|---:|---:|---:|
| L8→L16 recoverable→represented | 5,055 | +0.29388 | −0.15360 | **−0.44748** | [−0.45767,−0.43730] |
| L16→L32 recoverable→represented | 3,617 | +0.25755 | −0.17474 | **−0.43229** | [−0.44381,−0.42054] |
| L8→L32 recoverable→represented | 8,672 | +0.27782 | −0.14114 | **−0.41896** | [−0.42685,−0.41112] |

Conclusion:

> **The operational marginal value of the fixed relationship specialist is strongly Base-relative: when a larger base context comes to represent the same persistent relationship evidence, specialist advantage contracts sharply.**

Use **interventional support**, not causal theorem, in the wording.

### Component attribution and recency refinement

Report compactly in the main text:

- Long-only on recoverable DEV events: `ΔNDCG@10 = +0.33688`;
- Short-only and Popularity-only: negative in the same regime;
- recency is non-monotonic, including a positive `1–4` pocket.

Move full distance-bin and parameter-sensitivity matrices to Supplementary Material.

## 6.3 Conditional relative utility is not generic base difficulty

Start with exact-budget performance, then explain the result through event composition.

### Selection composition on pre-specified Twitch DEV

Population prevalence:

- represented `52.35%`;
- recoverable `12.54%`;
- unavailable `35.11%`.

| Selector | Represented | Recoverable | Unavailable |
|---|---:|---:|---:|
| Utility selection share | 29.70% (`0.57×`) | 34.13% (**`2.72×`**) | 36.17% (`1.03×`) |
| Difficulty selection share | 11.98% (`0.23×`) | 20.89% (**`1.67×`**) | 67.13% (**`1.91×`) |
| Oracle selection share | 50.39% | 43.00% (**`3.43×`**) | 6.61% |

Conclusion:

> **Base Difficulty disproportionately identifies hard-but-unavailable events, whereas conditional relative Utility more strongly targets events containing recoverable specialist evidence.**

Relationship-state labels remain post-hoc analysis variables and are not used by the selector.

## 6.4 Untouched second-platform validation and robustness

### Twitch/LiveRec held-out TEST

At exact budget `m=6,650` (`15.04%` invocation):

- Base NDCG@10 `0.58211`;
- Always Memory `0.53980`;
- Difficulty `0.58340`;
- Selective Utility `0.58983`;
- Selective−Base `+0.00772`, 95% CI `[+0.00641,+0.00903]`;
- Utility−Difficulty `+0.00644`, 95% CI `[+0.00528,+0.00762]`.

Secondary H@10:

- Base `0.75503`;
- Selective Utility `0.76448`;
- Difficulty `0.75252`;
- Selective−Base `+0.00945`;
- Utility−Difficulty `+0.01196`.

### Utility-estimation headroom

- predicted-versus-realized utility Spearman ≈ `0.173`;
- Oracle exact-budget NDCG@10 `0.64806`;
- current router captures approximately `11.71%` of Oracle gain.

Interpretation:

> **Exact-budget selection depends on utility ranking rather than perfect absolute calibration: the current estimator identifies a useful positive tail despite weak event-level correspondence, while the Oracle gap shows substantial remaining headroom.**

Do not describe current utility estimates as calibrated.

### Robustness summary

Keep main text concise and move detailed matrices to Supplementary Material:

- recoverable-state positive utility remains positive across history length, creator exposure, candidate count, and repeat-propensity strata;
- Memory sensitivity preserves the main Twitch state signs;
- independent base seeds preserve `Selective > Base` and `Utility > Difficulty`;
- same-protocol comparator checks establish credible strong bases without SOTA claims.

## 6.5 Deployment trade-offs

Report accuracy versus invocation rate, latency/throughput, and memory/cache footprint. Treat cost-thresholding as a deployment interpretation and practical frontier, not as an empirically calibrated cost-optimization contribution unless an explicit cost model is evaluated.

---

# 7. Discussion

## 7.1 Operational evidence valuation before evidence integration

Main implication:

> **An auxiliary evidence source should not be judged solely by standalone predictive strength; in this study its operational value is measured through the marginal ranking contribution of a fixed specialist relative to the current base and regime.**

This is the main bridge from live-stream relationship memory to the broader KBS audience.

## 7.2 Evidence state structures but does not determine utility

Use the three states as explanatory coordinates rather than a universal taxonomy of signs.

- Twitch: represented is negative in aggregate, recoverable strongly positive, unavailable negative.
- KuaiLive: represented can be positive, and state-specific utility changes when candidate regime changes despite fixed state prevalence.

Therefore avoid `state → fixed sign`; treat recency and operating regime as modifiers.

## 7.3 Why conditional relative Utility differs from Difficulty

Explain that base weakness is not sufficient: some difficult events contain no target-specific evidence that the relationship specialist can recover. Use selection composition to connect mechanism to decision performance.

## 7.4 Transparency versus architectural complexity

Defend the simple specialist as a scientific design choice: transparency makes evidence availability, component attribution, and marginal value inspectable. Do not argue that the weighted specialist is architecturally superior to learned long-memory models.

## 7.5 Relationship to evidence selection, VOI, deferral, and expert routing

State four boundaries succinctly:

- evidence selection/fusion concerns what information to retain or integrate;
- classical VOI concerns decision value of acquiring information;
- deferral/routing concerns instance allocation among predictors/experts;
- this study characterizes the operational marginal ranking value of one fixed transparent evidence specialist relative to a trained base.

Do not claim general deferral or information-value theory.

## 7.6 Remaining utility-estimation headroom

Use modest predicted-versus-realized association and limited Oracle capture to identify improved relative-utility ranking as the principal future algorithmic opportunity. Under exact-budget decisions, emphasize ordering quality; discuss absolute calibration only for threshold/cost deployment.

## 7.7 Limitations and external validity

Explicitly limit conclusions to:

- evaluated live-stream platforms and candidate protocols;
- strong finite-context sequential bases;
- explicit persistent user–creator relationship evidence as instantiated by the fixed specialist;
- offline ranking outcomes.

Do not imply causal effects on satisfaction, engagement, conversion, or GMV. Do not claim model-independent intrinsic evidence value or generalization to arbitrary auxiliary specialists.

---

# 8. Reproducibility and Data Availability

Add a short formal section immediately before the Conclusion.

Report:

- public datasets and access sources;
- code repository;
- experiment commits and released artifacts sufficient to reproduce reported results;
- preprocessing and candidate construction;
- random seeds;
- development-only analysis, policy-freeze, and untouched held-out test procedure;
- Supplementary reproducibility package with parameter tables, hashes, and detailed robustness outputs;
- Data Availability Statement consistent with Elsevier requirements.

Keep workflow failures/recoveries and low-level CI logs out of the narrative manuscript; preserve them in the audit/reproducibility package where needed.

---

# 9. Conclusion

Close with three points only:

1. **Scientific finding:** the fixed relationship-memory specialist has no fixed global ordering relative to a strong base; its operational marginal ranking value is Base-relative and regime-dependent.
2. **Mechanism:** recoverable persistent evidence is especially valuable in the Twitch setting when absent from the base representation, and specialist advantage contracts when the base comes to represent the same evidence.
3. **Decision implication:** conditional specialist-minus-base utility is more appropriate than generic base difficulty for selective specialist use under matched budgets, although current utility ranking remains far from Oracle.

Avoid introducing new limitations, literature, or claims in the Conclusion.

---

# Main figures and tables

## Figure 1 — Base-relative evidence valuation framework

Show:

- strong finite-context base;
- transparent relationship-memory specialist;
- analysis-only evidence states;
- serving-observable `Z` feeding `\hat\eta_r(z)`;
- specialist-minus-base utility supervision offline;
- exact-budget selective decision as the primary experimental rule;
- cost-sensitive threshold only as a secondary deployment interpretation.

Visually separate offline supervision/analysis variables from online selector inputs to reinforce leakage safety.

## Table 1 — Regime performance and fixed-composition decomposition

Combine compact KuaiLive regime results with sampled-active/full-active state-specific utility shifts. Make visually clear that candidate-regime sign reversal occurs with unchanged state prevalence.

## Figure 2 — Signature mechanism figure

### Panel A — Pre-specified development → untouched held-out test state replication

Show Memory−Base for represented, recoverable, and unavailable states.

### Panel B — Base-context intervention

Show `L=8/16/32`, canonical Memory fixed, and within-event recoverable→represented transitions with approximately `0.42–0.45` decline in specialist-minus-base utility.

Move fine context-distance bins to Supplementary Material unless space permits a small inset.

## Table/Figure 3 — Conditional relative Utility versus Difficulty

Combine:

- exact-budget NDCG@10 / H@10;
- selected-state composition;
- enrichment relative to population;
- Oracle composition as an analysis upper bound.

## Table 4 — Untouched second-platform TEST and robustness summary

Keep primary held-out results in the main table. Put full sensitivity, seed, comparator, and alternative-explanation matrices in Supplementary Material.

## Figure/Table 5 — Accuracy–invocation–latency/footprint frontier

Use only if space permits; otherwise move detailed serving curves to Supplementary Material and retain one compact deployment summary in the main text.

---

# Supplementary Material structure

## S1. Dataset preprocessing and candidate construction
## S2. Pre-specified validation protocol and reproducibility details
## S3. Full base comparator results
## S4. Memory component and parameter sensitivity
## S5. Context-distance and recency-bin analyses
## S6. Alternative-explanation stratification
## S7. Feature-family ablations and training-seed results
## S8. Complexity, latency, throughput, and footprint details
## S9. Additional bootstrap intervals and H@10 tables

---

# Claim discipline to maintain during drafting

Supported manuscript-level claims:

- the fixed relationship-memory specialist is regime-dependent rather than globally ordered against the base;
- `Δ_m` operationalizes the specialist's marginal ranking contribution relative to a fixed base and is not intrinsic model-independent information value;
- Base-relative evidence state strongly structures specialist utility in Twitch/LiveRec;
- recoverable-but-unrepresented evidence is the dominant positive Twitch relationship-memory regime;
- pre-specified development state structure reproduces on untouched held-out TEST;
- controlled context-capacity intervention supports a Base-relative visibility interpretation;
- evidence state does not uniquely determine utility across regimes;
- conditional relative Utility and Difficulty select materially different event compositions at the same exact budget;
- Utility better enriches recoverable events, while Difficulty disproportionately selects unavailable events;
- exact-budget selection requires useful utility ordering rather than perfect absolute calibration;
- selective Utility improves strong bases in the evaluated settings and transfers under untouched second-platform evaluation;
- substantial Oracle headroom remains.

Avoid claims of:

- a universal theory of auxiliary evidence valuation;
- intrinsic or model-independent value of relationship evidence;
- fixed utility signs for represented/recoverable/unavailable states;
- a universal context-length threshold;
- causal proof that visibility alone determines specialist utility;
- generic novelty in evidence selection, gating, MoE, Learning-to-Defer, long/short-term modeling, or feature fusion;
- SOTA / leaderboard superiority;
- calibrated event-level utility prediction or near-Oracle routing;
- generalization beyond the evaluated live-stream settings or arbitrary auxiliary specialists.