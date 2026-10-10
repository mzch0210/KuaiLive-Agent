# 第一阶段｜冻结科学主张、原始证据与源码基线

**状态：阶段一事实冻结基线，供后续文字修订作不可变对照。** 这不是新实验、新的 TEST 评价或代码分支锁定；是以 GitHub 可追溯 commit/blob SHA 固定**本轮修订前**的参考版本。后续源码修改应引用旧版与新版本 SHA。以下数值均在本轮读取的 canonical manuscript 中做过字面存在性校验，S1–S9 验证的是必要的精确 provenance；不能把“出现该数值”当成重新运行了模型。

## 源文件定位

| 对象 | 首次冻结标识 | 功能 |
|---|---|---|
| GitHub main 提交 | [f7cd9e7f48827eaded4109684bda70ee0e84d9ee](https://github.com/mzch0210/KuaiLive-Agent/commit/f7cd9e7f48827eaded4109684bda70ee0e84d9ee) | 第一阶段之前的当前正式主分支 |
| \`manuscript/kbs_latex/main.tex\` | **blob SHA \`5222d53e071987d651e3d5cb2f1a7a51c8323954\`** | §§1–7 的文字/数学/图表原稿；没有 Abstract 和 §8 |
| \`KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md\` | **blob SHA \`89734dbec9f852fcb728b2ef3a767d19ebe22109\`** | 中心命题、两条证据线路、C1–C3、§6.1→6.2→6.3 顺序 |
| \`SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md\` | **blob SHA \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`** | 数据、统计、DEV-only、模型/候选敏感性、CPU 时延来源 |
| §7 源匹配 PDF | [GitHub Actions #38037009736](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38037009736), commit \`4c603065\` | 先前成功 30 页 PDF 编译；技术确认不等于当前投稿叙事验收 |
| Twitch 原始冻结策略 | [GitHub Actions #35708072303](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/35708072303) | 主要 Twitch 单次 TEST 实验数据 |
| KuaiLive P0/P1/P2 来源 | [§6.3](main.tex) 与 [S5/S8](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md) | 原始固定模型、3 个训练 seeds、额外候选抽样 |

## 一、中心命题与创新范围

**大纲原话：** “The central problem is whether a fixed specialist instantiated from historical relationship evidence improves ranking relative to the trained base on a given event and candidate regime.”

- **C1 确认的知识对象：** \(\Delta_M(x)=u_K(M,x)-u_K(B,x)\)，仅关于指定训练后 Base \(B\)、固定 Memory \(M\) 和候选集；目标相关状态是 **retrospective diagnostic**，不是 gate 输入。
- **C2 确认的条件结构：** 相同 KuaiLive 用户目标事件/固定 raw scores 下，sampled-active 与 full-active 排序条件对应不同效用差，member/reference 的代数分配**描述性**，不能认定 candidate count 独立因果效应。
- **C3 确认的选择机制：** 仅 Twitch DEV 上训练及冻结门控阈值，TEST 上一次评估；Utility 的**14 个历史/Base 分数可观测特征**不能包含被评价目标；Difficulty 的 TEST top-\(m\) 仅是**事后匹配已经实际发生的 Utility 使用次数**的对照。

## 二、必须保护的实验数量、符号及统计结论

| 冻结主张 | 正式结果/常数 | 主文/补充证据 | 修订中必须遵守的解释 |
|---|---|---|---|
| Twitch 一次性 TEST 样本 | **44,221** 排序事件 | §5、§6.1、§6.2；S2/S7 | 与 DEV 样本分离 |
| Twitch 全量 Base / Always-Memory | **0.58211 / 0.53980** NDCG@10 | §6.1/6.2 | Memory 整体平均落后 **−0.04232**，不可抹去 |
| Twitch recoverable 目标 | **5,539**；Memory−Base **+0.22045** | §6.1，主文状态表 | 事后目标依赖分组，不能服务时直接观测 |
| Twitch Utility / Difficulty | **0.58983 / 0.58340** NDCG@10 | §6.2，冻结比较表 | Utility 相对 Base **+0.00772**；相对 Difficulty **+0.00644** |
| Twitch 成对 95% CI | Utility−Base **[+0.00641,+0.00903]**；Utility−Difficulty **[+0.00528,+0.00762]** | §6.2，原始冻结结果/S2 | 不追加新的事后多重比较声明 |
| 调用与可观测特征 | TEST **6,650/44,221=15.04%**；DEV 原阈值 **6,563/46,878**；14 features（history 6, Base 8） | §§4–6；S2/S7 | TEST 实际调用次数不等于 DEV 保证的固定预算 |
| 选择组描述性均值 | selected Memory−Base **+0.05136** / unselected **−0.05890** | §6.2 | 同一次 TEST 的策略选择结果，不是新独立样本 |
| Utility 预测与 Oracle | TEST Spearman **0.173**；同调用次数 Oracle **0.64806**；回收其 Base 上方潜在增益约 **11.7%** | §6.2、S2/S7 | 不推断逐事件校准准确或理论最优 gate |
| KuaiLive 配对事件 | **10,222** | §6.3；S5/S8 | 是事后已经检查的 TEST 事件，而不是新的冻结门控测试 |
| KuaiLive 原模型对 native 值 | sampled **−0.04120**；full **+0.04631**，paired shift **+0.08751** | §6.3；S5/S8 | 相同事件与固定模型对下的候选评价对照 |
| 2×2 描述性分配 | ranked candidate membership **+0.08827**；normalization reference **−0.00076** | §6.3，主文四格表；S8 | membership 混合 count/composition/ranking competition；无独立 causal effect |
| 初始化敏感性 | **3 个训练 checkpoint pairs**，3/3 direction reversal | §6.3；S8 | 同一批 10,222 用户，不是 3 个独立数据集 |
| 列表采样敏感性 | **9 个候选 draws = 3 sizes×3 draw seeds**，**仅围绕原始固定 checkpoint pair** | §6.3；S5 | 不得写成 3 checkpoint×9 draw 的 27 组训练重复 |
| Twitch 长短历史与容量 | \(L=8,16,32\) Bases **分别训练** | §6.4；S6 | Base weight变化与历史可见长度共同变化 |
| DEV-only 特征消融 | 14-feature OOF gain **+0.00838** @ 同 DEV 6,563 调用 | §6.4；S7 | 不可当成未触碰的独立 TEST |
| Twitch 调用频率 | **15.04%** | §6.2/6.5 | 不是 measured serving-time speed-up |
| KuaiLive warmed CPU | Base **0.991ms**，selective HGB **2.007ms**，增加 **+1.016ms**，约 **2.03×** | §6.5；S9 | 单独的 CPU replay、不同 gate、预备输入和缓存历史，非 Twitch 实际部署 |
| 离线指标定义 | one-positive **NDCG@10**，候选为各任务 eligible universe | §3、§5 | 不等价于线上 watch time、engagement 或 GMV |

**数值与材料一致性静态验证：** 本次检查确认上述核心数值的字符串版本在 canonical \`main.tex\` 中全部存在。S8 Table S8.1 提供 original seed **−0.04120411 / +0.04630669 / +0.08751080**，与主文四舍五入值吻合；S9 提供 KuaiLive Base **0.990585ms**、HGB **2.006624ms**、差 **1.016039ms** 与 ratio **2.025696**，与主文近似值吻合。此处未执行新训练/推断，不增加显著性结论。

## 三、限定性句子：保护范围清单

下列界限是研究真实性的组成部分，不能因为追求积极语气而删除：
- target-relative \`represented/recoverable/unavailable\` 需要目标 \`y\`，不是在线可观察特征；
- 比较必须指定 \(B,M,\mathcal C\)；不同平台绝对 NDCG 不构成同协议数值竞争；
- Twitch \`DEV-frozen\` 与 KuaiLive \`post-hoc already-inspected TEST\` 的实验性质不能混写；
- Difficulty 同调用数比较并不同时证明两个策略都具有 frozen serving budget；
- candidate-membership 分解属于协议内代数 allocation，ranked alternatives 改变时也改变 number/identity/hardness；
- 计算测量报告的是 KuaiLive warmed scoring overhead，且 gate 预测与实际分支是 archived mask replay；
- 表达主张不延伸至已证实跨平台门控转移、独立 candidate-count 因果效果或线上商业收益。

### 可删减的“防御式”表述是什么？

**只处理重复和位置错误，不删研究实质。** \`run/checkpoint/seed\` 时间线及历史选择原因应回到 §5/§6/S1–S9；\`not a causal candidate count effect\` 等必要边界集中写一次、必要时在 Discussion 简要提醒，不要在引言、结果、讨论三次逐字反复。处理完成后逐条复核上面的不可删清单。

## 四、源稿保护与第二阶段变更验证

1. 基准原稿 **main.tex blob SHA 5222d53e...**，大纲 **89734dbe...**，集成补充 **067d4e57...**，BibTeX 可通过 GitHub 版本回查。
2. 第二阶段每次更新只在计划指定章节范围内发生，以整文件 \`main.tex\` 原始与新版本的 \`git diff\` 或文本比较验证，不能改动冻结表中的事实、数值、数学含义和评价协议。
3. 第 1、6、7 章优先按既定论证顺序修订；每次合并保存来源 commit，编译通过后再执行下一段。
4. **停止条件：** 出现任何未事先批准的数值漂移、TEST 调参、跨平台门控实证主张、引用来源无正式发表记录、target leakage 叙述不明确，即暂停文字合并并核对源证据。
5. 第一阶段冻结只提供审计依据；**没有实际 GitHub branch protection、没有产生新的实验结果**。
