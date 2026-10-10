# 第二阶段｜大纲导向的 §1、§6、§7 论证重构与 Gate 2 审稿记录

**日期：2026-10-10；编辑范围：Introduction、Experimental Results、Discussion。**  
**第一阶段基线：** [Gate 1 验收](STAGE1_ARGUMENT_GATE1_ACCEPTANCE_2026-10-10.md)、[95 段审计](STAGE1_PARAGRAPH_ARGUMENT_MATRIX_2026-10-10.md)、[P1/P2 队列](STAGE1_P1_P2_EDIT_QUEUE_2026-10-10.md)、[冻结数据](STAGE1_FROZEN_CLAIMS_AND_BASELINE_2026-10-10.md)。  
**本阶段主稿源代码起点：** GitHub \`main\` \`f7cd9e7f48827eaded4109684bda70ee0e84d9ee\`；\`main.tex\` 旧 blob \`5222d53e071987d651e3d5cb2f1a7a51c8323954\`。  
**本阶段主稿最终提交：** [739748c0980775b4319686d2e72f10523a3968df](https://github.com/mzch0210/KuaiLive-Agent/commit/739748c0980775b4319686d2e72f10523a3968df)，新 blob \`663f9a7cb66a78a450ba3172a437e1940386e1f8\`。  
**科学主张依据：** [权威大纲](../../KBS_PAPER_OUTLINE_2026-09-23T2322+0800_SUBMISSION_ORIENTED.md)，前六章和 [S1–S9](SUPPLEMENTARY_INFORMATION_S1-S9_2026-10-10.md)。

## 1. 修改记录与审稿结论（实际执行，不是未来计划）

| GitHub 源码提交 | 受影响章节 | A/B 任务 | 执行内容与学术目的 | 影响范围验证 |
|---|---|---|---|---|
| [81c6142](https://github.com/mzch0210/KuaiLive-Agent/commit/81c614266b26012518b65d42547797857d14de5f) | **§1 Introduction** | A01, B01 | 重写 4 段科学动机/证据主线和末尾一句范围表达；以强 Base + 历史知识条件增益为核心张力；保留 Twitch 冻结政策与 KuaiLive 事后候选分析的互补性；保留原 C1–C3贡献列表。 | **§2–§7 完全一致** |
| [540b9d3](https://github.com/mzch0210/KuaiLive-Agent/commit/540b9d3f57764bfebebe7990f8fbc903ebabbfdc) | **§6 Results** | A03–A05, B06–B09 | 定向替换 20 个论证段落；保持 §6.1→§6.2→§6.3 的冻结大纲顺序及原有主要图表；先表达数据所说明的条件知识价值、决策增益和候选环境依赖；在 §6.4 区分 DEV feature/Memory/Base 互补性证据；§6.5 先显示**真实正向 CPU 开销**而非暗示速度收益。 | **§1–§5 和 §7 完全一致** |
| [739748c](https://github.com/mzch0210/KuaiLive-Agent/commit/739748c0980775b4319686d2e72f10523a3968df) | **§7 Discussion** | A06–A10, A11–A12 的本阶段科学叙事部分 | 依次解释：Base-relative relationship complementarity → candidate-regime-dependent operational valuation → utility-guided specialist choice → validity tiers → knowledge-based recommendation design principle。删去与 §6 重复的种子/抽样/状态均值/开销细节，保留必要证据和正式发表的最近邻对比。 | **§1–§6 完全一致** |

所有三个源码操作均在指定的 LaTeX \`\\section{}\` 跨节锚点内检查修改范围。依第一阶段计划，\`main.tex\` 数值、公式、文献键、图表和 S1–S9 不做任何新实验式改动。

### 章节定位变化

| 章节 | 修订前约计词数（LaTeX 空白分词） | 修订后 | 论证完成的“唯一任务” |
|---|---:|---:|---|
| Introduction | 413 | **450** | 定义 Base-relative historical-knowledge-use 科学问题，解释 Twitch 选择证据与 KuaiLive 候选依赖的互补性，正式提出 C1–C3 |
| Results | 2,101 | **1,945** | 提供条件效用、冻结选择效用和候选环境变化的主数据证据；DEV 诊断与 CPU 实测作为解释性附加结果 |
| Discussion | 1,231 | **947** | 将结果提升为历史知识的情境化决策价值解释，而不是 §6 的数字复述或协议审查清单 |
| Related Work | 578 | **578（未改）** | 第三阶段将继续统一最近邻比较和 Research Gap 表达 |
| Problem Formulation | 818 | **818（未改）** | 保留已稳定的数学逻辑和符号 |
| Framework | 943 | **943（未改）** | 保留训练 Base、fixed Memory 与 pre-outcome gate 的严格区分 |
| Experimental Setup | 1,356 | **1,356（未改）** | 保留候选、对照、统计与测试隔离的复现协议 |

§7 的减法是有意的学术编辑选择，原写作计划的 1050–1350 词属于建议区间而不是需要机械满足的期刊格式。当前 947 词、五小节、11 个学术段落；科学内容与必要边界依旧可追溯。若下一阶段协同修订 §2–§5 发现实质性机制解释缺口，应补充**新的论证**而不是重新填充已移走的日志细节。

## 2. 逐一审查学术主张与冻结证据

| 大纲贡献 | 新 §1 的研究动机 | 新 §6 的实际数据 | 新 §7 的解释 | 实证外推保护 |
|---|---|---|---|---|
| **C1 Operational valuation** | 强 Base 面前需评估知识的增量排序收益 | Twitch TEST Base **0.58211**、Always Memory **0.53980**，recoverable 状态贡献 **+0.22045**（n=5,539） | 知识的互补性对 Base 的有效历史覆盖有条件 | 事后 target-history group 非服务特征；不能当作内在信息价值的因果测量 |
| **C3 Selective use** | 选择调用依赖对专家相对收益的决策前预测 | DEV 冻结 Utility TEST **0.58983**，Utility–Base **+0.00772**、Utility–Difficulty **+0.00644**、Memory calls **6,650**，Spearman **0.173**、Oracle headroom recovered **11.7%** | 预测专家优势不同于预测 Base 的困难度；该差异对选择知识专家具有实证决策价值 | Difficulty 是事后 TEST top-\(m\) 等调用数对照；不宣称通用 L2D 新定理、线上可部署同预算 |
| **C2 Candidate regime** | 同一知识来源的价值需要在具体候选环境下解释 | KuaiLive 同队列 **10,222** 配对事件：sampled **−0.04120**、full **+0.04631**，shift **+0.08751**、membership **+0.08827**、normalization **−0.00076** | 候选集界定排名竞争，因此评价条件与知识价值相关 | 代数 allocation 非 candidate count 因果实验；三 trained pairs 与单 fixed pair 的九组抽样不是独立数据队列 |
| **Serving cost** | 知识是否值得使用包括获取其效用的计算代价 | KuaiLive 单独 warmed CPU Base **0.991 ms**、HGB **2.007 ms**，**+1.016 ms / 2.03×** | 低调用率与低 end-to-end latency 是不同的系统目标 | Twitch **15.04%** 调用率不能外推出 CPU 节省或线上转化 |

三项主要贡献没有“重新发明”。新的叙事区分两条证据链：**Twitch 主决策验证（C1→C3）**、**KuaiLive 候选环境解释（C2）**。§7 对两条链作理论/操作性综合，未宣称同一 gate 已跨平台验证。

## 3. 统计、写作规范和静态质量检查

**源代码复核：**
- 冻结版本到当前版本的逐 section 比较确认，**只有 Introduction、Experimental Results、Discussion 变化**；§2 Related Work、§3 Problem Formulation、§4 Framework、§5 Experimental Setup 的源文件文本 **byte-for-byte 不变**。
- LaTeX 仍有 **49 个唯一 labels、28 个被引用的 BibTeX keys**；无重名 label、未解析 ref/eqref、缺失 BibTeX 记录或此前已引用文献消失。
- **冻结主数据在主稿均仍存在**：44,221、0.58211、0.53980、−0.04232、+0.22045、+0.00772、+0.00644、6,650、15.04、Spearman 0.173、Oracle 11.7、KuaiLive 10,222、−0.04120/+0.04631/+0.08751、+0.08827/−0.00076、0.991/2.007/+1.016/2.03。
- \`S1–S9\` 的 frozen blob \`067d4e5713eb927d8aab3dee3bf2dde512b314ed\` 仍不变。§6.4 缩去的局部参数数值、候选随机样本详情和 S9 HGB microbench 技术参数本来已完整记录在补充材料。

**语言层面的可量化复核（只是辅助检查，不是期刊评分）：** 预设的否定/防御词模式在 Introduction 从 **4→1**、Results 从 **24→14**、Discussion 从 **19→10**；但冻结、DEV、TEST、协议等词保留是为了确保科学透明。没有通过删除负结果来提高“正面语气”。

**正式写作依据：** [KBS 官方范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)聚焦知识型 AI、推荐和预测/决策支持；[Elsevier 正式作者指南](https://www.elsevier.com/subject/next/guide-for-authors)要求 Results 清晰，Discussion 解释结果意义而非再次罗列，Experimental 信息具备复现性。该指南为一般建议，不冒称这是 KBS 特定 947 词限制。

## 4. 未解决事项与下一阶段依赖

**Gate 2 的范围：** §1/§6/§7 的大纲叙事修复、实证论断与跨章科学作用检查、主稿源代码与 LaTeX 构建。当前已完成源码层面的这些修订，尚须以**最终源匹配的 GitHub Actions 成功构建**确认技术关口（工作流 [38039728285](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38039728285)，source commit \`739748c\`）。

**阶段三仍待执行：**
- [A02 + B02] 最近邻比较与 Research Gap 的收束（§2）；不可将已发表的 L2D/不确定性动态排序误当成本稿首创。
- [B03–B05] §3 数学与 §4 主机制、§5 复现/比较器信息访问责任分离；对从 §6/§7 压缩出的必要资格/计算信息作逐项检查，优先利用已经存在的 §5/S1–S9，而不是直接新增数字或修改公式。
- [B10–B12] 全文 Base/Memory/Utility/Difficulty、candidate regime、target-conditioned history states 术语与学术表达一致性审校。
- §8 Conclusion、Abstract 仍不存在，直到阶段四后续工作才有已完成的稿件内容；不可宣称稿件可直接投稿。
- 尚未执行“整篇 PDF 全页审阅”；来源比对、CI 编译和 PDF 视觉检查是不同质量关口。

**本阶段编辑结论：** 核心大纲论点在 §1、§6、§7 形成一致的知识价值研究叙事；修订来自已有证据，没有用实验追加或过强修辞代替实证。全部三项源码修改可由单独 commit 回溯。只要最终 CI 确认通过，即可将 **Gate 2** 标为通过，转入阶段三而不重复对 §§1/6/7 作无目标的单节润色。
