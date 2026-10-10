# Discussion §7.4 — evidence-tier first-draft audit (2026-10-10)

**Paper:** *When Does Relationship Memory Help? Base-Relative Evidence Valuation for Live-Streaming Recommendation*  
**Canonical source:** [main.tex](main.tex)  
**Section:** §7.4, *Validity Boundaries*; insertion commit [dcc3bca](https://github.com/mzch0210/KuaiLive-Agent/commit/dcc3bcace7a202c2ae5bac29f3e12d190b257ea3).  
**Approved plan:** [optimized Section 7 writing plan](SECTION7_KBS_DISCUSSION_WRITING_PLAN_2026-10-10.md), especially “Optimization B — 7.4: use a hierarchy of scope, not a checklist of disclaimers.”  
**Status:** First scholarly draft added; this is an independent evidence/source check, not the later dedicated KBS reviewer-style tightening or final §7 integrated visual review.

## Scientific function and accepted structure

The section has three compact prose paragraphs, approximately **258 whitespace-delimited English words**, and performs a *scope interpretation* rather than a revision chronology or a list of disclaimers:

| Evidence tier | What the paragraph can legitimately establish | Evidence anchor | Essential inference boundary |
|---|---|---|---|
| **1. Identification and replication type** | The DEV-frozen Twitch selector shows within-protocol held-out ranking improvement on 44,221 events. Twitch DEV ablations and target-state diagnostics aid interpretation. KuaiLive paired ranking experiments show that fixed Memory-minus-Base utility is candidate-context-sensitive. | §§5.3, 6.1, 6.2, 6.3, 6.4; S2, S5, S7, S8 | KuaiLive paired P0/P1/P2 examine **previously inspected TEST** cases; three model initializations and nine negative-draw conditions share the *same observed user cohort*, and bootstraps condition on those observations. No KuaiLive independently frozen deployed policy is implied. |
| **2. Decision observability and metric scope** | Diagnostic state labels and target recurrence distance characterize outcomes after the target is known; only the 14 pre-outcome history/Base-score features enter the Utility selector. One-positive eligible-candidate ranking and coarse Twitch timestamp resolution specify what NDCG@10 describes. | §§3.3, 4.4–4.5, 5.1, 5.4, 6.4; S1, S4, S6 | Target-relative retrospective labels cannot serve as request-time inputs. Twitch source ten-minute first/last **observations** are not actual arrival/departure truth. L=8/16/32 reference checks use separately trained Bases, not a single-parameter randomized window-length intervention. |
| **3. Resource measurement and transfer** | Frozen Twitch routing used Memory on 6,650/44,221 = 15.04% of requests, while a *separate* warmed KuaiLive CPU replay gives Base 0.991 ms, Selective HGB 2.007 ms, overhead +1.016 ms and 2.03× the Base timing. | §6.5; S9 | The KuaiLive timing replay uses archived route masks and a **distinct HGB gate**; it is not a Twitch deployment study or evidence of net latency savings. No independently frozen zero-shot selector transfer to KuaiLive was tested. |

The narrative preserves the substantive adverse resource result and two different evidence levels while allocating only one concise paragraph to each level. It contains no extra numeric CI, benchmark claim, new publication citation, display or statistical test.

## Consistency and reference checks

- **Original C1–C3 upheld:** C1 is operational Base-relative evidence value, C2 candidate/history regime dependence, C3 pre-outcome specialist choice. §7.4 neither rewrites nor extends these claims.
- **Previous §7.1–7.3 accepted source preserved:** all text outside the new subsection insertion is byte-for-byte unchanged by commit dcc3bca. References to §§6.2, 6.3, 6.5, 4.4 and 5.1 resolve to existing manuscript labels.
- **Twitch TEST versus KuaiLive P0/P1/P2:** user bootstrap, training seeds and candidate-list randomness are separate uncertainty sources; a single sampled fixed user cohort is not a replication across data populations.
- **Historical-memory interpretation:** one-positive offline NDCG is a ranking metric under the platform’s candidate eligibility and temporal granularity, not an observed watch-time, engagement or GMV effect.
- **No invented uncertainty:** the section does not report new confidence intervals, P-values or inference that the frozen Twitch selection rule would optimize the candidate regimes explored in KuaiLive.
- **Reference metadata:** no new BibTeX entry was necessary. The prior formal-version comparison in §7.3 and the published Krichene–Rendle sampled-metrics discussion in §7.2 remain in place.
- **Source consistency before compile:** exactly one new subsection and one unique label \`sec:discussion-validity\`; all existing citations, \`ref\`/\`eqref\` keys, and labels were statically verified without gaps or duplicates.
- **Exact-source PDF compile: PASS.** For the precise [7.4 source commit dcc3bca](https://github.com/mzch0210/KuaiLive-Agent/commit/dcc3bcace7a202c2ae5bac29f3e12d190b257ea3), [GitHub Actions #38035806769](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38035806769) completed successfully. Its output is a **29-page** LaTeX PDF; compilation, nonempty PDF verification and artifact upload succeeded. Final LaTeX pass had **no fatal errors, undefined citations, unresolved references, overfull hboxes or BibTeX warnings**. The source-matched [PDF/log artifact #11664396786](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38035806769/artifacts/11664396786) is available for page inspection. Successful compilation is separate from fresh page-by-page visual proofing and from a future independent §7.4 reviewer-style tightening.

## Editorial handoff

Next, perform a dedicated §7.4 KBS reviewer-style tightening with focus on hierarchy clarity, whether the paragraph borders are sufficient, policy-versus-diagnostic inferential status, one-positive candidate interpretation, cross-platform transfer and complete reporting of KuaiLive replay overhead. Then draft §7.5 as a synthesis of knowledge-system design principles; retain §8 Conclusion and Abstract for subsequent phases.
