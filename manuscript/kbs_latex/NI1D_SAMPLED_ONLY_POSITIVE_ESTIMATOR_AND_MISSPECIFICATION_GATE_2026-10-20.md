# N12-NI / NI-1d — 强先验下 sampled-only 正向估计器及错设负对照

**2026-10-20 | PUBLIC SYNTHETIC POSITIVE CONTROL COMPLETE / REAL-DATA ESTIMATOR STILL NOT APPROVED / NI-2 HOLD。**

## 1. 研究对象与原始证据界限

本研究接续 NI1a（联合样本信息合同）、NI1b（无结构观测等价）与 NI1c（rank10/11 单个特殊候选检测概率），**不触碰私有 DEV、TEST、模型/门控、论文 main.tex、Supplement 或 H1**。不以合成训练取代合法的新 TEST，也不重新跑 G2/A1/A2。

**强假设且公开**：每一前结果可见类别Z只含两种潜在完整排名状态 (R_M,R_B)=(10,11)（Memory较好）与(11,10)（Base较好）；二者共享9个比target更好的候选，差一个特殊负例。所有B/M抽样使用**相同**574负例。两类Z的该排名结构**事先已知**，未知的是Z组内优劣状态混合概率pi(z)。模型只用训练时可见的sam-pled-S NDCG标签、Z和N拟合pi，不用任何真实完整F训练标签。在线/新事件决策时只使用Z/N和训练得到的群组参数，不用当次已观察目标。

**这不是**对 M3 的真实结构先验，也**没有**声称该方法具论文所需独立创新性。KDD2020 sampled evaluation correction、AAAI2021 rank-distribution estimation均形成强先例。

## 2. 正向识别与估计方案（无F训练标签）

单次采样中，唯一特殊负例被抽中的概率 p(N)=574/(N−1)。被抽中时，两个 ranker 的 sampled NDCG标签出现正或负差，符号恰好给出潜在full优势的方向；未被抽中时两者sampled标签完全相同。

在给定Z/N的训练折内，如果检测到正差的次数为n+、负差次数为n−，并且两种潜在状态拥有**相同检测概率**，则条件于检测事件的符号概率为pi(z)。于是 sampled-only MLE
```
pi_hat(z) = n+/(n+ + n−)
eta_hat_F(z) = (2*pi_hat(z)−1) / log2(11)
```
若n++n−=0则该条件值**没有足够可见训练信号**，目前toy回退0仅作为无数据占位（不得叫有效方法）；实际方法需明确不确定性/先验与训练折策略。此估计器的关键结构（仅两潜在rank状态、已知rank幅度、检测与方向准确）是极强假设，而非从S信息自动学习出的现实科学规律。

原始 sampled utility 的组均值取决于 `p(N)` 与共享9个领先负例的超几何分布，因而不同N会导致不同缩放，虽然真实full值仅由pi决定。理论上独立同分布的无限训练事件、pi固定且检测概率>0时，该已知结构族下的pi_hat可一致收敛；有限样本尤其大N时有相当大的稀疏检测不确定性。此为结构模型中的直接条件MLE性质，不能命名为新定理。

## 3. 正面合成结果

公开生成两个Z组，各50,000训练事件（仅合成，12个固定随机种子重复）。
- 组A：N=14,022，pi=.65，full eta=+.0867194479；
- 组B：N=53,762，pi=.85，full eta=+.2023453784。
- 旧S期望相对效用：A +.0035777517，B +.0025929146，**旧S把高价值排序颠倒**。
- sampled-only正向估计器使用训练观测中符号差频率恢复pi；完整F价值在人工模型中组B较高。

| 固定相同50%类别调用额度 | 12次合成训练重复选择真正高价值B的次数 | 实际完整候选总体效用收益 | 理论错误选择损失 |
| --- | ---: | --- | --- |
| 未校正S组均值 | **0/12** | +.043359724（选A） | **.057812965** |
| 已知结构sampled-only MLE | **12/12** | +.101172689（选B） | 0 |
| Full-information oracle for this toy | **12/12** | +.101172689（选B） | 0 |

注意：在这项组级50% fixed-quota toy里，old S和corrected S都调用**恰好一半**人群；它**不是**当前论文的online pointwise 30% DEV threshold policy，也不是对未知目标即时采样。完整值来自发生器的已知潜在分布，仅用于合成验证，估计方法没有训练时见到F label。上表12个训练replicates共用一组合成生成机制，不是12个外部数据集/新的TEST。

**负对照一**：若两个Z组使用相同N且仍只有pi差异，原sampled-S组均值会正确排序：之前观测到的反转来自候选规模不同引起的观测概率变化，不代表原S在所有场景都失败。

**负对照二（方法错设）**：若真实rank pair变为(9,10)/(10,9)，仅一个负例区分的采样方向仍能被发现，但真实full差 `u10(9)−u10(10)=.01196517`；套用假定(10,11)的 `1/log2(11)=.28906483` 会对**单状态full增量幅度**高估约 **24.16倍**。该数值是外部解析错设压力，不是数据上真实拟合的检验误差。方向判断在此toy仍可对，但**校准不可靠**，若两组真实差幅不同，政策选择也可能翻转。

## 4. 独立文献竞争、意义与停止规则

- Krichene & Rendle KDD 2020: https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ ——sampled metric不一致与bias/MSE校正为已知；不能以“一次sample S可纠正”作为理论首创。
- Jin et al. AAAI 2021: https://ojs.aaai.org/index.php/AAAI/article/view/16537 ——利用weighted likelihood/max entropy估计全量rank distribution；本模型的rank-mixture恢复可能是这类已有原理的专门情形。
- Subbiah, Rendle, Aggarwal CIKM2024: https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ ——训练rank估计先例，但未直接验证这里的paired conditional use decision。

**阶段裁决：NI-1d TOY POSITIVE ESTIMATOR DEMONSTRATED, METHOD GATE NOT PASSED。**

本实验的正面和不利错设结果共同构成有价值的**研究可行性证据**，但不足以批准 M3 corrected-S policy、NI-2 或 NI-3。现实采样条件下潜在full ranks不只两点；真正候选还需：训练折内合理且可检验的rank分布族、shared-negative joint emission、zero censored likelihood、有限样本uncertainty、先验/结构错设对实际决策的敏感性、明确的pretarget Z协议、相同资源价值目标、有效独立数据和完整文献对比。

如果没有这样的科学上正当的模型，不应继续反复提高人工toy分数。符合现行停止规则时保持V2b NOT_RUN，现稿仍限定于F对原未经校正S且创新性风险HIGH。若具备统计模型与合法新证据，再进入NI-2设计。

## 5. 实现与验证记录

- `analysis/kbs_plan_c/ni1d_positive_sampled_only.py` — sampled-only pi组参数估计，已知toy先验与完整F生成真值仅在**模拟器/评估**，不进入训练。
- `analysis/kbs_plan_c/test_ni1d_positive_sampled_only.py` — 六项科学测试：观测概率、解析排序反转、12种随机种子正向比较、错设强度、等N阴性对照、输入guard。本地独立执行 **6/6 PASS**。
- `.github/workflows/kbs-n12-ni1d-positive-sampled-only.yml` — 公共runner执行toy代码和unittest；**实际GitHub Actions结果应以后续运行核实为准**，不得把创建workflow等同CI成功。
- 新增程序和文档不更改Rev2.2 E0–E5完成状态；未更改旧论文38页/补充47页，也没有使用任何私人TEST。
