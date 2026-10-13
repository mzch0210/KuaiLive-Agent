# N8 — 三项核心学术风险的综合评估与分级解决方案

**日期：2026-10-13。定位：研究方案评估，非新实验结果；原 G5 TEST 与既有 N0–N8 主稿冻结。**

## 0. 执行结论

**新增第三项 P0 核心风险 R3：组合贡献的科学重要性/证据链完整性。** 当前文章已形成统一的*论证叙述*，但尚未在同一可比较任务中证实“候选环境影响知识效用目标 → 价值预测/选择器失配 → 候选感知修复带来决策效益”。前三项 RQ 的现有实验各有意义，但其结合尚不足以自动证明系统级方法或知识系统贡献。

**研究优先级：R3（整体科学问题与机制闭合）≥ R1（与 L2D 及知识门控的创新性差异）> R2（M3 约束合理性与成本反例），前二者相互耦合。** R2 不能用假定 Memory 成本高来消除；Twitch 自身存在 Utility 胜过两个固定策略的准确性证据，但也不证明生产时延优势。

**推荐方案：A 科学贡献证明结构精修 + B0 DEV 数据/候选可行性预检 + B1 同事件候选监督迁移→选择损失/修复试验 + B2 关系知识来源专属性消融；B3 Memory-first 仅在有真实成本动机时补充；C 新独立 TEST 仅当 B1/B2 有非平凡探索性发现、且可以获取未揭示标签和数据授权。** 将三个风险按科学假设与独立判据组合处理，而不是累加新方法。

## 1. 近期可验证的 KBS 与直接近邻研究

官方 KBS 范围： https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 ，包含知识工程、推荐系统、智能决策，但要求原创且兼顾理论与应用。

**KBS 2026 实证对照：**
- Xie et al., MHGFCL (KBS 341:115673, 2026): 异构知识多头自适应门控与知识融合，https://www.sciencedirect.com/science/article/pii/S0950705126004132 ；
- Yerragunta et al., *Dynamic conditional gating mechanisms for Question Answering over incomplete Knowledge Bases* (KBS 346:116167, 2026): 受控检验知识源精炼与门控的互补/重叠，不止叠加几个现象，https://www.sciencedirect.com/science/article/pii/S0950705126008932 ；
- Kim et al., KAPER (KBS 347:116236, 2026): 关系证据提取、选择与具体重排/解释质量形成连贯评估，https://www.sciencedirect.com/science/article/pii/S0950705126009627 ；
- Yue et al., *Collaborative knowledge and personalized preference alignment for sequential recommendation* (KBS 347:116234, 2026): 针对知识缺口和偏好偏差提出联合机制，https://www.sciencedirect.com/science/article/pii/S0950705126009603 。

**早于本研究的重要先例：**
- Narasimhan et al., NeurIPS 2022, *Post-hoc Estimators for Learning to Defer to an Expert*: 固定模型后训专家选择，https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html ;
- Mao, Mohri, Zhong, ICML 2024, *Regression with Multi-Expert Deferral*: 两阶段回归专家选择理论，https://proceedings.mlr.press/v235/mao24d.html ;
- Yuan et al., 2026, *Recommender System as Slow and Fast Thinkers*: DS-Frame 预算约束序列推荐（CIKM 2026 accepted; Sep arXiv manuscript）, https://arxiv.org/abs/2609.02671 ;
- Krichene & Rendle, KDD 2020, *On Sampled Metrics for Item Recommendation*: 采样候选对模型效用的非保序性，https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ 。

KBS 的近期实例表明**一条受控检验的知识机制与决策效益链**可以构成有效论文设计，但不意味着所有组合式研究都必须新建网络。最终学术重要性仍由编辑审稿裁定；不能根据若干论文的录用倒推出本稿录用概率。

## 2. 风险注册：R1、R2、R3 的区别与联系

| 风险 | 审稿问题 | 当前证据 | 缺口 | 优先级 | 状态 |
|---|---|---|---|---|---|
| **R1 创新性** | 相对效用选择是否只是 L2D/DS-Frame 在直播推荐上的实现？ | 明确定义固定 Memory−Base event NDCG 和三任务协议、两次冻结选择 TEST；已有 Direct/Two-stage DEV | 缺少决策问题特有、无法由通用专家分配/采样指标完全解释的*新增机制* | P0 | 部分控制 |
| **R2 实际决策价值** | M3 Always Memory 更准且预热更快，路由有必要吗？ | Twitch Utility 0.58983 > Base 0.58211、Memory 0.53980；M3 Memory 0.34679 > Utility 约 0.302，warmed 0.803ms < Utility 1.802ms | M3 30% call cap 为规定而非证明了真实稀缺；无全路径 serving economic proof | P0/P1 | 需限定；不可声称解决 |
| **R3（新增）组合贡献的重要性** | RQ1、RQ2、RQ3 是否构成一个**互相依赖的知识系统发现**？ | Twitch target-history异质性、KuaiLive 房间候选值反转、M3 六fit路由支撑分别存在 | **同一事件/同一实验协议没有直接检验 RQ2→RQ3，也缺知识身份特异性/失败边界的充分控制** | **P0** | **新增 OPEN** |

R3 不只是 R1 的同义改写。R1 比较已有算法优先权；R3 关切*三部分组合是否在知识价值预测/使用中产生新的可验证、不可分割的命题*。如果删去任一部分，论文应失去哪些可解释/可预测结果？现稿没有完成这一“不可替代性”检验。

## 3. 现有证据与不能从中直接得出的联合结论

### RQ1：关系知识条件价值（相对强）

Twitch TEST 44,221：Memory aggregate 0.53980 < Base 0.58211；target-history 可恢复未代表的 5,539 事件 Memory−Base +0.22045；Utility 0.58983 在 15.04% calls 下同时超过 Base/Memory。注意“recoverable”是目标揭示后才可贴标签，不能输入在线门控。

M3：Always Memory 0.34679 > Base 0.25800（primary seed），未必表现与 Twitch 同一模式。还不能说条件价值的全部原因已被识别；尤其不能从事后目标状态直接推断部署中可见的知识缺口。

### RQ2：候选环境依赖（确凿描述，有限推论）

Original KuaiLive 相同 10,222 **room** TEST 已查看样本，在 sampled 575 候选下 ΔMemory−Base = −0.04120，在 full-active 下 +0.04631；相应 +0.08751 平均配对变化可分成会员资格/normalization参考，但会员资格同时改变数量、组成和竞争。**不直接证明**在候选环境 S 学到的门控在 F 上决策质量一定下降，更不证明某种 candidate-aware 校准会修复这种下降。

### RQ3：选择决策（两项 frozen TEST，仍有约束）

Twitch Utility DEV-frozen TEST 同时胜过 Always Base/Memory；Difficulty TEST count-matched 是回顾性排序而非独立 frozen threshold。M3 Utility 对四个指定 frozen gate 目标在六个 Base fits 提升实际 NDCG、减少实际 calls，但六fit共享47,575事件/12,533用户，三个主 Holms 是 within-fit，不是全局调整；M3 Always Memory 仍在无约束 NDCG 和 warmed DEV 时延上更好。

**当前缺失的真正桥梁：** RQ2用已查看 room TEST，RQ3主实验用独立 author TEST；不能因为同属 KuaiLive 就认为已经同环境检验候选失配如何导致 gate regret。新增证据应首先补这一缺口。

## 4. 一个可被证伪的综合研究命题（不是新数学理论）

**建议中心命题**：

> For a fixed relationship-memory specialist, the candidate regime is part of the definition of its incumbent-relative knowledge value; training a value predictor under a mismatched regime can impair downstream specialist decisions, while explicitly aligning the candidate context may recover decision quality. Historical relationship evidence must provide predictive information beyond generic Base difficulty or popularity.

中文：对固定关系知识来源，候选制度不仅影响离线 NDCG 指标，还影响用于选择该知识来源的**监督目标**；不一致的候选制度可能引入价值估计/策略决策损失，而候选感知训练及校准能否恢复性能是需要检验的问题。

此命题明确区分：
- 已知常识：top-K NDCG 对候选变化敏感；
- 已知技术：专家分配根据条件相对收益；
- **值得检验的交互**：对*显式关系知识*，candidate-induced utility-label shift 是否传导到**在同一目标候选制度下的在线策略质量**，以及不同知识成分是否能够解释这一损失。

若该命题在严谨 DEV 试验中没有出现，必须如实收缩本文的联合贡献；不能仍以“三点组合”代替机制证明。

## 5. B0（第一步，零/低 GPU）数据、缓存与可识别性闸门

先查原始 KuaiLive room 与 M3 author 任务的区别及已有缓存；不能把 10,222 room TEST 与 50,049 M3 author DEV 当作可交换样本。确认以下事项：

1. 是否存在**同一批 DEV 事件**在 full-active 与不同 sampled-candidate 方案下的逐候选 Base/Memory 分数和时间前可观测特征？如果只有各自 NDCG 汇总，不足以复现 gate 的监督迁移；
2. 如果基于既有 full-active logits 重排构造 sampled 候选，原 Base 是否因候选集合进行 score standardization / 全候选归一化？其分数必须按已冻结模型的原候选规则重算/重新标准化，不能把已算好的 F 分数冒充 S 原始路径；
3. 排序时的候选资格、同刻直播活动、TRAIN-known author、目标未暴露、sample seed、tie-break、样本和用户分组能否原样记录；
4. **目标保留式 sampled metric 的 target inclusion** 只可用于回顾性评价诊断，不能作为在线可观察门控特征或在线 candidate generator；
5. 私有数据缓存哈希、模型权重、SHAs 和可用 self-host 环境是否与旧 DEV 冻结记录一致（不访问 G5 TEST 的真实标签）；
6. 能否在 DEV 的用户分组外层验证中得到所有策略**同一批 outer heldout 事件**的 full-active NDCG、调用次数与 paired user CI。

**B0 PASS** 才开展 B1；若评分不可用、不能证明 pre-outcome、或需读旧 G5 TEST 标签，应转为有限现有证据解释，不强行声称完成机制验证。

## 6. B1（最高优先 DEV 试点）：同事件候选失配 → 决策损失 → 校准修复

**设计最小矩阵**（一组 Base/Memory、一个已冻结初始种子开始）：

- **S→F**：仅在 sampled-candidate DEV ranking 增量标签上拟合 relative-value score，最终在 held-out **F full-active 候选**评价门控；
- **F→F**：同 DEV 内外分组下仅用 full-active label 训练的参考价值估计器；
- **candidate-aware→F**：在训练中明确使用候选组成/规模等**决策前观测**特征，或者在内层 DEV 校准 regime-aware score，评价同一 F 目标；
- **controls**：Always Base、Always Memory、原 Utility 可重现 DEV 值、Generic Base difficulty、historical heuristic；与规则失配但 value 模型与大小完全相同的 control；
- 候选大小、构成、历史命中率和 Base 分数分布的影响尽可能分层/配对，而不是从一个 S–F 差异就断言只由 candidate *count* 引起。

**验证：** User-disjoint outer folds 和 inner OOF threshold calibration；heldout outer labels 绝不用于拟合、阈值或选择模型；统一使用 full-active outer evaluation 作为目标制度，控制 observed calls **同预算或提供完整预算-效益前沿**。报告：
1. Predictive validity: candidate-specific delta label 的 MAE/calibration、sign/AUC（AUC 不能代替 rank-NDCG）；
2. **Downstream policy:** outer-F NDCG@10, HR@10, calls, Utility gain / *value of routing vs best fixed policy*, `V_F(pi_F)-V_F(pi_S)`, 95% user cluster CI；
3. Calibration and context-ablation：candidate-context feature removal、support share、number vs composition；
4. Negative results (when S→F matches or exceeds F→F) 必须完整报告。

**跨制度预算公平的防泄漏约定：** 必须区分两类问题：（i）**纯 S→F 迁移**只能在 S 标签/样本上完成训练和阈值校准，F outer outcomes 和 F inner utility labels 均不可用于该迁移策略；报告其在 F 上自然实现的 calls 和 decision quality，不能谎称已经公平相同调用率。（ii）**F 上的可比预算/校准实验**可以单独、明确标记使用内层 F-DEV 的标签来校准所有策略，或仅使用无标签的 F 预测分数分布进行调用比例调整，但必须把这个条件定义为已经进行 regime adaptation，而非纯 transfer。共同 F outer heldout 的 outcome 只能用于最终评价。把质量－调用预算曲线与自然实际调用率同时报告，以免等次数事后重排被误写成可部署点位规则。

**Scientific GO**：候选目标失配显著且具有实际意义地降低 full-active heldout gate choice quality（不能只出现 label/NDCG 表面符号翻转），候选感知方案在合理共享预算和同一外层用户验证中稳健减少损失；重复种子/其他划分支持方向，而不是仅一折微小差异。将实现的增量目标与最强 fixed strategy 共同展示，不仅比较 gate 间小优势。

**NO-GO**：无转移损失、候选感知校准未超合理简单 baseline、效果仅来自 target-conditioned candidate 构造或 hindsight selection。则 RQ2 保留为测量协议诊断，不可升级成政策泛化机制。

## 7. B2（重要的知识专属性检验）：究竟是不是“关系知识”的贡献？

当前 Memory 公式是固定 `0.45 Short + 0.45 Long + 0.10 train popularity`，本身非常简单；当前 RQ1 中可恢复历史的目标状态也是 hindsight 标签。审稿人可能质疑观察到的提升仅为**重复互动频率/热门度或任一通用专家分配器**，而非关系知识的特有条件效益。

使用**同一 DEV 决策事件**固定所有 Base、候选协议、预算、模型拟合大小，只对 Memory 的证据来源做**事前声明的对照**：
- Full Memory；
- Long-only、Short-only、popularity-only；历史性数据对照（如去掉用户-作者配对关系但保留合理边际频率的历史置换，仅作为 placebo，必须保持时间和训练边界）；
- 相同 12/14 决策前特征的 Direct gate / two-stage / Base-difficulty 等，只比较与相同 Memory expert 的对应决策；
- 在可恢复但 Base 窗口之外的**事后诊断子集**解释知识机制，不把这些类别喂入 gate。

**GO**：严格保持候选与训练条件后，长期关系或其与 candidate support 的交互解释了超出 popularity/纯短期重复的*可预测决策收益*，并在 full-active heldout DEV outer users 的预算/质量前沿上得到收益；必须检查是否依赖固定 0.45/0.45/0.10 无调权 Memory 低效率导致虚假的 gate 增益。

**NO-GO**：简单 popularity/Short-only 能复制或更好地解释大部分结果，且历史关系交互不增加实际选择质量。这意味着论文的“关系知识估值”专属性不充分；应收缩成**固定辅助排序器的条件价值研究**，不再突出特有知识机制创新。

## 8. B3 与真实外部价值：次级选项，不应抢走核心主线

对于 M3 Always Memory 更准更快的问题，第二阶段试点可用 **Memory-first**（默认 Memory，只有轻量 pre-choice 描述判断 Base 有更高价值时才付费调用 Base）。对照 Always Memory 的**绝对**质量和全路径 mean/p95 延迟，避免先计算完整 Base 再决定是否调用 Base。依然是既有 deferral 思想，科学新颖性需要来自知识缺口与候选条件的具体机制。

如果 B1 解决 R3、但 B3 不成功，文章依然可聚焦价值测量与决策选择条件，实事求是保留经济部署不足。若 B1 不成功而 B3 成功，论文本体可能需要重新定义问题与强证据，因此不能把旧 G5 TEST 当新主结果。

## 9. 方案组合与裁决

| 方案 | 解决 R1 | 解决 R2 | 解决 R3 | 代价/建议 |
|---|---|---|---|---|
| **A 仅论证精修** | 缩窄与前人重叠但不能创造独立结果 | 适当解释适用场景但不能证明成本 | **只能使叙述一致，无法闭合机制链** | 低成本；必须做，但不单独当科研解决 |
| **A+B1 迁移-选择实证** | 显著加强与 sampled metric + L2D 拼接的区别（成功时） | 仍缺成本动机；改进 under regime mismatch 的用法 | **直接针对 RQ2→RQ3 科学断点** | **第一优先** |
| **A+B1+B2 知识专属机制** | 明确超过通用路由、popularity/recency 的解释（成功时） | 仍需坦诚 Memory path 性能 | **对 RQ1→RQ2→RQ3 联合论点最有帮助** | **推荐目标配置** |
| **A+B1+B2+B3 Memory-first** | 可能拓展研究问题；大幅改变定位需慎重 | 可直接检验实际优势与全路径成本 | 不是直接替代 B1/B2 | 仅有明确 DEV 价值时做 |
| **新独立 frozen TEST** | 提供最强确认性支撑（若 B1/B2 成功） | 依合适实际成本定义而定 | 在新 unseen 样本上确认机制 | **条件执行，不可重用旧 G5 TEST** |

**重要的反事实判断**：如果移除“候选制度”后，同一 full-active 目标下决策质量没有损失，那么候选敏感性很可能只是度量/协议诊断，不足以支撑将其与路由共同作为重大知识系统方法贡献。若去掉真实关系历史后，gate 与绝对质量仍基本相同，那么所谓“关系知识的条件价值”也可能是通用排序专家差异。只有能够在受控条件下解释这些差异的合成命题，才比三个单独现象的拼接更强。

## 10. 与 N8 冻结状态和投稿计划的衔接

1. **原主稿和 G5 不变**：不改 N8 31 页主稿、34 页 S1–S9、原 12 项 R0 接受主张；该文档仅记录新的 R3 学术审查结论。
2. **探索性限定**：所有新 B1/B2 DEV 试点是 G5 已揭示后设计的研究。必须在运行前冻结候选规则、特征、预算、统计和 STOP 规则，但即使做了“预定计划”，也不能宣称这是原 G5 confirmatory family。
3. **新 TEST 门槛**：只有当 B1/B2 的效果为非平凡、跨外层用户/种子方向稳定并且有真实未揭示 outcome、数据权利与资源时，才重写科研假设并对新独立 TEST 一次性确认。
4. **退路**：如果 B1/B2 均未显示有价值的联动机制，不应靠重复 DEV 调参人为拼凑。该论文仍有 Twitch 的真实冻结互补选择收益和候选度量的重要诊断，但更合理的是按**受限的知识选择实证评估研究**投稿，接受 KBS 创新性不确定性或评估更合适的期刊。
5. **投稿技术/法律责任未消失**：AI 写作声明、人类作者审批、数据权利、永久存档、当前 KBS 门户规则仍是 N8 硬 HOLD 项。

## 11. 建议最小执行计划与停机条件

**G0（现在）**：科学命题和负向对照决议（本文件）；明确 R3 从 OPEN 走到 GO 的所需独立实验现象，而非先给结果再定义成功。

**G1（仅核查，不训）**：M3 现有 DEV 是否有足够完整的 per-event/per-candidate logits、完整活动 roster、pre-outcome Z 和可复用用户折；检查旧 room TEST 不能当新独立验证。若 cache 不足且需要重建大量 TEST 数据，STOP。

**G2（小规模 DEV）**：S→F、F→F、candidate-aware→F，同 F 外层事件/调用预算对照；先做单 seed。若没有可观测 policy regret 或环境感知校准无明显价值，STOP 不做大规模实验。

**G3（同一 DEV 知识消融）**：Short/Long/popularity 及合理 placebo；分析选择收益是否真由历史关系与候选交互构成。若知识专属信号不可识别，缩小 claim。

**G4（仅条件）**：若 G2/G3 成功且新未揭示样本/权利具备，冻结协议进行真正新 TEST；否则不重复试验刷结果。Memory-first 单列 R2 的独立探索项，不强行纳入当前投稿主实验。

**GO to stronger KBS thesis:** 至少有受控的同制度 decision-performance bridge，以及不被 trivial evidence placebo 复制的关系知识增量；没有前述证据时只能给出相对克制的经验发现。

**决策：R3 = P0 OPEN，建议以 G1/G2 先行投入，G3 条件衔接。论文目前并非无价值，而是有实证基础、尚未完全证明组合贡献必要性与重要性。**

## B1 experimental closure — post-G5 exploratory DEV (2026-10-13)

The recommendation to run B0→B1 has now been implemented. **B0 PASS**, **B1-1 exact corrected scoring parity PASS**, **B1-2 all 50,049 corrected DEV paired labels PASS**, and **B1-3 nested user-disjoint transfer and adaptation PASS**. This paragraph supersedes only the *execution status*, not the initial preregistered-science limits or G5 TEST freeze.

- [B1 full result and scientific-scope report](../../experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md).
- Core result on identical held-out full-active F DEV author events: **F→F − S→F NDCG@10 = +0.006159** (SASRec; 95% paired user-cluster CI [+0.004835,+0.007543]) and **+0.004970** (GRU4Rec; CI [+0.003550,+0.006369]). The effect has the same sign in all five outer user folds for both Base families. Outer observed Memory-call rates differ modestly (SASRec 29.95% vs 30.00%; GRU4Rec 29.97% vs 29.50%), **not exact same-call quotas**.
- Regime-adapted→F also exceeds S→F by +0.005349 SASRec and +0.004877 GRU4Rec. It **does not exceed F→F** and explicitly uses available F outer-training DEV labels; this demonstrates conditional in-domain supervision alignment, not a superior novel algorithm or pure target-domain-free transfer.
- All results are **newly designed post-G5 DEV exploration** based on **target-retained sampled offline ranking labels**. They do not establish a real online candidate generator, a pure candidate-count effect, or independent confirmatory data replication. Unconditional Always Memory continues to have higher M3 DEV NDCG; R2 economic deployment problem remains.
- **R3 status is now PARTIALLY MITIGATED**: the formerly missing RQ2→RQ3 decision-quality link has been examined and supported on a single shared M3 DEV cohort. The remaining major test is **B2 knowledge-origin specificity** (Short/Long/popularity/relationship placebo) and, conditional on its outcome, a truly new unseen independent TEST. R1 novelty remains an editorial substantive question; R2 actual cost remains open.

**No main article, supplemental paper package, G5 original TEST or R0 registered claim was altered by B1.**
