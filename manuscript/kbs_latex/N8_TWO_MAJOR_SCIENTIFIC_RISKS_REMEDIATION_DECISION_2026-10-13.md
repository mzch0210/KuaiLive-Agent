# N8 两项核心学术风险的解决方案与补充实验决策

**日期**：2026-10-13；**状态**：方案评估与研究决策建议，**非新增实验结果**。本文件不修改已冻结 G5 TEST、不变更预先定义的统计家族、不授权在论文中提前声称新结果。

## 一、结论与优先级

建议 **A 论文科学定位精修立即执行 + B 两个受控 DEV 可行性检查择优执行 + C 只有条件成立才启动真正独立确认性 TEST**。不建议未经试点先重训六个 Base，也不建议把 post-G5 DEV 表述为新的独立 TEST。

N8 已通过最终主稿和补充材料的技术 QA，但 **SUBMISSION HOLD**：原创性是可能影响 KBS 编辑初筛/外审的学术风险；Always Memory M3 对选择策略在绝对质量与预热计算时间上占优，是研究问题外部实用性的实证反例。KBS 官方定位强调原创、创造性、知识系统应用中理论与实践兼顾：https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 。

### 不能回避的近邻文献

- **Narasimhan et al., NeurIPS 2022**, *Post-hoc Estimators for Learning to Defer to an Expert*: 已研究固定预测模型之上的专家分配与成本；https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html 。
- **Mao, Mohri and Zhong, ICML 2024**, *Regression with Multi-Expert Deferral*: 兼有单阶段、预训练后第二阶段、实例依赖成本和回归损失理论；https://proceedings.mlr.press/v235/mao24d.html 。
- **Yuan et al., CIKM 2026 已录用/2026-09 arXiv**, *Recommender System as Slow and Fast Thinkers* (DS-Frame): 已对快速/慢速序列推荐进行预算控制选择；https://arxiv.org/abs/2609.02671 和 https://eprints.gla.ac.uk/392708/ 。
- **Krichene and Rendle, KDD 2020**, *On Sampled Metrics for Item Recommendation*: 已建立采样评估不保留模型排序关系的基础结论；https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ 。
- **Xie et al., KBS 2026**, *Fusing multi-head gating and focused-view contrastive learning for knowledge-aware recommendation*: 已研究适应性的知识融合门控；https://www.sciencedirect.com/science/article/pii/S0950705126004132 。

因此本文**不应**自称首次引入条件专家选择、相对效用学习、知识门控、预算路由或采样指标失真；数学恒等式 E[uM-uB|Z]=E[uM|Z]-E[uB|Z] 的人口目标也非新定理。

## 二、风险 1：现有证据能够支持怎样的原创性？

**更强而真实的贡献定位**：研究对象是透明固定关系记忆相对于**已训练的特定 incumbent**、在**特定在线可得候选环境**下的事件级 *NDCG 增量价值*；解释其由目标历史可恢复性和候选成员构成共同塑造，进而测试是否能够用决策前观测信息预测这一价值并制定有条件知识使用决策。这是 **knowledge-value measurement and decision evaluation**，而非新的 generic expert-router。

现有三个互补证据：
1. **Twitch 独立冻结 TEST**：Base 0.58211, Always Memory 0.53980, Utility 0.58983（44,221 事件，15.04% Memory 调用）；Utility 在准确率上同时超过两种固定策略，给出了不要求真实成本稀缺的互补性证据，但不能据此推断真实时延收益，也不能将 Difficulty 事后 TEST 等次数比较写成独立 DEV-frozen 路由。
2. **Original KuaiLive 已经分析过的 10,222 室内 room 事件**：同一 scorer 的 ΔMemory-Base 从 575 sampled-active candidates -0.04120 到 full-active +0.04631；2×2 分解把大部分变化归于 candidates membership（涵盖数量/组成/竞争），而非纯 candidate count 的因果效果。这项结果可说明**选择器监督标签要与部署候选环境对齐**，但采样指标现象已有成熟先例。
3. **M3 已冻结 47,575 author TEST**：两个 Base 家族 × 三种子，Utility 相对于四个既有目标在同时观察到的 NDCG 与 Memory 调用率上优于它们；但六 fit 共享 TEST 用户，Uncertainty 为 secondary，三个预定义 Holm 检验只在每 fit 内调整。Always Memory 在绝对准确率和独立的 warmed DEV 计时上均优于 Utility，不得作为 routing 的部署优势。

**现有论文最有价值的进一步创新路径**：不是开发一个更复杂的 HGB，而是验证 **candidate-regime-dependent utility supervision 对实际选择决策的可迁移性有何影响**。这能将 RQ2 的描述性结果和 RQ3 的冻结决策问题连接起来，回应审稿人“这只是已知 sampled metrics 问题和 L2D 拼接”的质疑。

## 三、风险 2：成本反例如何处理？

现有 M3 反例：Always Memory NDCG 0.34679 高于 Utility 0.30177–0.30400；256-event warmed DEV replay，Always Memory 平均 0.8033ms，Utility path 1.8018ms。此时基于真实观测的两轴（NDCG ↑，time ↓），**Always Memory 支配当前 Utility path**。仅仅让 Utility 比其他受限制选择器用更少的 Memory，不能建立端到端效率价值。合规权限/API 调用价格/稀缺 GPU/带宽如果没有证据，则不能被写成实有约束。

**低风险处理（立即）**：将主问题写成*何时关系知识的条件决策有预测价值*，强调 Twitch 准确率超过 Base 与 Memory；将 M3 定位为同一选择目标在强 Memory 设定下的「外生 call rule 的有界评估与失效条件」；在 Discussion 专门说明其现实可用性依赖外部条件，而且已有测时不支持节约总计算。不要从正文删除负面结果。

**潜在更强的科学解决办法（只作 DEV 可行性试验）**：在 M3 检验 **Memory-first / selective Base fallback**。由于 Memory 在平均排序和热路径计时均优于 Base，考虑历史特征支持的轻量 pre-choice gate：通常返回 Memory，仅在预计 Base 比 Memory 更好的事件选择 Base。其监督仍可用 ΔM，但给出的是 `a_B=1[\hat{ΔM}<τ]` 的相反动作。**关键约束**：gate 不可再依赖先计算完整 Base candidate scores；使用历史、时间、已公开候选元数据等决策前廉价特征，只有选择 Base 时才计算 Base；同时以真实全路径 latency、p95 和绝对 ranking NDCG 比较 Always Memory。若 gate 必须先运行 Base，计算优势可能不成立。

有可测试但未证实的潜力：M3 原 hindsight unlimited Oracle 0.38833 高于 Always Memory 0.34679，表示部分事件选择 Base 可能提高均值；但 Oracle 使用事后目标，不保证 pre-outcome 识别，也不构成新策略结果。

## 四、受控 DEV 实验优先级与具体设计

### P1（最高科研差异化）：candidate-regime supervision transfer

**目标**：检验仅在 sampled-active 上拟合的条件价值预测是否能在 full-active 排序中保持排序决策质量；比较 **sampled-trained → full**, **full-trained → full** 和 **regime-aware / candidate-support-conditioned → full** 三种情况。所比较的 incumbent、Memory、分组、历史和 target outcome 不变，模型参数冻结。候选集合应先由决策前可观测的活跃 roster 规则生成，**不能用已知 target 去修改实际门控特征**；如果研究仅是 outcome-retained sampled candidate 诊断，必须标注为 retrospective metric sensitivity，而非 prospective gate transfer。控制随机候选抽样、不同 candidate sizes、相同 per-user OOF 折、相同 Memory 调用预算、能否通过校准修复跨 regime 的价值偏移。至少报告 *value regression calibration, policy regret, NDCG, observed calls, CI*。

**资料**：优先复用 M3 既有 DEV 50,049 事件和已训练 Base/Memory 缓存，核实 full-candidate per-event logits 是否足够做子集反事实重排；否则做小型 pilot，不提前假定无需 GPU。

**科学 PASS**：存在跨 regime 的可测 utility 估计或 selection quality 下降，且预先指定的候选上下文表示/校准能在相同 data split、calls 下稳定修正；如只观察到已知样本评价排序变化、没有下游 policy 影响，则保留 RQ2 为描述诊断，不夸大创新。

### P2（最高部署合理性）：Memory-first selective Base fallback

**目标**：对比 Always Memory、Always Base、当前 Base-first Utility、History-only 或廉价 feature 的 Memory-first gate、固定简单 score fusion（如无需泄漏与可公平评估）及 hindsight upper bound。在 DEV 按用户外层 folds 完成校准；主比较为 **Memory-first − Always Memory NDCG@10** 的簇统计区间，并报告 end-to-end mean/p95 latency、底层每路径调用、训练/存储开销。

**假设**：可预测一小部分 Base 对 Memory 的收益，找到质量提高与可接受的额外成本之间的 Pareto 区域，而不再需要人造 30% Memory cap。不能仅凭 oracle headroom 声称它可实现。

**科学 PASS**：在严格 OOF/outer-DEV 中质量稳健超过 Always Memory，且真实全路径资源统计有可解释的成本--收益权衡（不要求错误地在两个轴同时严格超越）；若无法可靠识别该子群，主动保留 Always Memory 更优反例并停止部署优势方向。

### P3（仅在 P1/P2 成功后）：新的独立确认性 holdout

必须是尚未揭示 outcome 且事先冻结假设/阈值/样本规则的真正未来/独立 cohort；**不能对既已分析的 G5 TEST 子集重新命名为新 TEST**。若无法获得新的未见数据，P1/P2 仅放入标注清楚的探索性 Supplement，不能将它们视为对现有 G5 统计家族的补充确认性 p 值。原 G5 结果不重跑、不更新。

## 五、成本、科学价值与路线决策

| 路线 | 对风险 1 的价值 | 对风险 2 的价值 | 代价/约束 | 推荐 |
|---|---|---|---|---|
| **A：只改正文定位** | 改善论证；原理已有先例仍存在 | 明确 Twitch 无需成本的准确率收益，正面保留 M3 负结果 | 最低；无需 GPU | **立即执行** |
| **B1：DEV 候选迁移/校准** | **最直接修补 RQ2→RQ3 机制链条** | 无法证明外生成本或实际快 | 需核验全候选 Base 分数可得性及固定 folds | **优先小规模试点** |
| **B2：DEV Memory-first** | 提供不同场景的决策适应性，但路由理论本身非新 | 有机会回答为什么不用 Always Memory；必须胜过它或明示代价 | Gate 禁止预先依赖完整 Base；真实 latency 需测 | **受控试点** |
| **C：独立新 TEST** | 若 B1 机制清晰且预注册，有较强确认价值 | 若 B2 质量/成本成立，有较强外部效度 | 新的未见结果、数据权利、算力 | **有明确预期且条件允许才做** |

### 推荐执行顺序与 Stop/Go

1. **A1**：在不变动实验事实的前提下，将 Twitch 的 **高于两个固定策略** 作为无外生成本条件下最强的选择价值证据；将 M3 解释为强 Memory 机制下 30% 规则的 scoped policy test。审查 Title/Abstract/Introduction/Contributions/§6/§7/Conclusion 的措辞，避免“实际更快”“通用最优”“首次提出专家路由”。
2. **B1-0**：先做无训练成本的 cache/protocol feasibility gate；明确 M3 DEV 是否支持相同事件两候选 regime 的精确 rank 重算、全 candidate score 缓存、资格规则及 label-blind 决策。未 PASS 则不承诺 full pilot。
3. **B1**：候选 regime 的跨条件效用估计/选择效益小规模 DEV pilot；先检验是否存在超过原始 RQ2 的下游现象。
4. **B2**：利用 DEV 上历史-only pre-choice gate 测试 Memory-first 与 Always Memory 的 absolute quality 和全路径时间，不以 Original G5 TEST 做重新调参。
5. 只有 B1/B2 获得稳定非平凡结果并且找到新未揭示数据及法律授权，才进入 C 新 confirmation。否则保留当前 31-page main / 34-page supplement 与受限实证型论文主张，尽快进行作者合规验收。

## 六、审稿人会如何判定本方案？

**仅执行 A 的情况下**：能有效控制夸大论断，Twitch 给出选择知识胜过两单一策略的质量证据；但 KBS 最终是否认为主要是已知方法的特定领域应用仍有重大不确定性。

**执行 B1 且成功**：形成“候选上下文改变 marginal value target → target/selector miscalibration → calibrated policy recovers performance”机制链条；这是与已知 sampled metrics 和 L2D 更具体的实证差异。但若只在已看过的 DEV cohort 验证，不应声称独立跨数据集可复现。

**执行 B2 且成功**：避免强 Memory 时人为限制 Memory 调用的自相矛盾，把有条件**调用哪一位专家**的决策问题直接改为能否超过最强单一专家及其真实成本前沿。涉及更明显的方法/中心实验改变，只有证据支持时才考虑修稿，不作预先结论。

**执行 B1/B2 均未达成科学 GO**：不要再用多轮 DEV 微调制造漂亮的结果。保留 scoped 方法评估主张并接受 KBS 对 novelty 的剩余风险；必要时考虑更重视可复现应用/实证知识系统的备选期刊，但不宣称 KBS 不可能录用。

**当前状态：** 可立即进入 A 精修与 B1-0 可行性检查，但这些是推荐，不是已运行的新增训练；所有新统计应按后见 exploratory 证据身份记录。
