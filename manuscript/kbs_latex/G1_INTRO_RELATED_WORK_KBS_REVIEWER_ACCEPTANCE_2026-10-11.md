# G1｜Introduction 与 Related Work：KBS 主线及正式最近邻比较修订记录

**执行日期：2026-10-11。**  
**来源：** [G0 科学冻结及八章双向证据表](G0_FROZEN_BASELINE_CLAIM_EVIDENCE_TRACEABILITY_2026-10-11.md)、[第二轮 G0–G5 计划](KBS_PAPER_SECOND_PASS_SUBMISSION_NARRATIVE_REVISION_PLAN_2026-10-11.md)、[94 段编辑矩阵](KBS_SECOND_PASS_94_PARAGRAPH_AUDIT_2026-10-11.md)。  
**修改范围：只改 \`main.tex\` 的 §1 Introduction 和 §2 Related Work。**  
**源稿基线：** \`main.tex\` Git blob \`fa73ba31a56edd96f6eeaca272214b98bf4a9a9d\`。  
**最终编辑源稿：** [commit 21fef333f97450229777c1716884b71fc0a60a2d](https://github.com/mzch0210/KuaiLive-Agent/commit/21fef333f97450229777c1716884b71fc0a60a2d)，blob \`d98353c7356ade3c9c164463fadffe1363c558de\`。  
**分节提交记录：** [§1 commit aea35485](https://github.com/mzch0210/KuaiLive-Agent/commit/aea354850e294e10b472c92b95fe6dc94e3a61ef)；[§2 commit 21fef333](https://github.com/mzch0210/KuaiLive-Agent/commit/21fef333f97450229777c1716884b71fc0a60a2d)。  
**精确源码 PDF 工作流：** [GitHub Actions #38137569135](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38137569135)；以该运行的真实状态为准，未编译成功前仅确认 *source-level scholarly review*。

## 一、G1 修改及论证的独立职责

| 编辑队列 | 实际改动 | 独立审稿要检查的增量 |
|---|---|---|
| **A1 / S1-P01/02** | 引言第一段从“序列模型能够表示近期行为”转到“持久关系证据既可能已被强 Base 的评分包含，也可能在其可见历史之外形成互补”，进而定义何时固定知识专家实际改善当前排序。第二段承认融合、协作记忆及已知 defer 算法，同时提出具有不同学科解释目标的操作性评价问题。 | 主研究张力成为**incumbent 已能做什么与额外关系证据真正能增加什么**，没有简单重复两次研究缺口 |
| **A2 / S1-P03/04 和 C1–C3** | 直播推荐场景仅通过持久主播关系和变化候选环境引出两项变化来源；Twitch C1→C3 是冻结策略验证链，KuaiLive C2 是 fixed-ranker paired context comparison；contribution itemize 保留 C1、C2、C3 官方编号和已冻结实证边界。 | 两平台职责清楚，**不声称 gate 已跨平台验证**、target-state 可作为服务输入或候选 count 因果已被识别 |
| **A3 / §2 全部旧 S2-P01–06** | 将原有四个主子节 + Research Gap 缩合为三个主题：**Historical Representation and Auxiliary Knowledge**、**Selective Prediction and Specialist Allocation**、**Live-Streaming Recommendation and Candidate-Context Evaluation**。每个主题同时提出已知研究贡献及与当前操作性知识价值问题的具体关系。 | 不是通过标题数量做修辞：第 2 章正文由约 519→681 个 LaTeX 空白分词，为最近邻研究建立真正的科学对话 |
| **A4 / 对最强“缺乏新颖性”的替代解释** | 明确 L2D 先前已经研究专家选择和成本，GUIDER 已利用不确定性进行动态重排，MemRec 已构建和蒸馏协作记忆，Krichene/Rendle 已证明 sampled metric 模型比较可反转。本文的可辩护新增问题是**一个固定历史关系知识专家对指定 Base/候选集的增量价值，及其条件异质性、预先选择和候选评价情境证据**。 | 无“首次提出效用减法”“提出通用 defer 理论”“首次发现 sampled metric inconsistency”等错误创新主张 |

**修订字数核对（LaTeX 源文本近似统计）：** §1 **450→493**，§2 **519→681**；§3 **772**、§4 **903**、§5 **1337**、§6 **1934**、§7 **947**、§8 **216**，后六章逐字保持原样。此项统计不是 KBS 的格式限制，也不能仅凭篇幅增加判断学术质量。

## 二、正式发表最近邻验证（按主办方/出版社页面）

- **KBS 官方范围：** [Elsevier KBS](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)；关注原创 AI、知识系统、推荐/个性化和智能决策支持，兼顾理论与实际方法。无法据此推出 KBS 要求必须有新的通用数学定理。
- **Chen et al., MemRec, ACL 2026 (Jul, official anthology):** https://aclanthology.org/2026.acl-long.2061/；构建/管理 collaborative memory graph 并蒸馏可用上下文，已有多模型记忆关系工作。
- **Xu et al., GUIDER, AAAI 2026 official proceedings:** https://ojs.aaai.org/index.php/AAAI/article/view/38639；数据/模型 uncertainty 与 LLM-based recommender dynamic re-ranking。
- **Mozannar & Sontag, ICML 2020 official PMLR:** https://proceedings.mlr.press/v119/mozannar20b.html；专家 defer 目标、成本敏感估计与一致性理论。
- **Narasimhan et al., NeurIPS 2022 official proceedings:** https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract-Conference.html；基于既有模型的 post-hoc expert deferral。
- **Montreuil et al., AISTATS/PMLR 2026:** https://proceedings.mlr.press/v300/montreuil26b.html；专家可用性变化下的在线 defer。
- **Krichene & Rendle, Communications of the ACM 65(7), 2022 DOI 10.1145/3535335:** https://doi.org/10.1145/3535335；采样指标不能保证保留全量模型对比顺序。本稿沿用旧 BibTeX key \`krichene2020sampled\`，实际元数据为正式的 2022 年期刊版本。

**文献与主稿准确性门槛：** G1 没有新增、删除或修改 \`kbs_references.bib\` 中的记录。旧 §2 使用的 **28 个**不同 citation keys 在新 §2 中全部保留，未将 arXiv 预印本替代上述最近的正式发表版本。文献比较应该与已做的证据相符，不能靠否定已有工作取得创新性。

## 三、G0 冻结约束的 source-level 核验

实际从 G0 结束时的 GitHub **commit \`d4f39ca85e37783708520962d0eee7342dca29c5\`** 抽取同一个 \`main.tex\` blob 与最新版全文比对：

- **§3 Problem Formulation 起至文件末尾的全部源码 byte-for-byte 完全一致**。即方法、设置、Results、Discussion、Conclusion、所有表图、公式、结果数值和 BibTeX 使用方式未被本轮改动。
- **全部 50 个 \`\\label{}\` 唯一且无未解析 \`\\ref/\\eqref\`**。
- **正文有 28 个独立 \`\\cite{}\` BibTeX keys，全部存在**；此前引用键未丢失；未动的 reference file blob \`358e6599711421ac609cb1956cfc9cd122cdc341\`；未动的 S1–S9 blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\`。
- Twitch 44,221、Base 0.58211 / Memory 0.53980、Utility +0.00772/+0.00644、6,650 calls、KuaiLive 10,222 / −0.04120 / +0.04631 / +0.08751、candidate membership +0.08827、normalization −0.00076 和独立 positive CPU overhead +1.016 ms 等冻结字符串仍然完整存在。
- **信息访问：** Twitch Utility threshold 是 DEV-frozen 的 pointwise rule，Difficulty TEST top-m 使用 Utility 实际调用次数；KuaiLive 主要分析是已检查 cohort 的 candidate-protocol diagnosis，固定 raw rankers；membership term 包括 number/composition/competition，无 candidate-size 独立因果 claim。
- **自我限定处理：** 正文仍保留上述必要边界；主要删除重复研究缺口、无用途地按文献类别排队以及“本稿未做……”的防御式创新否定。Related Work 将既有研究贡献放到科学比较的主体位置。

## 四、G1 独立 reviewer-style 验收问题

1. **RQ 的可复述性：** 只看 §1，审稿人能复述为什么知识存在/表示增强不等于相对于强 Base 的增量决策价值，以及 Twitch/KuaiLive 两条证据链的关系。**PASS（原文论证符合）**。
2. **最近邻研究的真实性：** §2 明确每类前人解决的实际问题：MemRec 设计/蒸馏记忆、GUIDER uncertainty re-ranking、L2D 选择专家、Krichene/Rendle candidate-sampling metric consistency。**PASS（与官方正式出版内容一致）**。
3. **差异的科学类型：** 不称效用差值、一般 defer、采样比较差异为新理论，正面说明本文固定专家的 incumbent-relative knowledge value 和选择使用的实证贡献。**PASS（在当前证据范围内）**。
4. **证据等级与可推广性：** frozen Twitch TEST 不等于 KuaiLive transferred gate；selected Memory count 与 CPU overhead 不混同。**PASS**。
5. **跨章作用：** §1/§2 为 §3–§7 提出真正需要回答的可检验问题，§8 的最终知识决策结论无新增未支持主张。**PASS（静态文本对照）**。

**风险保留：** 这项改写提高解释清晰度，但无法以修辞消除 KBS 审稿人对跨模型稳健性、真实服务成本或比已有 L2D 更广泛算法创新的期望。G2/G3 才负责进一步提高 §6 的发现优先级和 §7 的文献层面解释；G1 不预先声称整篇已具备最终投稿质量。

## 五、技术关口与 G1→G2

- 最新源提交：[21fef333](https://github.com/mzch0210/KuaiLive-Agent/commit/21fef333f97450229777c1716884b71fc0a60a2d)。
- 精确提交构建：[GitHub Actions #38137569135](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38137569135)。**构建是否 PASS、页数、Overfull hbox、引用 warning 与 PDF artifact 以工作流实际结果更新，不预写成功**。
- G1 的完成条件：源码审稿 PASS，加上精确源码构建成功；若排版引入过宽行或图文覆盖，单独在 §1/§2 修复后重新构建。
- G2 准入：§6.1→§6.2→§6.3 顺序严格保持，主文固定表图和冻结核心数字不变，S1–S9 证据不变；仅根据第二轮矩阵重新组织结果段落。
