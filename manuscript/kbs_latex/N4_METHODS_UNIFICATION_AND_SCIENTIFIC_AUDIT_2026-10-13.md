# N4 — §3–§5 unified methods and evidence ownership: source audit

**Date:** 2026-10-13. **Stage:** N4 (journal-methods consolidation). **Current verdict:** content revision committed; full-source LaTeX compile and final N7/N8 reviewer QA checked separately, not implied by manuscript prose alone.

## Why the rewrite is scientific rather than cosmetic

The N3 accepted result structure needs (1) a precise empirical estimand, (2) an intelligible data and model path, and (3) clearly distinguished experimental/inference tiers. Earlier §3 repeated M3 DEV-30%/TEST-drift and retrospective Twitch comparison mechanics subsequently restated in §5; earlier §4 repeated all methods and objective lists later in §5. In this rewrite, §3 contains only the event and conditional-gain mathematics, §4 the fixed expert and admissible information flow, and §5 the actual protocols, comparator objectives and statistical family. All numbered equation identities, the framework diagram and two study tables are retained.

### §3 methodological invariants

- `u_K` is one-positive NDCG@K on an event-specific candidate list (K=10).
- `Delta_M=u_K(M)-u_K(B)` is fixed-expert-, incumbent- and candidate-relative; not general novelty in L2D.
- `eta_r(z)=E[Delta_M|Z=z,R=r]`; `E[a Delta]=E[a eta]` uses no hindsight selector features.
- `q_DEV` is a design-calibrated finite DEV count constraint; no implication of realized TEST call cap or measured latency.
- `S` is an exhaustive retrospective target-derived partition and cannot be used online.

### §4 methodological invariants

- KuaiLive rooms versus persistent creator memories, LiveRec streamers, M3 authors have different ranked units.
- Memory equation stays exactly Short $0.45$, Long $0.45$, training popularity $0.10$; M3 last ten Short positions and Long denominator count *all* strictly prior author events including TRAIN-unseen authors.
- No current target, current target-specific visibility state or relative utility leaks into an online selection input.
- The original framework figure is exactly retained, with its original label `fig:framework`.

### §5 methodological invariants

- Twitch 46,878 DEV / 44,221 TEST streamer events, 14 features; Utility DEV-frozen and Difficulty TEST-count retrospective.
- Original KuaiLive 10,222 room events, 575 inclusive sampled candidates, half-open live room availability, candidate 2×2 fixed raw scores; retrospective paired analysis only.
- M3 50,049 DEV / 47,575 TEST author events, 12,533 TEST users, TRAIN before 2026-03-23 12:00 and TEST from 2026-03-27 14:00 in recorded timezone-naive order; 4,096×575 checkpoint screen does not define final full-active TEST.
- M3 2 families × 3 trained seeds, 12 observable features, five decision objectives; 5 user-disjoint DEV OOF splits, all five pointwise policies calibrated up to 30% on DEV, not a TEST budget.
- M3 prequential observed earlier TEST histories permitted without observing current target. Label-blind G5 scores/decisions precede TEST target reveal.
- M3 significance family Utility−(Base,Difficulty,Specialist), separately three-Holm within each fit; 5,000 user-cluster resamples/sign permutations; same 12,533 users in all six fits.
- True typed-timestamp versus preplanned millisecond hash and any earlier tie tolerance nuances remain in Supplementary S1–S2; not editorially erased by claiming a fully identical original source expression.

## Deliverables and cross-stage integration

- Source file `main.tex`: all source lines outside §§3–5 left byte-identical.
- Original 8 main sections, full original 11 main figures/tables, original LaTeX labels and all preexisting valid references preserved.
- [Main-vs-supplement research ownership map](N4_METHODS_MAIN_SUPPLEMENT_OWNERSHIP_2026-10-13.csv) assigns 23 scientific units across §3–§5 to S1/S2/S3/S4/S5/S7/S8.
- Combined supplementary S1–S9 and source `kbs_references.bib` remain unchanged at N4.
- Post-G5 nested DEV Two-stage comparator is separate exploratory evidence; if methodologically useful it may be summarized later in a clearly labeled supplementary analysis, not retrofitted to N4 or original G5.

## Editorial handoff to N5

Rewrite Introduction and Related Work against the fixed §3 estimand and §6 findings, especially existing L2D, DS-Frame and sampled-metric precedents. N5 should use the completed optional nested-DEV pilot only to calibrate *bounded estimator-implementation positioning*, not to claim a general new deferral theory. N6 should interpret the substantive Always Memory cost/accuracy counterexample. N7/N8 must verify LaTeX, all references and publisher requirements and R0 original 12 claim tracks.

**Citation/context audits:** primary L2D paper (Narasimhan et al., NeurIPS 2022): https://proceedings.neurips.cc/paper/2022 ; source Krichene and Rendle (KDD 2020) https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ ; KBS primary publisher context https://www.sciencedirect.com/journal/knowledge-based-systems. N4 did not add a made-up bibliographic citation or claim a new theoretical result.

## N4 verified build, source-integrity and parallel evidence closure

**Exact N4 source:** `main.tex` Git blob `71c2b9aa2e2098e6d5d91407d697486434470de5`, committed as [`e7dad017363809942af45bc85c7a9251d123842f`](https://github.com/mzch0210/KuaiLive-Agent/commit/e7dad017363809942af45bc85c7a9251d123842f). **GitHub Actions compile #38340731142: SUCCESS**, including the distinct **Compile current KBS manuscript**, **Verify generated PDF** and **Retain compile preview and log** steps. Build archive `11786648183` (~488 KB ZIP, finite retention). This verifies LaTeX build and PDF existence, **not page-by-page editorial visual inspection**.
 
**Exact static audit of that N4 source:** 8 sections, 28 subsections, 2 main figures and 9 main tables, all original labels retained once; no unresolved `\\ref/`eqref` cross-references, duplicate labels or citation keys absent from `kbs_references.bib`. The main text outside §§3–5 remains byte-identical to the N3 accepted source. The combined S1–S9 SHA is unchanged at `3f9413f8ffe2a2ff1ef70640a3820d81b281055f`, bibliography unchanged at `a33cb506fc2d08b422232a10e91a9d06c44044f5`.

**N4 science/prose gate: PASS.** Definitions of `u_K`, `Delta_M`, `eta`, selection and paired-regime allocations remain in the Methods, with correctly stated pre-outcome feature access and exact G5 30%-on-DEV versus observed TEST call drift. R0 numeric claims are not recomputed by this source check and remain an N7/N8 responsibility.

**Parallel D1:** completed nested DEV pilot successfully under [Actions #38339908528](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38339908528); its [scientifically scoped aggregate summary and N5 gate](../../experiments/kbs_plan_c/N2_D1_PRIMARYSEED_DEV_EXPLORATORY_RESULTS_AND_N5_GATE_2026-10-13.md) was filed separately. This **post-G5 exploratory** result has not been inserted into §3–§6 nor into the accepted G5 preregistration family. Its small and budget-mismatched direct-vs-two-stage differences warrant circumspect N5 novelty attribution.

**Next planned stage:** N5 after a bounded D1 impact review, focused on Introduction/Related Work and accurate close-prior scholarly positioning. Overall manuscript submission readiness remains HOLD until N6–N8 and author-side permissions/archives are resolved.
