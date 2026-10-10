# Section 7 Discussion — KBS submission-oriented writing plan

**Date:** 2026-10-10. **Status:** Writing plan only; Section 7 has **not** been inserted into `main.tex`. **Canonical source:** [latest argument-restructured manuscript](main.tex), after [four-stage academic audit](KBS_FOUR_STAGE_ARGUMENT_RESTRUCTURING_REVIEW_2026-10-10.md); [approved outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md); [unified Supplementary S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md). Official journal scope: [KBS/Elsevier](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051); general publisher structure guidance: [Elsevier Guide for Authors](https://www.elsevier.com/subject/next/guide-for-authors) and [Elsevier Discussion advice](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/). These guide *academic presentation*; no unsupported KBS-specific mandatory Discussion word count is claimed.

## 1. Section 7 central argument — what the Results collectively mean

**Manuscript thesis to interpret, not redefine:** *Relationship memory has decision value when the ranking supplied by a specified historical specialist improves upon an incumbent Base for a particular candidate environment; this benefit is heterogeneous and only partly predictable before the target outcome.*

The three fixed contributions **C1 operational Base-relative evidence valuation**, **C2 history- and candidate-regime dependence**, and **C3 pre-outcome Utility-based expert choice** already have evidence in Chapters 3–6. Discussion must now interpret their **joint** consequence for the design of knowledge-based recommender systems. The distinction is not "more historical data yields better rankings" or "we invented optimal Learning-to-Defer", but "evidence is valuable through the incremental ranking action it makes preferable."

**Logical arc:** What is evidence value relative to? (7.1) → Why can it change with context/candidates? (7.2) → Can this value guide a decision? (7.3) → What evidence supports that inference and at what scope? (7.4) → What general *design principle* follows? (7.5).

**Style contract:** Positive, precise scholarly finding first; one substantive evidence anchor; one inference conditional when necessary. Avoid chronological account of experimental revisions, named GitHub runs/checkpoints, reviewer defenses, "we did not", and serial negative-claim sentences. Equally, **do not remove negative research results or validity boundaries**. Discussion interprets, Results reports; method hyperparameters/tables remain in Sections 4–6 and S1–S9. No additional figure/table is required.

**Target length:** approximately **1,050–1,350 English words**, not a KBS-specific regulatory limit. Five existing approved subsections, **11–13 concise paragraphs**, typically 2/2–3/2–3/3/2 paragraphs respectively; each subsection makes one distinct scientific point. Add at most one brief transition to Conclusion; avoid a second complete conclusion at 7.5.

## 2. Evidence tiers and links to prior chapters

| Evidence / interpretation role | Main source | Supplement | Scientific interpretation allowed | Never say |
|---|---|---|---|---|
| Fixed expert versus Base overall, target-state heterogeneity (C1) | §3 \(\Delta_M\), §4 target-relative states, **§6.1** | S1/S2/S4/S6 | Fixed relationship evidence has context-dependent *relative ranking* value. Twitch frozen TEST Base 0.58211 vs Memory 0.53980, overall Δ **−0.04232**; recoverable Δ **+0.22045** over n=5,539. | Target-state category is available when routing; observed states causally prove what the Base learned |
| Candidate universe and score reference (C2) | §3 regimes, §5 crossed scoring, **§6.3** | S1/S2/S5/S8 | KuaiLive 10,222 same-user fixed-checkpoint post-hoc matched analysis: sampled Δ **−0.04120**, full Δ **+0.04631**, shift **+0.08751**. Membership-reference algebra (+0.08827, −0.00076) describes allocation under a specific scoring procedure. | Candidate count alone causes shift; this is a newly proven general sampled-metric theorem or independent frozen test |
| Selective relative-Utility decisions (C3) | §3 \(\eta_r\), §4 14 features, §5 DEV OOF, **§6.2** | S2/S7 | Frozen Twitch TEST n=44,221: Utility−Base **+0.00772**; Utility−Difficulty matched-count **+0.00644**; selected realized Δ **+0.05136** versus unselected **−0.05890**; Spearman **0.173**; ~**11.7%** hindsight Oracle margin recovered. | Fully calibrated individual-level causal returns, universal optimal routing, online equal-count Difficulty threshold, or general L2D algorithm |
| Conditional interpretation and costs | §6.4/§6.5 | S3/S4/S6/S7/S9 | Feature-family, Long-only/Full and Base length diagnostics clarify contexts; KuaiLive warm CPU Base 0.991ms versus HGB 2.007ms quantifies cost in a separate protocol. | L8/L16/L32 isolates history length with fixed model parameters; low invocation rate proves efficiency savings |

Maintain the **three distinct uncertainty/evidence tiers**: frozen one-shot Twitch TEST for the Utility policy; Twitch DEV diagnostic subgroups/budgets for interpretation; previously examined KuaiLive TEST retrospective P0/P1/P2 candidate comparisons (three trained seeds ≠ three datasets; nine negative-draw conditions ≠ nine datasets). Never combine statistics across ranking units (Twitch streamers versus KuaiLive rooms) or model checkpoints.

## 3. Subsection blueprints and paragraph-level functions

### 7.1 Operational Value Is Base- and Context-Dependent
**Suggested budget: 180–230 words, 2 paragraphs.**

**Scientific question:** Why is the existence of persistent relationship history insufficient to establish its *value*?

- **Paragraph 1, central interpretation:** Start with the operational definition \(\Delta_M=u_K(M,x)-u_K(B,x)\), not a recap of how it was computed. Explain that a relationship specialist can be inferior on average and still provide a large positive relative gain where eligible older target relationships lie outside Base's input: **overall −0.04232 vs recoverable +0.22045**. The point is **nonuniform complementarity relative to the incumbent**. Distinguish evidence being available from an additional ranking actually being better. Do not infer the Base's internal representation state from its input length.
- **Paragraph 2, scientific context:** Interpret stronger separately trained Base contexts (S6), Long-only versus Full Memory (S4) as evidence that specialist advantage is relative to both the Base and the specialist specification. Compare selectively to knowledge fusion/reliability and negative-transfer prior art, e.g. `\cite{zhu2026mifusr,huo2026reliability,peng2025negative}`, and optionally decision-theoretic VOI `\cite{abbas2025voi}`. Keep distinction to **operational ranking action** versus inherent semantic value; avoid claiming an information-theoretic measurement or causal component effect.

**Candidate opening idea, not final prose:** “The empirical value of relationship history is best understood as an incremental ranking decision rather than a property of the history alone.”

**End-of-subsection handoff:** If ranking utility is Base-relative, it must also be measured in the appropriate **candidate-ranking context**, which leads to 7.2.

### 7.2 Interpreting Conditional Evidence and Candidate Regimes
**Suggested budget: 240–295 words, 3 paragraphs.**

**Scientific question:** Why should a positive historically recoverable subgroup in Twitch not become a universal rule for every candidate-ranking regime?

- **Paragraph 1 — reconcile complementary perspectives:** Twitch recoverable-history group is useful for explaining observed relationship-state heterogeneity. In KuaiLive, state membership stays identical under paired sampled/full protocols, but the aggregate specialist--Base ranking ordering flips; 4,589 represented / 206 recoverable / 5,427 unavailable, and state prevalence cannot explain the shift. The substantial represented/unavailable contributions mean candidate-regime value **is not reducible** to how much target history lies outside an input window. This is the crucial C1+C2 synthesis.
- **Paragraph 2 — what is new relative to prior metric literature:** The literature already establishes sampled-ranking metric inconsistency (`\cite{krichene2020sampled}`). Our *specific* additional perspective is the **matched specialist-versus-Base incremental-utility decision** and a crossed ranked-candidate / branch-score-standardization descriptive allocation. The P0 +0.08751 shift is mainly allocated to ranked membership (+0.08827) versus a small normalization contribution (−0.00076). Candidate **count, identity, ranking competition** move together, so this partition cannot identify causal candidate-size effects. Avoid a new sampled-metric theorem claim.
- **Paragraph 3 — restrained robustness significance:** Three fitted checkpoint seeds and nine fixed-checkpoint negative draws support directional stability within the tested KuaiLive regimes; not transportability, causal mediation or independent cohorts. L8/16/32 independently trained Base models cannot isolate visibility effects. Preserve a single retrospective source qualifier (KuaiLive post-hoc) without a paragraph-long list of experimental run IDs.

**Candidate topic sentence:** “The same relationship evidence can have different incremental ranking value even when the evaluated users, target-history states and trained scoring functions are held fixed.”

**End-of-subsection handoff:** If value varies with both history and the ranking environment, the practical next issue is whether to **predict relative benefit** from observables instead of using a static expert.

### 7.3 From Relative Utility to Selective Decisions
**Suggested budget: 215–265 words, 2 or 3 paragraphs.**

**Scientific question:** What exactly is gained by predicting the *difference* in expert and Base utility, as opposed to identifying difficult Base requests?

- **Paragraph 1 — decision interpretation:** Use identity \(\mathbb{E}[a(Z)\Delta_M]\) from Eq.~`\eqref{eq:expected-selective-gain}`: event selection matters because the alternative ranker may not solve the same problems the Base finds difficult. Link to fixed Twitch TEST Utility−Base +0.00772 and Utility−Difficulty equal-count +0.00644. Conditional observed selected Δ +0.05136 vs unselected −0.05890 emphasizes the utility of *where the specialist is used*. Make clear, in one clause, that Difficulty top-m uses **retrospectively matched** realized call count while Utility threshold is DEV-frozen.
- **Paragraph 2 — compare with prior routing work and calibration limits:** Learning-to-Defer provides the established routing framework (`\cite{mozannar2020defer,narasimhan2022posthoc,mao2025mastering}`), while the present study contributes a **specific knowledge-source valuation target and a frozen empirical decision test**. Predictive correlation 0.173 and 11.7% of hindsight two-ranking Oracle headroom recoverable establish decision usefulness **without** precise per-event utility forecasts or generalized optimality. DEV feature-family contrasts indicate history + Base descriptors are complementary at tested counts, not a universally calibrated selection model.
- **Optional paragraph 3 (short):** If manuscript rhythm benefits, connect the selection result to system architecture: conditional expert choice can be evaluated against all-Base and all-Memory even when the specialist's global mean is worse. Keep generic cost optimization for 7.5 and actual cost restrictions for 7.4.

**Candidate topic sentence:** “Selecting evidence should depend on its anticipated benefit over the incumbent, not solely on the incumbent's uncertainty or difficulty.”

**Handoff:** Useful selective decisions require reliable **evidence and resource accounting**, addressed in 7.4.

### 7.4 Validity Boundaries
**Suggested budget: 215–270 words, 3 compact paragraphs.**

This must be a **single coherent scope section**, not a defensive inventory of every excluded claim. Start by noting what the experiments establish, then explain which additional inferences would need additional evidence.

- **Paragraph 1 — evidentiary identification:** The one-shot DEV-frozen Twitch TEST justifies the claim of a fixed selector's offline ranking gain. Twitch DEV subgroup, feature and context tests are explanatory. KuaiLive candidate P0/P1/P2 use previously inspected TEST events and provide within-protocol robustness, not a second independent prospective selector test. Three checkpoint initializations and three candidate-list streams address separate variations but share the same observed users.
- **Paragraph 2 — observability and evaluation:** Target-relative evidence states and recurrence distance are retrospective, unlike 14 pre-outcome selector features. Room-level sampled/full candidates, one-positive labels, eligibility/missingness, and Twitch ten-minute first/last observation boundaries influence the meaning of ranking utility; context-length Bases are separately trained. Thus, observed associations do not identify target-specific causal histories or external engagement effects.
- **Paragraph 3 — serving/resources/generalization:** Twitch 15.04% Memory invocation rate is not a latency saving; separate KuaiLive warmed CPU scoring adds +1.016ms (2.03x Base) with archived route-mask replay. Per-request live cost, throughput, budget policies and online user/business outcomes remain unmeasured. No gate was transferred zero-shot between platforms. These are concrete additional experiments required for broader deployment or external-generalization claims, not defects that should dominate the section.

**Positive-scoped opening:** “The combined experiments identify reliable *within-protocol ranking decisions* and reveal the conditions under which their interpretation changes.” Then locate the boundary without reflexively repeating 'not...' in each clause.

### 7.5 Implications for Knowledge-Based Recommendation
**Suggested budget: 185–235 words, 2 paragraphs.**

**Scientific question:** What can a knowledge-based recommender designer learn even without universal policy transfer or online A/B evidence?

- **Paragraph 1 — three derived system design principles in prose, not a numbered list:** (i) assess an auxiliary evidence ranker by **paired incremental decision utility** relative to a specified Base; (ii) characterize historical evidence and candidate regimes at the same time, separating retrospective diagnosis from observable decision features; (iii) evaluate conditional selection by both *ranking quality* and *computation incurred*. These are cautious general **methodological implications**, not demonstrated online outcomes. Tie back to C1/C2/C3 in a single synthesis sentence.
- **Paragraph 2 — prioritized research directions:** Independently frozen additional datasets and independent cohort/temporal replications; factor-controlled candidate-hardness experiments that separate candidate size, composition and standardization; learned budget-aware and calibrated Utility predictors with joint quality/cost targets; production A/B and truly measured runtime resource accounting. Present a compact forward-looking agenda rather than individual defenses.

**Ending transition to eventual §8 Conclusion:** Reaffirm the distinction between **possessing historical evidence** and **knowing when it improves a ranking decision**, without re-enumerating all numeric results.

## 4. Citation and comparison placement

Already-present vetted bibliography keys; **do not add extra 2026 references merely for count**. Suggested total approximately **5–8 in-text citation keys, appearing in 3–5 citation clusters**, adjusted to prose necessity:
- **7.1:** `zhu2026mifusr`, `huo2026reliability`, `peng2025negative` (evidence complementarity/redundancy), optional `abbas2025voi` (decision utility, distinct construct).
- **7.2:** `krichene2020sampled` (the existing published 2022 *CACM* version); optional domain sources `rappaz2021liverec`, `qu2026kuailive` only when needed.
- **7.3:** `narasimhan2022posthoc`, `mozannar2020defer` and optionally `mao2025mastering`; **do not** claim inventing L2D or proving an optimal policy.
- **7.4:** focus on internal evidence and limitations, no unnecessary citation.
- **7.5:** prioritize original discussion/synthesis, at most one relevant prior comparison.

**Math/reference hygiene:** Mention \(\Delta_M\) and \(\eta_r\) only where decision-theoretically useful. Use existing `\ref{sec:relative-utility}`, `\ref{sec:results-heterogeneity}`, `\ref{sec:results-decision}`, `\ref{sec:results-regimes}`, `\ref{sec:results-robustness}`, `\ref{sec:results-efficiency}` and `\eqref{eq:expected-selective-gain}` sparingly. No new theorem, equations, conceptual jargon or tables necessary.

## 5. Reviewer-style risks to resolve while drafting

| Potential KBS objection | Drafting mitigation |
|---|---|
| "The value measure is just a subtraction and not novel." | Explain the research question and evidence/decision integration, not claim subtraction is a novel mathematical theory. |
| "Twitch conditional subgroup is label-defined and unavailable for deployment." | Separate retrospective diagnosis (7.1/7.2) from pre-outcome feature Utility routing (7.3). |
| "C2 simply replicates known sampled metric reversal." | Cite published sampled-metric prior art and foreground **fixed expert-versus-Base** choice and crossed z-score reference interpretation, without claiming causal effects. |
| "Why Full Memory when Long-only scores higher in recoverable DEV?" | Describe conditional trade-off in 7.1; avoid post-hoc optimized specialist assertions. |
| "Is selection advantage fairly compared to Base Difficulty?" | State matched **realized** count / retrospective difficulty top-m versus fixed Utility threshold; distinguish objective from online budget. |
| "How much practical value is there if predictive correlation is low?" | A positive frozen TEST decision gain can coexist with low pointwise predictive fidelity; mention 11.7% Oracle capture as a bounded improvement, not optimism about full optimality. |
| "What if full-candidate evaluation changes conclusions?" | 7.2 is an explicit statement that operational value depends on candidates; do not extrapolate KuaiLive to the frozen Twitch policy. |
| "Does a low invocation rate prove speed?" | Report controlled KuaiLive measured overhead and absent Twitch serving test in 7.4, do not claim cost reduction. |
| "Is the paper actually knowledge-based?" | Make history evidence an interpretable **decision-relevant source** with conditional valuation, avoiding unmeasured semantic knowledge/explainability claims. |
| "Are the many negative/limit statements a sign that experiments fail?" | Lead with positive scientific interpretations, group limitations in 7.4, and retain negative **empirical facts** centrally where they motivate the method. |

## 6. Writing and acceptance workflow

1. **Draft 7.1 and 7.2 together for conceptual consistency**, but commit/check each requested subsection independently if the author continues staged writing. Section 7.2 must not re-summarize §6.3 factorial metrics at length; source each inference.
2. **Draft 7.3** grounded in frozen one-shot Twitch policy, distinguish relative Utility from Base Difficulty and the Oracle, and avoid implying the retrospectively matched comparator was deployable.
3. **Draft 7.4** once preceding interpretations are stable; collect *only consequential* validity boundaries instead of repeating every Results disclaimer. No GitHub run IDs, historical artifact conflicts, raw-data SHA or analysis chronology in final prose.
4. **Draft 7.5** with a genuinely useful knowledge-based-recommender design synthesis and tightly prioritized future work; do not steal §8 Conclusion's role.
5. **Cross-chapter review:** Compare sentences against §§1–6, Outline C1–C3 and S1–S9. Every numerical statement must match exact original provenance, and every generalized sentence must be at the scale supported by observations.
6. **Journal-style check:** Five approved titles in order, approx. 1,050–1,350 English words, coherent topic sentences, at most strategic existing citations, no new figure/table or pseudotheorem, calibrated scientific language, no history of experiment execution.
7. **Source/build gate (only after explicit request to draft):** Insert `\section{Discussion}` with the five subsections **before the bibliography** in canonical `main.tex`; confirm stable bibliography keys and references; rebuild elsarticle via GitHub Actions and visually inspect beginning/end of 7.1–7.5 and boundary with future §8.
8. **Do not start §8 Conclusion or Abstract** until Section 7 receives scoped scientific and reviewer-style tightening. This respects the approved staged writing process.

**Editorial endpoint:** Section 7 succeeds when a KBS reviewer can state in one sentence **what has been learned about the decision value of historical knowledge**, distinguish that from an extra fusion architecture or generic expert gating theorem, identify which of C1–C3 support that claim, and understand the scope without reading a defensive checklist.
