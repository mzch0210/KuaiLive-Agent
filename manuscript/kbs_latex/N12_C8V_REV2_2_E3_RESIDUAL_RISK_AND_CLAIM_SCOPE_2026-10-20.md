# N12 Rev2.2-R1 E3 | 残余竞争解释、实际成本与历史 Null 主张强度核查

**日期：2026-10-20｜状态：E3-R1 ANALYST_AUDIT_COMPLETE / PASS_WITH_ONE_L1_WORDING_FIX / NO_NEW_EXPERIMENT / E4_AUTHORIZED_ONLY_FOR_SOURCE-GROUNDED_MICROEDIT。**

此项是对已核实公开论文源及项目冻结报告的**AI 辅助内部科学审核**，不是新的 self-host TEST、原始样本独立复现、真实外部人类 referee、作者 GO 或 KBS 投稿。方法学原创性风险保持 HIGH/CONTESTABLE。前序 E0/E1/E2 均完成；E2 裁决为 NO_MAIN_TEXT_CHANGE_REQUIRED，E3 不得将它重置为“必须大改 RQ2”。

## 0. 审计来源与已冻结科学基线

- 仓库 `mzch0210/KuaiLive-Agent`，分支 `kbs-n12-single-thesis-restructure-plan-20261014`；主论文 `manuscript/kbs_latex/main.tex` blob `c713811acf5c6c47df3e5cb34ee8a7af5cc4ff5e`；Highlights `65e3cddaeb67a1197c07683632894f6d21cce215`；Supplement S1–S10 blob `bb7d11074445988ecf637f895dad55084fc9577b`。这些是 E3 审阅时的公开文件快照，仓库后续仅新增审计文件不等于新文章构建。
- 上次真实科学论文双 PDF CI：C8V #39351014765、C7 #39351014645，38p main/47p supplement；相应科学提交 `7e4c5a6f616e22226f55e2396815d48cc838bf96`，不以本计划/审计提交冒充新的 CI。
- 冻结源：`N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md`（H1/H2 A4 #38518785650、A5 #38519174441）、`N10_ROUTE_C_C2B_MATCHED_DEV_COST_AND_R2_VERDICT_2026-10-14.md`（成本 #38530526158）、`N12_C8V_REV2_V2A_FINAL_METHOD_GATE_AND_V2B_STOP_2026-10-19.md`、`N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md`、`N12_C8V_REV2_2_E2_EXISTING_CONTRIBUTION_INCREMENT_AUDIT_2026-10-20.md`。
- 外部方法边界（非本次新颖性定论）：Krichene/Rendle KDD 2020 sampled ranking inconsistency + corrections https://research.google/pubs/on-sampled-metrics-for-item-recommendation/；Mao/Mohri/Zhong ICML 2024 deferral with costs https://proceedings.mlr.press/v235/mao24d.html；KBS 官方范围及原创性目标 https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。

## 1. 四项竞争解释分类结果

| ID | 来源已证实的事实 | 论文实际锚点 | 仍未识别/不能写的强论断 | E3 分类和 E4 动作 |
| --- | --- | --- | --- | --- |
| **C1 corrected-S** | 原 S 为 retrospective target-retained **uncorrected 575** 标签；B1 Adapted **使用 F 训练标签**；V2a 的 rank-expansion/uniform-prior 后验诊断未训练可解释的 sampled-only corrected policy，V2b NOT_RUN_BY_DESIGN | Related Work 100；RQ2 513–514；Discussion 624；Methods 326/349 | 不能说所有 sampled-only correction 必失败，不能把后验 MSE/toy regret 当 trained policy 质量 | **ALREADY_RESOLVED_IN_TEXT / L0 NO CHANGE**；真实 corrected-S 竞争解释继续 **SCIENTIFIC_GAP_OPEN** |
| **C2 实际资源/Always Memory** | H1 Always Memory weighted NDCG 0.348744，高于 SAS F 0.305446 和 GRU F 0.304530；匹配旧 256 DEV ×3 warmed pointwise Utility 均值 1.76941ms，Always Memory 0.69165ms；新 vectorized F gate 未测端到端成本；F/S H1 两策略实际调用率差 1.337/1.797pp | Abstract 26；Results 573–599；Discussion 617/626；Conclusion 633；Highlights 5 | 不能宣称 strict equal-call causal superiority、线上节能/成本/延迟收益，也不能以 fewer calls 代替总路径 cost | **ALREADY_RESOLVED_IN_TEXT / L0 NO CHANGE**；真实 quota 动机及最新 F gate serving cost **SCIENTIFIC_GAP_OPEN** |
| **C3 历史来源 Null** | 4096 H2 嵌套在额外 30k 内，真实−三随机化平均 +0.031145 [0.027389,0.035098]；三 seed 共享同一群体；strong ~76.8% rewire 影响多种历史结构；原该 cohort 事前 TRAIN-only Popularity margin **NOT VERIFIED**，部分后验 nonfloor 通过 | Fig.1 TikZ node **原 74 行**写 `Authentic history versus valid historical nulls`；RQ3 表注545/正文563–570、Methods 360、Discussion 622、Conclusion 633 已承认复合干预/子验收缺口 | 没有全部合约预揭盲 Null 检验通过，没有因果识别单个 relation semantic，也非三份独立测试 | **WORDING_FIX_REQUIRED / L1** 仅修 Figure 1 节点：`Authentic history versus constrained historical randomizations`；其他正文 **L0** |
| **C4 样本独立性与曝光局限** | B1/G2、A1/A2 共用 50,049 M3 DEV；H1 30,000 是额外目标 ID 但仍同 2026-03-27~31 记录期，与原 47,575 有潜在用户/历史交集；H2 4096 嵌套；Twitch/room/author 排名单位不同；单正例受已记录曝光政策影响 | Methods 264–267/294/322–374；RQ2 513–534；RQ3 540–570；Discussion 613–624；Abstract 26；Conclusion 633 | 不能称独立未来新采集期、独立外部数据复现、在线 welfare/GMV 因果或把 21.32/23.01% 误认整体 Memory call rate | **ALREADY_RESOLVED_IN_TEXT / L0 NO CHANGE**；真正未来期外推/曝光控制仍为 **SCIENTIFIC_GAP_OPEN** |

**跨材料核查**：Highlights 5 行依次强调候选监督、DEV 高价值请求分配、冻结 F 策略、constrained nulls、unequal call 和不利旧计时；与论文正文一致，**无需再改**。Abstract 同样包含 H2 prereveal 未核证、F/S 不等调用、Always Memory 与成本反例，**无需加入重复限制句**。Supplement 保留 S10 对 Null 事前验收差异与冻结统计来源的细节。Methods 明确 TEST source 新事件与未来独立时间测试的区别。

## 2. 唯一需要 E4 执行的 L1 图内文字修订

**科学问题**：Fig.1 逻辑框 `Authentic history versus valid historical nulls` 在视觉上可能被理解为全部 original prereveal 约束已完成，从而与主文 Table 注释、Methods 和 Discussion 实际的 **NOT VERIFIED** 相矛盾。图框不宜通过图中“valid”直接认证完整 Null protocol。

**建议精确差异（纯措辞；结果不变）**：

```diff
- Authentic history versus valid historical nulls};
+ Authentic history versus constrained historical randomizations};
```

- 保持 RQ3 图的结构、候选 F、固定 scorer、原运行结果、表格、指标和相邻正文不动；
- 这里的 `constrained` 只表示已明确说明的 time-/author-activity-/closed-hour 约束，不自动认证未验证的 TRAIN-only popularity pre-unseal 检查；
- 如果图框长度影响版面，允许仅为适配框宽重排 LaTeX 源码换行，禁止删掉科学限定；
- Figure caption 已明确 RQ3 是 parallel source validity，不构成 RQ2 因果中介，无需添加防御性新句。

**相似但不判为必改**：Introduction 的 `Independent fixed-candidate evidence for the historical source` 随后同一贡献明确其为 `parallel composite source-validity test`，Methods 及 Discussion 也说明 H2 嵌套同 30k、三 seeds 同一 cohort。此处 `Independent` 表达论证路径相对独立，现有上下文足以阻止“独立新 cohort”的误解，**默认 L0，不与 Fig.1 做成无必要的双重文字改稿**。若 E5 视觉审查或真实 E6 学者提出具体误解，可凭实质 issue 另行处置。

## 3. 禁止重复的改稿与科学识别不足

1. Related Work 已引 CIKM 2024 并在 Discussion 624 明确 corrected-S 未训练。**不要**把旧 V2a toy MSE 搬进主 Results，也不要通过测试已揭盲 30k 为 corrected-S 选择阈值。
2. Results 573–599 已有 A1 预算前沿和旧 Utility 不利 timing，Discussion 626 明确没有部署节省。**不要**再扩写一遍“Always Memory 最优”“gate 可能慢”。
3. H1 原样报告质量+calls 实际两个 operating points，不满足 1pp same-call；不新增无验证 matched-call CI、资源投入最优曲线或成本价格标签。
4. RQ3 有 composite historical source sensitivity，但非关系语义特异性因果证明；绝不事后补签 popularity prereveal 条件。
5. B1/G2 DEV 50,049、额外 H1 30,000、H2 nested 4,096 不是三个统计独立新时期，旧原 G5 47,575 上的六个 fit 也不是六个独立 TEST。
6. 不修改现有结论强度来回避 KBS 创新性 HIGH 风险，不假装 C1/C2/C4 的公开披露已解决对应的实证空缺。

## 4. E3 状态与 E4/E5 移交规则

- **E3 ANALYST_AUDIT_PASS / C1,C2,C4 已有文字充分 / C3 一处 L1 科学准确性措辞风险**。
- **E4 仅授权**修改 Fig.1 `valid historical nulls` → `constrained historical randomizations`，制作原位置与改后 SHA 的最小差异文件。不批准 Introduction、Related Work、RQ2、Discussion、Conclusion、Highlights、Supplement、BibTeX 任意“强化性”改写；如在 E4 发现别的独立事实错误，另记录并先停机审查。
- **E5 实现条件**：当前 N12 C8V + C7 工作流受 `main.tex` 推送触发，必须在**实际**新科学源码 commit 上通过两项双 PDF / 冻结事实与符号守卫，记录 run ID、head SHA、工件 IDs、PDF 页数；失败不得以关闭测试掩盖。原 38/47 页和 #39351014765/#39351014645 只是**旧 PDF 基线**。
- **E6 保留**：真实外部人类科学审阅与作者研究/披露签署皆 PENDING，KBS 投稿 HOLD。方法层竞争解释的科学缺口不能凭一次 wording patch 关闭。

**下一步**：E4-L1 一处 TikZ 节点文本修订，随后 E5 真实 CI 和科学/PDF QA。不新增任何 DEV/TEST 实验、统计或私有数据操作。
