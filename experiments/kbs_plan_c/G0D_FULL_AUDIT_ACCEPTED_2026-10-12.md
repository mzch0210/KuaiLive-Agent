# Plan C G0-D: accepted corrected full KuaiLive-M3 audit

**Status: VALID aggregate source audit / G0-D source-quality gate PASS.** The source-level structural eligibility check passes; the candidate/task protocol, row-level chronological split and new-trained DEV gate remain pending.

## Exact execution and provenance

- **Successful checkout-free User-host audit**: [GitHub Actions #38203111463](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38203111463); corrected aggregate artifact ID `11726179513`, file `full_source_audit_corrected.json`.
- Failed direct checkout-based attempt: [#38202905687](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38202905687). Checkout-free source transfer via `actions/cache` is the successful fallback, consistent with GitHub's cache-service semantics.
- Pinned official M3 revision: `138d213a23e261ed3094d27ed8a4b867fb9143fe`; two raw input files SHA256 reverified on this run. Code reports `kbs-plan-c-g0d-full-aggregate-v2`.
- Aggregate audit reported no exported event-level identities, model training, TEST scores or ranking metrics.

## Full-scan empirical results

| Audit statistic | Observed |
|---|---:|
| Raw live interaction rows | **35,806,596** |
| Live-room metadata rows | **6,564,013** |
| Rooms with parseable valid lifecycle | **6,537,125** |
| Room records with missing identity/time | **26,888** |
| User IDs observed | **21,938** |
| Author IDs observed | **1,061,343** |
| Distinct observed user-author pairs | **8,330,791** |
| Repeated user-author pair events (global, NOT per-target past) | **27,475,805** |
| Events matched to a room ID | **35,586,361** |
| Room IDs absent from valid metadata | **220,235** |
| Matched sessions where play starts outside room lifecycle | **153,955** |
| Session exits after recorded room end | **529,189** |
| CSV adjacent backward timestamp transitions | **17,825,705** |
| Median per-user interactions | **753** |
| Median distinct authors per user | **189** |
| Concurrent live-room count, sampled median | **37,406** |
| Concurrent live-room count, sample 10th–90th percentiles | **25,621–56,106** |

The above flags are not necessarily mutually exclusive. E.g. exiting beyond a room end does not imply that the play *began* when the room was unavailable. E1 must enforce entry-time eligibility `start ≤ play_start < end`, author identity match, and other preregistered filters. Active **rooms** may map to repeated authors: 37,406 is **not** a validated unique-active-author count.

## Temporal split diagnostics

- Raw event timestamps are ISO-like strings; room Parquet timestamps are native Arrow `timestamp[us]`. The parser converts both to epoch ms while treating timezone-naive source clocks as UTC *solely for internal consistent ordering*; upstream timezone is **not established**.
- Date range according to that internal convention: `2026-03-03` to `2026-03-31`. Public documentation presents the collection window as March 4–31. Do not claim the data physically begins in UTC on March 3 based on a naive timezone assumption.
- Cumulative event-count split *unfrozen proposals*: 70% at **2026-03-23 11:00** and 85% at **2026-03-27 13:00** on the internally assumed UTC clock.
- File has >17.8M adjacent time reversals; training/user Memory history needs explicit chronological ordering and deterministic ties.

## Eligibility of a fresh confirmation set

The KuaiLive original release is documented for May 2025, whereas M3 is documented for March 2026. This is a valid **different-collection-period** replication opportunity. Cross-release anonymized user identifiers cannot establish person-level disjointness; never claim it has been proven.

## Scientific decisions / outstanding G0-F gates

1. Rank **authors** (to make repeated relationship identity explicit); the older KuaiLive ranks rooms, so avoid claiming an identical task replication.
2. Require valid matched room and target play-start within room lifecycle; use a train-known author target universe for meaningful Base comparisons. Quantify coverage by split and report exclusions before any TEST metric.
3. Use one global chronological TRAIN→DEV→TEST boundary protocol, avoiding the official per-user 80/10/10 benchmark's future-data pooling.
4. Pre-register an efficient deterministic DEV/TEST evaluation cohort, document active eligible author candidate counts, and implement leakage-free chronological training histories.
5. Restrict rank/effect-size metrics and gate threshold selection to DEV until all E1–E3 policies and source identities are frozen.

The 2026-10-12 **first attempt** [#38202577543](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38202577543) wrongly encoded ISO/datetime source timestamps as integer; its all-invalid output is **discarded as scientifically invalid**, not a negative result. Correction provenance is retained in [G0D_AUDIT_CORRECTION_STATUS_2026-10-12.md](G0D_AUDIT_CORRECTION_STATUS_2026-10-12.md).
