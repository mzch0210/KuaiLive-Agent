# N12 Rev2.2-R1 E2 | 现有核心科学贡献增量审查

**日期：2026-10-20｜E2-R1 ANALYST_AUDIT_COMPLETE / PASS_WITH_NO_MAIN_TEXT_CHANGE_REQUIRED / NOVELTY_HIGH_CONTESTABLE / E3_NEXT。**

本记录依据当前 N12 分支公开 GitHub 源码和历史冻结 aggregate、对照已出版研究的官方来源做只读科学审查；**没有**重新载入 self-host 私有训练/DEV/TEST、没有新的实验或置信区间，也不是实际独立人类 referee 审阅。**本阶段不修改 main.tex、Supplement、BibTeX、图表、冻结模型或阈值。** 不能将本 E2 文件提交视为论文 PDF CI 成功或新的外部验证。

## 0. 基准与 E2 的审查对象

- 分支：`kbs-n12-single-thesis-restructure-plan-20261014`；E0 审核现行 `main.tex` blob `c713811acf5c6c47df3e5cb34ee8a7af5cc4ff5e`；最后真实双 PDF CI 基线为科学提交 `7e4c5a6f616e22226f55e2396815d48cc838bf96`、Actions #39351014765 / #39351014645，主文 38p、Supplement 47p。更新审查文件本身不是新的 PDF 编译。
- 已完成：Rev2.2 E0 来源映射 / E1 最近邻研究对照；Rev2.1 的 CIKM 2024 corrected-rank 引用、原始 S 未校正定义及 sampled-only corrected-S 未验证边界。
- 当前 E2 唯一要解决：**已经完整写入论文的 candidate-supervision → call reallocation → separately frozen F-ranking policy evidence，是否确有遗漏的非平凡科学事实/需要编辑的段落？** 不把新增重复段落视为科研增量。
- 已核对论文章节：Abstract 25–27，Introduction 37–52，Related Work 90–102，Methods 108–213 / 290–374，RQ2 442–534，Operational Conditions 573–599，Discussion 603–626，Conclusion 631–633（行号为 E0 审计版本）。
- 论文统计的 RQ1 Twitch 44,221 与旧 KuaiLive room 10,222，RQ2 M3 DEV 50,049 和额外 30,000，RQ3 同 30k 嵌套 4,096 **都不是同一个统计对象**；原六 M3 fitting seeds 共用一组 47,575 TEST 请求，不能当六个独立实验。

## 1. 研究对象和最近邻先例：新意处于下游实证合同，不是通用理论

固定专家 `M`、指定已训练 incumbent `B`、候选 `F` 和 pretarget 特征 `Z`，离线真实标签 `Δ_F=u_10(M;F)-u_10(B;F)`。同一个设计在 `S`（保留事后观测目标的 575 候选）上构造 `Δ_S`，分别训练、DEV 内校准 complete F/S policies，最终都在 F 上评价。

- Krichene & Rendle (KDD 2020) 已说明 sampled ranking metrics 可能与 full 排名不一致，且 correction 亦是先例：https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ 。
- Subbiah, Rendle & Aggarwal (CIKM 2024) 已讨论负采样 rank corrections 在 WARP/LambdaRank 训练中的作用：https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ 。并未据此验证本特定 paired relative-utility selector；但合法 corrected-S 是未排除的强竞争解释。
- Mao, Mohri & Zhong (ICML 2024) 已建立带预训练 predictor、专家和成本的 deferral 学习理论：https://proceedings.mlr.press/v235/mao24d.html 。差值回归、阈值、专家指派不是 N12 的算法原创。
- KBS 官方范围允许推荐/决策支持，但强调原创性及创新性，不自动承认“应用 sampled metrics + deferral”达到贡献门槛：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。

**E2 非平凡实证对象（严格表述）**：在一个明确的 *historical relationship specialist–incumbent–dynamic eligible roster* 任务合同里，候选制度不仅改变被报告的离线 rank utility，也改变拟合后具体请求的知识调用选择，并在另行冻结的、同采集期未曾评分的作者 ranking IDs 上体现 complete-policy F-ranking 差异。**新观测事实**而非新 `Δ`/deferral 方程或采样校正理论。

**可证伪挑战而非自证 novelty**：若该现象仅是已知 sampled bias + defer 的直接预期实现、不具一般izable 设计含义，则目前材料不能仅凭 E2 把 HIGH 创新性风险降级。此点保留给真实独立学者 E6 判断。

## 2. 原始证据和已写入正文的增量逐项核对

| 对象 | 冻结/原始来源 | 一致统计对象与数值 | 正文锚点 | E2 编辑裁定 |
| --- | --- | --- | --- | --- |
| S/F/Adapted 监督合同 | `experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`，Actions #38365477972 | 50,049 M3 author DEV / 12,628 users；同 12 pretarget F 特征及模型容量；S 仅用原 sampled labels；Adapted 可用训练阶段 F labels，**不是** sampled-only corrected-S | Methods 332–348、RQ2 513–534、Discussion 613–617 | **L0 NO CHANGE** |
| F/S 质量与请求重配置 | `manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md`，Actions #38389150075；公开 JSON | 同 50,049 DEV：SAS F/S 0.302658/0.296499，F-only/S-only 5350/5322，switch 10672 (21.32%)；GRU F/S 0.303093/0.298123，5639/5878，switch 11517 (23.01%) | Results 529–534、Discussion 615 | **L0 NO CHANGE** |
| 重新分配的是更高平均 value 请求 | 同 G2 | SAS 换入/换出平均 `Δ_F` 0.133417/0.076194，整 cohort 贡献 +0.014262/−0.008102=+0.006159；GRU 0.126600/0.079135，+0.014264/−0.009294=+0.004970。换入和换出两组均为正；代数分解**不是**新因果机制 | Results 529–534、Discussion 615 | **L0 NO CHANGE** |
| H1 额外封存策略比较 | `manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md`，A4 #38518785650 / A5 #38519174441 | 额外同采集期 30,000 target IDs、10,387 users、20 cells；SAS F−S +0.005391 CI [0.003646,0.007174]，Holm p=.000600，F/S 8704/9105 unweighted calls；GRU +0.003585 CI [0.001599,0.005576]，p=.000800，8629/9168。分别 F 少 401/539 calls | Abstract 26、Results 513–528、Discussion 613/617、Conclusion 631 | **L0 NO CHANGE**：已有主表和完整解释 |
| 额外 H1 的识别限制 | 同 A4/A5；H1 原 protocol | F/S calls 差 1.337/1.797pp > 原 1pp tolerance，分别校准的完整政策而非同资源标签单因子效应；weighted NDCG 与 unweighted calls 不能构造未验证的成本或 weighted call frontier；新 IDs 不等于未来时间外推 | Methods additional-target、RQ2 表注/正文、Discussion 617/624 | **L0 NO CHANGE** |
| A1 8 quota 内部 DEV frontier | `manuscript/kbs_latex/N9_A1_UNCONSTRAINED_POLICY_FRONTIER_2026-10-13.md`，Actions #38382693869 | 同 50,049 DEV：SAS 30% NDCG .302658 → 50% .319654 → 90% .341040，原 Always Memory .343509；无 cap 时大多调用 Memory。不是 30k 新质量–成本曲线 | Results 576–579；Supplement S10 | **L0 NO CHANGE** |
| A2 决策目标控制 | `manuscript/kbs_latex/N9_A2_DECISION_TARGET_CONTROLS_2026-10-13.md`，Actions #38383262381 | 同 50,049 DEV：30% Direct-vs-Two-stage SAS +.001310、**+318 calls**；GRU +.000119，CI 跨 0，**−59 calls**。Direct 相对 Difficulty / Specialist Quality 优势较明显，但无法声称普遍压倒 two-stage 或新 deferral 算法 | Methods controls / 既有 Supplement S10 | **L0**：当前补充材料承担合适证据层；不把小且 budget 不等对照强行搬成主创新 |
| RQ3 平行来源有效性 | 同 A4/A5、原 N9 B2 | H2 4096 是 30k 嵌套样本，authentic−三 null 平均 +.031145 CI [.027389,.035098]，同三 seed 共一批请求；TRAIN-only Popularity prereveal gate NOT VERIFIED | Results 540–570、Discussion 622 | **L0**；Figure 1 `valid historical nulls` 为 E0 已识别的 E3/L1 候选，非 E2 的额外科学发现 |

**来源层级说明**：核对的是仓库保存的报告、聚合 JSON、正文以及 Actions ID 的书面记录；这不是重新从私有事件计算指标。G2 与 B1/A1/A2 在同一 post-G5 DEV 并非相互独立的科学重复实验。

## 3. 最强实证链是否已有？——已写入，未发现新的主文解释缺口

### 3.1 RQ2 的完整桥梁已存在

- `main.tex` §3 明确 `η_r(Z)`、`Δ_S`、`Δ_F`、`R_{S→F}` 及 fitted complete-policy 对比的含义，不假定 F 必优。
- §5 独立列示训练/DEV/TEST、原 B1 三臂信息权限、额外 30k outcome-blind 冻结、四个 gates 和后验样本权重/CI，不能把 adapted control 错当纯 sampled-only correction。
- §6 RQ2 已直陈 **higher F NDCG at fewer realized F Memory calls** 的两个 H1 点，列出用户 CI、自然 calls、Holm、权重和 1pp 未达标；G2 请求级 21–23% 分配与 F-only/S-only 拆解以及 A2 辅助实验在正确证据层级。
- §7 第 613–617 行进一步说明两个 switched groups 平均 `Δ_F>0`，意义是优先级排序而非简单避免负效用；明确 G2 同队列代数恒等式不构成额外独立 TEST，也不是 H1 的 identified mediator。
- 摘要、§1 三贡献和结论均指向同一限定实证主张，不存在 E2 级别必须“重新强调 RQ2”或再造新图表的理由。

**核心判断**：若再次追加 switch 表、F 减少 calls 或无约束 Memory 的限制，将复制第 513–534、573–599、613–626 行，增多叙事噪音而不增加科学证据。默认 L0 / **NO_MAIN_TEXT_CHANGE_REQUIRED**。

### 3.2 有价值、但当前不具新增主文价值的背景

- B1 third arm adapted 使用 **F 标签**，不是合理 sampled-only 修正的测试；已正确说明。
- A1 DEV quota 扫描完整，但自然 realized call 和实际外部资源成本不同；§6 已显示。
- A2 Direct Δ 与独立两头预测的 conditional expectation 目标从理论上线性相同，结果多数同样；因此不能主张 `Δ` 自身必然优于合法 two-stage estimator。现有 Methods/Supplement 分配合理。
- B2 component-source 与候选 regime interaction 在 S10 内保存；非单一历史关系语义机制的识别已在 RQ3/Discussion 披露。**不建议**以增加 B2 比较为新主表主张。

## 4. E2 可证伪科学问题、竞争解释与创新性风险裁决

| 对抗性 KBS 质疑 | 当前可直接回答的证据 | 尚无法识别或排除的解释 | 结论 |
| --- | --- | --- | --- |
| “不就是 sampled metric bias + learning-to-defer？” | 不是仅评价指标方向：同 DEV 21–23% requests 改派且换入平均 full-F Memory value 更高，另封存 30k complete policies 有较高 F-ranking质量 | 该 downstream difference 是否构成显著非平凡的新理论/可迁移知识仍由审稿人判断；可能是已知原理在新任务中的可预测结果 | **NOVELTY_HIGH_CONTESTABLE / HUMAN_REVIEW** |
| “F 优势是不同 label 还是不同 thresholds 和 calls？” | B1 特征、模型容量、frozen rankers、候选保持一致；H1 完整 policies 同额外 F cohorts，call 数如实列出 | 不同训练标签与 DEV calibrations 共同变化，且实际 calls 超过 1pp 差额，因此**没有**严格标签单因子/等调用因果估计 | **COMPLETE_POLICY_ONLY** |
| “对照原 S 太弱？” | 明确 S 事后保留目标且未校正；已有 Adapted 需 F 标签；V2 两种纠偏诊断不适合作为政策宣告 | 未训练真正合法的 sampled-only corrected-S selector；不能说所有校正方案均不及 F | **OPEN_CORRECTED_S_RIVAL** |
| “为什么不总用 Memory？” | H1 Always Memory .348744 > SAS F selector .305446；原 warmed gate .1.769ms > Memory .692ms，A1 无 cap 时几乎全选 | 外部 quota 真实性、新 F gate 实时成本未测；不证明线上计算资源收益 | **SCOPED_QUOTA_ASSUMPTION** |
| “关系本身与 supervisor 差别是因果同一机制？” | 固定 F 候选历史 Null 在 H2 下有 source sensitivity | 扰动改变多种历史结构，三 seeds 非独立样本，原 H2 预揭盲 popularity 条件 NOT VERIFIED；RQ3 不是 RQ2 的 mediator | **PARALLEL_SOURCE_SUPPORT_ONLY** |

**实际科学增量审查的结论**：现有实验结果支持一项具体、边界清楚的 **system-methodology/empirical evaluation insight**，但不足以凭本次审查证明不可预期性、方法首创性或一般条件最优性。对 KBS 的真实 originality threshold **不予内部认证**。更强结论需要预先设计的新合法验证及真实独立研究者决定；Path A 不将该缺口伪装成修辞优化任务。

## 5. 候选编辑问题清单（E4 仅据此及 E3 后续裁决执行）

| ID | 当前位置 | source / 证据 | 信息增量 | 风险 / 编辑权限 | E2 决议 |
| --- | --- | --- | --- | --- | --- |
| E2-01 | Intro 47–52、Discussion 603–608 | E1 最近邻、KDD/CIKM/ICML 原始页 | 已有分界且清楚，不产生新的科学信息 | 新增名词易暗示未证理论；L0 | **NO CHANGE** |
| E2-02 | Results 513–534、Discussion 613–617 | B1/G2/H1 | 两组 calls/CI/DEV switch 已同时报道，无额外信息 | 第二次追加同样结果会冗余；L0 | **NO CHANGE** |
| E2-03 | Methods、Supplement S10、Results 529–534 | A1/A2/B1 adapted | 补充层已包含；新主文强调 A2 的小差异可能变成方法首创过度推断 | L0 | **NO CHANGE** |
| E2-04 | Operational Conditions 573–599、Discussion 626 | A1/旧延迟 | 负面事实与外部 quota 已披露 | L0 | **NO CHANGE** |
| E2-05 | RQ3 Figure 1 node（原第 74 行） | E0 和 H2 4096 prereveal null audit | **准确性修复**，不是新科学结果 | 待 E3 审查后执行 L1：`Authentic history versus constrained historical randomizations` | **HANDOFF_TO_E3** |
| E2-06 | 全文“frozen”或“independent”描述 | H1 额外同期间 IDs / DEV G2 | 现文已区分新 event IDs 与新 period | 如果 E3 发现错称独立新时段才修；L0 | **VERIFY_ONLY** |

**E2 不批准新的 Results table、Supplement 一轮迁移、重训 gate、重检原 TEST、伪造 matched-call CI 或更改 Abstract/Conclusion。** 原主文已足够围绕一条限定实证贡献展开；开放创新性风险由 E6 实际同行裁决，不要求 E4 为每个审查环节新增文本。

## 6. 执行结果、停止规则与移交 E3

- **E2-R1 ANALYST AUDIT: PASS_WITH_NO_MAIN_TEXT_CHANGE_REQUIRED**。这意味着已完成审查合同，**不意味着创新性风险解决**或真实外部同行确认。
- **E2 发现新增必改的 RQ2 正文科学缺口：0**。不是主张其他领域研究全部覆盖；只代表当前已经核对的原论文/数据/先例没有要求重复增强 B1/G2/H1 的理由。
- **唯一已记录准确性候选**为 E0 发现的 Figure 1 valid historical nulls；是否、如何改写必须由 E3 跨章检查后再进入 E4。
- 实验/样本/阈值/TEST 绝对不动；不把 50,049 G2 DEV 当成额外独立 TEST，不使用已揭盲 30k 选择新 S correction。V2b 仍 NOT_RUN_BY_DESIGN；不会用内部 E2 判词升级主稿贡献强度。
- **E3 NEXT**：检查 corrected-S、Always Memory/成本、historical Null 的实际图文矛盾和 sample independence，报告 ALREADY_RESOLVED / WORDING_FIX_REQUIRED / SCIENTIFIC_GAP_OPEN / NO_CHANGE；只有确认有问题才在 E4 微调。

**复核来源**：
- 当前主稿：`manuscript/kbs_latex/main.tex`（blob SHA 如上）。
- B1：`experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`。
- G2：`manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md` 及 `experiments/kbs_plan_c/N9_G2_E1_SUPERVISION_DECISION_SWITCHES_PUBLIC_AGGREGATE_2026-10-13.json`。
- H1/H2：`manuscript/kbs_latex/N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md`。
- A1/A2：`manuscript/kbs_latex/N9_A1_UNCONSTRAINED_POLICY_FRONTIER_2026-10-13.md`、`manuscript/kbs_latex/N9_A2_DECISION_TARGET_CONTROLS_2026-10-13.md`。
- 上游 N12：`manuscript/kbs_latex/N12_C6_RQ2_SUPERVISION_TO_DECISION_EVIDENCE_CHAIN_2026-10-19.md`、`manuscript/kbs_latex/N12_C8N_DECISION_ALLOCATION_NOVELTY_REWRITE_QA_2026-10-19.md`。
