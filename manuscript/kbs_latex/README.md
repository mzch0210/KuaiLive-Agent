# KBS LaTeX manuscript

This directory is the canonical LaTeX workspace for the *Knowledge-Based Systems* manuscript.

## Files

- `main.tex` — current manuscript source. It uses Elsevier's `elsarticle` class and now contains the abstract and all eight main sections: Introduction, Related Work, Problem Formulation, Base-Relative Evidence Valuation Framework, Experimental Setup, Experimental Results, Discussion and Conclusion. The Results section is organized as conditional-value heterogeneity, frozen decision validation, candidate-regime sensitivity, robustness and computational considerations.
- `kbs_references.bib` — BibTeX database for manuscript references.

## Current review baseline

As of 2026-10-08, Sections 1–4 form the reviewed writing baseline following a cross-section P0–P2 alignment of operational-value claims, mechanism interpretation, and method reproducibility. Earlier writing freezes were reopened only for these explicitly requested scientific corrections. Section 5 (Experimental Setup) has now been drafted directly in `main.tex`, following the updated academic outline. The 2026-10-08 conditional-value-first revision drafted all Sections 6.1–6.5, Discussion and Conclusion using previously frozen Twitch results and completed post-hoc KuaiLive P0/P1 diagnostics. These texts require normal coauthor and submission-stage evidence review, but are no longer unwritten. Reopen Sections 1–4 only for a substantiated scientific inconsistency or a journal requirement.

The frozen scientific boundaries include candidate-regime-specific event contexts, development-frozen utility thresholds with offline matched-budget controls, and non-causal interpretation of the separately trained context-length base comparisons. Section 4 instantiates these definitions without redefining the learning or evaluation protocol. Its method description distinguishes primary first-observed-crawl history from auxiliary strict-split history, explicitly follows the official Twitch ten-minute sampling semantics, distinguishes cross-platform policy re-fitting from zero-shot transfer, and excludes target-relative diagnostic labels from selector features. Reopen Section 4 only for a verified protocol discrepancy or journal-required correction.

## Maintenance rule

Future manuscript edits should be made in this directory rather than by creating new LaTeX files in the repository root. Markdown manuscript files elsewhere in the repository may remain as research/writing sources, but this directory is the paper-facing LaTeX workspace.

## Section 5 writing status

Section 5 was structurally rewritten on 2026-10-08 as a journal-facing Experimental Setup with five subsections and two compact scientific tables. The main paper now focuses on research tasks, baselines, comparison protocols, statistical analysis and essential implementation settings rather than chronological experiment audits. The prior six-subsection, 29-item line-edit version remains documented in [the historical reviewer tightening log](SECTION5_REVIEWER_TIGHTENING_2026-10-08.md); it is no longer the submission-oriented text. Sections 1–4 remain unchanged.

The cross-section [retrospective academic audit of Sections 1–4](SECTIONS1-4_RETROSPECTIVE_ACADEMIC_AUDIT_2026-10-08.md) motivated completed P0/P1 manuscript revisions: the memory-utility symbol is now $\Delta_M$ (with $m$ reserved for invocation count), the sampled-active fusion coefficient is scoped to its protocol, and Related Work and Framework were structurally tightened without altering the frozen experiment definitions.
**Published-version references:** All 24 citations in Section 2 Related Work and the two other bibliography records have a 2026-10-08 [final-publication source audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md). The bibliographic file now uses official DOI/PMLR/NeurIPS records rather than arXiv, with the INFORMS online-year/issue-year distinction documented. The reviewed BibTeX build succeeded in [run 37758378727](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37758378727). This closes the prior RW4 audit item for the currently cited works; any future new citation needs the same check.


The hosted PDF compilation workflow is `.github/workflows/kbs-manuscript-latex-build.yml`. The final 2026-10-08 structural revision passed [GitHub Actions build 37755123184](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184) and produced [PDF/log artifact 11539737383](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37755123184/artifacts/11539737383). No LaTeX errors or overfull lines remain in Section 5; two small overfull warnings persist in earlier chapters. This confirms successful compilation, not final publication layout approval. Dataset training scale and supplementary evidence provenance still require submission-stage completion.

**Latest results-first manuscript build:** [run 37760743139](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37760743139), [compiled PDF/log artifact 11542735354](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37760743139/artifacts/11542735354). Compilation and PDF upload succeeded; remaining small pre-existing layout warnings in Section 3/References are not proof of camera-ready typography.


## Abstract and Sections 6–8 drafting status

The main manuscript now has a complete **draft** abstract and five-subsection Section 6 aligned to the revised [submission outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md): 6.1 heterogeneous relationship-memory value (Twitch frozen group analysis); 6.2 prospective-features/frozen TEST decision value; 6.3 KuaiLive candidate-regime dependence (P0/P1 post-hoc); 6.4 DEV-only robustness and alternative explanations; and 6.5 benchmarked computational overhead. Sections 7–8 contain drafted Discussion and Conclusion. This is not yet a full submission package.

Evidence provenance:
- [Twitch one-shot TEST run 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), 44,221 target events, realized 6,650 Memory invocations and 5,000 paired bootstrap replicates: the primary policy validation.
- [Twitch DEV-only feature ablation run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454): supporting—not held-out—feature-family evidence.
- [KuaiLive factorial and seed ledger](../../KBS_KUAILIVE_FACTORIAL_SEED_RESULTS_2026-10-08.md), [GPU run 37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645): post-hoc regime comparison and limited independent-checkpoint robustness.
- [Separate CPU efficiency run 35730086758](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35730086758): neither Twitch policy latency nor evidence of real deployment savings.

Open acceptance gates: verify complete dataset/split statistics; reconcile historical KuaiLive Base identities; preserve a durable archive of models and per-user result files beyond expiring Actions; complete Supplementary exhibits and journal-specific declarations; independent scholarly review of tables, inferences and typographic layout. Optional P2 negative-sampling sensitivity remains unexecuted.

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
