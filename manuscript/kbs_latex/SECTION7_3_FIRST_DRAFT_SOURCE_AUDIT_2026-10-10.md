# Discussion §7.3 — first-draft scholarly source and evidence audit

**Date:** 2026-10-10. **Scope:** first scholarly draft of §7.3, *From Relative Utility to Selective Decisions*, in canonical [main.tex](main.tex), source commit [3615a0a](https://github.com/mzch0210/KuaiLive-Agent/commit/3615a0a2542bfe497013efb2cb83ed20296b0caa).  
**Governing plan:** [independently optimized Section 7 plan](SECTION7_KBS_DISCUSSION_WRITING_PLAN_2026-10-10.md), Section 7.3 Optimization A.  
**Earlier accepted §§7.1–7.2:** preserved exactly. No new model training, new policy selection, TEST rerouting, claim redefinition, new equation, main exhibit, or supplementary statistic.

## Paragraph-level scientific contributions

| Paragraph | Function | Anchor |
|---|---|---|
| 1 | Relate conditional incremental Utility to pre-outcome specialist allocation and differentiate the *relative alternative advantage* from Base's own anticipated loss | §3.3 Eq. (expected selective gain), §4.4 pre-outcome descriptors |
| 2 | Interpret held-out pointwise Utility selection against Base and same-count retrospective Difficulty; describe allocation-dependent means without causal subgroup claims | §5.2/§5.3 comparator information access, §6.2 frozen TEST, S2 and S7 |
| 3 | Place the empirical result beside formally published post-hoc deferral and uncertainty-guided reranking; quantify imperfect predictive ordering and fixed-ranker Oracle headroom | NeurIPS 2022 Narasimhan et al.; AAAI 2026 Xu et al.; §6.2 and original results provenance |

The section consists of **three English paragraphs**, about **256 whitespace-delimited prose words**, plus heading/label. It maintains finding-first academic prose and avoids a second Results table or a generic new learning-to-defer claim.

## Provenance and inferential audit

- **Primary evaluation:** one independently DEV-frozen Twitch TEST selection policy, **44,221** evaluated events.
- **Effects used in the text:** Utility−Base NDCG@10 **+0.00772**, Utility−Difficulty **+0.00644**, **6,650** specialist calls; §6.2 source user-paired intervals remain **[+0.00641,+0.00903]** and **[+0.00528,+0.00762]**, respectively, and are not retested.
- **Realized mask analysis:** Utility-selected Memory−Base conditional mean **+0.05136**; unselected **−0.05890**, arithmetic and descriptive, not independent causal subgroup tests.
- **Crucial equal-use qualification:** Difficulty's full-TEST-batch top-$m$ comparator obtains $m$ retrospectively from the frozen Utility policy's realized invocation count; it is **not** described as a separately DEV-frozen online threshold or a guaranteed serving budget.
- **Prediction and bound:** TEST Spearman **0.173**; approximately **11.7%** of the observed *same-count, two fixed rankers* hindsight Oracle improvement over Base recovered. This does not identify individual-level calibration or general optimum.
- **Knowledge/source positioning:** uses formally published NeurIPS 2022 key `narasimhan2022posthoc` and formally published AAAI 2026 key `xu2026guider`, previously verified in [the Related Work publication audit](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md). No new bibliography key required.
- **Bounded result:** this is an offline Twitch ranking decision result only, not evidence of KuaiLive gate transfer or lower end-to-end latency; §7.4 is reserved for those boundaries.

## Source-level acceptance and outstanding workflow

- New canonical subsection label `sec:discussion-selective-decisions` is unique; the existing Eq. and §6.2 label refs resolve in the source.
- All manuscript `\\cite{}` keys exist in the bibliography; no duplicates. One insert was made immediately before `\\bibliographystyle{elsarticle-num}`, leaving every earlier source character untouched.
- **First draft complete; separate KBS reviewer-style tightening not yet performed.**
- A matching GitHub Actions build was launched automatically by the source update: [workflow run 38035076650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38035076650), source `3615a0a`. Its final compilation and any PDF inspection must be recorded from the actual run result; no assertion of PDF PASS is made in this initial audit.
- Follow established staged practice: next perform independent §7.3 scholarly tightening if requested, then proceed to §7.4. Do not use this first-draft audit as full Discussion or final KBS submission acceptance.
