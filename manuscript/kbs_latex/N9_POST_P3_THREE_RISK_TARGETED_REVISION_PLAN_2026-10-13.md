# N9 post-P3 | Three scientific risks: targeted evidence and manuscript revision plan

**Established:** 2026-10-13. **Status: PLAN ONLY — NO NEW EXPERIMENT/TEST OR MANUSCRIPT ALTERATION AUTHORIZED BY THIS FILE.** This is the next bounded work package *under the existing N9/N1 decision-support thesis*, not a reset to method-first novelty, nor an update of frozen G5 outcomes. Start only after G0 research contrasts and permissible private data paths are documented.

## 0. Immutable baseline and objective

- Canonical eight-section article: `manuscript/kbs_latex/main.tex`, source blob `774cece1e35951c2d50af12ac398eb9f3bd3ff74`; 35-page latest successful preview, GitHub Actions `38385740136`.
- Combined S1–S10 supplement: `SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md`, blob `60d6ccb319f0229218d91b656408505df2630e70`; 37-page successful preview, Actions `38385758028`.
- Prior N9 decision, scientific risks and methodology: `N9_A3_DECISION_SUPPORT_RISK_VERDICT_2026-10-13.md`, `N9_P3_KBS_REFEREE_REVIEW_AND_REMEDIATION_2026-10-13.md`, and `N9_EXECUTION_GATE_STATUS_2026-10-13.json`. Scientific evidence remains BOUNDED; submission HOLD.
- Core claim: **incumbent- and candidate-regime-relative incremental ranking value of a fixed historical relationship expert, the decision consequences of supervising that relative value, and the conditions of specialist use**. We do **not** introduce a generic new selector, claim a new sampling theorem, or infer live-serving savings from a Memory-call fraction.
- Existing frozen tests: Twitch 44,221 streamer requests and M3 47,575 author requests / 12,533 TEST users; original KuaiLive 10,222 paired room events is a retrospectively examined diagnostic. Do not open existing G5 TEST outcomes for new training, thresholding or exploratory confirmation.
- B1/B2/A1/A2 are the *same* post-G5 exploratory KuaiLive-M3 DEV cohort: 50,049 author-ranking events / 12,628 users, primary 20261012 SASRec/GRU4Rec seeds. Five outer user-disjoint × four inner user-disjoint GroupKFold, 2,000 user-cluster bootstrap samples for descriptive intervals. Shared cohort and model seeds do not imply new independent tests.
- A0 private read-only source integrity passed in Actions `38382393789`; B1 paired source SHA256 `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea`. Verify exact manifest and SHA before any new fitting. Candidate-level score arrays and candidate identities for full score/rank fusion are **NOT** established.

The desired journal contribution is *decision-support scientific insight*. KBS aims at original, innovative knowledge-based and AI system research supporting prediction and decision-making and balancing theoretical/practical findings (https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051). Prior-art boundaries: Krichene & Rendle (KDD 2020, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/) establish sampled-metric inconsistency and correction; Mao, Mohri & Zhong (ICML 2024, https://proceedings.mlr.press/v235/mao24d.html) establish expert deferral with separate/direct estimators. The manuscript does not claim priority to these foundations.

## 1. Scientific risks and decision criteria

| Risk | Unresolved referee question | What would materially reduce it | Residual ceiling |
| --- | --- | --- | --- |
| R1 scientific originality of **knowledge valuation for decisions** | Is the candidate-supervision-to-knowledge-choice effect more informative than generic sampled metric distortion or a trivial relabeling of learn-to-defer? | E1 shows precisely which policy decisions change, their realized full-candidate value, sensitivity to feasible sampling correction and invocation mismatch, with concrete contrast to prior art | Same-DEV exploration cannot by itself establish general originality; do not claim novel routing mathematics |
| R2 objective and constraint justification | Under what **explicit knowledge-use cost/availability premise** is relative-value allocation decision-relevant, given Always Memory's greater M3 quality and faster warmed replay? | E2 derives quality–realized-call envelope and break-even shadow cost against **all** available policies; states gating overhead separately and avoids production-dollar assertions | Hypothetical utility units are not a measurement of real latency, access price or permissions |
| R3 integrated significance and historical-source mechanism | Does real historical relation *identity* matter above ordinary user/activity/candidate effects, and does the source×candidate interaction survive paired tests? | E3a paired raw source×candidate interaction with cluster CIs and pre-outcome strata; E3b degree/time-preserving source control only if feasible, with non-floor check | Full source causal identification and independent temporal replication remain unavailable without suitable new data |

**Success is NOT defined by making every p-value significant or having Direct beat two-stage / Always Memory.** Adverse or null outcomes are valid; final claims and KBS suitability must be adjusted based on them.

## 2. G0 — Freeze exploratory research contracts BEFORE additional analysis

**Action:** Freeze the latest public main/S10 sources and private hashes; declare exact primary and secondary contrasts, bootstrap seed and unit, data columns, group splits, and permitted read/write paths. Maintain an immutable source→claim→table registry, append rather than rewrite old result records. Log that G0 follows review of B1/B2/A1/A2 results; this is **prospective planning for additional exploratory analyses, not formal preregistration nor independent TEST**.

- Primary E1 outcome: $V_F(\pi_F)-V_F(\pi_S)$ on the *same* outer-group-held-out M3 author events, with actual call rates and policy disagreement; existing 30% inner maximum is primary to preserve B1, 10/50% sensitivity only if the private source and compute allow.
- E3a primary outcome: raw source×candidate interaction for **Full versus Long-only** on matched events, $I_i=[u_F(M_{Full},i)-u_F(M_{Long},i)]-[u_S(M_{Full},i)-u_S(M_{Long},i)]$. This is **not** the same as B2's already available `paired_source_regret_interactions`, which compare **selector transfer regret** across sources. Do not confuse those estimands.
- E2 primary object: entire *pre-existing* A1 full-active NDCG–**actual outer invocation rate** frontier, not an arbitrarily selected 30% result.
- Hierarchy: primary questions declared first; pretarget strata, S correction variations, 6-vs-12 features and secondary source effects labeled exploratory. Report interval widths and practical magnitude; if many post-hoc contrasts are screened, transparently document multiplicity rather than incorporating them into original G5 Holm family.
- Gate: source SHA, 50,049 unique DEV event IDs, 12,628 user IDs, temporal eligibility, pre-outcome feature status, no G5 TEST access, no private row export. Abort on mismatch.

**Deliverables:** `N9_G0_FROZEN_E1_E2_E3_CONTRAST_CONTRACT.md`; `N9_G0_DATA_AND_CACHE_ELIGIBILITY.json`; prior N9/G5 status unchanged until actual execution.

## 3. G1 — Highest-efficiency analyses in parallel: E3a + E2

### E3a — Historical source × candidate-regime interaction (R3, helps R1)

**Input:** exact B2 private event-source ablation CSV and manifest, *not merely the public B2 nested selector-regret JSON*. Verify Full and Long F/S target-retained scores and paired event identities. Full, Long, Short and popularity are already defined fixed source constructions; do not retune mixtures.

**Compute:** per-event $I_i$ above; cluster-mean, 95% paired **user** bootstrap CI (2,000 or a frozen higher number) and distribution of sign changes. Report $d_F=U_F(Full)-U_F(Long)$ and $d_S=U_S(Full)-U_S(Long)$; presently observed aggregate values $+0.010278$ and $-0.105104$, so the **descriptive** interaction is $+0.115382$. These point estimates are known already; the purpose is *paired uncertainty, heterogeneity and mechanism alternatives*, not rediscovery.

**Stratification:** only pre-outcome variables (history length, prior distinct creators, repeat intensity, candidate competition and Base-score dispersion), pre-specified quantile boundaries from training DEV. For each stratum, provide population counts, user counts, source utility gaps and paired uncertainty. Avoid target-defined retrospective groups as observable online policy features; no causal inference from conditional differences alone. Correct for measurement of sampled candidate size/identity jointly; cannot infer an isolated list-length mechanism.

**Accept:** independent source rehash passes and paired interaction is faithfully reproduced with CI; assess magnitude/stability and explanation boundaries irrespective of sign. If source arms are unavailable or parity fails, E3a HOLD; preserve B2 source reversal as descriptive only.

**Output:** `N9_G1_E3A_PAIRED_SOURCE_REGIME_INTERACTION.md` and safe aggregate JSON (no private IDs).

### E2 — Net decision value and access-shadow-price frontier (R2)

**Input:** existing A1 safe `experiments/kbs_plan_c/N9_A1_DECISION_FRONTIER_PUBLIC_AGGREGATE_2026-10-13.json` and, for user-cluster CIs, the existing hashed private full A1 nested outer-policy results if present; if per-user policy outcomes were not saved, regenerate only DEV pointwise outer decisions from exact cached inputs, not Base checkpoints.

For all observed A1 policies $\pi$ (inner max 0/10/20/30/50/70/90/100%) plus fixed Always Base and Always Memory, analyze

$J_{\lambda,g}(\pi)=V_F(\pi)-\lambda q(\pi)-g(\pi)$,

where $q$ is **observed held-out Memory-call fraction**, $\lambda$ a hypothetical per-invocation shadow cost measured in units of expected event NDCG, and $g$ any independently measured/proposed **full-path gate overhead** on the same scale. Set $g=0$ **only** in the explicitly marked idealized sensitivity analysis. Do not convert $\lambda$ to real currency or milliseconds without observed cost and a supported utility exchange rate.

Enumerate pairwise policy breakpoints and the **upper envelope** over all policies, not merely two Always endpoints. Report the range of $\lambda\ge 0$ where each strategy maximizes estimated $J$, bootstrap uncertainty for meaningful adjacent comparisons, and observed calls. Include a no-premise interpretation: if no resource cost/availability exists, Always Memory can be the correct M3 default and the selector only tests conditional choice quality.

**Accept:** all A1 30% outputs and fixed baselines reproduced, cost envelope numerically monotone/consistent where applicable, no unmeasured production-speed claim. Negative results narrow deployment relevance without invalidating candidate-context valuation.

**Output:** `N9_G1_E2_SHADOW_PRICE_DECISION_ENVELOPE.md` and one compact curve/table.

## 4. G2 — E1 candidate-supervision discrimination (R1 primary; R3 secondary)

**Experimental arms and fairness:**
1. **S→F** original B1 sampled-derived label, evaluated on full F outer events.
2. **F→F** original full-active label, evaluated on same F outer events.
3. **Adapted→F** original arm using **F training labels**, separately named and never framed as label-free adaptation.
4. **Corrected-S→F** only if G0 confirms exact offline sampling law, inclusion probabilities, tie treatment and a valid correction of ranking *utility* using information available without F outcome supervision. The estimator is defined and fixed **on inner training**, respecting literature assumptions. Do not improvise a correction from aggregated event NDCG or add F labels to this arm while calling it S-only.
5. If sampling correction is unsupported, **NO forced corrected-S result**. Report a correction-feasibility FAIL/HOLD and instead do the decision-level decomposition/label-disagreement sensitivity with the first three verified arms. F-supervised calibration is a distinct knowledge regime and must not be relabeled as S-only correction.

**Primary decision decomposition:**

$D_{S,F}=\Pr(\pi_S(Z)\neq\pi_F(Z))$;

$V_F(\pi_F)-V_F(\pi_S)=\mathbb{E}[(\pi_F(Z)-\pi_S(Z))\Delta_F(X)]$.

Report switch-to-Memory and switch-away shares separately, F incremental utilities on **disagreement** events, net difference, paired user bootstrap interval, and full F NDCG@10. These are definitional algebraic accounting identities, not new theoretical theorems.

**Resource fairness:** preserve original **inner-only** fitting/calibration for a 30% maximum. Report *both* inner maximum and actual outer calls. Optional other inner limits 10% and 50% provide sensitivity. To explore an equal-count comparison, use an **inner-training-defined** budget rule or a predeclared randomized tie policy; a retrospectively outer-count-matched batch is **only a nondeployable diagnostic**, and its use must be marked. No outer outcomes for threshold selection, no hindsight event-level target at inference.

**Interpretation branches:**
- If corrected S approximates F, the gap is largely compatible with known sampled-metric misalignment; emphasize faithful propagation of established evaluation lessons to explicit knowledge-use decisions, not a novel correction theorem.
- If corrected S improves upon S but leaves a reproducible choice gap with F, analyze pre-outcome candidate/history conditions and the residual informational difference without assuming it is uniquely relational.
- If budget-matched effects vanish, downgrade claims about the supervision regime's *independent policy advantage*, while keeping descriptive label-dependence.
- If the correction cannot be derived from available sampling information, no negative inference about theory should be drawn from absent experiment.

**Accept:** executable exact-source parity with B1's 30% arms, user-disjoint 5×4 split consistency, policy decision decomposition checks to machine precision and clear different training-information entitlements. Do not fabricate matching outer budgets or p-values.

**Output:** `N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION.md` plus correction-method feasibility/audit appendix and safe aggregates.

## 5. G3 — Conditional E3b structurally preserved relation placebo (R1/R3)

**Start only if G1/G2 leave a specific material alternative explanation that E3b can test, and original relation-time records are available legally.** This is not a default GPU-intensive experiment.

Candidate controls: (a) event-history permutations/matched-history pairs preserving user history length, recent/long history volumes and item popularity/activity marginals; (b) temporal-bin, degree-preserving viewer–creator bipartite edge swaps applied **strictly before each decision time**, with exact candidate eligibility preserved. Any such controls must pass privacy and future-leak audits. Score-placement shuffles from B2 are not enough to claim correct edge identity specificity.

**Pilot first** on a frozen small DEV subset with fixed seed: verify per-user and per-author marginals, temporal order, eligible authors, coverage, score spread and comparable opportunities for Memory selection. Check the specialist doesn't collapse to an almost-never-called floor. If too weak, investigate normalization or matched-strength controls transparently; do not tune controls until a wished-for treatment effect emerges.

If pilot passes, perform **one bounded full DEV-only** analysis with the same F/S regimes and user folds. Outputs should include utility differences, paired uncertainty, actual calls and coverage. GPU work only if raw ranking vectors genuinely need recomputation; reuse cached histories/rosters, time-ordered CPU scan and batched GPU inference; separately record CPU/GPU/wall time and scoring-parity checks. No new Base training.

**STOP** if valid non-floor relation identity control cannot be created from existing lawful data. That outcome limits the claim to source sensitivity, not a relation-specific causal proof.

## 6. G4 — Decision-support scientific contribution adjudication

For each R1/R2/R3 return **STRONG WITHIN TESTED DESIGN / BOUNDED / HOLD**, each with: named estimand, public evidence, private hash provenance, user-cluster interval where calculable, competing explanation, and exactly admissible manuscript sentences. No method-first versus valuation-first fork. Do not define STRONG as independent external replication when data are unchanged.

| Evidence result | Interpretation / manuscript decision |
| --- | --- |
| E1 shows candidate-supervision switch and retained decision value at defensible budgets | Strengthen valuation-to-choice evidence; still describe B1/E1 as post-G5 exploratory |
| Correction removes nearly all B1 transfer gap | Interpret as sample metric correction/target alignment, narrow theoretical novelty; emphasize empirical decision consequences |
| E3a source interaction stable and E3b passes structural non-floor control | Stronger conditional historical-source account, but avoid causal conclusions stronger than experimental intervention allows |
| E3b fails/has floor or E3a unstable | Show source heterogeneity only; drop relation-specific causal explanation |
| E2 shows a positive shadow-cost region | State hypothetical resource-conditioned optimality over studied policies; not real cost saving |
| E2 yields no credible cost/availability justification | Treat specialist allocation as constrained scientific decision illustration; Always Memory remains sensible default |
| No additional lawful blind TEST | Preserve independent Twitch/M3 evidence and avoid new confirmation or six-independent-cohort rhetoric |

**Output:** `N9_G4_THREE_RISK_EVIDENCE_VERDICT.md` and a new machine-readable risk-state JSON. Do not overwrite N9 P3 archive.

## 7. G5–G6 — Manuscript and supplementary revision gates

### G5a evidence-first revisions, after G4
- **§3 Problem Formulation:** define regime-indexed utility and optional shadow-cost model with full assumptions; keep $V_F(\pi_F)-V_F(\pi_S)$ as empirical contrast.
- **§5 Experimental Setup:** clearly partition frozen TEST, original room retrospective diagnostic and post-G5 M3 nested DEV; source-hash, 5×4 user GroupKFold, sampling correction eligibility, real observed calls, and planned source controls. Never call group-held-out DEV a new temporal TEST.
- **§6.3 Candidate-regime value:** present E1 switch-decomposition together with B1, in one concentrated main display; full budget details in S10.
- **§6.4 Sources and signals:** append E3a's paired Full-vs-Long interaction and E3b only if valid; don't overinterpret weak Short/popularity/history controls.
- **§6.5 Quality/constraints:** present E2 full resource-shadow-cost envelope, retain M3 Always Memory accuracy and faster warmed complete scoring path; distinguish unmeasured real deployment costs.
- **Supplement:** append structured S10.9–S10.11 or a coherent S11 **only if needed** for full calibration, placebo, folds and verification details. Preserve the existing 34 tables and prior S1–S9 unchanged unless a documented factual repair is required. Do not flood main text with redundant tables.

### G5b narrative revisions, only after G5a data audit
- **§1 Introduction and Abstract:** contribution is a *conditional historical-knowledge evaluation and decision-support empirical account*, not new expert deferral mathematics; reference candidate-regime-to-decision contribution with exact evidence tier.
- **§2 Related Work:** directly contrast KDD 2020 metric correction, ICML 2024 expert deferral, adaptive budgeted recommenders, and knowledge-aware fusion with the manuscript's specific empirical estimand. Claims must be side-by-side, not generic novelty self-advertisement.
- **§7 Discussion and §8 Conclusion:** one connected argument valuation → candidate supervision → knowledge-use choice → conditional resource premise. Honest contextual boundaries without excessive process-status text or self-negating repetition.
- Harmonize title, highlights and cover letter only after G4; avoid claims of real economic advantage or causal source identification without evidence.

### G6 journal submission review
- Versioned `main.tex` and S1–S10 build, no undefined citations/refs, figure/table legibility and 35/37-page baseline comparison; the final page count is not itself a quality criterion.
- Audit every new table value against hashes, run IDs, precise cohort, candidate generation, units, folds, bootstrap draw semantics, actual vs allowed Memory-call fractions, and inferential family.
- KBS official 2026 Guide for Authors and publisher AI policies rechecked for cover letter, highlights, statements and current submission requirements; human authors must approve accurate AI-assisted research-code/analysis disclosure, authorship, funding/COI and licensing/data privacy. No assistant-generated attestation.
- Author sign-off and final external-style critique. **Submission remains HOLD** if source verification, scientific claims or author compliance gates fail.

## 8. Cost, ownership and stop/go discipline

**Compute order by expected research value per unit effort:**
1. G0 source/estimand freeze and E3a/E2 using existing verified event-level source and A1 summary (CPU analysis first).
2. E1 switch decomposition/inner-fold regressions using existing B1 50k DEV cache; *sampling correction only if identifiable from the sampling design*.
3. E3b data/schema pilot; only then any bounded rescore with no Base retraining.
4. New blind TEST only if an unexposed lawful time-forward source is independently established and authors freeze the protocol. Not a precondition for the previous exploratory steps.

Stop gates: missing source digest; label/candidate leakage; incorrect temporal eligibility; 30% B1 parity break; contradictory realized-call accounting; unsupported correction estimator; ineffective placebo floor; or requirements to reopen old G5 TEST. Record partial results and change claims instead of silently retrying to force a positive finding.

**Research roles:** The research engineer owns code/caches and GPU efficiency; the scientific lead owns hypotheses/interpretation and fair comparators; human authors own ethics, rights, writing/AI-use disclosures and the KBS submission decision.

**Current immediate next action:** execute **G0** (contract + exact cache feasibility) only. This file documents the research plan; it does not itself start G1–G6 or upgrade any scientific risk to RESOLVED.
