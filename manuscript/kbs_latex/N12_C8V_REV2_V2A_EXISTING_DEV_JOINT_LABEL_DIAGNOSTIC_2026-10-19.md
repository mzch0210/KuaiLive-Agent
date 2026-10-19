# N12 C8V Rev2 | Original 50,049 DEV joint utility correction diagnostic (NO policy training)

2026-10-19. **READ-ONLY EXISTING DEV LABEL DIAGNOSTIC PASS, NOT AN INDEPENDENT CONFIRMATORY TEST.** Neither V2b policy training nor author approval occurred.

## Verified execution and data contracts

[GitHub Actions #39237415095](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39237415095): BOTH hosted source packaging and selfhost GPU-enabled private read-only DEV jobs **SUCCESS**. The analyzer used all 50,049 original B1 rows without selection; original B1 sampled label CSV SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea` and original full-active F CSV SHA256 `e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f` matched before reading. Full candidate counts ranged **14,022–53,762**; sampled-full rank monotonicity violations 0. All DEV data, frozen labels and authors stay private; exported only grouped scalar aggregates. No new fitting, hyperparameter selection, gate training, TEST or original files changed.

**Source**: `analysis/kbs_plan_c/n12_c8v_v2a_existing_dev_joint_label_diagnostic.py`. This is the original B1 *same-cohort exploratory DEV*, already used for earlier policy analysis; it is not new out-of-time independent evidence.

## Fixed candidate label mappings, before looking at outcomes

- `original_s`: pre-existing 575 target-retained candidate sampled NDCG.
- `rank_expansion`: recover sampled Top-10 outrank count x where sample NDCG positive, expand the rank as `1+(N-1)*x/574`, then transform to top-10 utility. Nonlinear truncation does NOT preserve unbiasedness.
- `uniform_prior_posterior`: compute full Top-10 NDCG posterior given sampled top-10 scalar and **uniform latent full rank prior 1..N**; the prior was NOT fitted to DEV and is an explicit candidate method assumption, not a realistic verified model of the platform.
- All methods compute paired `hat_delta=hat_u_M - hat_u_B` using the *same historical B1 sampled negative roster* as both original labels, not independently resampled Base and Memory.
- Full-F labels are used **only as outcomes for this diagnostic**, not to determine priors or learn policy thresholds. No fair quota comparison can be inferred.

## Actual aggregate result (original DEV, no new model)

| Method | SAS joint delta MSE | GRU joint delta MSE | SAS mean signed bias | GRU mean signed bias |
| --- | ---: | ---: | ---: | ---: |
| Original S | 0.154547688 | 0.156083555 | −0.063639362 | −0.059366980 |
| Rank expansion | 0.193363048 | 0.193387100 | −0.001364041 | −0.001419166 |
| Uniform rank-prior posterior | **0.082977598** | **0.087528999** | −0.079395706 | −0.078609398 |

**Interpretation:** Rank expansion virtually removes the *mean signed bias* in this existing cohort but **worsens per-request joint error MSE** relative to the old S labels. Uniform-rank posterior shrinks label magnitudes and reduces MSE but has large negative signed mean bias and is not justified by any empirical full-rank prior. Marginal per-expert NDCG MSE improvement need not improve paired utility quality.

## Toy sign-only gate diagnostic (uncapped, post hoc, not a learned selector)

| Method | SAS agreement with full-delta sign | GRU agreement | SAS toy regret | GRU toy regret |
| --- | ---: | ---: | ---: | ---: |
| Original S | .7089253 | .7115027 | .072524733 | .072382293 |
| Rank expansion | .7532618 | .7560191 | .074677682 | .074585882 |
| Uniform rank-prior posterior | .7141202 | .7169374 | .072524733 | .072382293 |

Rank expansion improves event-level **sign agreement** but **increases regret** under toy `hat_delta>0` calls: class accuracy and ranking utility regret are different evaluation objectives. The uniform-prior posterior has the same toy regret as original S, despite lower squared-error. Neither achieves an observed *trained policy* advantage.

Toy regret and misallocation counts are not a substitute for **actual user-fold trained DEV selector, threshold calibration, matched specialist-call budget or deployable cost**. Existing B1 S/F/Adapted training arms have already been run; results cannot be reused as evidence of new corrected-S performance.

## What this says about scientific innovation and revised V2b gate

- The original paper's claim remains valid **only for full F vs the originally tested retrospective uncorrected S**. This DEV check did not alter independently frozen same-period 30k H1 or nested 4096 H2.
- Neither tested correction is proven conditionally unbiased for `eta_F(z)=E[delta_F|Z=z]`; both remain conventional rank-estimation heuristics or an intentionally strong/unrealistic prior scenario. Google-authored KDD 2020 sampled-metric correction (https://research.google/pubs/on-sampled-metrics-for-item-recommendation/) concerns bias/MSE for sampled ranking evaluation; Subbiah et al. (CIKM 2024, https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/) address rank-based learning objectives. These are meaningful precedents, not turnkey proof of improved knowledge routing.
- **Decision: V2a empirical feasibility/source QA PASS; methodological choice remains HOLD; V2b NOT AUTHORIZED.** A legitimate incremental policy test would need a scientifically prespecified *conditional* or paired utility estimator, user-separated train/validation folds and equal information contract, and show an actual decision question beyond original B1 arms.
- No need to repeat B1 three arms, five-source B2, eight budget levels or old G5/B4-A TEST. If no theoretically valid competitor emerges, report bounded limitation, mark V2b `NOT_RUN_BY_DESIGN`, and begin I2 scientific novelty review.

## Operational control

This file preserves the exact original cohort & source hashes and reports only nonidentifying statistics. It does not constitute external academic approval, independent confirmatory validation, a new full-cohort evaluation of frozen policy quality, or journal submission. Current main.tex and Supplement remain unchanged.
