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
