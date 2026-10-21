# N12 Rev3.2 W1｜一页核心论证蓝图与 Results 场景分镜

**2026-10-20 | W1 EDITORIAL BLUEPRINT PASS FOR W2 PREPARATION / W2 NOT STARTED / MANUSCRIPT UNMODIFIED.**
与 W0 逐段归属表配套：\`REV3_2_W0_CLAIM_ROLE_AND_PARAGRAPH_MOVE_MATRIX_2026-10-20.md\`。本文是结构规划，不是可以直接粘贴冒充新科研贡献的主文或作者投稿承诺。

## 1. 全文“五句故事”及依赖关系

1. **Problem.** A pre-existing user–creator Memory source can complement a trained sequential recommender, but its value is the *increment over that incumbent on the currently eligible alternatives*, not the standalone Memory ranking score.
2. **Gap.** Standard sampling-evaluation work shows candidate sensitivity, and expert-deferral work studies allocating predictions; what the N12 offline evidence directly measures is how a candidate-regime-dependent **Base-relative supervised label** changes downstream allocation of a *fixed relationship knowledge source*.
3. **Estimand/decision contract.** For each candidate regime \(r\in\{S,F\}\), use \(\Delta_r=u_{10}(M;r)-u_{10}(B;r)\) to learn a gate from **pretarget** \(Z\); freeze separately trained/calibrated S- or F-supervised *complete policies* and evaluate both on identical full-active \(F\) candidate rosters. S is **the original uncorrected, target-retained 575-candidate offline supervision**, not a universally strongest S-only competitor.
4. **Primary evidence.** In **30,000 additional same-period, frozen M3 target events**, the F-aligned complete policies outperform their originally tested S-aligned counterparts under each policy's natural call rate: SASRec weighted full-F NDCG@10 \(+0.005391\), 95% CI \([0.003646,0.007174]\), F/S Memory calls \(8704/9105\); GRU4Rec \(+0.003585\), CI \([0.001599,0.005576]\), calls \(8629/9168\). The natural calls differ by 1.337/1.797 pp and thus this is **not** a strict equal-call single-label causal estimate.
5. **Meaning.** The DEV allocation trace (21.32% / 23.01% F/S different decisions on the same 50,049 DEV events) illustrates how policy decisions differ; a **parallel**, nested 4096-event authentic-versus-constrained-history-null analysis shows composite historical-source value \(+0.031145\), CI \([0.027389,0.035098]\). The generalizable study design lesson is that an incumbent-relative selective-knowledge-use claim must specify source, candidate universe, training-label regime and resource objective together; no corrected-S elimination, production cost savings or long-term causal user-welfare conclusions are implied.

## 2. 核心论证关系图（非统计因果识别图）

\`Viewer–creator history + fixed Memory; fixed Base; available candidates\`
→ \`Candidate-indexed realized Δr and pretarget conditional estimate ηr(Z)\`
→ \`S-supervised versus F-supervised frozen complete invocation policies\`
→ **\`H1 same-period 30k full-F ranking outcome and natural calls\`**
↘ *explanatory same-DEV sibling* \`G2 50,049 allocation differences\`

**Parallel validation of the source, not an effect of H1:** \`Authentic history\` vs \`closed-hour, time/availability/margin constrained composite null\` → \`H2 nested 4096 F ranking\`.

**RQ1 input observations**: Twitch historical-state diagnostic and the original KuaiLive **room** 10,222 paired sampled/full ranking reversal; these motivate but do not causally identify RQ2.

**Operating boundary**: Invocation cap is a DEV design constraint; Always Memory can be better unconstrained and the old pointwise gate has measured additional overhead. This is not a verified production resource saving.

## 3. 一页读者阅读线路和章节责任

| 读者的问题 | 唯一主要章节 | 为下一章创造的期待 |
| --- | --- | --- |
| Why historical knowledge *sometimes* helps but not uniformly? | Introduction §1 and RQ1 §5.1 | Need a Base-relative, candidate-sensitive valuation target |
| How does candidate sampling get into the decision, not only the metric? | §2 closest literature + §3 Δ/η/policy | Need frozen policy comparison under intended full candidates |
| What is the principal observed consequence? | **§5.2 H1 30k** | How did specific request allocation change? |
| Which requests changed knowledge use? | **§5.3 G2 DEV** | Is this an artefact of a useless historical specialist? |
| Does authentic history carry information under unchanged current F? | **§5.5 H2 composite source null, parallel validation** | What is known about use conditions and limits? |
| Why use this decision contract under budgets? | §5.6/§6, A1+DEV timing | Conclusion, a scoped knowledge-system design implication |

**§5.4 原始Twitch/M3 TEST策略结果是基础能力证明**，不能插在H1前变成主创新。避免把最初 G5 6 fits 称为六个独立新TEST。RQ1 room是ranked room、M3是persistent author；不能跨任务直接比较同一个因果效应。

## 4. Results six-scene outline & transition contracts

### 5.1. Candidate- and incumbent-dependent relationship value
- Claim: value is contextual; use Twitch recoverable-not-represented state and paired room regime reversal.
- Evidence: Twitch 44,221 TEST and the originally inspected 10,222 **room** events.
- Exit sentence function: a candidate-dependent value target can supply different selection supervision.

### 5.2. Main: Frozen policy consequences of candidate-aligned supervision
- First paragraph: explain the preexisting original M3 fixed Base/Memory and development-trained gates in **2–3 sentences**, without showing all original TEST comparisons.
- Deliver \(n=30,000\) H1 F/S full-F table within opening section; exact weighted-quality CIs, natural calls, S-label information contract, same-period event identity.
- Exit: policies differ; inspect *which requests* are reallocated on separate same-period DEV events, without treating G2 as an H1 mediator.

### 5.3. Allocation of historical knowledge across requests
- Evidence: original 50,049 DEV, 12,628 users; SAS 10,672 (21.32%), GRU 11,517 (23.01%) different decisions; F-only and S-only event-level full utility contrasts, net allocation accounting.
- Exit: fixed Memory policy is meaningful, but its unconditional value and independent source validation require separate checks.
- Note: same DEV retrospective G2, no new independent TEST.

### 5.4. Frozen base-relative selection evidence across incumbent families
- Short original Twitch Utility selection and original M3 TEST two ranker families×three seed fits. Main tables may migrate but no numerical source changes.
- Avoid describing overall selection strength as a new candidate-correction theorem.
- Exit: full-F H1 policy evidence is more specific than generic Utility-vs-Base; authentic history relevance addressed separately.

### 5.5. Authentic relationship source under fixed current candidates
- H2 4096 nested; authentic .334942 vs mean composite null .303797, weighted difference .031145 and user CI; underlying relationships strongly rewired and **one original TRAIN-only Popularity prereveal acceptance subgate NOT VERIFIED**, not overwritten by DEV completion.
- Smaller 1024 DEV and source component reversal stay supporting in S10, not promoted.
- Exit: source has composite value but operating goals still depend on actual cost and quota.

### 5.6. Operating conditions and measurement
- Count quota is externally stipulated; at no extra cost Always Memory full-F weighted quality .348744 exceeds F gates .305446/.304530; old 256DEV pointwise gate 1.769ms slower than Always Memory .692ms, newer vectorized F gate not production timed.
- End with: observed design is knowledge-use *under an explicit decision objective*, not generally faster and more accurate production deployment.

## 5. Figure, table and equation reader-orientation

- Intro figure \`fig:knowledge-value-chain\`: research-question and evidence *branch* only; RQ3 not downstream of H1.
- Method figure \`fig:framework\`: deployment pretarget-Z information contract and offline label training, **not** duplicate the RQ map; merge only if semantics can stay clear.
- **Main §5.2 table** \`tab:results-m3-b4a-supervision\` should remain fully visible. §5.5 historical null table \`tab:results-m3-additional-relation-identity\` must remain visible and link to the validity qualification.
- §5.4 \`tab:results-m3-robustness\` can move to Supplement after exact cell-preserving and cross-ref migration; \`tab:results-m3-policy\` retain a compact main summary for historical baseline context if helpful. §5.6 cost table might move to Supplement only if the main passage still tells actual measured negative cost evidence.
- No rewrite of mathematically identical \(\Delta_r\), \(\eta_r\), policy identity or numerical intervals to fit a literary arc. Current nine core method math environments are source-locked.

## 6. 首读试验（编辑模拟，不是独立人类同行审查）

**Q: What is the paper actually showing?**
A: Candidate-indexed relative-value labels for a fixed relationship source can change the *full deployed policy choice set* and ranking quality, in the measured offline protocols.

**Q: What is strongest?**
A: The held-aside same-period 30k previously unevaluated event IDs with both frozen complete policies compared under identical full-active ranking rosters, not strict equal Memory calls.

**Q: What is independent corroboration?**
A: RQ1's Twitch/room diagnostic and RQ3's nested H2 source randomization are different test roles; H2 is nested not a separate future cohort, G2 uses preexisting DEV.

**Q: What would be misleading?**
A: Calling G2 a causal mediator, pretending F beat corrected-S, claiming six fits are six new TEST populations, saying the gate saves actual inference time/cost, suppressing H2 acceptance gap or implying online user satisfaction gains.

**Editorial verdict**: **W1 STORYBOARD IS SCIENTIFICALLY CONSISTENT AND READY FOR W2 PLANNING**, subject to W0 fixture guards and a human full-paper read after W2–W7. This is **not** a verified independent external reviewer, nor a journal acceptance decision.

## 7. W2 exact entry checklist

1. Recheck exact science SHA+blobs and paragraph anchors before writing \`main.tex\`; do not rely on previous line numbers after source change.
2. Keep all seven original Results LaTeX table numeric blocks or move them with complete 17-row/49-cell and original-label migration fixtures, **never silently delete**.
3. Main \`eq\` bodies and 30k/H2 values immutable; distinction between main vs DEV/TEST cohorts survives Results rearrangement.
4. After Result changes use content-based QA for numeric cells and references; old section-slice fingerprints must be recalibrated with evidence-protecting invariants—not disabled.
5. No new paper claims, citations or dataset; follow W3–W8 for subsequent integration and final dual-PDF QA.

**Current state**: W0 and W1 documentary analysis only; \`main.tex\`/bib/Supplement/Highlights and original TEST remain untouched; PR#6 Draft; X1/X2 blocked; KBS P5 human signoff pending.
