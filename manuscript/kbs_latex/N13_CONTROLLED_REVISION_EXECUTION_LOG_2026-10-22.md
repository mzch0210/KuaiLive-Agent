# N13 Controlled Manuscript Revision — execution log

**Branch:** `kbs-n13-controlled-manuscript-revision-20261022`  
**Base:** N12 commit `683dd7988d163fed49a6e3846f9317eec3e483e5`  
**Scope:** controlled editorial and narrative revision; no new scientific claims, no new TEST evaluation, no threshold/model selection.

## Phase 1 — first batch applied

- Replaced three undefined internal `H1` references in the main paper with reader-facing descriptions of the additional-target policy evaluation.
- Rewrote the supplement's opening access paragraph to remove internal host/plan/decision labels while retaining the actual availability boundary.
- Rewrote S1.6's opening paragraph to distinguish public code and aggregate records from unpublished event-level rankings, processed bundles and checkpoints.
- Preserved the original data-access constraints and the requirement for responsible-author approval of any future deposit or final data-availability statement.
- Scientific metrics, sample definitions, frozen policies, uncertainty estimates, and inference procedures were not changed.

## Phase 2 — narrative and package alignment in progress

- Revised the title to **Candidate-Aligned Knowledge Valuation for Selective Relationship Memory Routing in Live-Streaming Recommendation** and synchronized the supplement subtitle.
- Revised the first contribution bullet to state the precise comparator and estimand: original uncorrected sampled labels, full-candidate ranking, and population-weighted call fractions. It now explicitly says the DEV allocation trace is not an independent confirmation of the additional-target result.
- Updated the third Highlight to report population-weighted Memory-call fractions rather than a raw-count claim.
- Added the N13 branch to the existing frozen-source semantic/PDF QA workflow's branch filter. Run [#39708878897](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39708878897) was dispatched for the revised source and is pending at the time of this log update.
- The first semantic/PDF QA attempts exposed stale lexical guards that required the old undefined `H1` label in two checks. The main scientific contract, semantic audit and its unit-test fixture were updated to require the equivalent reader-facing policy-evaluation wording. These are terminology-alignment changes only; the matched-call caveat and DEV-versus-additional-target evidence boundary remain required.
- The title, abstract and contribution framing have not changed any numeric result or evidence tier.

## Phase 3 — W0/W1 completed; first W2 structural move applied

- Created `N13_W0_CLAIM_ROLE_AND_PARAGRAPH_MOVE_MATRIX_2026-10-22.md` and `N13_W1_ONE_PAGE_ARGUMENT_STORYBOARD_2026-10-22.md` before changing the Results structure. They lock the single thesis, section ownership, table/equation anchors, immutable metric set and the non-causal RQ3 branch.
- Applied the first W2 Results-first move: the 47,575-event M3 Always-Memory-versus-Base paragraph was removed from RQ1, where it interrupted the Twitch-to-room candidate-regime argument, and placed at the start of the cross-task frozen-selection subsection as the unconstrained specialist quality ceiling. The numeric values are unchanged; the paragraph now provides direct context for the selective-policy results.
- The source change is structural and interpretive only. No training, threshold tuning, target reveal, TEST re-evaluation, or scientific re-estimation was performed.
- New main-source blob: `2c4ce5e20a3948f2699613e52d005d4edd9396ec`. Final C7/C8V and dual-PDF verification is pending for this source.

## Phase 4 — W2 Results narrative pass applied

- Rewrote the Results opening to preview the evidence order and the distinct role of the DEV allocation analysis.
- Tightened the primary H1 prose so the comparator definition is stated once before the result; the numerical effect/CI/Holm values remain unchanged. Consolidated realized call counts, weighted call fractions, the 1.337/1.797pp gaps and the complete-policy interpretation in one adjacent paragraph rather than repeating the same caveat across two paragraphs.
- Reframed the DEV allocation subsection as descriptive accounting and clarified that its switch partition does not causally decompose H1. Added a short transition to the established frozen-selection comparisons.
- No result cells, cohorts, statistical inference, or scientific claims were newly estimated. Main source blob after this pass: `1aa1a6112d50dc095747db67da2cbc2dd7765a00`. Full source contract and dual-PDF verification pending for this exact source.

## Phase 5 — frozen-guard wording alignment

- The first W2 CI run on source `1aa1a6112d50dc095747db67da2cbc2dd7765a00` correctly stopped at the frozen scientific guard because the consolidated H1 caveat no longer contained the guard's required phrase `not an experimentally isolated equal-resource`. The underlying meaning had been retained, but the wording guard is an explicit non-negotiable invariant. The sentence was restored to the guard-compatible wording without changing its meaning or any result value.
- Current `main.tex` blob: `96c090b78de9d48331029def3c7ca52c4e5c4453`. The currently visible workflow run was dispatched against the immediately preceding commit, so it does **not yet verify** this corrected blob; a successful run on the exact current source is still required before this phase can be marked accepted.

## Phase 6 — W3 framework / design responsibility pass applied

- Created N13_W3_FRAMEWORK_EXPERIMENTAL_DESIGN_RESPONSIBILITY_AUDIT_2026-10-22.md to lock section ownership before the edits.
- Framework now owns the conceptual definition of pretarget Z and the target-leakage contract; Experimental Design retains the task-specific feature schema but no longer repeats the full target-exclusion list. The Base/Memory model definition remains in the framework; Design names the M3 model families and seeds without repeating the entire Base/Memory description. The endpoint subsection retains NDCG@10, HR@10, realized call fraction and paired/user-level inference while removing a duplicate sentence about retrospective state assignment.
- Restored the exact frozen audit phrase “event decisions disagree” in the DEV allocation paragraph; counts and descriptive/non-causal interpretation remain unchanged.
- Current main-source blob after W3: 21c45169fc5d638ee3f980963e371841150bd0fe. This exact source still requires a successful C7/C8V, cross-source and dual-PDF run.

## Phase 7 — W4/W5 discussion and conclusion alignment (2026-10-22)

- Interpreted candidate-indexed value and the prior-art gap without reciting all frozen result tables; the known component-by-candidate-regime interaction is noted as DEV evidence, not a new causal result.
- Strengthened RQ2 interpretation as prioritization among valuable Memory calls, with unchanged DEV counts and a clear separation from H1 causal mediation.
- Concentrated H2 composite-source interpretation, incomplete prereveal TRAIN-only Popularity check, same-period cohort, corrected-S method-admission limit, Always Memory accuracy advantage and unfavorable legacy cost timing in the validity section.
- Conclusion now states the bounded knowledge-use decision contract and avoids a repeated result/limitation list.
- Main-source scientific semantics: no frozen results, formula bodies, method parameters, or TEST evaluations changed. Main blob after W4/W5: `434349de841af37194e5f16e0672738d019905bf`.
- Technical CI verification of this source **pending**; reviewer/legal/author publication gates remain open.

## Remaining phases

1. Continue W2: revise Results opening and section bridges so each subsection follows question → design/comparator → result → interpretation → transition; then align Experimental Design and framework responsibilities in W3.
2. Clarify the Always-Memory comparison, candidate-regime/knowledge-component interaction, and the distinction between ranking quality, call fractions, local kernel timing and unmeasured production costs.
3. Deduplicate the supplement only after claim-to-source mapping; preserve unique audit trails and explicitly retain the unverified pre-reveal popularity-margin condition.
4. Rebuild and verify main/supplement PDFs and the scientific source guards on the final changed source SHA.
5. Keep author-owned rights, declarations and journal submission decisions pending until the responsible author verifies them.

## Non-negotiable evidence boundaries

- The 30,000 additional targets are from the same recording period, not a future-period replication.
- Full-candidate supervision is compared with the original uncorrected sampled-label policy; no valid corrected-S policy was trained and evaluated.
- The F-aligned policy's lower realized call fractions do not establish lower end-to-end latency or deployment cost.
- The nested 4,096-target historical-null comparison retains the unverified pre-reveal TRAIN-only Popularity-margin condition; do not rewrite it as a completed preregistered check.

## W6 supplement editorial pass (2026-10-23)

- Verified C8V run [#39882720702](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39882720702) on commit `71ca2770ea415d580074d0d89ee872449a2ede8f`: both main-paper and complete-supplement jobs SUCCESS. This is the pre-W6 accepted source baseline.
- Supplement S1.5–S1.6 now state actual provenance and restricted derivative availability without instructions to authors or unapproved promises of permanent public deposits.
- Supplement S2.4 uses a neutral restricted-storage description in place of a named internal host while retaining sealed ranking and one-shot label reveal provenance.
- Supplement S3.3, S5.7 and S6.1 replace infrastructure troubleshooting narratives with the scientifically relevant result lineage and exclusion/canonical-source status, preserving citations and quantitative discrepancy details in S6.6.
- The entire S10 source section was compared as an identical source substring before committing: **no S10.1–S10.19 values, table cells, titles or historical-source acceptance statements were changed**. No new experiment was run.
- Source after W6: supplement blob `778fa2cf8e584ffea83e2b56ccba4f6278455172`; commit `2b1620e3fc2b9f998209cc09cf6cc15ef3fe4be1`.
- Current W6 workflow: [#39883705990](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39883705990); its final status must be checked before treating W6 as CI-accepted.
- W7 abstract and conclusion were compared against the W0/W1 storyboard: the 30k same-period policy result is central; weighted invocation, 50,049 DEV switch denominator, nested 4,096 historical-source study and the original uncorrected sampled comparator are all already identified. No additional abstract rewrite is warranted solely for wording variation.
- Remaining: source-to-provenance mapping before any further supplement deduplication, complete final PDF review, and author-owned data rights, declarations and submission approval.

## W6 source-aware dedup and W8 verified PDF review (2026-10-23)

- Committed [W6 deduplication decision matrix](N13_W6_SUPPLEMENT_DEDUPLICATION_DECISION_MATRIX_2026-10-23.md). Exact checkpoint-fingerprint repeats (S2.2/S8.3) were documented, not removed, because a safe complete S8 table renumber and cross-reference update was not needed for the narrow editorial scope. S7.7 versus S10.7 are distinct nested estimator protocols; S9.6 versus S10.17 differ in repetition/order/source accounting; S10.19 remains a frozen full-cell evidence repository.
- CI [#39883705990](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39883705990) SUCCESS for both main-paper and complete-supplement on source commit `2b1620e3fc2b9f998209cc09cf6cc15ef3fe4be1`. Both artifacts were downloaded and actual PDF bytes inspected. No paper or supplement content was changed since that science-PDF-tested commit; subsequent commits only added project tracking/decision documents.
- Main PDF SHA256: `325d2b08ad599a5fc5354ec513d4bf87f5daa92d9b3faeeaea70ba2a0798ab4d`, 36 pages; title `Candidate-Aligned Knowledge Valuation for Selective Relationship Memory Routing in Live-Streaming Recommendation`.
- Supplement PDF SHA256: `82bc6e0e5e3e62bfa4415562864089f7e3e805b5f2bf7d0b7dea4620ded0b272`, 47 pages; same subtitle. Actual PDF first pages were rendered for visual inspection; title synchronization and key content text extraction succeeded. The PDF still displays `Anonymous Authors` and a supplement frontmatter date of 21 October 2026; these are not assertions of author approval or current manuscript date.
- Source fields remain: main blob `1467c5ae4fbda0135e822b00be0f7741c5129498`; Supplement blob `778fa2cf8e584ffea83e2b56ccba4f6278455172`. This is a verified same-content build, though the PR branch head has subsequently moved due to documentation-only commits.
- Author-only gates remain **PENDING**: data rights, actual AI use and tool-specific disclosures, named CRediT/author list, funding, ethics, conflict of interest, anonymization according to the official KBS Guide, stable deposit and final GO/HOLD/REDIRECT. Do not call this submission-compliant before approval. There was no PR merge or journal submission.
