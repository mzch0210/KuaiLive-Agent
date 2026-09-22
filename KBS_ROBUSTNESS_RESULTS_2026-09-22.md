# KBS DEV-only robustness results — Memory sensitivity and finite-context stress

**Snapshot date:** 2026-09-22  
**Repository:** `mzch0210/KuaiLive-Agent`  
**Scope:** post-P1.3 journal-strengthening analyses on frozen DEV evidence only.  
**Untouched-test ranking inspected:** **No**.

## 1. Memory-parameter sensitivity — CLOSED

GitHub Actions run: `35724784990` (`KBS Memory sensitivity DEV-only`)  
Artifact: `kbs-memory-sensitivity-35724784990`

The analysis replayed the frozen P1.2 DEV Memory calculation and varied the transferred Memory definition without refitting the scientific router or touching test ranking.

Integrity checks:

- DEV targets: 46,878;
- original frozen Memory replay rank mismatches: 0;
- maximum NDCG replay difference: `5.55e-17`;
- candidate reconstruction mismatches: 0;
- history reconstruction mismatches: 0.

Seven sensitivity configurations were evaluated:

- long-term weight: 0.30 / 0.45 / 0.60;
- short-history length: 5 / 10 / 20;
- short-term decay: 2 / 3 / 5.

All configurations preserved the principal relationship-horizon sign pattern:

- recent-visible: Memory−Base < 0;
- long-horizon-only: Memory−Base > 0;
- unseen: Memory−Base < 0.

Selected DEV NDCG@10 effects:

| Configuration | recent-visible | long-horizon-only | unseen | overall |
|---|---:|---:|---:|---:|
| frozen 0.45/0.45/0.10 | −0.01995 | +0.23097 | −0.19562 | −0.05016 |
| long weight 0.30 | −0.03744 | +0.13852 | −0.19520 | −0.07076 |
| long weight 0.60 | −0.00924 | +0.28231 | −0.19574 | −0.03815 |
| short K = 5 | −0.02644 | +0.23785 | −0.19562 | −0.05269 |
| short K = 20 | −0.01864 | +0.23030 | −0.19563 | −0.04956 |
| decay = 2 | −0.02512 | +0.23889 | −0.19562 | −0.05187 |
| decay = 5 | −0.01478 | +0.22027 | −0.19562 | −0.04879 |

Interpretation: the long-horizon mechanism is not an artifact of the single transferred Memory hyperparameter setting. Increasing long-term weight strengthens the long-horizon benefit while leaving unseen cases strongly harmful.

## 2. Finite-context stress test — CLOSED

GitHub Actions run: `35725938757` (`KBS finite-context stress DEV-only`)  
Artifact: `kbs-context-window-stress-35725938757`

This analysis used frozen DEV Base and Memory outcomes and reconstructed the distance to the most recent prior interaction with the target streamer. No model, Memory definition, or gate policy was retrained.

Integrity checks:

- DEV targets: 46,878;
- history reconstruction mismatches: 0;
- seen-before mismatches: 0;
- seen/unseen horizon mismatches: 0;
- frozen relationship-horizon counts replayed exactly: recent-visible 24,541; long-horizon-only 5,879; unseen 16,458.

### 2.1 The frozen LiveRec horizon is almost exactly a 16-interaction visibility boundary

Among seen-before events, the best simple cutoff is 16 prior interactions. It differs from the frozen recent-visible label on only 13 events out of 30,420 seen-before events (~0.043%).

At the 16-interaction split:

| Diagnostic group | n | Memory−Base NDCG@10 | 95% CI |
|---|---:|---:|---:|
| last seen within 16 interactions | 24,546 | −0.01980 | [−0.02288, −0.01666] |
| last seen beyond 16 interactions | 5,874 | +0.23057 | [+0.22143, +0.23953] |

This closely reproduces the frozen relationship-horizon result without using the horizon label itself.

### 2.2 Distance-bin stress test reveals a non-monotonic short-range pattern

| Last prior target-streamer distance | n | Memory−Base NDCG@10 | 95% CI |
|---|---:|---:|---:|
| 1–4 | 13,963 | +0.04606 | [+0.04276, +0.04938] |
| 5–8 | 5,556 | −0.06511 | [−0.07180, −0.05852] |
| 9–16 | 5,027 | −0.15268 | [−0.16096, −0.14455] |
| 17–32 | 3,621 | +0.25668 | [+0.24486, +0.26827] |
| 33–64 | 1,716 | +0.20707 | [+0.18985, +0.22384] |
| 65+ | 537 | +0.12965 | [+0.10092, +0.15807] |
| unseen | 16,458 | −0.19562 | [−0.20025, −0.19099] |

The finite-context mechanism is therefore **strong but not monotonic at very short recency**. Explicit relationship Memory is useful for extremely immediate repeats (1–4), harmful for the middle of the visible context (5–16), strongly useful once the relationship falls outside the 16-step context (17+), and strongly harmful when the relationship has never been observed.

### 2.3 Scientific interpretation

The primary mechanism claim remains supported and becomes more precise:

> The dominant complementary value of persistent relationship Memory appears when the target relationship lies outside the strong sequential base's finite 16-step context. However, there is also a distinct ultra-recent repeat regime (1–4 interactions) where explicit Memory adds positive value; the negative recent-visible aggregate is driven mainly by distances 5–16.

Accordingly, the manuscript should avoid a monotonic claim such as “the farther the relationship, the more useful Memory becomes.” A safer statement is that **Memory utility is structured by relationship visibility and recency regime, with a sharp positive shift beyond the finite context and a separate ultra-recent repeat pocket**.

## 3. Implication for the KBS manuscript

These two DEV-only robustness checks strengthen RQ3 without changing the frozen P1.3 result or the scientific gate:

1. the horizon sign reversal is robust to reasonable Memory parameter perturbations;
2. the 16-step finite-context boundary independently recovers the main long-horizon effect;
3. the distance-bin analysis identifies an additional non-monotonic short-range structure that should be presented as mechanism nuance rather than used for post-hoc routing redesign.

No test-based rescue tuning or new test access is justified by these results.
