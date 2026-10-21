# N12 C8V Rev2 | corrected-S候选估计器的合成审查

日期2026-10-19。**公开合成方法审查 PASS，corrected-S政策科学验证 NOT DONE，V2b NOT AUTHORIZED。** 本轮没有访问私人DEV/TEST行、没有训练模型或修改论文。

## 1. 原始源的证明边界

B1-2采用 `N` 个完整候选中保留观测目标、无放回抽574个负例组成575个S候选。完整排名为 `R`，样本中排在正例前方的负例数 `X`，则 `X~Hypergeometric(N−1,R−1,574)`，采样标量 `u_S=1/log2(X+2)`（`X<=9`）或0（`X>=10`）。已自托管核验全部50,049来源存在且哈希匹配，并在固定的128 DEV事件核对三评分器完整F排名、原B1 S标量各0差异：成功运行 [#39232305650](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39232305650)。这些是**旧标签重建而非新校正方法**。

**更精确的信息可用性结论**：旧B1 CSV虽不保留完整S ranking或575候选分数，但对单正例NDCG@10，若 `u_S>0`，由数值可唯一反推出 `X\in{0,...,9}`；若 `u_S=0`，则 `X>=10`且固定评分器原完整排名 `R>=X+1>10`，故完整 `u_F=0`。因此**仅对以完整Top10 NDCG为纠偏目标**，旧CSV中的标量、完整候选数量N与原采样协议已提供某些映射的全部信息；不应再声称“必须重建完整S排名才能做任何corrected-S”。若欲研究样本Top10外的完整排名估计、成对Score/Joint error或完整F得分向量，则仍可能需要更多私有字段/重建。

## 2. 三种候选估计与其明确偏差范围

A. `original_s`：保持原采样NDCG不变；这是旧B1已测试的监督标签，非新实验。

B. `rank_expansion`：若采样 outrank `X<=9`，按 `R_hat=1+(N-1)X/574` 估计完整排名并代入截断NDCG@10；若 `u_S=0` 则输出0。对于给定R，`E[X|R]=574(R-1)/(N-1)`，故在能观察完整X时 `R_hat` 的条件期望等于R；但 `u_{10}(R_hat)` **不是** `u_{10}(R)` 的无偏估计，尤其截断变换有高偏差。此方法受CIKM2024 Subbiah–Rendle–Aggarwal rank-estimation研究启发，不声称逐字实现其WARP/LambdaRank方法。原sampled scalar在X>=10时删失，当前方法只针对Top10指标修正。

C. `uniform_prior_posterior`：在**明确假设真实R在1..N均匀分布**时，根据精确超几何式计算 `E[u_F|X]`；这一先验不是现有KuaiLive用户真实排名分布的验证结论，因此**不能当作已经批准的校正器**。任一历史先验要成为条件效用监督，需在受控DEV训练折内确定，防止target-label泄漏到预决策输入。

## 3. 合成压力测试真实结果与局限

- 公共固定合成条件：`N=14,022`或`53,762`，`n=574`，两类明确指定的真实完整排名先验——top-heavy与tail-heavy。对每个真实R由**精确超几何概率**求各候选纠偏的条件期望、均方误差、总体合成偏差。不从私有DEV或TEST校准混合权重。
- [GitHub Actions #39235271548](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39235271548)：**SUCCESS，8项单元测试通过**，源代码及安全聚合JSON保留于 artifact ID **12178771181**。
- 在合成`N=14,022` top-heavy的误差（按相同固定先验加权）：

|方法|合成偏差|MSE|
|---|---:|---:|
| 原始 S NDCG | +0.415212 | 0.263867 |
| 排名扩展后NDCG | +0.266176 | 0.212948 |
| 均匀排名先验的后验NDCG | −0.327361 | 0.224780 |

- 在同样`N=14,022` tail-heavy的误差：

|方法|合成偏差|MSE|
|---|---:|---:|
| 原始 S NDCG | +0.323811 | 0.206333 |
| 排名扩展后NDCG | +0.114875 | 0.108164 |
| 均匀排名先验的后验NDCG | −0.011332 | 0.016158 |

**解释：** 排名扩展改善了上述两个合成混合分布下的采样误差，但仍有明显正偏；人为均匀先验后验在tail-heavy例子表现较好，在top-heavy例子则严重低估。没有一种仅凭这一组合成压力结果的估计器值得宣称“实际DEV已验证”。以上MSE评价对象是**单专家 full Top10 NDCG**，**不是**成对Memory−Base增量效用误差，更不是下游门控策略收益。因此**不能利用这些数字直接选择V2b赢家**。

## 4. 对当前新颖性主张的意义及方法文献

- Krichene & Rendle (KDD2020)已经建立 sampled metrics不一致及偏差/MSE校正： https://research.google/pubs/on-sampled-metrics-for-item-recommendation/
- Subbiah, Rendle & Aggarwal (CIKM2024)已讨论利用采样负例改进训练排名估计，对N12的监督问题形成较近先例： https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/
- 正确的区别是**总体或训练时rank correction** vs **用于冻结Base与Memory相对Top10效用、并监督其调用选择的逐请求条件估计**；CIKM的方法不能在未经专门证明前搬入原方法并称普遍优于F。
- A/B/C比较的下一阶段应先设计**联合同一S抽样下的Memory/Base配对误差**（相关而非两套独立采样），并在original DEV用户分组训练折内预定可能的先验信息合同。除非它还能检验旧B1三臂未回答的拒绝性科学假设，否则可选择取消V2b并将论文主张约束为“F相对原未校正S监督”。

## 5. 验收判定

**V2a数据与旧标签来源一致性 PASS；公开单专家纠偏合成压力 PASS；方法选择门槛 HOLD。** 下一阶段的必要条件：① 同候选、同抽样的Base/Memory joint rank correction synthetic test；② 明确预目标可用信息与DEV训练折先验，审查target-retained offline label与deployment信息隔离；③ 方法独立审稿与学术价值评估；④ 若仍有明显增量才分开批准V2b DEV-only policy pilot。绝不使用已揭盲B4-A 30k决定校正方法，不强制重复已有B1 S/F/Adapted三臂。

本次未改main.tex，论文仍是已验收37p主文、47p完整Supplement。