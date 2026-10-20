# N12-NI / NI-0 — 全项目创新性竞争假设与证据缺口登记

**2026-10-20 | NI-0 COMPLETED / REVIEW-OF-EXISTING-EVIDENCE / NI-1 OPEN / NO NEW SCIENTIFIC CLAIM AUTHORIZED。**

这是新的创新性研究决策支线，**不重置**已经完成的 Rev2.2-R1 E0–E5，不改变 E6 未签署的状态。执行前现行 GitHub N12 分支 HEAD `f6296fadc20c75d2df89be19afd941ef358f3286`；上次真实双 PDF 对应科学源 `36d9c3f2daed116061f12722db56448f371de60e`、C8V #39364334948、C7 #39364334815，主文38页/补充47页。本次仅提交科研治理说明，不代表另一轮 CI、论文改稿或新实验。

## 1. 唯一总体目标与科研决策

**问题**：对一个已固定的 Base `B`、历史 Short–Long–Popularity Memory `M`，事件满候选 `F` 下的配对条件知识价值
`eta_F(z)=E[u10(M;F)-u10(B;F)|Z=z]` 能否在只拥有事后 target-retained、574 无放回负样本 `S` 的训练信息下得到足以支持**固定资源下合理专家调用**的估计？其效果是否在与有统计依据的 corrected-S 控制公平比较时仍具有实质额外价值？

**最高优先科学竞争者**：不是初始未经校正 S（已比较），而是目标、信息与决策资源都清楚的 **sampled-only corrected-S**。若该竞争者接近 F，就不能再宣传全量监督有不可替代的特殊优势。若 corrected-S 的信息受限到本来无法非参数识别，则须说明所用额外假设、标注/评分代价和能/不能恢复的政策效用，而不能仅用“更真实的 F 效果好”替代科学解释。

**暂时最强、已经有资格写进现稿的结论（不修改）**：同一 DEV 上 F/S 监督导致约21%–23%请求具体调用发生更换，两个另封存但同一采集期的30k F/S *complete* policies 呈现加权 full-F NDCG F 超过原未经校正 S +.005391 / +.003585，分别自然少401/539次调用。不是 strict same-call causal label effect，且未比较有效 corrected-S。论文既有 RQ1/RQ3 和成本反例不因新支线自动变为强因果机制。

## 2. 对完整项目的去重检索

| 已完成资产（以原报告为准） | 人群、证据层级和结果 | 本次处理 |
| --- | --- | --- |
| 早期 Selective v1/v2 | 旧 KuaiLive sampled-room 10,222 用户，v2 +.013134；五候选样本种子及另 3,878 用户时间切分另有结果，**不是**M3 F/S 作者排序的同一实验 | 既存 RQ1 背景，不重测 |
| Twitch P1.3 | 44,221 held-out streamer requests，Memory整体不如Base；5,539 target-defined recoverable subgroup Memory−Base +.22045 | 保留事后分组和有限context限定；不当 online gate 的现成标签 |
| 旧 KuaiLive room S/F | 10,222 配对同事件，Memory−Base S −.04120、F +.04631；已研究score-normalization和候选组成 | 既有非因果 candidate sensitivity，不重新称首次采样失真 |
| M3 Plan C G5 | 47,575 TEST author events；两Base×三seed共用TEST；冻结 Utility 领先多个指定基线，但 Always Memory 更准 | 不重开或重新命名为六个独立验证 |
| B1/G2 | 50,049 DEV/12,628 users；原 S、F、F-label-assisted Adapted 已跑；10672/11517 decision flips，两个换位群体效用不同 | **已做**分解，不重做；探查只允许明确的新识别问题 |
| B2/G1 与 Route B 零支持 | Five source controls；Full−Long 交互+.115382，92.83%事件至少一个regime gap=0、严格双非零反转66 | 不把零值结构解释为新的独特关系因果 |
| A1/A2、成本 | 8 caps 和 Direct/Two-stage 等DEV目标比较已跑；30%最优只是部分假设lambda范围，old selector 1.769ms > Always Memory .692ms | 只作为配套资源合同；不得再次“新增8预算实验” |
| B4-A H1/H2 | 同期额外30k H1完整政策，嵌套4096历史Null +.031145，原TRAIN-popularity prereveal subgate未验证 | 都是已揭盲评价；不用于为新 corrected-S 选方法 |
| N10–N12、Rev2.2 | 科学合同、图表、最小修改、语义/双PDF技术QA已完成；E6 真实学者意见/作者GO仍缺 | **保持全部记录** |
| V2a | 超几何设计、单标量非普适逐事件无偏识别、共享S负样本joint synthetic、50,049DEV joint指标诊断；V2b明确NOT_RUN | 直接复用，不冒充 NI-1 新定理或新实验 |

**原始项目文件**：`SELECTIVE_AGENT_V2_RESULTS.md`、`SELECTIVE_AGENT_V2_ROBUSTNESS_RESULTS.md`、`KBS_EVIDENCE_STATE_CLOSURE_2026-09-23_RUN35829433706.md`、`experiments/kbs_plan_c/G5_ONE_SHOT_TEST_RESULTS_AND_ACCEPTANCE_2026-10-12.md`、`experiments/kbs_plan_c/B1_FULL_DEV_REGIME_TRANSFER_RESULTS_AND_R3_IMPACT_2026-10-13.md`、`experiments/kbs_plan_c/B2_COMPLETE_DEV_KNOWLEDGE_SOURCE_SELECTOR_ANALYSIS_2026-10-13.md`、`manuscript/kbs_latex/N9_G2_E1_SUPERVISION_DECISION_DECOMPOSITION_2026-10-13.md`、`N9_A1_UNCONSTRAINED_POLICY_FRONTIER_2026-10-13.md`、`N9_A2_DECISION_TARGET_CONTROLS_2026-10-13.md`、`N9_B1_ZERO_STRUCTURE_AND_DECISION_FAIRNESS_AUDIT_2026-10-14.md`、`N9_ROUTE_B_B4A_A4_A5_FROZEN_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-14.md`、`N12_C8V_REV2_V2A_FINAL_METHOD_GATE_AND_V2B_STOP_2026-10-19.md`、`N12_C8V_REV2_2_E2.../E3.../E5...`等。路径未写前缀的N9/N12报告均位于`manuscript/kbs_latex/`。此次未读所有私有event数据，不声称私人测试重复计算。

## 3. 注册互相竞争的科学解释——优先能推翻项目中心论点的假设

| ID | 解释/预测 | 现证据（不能当新验证） | 关键可反驳设计 | 风险优先 |
| --- | --- | --- | --- | --- |
| **R1 Known sampling + deferral** | 原S失真本是采样评价偏差，标准决策导向专家选择理应受影响，无独立理论 | KDD2020、AAAI2021、CIKM2024、ICML2024与已做G2/H1 | 对照确实有效的 corrected-S/decision-aware prior，判断剩余差异是否非平凡 | **最高 / 原创性** |
| **R2 Weak-S baseline** | F之所以更强，只因原 S 575个未校正正例保留样本极弱 | V2a 两修正启发式已测，**不构成**真实经训练的政策对照 | 有可追溯信息合同/数学性质的 sampled-only corrected paired-value监督 | **最高 / 实验竞争者** |
| **R3 Call-budget confounding** | 原S/F分别拟合并校准阈值，quality差不完全来自label本身 | H1原F/S实际calls自然不同1.337/1.797pp；G2差小但同DEV | 设计清楚在线与batch不同的 fixed-resource estimand、DEV calibrated thresholds、独立新评价 | 高 / 识别 |
| **R4 Top-10 support discontinuity** | 候选改变主要跨越top10零值阈值，非特殊历史关系效应 | Full−Long 92.83%零支持、S/F sign transitions大多涉及零 | 正式区分label-boundary变化、排序信息损失与身份语义，独立验证而非重复九单元格 | 高 / 机制 |
| **R5 Conditional information is not identifiable** | 单次采样截断标量不足以确定`eta_F`而须假设、额外标签或多次采样 | 已有V2a单事件无偏不可能性条件; N DEV min14022 | 证明/界定条件分布下的识别集合、估计目标和哪些额外信息能缩小该集合 | 高 / 可能新研究路线 |
| **R6 Quota not real** | Always Memory更准；旧pointwise gate更慢，selector在当前服务场景无成本优势 | G5/H1 Always Memory和旧256DEV计时；vectorized F未计时 | 先取得合法实测成本/访问约束，再评估决策价值；否则仅讨论假设quota | 高 / 实用价值 |
| **R7 History-null composite** | 三个null同时改重复对、高阶关系等，缺乏单一关系语义识别 | H2 4096、三seed同cohort；pre-unseal Popularity项没通过验证 | 新 precommitted 正交机制对照；当前不冒充已完成 | 中高 / 机制 |
| **R8 Population/protocol generality** | Twitch、room、M3 author和同期间H1不能合并为独立未来时期复现 | task、ranking unit、cohort不同，原TEST被揭盲 | 新许可的未来时段/新模型与候选制度完整协议 | 中高 / 外推 |

**失败/中性结果登记规则**：如果 corrected-S 与 F 打平 → **削弱**“F监督不可替代”；如果新数据F无优势→降低原现象推广；如果所有合理校正器都需借用F labels→只得到“现有S单次标量下的不可识别/额外信息依赖”，不证明每类corrected-S永远失败；如果新条件下strict-q优势为零→只保留旧complete-policy结论。

## 4. 近邻文献真实定位（出版页核对，不借用项目自我表述为验证）

1. Krichene & Rendle, KDD 2020, *On Sampled Metrics for Item Recommendation*, DOI 10.1145/3394486.3403226, https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ ：采样评价和修正是已知。
2. Li, Jin, Gao & Liu, KDD 2020, *On Sampling Top-K Recommendation Evaluation*, https://www.kdd.org/kdd2020/accepted-papers/view/on-sampling-top-k-recommendation-evaluation.html ：已有sample/global hit-rate关系。
3. Jin, Li, Mudrak, Gao & Liu, AAAI 2021, *On Estimating Recommendation Evaluation Metrics under Sampling*, DOI 10.1609/aaai.v35i5.16537, https://ojs.aaai.org/index.php/AAAI/article/view/16537 ：总体rank distribution估计/加权MLE、最大熵，不能把单标量的信息界限泛化为不可能估计总体指标。
4. Ihemelandu & Ekstrand, WI-IAT 2023, *Candidate Set Sampling for Evaluating Top-N Recommendation*, DOI 10.1109/WI-IAT59888.2023.00018, https://mdw.ekstrandom.net/pubs/wi-sampled-eval ：候选抽样与popularity bias相互作用，挑战“N12首次考虑候选环境”的任何措辞。
5. Subbiah, Rendle & Aggarwal, CIKM 2024, *Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling*, DOI 10.1145/3627673.3679943, https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ ：已有训练时的rank corrections。
6. Mao, Mohri & Zhong, ICML 2024, *Regression with Multi-Expert Deferral*, https://proceedings.mlr.press/v235/mao24d.html ：已有两阶段/多专家cost-sensitive deferral。
7. Mandi et al., JAIR 2024, *Decision-Focused Learning: Foundations, State of the Art, Benchmark and Future Opportunities*, DOI 10.1613/JAIR.1.15320, https://mlanthology.org/jair/2024/mandi2024jair-decisionfocused/ ：预测与决策目标对齐成熟。
8. Zhong et al., KBS 2026, *Scene-aware memory discrimination: Deciding which personal knowledge stays*, DOI 10.1016/j.knosys.2026.115496, https://www.sciencedirect.com/science/article/pii/S0950705126002388 ：场景条件知识留存已知；N12不同在固定source的use decision，但不同≠创新充分。
9. 官方KBS scope https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051 ：original、innovative且要求知识与智能决策实际价值；scope fit并非科学新颖性认证。

**待进一步全文级比对**：AAAI 2021的rank-mixture假设是否能直接产生本任务条件`eta_F(Z)`统计对照；CIKM2024的rank correction应用于相同单次sample top10标签是否有形式化合同；2026知识调用决策的新预印本。未阅读全文证明相反之前，不得写“从未有研究”。

## 5. NI-1 准入与项目停止规则

**NI-0 完成判定：PASS_WITH_HIGH_NOVELTY_RISK_OPEN**。已将R1/R2/R3列为最关键的可证伪组合；不因已有20余次Actions成功或报告充分就降低风险。

NI-1从原V2a的信息与估计对象审计**之后**继续：
- 明确 `Y_S` 具体11态删失观察、`N`、`Z`、两rankers**共享574负样本**的采样合同，区分单事件与条件总体估计，列明可证明和不可识别部分。
- 给出至少一个**具体且有来源/假设的统计候选**或者诚实表明未找到；不得以两个已拒绝的原方法重复探索当作NI成功。
- 对新候选先做文献/先验/信息权限可用性可证伪验收，再决定是否能提交**独立NI-2设计**；若没有，就 STOP corrected-S policy，不准V2b偷跑。
- 不读取原G5 TEST或B4-A 30k标签调参、不改动历史Null或虚称真实人工独立评审。

**计划阶段顺序：NI-0（本文件DONE）→ NI-1（仅研究方法准入，不默认模型训练）→ NI-2（资源协议与数据可行性）→ NI-3（有新独立合法数据才可预注册）→ NI-4（仅在新科学证据出现后修改论文）→ NI-5（E6责任作者GO/NO-GO）。**
