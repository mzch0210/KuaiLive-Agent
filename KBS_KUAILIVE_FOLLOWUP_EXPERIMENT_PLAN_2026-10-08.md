# KBS KuaiLive supplemental experiments — frozen execution and efficiency plan

**Version:** 2026-10-08 / plan v1  
**Status:** PLAN ONLY — no new GPU runs authorized or launched by this document.  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Paper:** *When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation*  
**Canonical outline:** [KBS outline](KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)  
**Baseline evidence:** [completed same-checkpoint report](KBS_KUAILIVE_SAME_CHECKPOINT_RESULTS_2026-10-08.md); [successful GPU run 37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476)

## 0. Scientific decision and evidence boundary

The successful paired KuaiLive diagnostic kept the same two trained model checkpoints, fixed sampled-DEV alpha, one Memory rule and 10,222 target events; sampled-active Memory−Base = −0.0412041108, full-active = +0.0463066865; paired shift = **+0.0875107973**, 95% user-paired bootstrap CI **[+0.0818320603,+0.0931087796]**.

Remaining critical questions:

1. **P0 / mechanism attribution:** What part of this *protocol-dependent, descriptive* shift arises from replacing sampled with full-active candidates, and what part arises from using different reference populations for the two per-branch z-standardizations? The score normalization and candidate membership currently change jointly.
2. **P1 / random-seed robustness:** Does the sign and approximate magnitude of the paired shift persist under *independently trained* room and streamer models with all evaluation rules held fixed?
3. **P2 / optional sampling robustness:** How variable is a sampled-active contrast across negative-sample counts and independent sampled-negative lists? This is secondary to P0/P1.

**Research-status rule:** all follow-ups are **post-hoc supporting diagnostics on an already-inspected TEST population**, not new untouched test confirmation. Frozen historical KuaiLive and Twitch policy checkpoints, thresholds and outcomes remain unchanged. All new seeds, signs, null results, failed checks and subset counts are reported, regardless of favorability.

## 1. P0 — 2 × 2 candidate membership × z-score-reference analysis (no training)

**Highest priority.** Reuse the exact existing checkpoint pair from the hash-verified private GPU-runner cache:

- room SHA256: `b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7`
- streamer SHA256: `82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945`
- original DEV-selected room fusion weight **alpha = 0.125**, streamer weight **0.875**; reuse without TEST tuning;
- frozen room TRAIN/DEV/TEST input hashes and room-to-streamer map from run 37746520476; `n=10,222`.

For every user/time/target event, construct the target-inclusive sampled set `S` and nested full-active set `F`. Compute the raw room- and streamer-branch scores over **F once** using the frozen model pair; subset these arrays to obtain raw scores on S. Independently compute the per-event, per-branch `(mean,std)` from either S or F, using the existing population-STD convention and identical zero-variance fallback.

Define `g(C,R) = NDCG@10(M on candidate set C) - NDCG@10(B on candidate set C, normalized with statistics estimated from candidate reference set R)`. Here `C,R ∈ {S,F}`; fixed alpha is used in all cells. Critically, mixed cells `g(S,F)` and `g(F,S)` apply external reference moments to the candidate scores; these are *analytic counterfactual rankings*, not deployed policies. Memory scores depend on candidate membership C but not normalization reference R.

| Cell | Candidate items ranked | z-score reference | Role |
|---|---|---|---|
| **g(S,S)** | sampled | sampled | Must recover existing original sampled result exactly |
| **g(S,F)** | sampled | full | Mixed analytic cell: membership fixed, normalization changed |
| **g(F,S)** | full | sampled | Mixed analytic cell: normalization fixed, membership changed |
| **g(F,F)** | full | full | Must recover existing original full-active result exactly |

Let `A=g(F,F)`, `B=g(S,S)`, `P=g(F,S)`, `Q=g(S,F)`. Compute **two-path Shapley-style descriptive decomposition** (per user, then mean):

```text
membership = 1/2 * [(P - B) + (A - Q)]
normalization = 1/2 * [(Q - B) + (A - P)]
total = membership + normalization = A - B
```

Use *identical user-bootstrap index draws for all related cells, components and subgroup estimates*, 3,000 replicates with recorded seed(s). Report aggregate means and CIs for `A-B`, membership and normalization contributions, both order-specific path contributions and the three retrospective evidence states. Report zero-variance fallback and target-tie frequencies; do not quietly change tie-breaking between old and new scorers. State clearly that Shapley components are **algebraic, protocol-dependent attributions**, *not causal estimates*.

**P0 validation gates:**

- On a synthetic fixture: nested-set membership and target uniqueness; model fusion and tie logic; identical shared reference scoring; nonzero and zero variance; formula identity for each event.
- On the full matched TEST population: exactly 10,222 one-to-one users, S⊆F, identical target and pre-target Memory; unchanged checkpoint and alpha, source input SHA256.
- Original cells reproduce `g(S,S)=-0.041204110825603886`, `g(F,F)=+0.04630668646082395` and `mean(A-B)=+0.08751079728642783` to numeric tolerance (recommend ≤1e−10 in aggregate), with user-level rank equality where a reference per-user file is already locally available.
- The decomposition identity holds per user and overall to floating-point precision; subgroup-weighted means reproduce overall means. A scientific sign is **never** a CI-workflow success condition.
- Fail closed on missing/changed models, mismatched candidate mapping, nonfinite raw scores and unexpected tie-rule drift.

**Implementation path:** add `analysis/kbs_kuailive_factorial.py` or a minimally invasive optional mode in `analysis/kbs_kuailive_same_checkpoint.py`; reuse existing `load_rechorus`, `encode_phase_users`, `candidate_sweep`, `subset_indices`, `memory_rank` and `zscore` logic. **Do not refit models, retune alpha, reconstruct the Zenodo dataset or re-evaluate DEV.** For each user, compute and consume full-candidate score arrays in one pass, recording only four ranks and minimal metadata. Do not upload large per-candidate matrices unless a justified future use case requires them.

**Expected files:** `factorial_report.json`, `factorial_per_user.csv.gz`, `factorial_state_ci.csv`, `factorial_validation.json`, SHA256 manifest, compact timing/resources. Preserve existing frozen source reports unmodified.

## 2. P1 — independent model-training seed robustness

**Minimum predeclared panel: three checkpoint pairs total.** Already completed seed `20260918` is one; newly train room and streamer pairs at fixed seeds `20260919` and `20260920`. If a stronger paper-scale robustness table is needed, define two additional seeds **before running them** (suggest `20260921`, `20260922`) for a complete five-seed panel. Any three-seed panel is explicitly a *limited* stability check rather than conclusive population-of-seeds inference. **Never decide which seed results to retain based on their signs.**

Keep frozen for the primary sensitivity:

- identical input TRAIN/DEV/TEST, eligible room set, Memory specification, feature preprocessing and ReChorus source commit;
- architecture and training hyperparameters from original job: SASRec, embedding size 64, 1 layer, 4 heads, max history 50; LR 0.0005, L2 1e−6, batch size 1024, max epochs 30, early-stop patience 5 using DEV only;
- **alpha_room = 0.125 for every primary seed** to isolate checkpoint randomness; do not use TEST to choose alpha. Optionally, report a *secondary*, separately labeled per-seed sampled-DEV-selected alpha, with the same DEV grid and no TEST tuning.
- once trained, evaluate all four P0 normalization/candidate cells **in the same forward-scoring pass** rather than re-running inference separately.
- for `20260918`, reuse the existing verified checkpoint pair and P0 result; never retrain it.

**Reporting:** one row per seed with model hashes; DEV early-stop epoch and DEV reference metric, sampled/full Base, sampled/full Memory (invariant if data/Memory fixed), their within-regime deltas, paired full-minus-sampled shift, within-seed paired bootstrap CI and P0 membership/normalization components. Report **across-seed mean±SD, min/max and directional consistency**; do not pool 3×10,222 observations as statistically independent and do not mistake within-seed bootstrap precision for between-seed reproducibility. Repeated TEST analysis remains post-hoc, and additional seeds are not evidence of untouched TEST replication.

**Training-cache safety:** cache *each model pair* under a key encoding `seed + training config hash + source commit + dataset-input hashes`. Check a manifest and SHA256 of both weights before reuse. Never use the existing fixed-seed-only cache path for a different seed. On restart, resume completed training pairs and previously verified per-seed scoring; **never rerun successful seeds merely because a later seed failed**.

**Minimum acceptable scientific package:** three genuinely distinct checkpoint SHA256 pairs and three complete per-seed rows, with all guards passing. Any mixed/negative signs are reported and narrow the paper's claim. A five-seed panel is preferred only if extra compute is justified independently of seeing favorable results.

**Expected files:** `seed_summary.csv`, `seed_config_manifest.json`, `seed_<id>_factorial_report.json`, `seed_variation_notes.md`, reproducibility hashes and compact logs.

## 3. P2 — optional negative-sampling robustness, no model training

Using existing full-candidate raw scores, examine candidate sizes `128,256,575` and full-active, with **three pre-recorded negative-sampling draws** for each sampled size where the eligible population permits. Preserve the positive target and sample without replacement. Retain the already frozen 575-item original sample as its own specifically identified condition; do **not** replace it with a new draw.

Report distributions of sampled Memory−Base, full-minus-sampled paired shift, sign consistency, state-specific changes, candidate counts and tie/degenerate-normalization rates. This does not recover unbiased full-catalogue relevance estimates or prove validity of the logged negatives; it tests sensitivity of the *observed protocol*. To avoid additional candidate-score computation, perform P2 inside P0's per-event pass or from a private compact score cache; do not retrain checkpoints.

Proceed only after P0 and the minimal P1 package; otherwise label this item **proposed and unexecuted**.

## 4. GPU runtime and file-transfer budget (observed vs estimated)

**Measured reference, not a guaranteed schedule:** run `37746520476` began 2026-10-08 07:55:59 UTC and finished 08:05:49 UTC (~9m50 wall time). Its log shows training started ~07:56:46 and model training finished ~08:03:17 (~6m31). DEV alpha fitting + TEST scoring and report creation ran ~08:03:17–08:04:46 (~1m29); uploading a ~302 MB bundle took approximately 50 seconds; other time covered setup/cache/pinned source verification.

Optimization decisions:

1. **P0 uses cached models, not training:** expected dominant cost is a single full-active candidate-scoring pass plus startup, not ~6.5 minutes of retraining. Existing per-user user-embedding computation is reused. An observed-runtime-based planning budget is a few minutes rather than an asserted guarantee.
2. **P1 trains only missing seeds, once per model branch:** two additional seed pairs under fixed protocol. Hardware and software conditions affect wall time; budget using the original ~6.5-minute pair-training observation, plus evaluation overhead per seed.
3. **No repeated 302 MB model uploads:** the original verified checkpoint weights already exist in artifact `11536890439`; new follow-up artifacts primarily contain small compressed per-user outcomes, hashes and configs. For reproducibility, preserve separately at least one durable copy of any *new* trained checkpoint pair or a documented regeneration recipe; private runner cache alone is not a permanent scientific archive.
4. **Do not re-download raw data:** verified dataset input cache and four frozen SHA256 checks are reused; no Zenodo ingest or room candidate rebuilding.
5. **One pass per seed:** compute room/streamer raw full-candidate scores once; subset sample ranks; 2×2 factorial cells and optional P2 draw ranks from the same score vectors. Cache event outputs for repeated bootstrap; never bootstrap by rescoring models.
6. **Compact CI calculation:** generate a common user-resampling index matrix or deterministic reproducible index stream once per seed, reuse across outcomes/subgroups. Use vectorized bootstrap; avoid storing large item-by-user-by-bootstrap tensors.

**Protection:** keep the owner's explicit manual `workflow_dispatch` GPU approval and self-hosted non-root/security checks; pushes run only hosted preflight, never private-GPU training. Use the existing single-GPU concurrency group, serial execution of new seeds and skip-if-valid model/checkpoint caches. Limit elapsed GPU runtime and artifact size with job gates. No experiment runs have been launched by this plan.

## 5. Stage gates, decision logic and paper placement

| Stage | Evidence gate | If it succeeds | If it fails or effect differs |
|---|---|---|---|
| 0: hosted synthetic | module compile, deterministic mock 2×2 tests and exact decomposition | permit controlled private checkpoint reuse | fix implementation without looking at real TEST outcomes |
| 1: P0 | old sampled/full rows exactly replay, four cells finite, per-user additive identity | strengthen Section 6.1 mechanism panel; report both attributions | investigate mismatch before interpreting new cells; keep old published diagnostic unchanged |
| 2: P1 (3 seeds) | two distinct new model pairs, protocol fixed, every seed recorded | report mean±SD and sign stability, qualify 3-seed uncertainty | retain all outcomes, discuss initialization sensitivity; extra 5-seed panel only with separately recorded rationale |
| 3: P2, optional | fixed draws, nesting and reused raw scores, no training | supplementary sampling sensitivity figure/table | disclose limited protocol robustness; do not relabel sampling sensitivity as causal effects |
| 4: manuscript freeze | full provenance links, archived compact CSV/JSON, plot-to-claim matrix | update Section 6.1, Section 7.2, 7.4 and S5; adjust abstract only with proper status tags | qualify or retract unsupported causal/mechanism wording |

**Scientific targets (NOT pass/fail signs):**

- H1 descriptive: the candidate-membership and normalization-reference components are separable as an *exact algebraic decomposition* under fixed raw scores; either may be positive, negative or zero.
- H2 reproducibility: the original positive paired shift may or may not reproduce across seeds; report all fixed-seed outcomes and distinguish bootstrap/user heterogeneity from training-seed heterogeneity.
- H3 sampling sensitivity (optional): the operational contrast may depend on sampled candidate count and draw.

**Section placement:** Section 5 should retain its six-subsection methods structure, adding at most 2–3 sentences defining the factorial counterfactual/reference normalization and seed panel **after results exist**; Section 6.1 should show the new 2×2 components and seed stability in a compact panel without crowding Twitch held-out evidence (Section 6.4); place per-seed and negative-sampling tables in Supplementary S5/S8. Discussion Section 7.2 must maintain the boundary between state prevalence, conditional utility and candidate-selection effects; Section 7.4 must state the noncausal, post-hoc and single-platform limits.

## 6. Provenance and literature

- Original diagnostic results and source: [completed evidence ledger](KBS_KUAILIVE_SAME_CHECKPOINT_RESULTS_2026-10-08.md).
- The previously frozen Twitch/LiveRec held-out policy remains unmodified.
- Krichene and Rendle (2020), *On Sampled Metrics for Item Recommendation*, KDD, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ — sampled rank metrics need not preserve model comparisons.
- Ihemelandu and Ekstrand (2023), *Candidate Set Sampling for Evaluating Top-N Recommendation*, WI-IAT, https://doi.org/10.1109/WI-IAT59888.2023.00018 — candidate selection strategies interact with evaluated performance and popularity-related bias.
- *Improving Methodological Standards in Recommender Systems Offline Evaluation* (2026), ACM Transactions on Recommender Systems, https://doi.org/10.1145/3800587 — documents rigorous baseline, experimental provenance, seed and reproducibility practices.

**Status:** plan written, reviewed against the current evaluator and owner-guarded workflow; no new experiment results are asserted and no GPU execution is started here.
