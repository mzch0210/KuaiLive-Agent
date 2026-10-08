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

Section 5 completed a 29-item KBS reviewer-style line-by-line tightening pass (2026-10-08); the canonical LaTeX retains six subsections and two method/protocol tables. See [`SECTION5_REVIEWER_TIGHTENING_2026-10-08.md`](SECTION5_REVIEWER_TIGHTENING_2026-10-08.md) for the audit register and outstanding provenance checks. The revision distinguishes KuaiLive versus Twitch percentile/OOF implementations, protects the sampled/full candidate-protocol boundary and preserves target-outcome access controls. All user/event counts, source references and previously frozen versus post-hoc experiment identities must remain traceable to the associated source artifacts. Its controlled same-checkpoint comparison is described as a supporting diagnostic, not a new independent confirmatory held-out experiment; numerical results belong in Section 6 after separate review of evidence provenance. No previously reviewed Sections 1–4 were modified in this drafting step.

A dedicated hosted LaTeX compilation workflow is defined at `.github/workflows/kbs-manuscript-latex-build.yml`, with PDF and build logs retained as GitHub Actions artifacts after successful execution.

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
