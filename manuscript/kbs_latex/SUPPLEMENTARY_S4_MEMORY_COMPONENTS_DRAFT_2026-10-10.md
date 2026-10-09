# Supplementary S4 — Memory component and history-horizon diagnostics

**Status:** Scholarly draft from a completed DEV-only experiment. Not yet typeset or coauthor-approved as a final journal supplement. **Primary source:** [Twitch DEV run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454), job 106700833375, artifact 10688746451, 46,878 one-target-per-user development events. **Purpose:** Support C1 and Section 6.4 without changing the approved paper contribution or one-shot TEST analysis.

## S4.1 Specification and reproduction

We replay the following fixed-scoring specialist rankings on identical available-streamer candidates: Popularity only (training-only normalized log-popularity); Short only (last 10 pre-target user–creator events with exponential recency decay); Long only (historical creator-specific count divided by the highest such count for that user); Short+Long (equal weights; ranking-equivalent to the 0.45/0.45 coefficients without popularity); and frozen Full Memory (0.45 Short + 0.45 Long + 0.10 Popularity). The original archived evaluator reproduced the frozen Full Memory ranks, NDCG@10 and HR@10 **with zero mismatches**, as well as candidate counts and history lengths.

Represented, recoverable-but-unrepresented and unavailable states use the **observed target**, making them retrospective groups rather than features available to a deployment selector.

## S4.2 Complete DEV component results

| Target history state | Events | Ranker | NDCG@10 | Base | Ranker−Base | 95% paired bootstrap CI |
|---|---:|---|---:|---:|---:|---|
| Overall | 46,878 | Popularity only | 0.08589 | 0.57185 | −0.48596 | [−0.48989, −0.48193] |
| Overall | 46,878 | Short only | 0.39574 | 0.57185 | −0.17612 | [−0.17928, −0.17303] |
| Overall | 46,878 | Long only | 0.52761 | 0.57185 | −0.04424 | [−0.04722, −0.04130] |
| Overall | 46,878 | Short+Long | 0.52081 | 0.57185 | −0.05104 | [−0.05393, −0.04825] |
| Overall | 46,878 | Full Memory | 0.52170 | 0.57185 | −0.05016 | [−0.05307, −0.04741] |
| Represented | 24,541 | Popularity only | 0.10554 | 0.85972 | −0.75417 | [−0.75839, −0.74993] |
| Represented | 24,541 | Short only | 0.74451 | 0.85972 | −0.11521 | [−0.11959, −0.11076] |
| Represented | 24,541 | Long only | 0.84720 | 0.85972 | −0.01251 | [−0.01549, −0.00952] |
| Represented | 24,541 | Short+Long | 0.84671 | 0.85972 | −0.01300 | [−0.01599, −0.01003] |
| Represented | 24,541 | Full Memory | 0.83977 | 0.85972 | −0.01995 | [−0.02307, −0.01693] |
| Recoverable | 5,879 | Popularity only | 0.07861 | 0.30201 | −0.22340 | [−0.23230, −0.21448] |
| Recoverable | 5,879 | Short only | 0.01293 | 0.30201 | −0.28908 | [−0.29699, −0.28092] |
| Recoverable | 5,879 | Long only | 0.63890 | 0.30201 | +0.33688 | [+0.32767, +0.34628] |
| Recoverable | 5,879 | Short+Long | 0.58673 | 0.30201 | +0.28471 | [+0.27585, +0.29355] |
| Recoverable | 5,879 | Full Memory | 0.53298 | 0.30201 | +0.23097 | [+0.22177, +0.24036] |
| Unavailable | 16,458 | Popularity only | 0.05918 | 0.23900 | −0.17982 | [−0.18475, −0.17486] |
| Unavailable | 16,458 | Short only | 0.01242 | 0.23900 | −0.22658 | [−0.23127, −0.22197] |
| Unavailable | 16,458 | Long only | 0.01131 | 0.23900 | −0.22770 | [−0.23243, −0.22312] |
| Unavailable | 16,458 | Short+Long | 0.01131 | 0.23900 | −0.22770 | [−0.23243, −0.22312] |
| Unavailable | 16,458 | Full Memory | 0.04338 | 0.23900 | −0.19562 | [−0.20033, −0.19088] |

The above CIs are the **original 5,000-user-resample percentile intervals for Ranker−Base** within each fixed group. They are conditional on fitted rankings and retrospective group assignments, unadjusted for 20 comparisons.

## S4.3 Direct same-user paired variant comparisons

We additionally compare the original variant-specific NDCG@10 of the identical **5,879 recoverable DEV users**, rather than subtracting marginal CIs. The new 5,000-replicate user-paired percentile bootstrap uses seed 20261012. All 20 original mean Variant−Base results were reproduced within 1e−12 before the new pairing.

| Recoverable DEV contrast | Mean difference | Conditional paired 95% CI |
|---|---:|---|
| **Long only − Full Memory** | **+0.10592** | **[+0.10096, +0.11061]** |
| Short+Long − Full Memory | +0.05374 | [+0.04956, +0.05792] |
| Long only − Short+Long | +0.05217 | [+0.04918, +0.05508] |
| Short only − Full Memory | −0.52005 | [−0.52720, −0.51288] |
| Popularity only − Full Memory | −0.45437 | [−0.46295, −0.44594] |

The Long-only versus Full Memory contrast is **negative** in the unavailable subgroup (−0.03208), underscoring state dependence rather than universal superiority.

## S4.4 Interpretation and uncertainty limits

The observed recoverable subgroup shows stronger performance for the long-history ranking variant than for the originally fixed Full Memory. However, changing component scores also changes candidate ordering, score ties and interactions among retained components. This is **not causal identification** of the information contribution of each term, not a newly selected expert, and not justification for modifying the previously frozen policy. The bootstrap keeps Base, group membership and variant scores fixed, excludes training and model-choice uncertainty, and is exploratory without multiplicity control. The scientific inference remains **operational and Base-relative** under the specified evaluation protocol.

## S4.5 Reproducibility

Original artifact input SHA256s:
- Event scores: b84e187290a7df2918e3bd050c4ab0a6a2baac611f72eb72f8616c7634c0644b.
- Original 20-row table: cc97794c49431c547ccf08a29da96bc275a900ed78a9ae71674b748b05e0750a.

All rows and new paired contrasts can be reproduced without training or TEST access using [the stage-2 DEV replay source](../../analysis/kbs_section6_stage2_dev_replay.py). The original rank-level arrays remain available in Actions artifact 10688746451. Complete supplementary publication formatting and coauthor sign-off are outstanding.
