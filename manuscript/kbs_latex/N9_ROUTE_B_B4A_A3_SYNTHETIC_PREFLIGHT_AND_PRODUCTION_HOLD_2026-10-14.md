# B4-A A3 | Public freeze and synthetic blind-scoring preflight

Date: 2026-10-14

**Status: SYNTHETIC/PUBLIC PREFLIGHT PASS; PRODUCTION A3 HOLD; A4 HARD HOLD.**

## Completed in this branch

- Added analysis/kbs_plan_c/n9_b4a_a3_synthetic_preflight.py (public JSON-only cross-source freeze check and synthetic causal replay).
- Added analysis/kbs_plan_c/test_n9_b4a_a3_synthetic_preflight.py (seven adversarial tests).
- Added .github/workflows/kbs-n9-route-b-b4a-a3-synthetic-preflight.yml (GitHub-hosted ubuntu-latest, contents read-only, no self-hosted private data).
- Reconciled outdated A2 flags in N9_ROUTE_B_EXECUTION_STATUS_2026-10-14.json. A3/A4 authorization remains false.
- GitHub Actions run https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38515403899 SUCCESS; 7/7 tests passed.

Public freeze checks verify: 4,723,652 eligible residual events; main 30,000 events and 10,387 users, mechanism subset 4,096 events and 3,059 users; zero old-G5 event ID overlap; four locked DEV-trained HGB gate/threshold contracts; twenty original date-by-history-quartile population cells; original Kish effective sample sizes 26,849.294 and 3,659.421. Main sample SHA256 be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14; nested sample SHA256 40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059. No sample or model was changed.

The synthetic replay checks request-specific no-current-target access, update-after-prediction, stable source order for equal timestamps, rejection of invalid target/output sets, and rewired historical relations activating only after their source hour closes. These checks only validate a TEST-free toy contract; they DO NOT validate a production 30k scoring pass.

## Required A3 production gates (all HOLD)

1. **Human data-rights approval.** Verify precisely downloaded M3 source version, scholarly use and publication terms, ethics/privacy, and rules for private relation edges and aggregates. The KuaiLive-M3 paper describes CC BY-NC-SA 4.0 but Hugging Face dataset metadata displays CC BY-SA 4.0. No human attestation of exact-version permissible processing has been obtained; a successful technical test cannot supply it.
2. **Production target-blind scorer implementation and source QA.** Build an isolated private A3 runner. Check SHA and feature parity against G1/G5/A2, full-active TRAIN-known rosters and original Base/Memory tie conventions, exact source timezone-naive ordering, per-user temporal monotonicity, and no same-request author anywhere in rank, candidate, history snapshot or gate features. Explicitly preserve original stable source row order for equal-clock events. Previously observed authors enter only subsequent historical states.
3. **Fixed, same-candidate decision evaluation.** Two Base families at primary seed 20261012; SASRec and GRU4Rec each use fixed F-aligned and S-aligned gates, identical F request features, original A2 OOF thresholds. No new training, recalibration, retrospective target-retained sampled candidate features, post-label changes, or artificial TEST call matching. Record realized calls exactly.
4. **Frozen H2 historical null.** The nested 4,096 requests use the same F roster and three predeclared seeds 20261014, 20261015, 20261016. Preserve per-user observed times and per-hour author activity, enforce both original-time author availabilities, use closed-hour swaps only, and finish all original/null target-blind Top-10 rankings before opening any current author.
5. **One-shot output SHA contract.** Before A4, independently verify full event coverage, input/model/runner SHA, history/roster consistency, target-blind output field allowlist, fixed Top-10 and action arrays, the original 30k/4096 sample hashes, and no private user/author/edge uploads. Save private files with exclusive-create semantics: reruns must never overwrite an already sealed prediction result.

## A4 through A7 remain unavailable

A4 may read target author labels only once after the above A3 requirements and accountable investigator approval. A5 uses user-cluster paired weighted inference (5,000 resamples), fixed three directional comparisons with Holm correction, null non-floor checks, and full reporting including negative results. A6 adjudicates H1/H2 without hunting favorable seeds or changing sample; only then may A7 make evidence-aligned paper edits and perform KBS QA.

No real B4-A TEST author, NDCG or policy ranking was opened or scored in this continuation. No external time-period cohort has been established. Route B B3 scientific risk adjudications and the manuscript remain unchanged, and submission stays HOLD.
