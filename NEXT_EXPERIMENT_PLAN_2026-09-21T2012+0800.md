# KuaiLive-Agent — Post-P0 Next Experiment Plan

**Snapshot timestamp:** 2026-09-21 20:12 +08:00  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Current phase:** P0 CLOSED; P1 cross-platform external validation + manuscript freeze.  
**Supersedes for current execution:** `NEXT_EXPERIMENT_PLAN_2026-09-21T1524+0800.md` while preserving the older snapshot for provenance.

---

# 1. Executive decision

The project should **not reopen broad KuaiLive model expansion**. The major internal-validity and mechanism risks are now closed:

- persistent-streamer identity shortcut — CLOSED;
- sampled-candidate dependence — CLOSED by full-active ranking;
- relative utility vs generic difficulty — CLOSED in sampled and full-active regimes;
- final Dual-ID state/confidence information ablation — CLOSED;
- strict temporal validity — CLOSED;
- adaptive-computation / DS-Frame collision — CLOSED sufficiently;
- DS projected-room bootstrap consistency — CLOSED at 5,000 resamples;
- DCGLive official-protocol compatibility — AUDITED / CLOSED;
- inference latency and gate cost — CLOSED.

The new scientific picture is:

> **Memory-relative utility is regime-dependent. Its aggregate sign changes across candidate universes and temporal regimes, while learned relative-utility routing continues to exploit within-regime heterogeneity beyond generic hard-case routing.**

The next high-value experiment is one untouched **cross-platform LiveRec/Twitch validation with the official strong LiveRec base**.

---

# 2. Closed P0 evidence

## P0-A — Full-active candidate-universe validation — PASSED

Primary runs:

- `35580324870` — full-active Dual-ID validation;
- `35581670479` — full-active conditional-utility closure.

### A1 strict transfer

- Dual-ID: 0.398353;
- Always Memory: 0.432019;
- Selective: 0.430152;
- Selective − Base: **+0.031799**;
- 95% CI: **[+0.028143,+0.035554]**;
- invocation: 29.18%.

### A2 full-active native, primary

- Dual-ID: 0.398353;
- Always Memory: 0.432019;
- Selective: **0.451801**;
- Selective − Base: **+0.053448**;
- 95% CI: **[+0.048252,+0.058836]**;
- invocation: 64.44%;
- Selective − Always Memory ≈ +0.01978.

Candidate universe: mean 8,269 active rooms at test, median 8,132, p95 12,301. All positives are legally active.

Scientific consequence: sampled-active Memory−Base is negative, full-active Memory−Base is positive. Candidate universe is itself a regime variable.

## P0-B — Conditional-utility mechanism — PASSED

Sampled-active:

- Spearman predicted-vs-realized utility `rho=0.2049`;
- utility router − difficulty router at exact K: **+0.005458**;
- 95% CI **[+0.002659,+0.008464]**;
- learned gate captures ~17.0% exact-K oracle gain.

Full-active:

- `rho=0.2399`;
- utility router − difficulty router: **+0.014431**;
- 95% CI **[+0.010938,+0.017908]**;
- learned gate captures ~50.3% exact-K oracle gain.

Use “utility stratification / decision-useful prediction,” not “well calibrated.”

## P0-C — Final Dual-ID information ablation — PASSED

Combined state + confidence is strongest in sampled and full-active regimes. Claim complementarity, not universal dominance of confidence-only features.

## P0-D — DCGLive compatibility audit — CLOSED

Official DCGLive is conceptually close but not numerically compatible with the frozen task because of material differences in data slice, split, candidate universe, availability handling, state-update semantics, and metric context.

Decision:

- cite prominently;
- no official-score head-to-head in the main table;
- only implement `DCGLive-adapted` if reviewers explicitly require a common-protocol graph baseline.

---

# 3. P1 — LiveRec Twitch 100k external validation — ACTIVE

## Scientific question

> **Does conditional relationship-memory utility transfer to a different live-stream platform with dynamic availability and repeat consumption when evaluated against a strong domain-specific base?**

This is cross-platform validation of the conditional-specialist principle. It is not intended to reproduce KuaiLive's room-vs-streamer identity geometry.

## Frozen official lineage

Pin official `JRappaz/liverec` source at commit:

`27eaf33d258d1c1ea2d6da1da81a5360e8c8ce6b`

Primary base configuration follows the official launcher:

- model `LiveRec`;
- `fr_ctx = true`;
- `fr_rep = true`;
- `seq_len = 16`;
- `dim = 64`;
- `lr = 5e-4`;
- `l2 = 0.1`;
- official availability-aware candidate ranking;
- dev-only early stopping;
- no test tuning.

## P1.0 — Data/protocol audit — CLOSED / PASSED

Workflow run: `35582379331`.

Audit reproduces:

- 3,051,733 rows;
- 100,000 users;
- 162,625 streamers;
- `max_step=6148`;
- `pivot_1=5648`;
- `pivot_2=5898`;
- `seq_len=16`;
- official availability `start <= s < stop`.

Targets:

- train 99,299;
- dev 46,878;
- test 44,221.

Repeat-target fraction:

- train 48.62%;
- dev 52.36%;
- test 54.91%.

Active candidate counts are roughly 800 per event and every audited target is active.

## P1.1 — Strong LiveRec base reproduction — NEXT / START NOW

Goal: reproduce the official LiveRec architecture and dev selection under modern dependencies before introducing Memory.

### Protocol

1. pin official source commit above;
2. download the same Twitch 100k benchmark mirror used by P1.0;
3. use the official train/dev sequence and availability semantics;
4. preserve official `fr_ctx` and `fr_rep` components;
5. use dev-only early stopping;
6. do **not** tune on test;
7. freeze model checkpoint + dev metrics + runtime environment as an artifact.

### Runtime rule

If the 2021 implementation requires compatibility changes under modern PyTorch, changes must be behavior-preserving and documented. Do not alter target construction, candidate availability, architecture, or loss merely to make the code faster.

### Base reproduction pass condition

- training executes without NaN/divergence;
- dev ranking metrics are finite;
- active-only ranking semantics are preserved;
- repeat/new target metrics are produced;
- no test metric is used for model selection.

A historical-paper metric mismatch is not by itself a failure if code/runtime differences are documented and the reproduced implementation is faithful.

## P1.2 — Dev-only Memory + utility-gate fitting — AFTER P1.1

Freeze before test:

### Explicit relationship MemoryFusion

For each available streamer using history strictly before target:

- short-term recency relationship;
- long-term normalized visit frequency;
- train-only global popularity.

Frozen transferred combination:

`MemoryFusion = 0.45 * short + 0.45 * long + 0.10 * popularity`.

### Utility features

State:

- log history length;
- repeat rate;
- preference entropy;
- recent-vs-older drift;
- temporal regularity;
- state complexity.

Base confidence over the legal active candidate universe:

- std/range;
- top-score margins;
- top-score z;
- normalized softmax entropy;
- top-10 softmax mass.

### Gate

- primary HGB family frozen from KuaiLive;
- dev target = event-level `Memory NDCG@10 − LiveRec NDCG@10`;
- 5-fold OOF dev utility predictions for threshold selection;
- final model fit on all dev.

### Generic-difficulty control

Fit a same-feature base-difficulty HGB and compare at exactly the primary router's invocation budget K.

## P1.3 — Untouched one-shot test — AFTER P1.2

Only after base + memory + gate are frozen:

Primary rows:

- strong LiveRec Base;
- Always Memory;
- Selective Memory;
- matched-budget Difficulty Router;
- exact-K Oracle as analysis-only headroom.

Report:

- NDCG@10;
- HR/Recall@10;
- invocation rate;
- repeat vs novel target breakdown;
- candidate-count distribution;
- utility strata;
- >=5,000 paired user bootstrap resamples.

### Primary success rule

`Selective − LiveRec Base > 0` and bootstrap 95% CI lower bound > 0.

### Mechanism replication rule

Prefer `Utility Router − Difficulty Router > 0` with positive paired CI.

### Failure rule

If null/negative:

- no test rescue tuning;
- preserve result;
- narrow cross-platform generalization claims;
- treat outcome as a boundary condition consistent with regime-dependent specialist utility.

---

# 4. Manuscript work in parallel

Do not wait for P1 to draft.

Immediate writing/figure tasks:

1. Figure 1 — framework concept.
2. Figure 2 — sampled + full-active utility stratification, matched-budget difficulty comparison, oracle headroom.
3. Figure 3 — regime transition map showing Memory−Base and invocation across sampled LOO, full-active LOO, GTS-Last, GTS-Successive.
4. Table 1 — sampled identity-aware effectiveness.
5. Table 2 — full-active strict-transfer/native effectiveness.
6. Table 3 — sampled/full-active information ablations.
7. Accuracy–latency–invocation table/figure.
8. Related Work — explicitly add Learning-to-Defer lineage and DCGLive protocol distinction.
9. External validation section shell — fill only after P1.3.

---

# 5. P2 — OPTIONAL after P1 / manuscript freeze

## P2.1 KuaiLive-M3

Useful contemporary within-ecosystem validation, but weaker externality than Twitch.

## P2.2 Richer uncertainty estimators

Low priority. The paper is not an uncertainty-estimation competition.

## P2.3 DCGLive-adapted

Only on explicit reviewer demand. Label as adapted and enumerate all protocol changes.

## P2.4 Secondary outcomes

Repeat/novel, head/tail, engagement/satisfaction only when labels support them. No causal business claims.

## P2.5 Genuine LLM/agentic extension

Separate paper direction; do not rebrand MemoryFusion.

---

# 6. No-go list

Do not:

- add more sampled-negative seeds;
- reopen identity controls without a concrete reviewer failure mode;
- retry official room-ID DS-Frame full-softmax on the million-room universe;
- retrofit every robustness experiment to Ridge;
- add broad generic backbone families;
- retune after P1 test inspection;
- treat generic deferral/routing as the paper's novelty;
- claim Memory is globally inferior or globally superior independent of regime.

---

# 7. Stopping rule

For an ESWA-first strategy, the KuaiLive internal evidence chain is already submission-grade; P1 is a high-value generalization test, not an internal-validity rescue.

For KBS / Information Sciences, successful P1 becomes more important because the conceptual framing is broader.

Once P1.3 is frozen, do not add P2 unless it answers a specific reviewer-risk question. Move directly to manuscript completion and submission package preparation.

---

# 8. Final hierarchy

> **P0 = CLOSED.**  
> **P1.0 = CLOSED / PASSED.**  
> **P1.1 = NEXT: reproduce and freeze official strong LiveRec base.**  
> **P1.2 = then fit Memory/utility gate on dev only.**  
> **P1.3 = then evaluate untouched test once.**  
> **P2 = optional only after the external result is frozen.**

The project is now in **external validation + manuscript freeze**, not architecture expansion.