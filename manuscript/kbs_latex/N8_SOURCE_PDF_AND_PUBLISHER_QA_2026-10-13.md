# N8 — exact-source main/supplement PDF and artifact QA

**Date:** 2026-10-13. **Status:** Technical source/PDF PASS; final publisher/author content sign-off HOLD.

## 1. Main manuscript: compiled and inspected

- **Current exact `main.tex` Git blob:** `40be249de52c0ae423b793c0dd4c55f2fdd69f46`. The manuscript was edited in N7 and accepted as source at `e3e0738abc28910caefc0e41a363466b99d0abdf`; subsequent N8 documentation and supplementary workflow commits did not change the main article bytes.
- **Exact-source GitHub Actions:** [#38344272685](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38344272685), SUCCESS. Artifact ID `11788491619` (ZIP containing `main.pdf`, `main.log`, BibTeX log).
- **Verified PDF:** 31 US Letter pages, 487,639 bytes, SHA256 `dfc91a943145485bcf7217d589580ba8df29ac6ebd6cd1dcba91d37a21ee4200`.
- **Static checks:** eight main chapters, 2 figures, 9 tables, 53 distinct LaTeX label identifiers, no missing citation keys, undefined references or duplicate labels. All 12 original R0 accepted scientific claim numeric/identity tokens remain present at displayed precision.
- **Render and visual checks:** rendered a full 31-page overview and inspected the first/last pages and critical pages 9, 13–14, 18–23 and 26–27 in detail. The 11 visual elements and the Always Memory cost/accuracy reference appear in their expected narrative contexts. All extracted text blocks remained inside page rectangles under text-block bounding-box analysis.
- **TeX log:** zero fatal LaTeX errors, zero unresolved reference/citation warnings, one nonfatal overfull hbox (`3.47444pt`, around source lines 86–87) and three underfull hbox warnings. The small overfull is a **minor typesetting item** to smooth before author-approved final files, not an unacknowledged perfect-typesetting claim.

## 2. Final integrated supplement: compiled and inspected

- **Current exact combined `SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md` Git blob:** `f5575d29ac3de222a04f78b48698cae119eac0bf`; the existing filename is intentionally preserved even though the internal title metadata now correctly dates the updated supplement **13 October 2026**.
- **Source assembly:** Guarded GitHub-hosted merge [#38356550506](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38356550506) combined separate post-G5 S7.7 with frozen S1–S7.6 and S8–S9, confirmed all 9 top-level sections and unique new `Table S7.5`. A second verified guard corrected date/assembly status without touching the original G5 statistics.
- **Final dated PDF build:** [#38357256339](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38357256339), SUCCESS, artifact ID `11793380796`, including the matching Markdown, Pandoc TeX, LaTeX log and PDF.
- **Verified final PDF:** 34 pages, 176,228 bytes, SHA256 `96884692596c661bfb2d9d74f506582c042581cedc11ddf7b5f9764e6a75e522`. Cover explicitly shows **13 October 2026**. S7.7 and Table S7.5 appear on **page 23** before S8; their four DEV estimator rows, call counts and paired CI columns are legible on detailed rendering.
- **TeX log:** no fatal errors, no overfull hbox/vbox diagnostic, eight nonfatal underfull hboxes. Landscape tables create a few sparse neighboring pages (including near pages 24, 27 and 28), which is a **minor pagination-efficiency/style opportunity**, not a numerical or source-integrity failure. A full 34-page overview and representative page/title/table renderings were visually inspected.
- **Scope:** Both old and new supplemental analyses remain described with their correct **frozen vs retrospective vs post-G5 exploratory** evidence tiers. S7.7 does not create another frozen TEST or change the original S8 Holm comparisons.

## 3. Closest-source and journal compliance audit

- Original journal scope confirmed at https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 . KBS explicitly covers recommender systems and decision-support research, but topic fit is not equivalent to guaranteed methodological novelty.
- Formal ICML 2024 regression deferral source verified: https://proceedings.mlr.press/v235/mao24d.html ; adaptive fast/slow recommender DS-Frame is an arXiv 2026 public manuscript with CIKM 2026 acceptance status according to the authors' institutional record https://eprints.gla.ac.uk/392708/ . Manuscript does not assert a novelty already solved by those authors.
- Elsevier Highlights general policy: https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript ; five bullets, each 68–75 characters, editable Word created and rendered.
- Elsevier 2026 AI use statement requirement: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals . Required human verification, actual declaration, data rights and originality approvals are **not closed**.
- Direct fetch of current KBS Guide for Authors at https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors produced HTTP **403**, so **no journal-specific submission exception or requirement is fabricated**.

## 4. Deliverable status and remaining gates

**TECHNICAL PDF QA PASS.** Main 31-page and combined S1–S9 34-page sources/PDFs are reproducibly linked to GitHub Actions artifacts and exact SHA256s; they contain no detected missing scientific objects or unresolved cross-references. Temporary Actions artifacts are **not permanent source archiving**, and a visually valid PDF does not authorize submission.

**Remaining scientific/editorial considerations:** one small main overfull hbox and sparse landscape-supplement pagination can be further optimized without changing science; novelty and cost-constraint residual risk persists. **Human mandatory tasks:** validate citation details and scientific calculations against private sources, complete authors/CRediT/funding/COI/generative-AI disclosures, determine legal dataset/model sharing, check KBS live submission requirements, and approve final copies. See the N8 author-signoff checklist.

**Submission readiness: HOLD**, not an implied acceptance or guarantee.
