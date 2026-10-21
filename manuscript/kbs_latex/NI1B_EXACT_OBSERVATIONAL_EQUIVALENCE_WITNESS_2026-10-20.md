# N12-NI / NI-1b — 单次采样联合标签的严格观测等价反例

**2026-10-20 | EXACT_RATIONAL_SYNTHETIC_WITNESS_PASS_LOCALLY / CI_VERIFICATION_PENDING / NO_PRIVATE_DATA / METHOD_CANDIDATE_NOT_VALIDATED。**

## 0. 研究问题、位置与禁用事项

本文件为 NI0、NI1-a 后续的**独立数学合成构造**，不把此前V2a的“无法逐事件普适设计无偏”误报成新结果。问题更窄且更直接：对于**固定候选数N与常值前结果特征Z**，仅看到原B1保留目标/574共享负例的两个rankers的单正例 **sampled NDCG@10 联合观测**，是否能够唯一确定 `eta_F(Z)=E[Δ_F|Z]`？答案是：在**完全不限制latent full-rank distribution**的模型类中，不能。这里提供精确的概率分布等价证据；它**不**证明真实M3的条件效用不识别、所有corrected-S不可能或得到了新定理。

科学与来源基线：B1从N候选中保留事后观测target，按uniform without replacement从余下N−1抽n=574个负例；Base/Memory使用同一负例组。原V2a存有完整的rank hypergeometric推导、共享抽样synthetic、原始128事件复算、50,049 DEV的JΔ诊断。不可访问原G5/H1已揭盲 TEST重新选方法；本轮完全不访问任何私人数据或模型。

## 1. 构造与可验证定理

令`R_M`为真实目标在完整F中对Memory的rank，`R_B=N`对Base固定最差。两个模型在同一保留目标样本S内评分；因此对Base所有样本都有`X_B=n`，采样NDCG=0，且`u_F(B)=0`。Memory的`X_M`为574样本中位于真实目标之前的负例数，其条件分布

`P(X_M=x|R_M=r,N)=C(r-1,x)C(N-r,n-x)/C(N-1,n)`.

观察`Y_M=u10(1+X_M)`只有**11个类别**：`X_M=0..9`对应10个正NDCG值，以及`X_M>=10`对应单一0。观测联合标签`(Y_M,Y_B)`因`Y_B=0`，也仅有这11类。

对以下 **12个备选完整rank** `R∈{1,3,10,11,22,40,80,100,150,200,300,1200}`，在固定N下构成11×12的精确分子列矩阵（分母共同为`C(N−1,574)`）；使用有理数Gauss-Jordan 消元求非零核向量`v`使`Av=0`。因为每列概率归一，自动`sum(v)=0`；把正负部分分别归一化，就得到两个真正的潜在rank概率分布`P_A(R|Z)`与`P_B(R|Z)`。它们的**所有11个 sampled top10 联合标签类别概率都严格相同**，但完整效用`E[u10(R)]`不同。脚本里校验 `sum_j (p_A-p_B)_j A_{ij}=0` 用Python `fractions.Fraction` 有理数恒等式，不是浮点近似、有限样本p-value或多次随机模拟。

下表是两个**人工挑选的N值**（它们处于历史已证实DEV候选规模的最低/最高端，而不声称存在对应的实际私人事件）：

| N | 世界 A的full Memory效用 | 世界 B的full Memory效用 | 完整期望绝对差 | sampled联合标签分布差 |
| ---: | ---: | ---: | ---: | --- |
| **14,022** | 0.070933365 | 0.315655401 | **0.244722036** | **严格等于0** |
| **53,762** | 0.088305676 | 0.337997096 | **0.249691420** | **严格等于0** |

注：文件中的world A/B标签是`solve_kernel_vector`的正/负核拆分；以上A是低效用世界，B是高效用世界。精确反例不依赖NDCG近似，最终full NDCG数值仅在展示时按浮点输出。

**为什么也是共享-negative joint反例？** Base rank恒为N意味着每次shared S里Base的sampled label恒为0，所以Memory sampled标签边际一致立刻推出`(Y_M,Y_B)`联合分布一致。Base=last是反例的一项**刻意特殊假设**，而不是对原M3 Base表现的经验描述。它足以驳倒对所有合法潜变量分布、只用这种观察都能普适唯一识别的命题，却不能推断现实更宽约束下的具体损失。

## 2. 它如何影响 *固定调用预算* 决策？（人工双strata扩展）

构造两种可观测前结果类型`Z=z_1,z_2`，各占一半，且对两类都使用完全相同N与上述观测联合S标签分布。在**世界 W1**，z1对应高Full Memory效用潜在分布，z2对应低分布；在**世界 W2**调换二者。B在两类始终rank=N，故ΔF等于Memory full效用。两世界在`(Z,N,Y_B^S,Y_M^S)`上的**联合观察分布严格相同**，但最优50%固定调用预算的专家分配组别相反。

若要求一种只根据这种训练观察、以同一规则选择`z_1/z_2`的策略，在两个世界的最好选择不能同时一致：取任意固定策略给z1调用概率a、z2调用概率1−a，W1/W2分别有`(1−a)gap/2`与`a gap/2`的满总体损失；二者极大值至少`gap/4`。如果强制确定性选择某一组，最坏损失为`gap/2`。此处的数学minimax lower-bound对这个**人工两个世界和50%组级资源合同**成立，不是现实M3的性能下界，也非一般learn-to-defer新定理。

按上面两个N的示例，minimax gap/4约为 **0.061180509** 和 **0.062422855** full NDCG 单位。注意这是**刻意设定的人工世界、Base恒差和无结构latent先验**；数值仅展示极端识别限制可以对决策产生影响，不应写入现稿主Results。这里的`50%固定组级选择`与N12现有pointwise阈值/30% DEV校准绝非同一个政策估计对象。

## 3. 与已有理论的真正差异和尚未证明之处

- **旧V2a**：从单次sample rank无法普适设计无偏恢复逐事件full top10 utility；其论证不自动等于总体条件期望不识别。
- **NI-1b**：在不限制latent rank分布、只拥有一次sample top10 scalar时，构造两种**相同全部观测分布，但full条件效用不同**的世界；再给出有条件50%预算下最优调用相反的两个世界。这是现有审查问题上的**更强、不同的逻辑命题**。
- **但也有限制**：rank support和概率是为制造反例而挑选的，Base rank=N是特殊结构，Z只有人工两个类别。加入可信的full-rank分布先验、辅助训练数据、多次独立sampling、score vectors或严格参数模型可能收缩识别集合。真实M3的所有`N,Z,B,M`条件是否满足这些限制**未检验**；本结果不是在公开资料中首创的未经其他文献发现的新数学定理。
- AAAI 2021《On Estimating Recommendation Evaluation Metrics under Sampling》已研究总体rank distribution反演/假设与估计；KDD2020 sampled metric及CIKM2024 rank correction均是重要先例。NI-1b必须经进一步全文级文献和证明审核，才能判定是否有期刊科研创新。相关第一手来源：https://ojs.aaai.org/index.php/AAAI/article/view/16537 、https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ 、https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ 。

## 4. 实际代码和本轮验证

- `analysis/kbs_plan_c/ni1b_sampled_joint_identifiability.py`：纯标准库`math.comb`+`fractions.Fraction`构建公开精确反例、输出匿名rank分布/效用；**不**使用私有event ID、数据、checkpoint或真实用户记录。
- `analysis/kbs_plan_c/test_ni1b_sampled_joint_identifiability.py`：四项公开本地单元测试：概率归一、核空间等价、full效用gap/组级minimax、无效输入guard。**本地环境4/4 PASS**。
- `.github/workflows/kbs-n12-ni1b-public-exact-identifiability.yml`：新增只监听相关数学源码变更的标准GitHub Actions runner QA。**实际线上run PASS必须另外读取GitHub Actions结果**；仅有本地通过不可以冒称线上成功。
- 代码/测试/工作流/科学文件单独提交，任何报告提交后的branch HEAD不等于真正论文科学源；main.tex、Supplement、原B1/原TEST、原V2a代码均未修改。

## 5. NI-1b 决策与NI-1c阻断门

**NI-1b SCIENTIFIC MATH WITNESS: SOURCE-VERIFIABLE SYNTHETIC PASS（当前本地测试）**。这是对“无结构sampled标签足以识别full条件知识价值”主张的反例，而非批准某个正确的 sampled-only corrected-S 估计器。

**NI-1c = HOLD / NOT AUTHORIZED**，理由：无结构不可识别示例不自动给出有意义的corrected-S训练方法、识别范围、真实人群可验证假设或可用数据合同。必须先经过(i)精确数学和相关文献的独立核查，(ii)对模型家族和先验/约束如何缩小不确定性的书面说明，(iii)在合成/公开数据中对强假设提出对抗敏感性检验，再考虑进行 *DEV-only* 方法验证。不可因出现0.24效用差就把它升为N12新主贡献，也不能跳过V2b方法权限门槛。

**未来若人工作者决定无法开展新方法研究**：保留现稿 bounded F-vs-tested S，继续E6作者本人的KBS投稿HOLD/GO裁决；没有真人外部研究者时可以内部继续论证，但不能伪造人类签署。
