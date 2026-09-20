# Frozen Official-Negative Recent-Exposure Robustness Protocol

Status: **FROZEN BEFORE OUTCOME INSPECTION**

This protocol is a robustness test for the Dual-ID + Selective Memory result using KuaiLive's official `negative.csv` records (exposures presented to a user but not clicked). It is not a causal evaluation and it is not interpreted as a contemporaneous target-time slate unless every negative is active at the target timestamp.

## Why the original strict protocol was abandoned

The first strict protocol required each negative room to:

1. come from official `negative.csv`;
2. occur before the dev/test positive target;
3. fall within the preceding 24 hours; and
4. still be live at the target click timestamp.

Run `35483640099` showed that this protocol has essentially no support: only **1 / 10,222** users had at least 10 qualifying negatives in both dev and test. This is a coverage failure, not a model failure, and no model metric is interpreted from that run.

## Coverage audit used to freeze the replacement protocol

Coverage-only audit run: `35486412089`.

The audit examined only official unclicked exposures strictly before each target. No model scores or recommendation metrics were used to choose the protocol.

Audit facts:

- evaluation users: 10,222
- raw `negative.csv` rows: 12,705,835
- negative rows belonging to evaluation users: 6,653,287
- shop-room negative rows belonging to evaluation users: 588,499
- evaluation users with at least one shop-room negative exposure: 10,139
- lookback grid: 1, 6, 24, 72, 168, 336 hours
- candidate-negative grid: 5, 10, 20

Frozen selection rule:

1. Prefer `k = 10` real negatives.
2. Require at least 2,000 users to have sufficient official negatives in **both** dev and test.
3. Among qualifying protocols, choose the **shortest** lookback.
4. Only if no `k = 10` protocol qualifies, fall back to `k = 5` using the same rule.
5. The rule uses coverage only; model metrics are not consulted.

The selected protocol is therefore:

- **lookback = 168 hours (7 days)**
- **k = 10 official unclicked exposures**
- **eligible users = 4,181 / 10,222 = 40.90%**
- dev users with >=10 qualifying negatives: 4,600
- test users with >=10 qualifying negatives: 4,529

## Candidate construction

For each dev/test positive target:

- use only official `negative.csv` exposures for the same user;
- use only exposures with `exposure_timestamp < target_click_timestamp`;
- use only exposures within the preceding 168 hours;
- restrict to shop-room live IDs in the prepared shop universe;
- deduplicate repeated impressions of the same `live_id`;
- exclude the positive target `live_id` itself;
- take the 10 most recent distinct qualifying rooms;
- do **not** require those earlier-exposed rooms to remain live at target click time;
- do **not** use any exposure after the target click.

Interpretation: this is **recent-exposure episode ranking**: rank the later clicked target against live rooms that were genuinely shown earlier and skipped. It is deliberately not described as same-instant slate ranking.

## Frozen model/evaluation settings

No model family or hyperparameter is retuned for this robustness test.

- Room-SASRec: same frozen SASRec hyperparameters used in the Dual-ID identity-control experiment.
- Streamer-SASRec: same frozen SASRec hyperparameters.
- Dual-ID: `alpha * z(RoomSASRec) + (1-alpha) * z(StreamerSASRec)`, with alpha selected on dev only over the existing fixed grid.
- Memory expert: same MemoryFusion implementation.
- Selective gate: same HGB residual-regression gate and user-state + base-confidence features.
- Gate threshold: chosen from 5-fold OOF dev predictions only.
- Test is evaluated once after dev fitting/selection.
- Primary metric: NDCG@10 on 1 positive + 10 official negatives.
- Uncertainty: paired bootstrap 95% CI.

Frozen pass rule:

> **PASS iff dev-learned Selective(Memory vs Dual-ID) improves Dual-ID on test and the paired-bootstrap 95% CI lower bound of the improvement is > 0.**

Always-on MemoryFusion is reported as a diagnostic but is not required to beat Dual-ID.

## Guardrails

- No causal, CTR-lift, GMV-lift, IPS, or SNIPS claim is allowed because `negative.csv` supplies exposure outcomes but no valid logged propensities are available in this protocol.
- The eligible cohort is exposure-dense and therefore not assumed to represent all KuaiLive shop users.
- A PASS supports robustness to **real logged unclicked exposures**; it does not prove robustness to every production candidate-generation mechanism.

Formal evaluation workflow: `.github/workflows/exposure-episode-dual-id.yml`
