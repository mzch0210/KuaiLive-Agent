# N12 Rev2.1 I2-A prior-art and claim-scope landing record (2026-10-20)

**Status: original manuscript claim audit performed; minimal I2-B edits authored in the same reviewed commit. I2-C new dual-PDF build is NOT YET accepted until GitHub Actions records are checked.** No original TRAIN/DEV/TEST run, frozen policy, numerical table, model weight or Supplement content is altered.

## Source-checked prior art

- Krichene & Rendle, *On Sampled Metrics for Item Recommendation* (KDD 2020), already cited by the manuscript, addresses sampled ranking metric consistency and bias/MSE correction: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Anushya Subbiah, Steffen Rendle and Vikram Aggarwal, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling*, **CIKM 2024**, proceedings **4066–4070**, DOI **10.1145/3627673.3679943**; training-rank estimation for WARP/LambdaRank: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ ; DBLP https://dblp.org/rec/conf/cikm/SubbiahRA24 . Google Research also lists a 2025 duplicate page; the refereed CIKM entry was selected for bibliography.
- Claims deliberately do **not** present N12 as the invention of sampling correction or learning-to-defer.

## Exactly three scientific wording edits

1. Related Work, `Candidate-Dependent Ranking in Live Recommendation`: acknowledges sampled-negative rank-estimation correction for WARP/LambdaRank and distinguishes that precedent from conditional historical expert-use evaluation.
2. RQ2, `Actual-candidate labels improve frozen policy outcomes`: states S means **original uncorrected retrospectively target-retained 575-candidate labels**; the pre-existing B1 adapted DEV control uses full-candidate labels (not sampled-only corrected-S).
3. Discussion, `Source Validity, Evaluation Limits and Actual Operating Conditions`: a valid sampled-only conditional paired-utility correction could narrow F/S differences; **no selector trained on such corrected labels has been evaluated**.

## Frozen content protections

All seven original primary Results LaTeX tables, four migrated Supplement tables (17 rows/49 original cells), original equations, event-cohort and user counts, effect sizes, paired CIs, Holm p values, test labels, same-period vs independent descriptions, H2 unverified prereveal acceptance and adverse cost remain unchanged by this targeted editorial commit. Existing C6 source equation/table contract, C7 full-cell audit and C8V semantic audit remain operational. A new I2 source regression guard and negative tests protect the three added scientific boundaries. Actual LaTeX builds/logs must be checked in new CI before recording PASS.

**Path A stays in force. V2b is NOT_RUN_BY_DESIGN for the two currently examined heuristics; this does not prove other corrected-S strategies ineffective. I2-D human independent referee review and C8-A responsible-author approval remain pending.**
