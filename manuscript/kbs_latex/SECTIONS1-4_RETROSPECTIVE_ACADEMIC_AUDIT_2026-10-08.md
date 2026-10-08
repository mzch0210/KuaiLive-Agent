# KBS manuscript: retrospective academic audit of Sections 1–4

## Follow-up status verification (2026-10-08)

This document preserves the **original findings before repair**. Its recommendations are historical, not a description of remaining defects in the current [canonical LaTeX manuscript](main.tex).

| Original issue | Current status | Evidence in manuscript |
|---|---|---|
| PF1 P0: `\\Delta_m` symbol overlaps budget `m` | **FIXED** | Specialist utility uniformly `\\Delta_M`; invocation count remains `m` |
| F2 P0: fusion coefficients read as globally fixed at 0.1/0.9 | **FIXED** | Section 4.1 explicitly limits the coefficients to the primary sampled-active evaluation |
| I1 P1: Introduction overloads findings | **FIXED** | Two empirical observations and three compact contributions replace the detailed result inventory |
| I3 P1: unclear experimental provenance of introduction claims | **PARTIALLY CLOSED** | KuaiLive same-checkpoint and three-seed evidence now appears in Section 6.1; the separately frozen Twitch claim awaits formal Section 6.4 drafting |
| RW1/RW2 P1: citation catalog and repetitive negative positioning | **FIXED IN PROSE** | Conceptual synthesis by research family, one Research Gap closing; redundant positioning table removed |
| RW4 P1: recent citation title/DOI/publication verification | **CLOSED (2026-10-08)** | All 24 Related Work citations and 2 additional BibTeX entries checked against finalized journal/proceedings metadata; official URLs and date correction committed. See [publication audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md). |
| PF2/PF3 P1: protocol implementation and speculative cost optimization mixed into formulation | **FIXED** | Section 3 retains formal pointwise rule and matched-count definition; unevaluated cost equation removed |
| F1/F3/F4 P1: repeated motivation, Twitch eligibility and training/OOF settings in framework | **FIXED** | Section 4 now emphasizes model/memory/states/observable features; concrete temporal eligibility and selection procedures are in Section 5 |

**Build evidence:** [GitHub Actions run 37757306655](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37757306655) completed successfully after the source revisions and Section 6.1 insertion. This verifies LaTeX compilation, not external bibliographic authenticity, readiness of incomplete results sections, or journal acceptance.

**Remaining P1 closure actions:** the Related Work publication-version check is complete; complete the Twitch held-out result subsection with its original frozen provenance, then cross-check the Introduction's Twitch statement. Confirm publication metadata updates or corrections again at submission. No P0 mathematical notation or fusion-coefficient defects remain in the inspected current source.

---

**Date:** 2026-10-08  
**Scope:** Actual Sections 1–4 of [the LaTeX manuscript](main.tex), evaluated against the newly restructured Section 5 and the frozen experimental protocols.  
**Change control:** The audit does **not** modify Sections 1–4. Critical terminology/notation changes require a focused, cross-section review before applying them.  
**Review standard:** Scientific rationale in Introduction, scholarly synthesis in Related Work, coherent mathematics in Problem Formulation, methodological definition in Framework, reproducible study design in Experimental Setup, findings in Results, and interpretation in Discussion. These are editorial criteria, not mandatory KBS subheading counts.

## Summary

| Section | Current academic status | Similar problem to former Section 5 | Priority |
|---|---|---|---|
| 1. Introduction | Strong research motivation but an overlong and heavily qualified preview of results | Moderate; compressed results and repeated self-defense | P1 |
| 2. Related Work | Relevant neighboring work but catalog-style recent-study descriptions and repetitive negative positioning | Moderate-high; reference inventory rather than integrated synthesis | P1 |
| 3. Problem Formulation | Good mathematical abstraction; some protocol and untested cost extensions in the formal core | Limited; conceptual sprawl rather than an experiment diary | P0 symbol clarity, P1 scope |
| 4. Base-Relative Evidence Valuation Framework | Necessary method definitions but substantial overlap with dataset/protocol and evaluation sections | High in parts; duplicates implementation protocol and defensive caveats | P0 parameter scope, P1 restructuring |

## 1. Introduction

**Strength:** The first paragraph poses the scientific problem of incremental ranking utility beyond a trained sequential base; the contribution list correctly avoids claiming a new general learning-to-defer theorem.

**I1 / P1 — Excessive results preview.** The paragraph beginning “Our empirical results show why this distinction matters” covers KuaiLive regime reversal, Twitch diagnostic states, their held-out replication, a development-only context-capacity shift of 0.42–0.45, and retraining qualifications. A reader must process much of Sections 6–7 before seeing the method. **Recommendation:** Preserve at most two evidence anchors: the matched candidate-regime sensitivity and the primary frozen held-out selective decision result. Move the capacity number and competing explanations to Results/Discussion.

**I2 / P2 — Repeated protective claims.** The introduction repeatedly states what operational valuation is not, what routing novelty is not, and what cannot be causally inferred. Retain one compact scope qualification in the final contribution paragraph; do not delete the important distinction from intrinsic information value.

**I3 / P1 — Empirical claim provenance.** The third contribution mentions “independent base seeds.” Keep this claim only when the reported Section 6 experiment explicitly identifies the seed panel, its checkpoints, variability, and diagnostic versus frozen held-out status. The follow-up seed workflow [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645) reports success but its results require paper-specific scientific review before being promoted as a headline claim.

**I4 / P2 — Premature taxonomy detail.** The complete represented/recoverable/unavailable taxonomy is explained in Introduction, then formally redefined in Section 4. Keep the conceptual intuition in Section 1 and its exact operational definition in Section 4.

## 2. Related Work

**Strength:** The paper identifies four relevant areas: long-horizon sequential recommendation, evidence integration/reliability, learning to defer and expert routing, and dynamic live-streaming recommendation.

**RW1 / P1 — Citation-by-citation list.** The long “Auxiliary Evidence Integration” subsection reads as a catalog of 2025/2026 multihead gating, information fusion, denoising, KAPER, reliability, QA gating, negative-transfer and value-of-information methods. Reorganize this subsection around two conceptual families: evidence construction/integration and evidence reliability/conditional deployment. Compare their optimized target against specialist-minus-base ranking utility.

**RW2 / P1 — Positioning repeated through negation.** Each subsection and the six-row Positioning Summary table repeat variations of “these works do X; we instead do Y.” Make the research gap a positive, testable statement once at the end. Remove duplicate closings elsewhere.

**RW3 / P2 — Redundant table.** The positioning table currently reproduces several adjacent prose paragraphs. Either omit the table or shorten prose and add genuinely informative dimensions, such as optimization target, evaluated signal, and whether the expert is fixed.

**RW4 / P1 — Reference verification still required.** Current BibTeX keys are not evidence that every recent article's title, publication status, DOI and attribution are correct. Check publisher articles or indexing records for contemporary work. This audit does not allege a particular reference is fabricated.

## 3. Problem Formulation

**Strength:** The event-context definition, single-target NDCG utility, model-relative contrast, conditional expectation and regime decomposition form a coherent formal chain. This chapter is generally written as an academic problem definition, not a lab notebook.

**PF1 / P0 — Ambiguous notation.** The notation Δ_m means Memory-minus-Base utility, while the same chapter defines m as the count of specialist invocations for an equal-count comparison. This creates a misleading impression that the utility contrast itself is parameterized by the invocation budget. **Recommended precise fix:** reserve m for the invocation count and rename the specialist contrast throughout the manuscript, e.g., Δ_M(x), with associated equation and discussion updates. This preserves the scientific definition and requires a synchronized replacement rather than a single isolated change.

**PF2 / P1 — Evaluation implementation inside formalism.** The “Development-Frozen Selective Invocation and Matched-Budget Evaluation” subsection discusses OOF threshold selection, stable row-index tie rules and test batch invocation counts. Keep the abstract selection rule and equal-count comparator; move specific training/fold/tie implementation to Section 5 or the supplement.

**PF3 / P1 — Unmeasured cost extension.** Equation eq:cost-rule introduces an expected invocation-cost variable and lambda but the paper does not fit or evaluate a calibrated cost model. Retain it only if the decision-theoretic framing requires it; otherwise place the extension in Discussion or the supplement. It may otherwise prompt a reviewer to ask for cost-effectiveness experiments beyond the established claims.

**PF4 / P2 — Multiple layers of caveats.** “Not an intrinsic value,” “not causal,” “Oracle not available online,” and “not a new theorem” reappear across the chapter. Each important distinction should be stated once at the mathematical point where it is needed; broader limitations belong in Discussion.

**Keep intact:** candidate-regime-specific event identities, the expected selective gain identity, exclusion of target-dependent variables from the serving features, and the decomposition of state prevalence versus conditional utility.

## 4. Base-Relative Evidence Valuation Framework

**Strength:** The Base/Memory/pre-outcome gate separation is clear, Figure 1 identifies online versus retrospective information, and the fixed Memory formula and diagnostic three-state definition merit full display in the main manuscript.

**F1 / P1 — Introductory mission statement repeats Section 1.** Three scientific purposes are enumerated again at the start. Replace with a concise explanation of the modules and Figure 1, avoiding a second contribution list.

**F2 / P0 — Fusion alpha is not universally 0.1/0.9.** The Section 4.1 statement “Their linear combination uses development-selected room and streamer weights of 0.1 and 0.9” reads as a global setting. It is the original sampled-active policy configuration; the completed same-checkpoint paired diagnostic uses a separately selected alpha_room of 0.125. The new Section 5 correctly distinguishes experimental references. **Minimum corrective sentence:** “For the primary sampled-active policy evaluation, the development-selected room and streamer fusion coefficients are 0.1 and 0.9; regime-specific diagnostics use coefficients specified with their protocols.”

**F3 / P1 — Twitch data eligibility restated within the algorithm.** The Specialist subsection explains ten-minute observation semantics, first-versus-last historical eligibility and strict-split boundaries. These belong in new Section 5.1 and the supplement. Keep the general definition of eligible pre-target history and a short cross-reference.

**F4 / P1 — HGB and controls mixed with framework presentation.** Feature semantics belong in Section 4, but the exact HGB hyperparameters, OOF threshold grid, TEST freeze, and how the Difficulty/Oracle budgets are counted belong predominantly in Sections 5.2–5.3. Reduce repeated descriptions and retain one explicit pre-outcome feature-permission statement.

**F5 / P2 — Project implementation tokens.** Literal fr_ctx and fr_rep flag names, “frozen exports” and multi-split experiment variations reduce academic readability in the main framework. Place flags and concrete file/protocol metadata in the supplement; describe context and repeat components at the algorithm level.

**F6 / P2 — Dense disclaimers around states.** Multiple consecutive sentences note that visible history need not be learned, states do not imply utility signs, and state membership is not causal. Keep the operational definition and serving-time leakage rule; relocate the broader interpretation limitations to Discussion.

**F7 / P2 — Figure visual layout.** The method flow is relevant, but the large caption and TikZ node widths merit a PDF visual check. This is a presentation question, not evidence that the algorithm is invalid.

## Cross-chapter priorities

1. **P0 scientific consistency:** resolve the Δ_m / m symbol collision manuscript-wide; qualify the original 0.1/0.9 fusion coefficients in 4.1; ensure each Introduction result maps to one traceable experiment.
2. **P1 structural alignment:** synthesize Related Work, remove unnecessary cost-model diversion if not evaluated, relocate data eligibility and HGB controls from Section 4 to Section 5/supplement, and shorten Introduction results.
3. **P2 polish:** consolidate negative disclaimers rather than multiplying them; decide whether the Related Work positioning table adds unique value; review Figure 1 for typographic density.
4. **Submission verification:** complete Table 1 input sizes and chronology from frozen data manifests; verify all recent paper bibliography entries and durable experiment artifacts; examine final PDF, particularly adjacent tables and equations.

## Section 5 change already completed

Section 5 was rewritten in place in the same LaTeX file as a scientific evaluation design. The five subsections are Datasets and Prediction Tasks; Baselines and Compared Methods; Experimental Protocols; Evaluation Metrics and Statistical Analysis; and Implementation Details. Two tables and the paired regime-shift definition remain. Approximately 1,954 words were reduced to 1,365 words, but no scientific result was created by editing prose. Earlier six-section reviewer copy-edit notes remain historical material rather than instructions for the new manuscript.

**Academic judgement:** The manuscript is now better organized in Section 5, but Sections 1–4 still need selective revisions. Section 3 has relatively low experiment-diary risk; Section 4 and Related Work have larger structural repetition risks. This document is an internal reviewer-style critique, not a real journal reviewer decision or a claim that the publisher mandates a particular word count.

## Editorial guidance

- Elsevier, “Your Paper Your Way” (general editorial reference specific to Next journals, **not** the KBS journal-specific Guide for Authors): https://www.elsevier.com/en-gb/subject/next/guide-for-authors
- Elsevier, “How to conduct a review”: https://www.elsevier.com/reviewer/how-to-review
- Elsevier, “The condensed read: How to structure a science paper”: https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper

**Journal-specific guidance:** The KBS publisher's official [journal scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) confirms its interest in recommender systems and balanced theory/practical AI. The [KBS Guide for Authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors) should be checked separately at submission; its full live text could not be retrieved from the browser in this audit. None of this report's suggested word counts, subsection counts, or editorial preferences are asserted as KBS-enforced requirements.
