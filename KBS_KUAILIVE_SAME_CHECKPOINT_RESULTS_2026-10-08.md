# KuaiLive same-checkpoint candidate-swap — completed evidence ledger

**Date:** 2026-10-08  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Scientific status:** **completed GPU experiment, post-hoc supporting diagnostic**; not a new untouched held-out confirmation or revision of any frozen original policy.  
**GitHub Actions:** [run 37746520476](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476) — `preflight` and `paired_gpu` both **success**; all paired TEST scoring, report generation and artifact upload steps passed.  
**Result artifact:** [ID 11536890439](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37746520476/artifacts/11536890439), named `kbs-kuailive-paired-37746520476` (~302 MB); GitHub retention 90 days, not a permanent archive. The GPU job log emits the `report.json` payload verbatim, reproduced in this ledger for traceability.  
**Evaluator:** `analysis/kbs_kuailive_same_checkpoint.py`; workflow `.github/workflows/kbs-kuailive-same-checkpoint.yml`.

## 1. Design and protocol identity

- TEST population: `n = 10222` one target per user, same `(user, time, target room)` in the sampled-active and full-active candidate contexts.
- Sampled candidates: 1 target + 574 eligible negatives; full-active: all time-eligible rooms with the target preserved.
- **One newly trained** ReChorus Room-SASRec checkpoint and one newly trained Streamer-SASRec checkpoint (not bitwise-identical to historic frozen checkpoints).
- Fusion `alpha_room = 0.125`, `alpha_streamer = 0.875`, chosen **once on sampled DEV**, applied unchanged to TEST candidates in both regimes.
- The **same raw model score vectors** are computed over full-active rooms; sampled scores are recovered by exact subsetting; each candidate set is standardized independently, as required by the baseline score definition.
- Relationship Memory uses the same fixed Short/Long/Popularity definition and eligible pre-target history on both sides.
- Statistical procedure: 3,000 **paired user-level percentile bootstrap** replicates for regime contrasts and subgroup shifts. This is a post-hoc diagnostic on the already-studied TEST population; CI interpretation remains conditional on its fixed checkpoints and analytic protocol.

## 2. Main results, NDCG@10

| New matched-checkpoint protocol | sampled-active | full-active |
|---|---:|---:|
| Base | 0.607091575 | 0.385712423 |
| Memory | 0.565887464 | 0.432019110 |
| Memory−Base | **−0.041204111** | **+0.046306686** |
| 95% paired user-bootstrap interval for Memory−Base | [−0.048203881, −0.034140382] | [+0.039776941, +0.052967778] |

**Primary paired effect:** `(Memory−Base)_full − (Memory−Base)_sampled = +0.087510797`, 95% bootstrap CI **[+0.081832060, +0.093108780]**, `n=10222`.

The ordering sign reversal **persists despite fixed checkpoints and fusion alpha**. The Memory scores under the two regimes match historical frozen decomposition values, but the *new* Base values differ from the historical baselines. This result must **not** replace historical or frozen-policy rows as if they were a single experiment.

## 3. State-specific decomposition (target-relative, retrospective only)

| State | n | Prevalence | Sampled Memory−Base | Full Memory−Base | Paired shift | 95% CI for shift |
|---|---:|---:|---:|---:|---:|---|
| represented | 4589 | 0.44893367 | +0.12859273 | +0.21649726 | **+0.08790453** | [+0.08023224, +0.09556630] |
| recoverable-but-unrepresented | 206 | 0.02015261 | +0.18445166 | +0.08248276 | **−0.10196890** | [−0.15224207, −0.05221326] |
| unavailable | 5427 | 0.53091372 | −0.19334762 | −0.09897742 | **+0.09437020** | [+0.08602085, +0.10213970] |

All 10,222 events remain in the same retrospective state under both candidate regimes. The exact weighted decomposition of the overall paired shift is:

- represented contribution: `+0.03946330`
- recoverable-but-unrepresented contribution: `−0.00205494`
- unavailable contribution: `+0.05010243`
- total: **`+0.08751080`**

The aggregate reversal is **not explained by a larger recoverable-state prevalence** (state proportions are exactly fixed). The recoverable state's relative gain decreases, even though it stays positive in both candidate regimes. The positive overall shift arises primarily from larger represented relative gains and smaller—but still negative—unavailable relative losses.

## 4. Audit and model identity

```text
Room-SASRec model SHA256:
b8c9fbb06ad6a627e44477c6387a6fb2eadaad783caa998201b3de76fa0cf0e7
Streamer-SASRec model SHA256:
82db309e03947187430c844aab35bbce4a8ed4702c32914d1b4e3e0be987d945
ReChorus source commit:
c164ec4303cc20ddcfbd1b57de366a481811d1e5
Frozen matched TEST input SHA256:
3491862df4de5cfb487fbd21c2f62c2d1d62acac110f852cc83c019dfcc6e956
```

The evaluator's reported guards are all true: same TEST identities; same checkpoint pair and fusion alpha; sampled candidates nested in full-active; same specialist; user-paired bootstrap; and evaluation outcomes do not control success/failure. These assertions should be interpreted together with the implemented runtime checks, not as proof of isolated causal effects.

## 5. Historical numbers are distinct evidence

The earlier frozen KuaiLive state-decomposition record reported `sampled Base 0.61714`, `Memory 0.56589`, `Memory−Base −0.05125`, and `full-active Base 0.39835`, `Memory 0.43202`, `Memory−Base +0.03367`. A separate manuscript planning record reports a different historical sampled Base `0.60784`; its protocol lineage must be resolved before comparing historical Base values. None of these are the new paired-protocol Base values `0.60709` and `0.38571`. Their scientific roles differ: historical operational regimes versus new single-checkpoint post-hoc control.

## 6. Claim boundaries and paper updates

**Supported:** The sampled/full sign reversal of the operational Memory-minus-Base NDCG@10 contrast persists for this one fixed checkpoint pair, one DEV-selected alpha and matched TEST population. A paired shift of about 0.0875 is well away from zero under a user-paired conditional bootstrap.

**Not supported:** That candidate membership is the isolated causal mechanism (candidate-wise z-standardization also changes); that long-horizon recoverability primarily explains the aggregate reversal; that the effect holds for every random seed or dataset; or that the post-hoc reused test constitutes another untouched confirmatory test.

**Manuscript plan:** Replace Section 6.1's pending panel with the completed standalone panel and state-decomposition table. Tighten Abstract/Introduction claims to say fixed-checkpoint candidate-regime dependence rather than causal candidate-set effects; update Discussion 7.2 and Limitations 7.4 accordingly. Keep Twitch's canonical frozen-policy result untouched. Optional new supporting studies, if undertaken, should isolate normalization against a fixed reference and examine checkpoint-seed variation before overgeneralizing.

**Source-of-truth order:** original frozen artifacts for historical numbers; GitHub run 37746520476 log and uploaded report for this *new* diagnostic; canonical manuscript/outline as derivative prose, never the source of experimental metrics.
