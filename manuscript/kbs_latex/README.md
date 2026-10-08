# KBS LaTeX manuscript

This directory is the canonical LaTeX workspace for the *Knowledge-Based Systems* manuscript.

## Files

- `main.tex` — current manuscript source. It uses Elsevier's `elsarticle` class and currently contains Sections 1–5 and a completed Section 6.1 draft: Introduction, Related Work, Problem Formulation, Base-Relative Evidence Valuation Framework, Experimental Setup, and the first part of Experimental Results.
- `kbs_references.bib` — BibTeX database for manuscript references.

## Staged-writing rule

The [conditional-value-first submission outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md) is an approved **plan**, not completed manuscript text. Keep the canonical LaTeX at Sections 1–5 plus the existing evidence-verified KuaiLive Section 6.1 until the next section is separately assigned and reviewed. Do **not** jointly generate Abstract, all Results subsections, Discussion and Conclusion; write Abstract near the final synthesis stage. The 2026-10-08 premature full-manuscript expansion was reverted to the previously verified source revision, without changing the underlying frozen results or published bibliography.

## Current review baseline

As of 2026-10-08, Sections 1–4 form the reviewed writing baseline following a cross-section P0–P2 alignment of operational-value claims, mechanism interpretation, and method reproducibility. Earlier writing freezes were reopened only for these explicitly requested scientific corrections. Section 5 (Experimental Setup) has now been drafted directly in `main.tex`, following the updated academic outline. Section 6.1 now presents verified KuaiLive P0 factorial and P1 three-seed results. Sections 6.2–6.5 and Sections 7–8 remain to be drafted. Reopen Sections 1–4 only for a substantiated scientific inconsistency or a journal requirement.

The frozen scientific boundaries include candidate-regime-specific event contexts, development-frozen utility thresholds with offline matched-budget controls, and non-causal interpretation of the separately trained context-length base comparisons. Section 4 instantiates these definitions without redefining the learning or evaluation protocol. Its method description distinguishes primary first-observed-crawl history from auxiliary strict-split history, explicitly follows the official Twitch ten-minute sampling semantics, distinguishes cross-platform policy re-fitting from zero-shot transfer, and excludes target-relative diagnostic labels from selector features. Reopen Section 4 only for a verified protocol discrepancy or journal-required correction.

## Maintenance rule

Future manuscript edits should be made in this directory rather than by creating new LaTeX files in the repository root. Markdown manuscript files elsewhere in the repository may remain as research/writing sources, but this directory is the paper-facing LaTeX workspace.

## Section 5 writing status

Section 5 was structurally rewritten on 2026-10-08 as a journal-facing Experimental Setup with five subsections and two compact scientific tables. The main paper now focuses on research tasks, baselines, comparison protocols, statistical analysis and essential implementation settings rather than chronological experiment audits. The prior six-subsection, 29-item line-edit version remains documented in [the historical reviewer tightening log](SECTION5_REVIEWER_TIGHTENING_2026-10-08.md); it is no longer the submission-oriented text. Sections 1–4 remain unchanged.

The cross-section [retrospective academic audit of Sections 1–4](SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md) motivated completed P0/P1 manuscript revisions: the memory-utility symbol is now $\Delta_M$ (with $m$ reserved for invocation count), the sampled-active fusion coefficient is scoped to its protocol, and Related Work and Framework were structurally tightened without altering the frozen experiment definitions.
**Published-version references:** All 24 citations in Section 2 Related Work and the two other bibliography records have a 2026-10-08 [final-publication source audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md). The bibliographic file now uses official DOI/PMLR/NeurIPS records rather than arXiv, with the INFORMS online-year/issue-year distinction documented. The reviewed BibTeX build succeeded in [run 37758378727](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37758378727). This closes the prior RW4 audit item for the currently cited works; any future new citation needs the same check.


The hosted PDF compilation workflow is `.github/workflows/kbs-manuscript-latex-build.yml`. The final 2026-10-08 structural revision passed [GitHub Actions build 37755123184](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184) and produced [PDF/log artifact 11539737383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184/artifacts/11539737383). No LaTeX errors or overfull lines remain in Section 5; two small overfull warnings persist in earlier chapters. This confirms successful compilation, not final publication layout approval. Dataset training scale and supplementary evidence provenance still require submission-stage completion.


## Section 6 drafting status

Section 6.1, `Candidate-Regime Sensitivity of Base-Relative Memory Utility`, is now in the canonical LaTeX manuscript as a research-results section (not an execution diary). It reports the verified matched-user sampled/full sign reversal, all four P0 candidate/reference-normalization combinations, the two-order additive allocations and paired 95% confidence intervals, and all three P1 independently trained seeds with mean/SD and retrospective evidence-state decomposition. Its outcome provenance is [the verified P0/P1 evidence ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md), based on [GPU run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645). This is supporting post-hoc evidence on an already-inspected TEST population, separate from the frozen Twitch held-out policy evaluation that belongs in Section 6.4. The optional P2 candidate-negative-sampling sensitivity has **not** been executed.

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
