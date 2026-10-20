# N12-NI / NI-1e — 四状态共享负样本联合混合估计与错设反例

**2026-10-20 | PUBLIC SYNTHETIC POSITIVE/NEGATIVE CONTROLS PASS LOCALLY / GITHUB CI PENDING VERIFICATION / REAL M3 ESTIMATOR NOT APPROVED / NI-2 HOLD.**

## 核心设计（本次新增；不重复NI-1b/c/d）
本轮将NI-1d已知的两个(10/11)点扩展为四个相互差异较大的latent rank-pair/overlap状态，使用同一574无放回抽样的 **Base和Memory joint censored top10 NDCG emission**。对组内4种状态的混合权重使用**只观察采样标签**的EM最大似然拟合；完整F的状态rank用于模型**事先假定的支持集**及合成生成真值，**不**输入训练事件的full outcome。

四个**人为选定、预先公开**的原子：(label, R_B,R_M,o)= A(3,8,2), B(14,5,3), C(40,18,7), D(12,11,6)；o为两专家排在目标前面负例身份的交集。对每状态，非目标分为两者ahead、仅Base ahead、仅Memory ahead、均不ahead四类；单次shared-negative多元超几何抽样，观测到(min(X_B,10),min(X_M,10))，10是零值删失类别。代码用精确组合数形成概率质量，再用浮点运算实现EM。四原子是强烈的事前结构信息，**并非**在M3中已知。

人工两组：A为N=14022和混合权重(.25,.10,.55,.10)；B为N=53762和(.10,.55,.15,.20)。每组训练20,000个合成事件和额外4,000个独立生成的合成观测，仅用S标签计算留出对数损失；6个随机种子重复，训练/留出事件独立但共享人为世界模型。固定50%组级quota，调用一个组的全部请求（与当前在线逐请求30%策略不同）。

## 实际公开本地计算及阴性对照

| 6次均值 | A (N=14,022) | B (N=53,762) |
| --- | ---: | ---: |
| 生成真值完整Δ_F | −0.007449 | +0.194316 |
| 原S训练标签均值 | +0.088358 | +0.028243 |
| 正确四状态支持族的S-only EM估计Δ_F | −0.005025 | +0.193831 |
| 故意错误支持族的S-only EM估计Δ_F | +0.108037 | +0.135053 |
| 正确族留出sampled-S负对数似然/事件 | 2.239198 | 0.715265 |
| 错误族留出sampled-S负对数似然/事件 | 2.277216 | 0.715708 |

**同样50%组级预算**下，raw S优先错误选A（0/6正确），正确族EM选B（6/6正确）。错误族在本设置里也选B（6/6正确），**因此绝不能声称“支持族错设必导致错误路由”**；其错误主要体现在 **full条件效用校准**：组A估计从真实−.0074误判为+.1080，组B从真实+.1943变为+.1351，留出sampled likelihood在大N时仅变化约0.00044/事件。这展示**预测sampled-S表现接近也不等于full-F价值校准正确**，而非对KBS论文实验的直接证据。

额外开发性有限样本扫描（非默认CI）：500/2000/20000每组合成训练、12个生成随机种子，正确族选择B为12/12；错误族分别9/12、11/12、12/12。这个数据说明错误模型在样本稀少时有一定策略风险，但并不能保证未来模型存在同样趋势，也不是预注册原假设检验；不可用作显著性声明。

**数学/代码审计边界**：这里的状态支持集是造例者知道的；在真实M3中，无法仅从原单次S标量确定这四个支持原子或其重叠o。正确模型的精确模拟恢复是“给对支持族就能拟合权重”的正向控制，**不代表识别了未知的真实full rank distribution**，更不是原创算法首创。样本小、candidate N大时差异主要受弱抽样信号和似然曲率影响；本文件没证明通用sample complexity bound和通用可识别性。

## 新颖性先例与停止门
- [Krichene & Rendle KDD2020](https://research.google/pubs/on-sampled-metrics-for-item-recommendation/)已研究sampled metric不一致及纠正。
- [Jin et al. AAAI2021](https://ojs.aaai.org/index.php/AAAI/article/view/16537)已有估计采样下global rank distribution的weighted MLE和maximum entropy方法。NI-1e的低维混合EM原则不应当作新方法首创。
- 真正有希望的新的科学对象仍为 **共享sampled negatives下两个固定专家的条件full Δ估计是否足以支持预目标知识调用**，前提是能找到数据支持且可证伪的联合潜变量假设。

**阶段结论：NI-1e TOY FAMILY POSITIVE CONTROL + MISSPECIFICATION RISK DEMONSTRATED / METHOD GATE HOLD / NI-2 AND PRIVATE V2b NOT APPROVED。**

继续阶段需针对**从S数据学习或验证支持原子**提出稳健、不依赖F训练标签的约束，并报告高N时分布类的识别/似然条件数、样本量和留出风险；不能反复人工选择支持集刷更佳结果。若无可信可识别真实模型，则按照NI-1停止规则返回原Path A投稿/转向决策，原论文仍冻结38页主文和47页Supplement。

## 本次交付
- `analysis/kbs_plan_c/ni1e_joint_censored_mixture.py`: shared-negative hypergeometric emission, censored likelihood, S-only EM, wrong-state negative control, synthetic S holdout。
- `analysis/kbs_plan_c/test_ni1e_joint_censored_mixture.py`: 4项公共test，本地4/4 PASS。
- `.github/workflows/kbs-n12-ni1e-joint-censored-mixture.yml`: Ubuntu-hosted runner自动计算和test；**待GitHub实际状态核实方可称CI PASS**。
- 无私人DEV/TEST、训练模型、真实历史原始资料外传、论文主稿改动；E0–E5保持已完成。
