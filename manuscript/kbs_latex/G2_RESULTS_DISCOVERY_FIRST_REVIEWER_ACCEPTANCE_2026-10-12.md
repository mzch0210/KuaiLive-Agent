# G2｜KBS Experimental Results 科学发现优先修订与独立 Reviewer 核查

**日期：2026-10-12；执行范围：仅 §6 Experimental Results 的正文叙述。**  
**状态：G2 全部计划源码编辑及科学一致性检查完成；最终源匹配编译和渲染验收以 GitHub Actions 的实际结果为准，不预先冒称构建成功。**

## 0. 冻结基线、科学来源和任务队列

- **G1 验收主稿：** commit [e5409c2c](https://github.com/mzch0210/KuaiLive-Agent/commit/e5409c2c464915c96ce636de1153a4892608b4dc)，Git blob \`0ccd9b02874e0bd5f5fc16a025ce49d1c660fe2f\`。
- **G2 完整修订主稿：** 最终提交 [dcd95a6d](https://github.com/mzch0210/KuaiLive-Agent/commit/dcd95a6d0d2b06adf1eaf51794a0528771b6ef6a)，Git blob `76b100a846c99f98ccca8e93249d7fcc166c7d66`。此前 §6 全部内容修订为 [ed0c5aa1](https://github.com/mzch0210/KuaiLive-Agent/commit/ed0c5aa1952dfff2d9a152037bf7d116084a96e3)；最终提交仅拆分 §6.2 一句置信区间长句。
- **实施提交：** [5e59cd4e](https://github.com/mzch0210/KuaiLive-Agent/commit/5e59cd4ec674d7b4652673f58b751a302bd32cd0)（§6.1/§6.2）；[1801bc76](https://github.com/mzch0210/KuaiLive-Agent/commit/1801bc76ee4c4ab9c7b785b5a8464aa31c4800af)（§6.3–6.5）；[ed0c5aa1](https://github.com/mzch0210/KuaiLive-Agent/commit/ed0c5aa1952dfff2d9a152037bf7d116084a96e3)（候选环境非单因素的表述）；[dcd95a6d](https://github.com/mzch0210/KuaiLive-Agent/commit/dcd95a6d0d2b06adf1eaf51794a0528771b6ef6a)（针对日志 32.92719pt overfull 的 §6.2 排版修复，所有结果数值原样保留）。
- **写作/期刊依据：** [G0 双向主张证据矩阵](G0_FROZEN_BASELINE_CLAIM_EVIDENCE_TRACEABILITY_2026-10-11.md)、[G0–G5 第二轮计划](KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md)、[94 段编辑清单](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md)；[Elsevier Results 正式写作建议](https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/how-to-write-the-results-section-of-a-research-paper/)（客观、主要发现优先、图表与正文互补、保留负结果；此为通用出版指导而非 KBS 特定字数要求）。
- **科学资产冻结：** [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md) Git blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`；[\`kbs_references.bib\`](kbs_references.bib) Git blob \`358e6599711421ac609cb1956cfc9cd122cdc341\`。

## I. 先明确 G2 的学术成果，而不是用“删除过程词”衡量成功

**主线严格保留 §6.1（C1）→§6.2（C3）→§6.3（C2）**；§6.4、§6.5 是对主要发现的 DEV 解释与成本检验，不是新增的独立冻结策略试验。

| G2 任务 | 直接修改 | 学术改善及 Reviewer 判断 |
|---|---|---|
| **B1 §6.1** | 开头把整体 Memory 负效用与在 recoverable target-history group 上的正平均效用形成对照；清晰交代 target-defined states 属事后诊断；从观测差异自然引出 pre-outcome Utility prediction | **PASS**。负结果是条件互补的重要证据；未把 recoverable state 错用为在线可观测变量 |
| **B2 §6.2** | 将 Utility–Base 和 Utility–Difficulty 冻结 TEST 的精确 paired 效果集中为主要结果；selected vs unselected mask 和 DEV 目标组富集写在同一支持性段落；Oracle 的有限恢复率紧贴预测机会说明 | **PASS**。保留 DEV-frozen Utility threshold vs retrospectively TEST-batch top-\(m\) Difficulty/Oracle 的信息访问区别；支持段落不是第二个独立验证 |
| **B3 §6.3** | 以原固定 pair 候选符号反转引领段落，2×2 crossed reference 的描述性 allocation 紧随其后；三 trained pairs 和原始固定 pair 的九个 draws 合并为一次稳健性说明；状态组效应最后解释相同 target-state prevalence 的非充分性 | **PASS**。没有把 candidate-set composition 单独识别为原因；不把 seed 和抽样绘制说成独立 TEST 或 gate transfer |
| **B4 §6.4** | 统一围绕两条解释线：**pre-outcome history+Base-score features 的互补预测信息**；**Memory 历史组件以及重训 Base 已见历史改变 relative utility**。保留 DEV feature-family 表，其他 component/grid/recency 结果作为相应解释的支持，减少程序复盘 | **PASS**。所有数字、可区分的 DEV 数组与多训练 Base 的 caveat 均保留，不升级为冻结 TEST 结果 |
| **B5 §6.5** | 实际报告 warmed KuaiLive CPU 的正开销，区分 Twitch 15.04% invocation 与另一个 14.25% 独立 CPU replay；减少成本组成的重复描述 | **PASS**。没有把 selective use 解释为 net speedup，也没有暗示真实线上 A/B 收益 |

**数字、图表和方法存量：** 第六章的全部主 figure/table 及 captions 在 G2 期间**逐字保持不变**，同时全部显示公式环境保持不变；所有原结果数据和 CI 没有重新计算/创造。文本编辑只重排解释力度与逻辑顺序，不更改标的、候选、特征、Memory 系数或固定选择阈值。

## II. Reviewer-style 源码严谨性核验

- **严格变更范围：** 以 G1 \`e5409c2c\` 版本为基准，当前主稿从 \`\\section{Experimental Results}\` 到 \`\\section{Discussion}\` 之外的全部源码**逐字相同**。§1–§5 与 §7–§8、参考文献均未修改。
- **LaTeX 交叉引用：** 主稿仍有 **50** 唯一 \`\\label\`；所有 \`\\ref/\eqref\` 可解析；所有 **28** 个独立引用键均存在 BibTeX，未在 G2 新增未核实论文。
- **统计/分组：** Twitch frozen TEST 44,221、DEV 46,878；Utility 6,650 calls (15.04%)；Difficulty top-\(m\) 事后 batch 选取；Oracle 11.7% 和 Spearman 0.173；KuaiLive 10,222 matched events、完整/采样反转、matched 2×2 allocation、three checkpoint pairs + nine draws；单独 CPU overhead 均保留原表达范围。
- **数值不可变性：** 核对全部保留的原始主结果数据串，内容未改。源码 token 比较只显示部分数值的文字出现次数发生变化（例如 6,650 少出现一次），属于去重；没有编辑 figure/table 中任何数值或图轴。
- **评价类别：** C1/C3 是 Twitch frozen TEST 的主要因果外推受限离线证据；C2 是 KuaiLive already-examined TEST 配对描述性分析；§6.4 是 DEV-only 辅助解释；§6.5 为独立 KuaiLive warmed scoring benchmark。
- **学术叙事：** 每个主要小节第一段均给出一个可复述的 empirical finding，后续段落提供必要置信区间和解释性对照；将最新研究的理论比较留给 §7 Discussion，在 Results 中优先解释自身数据。

## III. G2 结论与 G3 准入

**G2 正式验收：PASS（科学论证、源文件范围、编译与局部视觉版面）。** 第一次完整内容版本的 [Actions #38192050763](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38192050763) 曾发现 §6.2 两组连续置信区间中的 32.92719pt Overfull；最终提交 `dcd95a6d` 拆分该句但不改变效应/CI。与此最终 commit 完全匹配的 [GitHub Actions #38192207908](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38192207908) 已 **success**，编译、有效 PDF 验证、artifact 上传均通过；最终 PDF **29 页**，整次构建 **0 个 Overfull hbox**，最终轮次无致命 LaTeX 错误、未解析 cross-reference/citation 或 BibTeX volume/issue 冲突。[源匹配 PDF 与编译日志 artifact #11721809086](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38192207908/artifacts/11721809086)。

**真实 PDF 视觉复核：** 已下载 artifact 内实际 `main.pdf`，用 `pdfinfo`/`pdftotext -layout` 检查 29 页完整性，渲染并逐页概览第 **15–22 页**（§6 从 p15 开始，第 7 章从 p21 开始）。第六章状态图、Twitch policy 表、KuaiLive crossed reference 表、DEV 特征对照表及跨章分页没有发现文字明显越界、图表覆盖、孤立标题或异常空白。此为**受影响页面验收**；全篇分页终审仍属 G5。

**G3 的边界：** 按原计划只修订 §7 Discussion，以更紧密的学术解释连接新的 §1/§2 与现有 §6 的证据，尤其与 L2D/sampled-metric/knowledge fusion 的文献对话。不得扩大为跨平台 selector validation、因果 candidate-size、净计算节省或先改掉 §8 结论。完成 G3 后才进入 G4 §3–§5 的最小协调、§8 一致性与 G5 全文 KBS reviewer audit。
