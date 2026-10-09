# Section 6.2 frozen decision results — source and inference audit

**Date:** 2026-10-09  
**Scope:** [LaTeX §6.2 Decision Value of Predicting Relative Utility](main.tex) only.  
**Evidence hierarchy:** independent development-frozen pointwise Utility threshold tested once on untouched Twitch TEST; ex-post exact-count Difficulty/Oracle controls for selecting the same number of events; retrospective group-composition analysis computed **exclusively on development OOF predictions**. No additional policy fit or TEST-driven model revision was performed for this writing task.

## Sources of record

1. [Frozen Twitch one-shot TEST workflow 35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303), evaluation job `106686133973`, final artifact `liverec-p1-3-test-final-35708072303` (ID `10684864297`), JSON `p1_3_test_final_report.json` and event-level predictions. Outcome summaries and CIs quoted below are directly printed in the successful job log.
2. [Frozen DEV Utility/Difficulty gate workflow 35698158121](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35698158121), fit job `106652715390`, artifact `liverec-p1-2-dev-freeze-35698158121` (ID `10680854557`), report `p1_2_dev_gate_report.json` and `p1_2_dev_oof_predictions.csv.gz`.
3. The publication-facing model/feature/threshold permissions are defined in `main.tex`, Sections 3.4, 4.5 and 5.2–5.3; this manuscript subsection does not redefine them.

## Frozen Twitch TEST: 44,221 one-target-per-user events

| Policy | NDCG@10 | HR@10 | Memory invocations |
|---|---:|---:|---:|
| Always-Base | 0.5821113853 | 0.7550258927 | 0 |
| Always-Memory | 0.5397954318 | 0.6840189050 | 44,221 |
| Utility, DEV-frozen pointwise threshold | 0.5898344192 | 0.7644784152 | 6,650 |
| Difficulty, retrospective top-6,650 | 0.5833967726 | 0.7525157730 | 6,650 |
| Oracle, TEST-outcome hindsight top-6,650 | 0.6480594078 | 0.8045498745 | 6,650 |

**DEV-selected Utility threshold:** `0.004734357474290205`; **realized TEST invocation rate:** `0.1503810406820289` (15.04%). The Difficulty regressor uses the same 14 pre-outcome features as Utility but predicts Base loss rather than Memory-minus-Base utility. Its **TEST top-m event count is set retrospectively** from Utility's realized `m=6650`; it is not a separately fixed, online-capable count budget. The Oracle requires actual TEST utility and is unambiguously nondeployable.

| Paired frozen TEST contrast | Point estimate | Paired user-bootstrap 95% CI | Resamples |
|---|---:|---|---:|
| Utility minus Base, NDCG@10 | +0.007723033914 | [+0.006412671356, +0.009030280806] | 5,000 |
| Utility minus equal-count Difficulty, NDCG@10 | +0.006437646621 | [+0.005282553511, +0.007617862964] | 5,000 |
| Utility minus Base, HR@10 | +0.009452522557 | [+0.007756495783, +0.011171163022] | 5,000 |
| Utility minus equal-count Difficulty, HR@10 | +0.011962642184 | [+0.010334456480, +0.013636055268] | 5,000 |

**Prediction limitations:** Spearman between predicted and realized event utility `0.173041597355`; Oracle-minus-Base headroom `0.065948022533`; Utility captures `0.117107892213` of this fixed-count hindsight gain (11.7%). Do not describe Oracle as an operational method or theoretical bound for arbitrary future costs.

## Independent DEV-only group composition: 46,878 events

The original DEV gate's OOF CSV was read directly from artifact `10680854557`; **no TEST file was used**. Counts and enrichment were independently recomputed using the original `relationship_horizon`, `use_utility` and `use_difficulty` columns. Selection enrichment is

`(n_selected_in_group / n_selected_total) / (n_group / n_total)`.

| Target-relative DEV group | Population count | Utility selected | Difficulty selected | Utility enrichment | Difficulty enrichment |
|---|---:|---:|---:|---:|---:|
| Recent visible (represented) | 24,541 | 1,949 | 786 | 0.56727 | 0.22877 |
| Long horizon only (recoverable) | 5,879 | 2,240 | 1,371 | 2.72152 | 1.66571 |
| Unseen (unavailable) | 16,458 | 2,374 | 4,406 | 1.03032 | 1.91220 |
| **Total** | **46,878** | **6,563** | **6,563** | — | — |

These groups use observed targets and are assigned *after the outcome* solely to explain the OOF selected-event composition; the selectors are fitted without target-state membership. This evidence is descriptive and does not prove that group recognition mediates the held-out benefit. OOF training scores may be statistically dependent through overlapping folds; they are not a new independent untouched TEST.

## Manuscript acceptance checks

- §6.2 contains five concise result paragraphs and one comparison table. All frozen test metric values and confidence intervals are copied from the original final TEST report.
- Equal-count retrospective Difficulty and hindsight Oracle are explicitly distinguished from the pointwise DEV-frozen Utility policy in the prose and table caption.
- Original §6.1 figure and TEST state table remain untouched; future §6.3 KuaiLive migration source remains separately archived.
- Later §6.4 may analyze feature-family ablations but §6.2 should not pre-empt or over-claim those DEV-only experiments.
- The standard Results versus Discussion boundary remains: no new performance causality or deployment inference is claimed in §6.2.

**Academic writing rationale:** The [official KBS journal description](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051) highlights original AI decision support and practical/theoretical balance; [Elsevier's Results-section guidance](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/) recommends clear scientific questions, objective findings and nonduplicative tables. These are editorial principles, not additional experimentally verified evidence.
