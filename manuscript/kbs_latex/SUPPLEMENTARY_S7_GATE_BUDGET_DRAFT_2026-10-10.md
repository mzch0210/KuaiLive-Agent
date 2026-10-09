# Supplementary S7 — Twitch DEV out-of-fold feature-family invocation budgets

**Status:** Source-checked scholarly draft, not a final journal-formatted supplement. **Scientific scope:** exploratory Twitch DEV reanalysis supporting Section 6.4 / C3; does not change the frozen one-shot TEST policy, the approved C1–C3 novelty, or the expert scoring coefficients. **Original source:** [DEV-only run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), job 106700833375, artifact 10688746451.

## S7.1 Existing prediction evidence and common-budget protocol

The original artifact contains **46,878 unique DEV user events**, each with the same Base and fixed Memory NDCG@10 and 5-fold OOF predicted relative utility and predicted Base difficulty for three feature families: history-only (6 features), Base-score-only (8), and their combination (14). These saved prediction vectors were **replayed without fitting any new model**, modifying thresholds or examining TEST labels.

We compared five exact batch-level invocation fractions: **5%, 10%, 15%, 20%, and 30%**. The corresponding integer budgets were chosen by floor(n×fraction+0.5): **2,344; 4,688; 7,032; 9,376; 14,063**. For each family and prediction target, events are sorted by its existing OOF prediction in descending order; the original event row order deterministically breaks ties. The top m events use Memory and all others use Base; decisions are compared on exactly the **same users**.

This exact top-m operation is a **retrospective batch comparison**; it is not the primary Utility policy's DEV-frozen pointwise threshold or an online deployable hard-budget rule. The budget grid was set before running the current replay, but the development data had previously supported OOF learning and the original operating-point choice. No new held-out inference follows.

**Replay guards passed:** archived OOF/source-table SHA256s; all user IDs unique; event-level utility identity; all six original **6,563-call** Utility/Difficulty selection masks identical to the original; original three Utility-vs-Base means reproduced to absolute error below 1e−12. The 6,563-point is the **historical DEV-selected 14.00017%** operating count, not an independently chosen 15% and not the separate frozen TEST's 6,650 calls.

## S7.2 Same-count Utility-selection performance

Values below are **mean NDCG@10 gains versus the same DEV Base** (Base NDCG@10 = 0.5718534); NDCG estimates and paired intervals are conditional on the original OOF predictions and exact count.

| DEV Memory call budget | m calls | History-only Utility | Base-score-only Utility | Combined Utility |
|---|---:|---:|---:|---:|
| 5% | 2,344 | +0.00221 | +0.00220 | **+0.00598** |
| 10% | 4,688 | +0.00349 | +0.00232 | **+0.00774** |
| 15% | 7,032 | +0.00371 | +0.00137 | **+0.00832** |
| 20% | 9,376 | +0.00406 | +0.00045 | **+0.00792** |
| 30% | 14,063 | +0.00311 | **−0.00282** | **+0.00736** |
| Original K=6,563 (14.00017%) | 6,563 | +0.00372 | +0.00160 | **+0.00838** |

The **combined features** obtain the highest observed Utility gain at each of the five specified percentages, but the gain is **non-monotonic** with the invocation count. Base-score-only selection becomes detrimental at 30% in this DEV replay. This qualified result supplements, rather than supersedes, the one-point feature-family table in the main Results.

### Confidence intervals for combined Utility versus Base

| DEV call budget | Combined mean Utility−Base gain | Conditional paired 95% CI |
|---|---:|---|
| 5% | +0.00598 | [+0.00513, +0.00685] |
| 10% | +0.00774 | [+0.00665, +0.00884] |
| 15% | +0.00832 | [+0.00704, +0.00962] |
| 20% | +0.00792 | [+0.00649, +0.00940] |
| 30% | +0.00736 | [+0.00574, +0.00906] |
| Historical K=6,563 | +0.00838 | [+0.00714, +0.00966] |

## S7.3 Direct pairwise comparisons, including the Difficulty objective

In addition to separate Utility gains, all comparisons below directly subtract **same-user selected-ranking utility under identical m calls**: Combined versus History-only, Combined versus Base-score-only, and Combined Utility versus Combined Difficulty. These are **DEV OOF batch-top-count comparisons**, not separately fitted alternative online policies.

| Budget | Direct paired comparison | Mean NDCG@10 difference | Conditional paired 95% CI |
|---|---|---:|---|
| 5% | Combined − History | +0.00377 | [+0.00284, +0.00472] |
| 5% | Combined − Base-score | +0.00379 | [+0.00307, +0.00450] |
| 5% | Combined Utility − Combined Difficulty | +0.00356 | [+0.00285, +0.00425] |
| 10% | Combined − History | +0.00425 | [+0.00309, +0.00538] |
| 10% | Combined − Base-score | +0.00542 | [+0.00446, +0.00646] |
| 10% | Combined Utility − Combined Difficulty | +0.00569 | [+0.00468, +0.00671] |
| 15% | Combined − History | +0.00461 | [+0.00336, +0.00579] |
| 15% | Combined − Base-score | +0.00695 | [+0.00579, +0.00814] |
| 15% | Combined Utility − Combined Difficulty | +0.00746 | [+0.00630, +0.00863] |
| 20% | Combined − History | +0.00386 | [+0.00273, +0.00502] |
| 20% | Combined − Base-score | +0.00747 | [+0.00608, +0.00884] |
| 20% | Combined Utility − Combined Difficulty | +0.00933 | [+0.00802, +0.01063] |
| 30% | Combined − History | +0.00424 | [+0.00310, +0.00542] |
| 30% | Combined − Base-score | +0.01018 | [+0.00865, +0.01170] |
| 30% | Combined Utility − Combined Difficulty | +0.01321 | [+0.01171, +0.01471] |
| Historical 6,563 | Combined − History | +0.00466 | [+0.00347, +0.00588] |
| Historical 6,563 | Combined − Base-score | +0.00678 | [+0.00564, +0.00793] |
| Historical 6,563 | Combined Utility − Combined Difficulty | +0.00713 | [+0.00602, +0.00828] |

The 3,000-replicate **paired percentile bootstrap** resamples the 46,878 unique DEV users with replacement and holds OOF models, predicted scores, selected masks and counts fixed (seed 20261010). All reported intervals are **pointwise and unadjusted**; the table contains overlapping exploratory comparisons and does not establish familywise significance or across-all-budget dominance.

## S7.4 Statistical interpretation

This analysis uses precomputed cross-fitted OOF prediction vectors, so the score for an event is not generated from a regressor fitted on that event. Nevertheless, the same DEV population has been used for earlier feature design, model and threshold selection. Report these as **conditional descriptive sensitivity estimates**, not unbiased uncertainty intervals incorporating nested tuning/model-fitting variability. The exact top-m decision uses an evaluation batch, unlike the independent TEST's frozen pointwise threshold, and cannot establish serving-time cost, fair online budget guarantees, external KuaiLive transfer, causal feature complementarity or universal superiority over learning-to-defer alternatives.

The bounded conclusion is that **the original combined history + Base-score feature family supports positive relative-utility selection gains across this finite DEV operating grid**, with direct paired comparisons versus the restricted feature families and a Base-Difficulty objective. This is relevant to C3 but **not a new test of the frozen selector**.

## S7.5 Reproducibility and remaining publication work

Original archive member SHA256s:
- OOF predictions: 25b5e560ce67d16221e483e9c18cad679eb28525ce0a8279ae91555726547627.
- Original 3-family comparison: 58d835e0ae53c43fe1ae522fdefee83374ba4ae58900968ea741780cffe92e48.

Reproduction source: [analysis/kbs_section6_stage2_dev_replay.py](../../analysis/kbs_section6_stage2_dev_replay.py). Input files reside in archived artifact **10688746451**. Its output tables contain **all six prediction orderings at the five budgets plus the original 6,563-call reference**, and direct paired contrasts for each; the entire output can be regenerated from archived inputs without model training. This S7 scholarly draft must be integrated into the final formal supplement with approval and complete citation/reference validation.
