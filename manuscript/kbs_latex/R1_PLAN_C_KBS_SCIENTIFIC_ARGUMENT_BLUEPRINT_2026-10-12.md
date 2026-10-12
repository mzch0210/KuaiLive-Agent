# R1 — Scientific argument and contribution hierarchy for KBS + Plan C

**Date:** 2026-10-12. **Decision:** R1 SCIENTIFIC BLUEPRINT PASS; R2 §5 Experimental Setup is authorized. **Scope:** editorial architecture and evidence allocation only. The eight-section canonical main.tex, S1–S9 supplements, frozen G0F/G5 TEST protocol and all neural experiments remain unchanged.

**Inputs verified:** [R0 evidence audit](R0_PLAN_C_EVIDENCE_PROTOCOL_AUDIT_2026-10-12.md), [12-record claim evidence ledger](R0_PLAN_C_CLAIM_PROTOCOL_EVIDENCE_MATRIX_2026-10-12.json), [original main.tex](main.tex), [original outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md), [frozen M3 TEST](../../experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md).

## 1. Central thesis and intellectual identity

Retain working title: **When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation**.

**Proposed scientific thesis, for later adaptation to the abstract and introduction:**

> The incremental ranking value of a fixed relationship-memory specialist is defined relative to a designated incumbent and its eligible candidates; estimating this event-specific advantage from pre-outcome context supports selective evidence use under a specified specialist-invocation constraint, with decision gains verified under two distinct frozen-test recommendation protocols.

**Necessary companion statement:** Decision quality conditional on an invocation constraint does not by itself imply a new universal deferral theory, unconditional superiority over always-Memory, lower total serving latency, a hard live TEST quota, six independent populations, or cross-platform zero-shot transfer of a trained gate.

The estimand remains specialist-relative single-positive ranking gain Δ_M(x;r) = NDCG@10(M,x;r) − NDCG@10(B,x;r). Conditional expectation η_r(z)=E[Δ_M|Z=z,R=r] is an application of established model/expert comparison; neither subtraction nor thresholding itself is claimed as a new theorem.

**Research identity:** Marginal relational-evidence valuation and prospectively specified expert choice in ranking; NOT a knowledge-graph encoder, general gate invention, SOTA leaderboard paper, cost-optimizer, or causal proof that candidate size alone drives effects.

## 2. Claim hierarchy: valuation → context → decision

| Claim | The scientific issue it resolves | Decisive evidence | Causal / interpretation limit | Function |
|---|---|---|---|---|
| **C1: Base-relative evidence valuation** | What does fixed relationship Memory contribute beyond the same-event incumbent and candidate set? Incremental value is not universal and can be conditional. | Twitch TEST Memory−Base −0.04232 overall but recoverable subgroup +0.22045; M3 TEST Memory +0.086–0.089 above its six fitted Bases. | Opposite means are observed across different ranked tasks and incumbents, not a single isolated cause. | Defines the decision target. |
| **C2: candidate-regime dependence** | Candidate construction can change the ranking comparison that defines knowledge value. | Original room-level KuaiLive, n=10,222 paired, sampled 575 rooms Δ −0.04120, full-active rooms +0.04631, shift +0.08751. | Old KuaiLive is already examined TEST with post-hoc regime diagnosis; crossed attribution is descriptive, not pure causal size. M3 author setting is NOT a new same-event C2 experiment. | Explains why an expert's relative utility is conditioned on the ranking regime. |
| **C3: decision benefit from relative-utility estimation** | Is predicting Memory minus Base more useful for choosing the fixed expert than merely predicting Base difficulty, specialist quality or uncertainty? | Twitch DEV-frozen Utility TEST +0.00772 versus Base and +0.00644 versus retrospective matched Difficulty. M3 independent one-shot frozen TEST: 47,575 events / 12,533 users, 2 Base architectures × 3 training seeds, five independently DEV-frozen selectors, all six Utility wins. | Twitch Difficulty is TEST-batch retrospectively count matched; M3 policies have differing realized TEST call rates, with a DEV-only ≤30% cap. No direct cost-saving proof. | **Primary empirical conclusion and headline §6.2.** |

The three statements are not three unrelated claims: **C1 operationalizes value; C2 identifies an essential conditioning dimension; C3 evaluates whether knowing the relative value helps a decision**. The author's model-specific six-seed findings corroborate C3 within **one** M3 TEST population, not six independent datasets.

## 3. Three precise research questions

**RQ1 (C1):** How does fixed relationship Memory's ranking contribution differ relative to an incumbent across observed history conditions and recommendation environments? Answer in §6.1 via overall and conditional Twitch TEST and mean-positive M3 TEST; do not attribute cross-platform sign reversal to a single factor.

**RQ2 (C2):** How sensitive is the measured specialist-minus-incumbent ranking utility to the contemporaneous candidate environment? Answer in §6.3 with paired old KuaiLive room sets, separating descriptions of candidate membership/normalization reference from causal claims.

**RQ3 (C3):** Do decision-time predictions of expert-relative ranking utility support better constrained expert selection than predictions of Base difficulty, expert standalone quality or Base uncertainty? Answer in §6.2 with Twitch and M3 separately frozen experiments; §6.4 measures consistency over fitted seeds; §6.5 reports unconditional expert quality and costs.

Do not invent a fourth research question just to accommodate Plan C or its execution chronology.

## 4. Nearest verified literature and exact innovation boundary

KBS official scope includes knowledge-based AI, recommender systems and intelligent decision support, with both methodological and practical expectations: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051

| Existing publication | Established contribution | Correct differentiation | Primary publication |
|---|---|---|---|
| Xie et al. 2026, MHGFCL, Knowledge-Based Systems, DOI 10.1016/j.knosys.2026.115673 | Multi-head fusion gate and focused-view contrastive learning for KG-aware recommendation, tested on 3 datasets. | Enhances and fuses learned representations; our fixed relational specialist is separately evaluated for **event-specific incremental ranking utility** relative to a frozen incumbent. Not the first gate. | https://www.sciencedirect.com/science/article/pii/S0950705126004132 |
| Kim et al. 2026, KAPER, Knowledge-Based Systems, DOI 10.1016/j.knosys.2026.116236 | Preference-relevant KG path evidence extraction for explanation and LLM reranking. | Selects evidence/path content; our study values a *fixed* ranking alternative against the incumbent. Not the first selective use of historical knowledge. | https://www.sciencedirect.com/science/article/pii/S0950705126009627 |
| Yerragunta et al. 2026, Knowledge-Based Systems, DOI 10.1016/j.knosys.2026.116167 | Dynamic conditional multi-stage gating in incomplete-KB question answering. | Different end-to-end QA knowledge fusion; demonstrates the broader gating idea is established. | https://www.sciencedirect.com/science/article/pii/S0950705126008932 |
| Chen et al. 2024, CKLF, Knowledge-Based Systems, DOI 10.1016/j.knosys.2024.111446 | Cognitive and sequence-aware graph knowledge representation for recommendation. | Long/short history modeling is known; the question here is the *marginal ranking value* beyond a specified incumbent. | https://www.sciencedirect.com/science/article/pii/S0950705124000819 |
| Mozannar & Sontag, ICML 2020 | Consistent defer-to-expert estimators. | This paper does not invent general-purpose comparative deferral. | https://proceedings.mlr.press/v119/mozannar20b.html |
| Narasimhan et al., NeurIPS 2022, Post-hoc estimators for learning to defer to an expert | Selection over fixed Base versus costly expert and accuracy/cost reasoning. | **Closest decision-theoretic antecedent.** Distinguish the ranking-specific fixed relational evidence target and causal temporal/candidate protocols, not mathematical originality in the gate. | https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html |
| Krichene & Rendle, KDD 2020, DOI 10.1145/3394486.3403226 | Sampled ranking metrics may invert relative model ordering. | C2 does not claim to rediscover this. It demonstrates the **knowledge-choice consequence** of candidate-sensitive relative ranking utility in the old paired room protocol. | https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ |
| Xu et al., AAAI 2026, GUIDER, DOI 10.1609/aaai.v40i19.38639 | Uncertainty-guided LLM-based reranking. | M3 compares a **simple Base margin uncertainty proxy**, NOT the GUIDER algorithm; no claim of directly outperforming GUIDER. | https://ojs.aaai.org/index.php/AAAI/article/view/38639 |

**Publication gap statement for adaptation, not verbatim assertion of all literature:**

> Prior work has developed representations, fusion schemes and expert-allocation procedures for auxiliary knowledge. This study asks a different empirical question: whether the incremental ranking contribution of a fixed historical relationship specialist, relative to a trained incumbent under the same temporally eligible candidate protocol, is conditionally predictable and useful for pre-outcome ranking selection.

No unsupported “first” or “universally SOTA” claims. These verified works represent principal intellectual neighbors rather than an exhaustive survey; §2 and R7 will complete and double-check manuscript citations.

## 5. Specific rhetorical contract for each unchanged main section

**§1 Introduction (R5, edit after results).** Five-paragraph arc: historical relationships and incumbent overlap → fixed evidence is not always helpful relative to incumbent → candidate availability changes the ranking question → predict fixed specialist-minus-Base benefit rather than only Base difficulty → evidence roles (Twitch frozen selection, old room paired context diagnostic, M3 frozen new-time author task). End with three tight C1/C2/C3 contributions. Avoid an experiment-timeline narrative.

**§2 Related Work (R5).** Three strands: (i) historical/relational knowledge in recommendation; (ii) expert choice, known Learning-to-Defer and uncertainty-based methods; (iii) live-streaming temporal availability and sampled-metric risks. End with the precise incremental-utility research gap; do not imply that KAPER, MHGFCL, GUIDER or post-hoc deferral were absent.

**§3 Problem Formulation (R4).** Retain event/ranking utility, Δ_M, η_r and the selected gain expression. Separate pre-outcome observable Z from target-dependent diagnostic states. Add only exact DEV pointwise call-rate calibration versus *realized* TEST call fractions, and difference between descriptive budget count and true resource cost. Twitch retrospective top-m is not a deployable frozen pointwise Difficulty policy.

**§4 Framework (R4).** Three linked objects: fixed incumbent B, transparent relation Memory specialist M, pre-outcome conditional utility gate. Separate platform implementations: LiveRec streamers / KuaiLive old Dual-ID live rooms / M3 SASRec or GRU4Rec creators. Twitch gate **14 features**; M3 **12 features**; no single zero-shot gate transfer. Keep fixed short/long/popularity components and note M3 all-prior-event history semantics; avoid suggesting target-defined history states are legal online gate inputs.

**§5 Experimental Setup (R2 FIRST canonical edit).** Replace two-task opening and Table 1 with **three separately specified evaluation protocols**. State author versus room unit and distinct splits; M3 4,096 × 575-author panel was DEV *checkpoint screening only*; full-active TEST median **31,065 warm active authors**. Describe two architectures × three model seeds, five independently DEV-frozen gate objectives, 47,575-event one-shot target-blind G5-A and independent G5-B label reveal. History is prequential: only *strictly earlier observed* TEST interactions are available as future-event history. Present actual TEST invocation rate for all strategies and the difference between DEV constraint and TEST realizations. Primary M3 hypotheses = Utility−Base, Utility−Difficulty, Utility−Specialist; group-wise Holm of three tests within each of six fitted-model conditions, 5,000 user-cluster bootstrap and 5,000 signflips, correlated same-cohort results; secondary Uncertainty tests are not in these three preregistered comparisons.

**§6 Experimental Results (R3).** Keep five sections, change evidence arrangement:
- **6.1 Heterogeneous Utility:** Twitch negative overall / positive target-defined recoverable subgroup; M3 Memory positive versus six Base means. Cross-protocol explanation descriptive, not causal.
- **6.2 Decision Value (CENTER):** Twitch frozen policy versus matched-test-count retrospective Difficulty, plus M3 one-shot five DEV-frozen strategies versus Base; actual TEST rates and unconditional Memory side by side. Uncertainty strongest non-Utility in M3 but secondary comparator.
- **6.3 Candidate-Regime:** old KuaiLive paired same 10,222 room targets, sampled-575 vs full-live sign reversal, descriptive reference allocation; don't reclassify M3 author task as candidate-count intervention.
- **6.4 Robustness:** two Base architectures × three independently trained seeds on **one** TEST cohort, paired CI and group-specific three-Holm; Twitch feature-family DEV ablations remain contextual diagnostics.
- **6.5 Invocation Budget and Cost:** M3 Always Memory NDCG **0.346792** > Utility **0.301766–0.304004**; warmed DEV means Always Base **1.4245 ms**, Always Memory **0.8033 ms**, Utility selective **1.8018 ms**, only 256 sampled requests; NOT an end-to-end production speedup or deployed scarcity benefit. M3 actual gate calls vary despite DEV ≤30% threshold calibration, including History **35.47%**. Quantify full-path overhead honestly.

**§7 Discussion (R5).** Explain incumbent-relative knowledge value, event and candidate conditioning, why expert relative utility differs from difficulty/uncertainty for a *particular* Memory, relation to L2D and knowledge fusion, **Always Memory accuracy and cost dominance in M3**, limits of a nominal call constraint and noncomparable ranked units, prequential history and same-TEST multi-seed dependence. Give coherent synthesis, not duplicate §6 numeric tables or a lengthy apology list.

**§8 Conclusion (R5).** Three moves: empirical relative evidence value; bounded decision benefit of frozen Utility across different prospective TEST conditions; full candidate/budget/deployment scope. No universal savings, no causal platform attribution, no zero-shot generalization claim.

Abstract, Highlights and journal submission declarations only after full claims and supplement stabilize (R8). Do not invent exact KBS word/page/highlights requirements.

## 6. Main figure/table redesign without inflating the already ~29-page old build

| New display function | Recommended treatment | What it must prove / disclose |
|---|---|---|
| Three-protocol overview | **Replace** current 2-row Table for Twitch / old room KuaiLive / M3 author | Split, unit, candidates, n DEV/TEST, and distinct inferential role in a compact table |
| Policy comparison status | **Replace/condense** current compared-methods Table | Twitch Utility DEV-frozen vs retrospective Difficulty; M3 5 DEV-frozen pointwise; Random and Oracle clearly retrospective |
| Frozen TEST policy performance | Keep Twitch table and add **one concise M3 representative-seed table or task-separated blocks** | Base, Memory, Utility, Difficulty, Specialist, Uncertainty, History; each M3 actual TEST %; different tasks never pooled |
| M3 six-fit robustness | One small plot or six-row table of Δ(Utility−Base) and secondary Δ(Utility−Uncertainty) | 2 families × 3 seeds all same heldout users; full 18 CI pairs and Holm data to S8 |
| Candidate-regime evidence | **Retain** old same-event 2×2 room table/plot with condensed prose | −0.04120 vs +0.04631; reference allocation descriptive |
| Cost comparison | Replace or compact existing §6.5 resource table, preserve separate evidence contexts | Explicit Always Memory winner on measured warm M3 paths; no cost-saving claim |
| Twitch state/ablation | Keep informative history-state plot; move fine-grain feature-family table if layout strained | States are target-dependent diagnostics, 14-feature ablation is DEV-only |

Target ~1 protocol table, ~1–2 policy tables, ~1 multi-seed graphic, ~1 candidate-regime table and ~1 compact cost table in the main; other full numeric matrices belong in S1–S9 or focused S10. Exact display count and old floating positions will be decided during R3 build, not artificially fixed.

## 7. Exact R0 source conflict resolution owners

| R0 code | Architectural solution | Planned editing stage |
|---|---|---|
| P0-01 | Three evidence protocols / not only Twitch + old KuaiLive | R2 §5, R5 §1/§7/§8 |
| P0-02 | Separate Twitch retrospective comparator from M3 five DEV-frozen comparators | R2 §5, R3 §6.2, R6 S7 |
| P0-03 | DEV max-30% threshold selection vs unequal realized TEST calls | R2 §5, R3 §6.2/§6.5, R4 §3 |
| P0-04 | Include unconditional Always Memory and actual negative M3 warmed latency | R3 §6.5, R5 §7, R6 S9 |
| P0-05 | 14 vs 12 features, room vs author, 575 screening vs full TEST | R2 §5, R4 §4, R6 S1–S3 |
| P0-06 | M3 Holm within three per model/seed; shared TEST cohort | R2 §5, R3 §6.4, R6 S8 |
| P1-01 | G0F typed timestamp hash discrepancy | R2/S1; no retrospective "perfect code match" claim |
| P1-02 | Different deterministic tie conventions in older DEV and G5 frozen TEST | R2/S2 without modifying result generation |
| P1-03 | S1–S9 old sole-Twitch scope | R6 |
| P1-04 | Differentiation from general deferral / known knowledge gating | R5/R7 |
| P1-05 | Archive old G4 in-progress as dated provenance, prefer completed G5 | R6 |
| P1-06 | Stable research artifacts with privacy and hash guarantees | R6/R8 |

## 8. Anticipated top reviewer objections and evidence-backed answers

| Potential KBS reviewer concern | Scientific answer | Do not claim |
|---|---|---|
| This is an existing Learning-to-Defer algorithm | Correct: generic relative allocation exists. Novel study is the fixed relational ranking specialist's candidate-conditional marginal evidence value and prospective recommendation evaluation. | General first deferral theory, novel conditional expectation theorem |
| Mean Memory gain has opposite signs | Tasks, reference Base and candidate regimes differ; C1 measures conditional value; old paired C2 shows candidate effects in one setting. | Candidate count solely caused cross-task sign reversal |
| Why choose Utility when Always Memory is better and faster? | The experimental objective is decision quality under **specified call constraints**, whose practical economic necessity is NOT demonstrated for current M3; the warm microbenchmark challenges a deployment advantage. | 70% system savings, economically optimal rollout |
| Were all methods at the same TEST budget? | No: all M3 frozen pointwise thresholds were selected under the same DEV budget constraint, actual TEST rates differ, and Twitch Difficulty is retrospectively matched. | Strict common 30% TEST quotas or equal real hardware costs |
| Six seeds produce six independent successes? | Six trained models evaluated on the same TEST user cohort, with grouped paired intervals and three-Holm per model/seed; not six independent population replications. | Global 18-test FWER, six independent datasets |
| History leaks TEST target? | G5-A uses prequential **strictly prior** observed TEST interactions; current TEST target and future are excluded from gate/top10 input, target labels opened only later in G5-B. | No TEST interactions ever enter user history |
| Does this beat GUIDER or modern SOTA? | A Base-margin uncertainty proxy was compared, not complete GUIDER; designated Base pair is not an exhaustive SOTA comparison. | Direct GUIDER or across-protocol leaderboard superiority |

## 9. Gate acceptance

- [x] One clearly worded scientific thesis (fixed Memory, incumbent, candidates, decision-time Utility).
- [x] C1 → C2 → C3 forms a coherent scientific argument; C3 is the centerpiece, not a fourth Plan C claim.
- [x] Twitch, original KuaiLive room, new M3 author evidence identities are noninterchangeable and traced to R0.
- [x] All twelve R0 evidence IDs assigned a home via C1–C3, methods, cost and supplementary sections.
- [x] Frozen TEST comparator status, model-seed dependence, call-rate drift, Holm assumptions, Always Memory and measured negative cost all included.
- [x] 2024–2026 original KBS papers and original deferral/sampling sources checked at publishers; novelty bounded by prior methods.
- [x] Eight-section structure and targeted tables/figures specified; no chronological "Plan C" section.
- [x] No main.tex, supplement or frozen source edited in R1.

**R1 DECISION: PASS; R2 NOW READY.** First canonical edit must be §5 Experimental Setup, not Abstract/Introduction. Retain argument-first academic prose, keep execution logs outside the paper, and avoid post-TEST policy changes.
