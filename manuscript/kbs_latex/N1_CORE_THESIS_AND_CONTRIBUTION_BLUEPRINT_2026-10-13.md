# N1 — KBS thesis-first scientific argument and contribution blueprint

**Date:** 2026-10-13. **Stage:** N1 of [2026-10-13 thesis-first master plan](KBS_THESIS_FIRST_REVISION_MASTERPLAN_2026-10-13.md).
**Verdict:** **SCOPED N1 PASS** (unique thesis, evidence roles, prior-art limits and downstream manuscript instructions determined); **SCIENTIFIC NOVELTY/OPERATIONAL PREMISE NOT FULLY CLOSED** — N2 decision required before claiming KBS submission readiness.
**Editing scope:** design/research-positioning blueprint only. `main.tex`, `kbs_references.bib`, G5 files, and canonical S1–S9 are unchanged. No new inference, retraining or external human peer review has been performed.

## 1. Single-page argument card — immutable scientific direction

### Research tension (one scientific premise)
Sequential recommenders already exploit historical behavior, while user–creator relationships may contain additional long-horizon signals. The availability of such evidence, and the standalone accuracy of a memory ranker, do not determine its marginal benefit over an already trained incumbent for a particular set of eligible alternatives. Knowledge integration therefore poses a **measurement problem** before it poses a conditional use decision.

### ONE central scientific question (must unify the paper)
**Under what incumbent and candidate contexts does an independently specified, fixed relationship-memory ranker add event-level top-K ranking utility, and can that predicted marginal value improve specialist choice under a declared invocation constraint?**

### One-sentence thesis (preferred; candidate for Introduction and Abstract)
> **The marginal ranking utility of a fixed relationship-memory specialist depends on the incumbent and candidate context; predicting this utility provides a more informative decision signal than the tested incumbent-difficulty and standalone-specialist criteria under specified specialist-invocation rules.**

This is a *bounded empirical and decision-quality claim* for the tested protocols and comparators, not a claimed new general theorem in learning to defer, a globally optimal selector, a universal candidate-size causal mechanism, SOTA, or a demonstrated production cost saving.

### Research questions form a cumulative explanation, not three parallel paper topics
| Question | Scientific function | Main result | Interpretive limit |
|---|---|---|---|
| **RQ1: When does fixed relationship memory provide marginal value?** | **define, observe and explain heterogeneity** of event-level `Memory−Base` NDCG@10 | Twitch frozen TEST (44,221, Base 0.58211 vs Memory 0.53980; recoverable-history target subgroup +0.22045) and distinct M3 author TEST (47,575, Memory 0.346792 > six trained Base scores 0.25800–0.26065) | Twitch retrospective target-defined state is **not** a gate-time feature; across environments Base/task/candidates/time co-vary |
| **RQ2: Why does the candidate ranking context belong to the valuation?** | **qualify the estimand**, explaining that even fixed expert/Base comparisons can change in different candidate regimes | Original KuaiLive, same 10,222 room events: Memory−Base −0.041204 sampled-active (575) vs +0.046307 full-active, paired shift +0.087511; 2×2 candidate membership/reference allocation descriptive | This is already inspected TEST, retrospective paired diagnostic; NOT a fresh M3 replication, a pure list-length causal effect, or a new sampled-metric inconsistency theorem |
| **RQ3: Does predicting marginal knowledge value improve the selection decision?** | **test decision relevance** using available features, fixed Base/Mem, and defined selection constraints | Twitch DEV-frozen Utility 0.58983 > Base 0.58211 and retrospectively count-matched Difficulty 0.58340 at 6,650 calls; independent M3 six fitted Bases, five DEV-frozen policy objectives, Utility NDCG 0.301766–0.304004 and better NDCG with fewer observed Memory calls than **each of the four named alternative policies** for every fit | Twitch equal-count Difficulty is retrospective; M3 policies are not exactly equal TEST calls; six fits share TEST users; 3 predeclared Holm contrasts within each fit; uncertainty comparison secondary |

**Theoretical/empirical reading order:** Observing conditional value (RQ1) makes the choice problem meaningful (RQ3); the paired candidate analysis (RQ2) explains why the value target itself must be specified relative to ranking environment. In the **Results**, lead with RQ1 → RQ3 → RQ2, then mechanism and cost. In the **Introduction** the estimand can be defined using candidate context before the main decision contribution. This is one scientific narrative, not a claim that C2 experiment causally precedes C3 or validates its training.

### Essential adverse result to use constructively
KuaiLive-M3 **Always Memory NDCG@10 0.346792** is better than **all** Utility 0.301766–0.304004; in a distinct 256-event, warmed DEV RTX3090 scoring replay **Always Memory 0.8033ms** is faster than **Utility 1.8018ms** (Base 1.4245ms). This makes the practical rationale for *the imposed specialist-call constraint* a genuine unresolved premise. The scientific interpretation is:
> **Predictive quality for allocating a constrained knowledge expert and the system-level justification for imposing that constraint are different research questions.**

The paper can establish the first for a stipulated call budget; it **cannot establish the second as an observed production benefit**. N2 shall separately decide whether a new independent cost-constrained/use-case or competitive baseline experiment is needed. Do not remove this outcome from the main Results, Discussion or scientific referee audit.

### Preferred positioning: scientific evaluation + decision-quality (Plan A)
The proposed contribution is **a rank- and candidate-conditioned, incumbent-relative evaluation of explicit relationship memory, coupled with a frozen test of its pre-outcome prediction for specialist selection**. The Methods contribution is the **task-specific operationalization** of known comparative-expert decision principles, not the novelty of a regression score or threshold. New architecture/general learning-to-defer, adaptive-computation and economic superiority claims are excluded. Strength of the *combination* must be argued empirically; none of its component ideas is declared independently unprecedented.

## 2. Three contributions in proposed publication-facing academic English

Proposed wording to be integrated in N5, once N2 checks the strength of the evidence premise. Do not copy RQ or artifact names into journal text:

1. **Incumbent-relative valuation of relationship evidence.** *We characterize the event-level ranking contribution of explicit relationship memory relative to trained sequential recommenders, identifying distinct patterns of historical complementarity across two held-out live-streaming ranking settings.* (Do not claim a new theory of information value or a cross-platform causal effect.)
2. **Candidate-conditioned interpretation of knowledge value.** *A paired evaluation on the same live-room recommendation events shows that the measured incremental value of the fixed memory specialist can reverse across eligible candidate regimes, establishing the importance of the ranking context when constructing and interpreting utility-based supervision.* (Established sampled-metric inconsistency is credited to prior work; the novel empirical instance is fixed expert-minus-incumbent label sensitivity, not a proof.)
3. **Marginal-utility-guided specialist selection.** *Using only pre-outcome information, we evaluate specialist selection targeted at expected incremental ranking utility. Held-out Twitch results and a separately frozen, forward-time KuaiLive-M3 evaluation demonstrate gains over specified alternative objectives, including six fitted incumbent configurations in which the Utility rule improves NDCG while making fewer observed specialist calls than each named alternative.* (No total latency or hard online TEST budget claim; statistical scope preserved.)

Order these as C1, **C3**, C2 if journal contribution list should foreground decision outcome: C2 functions as the explanatory validity contribution. Either list order is acceptable if the text explicitly states RQ2 is diagnostic rather than another independent selection test.

## 3. Reconstructed argument chain for all eight sections

| Section | Actual burden of proof | Scientific paragraph choreography | N-stage |
|---|---|---|---|
| §1 Introduction | Why existing representation/fusion measures cannot decide **when a fixed expert adds ranking utility over a trained Base** | incumbent already encodes history → marginal value may be positive/negative → candidate-conditioned relative outcome → select fixed expert only with pre-outcome observable features → frozen evidence and boundary; end with hierarchical C1/C3/C2 | N5 |
| §2 Related Work | Identify prior art and specific incremental gap, not assert lack of knowledge gating or L2D | knowledge representation/fusion/conditional gating → deferral/post-hoc expert selection and 2026 DS-Frame budgeted recommender → sampled metrics/live room availability → **specific empirical measurement/decision question** | N5 |
| §3 Problem Formulation | Make `Δ_M(x)=u10(M,x)−u10(B,x)` and `η_r(z)=E[Δ_M|Z=z,R=r]` precise | decision-time event + same-candidate rank utility → relative fixed expert target → conditional expected gain → threshold under stated call design; cite established deferral objective | N4 |
| §4 Framework | Explain the **fixed Base–Memory–gate** observational flow | transparent short/long/popularity memory → pre-outcome history+Base score descriptors → relative-utility estimator and frozen routing; do not scatter three protocols and file stages through common method | N4 |
| §5 Experimental Setup | Provide the only definitive main-text specification of **three nonexchangeable tasks** and protocol roles | one dataset/ranking-unit table (Twitch streamer, original KuaiLive room, M3 author); comparator freeze; out-of-time conditions, 30% DEV not TEST, prequential earlier TEST interactions; user-cluster 3-Holm scope | N4 |
| §6 Results | Prove progressive discoveries rather than inventory experiments | conditional value → frozen Utility decision quality → candidate-conditioned supervised target → supporting DEV mechanism & six-fit robustness → operational cost counterevidence | N3 |
| §7 Discussion | Derive knowledge-system meaning beyond repeating scores | relative not intrinsic knowledge value; why predicting *this* fixed expert's relative ranking utility is more decision-targeted than Base difficulty; candidate-conditioned evaluation; distinguish specified Memory calls from measured serving cost; concise generalizability | N6 |
| §8 Conclusion | Answer ONE scientific question and its decision meaning | relationship knowledge's relative and context-dependent contribution → usefulness of marginal-value prediction under stated call design → context and cost aware knowledge-system evaluation | N6 |

**Public-facing diction:** `frozen`, `TEST`, `one-shot`, `stage G5`, `original P0` and repeated negations are accurate source-audit terms but are not a substitute for academic claims. Concentrate necessary sample, timing, inferential and retro/prospective differences in §5 and table captions; journal prose should open each result with its finding. Accurate negative evidence is never suppressed.

## 4. Current quantitative scientific claim gate (original results not rerun)

- **Twitch:** Base 0.58211; Memory 0.53980; Utility 0.58983; 44,221 streamer TEST events, 6,650 (15.04%) Utility Memory invocations. Compared Difficulty 0.58340 at retrospectively equal TEST count.
- **Original KuaiLive:** room task, same 10,222 events; signed `Δ_M` reversal −0.04120 to +0.04631; paired shift +0.08751, accepted 95% user-paired CI [0.08210, 0.09326]; six-fit M3 author results **not** compared numerically to room NDCG.
- **M3:** 47,575 author ranking events/12,533 users; SASRec and GRU4Rec 3 separately trained seeds each **same TEST cohort**; all four named selector alternatives (Difficulty, Specialist Quality, Uncertainty, History) have lower NDCG and more realized specialist calls than Utility **within each fit** (see combined S7.4 + S8.4). Utility rates 27.718%–29.215%. History TEST rate 35.472%; common selection criterion was **maximum 30% on DEV**. Primary three one-sided Holm adjusted comparisons within each fit: Utility−Base, Utility−Difficulty, Utility−Specialist. The other objectives, including Uncertainty, are valid descriptive comparisons but not an enlarged registered six-block/global Holm inference family. All inference relies on the 5,000 user-cluster tests on the shared cohort.
- **M3 resource:** 256 prespecified warmed DEV events on RTX3090, input data ready; Always Memory outruns Utility (0.8033 vs 1.8018 ms) and outperforms it in ranking quality (0.34679 vs 0.30177–0.30400) in *different measured evidence settings*. Therefore do not conflate the two as an end-to-end TEST cost frontier.
- **Knowledge eligibility:** fixed Short/Long/Popularity component, trained Base and available candidates within each protocol. Target-derived historical categories and retrospective recency bins are **not selector inputs**.

## 5. Changes relative to previous N0, R7 and old C1–C3 narration

- **Stronger independent nearest-prior challenge:** DS-Frame (Yuan et al., September 2026 arXiv; CIKM 2026 accepted, forthcoming event) already uses fast/slow sequential recommenders and a learned selector with controllable computation budget. This is **HIGH direct collision** with broad “gated/budgeted recommender” novelty. The main bibliography currently lacks DS-Frame; N5 should add accurate, publisher-status-correct bibliographic details after checking available authoritative record. No head-to-head DS-Frame experiment is claimed.
- **Existing KBS gating is not absent:** CKLF, MHGFCL, KAPER, and Yerragunta et al. establish prior knowledge representation, gate/fusion and selective path usage. Do not infer originality from a new label alone.
- **Existing learning to defer is broader:** Mozannar/Sontag (2020), Narasimhan et al. (2022), Mao/Mohri/Zhong (2025) and 2026 online varying-expert literature cover deferral and relative expert performance. No claimed new ranking-optimality theory.
- **Existing sampled candidate effect is known:** Krichene/Rendle (2020); C2 novelty is the paired interpretation for the **fixed relationship specialist** and **conditional value label**, not a general sampled-NDCG proof.
- **Existing live-ROOM methods are strong:** LiveRec, KuaiLive and DCGLive establish availability, room-level identities and dynamics. M3 author ranking is intentionally another task; it is not a replacement of the original live-room task.

## 6. Non-negotiable N2 decision questions (do not solve by wording)

1. **Meaningful call constraint:** Can credible external memory/API access price, permissions or compute bottleneck be measured? If not, choose evaluation/decision-quality Plan A and maintain "stipulated specialist-call constraint" throughout.
2. **Mature competitor fairness:** Does accepted two-stage L2D / DS-Frame / stronger Base or parameter-matched ranker comparison need a **new holdout** to support a KBS original-contribution claim? Existing named five-policy comparisons do not establish general SOTA or equivalence to full GUIDER/DS-Frame.
3. **Budget comparability:** Because frozen TEST call counts vary, avoid equal-TEST-cost superiority; if N2 proposes same-call-budget frontier, declare new exploratory comparison with existing TEST or genuinely independent new TEST, never a re-frozen confirmatory G5 claim.
4. **Candidate metric as an auxiliary explanatory analysis:** Do not inflate C2 with pure-count or platform-transfer effects without independent controlled evidence.
5. **Archival rights:** No lasting public model/data DOI exists just because GitHub Actions produced artifacts. Handle author/legal availability independently in N8.

## 7. Explicit approval rules, not a manuscript revision

**N1 argumentative-positioning PASS** requires: (a) one thesis, (b) RQ1–RQ3 and exact evidence hierarchy, (c) differentiation table with published primary sources including 2026 fast/slow recommender collision, (d) no algorithmic/economic claims unsupported by TEST, and (e) N2 open issues with a go/no-go decision rule. These are met in this blueprint. **KBS novelty acceptance likelihood is neither measured nor guaranteed**. If N2 finds the absence of a substantive call constraint or fair mature gate comparison fatal for the chosen contribution claim, revert to a narrower validated contribution or conduct *new protocol-frozen* independent experiments before making stronger assertions.

**Next stage:** N2 should give a written priority-ranked experiment/claim decision. Only after N2 should N3–N6 edit the canonical `main.tex`, ensuring the reviewable scientific contribution—not repository workflow—is the basis of the final manuscript.
