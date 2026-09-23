# KBS Context-Length Intervention Repair Evidence

**Status:** CLOSED / SUCCESS  
**Scope:** DEV-only context-length intervention aggregation repair  
**GPU retraining performed:** no  
**P1.3 TEST ranking inspected:** no

## Immutable inputs

- Original GPU intervention run: `35830028173`
- GPU artifact: `kbs-context-length-gpu-35830028173`
- GPU artifact ID: `10752233546`
- GPU artifact digest: `sha256:63b2c7397f32fccfb297b0291d7d4e09f0645d348efe548c9d9d33e55f0a1fb6`
- Frozen P1.2 run: `35698158121`
- Frozen P1.2 artifact ID: `10680854557`
- Frozen L16 OOF SHA256: `9757064252c097934fa31f10a68e11bb43853ca1132aaa49da2b9794f60d3816`

Repair workflow:

- Run: `35877647543`
- Commit: `7305cf890d3d15ffcf98bb0399b64ab091398e60`
- Output artifact: `kbs-context-length-aggregate-repaired-35877647543`
- Output artifact ID: `10757614400`
- Output artifact digest: `sha256:f368adddb32a22d5a6d909e91f164453c2d025b72ce59ff164db8d770c03abc6`

## Root cause

The first hosted aggregation correctly failed closed because the L8/L32 evaluator reused a later relationship-Memory history helper whose eligibility rule differed slightly from the immutable frozen P1.2 exporter.

Frozen P1.2 used all user interactions with `start < target_step`. The later helper additionally filtered rows by a split-end `stop` criterion. This affected only a boundary subset but violated the intervention requirement that auxiliary Memory remain identical across Base context lengths.

Observed drift relative to frozen P1.2, identically for L8 and L32:

- history-length mismatch: 50 / 46,878 users
- total history-count difference: -51 interactions
- Memory-rank mismatch: 15 / 46,878 users
- Memory-NDCG mismatch: 14 / 46,878 users
- mean raw Memory-NDCG difference: `+3.9039818527e-05`

A second provenance-only issue was also found: the original GPU `SHA256SUMS` manifest included its own file. The repair workflow verifies every payload entry while excluding only that self-referential manifest line. No scientific data file is excluded from checksum verification.

## Repair principle

The repaired aggregation does **not** loosen the Memory-invariance guard.

Instead:

1. the immutable frozen P1.2 L16 event-level artifact is the canonical source for `memory_rank0`, `memory_ndcg10`, `history_len`, and `seen_before` for all context lengths;
2. L8 and L32 artifacts contribute only their independently trained Base outputs and their `recent_visible` status;
3. each context-length state is reconstructed as:
   - `recent-visible` if the target is visible in that Base context;
   - `long-horizon-only` if it is not visible but exists in canonical pre-target history;
   - `unseen` otherwise;
4. the only scientific intervention variable is therefore Base `seq_len`.

All guards passed:

- same event identity across L8/L16/L32;
- canonical Memory rank invariant;
- canonical Memory NDCG invariant;
- canonical history invariant;
- represented set nested as `L8 ⊆ L16 ⊆ L32`;
- unseen set invariant;
- no P1.3 TEST ranking inspected.

## Overall DEV results

| Base context | Base NDCG@10 | Canonical Memory NDCG@10 | Memory−Base | 95% bootstrap CI |
|---:|---:|---:|---:|---:|
| 8 | 0.52619 | 0.52170 | -0.00450 | [-0.00756, -0.00127] |
| 16 | 0.57185 | 0.52170 | -0.05016 | [-0.05307, -0.04731] |
| 32 | 0.59663 | 0.52170 | -0.07493 | [-0.07766, -0.07227] |

## Base-relative evidence-state results

| Context | State | n | Memory−Base | 95% bootstrap CI |
|---:|---|---:|---:|---:|
| 8 | recent-visible | 19,486 | +0.00271 | [-0.00039, +0.00582] |
| 8 | long-horizon-only | 10,934 | +0.26042 | [+0.25288, +0.26779] |
| 8 | unseen | 16,458 | -0.18904 | [-0.19383, -0.18442] |
| 16 | recent-visible | 24,541 | -0.01995 | [-0.02286, -0.01681] |
| 16 | long-horizon-only | 5,879 | +0.23097 | [+0.22191, +0.24034] |
| 16 | unseen | 16,458 | -0.19562 | [-0.20038, -0.19111] |
| 32 | recent-visible | 28,158 | -0.02309 | [-0.02616, -0.01995] |
| 32 | long-horizon-only | 2,262 | +0.18861 | [+0.17526, +0.20265] |
| 32 | unseen | 16,458 | -0.19985 | [-0.20448, -0.19505] |

## Transition evidence

The key intervention diagnostic compares the same events as Base visibility expands.

### L8 → L16

`recoverable-but-unrepresented → represented`:

- n = 5,055
- specialist-minus-base utility: `+0.29388 → -0.15360`
- change: `-0.44748`
- 95% bootstrap CI: `[-0.45767, -0.43730]`
- Base change: `+0.44748`
- Memory change: `0`

### L16 → L32

`recoverable-but-unrepresented → represented`:

- n = 3,617
- specialist-minus-base utility: `+0.25755 → -0.17474`
- change: `-0.43229`
- 95% bootstrap CI: `[-0.44381, -0.42054]`
- Base change: `+0.43229`
- Memory change: `0`

### L8 → L32

`recoverable-but-unrepresented → represented`:

- n = 8,672
- specialist-minus-base utility: `+0.27782 → -0.14114`
- change: `-0.41896`
- 95% bootstrap CI: `[-0.42685, -0.41112]`
- Base change: `+0.41896`
- Memory change: `0`

## Interpretation boundary

These DEV-only intervention results strongly support a Base-relative visibility interpretation: when the same persistent relationship evidence becomes represented by a larger Base context, its marginal specialist value falls sharply. The result is not a universal causal theorem, does not establish that context length is the only determinant of utility, and must not be used to reselect or retune the frozen P1.3 TEST policy.
