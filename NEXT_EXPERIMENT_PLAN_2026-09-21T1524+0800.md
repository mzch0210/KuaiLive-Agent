# KuaiLive-Agent — Revised Next Experiment Plan (P0 / P1 / P2)

**Original snapshot:** 2026-09-21 15:24 +08:00  
**Current revision:** 2026-09-21, after completed P0 full-active + mechanism closure  
**Current phase:** manuscript consolidation + external validation; P0 internal-validity phase is complete.

---

# 1. Executive decision

The high-risk internal-validity questions are now closed:

- persistent-streamer identity shortcut: **closed**;
- sampled-candidate dependence: **closed by full-active ranking**;
- utility-vs-generic-difficulty mechanism: **closed in sampled and full-active regimes**;
- final Dual-ID information-source ablation: **closed**;
- strict temporal validity: **closed**;
- adaptive-computation / DS-Frame collision: **closed sufficiently**;
- DS projected-room bootstrap consistency: **closed at 5,000 resamples**;
- DCGLive official-protocol compatibility: **audited / closed**;
- selector and serving latency: **closed**.

The new scientific picture is stronger than the pre-P0 plan:

> **Memory-relative utility is regime-dependent. Its aggregate sign reverses across candidate universes and temporal regimes, while learned relative-utility routing continues to exploit within-regime heterogeneity beyond generic difficulty.**

Therefore the project should not reopen P0 model expansion. The next high-value work is **one cross-platform external validation**, followed by manuscript freeze.

---

# 2. P0-A — Full-active live-room ranking — CLOSED / PASSED

## Full-active universe

Test candidate count:

- mean 8,269.1;
- median 8,131.5;
- p95 12,301;
- max 13,266;
- all 10,222 positives metadata-active.

The full-active dev fusion again selects room 0.1 / streamer 0.9.

## A1 strict-transfer stress test

- Base NDCG@10: **0.398353**
- Always Memory: **0.432019**
- Selective: **0.430152**
- Selective − Base: **+0.031799**
- 95% CI: **[+0.028143,+0.035554]**
- invocation: **29.18%**.

Conclusion: the sampled policy transfers positively, but candidate-distribution shift changes the invocation policy and Always Memory is slightly above Selective.

## A2 full-active-native primary test

Full-active dev only is used for alpha/gate/threshold selection.

- Base: **0.398353**
- Always Memory: **0.432019**
- Selective: **0.451801**
- Selective − Base: **+0.053448**
- 95% CI: **[+0.048252,+0.058836]**
- invocation: **64.44%**
- Base HR@10: 0.519174
- Memory HR@10: 0.515750
- Selective HR@10: **0.557523**.

Primary pass rule: **PASS**.

## Scientific consequence

The candidate universe itself is a regime variable:

- sampled-active: Memory − Base ≈ **−0.04196**;
- full-active: Memory − Base ≈ **+0.03367**.

Do not keep “Memory is globally inferior” as an unqualified paper-wide claim.

---

# 3. P0-B — Conditional-utility mechanism closure — CLOSED / PASSED

## Sampled-active

- predicted-vs-realized utility Spearman rho: **0.2049**;
- bottom decile realized utility: **−0.1435**;
- top decile: **+0.1072**;
- matched-budget utility − difficulty: **+0.005458**;
- 95% CI: **[+0.002659,+0.008464]**;
- learned gate captures ~**17.0%** exact-K oracle gain.

## Full-active

- Spearman rho: **0.2399**;
- bottom decile realized utility: **−0.1430**;
- top decile: **+0.1774**;
- matched-budget utility − difficulty: **+0.014431**;
- 95% CI: **[+0.010938,+0.017908]**;
- learned gate captures ~**50.3%** exact-K oracle gain.

Conclusion:

> Relative-utility prediction is modestly predictive but decision-useful, and it adds significant routing information beyond generic base difficulty in both candidate regimes.

Avoid “well calibrated” and “near oracle.”

---

# 4. P0-C — Dual-ID information-source ablation — CLOSED / PASSED

## Sampled-active

- history threshold: +0.008704;
- state only: +0.004884;
- confidence only: +0.004910;
- state + confidence: **+0.013197**.

## Full-active

- history threshold: +0.035844;
- state only: +0.038783;
- confidence only: +0.046962;
- state + confidence: **+0.053654**.

Conclusion:

- combined state + confidence is strongest in both regimes;
- the relative value of confidence features changes with the candidate universe;
- do not claim confidence alone dominates history in the sampled regime.

---

# 5. P0-D — DCGLive compatibility audit — CLOSED

DCGLive is required direct related work but its official setup is not numerically comparable to the frozen main protocol.

Material differences include:

- transformed KuaiLive event stream rather than the frozen shop-only export;
- global chronological 80/10/10 interaction split rather than per-user LOO;
- ranking against all room IDs rather than legal active rooms at each target time;
- sequential validation/test updates of dynamic graph embeddings and adjacency.

Decision:

- cite/explain DCGLive prominently;
- do not place its official score in the same main-effectiveness table;
- only implement a clearly labeled `DCGLive-adapted` common-protocol version if reviewers explicitly demand it.

---

# 6. P0-hygiene — DS projected-room 5k bootstrap — CLOSED

The projected-room analysis was rerun with 5,000 bootstrap resamples without retraining or changing budgets.

All key budget comparisons remain positive within each system. Guardrail unchanged:

> Do not claim Selective Memory has larger routing gain than DS-Frame. DS often has larger within-system routing gain; absolute cross-system NDCG is confounded by different base systems.

---

# 7. P1 — Untouched cross-platform external validation — NEXT PRIMARY EXPERIMENT

## Preferred dataset: LiveRec Twitch 100k

Reference: `JRappaz/liverec`.

Why it remains the best P1:

- Twitch, outside Kuaishou;
- ~100k users;
- ~3M interactions;
- ~162.6k streamers/channels;
- dynamic item availability;
- repeated consumption is a first-class problem property.

## P1 research question

> **Does regime-conditioned relationship-memory utility transfer to a different live-stream platform with dynamic availability and repeat consumption?**

The external test does not need to reproduce KuaiLive's ephemeral-room / persistent-streamer identity geometry.

## P1 protocol to freeze before test

1. Reproduce the official dataset construction and availability semantics.
2. Use a **strong LiveRec availability/repeat-aware base** if the official code can be reproduced reasonably; vanilla SASRec may remain a reference row but should not be the only base.
3. Define an explicit relationship-memory specialist using train-history-only repeat/relationship information.
4. Define transferable state/confidence features before looking at test outcomes.
5. Fit the relative-utility estimator and threshold on dev only.
6. Add a same-feature generic-difficulty router at the exact same invocation budget.
7. Evaluate test once.
8. Bootstrap by user (>=5,000 for the final main comparison).
9. Report Base / Always Memory / Selective, utility-vs-difficulty, invocation, candidate availability statistics, and oracle headroom.

## External success criterion

Primary:

- Selective − strong Base mean > 0;
- 95% CI lower bound > 0.

Secondary mechanism criterion:

- relative-utility router > difficulty router at matched budget, preferably with positive paired CI.

If null/negative:

- no test retuning;
- report as a cross-platform boundary condition;
- narrow generalization claims rather than rescue the test.

---

# 8. P2 — Optional only after P1 / manuscript freeze

## P2.1 — KuaiLive-M3

Same-ecosystem contemporary validation; useful but weaker externality than Twitch.

## P2.2 — Richer uncertainty estimators

Ensemble variance / MC dropout / calibrated confidence. Low priority: the paper is not an uncertainty-estimation competition.

## P2.3 — DCGLive-adapted common protocol

Only if a reviewer explicitly requests it. Must be labeled adapted and document every changed protocol component.

## P2.4 — Secondary behavioral outcomes

Repeat vs novel streamer, head/tail, engagement/satisfaction where labels support it. No causal GMV/purchase language.

## P2.5 — Genuine LLM/agentic extension

Separate paper direction. Do not rebrand current MemoryFusion as an LLM agent.

---

# 9. Work that stays closed / should not be reopened

- more sampled-negative seeds;
- another official direct room-ID DS-Frame full-softmax attempt;
- broad new sequential backbone families;
- refitting the entire robustness/GTS chain to Ridge;
- more near-duplicate temporal splits;
- broad latency reruns;
- identity controls beyond the current Dual-ID unless reviewers identify a concrete failure mode.

---

# 10. Immediate execution order from this point

1. **Freeze the post-P0 paper narrative** around regime-dependent relative utility.
2. Generate main Figure 2 (utility stratification / difficulty / oracle) and Figure 3 (regime transition map) from the now-frozen outputs.
3. Begin/continue full manuscript writing in parallel.
4. Run **P1 LiveRec Twitch 100k** with the pre-registered external protocol above.
5. After P1, freeze the main paper tables/figures and select final target journal.
6. Add P2 only if P1 outcome or reviewer-risk analysis creates a specific need.

---

# 11. Journal-dependent stopping rule

## ESWA first

The KuaiLive evidence chain is now internally submission-grade after P0. A successful P1 would materially strengthen the paper but is no longer needed to close an internal-validity gap.

## KBS / Information Sciences

P1 is more important because the manuscript's conceptual claim is broader than one application dataset.

## IPM

Emphasize information value, confidence, candidate/temporal regime dependence, and matched-budget routing rather than adding another architecture family.

---

# 12. Final hierarchy

> **P0 = CLOSED.** Identity, candidate universe, relative utility vs difficulty, information ablation, temporal validity, collision defense, and latency are all closed.  
> **P1 = NEXT.** One untouched cross-platform LiveRec/Twitch validation with a strong domain-aware base.  
> **P2 = OPTIONAL.** Only targeted extensions after P1/manuscript freeze.

The project has moved from validity closure to **external validation and manuscript freeze**.
