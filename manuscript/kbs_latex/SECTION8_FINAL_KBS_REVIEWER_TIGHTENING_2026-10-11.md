# Section 8 — Final KBS Reviewer-Style Tightening and Cross-Chapter Acceptance

**Date:** 2026-10-11.  
**Task:** Independently strengthen the final scientific argument of §8 Conclusion and distinguish its job from §7, especially §7.5.  
**Canonical source commit:** [e9d07952c7d9964c67fee31f3c3a16af6b96d85f](https://github.com/mzch0210/KuaiLive-Agent/commit/e9d07952c7d9964c67fee31f3c3a16af6b96d85f); source blob \`fa73ba31a56edd96f6eeaca272214b98bf4a9a9d\`.  
**Prior Conclusion first draft:** [cfb5a623](https://github.com/mzch0210/KuaiLive-Agent/commit/cfb5a623d7cdfa7a41350b97f9a6f18e3b4de21c), [first draft and 29-page PDF acceptance audit](SECTION8_FIRST_DRAFT_AND_REVIEW_AUDIT_2026-10-11.md).  
**Governing writing plan:** [Section 8 KBS Conclusion plan](SECTION8_KBS_CONCLUSION_WRITING_PLAN_2026-10-10.md), [authoritative manuscript outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md).  
**Evidence:** accepted §1–§7 source, [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md).  
**Journal framing:** [Elsevier KBS official scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) and [Elsevier Discussion/Conclusion editorial advice](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/steps-to-write-excellent-discussion-in-manuscript/). General editorial advice is not a KBS-specific word-limit rule.

## I. Independent reviewer diagnosis and substantive remedy

**Outcome: reviewer-style tightening implemented, scientific narrative accepted at source level.** The initial 221-word Conclusion was evidence-correct but its final paragraph partially duplicated §7.5, reiterating design principles and future deployment tests. The central scientific insight—why predicting **specialist-minus-incumbent advantage** is preferable to incumbent-only difficulty when choosing relationship knowledge—also needed a more explicit concluding statement.

| Priority | Initial weakness | Actual §8 edit | Acceptance |
|---|---|---|---|
| **P1 scientific strength** | “predicting specialist-relative utility improves ranking” primarily restated an outcome; it did not fully articulate why this matters for knowledge-driven expert choice. | Second paragraph now explicitly contrasts **anticipating specialist advantage** with **identifying requests difficult for the incumbent**, immediately supported by the frozen Twitch Utility vs retrospectively invocation-matched Difficulty comparison. | **PASS** |
| **P1 §7.5 overlap** | Old final paragraph duplicated §7.5's *general design agenda* and finished with future deployment validation, already discussed in §7.5 and §7.4. | Final paragraph is now a single **study-specific conclusion**: historical knowledge is useful as a decision-relative ranking resource, and pre-outcome estimates can turn that value into a testable conditional-choice signal in the evaluated offline setting. The explicit future-deployment sentence and repeated evaluation-checklist language are removed. | **PASS** |
| **P1 evidential precision** | Twitch subgroup observations or KuaiLive consistency could inadvertently be taken as universal serving knowledge. | First paragraph explicitly says **positive mean advantage** for target-defined recoverable history; second distinguishes held-out Twitch DEV-frozen policy from paired KuaiLive fixed-ranker comparisons, says the candidate decomposition is **descriptive** and makes no candidate-number causality claim. | **PASS** |
| **P2 academic tone and density** | Three paragraphs contained modest repetition of “this study,” “together,” “incremental,” and exploratory future work. | Preserved three paragraphs but tightened transitions and made the final sentence declarative rather than procedural. Approximate English body words **221 → 214**. | **PASS** |

**Crucial role boundary:**
- **§7.1–§7.3 Discussion:** explain *why* history can complement or overlap the trained Base, *why* candidate regimes matter, and *why* Utility differs from Difficulty; compare to formally published prior art.
- **§7.4–§7.5 Discussion:** specify inference limitations and transferable **design/evaluation principles**, including runtime costs and future validation.
- **§8 Conclusion:** state **what this study establishes** under its actual experiments and close the paper's research question. The final text does **not** repeat the §7.5 forward-looking candidate-hardness, budget, online/A-B and computing evaluation agenda.

## II. Locked science and exact supported conclusions

**Paragraph 1 / C1 — conditional historical value.** Twitch frozen TEST shows the fixed relationship Memory is overall below Base, but retrospectively defined recoverable target-history events have a substantial **positive mean** Memory–Base advantage. Thus evidence availability alone is not proof of universal augmentation. The Conclusion does not claim the Base's internal representation was causally measured or that recoverable state is a pre-outcome serving feature.

**Paragraph 2 / C3 then C2 — two complementary experimental roles.** Twitch Utility predictor uses pre-outcome descriptors, its gate and threshold were frozen from DEV, and it improves held-out ranking against Base and Difficulty matched **retrospectively** to Utility's actual call count. Relative utility captures *expert opportunity* rather than simply identifying difficult requests. KuaiLive uses paired previously examined TEST events with a fixed Base–Memory comparison in changing sampled/full-active candidate regimes; the sign reversal remains directionally consistent across separately trained pairs and fixed-pair candidate draws. The membership/reference decomposition is descriptive; membership mixes count/composition/competition, and no cross-platform frozen router is claimed.

**Paragraph 3 / Knowledge-Based Systems scientific inference.** The final answer is *decision-relative knowledge valuation*: a fixed relationship specialist's ranking value is defined relative to the incumbent and actual alternatives, while pre-outcome predictions of marginal value can guide selective use under the reported offline evaluation. This is **not** a new general defer theorem, an intrinsic knowledge reliability metric, or evidence for net online speed-up. The important separate KuaiLive warmed CPU measurement records **positive** overhead and remains correctly in §6.5/§7.4.

No new result, data split, confidence interval, causal statement, statistic, math notation, formal citation or source bibliography edit was introduced.

## III. Source-level Gate and build record

- **Only §8 Conclusion text changed.** The complete pre-Conclusion manuscript **§§1–7 is byte-identical** to the prior accepted commit \`cfb5a623\`, as are the bibliography and file ending. Entire S1–S9 and \`kbs_references.bib\` SHA are unchanged.
- **Body:** 3 paragraphs, **68 + 87 + 59 = 214 whitespace-delimited words**. No extra headings, equations, figure, table, numerical metrics or citations.
- **Reference integrity:** **50 distinct \`\\label\` keys**, no duplicates or broken \`\\ref/\\eqref\`; **28 BibTeX citation keys**, all resolved to unchanged bibliography records.
- **Core frozen results:** unchanged in §§1–7 and S1–S9, including Twitch TEST Base/Memory, Utility/retrospective Difficulty and paired KuaiLive candidate reversal, plus positive separate CPU overhead.
- **CI/build: PASS.** Exact-source commit `e9d07952c7d9964c67fee31f3c3a16af6b96d85f` built successfully in [GitHub Actions #38123108655](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38123108655): **29-page PDF**, successful compile/PDF-validity/artifact-upload stages, no missing final citations or cross-references, no fatal LaTeX error and **zero Overfull hbox warnings throughout the build**. [Source-matched PDF and logs artifact #11696580608](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38123108655/artifacts/11696580608). The actual PDF was downloaded and checked with `pdfinfo` and text extraction; §8 occupies page **24**, References starts page **25**. Pages 24–25 were rendered at 125dpi and visually inspected, with no orphaned section title, text clipping, overlap or abnormal blank transition.

## IV. Independent acceptance criteria and next step

**Scientific and prose check: PASS.** The revised §8 answers *when relationship memory helps*, covers C1→C3→C2 in verified evidence order, states the distinct estimated-benefit vs Base-difficulty target, and ends on a result-grounded KBS knowledge decision rather than duplicating §7.5's general design advice.

**Exact source/technical gate: PASS.** The matched [Actions #38123108655](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38123108655) PDF build succeeded and actual pages 24–25 passed visual QA. **Final §8 reviewer-style tightening accepted.** Preserve §§1–§8 as the current academic source for independently drafting Abstract. Author-approved publishing declarations, the KBS-specific guide and a final complete-manuscript pagination audit remain submission-package requirements; §8 acceptance is not full article readiness.
