# Section 8 Conclusion — KBS submission-oriented writing plan

**Date:** 2026-10-10  
**Target journal:** *Knowledge-Based Systems*  
**Status:** WRITING PLAN APPROVED FOR DRAFTING; **§8 has not yet been inserted into canonical \`main.tex\`.** This file records the precise scholarly task, evidence obligations and acceptance tests for the *next* drafting step, not the completed Conclusion.  
**Current manuscript:** [main.tex](main.tex), final Stage-4 seven-chapter scientific/technical acceptance source commit [70adf0c](https://github.com/mzch0210/KuaiLive-Agent/commit/70adf0c4620fa7454f6a4fd71e955f0eb9c32721), file blob \`37c0b5fbefb945174aa13b18da80d8af87b502a3\`.  
**Authoritative plan and scientific scope:** [submission-oriented outline, §8](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md), blob \`89734dbec9f852fcb728b2ef3a767d19ebe22109\`.  
**Validated evidence:** [integrated supplementary S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md), blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`.  
**Acceptance baseline:** [Stage-4 independent KBS scientific and PDF audit](STAGE4_INDEPENDENT_KBS_SUBMISSION_REVIEW_2026-10-10.md); [full argument revision record](KBS_OUTLINE_ALIGNED_ARGUMENT_REVISION_PLAN_2026-10-10.md).

## 1. Editorial verdict: preserve the existing scientific thesis, do not redesign the Conclusion

The outline specifically prescribes that the still-unwritten §8 must **synthesize three findings without adding numerical results**:

> (i) persistent relationship history is conditionally useful against a strong Base; (ii) a DEV-frozen relative-Utility selector improves untouched Twitch ranking despite the expert's inferior aggregate results; and (iii) KuaiLive's sign reversal persists across three model seeds and is described primarily by ranked-candidate changes in a post-hoc algebraic attribution. Scope remains operational, offline, model- and regime-dependent.

The preceding seven chapters have already developed a consistent question:

> **When does a fixed historical-relationship specialist produce incremental ranking value relative to the incumbent model and eligible candidate environment, and can that value guide selective invocation before the outcome?**

The Conclusion must **close** this question with a compact synthesis of **C1**, **C3** and **C2**—in the actual evidence sequence **Twitch conditional-value → Twitch selective-decision validation → KuaiLive candidate-context analysis**. It should not introduce an additional hypothesis, theorem, algorithm, experiment, business result or generalized policy transfer.

**KBS positioning:** The journal's [official aims and scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) encompass AI-based knowledge systems, recommender systems and intelligent decision support, with both theoretical and applied contributions. The Conclusion should therefore emphasize the knowledge-decision inference: **availability of relationship evidence, its incremental utility against the current Base, and the decision to use it are distinct but connected questions**. This study operationalizes this connection; the subtraction formula or L2D notion is not itself presented as a new general theory.

**General editorial support, not a KBS-specific length mandate:** Elsevier's [scientific-paper organization advice](https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper) treats the Conclusion as a short synthesis of advances and implications. Its separate [Next-journals Guide for Authors](https://www.elsevier.com/subject/next/guide-for-authors) describes a short Conclusions section but **must not** be represented as the controlling *KBS-specific* author guide. The [KBS Guide for Authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors) returned HTTP 403 during automated review; do not assert an exact KBS-required conclusion length or format from this restriction.

## 2. Structural design — three paragraphs, no internal headings

**Proposed source form:** one numbered \`\\section{Conclusion}\` and optionally its unique \`\\label{sec:conclusion}\`, inserted **after all §7 paragraphs and before the bibliography**; no \`\\subsection\`, displayed equations, citations, new figures or tables.

**Suggested scope: ~180–240 English prose words**, three paragraphs. The span is an authoring target to support argument density, **not a journal-imposed rule**. Every paragraph should perform a nonredundant scholarly task. The text must stand alone as the article's final answer without requiring the reader to re-scan §6 tables.

| Paragraph | Suggested length | Argumentative job | Frozen support / linguistic stance | Avoid |
|---|---:|---|---|---|
| **P1 — answer the central question (C1)** | **50–70 words** | Return to the Introduction's *incremental knowledge value* problem; state that a fixed relationship specialist is conditionally complementary to the Base, particularly with eligible historical relationships not visible in its input. Make explicit that overall specialist weakness and positive local contribution coexist. | §1 Introduction, §3 \(\Delta_M\), §6.1 Twitch overall vs recoverable-state contrast, §7.1 | Redefining formulas; listing subgroup/event counts; saying Memory universally outperforms Base; claiming causal discovery of the Base's internal representations |
| **P2 — selectivity and candidate context (C3, C2)** | **75–100 words** | In *evidence order*, state that DEV-frozen Twitch relative-Utility selection improves held-out ranking against Base and equal-invocation Difficulty; then state that paired KuaiLive candidate changes can reverse the fixed specialist's measured relative advantage, with ranked alternatives dominating the **descriptive** allocation, and that the direction is stable under existing within-cohort model/draw checks. | §6.2 plus S2/S7 for Twitch; §6.3 plus S5/S8 for KuaiLive; §7.2–7.3 | Treating retrospective TEST top-\(m\) Difficulty as separately frozen serving policy; depicting KuaiLive as a second transferred Twitch gate validation; isolated causal effect of candidate count; seed/draw detail dump |
| **P3 — one KBS-level closing insight** | **50–70 words** | State the general *decision-oriented knowledge assessment principle*: evaluate the marginal value of a fixed knowledge specialist against a defined incumbent/candidate context, then use pre-outcome predictors to decide when to draw on that evidence. End with a precise offline, model-and-regime-specific scope, possibly one forward-looking sentence on independent deployment validation. | §7.4 inference scope, §7.5 knowledge-based recommendation implications | Repeating §7.5's extended design agenda; generic claims such as "revolutionizes intelligent recommendation"; online engagement/GMV improvement; net latency savings; multiple paragraphs of limitations or future research |

**Discussion vs Conclusion:** §7.1–7.3 **interpret why** complementarity, candidate regimes and relative Utility matter and relate them to literature. §7.4 explains inferential validity. §7.5 converts the interpretation into design/evaluation principles. **§8 reports what this particular study finally establishes**, with one closing knowledge-systems inference. It must not become a sixth Discussion subsection or a second Abstract.

## 3. Proposed English argument anchors (planning cues, not a complete draft)

The following three short sentences are **paragraph openings to refine during drafting**, not a paste-ready Section 8:

**P1:** “This study examined historical relationship memory as a source of incremental ranking utility relative to a trained incumbent, revealing pronounced conditional value despite the specialist's lower average performance.”

**P2:** “A selector trained to anticipate specialist-relative benefit improved held-out Twitch ranking over the incumbent and a matched-invocation difficulty control; complementary KuaiLive evidence showed that the same fixed specialist's measured benefit also depends on the eligible ranking alternatives.”

**P3:** “Taken together, these findings support evaluating and using relationship knowledge according to its expected decision-level contribution under a specified model and candidate context.”

Use these as a **cohesive argument**, not three repeat introductions. P1 explains *what becomes useful*, P2 explains *what was actually validated*, and P3 gives *the final answer*. “Improved” in P2 is platform-specific; the two platform findings are complementary, not interchangeable test replications. If citing the KuaiLive sensitivity checks verbally, say “across the examined training initializations” rather than conflating seeds and negative-draw repetitions.

## 4. Scientific claim-lock table for final drafting

| Intended conclusion claim | Exact existing result location | Required nuance / prohibited inference |
|---|---|---|
| Relationship specialist can help only under identified contexts despite negative global average | Twitch **§6.1**; S2/S4/S6, §7.1 | Full-memory overall worse than Base; recoverable state target-defined and **retrospective**; no online state labels |
| Prediction of incremental rather than incumbent-only difficulty improves frozen ranking choices | Twitch **§6.2**; S2/S7, §7.3 | Utility regressor and threshold **DEV-frozen**; frozen TEST once; Difficulty **TEST-batch top-\(m\) at observed Utility call count**, not independently DEV-frozen threshold |
| Measured candidate-protocol specialist value can reverse with fixed event/rankers | KuaiLive **§6.3**; S5/S8, §7.2 | Same previously examined 10,222 events; fixed trained rankers; membership allocation algebraic/descriptive, mixes candidate size, composition and ranking competition; 3 trained pairs, extra 9 draws only at original pair; not a new untouched TEST policy |
| Implications for knowledge-based decision systems | **§7.4–7.5** plus the empirical record | Operational offline ranking value relative to model/candidates; no net-serving speedup demonstrated. Distinct warmed KuaiLive CPU replay showed **positive** overhead, so avoid universal efficiency or production feasibility claims |

**Numeric policy for §8:** The canonical outline says **“without adding numbers.”** Accordingly the Conclusion should use **no new numeric estimates** and **normally no quantitative metrics, confidence intervals, sample sizes, seed counts, tables or formulas at all**: the Results carry their full precision, and Discussion contains selective interpretive anchors. If a number unexpectedly becomes essential to a logical claim, return to the existing Results/S1–S9 and explicitly justify the deviation before inserting it. Do not create new statistics.

## 5. Academic rhetoric requirements and KBS-specific reviewer hazards

**Use**
- Declarative scientific prose oriented around one answer to the title question, with verbs such as *demonstrates within the evaluated setting*, *indicates*, *shows that*, *supports* and *connects* appropriately matched to evidence strength.
- An affirmative description of the meaningful **negative overall Memory result** as a finding that clarifies *conditional complementarity*, not an apology for expert weakness.
- Concise evidence-status signals if material: “DEV-frozen Twitch TEST”, “paired KuaiLive candidate-regime comparison”, “in the evaluated offline ranking settings”.
- Consistent defined names: Base, Memory, Utility, Difficulty, relationship evidence, ranking utility, candidate regime and pre-outcome features.

**Avoid**
- Repeating “not a new theorem”, “not general L2D”, “not a causal test” or detailed run/protocol/seed histories. Their substantive boundaries were already recorded in §§2–7.
- Formula strings \(u_K,\Delta_M,\eta_r\), precise CI/millisecond tables, new references, future-work shopping lists, data-splitting tutorials or retrospective methods narrative.
- Equating availability, reliability and realized decision improvement. Avoid “reliable evidence must help” and “always select Memory where target is recoverable” because target history states use the realized target.
- Claiming transfer of a Twitch selector to KuaiLive, demonstration of a prospective cost-optimal policy or gains in production latency, real engagement or revenue.
- Turning the last sentence into generic “This study opens many promising directions”; finish instead on **the conditional, incumbent-relative knowledge-use thesis**.

**Evidence-tier nuance that must survive compression:** The paper validates selective policy choices independently on Twitch, while KuaiLive contributes paired post-hoc diagnostic evidence about candidate contexts. The Conclusion should not write “the proposed adaptive routing method is shown effective across both datasets.”

## 6. Implementation / QA sequence — one-scoped edit only

1. **Freeze inputs before writing.** Re-fetch canonical \`main.tex\`, outline and S1–S9 SHAs; ensure no intervening edits changed §§1–7.
2. **Write P1–P3 as continuous academic English**, guided by the table above. Preserve the three findings and the evidence sequence; target ~180–240 prose words without mechanical filler.
3. **Insert only** a \`\\section{Conclusion}\` (and label if used) **before** \`\\bibliographystyle{elsarticle-num}\`. Do not alter §§1–7, bibliography, supplementary, figure captions, models or numbers.
4. **Reviewer-style tightening of §8 alone:** check the scientific answer, relative value versus Base Difficulty, candidate environment interpretation, lack of procedural/defensive prose and distinctness from §7.5; compress repeated text without losing empirical specificity.
5. **Source-quality gates:** compare all earlier sections byte-for-byte against accepted Stage-4 blob; verify 49 old labels remain, any new Conclusion label is unique, 28 cited keys still resolve, all main evidence numerals remain elsewhere, no unexpected \(u_K\) definition changes.
6. **Exact-source LaTeX CI + PDF review:** ensure compile success, correct §8 placement before References, no orphan title, undefined ref/citation, overfull hbox, caption displacement or strange trailing blank page. Inspect actual affected final pages, not just logs.
7. **Stage-8 handoff:** record commit, source SHA, exact CI run, PDF/log artifact, word count, independent referee disposition and remaining submission tasks. Then author the **Abstract separately**, checking it against §1–§8 and KBS-specific current submission requirements rather than pasting Conclusion prose.

## 7. Acceptance checklist

**Scientific argument**
- [ ] §8 answers **when relationship memory helps** under a specified Base and eligible candidate regime, without inventing a new contribution.
- [ ] C1 + C3 + C2 appear as **connected evidence**, with Twitch held-out decisions distinguished from KuaiLive post-hoc candidate analysis.
- [ ] Overall Memory underperformance is retained as meaningful evidence for conditionality; beneficial recoverable relationships are not promoted into serving labels.
- [ ] Equal-invocation Difficulty's retrospective TEST-batch protocol remains distinguishable from DEV-frozen Utility.
- [ ] Candidate regime reversal is descriptive, not claimed as candidate-count-only causal or zero-shot router transfer.
- [ ] No unmeasured latency reduction, business uplift or global model superiority is asserted.

**Academic style**
- [ ] Three concise paragraphs; **no subheadings, citations, numerical results, tables or new equations**.
- [ ] §8 synthesizes conclusions rather than retelling the full Results, duplicating §7.5's agenda, reviewing Related Work or defending experimental process.
- [ ] Positive, scholarly, bounded language; no apology-style negative language or procedural audit narrative.
- [ ] Last sentence leaves one unambiguous contribution: **knowledge use should be guided by the marginal value it adds to the incumbent ranking decision in context**.

**Technical**
- [ ] Existing accepted §§1–7 are byte-identical; S1–S9 and BibTeX are unchanged.
- [ ] Exact-source CI and PDF layout pass, with corresponding GitHub artifact and no undefined citations or references.
- [ ] Abstract remains unwritten until §8 has been separately tightened; author metadata and truthful publisher-required declarations remain pending.

**Current status:** Planning completed; canonical \`main.tex\` still has only seven \`\\section{}\` blocks and no abstract. **Do not mark the complete manuscript submission-ready on the strength of this plan.**
