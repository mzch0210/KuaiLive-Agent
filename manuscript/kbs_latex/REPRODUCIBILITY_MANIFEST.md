# KBS Reproducibility Manifest — versioned index (2026-10-21)

**Purpose.** A navigation layer for existing science, freeze and permission evidence. This is **not** a second claim ledger, a new experiment, legal authorization, a deposit DOI, or a statement that private TEST event-level data are publicly available. Do not interpret dates or status in historical reports as current unless superseded here.

## Source of truth and review state

- Current manuscript title: *Candidate-Regime Supervision for Selective Relationship Memory Use in Live-Streaming Recommendation*.
- Canonical working branch: `kbs-n12-single-thesis-restructure-plan-20261014`, PR [#6](https://github.com/mzch0210/KuaiLive-Agent/pull/6), remains **Draft / unmerged / unsubmitted**.
- Scientific source files: [main.tex](main.tex), [S1–S10 Supplement](SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md), [Highlights](Highlights.txt), [BibTeX](kbs_references.bib).
- Peer/editor report is a user-provided review document; no externally identifiable scholarly referee or journal decision is certified. No external pre-submission human review was requested. Current project novelty assessment remains **HIGH / CONTESTABLE**.
- Exact current revision SHA must be resolved from the branch when archiving; source and PDF hashes must be taken from the successful **same-head** CI run. Do not carry forward historical PDF byte digests after manuscript changes.

## Scientific evidence provenance — reuse existing records

| Role | Canonical pre-existing evidence | Scope / interpretation |
|---|---|---|
| Cross-version baseline | [N12 evidence inventory](N12_C8V_REV2_CROSS_VERSION_EVIDENCE_INVENTORY_2026-10-19.md) | Historical research ledger, not new independent TEST |
| Claim-to-source / reuse and rights | [C7 ledger](N12_C7_CLAIM_SOURCE_REPRODUCIBILITY_AND_RIGHTS_REGISTER_2026-10-19.md) | Original cohorts, sampled/F candidate units, privacy and permission tiers |
| Frozen original TEST | [Plan C G5](../../experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md) | M3 original 47,575-event TEST, six Base fits on shared TEST |
| 30,000 target H1 / nested H2 | [B4-A A4/A5 results](N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md) | Same-period event-ID-disjoint H1; H2 4,096 nested events; frozen population weights |
| Population weights | [20-cell weights JSON](../../experiments/kbs_plan_c/N9_ROUTE_B_B4A_A2_POPULATION_WEIGHTS_2026-10-14.json) | Predetermined five dates × four pretarget-history quartiles; not equal-population cells |
| Primary weighted invocation values | [Supplement Table S10.9](SUPPLEMENTARY_INFORMATION_S1-S10_2026-10-13.md) | SAS F/S 29.203/30.537%; GRU F/S 29.008/30.809%; naturally unequal call rates |
| A4 evaluation/statistics | [One-shot unseal script](../../analysis/kbs_plan_c/n9_b4a_a4_one_shot_unseal.py), [weighted statistics](../../analysis/kbs_plan_c/n9_b4a_a4_weighted_stat_contract.py), [independent A5 audit](../../analysis/kbs_plan_c/n9_b4a_a5_independent_aggregate_audit.py) | Event-level predictions and private IDs are not asserted public |
| Gate OOF/refit | [B4-A A2 freeze](N9_ROUTE_B_B4A_A2_DEV_FROZEN_MODELS_AND_STATISTICAL_CONTRACT_2026-10-14.md) | Four user-group folds, OOF-calibrated thresholds, final full-DEV HGB model |
| Historical source validity | [B4-A A4/A5](N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md) and [C3A validity audit](N10_ROUTE_C_C3A_NULL_VALIDITY_AUDIT_2026-10-14.md) | Composite history rewiring; original H2 cohort-specific prereveal popularity subgate **NOT VERIFIED** |
| Corrected sampled-label research | [NI1G method decision](NI1G_CORRECTED_S_METHOD_GATE_2026-10-20.md) | Real corrected-S policy **NO-GO**; synthetic work does not establish train-only identifiability |
| Resource/latency | [N10 C2B benchmark](N10_ROUTE_C_C2B_MATCHED_DEV_COST_AND_R2_VERDICT_2026-10-14.md) | Older pointwise Utility DEV route slower; newer vectorized F gate not timed |
| Narrative/PDF baseline | [Rev3.2 W8 acceptance](REV3_2_W8_FINAL_ARGUMENT_AND_DUAL_PDF_ACCEPTANCE_2026-10-21.md) | Pre-S1 scientific acceptance only; use newer successful CI after revisions |
| Author-owned submission gates | [Existing P5 decision packet](REV3_P5_AUTHOR_GO_HOLD_REDIRECT_DECISION_PACKET_2026-10-20.md) | Author identity, licences, declarations, final GO/HOLD/REDIRECT not yet authorized |

## Machine-checkable source guards and reconstruction entry points

- [Frozen C6 scientific contract](../../analysis/kbs_plan_c/n12_c6_scientific_contract.py) preserves all original scientific result-table content.
- [C7 full-cell source audit](../../analysis/kbs_plan_c/n12_c7_full_table_cell_audit.py) audits relocated historical tables (17 rows / 49 numeric cells) against source fixtures.
- [C8V semantic audit](../../analysis/kbs_plan_c/n12_c8v_scientific_semantics_audit.py) checks cohort denominators, frozen primary values, 20-cell weighted H1 call fractions, source limitations and citations.
- [.github C7 workflow](../../.github/workflows/kbs-n12-c7-evidence-pdf-qa.yml) and [.github C8V workflow](../../.github/workflows/kbs-n12-c8v-v0-semantic-pdf-qa.yml) both build main and Supplement PDFs, run scientific checks and upload time-limited artifacts.
- Public environment files [requirements.txt](../../requirements.txt), [requirements-deep.txt](../../requirements-deep.txt) support environment reconstruction but do not themselves prove that all private checkpoints or processed data are reproducible.

## Publication and data-rights boundaries

1. Upstream public sources include [KuaiLive Zenodo](https://zenodo.org/records/16565801), [KuaiLive research repository](https://github.com/imgkkk574/KuaiLive) and [Twitch/LiveRec](https://github.com/JRappaz/liverec). Data origin, release revision and exact redistributed rights must be independently verified; public access is not universal redistribution permission.
2. Processed KuaiLive-M3 event bundles, trained checkpoints, event-level TEST predictions and sealed private audits are **not guaranteed publicly retrievable**. Do **not** publish raw users, authors, histories, private model artifacts or their event-level prediction files without ownership, license and privacy authorization.
3. GitHub Actions artifact ZIPs expire (most current October 21 builds list expiry around December 20, 2026). On archival, record the exact run ID, head SHA, both artifact IDs, actual PDF hashes and pages after downloading; a ZIP artifact digest is not the enclosed PDF's SHA256.
4. No repository DOI, stable third-party full reproduction, final rights clearance, official KBS submission-form compliance, author list or AI/CRediT/Funding/COI/data statement is claimed completed. Resolve with responsible authors as recorded in P5.
5. If manuscript submission requires blinded review, assess whether creator handles, owner-specific GitHub links, self-host descriptors or private paths identify the authors, and prepare a legitimately anonymized review copy without erasing durable scientific provenance.

**Stop rules:** Do not revisit revealed initial G5/H1 TEST for model/threshold selection; do not revive NI1G NO-GO without new defensible information and authorization; do not turn composite H2 source evidence into a causal semantic effect; do not claim invocation-call reductions are production cost savings.
