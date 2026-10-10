# Section 7.5 — independent KBS reviewer-style tightening

**Date:** 2026-10-10  
**Scope:** \`§7.5 Implications for Knowledge-Based Recommendation\` in canonical [main.tex](main.tex).  
**First draft:** [b070663](https://github.com/mzch0210/KuaiLive-Agent/commit/b070663929903e60c2d115aea46c3c0f26d1151e); [first-draft evidence audit](SECTION7_5_FIRST_DRAFT_SOURCE_AUDIT_2026-10-10.md).  
**Scoped tightening:** [9a6b3a4](https://github.com/mzch0210/KuaiLive-Agent/commit/9a6b3a40b04f6fd7fcf9884da8d0c95db7136043) and final [cb022ee](https://github.com/mzch0210/KuaiLive-Agent/commit/cb022ee38b1eeaaa810c24eb823076d7e8f64dfe).  
**Whole-section acceptance:** [complete cross-subsection / cross-chapter audit](SECTION7_COMPLETE_CROSS_SECTION_CROSS_CHAPTER_KBS_AUDIT_2026-10-10.md), corresponding source commit \`4c603065\`.

## Independent reviewer diagnosis and disposition

**Decision: accepted after tightening.** The initial two-paragraph first draft contained the right C1–C3 content but risked appearing as a sequential summary of contributions followed by a broad future-work list. For a KBS Discussion, the scientific object should instead be a **unified account of when additional historical knowledge merits affecting an incumbent ranking decision**. The accepted replacement presents that principle and explicit design conditions, rather than naming C1/C2/C3 as paragraph-level outline tags.

| Reviewer priority | First-draft vulnerability | Direct change | Status |
|---|---|---|---|
| **P1 central thesis** | Three contributions could be read as separate observations or a new universal learning-to-defer theorem. | Integrates **paired Base-relative valuation → historical/candidate heterogeneity → pre-outcome selective invocation** into one empirical decision account. The algebraic subtraction is not claimed to be novel general theory. | Resolved |
| **P1 operational applicability** | “Additional evidence” alone did not spell out the exact unit of benefit. | Identifies **the trained Base, fixed separately scored specialist, *same request*, and eligible candidate set** as the operational evaluation context; pre-outcome history and Base scores support only the invocation estimator. | Resolved |
| **P1 relation to §8 Conclusion** | A general conclusion-like or future-work-heavy ending could duplicate the final paper's results summary. | §7.5 now gives *system design and research evaluation implications*; §8 will instead state the question, established contributions, essential frozen evidence and concise final conclusion. No new empirical headline is invented here. | Resolved |
| **P2 knowledge validity** | Reliable or available evidence might incorrectly imply beneficial specialist use, regardless of the incumbent. | Separates evidence **availability**, **reliability** and **incremental ranking decision utility** without claiming to measure intrinsic reliability; value remains base-and-regime-relative. | Resolved |
| **P2 candidate and transfer causality** | Study could be mistaken for proof of candidate-count causation or direct KuaiLive transfer of Twitch policy. | Matched KuaiLive observations are treated as **candidate-regime-dependent utility**, while isolated candidate count/composition/hardness and independently frozen cross-platform routing are specifically marked as future tests. | Resolved |
| **P2 cost and budgets** | Selector call fraction could masquerade as net serving improvement. | Recommendations call for budget-aware selection, **feature/gate/specialist** timing and prospective end-to-end measurements. Separate KuaiLive HGB CPU replay retains the **positive +1.016 ms overhead**; no Twitch speed-up is claimed. | Resolved |
| **P2 academic prose/length** | Explicit contribution-label scaffolding and repetitive negative qualification weakened the synthesis. | Two academic prose paragraphs; **~217 words**, within the approved **185–235** budget, with first paragraph interpreted principle and second paragraph testable design implications. | Resolved |

## What Section 7.5 establishes—and does not establish

The result is a **knowledge-decision interpretation** supported by the pre-existing frozen and retrospective evidence, not an extra statistically independent replication. §7.5 contains no new equations, citations, labels derived from targets, tables, models, or numerical estimates. It preserves the distinction between the one-shot Twitch DEV-frozen/TEST policy comparison and reused KuaiLive TEST candidate-regime diagnostics.

Its conceptual novelty lies in **linking the operational value of a fixed relationship-history specialist to candidate-conditioned ranking utility and pre-outcome invocation**, not in inventing routing or long-term memory. Formally published prior art (ICML 2020 Mozannar–Sontag, NeurIPS 2022 Narasimhan et al. and CACM 2022 Krichene–Rendle) is already acknowledged in Related Work/§7.2/§7.3, with no redundant citations introduced into §7.5.

## Technical acceptance

- The final source update to §7.5 changed **only the §7.5 text** before the bibliography. A subsequent **one-sentence §7.2** clarification of KuaiLive trained-seed versus candidate-draw variation is separately recorded in the whole-Section-7 audit.
- The matching full-manuscript source commit \`4c603065\` successfully built in [GitHub Actions #38037009736](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38037009736) into a **30-page PDF**, [artifact #11664122570](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38037009736/artifacts/11664122570); final-pass citations, references and layout checks passed.
- A rendered view of the exact-source PDF **pages 22–25** was inspected: all five Discussion subsections flow coherently, §7.5 appears on page 25 and transitions into References without a displaced heading or interfering float.
- The full scientific claim matrix, mathematical/source checks, S1–S9 cross references, citation audit and §8 vs §7.5 responsibility boundary are documented in the [complete cross-section/cross-chapter audit](SECTION7_COMPLETE_CROSS_SECTION_CROSS_CHAPTER_KBS_AUDIT_2026-10-10.md).

**Status:** §7.5 independently tightened and accepted; §§7.1–7.5 now jointly accepted under the detailed whole-Discussion audit. §8 Conclusion and Abstract remain unwritten and outside this acceptance.
