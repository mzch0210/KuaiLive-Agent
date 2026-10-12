# Plan C G3/E2 — Full-Active DEV Evidence and Reviewer-Style Assessment

**Audit date:** 2026-10-12  
**Evidence status:** Confirmed **DEV** findings; **TEST remains sealed**. Neither the 47,575-event held-out cohort nor an independent trained-seed replication was used in these results. The report is an acceptance-oriented appraisal, not an assertion that the journal will accept the manuscript.

## Verified executions and provenance

| Stage | Run | Status | Result |
|---|---|---|---|
| G2 TRAIN SASRec + GRU4Rec | [#38205618676](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38205618676) | success | both three-epoch fits; frozen epoch-3 checkpoints |
| G2 DEV checkpoint selection | [#38208337267](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38208337267) | success | 4096-event, 575-active-author paired checkpoint screen |
| G3 full-active DEV scoring | [#38211598562](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38211598562) | success | 50,049 events, ~33,759 active warm author candidates median |
| **G3 corrected Memory replay** | [#38212426384](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38212426384) | **success** | full-history Memory consistency verified; aggregate artifact `11729827845` |
| **E2 five DEV OOF gate comparators** | [#38212894692](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38212894692) | **success** | 12,628 unique DEV users, all 50,049 events, aggregate artifact `11730217172` |
| **E2 paired user-cluster Bootstrap** | [#38213440850](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38213440850) | **success** | 5,000 resamples, aggregate artifact `11730183210` |

Consistent upstream scientific protocol SHA256: `bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`. Selected Base checkpoint hashes:

- SASRec epoch 3: `18fb25d68970e73661a4b1418f5be05e7f8bed678d097533adf3cf1d9964d17e`.
- GRU4Rec epoch 3: `6c83dcb2e76f86e1018af467c0b0494f09b5d552c885700e92ea657cd9cc8d1a`.

Corrected G3 event-level DEV paired file SHA256: `e144d9ed4c155b51a182a58150ea17d797b3eb4ee0dac0475ccba1d34f277e8f`. E2 verified this same SHA256 before fitting. The original provisional Memory scorer was excluded because its recent-history distance and long normalization omitted TRAIN-unseen prior authors; corrected replay consumed all pre-target historical events without recomputing Base. All event-level and checkpoint files remain in private User-host cache.

## 1. Overall Base-versus-Memory outcome on identical full-active DEV events

| Condition | NDCG@10 | HR@10 | Delta NDCG vs Base |
|---|---:|---:|---:|
| Always SASRec | **0.25816744** | 0.39013767 | — |
| Always GRU4Rec | **0.25897147** | 0.39155627 | — |
| **Always Memory** | **0.34350918** | **0.53147915** | **+0.08534174 SASRec; +0.08453771 GRU4Rec** |

The fixed relationship Memory's NDCG exceeds SASRec by **33.06% relative** and GRU4Rec by **32.64% relative** on these DEV events. This is strong *within-DEV, within-task* evidence that remembered creator relationships can be informative under the M3 full-active candidate definition. It does **not** imply transfer of identical absolute numbers to earlier KuaiLive room-ranking or Twitch candidate protocols, nor independently disjoint person identities across differently anonymized releases.

## 2. Five comparable DEV OOF selective call policies

All use the same per-event Base and Memory scores, a **maximum 30% call budget**, a fivefold user-disjoint DEV OOF gate regressor where applicable, and one pointwise threshold selected to maximize the observed OOF DEV net benefit at that budget. OOF prediction and threshold selection are distinct steps: the former is cross-fitted by user, **the latter is optimized on the same OOF DEV outcome labels**, so these are discovery estimates.

| Policy | SASRec full-active DEV NDCG | GRU4Rec full-active DEV NDCG |
|---|---:|---:|
| Always Base | 0.25816744 | 0.25897147 |
| **Utility, 29.993% call-rate** | **0.30276428** | **0.30353095** |
| Uncertainty, ~29.99% | 0.28851614 | 0.28886606 |
| Difficulty, ~29.99% | 0.28250754 | 0.28380490 |
| Specialist Quality, ~29.99% | 0.27804850 | 0.27920943 |
| History, ~29.99% | 0.27484217 | 0.27557367 |
| **Always Memory, 100%** | **0.34350918** | **0.34350918** |
| Hindsight best-of-two **Oracle, not deployable** | 0.38762159 | 0.39063434 |

A hypothetical *uniformly random 30%* call-rate would have expected NDCG of Base + 0.3 × (Always Memory − Base) conditional on the same DEV event cohort, i.e. **0.28377 SASRec** / **0.28433 GRU4Rec**. This is a mathematical expectation, not a measured random-seed experimental baseline. Utility beats that expectation, whereas difficulty and specialist quality do not; uncertainty also exceeds it. Include an explicit seeded Random@30 control in future confirmation for interpretability.

The Utility gain over Always Base is **+0.04459685 SASRec / +0.04455948 GRU4Rec**, or approximately **+17.27% / +17.21%** relative. Utility > Difficulty by **+0.02025674 / +0.01972605** and Utility > strongest non-Utility comparator Uncertainty by **+0.01424815 / +0.01466489**, respectively. The same ranking of the five methods holds for both Base architectures.

Crucially, **the 30%-budget Utility gate underperforms the 100%-call Always Memory alternative by 0.04074 and 0.03998 NDCG**. This is **not** a valid basis to claim universal quality superiority of selection. The scientific hypothesis supported by these DEV results is *conditional selection decision value under matched specialist-call budget* — **not** *selective policy is globally best regardless of resource budget*.

## 3. User-cluster paired uncertainty (5,000 resamples)

Each interval below is a conditional percentile CI, paired on the **same 12,628 users** and frozen selected policy, preserving within-user dependence. These intervals **do not nest threshold optimization or re-training**, and cannot correct validation-set selection optimism.

| Comparison | SASRec: paired Δ [95% conditional CI] | GRU4Rec: paired Δ [95% conditional CI] |
|---|---|---|
| Memory − Base | +0.085342 [0.082528, 0.088160] | +0.084538 [0.081699, 0.087378] |
| Utility − Base | +0.044597 [0.042615, 0.046579] | +0.044559 [0.042591, 0.046537] |
| **Utility − Difficulty** | **+0.020257 [0.018299, 0.022233]** | **+0.019726 [0.017731, 0.021718]** |
| Utility − Uncertainty | +0.014248 [0.012524, 0.016001] | +0.014665 [0.012900, 0.016431] |
| Utility − Specialist | +0.024716 [0.022565, 0.026793] | +0.024322 [0.022155, 0.026438] |
| Utility − History | +0.027922 [0.025330, 0.030506] | +0.027957 [0.025351, 0.030631] |
| Utility − Always Memory | −0.040745 [−0.042762, −0.038734] | −0.039978 [−0.042115, −0.037883] |

These conditional DEV differences are numerically stable. However, no *independent TEST hypothesis rejection*, *cross-training-seed robustness*, or *family-wise corrected independent confidence intervals* has yet been produced. Do not report the bootstrap minimum tail fraction 1/5001 as an independent TEST p-value.

## 4. Hindsight Oracle and available value of perfect decisions

Full-choice hindsight Oracle NDCG is **0.38762159 SASRec / 0.39063434 GRU4Rec**. This is an *unconstrained* eventwise retrospective best-of-two and uses the target outcome; it is not available to a live selector.

Within the selected 30%-call setting, Utility captures approximately **34.45% / 33.84%** of the unrestricted hindsight Oracle's incremental gain over Base, whereas Always Memory at 100% captures **65.92% / 64.21%**. The different call budgets make direct efficiency comparisons unsuitable. A **budget-matched hindsight Oracle@30** on the same DEV utility array is still needed as a more relevant ceiling and should be labeled nondeployable.

## 5. Reviewer-critical implementation and interpretation caveats

1. **DEV optimization bias:** User-group OOF predictions are out-of-fold, but each threshold was then optimized using all OOF DEV targets. Fixed-policy user bootstrap conditions on this threshold and cannot serve as independent generalization inference. Final TEST must use **fixed frozen policies only**. Independent/test-specific significance with user-cluster paired intervals and preregistered multiplicity correction still pending.
2. **Always Memory dominates on M3 DEV:** This is the largest scientific-argument tension. Explain the 30% expert-call constraint explicitly. Report a genuine quality-versus-cost tradeoff and why always using Memory is not preferable under the target deployment requirements; otherwise a KBS reviewer may reject the selective architecture as unnecessary in this regime.
3. **Candidate-sensitive gating feature overhead:** `x_memory_history_supported_share` is computed by enumerating the full active-author roster and Memory-derived historical support, though it is label-free and pretarget. A 30% final invocation rate is **not** proof that only 30% of Memory-related scoring cost was paid. Benchmark preprocessing, Base, gate and Memory specialist costs separately; seek an equivalent sparse feature calculation and rerun DEV/TEST under a time-aware budget if cost claims are central.
4. **Two Base architectures, one fitted seed:** Independently retrained seed20261013/14 SASRec and GRU4Rec have not been run. These are compact D=64 baselines with specific training budgets, not guaranteed strongest state-of-the-art baselines. Any robustness/competitiveness claim must be bounded accordingly.
5. **Task change:** New M3 author-ranking and warm active-author candidate policy are structurally distinct from the original room-based KuaiLive benchmark and official per-user split. Absolute NDCG and historical NDCG shifts must not be compared without these qualifiers.
6. **Causal history:** Historical interactions are ordered by event clock then stable source-row tie. This is a documented convention, not observational proof about the real-time ordering of clock-tied events.
7. **DEV fairness:** All selective methods operate on identical frozen Base/Memory outcome arrays, similar 29.99% call rates, and only 12 pretarget numeric `x_*` features. The Memory-specific support feature is label-free but may be computationally expensive and merits an ablation to assess whether it disproportionately advantages Utility.
8. **Variance across dataset/task versus seeds:** The strong positive M3 Memory average can coexist with a negative Twitch overall Memory average; this is evidence of regime dependence, *not* evidence that a specific hypothetical relationship state has been independently causally identified.

## Publication-facing recommendation

**Keep the manuscript's central contribution as a learned Base-relative utility selector under a specified expert-call budget**, with the M3 results as substantive independent-period *DEV* support for its decision rule and cross-architecture consistency. The observed M3 quality frontier suggests an additional framing around adaptive deployment budgets, but this should not be promoted to a new central scientific claim without 30/50/100% resource tradeoffs and corresponding held-out comparisons.

**Prioritized next:** (i) measure true gate-versus-Memory latency/cost and add Random@30 and budget-matched Oracle@30, (ii) freeze all model/policy/hyperparameter choices and run additional preregistered seeds if cross-seed claims are intended, (iii) one-shot independent TEST 47,575-event evaluation with user-cluster paired CIs, three preregistered Holm-corrected contrasts, and a transparently disclosed Always Memory baseline. Preserve all negative findings. These are research-strengthening tasks, not claims that initial G3/E2 workflows failed.

**Evidence policy:** all reported figures are derived from cited project-controlled GitHub Actions artifacts, not fabricated or extrapolated into unseen TEST outcomes.
