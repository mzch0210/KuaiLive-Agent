# Route B — B2 medium-scale relationship-identity control: source and execution eligibility

**2026-10-14 | B2 PREOUTCOME SAMPLE PASS, MEDIUM RELATION REWIRE/SCORING HOLD.** [GitHub Actions #38498724492](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38498724492).

## 1. Concrete work executed

On the original private M3 DEV source, the read-only preflight verified the B1 SHA256 and the same 50,049-event DEV cohort. It loaded **only event/user/time and pretarget history-count fields**, not ranking outcomes or target labels. It deterministically froze 1,024 requests (**992 distinct users**) in **16 strata**: four chronological time quartiles × four pretarget history-activity quartiles, 64 requests per stratum. It explicitly excluded the 128 events from the previous late-period feasibility pilot.

The private IDs/timestamps/history counts are stored on the authorized self-host at `~/.cache/kuailive-agent-kbs/klm3_n9_route_b_b2_pretarget_sample_v1/B2_MEDIUM_EVENTS_PRIVATE.npz`; private snapshot SHA256 is `6ad1a0753e181ac638636c278d226832b08d90d7d4867019910c61b96d7507da`. Only safe counts and the digest were added to the public repository, at `experiments/kbs_plan_c/N9_ROUTE_B_B2_MEDIUM_SAMPLE_PREFLIGHT_PUBLIC_2026-10-14.json`.

**This is an actual executed source/sample-freezing task, not completion of the middle-sized mechanism experiment.** No target rank observed, no Memory/Long rescoring, no historical relation edges altered, no Base weights or original G5 TEST accessed.

## 2. B2 temporal intervention gate, blocking actual 1,024-event scoring

The earlier 128-event pilot rewired *only an historical prefix preceding the earliest selected request*. Its exact time/author-degree preservation cannot be carried over unchanged to samples from all DEV temporal quartiles. A valid 1,024-event design must handle rolling causal history:

1. For each target request at time `t`, reconstruct original viewer history using only interactions with source time strictly less than `t`.
2. Swap historical relationship authors only within **fully closed** time bins prior to `t` (or use a separately proven sequentially online-valid swap); never allow a later interaction in the same open bin to change what the target request would have observed.
3. Require both cross-swapped authors to be active at both respective source interaction timestamps, maintain per-user event timestamps/counts, exact hourly author activity marginals for swapped closed bins and the same fixed target candidate eligibility.
4. First reproduce the original Full/Long F/S NDCG for the new selected 1,024 events, comparing every event against sealed B1/B2 outputs. Any parity or temporal failure => **HOLD** before constructing causal claims.
5. Freeze three null random seeds (20261014/20261015/20261016) and *one* constrained temporal null construction before examining outcomes. Record realized altered-edge coverage and nonfloor specialist quality for every seed, not selecting the largest advantage.
6. Compute main real-minus-valid-null Full F quality with paired **user** bootstrap, descriptive seed variability, sampled S secondary only; 1,024 → 2,048 expansion only for predeclared interval precision needs, not statistical-significance search.
7. **Human data-rights, privacy and study-authorship signoff remain required** for any broader private relationship-edge transformation/derived data release. Existing dataset visibility/previous pilot success do not themselves certify all applicable rights.

## 3. Why the new B1 results increase the importance of these gates

The executed B1A nine-cell decomposition showed **46,462** events have at least one zero Full−Long source gap; **0.100885 out of the total 0.115382** signed candidate-source interaction is attributable to those at-least-one-zero cells. A statistically significant candidate-source interaction therefore remains consistent with metric top-10 support changes. This is exactly why a valid, nonfloor historical-identity control is scientifically valuable, but not an excuse to relax temporal eligibility or data-rights checks.

**B2 decision:** `SAMPLE_FREEZE_PASS / TIME-SAFE_ROLLING_SWAP_PROTOCOL_PENDING / RIGHTS_REVIEW_PENDING / FULL_SCORING_NOT_EXECUTED`. No escalation to 50,049-event DEV, no new TEST authorization, no manuscript edits.
