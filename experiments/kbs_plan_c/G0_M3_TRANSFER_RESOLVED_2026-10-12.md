# G0-D KuaiLive-M3 data transport resolved (2026-10-12)

**Status: source transport VERIFIED / G0-D source availability PASS.** This closes the network transfer blocker; it does **not** complete temporal/candidate/cohort-independence auditing or authorize training on TEST.

## Exact official source and User-host files

- Source: [KuaiLive-M3 on Hugging Face](https://huggingface.co/datasets/imgkkk2004/KuaiLive-M3); pinned source commit `138d213a23e261ed3094d27ed8a4b867fb9143fe`.
- User-host persistent directory: `/home/kuailive-runner/.cache/kuailive-agent-kbs/klm3`.
- `live_interaction.csv`: 4,565,993,701 bytes; SHA256 `2db0daab66ec18062d453cdbbc43cbb44f75559914ef53756dfd6635812ec653`.
- `live_room_meta.parquet`: 237,756,481 bytes; SHA256 `130986065f8fff7cb1146a7c6508979cf0df60f39a7d923f35003e1f29f0599a`.
- The two original files were validated against pinned upstream checksums on GitHub-host, then revalidated after unpacking on User-host. The final persistence integrity check passed.

## Audit evidence

| Run | Result | Scientific/engineering status |
|---|---|---|
| [Hosted connection probe #38200877497](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38200877497) | Success | Hugging Face API and redirected CDN byte-range accesses succeeded |
| [Hosted M3 schema check #38200961749](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38200961749) | Success | Verified complete 238 MB Parquet source; 6,564,013 room records. Interaction CSV verified header from 2 MB prefix |
| [Source/cache relay #38201166805](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38201166805) | Overall failure, **both-host data transfer and SHA checks passed** | GitHub-host downloaded exactly two files, verified SHA, transferred 1,560,350,070-byte compressed Actions cache. User-host received, decompressed and rehashed. Final job failed because pre-existing empty/partial `klm3` cache directory lacked `SHA256SUMS` |
| [Atomic finalize #38201467479](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38201467479) | Overall failure, **persistent install and rehash passed** | Old incomplete cache moved to quarantine; verified staged files installed at exact persistent path. Reporting-only command failed because system `python` was not on PATH |
| [Final User-host verification #38201535594](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38201535594) | **Success** | Full two-file SHA recheck, 5,000-row interaction schema sanity check; compact report artifact [11725177152](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38201535594/artifacts/11725177152) |
| [Intermediate cache cleanup attempt #38201618502](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38201618502) | Failure | Exact temporary cache deletion via GitHub-host GITHUB_TOKEN returned HTTP 401; intermediate Actions cache may remain until removed with valid credentials or evicted. Does **not** affect User-host verified source |

## Confirmed data schema

- `live_interaction.csv` columns: `user_id`, `author_id`, `live_id`, `live_play_start_timestamp`, `live_play_end_timestamp`, behavior and count fields.
- `live_room_meta.parquet` columns: `author_id`, `live_id`, `live_name`, `start_timestamp`, `end_timestamp`, `live_duration`.
- Final User-host audit checked 5,000 rows for all required identity/timestamp fields, **zero missing required values in that bounded sample**.
- Parquet footer was inspected successfully on GitHub-host; User-host's initial virtualenv lacked `pyarrow`, so its final report explicitly says footer_check=false instead of inventing success.
- Neither source checksum nor header audit establishes temporal eligibility, available candidates or lack of historical dataset overlap.

## Next scientific gate

Perform G0-D full time-eligibility, repeated-user/author histories, room availability and original KuaiLive source-overlap audit on User-host with streaming processing, **without examining held-out ranking outcomes**. Then fix a single E1–E3 protocol, only afterwards launch GPU Base training and DEV OOF gate comparison.

## Efficiency and reuse

Do not re-download the same M3 source. All further experiments should reuse validated local `klm3/SHA256SUMS` under the 3090 runner cache. Do not upload raw interaction rows to public GitHub Actions artifacts or commit them to Git. The intermediate 1.56 GB Actions cache was an emergency relay of already-public CC BY-SA-listed source and is not the durable scientific record.
