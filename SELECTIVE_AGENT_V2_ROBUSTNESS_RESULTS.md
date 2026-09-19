# Selective Agent v2 — Robustness Results

Status: **PASS**

## A. Candidate-sampling seed robustness

Protocol is fixed across seeds: KuaiLive-Shop leave-one-out split, 574 legal active-at-time negatives + 1 positive, tuned SASRec (`lr=5e-4`, `history_max=50`), fixed training seed `20260918`, and the locked Selective Agent v2 HGB gate with 5-fold OOF dev threshold selection. Only the candidate sampling seed changes.

| Candidate seed | SASRec test NDCG@10 | Selective test NDCG@10 | Absolute delta | Relative delta | 95% CI |
|---|---:|---:|---:|---:|---:|
| 20260918 | 0.610098 | 0.623232 | +0.013134 | +2.15% | [+0.010114, +0.016310] |
| 20260919 | 0.609109 | 0.622921 | +0.013812 | +2.27% | [+0.010659, +0.016962] |
| 20260920 | 0.605386 | 0.616594 | +0.011208 | +1.85% | [+0.008509, +0.013899] |
| 20260921 | 0.609905 | 0.619280 | +0.009375 | +1.54% | [+0.006770, +0.012005] |
| 20260922 | 0.605990 | 0.615309 | +0.009319 | +1.54% | [+0.006659, +0.011916] |

Across all five seeds:

- mean absolute delta: **+0.011370**
- mean relative delta: **+1.87%**
- minimum absolute delta: **+0.009319**
- minimum 95% CI lower bound: **+0.006659**
- all five seed-specific 95% CIs are strictly positive.

The new-seed GitHub Actions run is **35448130301** and all four new seed jobs plus summary completed successfully.

## B. Global temporal landmark robustness

GitHub Actions run: **35448150972** — completed successfully.

Leakage-safe temporal protocol:

- global train cut: 80th percentile timestamp = `2025-05-20 10:31:59.642 UTC`
- global dev cut: 90th percentile timestamp = `2025-05-23 10:00:04.500 UTC`
- eligibility: at least 3 train-period interactions plus at least 1 dev-window and 1 test-window interaction
- target: first event for each eligible user in the future dev/test window
- dev history: train-period only
- test history: train-period + the selected dev landmark only; unused within-window future events are excluded
- users: **3,878**
- train rows: **280,706**
- dev rows: **3,878**
- test rows: **3,878**
- legal fixed candidate protocol: **574 negatives + 1 positive = 575 candidates**

Results:

| Method | Dev NDCG@10 | Test NDCG@10 |
|---|---:|---:|
| SASRec | 0.562031 | 0.493621 |
| MemoryFusion always | 0.559694 | 0.499498 |
| **Selective Agent v2** | **0.587969 (OOF)** | **0.518484** |

Selective Agent v2 vs SASRec on temporal test:

- absolute delta: **+0.024862**
- relative delta: **+5.04%**
- paired user-level bootstrap 95% CI: **[+0.018044, +0.031789]**
- test gate rate: **39.40%** (`1,528 / 3,878` users)
- selected users mean history length: **139.06**
- unselected users mean history length: **30.68**

The tuned SASRec configuration remains frozen; on this shifted split its best dev checkpoint is epoch 28, with dev NDCG@10 = 0.5620 and test NDCG@10 = 0.4936.

## Interpretation

Both major robustness gates pass:

1. The Selective Agent v2 gain is not an artifact of one candidate-negative sample: every one of five candidate seeds yields a positive and statistically significant improvement over tuned SASRec.
2. Under a substantially harder global temporal shift, the gain persists and becomes larger. This is consistent with the mechanism that explicit memory becomes particularly valuable when the sequential model is uncertain and the user has accumulated a long history.

The evidence supports the claim:

> A strong sequential recommender should remain the default, while explicit fused memory should be selectively invoked using user-state and base-model uncertainty signals.

These results do not establish causal business impact and do not turn MemoryFusion into an LLM agent; they validate selective memory augmentation under the frozen offline recommendation protocol.
