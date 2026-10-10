# KBS Section 6 — Phase 3 reprioritization after Phase 2

**Date:** 2026-10-10  
**Decision type:** Scientific/experimental prioritization only. **NO experiment was initiated** and no canonical manuscript, frozen selector, checkpoint, TEST labels or C1–C3 novelty statement is modified by this file.  
**Scientific authority:** [approved submission outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md), [integrated revision master plan](../../KBS_SECTION6_INTEGRATED_SUBMISSION_REVISION_PLAN_2026-10-09.md).  
**New evidence:** [successful Stage-2 audit/replay](SECTION6_STAGE2_S4_S7_REPLAY_AND_REVIEW_2026-10-10.md), [archived-source replay run 37959745609](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/37959745609), [S4 component draft](SUPPLEMENTARY_S4_MEMORY_COMPONENTS_DRAFT_2026-10-10.md), [S7 OOF budget draft](SUPPLEMENTARY_S7_GATE_BUDGET_DRAFT_2026-10-10.md).

## 1. Decisions in one view

**Execution closure, 2026-10-10:** The conditional Stage-3B P2 has since been **executed and scientifically verified** on the exact frozen P0 KuaiLive checkpoints: [successful hosted CPU run #38014145900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38014145900), [source-checked full result](SECTION6_STAGE3_P2_RESULTS_2026-10-10.md), [KBS reviewer decision](SECTION6_STAGE3_P2_KBS_REVIEWER_TIGHTENING_AND_REMAINDER_DECISION_2026-10-10.md), and [complete S5 draft](SUPPLEMENTARY_S5_CANDIDATE_REGIME_P2_DRAFT_2026-10-10.md). Nine predeclared 128/256/575 candidate draws each retain negative sampled Memory−Base while the unchanged full-active mean is positive. All 10,222 original per-user P0 ranks were reproduced. The newer reviewer decision supersedes this document's earlier prospective "if executed" language **for execution status only**. Stage 3C extra gate objectives and Stage 3D retraining/deployment experiments are **not scheduled** for the bounded approved C1–C3; only their documentary S2/S3/S8 obligations remain. Formal S1–S9 packaging and author approval are still outstanding.



**YES, Phase 3 priorities change.** The original three P2 options are no longer equally valuable. Repeated gate-target or stronger-Base exercises should NOT be compulsory, because Phase 2 directly addresses the formerly important uncertainty about whether combined observable features outperform the two partial feature sets only at one post-selected invocation count. More importantly, Phase 2 does **not** test the stability of Section 6.3's KuaiLive sampled/full reversal to independent negative candidate draws. If any new computational experiment is justified, that fixed-checkpoint P2 protocol is first in line, **but remains conditional and retrospective**, not an entry condition to the manuscript's originality.

| Candidate item | Before Phase 2 | New status | Decision criterion |
|---|---|---|---|
| KuaiLive fixed-score sampled-negative size/draw sensitivity P2 | Optional P2 | **First priority among *conditional* new runs** | Run if original full-candidate score arrays/checkpoint hashes can be recovered at modest cost **and** authors wish to claim robustness beyond the one original sampled-negative set. Otherwise retain precisely bounded original C2 statement and disclose limitation. |
| Additional expert-utility / positive-delta / simple-heuristic gates | Optional | **Deferred / conditional second-line diagnostic** | Run **DEV-only** only after documenting a specific unanswered difference from frozen Utility vs Difficulty and historical history-threshold controls. Do not redefine novelty as gate-method superiority. |
| New stronger Base training | Optional | **Defer; documentation first** | Existing Base is an operational reference, not the claimed optimal architecture. Refit only if an exact same-candidate audit identifies a material training/protocol flaw not curable by honest disclosure in S3. |
| More KuaiLive training seeds or latency/online tests | Optional | **Not scheduled** | Three seeds reproduce paired direction on same 10,222 users but do not constitute independent datasets. Cost claims already correctly report increased latency, not speedup. |
| Memory component explanation / fixed specialist choice | Originally covered via S4 | **Mandatory no-training reviewer check** | Confront Long-only > Full in recoverable DEV and Long-only's different behavior in unavailable events; document that the frozen Full Memory is a pre-existing interpretable *reference*, not a DEV-optimized maximizer. Use the completed S4 matrix; do not tune weights on historical TEST. |
| S7 multiplicity/OOF sensitivity | Originally a supplement task | **Mandatory inference-language check, no new training** | Keep all confidence intervals as **pointwise, conditional, exploratory**, and explicitly forbid calling the five-budget grid a new TEST or an independently validated universal budget frontier. Simultaneous intervals are optional if authors want familywise claims, which the current outline does not demand. |

## 2. Why these changes follow from the observed evidence

### C3 no longer demands an extra Gate race

The source-pinned Twitch DEV OOF replay compared **46,878** events at predeclared common invocation fractions **5%, 10%, 15%, 20%, 30%** (and replayed historical K=6,563). Combined 14-feature Utility yields **+0.00598/+0.00774/+0.00832/+0.00792/+0.00736** NDCG@10 versus Base, always the largest *observed* gain among the three feature groups in this grid. Base-score-only at 30% becomes **−0.00282**. OOF combined Utility additionally dominates the OOF combined Difficulty score ordering at these counts. Their direct **within-user** paired comparisons and pointwise unadjusted intervals were archived.

This narrows a *specific* former threat: the complete feature set's apparent advantage is not restricted to the one original K=6,563 comparison. It **does not establish** that estimating delta utility outperforms predicting Memory quality or a transparent heuristic in general; that broader claim is **not part of approved C3**. The one-shot, development-frozen Twitch TEST comparison (Base **0.58211**, Utility **0.58983**, equal-count Difficulty **0.58340**) remains the primary C3 confirmation and is untouched.

### C1 gains a more nuanced component-mechanism result

Same-user DEV variants in recoverable-but-unrepresented **n=5,879** show Long-only NDCG@10 **0.63890**, Full Memory **0.53298**, Base **0.30201**; Long-minus-Full **+0.10592**, paired 95% percentile CI **[+0.10096,+0.11061]**, with **5,000 fixed-score user bootstrap resamples**. However, Long-only does **not** outperform Full Memory uniformly: for unavailable targets the Long-minus-Full contrast is approximately **−0.03208**, and on *overall* DEV Long-only **0.52761** and Full Memory **0.52170** both trail LiveRec Base **0.57185**.

The proper answer to a KBS reviewer's "why not deploy Long-only?" question is NOT post-hoc expert reweighting. The scientific object is the relative utility of the **specified fixed interpretable expert**, and the alternative component ranks are explanatory sensitivity analyses, **not a newly selected specialist**. Because the states use the *realized target*, the recoverable group is not known when routing an event. Replacing frozen Full Memory with a score chosen after examining these state-defined results would create a different policy requiring separate DEV design and genuinely independent validation. No new test is needed just to clarify this boundary.

### C2's remaining variation is *candidate draws*, not training seed

The fixed-checkpoint KuaiLive P0/P1 analyses already show matched **10,222** events, native sampled Memory−Base **−0.04120**, full **+0.04631**, paired shift **+0.08751** with three model seeds maintaining direction. The 2x2 candidate/reference allocation remains **descriptive**, and candidate membership includes size, composition and ranking difficulty, which cannot be causally isolated by the table. Three model training seeds evaluated against the same original sampled candidate list do **not** test variability under independent negative lists or multiple sample sizes. Historical "candidate seed" runs retrained a different SASRec protocol and must not be mistaken for the missing fixed-score P2.

Krichene and Rendle's *On Sampled Metrics for Item Recommendation* (CACM 2022, DOI 10.1145/3535335; original KDD 2020) provides the general sampled-metric ranking inconsistency theorem; **we do not claim this as novel**. P2 would characterize the particular fixed KuaiLive Room/Streamer–Memory contrast under varying candidate draws, not demonstrate or claim a new general theorem.

## 3. Revised Phase-3 execution gates

**Gate 3A — scientific preflight (NO training, recommended now)**

1. Lock exact C1–C3 permitted claims from the outline; record the new S4 trade-off and explicit no-component-causality caveat.
2. Check that S7 five-budget figures are consistently described as DEV OOF **batch top-m** outcomes with pointwise conditional resampling, no multiplicity/optimizer bootstrap or serving SLA statement.
3. Verify S2 identity metadata: P0 Room/Streamer checkpoint SHA, alpha **0.125**, 10,222 user/time/target IDs, original sampled 575 candidates, original eligible active-room universe, saved score arrays, target-inclusion rules, candidate ties and score standardization. Write a feasibility pass/fail; **do not** use TEST labels for selection or retuning.
4. Check whether the Section 6.3 author-intended wording extends beyond the original sampled set. If not, proceed to stage-4/5 manuscript and supplement packaging without a new experiment. If yes, P2 is worth running.

**Gate 3B — conditional P2 candidate sampling test**

If 3A passes and the wider robustness claim is needed, precommit sizes **128, 256, 575, full-active** (positive target included) and **at least three independently fixed negative-list seeds per sampled size**, keeping the original 575 set separately labeled. If score reuse makes it inexpensive, consider 5–10 draws instead of 3 for more informative descriptive spread, **but select this before inspecting outcomes**.

Fix per-user timestamp/target/eligible history, model checkpoint hashes, alpha, Memory, candidate eligibility and the frozen full-active raw branch logits. Sample only from eligible active unobserved rooms; prestate how insufficient candidates and edge-case target inclusion are handled, recording excluded/missing events and never cherry-picking. For every draw/size report paired user-level Base/Memory NDCG@10 and Memory-minus-Base difference, full minus sampled shift and bootstrap CIs **conditional on that draw**, sign distribution across draws, all unfavorable trials, and candidate-composition characteristics. Where feasible, reuse full-score vectors to compute the same ranked-candidate × score-reference 2x2 for each setting. Distinguish *draw-to-draw spread* from *user-level bootstrap uncertainty* and *between-checkpoint-seed* SD; do not treat reused users as independent dataset replicates.

**Interpretation safeguards:** This is previously inspected KuaiLive TEST and is therefore **post-hoc sensitivity**, not fresh held-out TEST confirmation or prospective selector deployment. If directions vary or some counts do not reverse, report them and narrow C2's operating-context statement to conditions supported by the observed grid. Do not retune alpha or remove inconvenient draws.

**Stop rule:** If fixed full-score arrays cannot be reliably recovered, or P2 requires new model training without a clear scientific benefit, **do not silently substitute** historical changing-model candidate-seed experiments. Mark P2 not executed, retain a specific original S-versus-F protocol claim and disclose sensitivity-to-draw as untested.

**Gate 3C — additional DEV gate objectives only if warranted**

The current evidence tests Utility against Base and matched-count Difficulty and S7 shows robustness of combined features across five DEV budgets. If reviewer/author concern specifically requires disentangling positive-delta regression, predicting expert quality, or simple history-only rule beyond already available controls, perform a **new fixed-feature, comparable-capacity, nested/OOF DEV-only comparison** using those objectives and same matched budget grid. Report potentially negative results; no frozen TEST gate/threshold is reselected. Else **skip**.

**Gate 3D — strong Base and runtime**

Complete S3 documentation on actual hyperparameter search, training epochs, candidate matching and original checkpoint nonidentity. Do not invest in retraining a benchmark leaderboard without a traceable complaint that invalidates the chosen Base-relative scientific object. No additional latency experiments necessary for current bounded claims.

## 4. Outputs and acceptance checklist

Recommended phase-3 minimum output if no P2 is launched: (1) a **decision log** specifying "P2 conditional/skip" with exact source and reason, (2) a short **S4 fixed-expert explanatory note**, (3) an **S7 inference statement** barring TEST/online/familywise claims, and (4) checkpoint/raw-score feasibility inventory. These can directly feed formal S2/S4/S7 supplements and do not require GPU.

If P2 is launched, additionally deliver a registered YAML/JSON design, fixed seed/sample inventory, checksum manifest, downloadable paired score outputs, all-sample effect/CI summaries, an immutable Action run and a source-linked S5/S8 draft. Update main Section 6.3 only after reviewing the complete signed evidence, with no retroactive omission or strengthened held-out language.

Decision to enter Phase 4 (whole Results integration) should rest on: C1–C3 retained; source-to-claim evidence fully explicit; any chosen experiment completed according to its predeclared rule; all positive/null/negative outcomes documented; and Section 6 manuscript interpretations matched to proper retrospective/DEV/frozen TEST hierarchy.

## 5. External methodological support

- [Official Knowledge-Based Systems aims and scope](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051): recommends quality in AI methods, personalization, and decision-support applications; this project remains a Base-relative, operational study rather than an unrestricted gate-architecture race.
- Krichene and Rendle, [*On Sampled Metrics for Item Recommendation*](https://doi.org/10.1145/3535335), *Communications of the ACM* 65(7):75–83 (2022). Sampled ranking metrics need not preserve ordering.
- Ferrari Dacrema, Cremonesi, and Jannach, [*Are We Really Making Much Progress?*](https://doi.org/10.1145/3298689.3347058), RecSys 2019. Motivation for transparent baseline/protocol documentation, not a demand to beat a universal SOTA.
