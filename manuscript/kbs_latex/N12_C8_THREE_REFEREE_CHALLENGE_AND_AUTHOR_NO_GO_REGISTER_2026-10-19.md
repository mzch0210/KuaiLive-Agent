# N12-C8 | Adversarial KBS Editor / Methods / Knowledge-Deployment Referee Simulation

Date: 2026-10-19. **Independent-role critique simulation completed; NOT a real external peer review or editorial decision. C8 overall NOT PASS pending substantive owner signoff and unresolved rights.** Working draft PR #6. Paper C7 verified run #39205375045: 36p/47p, 17 rows/49 numeric cells and 11-table sources matched. No new TEST rows, estimates or model fits used.

## Referee 1 — KBS associate editor: significance, coherence, originality

**Editorial assessment: Major Revision/Contribution risk unresolved.** Article title and one-thesis argument are clearer after C6: the candidate universe matters for knowledge-value *supervision*, not just for sampling metrics. The reviewer can identify RQ1 premise, RQ2 main result, and parallel RQ3 source control. Yet this still risks appearing as a direct consequence of established sampled rank evaluation inconsistency (Krichene and Rendle 2020) plus conditional experts (Mao, Mohri and Zhong 2024).

**Major E1 (P0). Where is the principle not already supplied by earlier work?** Candidate-aligned labels produce better target-environment policies; this may be unsurprising train/test matching. The manuscript needs to say precisely what the historical knowledge-decision setting reveals beyond demonstrating well-known off-policy sampling bias: two distinct rankers fixed, scalar knowledge-value label indexed to candidate regime, then actual specialist allocations differ on identifiable events. The DEV switching and 30k frozen H1 are credible yet not a generalizable theorem; the claim must remain empirical and bounded. **Partial response already in** Introduction contribution bullets; Discussion `What Is New About Candidate-Indexed Knowledge Value?`; RQ2 Results. **Not resolved** unless external editorial judgement finds this knowledge-system advance substantial.

**Major E2 (P0). What is the knowledge system?** The fixed 0.45 Short+0.45 Long+0.10 Popularity scorer is transparent but ordinary history counting, not semantic knowledge graph inference. Source validity under a strong constrained historical null argues history carries information; it does not prove relationship identity as a unique higher-order knowledge mechanism. **Partial response:** Method fixed source definition, RQ3 Results and Discussion explicit non-semantic/composite caveat. **Residual:** knowledge-science advance may be narrower than top-of-KBS expectation.

**Major E3 (P1). What does this tell designers?** Decision-target alignment is a potentially transferable evaluation contract, conditional on actual candidates and access quota. But no real external access scarcity is measured; Always Memory is a superior unconditional accuracy reference. **Response:** §5.4 and Discussion operational conditions openly report adverse accuracy and timing. **Residual:** practical significance depends on independently demonstrating access constraints in deployment.

**Editorial stance:** no automatic rejection can be inferred; no automatic 'KBS-ready' conclusion either. **Go only for a bounded empirical evaluation paper, after author accepts P0 novelty risk**, unless independent new evidence is authorized.

## Referee 2 — Statistical / causal methods

**Assessment: Major Revision on identification, despite strong audit trail.**

**Major M1 (P0). F/S supervisor comparisons are not isolated equal-budget effects.** 30k frozen SAS F/S 8704/9105 (1.337pp difference), GRU 8629/9168 (1.797pp). Original approximately 1pp tolerance missed. Different thresholds and observed calls make total frozen-policy effects valid but label-only equal-cost causality unproved. **Partial response:** §5.2 Table H1 caption and Discussion. **Decision:** ACCEPT BOUNDED; REJECT strict same-budget causal claim; no threshold reset on revealed TEST.

**Major M2 (P0). History-null prereveal acceptance incomplete.** The 4096 same-cohort TRAIN-only popularity nondegeneracy floor was NOT VERIFIED before label revelation. Three seeded nulls share one cohort; rewiring ~76.8% links breaks multiple structural elements. **Partial response:** §4 evidence design, §5.3 table and Discussion; **cannot retrospectively repair original acceptance**. The original prespecification failure may justify downgrade of source-validity strength.

**Major M3 (P1). Independence/time/precision labels.** 30k new event IDs collected in same March 2026 interval, overlaps original users/histories, nested 4096 subset, six trained incumbents evaluated on same original 47,575 test; 20-cell eligible-weighted estimand distinct from raw call counts. User bootstrap and Holm family should remain separate. **Partial response:** §4 design, Table H1 footnote, §5.2/5.3/6. Original CI source unchanged under 49-cell + table freeze auditor.

**Major M4 (P1). Label visibility and offline measurement.** Sampled S target-retained candidate design is retrospective offline supervision only; ranking with one observed positive affected by exposure/logging policy. No causal online A/B or IPS protocol is identified. **Response:** §3 pretarget separation, §4 and §6 offline limits.

**Methods verdict:** empirical associations and frozen-policy outcomes are credible within the stated setting; fully identified strict budget, real-time outcomes and individual relation causality are **not** supported. Do not overclaim.

## Referee 3 — Knowledge-system / deployment reviewer

**Assessment: Major Revision; demonstration of usefulness under a real deployment constraint still missing.**

**Major S1 (P0). Why use a gate at all on M3?** Always Memory 0.348744 on additional target cohort > SAS F policy .305446 / GRU F .304530. Original pointwise Utility DEV 1.769 ms > Always Memory .692 ms. Calling Memory less frequently can increase computation because Base/feature/gate overhead still runs. Old timings are not new vectorized F gate, but there is no positive total cost proof. **Response:** §5.4 and §6.3 make the limitation explicit. **Unresolved if manuscript claims actual production efficiency**; after C6 it should not.

**Major S2 (P1). Is source specificity evidenced?** RQ3 real history null versus constrained null confirms information in original arrangement under fixed present candidates, but changing repeated pairs plus higher-order structures cannot isolate a semantic cause. DEV B2 Long-only larger transfer regret than Full mixture; Short-only penalty co-occurs with massive realized call-rate change; weak popularity/placebo may have floor. **Response:** source definitions/DEV supplementary, §6.2/6.3. No monotonic 'more relationship knowledge -> larger regime effect'.

**Major S3 (P0 compliance). Can an outside lab repeat the study from provided repo?** The public source, exact result table cells and PDF builds can be reproduced; private raw per-event test targets, certain data/model caches and release rights are not proven public, so original frozen H1/H2 uncertainty estimates cannot presently be recomputed by arbitrary outsiders. Need a bounded data/code availability statement and proven training/inference information-contract documentation. **Response:** C7 claim rights register; **rights/owner permission pending**, so this is a submission blocker.

**Systems verdict:** knowledge-value evaluation contribution may be publishable as a scoped empirical study, but does not establish online throughput/cost advantage.

## Major-comment resolution matrix

| Comment | Priority | Existing evidence or manuscript location | Disposition |
| --- | --- | --- | --- |
| E1: novelty beyond generic deferral/sampled metric | P0 | Intro §1 bullets; Related Work §2; Discussion §6.1; C6 novelty matrix | **OPEN — author risk acceptance / editorial judgment** |
| E2: relation knowledge is frequency-based | P0 | Method §3; RQ3 §5.3; §6.1/6.3 | **NARROWED, unresolved uniqueness** |
| E3: actual external access scarcity | P1 | §5.4; §6.3; negative timing | **OPEN; scope limited** |
| M1: H1 F/S call imbalance | P0 | §4.5; §5.2 H1; §6.2 | **DISCLOSED; strict causal claim disallowed** |
| M2: H2 prereveal floor and composite null | P0 | §4.5; §5.3 H2; §6.3 | **DISCLOSED; missing control cannot be backfilled** |
| M3: same-period sample and dependencies | P1 | §4 evidence hierarchy; §5.2–5.3 | **DISCLOSED** |
| M4: target-retained S/observational logging | P1 | §3/§4 pretarget contract; §6.3 | **DISCLOSED; no online causal claim** |
| S1: Always Memory accuracy and timing | P0 | §5.4; §6.3 | **DISCLOSED; positive cost claim removed** |
| S2: relation source×supervision specificity | P1 | DEV B2; §6.2–6.3 | **NARROWED; true causal interaction unproved** |
| S3: reproducibility/license/privacy | P0 | C7 data-rights register and reproducibility tiers | **OPEN — human/data owner verification required** |

## Human author and submission decision gate (NO-GO until resolved)

The simulated three-referee review is a stress test, **not** the three external journal referees and not permission to submit. Required recorded confirmations:

- Authorship: remove `Anonymous Authors` placeholder in appropriate submission route; all real authors personally confirm membership/order, CRediT, corresponding author, funding, COI, ethical research and cover-letter assertions.
- Data: actual original KuaiLive release+M3 exact version and license owner; confirm redistribution, research/derivative rights, private identifiers, event logs and trained weights; identify which public results truly independently replicable.
- Elsevier updated 2026 policy: ChatGPT-assisted substantial scientific text organization/revision must be accurately declared by humans with tool/purpose/responsibility immediately prior to refs; research-method AI use, if any, requires reproducible Methods description. This record **does not itself insert author-affirmed AI declaration into the manuscript**. https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals
- Journal KBS live submission guide (word limits/artwork/preprint/ethics/Highlights) verified at submission; no invented policy limit. Author personally examines final 36p/47p PDF and C7 row-cell provenance.
- Major E1/E2/S1 + M1/M2 remain science tradeoffs. Human decision branches: **BOUNDED SUBMISSION** (accept editorial novelty risk), **NARROW AND REVISE**, or **AUTHORIZE NEW INDEPENDENT SCIENTIFIC EVIDENCE** (with separately locked new data, no retrospective TEST tuning). The assistant cannot sign any author or data-owner decision.

**Stage decision:** C8 technical reviewer simulation **COMPLETE**; C8 overall **BLOCKED_PENDING_HUMAN_CONFIRMATION_AND_EDITORIAL_GO_NO_GO**. Draft PR #6 remains DRAFT; not merge/submit.
