# Route B B4-A — A0/A1 eligibility, history-exposure and blind sample freeze

**Date 2026-10-14 | A0 TECHNICAL PASS; A1 SAMPLE SHA-SEALED PASS; A2/A3/A4 NOT STARTED; SUBMISSION HOLD.**

## Scientific and ethics interpretation

This is an *additional held-out TARGET evaluation in the original M3 collection interval*, **not** a newly sampled chronological external TEST. G1 and G5 have already processed the full eligible event stream, including residual TEST history. Only the **ranking target sets** are disjoint from G5's selected evaluation targets. Unexposed/outcome-blind status is **restricted to the new policy/evaluation pipeline**, not a claim that event author identifiers have never been processed by any program.

The official Hugging Face KuaiLive-M3 listing currently shows `cc-by-sa-4.0`, while the separate original KuaiLive project explicitly uses CC BY-NC-SA 4.0. Original source version, any applicable M3-specific license and restrictions on private derived relationship data require accountable human confirmation prior to publication or expanding privileges. No raw author/user interaction records were uploaded.

## A0 — executed private cohort count

- [GitHub Actions #38505464173](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38505464173): **SUCCESS**. Historical original G1 source, old G5 sealed TEST cohort and TRAIN-known author set byte SHA256 matched their locked manifest.
- G1 room/time-eligible original TEST events: **5,124,893**; original G5 selected ranking targets: **47,575**.
- Remaining events with **TRAIN-known target author and prior_events>=2**, excluding every original G5 target ID: **4,723,652** events from **21,565** users. Old G5 target event-ID overlap: **zero**.
- Events whose users do **not** appear in original G5 target users: **437,049 events / 9,033 users**. User-disjoint tests remain only a potential sensitivity analysis, not a separate forward-time cohort.
- Source days and counts: March 27 382,408; March 28 1,210,988; March 29 1,218,047; March 30 1,131,623; March 31 780,586. G1 clock is source timezone-naive, not physically verified UTC.
- Read original existing causal stream and TRAIN-known author eligibility inside private DuckDB SQL; output only counts and source SHA status, no target author, NDCG or model predictions. Aggregate source: `experiments/kbs_plan_c/N9_ROUTE_B_B4A_A0_AGGREGATE_ELIGIBILITY_2026-10-14.json`.
- Initial A0 Action #38505388815 failed at **DuckDB module import** before querying. The successful retry used the previous G1 locked isolated DuckDB 1.4.1 environment; source bytes unchanged.

## A1 — executed label-free event selection and immutable private SHA

- [GitHub Actions #38505873258](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38505873258): **SUCCESS**, and full private output sealed at `~/.cache/kuailive-agent-kbs/klm3_n9_route_b_b4a_a1_30000_4096_v1`. No target author columns, model training, ranking scores or target NDCG in the files.
- Main B4-A target set: **30,000 events / 10,387 users**; SHA256 **`be96c9dbf13a14e0db85df24202e318b691b41a4250a3f5e9bc877d4e28d1e14`**.
- Mechanism subset *within that main set*: **4,096 events / 3,059 users**; SHA256 **`40c950e6a9d79ce3e4330b8b8f434dda764570fd369bdeb83a7b4d587c00d059`**.
- Original G5 target event ID intersection: **zero**. Both selections are deterministic `SHA256(fixed task/seed || source_event_id)` priorities; their ranking **does not contain target author ID, target-specific NDCG, or Memory gains**.
- Main selection is **5 dates × 4 within-date ranks of pretarget history length**, 1,500 per cell (20×1,500=30,000). Original proposal of a uniform 5-date×3 absolute-count stratification failed before sampling: very few TEST events had only 2–9 prior interactions (e.g. March 27 had 8), and some 10–49 strata had under 2,000. A pure metadata-only diagnostic disclosed these group counts. The replacement *within-day pretarget-history rank quartiles* was made **before any selection result or target outcome was read**, with a new code SHA. Two failed attempts (#38505673902 and #38505766001) produced no sample.
- The 4,096-event nested subset is independently hash-ranked over the sealed 30,000 main events; individual cell counts are public. The private event lists and user/time columns remain self-host only. Aggregate: `experiments/kbs_plan_c/N9_ROUTE_B_B4A_A1_SEALED_SAMPLE_PUBLIC_2026-10-14.json`.

## Essential inferential and execution safeguards before A2

1. **Stratification estimand:** Equal-sized date×history cells **do not** reproduce original event prevalence (March 27 is oversampled, among others). A2 must predeclare the **primary statistic** as either the balanced-cell target distribution or a **population-weighted mean using 20-cell eligibility counts**. Recommend naturally weighted eligible-source-event mean as *primary* and 20-cell balanced mean as *sensitivity*. Derive weights from A0/A1 pretarget metadata **before target reveal**. Cluster-by-user resampling must respect the defined target estimand. Do not opportunistically switch weights after seeing results.
2. **A2 DEV-only fixed models:** the nested 5×4 B1 OOF DEV results are **not** a single already deployable frozen gate for B4-A. Fit one final SASRec/GRU4Rec × F/S HGB gate using the old 50,049 DEV source only, with pretarget 12 features, and define their decision thresholds on **user-disjoint DEV OOF**. Freeze model checkpoints, features, seeds, threshold decision tie policy, and predicted resource calls.
3. **Future-history / roster parity:** A3 must compute all 30,000 cases without accessing **same-request author**. The full causal stream may contain earlier TEST interactions, which are allowed only after they have occurred. Candidate roster is full-active TRAIN-known authors, and original G5 score semantics must be source-SHA-verified.
4. **Mechanism comparator:** fixed predeclared 4,096 requests, same F universe and three previously fixed closed-hour author-active relation-null seeds. Complete all blinded null top-10 before a single target reveal. Verify non-floor after reveal, reporting invalid negatives faithfully.
5. **Owner license and research use:** prior A0/A1 technical work on an existing permitted host is not human attestation of precise dataset version rights; authors must review the fixed M3 license, privacy, publication and AI disclosure before A2/A4 administrative GO.
6. **No G5 TEST reopening, no new chronological data, no current B4-A label reveal, no main manuscript change.** B4-A A2/A3/A4 currently **HOLD**.

### Exit state

**A0/A1 technical package is successful and strictly source/target-blind in the stated sense; A2 full DEV model freeze, A3 target-blind scores, and A4 one-shot target reveal remain for a separate controlled step.** Publication evidence is not upgraded until frozen A4/A5 are completed and validated.
