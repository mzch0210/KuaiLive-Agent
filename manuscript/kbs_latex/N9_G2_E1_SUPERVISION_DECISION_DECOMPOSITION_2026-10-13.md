# N9–G2 / E1 — Candidate supervision alters where relationship knowledge is used

**2026-10-13 | E1 B1-compatible primary-arm replication PASS.** [Private-run GitHub Actions #38389150075](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38389150075); exact 50,049 M3 author DEV events/12,628 users, same frozen primary SASRec/GRU4Rec, original twelve decision-time features, HGB(120) and 5 outer × 4 inner user-group folds, 30% *inner* threshold limit. This is **post-G5 exploratory DEV**, not an independent TEST or a new preregistered correction family. G5 TEST not read, no Base retrained and private user/event rows not exported.

## 1. Decision and ranking parity

| Base | S→F F NDCG | F→F F NDCG | Calls S/F | Different decisions | F-only calls | S-only calls | Δ F NDCG |
|---|---:|---:|---:|---:|---:|---:|---:|
| gru4rec | 0.298123 | 0.303093 | 15001/14762 | 11517 (23.01%) | 5639 | 5878 | +0.004970 |
| sasrec | 0.296499 | 0.302658 | 14988/15016 | 10672 (21.32%) | 5350 | 5322 | +0.006159 |

The original B1 S→F and F→F held-out quality and realized call counts are **reproduced to original numerical precision**. The identity 
\[
V_F(\pi_F)-V_F(\pi_S)=\mathbb E[(\pi_F-\pi_S)\Delta_F]
\]
is verified at event level by direct accounting with numerical tolerance $10^{-14}$. This is an algebraic decomposition, **not a new theorem**.

## 2. Switch-level valuation mechanism

**GRU4REC:** Full-trained rule adds Memory on 5639 events with mean realized F source advantage 0.126600; it drops Memory on 5878 events where the advantage is 0.079135. Across the *whole original DEV cohort*, the add contribution is +0.014264 NDCG, the drop contribution -0.009294, net +0.004970 (user-paired 95% CI [0.003550, 0.006369]). Importantly, both switching groups have positive mean specialist advantages: the evidence is consistent with **higher-value allocation under a capped call regime**, not principally a rule avoiding negative Memory cases. Exact calls remain naturally different, so this is not a strictly equal-budget intervention.

**SASREC:** Full-trained rule adds Memory on 5350 events with mean realized F source advantage 0.133417; it drops Memory on 5322 events where the advantage is 0.076194. Across the *whole original DEV cohort*, the add contribution is +0.014262 NDCG, the drop contribution -0.008102, net +0.006159 (user-paired 95% CI [0.004835, 0.007543]). Importantly, both switching groups have positive mean specialist advantages: the evidence is consistent with **higher-value allocation under a capped call regime**, not principally a rule avoiding negative Memory cases. Exact calls remain naturally different, so this is not a strictly equal-budget intervention.


The learned S and F policies have comparable overall invocation counts but disagree on a **substantial fraction of the particular events** selected. This sharpens the interpretation of the original B1 F-supervision improvement: the candidate regime affects **knowledge-call allocation**, not merely the reported sample ranking metric. However, this does not establish that the phenomenon is uniquely caused by relational identity rather than generic ranking/candidate evaluation.

A separate B1 relative-value *label sign* diagnostic includes transitions to/from zero: 26941 SASRec and 26937 GRU4Rec events differ in sign category, whereas strict positive–negative reversals with both nonzero are only 157 and 145. **Never call the three-class mismatch a pure sign reversal.**

## 3. Corrected-S feasibility decision

The original offline S construction uses deterministic, uniform **574 negative-author draws without replacement** from the eligible F roster *after retaining the subsequently observed target* among 575. This law is documented in `analysis/kbs_plan_c/b1_dev_regime_pilot.py` and B1 source-construction code. It is suitable for retrospective evaluation-label generation, **not live target-aware candidate choice**. Existing private B1 CSV supplies sampled **top-10 NDCG scalar**, full NDCG reference and candidate-count features; it does not by itself establish the complete sampled rank for all outcomes or exact per-candidate score vectors needed to claim the applicability, finite-sample properties and parity of a specific inverse-sampling ranking correction.

Krichene and Rendle, *On Sampled Metrics for Item Recommendation* (KDD 2020), demonstrate general inconsistency of sampled top-K metrics and derived corrections (https://research.google/pubs/on-sampled-metrics-for-item-recommendation/). **No correction arm has been run or fabricated in this phase.** Next gate: identify an estimator valid for target-retained 574-without-replacement sampling, precise candidate size and capped top-10 NDCG, with only information available in outer training. If no well-defined estimator from cached data is verified, mark Corrected-S HOLD; E1 decision-accounting remains complete.

## 4. R1/R3 scientific consequence, and remaining gates

**R1:** empirical contribution now articulates a 21–23% supervision-dependent *decision disagreement* under nearly equal natural call rates and its realized value difference, rather than relying only on sampled/full NDCG levels. This materially strengthens decision-support differentiation but does not invent deferral mathematics or rule out known sampled-metric effects.

**R3:** combined B1/E1 plus E3a establishes a more concrete evidence chain from historical-source value to candidate-regime supervision and constrained knowledge-allocation behavior. These are two analyses on the **same post-G5 DEV cohort**, not independent replication, and E3a's source effect is not causal identity proof.

Next possible work: G3 source-placebo **metadata/privacy/pilot feasibility first**; only run an expensive controlled rerank if an honest non-floor time/degree-preserving history intervention can be defined and rights verified. G4 will adjudicate risk strength before editing the main article or Supplementary.

Artifacts: `analysis/kbs_plan_c/n9_g2_e1_supervision_decision_switches_dev.py`, `.github/workflows/kbs-n9-g2-e1-supervision-decision-switches-dev.yml`, and `experiments/kbs_plan_c/N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json`.
