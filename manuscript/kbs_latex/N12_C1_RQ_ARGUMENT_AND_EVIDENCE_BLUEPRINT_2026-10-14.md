# N12-C1 | Single-Thesis Argument, Three RQs and Evidence Architecture

Date 2026-10-14. **C1 blueprint frozen, not a revised manuscript and not an experiment.** N11 source: 39p main, 45p supplement, and N12-C0 complete mapping of 152 content blocks, 59 LaTeX labels, 13 tables and 3 figures. Neither private A4 labels nor TEST outcomes were opened.

## 1. Unified KBS contribution

**Single thesis:** An already specified source of historical viewer–creator relationships has downstream ranking value defined by its incremental utility over the designated incumbent under the current candidate environment. Pretarget estimates of that conditional value can guide the use of the source under a stated invocation limit; fixed-candidate historical null comparisons provide independent evidence of source validity.

In the diagram, RQ1 establishes the value object. RQ2 takes the value object's candidate-indexed supervision and examines its use-time decision consequences. RQ3 is a **parallel** source-validity intervention on the historical evidence while holding the current candidates fixed. **There is no RQ2→RQ3 causal mediation arrow.** System resource evaluation tests an application boundary, not a fourth primary scientific finding.

### RQ1: When is fixed relationship memory incrementally useful?

Definition: the value target is event-level NDCG@10 of Memory minus the event-level NDCG@10 of designated Base, under **one common candidate set**. History recoverability describes where knowledge complements Base retrospectively. Changing candidate membership can change the measured sign of that same comparison.

- Twitch original frozen TEST: 44,221 streamer events; overall Base 0.58211 versus Memory 0.53980; recoverable-but-unrepresented history can nonetheless improve ranking by +0.22045 in the relevant retrospectively defined subgroup.
- Original KuaiLive: 10,222 prior-examined paired room events, sampled-active Memory-minus-Base −0.04120 versus full-active +0.04631, paired shift +0.08751. Crossed-factor design examines candidate membership versus score-reference normalization. Membership effect jointly changes set size, identities and ranking competition; this is not an isolated count-only causal effect.
- RQ1 takeaway: the source's value cannot be interpreted without its incumbent, historical evidence and actual eligible alternatives.
- Handoff to RQ2: candidate composition influences the labels used to supervise a selector; test whether candidate-aligned label training has consequential results on the final F candidate regime.

### RQ2: Does candidate-aligned value supervision improve pre-outcome selection?

- Defined target: F-aligned versus sampled-candidate S labels, with the same pretarget observable feature contracts and F evaluation rosters. The DEV candidate sampler retrospectively retains the observed relevant target for supervision; the deployed policy cannot see that target.
- Original frozen M3 47,575 author-ranking TEST requests with SASRec/GRU4Rec across six trained Base fits form initial choice evidence, not six independent target datasets.
- Additional B4-A frozen 30,000 author-target IDs / 10,387 users come from the same 2026-03-27 through 2026-03-31 source period, disjoint from original evaluated TEST target IDs, but may share history and viewers; they are **not a newly collected future-time independent TEST**.
- Frozen SASRec F-minus-S weighted F NDCG@10 +0.005391 (CI [0.003646,0.007174], Holm p 0.000600); GRU4Rec +0.003585 (CI [0.001599,0.005576], Holm p 0.000800).
- SASRec F/S calls 8,704/9,105 (1.337 pp difference), GRU F/S calls 8,629/9,168 (1.797 pp). These exceed the old approximately equal-call 1pp tolerance. Describing the contrast as a *strict equal-budget causal comparison* is prohibited.
- DEV 50,049 S/F supervision transfer provides exploratory support, not an external repeat. The older frozen pointwise Utility gate, these DEV-trained transfer policies and B4-A F-aligned gates must not be conflated.
- Handoff to RQ3: more effective selection on F candidates does not itself prove that true relationship identities, rather than candidate composition or general author exposure, are the historical source of ranking information.

### RQ3: Does authentic history matter with current candidates held fixed?

- B4-A nested 4,096 targets/3,059 users, within the 30,000 additional sample. Closed-hour, author-hour-margin/time/source-availability-preserving historical-author permutations with seeds 20261014/15/16. Fixed original Memory scoring implementation, frozen contemporary F candidates.
- Original weighted F NDCG@10 0.334942. Nulls 0.303905 / 0.304689 / 0.302796, per-event mean null 0.303797. Paired original-minus-null +0.031145, CI [0.027389,0.035098], Holm p 0.000600 (the third of exactly three prespecified B4-A directional hypotheses). ~76.78–76.80% source edges rewired; three seeds share one evaluation cohort.
- The earlier 1,024-request DEV null cohort had TRAIN-only Popularity baseline 0.021867 and all three corresponding DEV nulls exceeded it. However the **B4-A same-cohort TRAIN-popularity floor was NOT VERIFIED AS PREDECLARED prior to A4**; DEV acceptance must never be borrowed to certify it retrospectively.
- This source perturbation also changes viewer–author repeated pairs and higher-order neighborhoods. It supports authentic historical arrangement value under a composite strong intervention, not a unique semantic or isolated-pair causal effect.

### Resource conditions are a bound on RQ2, not the research purpose

- Absolute Always Memory M3 additional-target weighted F NDCG@10 0.348744 exceeds F-aligned selective SASRec 0.305446 and GRU4Rec 0.304530. There is no proven unconstrained selection accuracy dominance.
- Actual RTX3090 256 distinct DEV ×3 counterbalanced original pointwise Utility selector mean 1.76941 ms versus unconditional Memory 0.69165 ms, despite selector Memory-call fraction 31.25%. Its measured gate/base/feature work does not prove cheaper serving; do not mistake it for a benchmark of the newer B4-A vectorized F policy, cloud production, money or energy.
- Positive use-time inference: selecting requests under an externally stipulated Memory invocation limit, not established online cost savings.

## 2. Argument structure and section contracts

| New section | One assigned intellectual job | Required bridge | Unacceptable duplication |
| --- | --- | --- | --- |
| 1 Introduction | One knowledge-value problem and why Base/candidate-relative value matters; motivate RQ1–RQ3; three evidence-anchored contributions | Defines what counts as useful external relationship information at decision time | Project progression and repeated legalistic exclusions |
| 2 Related Work | Separate knowledge admission (2026 KBS SAMD), knowledge view fusion (2026 KBS MHGFCL), delegated prediction (learning-to-defer/DS-Frame), candidate-sensitive ranking (KDD sampled metrics) | Gap is a fixed, auditable source's value under actual candidates and its choice consequences | “we are not a new theorem” repeated under every prior |
| 3 Knowledge Valuation and Selective Use | Define eligible ranking unit, fixed B and Memory 0.45/0.45/0.10, observed target only offline, Δ, η, sampled/full labels, pretarget Z, frozen selection threshold | Objects fixed before evaluation | Two separate formulation/framework chapters repeating the same symbols |
| 4 Experimental Design | Introduce evidence hierarchy and exact sources of validation; map each sample to an RQ; define freeze, 20-cell weights, clustered uncertainty and three Holm tests | Makes the inferential status of all forthcoming claims self-evident | Historical B0/B1/B2 narrative and full script/run logs |
| 5.1 RQ1 Results | Historical complementarity and candidate reversal; Twitch and original KuaiLive | Label changes motivate testing downstream decisions | Claims of causal transfer across unlike streamers/rooms/authors |
| 5.2 RQ2 Results | Original M3 held-out choice and separate 30k frozen H1; DEV transfer used as explanatory analysis | Value-use claim leaves authenticity unresolved | Equal-budget claims or merging different gate identities |
| 5.3 RQ3 Results | Frozen 4096 H2 authentic/null main table; exploratory DEV null as secondary | Source validity complements choice consequences | Misrepresenting three seeds as independent cohorts or original floor as PASS |
| 5.4 Operating Conditions | Unconditional Memory accuracy and actual negative runtime cost; constrained-call interpretation | Cost is boundary on actual deployment | Turning routing overhead into claimed economic savings |
| 6 Discussion | Knowledge-science implication, candidate-indexed target, historical validity/external-time and resource bounds | Unifies findings under the same fixed source and incumbent | Recopying every numerical result or list of disclaimers |
| 7 Conclusion | State what relationship knowledge-use valuation contributes | Closes the same thesis as abstract/introduction | Unverified new claims or a defensive “not a gate algorithm” ending |

## 3. Table and figure allocation and editorial sign-off

Main table priorities: task/evidence-tier table; paired candidate factorial; original M3 frozen policy; six-fit robustness summary; frozen 30k F-minus-S H1; frozen 4096 real-history vs 3 null H2; compact Twitch TEST policy if necessary; concise adverse system cost. Full DEV S/F transfer, DEV source-component ablation, Twitch feature ablation, complete comparator enumeration and earlier implementation timing belong in the appropriate S1–S10 sections with precise main references. This is an editorial target, not a hard numerical page or table maximum; no frozen scientific content may vanish.

**Diagram redesign**: center “fixed knowledge source M, incumbent B, candidate regime C → event-level Δ”; first branch estimates η using pre-outcome Z and follows decision to Base or Memory subject to a call quota; **parallel** branch holds F candidates fixed and compares original historical source with time-valid null histories. Never imply RQ2 produces RQ3's perturbation result. Method figure separately distinguishes online features from retrospective label and diagnostic states.

Writing contract: each research paragraph makes a focused claim, identifies its fixed comparison and evidence, interprets the result, and hands off to the next question. The abstract/Introduction/Discussion/Conclusion must describe the *same* new knowledge-valuation object. Positive scholarly language is appropriate, but adverse measured costs, non-equal F/S calls, missing predeclared H2 popularity control and same-period sampling cannot be discarded.

## 4. Exit conditions for N12-2

- Single thesis and RQ1–RQ3 have unique, nonoverlapping roles; RQ3 is a parallel evidence branch.
- Every original paragraph, label, equation, figure, table has a traceable destination in N12-C0 map (no deletion at this stage); full main-to-supplement migration must preserve values and references during implementation.
- All B4-A frozen effects, confidence intervals, call counts, adverse Memory references and unverified popularity condition are in the new evidence contract.
- N12 work performed so far is **text/source mapping only**; no re-use of private A4 labels or new TEST scoring.
- After C0/C1 automated checks pass, N12-2 may begin Introduction/Related Work revision, then N12-3 merged framework, continuing with full editorial QA per N12 plan.

Sources: official Elsevier KBS scope https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 ; SAMD https://www.sciencedirect.com/science/article/pii/S0950705126002388 ; MHGFCL https://www.sciencedirect.com/science/article/abs/pii/S0950705126004132 .
