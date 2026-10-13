# N9–G3 | Validated time/activity-preserving relationship identity placebo pilot

**2026-10-13 | 128-event DEV pilot: structural and original-score parity PASS, predeclared non-floor gate PASS. Full E3b experiment NOT DONE; no independent TEST or final causal claim.**

## 1. Executed verification sequence

1. [Metadata-only eligibility #38389532148](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38389532148) established the 35,432,406-row sealed causal history, 6,537,125-row active-room interval source and original DEV clocks.
2. [First structural pilot #38390243060](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38390243060) selected **128 chronologically stratified events from the final DEV quartile**, 126 users, and 547,992 earlier source interactions; found 550 occupied 1-hour windows with cross-user / cross-author candidate swap opportunities.
3. [Strict cross-active eligibility #38390834055](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38390834055) repaired a microsecond/nanosecond bin-width error, then verified 63,619 disjoint swaps touching 127,238 interactions (23.22%), all before earliest pilot target. Exactly preserved per-hour author interaction counts, each user's interaction count and timestamps, and swapped authors' presence in the room-availability source at both corresponding interaction times.
4. [Private intervention snapshot #38391152867](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38391152867) reproduced the same swaps, kept raw event and author IDs in a restricted self-host cache **only**, and exported no user-level rows.
5. [Memory F/S scoring pilot #38391389532](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38391389532) reproduced the original Full and Long-only ranking scores **event-by-event** against original frozen B1/B2; recomputed fixed Memory after swap; original source hashes and non-floor gate PASS.

Original author ranker and Base weights remained fixed; all results are DEV-only. The historical activity null is a time-respecting, marginal-preserving **pilot design**; see the analogous temporal degree-preserving null-model principles in *Randomizing growing networks with a time-respecting null model* (Physical Review E, 2018, DOI 10.1103/PhysRevE.97.052311). It does not make the present implementation automatically a formal causal intervention or future-time replication.

## 2. Observed pilot ranking quality

| Memory score | Original F | Co-active history-null F | Original offline sampled S | History-null sampled S |
| --- | ---: | ---: | ---: | ---: |
| Full Memory | 0.396585 | 0.384386 | 0.661360 | 0.669835 |
| Long-only | 0.343834 | 0.338663 | 0.735098 | 0.729292 |
| Popularity-only reference | 0.037155 | unchanged | 0.229421 | unchanged |

The Full Memory original-minus-null F gap is **0.012199**. Under target-retained sampled S, the original-minus-null Full gap is **-0.008474**, i.e. slightly negative on these selected pilot events. Original Long-minus-null gaps are 0.005170 (F) and 0.005806 (S).

The original Full F rank is relevant in 72/128 events; null Full F remains relevant in **68/128**. The null's F NDCG 0.384386 is far above popularity-only 0.037155. Thus the control **does not suffer the severe floor effect** of the original B2 within-event cyclic-placement null.

## 3. Why this is not yet an identity-specificity result

- This was a **non-random retrospective 128-event pilot from the latest chronological DEV quartile**, not a representative sample of all 50,049 DEV events or a new independent TEST.
- The 23.22% change applies to **prefix history of 126 selected users**, not to all user–creator relations at all times. Later histories remain unchanged to avoid future information.
- Temporal bin, user activity and author degree constraints are exact within the selected subset; these do not guarantee preservation of all higher-order co-consumption patterns, repeated pair counts or expert score strength across the full cohort.
- Although the pilot is *non-floor*, the Full Memory original-minus-null difference is small and opposite-signed across F and S. No pilot user-bootstrap interval or preregistered null distribution was calculated; **neither a causal gain nor a population-null effect is established**.
- True and null paths were scored under the same original candidate rosters, with target identity used **for offline evaluation only**. No target information was used to choose historical swaps.

## 4. Next experiment gate and efficiency choice

The predeclared **non-floor feasibility gate PASS** means a meaningful fuller E3b could be undertaken. It does **not authorize** labeling R3 STRONG immediately.

Before investing in 50,049-event full DEV rewiring, a time-leakage-safe full-cohort protocol must be fixed. A naive global swap using later interactions from the same time bin to alter an earlier DEV request would use information unavailable at that request. An acceptable design applies author-activity swaps only after each time bin has closed (or restricts interventions to a historical prefix strictly preceding all evaluated requests), specifies the exact resulting estimand, and preserves room eligibility. It must report paired user intervals, realized specialist calls, identity coverage, and whether the null has enough useful ranking signal. Do **not** equate the existing selected-user prefix pilot with a fully causal relation-identity ablation.

**Decision:** G3 pilot **PASS**; full E3b candidate design and resource gate **PENDING**. Progress to G4 scientific assessment only with evidence-tier BOUNDED, or execute one lawful and temporally valid expanded test before stronger claim. No modifications to eight-section main article or S1–S10 are made at this point.

Evidence source: `experiments/kbs_plan_c/N9_G3_CROSS_ACTIVE_NULL_128_DEV_PUBLIC_AGGREGATE_2026-10-13.json`; pilot code `analysis/kbs_plan_c/n9_g3_private_rewire_memory_parity_pilot.py`, restricted swap source `analysis/kbs_plan_c/n9_g3_private_rewired_prefix_snapshot.py`.
