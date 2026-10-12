# Plan C G0-D status and audit correction — 2026-10-12

**Status:** Source-verified M3 files present on User-host; corrected full temporal/candidate eligibility audit still pending; *not authorized* to freeze E1–E3 experiment protocol or run held-out TEST.

## Reproducible progress

- User-host raw source inputs verified by SHA256; see [G0 transfer record](G0_M3_TRANSFER_RESOLVED_2026-10-12.md).
- Published datasets have different observed collection periods: original KuaiLive **2025-05-05 to 2025-05-25**, KuaiLive-M3 **2026-03-04 to 2026-03-31**. This supports different-period replication only, not verified real-user disjointness (different anonymization).
- First complete [G0-D run #38202577543](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38202577543) read 35,806,596 interaction rows and 6,564,013 metadata rows; **its eligibility statistics are invalid**: all rows falsely coded missing due to an incorrect integer-only timestamp parser. *No performance metrics were calculated or used.*
- [Type-only audit #38202793392](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38202793392) confirmed actual source representation: interaction timestamps are **ISO-8601-like strings**; Parquet room boundaries are **Arrow `timestamp[us]`** and convert to Python `datetime`, not integer epoch fields.
- Parser corrected in `analysis/kbs_plan_c/g0d_full_audit.py`, with targeted unit tests and hard fail-on-zero-valid-room/user/eligibility checks. Naive source timestamps are consistently assigned UTC for analytical ordering; this is **not** a claim that upstream logs have explicitly documented UTC timezone.
- [Corrected direct run #38202905687](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38202905687) has passed hosted tests, but the User-host checkout step is affected by intermittent GitHub access; aggregate results unverified.
- [Checkout-free fallback #38203111463](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38203111463) packages the corrected code on GitHub-host with checksum in Actions cache and can restore/execute it on User-host *without* contacting github.com from the server. Hosted packaging PASS; User-host execution is pending runner availability.

## G0-D acceptance conditions

Only accept a final JSON from `kbs-plan-c-g0d-full-aggregate-v2` with a source byte rehash, >=1M valid room IDs, >=30M event rows, >=15k valid unique users, positive room-to-event match count, nonempty date range and available-room sample, and no exported event-level rows or held-out ranking metrics.

Do not treat the first all-zero/invalidity report as dataset evidence; do not train on `TEST` or change eligibility after viewing predictive TEST utility. Further work after corrected aggregate audit: inspect temporal consistency, freeze the exact global TRAIN/DEV/TEST clock boundaries, define author/room candidate matching and Base/Memory label construction, then move to E1/E2 shared DEV pipeline.

## Evidence policy

Preserve both failed and successful runs; do not conceal negative results, conflate scientific invalidity with a negative result, or reinterpret observed source identities as verified cross-dataset user matches.
