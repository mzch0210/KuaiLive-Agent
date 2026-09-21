# Full-Active Dual-ID Validation Results — 2026-09-21

**Primary workflow:** `Full-active Dual-ID candidate-universe validation`  
**Run:** `35580324870` — success  
**Mechanism-closure workflow:** `Full-active conditional utility closure`  
**Run:** `35581670479` — success  
**Task:** next live room (`live_id`)  
**Users:** 10,222  
**Candidate rule:** every metadata-active shop room satisfying `start_timestamp <= t < end_timestamp` at the target event time.

---

## 1. Candidate-universe audit

All 10,222 test positives were metadata-active at their event timestamps (`target_active_rate = 1.0`). No positive needed the fallback inactive-target insertion.

### Test active-candidate counts

- mean: **8,269.11**
- median: **8,131.5**
- p10: **5,290.5**
- p90: **12,031.9**
- p95: **12,301**
- max: **13,266**
- min: **575**

### Dev active-candidate counts

- mean: **8,196.36**
- median: **8,169**
- p10: **4,929.7**
- p90: **12,070.9**
- p95: **12,544.95**
- max: **13,297**
- min: **576**

The full-active candidate universe is therefore roughly an order of magnitude larger than the frozen 575-candidate sampled-active protocol.

The full-active dev alpha search still selects **room = 0.1 / streamer = 0.9**, exactly matching the sampled-active Dual-ID fusion. This is useful identity-control stability evidence.

---

## 2. Why two full-active protocols were pre-specified

Candidate expansion changes candidate-wise z-normalization and confidence-feature distributions. Therefore the experiment separates:

- **A1 strict transfer:** sampled-regime alpha/HGB/threshold transferred without full-active calibration; full-active candidate-dependent quantities are only mechanically recomputed;
- **A2 full-active native:** alpha, confidence features, HGB, and threshold are selected/fitted on full-active **dev only**, followed by one-shot test evaluation.

A1 measures transfer robustness. A2 is the primary scientific validity test.

---

## 3. A1 — strict-transfer stress test

Frozen sampled policy transferred to full-active ranking:

- Dual-ID base NDCG@10: **0.3983529**
- Always Memory NDCG@10: **0.4320191**
- Selective NDCG@10: **0.4301516**
- Selective − Base: **+0.0317987**
- paired bootstrap 95% CI: **[+0.0281425, +0.0355535]**
- test invocation: **29.18%** (2,983 / 10,222)
- Base HR@10: **0.5191743**
- Memory HR@10: **0.5157503**
- Selective HR@10: **0.5489141**

Always Memory − Base:

- **+0.0336662**
- 95% CI approximately **[+0.02701, +0.04034]**.

Interpretation:

> The frozen sampled-candidate policy transfers positively to full-active ranking, but candidate-distribution shift changes its invocation rate and it does not beat Always Memory. This validates the need to distinguish transfer robustness from a candidate-native policy.

---

## 4. A2 — full-active-native primary test

All calibration uses full-active dev only.

- dev-selected alpha: **room 0.1 / streamer 0.9**
- dev-selected HGB threshold: **−0.0088912**
- dev OOF Selective NDCG@10: **0.4468705**
- dev OOF invocation: **59.998%**

### Test

- Dual-ID base NDCG@10: **0.3983529**
- Always Memory NDCG@10: **0.4320191**
- Selective NDCG@10: **0.4518011**
- Selective − Base: **+0.0534483**
- paired bootstrap 95% CI: **[+0.0482525, +0.0588362]**
- test invocation: **64.44%** (6,587 / 10,222)

HR@10:

- Base: **0.5191743**
- Always Memory: **0.5157503**
- Selective: **0.5575230**

Primary pass rule is satisfied.

Importantly, Selective is above **both** fixed choices under full-active ranking:

- Selective − Base = **+0.05345**
- Selective − Always Memory = approximately **+0.01978**.

---

## 5. Candidate-regime reversal

The most important scientific finding is not merely that full-active “passes.” The aggregate model ordering changes with the candidate universe.

### Sampled-active LOO (575 candidates)

- Dual-ID: **0.6078439**
- Always Memory: **0.5658875**
- Memory − Base: approximately **−0.04196**
- Selective: **0.6210175**
- invocation: **14.25%**

### Full-active LOO (~8.3k candidates on average)

- Dual-ID: **0.3983529**
- Always Memory: **0.4320191**
- Memory − Base: **+0.0336662**
- Selective: **0.4518011**
- invocation: **64.44%**

Therefore the globally-inferior-memory phenomenon is **real but regime-specific**, not a universal ordering. Candidate-universe expansion alone changes the prevalence/importance of memory utility enough to reverse the aggregate ordering.

Safe overarching claim:

> **Explicit relationship memory has no fixed global ordering relative to a strong identity-aware sequential recommender. Its marginal ranking utility varies across user states and evaluation regimes, including the candidate universe.**

---

## 6. Full-active utility stratification

Using the full-active-native dev-fitted utility predictor:

- Spearman predicted vs realized `Memory − Base`: **ρ = 0.23993**
- p-value: **8.76e−134**

Extreme deciles:

| Predicted-utility stratum | Realized Memory − Base | Positive-realized fraction |
|---|---:|---:|
| Bottom decile | **−0.14295** | **9.48%** |
| Top decile | **+0.17740** | **33.72%** |

Interpretation: predicted relative utility remains modestly but clearly informative under the much larger candidate universe.

---

## 7. Relative-utility routing vs generic difficulty — full-active

Exact matched budget: **K = 6,587**, i.e. **64.44%** invocation for both learned routers.

| Router | NDCG@10 | Gain vs Base |
|---|---:|---:|
| Base-difficulty HGB, exact-K | **0.4373703** | **+0.0390174** |
| Relative-utility HGB | **0.4518011** | **+0.0534483** |
| Oracle relative utility, exact-K | **0.5045696** | **+0.1062168** |

Paired user-bootstrap:

- Relative-utility − Difficulty = **+0.0144309**
- 95% CI = **[+0.0109380, +0.0179078]**.

Thus the earlier sampled-active conclusion is replicated and strengthened:

> **Directly predicting specialist-minus-base utility adds significant routing value beyond generic hard-case detection, even under full-active ranking.**

---

## 8. Oracle headroom — full-active

- exact-K oracle gain: **+0.1062168**
- learned utility gate gain: **+0.0534483**
- fraction of exact-K oracle gain captured: **50.32%**

Unrestricted realized-positive oracle:

- fraction with strictly positive realized delta: **19.69%**
- oracle NDCG@10: **0.5045696**
- gain vs Base: **+0.1062168**
- learned gate captures **50.32%** of oracle gain.

The exact-K and unrestricted oracle gains are identical because after all positive-delta cases are selected, the additional exact-K selections are largely zero-delta cases.

Compared with sampled-active ranking (~17% oracle gain captured), the same conceptual gate family is substantially more decision-effective in the full-active regime. This is another form of regime dependence.

---

## 9. Full-active information-source ablation

| Gate | Test NDCG@10 | Delta vs Base | 95% CI | Invocation |
|---|---:|---:|---:|---:|
| History threshold | 0.4341971 | **+0.0358442** | [0.0311967, 0.0404009] | 52.92% |
| State-only HGB | 0.4371359 | **+0.0387831** | [0.0336695, 0.0439738] | 63.22% |
| Confidence-only HGB | 0.4453153 | **+0.0469624** | [0.0414914, 0.0526025] | 72.21% |
| State + confidence HGB, reconstructed | **0.4520066** | **+0.0536537** | [0.0482370, 0.0588901] | 62.17% |
| Frozen full-active-native combined HGB | 0.4518011 | **+0.0534483** | [0.0481878, 0.0587226] | 64.44% |

Combined state + confidence remains strongest. Unlike sampled-active ranking, confidence-only is also stronger than history/state alone here, so the relative information value of confidence signals itself changes with the candidate regime.

---

## 10. Manuscript consequence

The paper should no longer use “memory is globally inferior” as an unqualified overarching identity of the specialist. The stronger and safer thesis is:

> **Memory-relative utility is regime-dependent. Under sampled-active LOO, memory is globally inferior but locally complementary; under full-active ranking and strict temporal shift, memory becomes broadly valuable. In all tested regimes, learned relative-utility routing can exploit heterogeneity beyond a fixed global model choice, and it contains information beyond generic base difficulty.**

This turns full-active evaluation from a mere robustness checkbox into a central result about **candidate-regime dependence**.

---

## 11. P0-A status

**P0-A full-active candidate-universe validation: PASSED / CLOSED.**  
**Full-active mechanism replication: PASSED / CLOSED.**
