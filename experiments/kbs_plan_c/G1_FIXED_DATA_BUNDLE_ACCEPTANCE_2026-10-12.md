# Plan C G1 — accepted reproducible forward-time author event bundle (2026-10-12)

**G1 result: PASS**. The new M3 source, time-forward split, chronologically ordered per-user histories, fixed deterministic DEV and sealed TEST panels are now present on User-host. Base training, gates and held-out TEST ranking evaluation have **not** been executed.

## Evidence

- [Successful real User-host G1 run #38204470450](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38204470450)
- Aggregate manifest artifact **11726687446** (`manifest.json`), produced under fixed DuckDB `1.4.1`.
- Scientific source: pinned M3 revision `138d213a23e261ed3094d27ed8a4b867fb9143fe` with raw source byte SHA256 independently verified.
- Protocol file: [G0F_PRETEST_PROTOCOL_2026-10-12.json](G0F_PRETEST_PROTOCOL_2026-10-12.json), SHA256 **`bf6234eb95ecb24a568b2e7556846c41c4f3e1fdcd7774397003beaf56341a3c`**.
- Time protocol uses **timezone-naive source clock ordering** (no physical UTC claim). Boundary TRAIN/DEV `2026-03-23 12:00:00`; DEV/TEST `2026-03-27 14:00:00`, equalities assigned to the later split.
- Warm author universe = authors in eligible TRAIN, **897,025** authors. Eligible target rows require matched room/author ID and `room.start <= play_start < room.end`.

## Accepted exact counts

| Category | Eligible events |
|---|---:|
| TRAIN | **24,995,148** |
| DEV | **5,312,365** |
| TEST | **5,124,893** |
| Frozen deterministic evaluation DEV cohort | **50,049** |
| Frozen deterministic evaluation TEST cohort | **47,575** |
| Eligible rooms in source | **6,537,125** |

Selected DEV/TEST cohorts are warm-author target events with at least 2 earlier valid user events and a fixed hash keep-rate; the output report includes no target ranking metrics. These cohorts were determined by the pre-specified source protocol, not by optimizing any TEST gain.

## Persistent output and checksums

Host root: `/home/kuailive-runner/.cache/kuailive-agent-kbs/klm3_plan_c_g1_v1`. Source raw files remain separately under `~/.cache/kuailive-agent-kbs/klm3`.

| Artifact | SHA256 |
|---|---|
| `train_author_events.parquet` | `c4bc640e6ee2ccf237960cb72fd586f169ee0bf77828e92dad7e95a5e47d9781` |
| `causal_stream_sealed.parquet` | `6cbc9b51935244f3e05c337b517e82680551532ec3d3d655de9c2e5ead4880f9` |
| `dev_cohort.parquet` | `b6cd7de4fac6246e4acf9c605c16c9dd033ce986c963985e7effd3e7497a4889` |
| `test_cohort_sealed.parquet` | `e60da60672ea1921dd3a5fccfb0aa76a3a06d50834e8080a07b2465777c9bdb1` |
| `train_known_authors.parquet` | `1cd2c1f281c1ca2f6ee1da32d568c693f8345489dc361f5a965049459091d9fe` |
| `available_room_intervals.parquet` | `e38c73ed00a43282c66153936828318108e60c71830bce2cadb970b04d8629e5` |

All files stay on User-host; GitHub artifacts contain only the aggregate manifest and fingerprints. G1 generation took approximately **22 seconds**, per the job manifest, after the User-host source and code-cache restore stages. Do not conflate G1 processing time with full training and scoring time.

## Scientific caveats

1. The official KLM3 target-only/CDR protocol splits each user chronologically 80/10/10, while our planned independent replication adopts a **global** forward-time split. Direct raw NDCG numbers are therefore not exchangeable.
2. Ranking target is **author**, unlike the original KuaiLive paper's room-ranking; compare relative decision value and direction, not unqualified identical-task performance.
3. Primary full-active candidate set uses distinct **TRAIN-known** live authors at each event time; candidate universe and performance are conditional on the warm-start target policy.
4. Previous C1–C3 Twitch and original KuaiLive evidence is unchanged and not retuned.
5. `causal_stream_sealed.parquet` includes chronological observations across segments for later causal state construction; training procedures must consume only `train_author_events.parquet`. Test cohort must not be used for model or gate optimization.
6. Full-active candidate feasibility in terms of *unique warm authors* is analyzed separately on DEV only, never inferred from the earlier full-source room-count median.
