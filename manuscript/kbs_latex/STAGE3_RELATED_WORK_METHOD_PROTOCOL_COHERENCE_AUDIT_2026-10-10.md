# 第三阶段｜Related Work、Problem Formulation、Framework 与 Experimental Setup 投稿级协调修订及 Gate 3 审查

**日期：2026-10-10。主稿范围：§§2–5。第三阶段 Gate 3 已完成并通过源码、科学论证及精确提交版本编译验收。**

- **权威大纲：** [KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)。
- **任务依据：** [四阶段修订计划](KBS_OUTLINE_ALIGNED_ARGUMENT_REVISION_PLAN_2026-10-10.md)、[第一阶段 P1/P2 队列](STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md)、[科学事实冻结基线](STAGE1_FROZEN_CLAIMS_AND_BASELINE_2026-10-10.md)。
- **第三阶段之前主稿：** 第二阶段稳定源码 commit [cfc8676d](https://github.com/mzch0210/KuaiLive-Agent/commit/cfc8676d707d7525023a957f3732452d6161f3d7)，`main.tex` blob `6e04bb654f3e950205be249b34cfeb62c36b9c25`。
- **第三阶段实际完成源稿：** commit [db6f9654](https://github.com/mzch0210/KuaiLive-Agent/commit/db6f96545fdbdede198f4a129a29f6db0735a92b)，`main.tex` blob `afee37b087dee507f908e0d16816cd462daf7823`。其前一个 §5 主修订为 [4123e6e0](https://github.com/mzch0210/KuaiLive-Agent/commit/4123e6e0e7e2b0354342e5d361dc5001cc8b843e)。
- **引用和实验依据：** [kbs_references.bib](kbs_references.bib)、[正式发表版本文献审查](RELATED_WORK_PUBLICATION_AUDIT_2026-10-08.md)、[S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)。

## 一、执行结果：职责归位而非再次重构中心论点

| 执行提交 | 任务 | 具体修改及学术作用 | 科学对象或限制 |
|---|---|---|---|
| [f1581e0b](https://github.com/mzch0210/KuaiLive-Agent/commit/f1581e0bf87b6da5971f7d18e689874494d0013c) | **A02/B02：Related Work** | 保留原有四组文献和 Research Gap，但各组沿明确比较轴组织：historical representation vs incremental decision value；fusion/reliability vs incumbent-relative specialist effect；general learning-to-defer/uncertainty routing vs fixed relationship-memory benefit；live-streaming representation vs candidate-dependent valuation。研究缺口由科学命题收束，而不是罗列他人没有完成的工作。 | 不声称 \(\Delta_M\) 是新数学定理，不将 post-hoc expert routing、MemRec 或 sampled-metric ordering 首创归于本文；保留已有全部已引用文献 |
| [05060c04](https://github.com/mzch0210/KuaiLive-Agent/commit/05060c046504ed15c4e4bac44ad90c6a505e9b68) | **B03/B04：§3 Problem / §4 Framework** | §3 更清楚区分 event ranking utility、relative-utility supervision、pre-outcome conditional expectation、threshold decision、regime decomposition；§4 以 Base→fixed Memory alternative→relative-utility prediction→conditional output 串起公式和 Figure 1。目标相关状态仅承担 retrospective diagnosis，强化 observable vs target-dependent 信息角色。 | 公式与编号全部保持原样；不改变 Memory 系数、Base 配方、特征数量、历史记录资格或任何目标标签定义 |
| [4123e6e0](https://github.com/mzch0210/KuaiLive-Agent/commit/4123e6e0e7e2b0354342e5d361dc5001cc8b843e) | **B05/B10：§5 Experimental Setup** | 将 Twitch DEV-fitted/threshold-frozen TEST、Base-Difficulty 和 Oracle 的 **hindsight top-m equal-call selection** 及 DEV-only estimators 置于 comparator/protocol 小节。KuaiLive 任务候选、原 fixed-checkpoint paired analysis、两种 score standardization 参考及 paired decomposition 明确保留。Bootstrap 与复现实验细节集中；方法比较表注精确区分冻结模型/阈值与事后 event selection。 | 没有把 Difficulty top-m 描述为独立固定 serving threshold；没有把原 KuaiLive 已检查 TEST 称为一次新冻结策略验证；candidate number/composition effects 不作因果分离推断 |

**§5 最后一项精度修订：** [db6f9654](https://github.com/mzch0210/KuaiLive-Agent/commit/db6f96545fdbdede198f4a129a29f6db0735a92b) 将“估计器在 DEV 重新拟合并冻结应用 TEST”的笼统说法，收紧为**Twitch 冻结门控 TEST 的确切行为**，并将 KuaiLive 候选环境分析明确定位于**已检查 TEST 同队列的配对评价**。这保护跨章证据等级，未更动模型、阈值或结果。

## 二、按章工作归位及文字浓度

| 章节 | 阶段二近似词数 | 阶段三近似词数 | 独立学术职责 |
|---|---:|---:|---|
| **§2 Related Work** | 578 | 519 | 正式发表最近邻的真实贡献及 knowledge-as-decision-value 的科学缺口 |
| **§3 Problem Formulation** | 818 | 772 | 事件级增量排序价值、条件预测目标与期望决策收益的形式化 |
| **§4 Framework** | 943 | 903 | 双平台固定 Base、独立 Memory、可观测选择器的可执行实例化 |
| **§5 Experimental Setup** | 1356 | 1301 | 数据与候选协议、TEST 冻结、比较器信息访问、统计/实现复现 |
| **§1/§6/§7** | 阶段二版 | **逐字未变** | 核心问题、实证结果、综合解释的稳定叙事 |

以上为 LaTeX 源文本空白分词近似值，不是 KBS 强制字数或净英文词数。压缩处理以信息归位和明确句子职责为目的，不以“越短越好”或删掉实际负结果为目标。

## 三、最接近研究比较——正式发表记录及准确对照

本阶段**没有新增未经核验引用**。全部既有 citation keys 原样保留，侧重提高对比论证质量。以下形式化文献定位已再次通过其正式出版页面核查：

1. **MemRec — Chen et al., ACL 2026**，*MemRec: Collaborative Memory-Augmented Agentic Recommender System*，[ACL Anthology 正式版](https://aclanthology.org/2026.acl-long.2061/)，DOI `10.18653/v1/2026.acl-long.2061`。主要贡献是管理与蒸馏 collaborative memory graph 向 LLM recommenders 提供上下文；不同于本稿评估一个固定关系 ranker 相对既有 Base 的事件级净效用。
2. **Mozannar & Sontag, ICML 2020**，[PMLR 正式版](https://proceedings.mlr.press/v119/mozannar20b.html)：研究如何在分类器与专家之间学习 defer 决策。
3. **Narasimhan et al., NeurIPS 2022**，[NeurIPS 正式版](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html)：已有模型的 post-hoc deferral 与 error/cost comparison 已属已知方法学。
4. **GUIDER — Xu et al., AAAI 2026**，[AAAI 论文正式页](https://ojs.aaai.org/index.php/AAAI/article/view/38639)，DOI `10.1609/aaai.v40i19.38639`：以 LLM uncertainty 指导 re-ranking 的适应策略。
5. **DCGLive — Guo et al., The Web Conference 2026**，[ACM 论文正式版](https://doi.org/10.1145/3774904.3792241)：动态 room-level collaboration、room/streamer/user graph 表示与直播房间动态，不等同本稿的固定 specialist-value 比较。
6. **Krichene & Rendle, Communications of the ACM 65(7), 2022**，[DOI 正式版](https://doi.org/10.1145/3535335)：sampled item-ranking metrics 可改变模型比较顺序。本文将这个已知评价问题放到 relationship-evidence specialist 与 incumbent 的相对知识价值分析中，而非声称首次发现 sampled metric inconsistency。

**期刊定位：** Elsevier [Knowledge-Based Systems 官方期刊主页](https://www.sciencedirect.com/journal/knowledge-based-systems)及 [Guide for authors](https://www.sciencedirect.com/journal/knowledge-based-systems/publish/guide-for-authors)。本稿重点是 operational knowledge valuation 与 adaptive decision support 的连接，不能仅以路由效果或历史建模细节作为中心创新。

## 四、事实保全、跨章一致性和检验结果

### 源文件粒度

- 对比第三阶段开始时的 `cfc8676d` 源文件，**仅 §2、§3、§4、§5 发生任何文本变化**；§1 Introduction、§6 Results、§7 Discussion **逐字完全一致**。这是分节切片比对，不是根据记忆估计。
- `main.tex` 的 **全部 49 个 \label** 无重复，**全部 \ref/\eqref** 可解析，**28 个独立已引用 BibTeX 键**均存在于仍未修改的 `kbs_references.bib`。
- **所有公式环境原文逐字不变**；Figure 1、结果图与主要表格不变，仅调整 §5 的 **Compared Methods 表注**以避免把事后 hindsight comparison 写成 frozen online gate。
- **S1–S9 原始集成证据 blob `067d4e5713eb927d8aab3dee3bf2dde512b314ed` 不变**。
- 冻结主结果数值均保留：Twitch **44,221、0.58211、0.53980、−0.04232、+0.22045、+0.00772、+0.00644、6,650、15.04%、Spearman 0.173、Oracle headroom 11.7%**；KuaiLive **10,222、−0.04120→+0.04631、shift +0.08751、membership +0.08827、score-reference −0.00076**；独立 KuaiLive CPU **0.991ms vs 2.007ms、+1.016ms/2.03×**。
- **研究身份和证据等级严格分开：** C1/C3 的主证据是 Twitch frozen held-out comparison；C2 在已检查同队列 KuaiLive TEST 事件上解释 candidate-regime sensitivity；三训练 checkpoints 和固定 checkpoint 九采样不是多队列复制；CPU 对象是单独 warmed gate/HGB replay with positive overhead。
- **未重复数据训练、调参或 TEST 选择**。现有开发诊断未升级为新独立 TEST 确认。

### 人工同行审稿式判定

**P1 科学论证：** 在本次 §§2–5 的修改范围内，没有发现因编辑而产生的新定义矛盾、在线/离线信息泄漏、错误外推或未正式发表的关键引文。原先 A02、B02–B05 的表达和职责问题已解决。

**P2 文体：** 合并重复的“see Section X”、解释为什么没有做某项操作等过程性句子；保留真正保护科学解释的 target-only label、observed TEST count、offline NDCG、candidate selection 和 source quality 边界。

**下游保留工作：** 第三阶段只验收当前前七章的学术论证一致性，**§8 Conclusion 和 Abstract 尚未撰写**；最终整篇 PDF 逐页排版检查、作者/伦理/利益声明、KBS 作者指南最终核对仍属第四阶段或后续投稿包准备。

## 五、最终构建与 Gate 3 判定

**Gate 3：PASS。** 最终精修源文件 commit [db6f9654](https://github.com/mzch0210/KuaiLive-Agent/commit/db6f96545fdbdede198f4a129a29f6db0735a92b) 在严格匹配的 [GitHub Actions #38040591733](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040591733) 中 **success**，生成 **28 页 PDF**，完成 LaTeX 编译、非空 PDF 验证及 artifact 上传。全轮次 **0 次 Overfull hbox**，最终 pdflatex 轮次无致命错误、未解析引用或交叉引用、BibTeX volume/issue 冲突警告。[源码匹配 PDF 与日志 artifact #11665259920](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040591733/artifacts/11665259920)。前一提交 [4123e6e0](https://github.com/mzch0210/KuaiLive-Agent/commit/4123e6e0e7e2b0354342e5d361dc5001cc8b843e) 也单独通过 [#38040451900](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38040451900)，证明最后的 §5 明确化改动未造成编译回退。本关口核验的是已有 §1–§7 科学论证、定义、数据与来源的连续性和技术正确性；**不等于对 28 页 PDF 的全页视觉验收，也不等于已完成第八章和摘要。**
