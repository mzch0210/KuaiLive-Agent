# Plan C G5 — One-shot held-out TEST execution protocol and provenance

**Date:** 2026-10-12. This ledger is frozen in GitHub before G5 target-label evaluation, and does not contain any observed TEST ranking numbers.

## Prerequisites verified

1. Original G0F scientific pre-registration: [G0F_PRETEST_PROTOCOL_2026-10-12.json](G0F_PRETEST_PROTOCOL_2026-10-12.json). Source G1 manifest SHA256 `bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`; TEST cohort byte SHA256 `e60da60672ea1921dd3a5fccfb0aa76a3a06d50834e8080a07b2465777c9bdb1`; test cohort count **47,575**.
2. Six independent-fitted models: SASRec/GRU4Rec × training seeds 20261012/13/14, all selected from a common 4,096-event, 575-active-author DEV checkpoint screen. None selected or retuned from TEST.
3. Five independently DEV-frozen policy objectives per model: Utility, Difficulty, Specialist, Uncertainty and History; budget constraint max 30% calls **on DEV**. The exact pointwise DEV threshold remains fixed for TEST; its actual TEST call fraction may change and **must not be forced or adapted**.
4. [G5 frozen SHA registry](G5_PRETEST_SIX_BASE_FROZEN_REGISTRY_2026-10-12.json) committed before any TEST scoring. [G5 hash-only User-host audit run #38225118849](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38225118849) **success**, six checkpoint, six frozen gate policy and eighteen supervised gate-model hashes matched this registry. SHA-only preflight did **not** load any TEST outcome rows.
5. Corrected frozen Memory 0.10 TRAIN popularity + 0.45 last-10 of **all prior events**, plus 0.45 all-prior count divided by max frequency among **all** historical authors; previous authors unknown to TRAIN consume temporal positions and contribute to the long denominator. All rank candidates are distinct warm TRAIN-known currently-live authors. Candidate membership does not use the known target label.
6. G4 full-active DEV results are complete for six checkpoints and the warmed cost test is *not* evidence of net production speedup: [G4 report](G4_EXTRA_SEED_FULL_ACTIVE_DEV_GATE_AND_COST_RESULTS_2026-10-12.md).

## G5 implementation plan / target confidentiality

**Stage G5-A:** [Workflow](../../.github/workflows/kbs-plan-c-g5-a-unlabeled.yml) — strict, causal, prequential TEST feature computation. The 47,575 selected test event IDs, user IDs and clocks are read *without the same-event target author*. All TRAIN/DEV and only **earlier** TEST interactions may update the observed history. For each test event, the six Base and the Memory expert score the **same** full currently available warm-author set, without access to the current target author. Store a target-blind top-10 author list for each expert and six × five frozen gate score/call arrays. Verify complete event coverage, SHA and exact registry. The event-level files remain on User-host. G5-A produces **no TEST ranks or NDCG**, and uploads only a nonidentifying manifest.

**Stage G5-B:** [Workflow](../../.github/workflows/kbs-plan-c-g5-b-confirm.yml) — may run only after successful, immutable G5-A and synthetic stats tests. This is the **one-shot TEST label reveal and confirmation**. Verify all target-blind file digests, label IDs, source cohort SHA; convert author target labels to frozen TRAIN author token indices; compute exact top-10 hit positions for six Base models and the fixed Memory. Calculate all five frozen policy outcomes with **no TEST-based threshold calibration**. The reported NDCG is `0` for target outside the recorded top 10, or `1/log2(rank+1)` within top 10. All events are retained irrespective of policy success, and negative findings are not suppressed.

## Confirmatory tests and uncertainty

Three pre-declared one-sided contrasts per Base/seed: Utility versus (1) Always Base, (2) Difficulty, (3) Specialist. Perform the original pre-registered five-thousand **user-cluster paired bootstrap** for 95% percentile intervals, and 5,000 user-cluster sign-randomization draws to estimate one-sided comparison p-values. Apply **Holm sequential multiplicity adjustment** to the three contrasts separately for each family/seed (Holm 1979, *A Simple Sequentially Rejective Multiple Test Procedure*, *Scandinavian Journal of Statistics* 6(2):65–70).

The cluster sign test additionally assumes approximately sign-symmetric null differences at the **user cluster** level. The 18 tests across six fitted models share evaluation cases; Holm protection within three-model-specific contrasts must **not** be presented as one global 18-comparison FWER guarantee. Report actual means, 95% intervals, unadjusted and adjusted p-values, call fractions, and all failures. The 20-seed DEV random draws and Oracle@budget are explanatory benchmarks, not confirmation hypotheses.

**Secondary descriptive comparisons:** Always Memory; Uncertainty and History; uniform Random@30 conditional expectation; hindsight Oracle@30 nondeployable ceiling; multi-seed mean and standard deviation. Full-active vs 575-sampled candidate metrics use different protocols, so do not combine absolute numbers.

## Efficiency / integrity

- One stream replay and one room-availability sweep for **all six** neural Base checkpoints plus shared fixed Memory. No re-training, downloaded reprocessing, or six repeated rosters.
- GPU/CPU work split: GitHub-host static checks and source signing; existing User-host RTX3090 for private source-data inference and fit artifact access.
- Store just **seven target-blind top-10 lists per event** (6 Base + 1 Memory), not a giant candidate score tensor. Store only six × five call decisions and hashed per-event private metadata. This gives event-level exact NDCG@10 under the deterministic frozen top-k ranking convention.
- Do not upload user IDs, individual TEST targets, personal histories, candidate memberships or model checkpoint bytes to public GitHub.
- After labels are opened, do not alter, refit or select any model, gate or data policy. A failed TEST confirmatory comparison remains a valid scientific result and is reported honestly.

## Scientific inference caution

The new M3 author's current-room task and global time split differ from the original KuaiLive room recommendation and per-user benchmark. Independent observation period does not imply person-disjoint dataset replication. Also, a specialist invocation fraction below 30% cannot establish a 70% reduction of *total compute latency*; actual warmed DEV replay found the selective path slower than Always Memory. Retain this negative result in publication-facing cost discussion.
