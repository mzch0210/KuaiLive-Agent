# KBS evidence-state closure results

**Status:** completed hosted analysis  
**Workflow run:** `35829433706`  
**Controller commit:** `c1eb7ddc80a51ca80728ebc9d8bac7f6e8ca6f1f`  
**Scope:** frozen-data analysis only; no P1.3 TEST ranking was inspected.

This file preserves the compact scientific outputs of the completed hosted P0/P1 closure analyses. It is an evidence summary, not a protocol or manuscript outline.

## 1. Twitch / LiveRec frozen DEV evidence-state closure

Frozen P1.2 DEV events: `n = 46,878`. Exact matched invocation budget: `K = 6,563` (`14.0002%`). The reconstructed public Twitch history matched the frozen event history exactly (`missing_users = 0`, `missing_creators = 0`, `history_len_mismatches = 0`). The weighted state decomposition exactly reproduced the overall Memory-minus-Base mean.

### 1.1 Evidence-state summary

| Relationship state | Base-relative interpretation | n | Prevalence | Base NDCG@10 | Memory NDCG@10 | Memory−Base | 95% bootstrap CI | P(Δ>0) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| recent-visible | represented | 24,541 | 0.52351 | 0.85972 | 0.83976 | -0.01995 | [-0.02306, -0.01681] | 0.17420 |
| long-horizon-only | recoverable-but-unrepresented | 5,879 | 0.12541 | 0.30201 | 0.53298 | +0.23097 | [+0.22189, +0.24035] | 0.64382 |
| unseen | unavailable | 16,458 | 0.35108 | 0.23900 | 0.04338 | -0.19562 | [-0.20033, -0.19088] | 0.03743 |

Overall Memory−Base: `-0.0501572792`.

### 1.2 Utility vs Difficulty selection composition at exact same budget

| Router | Evidence state | Selection share | Population prevalence | Enrichment |
|---|---|---:|---:|---:|
| Utility | represented | 0.29697 | 0.52351 | 0.5673× |
| Utility | recoverable-but-unrepresented | 0.34131 | 0.12541 | **2.7215×** |
| Utility | unavailable | 0.36172 | 0.35108 | 1.0303× |
| Difficulty | represented | 0.11976 | 0.52351 | 0.2288× |
| Difficulty | recoverable-but-unrepresented | 0.20890 | 0.12541 | **1.6657×** |
| Difficulty | unavailable | 0.67134 | 0.35108 | **1.9122×** |
| Oracle | represented | 0.50389 | 0.52351 | 0.9625× |
| Oracle | recoverable-but-unrepresented | 0.42999 | 0.12541 | **3.4286×** |
| Oracle | unavailable | 0.06613 | 0.35108 | 0.1884× |

Interpretation supported by these frozen DEV diagnostics: generic Base Difficulty concentrates strongly on unavailable events, whereas Utility more strongly enriches recoverable-but-unrepresented events. This directly supports the distinction between Base difficulty and specialist solvability. Relationship-state labels remain analysis-only and were not selector inputs.

### 1.3 Alternative-explanation stratification within long-horizon-only events

The long-horizon Memory−Base effect remained positive with positive 95% bootstrap intervals across all quartile-like strata examined.

- **History length:** approximately `+0.217` to `+0.250` across strata.
- **Target creator prior exposure:** approximately `+0.154` to `+0.323` across strata.
- **Candidate count:** approximately `+0.212` to `+0.270` across strata.
- **User repeat propensity:** approximately `+0.187` to `+0.289` across strata.

These analyses do not establish causality. They show that the positive recoverable-but-unrepresented effect is not trivially eliminated by stratifying on any one of these observable factors.

## 2. KuaiLive candidate-regime evidence-state decomposition

Frozen test users: `n = 10,222`. The same events are evaluated under sampled-active and full-active candidate regimes, so evidence-state prevalence is identical by construction (`max absolute prevalence difference = 0`).

### 2.1 Aggregate regime reversal

| Regime | Base NDCG@10 | Memory NDCG@10 | Memory−Base |
|---|---:|---:|---:|
| sampled-active | 0.61714 | 0.56589 | -0.05125 |
| full-active | 0.39835 | 0.43202 | +0.03367 |

The state-weighted decomposition reproduced each aggregate Memory−Base value to numerical precision.

### 2.2 State-specific change from sampled-active to full-active

| Base-relative evidence state | n | Sampled Δ | Full-active Δ | Full−Sampled shift | 95% bootstrap CI |
|---|---:|---:|---:|---:|---:|
| represented | 4,589 | +0.11508 | +0.19261 | +0.07752 | [+0.07046, +0.08472] |
| recoverable-but-unrepresented | 206 | +0.17779 | +0.08049 | -0.09731 | [-0.14897, -0.04647] |
| unavailable | 5,427 | -0.20060 | -0.10251 | +0.09809 | [+0.08988, +0.10649] |

Because the event set and evidence-state composition are unchanged in this candidate-regime comparison, the aggregate sign reversal cannot be attributed to state-prevalence change here. It is associated with candidate-regime changes in state-specific Base-relative utility. This does not imply that temporal regime changes preserve state composition.

## 3. Execution and integrity

Both hosted jobs completed successfully with compilation, built-in self-tests, real frozen inputs, and protocol-invariant checks before artifact upload.

- Twitch artifact: `kbs-twitch-evidence-state-closure-35829433706`, artifact ID `10736088263`.
- KuaiLive artifact: `kbs-kuailive-regime-decomposition-35829433706`, artifact ID `10735459544`.
- Twitch analysis wall time: approximately `4.66 s`; peak RSS approximately `545 MB`.
- KuaiLive analysis wall time: approximately `1.53 s`; peak RSS approximately `228 MB`.

No CI success condition depended on the sign or favorability of the scientific result.
