# N12-NI / NI-1 — corrected-S 条件效用可识别性与方法准入裁决

**2026-10-20 | NI-1 INFORMATION CONTRACT + CANDIDATE DESIGN REVIEW COMPLETE / ESTIMATOR NOT APPROVED / POLICY TRAINING HOLD / NI-2 NOT AUTHORIZED。**

## 0. 状态与科学审阅权限

本文件接续已完成 `NI0_NOVELTY_RIVAL_HYPOTHESES_2026-10-20.md` 和 2026-10-19 的**全部** V2a 七类审查（源校验、rank theory、128 原标签复现、单专家 synthetic、Base–Memory shared-negative joint synthetic、50,049 DEV joint posterior diagnostics、V2b停止），不冒充这些工作的独立重跑。未读取私人TEST、未评分/训练任何策略、未更改main.tex或Supplement。这里的数学推导与提案仍需独立检查，不构成同行评议、方法正确性的最终认证或任何新实验成果。

## 1. 可得训练信息、反事实和绝对禁止项

单事件 `x` 的候选宇宙 `F` 中包含已观察的单个真实target（该target只可在**训练标签计算**时使用），`N=|F|`。原B1 offline `S` 是保留该target并在 `F\target` 中按均匀无放回抽取 `n=574` 个负例。Base B 与 Memory M 在**完全同一**`S` 上打分。训练时的`Z`由事件发生之前的历史、Full-F候选数量和Base评分统计组成，但绝不包含target标签；部署时不能构造target-retained S。所有策略评价仍是在真实 F 上进行。

固定B或M的全量target rank `R_A`，前置负例数 `X_A=R_A^S-1`，单事件`Y_A^S = 1/log2(X_A+2)` (若 `0<=X_A<=9`)，否则`0`。观察到`Y_A^S=0` 等于只知道`X_A>=10`（不等于知道具体X）；`Y_A^S>0`唯一解出 `X_A∈[0,9]`。单个模型条件分布：

`P(X_A=x | R_A=r,N)= C(r-1,x) C(N-r,n-x) / C(N-1,n)`。

联合 B/M 的随机性**不独立**：令`a=R_B−1,b=R_M−1,o`为两组ahead-target负例身份交集。则四种负例类别总体数为 `(o,a-o,b-o,N-1-a-b+o)`；574无放回抽样服从多元超几何，构成 `P(X_B,X_M | R_B,R_M,o,N)`。纠偏需保留共享样本相关，而不能用独立B/M采样误差假设代替原协议。名义目标 `eta_F(z)=E[u10(R_M)-u10(R_B)|Z=z]`；部署策略仅看到`Z`。

信息权限**明细**：
- **S-only 合法**：训练折内非目标`Z,N`、原target-retained S标量 (B和M)、采样律/种子、从**S信息**训练得到的参数/先验（声明拟合流程/假设）、训练折内CV、外部事前可得的普适知识。
- **F-assisted**：使用任何每事件F NDCG/rank、全量监督、全量F score vectors或由这些推导的训练prior/threshold/model selection；可以作为性能上限/对照，但**不能**叫sam-pled-only。
- **评价专用**：在DEV outer-user heldout fold上按已存在来源计算真实F outcome，供比较，不得反向影响任何该fold拟合或后验标签；已经揭盲的G5/B4-A 47,575/30,000 TEST完全不可用于选择新校正方法。
- **审计source facts**：私有DEV文件16份及模型/原B1 CSV SHA已由#39230682113验证；128定点DEV复算sample labels 0差(#39232305650)。原B1 CSV仅存两模型的S NDCG scalar，而非完整sampled score vec；已有50,049 DEV N范围14,022–53,762(#39237415095)。可运行性≠已批准新的训练。

## 2. 原V2a已充分证明的边界，不当作NI-1的新理论

**已经成立的限定命题**：当一事件仅使用一次采样rank `X` 与 `N`，且没有额外先验/共享人群假设时，`N>=585`、`n=574`、`K=10`满足 V2a 给出的多项式根数充分条件，**不存在对所有真实完整rank R均精确设计无偏的单事件 `u10(R)` 数值映射**。实际只观察sampled NDCG这一截断标量，信息不多于`X`。该证明是一个有限信息限制，不推论“跨用户条件rank分布无法估计”“所有采样校正不可能”或“F训练永远优于有效corrected S”。

**新方案不能借用的伪创新**：重做超几何式、再次运行单/联合synthetic既有样例、再次比较`rank_expansion`与`uniform_prior_posterior`的后验DEV MSE，重复B1三臂、G2调用换位、A1八档预算或宣称约53.8%三态变化全是正负号翻转，都不产生新科学发现。

已获来源：
- [Krichene & Rendle KDD 2020](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)，采样度量偏差和修正。
- [Li et al. KDD 2020](https://www.kdd.org/kdd2020/accepted-papers/view/on-sampling-top-k-recommendation-evaluation.html)，采样top-k评价。
- [Jin et al. AAAI 2021](https://ojs.aaai.org/index.php/AAAI/article/view/16537)，加权估计/最大熵推断总体rank distribution；这说明总体估计不等于事件逐点不可识别。
- [Subbiah, Rendle & Aggarwal CIKM 2024](https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/)，训练时负采样rank估计；不能未经修改直接声称适于本任务的joint conditional NDCG。
- [Mao, Mohri & Zhong ICML 2024](https://proceedings.mlr.press/v235/mao24d.html)，expert deferral本身已有先例。

## 3. 是否存在可以严肃考虑的 sampled-only 方法？仅给出**未批准的研究候选**

**候选 C1：training-fold-only、shared-negative coupled rank-distribution model。**

为训练事件建模 latent `(R_B,R_M,o)`在给定可得`(Z,N)`下的联合分布`p_θ(r_B,r_M,o|Z,N)`（可以限制到粗rank分档/monotonic parametric families以控制不可识别维度，且必须事先界定）。observed training labels `Y_S=(u10(1+X_B),u10(1+X_M))`由上述多元超几何sample emission，经过零值censoring。因此最大化仅依赖`(Z,N,Y_S)`的**observed likelihood**；折内训练后计算后验`E_θ[Δ_F | Y_S,Z,N]`作为训练标签，再拟合部署只依赖pretarget Z的gate，内折OOF阈值与30%业务假定保持原逻辑。绝对不能把计算后验时用过的target-retained S观测直接送入*部署时*选择器。

**关键科学边界**：
1. 这只是一个统计模型草案，**不是**已经验证的sample-only corrected-S，也不是已证明的唯一/无偏估计器；任何 `θ`先验参数都要由**外层训练用户**内的S标签估计，不能偷用full-F outcome。
2. 对给定`N`，观察到的`(Y_B^S,Y_M^S)`是删失的有限离散结果；潜变量`(R_B,R_M,o)`空间极大，不同latent priors可能诱导同样观察分布而`eta_F`不同。方法必须**正式证明或者至少以显式反例/敏感性展示**这个识别限制；仅用训练似然拟合良好不能证明纠偏科学有效。
3. 需对`Z`的高维条件统计与`N`的变化声明可检验结构假设。两个模型共享S负例带来coupling，不允许独立相乘两个univariate posterior就声称与设计一致。
4. `o` 的上/下界及相同candidate/tie约束必须满足原B1程序；没有完整负例特征不能随意借用未观测的score overlap。
5. 拟合出来的 posterior `E[Δ_F|Y_S,Z,N]`虽可用于训练，再经过塔式期望关系评估`eta_F(Z)`仍取决于`p_θ`是否可信。是否优于原未经校正 S **不确定**，更不允许先宣称“可恢复F”。
6. 模型可以使用公开、事前可验证的extra population information，但它与“仅依赖一次S观测”需分成不同信息条件。训练折内`F`真实rank/labels一经用于校准先验，即必须标记`F-assisted`并另列。

**替代 C2：partial identification/sensitivity bounds。** 对所有满足观察`P(Y_B^S,Y_M^S|Z,N)`和特定公开约束的latent `p(R_B,R_M,o|Z,N)`，求`eta_F(Z)`最小/最大可能范围或分配策略regret上界。若区间宽到跨过决策阈值，结论是**在该信息合同下决策不稳健**而不是声称总体值不可估。相应数值求解/总体类别参数化需另行明确，并与 AA AI2021 rank distribution prior/weighted likelihood进行最近邻原创性对比。

**可行性最重要的门槛**：在不读取原F outcome选法的条件下，提出至少**两个同样拟合sample observation却对policy decision有不同推断**的合法共同分布示例，或者证明在明确的强结构假设下可获得识别/稳定界。没有此项，就算训练出漂亮的corrected-S DEV结果，也难说科学上具独立非平凡性。

## 4. 方法考核顺序和严格停止点（防止无限探索）

**NI-1a 文献/信息审查（本文件完成）**：明确真实源、sample likelihood、target estimand、原已完成工作以及两类只属于*假说*的候选。结果：`SCOPING_PASS / NO_ESTIMATOR_VALIDATED`。

**NI-1b 独立数学辨识门（未完成）**：用符号推导或与真实cohort无关的 synthetic/公开toy，设计一对可验证latent distributions：
- 保持原同一负样本joint sampling和当前 N-range；
- 比较相同/极相近观测S联合分布下的不同full `eta_F(Z)`，同时声明限制与数值误差；
- 检查前述C1的模型假设是否对潜变量具有足够识别约束，并以负向样例测试；
- 外部文献检验这个辨识对象是否已被发表结果完全解决；任何独立新定理主张必须经严谨证明而非synthetic。
只允许**合成/符号**研究，未批准任何既有DEV/TEST上选择策略。

**NI-1c 方法候选准入门（PENDING）**：需提供明确`p_θ`类、观察似然、参数学习的train-only权限、前结果feature信息、censoring/ties、可识别性与敏感性报告、预声明的regret/utility终点，以及学术独立/责任作者方法审查。不得因缺真人临时把AI内部评价冒充人类独立审稿。无方法经此门→`STOP_RESEARCH_METHOD_NOT_IDENTIFIED`，返回Path A，不执行NI-2/3。

**NI-2 仅在准入之后**：审查online pointwise gate与per-batch topK严格call匹配的**不同资源estimands**、训练校准位置、目标抽样加权和新时期合法数据。原A1八预算、A2二阶段已做，不能直接冒充sampled-S corrected-vs-F的等资源实验。

**NI-3 仅有新独立合法评价可用才批准**：一次预注册、固定corrected-S/F/original S、共享Base/Memory、候选F、call objective，明确失败可发表；旧G5和H1已揭盲的47,575/30,000绝不再作为新方法验证/挑参来源。若只能用旧DEV，至多标探索性新训练，不可叫新冻结确认。

## 5. 不同结果如何改变 KBS 原创性

| 结果 | 允许学术结论 | 禁止 |
| --- | --- | --- |
| sampled-only在合理假设下可训练、且同资源下与F接近 | 原始未经校正S弱；科学方向可能转为**最少信息的充分性**，需真实新贡献 | 仍称F不可替代 |
| corrected-S仍低于F且新独立证据稳健 | 特定真实sampling+assumption族仍不能保留F决策价值 | 推论所有可能corrected S失败 |
| 观察S对`eta_F`在弱假设下部分识别区间宽 | 信息本身不足以保证稳健专家选择，需公开假设/更多观测 | 冒充样本级绝对不可预测或新通用定理 |
| C1模型并非可识别/敏感性极高 | 停止candidate并维持原稿bounded风险；可能成立一个负面信息发现，但要有新理论 | 为完成任务执行大量DEV winner search |
| 未找到新合法未见数据或权利不允许 | 只完成现有Path A投稿/转向决策，严守既有冻结证据 | 以已揭盲TEST新calibration构成“独立确认” |

## 6. 阶段结论

**NI-1当前判定：SCOPING_DONE / CORRECTED_S_METHODOLOGY_NOT_YET_IDENTIFIED / NI-1b NEXT / V2b NOT_RUN / NO NEW SCIENCE IN MANUSCRIPT。**

唯一可立即开展而不污染既有评估的后续工作是**公开/合成的潜变量识别反例或正向条件证明**；此项不要求再次扫描私有50,049 DEV，也不允许虚构政策因果改进。若完成后未能提出有可靠辨识假设的模型，应在NI-1c主动终止、将这一未决竞争解释继续保留于KBS论文，不在已有数据上寻找更漂亮的数字。
