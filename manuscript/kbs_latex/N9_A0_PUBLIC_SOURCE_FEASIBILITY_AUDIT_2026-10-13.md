# N9-A0 | Public source, private-cache and fair-comparison feasibility audit
Date: 2026-10-13. **Status: SOURCE/CODE STATIC AUDIT COMPLETE; PRIVATE RUNNER ATTESTATION PENDING.** No workflows launched, no GPU or private labels accessed.

## 1. Repository source checks performed
- Read `analysis/kbs_plan_c/b1_full_dev_candidate_labels.py`, `b1_nested_regime_transfer_dev.py`, `b2_nested_knowledge_specificity_dev.py`, `frozen_gate.py`, `.github/workflows/kbs-b2-inline-offline-nested-dev.yml`, B1/B2 experiment report and private-source attestation metadata.
- B1 source-construction code writes `dev_pair_candidate_labels.csv`, containing the corrected F source rows and appended **sampled_memory_ndcg10, sampled_sasrec_ndcg10, sampled_gru4rec_ndcg10, b1_sampled_candidate_count**. It checks source/event order, digest and DEV identity before generating the 575 target-retained S labels.
- B1 nested runner checks `summary.json` schema, row count 50,049, DEV-only, exactly 12,628 users and exact per-event source SHA, and uses GroupKFold 5 outer / 4 inner. It calculates F and S base and specialist per-event utility. Its public outputs do not contain private identities.
- B2 nested source code checks parity of full Memory F and sampled S scores, source CSV SHA256, events and users; production log of successful fallback job reports rehash before fitting. Private `dev_memory_source_ablation_pairs.csv` remains on the private self-host. Its manifest and `B2_NESTED_DEV_SOURCE_SPECIFICITY_AGGREGATE_2026-10-13.json` provide public aggregate result provenance.
- Public scripts and aggregate proof allow protocol and source-contract review, **not independent present-turn byte-verification of the private event source**, nor proof that all per-candidate ranker scores are cached.

## 2. Existing private artifacts: source contracts, not independently accessed files
| Desired data | Where code says it should reside | Publicly established | Outstanding gate |
| --- | --- | --- | --- |
| Original corrected M3 DEV F event utility | `klm3_g3_dev_fullactive_base_memory_corrected_v1/dev_full_active_pairs.csv` | Prior run source SHA reported; B1 code validates | Rehash on private runner before new analysis |
| B1 paired DEV F/S event rows | B1 `dev_pair_candidate_labels.csv` + `summary.json` | 50,049 rows and SHA `37a43cb7622c708c6b1c87c3e916b0058275792654465a7b329ce2bac44bceea` reported | Verify full file on private runner; no identity export |
| B2 five-source F/S event rows | `$HOME/.cache/kuailive-agent-kbs/klm3_b2_full_dev_memory_source_ablation_seed20261013_v1/` | Successful nested run had on-run hash gate | Rehash before any further fit; verify raw ranker score caches separately |
| B2 full nested outputs | `$HOME/.cache/kuailive-agent-kbs/klm3_b2_nested_knowledge_specificity_seed20261013_v1/summary.json` | Public aggregate schema and run ID 38369503457 | Source↔summary digest check before reuse |
| Actual per-candidate Base and Memory scores for score-fusion A2 | Not demonstrated by B1/B2 **event-level NDCG rows** | **UNVERIFIED** | Find private exact-roster logits/cache, otherwise limited DEV-only rescore; A2 fusion HOLD |

## 3. A1 and A2 go/no-go rules, relative to frozen decision-support thesis
- **A1 conditional GO** if private B1/B2 per-event F utilities, 12 pre-outcome features, user groups and source hashes pass. A nested user-disjoint analysis can derive the quality–call frontier without new Base training. Its purpose is robustness and interpretability of *decision support*, not forcing superiority to Always Memory.
- **A2 direct relative-value and two-stage comparison** can use event-level utilities if private source is attested, but ensure matching fold, model capacity and full evaluation candidate regime.
- **A2 raw score/rank fusion HOLD** until **per-candidate** Base/Memory score vectors, candidate IDs and event-time eligible roster are actually found or exact-scoring is recreated DEV-only. A scalar event-level NDCG is insufficient to compute a fused ranking. The source contract does not establish such full scores.
- **Knowledge-source placebo/feature controls**: same source/user folds, equal model capacity, report actual calls and guard against popularity/placebo zero-call floors and Short-only drift. Do not present source interaction as a causal relation-specific theorem.
- **T0/T1**: no fresh TEST may be opened without metadata-only lawful unexposed cohort and a frozen protocol.

## 4. Efficiency and reproducibility safeguards
- Reuse B1/B2 cached historical scan + candidate roster; avoid re-downloading data or recomputing all 50,049 events unless hashes/required score arrays demand it.
- If rescore is necessary, perform one time-ordered history/roster scan, large-batch GPU inference, identical eligibility, FP32/tie rules and corrected all-prior Memory. Separately report CPU scan, GPU scoring, overall wall time and numerical parity; low GPU utilization alone is not failure (existing B1 reported 113.08 s overall but ~0.50 s for sampled GPU ranking).
- Never upload row-level user/event IDs, target labels or full private scores. Report only safe aggregates and manifest digests.

## 5. Exact follow-on
1. Use an authorized privacy-safe self-host runner to check source directories, sha256, model and roster score caches, user-group/event counts. Output **boolean/source digests/counter summaries only**, without event labels.
2. If checks pass, lock A1 decisions and prepare nested DEV-only execution; otherwise A1 remains HOLD, rather than pretending the environment is ready.
3. If raw per-candidate score caches absent, make a separate bounded feasibility/cost decision before A2 fusion. No expensive GPU job was authorized or executed during this static audit.

GitHub documents provide prior-run evidence, not fresh personal access to the runner. This audit is not a re-execution of B1/B2 or G5.
