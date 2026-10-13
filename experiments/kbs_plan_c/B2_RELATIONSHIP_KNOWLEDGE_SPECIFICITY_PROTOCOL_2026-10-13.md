# B2 — Relationship-knowledge specificity: locked DEV-only ablation protocol

**13 October 2026. Status:** prospective to B2 DEV analyses but **post-G5 and post-B1 exploratory**; G5 TEST, canonical M3 frozen policy family and original N8 manuscript will not be touched.

## Scientific question

Does the observed dependence of fixed Memory-minus-Base value on candidate context and the S→F transfer deficit require actual user–author **historical relationship** information, or is it reproduced by long-only, short-only, global train popularity, or a broken user–author relationship control? We will NOT claim a new general-purpose deferral algorithm or causal identification of pure candidate-set size.

## Fixed evidence and data boundary

- 50,049 M3 **DEV** author-ranking events; 12,628 users, original corrected full-active paired DEV source and B1 S/F labels SHA-locked.
- The original pre-trained SASRec and GRU4Rec Base fits remain unchanged. Reuse their full-active and 575 target-retained sampled **offline label** values from B1; never retrain Base or open prior G5 TEST.
- Replay the exact pretarget TRAIN+earlier DEV causal history once with **TRAIN-unseen authors consuming short slots and the all-author long denominator**; one event-time eligible TRAIN-known roster pass; reconstruct sampled candidate set with B1 seed and original event ID.
- Original fixed Memory scoring: `0.10 * P_train + 0.45 * Short_all_prior + 0.45 * Long_all_prior`. Target-retained S is offline metric supervision only. **No target ID/outcome/sample-selected-score enters gate features.**

## Locked comparisons

| Arm | Memory evidence | What this controls |
|---|---|---|
| `full` | P + Short + Long | **Must exactly reproduce original corrected DEV F rank and B1 sampled NDCG for every pilot/full event** |
| `long_only` | only long count / max among **all** prior authors | Is long-term relationship information material? |
| `short_only` | only most recent 10 **all-prior** positions, zeros for unknown tokens | Is recent interaction sufficient? |
| `popularity_only` | TRAIN-only globally normalized author popularity | Can non-personal evidence explain decisions? |
| `relationship_shifted` | P + **cyclically rotate the whole (Short+Long) support/strength vector** across event-time eligible sorted author candidates | Null placement preserves *the per-event history-score multiset* but breaks its specific user–author alignment; event/time-derived deterministic rotation, **never uses target** to assign support |

The rotated null is an exploratory *within-event relationship-placement placebo*, **not** a realistic retrained expert and not an exact marginal-popularity-preserving user-history permutation. Preserve and report this limitation, and do not conflate candidate identity scrambling with equal resource budgets or causal estimates. Use `seed=20261013`; a positive nonzero modulo offset is determined from event ID alone.

## B2-1 score parity gate (first execution)

Deterministically select **128** time-spread M3 DEV events; independently reconstruct F and S rankings for all five Memory arms. The `full` arm MUST match (a) original corrected F Memory rank and (b) B1 sampled Memory NDCG exactly on **all 128**. If a single discrepancy appears: HARD HOLD, no full B2.

For all arms require valid target/roster identity, finite nonnegative component scores, unique sampled subset, strict pretarget histories, no export of private user/event/candidate IDs, unchanged B1 F/S Base labels. Report mean F/S NDCG and elapsed CPU histories/roster/score time. Historical score-vector permutation must be independent of target outcome.

## B2-2 full paired DEV label gate (only after B2-1 PASS)

On all 50,049 DEV events **one** stream replay, **one** activity roster sweep shared by all arms, no GPU or Base scoring since B1 Base F/S results remain frozen. Per-event variant F and S NDCG + fixed Base labels written **privately** to a new non-overwriting SHA manifest; public result only contains per-arm aggregates/timing and provenance. Full-Memory parity against original corrected F and B1 sampled S must be perfect. Report full and sampled mean Memory−Base utility, target sign-category changes, and fixed always-Memory quality for each source component.

## B2-3 actual selector effect (only after B2-2 PASS)

For each fixed variant, both pretrained Base families, run exactly the B1 5×4 user-disjoint nested scheme with **frozen 12 original F pretarget features**, identical HGB hyperparameters and the original `select_threshold` with ≤0.30 inner OOF calls. Primary comparison S→F and F→F per Memory variant. Use **matched outer full-active heldout event cohorts**, natural actual Memory-call counts and paired user-cluster 95% intervals; avoid falsely claiming equal-call quota on outer DEV. Include Always Base and each variant's Always Memory, not only within-router contrasts.

Additional no-history-information control: compare same fits **without the history-support feature**, because the original 12 F features include a `x_memory_history_supported_share` computed from real full-Memory history. This sensitivity is required before claiming nonpersonal popularity-only effects, since retaining a true-history feature in that arm can contaminate interpretation.

**B2 scientific GO** requires source-specific, nontrivial out-of-user F selection quality and candidate-regime regret/recovery that is not reproduced by popularity-only and relationship-broken controls. The necessary test is a **paired difference of regret penalties** across variants, not a comparison of separate interval overlap. If short-only explains the same benefit, the contribution narrows to immediate interaction repetition rather than persistent relational knowledge. If null placebo works similarly, knowledge-specificity claim is NO-GO. Report adverse outcomes.

**Evidence ceiling:** all new B2 findings remain *post-G5 exploratory DEV*. Fresh independent unseen and authorized TEST outcomes, frozen before reveal, are needed to claim confirmatory generality. Does not solve M3 Always Memory absolute advantage/real serving economics risk.

## Efficiency and safe execution

1. DEV-only sample pilot, byte-verified source bundle relayed GitHub-hosted → self-host (no self-host Git checkout because github.com:443 previously timed out).
2. Replay CPU historical events once and build rosters once, reuse frozen B1 Base scores; compute five Memory component ranks in batches/NumPy, no unnecessary GPU work.
3. Stop at the first mismatch or missing privacy/source proof. Never overwrite existing private sources. GitHub artifacts limited to aggregate counts, provenance digests and timings.

Key related sources: Yerragunta et al., *Dynamic conditional gating mechanisms for Question Answering over incomplete Knowledge Bases*, KBS 346, 116167 (2026), https://www.sciencedirect.com/science/article/pii/S0950705126008932 ; Krichene & Rendle, *On Sampled Metrics for Item Recommendation*, KDD 2020, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ .
