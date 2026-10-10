# Final whole-chapter KBS reviewer-style assessment — Results 6.1–6.5

**Audit date:** 2026-10-10  
**Scientific authority:** [Submission-oriented outline](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md), especially frozen C1–C3; [canonical LaTeX](main.tex) after all three empirical strengthening stages.  
**Status:** **Results scientific-content and exact-source PDF-layout audit PASSED** with documented scientific-precision and float-placement corrections. This is **not** equivalent to final manuscript or supplementary package acceptance. Further S1–S9 document assembly, bibliographic signoff, non-Results sections 7–8, Abstract and coauthor review remain explicitly open.  
**Review standard:** Assess whether each empirical claim follows from its stated data/model/protocol, whether C1–C3 receive the promised evidence, whether controls and uncertainty are comparable, whether results repeat needlessly, whether causal/generalization claims overreach, and whether the main/supplement boundary is defensible. We do not redefine novelty as a new Gate architecture or demand unbounded SOTA gains.

## Executive editorial verdict

**Scientific result chain:** **C1 supported**, **C2 supported as protocol-bound descriptive finding**, **C3 supported as bounded pointwise frozen-policy decision value**, and **6.5 computational qualification honest**. No new GPU training, additional random-negative draws or further Gate target comparisons is mandatory for the **claims actually written**. The existing whole-chapter flow is coherent: 6.1 heterogeneous fixed-specialist value → 6.2 observable selection → 6.3 evaluation-regime boundary → 6.4 explanatory DEV robustness/alternative explanations → 6.5 controlled scoring cost.

**Strength is not universality.** The Frozen Twitch TEST and post-hoc KuaiLive TEST cannot be pooled as independent replications of a common learned gate. Target-relative states are never serving-time features. Fixed-checkpoint candidate-set changes combine size and membership; their cross-reference score-normalization algebra is not a randomized experiment. The primary utility selector wins modestly (+0.00772 NDCG) and captures only about 11.7% of a sharply constrained hindsight Oracle ceiling. KuaiLive P2 adds 9 of 9 signed sampled/full reversals for three declared sizes × three declared RNG streams, **not** an all-draw/causal law.

**Readiness decision:** Section 6's scientific *text* may be treated as conditionally stabilized following source-matching PDF verification. Submission package readiness remains **BLOCKED** by unassembled or incomplete formal supplements, particularly S1/S2/S3/S6/S8 and conversion of existing S4/S5/S7/S9 drafts into correctly captioned, referenced and source-verified journal material. Reconfirm journal-specific supplementary requirements using Elsevier's current guide; do not equate Markdown drafts with submitted supplements.

## 1. C1–C3 contribution-to-evidence audit

| Contribution defined by outline | Main-section validation evidence | Scientific sufficiency | Claim / restriction required |
|---|---|---|---|
| **C1 Operational Base-relative evidence valuation** | §6.1 one-shot frozen Twitch TEST: n=44,221, Base NDCG 0.58211 vs Memory 0.53980, difference −0.04232; recoverable n=5,539: Memory−Base +0.22045, versus represented −0.01935 and unavailable −0.18215. §6.4 on DEV n=46,878: Local Memory weight/window/decay robustness; fixed-ranking component variants in recoverable n=5,879, Long-only 0.63890 vs Full Memory 0.53298, paired gap +0.10592 [0.10096,0.11061]. | **PASS within fixed Base/expert and candidate set.** Independent DEV/TEST window sign agreement is NOT cross-platform confirmation. | Must say **operational value relative to this Base**, not intrinsic or causally isolated information gain. Target-defined recoverable/represented/unavailable states are retrospective only. Full Memory remains frozen even if Long-only scores higher in DEV subgroups. |
| **C2 Candidate-regime dependence of conditional utility** | §6.3 post-hoc KuaiLive n=10,222 exact same P0 trained checkpoint pair α_room=0.125: sampled −0.041204 vs full +0.046307; paired difference +0.087511, CI [0.08210,0.09326]. 2×2 path average membership +0.088270, normalization −0.000759; three independently trained pairs +0.08751,+0.08363,+0.08408 (same users). P2: nine drawn samples (128/256/575 × three RNGs) all sampled-negative/full-positive, means by size −0.07983,−0.06799,−0.04158. | **PASS as specifically post-hoc, fixed-checkpoint operational diagnostic.** P2 materially reduces the possibility that the one originally sampled 575-negative set alone determined the reversal. | No pure candidate-count causality; size, identity, difficulty, z-score reference may vary. 3 trained model seeds share users; three sampled RNG seeds repeat same user cohort and one model. All CIs are conditional and none creates an independent untouched TEST. Distinct native KuaiLive policy Base values 0.60784/0.39835 and separate comparator Base 0.61714 are never the P0 paired 0.60709/0.38571. |
| **C3 Conditional relative-Utility choice** | §6.2 Twitch one-shot frozen TEST n=44,221, policy invokes Memory 6,650 times: Base 0.58211, Utility 0.58983 (paired +0.00772 [0.00641,0.00903]), retrospective exact-count Difficulty 0.58340 (Utility−Difficulty +0.00644 [0.00528,0.00762]); Oracle 0.64806; predicted-realized Spearman 0.173 and ~11.7% hindsight headroom recovered. §6.4 DEV five OOF call budgets 5–30% show combined features highest among three studied feature families on this inspected grid, nonmonotonic. | **PASS for the frozen pointwise rule and compared controls**; effect magnitude modest, not close to hindsight optimum. | Difficulty is matched **after seeing the TEST batch's frozen Utility call count**, and its top-m rule is not an equivalent prospective pointwise budgeted policy. Oracle knows realized labels and bounds only those two rankings/exact m on evaluated batch. No all-gate objective superiority claim. S7 DEV budget curves are score replay, conditional OOF uncertainty, not new held-out policy confirmation. |

### Workload and cost (6.5, supporting rather than a fourth independent contribution)

Frozen Twitch **15.04%** calls is an invocation-frequency statistic and says nothing about Twitch inference latency. The **separate** warm cached KuaiLive 575-candidate CPU benchmark has Base mean **0.9906 ms**, Selective HGB **2.0066 ms**, i.e. **+1.0160 ms / 2.03× Base**. Gate inference runs but candidate routing branches follow archived frozen masks. The conditional HGB complexity O(TD) (fitted T=81, maximum depth D=3) and Memory scoring O(C) assume cached relationships and prepared features; neither is a universal full-stack throughput bound. **PASS:** the text does not claim acceleration, online conversions, SLA or gate-family equal-quality timing.

## 2. Numerical reconciliation and inference conventions

| Audit item | Recalculation / verification | Status |
|---|---|---|
| TEST group partition and overall difference | 24,285+5,539+14,397=**44,221**; weighted means [−0.01935012,+0.22044597,−0.18214811] = **−0.04231595**, consistent with §6.1 −0.04232 | PASS |
| Utility policy arithmetic | 0.5898344192−0.5821113853=**+0.0077230339**; 0.5898344192−0.5833967726=**+0.0064376466** | PASS |
| Oracle definition and modest recovered gain | (0.5898344192−0.5821113853)/(0.6480594078−0.5821113853)=**0.11710789** (11.71%) | PASS |
| TEST memory call count | 6,650/44,221=**15.04%**, not HGB auxiliary KuaiLive 14.25% | PASS |
| P0 factorial algebra | +0.0882696253−0.0007588280=**+0.0875107973**, equals paired FF−SS | PASS |
| KuaiLive P2 exact-draw inspection | Reopened archived **10,222×65** per-user dataframe, nine size/seed means, 38-row user-bootstrap CSV; no missing user IDs, no omitted draw, 9/9 signed reversal, user-level 2×2 allocation identities matched to floating-point tolerance | PASS |
| P1 seed and P2 sampled-draw definitions | P1 varies fitted model pair across seeds 20260918/19/20, same users and originally matched candidates; P2 fixes 20260918 weights and changes negative lists across three independent RNG streams and three sizes | PASS — do **not** combine counts as 12 independent data replications |
| Bootstrap reporting | Twitch TEST main effects use 5,000 one-user paired resamples, KuaiLive P0/P2 use 3,000; new Twitch DEV S4 direct variant contrasts 5,000 and S7 exact budget curves 3,000; CIs conditional on fixed predictions, masks, budgets, ranked labels and inspected subgroup assignments | PASS with explicit limited inference. No training/rethreshold bootstrap or experiment-wide multiplicity bands |
| DEV/Twitch vs previously inspected KuaiLive test | §6.1–6.2 main Twitch confirmation; §6.3 KuaiLive post-hoc; §6.4 Twitch DEV explanatory + separately sourced historical KuaiLive baseline diagnostic; §6.5 different CPU workload | PASS; resist treating datasets as one experiment or aggregating cross-platform effect sizes |
| Full/partial Memory sensitivity | Seven **local parameter perturbations** retain signed state patterns; five **component-removal ranking variants** may change those signs. These are distinct tests | **WORDING REPAIRED** to prevent an apparent contradiction |
| External sampled-metric relation | General non-preservation of model ordering under sampled ranking metrics was established by Krichene & Rendle, KDD 2020 / CACM 2022. New KuaiLive result is a specific controlled Base-relative diagnostic, not a new theorem | PASS |

## 3. Reviewer issues and concrete dispositions

### Issue R1 — Ambiguity in negative sampling identity (P1, corrected)

**Old wording:** §5.1 described 574 “unobserved rooms” in sampled-active candidate lists. Original P2 input/code show negative rooms are **active and not the current target**, but may have appeared in that user's earlier interactions. Historical 575 lists include 601 prior-interaction negative overlaps involving 433 users. “Unobserved” can misleadingly suggest a globally never-before-seen user-room constraint, which was **not** implemented.

**Correction implemented:** §5.1 now describes **574 contemporaneously active non-target rooms sampled without replacement**, explicitly acknowledging that past visits can occur and that these are not verified dislikes. No user cohort, negative list or model changed.

### Issue R2 — Unqualified strong-Base comparator description (P1, corrected)

**Old wording:** §5.2 claimed the supplementary GRU4Rec/ContraRec/SASRec checks “establish the competitiveness” under a uniform-looking protocol. In fact, comparative models have limited and heterogeneous tuning/epoch budgets, and a KuaiLive auxiliary Base from a different checkpoint must not silently replace paired P0.

**Correction implemented:** §5.2 now calls them **limited reference-competitiveness checks** under documented candidate protocols, with **nonuniform training and tuning budgets**, and says they do not replace the designated fixed Base. No SOTA victory or fully equivalent-budget claims remain. Formal S3 must provide actual trainer configurations, epochs, DEV selection and checkpoint provenance before submission.

### Issue R3 — Three random mechanisms conflated or silently omitted (P1, corrected)

**Old wording:** §6.3 final status referred only to “factorial and seed analyses” even after P2 was integrated, risking an implicit omission or accidental confusion of P1 model seeds with P2 candidate draws.

**Correction implemented:** §6.3 now explicitly groups **factorial, checkpoint-seed, and candidate-draw analyses** as **supporting post-hoc diagnostics**, none being new frozen Twitch validation or zero-shot transfer.

### Issue R4 — Apparent contradiction between local Memory stability and variant removal (P1, corrected)

**Old wording:** §6.4 asserted sign stability across “seven evaluated Memory configurations,” immediately before the five component-only variants, whose directions are not all the same.

**Correction implemented:** §6.4 specifies that sign stability refers to **seven local parameter perturbations**, **not** to component-removal variants. Different experimental designs are disambiguated without weakening any verified result.

### Issue R5 — Redundancy and information density (minor, scoped no further main edit)

- §6.1 graph DEV/TEST signs and state table TEST absolute metrics/CIs are **complementary**, not duplicative; the paragraph names the pivotal values only.
- §6.2 presents key paired advantages that are not derivable from rounded table entries at full precision, while its table conveys all five decision alternatives and both ranking metrics.
- §6.3 factorization table shows the only needed four-cell matrix; P2 is **one short prose paragraph** while all nine draws, CIs and decompositions belong to S5. Do not add another 9-row main table.
- §6.4 preserves one small feature-family table and two sharp new results (five-budget directional sensitivity; Long-only vs fixed Full Memory). Full grids belong to S4/S6/S7. Repeating the same TEST-frozen caution is partly necessary because three scientific evidence tiers are mixed in this subsection; avoid deleting essential qualifiers solely to shorten prose.
- §6.5 reduced the original four-alternative latency table to the controlling Base-versus-HGB result and a short conditional-complexity account. S9 carries other pipeline timings/memory. **No added main figure/table required**.

The sequence and transitions are satisfactory. Do not relocate core tests across 6.1–6.5 or expand Section 6 into a Discussion. Issues of underlying mechanisms, deployment or transfer belong in a future Section 7, clearly marked as interpretation or untested hypotheses.

### Issue R6 — Results exhibits floating across a subsection boundary (P1, corrected)

A rendered-PDF review found that the §6.1 state figure and evidence-state table had originally appeared **after the §6.2 heading**, although source citation and numerical labels were correct. This confused experimental roles. A local standard LaTeX \`placeins\` / \`\\FloatBarrier\` before §6.2 was combined with relaxing the Table 3 float from bottom-only \`[!b]\` to \`[!htbp]\`. The first barrier-only attempt created a nearly empty float page, so that rejected layout was not retained.

**Exact-source final PDF PASS:** Figure 2 is on page **17**, Table 3 appears at the **top of page 18**, and the §6.2 heading begins **after** Table 3 on that same page. No redundant blank float page remains. These were layout-only adjustments, not changes to any group statistic.

### Issue R7 — Computational results ending before References (P2, corrected)

An intermediate manuscript build placed the last 2–4 lines of §6.5 on the opening References page. The last deployment-cost caveat, the first invocation-frequency paragraph and repetitive §6.4 baseline cross-reference prose were condensed without removing the distinct Twitch/KuaiLive inference boundary or changing **0.991/2.007 ms, +1.016 ms, 2.03×, 14.25% calls, or HGB T=81/D=3**. No forced page break was used.

**Exact-source final PDF PASS:** all of §6.5 ends on page **23**; References begins on page **24**, with no isolated paragraph tail, figure/table relocation to the wrong chapter, or clipped text.

## 4. Residual scope/validity concerns for reviewers (not numerical errors)

| Priority | Remaining vulnerability | Exact needed publication action |
|---|---|---|
| **P0 — submission package** | **Formal S1/S2/S3/S6/S8 are not present as completed supplement drafts in the canonical manuscript folder**. S4/S5/S7/S9 exist only as **draft markdown**, not a unified approved supplementary deliverable. Main §6.4 refers explicitly to S6; §6.3 to S5; §6.5 to S9. | Assemble accurate, independently checked S1–S9 with manuscript-to-supplement label/caption map, frozen source hashes, rerunnable scripts and archive provenance. Journal-specific requirements must be checked rather than inferred. Do **not** declare paper submission-ready while these references lack a real packaged destination. |
| **P1 — scientific external validity** | Primary pointwise Utility policy wins only one independent frozen Twitch TEST. Different KuaiLive policy experiments are historically inspected and use different checkpoint/budget settings. | State dataset-specific limits and distinction in Discussion/abstract. A new confirmatory data collection would be required for broader transfer conclusions—not proposed by the bounded outline. |
| **P1 — confounding in retrospective state and candidate analysis** | Observed target defines recoverable/unavailable; KuaiLive candidate count, items and score reference change jointly; context-length models were retrained. | Keep noncausal and post-hoc wording; no target-group inference as a serving rule, no independent effect of candidate count, no pure sequence-visibility causal claim. |
| **P1 — uncertainty** | User-bootstrap CIs on frozen policy decisions and DEV OOF predictions do not include retraining, selection of threshold/feature family, multiplicity or distribution shift. | Preserve exact conditional CI semantics in figure/table footnotes and supplements. No post-selection p-value story or universal feature-family superiority. |
| **P1 — Base competence** | Auxiliary baselines have uneven and limited tuning, Twitch small sequential variants were trained for five epochs; the designated fixed Base is not proven globally optimal. | Formal S3 fair-candidate provenance + actual training budgets. **Do not** impose expensive additional training unless a genuine invalid Base setup is discovered. |
| **P1 — efficiency** | Auxiliary cached KuaiLive timing executes Gate prediction but branches according to replayed masks, not autonomous production routing; per-replica CPU mix and missing cache/update/I/O time limit practical generalization. | Keep S9 traceable; never claim online SLA, throughput or saved Twitch serving computation. |
| **P2 — presentation** | Early Section 3 has one existing ~5.51-pt overfull warning, outside Section 6; final publication formatting will change after Section 7, 8 and Abstract. | Address once final main paper layout is assembled. Verify cross refs and full PDF at final source SHA. |

## 5. Final source diff, bibliography and PDF acceptance

The audit resulted in **limited textual and layout revisions**, leaving **all** scientific outcomes, trained checkpoints, data subsets, thresholds, Math/Delta definitions, bootstrap CIs, numbered tables/plots and C1–C3 contribution statements unchanged:

1. **§5.1 — candidate eligibility:** define sampled negatives as **current-time eligible non-target rooms**, not rooms the user has never previously clicked; the latter constraint was never part of the protocol.
2. **§5.2 — comparator fairness:** accurately label heterogeneous/training-limited auxiliary Base comparisons as **limited reference-competitiveness checks**, not a uniformly tuned SOTA competition.
3. **§6.3 — evidence hierarchy:** explicitly include candidate-draw P2 along with checkpoint-seed and factorial results as **retrospective supporting diagnostics**, not fresh policy confirmation.
4. **§6.4 — experiment-family separation:** qualify the sign preservation of **seven local parameter perturbations** so it is not mistaken for the distinct **component-removal variants**.
5. **§6.4 and §6.5 — Results density:** compress repeated auxiliary Base limitations and invocation-cost/deployment caveats, without omitting inference restrictions or the measured latency/complexity results.
6. **§6.1 and §6.2 — figure/table relationship:** add a local FloatBarrier and permit evidence table top placement so Figure 2 and Table 3 remain **before** the §6.2 heading without a mostly-empty float-only page.

Full source trail: [initial precision fix 0194e8ae](https://github.com/mzch0210/KuaiLive-Agent/commit/0194e8ae28918f7ce0d7bf1181aac9174644ba16), [local Memory clarification 9e258636](https://github.com/mzch0210/KuaiLive-Agent/commit/9e258636c487ba63db30bb45460de196537c6560), [cost clarification 442b6cdb](https://github.com/mzch0210/KuaiLive-Agent/commit/442b6cdb515a50ee6072f7fc637ee0b4c41d2075), [float barrier 571e6d82](https://github.com/mzch0210/KuaiLive-Agent/commit/571e6d828117f301a82ed321509542dedb14ec10), [top-allowed table b597d9f2](https://github.com/mzch0210/KuaiLive-Agent/commit/b597d9f273067f465b01b885e6a3ca631edd4259), and **final source [86653733](https://github.com/mzch0210/KuaiLive-Agent/commit/86653733ac032214d1baaed9f4aed81b21acc045)**.

**Exact-source PDF acceptance — PASSED.** [GitHub Actions #38016815215](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38016815215), [build PDF and log artifact #11655883649](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38016815215/artifacts/11655883649). This build matches source SHA **86653733** and produces **27 pages**. Log checked: **0 fatal LaTeX errors, 0 undefined citations/references, no newly introduced overfull box**; the sole pre-existing **5.51282-pt** Section 3 overfull remains. The actual PDF pages **16–24** were rendered and inspected: §6.1 Figure 2 on page 17, Table 3 before §6.2 on page 18, §6.3 paired factorization and P2 remain in their intended order, §6.4 feature table/DEV mechanisms remain together, and §6.5 finishes page 23 with References on page 24.

**Source-reference integrity:** Main text has **25 distinct citation keys, all present in BibTeX**, **43 LaTeX labels with zero duplicates**, and **zero missing textual \`\\ref\`/\`\\eqref\` keys**. There is **one state figure and four Results tables**, with the full nine-draw P2 matrix and extensive mechanism/budget/latency panels located in their designated **draft** supplements, not duplicated in Results. Main §6 refers to supplementary S4/S5/S6/S7/S9; **S6 is not yet assembled as a final supplement**.

| Acceptance test | Result |
|---|---|
| C1–C3 empirical correspondence and original outline novelty | **PASS** |
| Main text numerical identities, user-level P2 and model/sampling distinctions | **PASS** |
| Conditional inference and noncausal/out-of-distribution limitations | **PASS** |
| No inappropriate all-method SOTA or online efficiency claims | **PASS** |
| Nonredundant primary evidence displays | **PASS** |
| Final source-specific LaTeX build and 27-page visual verification | **PASS** |
| Submission-ready unified S1–S9, author signoff and reference packaging | **OPEN** |
| Unwritten Sections 7–8 and Abstract | **OPEN — later independent stages** |

**Editorial decision:** Chapter 6's **scientific Results content and current standalone layout** are ready to serve as the evidentiary foundation for further manuscript stages. **The paper itself is not submission ready** until formal S1–S9 and subsequent sections are completed, approved and finally cross-checked.

## Primary sources and scope references

- [Official Knowledge-Based Systems description](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051): original AI research, recommender systems, intelligent prediction/decision support and balance of methods and applications.
- Krichene & Rendle, [On Sampled Metrics for Item Recommendation](https://doi.org/10.1145/3535335), *Communications of the ACM* 65(7), 75–83 (2022); original KDD 2020. Used only to delimit an **existing** known sampled-ranking phenomenon, not to claim new sampled-metric theory.
- Li et al., [Towards Reliable Item Sampling for Recommendation Evaluation](https://doi.org/10.1609/aaai.v37i4.25561), AAAI 2023. Establishes importance of evaluation protocol details without implying the new P2 is independently confirmed.
- [Elsevier Supplementary requirements, updated 2026-06-01](https://www.elsevier.support/publishing/answer/what-are-the-requirements-for-my-supplementary-material): requirements are journal-specific; must follow Knowledge-Based Systems' current Guide for Authors.
