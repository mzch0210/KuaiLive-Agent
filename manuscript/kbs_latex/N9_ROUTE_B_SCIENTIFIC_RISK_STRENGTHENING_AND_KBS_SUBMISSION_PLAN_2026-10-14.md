# N9 Route B | 科学风险增强与 KBS 投稿定向修订执行计划

**制定日期：2026-10-14。状态：PLAN ONLY（未经执行，不改变旧研究结论与投稿状态）。**
**主线冻结：Knowledge Valuation and Decision Support，NOT a novel Memory selector.**
本文件是 G0–G6 完成后的下一轮分支计划，不追溯改写旧计划，不宣布 G3b 已全量完成。若执行，应另建证据和运行状态文件，保留此前所有 frozen results。

## 0. 已核查基线和本次必要性

- GitHub 主稿 \`manuscript/kbs_latex/main.tex\` blob \`dd57e309fca7ddd59f05d40512539d0ac31aa0c8\`；36 页、八章、11 表、2 图。Actions \`38391955348\` SUCCESS。
- Supplement \`SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md\` blob \`183971e05aa4341dee13a4a8237cc54b0553ae0c\`；39 页、S10 共 12 小节，Actions \`38392829047\` SUCCESS。旧 S1–S9 未修改。
- 原冻结 TEST：Twitch 44,221 streamer events；KuaiLive M3 47,575 author events/12,533 users。旧 KuaiLive room 10,222 retrospective diagnostic。**三者不能混成一个独立确认总体。**
- B1/B2/A1/A2/E1/E2/E3a 全部是**相同 post-G5 M3 DEV**，50,049 author-ranking events / 12,628 users；5 outer × 4 inner user-disjoint GroupKFold 与 2,000 user-cluster descriptive bootstrap；S 为含事后目标保留的离线 575-item sample，不是在线生成候选。
- E1: F-vs-S trained policies differ on **10,672 SASRec requests (21.32%)** / **11,517 GRU4Rec (23.01%)**；F-supervision net gain +0.006159 / +0.004970 F NDCG at similar but **not strictly equal** realized calls。
- E3a: fixed Full-versus-Long F−S interaction **+0.115382** [0.111724,0.119065] user-cluster CI；**46,462/50,049** have at least one zero source gap; **66** strict opposite nonzero gap signs。
- E2: in idealized zero-gate-overhead \`J_lambda=F_NDCG−lambda*realized_call_fraction\`, the 30%-inner-cap policy is among observed-policy envelope maximizers only at [0.084516,0.111321] SASRec / [0.083119,0.104379] GRU4Rec; these are hypothetical NDCG-equivalent costs, **not observed finance/latency**。
- E3b: 128 late-quarter DEV event history-identity placebo with 63,619 co-active degree/time-preserving swaps; original F Full 0.396585, placebo 0.384386; original offline S Full 0.661360, placebo 0.669835；**non-floor pilot PASS but neither user CI nor population relation-identity causality**. Source \`N9_G3_TIME_PRESERVING_RELATION_PLACEBO_PILOT_2026-10-13.md\`。
- \`N9_G4_THREE_RISK_EVIDENCE_VERDICT_2026-10-13.md\` adjudicated **R1 BOUNDED / R2 BOUNDED / R3 BOUNDED**；投稿 HOLD。
- Frozen B1 source SHA256 \`37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea\`；B2 private source digest must be checked against its original private summary; no G5 TEST read or new training authorization.

**Research objective:** distinguish known sampled-metric distortions / generic expert deferral from empirical \`incumbent-relative knowledge-value → candidate alignment → request-specific decision-value\` insight; assess whether viewer–creator **correct historical identity** contributes above time/activity/popularity structure; quantify conditional rather than asserted production value.

KBS official scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 (original innovative AI/knowledge systems, recommendation, intelligent decision support, theory and application). Prior boundaries: Krichene & Rendle KDD 2020 https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ ; Mao, Mohri & Zhong ICML 2024 https://proceedings.mlr.press/v235/mao24d.html ; Ren et al. Phys Rev E 2018 temporal degree-preserving null https://doi.org/10.1103/PhysRevE.97.052311 . We **do not** claim these prior ideas as new.

## 1. Six stages and mandatory gates

| Stage | Task | Primary risk | Main artifact | Start gate |
| --- | --- | --- | --- | --- |
| **B0** | Freeze evidence/estimands/sample and independent-review protocol | R1/R2/R3 | \`N9_B0_ROUTE_B_PROTOCOL_FREEZE_2026-10-14.md\` + SHA manifest | Current main/supp/DEV manifest verified |
| **B1** | E3a zero-mass decomposition + E1/E2 fairness/precision audit | R1/R2/R3 | \`N9_B1_ZERO_STRUCTURE_AND_DECISION_FAIRNESS_AUDIT.md\`, safe JSON | B0 PASS; verified existing event/user data |
| **B2** | E3b *medium-sized* time-safe structure-preserving null, multiple seeds | R3 | \`N9_B2_MEDIUM_DEV_RELATION_IDENTITY_NULL.md\`, manifests, safe aggregates | B1 interpretation + temporal/candidate parity + ethics/data-rights + resource PASS |
| **B3** | Stop/expand experimental decision & R1/R2/R3 independent referee-style verdict | All | \`N9_B3_RISK_AND_EVIDENCE_VERDICT.md\` | B2 robust assessment, including valid null outcome |
| **B4 (conditional)** | Lawful truly new blind forward-time TEST | Generalization | blind eligibility/approval and preregistered run | independent data existed uninspected & lawful; otherwise SKIP |
| **B5–B6** | Two rounds of manuscript revision and KBS submission audit | All | versioned main/S10 or S11, source-to-claim audit, PDFs | B3; B4 if independently authorized; human sign-off to submit |

**Never make B2/B4 expansion contingent on producing a favorable sign or small p-value.** All later experiments on known DEV are **post-hoc/exploratory**, even if this plan freezes upcoming analytic choices. Do not rebrand 5 folds or multiple random nulls as independent TEST cohorts.

### B0 — Pre-analysis freeze and independent validity review

- Freeze the *scientific question*, not an expected answer. Primary R1 inquiry: what share of E3a interaction is due to F/S zero-support changes vs magnitude of nonzero gaps, and can E1 policy reallocation remain meaningful when call counts/information are controlled? Primary R3 inquiry: user-level F original-minus-valid-null Full Memory NDCG difference on a **newly selected, broader DEV sample**; secondary S difference and source×regime null contrast. R2 is prior sensitivity/fairness, not an economic claim.
- Create exact source SHA register, 50,049 DEV events/12,628 users, user and timestamp fields, full candidate eligibility, target retention, original Base/Memory model checksums and corresponding private cached scores. Record original G5 TEST as forbidden input and current main/S10 as no-write baseline before final G5-like revision.
- Freeze B1 sign/zero partition, bootstraps, tie handling, primary metrics and descriptive strata. Freeze B2 sample *before* inspecting additional sampled outcomes; select **distinct/new events from all chronological DEV quartiles**, avoiding the prior 128 cherry-picked late-quarter pilot in the primary estimate. Stratify by pretarget clock/history, preserve user clustering and report event/user numbers. Avoid selecting on observed NDCG or null advantage.
- Freeze B2 three to five distinct null swap seeds **before execution**, exact degree/time/availability constraints, no future edges; label differing null seeds as **same cohort null randomness**, not external replications.
- Data rights: no private event/user edges in public GitHub or action artifacts; private causal stream and model checkpoints stay self-host; human investigators confirm dataset terms and authorization for each additional processing/release step.
- Explicit outputs \`GO/HOLD\` separately for (a) B1 analysis, (b) temporal null, (c) budget/capacity, (d) rights/privacy.

### B1-A — Zero-mass, source-contrast, and contribution decomposition (low cost, first)

Define per event:
\`dF_i=u10(Full,F,i)-u10(Long,F,i)\`,
\`dS_i=u10(Full,S,i)-u10(Long,S,i)\`,
\`I_i=dF_i-dS_i\`.

- Compute the **3×3 cross-tab** of signs \`(-,0,+)\` for dF and dS, event share and distinct-user count. Avoid calling transitions to/from zero strict sign reversal.
- For each cross-tab cell \`A\`, report \`C_A=(1/N)Σ_i 1_A(i)*I_i\`, its signed contribution to mean interaction, positive/negative cancellation, **and** group-specific means. Verify \`Σ_A C_A == +0.1153818679\` to numerical precision. A relative share exceeding 100% is possible under cancellation; show signed counts/values rather than misleading percentage pie.
- Analyze NDCG-support cases: both zero; only F nonzero; only S nonzero; both nonzero same/opposite sign. Distinguish top-10 censoring/target presence from substantive changes in relationship preferences.
- User-cluster bootstrap (2,000 or a method frozen before running) for major contributions and original total, if per-user outcomes available. Descriptive pretarget hist_distinct, hist_event_count, candidate count / dispersion strata with denominators, no target-based online selector features.
- A deliberately **general** comparison against ranking evaluation distortion: show which observations follow automatically from candidate-regime-dependent NDCG, and what remains a separate decision-valued empirical consequence. No new metric consistency theorem.
- **Pass** when accounting identities/source SHA/bootstraps agree; a weak/non-distinct mechanism is a legitimate result that narrows R1/R3 rather than causing endless experiments.

### B1-B — Decision and constraint comparability audit (low cost, in parallel)

- Reuse original E1 private S/F nested outer decisions (or exact reproducible B1 refit); check B1 30% F and S policy quality and **observed** calls: SAS 15,016 vs 14,988 (28 difference), GRU 14,762 vs 15,001 (−239 difference). User-disjoint inner calibration, no outer target leakage. E1 switch accounting, 21–23% policy disagreement, positive average switched-on and switched-off increment must exactly reconstruct +0.006159 / +0.004970.
- Report call-rate difference effects explicitly; if meaningful, an additional common *precommitted inner-only* budget/threshold calibration or randomized tie rule may provide a realizable sensitivity comparison. Matching observed outer counts/labels retrospectively is **non-deployable diagnostic only**, not equal-budget proof.
- Separate model quality and training-information entitlement: F→F uses F labels; S→F uses retrospective S labels; Adapted uses F labels; Two-stage differs in fitted head count. Do not claim method superiority solely from this contrast.
- Audit A1/E2 full frontier and shadow-price intervals from actual outer calls; if joint per-user A1 predictions exist, bootstrap paired breakpoints with clustered resampling; otherwise report **point-estimate sensitivity only**, not invented CI. Keep potential gate overhead and actual service-resource costs distinct.
- **Corrected-S: CONDITIONAL HOLD** unless the offline target-retained 574-negative-without-replacement sampling law, exact candidate roster/rank scores, selection inclusion probabilities and a defensible NDCG@10 estimator are all established and supervised only with legitimate training-fold information. Never invent correction from scalar NDCG.
- **Pass** when all information, calls, source hashes and scientific inference claims are auditable. No Base re-training or method architecture search.

### B2 — E3b medium-scale history-identity placebo experiment (controlled, not automatically full DEV)

**B2.0 Feasibility and temporal correctness:**
- Current 128-event late-quarter co-active pilot PASSED only a restricted historical-prefix design. It may not represent a correct rolling intervention for early or current-hour requests. Verify how the sealed causal stream is grouped/sorted by user and timestamp and how the original scorer builds Long and Short state.
- A request at time t may only see history before t. For any hourly-bin rewiring, include an altered bin **only after that bin has closed**; within an open bin, preserve causal original pre-t events or define a separately frozen sequentially valid swap. Never use an interaction later than t in constructing the null history for request t.
- Check both old and exchanged authors are available at original interaction times, not just target event time. Preserve per-user interaction count/timestamps, per-hour author counts and fixed target full-active candidate roster; audit degree marginals, candidate eligibility, repeats and original/null history coverage.
- First reproduce all original Full/Long, F/S scores **event-by-event** against frozen B1/B2 on the new sample before any placebo estimation. If original parity or time causality fails: **STOP**, do not trust null scores.

**B2.1 Frozen medium sample and null arms:**
- Start with **1,024 previously unexamined DEV events** sampled by a fixed seed across all chronological DEV quartiles and user strata (not 128-event late-quarter pilot); choose a second fixed **2,048-event** ceiling only if paired interval precision is insufficient and feasibility/CPU budget passes. The original 128 pilot must be reported separately and excluded from the primary analysis.
- Use *one* strict degree/time/activity-preserving null design and **3–5 pre-fixed swap seeds** to assess randomization sensitivity. All controls share exactly the same candidate F/S rosters, scoring implementation, target retention and Base; changing historic edge identities is the sole intended manipulation. Multiple draws are not independent datasets.
- Fixed Full Memory and Long-only primary scores; use sampled S only as an **offline diagnostic**. Add popularity-only as a floor reference (not as a fair expert) and optional generic/strength-matched source only if G0 validates comparability.
- Freeze the **existing pilot non-floor gate as a diagnostic**, not as a way to optimize placebo strength: for Full F control >= max(0.10, 0.3×original Full F); Full S >= 0.20; Full F >= popularity F + 0.02; >=10 positive-NDCG Full-F control events on pilot equivalent; >=10% prefix edge changes. For larger sample, also report control-to-real NDCG ratio, score spread, pair/author coverage, effective ranked support and counts. **If control collapses, mark INVALID**, do not claim real Memory's mechanistic superiority.
- Record full physical runtime/CPU/GPU, stable source hashes and false-positive future leakage tests; CPU streaming and stable cached rosters are preferred; GPU only where required by the actual scoring path.

**B2.2 Scientific estimands and precision:**
- Primary: \`T_F = mean[u_F(real Full)-u_F(null Full)]\`, paired by event and **bootstrapped by user**, with interval and counts; across-null-seed means and variability must be reported separately or using a clearly stated hierarchical approach.
- Secondary: \`T_S\`, \`T_F-T_S\`, Long-only source, and pretarget history-length/diversity conditional effects; avoid multiple unadjusted significant subgroup findings. Specify if model includes unchanged 10% popularity or other non-relational information, so \"relation identity contribution\" is interpreted conditional on preserved structure rather than universal causal effect.
- **Precision-driven, not significance-driven escalation:** before resampling choose a useful target interval half-width (e.g. 0.015 NDCG F on mean real-minus-null); if unmet at 1,024 but valid, expand to the predeclared 2,048 event ceiling, then stop or narrow claims. If control has non-floor but real-null effect near zero, **report near-zero**; do not alter swap windows or random seed to force superiority.
- No complete DEV 50,049-event run without a separate B3 approval and concrete reason it would change interpretation, uncertainty or KBS reviewer decision.
- All B2 conclusions **remain exploratory same-period DEV evidence**; even positive original-minus-null under F is not a randomized clinical-style causal effect nor fresh TEST.

### B3 — Go/stop scientific adjudication (no searching for positive outcomes)

Assess **R1, R2, R3 separately** as \`STRONG_WITHIN_TESTED_DESIGN / BOUNDED / HOLD\`, always conditional on original TEST vs post-G5 DEV evidence tiers. Include exact source→claim, positive/negative results, bootstrap units, competing explanations, fair comparison and permitted text.

- **Case A: stable nonfloor true-history advantage** beyond uncertainty in F on multiple fixed null seeds. Strengthen *within observed cohort* identity-specificity, but do not claim all historical relationship mechanisms are uniquely causal. If interaction additionally depends on F/S, state candidate dependence with effect and CI.
- **Case B: real and structurally valid null are close** or CI is wide. Downgrade independent identity-specificity claim and retain source composition/candidate supervision decision effect; useful negative scientific evidence, not grounds to run seeds until a desired result.
- **Case C: apparent advantage appears only on target-retained S**. No full-ranking identity advantage; discuss sampled regime evaluation specificity honestly.
- **Case D: controls fail causal timeline, activity, score parity or floor.** Stop E3b; present only 128 pilot as feasibility, not mechanism support; do not include invalid full analysis.
- **Case E: new truly unseen lawful cohort becomes available.** Activate B4 once external provenance and preregistered two primary hypotheses are authorized; otherwise explicit SKIP, no conversion of old examined G5 TEST to \"fresh test\".
- B3 may recommend **Route A bounded submission** when further experiments no longer produce identifiable information; further DEV expansion is not mandatory.

### B4 — Conditional independent confirmation (strictly optional)

- Start with a metadata-only blind eligibility audit of an unexposed independent chronological author-ranking period: legal data rights, cohort-unit alignment, genuine untouched outcome status, minimum event/user coverage, model/checkpoint/sampling parity and publication permissions.
- Authors must approve separate preregistered comparisons *before accessing outcomes*: primarily F-supervision downstream decision value over a precommitted comparator; secondarily Full-minus-Long source×candidate interaction or real-vs-valid-null identity effect (depending on B3). Frozen chosen folds/budgets/alpha/familywise handling.
- Execute once only; no reuse of G5 TEST or post-G5 50,049 DEV as independent test. If unavailable or rights ambiguous **B4 SKIP** and manuscript keeps bounded exploratory wording.

### B5 — Two-pass manuscript revision for coherent KBS thesis

**B5a evidence-first:**
- §3: keep incumbent-relative knowledge-value estimand; regime indices, switch accounting and source interaction remain empirical contrasts; no invented general theorem.
- §5: freeze cohort tiers (Twitch/M3 original TEST, 10,222-room retrospective, same 50,049 DEV and B2 medium DEV), 5×4 user-fold, offline target-retained sampled S, exact candidates, 120 vs original frozen 200 HGB iterations, actual calls, valid temporal null and inference units.
- §6.3: make E1's request-level decisions the core **decision-consequence** evidence; use one compact display for the 21–23% switch and paired value, E3a 3×3 accounting in S10.
- §6.4: retain one compact source-by-regime table and paired interaction; if B2 valid, insert original-minus-control F/S means/CI without overstating causality. If B2 null, narrow relationship-identity assertions.
- §6.5: cost-conditioned decision-support interpretation with actual q and hypothetical lambda, Always Memory adverse evidence retained; no actual money or serving-speed savings.
- S10: put 3×3 counts/contributions, full bootstrap/multi-seed/temporal controls, B1 original-call parity and optional E2 precision, pilot and new sample distinct. Prefer S10.13+ rather than create another uncontrolled sprawling supplement.

**B5b narrative-last:**
- Abstract, §1 Intro, §2 Related Work, §7 Discussion, §8 Conclusion and highlights rewritten only after B3; no algorithm-first change. Organize around **three RQs**: when is fixed relation knowledge valuable relative to the incumbent? how do candidate regimes alter its value/sources? when does valuation meaningfully improve resource-bounded knowledge-use decisions?
- Compare directly with KDD sampled metric inconsistency, ICML deferral and current KBS knowledge-aware rec, not vague \"first ever\" claims.
- Keep original adverse Always Memory and zero-mass/null findings. Remove process-stage, self-disclaiming repository language from journal prose while preserving transparent scientific limitations.

### B6 — KBS submission-grade QA and accountable authorship

- Compile current LaTeX main and S1–S10, check final reference/cross-ref, tables/figures, legend and PDF page visual inspection. Current 36/39-page previews are technical baselines, not journal page limits. Do not infer mandatory highlights/graphical abstracts/word count without checking the **live KBS Guide for Authors**; the ScienceDirect guide can be access-restricted and must be manually reviewed at submission.
- Claim-to-source table for every new numeric estimate (exact SHA, source ranker, F/S, user count, caller rate, CI family, fold and significance label). All numerical visuals must derive reproducibly from data, never generated by image models.
- Elsevier generative AI policy requires a manuscript preparation declaration when AI materially contributed to writing, and reproducible Methods disclosure when AI supported **research code or methods**. Review official policy https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals . Human authors must verify exact tools, versions, usage and oversight, cannot outsource actual attestation.
- Check original KuaiLive / M3 / Twitch dataset releases, data privacy rights, code/checkpoint redistribution, ethical/institutional claims, CRediT, contributions, COI/funding, data/code availability, exact KBS submission fields, author final approval. No need to publicly release private raw records if rights restrict them, but reproducibility claim must match accessible artifacts.
- Final gate: (a) **scientific GO**, if core claims are evidence-supported with non-invented confidence; (b) **technical GO**, if files compile and sources match; (c) **author/rights GO**, signed off by humans. Missing one keeps **SUBMISSION HOLD**.

## 2. Priority and compute discipline

**P0:** B0 freeze, B1 zero/interactions and fairness audit (existing hashes, no full GPU).  
**P1:** B2 temporal identity null 1,024 → optional 2,048 DEV event sample, multiple frozen seeds; calculate CPU roster/window costs and parity *before* larger execution.  
**Conditional P1:** B4 genuinely blind lawful TEST, only with independent source.  
**P2:** B3 adjudication; B5/B6 coherent revision, citations, ethics and journal-specific author forms.  
**Explicit deprioritization:** extra deep gates, repeated HGB hyperparameter search, generic rank/score fusion requiring unverified per-candidate vectors, arbitrary large-scale new Base training, and more exploratory tests in already-seen G5 TEST.

## 3. Acceptance and exit contracts

| Risk | Required minimum before claiming adequate mitigation | Stronger condition, if data permit | Adverse outcome branch |
| --- | --- | --- | --- |
| **R1** | B1 isolates zero-support and real decision reallocation vs known sampled metric artifact; precise prior-art differentiation and fair calls | lawful correction or valid relation-identity comparator produces additional explanation | frame empirical transfer of known metric issues to knowledge decisions; no novel metric/routing claims |
| **R2** | frozen all-policy quality/call envelope, audited q and training information, hypothetical-cost only | measured full-path costs and resource premise | retain decision support as conditional science; Always Memory default without cost |
| **R3** | B1 full source decomposition plus valid B2 null with paired user interval, repeated null stability and no floor | genuine independent time period TEST or larger temporally sound confirmation | narrow to candidate-dependent source valuation, not causal identity-specificity |

**Rule:** Null or weak effects don't automatically mean manuscript failure; instead reduce scope, preserve frozen primary TEST evidence and reassess whether the *joint* knowledge-valuation-to-decision insight still adds enough beyond KDD/ICML foundations. No false probabilistic acceptance guarantee.

## 4. Immediate next step and unchanged project state

Start **B0**: verify versioned data and write frozen \`N9_B0_ROUTE_B_PROTOCOL_FREEZE_2026-10-14.md\`, then B1 analyses. This plan file itself **does not execute B0–B6, run GPU, change original G5 TEST or alter main.tex/S10**. The existing \`N9_EXECUTION_GATE_STATUS_2026-10-13.json\` remains authoritative for completed prior G0–G6 and submission HOLD until actual next-stage runs succeed.
