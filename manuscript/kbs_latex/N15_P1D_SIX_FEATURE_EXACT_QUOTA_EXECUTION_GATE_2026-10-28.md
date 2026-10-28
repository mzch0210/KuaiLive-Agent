# N15 P1-D — Six-feature exact-quota Full-vs-Long source interaction

**Date:** 2026-10-28  
**Status at commit:** USER CONFIRMATION RECORDED; protocol frozen; public synthetic QA is triggered by the new workflow; private self-hosted run is triggered only after public preflight passes. No empirical P1-D result is claimed in this record until a successful run and aggregate audit are verified.

## 1. Authorization scope

The user explicitly confirmed “确认数据可以使用” on 2026-10-28. The rights register records this as project-level confirmation to proceed with the narrow internal diagnostic, not as an independent legal opinion or proof that all upstream licenses match.

The official KuaiLive project page identifies CC BY-NC-SA 4.0; a secondary dataset hosting page has shown different metadata. The exact upstream terms and public redistribution permissions remain author-side checks. This experiment does not redistribute data or private derived files.

## 2. Frozen one-shot protocol

- **Only quota:** q=0.30; no q=.10/.20/.40 runs.
- **Source arms:** Full Memory and Long-only Memory.
- **Feature panel:** exactly six existing descriptors: candidate count plus the five frozen Base-score descriptors. This is not a literal no-history panel because Base scores may encode user history.
- **Population:** certified B1/B2 reused DEV, 50,049 events / 12,628 users; exact source hashes, roster, user assignments and shared columns must pass existing gates.
- **Folds:** the existing five user-disjoint outer folds; same frozen HGB capacity, same label-blind stable tie rule, same exact per-fold top-k quotas.
- **Outcome scale:** both F- and S-supervised policies are evaluated on the same source-specific full-active F incremental value. S labels are the original target-retained labels and remain offline-only.
- **Primary estimand:** D_s(0.30) = full-F NDCG of F-supervised policy minus full-F NDCG of S-supervised policy for source s; I(0.30) = D_Full − D_LongOnly.
- **Uncertainty:** paired user-cluster bootstrap interval, descriptive only. No confirmatory p-value or independent-replication claim.
- **Output:** aggregate-only JSON on the self-host; no row/user/event identifiers, per-event scores, checkpoints, model weights or private CSVs uploaded.
- **Forbidden:** TEST/G5/B4-A access, model retraining, extra source arms, quota expansion, post-outcome feature search, or public release of private data.

## 3. Provenance and gate conditions

The workflow requires public syntax/synthetic tests to pass first. On the self-host it must validate B1/B2 manifest schemas, exact frozen B1 SHA, B2 CSV SHA, 50,049-event/12,628-user roster, DEV-only split, identical event/user assignment, parity of the existing shared Base/Full outcomes and features, and absence of TEST access. It aborts on any mismatch.

The workflow is deliberately limited to a single q=.30 diagnostic. P1-D is exploratory reused-DEV analysis, not a new independent test. A successful CI run demonstrates execution and protocol invariants, not legal adjudication or KBS acceptance.

## 4. License boundary

Public-source license declarations differ across hosting surfaces. The user’s project-level confirmation permits this narrow internal run for the current project, but does not itself establish the right to redistribute upstream data or every private derived artifact. Public release of source rows, identifiers, model weights, or private-derived artifacts remains prohibited absent separate rights verification.

## 5. Decision rules

- If source hashes, roster, or parity fail: stop; record NOT_IDENTIFIABLE_FROM_AVAILABLE_ARTIFACT.
- If public synthetic preflight fails: do not run private data.
- If the private run succeeds: interpret I only as conditional descriptive evidence under this six-feature panel and q=.30.
- If I weakens, crosses zero descriptively, or reverses relative to P1-B: narrow the manuscript claim; do not search more panels.
- P3 independent confirmation and KBS submission remain HOLD until separate criteria are met.
