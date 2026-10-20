# Rev3.0 P0 — 最近邻文献与科学贡献碰撞审查（2026-10-20）

**状态：SOURCE_PAGES_VERIFIED / ADDED_PRIOR_ART_IDENTIFIED / NOVELTY_HIGH_CONTESTABLE / NO_NEW_RESULT.** 仅修改 Related Work 及引用表所需材料，不碰冻结 M3/Twitch/room/H1/H2 数据。此表基于可访问的论文一手出版社页面与摘要/作者公开记录，**不是对全部全文、证明细节的独立形式验证**；不以“文中未包含相同数据集”为原创性充分依据。

## 1. 真正新增的来源核查

| 论文 | 一手书目信息 | 已有贡献、N12不能自称首创 | N12能保留的具体经验增量 |
| --- | --- | --- | --- |
| Krichene & Rendle KDD 2020 | DOI 10.1145/3394486.3403226; https://research.google/pubs/on-sampled-metrics-for-item-recommendation/ | 采样 topK ranking指标和全量rank方向不一致，bias/MSE校正已有 | 观察历史关系专家的监督标签在full活跃候选上改变预目标调用 |
| Jin, Li, Mudrak, Gao & Liu, AAAI2021 | DOI 10.1609/aaai.v35i5.16537, 35(5):4147–4154; https://ojs.aaai.org/index.php/AAAI/article/view/16537 | weighted maximum-likelihood 和 maximum-entropy 估计整体完整rank distribution/topK指标已有 | 非通用rank校正算法；观察固定Memory/Base完整政策的后续分配与结果 |
| Li (Dong), Jin (Ruoming), Liu (Zhenming), Ren (Bin), Gao (Jing) & Liu (Zhi), AAAI2023 | DOI 10.1609/aaai.v37i4.25561, 37(4):4409–4416; https://ojs.aaai.org/index.php/AAAI/article/view/25561 和 https://mlanthology.org/aaai/2023/li2023aaai-reliable/ | 小K采样blind spot、改进estimator、adaptive sampling和EM已有，NI-1 toy不能叫首次信息界或EM校正 | 本稿不声称在采样S-only校正层有新方法；只给出原未经校正S和完整F监督下知识调用政策的实证 |
| Ngozi Ihemelandu & Michael D. Ekstrand, WI-IAT 2023 | DOI 10.1109/WI-IAT59888.2023.00018，pp.88–94; https://mdw.ekstrandom.net/pubs/wi-sampled-eval | 候选集选取和流行度偏差交互、不同采样策略评价已有 | M3特定目标是full-active上的Memory-minus-Base价值和监督→调用而不是候选采样质量本身 |
| Subbiah, Rendle & Aggarwal, CIKM2024 | DOI 10.1145/3627673.3679943; https://research.google/pubs/improved-estimation-of-ranks-for-learning-item-recommenders-with-negative-sampling/ | WARP/LambdaRank类训练时rank correction已有 | 该文不直接在本论文记录的固定历史知识专家—Base协议进行full-vs-uncorrected-S完整政策冻结对照 |
| Mao, Mohri & Zhong, ICML2024 | PMLR 235:34738–34759; https://proceedings.mlr.press/v235/mao24d.html | 预训练predictor、学习委托多个专家、instance-dependent cost、consistency的理论已有 | N12不主张新deferral算法、同预算因果效应；专注监督的候选协议改变调用配置的具体实证 |
| 2026 KBS memory / knowledge-aware近邻 | 既有主稿参考文献：Zhong等SAM D、Xie等MHGFCL（原bib保留） | memory retention、knowledge fusion等已有 | N12固定历史专家，用时测增量价值；不同研究对象不自动证明非平凡性 |

## 2. 新近先例对中心贡献的最大反证

**强烈反方**：“样本评价不一致是KDD2020；恢复rank分布是AAAI2021；blind spots、EM已在AAAI2023；委托专家ICML2024已有，为什么由未经校正S导致不同调用不是当然结果？”

**允许回答**：这不是新理论证明或现成纠偏方法。N12在明确的live历史知识—固定Base和active候选协议中，观察到DEV 50,049相同请求21.32%/23.01%重新分配；在额外同期、未用于原评估的30,000冻结完整政策请求上，SAS/GRU F较原S full-NDCG +.005391/+.003585，且Memory natural calls较少。异采样任务和G2描述不是独立新机制，不能说这是不可预期普遍规律。真正且仍强的竞争者是**有效sampled-only corrected-S**，NI-1g在当前方法没有通过准入，不能宣称被数据排除。

**尚开放**：基线S是否过弱；strict equal-resource comparison缺失；用户/时期外推；Always-Memory无quota质量更高；旧选择器延迟劣势；H2复合Null不是来源语义单独因果；KBS原创性“是否显著超越已知方法组合”仍属HIGH-CONTESTABLE。无直接同构先例被本轮来源页证明，但**未发现不是不存在的证明**。

## 3. 精确修改方案及明确禁止

- 在 `main.tex` 第102行附近 `\subsection{Candidate-Dependent Ranking in Live Recommendation}` 的相关段落补入 *仅一段或相同段的少量句子*，明确 AAAI2021 weighted-MLE/max-entropy; AAAI2023 sampling blind spot/adaptive/EM; WI-IAT2023 candidate popularity interactions。沿用KDD2020及CIKM2024已有引用，保留目前 “具体 knowledge-use decision” 的窄范围差异。
- 在 `kbs_references.bib` 正式新增三条来源的准确书目信息/DOI与稳定官方 URL。**不**更改标题、摘要、三个contributions、统计/图表、Supplement、Highlights、其它Related Work。
- source页确认并不意味着已全篇逐式对照；“未在一手页面找到本课题exact paired conditional policy”只能作为有限证据，不允许写成“第一篇/唯一/已证明修正不可能”。
- 不在NI-1b–f synthetic上创造新Results或理论声称。保留此前 V2a failed methods与NI-1g NO-GO。

## 4. P0阶段验收

**P0 source audit PASS_FOR_MINIMAL_REFERENCES_ONLY / NOVELTY_RISK_UNCHANGED**。后续 P2 完成需检查：三个新增bib key都被正确引用、双PDF C7/C8V成功、LaTeX/bib无undefined reference、原数据源/CI未变、最终PDF可读。不能以本P0为KBS原创性认证。

责任作者在科学上须进一步审核文章原文及贡献定位，尤其人工确认实际阅读与遵守引用许可；AI自动核查不能代替真实研究者独立评价。


## 2026-10-20 执行增补（实际源码）

核对AAAI官网作者列表发现初始BibTeX录入的部分作者姓名有误，现已用一手官网修正：AAAI2021为 Ruoming Jin, Dong Li, Benjamin Mudrak, Jing Gao, Zhi Liu；AAAI2023为 Dong Li, Ruoming Jin, Zhenming Liu, Bin Ren, Jing Gao, Zhi Liu；WI-IAT2023 为 Ngozi Ihemelandu, Michael D. Ekstrand。实际BibTeX修正 commit `5a59e5aba3952d5c7c02a5fdc07c3b1983885519`；Related Work 精确补充 commit `1b0fbe83686ab289dd350cd5a49e5868447e142a`。原文新引文实际可解析与PDF需以下一轮CI报告为准。原 P0 `source audit PASS` 不意味着正文PDF或KBS novelty审核PASS。
