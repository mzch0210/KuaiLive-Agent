# N12 NI-1g — Corrected-S Method Gate

**2026-10-20. Final decision: NI-1 research audit complete; NO-GO for current corrected-S candidates entering real policy training. NI-2/NI-3 not authorized. V2b NOT_RUN_BY_DESIGN. Original manuscript unchanged.**

This is a scientific-method eligibility ruling, **not** a claim that all sampled-only correction is impossible, a KBS rejection verdict, a new experiment, or a substitute for an independent human reviewer.

## Evidence reviewed

- V2a source parity, shared-negative joint simulations, 50,049 DEV retrospective diagnostics, and previously rejected rank-expansion/uniform-prior candidates.
- NI-1b exact observational-equivalence construction; NI-1c top-10 boundary detection; NI-1d known two-state positive control; NI-1e four-state shared-negative EM and deliberately misspecified support; NI-1f 16-state partial-identification LP and synthetic finite-sample sensitivity.
- Public GitHub CI runs **#39384747179, #39386374485, #39388240227, #39389551092 and #39390620262** all completed successfully. These validate the *stated synthetic contracts*, not real-world model efficacy.
- Paper baseline: C7 **#39364334815**, C8V **#39364334948**, scientific source **36d9c3f2daed116061f12722db56448f371de60e**, 38-page main and 47-page supplement.

## Decision logic

1. **Synthetic identifiability / sensitivity: PASS under explicit assumptions.** Unrestricted latent-rank models may produce identical sampled observations with different full utility. Strong, externally supplied rank-support assumptions permit certain sampled-only corrections.
2. **Real corrected-S method: NO-GO.** Current positive estimators depend on latent full-rank and shared-overlap support specified by the synthetic generator, unavailable as validated train-only sampled information in actual M3. NI-1f's total-variation tolerances are illustrative sensitivity parameters, not statistically calibrated confidence limits.
3. **Conditional policy guarantee: NOT ESTABLISHED.** No principled train-only estimator of full conditional Memory-minus-Base NDCG, no demonstrated misspecification-robust confidence or regret guarantee, and no strictly matched, independently evaluated deployment-level policy.
4. **Originality: HIGH-CONTESTABLE.** Sampling correction, rank-distribution MLE/entropy, small-K blind spots, adaptive sampling and EM, and learning to defer have published precedents. Current toy EM/LP does not establish an original algorithm.

## Nearest first-party sources

- Krichene and Rendle, KDD 2020: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Jin et al., AAAI 2021: https://ojs.aaai.org/index.php/AAAI/article/view/16537
- Li et al., AAAI 2023: https://ojs.aaai.org/index.php/AAAI/article/view/25561
- Subbiah et al., CIKM 2024: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/
- Mao et al., ICML 2024: https://proceedings.mlr.press/v235/mao24d.html
- KBS journal scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051

## Hard gates for any future restart

A novel method proposal must first show: (a) a legal sampled-only information contract without disguised full-label priors; (b) a falsifiable and defensible joint-rank model or meaningful identified bounds; (c) finite-sample and misspecification analysis connected to conditional full-value or decision regret; (d) a precise online-versus-batch matched-call estimand and precommitted user-group fitting/calibration; (e) genuinely new authorized evaluation data rather than repurposed revealed G5/H1 TEST; and (f) a specific nontrivial difference from the literature with responsible-author approval. Absent these, do not start NI-2, NI-3 or V2b.

## Handoff

Preserve Path A and current scientific manuscript. RQ2 already reports only F complete-policy superiority over the **original uncorrected target-retained sampled S**, along with different natural call rates. The trained corrected-S rival, external quota justification, real gate cost, new-period generalization and RQ3 composite-null prereveal shortfall remain openly limited.

**NI-0 DONE; NI-1a–f synthetic investigation COMPLETE; NI-1g FINAL METHOD NO-GO; NI-2/NI-3 NOT STARTED; NI-4 NO MANUSCRIPT CHANGE; E6/NI-5 RESPONSIBLE AUTHOR JOURNAL GO/REDIRECT/HOLD PENDING.** An unavailable private external pre-review is not verified as a KBS submission requirement. A human responsible author must review declarations, permissions and the submission decision.