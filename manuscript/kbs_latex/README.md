# KBS LaTeX manuscript

This directory is the canonical LaTeX workspace for the *Knowledge-Based Systems* manuscript.

## Files

- `main.tex` — current manuscript source. It uses Elsevier's `elsarticle` class and currently contains Sections 1–5 and reviewer-tightened Sections 6.1–6.3: Introduction, Related Work, Problem Formulation, Base-Relative Evidence Valuation Framework, Experimental Setup, and the first part of Experimental Results.
- `kbs_references.bib` — BibTeX database for manuscript references.

## Staged-writing rule

The [conditional-value-first submission outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md) is an approved **staged writing plan**. As of 2026-10-09, Twitch `6.1 Heterogeneous Utility of Relationship Memory` has been reviewer-tightened and `6.2 Decision Value of Predicting Relative Utility` has been reviewer-tightened in the main text; 6.4–6.5, Discussion, Conclusion and Abstract remain unwritten. The fully verified original KuaiLive P0/P1 Section 6.1 was saved without alteration as [the 6.3 migration source](section6_3_kuailive_migration_source.tex) before replacing it. Do **not** jointly generate multiple unassigned chapters. Write the Abstract after the evidence and main interpretation have stabilized.

## Current review baseline

As of 2026-10-08, Sections 1–4 form the reviewed writing baseline following a cross-section P0–P2 alignment of operational-value claims, mechanism interpretation, and method reproducibility. Earlier writing freezes were reopened only for these explicitly requested scientific corrections. Section 5 (Experimental Setup) has now been drafted directly in `main.tex`, following the updated academic outline. Section 6.1 now presents the verified Twitch DEV/TEST relationship-state results, with paired 95% intervals and a non-leakage interpretation. KuaiLive P0/P1 results were retained verbatim in an uncompiled migration archive and their relevant scientific findings now appear in the new Section 6.3. Sections 6.4–6.5, Sections 7–8 and the Abstract remain to be drafted. Reopen Sections 1–4 only for a substantiated scientific inconsistency or a journal requirement.

The frozen scientific boundaries include candidate-regime-specific event contexts, development-frozen utility thresholds with offline matched-budget controls, and non-causal interpretation of the separately trained context-length base comparisons. Section 4 instantiates these definitions without redefining the learning or evaluation protocol. Its method description distinguishes primary first-observed-crawl history from auxiliary strict-split history, explicitly follows the official Twitch ten-minute sampling semantics, distinguishes cross-platform policy re-fitting from zero-shot transfer, and excludes target-relative diagnostic labels from selector features. Reopen Section 4 only for a verified protocol discrepancy or journal-required correction.

## Maintenance rule

Future manuscript edits should be made in this directory rather than by creating new LaTeX files in the repository root. Markdown manuscript files elsewhere in the repository may remain as research/writing sources, but this directory is the paper-facing LaTeX workspace.

## Section 5 writing status

Section 5 was structurally rewritten on 2026-10-08 as a journal-facing Experimental Setup with five subsections and two compact scientific tables. The main paper now focuses on research tasks, baselines, comparison protocols, statistical analysis and essential implementation settings rather than chronological experiment audits. The prior six-subsection, 29-item line-edit version remains documented in [the historical reviewer tightening log](SECTION5_REVIEWER_TIGHTENING_2026-10-08.md); it is no longer the submission-oriented text. Sections 1–4 remain unchanged.

The cross-section [retrospective academic audit of Sections 1–4](SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md) motivated completed P0/P1 manuscript revisions: the memory-utility symbol is now $\Delta_M$ (with $m$ reserved for invocation count), the sampled-active fusion coefficient is scoped to its protocol, and Related Work and Framework were structurally tightened without altering the frozen experiment definitions.
**Published-version references:** All 24 citations in Section 2 Related Work and the two other bibliography records have a 2026-10-08 [final-publication source audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md). The bibliographic file now uses official DOI/PMLR/NeurIPS records rather than arXiv, with the INFORMS online-year/issue-year distinction documented. The reviewed BibTeX build succeeded in [run 37758378727](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37758378727). This closes the prior RW4 audit item for the currently cited works; any future new citation needs the same check.


The hosted PDF compilation workflow is `.github/workflows/kbs-manuscript-latex-build.yml`. The final 2026-10-08 structural revision passed [GitHub Actions build 37755123184](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184) and produced [PDF/log artifact 11539737383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184/artifacts/11539737383). No LaTeX errors or overfull lines remain in Section 5; two small overfull warnings persist in earlier chapters. This confirms successful compilation, not final publication layout approval. Dataset training scale and supplementary evidence provenance still require submission-stage completion.


## Section 6 drafting status (2026-10-09)

**6.1–6.3 have completed scoped reviewer-style tightening; 6.4–6.5 remain unwritten.** [`main.tex`](main.tex) now contains `Heterogeneous Utility of Relationship Memory` based on [Twitch frozen one-shot TEST run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303) and its 46,878 DEV / 44,221 TEST event protocols. The new section provides:
- a Results-style scholarly argument from aggregate inferiority to target-relative three-state heterogeneity;
- Figure 2, using DEV and TEST Memory-minus-Base point estimates and TEST 5,000-replicate paired-bootstrap 95% intervals;
- a compact TEST state table with Base/Memory NDCG@10, sample counts, paired effect sizes and intervals;
- an explicit distinction between retrospective target-based diagnostic states and pre-outcome serving features, motivating the now-drafted Section 6.2.

**New Section 6.2 (2026-10-09):** The single [drafted Results subsection](main.tex) `Decision Value of Predicting Relative Utility` reports Twitch frozen one-shot TEST policy comparisons (Base, Memory, Utility, Difficulty and Oracle), paired NDCG@10/HR@10 confidence intervals, actual Utility invocation frequency, retrospective exact-count controls, the DEV-only OOF evidence-state selection-enrichment diagnostic and prediction/headroom limitations. All values and source checks are traceable in [Section 6.2 provenance record](SECTION6_2_RESULTS_PROVENANCE_2026-10-09.md). The paired decision evidence is from [run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303); DEV-only composition is from [run 35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121). No TEST labels enter the Utility regressor or invocation threshold; only the hindsight Oracle and ex-post budget count use TEST outcomes. Initial academic and PDF layout checks remain distinct from eventual coauthor approval.

**New Section 6.3 (2026-10-09):** The [paper-facing first draft](main.tex) `Candidate-Regime Dependence of Relative Utility` has been independently written from the preserved KuaiLive P0/P1 archive and [verified run ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md). It reports 10,222 matched KuaiLive events, the native sampled/full contrast, its paired 95% interval, the crossed candidate-membership/normalization 2×2 table, three independently trained checkpoint pairs, and a concise retrospective evidence-state contribution analysis. Interpretation is explicitly noncausal and post-hoc; the same-TEST analyses are not mislabeled as new frozen policy validation. Per-seed full tables, checkpoint IDs, state decompositions and procedural records remain in the [dedicated Section 6.3 evidence audit](SECTION6_3_RESULTS_PROVENANCE_2026-10-09.md) and original ledger. Section 6.3 has completed its separately requested reviewer-style tightening; coauthor approval and final Supplementary S5/S8 assembly remain pending.

**Preserved research content:** [`section6_3_kuailive_migration_source.tex`](section6_3_kuailive_migration_source.tex) is an exact archival copy of the prior KuaiLive P0/P1 Section 6.1, including factorial and seed tables, for controlled migration to 6.3. The canonical results ledger remains [`KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md`](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md).

**Section 6.2 reviewer-tightened version:** final manuscript commit [`29801a2f`](https://github.com/mzch0210/KuaiLive-Agent/commit/29801a2f3dfba95ce5528962babb05b0eccfe89d), successful [Actions compilation #37879043504](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37879043504), [PDF/log artifact #11593392050](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37879043504/artifacts/11593392050). See the [reviewer-style issue and source audit](SECTION6_2_KBS_REVIEWER_TIGHTENING_2026-10-09.md) and the [frozen numerical evidence record](SECTION6_2_RESULTS_PROVENANCE_2026-10-09.md). Reviewer-style tightening completed; coauthor approval and later integration review remain pending.

**Section 6.3 build and visual verification:** latest code commit [`94ac9289`](https://github.com/mzch0210/KuaiLive-Agent/commit/94ac9289be00d381e2c8b98562a905712ef6ec81) passed [GitHub Actions #37880277301](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37880277301), with [PDF/log artifact #11594088285](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37880277301/artifacts/11594088285). The final 24-page PDF was visually checked on pages 19–20, with the four-cell table and complete post-hoc evidence boundary legible. See the [Section 6.3 source audit](SECTION6_3_RESULTS_PROVENANCE_2026-10-09.md). This earlier first-draft artifact is retained for comparison; the final reviewer-tightened version is documented below.

**Section 6.3 reviewer-style tightening completed (2026-10-09):** [full scholarly review audit](SECTION6_3_KBS_REVIEWER_TIGHTENING_2026-10-09.md), final Section 6.3 source commit [`a1eb2f65`](https://github.com/mzch0210/KuaiLive-Agent/commit/a1eb2f6560b1af1f5d62e26f4358790534a29570), successful [LaTeX build #37882832573](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37882832573), and [PDF/log artifact #11595053815](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37882832573/artifacts/11595053815). The 24-page PDF was checked on pages 19–20; the bibliography contains the 2022 formally published *Communications of the ACM* version. Edits narrowed noncausal 2×2 allocations, seed-level robustness, sampled-metric novelty claims, and main-vs-supplement content allocation. Coauthor approval remains pending.

**Not drafted:** Sections 6.4–6.5, Discussion, Conclusion and Abstract. Optional P2 sampling sensitivity has not been run.

**Reviewer-style 6.1 tightening complete:** see [the line-by-line academic review and frozen-result cross-check](SECTION6_1_KBS_REVIEWER_TIGHTENING_2026-10-09.md). Final PDF visual verification and compilation: [run 37876933951](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37876933951), [PDF/log artifact 11592638016](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37876933951/artifacts/11592638016). The 6.1 review remained restricted to 6.1. Section 6.2 has now been drafted independently, without modifying any later chapter.

**Verified Section 6.1 build:** [GitHub Actions #37875699664](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37875699664) completed successfully and uploaded [PDF/log artifact #11592361414](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37875699664/artifacts/11592361414). The compiler reports no fatal errors or new Section 6.1 overfull boxes; one minor pre-existing overfull paragraph remains in an earlier chapter. This is a successful PDF smoke test, not finished typographic author review.

## Build

A typical local build is:

```bash
pdflatex main.tex
bibtex8 main
pdflatex main.tex
pdflatex main.tex
```

If the local TeX installation provides `bibtex` rather than `bibtex8`, use `bibtex main` instead.

The source depends on a TeX distribution that includes Elsevier's `elsarticle.cls` and `elsarticle-num.bst`.
