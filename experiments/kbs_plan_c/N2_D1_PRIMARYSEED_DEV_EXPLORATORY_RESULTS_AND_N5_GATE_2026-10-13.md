# N2-D1 two-stage fixed-expert DEV pilot: completed, exploratory evidence for N5

**Date:** 2026-10-13. **Status:** SUCCESSFUL RUN, **POST-G5 EXPLORATORY ONLY**. Not part of N4 canonical Methods/Results or the predeclared G5 inference family.

## Verifiable provenance

- GitHub Actions run: [#38339908528](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38339908528), workflow `kbs-n2-d1-dev-pilot.yml`, source commit `8fef2bb01efa0f3976c71839a2fd07507658fa58`. Both hosted synthetic and private self-host nested DEV jobs succeeded, following the [original missing-sklearn run #38336227770](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38336227770).
- Input: 50,049 frozen corrected M3 full-active DEV author events for each of two 20261012 Base seeds (SASRec and GRU4Rec), identical fixed relationship Memory and candidate sets, 12 pre-outcome features.
- Procedure: five outer user-disjoint DEV folds, four inner user-disjoint OOF folds for fitting and pointwise threshold selection under max 30% inner DEV Memory-call limit. Both methods use histogram gradient boosting; Direct predicts `u(M)-u(B)`; Two-stage predicts `u(M)` and `u(B)` separately, then subtracts.
- The run log recorded `test_accessed:false`; no G5 labels accessed, no original TEST threshold or registered result edited.
- Public aggregate artifact `11785704918` (`kbs-n2-d1-primaryseed-two-stage-nested-dev-aggregate`) has a finite Actions retention period; log-reported result JSON SHA256: `b944e791e4797f97892bbbddb6f6729014a00cc3bc11e3cb6f1229b207897706`. User-event rows and private model files remain on host.

## Exact aggregate results from successful job logs

| Base (train seed 20261012) | Estimator | Nested DEV NDCG@10 | Gain over Always Base | Observed Memory calls | Call fraction |
|---|---|---:|---:|---:|---:|
| SASRec | Direct | 0.3026780048 | +0.0445105667 | 14,980 | 29.9307% |
| SASRec | Two-stage | 0.3013259618 | +0.0431585237 | 14,693 | 29.3572% |
| GRU4Rec | Direct | 0.3029891960 | +0.0440177248 | 14,716 | 29.4032% |
| GRU4Rec | Two-stage | 0.3029385126 | +0.0439670414 | 14,751 | 29.4731% |

- Direct minus Two-stage nested DEV NDCG: **+0.0013520430** (SASRec), **+0.0000506834** (GRU4Rec). Raw mean differences are descriptive; their uncertainty intervals were stored in the aggregate artifact but **have not yet been independently cross-checked in this memo**. No significance inference is asserted.
- SASRec Direct selected **287 more** Memory calls than Two-stage; thus its higher quality is **not a same-call-quality superiority result**. GRU4Rec Direct selected 35 fewer calls while improving its NDCG by only 0.000051; practical and inferential relevance cannot be decided from these means.
- Five outer folds re-use the same DEV observation pool rather than furnishing five independent external datasets; neither two fitted Base families nor random seeds are independent populations. The experiment was designed after original G5 TEST outcomes had been inspected, making it **exploratory** despite the nested DEV setup.
- Since conditional expectation is linear, `E[u(M)-u(B)|Z]` and `E[u(M)|Z]-E[u(B)|Z]` denote the **same population estimand**. This contrasts finite-sample regression implementations, **not** all published L2D estimators or the original DS-Frame architecture.

## Editorial handoff (N5 before final Introduction/Related Work commit)

**Preliminary scientific verdict: Do not expand claims.** Both regressions support selective value in nested DEV. The differences are modest and not consistently measured under the same realized calls. Accordingly, the central novelty remains the fixed relationship-memory relative ranking-value construct under incumbent/candidate context and its independently frozen decisions against the *original specified four objectives*, rather than a universal claim that direct-value regression beats post-hoc expert allocation. For a stronger method-superiority claim, additional fair budget-aligned comparison and genuinely independently unseen TEST would be needed.

N4 Methods describe only the established, frozen primary G5 framework; if the authors decide to publish D1, add it as explicitly exploratory comparative implementation evidence with full runtime/uncertainty/source discussion in the supplement, without modifying G5's preregistered family or trial identity. Final inclusion is a later N5/N7 editorial judgment.
