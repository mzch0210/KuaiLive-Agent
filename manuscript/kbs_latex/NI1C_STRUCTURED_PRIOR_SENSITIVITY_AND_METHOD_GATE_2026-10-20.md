# N12-NI / NI-1c — 强结构假设下的 sampled-only 条件效用敏感性与准入裁决

**2026-10-20 | STRUCTURED_PUBLIC_SYNTHETIC_REVIEW_COMPLETE / NO_CORRECTED_S_ESTIMATOR_APPROVED / V2b_NO_TRAINING / NI-2_NOT_AUTHORIZED。**

本次新增的数学检验不是 NI-1b 完全相同观测分布的复述：在完整ranking只差**一个**候选先后关系、其余结构全部固定这一*更强结构假设*下，我们精确计算sampled-S观察的可区分性（不是断言严格不可识别）。仅用数学及公开合成脚本，不读取私人DEV/TEST，不拟合门控，不修改论文。

## 1. 精确定义、与 NI-1b 的重要差异

两个对称人工世界，在给定候选集合N中，真实目标在Memory和Base的完整F排名分别为：

- W+：Memory rank=10，Base rank=11，全F相对效用为 `+1/log2(11)=+0.2890648263`；
- W−：Memory rank=11，Base rank=10，全F相对效用为 `−1/log2(11)=−0.2890648263`。

9个比target排名靠前的候选对两rankers相同，只有**一个特殊候选**在worse model中比target靠前，其他候选均低于target。B/M用**同一个**离线target-retained uniform-without-replacement `n=574` 的负例集合，严格等同原B1的抽样耦合逻辑。

- 若特殊候选**没有**被抽中，两个模型的sampled rank完全相同，观察到`Y_B^S=Y_M^S`，对W+、W−完全不携带谁full更优的信息。
- 若特殊候选被抽中，联合`(Y_M^S,Y_B^S)`不同，且符号方向分别严格相反。精确探测概率 `p=n/(N-1)`。
- 因此两个世界的**一次抽样完整联合标签分布的总变差距离**正好`TV=p`（两个off-diagonal支持互斥，相同对角支持重叠）；不是NI-1b的`TV=0`。如果事件条件世界不变、每次都是独立新随机采样，50次全部漏掉差异的概率为 `(1-p)^{50}`；注意这样的重复采样**并非现有B1单次sample事件协议**，只是额外信息敏感性展示。

## 2. 精确概率和合成结果

| 完整候选数N | 一次样本探测差异`574/(N−1)` | 一次观测相同概率 | 50次独立抽样均未探测概率 | 满F两世界Δ差的绝对值 |
| ---: | ---: | ---: | ---: | ---: |
| 14,022 | **0.0409385921** | 0.9590614079 | 0.1236860666 | 0.5781296526 |
| 53,762 | **0.0106768847** | 0.9893231153 | 0.5846659723 | 0.5781296526 |

Full-utility表中的0.5781296526是两个世界的**signed Δ差**，不是一个模型的NDCG改善。单世界满F的正/负相对效用是±0.2890648263。上述N为原DEV中经hash校验的full-candidate count最低/最高值（源#39237415095），**不是声称这些人工rank构造真的存在于DEV样本中**。

共享9个head negative中的h个在被抽中“特殊候选”的条件下服从`Hypergeom(N-2,9,n-1)`，采样效用非零gap期望需要计算`u10(h+1)-u10(h+2)`并受其抽样概率加权。即使满F差为0.289，单次S中多数观测仍为相同标签：当N=14,022时正世界sampled delta期望约 **0.01192584**；当N=53,762时约 **0.00370416**。将这种衰减宣称为“现实模型存在相同误差”是不合法的。

## 3. 能验证/不能验证的科学结论

**能验证：**
- 若对完整排名施加极强的one-candidate-difference支持假设，两世界*不是*严格统计不可识别：其采样观测分布确实不同，`TV=n/(N-1)>0`。
- 但单事件sampled top-10标签可能对full决策符号非常不敏感，样本规模N越大且n固定，特殊候选被观测概率越低。
- 因此，NI-1b的无结构严格观测等价和本NI-1c强结构下近似不可区分是**不同且互补**的证据，不能合并成“校正不可能”的无条件通用定理。

**不能推论：**
- 不能说明目前KuaiLive实际SASRec/GRU4Rec模型确实以这种rank10/11结构分布，也不能拿人工世界fullΔ数值解释原H1 +.005391/+.003585。
- 不能否定群体/条件rank distribution估计。Jin 等 AAAI2021已提出weighted-MLE/max-entropy式总体分布估计，Krichene/Rendle KDD2020明确讨论可改善sampled-metric质量的修正。此检验不是这两类已有方法的反例。
- 不能仅凭一次sampled标签在人工事件上难以识别就推出“所有训练折S-only方法的条件`eta_F(Z)`无法学习”：共享Z的事件、大样本、结构先验、辅助协变量、合法重复采样均可能恢复决策。
- 不能证明有价值且新的 corrected-S estimator、真实30%在线逐请求quota政策或公平matched-budget效果。
- 本构造的exact detection identity是基础无放回抽样概率，而不是已经确认首次发现的可投稿新定理。

## 4. 与 prior art 的精确界线

- Krichene & Rendle, KDD2020, [On Sampled Metrics for Item Recommendation](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)：sampled指标不一致，以及bias/MSE correction先例。
- Jin, Li, Mudrak, Gao & Liu, AAAI2021, [On Estimating Recommendation Evaluation Metrics under Sampling](https://ojs.aaai.org/index.php/AAAI/article/view/16537)：rank distribution与总体指标的weighted MLE/max entropy估计；意味着可识别性不能仅凭逐事件不一致而否定。
- Subbiah, Rendle & Aggarwal, CIKM2024, [Improved Estimation of Ranks for Learning Item Recommenders with Negative Sampling](https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/)：已有更有效的采样rank estimates；目前不能照搬成joint conditional top10 corrected-S。

## 5. 可复现程序和进度

- `analysis/kbs_plan_c/ni1c_topk_one_candidate_sensitivity.py`：输出两个N的精确有理数探测概率、full Δ符号、50次理论独立抽样漏检率、联合observed TV。
- `analysis/kbs_plan_c/test_ni1c_topk_one_candidate_sensitivity.py`：4项public-only单元测试检查TV、full Δ flip、重复采样概率与异常输入。
- `.github/workflows/kbs-n12-ni1c-structured-sensitivity.yml`：ubuntu-24.04自动化执行公共脚本/测试；**不能在真实Actions completed/success前写CI PASS**。
- 之前NI-1b精确有理数观测等价 [#39384747179](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39384747179) 为已验证成功；NI-1c独立检验不重开历史NI-1b或V2a。

## 6. NI-1c 核心方法准入结论与未来研发停止规则

**NI-1c 科学作用：STRUCTURAL_SENSITIVITY_ESTABLISHED_ON_PUBLIC_SYNTHETIC / NO_CORRECTED_S_FIT_APPROVED。**

NI-1a定义了采样信息合同；NI-1b已做严格观测等价；NI-1c新增*强结构但仍弱探测*反例。它们共同说明：需要额外结构与估计风险控制来学习full条件效用，但**没有提供已验证的 sampled-only estimator**。

**方法学准入仍为HOLD**，NI-2/NI-3及V2b都**未授权**。下一项若继续NI-1，应研究**可解释、训练折内识别的latent-rank分布族**及其在heldout sampled-S observation下的拟合与敏感性界，并先提出可被数据推翻的具体观测约束。可以考虑基于现有文献的distribution-estimation/decision-regret界，但不能重复已经验证的prior toy；没有可信方法时就停留在bounded论文Path A并交由责任作者决定KBS GO/NO-GO。

此NI-1c文件及代码的提交均未改变`main.tex`、Supplement、原B1/原G5/H1测试、私有事件/模型或当前论文冻结表/CI基线。
