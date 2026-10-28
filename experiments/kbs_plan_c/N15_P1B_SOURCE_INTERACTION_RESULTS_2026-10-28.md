# N15 P1-B — Full-vs-Long source × supervision interaction results

**Date:** 2026-10-28  
**Decision status:** COMPUTATION PASS; result is **POST-G5 EXPLORATORY DEV ONLY**. No new confirmatory TEST result and no manuscript promotion yet.

## 1. Run and artifact provenance

- Successful Actions run [#40622271751](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622271751), commit `96eaa2a809e7288ac037933bcaca8785d4c107f7`.
- A preceding duplicate run [#40622237969](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622237969) also completed successfully.
- Latest aggregate-only artifact: [n15-p1b-source-interaction-dev-aggregate](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/40622271751/artifacts/12788126538), artifact SHA256 `6aab1febf65a5fde75535c69ec0040e14970501058e05021e14abaa66153e214`.
- Output schema `kbs-n15-p1b-exact-budget-source-supervision-interaction-v1`; status `DEV_EXPLORATORY_ONLY`; 50,049 events and 12,628 users.
- B1 source SHA256: `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. B2 source SHA256: `35c4a4024f06d3de3548047fbe28e71e4697a5b96860a08a4cd8dd78c9bc9fdf`.
- The private job verified B1/B2 source, schema, event/user roster, user assignment, Full score/Base score and 12 pretarget-feature parity before fitting. The run output confirms `n_test_labels_accessed=0` and `prospective_confirmatory_result=false`. No row-level data or model weights were uploaded.

## 2. Frozen estimand

For each source (s\in\{\mathrm{Full},\mathrm{LongOnly}\}), let

`D_s(q) = NDCG10_F(F-supervised exact-call policy) − NDCG10_F(S-supervised exact-call policy)`

on the same source's full-active F utility scale. The source-by-supervision interaction is

`I(q) = D_Full(q) − D_LongOnly(q)`.

Negative `I(q)` means the F-vs-S policy-quality gap is smaller under Full Memory than under Long-only Memory. This is a total supervision-and-policy contrast, not a randomized label-only causal effect.

## 3. Primary result at q = 0.30

Each policy made exactly 15,014 Memory calls per source across the 50,049 DEV events. The Full-source `D` estimates reproduce the P1-A point estimates to floating-point tolerance.

| Base family | Source | F-supervised policy full-F NDCG@10 | S-supervised policy full-F NDCG@10 | (D_s(0.30)) |
|---|---|---:|---:|---:|
| SASRec | Full | 0.302636 | 0.296502 | +0.006133 |
| SASRec | Long-only | 0.299080 | 0.287899 | +0.011180 |
| GRU4Rec | Full | 0.303570 | 0.298172 | +0.005398 |
| GRU4Rec | Long-only | 0.300484 | 0.290193 | +0.010291 |

| Base family | (I(0.30)=D_{Full}-D_{LongOnly}) | User-cluster bootstrap 95% interval (descriptive) |
|---|---:|---:|
| SASRec | **−0.005047** | [−0.007022, −0.003235] |
| GRU4Rec | **−0.004893** | [−0.006725, −0.003070] |

In absolute NDCG terms, the F-supervision advantage is about 0.50 percentage points smaller under Full than Long-only. Long-only's observed F-vs-S gap is 1.82× the Full gap for SASRec and 1.91× for GRU4Rec. The descriptive user-cluster intervals do not cross zero, but condition on the already-fitted fold policies; they do not include model refitting, new-cohort or all-protocol uncertainty.

## 4. Predeclared quota sensitivity

All quotas were fixed before execution. Values below are (D_{Full}), (D_{LongOnly}), and (I=D_{Full}-D_{LongOnly}). Intervals are descriptive user-cluster bootstrap intervals conditional on the fitted policies.

| Family | q | (D_{Full}) | (D_{LongOnly}) | (I(q)) | 95% descriptive interval for (I(q)) |
|---|---:|---:|---:|---:|---|
| SASRec | 0.10 | 0.004644 | 0.006773 | −0.002129 | [−0.003481, −0.000915] |
| SASRec | 0.20 | 0.005804 | 0.009541 | −0.003737 | [−0.005339, −0.002176] |
| SASRec | 0.30 | 0.006133 | 0.011180 | −0.005047 | [−0.007022, −0.003235] |
| SASRec | 0.40 | 0.006512 | 0.012789 | −0.006277 | [−0.008387, −0.004201] |
| GRU4Rec | 0.10 | 0.002930 | 0.006064 | −0.003134 | [−0.004437, −0.001936] |
| GRU4Rec | 0.20 | 0.005297 | 0.009402 | −0.004105 | [−0.005688, −0.002477] |
| GRU4Rec | 0.30 | 0.005398 | 0.010291 | −0.004893 | [−0.006725, −0.003070] |
| GRU4Rec | 0.40 | 0.007151 | 0.011645 | −0.004494 | [−0.006705, −0.002412] |

The direction is stable across both Base families and all four predeclared quotas. This is a sensitivity result on one reused DEV cohort, not independent replication or a reason to choose q after seeing results.

## 5. Decision-exchange decomposition at q = 0.30

| Family | Source | F-only = S-only | Share of all events whose action changes (both sets) | Mean ΔF: F-only | Mean ΔF: S-only | F-only minus S-only mean |
|---|---|---:|---:|---:|---:|---:|
| SASRec | Full | 5,338 | 21.33% | 0.13323 | 0.07572 | 0.05751 |
| SASRec | Long-only | 8,221 | 32.85% | 0.12034 | 0.05228 | 0.06807 |
| GRU4Rec | Full | 5,786 | 23.12% | 0.12447 | 0.07777 | 0.04669 |
| GRU4Rec | Long-only | 7,812 | 31.22% | 0.11876 | 0.05283 | 0.06593 |

This suggests the larger Long-only gap is associated with both more changed decisions and a larger full-F utility separation between exchanged sets. This is descriptive accounting, not causal mediation.

## 6. Reconciliation with earlier B2 evidence

The earlier B2 nested DEV threshold-policy results (all 12 features) reported:
- SASRec: (D_{Full}=+0.006159), (D_{LongOnly}=+0.010605), (I=-0.004445); natural call counts differed between F/S.
- GRU4Rec: (D_{Full}=+0.004970), (D_{LongOnly}=+0.010262), (I=-0.005292); natural call counts differed between F/S.

P1-B yields the same qualitative ordering under exact offline batch quotas, but not identical point estimates. This is **estimand sensitivity across two policy protocols on reused DEV**, not independent replication. Do not pool the numbers or describe the older threshold-policy result as equal-budget.

## 7. Scientific interpretation and next gate

**Supported:** under this fixed offline allocation protocol, F-supervised decisions outperform S-supervised decisions on the common full-active F utility scale for both sources; the observed gap is consistently larger for Long-only than Full across the two Base families and four quotas.

**Not supported:** a causal claim that knowledge source itself causes the difference; generalization outside this cohort; an online/real-time feasible policy; measured latency/cost reduction; or confirmation on G5/TEST.

Next action:
1. Complete a bounded estimand reconciliation using the existing B2 aggregates only; no repeated DEV model fitting.
2. Keep a method-only corrected-S eligibility audit open; NI1g NO-GO for prior candidates is not proof that all valid corrections fail.
3. Gate any new confirmation on a previously unseen, lawful, independently eligible cohort and a frozen analysis plan. If no such cohort is available, retain the evidence as exploratory and do not promote a causal claim to the KBS paper.

**Status:** P1-A/P1-B computation PASS; P1-C reconciliation NEXT; independent P3 and KBS submission remain HOLD.
