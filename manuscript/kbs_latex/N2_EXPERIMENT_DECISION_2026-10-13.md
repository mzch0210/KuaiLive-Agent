# N2 — KBS 增补实验必要性、科学价值及执行可行性决策

**审查日期：2026-10-13。阶段：N2。裁决：`PASS—DECISION ONLY`，正文的 KBS 投稿准备状态仍为 `HOLD`。**
**性质：** 本文件正式决定哪些实验值得开展、哪些结论应当缩窄，以及何种条件允许新增证据升级；**并未声称新实验已经完成或运行了 TEST**。本轮没有改变 `main.tex`、参考文献、合并 S1–S9、六模型 G5 权重和门控阈值。
**科学立场：** 采用 N1 的 Plan A：研究固定关系知识专家相对指定 Base、指定候选环境的增量排序价值，以及在约定的 Memory 调用限制下预测该价值的选择决策。除非出现**独立新证据**，不将研究定位成新通用 L2D 算法、端到端计算加速系统、正式 SOTA 对照榜单或候选数量的单独因果效应。

## 0. 一页裁决 / 正式执行指令

1. **主稿编辑继续：GO。** 现有 Twitch 冻结 TEST、原始 KuaiLive 配对诊断、M3 G5 冻结 TEST + 6 个 fitted Base 已足够支撑**限定范围的经验研究**；现在不应以“先补大量实验”取代 N3–N6 以发现为核心的整稿改写。
2. **新增最近邻方法的公平小实验：CONDITIONAL GO，优先做 DEV-only。** 利用已存在的 50,049 个 M3 DEV event-level paired Base/Memory 结果和用户分组 OOF 代码，在不访问 G5 TEST 的前提下，新增一个固定专家、相同 pre-outcome feature 的 **two-stage post-hoc deferral** 候选控制：分别预测 `E[u(M)|Z]` 与 `E[u(B)|Z]`，通过差值形成路由分数，与现有直接预测 `E[u(M)-u(B)|Z]` 的 Utility 进行 nested-user-holdout DEV 对比。优先检验“相对效用定义的新颖实证价值”与“具体回归训练方式的新颖性”的区别。**无独立新 TEST 时，DEV 比较只能是探索性；不能加进原 G5 预注册显著性家族。**
3. **真实部署/服务效率：NO-GO FOR CLAIM。** 在现有 256 DEV 预热算例里 Always Memory 同时具有更高 TEST 排名精度和更低预热路径均时；没有独立调用价格、权限规则或真实成本的测量。保留“给定调用约束下的 decision-quality”，放弃“减少总时延、真实部署更有效率”。如果作者以后能够提供确切系统成本结构和真实调用约束，另行设计新实验；**不得虚构**专门计费 API 或 memory permission 成本。
4. **更强 Base 及成熟方法比较：CONDITIONAL GO，不预设重新训练。** 当前 S3 足以证明指定 Base 的合理性，不能证明 SOTA、公平调参或所有更强 ranker 的鲁棒性。审稿风险不因语言表达自动消失。若前述 DEV two-stage control 显示原 Utility 优势不足或实际 KBS originality 审稿风险仍不可接受，则推进更强 repeat-aware/long-horizon author Base 与**合法新独立后期测试**的预注册研究。否则不因追求实验数量扩展训练。
5. **直接完整复现 DS-Frame/完整 GUIDER 到现有 M3 排名：当前 NO-GO。** DS-Frame 使用自身训练的 fast/slow latent refinement 而本稿的专家是固定 Short–Long–Popularity Memory；GUIDER 是 LLM logits 的 Dirichlet 数据/模型不确定性重排。两者不是直接替换现有两个 gate 的同任务专家，任何局部特征模仿不得标为“复现 DS-Frame/GUIDER”。先科学比较设计和文献定位，而非建立不公平/昂贵的伪 head-to-head。
6. **再次构造原 KuaiLive 候选数干预：NO-GO for main paper。** 现有 same-event paired P0/P1/P2 已足够支持候选依赖的解释性证据；再在同一已检查 TEST 上做 sampling 只能是事后稳定性分析，不是独立验证。
7. **N8 规范与持久归档：MANDATORY治理任务。** 现在只确认 SHA/manifest 和代码结构；用户主机事件级数据及权重尚未获得由作者证明的长期开放授权或稳定 DOI，不能因为 GitHub workflow artifact 存在而声称可长期取得。

**整体 GO 结论：** 进入 N3，不等候计算密集型新训练。把 N2-D1 的 DEV two-stage comparator 作为一项可独立执行的**高价值、低训练成本**补充验证；其是否成为正文“新增结果”，必须由预先登记的评价身份和真实的数据可用性决定。

## 1. 现有科学证据是否已足够回答论文问题？

| 研究命题 | 已验收的最高层证据 | 是否需要追加实验才能在正文限定表述？ | KBS 余留审稿风险 |
|---|---|---|---|
| **RQ1 关系记忆相对 Base 的条件性排序价值** | Twitch 冻结 TEST：Base NDCG@10=0.58211、Memory=0.53980；事后可恢复历史目标子组 Memory−Base +0.22045；M3 full author TEST：Memory=0.346792，六 Base ≈0.258–0.261 | **不必须**，用于描述固定专家与指定 Base 的差别；可以增加一个更强 Base 以探究这种差别的稳健性 | Memory 在 M3 强于所有 Base，可能使审稿人质疑 Base 合理训练/专长；S3 是限定配置，不是同等调参 SOTA |
| **RQ2 固定专家价值标签依赖候选排序环境** | 同一 KuaiLive 10,222 房间事件，575 sampled Δ=−0.041204、full-active Δ=+0.046307；配对变化 +0.087511，2×2 成员/参照描述分配 | **不必须**，只证明该既定房间任务上的事后配对情境差异 | 已有 sampled-metrics 文献；非新的候选长度纯因果推断或独立复现 |
| **RQ3 预测该专家相对价值可以支持约束下选择** | Twitch Utility 0.58983 > Base 0.58211、Difficulty 0.58340（后者 TEST-count retrospectively matched）；M3 六拟合共享 47,575 TEST，Utility 0.301766–0.304004，胜四个指定策略且观测 calls 更少 | **限定主张不必须**，但 **high-value** 追加同固定专家 two-stage L2D 方法对照，有助于降低“只是相同 post-hoc gate”的风险 | 现有四个 M3 gate 不等价于成熟 deferral/DS-Frame，TEST calls 非严格同一 |
| **真实更优资源配置/实用调用效率** | M3 256 DEV warmed RTX3090：Always Memory 0.8033ms vs Utility 1.8018ms；Frozen TEST Always Memory 0.346792 > Utility | **必须有新独立真实成本依据才能作此主张**，现阶段禁止部署效率 claim | 人工设定 30% DEV calls 的实际意义不明确；有较强反证 |

**关键区分：** “现有证据可以支持限定研究命题”不等于“现有方法具有足够 KBS 创新性且有高接受概率”。期刊官方定位中要求原创、创新研究并兼顾实践与理论；在与 2026 年 DS-Frame 和既有 L2D 比较后，这一重大科学意义风险仍在。

## 2. 相近文献检索结论如何改变追加实验优先级？

1. **Narasimhan et al.，NeurIPS 2022，Post-Hoc Estimators for Learning to Defer to an Expert**：确立 fixed-base, post-hoc expert allocation 的先例。其研究重点不等同于本文 event top-K NDCG，但基础 decision principle 不新。最公平也最省资源的补充是**保持相同固定 ranking experts、相同可见 features 和同一 user-split，研究 two-stage prediction vs direct gain prediction**；而不是换成新的 slow system 后归因于 gating。
2. **Mozannar & Sontag，ICML 2020；Mao et al.，ICML 2025**：说明学习分配专家不是本稿独有；成熟方法对照有意义，但他们主要研究分类/专家决策 surrogate，在单正例 top-K ranker 上需调整**loss/objective、可用输出与标签定义**，不能把现成分类 accuracy 直接当作 NDCG。
3. **Yuan et al.，DS-Frame，2026-09 arXiv；2026-08 已获 CIKM 2026 接收，会议 2026-11 尚未举行**：使用快慢顺序推荐及受预算约束的 learned selector，构成“预算化慢快系统是本文方法创新”的高冲突。**完整 DS-Frame slow ranker 并非本稿固定 Memory**；相关公共代码仓 README 展示 `main.py --model_name PRL` 等，并没有经过本轮验证的可直接在本稿 full-active author+fixed memory 协议运行的成套同条件基准。N5 必须引用并客观说明区别，不得捏造 head-to-head。
4. **GUIDER，AAAI 2026**：实际使用基于 LLM logits 的 Dirichlet DU/MU，不等于 M3 所采用的简单负 Base margin Uncertainty 启发式；当前表只能声称优于**所定义的 margin proxy**，不能声称优于 GUIDER。
5. **Krichene & Rendle，KDD 2020**：已经证明 sampled-rank evaluation 改变模型比较。故没有必要为“采样会改变评价”本身再做大规模实验；正确贡献是解释固定 Memory−Base 信号在 intended ranking context 下的含义。

**已核实公开来源：**
- KBS official: https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051
- ICML L2D: https://proceedings.mlr.press/v119/mozannar20b.html
- NeurIPS 2022 Post-Hoc: https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html
- ICML 2025 multiple experts: https://proceedings.mlr.press/v267/mao25c.html
- DS-Frame primary arXiv: https://arxiv.org/abs/2609.02671 ; Glasgow 2026-08 accepted record: https://eprints.gla.ac.uk/392708/
- DS-Frame public GitHub: https://github.com/ZichenYuan233/Recommender-System-as-Slow-and-Fast-Thinkers
- GUIDER AAAI proceedings: https://ojs.aaai.org/index.php/AAAI/article/view/38639
- Sampled-metric primary author source: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/

## 3. 资源及数据真实性审计

| 现有资产 | 检查结果 | 新实验适用范围 |
|---|---|---|
| M3 预先构建的 DEV event bundle | **50,049** 冻结 DEV full-active author events；源码 `G1_FIXED_DATA_BUNDLE_ACCEPTANCE` + G4，均在私有 User-host | two-stage gate fitting、nested DEV calibration/evaluation、cost replay；不能视为未观察过的外部 TEST |
| Pairwise score/feature cache | `analysis/kbs_plan_c/g3_fit_dev_gates.py` 需要 byte-verified `dev_full_active_pairs.csv`，用户已预先处理的 `memory_ndcg10`、family-specific `*_ndcg10`、12 pre-outcome features | 理论上可复用，无需对 50,049 个事件重新计算全候选 ranker；运行前必须验证私有缓存存在且 SHA 正确 |
| Base 模型训练 | SASRec、GRU4Rec×3 已有，原 DEV checkpoint screen 4,096×575，TEST 不能再用作训练或选择 | 新 gate DEV 可仅用 CPU HGB 与已有分数；强 Base 则需要 GPU 及独立方法设计 |
| User-host G0 实测资源 | NVIDIA RTX 3090（23.56 GiB VRAM）、约 59.47 GiB 当时可用 RAM、缓存卷约 1162.48 GiB 空闲；运行记录为 2026-10-12 | 证明当时可执行可用；**不证明今天主机仍在线、私人缓存仍在、或仍有相同资源** |
| 冻结 G5 TEST | 47,575 events / 12,533 users，G5-A 先 label-blind score，G5-B 独立 reveal，一次性统计已完成 | **永久保持现有 G5 主结果和推断家族**；任何后续 new model 的 G5 重算只能明确标注 post hoc exploratory，不能说新 untouched confirmatory |
| 数据上游时间划分 | TRAIN < 2026-03-23 12:00；DEV 2026-03-23 12:00 至 2026-03-27 14:00；TEST 自 2026-03-27 14:00 起 | 当前全局 TEST 后没有**已验证为未接触、可再次作独立后期验证的新自然时间数据源**；新的 independent holdout 必须先作数据可得性/重叠/合法性检查 |

### 3.1 关于“额外一轮独立 TEST”的硬约束

因已有 G5 TEST 被阅读并用于形成 N1/N2 文稿判断，新的 model comparator 即使只在 DEV 训练、随后在同一 G5 TEST 评分，其推断身份仍是**后设、研究过程已知结果之后的新增比较**。可以报告和附补充材料，但不得并入 G5 预注册三对照/六拟合的正式家族，也不得凭借不同随机种子宣称新的独立事件样本。

要获得**新独立确认**，原则上应有真正新到的 chronologically later observed events，或另一公开且事先定义的 ranking task/source；应先核验许可、候选生成、基模型训练和用户重叠风险，然后冻结完整方法及主统计再揭示新结果。目前尚**没有确证此种新测试资源可得**。不能简单从已看到 TEST 的同一数据中选一部分包装成 independent TEST。

## 4. 成本约束：为什么不应直接再做“加速实验”

G4 的真实 256 DEV event warmed replay（原 primary SASRec、RTX3090、输入历史/候选已准备）：

| 路径 | mean ms/event | 证据解释 |
|---|---:|---|
| Always Base | 1.4245 | 指定 Base 排名路径；并非最便宜 |
| Always Memory | **0.8033** | 固定 Memory 全调用且平均更快 |
| Utility selective | **1.8018** | 计算 pre-gate descriptors 和 HGB 推断增加开销 |
| pre-gate sparse feature assembly | 0.2395 | Utility 的预决策成本之一 |
| gate inference only | 0.6207 | Utility 的预决策成本之一 |

在主 M3 TEST 上 Always Memory 0.346792 亦比任何 Utility 0.301766–0.304004 更准确；但**注意两组指标来自不同条件**：质量是 47,575 TEST，耗时是独立 256 DEV 路径，不能说已经测得一个同分布完整 TEST 的真实 Pareto frontier。

**决定：** 论文只讨论在一个**外生给定** Memory-call limitation 下可提高的选择质量；不把它写成当下环境中实际有用的降低服务器成本技术。如果目标后续改为经济/在线路由，则必须在另行设计的 workload 下实测：数据维护、候选构造、Base scoring、Gate descriptor、gate inference、Memory scoring、真实外部成本和 batch/并发，给出模型选择与延迟的同样事件条件比较。可设定不同的**假设**外部每次调用成本开展敏感性分析，但零成本/人为成本输入不是实测 proof。

## 5. 明确的 7 项实验/治理裁决

| ID | 类别 | 裁决 | 推荐等级 | 经济性/科学收益 | 是否阻断 N3？ |
|---|---|---|---|---|---|
| **N2-D1** | 固定专家 two-stage L2D DEV baseline | **GO DEV EXPLORATORY** | **最高（P0 对照风险）** | 仅复用已有 DEV OOF 特征、两种专家 event NDCG；不需要重训六 Base。直接回应“已有 L2D 已经包含增量价值” | **否**；但在 N5/N8 最终是否宣称方法优于竞争选择框架前必须回看其结果 |
| **N2-D2** | 真实 expert-call 成本和权限限制 | **NO-GO CLAIM; CONDITIONAL MEASUREMENT** | **P0 科学风险** | 如果证明确有生产成本，提升调用约束的必要性；没有外部系统就不应虚构 | **不阻断限定 Plan A**；严格阻断 deployment/speed superiority claim |
| **N2-D3** | 更强且适当调参的 M3 author Base | **CONDITIONAL GO** | P1 | 检验 memory advantage 是否只是弱 Base 导致；会占 GPU/再设计，存在主证据不可比风险 | **否**；若转向 generalizable independent utility claim 则必须评估 |
| **N2-D4** | DEV / 新独立 TEST 的 budget-matched policy | **GO protocol/design ONLY** | P1 | 有利于更严谨解释实际 TEST 调用率不同的问题；新 TEST 目前可得性未证实 | **否**；不能改写已冻结 G5 |
| **N2-D5** | 完整 DS-Frame / GUIDER 重实现 | **NO-GO IMMEDIATE** | P2/条件性 | 任务、慢专家或 logits 不同，不具备可直接公平替换的前提；成熟文献纳入 §2，必要时新研究 separately registered | **否** |
| **N2-D6** | 原 KuaiLive 同 TEST 继续候选抽样 | **NO-GO MAIN** | P2 | 既有 P0/P1/P2 已做足够诊断，边际创新性较低、独立性无新增 | **否** |
| **N2-D7** | 授权/持久开放复现资产 | **MUST COMPLETE BY N8** | P1 governance | 发表合规、科研透明性、持久归档；缺失 DOI 不能假设 | **不阻断 N3**，阻断“全部复现资产已公开”声明 |

### 5.1 为什么 N2-D1 优先于大规模方法复现？

它比较**同一个决策问题**：给定相同 fixed (B,M)、相同 candidate list 和 observable feature (Z)，预测 (u(M)-u(B)) 的直接方法，是否比**先估计两方效用再相减**更适合选择外部关系专家？与既有 L2D 原理高度接近，恰好回答最尖锐审稿问题，且可以复用已有数值排名、训练代码和 DEV 用户划分。

实验可能得到三种诚实结果：
- **A：two-stage 与直接 Utility 大致等价。** 进一步证明相对效用是有用的 *measurement target*，但没有理由宣称 direct regressor 的方法创新；论文应压缩“新门控方法”贡献，继续强调 candidate-conditioned knowledge valuation。
- **B：two-stage 优于直接 Utility。** 原文不得继续宣称直接 Utility 比成熟专家选择设计更强；可改为研究 relative-knowledge value 与 alternative estimators 的实验结论；若想增强方法主张，提出新机制并在独立新测试确认。
- **C：直接 Utility 优于 two-stage。** 只能称 DEV 探索发现，不能据此在已知 G5 TEST 做新的 confirmatory 选择；形成 N8 可核查的 supplemental exploratory result，另行独立 TEST 才能主张普遍 superior。

这三种情况均可能提升学术诚实度；并不保证发表概率提高到某个可量化程度。

## 6. N2-D1 推荐实验协议概要

完整技术草案见 [N2_TWOSTAGE_L2D_DEV_PROTOCOL_DRAFT_2026-10-13.md](N2_TWOSTAGE_L2D_DEV_PROTOCOL_DRAFT_2026-10-13.md)。

- 输入：每 fit 同一 50,049 DEV event IDs（和当前 G3/G4 byte-verified paired cache），标签 (Y_B=u_{10}(B,x),Y_M=u_{10}(M,x))，仅 12 个 pre-outcome features；不得读取 target-derived history state 或任何 TEST 标签。
- 政策 A：现有 direct relative-utility predictor (hateta_A(Z))。
- 政策 B：fixed-expert post-hoc two-stage (hateta_B(Z)=widehat{mathbb{E}}[Y_Mmid Z]-widehat{mathbb{E}}[Y_Bmid Z])。在相同训练算法/训练折、同等特征资源下拟合；不把简单两阶段对照称为复现 Narasimhan 等的完整 surrogate algorithm。
- nested **group-by-user** development-only setup：外部留出 user folds 只用于比较政策；只在外部训练 users 内拟合 OOF estimator、阈值和超参数；重复 5 folds 实现交叉输出；不得在整个 DEV 上先选阈值再对同一 DEV 报告无偏结果。
- 对两个政策同时评估 NDCG@10、Memory calls、同调用约束下的比较、user paired bootstrap 和五份模型估计量；模型组共享 DEV 用户，不能当作五个独立研究群体。依 DEV 冻结设置和是否形成独立 TEST 将证据明确标注为 exploratory。
- 允许同 user/held-out outer fold 小样本 imbalance 的方差估计，必须只从完整有效 event rows 得到；不通过删掉难例制造拟合优势。原 G5 预注册主对照不改变。
- 禁止“预先宣布胜出”“修改现有 30% DEV 定义使比较必胜”“用两个回归器的总成本与一个回归器比而不报告其 Gate 推断额外耗时”。

## 7. N3–N8 正文修订约束与完成标准

- **N3 Results:** 不等 D1，就以现有冻结证据重组；将六拟合 Utility 对指定四个 gate 的 **TEST NDCG 更高 + Memory calls 更少** 作为有条件主观察结果；同时保留 Uncertainty 次要比较、History drift、Always Memory TEST 0.346792 和 warmed DEV 的不利计时。D1 若后来有 DEV 结果，作为 exploration 单独附录，绝不重写 G5 已接受主显著性。
- **N4 Methods:** 在 §5 统一声明当前五个 policy 的固定 Base/Memory 公平性、realized TEST call drift、Twitch retrospectively count-matched control；任何 D1 必须准确说明其多一份训练/推断的成本。
- **N5 Intro/Literature:** 增加 DS-Frame 的准确 2026 预印本与已接收 status，以及 L2D two-stage deferral 的原始文献；不在尚未执行 D1 时写“优于 L2D/DS-Frame”。
- **N6 Discussion:** 将“在指定外生调用规则下增量效用信号有效”和“实际部署是否值得调用门控”严格分开，将 Always Memory 的 counterexample 作为知识系统使用决策的概念贡献，而非尾随一串自我辩护。
- **N7/N8 Audit:** 继续追溯 R0 全 12 项问题与未完版权、数据可用性、作者声明和正式 PDF，防止结构改稿消除合规科学限定。不能把本 N2 的实验设计写成“已完成 supplemental experiment”。

**N2 PASS 的含义是最优先科学行动已排序、证据升级规则与 NO-GO 主张已冻结、后续改稿有准入条件；不是对 KBS acceptability 的完整认证。**

## 8. 后续阶段交接结论

**允许立即 N3。** 使用 N1 的唯一主论点和 N0 的逐段责任映射，先实现 discovery-first §6。D1 另作为新 DEV-only pilot，必须先生成真实可运行、数据守卫完整的协议和新工作流（不得触发旧 G5），运行之后如无新测试要明确标注 exploratory。D2 必须作为稿件范围硬约束；若作者明确希望改变为“实际计算节约”主张，则在 N2-D2 得到独立真实资源依据前，应停止这一 claim 而非开始没有业务解释的 GPU benchmarking。
