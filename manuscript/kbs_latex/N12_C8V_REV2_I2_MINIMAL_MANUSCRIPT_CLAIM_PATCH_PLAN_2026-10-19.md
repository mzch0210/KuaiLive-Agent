# I2 Rev2.1 · Path A 已确定的最小科学改稿与验收合同（2026-10-19）

**用户已选择路径 A：有限、证据边界明确的经验研究稿。以下为当前执行规格；Rev2 原提议保存在后面作审计。** 本次只修改计划，不修改主文、BibTeX、Supplement 或冻结TEST。最新总方案见 `N12_C8V_SCIENTIFIC_NOVELTY_VALIDATION_AND_PRIOR_EDIT_REMEDIATION_PLAN_2026-10-19.md`。

## 执行顺序及可观测验收

1. **I2-A—先例及逐句来源核对：NEXT。** 核实 Subbiah, Rendle and Aggarwal (CIKM 2024) 的正规书目字段/DOI 10.1145/3627673.3679943，核对当前 `main.tex` RQ2、Related Work、Discussion及 `kbs_references.bib`。冻结的30k F/S差值、调用数、CI/Holm与同队列独立性、RQ3原Popularity门槛缺口不得修改；给出三处确切段落修改表与未改内容清单。
2. **I2-B—三处最小正文改稿：NOT STARTED。** 在 Related Work 区分KDD2020采样指标与CIKM2024训练时排名校正，不能宣称提出新统计校正算法；在RQ2/Discussion精确定义原S为575候选、目标后保留的**未校正**标签，明确B1 Adapted使用F标签；在Discussion说明训练后合法corrected-S选择器仍未检验，可能缩小F/S结果差异。不得新建主Results表、重新解释V2诊断为新确认实验、重复全篇重构。
3. **I2-C—回归防篡改与真实双PDF：NOT STARTED。** 迁移任何因Discussion/Related Work改写而过时的旧C5文本指纹，仍保护11张Results原表与4迁入Supp原始17行49cell、原公式、样本/调用基数与所有冻结统计结果；编译主文/完整Supplement、审查BibTeX和引用、无undefined refs、人工逐段对照主张。页数允许有证据支持的小幅变化。
4. **I2-D—真实独立科研审阅：NOT STARTED。** 由人类方法学/推荐系统研究者判断 candidate-regime-indexed knowledge-use supervision 是否具有足够KBS原创性，尤其审查corrected-S替代解释仍开放、DEV同队列探索、同采集期30k、非严格同调用、H2 composite Null与不完整预验收；过去助手模拟审稿不替代这一环节。
5. **C8-A—真实作者最终批准/投稿：NOT STARTED。** 核对KBS当时有效的官方作者指南、Highlights、CRediT/AI辅助声明、Funding/COI及数据使用的实际权限；数据许可元数据的差异并不自动禁止投稿，但隐私/未经授权分发应按实际情况评估。未获作者批准不合并PR、不宣称投稿。

**V2正式裁决：** 私有数据及原B1标签审计已通过；两个简单校正启发式尚无对条件增量效用监督/受限策略的有效证明，`V2b = NOT_RUN_BY_DESIGN_FOR_CURRENT_CANDIDATES`。这不否定所有可能的corrected-S。路径A主线不再把新corrected-S训练视为投稿前必完成任务，除非作者以后另立更强研究目标。

**当前尚无论文改动。** 37页主文、47页补充材料是最近一次既有CI的页数，而不是Rev2.1新编译后的结果。

---
## 历史附录：Rev2 I2改稿建议（供来源审计）

# N12 C8V Rev2 I2 | 最小论文主张修订清单（仅审稿建议，未改稿）

2026-10-19。**I2 analyst source-to-claim audit completed / actual manuscript patch NOT STARTED / independent referee and author signoff PENDING**. This review reads the unchanged 37-page `main.tex`, the 47-page supplement and original B1/N9/B4-A records; it does not create new TEST or overrule past frozen results.

## Current accurate, verified claims (retain without reopening)
- Abstract and Introduction already emphasize the fixed Memory expert vs fixed Base, F/S candidate-indexed labels, M3 extra same-period 30k and nested 4096 historical null. The Abstract states DEV decision discrepancy 21.32/23.01 **percent of requests**, not of Memory invocations.
- Results RQ2 (paragraph `Actual-candidate labels improve frozen policy outcomes`) accurately reports full policy comparison SAS +.005391/GRU +.003585 and F/S calls SAS 8704/9105 GRU 8629/9168, noting >1pp natural difference. Exploratory B1/DEV is not independent H1 causal mediation; the Adapted arm is explicitly F-label-assisted in Methods and Supp.
- RQ3 validation correctly distinguishes observed null support and ~76.8% history perturbation from the unverified original same-cohort TRAIN-only Popularity pre-reveal subgate.
- Always Memory unbounded M3 accuracy is stronger and *old pointwise Utility* matched-latency is adverse; both acknowledged.
- The old B1 three-arm, A1 eight budgets, A2 Direct/Two-stage and B2 sources already exist; none should be ordered again to support I2.

## Priority wording gaps to address in targeted revision
1. **P1 nearest correction prior work**: Related Work's candidate-dependent paragraph currently cites KDD2020 sampled metric inconsistency but not the closely relevant negative-sampling *training rank correction* precedent. If citing CIKM 2024, verify official bib fields, add one accurate sentence explicitly differentiating evaluation correction and sampled-rank estimator for trained recommendation losses from this study's request-level paired relative NDCG. Do NOT credit N12 with inventing rank correction. Recommended first-party source: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ .
2. **P1 alternative-explanation boundary**: Results/Discussion currently compare F to 'sampled' S but never explicitly state that this is the **uncorrected, retrospectively target-retained 575-candidate** B1 training label. A concise RQ2/Discussion qualification should distinguish S from (a) B1 Adapted uses F target labels, and (b) a statistically valid F-unassisted corrected-S candidate, **which has not been tested as an actual trained gate**. A valid such method might narrow the observed gap, which remains open.
3. **P2 negative method screen in manuscript?** V2a post-hoc 50,049 same DEV label diagnostic (#39237415095) shows that naive full-rank linear expansion worsens paired relative utility MSE (SAS .154548 → .193363; GRU .156084 → .193387), while uniform full-rank posterior shrinks MSE (.082978/.087529) under an unsupported prior but does not improve toy sign-gate regret. This is a **method selection diagnostic on the same DEV**, not a confirmatory result or actual policy ablation. Avoid opening a new Results table or selling it as a new study. Optional single bounded limitation citation in Supplement after author review, not mandatory for submission.
4. **P2 causality and cost boundaries**: Maintain original test call nonparity, DEV exploration vs same-period 30k, composite H2, unverified acceptance subgate, and old pointwise timing limitations. No alterations to numeric claim contracts.

## Minimal patch plan if author accepts scholarly scope
- Related Work `Candidate-Dependent Ranking`: a single CIKM2024 prior-art sentence after Krichene 2020; add the new reference in BibTeX with bibliographic check.
- RQ2 or Discussion `From Supervision Regime to Allocated Knowledge Calls`: a short sentence that S is the original **uncorrected** sampled-label protocol; adapted was F-assisted; no sampled-only statistically corrected alternative was evaluated as a fitted selector.
- Discussion `Source Validity, Evaluation Limits and Actual Operating Conditions`: one honest limitation: 'A statistically well-founded correction of sampled supervision might narrow this difference; our results do not rule it out.' This MUST NOT be stated as proof that any particular correction works.
- Highlights generally already bounded and do not need rewriting.
- No new figure, equation, table, claim of method invention or revised significance value. The existing C6/C7/C8V dual PDF test suite should be rerun after any manuscript text/BibTeX edits; watch previous guard fingerprints if they are scoped to text outside results.

## Method decision and review gate
**V2a analyst judgement: NO QUALIFIED CORRECTED-S ESTIMATOR CURRENTLY IDENTIFIED. The two tested heuristics do not pass the scientific-increment gate. For these candidates V2b = NOT_RUN_BY_DESIGN; not an impossibility theorem about all corrected-S.** The resulting paper can use **bounded empirical route A** without re-running old TEST. Alternatives for stronger claims require genuinely new external-time or fair equal-call causal design, not a new iteration on the same revealed B4-A 30k.

This is a proposed micro-revision, not an author-approved change. Independent scientist must inspect prior art, method assumptions and claim strength. Responsible authors must approve final wording, declarations and KBS-specific submission check. PR #6 remains Draft.