# N13 W1 — One-page argument storyboard

**Status:** Storyboard locked before the first Results-source reorganization.  
**Source:** N13 `main.tex` pre-W2 blob `e772647e6c6e0e54219bf53c949de752b59054fa`; frozen N12 parent `683dd7988d163fed49a6e3846f9317eec3e483e5`.

## Five-sentence argument

1. **Problem:** A live-streaming recommender may hold a useful historical viewer–creator relationship source, but its usefulness is conditional: it can complement the incumbent on one request and add little or negative ranking value on another.
2. **Gap:** Existing knowledge representation, selective-inference and sampled-ranking work does not by itself establish whether candidate-regime-dependent labels for the incremental value of an already fixed source change the downstream requests selected for that source and the resulting full-candidate ranking quality.
3. **Estimand and design:** We define event-level Memory-minus-Base NDCG@10 under a specified candidate roster, fit separate policies from pretarget information using sampled-active or full-active utility labels, freeze their DEV thresholds, and evaluate both policies on identical full-active candidates.
4. **Primary result:** On 30,000 previously unevaluated M3 author-ranking targets from the same recording period, full-candidate-supervised frozen policies improve weighted full-candidate NDCG@10 over the original uncorrected sampled-label policies by 0.005391 for SASRec and 0.003585 for GRU4Rec, while their naturally realized population-weighted Memory-call fractions are lower.
5. **Meaning and parallel evidence:** The paired room-ranking reversal explains why the value label is candidate-indexed; the shared-DEV switch trace describes changed allocation without proving H1 mediation; a separate nested fixed-candidate history-null comparison supports authentic-source value while retaining the unverified same-cohort prereveal Popularity-margin check and the absence of demonstrated production-cost savings.

## Research-question logic

```text
RQ1 — Diagnose the value object
  fixed Base + fixed Memory + actual candidates + usable history
  → measured incremental value can change with candidate regime
                         |
                         v
RQ2 — Primary policy consequence
  sampled- versus full-candidate relative-value supervision
  → separate DEV-frozen policies → same full-candidate evaluation
  → H1 policy-level NDCG/call-fraction comparison
  → DEV switch trace explains allocation descriptively, not causally
                         
RQ3 — Parallel source-validity check (not downstream mediation)
  same target cohort / current candidates / Memory scorer
  → authentic historical relationships vs constrained history nulls
  → source arrangement carries information under the tested intervention

Operational condition on RQ2:
  call quota is an explicit policy objective;
  measured legacy gate timing is adverse;
  production latency/savings are not established.
```

## Results storyboard (target order)

| Target order | Question answered | Lead evidence | End-of-subsection bridge |
|---|---|---|---|
| 5.1 RQ1: value context | Why can the fixed source's incremental value differ by request/candidate roster? | Twitch history-state pattern, then 10,222-event KuaiLive room candidate reversal | This makes the candidate regime used for utility labels consequential, motivating H1 |
| 5.2 RQ2 primary H1 | Do full-candidate labels change the frozen policies' full-candidate outcomes? | 30,000-target H1 table; weighted NDCG effects and weighted call fractions | Establish the policy-level outcome before looking at request-level DEV allocation |
| 5.3 Allocation trace | Which requests change Memory use under the two supervision regimes? | 50,049 shared DEV requests; switch counts and value accounting | Descriptive explanation only; no mediation claim |
| 5.4 Frozen selection context | How does utility-based pretarget selection compare with Base/other gates on the existing task cohorts? | Twitch frozen pointwise Utility; M3 47,575-event frozen Utility and six-fit summary; Always Memory ceiling | Keep ranking quality distinct from call-rate objective and cost |
| 5.5 RQ3 source validity | Does authentic history matter when candidates and scorer are held fixed? | Nested 4,096-target H2 primary table, then separate DEV null/component context | Parallel evidence, not H1 mechanism; disclose cohort-specific missing prereveal gate |
| 5.6 Operating conditions | What is and is not supported about resource use? | Always Memory quality; quota sensitivity; measured legacy pointwise GPU timing | Call constraint may motivate selection; no production savings claim |

## Figure and table placement sketch

- Introduction `fig:knowledge-value-chain`: keep the two branches from RQ1 value definition to (i) RQ2 selection consequences and (ii) RQ3 source-validity test. Do not draw an RQ2-to-RQ3 causal arrow.
- RQ1 `fig:results-evidence-states` and `tab:results-factorial`: retain together with the Twitch state and KuaiLive paired room result.
- H1 `tab:results-m3-b4a-supervision`: place within the first paragraph block of 5.2; its sample definition and weighted-call estimand should be stated immediately before or in the caption.
- Frozen context `tab:results-twitch-policy`, `tab:results-m3-policy`, `tab:results-m3-robustness`: keep in 5.4, with M3 Always-Memory/Base ceiling paragraph adjacent to the M3 policy comparison.
- H2 `tab:results-m3-additional-relation-identity`: first table in 5.5; place the **NOT VERIFIED** same-cohort pre-reveal check immediately adjacent, not buried in a later general limitation.
- Resource `tab:results-n10-cost`: keep in 5.6 with hardware, 256 distinct requests, counterbalanced repetitions and the exact tested legacy selector stated once.

## W1 acceptance criteria

- H1 is the primary result and appears in 5.2 immediately after the motivating RQ1 result, not after a long list of baseline experiments.
- RQ3 is explicitly parallel to RQ2 and never framed as its causal mediator.
- No result is presented as independent merely because a different model fit, randomization seed or ranking unit is shown.
- The same-period 30k sample is never described as future-period replication.
- The S comparator remains the original uncorrected target-retained sampled protocol; corrected-S is not claimed as tested.
- H1 naturally realized calls are unequal; weighted call fraction and raw call counts are not conflated.
- The source-specificity result retains its same-cohort prereveal Popularity-margin check status **NOT VERIFIED**.
- Always Memory accuracy and measured legacy gate timing remain visible in the operating-boundary discussion.
