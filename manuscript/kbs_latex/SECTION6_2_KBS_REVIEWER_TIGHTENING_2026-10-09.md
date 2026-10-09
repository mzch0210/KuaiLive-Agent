# Section 6.2 — simulated KBS reviewer-style tightening

**Date:** 2026-10-09  
**Scope:** Only [Section 6.2, *Decision Value of Predicting Relative Utility*](main.tex) and its policy-comparison table. Sections 1–5, the previously reviewer-tightened Section 6.1, the preserved KuaiLive Section 6.3 migration source, and all unwritten chapters were not modified.  
**Writing baseline:** prior Section 6.2 first draft, source blob `f3a72268e2e811d515bd18b253db55cd21f079de`.  
**New revision:** commit [`b0a1fffc`](https://github.com/mzch0210/KuaiLive-Agent/commit/b0a1fffc986330186a90b916e950229aca74bc39).  
**Evidence:** [TEST one-shot workflow #35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), evaluator `analysis/liverec_p1_test_evaluate.py`; [DEV gate-fit workflow #35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121), `analysis/liverec_p1_dev_gate_fit.py`; [underlying frozen-result ledger](SECTION6_2_RESULTS_PROVENANCE_2026-10-09.md).

## Overall review decision: scientifically supported, but requires correct comparison permissions and bounded claims

The primary one-shot held-out contrast is clear, numerically reproducible, and distinguishes a frozen Utility selector from an always-Base ranking. The most likely reviewer objections concern (i) comparing a **pointwise development-frozen rule** with a **retrospective batch-wide top-$m$ comparator** as though both were deployable policies; (ii) overstating the meaning of an Oracle constructed from observed TEST outcomes; (iii) implying fixed-policy paired Bootstrap intervals include model/refit uncertainty; and (iv) claiming that retrospective relationship-state enrichment explains causal expert solvability.

## Issue-by-issue resolutions

| Priority | Reviewer objection | Resolution in revised Section 6.2 | Evidence/source |
|---|---|---|---|
| **P0-1** | Utility may be portrayed as a test-tuned threshold selector. | State that the regressor and pointwise invocation threshold were chosen from DEV OOF and frozen before one-shot TEST; report actual 6,650/44,221 events (15.04%). | TEST source lines 147–156; manifest threshold `0.004734357474290205` from DEV fit. |
| **P0-2** | Equal invocation *counts* do not mean equal access to information or identical deployability. | Explain that Difficulty uses the same pre-outcome feature family but is **ranked across the full TEST batch**, using $m$ fixed after observing Utility's realized TEST selection count. Keep comparison as an offline **event-choice at matched count** analysis, not an online fixed-count/budget guarantee. | `liverec_p1_test_evaluate.py` lines 24–34, 147–162. |
| **P0-3** | Oracle can be misconstrued as an attainable online baseline or unrestricted theoretical upper bound. | Describe Oracle as the maximal *hindsight fixed-$m$ choice* between these two specified Base/Memory rankings on this same evaluation population. Not valid for different experts, candidate protocols, budgets, or deployment. | `liverec_p1_test_evaluate.py` lines 145–162; oracle NDCG@10 0.6480594. |
| **P0-4** | Section 6.1 uses outcome-dependent states; cannot treat them as serving features. | Open Section 6.2 by distinguishing the target-defined diagnostic states of 6.1 from the pre-outcome history and Base-score features used in the gate. DEV group enrichment remains post-hoc descriptive. | Manuscript Sections 3–5 and original frozen feature schema. |
| **P1-1** | Confidence intervals might appear to account for threshold choice, training variability, and future invocation rate. | Cite 5,000 paired event/user bootstrap resamples while holding fitted predictors, threshold and observed selection masks fixed. These are conditional CIs for the observed test ranking outcomes, not re-training uncertainty. | `liverec_p1_test_evaluate.py` lines 37–56, 155–190. |
| **P1-2** | The main table and prose could repeat every metric and comparator. | Main table contains all 5 policy rows; prose gives two principal paired ΔNDCG@10 estimates and compact secondary HR@10 contrasts with intervals. | Original successful final TEST JSON and Section 6.2 result table. |
| **P1-3** | The central Difficulty control needs precise estimand and restricted generality. | Emphasize Utility–Difficulty = +0.00644 [0.00528,0.00762] *at this fixed TEST invocation count*; do not claim global dominance over all difficulty-based selectors or calibration methods. | Final TEST report, paired Bootstrap. |
| **P1-4** | DEV OOF enrichment might be misused as causal mechanism or independent validation. | Retain the 2.72× vs 1.67× recoverable and 1.03× vs 1.91× unavailable group contrasts solely as retrospective selection-composition context; state target labels unavailable to either regressor. | DEV-only artifact 10680854557; OOF fit test. |
| **P1-5** | Claiming convergence to Oracle would be inconsistent with modest predictive accuracy. | Explicitly report Spearman 0.173, Utility capture of 11.7% of fixed-$m$ hindsight Base-gap, and restriction of that ratio to observed TEST models and events. | Frozen TEST report, `oracle_headroom`. |
| **P1-6** | Results text should not become an experimental diary or Discussion. | Use five short evidence-focused paragraphs plus one self-contained result table, referring to Section 5 rather than recounting GitHub/runner chronology in the actual manuscript. | [Elsevier Results guidance](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/). |

## Quantitative integrity gate

| Item | Fixed, verified value |
|---|---|
| Test events | 44,221; one target per user |
| DEV-trained Utility threshold | 0.004734357474290205 |
| Realized Memory invocations | 6,650 (15.038104%) |
| Always-Base / Always-Memory / Utility NDCG@10 | 0.5821113853 / 0.5397954318 / 0.5898344192 |
| Retrospective Difficulty / hindsight Oracle NDCG@10 | 0.5833967726 / 0.6480594078 |
| Utility−Base NDCG@10 | +0.0077230339, 95% paired CI [+0.0064126714, +0.0090302808] |
| Utility−Difficulty NDCG@10 | +0.0064376466, 95% paired CI [+0.0052825535, +0.0076178630] |
| Utility−Base HR@10 | +0.0094525226, CI [+0.0077564958, +0.0111711630] |
| Utility−Difficulty HR@10 | +0.0119626422, CI [+0.0103344565, +0.0136360553] |
| Spearman predicted–realized utility | 0.1730415974 |
| Fixed-count Oracle gain over Base | +0.0659480225 NDCG@10 |
| Fraction of hindsight gain captured | 11.710789% |

All point estimates and intervals are from the **original** frozen final TEST run. No new TEST analysis was used to select a gate or redefine hypotheses in this writing revision. CI exclusions of zero apply to the reported paired contrasts; they are not claims of multiplicity-adjusted inference across every exploratory comparison.

## Remaining acceptance limits

- This is one held-out dataset and one frozen policy, not a multi-dataset gate replication.
- Difficulty's batch-wise top-$m$ implementation and access to the *realized count* must remain explicit in the main paper; a new independently DEV-frozen Difficulty threshold experiment would require a separate frozen trial.
- The hindsight Oracle is optimal only over the fixed set of two ranking actions with exactly the same selected count.
- No claimed online speedup, business uplift, causal outcome effect, or learned-theory novelty follows from the observed ranking results.
- Full reproducibility requires long-lived per-event predictions, exact model hashes, and unexpired evaluation artifacts; Actions compilation alone is not a provenance substitute.

## Publication context

The [official NeurIPS 2022 publication](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract-Conference.html) on post-hoc deferral establishes that routing among a model and expert is a recognized technical problem; the paper here claims *live-streaming relationship-evidence utility conditions and observed decision value*, not inventing that general paradigm. [Elsevier's Results-writing guide](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/) recommends accurate, nonredundant reporting of both positive and negative evidence.

## Final source, build, and typography verification

The final scoped rewrite is at [commit `29801a2f`](https://github.com/mzch0210/KuaiLive-Agent/commit/29801a2f3dfba95ce5528962babb05b0eccfe89d). After removing an ineffective manual `samepage` pagination rule, the DEV-only composition and Oracle explanations were condensed without removing the essential numeric comparisons, information boundary, or restricted bound. The active main-paper subheadings remain exactly 6.1 and 6.2; no other section was drafted or reopened.

The revised manuscript compiled successfully on [GitHub Actions #37879043504](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37879043504), with [PDF/log artifact #11593392050](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37879043504/artifacts/11593392050). The resulting PDF contains 23 pages. Rendered pages 18–19 were inspected: Section 6.2 prose and the five-row policy-comparison table are readable, with no clipped metrics, missing references or Section 6.2 overfull-box warning. The short concluding Oracle paragraph currently spans a normal page boundary; it is grammatically coherent on both sides and will be reflowed when later sections are added. The one existing 5.51-pt overfull paragraph lies in earlier LaTeX lines 141–142, outside this editing scope.

**Status:** Reviewer-style editorial tightening, original-source verification, LaTeX compilation and rendered-PDF inspection **completed**. Coauthor academic approval and eventual multi-section integration review remain necessary. This is not a real KBS peer-review report or a guarantee of acceptance.
