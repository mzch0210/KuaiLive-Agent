# R8 — initial abstract, highlights and submission-readiness audit (not final acceptance)

**Date:** 2026-10-12. **Gate state:** R8 **TECHNICAL PDF PASS; AUTHOR/SUBMISSION HOLD**. The [37-page original workflow PDF QA](R8_PLAN_C_PDF_AND_SOURCE_QA_2026-10-12.md) passed on run 38271581420; this remains a working draft rather than author-approved KBS submission. This is a source preparation and explicit author handoff, not an assertion that the paper can be submitted.

## 1. Work now implemented

- `main.tex` frontmatter: a single-paragraph **197-word** descriptive Abstract derived from the frozen Twitch, original KuaiLive and M3 evidence. It reports both positive selection evidence and adverse unconditional-Memory accuracy/cost evidence; it distinguishes retrospective paired room diagnosis from separately frozen M3 and Twitch selection. No scientific equations, figures, tables, hypotheses, model/checkpoint files or experiment outputs changed.
- `R8_HIGHLIGHTS_2026-10-12.txt`: four candidate journal Highlights, each at most 85 characters, in a separately editable text source. Elsevier general guidance (updated June 1, 2026): [author help](https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript); whether KBS requires them is **not verified**.
- `README.md`: current stage notice preceding preserved historical records; previously accepted R0–R7 and G0–G5 are not rewritten retrospectively.
- Canonical R7 source prior to Abstract: [GitHub R7 commit](https://github.com/mzch0210/KuaiLive-Agent/commit/209c6c1265cdaa5472eefaeae27ca364b4cab485), full R7 exact-source LaTeX compile [run 38271143878](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38271143878) successful.

## 2. Preliminary source-to-evidence and citation checks

| Check | Author-facing interpretation |
|---|---|
| Three ranked units and two frozen selector TESTs | Twitch streamer 44,221; original KuaiLive retrospective paired room 10,222; M3 author TEST 47,575 from 12,533 users. No person-disjoint or same-task cross-release claim. |
| Frozen decision and inference | M3 two fitted architectures × three seeds = six correlated checks on the same TEST cohort; 3 primary contrasts with Holm separately within each fit; Uncertainty comparison secondary. |
| Real call budget | M3 at most 30% **DEV**, observed TEST rates can vary (History 35.472%); Twitch Utility 6,650 / 44,221 and Difficulty retrospectively count-matched. |
| Adverse economic evidence | M3 Always Memory 0.346792 > Utility 0.301766–0.304004 on TEST and warmed DEV 0.8033 ms < selective 1.8018 ms. No production speedup claim. |
| Supplement | R6 S1–S9 33-page source accepted, including six checkpoints, gate rates, all 18 per-fit primary CIs and old/new cost evidence. NOT rewritten in R8. |
| Bibliography | R7 already checked 30 cited unique keys against 31 unique `kbs_references.bib` entries including published CKLF; exact-source compilation passed on R7. Reverify post-Abstract PDF before final closure. |

## 3. Nondelegable author facts and publication permissions — unresolved

1. **Authorship:** supply correct ordered author names, affiliations, correspondence email, CRediT roles and each author's approval. `Anonymous Authors` remains in LaTeX intentionally; do not guess review-blinding conventions.
2. **Funding and interests:** authors provide exact grant numbers, real funders, grant-holder relationships and any competing interests; truthful "none" also requires confirmation. Do not infer from department affiliation.
3. **AI disclosure:** the June 2026 [Elsevier GenAI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) calls for transparent disclosure of relevant AI-assisted manuscript preparation. The authors must validate which tools were used, for what purpose, what they independently checked, and approve the final statement. A ChatGPT manuscript-writing interaction alone is not proof that a named author reviewed every claim.
4. **Data and code:** ensure legal rights for data derived from KuaiLive-M3/Twitch/original KuaiLive, whether model weights/event data can be released, anonymization/privacy, stable checksum-backed code snapshots, and permanent deposit DOI if authorized. GitHub Actions artifacts have finite retention; do not claim a DOI, permanent reproduction package or public raw TEST data absent proof.
5. **Journal-specific guide:** current [KBS Guide for Authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors) returns HTTP 403 to automated retrieval. The submission author must verify actual Abstract/Highlights/keywords/graphical-abstract/declaration/length/file-blinding instructions in the journal portal. Elsevier publisher-wide Highlights rules do **not** establish KBS-specific mandatory status.
6. **Author-side scientific decision:** reviewers may object to limited operational necessity for the call constraint and absence of directly trained competitor gating baselines. Keep these as evidence limits, not statements that a new experiment was performed; decide separately whether new evidence is required.

## 4. Remaining executable R8 verification before PASS

- **COMPLETE for this draft only:** exact-source LaTeX workflow, all-page layout overview and detailed key-table checks. Repeat after author/declaration changes; see the PDF/source QA report.
- Compare every main-text quantitative result and the Abstract against the accepted G5 TEST/source matrix and R6 S1–S9; confirm there is no stale Twitch-only frozen claim or TEST-not-run statement in current canonical sources.
- Mark all 12 R0 issue IDs *closed* only after the combined end-to-end paper/source/permissions signoff. R7 novelty resolution is **not** sufficient for submission-wide issue closure.
- Collect and insert authors' real frontmatter and declarations, validate publisher policies, obtain copyright/data rights approval, then recompile and re-review PDF. Preserve frozen experiment chain unchanged.

**Verdict:** Editorial content preparation advanced; **R8 HOLD** pending actual final-source PDF and author-owned submission evidence. No purported Elsevier/KBS acceptance probability is estimated.
