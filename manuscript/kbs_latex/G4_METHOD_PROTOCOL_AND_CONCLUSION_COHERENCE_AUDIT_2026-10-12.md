# G4 — KBS §3–§5 Formal/Method/Protocol Coordination and §8 Conclusion Cross-Chapter Audit

**Date:** 2026-10-12  
**Task:** Complete second-pass G4 without redesigning the contribution or adding unsupported claims.  
**Status: G4 formally PASS** — scientific/source integrity, exact-source GitHub Actions build and rendered method/protocol PDF pages all accepted. G5 remains pending.

## 1. Accepted evidence baseline and precisely scoped source change

- **G3 accepted source:** [commit 02067047](https://github.com/mzch0210/KuaiLive-Agent/commit/02067047cb1b9d5165a254080030ade86a399701), `main.tex` Git blob **dc00dcf0e1a8c1f2225202651fc797f8eba43352**.
- **G4 D1 (§3):** [commit ed489843](https://github.com/mzch0210/KuaiLive-Agent/commit/ed4898436aad028a0726f927c2afc82dc78081af) — event-level utility, conditioning descriptors, expert selection and descriptive regime identity.
- **G4 D2 (§4):** [commit 944841ba](https://github.com/mzch0210/KuaiLive-Agent/commit/944841ba347e1babd1b609cd59a30f220fc88f41) — actual Base/default ranking → Utility prediction → conditional Memory invocation, no altered features or architecture.
- **G4 D3 (§5):** [commit 42d6db84](https://github.com/mzch0210/KuaiLive-Agent/commit/42d6db84f7aaf72cb5ce01fa6b70e970946c14e5) — TRAIN/DEV/TEST access and retrospective equal-call baseline distinction, with exact fixed **raw** score condition for crossed candidate/reference evaluation. **Current `main.tex` blob 4a8d07da093bd350339c68f1617d98de1a32780f.**
- **G4 D4 (§8):** Checked final existing three-paragraph Conclusion against G1 Introduction/C1–C3, G2 Results and G3 Discussion; **no unsupported claim or functional duplicate requiring a §8 edit**. §8 is byte-for-byte identical to G3.
- [Formal evidence freeze and traceability (G0)](G0_FROZEN_BASELINE_CLAIM_EVIDENCE_TRACEABILITY_2026-10-11.md); [second-pass action plan](KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md); [G1 report](G1_INTRO_RELATED_WORK_KBS_REVIEWER_ACCEPTANCE_2026-10-11.md); [G2 report](G2_RESULTS_DISCOVERY_FIRST_REVIEWER_ACCEPTANCE_2026-10-12.md); [G3 report](G3_DISCUSSION_SCIENTIFIC_INTERPRETATION_REVIEW_2026-10-12.md).

**Edit scope:** §3 Problem Formulation, §4 Base-Relative Evidence Valuation Framework, and §5 Experimental Setup *ordinary prose only*. Everything before `\\section{Problem Formulation}` and from `\\section{Experimental Results}` through the document end is byte-identical to the G3 accepted source. The entire §6 scientific evidence, §7 explanation, §8 conclusion, bibliography, and S1–S9 remain unchanged.

## 2. Independent reviewer diagnosis and implemented fixes

| Queue | Scientific presentation issue | Concrete correction | Reviewer judgment |
|---|---|---|---|
| **D1 §3 — define the target once** | The Introduction/Discussion interpretation (“history has value when it improves Base”) was repeated within the formal object definitions, obscuring the mathematical dependency among event utility, `Δ_M`, `η_r` and conditional gain. | Start directly with relative-value formalization; define the specified Base–specialist/candidate dependency precisely; allow `eq:expected-selective-gain` to supply the objective instead of more narrative paraphrases. | **PASS** — all displayed equations, math meanings and order unchanged. |
| **D1 §3 — observable variables** | Generic “candidate-set descriptors” and “confidence signals” could be misread as separately measured/calibrated confidence or broader features than the actual estimator uses. | `Z` is accurately described as history summaries and **Base candidate-score distribution and margin descriptors**, which are not necessarily calibrated uncertainty. Target-defined states, realized utility and target recurrence remain offline-only. | **PASS** — avoids unsupported model-calibration and label-leakage implications. |
| **D1 §3 — controlled comparison** | Selection decision, invocation frequency and retrospective control access were explained in several adjacent sections. | Keep the fixed pointwise decision definition in §3; define realized number `m` and refer to §5 for TEST batch access of the comparator; state state prevalence vs state-conditional utility once. | **PASS** — no guarantee that independently frozen Difficulty has identical call count is implied. |
| **D2 §4 — actual mechanism** | Framework opener and later selection paragraph repeated §3 definitions instead of explaining what is scored when. | Explicit Base ranking/score descriptors → history/score predictor → **conditional Memory ranking only after positive decision**, consistent with Figure 1. Base architectures retain their different ranking units. | **PASS** — specialist scoring formula remains exactly **0.45 Short + 0.45 Long + 0.10 Popularity**, without retraining or alternative policy. |
| **D2 §4 — comparison responsibilities** | Memory purpose and Base Difficulty objective were restated from multiple chapters. | Keep transparency of fixed specialist and a short objective-level Difference-vs-Difficulty statement; move retrospective TEST top-`m` details to the unique formal experimental comparator location, §5. | **PASS** — complete 14-feature construction and target-state definition remain in Methods. |
| **D3 §5 — formal policy access** | Training protocol fitted, selected, and frozen stages were compressed into an overlong paragraph, with risk of confusion about what was prospectively selected. | Separate the protocol into two linked paragraphs: trained Base on TRAIN; Utility/Difficulty fit on DEV; OOF threshold DEV; frozen pointwise Utility before Twitch TEST. Equal-count Difficulty/Oracle are expressly retrospective **TEST top-`m`** at the Utility policy's realized number of calls. | **PASS** — independent Twitch policy evaluation is correctly distinguished from retrospective equal-count scoring. |
| **D3 §5 — raw vs standardized scores** | “holding original ranking scores fixed” in crossed KuaiLive scoring could suggest all standardized scores remain unchanged when the score-reference set varies. | State that **raw Base branch predictions and Memory scores** remain fixed. The candidate membership and standardization reference are separately changed in the 2×2 descriptive calculation. | **PASS** — no independent candidate-count causal claim, no KuaiLive gate transfer. |
| **D4 §8 — coherent final answer** | Need to check whether G1/G3's narrative improvements require a rewritten Conclusion. | Compared all three Conclusion paragraphs with current C1/C3 Twitch evidence and C2 KuaiLive candidate diagnostics. Conclusion's final empirical inference remains correct and distinct from §7.5's design implications. | **PASS; §8 intentionally unchanged.** |

The strengthened wording remains affirmative and manuscript-appropriate; necessary scientific constraints remain explicit. There was **no systematic deletion of “not”, “DEV”, “TEST”, “retrospective” or negative results**. Process-specific details are deliberately centralized in §5 and supplements instead of reintroduced as argumentation throughout §3–4.

## 3. G4 formal invariant and cross-chapter scientific consistency

**Actually checked against the exact accepted G3 source:**

- **Eight numbered chapters** remain in their previous order. §1–2 before §3 and §6–8 after §5 are **byte-identical**.
- **Every displayed `equation`/`align` environment and every `figure`/`table` environment** is exactly unchanged. This preserves event-level one-positive NDCG, fixed Memory score, conditional expected gain, observed gate selection and 2×2 crossed standardization allocation, as well as all figure and table captions.
- **50 unique LaTeX labels**, zero duplicates, zero missing `\\ref/\eqref` label targets.
- **28 distinct cited BibTeX keys**, all present in `kbs_references.bib` (blob **358e6599711421ac609cb1956cfc9cd122cdc341**).
- **All checked core result-number strings** unchanged in the manuscript, including frozen Twitch TEST Base/Memory and Utility/Difficulty, paired KuaiLive sampled/full reversal and **positive** warmed CPU overhead. No new models trained and no bootstrap/CI recomputed.
- **Integrated S1–S9** remains blob **067d4e5713eb927d8aab3dee3bf2dde512b314ed**.
- The inferential hierarchy remains: Twitch DEV-frozen Utility threshold evaluated on held-out TEST; DEV exploratory analyses; KuaiLive paired previously examined TEST candidate-regime diagnostic; distinct warmed HGB CPU replay. **Neither target-defined history states nor realized event utility became a decision-time feature.**

**D4-specific check of §8 Conclusion:** P1 states conditional history evidence value relative to the incumbent, P2 correctly distinguishes DEV-frozen Twitch policy and retrospectively matched Difficulty from KuaiLive fixed-model candidate regime diagnostic, and P3 asserts only conditional knowledge-decision usefulness in the studied offline rankings. It does not claim a new general L2D algorithm, candidate-number causality, independent gate transfer, latency savings or online business uplift. **§8 is intentionally unchanged.**

## 4. Journal writing and standards verification

- [Official Knowledge-Based Systems Aims and Scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051): innovative AI, knowledge-based systems, recommendation and decision support, balancing methodological and applied contributions.
- [Elsevier journal reviewer guide](https://www.elsevier.com/reviewer/how-to-review): methods are assessed for adequate reproducibility detail; claims and conclusions must be supported by study design and appropriate statistical reporting.
- [Elsevier science-paper structure guide](https://www.prod.webpresence.elsevier.com/connect/the-condensed-read-how-to-structure-a-science-paper): Methods describes *how*, Results *what*, Discussion *what it means*. **These are general publisher editorial recommendations, not mandatory KBS subsection or word-count rules**.
- The latest specific KBS author guide should be rechecked in the final submission-package stage; no publisher-exclusive template restriction is inferred from a generic source.

## 5. Technical build and proofing gate — formally PASSED

- **Exact-source CI PASS:** [GitHub Actions #38194254351](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38194254351) at commit `42d6db84f7aaf72cb5ce01fa6b70e970946c14e5` completed **success**; LaTeX compilation, PDF verification and artifact upload all passed. Final PDF **29 pages**, **445,293 bytes**; **0 Overfull hbox** across all compile passes, no fatal errors and no unresolved final citation/reference targets. The raw log has four Underfull notices, without visible text loss. [Matching PDF and logs artifact #11723150138](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38194254351/artifacts/11723150138).

- **Actual PDF layout PASS:** Downloaded and extracted the exact-source artifact. `pdfinfo` confirms a 29-page Letter-size PDF; PDF text extraction locates §3 beginning on p5, §4 on p7, §5 on p10 and §6 on p15. All 29 pages were checked for text blocks beyond page boundaries (none). Rendered **pages 4–15** at 115 dpi and examined the 12-page contact sheet. Figure 1, the dataset table, the methods-comparison table and the displayed equations remain visible without clipping, overflow, orphan chapter headings or anomalous blank transitions. Final whole-manuscript proofing will be carried out in G5 after any further manuscript changes.

- **G4 independent reviewer disposition: PASS.** §3–§5 now connect to the G1 scientific question and G2/G3 evidence with tightly scoped, reproducible methods prose; §8 requires no rewrite. The next step is **G5 independent eight-chapter editorial and full-PDF review**. Abstract, Highlights, author-reviewed disclosures and final KBS-specific Guide for Authors confirmation remain pending; G4 does **not** make the paper submission-ready.
