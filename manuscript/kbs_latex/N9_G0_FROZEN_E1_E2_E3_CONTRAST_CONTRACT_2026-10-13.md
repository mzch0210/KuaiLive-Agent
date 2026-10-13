# N9–G0 | Frozen exploratory E1/E2/E3a research contract
Date: 2026-10-13. Status: **G0 protocol locked for exploratory DEV analyses; no new confirmatory TEST**.

## Immutable research question
Why must a fixed viewer–creator relationship knowledge source be valued **relative to its incumbent and candidate regime**, and when does that candidate-specific supervision substantively alter decisions to invoke the source? The submission remains a knowledge-valuation and decision-support study, not a novel routing algorithm.

## Original scientific evidence and exclusions
Original Twitch and KuaiLive-M3 G5 TESTs remain frozen. Do not use any G5 TEST for training, tuning, post-hoc matching or additional confirmation. The 10,222-room retrospective candidate experiment is neither M3 author-level nor an independent replication. B1, B2, A1, A2 and new G1/G2 analyses use the **same post-G5 M3 DEV author cohort**: 50,049 events, 12,628 users, primary Base seed 20261012. SHA256-verify source before use and never publish event/user IDs.

GitHub audited sources:
- B1 private `klm3_b1_full_dev_candidate_labels_seed20261012_v1/dev_pair_candidate_labels.csv`; expected SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`.
- B2 private `klm3_b2_full_dev_memory_source_ablation_seed20261013_v1/dev_memory_source_ablation_pairs.csv`; validate SHA256 **against its existing private summary.json** and original full F/S Memory parity; no hardcoded guessed digest.
- A1 public `experiments/kbs_plan_c/N9_A1_DECISION_FRONTIER_PUBLIC_AGGREGATE_2026-10-13.json`, blob `a40aed41a4217220db9024aa667107ba1ff8eb66`; A1 workflow source `analysis/kbs_plan_c/n9_a1_decision_support_frontier_dev.py`.

### Predeclared estimands and analysis ranking
**G1–E3a, primary:** `I_i=(F_full_i-F_long_i)-(S_full_i-S_long_i)` on matched **raw fixed-source event NDCG**. Existing public descriptive mean: 0.115382 from (0.343509−0.333231)−(0.668498−0.773602). Calculate event-paired **user-cluster** bootstrap percentile 95% interval, 2,000 replicates (seed 20261013). This is different from B2 public `paired_source_regret_interactions`, which measure **nested policy transfer** regret differences; never confuse them. Secondary: dF and dS with paired intervals, independent users and counts, sign categories **distinguishing zero**. Exploratory strata by decision-time 12-feature history/candidate metrics, no hindsight evidence-state strata. No claim that changed candidate number is the unique cause; identities/competition also change.

**G1–E2, primary:** all A1 policies on the same full-active DEV cohort, fixed Base and Memory endpoints, and calibrated call ceilings `0, .10, .20, .30, .50, .70, .90, 1`. Use **outer realized** q, not inner target. Evaluate `J_λ(π)=V_F(π)−λ q(π)` for λ>=0 **under a visibly labelled idealized zero gate-overhead assumption**. Find exact upper-envelope breakpoints across **all** policies and fixed endpoints, including any policies never optimal. This is hypothetical NDCG-unit shadow cost, not money or measured latency; add `g(π)` only if independently measured on a comparable workload and commensurate units. Secondary paired CIs require per-user outcomes; the published A1 summary does not contain enough covariance to invent adjacent-envelope uncertainties.

**G2–E1, primary:** original 30% inner-call maximum B1 S→F versus F→F, with adapted F-supervision arm described separately. Compare `D=P(π_S != π_F)` and `V_F(π_F)−V_F(π_S)=E[(π_F−π_S)(u_F(M)−u_F(B))]`, split switches on/off with user-paired interval; report each actual outer call count and full-ranking NDCG; exact B1 arm value/call parity is mandatory. Follow original 5 outer × 4 inner user GroupKFold, 120 HGB iterations, target not visible as decision-time feature. Additional 10%/50% ceilings and sampling-metric correction strictly secondary and conditional. **Corrected-S requires known sampling law, inclusion probabilities, legal candidate scores, and unbiased/justified ranking-utility estimator without F-supervision**. Never use an arbitrary shrinkage to full-label targets or hindsight outer matching as a legitimate sampled-only corrected estimator.

**G3–E3b, conditional:** one genuine time-valid relation-identity placebo only if E3a/E1 reveal a material alternative explanation and per-event temporal relations can be permissibly reconstructed. Pilot must preserve activity marginals/time/candidate eligibility; reject near-zero-call/floor collapse rather than claiming causal identification.

### Research integrity and no peeking
Exploratory research protocol was set *after reviewing B1/B2/A1/A2 results* and does **not** constitute preregistration. Five folds and two Base families are not independent external cohorts. All new CI statements descriptive; original within-fit G5 Holm family unchanged. F/S sampled labels are **target-retained retrospectively** and never presented as online candidate generation. Regression thresholds fit and calibrated inner-only; outer outcomes used solely to evaluate. No row-level identity/target exports. Existing project artifacts remain immutable. Stop on source SHA, roster, event split, temporal or metric parity failure, even if outcome would be interesting.

### Resources and journal writing
E3a reads and aggregates verified private B2 event records on the self-host; E2 first uses GitHub public A1 aggregates in CPU-only audit with no training. E1 reuses B1 pairs and 5×4 folds; GPU not necessary for HGB unless missing source requires formally authorized DEV-only rescoring. Report wall/CPU/GPU time if any rescoring.
S10 and §5–§7 update only **after G4 risk verdict**; not before; abstract/conclusion last. Any null or adverse results must narrow claims, not trigger unlimited retuning.
