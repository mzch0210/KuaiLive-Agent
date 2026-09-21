# Conditional Utility Closure Results — 2026-09-21

**Workflow:** `Dual-ID conditional utility closure`  
**GitHub Actions run:** `35579466898`  
**Status:** success  
**Task:** next-live-room, frozen sampled-active 575-candidate protocol  
**Users:** 10,222

---

## 1. Frozen primary reproduction

- Dual-ID base NDCG@10: **0.6078439**
- Always MemoryFusion: **0.5658875**
- Frozen Selective HGB: **0.6210175**
- Selective − Dual-ID: **+0.0131736**
- paired bootstrap 95% CI: **[+0.0102262, +0.0160946]**
- frozen invocation: **14.2536%** (1457 / 10222)
- reproduced Dual-ID alpha: room **0.1**, streamer **0.9**

The closure run reproduces the frozen primary scientific result before adding mechanism analyses.

---

## 2. Predicted relative utility vs realized specialist advantage

Spearman association between frozen predicted `Memory − Dual-ID` utility and realized event-level utility:

- **rho = 0.20494**
- **p = 2.28e-97**

Extreme deciles:

| Predicted-utility stratum | Realized Memory − Base utility | Fraction with positive realized utility |
|---|---:|---:|
| Bottom decile | **−0.14351** | **12.12%** |
| Top decile | **+0.10723** | **32.55%** |

Interpretation:

> The gate is **modestly predictive but decision-useful**. Predicted relative utility clearly stratifies realized specialist advantage, but the rank association is far from perfect and should not be described as strong probabilistic calibration.

Use “utility stratification / heterogeneity” rather than “well calibrated.”

---

## 3. Relative utility is not merely generic base difficulty

All routers below invoke Memory for the exact same **K = 1457** users (14.2536%).

| Router | Test NDCG@10 | Gain vs Dual-ID |
|---|---:|---:|
| Base difficulty HGB, exact-K | 0.6155595 | **+0.0077156** |
| Frozen relative-utility HGB, exact-K | **0.6210175** | **+0.0131736** |
| Oracle relative utility, exact-K | 0.6853047 | **+0.0774608** |

Paired user-bootstrap comparison:

- relative-utility router − difficulty router = **+0.0054581**
- 95% CI = **[+0.0026588, +0.0084643]**

This directly supports the method claim:

> **Specialist-minus-base utility contains actionable information beyond merely identifying hard base-model cases.**

The difficulty router itself is useful, so the correct conclusion is not that difficulty is irrelevant. It is that relative-utility prediction adds significant routing value beyond difficulty at the same specialist budget.

---

## 4. Oracle headroom

### Exact frozen invocation budget

- exact-K oracle gain vs Dual-ID: **+0.0774608**
- frozen HGB gain: **+0.0131736**
- fraction of exact-K oracle gain captured: **17.01%**

### Unrestricted realized-positive oracle

- fraction of test users/events with positive realized `Memory − Base`: **14.8308%**
- oracle NDCG@10: **0.6856283**
- gain vs Dual-ID: **+0.0777844**
- frozen HGB captures **16.94%** of this oracle gain.

A useful empirical observation is that the realized-positive prevalence (~14.83%) is numerically close to the frozen invocation rate (~14.25%), yet the frozen router captures only ~17% of oracle gain. Therefore the main remaining modeling headroom is **which cases are selected**, not simply the overall escalation budget.

Safe interpretation:

> Current routing is useful and statistically significant but far from oracle; substantial specialist-selection headroom remains.

Do not claim the HGB gate is close to optimal.

---

## 5. Final-base information-source ablation

| Gate | Test NDCG@10 | Delta vs Dual-ID | 95% CI | Invocation |
|---|---:|---:|---:|---:|
| History threshold | 0.6165479 | **+0.0087040** | [0.0058222, 0.0116712] | 18.04% |
| State-only HGB | 0.6127282 | **+0.0048843** | [0.0030236, 0.0068184] | 7.59% |
| Confidence-only HGB | 0.6127534 | **+0.0049095** | [0.0030836, 0.0067869] | 4.20% |
| State + confidence HGB, reconstructed | **0.6210406** | **+0.0131967** | [0.0103235, 0.0162537] | 14.31% |
| State + confidence HGB, frozen primary | **0.6210175** | **+0.0131736** | [0.0102262, 0.0160946] | 14.25% |

Interpretation:

1. The final Dual-ID base still supports the information-source claim.
2. State-only and confidence-only are individually useful but weaker than the simple history threshold in this final-base experiment.
3. **The strongest evidence is complementarity:** combining state + confidence substantially outperforms either information source alone and the history-only heuristic.
4. Therefore avoid wording such as “confidence alone dominates history.” The defensible claim is that **base confidence provides complementary information when combined with behavioral state**.

---

## 6. Manuscript consequences

### Main Figure 2

Use a multi-panel mechanism figure:

- predicted utility deciles vs realized `Memory − Base` utility;
- positive-realized-utility fraction by decile;
- cumulative gain vs invocation budget with oracle;
- matched-budget relative-utility vs generic-difficulty routing.

### Main Table 2

Use the final Dual-ID information ablation above.

### Recommended wording

> Predicted memory-relative utility exhibits a modest but highly significant association with realized specialist advantage. At the same 14.25% escalation budget, direct relative-utility routing significantly outperforms routing based only on base difficulty, demonstrating that the selector learns information beyond generic hard-case detection. Nevertheless, the learned selector captures only about 17% of exact-budget oracle gain, leaving substantial routing headroom.

### Guardrails

- Do not call the analysis causal.
- Do not call the utility estimator “well calibrated.”
- Do not claim state-only or confidence-only beats the history heuristic.
- Do not claim current HGB is near oracle.

---

## 7. P0 status

- **P0-B conditional-utility mechanism closure: PASSED / CLOSED.**
- **P0-C final Dual-ID information-source ablation: PASSED / CLOSED.**

Remaining primary kill gate: **P0-A full-active candidate-universe validation.**
