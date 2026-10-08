# KuaiLive factorial candidate/reference normalization and three-seed robustness — completed evidence

**Date:** 2026-10-08  
**Scientific status:** completed, **post-hoc supporting** controlled-protocol diagnostic on the already-studied 10,222-user KuaiLive TEST population, not a fresh independent held-out policy trial.  
**GPU run:** [37751814645](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645) — both preflight and paired_gpu succeeded, including all P0 replay, P1 training, report, manifest and artifact-upload steps.  
**Compact source artifacts:** [11538678848](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538678848) (`kbs-kuailive-factorial-results-37751814645`, results JSON and 10,222-event CSV.gz per seed); [11538867565](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37751814645/artifacts/11538867565) (new seed checkpoint pairs, 604 MB compressed). Both currently exist but GitHub Actions retention is finite.  
**Scripts:** [`analysis/kbs_kuailive_factorial.py`](analysis/kbs_kuailive_factorial.py) and [GPU workflow](.github/workflows/kbs-kuailive-factorial-seeds.yml).  
**Prior comparison:** [single-checkpoint same-candidate report](KBS_KUAILIVE_SAME_CHECKPOINT_RESULTS_2026-10-08.md).

## Protocol and interpretation

For each user, `S` is the same 575-item target-plus-negative sampled-active set and `F` is its verified full-active superset. One fixed trained Room-SASRec and Streamer-SASRec model pair yields full-candidate raw scores, reused by exact subset extraction for `S`. Room fusion `alpha=0.125` is fixed across all three training seeds and both candidate regimes; Memory, history and target are unchanged.

Let `g(C,R)` denote **Memory NDCG@10 minus Base NDCG@10**, where `C` is the **ranked candidate set** and `R` is the candidate set supplying separate per-branch z-score normalization moments. Four values are obtained per matched event:
- `SS` = sampled rank set / sampled normalization reference (original protocol);
- `SF` = sampled rank set / full-active normalization reference (analytic mixed counterfactual);
- `FS` = full-active rank set / sampled normalization reference (analytic mixed counterfactual);
- `FF` = full-active rank set / full-active normalization reference (original protocol).

The two-path Shapley-style **descriptive algebraic decomposition**, calculated per user and then averaged, is:

```text
Membership  = [(FS - SS) + (FF - SF)] / 2
Normalization = [(SF - SS) + (FF - FS)] / 2
Total shift = FF - SS = Membership + Normalization
```

The factor terms are path-average allocations under the exact specified scoring scheme, **not causal identification** of independent real-world manipulations. They also depend on single-target NDCG@10 and the chosen candidate sets; candidate count itself changes rank difficulty.

## P0: baseline checkpoint and full 2×2 factorial

Seed `20260918` was replayed with identical checkpoint SHA256s and dataset hashes. Both original matched cells and their difference exactly reproduce the earlier [run 37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476).

| Memory−Base NDCG@10; `20260918` | Reference `S` | Reference `F` |
|---|---:|---:|
| **Rank candidates `S`** | **SS −0.04120411** | SF −0.04141760 |
| **Rank candidates `F`** | FS +0.04761085 | **FF +0.04630669** |

**P0 user-paired percentile bootstrap (3,000 replicates; 10,222 users):**

| Descriptive quantity | Mean | 95% user-paired CI |
|---|---:|---:|
| Membership allocation | **+0.08826963** | [+0.08286671, +0.09397065] |
| Normalization allocation | **−0.00075883** | [−0.00117294, −0.00035507] |
| **FF − SS** | **+0.08751080** | [+0.08209796, +0.09325975] |

Thus the membership component contributes approximately **100.87%** of the net shift; the normalization component offsets about **0.87%**. This percentage describes a signed algebraic contribution, **not a percentage of explained statistical variance**. The new P0 bootstrap CI for `FF−SS` differs slightly from the earlier run's CI because bootstrap seed/index draws differ; the point estimand and identical event scores are the same.

For the primary seed the Base scores underlying the cells were `Base_SS=0.60709158`, `Base_SF=0.60730507`, `Base_FS=0.38440826`, `Base_FF=0.38571242`; Memory is `0.56588746` on S and `0.43201911` on F. **Do not substitute any of these as historical native or strict-transfer Base anchors.**

## P1: new independent training seeds

All three model checkpoint pairs are distinct (two new pairs were trained once at seeds 20260919 and 20260920; 20260918 reused its verified cache). Training protocol, input data, alpha, Memory and evaluation samples are held constant. No seeds were dropped for sign or magnitude.

| Training seed | Sampled Memory−Base (SS) | Full Memory−Base (FF) | FF−SS | 95% paired CI | Membership | Normalization |
|---|---:|---:|---:|---|---:|---:|
| 20260918 | −0.04120411 | +0.04630669 | **+0.08751080** | [+0.08209796,+0.09325975] | +0.08826963 | −0.00075883 |
| 20260919 | −0.05157020 | +0.03206113 | **+0.08363134** | [+0.07804704,+0.08938187] | +0.08438602 | −0.00075469 |
| 20260920 | −0.04903770 | +0.03504633 | **+0.08408403** | [+0.07853540,+0.08945325] | +0.08424480 | −0.00016077 |

Across seeds (treating each checkpoint pair as one training realization):
- `FF−SS` **mean +0.08507539**, sample **SD 0.00212124**, range **[+0.08363134,+0.08751080]**; all 3/3 exhibit negative SS and positive FF contrasts.
- `SS` mean **−0.04727067**, `FF` mean **+0.03780472**.
- Mean membership allocation **+0.08563348**; mean normalization allocation **−0.00055809**.
- The per-user bootstrap uncertainty conditions on the seed/checkpoints and evaluation users; the seed SD reflects changes across three training realizations. Three seeds are **not** an independent dataset replication or a sufficiently large distribution for a general population-of-seeds confidence claim.
- The normalization contribution's 95% user-paired interval overlaps zero at seed 20260920 `[−0.00052317,+0.00017555]`; its negative sign should not be called universally significant.

**Trained checkpoint SHA256 identities:**

| Seed | Room checkpoint | Streamer checkpoint |
|---|---|---|
| 20260918 | `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7` | `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945` |
| 20260919 | `395d1b1c881d20cbda5d24c36c30685fd1524a0ec98586c8c71ad7c245505b2a` | `9f1b11cf27e0c802f71bb8b1bef646bb392b28d560e3aabda03f36fe01e2b637` |
| 20260920 | `84c4ef5e45592fc480096dfe4e501046ede37c1f936484ed83f3bd56e1f49191` | `7043b275b56a75fd5d7aeadfd7e69d5447128ce9f55f3bd6a0f275a24dd2d144` |

## State-wise robustness

The retrospective target-relative state partition stays exactly fixed at `represented=4589`, `recoverable-but-unrepresented=206`, and `unavailable=5427` users for every seed and candidate universe.

| State | Share | Seed 20260918 shift | Seed 20260919 shift | Seed 20260920 shift | Across-seed mean shift | Contribution to overall mean |
|---|---:|---:|---:|---:|---:|---:|
| represented | 44.89% | +0.087905 | +0.081922 | +0.088711 | **+0.086179** | +0.038689 |
| recoverable-but-unrepresented | 2.02% | −0.101969 | −0.100521 | −0.127426 | **−0.109972** | −0.002216 |
| unavailable | 53.09% | +0.094370 | +0.092067 | +0.088200 | **+0.091546** | +0.048603 |

The weighted contributions sum to `+0.085075` up to displayed rounding. The aggregate reversal is thus **not** due to larger prevalence or larger candidate-regime gains within the recoverable group: this group's relative advantage **contracts** in all three seeds. The positive shift predominantly comes from represented events and smaller relative losses on unavailable events. The latter may remain negative in absolute Memory-minus-Base terms.

## Integrity and efficiency

- The workflow verified training and test input SHA256, fixed ReChorus commit `c164ec4303cc20ddcfbd1b57de366a481811d1e5`, deterministic full-score/subset identity, model SHA256 identities, 10,222 unique users per seed, and inclusion of the sampled positive and sampled candidates in full candidates.
- Source ZIP reinspection independently reproduced 10,222 unique user rows for **each** seed. The maximum absolute discrepancy in the event-level `Membership + Normalization - (FF−SS)` identity was approximately `1.7×10^-16`; all 3 seed CSV datasets had exactly the same state counts.
- One full-candidate scoring pass per seed is reused for all four cells and 3,000 user-bootstrap draws. Each per-seed factorial scorer took roughly **70 seconds wall time**; the P0 stage did **not** retrain. The full GPU job ran ~19m49s, including two new model pairs and uploads.
- Compact data/results artifact was **<1 MB**, separately from **604 MB** of newly trained weights, avoiding duplicate uploads of the original seed-20260918 weights.
- `torch.load(weights_only=False)` emitted an upstream security/future warning; this is not an experimental failure but should be treated as a future reproducibility and trusted-model-loading hardening item.

## Evidence strength, limitations, and manuscript implications

**Supported, as a post-hoc protocol contrast:** the fixed-checkpoint sampled/full inversion persists for all three prespecified training seeds. In a 2×2 evaluation-protocol decomposition, the *ranked candidate universe* drives the large majority of the observed difference; changing the z-score reference alone contributes little net difference for these models and users. The same state-conditional pattern repeats across seeds.

**Not supported:** independently randomized causal identification of candidate-set effects; a universal sign law across datasets or training seeds; generalization to online user satisfaction or commercial conversion; or recasting this reused-TEST diagnostic as new independently confirmatory policy evidence. The 2×2 mixed cells intentionally depart from the original serving score calibration.

**Main paper:** report the matched-checkpoint paired effect and main P0 factor decomposition together in Section 6.1, ideally in a figure whose label explicitly says “post-hoc supporting diagnostic.” Summarize three-seed direction and mean±SD in Section 6.1 or supplementary S5, with per-seed/stratified tables and source manifests in the supplement. In Discussion Section 7.2, refine the mechanism language to “candidate-universe-dependent rank utility dominates the standardization-reference allocation in the specified two-path decomposition,” not isolated real-world causal membership effects. Preserve the original frozen Twitch utility policy result as a separate evidence tier.

**Potential next analysis:** P2 variation of negative sample sizes/draws is optional; it is valuable for the dependence of effect magnitude on negative-sample design, but not necessary to establish that P0/P1 executed successfully.

## Scholarly reference

Krichene and Rendle (2020), [*On Sampled Metrics for Item Recommendation*](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/), KDD, DOI 10.1145/3394486.3403226. Their work documents that sampled ranking metrics can fail to preserve even relative comparisons between recommenders, motivating explicit separation of sampled and full-candidate evaluation settings.
