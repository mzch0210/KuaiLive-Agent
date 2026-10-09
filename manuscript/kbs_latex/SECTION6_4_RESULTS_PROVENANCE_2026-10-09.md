# Section 6.4 — robustness and alternative explanations: original result audit

**Date:** 2026-10-09  
**Manuscript scope:** [Section 6.4, Robustness and Alternative Explanations](main.tex), one DEV-only table. Sections 1–5 and existing Sections 6.1–6.3 are unchanged. Section 6.5, Discussion, Conclusion and Abstract remain unwritten.  
**Status:** Source-checked academic first draft. Independent KBS reviewer-style tightening, submission supplementary assembly and coauthor approval are distinct future gates.

## Source hierarchy (all DEV-only unless indicated)

1. [Successful run 35713931454](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35713931454) (job `106700833375`) computed both original Memory-component ablation and the exact-K OOF family comparison. Inputs are the original frozen development predictions, verified by SHA256 `9757064252c097934fa31f10a68e11bb43853ca1132aaa49da2b9794f60d3816`; the family experiment explicitly says `test_ranking_inspected: false`. All 5-fold predictions use shuffled KFold seed 20260918, 46,878 events; **K=6,563** common to all compared feature families, not the frozen TEST's 6,650 calls.
2. [Completed Memory-sensitivity record](../../KBS_ROBUSTNESS_RESULTS_2026-09-22.md), supporting [run 35724784990](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35724784990): seven DEV-only variants change long weight, short-window size and short-term decay while retaining the official Base, without re-fitting the frozen decision policy or re-opening TEST.
3. [Repaired and verified context-length intervention record](../../KBS_CONTEXT_LENGTH_INTERVENTION_REPAIR_2026-09-23_RUN35877647543.md), [repaired hosted workflow 35877647543](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35877647543) and [original GPU context models 35830028173](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35830028173). The repaired aggregation fixes frozen-Memory history-eligibility mismatch in a secondary evaluator by taking canonical frozen P1.2 Memory predictions for **all** L8/L16/L32 comparisons. Memory is invariant by direct rank/NDCG checks; the Base is independently re-trained at each length. Do not rely on the earlier failed aggregate or silently mix its Memory values.
4. [Recency and finite-context record](../../KBS_ROBUSTNESS_RESULTS_2026-09-22.md), [DEV run 35725938757](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35725938757): frozen predictions analyzed by recency bin, not independent causal visibility interventions.
5. **Designated Base competitiveness:** [Twitch same-event DEV comparison 35815886641](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35815886641) (job `107045171458`) and [KuaiLive same-candidate comparison 35820514662](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35820514662) (job `107051151609`). Auxiliary alternatives have limited architecture-size and learning-rate searches; they are **not** exhaustive optimized SOTA baselines. KuaiLive historical Dual-ID (0.61714 TEST in the independent competitiveness bundle) has a different checkpoint provenance from 6.3 same-checkpoint sampled Base (0.60709). These absolutes must not be implicitly identified or inserted into a paired difference.

## Feature-family OOF table — original job output

| Feature group | Predictors | OOF Utility-Baseline NDCG@10 gain, K=6,563 | Bootstrap 95% CI | Spearman predicted vs realized utility |
|---|---:|---:|---|---:|
| History state descriptors | 6 | +0.0037183814813 | [+0.0025587913688,+0.0049013986338] | 0.147905250962 |
| Base-score/confidence descriptors | 8 | +0.0016020356383 | [+0.0004817064653,+0.0027022333513] | 0.091089714427 |
| Combined | 14 | +0.0083809818615 | [+0.0071308497351,+0.0096265489595] | 0.189895698727 |

All gains are measured against the common development Base `0.5718533988252722`. Exact-K comparison is a descriptive same-count **OOF developmental** analysis; no selector or threshold was retrained/reselected on the untouched P1.3 TEST. The combined feature family's gains must not be presented as a causal synergy effect or a new independent TEST result.

## Frozen Memory sensitivity and recency

- Seven variants preserve the DEV sign ordering: represented/recent-visible **negative**, recoverable/long-horizon-only **positive**, unavailable/unseen **negative**. Long-weight 0.30 yields +0.13852 in recoverable; long-weight 0.60 yields +0.28231, showing quantitative sensitivity rather than invariance.
- DEV recency bins reveal a **non-monotonic** relationship: last target creator 1–4 events ago +0.04606; 5–8 −0.06511; 9–16 −0.15268; 17–32 +0.25668; 33–64 +0.20707; 65+ +0.12965; unseen −0.19562. Do not claim more age always means more utility.

## Context-length paired checks — repaired record only

| Trained Base context | Base DEV NDCG@10 | Fixed canonical Memory DEV NDCG@10 | Memory−Base |
|---:|---:|---:|---:|
| 8 | 0.52619 | 0.52170 | −0.00450 |
| 16 | 0.57185 | 0.52170 | −0.05016 |
| 32 | 0.59663 | 0.52170 | −0.07493 |

Visibility-transition comparisons use only matched DEV users: recoverable→represented for L8→L16 n=5,055 and Δ(Memory−Base) −0.44748 (95% CI [−0.45767,−0.43730]); L16→L32 n=3,617, shift −0.43229 (95% CI [−0.44381,−0.42054]). Although the canonical Memory rank remains frozen and those differences necessarily equal the negative Base gain on matched users, **independently retrained Base weights** prevent identifying a pure context-visibility effect.

## Inference and main-versus-supplement boundary

- Keep in main manuscript: one exact-count OOF feature-ablation table, two meaningful sensitivity observations (parameter sign invariance and non-monotonic recency), concise fixed-Memory context-length comparison with explicit retraining caveat, and one sentence about the limited competitiveness check.
- Leave for planned Supplementary S5/S8: per-component full Memory ablations, all threshold-dependent feature results and exact-5,000 replicate CSVs, all seven Memory settings, 7 recency bins with intervals, three context-length panels and transitions with model/source SHA fingerprints, and comparator training-grid details.
- **No completion claim:** P2 KuaiLive candidate negative-sample-size/draw sensitivity still has not been run. Section 6.4 does not present it as a completed robustness result.
- **No broad causal or SOTA claim:** These studies narrow plausible alternative explanations but do not isolate the effects of history visibility, prove one mechanism, exhaust benchmark architectures or establish online recommendation utility.
- **No evidence leakage:** All above feature-family and context-length analyses are restricted to DEV. The DEV-frozen Utility policy and untouched TEST evidence in Section 6.2 remain unchanged.

## Scholarly reporting references

[Elsevier guidance on Results](https://cn.scientific-publishing.webshop.elsevier.com/manuscript-preparation-cn/how-to-write-the-results-section-of-a-research-paper/) distinguishes objective findings from wider Discussion, recommends reporting inconvenient results and avoiding redundancy between tables/figures/prose. The [official KBS journal information](https://www.sciencedirect.com/journal/knowledge-based-systems/about/policies) is the publisher's source for journal-specific requirements; no invented KBS figure-count or word-count rule is assumed.

## Final build and typographic evidence

- **Final main.tex source commit:** [`80d1db1c`](https://github.com/mzch0210/KuaiLive-Agent/commit/80d1db1cd240adc89d1ef7dc24122bf35ddf5153). The second commit changed only one in-section wording detail, from “seven perturbations” to the accurate “seven evaluated configurations,” which includes the reference long-term weight 0.45.
- **Matching GitHub Actions compilation:** [Run #37883819061](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37883819061) completed **successfully** and uploaded [PDF and compilation log artifact #11595443761](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37883819061/artifacts/11595443761).
- **Rendered PDF:** 26 pages (Letter). PDF pages **21–22** were inspected; the feature-family Table 6 is legible, with no clipped rows or columns. The first 6.4 page ends at a complete parameter-sensitivity paragraph, followed by context-length, nonmonotonic recency and comparator limitations on the next page. No unwanted orphaned scientific-limit sentence at the bibliography transition; references begin after the section's last sentence.
- **LaTeX checks:** PDF output verified, zero fatal LaTeX errors, no missing cross-reference labels or bibliography keys and no new 6.4 overfull boxes. One pre-existing **5.51282 pt** overfull warning occurs in earlier manuscript source lines 141–142, outside the scope of this section.
- **Editing-scope guard:** Original manuscript from commit `a1eb2f65` and the new 6.4 manuscript match byte-for-byte through Section 6.3 and after the bibliography hook. Section 6.5 and subsequent chapters were not drafted. No new experiment was performed or frozen TEST policy revised.

**Acceptance status:** Section 6.4 **first scholarly draft completed**, sources verified, LaTeX compiled and PDF visibly inspected. Independent KBS reviewer-style tightening, formal Supplementary S5/S8 packaging and coauthor scientific approval remain pending.
