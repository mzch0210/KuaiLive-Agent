# KBS LaTeX manuscript

This directory is the canonical LaTeX workspace for the *Knowledge-Based Systems* manuscript.

## Files

- `main.tex` — current manuscript source. It uses Elsevier's `elsarticle` class and currently contains Sections 1–5: Introduction, Related Work, Problem Formulation, Base-Relative Evidence Valuation Framework, and Experimental Setup.
- `kbs_references.bib` — BibTeX database for manuscript references.

## Current review baseline

As of 2026-10-08, Sections 1–4 form the reviewed writing baseline following a cross-section P0–P2 alignment of operational-value claims, mechanism interpretation, and method reproducibility. Earlier writing freezes were reopened only for these explicitly requested scientific corrections. Section 5 (Experimental Setup) has now been drafted directly in `main.tex`, following the updated academic outline. Section 6 remains unwritten in the formal LaTeX manuscript. Reopen Sections 1–4 only for a substantiated scientific inconsistency or a journal requirement.

The frozen scientific boundaries include candidate-regime-specific event contexts, development-frozen utility thresholds with offline matched-budget controls, and non-causal interpretation of the separately trained context-length base comparisons. Section 4 instantiates these definitions without redefining the learning or evaluation protocol. Its method description distinguishes primary first-observed-crawl history from auxiliary strict-split history, explicitly follows the official Twitch ten-minute sampling semantics, distinguishes cross-platform policy re-fitting from zero-shot transfer, and excludes target-relative diagnostic labels from selector features. Reopen Section 4 only for a verified protocol discrepancy or journal-required correction.

## Maintenance rule

Future manuscript edits should be made in this directory rather than by creating new LaTeX files in the repository root. Markdown manuscript files elsewhere in the repository may remain as research/writing sources, but this directory is the paper-facing LaTeX workspace.

## Section 5 writing status

Section 5 was structurally rewritten on 2026-10-08 as a journal-facing Experimental Setup with five subsections and two compact scientific tables. The main paper now focuses on research tasks, baselines, comparison protocols, statistical analysis and essential implementation settings rather than chronological experiment audits. The prior six-subsection, 29-item line-edit version remains documented in [the historical reviewer tightening log](SECTION5_REVIEWER_TIGHTENING_2026-10-08.md); it is no longer the submission-oriented text. Sections 1–4 remain unchanged.

The cross-section [retrospective academic audit of Sections 1–4](SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md) identifies notation ambiguity (memory-utility subscript versus invocation count), an overgeneralized historical fusion coefficient, Related Work listing/redundancy, and methodological repetition in Section 4. These are prioritized recommendations, not silent changes to the reviewed scientific baseline.

The hosted PDF compilation workflow is `.github/workflows/kbs-manuscript-latex-build.yml`. The final 2026-10-08 structural revision passed [GitHub Actions build 37755123184](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184) and produced [PDF/log artifact 11539737383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184/artifacts/11539737383). No LaTeX errors or overfull lines remain in Section 5; two small overfull warnings persist in earlier chapters. This confirms successful compilation, not final publication layout approval. Dataset training scale and supplementary evidence provenance still require submission-stage completion.

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
