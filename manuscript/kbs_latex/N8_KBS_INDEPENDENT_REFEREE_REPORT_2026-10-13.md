# N8 — KBS independent-perspective referee-style assessment

**13 October 2026 | Manuscript:** *When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation*.

**Decision: SCIENTIFICALLY COHERENT AFTER N0–N7; SUBMISSION READINESS = HOLD.** This is an internally generated editor/method/reproducibility review from three perspectives, **not three independent human referees**, a journal editorial decision, or a probability of acceptance.

## 1. Editor perspective: fit, thesis and contribution

**Journal fit — adequate.** The publisher identifies recommender systems, knowledge presentation and intelligent decision-support systems within KBS's scope and calls for original innovative research and a theory/practice balance: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 .

**Single-paper thesis — PASS.** §§1–8 now progress from *fixed relationship-knowledge value conditional on an incumbent and ranking candidate regime* to *predicted marginal value guiding the selection of that knowledge*, followed by the candidate-regime diagnostic and empirically observed resource boundary. Abstract, Results and Conclusion retain the same thesis and three nonexchangeable experiment roles.

**E1 (MAJOR; novelty, PARTIAL).** Generic conditional expert selection has a strong literature precedent. Mozannar & Sontag (ICML 2020) and Narasimhan et al. (NeurIPS 2022) cover expert deferral and post-hoc selectors. Mao et al., *Regression with Multi-Expert Deferral* (ICML 2024, https://proceedings.mlr.press/v235/mao24d.html) establish two-stage and single-stage regression deferral with consistency analysis. DS-Frame (arXiv:2609.02671; accepted CIKM 2026) studies adaptive fast/slow sequential recommendation under compute budgets. Existing knowledge gating and sampled metric sensitivity also precede this manuscript. **N5 correctly narrowed the novelty** to the domain-specific measurement of a fixed transparent relationship specialist's incumbent-/candidate-relative event ranking utility and its frozen selection tests. The editor must still judge whether this empirical methodological contribution is sufficiently original for KBS. **Do not add "new universal selector", "first budget-aware routing", full-L2D head-to-head or SOTA claims.**

**E2 (MAJOR; absolute deployment advantage, PENDING EXTERNAL EVIDENCE).** In M3 the unconstrained Always Memory ranker obtains NDCG@10 0.34679, exceeding Utility 0.30177–0.30400 across six fits, and its warmed DEV path is faster (0.803 ms vs 1.802 ms for the Utility route on 256 events). The paper reports this adverse result in the Abstract, §6 and §7 and does not claim lower total latency. **Under actual observed quality and warmed scoring conditions, unconditional Memory is preferable; the invocation-count constraint is stipulated, not economically validated.** Either maintain bounded conditional decision-quality positioning or measure a real independently justified access/pricing/latency constraint before advancing deployment claims.

**E3 (MINOR; readability, PASS).** Main article has eight sections, three aligned contribution components, two meaningful figures, nine distinct-purpose tables, and no arbitrary fourth confirmatory study. N7 removed twelve specific redundant passages without suppressing inferential boundaries.

## 2. Methods referee perspective: comparison, inference, leakage

**M1 (MAJOR; comparator strength, PARTIAL).** Designated SASRec/GRU4Rec/LiveRec and room Dual-ID Base rankings are appropriate defined *incumbents*, but auxiliary model studies have different data, tuning budgets and tasks. The manuscript cannot claim dominance over CKLF, MHGFCL, KAPER, GUIDER, full DS-Frame or stronger general expert-defer methods. S3 makes Base competitiveness transparent but does not supply identical-data, resource-matched SOTA comparisons. New DEV Direct-vs-Two-stage regression sensitivity is useful only as a bounded *post-G5 exploratory estimator comparison*.

**M2 (MAJOR; budget fairness, SCIENTIFIC SCOPE VERIFIED).** Five M3 selection objectives share the original <=30% **DEV** threshold calibration but do not share identical **TEST** Memory-call rates. The primary SASRec Utility has 29.21% TEST calls, versus Uncertainty 30.18% and History 35.47%; the six-fit Utility range is 27.72–29.21%. Utility's two-axis measured dominance over those four specified objectives is reportable, but never as a perfectly same-call online budget evaluation or production cost reduction. Twitch's equal-count Difficulty reference is retrospectively TEST-ranked, not a second DEV-frozen deployable policy.

**M3 (MAJOR; statistical family, VERIFIED WITH SCOPE).** Six M3 Base fits share the same 47,575 TEST events and 12,533 users. The original three predeclared contrasts (Utility vs Base, Difficulty, Specialist Quality) are Holm-corrected **within each** Base fit; inference does not correct the full 18 pooled contrasts or include the stronger Uncertainty proxy in that primary family. User-cluster resampling and paired statistics condition on the fixed cohort, rankers and policies. The six fitted models are not independent cohorts.

**M4 (MAJOR; chronological leakage, SOURCE-PROTOCOL VERIFIED).** M3 earlier observed TEST-period interactions may enter later histories prequentially; current and future targets may not enter decision features, candidate eligibility, thresholds or model scores. Source S1–S2 records actual timestamp-type hash/tie conventions and why original G0F notation differs from locked executable sampling. This is a protocol/source review, not a new raw-event audit.

**M5 (MAJOR; candidate causal identification, SCIENTIFIC SCOPE VERIFIED).** Original KuaiLive paired 10,222 room-ranking events are retrospective and already inspected, not a new independent M3 TEST; crossed 2×2 candidate-membership and score-reference accounting is descriptive. Membership bundles candidate number, identity and competition, and cannot identify the pure causal effect of candidate count. Krichene and Rendle already established sampled-ranking metric hazards; the contribution is a specific implication for the fixed Memory-minus-Base utility *label*.

**M6 (MINOR; post-G5 exploratory baseline, PASS WITH LABEL).** S7.7 reports Direct and Two-stage nested DEV on 50,049 events/12,628 users in SASRec/GRU4Rec primary seed. SASRec Direct difference +0.001352 (paired user CI [+0.000422,+0.002198]) uses **287 more Memory calls**; GRU4Rec +0.000051 interval crosses zero. The two methods target the same conditional expectation and this analysis does not establish a new deferral objective, a deployment saving or an extra confirmatory G5 TEST. The original S8 inference family is unchanged.

## 3. Writing and reproducibility referee perspective

**R1 (P0; permanent archives and rights, OPEN).** Public upstream dataset references, model code and GitHub Action history are not equivalent to a durable authorized replication package. Private M3 processed event rows, checkpoint weights and G5 TEST labels have not been independently verified as lawfully redistributable; expiring GitHub artifacts are not DOIs. Authors must determine dataset licencing, anonymization/consent/permissions, public versioned code, accessible source-level manifests and lawful access routes. The data-availability statement must disclose the actual restriction and not invent an archive.

**R2 (P0; author-controlled declarations, OPEN).** Main PDF still contains "Anonymous Authors" and no author-verified affiliations or final CRediT/funding/competing-interest statements. The manuscript underwent substantive AI-assisted rewriting, not only grammar checks. Under Elsevier's updated June/August 2026 policy, a separate generative-AI preparation declaration must identify the tool, purpose and author oversight and be placed before references; human authors must personally review/approve it. Do not falsely assert that this review has occurred. Official policy: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals .

**R3 (P1; KBS portal, HOLD).** The official KBS Guide for Authors URL is currently inaccessible to automated fetching (403). The official Elsevier Highlights help specifies 3–5, <=85-character bullets; exact KBS-specific compulsory files, anonymization, word-count, data statement and declarations must be verified by the corresponding author inside the live submission portal, rather than assumed from general Elsevier rules.

**R4 (P1; PDF typesetting, MINOR ISSUES).** A 31-page exact N7 main-PDF from Actions #38344272685 has zero page-exterior text bounding blocks, no unresolved references or missing citations, and one nonfatal 3.47-point overfull hbox. The integrated 34-page supplement from the first #38356747448 build includes S7.7/Table S7.5 on page 23 and has no overfull hbox/vbox; some landscape tables create sparse adjacent pages. See the N8 source/PDF QA for exact hashes and the superseding dated final build. This establishes visual/page-level technical review, not acceptance of every stylistic journal rule.

## 4. Response to core KBS review questions

| Likely question | Present evidence-supported response | Residual severity |
|---|---|---|
| What new idea beyond L2D? | Candidate-aligned evaluation of fixed relationship specialist's relative ranking value and its two separate TEST-frozen selection validations | MAJOR / editorial originality judgment |
| Why route if Always Memory is better and faster? | Allocation performance is evaluated under a **stipulated** specialist-call constraint; there is **no claim** of operational advantage | MAJOR if positioned as practical deployment |
| Are all six fitted models independent? | No: same 12,533 TEST users and event cohort, model initialization changes only | Scientifically controlled |
| Is KuaiLive sign reversal novel metric theory? | No: descriptive paired candidate-regime consequence for the expert-value target, consistent with known sampled metric risk | Scientifically controlled |
| Are Direct and Two-stage compared fairly? | Same features and nested DEV; unequal realized calls; post-G5 exploratory only | Restricted exploratory comparison |
| Can reviewers reproduce everything publicly? | Not yet; public source and aggregate evidence exists, but full licensed, durable derived-data/model archive does not | P0 author action |

## 5. Stage gate

**N8 scientific-consistency audit: PASS WITH MAJOR RESIDUAL RISKS. N8 full KBS SUBMISSION READY: HOLD.**

The two research-level residual concerns are (a) editorial valuation of a primarily empirical knowledge-utility contribution against existing deferral/gating literature and (b) an economically unvalidated specialist-call constraint. They are adequately *bounded in wording* but not experimentally solved. The hard final delivery blockers are (c) source rights/data archive, (d) author declarations and sign-off, and (e) KBS portal-specific requirements. No future independent TEST or external peer review has been manufactured.

A separate N8 source/claim audit and author checklist govern final closure.
