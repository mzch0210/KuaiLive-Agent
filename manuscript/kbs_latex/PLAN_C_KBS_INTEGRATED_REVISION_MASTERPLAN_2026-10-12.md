# KBS manuscript revision master plan — integrating frozen Plan C evidence

**Status:** Approved for planning only; **no change to the canonical manuscript or existing supplementary files by this document**.
**Date:** 2026-10-12. **Target:** Knowledge-Based Systems (Elsevier).
**Canonical source:** manuscript/kbs_latex/main.tex, eight sections; supplementary S1–S9 integrated draft 2026-10-10; KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md.
**New frozen evidence:** experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md, G4_EXTRA_SEED_FULL_ACTIVE_DEV_GATE_AND_COST_RESULTS_2026-10-12.md, G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json and GitHub Actions successful G5-A #38225946950, G5-B #38226690320.

## 0. Editorial decision and immutability

Retain the title **When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation**, subject to late-stage title fit confirmation. Retain **eight main sections**. Rewrite by scientific argument, not experiment chronology. Preserve previously frozen original Twitch / original KuaiLive sources and all Plan C G5 TEST outcomes as **immutable**. Do not change models, split, gate thresholds, feature specifications, post-hoc decision rules, hypotheses, observed scores, uncertainty estimates or the original report status based on TEST. Any new TEST-dependent analysis is transparently **exploratory** and must not replace the G5 one-shot inference.

**Central thesis:** For a specified trained incumbent and eligible candidate universe, a fixed relational-knowledge specialist has measurable event-specific *incremental ranking utility*; decision-time estimation of that *relative* utility supports selective evidence use in a specified invocation-constrained setting, but neither proves a new universal deferral algorithm nor guarantees unconditional superiority, lower latency or net deployment savings.

**Hierarchical claims:** C1 operational Base-relative value (measurement; Twitch and M3 different signs), C2 ranking-context dependence (original KuaiLive paired room samples; M3 is *not* a replicated same-event room intervention), and C3 prospective-feature decision value (frozen Twitch TEST and newly one-shot frozen M3 author-ranking TEST). C1 and C2 give scientific conditions for C3 rather than three parallel inventions.

## 1. Version-anchored evidence matrix (R0, publication P0)

Construct a frozen **claim–protocol–outcome–source** ledger before editing prose, with fields:

- Claim ID (C1, C2, C3, costs); dataset release and collection period; ranked unit (room versus author/streamer); Base model family, trained seed, selected checkpoint; fixed Memory rule; prior-event history eligibility; split logic; candidate membership and number/availability; event and unique-user counts.
- Status: independent frozen TEST / retrospective paired diagnostics / DEV-only selection / nondeployable hindsight benchmark / warmed replay.
- Event-level metric, exact unrounded pairwise contrast, 95% user-cluster interval with method and assumptions, declared inferential family, adjustment method; policy pointwise threshold and **realized** TEST call count and fraction; frozen artifact SHA/Actions run.
- Special flags: label-free versus target-dependent feature; prequential previous-TEST history allowed; candidate ID tie-breaking; intended resource interpretation; scientific claim beyond evidence (prohibited).
- Three mandatory cross-protocol checks: **Twitch (streamer recommendation, 44,221 TEST, 14-feature HGB, Utility frozen threshold, Difficulty retrospectively top-m matched)**; **original KuaiLive (room ranking, 10,222 paired already-inspected TEST targets, 575 sampled rooms versus full-active room regime, no second frozen gate confirmation)**; **new KuaiLive-M3 (author ranking, 47,575 forward-time TEST / 12,533 users, 12-feature gate, 6 independently trained checkpoints, five DEV-frozen pointwise strategies, full available warm authors)**.

Accept original observed main findings:
- Twitch TEST Base NDCG@10 0.58211, fixed Memory 0.53980, Utility 0.58983, 6,650 / 44,221 invocations; Utility−Base +0.00772, Utility−retrospective-Difficulty +0.00644. Target-relative recoverable subgroup helps whereas overall Memory is negative.
- Original KuaiLive same-event room candidate-regime Memory−Base sampled −0.04120, full +0.04631, paired shift +0.08751. Do not report the two-factor allocation as isolated causal membership/size effect.
- M3 author full-active one-shot TEST fixed Memory NDCG@10 0.346792; SASRec Base at first seed 0.258004, its Utility 0.302866, strongest non-Utility comparator Uncertainty 0.289373. Across 6 Base fits Utility NDCG@10 ranges 0.301766–0.304004. Do not pool absolute NDCG across Twitch, original KuaiLive and M3 as identical ranking tasks.
- Three primary one-sided contrasts per Base/seed in M3: Utility−Base, Utility−Difficulty, Utility−Specialist; 5,000 user-cluster bootstrap CIs and 5,000 sign randomizations; **Holm adjustment of three contrasts separately for each Base/seed**, not a global 18-hypothesis family. Utility−Uncertainty is substantively important secondary effect, **not** one of those three preregistered primary contrasts.
- M3 G5 TEST sample-specific call fractions are naturally different despite all methods' DEV 30%-cap optimization. Primary SASRec seed Utility 29.215%, Difficulty 29.904%, Specialist 29.568%, Uncertainty 30.180%, History 35.472%. Across six Base fits actual Utility 27.718–29.215%, Difficulty approximately 29.65–30.33%, Uncertainty about 29.41–30.26%; History 35.47%. Hence **never** write matched TEST invocation count, hard 30% TEST quota, or uniform realized budget for M3. Report absolute performance together with actual calls; 30%-cap is a **DEV policy-selection design**.
- M3 Always Memory outranks all frozen Utility policies (0.346792 versus 0.301766–0.304004); warmed offline DEV replay 256 events: Always Memory ~0.803 ms mean; Utility route ~1.802 ms mean; no demonstrated net latency saving or unconditional optimal deployment. A *fixed expert-call allowance* is a research design constraint; real external invocation cost has **not** been proven.

**R0 acceptance:** Every main-text number maps to a verified evidence file and exact metric/scope. Independent reviewer can reproduce the key comparison and identifies whether a claim is inferential or descriptive. Any SHA mismatch or missing provenance blocks the editing gate; no simulated replacements.

## 2. Contribution logic and argument architecture (R1, P0)

**Introduction progression** (4–5 tightly developed paragraphs, not process description): (a) base already absorbs history; (b) fixed relational evidence can overlap or complement; (c) incremental *value is relative* to incumbent + candidates; (d) event-level relative utility is predictable and can serve constrained selection; (e) two independent frozen decision environments, paired candidate protocol as explanation; contributions C1–C3.

**One-sentence main idea:** The relevant question is not whether additional historical knowledge exists or is predictive on its own, but whether invoking this fixed relational specialist improves the selected ranking compared with the incumbent in the current candidate context.

Keep C1/C2/C3 as three mutually reinforcing claims:
- C1 value defined and measured; cross-context positive versus negative mean shows context dependence, not causal attribution.
- C2 paired same-event old KuaiLive demonstrates candidate-regime effect (candidate size/composition/ref combined), not another prospective test.
- C3 most important evidence: same-event real frozen policies, both Twitch and new M3, fair declared comparators and caveats.
No new abstract novelty claim about deferral theory, sampled metric phenomenon, universally stronger neural model, causal intervention, zero-shot platform transfer, end-to-end system acceleration or fixed quota enforcement.

**R1 acceptance:** In each section the first paragraph answers what question it serves; claims in intro matched verbatim in §6/§7; the paper reads as C1→C3 supported by C2, not eight isolated experiments.

## 3. Precise section-by-section edits (R2–R5)

### §1 Introduction — revise after empirical §§5–6 stabilize

Replace obsolete statement "Twitch provides the frozen selective test while KuaiLive supplies candidate diagnostics" with differentiated Twitch/original KuaiLive/M3 evidence roles. Use M3 as *independent later-period frozen author task*, explicitly not an identical original room task or disjoint-person replication. Add 6 Base fit verification as empirical strength, not 6 independent datasets. Tighten 3 contributions without turning proof limits into apologetic narrative.

### §2 Related Work — literature positioning before polishing §1

Organize 3 families only: historical/knowledge-enhanced recommendation, deferral and uncertainty-guided allocation, and live-streaming/real candidate evaluation. Explicitly compare with Learning-to-Defer and existing dynamic knowledge gating: novel contribution is the *study of fixed relationship knowledge's ranking-specific incremental value under frozen comparator protocols*, not new general gating framework. Cite and fact-check KBS 2024 CKLF, KBS 2026 KAPER / MHGFCL / Yerragunta et al., plus officially published papers already in manuscript; do **not** claim direct algorithm replication of these methods.

### §3 Problem Formulation — targeted rather than wholesale rewrite

Keep event utility u_K, Δ_M, E[Δ_M | Z,R], and E[aΔ_M] as primary analytical foundation. Clarify the strict distinction:
- Constraint on DEV selected specialist calls, expected online call-rate versus **actual** TEST realized rate.
- Cost-of-expert objective not identical to true wall-clock compute or deployment utility: 30% Memory calls does not mean 70% total cost saved.
- DEV-frozen pointwise threshold (Twitch and M3) versus post-hoc batch top-m controls (original Twitch Difficulty/Oracle). M3 all five methods are DEV-frozen pointwise.
- User-level temporal eligibility and prequential earlier TEST observations, without current/future target leakage.

### §4 Framework — unify core value, state platform-specific implementations separately

Retain transparent Short/Long/Popularity fixed Memory conceptual equation. Document M3 source definition including all prior user-author events in Short 10 recency slots and all-author Long denominator, frozen TRAIN warm author candidate eligibility. Explain M3 Base SASRec, GRU4Rec and 3 independent trained seeds and DEV-selected checkpoints. Declare **14 Twitch pre-outcome features** versus **12 M3 pre-outcome features** explicitly, with exact feature list mapping in supplementary; avoid suggesting identical learned cross-dataset model or universal feature representation. State sparse history-support feature exactness and whether candidate support preprocessing precedes gate decision. Retain no target-defined states in gate inputs.

### §5 Experimental Setup — complete protocol redesign (primary P0)

Partition experimental tasks into **three named protocols** with a one-page compact table:
(A) Twitch LiveRec/streamer, 46,878 DEV / 44,221 TEST, official frozen pointwise Utility + retrospective equal-m controls.
(B) Original KuaiLive/room, 10,222 DEV/TEST subjects, previously examined paired candidate-regime diagnosis, no second independent prospective gate.
(C) M3/author, global forward-time TRAIN 24,995,148 events; DEV 50,049 / TEST 47,575; 12,533 TEST users; real-time available warm-author full roster; ~31,065 median TEST candidates; 2 Base families × 3 selected checkpoints; five DEV user-disjoint OOF gate objectives; prospectively fixed pointwise thresholds, one-shot TEST; exact target-blind top10 and causal history procedure.

Directly distinguish 575-candidate **DEV checkpoint screening panel (4096 events)** from full-active DEV/TEST NDCG. Define primary/secondary contrasts, user-cluster paired uncertainty, 5000 sign flips and Holm within each model/seed's 3 comparisons only, and potential sign-symmetry null assumption. Document 30%-cap **on DEV**, report realized TEST rates and show controls have unequal TEST call rates. Distinguish 20-seed random draws and hindsight Oracle@30 expected value from deployable frozen methods. Report absolute Memory comparator and fixed policy timing caveats. Preserve chronological original status and exact frozen SHA in supplement.

### §6 Results — central scientific rewrite, no experimental chronology

Proposed **five subsections** matching the original stable 6.1–6.5 structure:
- **6.1 Heterogeneous Relationship-Evidence Utility**: Twitch positive recoverable subgroup but negative overall; M3 fixed Memory positive versus six independently trained Base fits; interpret the contrast without claiming a single causal factor.
- **6.2 Decision Value of Predicting Relative Utility**: lead with frozen Twitch and M3 TEST results, prioritize Utility−Base, Utility−Difficulty and Utility−Specialist in M3; show strongest non-Utility Uncertainty descriptively and actual invocation rates, Always Memory, budget Oracle contextual bound. Explain different Twitch retrospective Difficulty versus M3 frozen Difficulty controls.
- **6.3 Candidate-Regime Dependence**: retain original 10,222-event old KuaiLive room sample/full same-event reversed sign and descriptive candidate/reference allocation. M3 full-author settings demonstrate application, **not** second candidate-size intervention.
- **6.4 Robustness/Explanatory Diagnostics**: 2 Base × 3 seeds TEST consistency, user-cluster CIs, correct inference family; original Twitch 14-dimensional feature-family DEV ablation and memory components; move full 6×5 numeric tables and 18 inferential intervals to supplement.
- **6.5 Invocation Constraints and Computational Overhead**: show DEV 30% versus TEST realized call fractions; Always Memory dominance and actual warmed replay costs; 256-event warm DEV replay is not production latency. If always Memory cheaper and better in the observed M3 conditions, explicitly say selective deployment is **not justified as superior on these measured axes**.

Primary results table suggestions: (1) 3-protocol definition, (2) Twitch and M3 frozen TEST policy table with real rate, (3) six-model dot/interval figure for incremental Utility and Uncertainty comparisons, (4) original KuaiLive paired regime table/figure, (5) compact computational path table. The total must remain readable; move auxiliary detail into S1–S9 or S10 appendices rather than appending bulky blocks.

### §7 Discussion — new causal scientific synthesis (P0)

Reorganize around (i) what *relative valuation of fixed knowledge* contributes conceptually; (ii) why Twitch and M3 show opposite average Memory relationships (do not attribute to isolated factors); (iii) why Utility beats incumbent difficulty/uncertainty/quality for a specified specialist and when the gate is useful; (iv) relation to established deferral methods and recommendation knowledge fusion; (v) always-Memory, external call budgets, positive gate overhead and real deployment applicability; (vi) remaining cross-dataset non-identical task, observed-history prequential behavior and multi-seed same-cohort dependencies. Discuss substantive implications instead of restating every table.

### §8 Conclusion and frontmatter — last after all evidence stable

Three precise conclusion moves: (i) conditional knowledge value, (ii) frozen relative-utility decision gains in two distinct evaluation settings, (iii) context and deployment boundaries. Write Abstract and 3–5 Highlights after the body; no fabricated end-to-end cost or generalization claim. Title/keywords revisited last. Authors/affiliations, corresponding author, funding, conflicts, code/data accessibility, CRediT/AI-use declaration require author's facts/approval; do not invent them.

## 4. Supplementary redesign (R6, P0/P1)

Retain S1–S9 content and traceability, but update stale global scope statement saying only Twitch has independent frozen policy. Suggested ownership:
- S1 data source, collection period, G1 global versus per-user split, user-/item-level identifiers, strict causal history and prequential policy.
- S2 model training and precise freeze chain, 6 checkpoints, chronological history, all hashes and original P0/P2 provenance.
- S3 baseline fairness, model budget, 575 screening versus full candidate evaluation, original Dual-ID versus M3 SASRec/GRU4Rec comparability.
- S4 Twitch component and history sensitivity, untouched original.
- S5 original KuaiLive room sampled/full paired regime factors and nine draws (retrospective only).
- S6 Twitch length-state and recurrence controls, untouched original.
- S7 Twitch DEV feature/rate and M3 12-feature OOF, 5 policy thresholds, actual TEST invocation fraction, Random@30 and Oracle@30 policy definitions.
- S8 original KuaiLive room seed sensitivity **and separate** new M3 author three-seed full-active DEV/TEST; 18 paired CIs and model-specific Holm correction tables.
- S9 separate computational evidence from original 575-room CPU benchmark and new 256-event RTX3090 M3 warmed replay; explicit exclusions; no borrowed Twitch invocation percentages.

If S7/S8/S9 become too long, create a clearly referenced S10 focused on **M3 independent frozen validation and audit** instead of merging unrelated rank tasks. Do not duplicate all table content in main text.

**R6 acceptance:** Every supplement claim and file link refers to the right dataset/seed/TEST; no unresolved contradiction such as "M3 not yet evaluated" or "Twitch only frozen TEST"; formulas/platform feature differences and call-rate drift are explicit. User-/event-level private data remain private and archived Actions artifacts are not represented as permanent repositories.

## 5. KBS competitor literature and editorial fit (R7, P1)

Official journal scope encompasses recommender systems, knowledge representation/engineering, AI methods and decision support; this supports relevance but not probability of acceptance. Study exact published KBS:
- Xie et al. (2026), *Fusing multi-head gating and focused-view contrastive learning for knowledge-aware recommendation* (KBS Vol.341; DOI 10.1016/j.knosys.2026.115673).
- Kim et al. (2026), *Leveraging graph path evidence for explainable recommender systems* (KBS Vol.347, DOI 10.1016/j.knosys.2026.116236).
- Yerragunta et al. (2026), *Dynamic conditional gating mechanisms for Question Answering over incomplete Knowledge Bases* (KBS Vol.346, DOI 10.1016/j.knosys.2026.116167).
- Chen et al. (2024), *Cognitive-based knowledge learning framework for recommendation* (KBS Vol.287, DOI 10.1016/j.knosys.2024.111446).
- Mozannar & Sontag (ICML 2020) consistent learning to defer; Krichene & Rendle (KDD 2020; CACM 2022) sampled ranking metrics; original paper's official published sources for GUIDER and MemRec.

Write literature-to-claim gap matrix: prior work improves knowledge *representation/fusion/gating* versus this paper quantifies fixed **specialist-relative event ranking value** under task-appropriate candidate eligibility and TEST-frozen prospective invocation; do not use vague unsupported “first” or assert state-of-the-art best NDCG across nonmatched methods. Attribute originality to the verified empirical synthesis and its decision-specific target, not to novel general conditional expectations.

## 6. Publication safety / final QA (R8, P0)

- Frozen numbers/source: compare every manuscript decimal against exactly accepted README/artifact JSON before rounding; negative/positive signs and CIs, sample counts, call rates, seed numbers, model epoch and paired scope. Always Memory present in main policy table, and warmed cost disadvantage present in §6.5.
- Protocol/logic: no mixing of Twitch 14-feature HGB versus M3 12, original KuaiLive room versus M3 author, 575 screening versus 31k full TEST candidates, retrospectively TEST top-m versus DEV-frozen pointwise, derived six seeds versus independent datasets, Holm per three versus global 18, early TEST history versus current target leakage.
- Editing style: argument-driven academic prose; eliminate workflow updates, git run IDs, patch chronology and apology-style self-limitation from main text. Keep substantive limitations coherently in Methods and Discussion. Main claim measured before qualifiers; avoid concealment of unfavorable Always Memory evidence.
- Build: reproducible LaTeX PDF, unresolved citation/reference checks, tables/figures legibility, no overfull boxes, claims/source consistency review, independent KBS reviewer-style edit with concrete objections and completed remediation gate.
- Elsevier policies: up-to-date AI-assisted manuscript preparation declaration is required when AI substantively rewrites prose; authors verify and approve tool name, purpose, oversight and scientific accountability. Data availability, author/contributor/funding/conflicts declarations as applicable. Elsevier generic Highlights guidance states 3–5 highlights, up to 85 characters each **when the target journal requires or accepts them**. The KBS-specific Guide for Authors may return 403 from automated search; journal-specific mandatory abstract word count/Highlights/graphical abstract/length must be checked by the authors at the submission portal and **not fabricated as verified facts**.
- Submission gate: abstract, actual authors/affiliations, declarations, editable manuscript, figures/tables, response to critical novelty and economics reviewer concerns, final PDF, supplemental file(s), in-line data/software source, checksums and authors' approval.

## 7. Proposed staged execution with evidence gates

| Gate | Purpose | Inputs | Output | Conditions for pass |
|---|---|---|---|---|
| R0 | lock evidence/compare three protocols | current main, supplement, G5 accepted JSON | claim–protocol–evidence matrix and P0 issues | all 3 datasets, frozen scope and actual call rates, 6 Base and test CI identity traced |
| R1 | scientific narrative/novelty blueprint | R0 + KBS literature | revised C1–C3 argument map, headings and planned main figures | main sentence and three claims nonoverlapping; novelty not overclaimed |
| R2 | rewrite §5 Experimental Setup | R1, source G0F/G5 | protocol-valid §5 and method appendix crosslinks | TEST thresholds, 12-vs-14 features, prequential, per-seed Holm all accurate |
| R3 | rewrite §6 Results | R2 + measured results | compact five-subsection main evidence with tables/figures | no missing Always Memory; Frozen TEST vs retrospectives/cost boundaries clear |
| R4 | revise §3–4 theoretical/method bridge | R2–R3 | matched formalism, M3 implementation + diagram | unchanged mathematics, no phantom universal budget or leakage |
| R5 | revise §1–2, §7–8 prose after evidence | R3–R4, primary literature | claim-first end-to-end manuscript | coherent C1/C2/C3 with substantive cost critique |
| R6 | supplement S1–S9 integration | R0–R5 | traceable complete supplementary manuscript | no stale Twitch-only frozen claim, appendix/table numbers synchronized |
| R7 | literature/novelty referee-style audit | R5–R6 | review challenges/answers, bibliography QA | precise differentiation from L2D, KBS gating/knowledge fusion and sampled metrics |
| R8 | submission engineering and independent full-paper QA | all previous, authors' facts | reproducible PDF and complete submission pack | line-by-line evidence signoff, zero unresolved citations, all author/declaration fields completed |

**Scientific workflow:** R0 → R1 → R2 → R3 → R4 → R5 → R6 → R7 → R8. Within R4 or R6, noncanonical copies may be drafted in parallel, but no conflicting simultaneous edits to main.tex. Create durable Git commits after each gate. Each gate must produce (a) changes, (b) detailed evidence checks, (c) explicit residual issues, and (d) PASS / BLOCK decision before the next gate. Do not change immutable experiment artifacts, TEST policies or registration hashes.

## 8. Priority and contingency

**P0 — mandatory before revised KBS submission:** cross-protocol evidence ledger, new three-task Experimental Setup, frozen TEST decision results, changed contribution positioning, actual call rate fairness, negative Always Memory deployment evidence, complete supplement sync, final build and author declarations.

**P1 — materially improves novelty and quality:** inspect nearest accepted KBS works, tighten explanatory synthesis, build clear 6-Base robustness graphic, condense tables, independently check paper-level inferential claims and C2 mechanism boundaries.

**P2 — optional future experimental work, not a condition of current revision:** further candidate-composition controls or deployment/cost experiments; if undertaken, explicitly exploratory and separate from frozen Plan C. Do not conduct new TEST-guided threshold searches or post-hoc selection of favorable Base seeds to alter the primary acceptance claim.

**Key editorial decision:** On currently measured warmed M3 paths, Always Memory is both more accurate and faster than Utility. Therefore the strongest paper is **not** an optimal deployment/speedup claim. Preserve the call-constrained *decision-quality* finding as the estimand, state conditions when such calls represent a meaningful external scarce resource, and avoid presenting an unmeasured constraint as a production fact.

## 9. Official resources verified when planning

- Journal scope: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- KBS recent papers: https://www.sciencedirect.com/journal/knowledge-based-systems/vol/341/suppl/C ; https://doi.org/10.1016/j.knosys.2026.116236 ; https://doi.org/10.1016/j.knosys.2026.116167 ; https://doi.org/10.1016/j.knosys.2024.111446
- Elsevier manuscript AI use: https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals (updated June 2026).
- Elsevier Highlights guidance: https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript (June 2026).
- KBS journal-specific Guide for Authors: https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors (automated access failed with 403; author/submission portal verification required).

**Plan is nonauthoritative with respect to frozen scientific source files.** It becomes an execution guide only when the authors approve; no experiments or manuscript source files were edited in creating the plan.
