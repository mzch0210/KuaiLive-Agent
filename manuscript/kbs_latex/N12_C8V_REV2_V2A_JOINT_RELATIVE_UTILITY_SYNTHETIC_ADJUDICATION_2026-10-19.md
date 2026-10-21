# N12 C8V Rev2 | Paired Base/Memory corrected-S joint utility synthetic adjudication

2026-10-19. **PUBLIC JOINT SYNTHETIC TESTS PASS; CORRECTED-S DEV POLICY VALIDITY NOT ESTABLISHED, V2b NOT AUTHORIZED.** This is not an experiment on private DEV/TEST or any trained policy.

## 1. Why this was needed

Earlier V2a stress validated per-expert sampled Top-10 NDCG and synthetic rank-expansion/baseline/prior mappings. But N12's label is **delta** `u_10(M;F)-u_10(B;F)`, constructed using the **same target-retained 574-negative sample** for both frozen rankers. Correlation of their sampled errors matters:

`Var(e_M-e_B)=Var(e_M)+Var(e_B)-2 Cov(e_M,e_B)`.

Original B1 sampled scalar labels are the observed top10 utilities; the 128-DEV original S/F label parity [#39232305650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39232305650) confirmed equality against archived B1, but no method has yet been shown superior for corrected-S joint utility or deployment.

## 2. Synthetic joint rank design and proof scope

For each synthetic event, fix `N`, Base full rank `R_B`, Memory full rank `R_M`, and overlap `o` of the `R_B-1` and `R_M-1` negatives ranked ahead of the target. The `N-1` non-targets split into **both ahead, Base-only ahead, Memory-only ahead, neither ahead** with counts

`(o, R_B-1-o, R_M-1-o, N-1-(R_B+R_M-2-o))`.

Draw one 574-item negative set uniformly without replacement and calculate two sample ranks using these *same candidate IDs*. Joint error and its covariance are therefore generated with a valid B1-like sampling coupling. Synthetic full ranks/overlap are authored, **not** measured on M3.

Three methods are unchanged from prior V2a method screen: original sampled NDCG, rank expansion `1+(N-1)X/574` plugged into top10 NDCG, and explicit uniformly distributed full-rank prior posterior. These are candidate estimators only: they do not represent a faithful new implementation of all cited prior-art corrections.

Predefined test: N=14,022 / 53,762, eight Base/Memory full-rank pairs including two zero-delta types, minimal vs maximal feasible ahead-set overlap (32 scenarios); each scenario has **512** fixed-seed without-replacement samples. Report per-method signed bias, MSE, false Memory calls, lost positive calls, and toy oracle sign-of-delta assignment regret. Equal-weight scenario average is purely synthetic, not an empirical DEV population estimate.

## 3. Recorded CI outcome

- [GitHub Actions #39236652772](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39236652772) **SUCCESS**. **Eight** tests passed, including partitions, exact shared-negative nested ordering, equal-score zero effects, source-overlap sensitivity, deterministic fixed seed and independent-sampling negative control.
- <https://github.com/mzch0210/KuaiLive-Agent/blob/kbs-n12-single-thesis-restructure-plan-20261014/analysis/kbs_plan_c/n12_c8v_v2a_joint_relative_utility_synthetic.py> implements this public synthetic data generator and safe metrics only.
- Nonidentifying reproducible aggregate artifact is in the successful CI.

| Estimator | Synthetic joint \u0394 signed bias | Joint \u0394 MSE | Toy oracle-sign policy regret |
| --- | ---: | ---: | ---: |
| Original S | −0.0167472 | **0.2761116** | **0.1688206** |
| Rank-expansion S | −0.0297241 | 0.3501769 | 0.1695217 |
| Uniform-prior posterior S | −0.0034916 | 0.2870648 | **0.1688206** |

**Important:** A smaller average signed bias from cancellation does not mean better rank ordering or better request-level conditional value supervision. Here the rank-expansion correction that improved individual-ranker NDCG MSE under prior synthetic mixtures fails to improve joint delta MSE in this distinct designed sample. The toy policy regret is not an experimentally frozen, learned, capped selector.

### Negative control

For N=14,022, Base full rank 2 and Memory full rank 8, all Base-ahead negatives are nested within Memory-ahead set. When using **the same 574 negatives**, sampled Memory rank can never be better than sampled Base rank (0 wrong positive Memory-preference labels/512). **Illegally drawing independent samples for the two rankers** caused 16 wrong positive Memory labels/512 in this deterministic synthetic run. This is an *illustration of non-equivalent coupling*, not a measured contamination in original B1, which used shared candidates correctly.

## 4. Literature and scientific originality limits

Krichene and Rendle (KDD 2020) establish sampled metric inconsistency and that corrections can improve bias or MSE; not all corrected estimators are pointwise unbiased: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/. Subbiah, Rendle and Aggarwal (CIKM 2024) estimate ranks under negative sampling for learning recommenders, specifically WARP/LambdaRank, which makes generic rank correction **prior art**, not N12 originality: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/.

The scoped novelty remains **candidate-regime-indexed supervision for using an external historical relationship specialist** and its empirical allocation consequences. Shared-negative sampling changes how competing specialists' label errors correlate; however the present joint coupling result is a generic statistical design property, not a newly proven *relationship-specific* mechanism or new learning algorithm.

## 5. Decision and missing gates

**V2a joint-synthetic contractual PASS, but new V2b policy training still HOLD.** A paper-ready corrected-S alternative requires a predeclared conditional `E[\u0394_F | Z]` information contract, a principled paired estimator and DEV user-fold calibration design, plus methods/author approval that such a DEV-only comparison is worth performing. Existing B1 original-S/F/Adapted three-arm DEV already answers the simpler arm question; it must not be repeated blindly. If no corrected method validly targets the new scientific question, stop V2b by design and position the empirical paper with bounded claims.

No author approval, new TEST reveal, full 50,049-row replay, private event export, main.tex edit, or new supplementary PDF was performed here.
