# KBS 审稿式评估：N2-D1 Two-stage DEV 试验对论文贡献和 N5–N8 的影响

**日期**：2026-10-13；**证据身份**：2026-10-13 G5 TEST 揭示之后设计的 `POST_G5_EXPLORATORY_NESTED_DEV`；**验收**：原始 GitHub Actions 聚合 ZIP 经过独立读取、summary.json SHA256 一致性核验；**结论**：对限定的相对价值决策目标提供中等强度的 DEV 方法鲁棒性补充，但不建立 Direct 对成熟 L2D 的普遍优越性。**不修改 main.tex、已冻结 G5 TEST、原始假设家族**。

## 1. 原始证据、统计方案和出处

- [成功运行 #38339908528](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/38339908528)，source commit `8fef2bb01efa0f3976c71839a2fd07507658fa58`，hosted synthetic 和 private self-host 均成功。
- Aggregate artifact GitHub Actions ID `11785704918`，ZIP 内 `summary.json` 的 SHA256 = `b944e791e4797f97892bbbddb6f6729014a00cc3bc11e3cb6f1229b207897706`，与成功日志中的输出一致。临时 artifact 可能过期，正式可复现声明需有合法稳定归档。
- 两种 incumbent：SASRec/GRU4Rec，**只有主种子 20261012**，均使用 M3 full-active author **同一 DEV 50,049 事件、12,628 用户**；不是 TEST 47,575 事件/12,533 用户，也不是独立人群。
- 5 外层用户互斥验证折 × 4 内层用户互斥 OOF；每个外层训练子集以内层 OOF 为两种方法独立确定 `<=30%` DEV specialist-call 阈值，然后在外层验证用户上报告 NDCG、calls；原 G5 TEST 未用于本次拟合、评价或门控复核。
- Direct: `E[u(M)-u(B)|Z]` 的单一 HGB；Two-stage: `E[u(M)|Z]-E[u(B)|Z]` 的两个独立 HGB。在总体数学上是**同一个条件期望估计目标**，比较的是有限样本拟合和门控校准；不等于 NeurIPS 2022 Narasimhan 等人的完整 surrogate-loss 后验 deferral 算法，更不是完整 CIKM 2026 DS-Frame。
- 源代码 `analysis/kbs_plan_c/n2_d1_nested_dev_pilot.py` 使用 **2,000** 次用户聚类 Bootstrap，百分位 95% 区间；本项目未为两架构 DEV 探索性对照指定任何独立 TEST confirmatory 多重比较家族。

## 2. 原始汇总和逐用户簇差异区间

| Incumbent, 主种子 | Direct NDCG@10 | Two-stage NDCG@10 | Direct−Two-stage | 95% user-cluster bootstrap CI | Direct 调用 | Two-stage 调用 |
|---|---:|---:|---:|---:|---:|---:|
| SASRec 20261012 | 0.3026780048 | 0.3013259618 | +0.0013520430 | **[+0.0004223061,+0.0021976582]** | 14980 (29.9307%) | 14693 (29.3572%) |
| GRU4Rec 20261012 | 0.3029891960 | 0.3029385126 | +0.0000506834 | **[−0.0008222777,+0.0009070940]** | 14716 (29.4032%) | 14751 (29.4731%) |

- **DEV reference quality:** SASRec Always Base 0.2581674381、GRU4Rec Always Base 0.2589714713；同一 DEV Always Memory 0.3435091807。Direct/Two-stage 各提升 Base 约 +0.0432 至 +0.0445，但 Always Memory 的无约束绝对准确率仍高于所有约束政策。**真实调用价格/节省未在此试验测量**。
- **SASRec 解释:** 五个 outer folds 的 Direct−Two-stage NDCG 差均为正，整体 CI 不含 0；但 Direct 多调用 **287** 次 Memory（+0.5734 个百分点）。因此两政策在已观测 NDCG/Memory-call 二轴上不构成 Direct 的 Pareto 优势，不能断言相同 TEST/DEV 成本下更优。这里不能沿用原 G5 “Utility wins quality and fewer calls versus four specified alternatives” 的表述。
- **GRU4Rec 解释:** Direct 多 +0.0000507 NDCG 且少调用 35 次（约 −0.0699 个百分点），但区间跨 0，outer folds 有正有负。是描述性近似持平，而非获得确认性优势。
- 这些区间在预设对比的用户依赖结构下描述不确定性，**不是**事前预注册独立 holdout 的方法优越性证明；不能将 SASRec 不含 0 解释为“论文新算法显著优于成熟 deferral”。
- 存在明确的两类额外推断限制：两种估计方式具有不同的推断时计算路径（1 vs 2 HGB），且只有两个原有 Base 主种子；新 DEV 并没有完整六拟合算法鲁棒性，也没有独立计算端到端延迟/外部专家调用价格。

## 3. 对论文 RQ 与核心贡献的正、负影响

| 科学问题 / 当前证据 | DEV 新结果的影响 | 允许的论断与需回避的加强 |
|---|---|---|
| **RQ1：关系记忆的 Base-relative 条件价值** | **维持不变**。Twitch TEST 条件异质性、M3 TEST Base vs Memory 非本 DEV 能推翻或确认的同一检验。 | 仍可陈述 knowledge value depends on trained incumbent/history context；DEV 并未识别新的历史机制。 |
| **RQ2：候选环境改变相对价值标签** | **维持不变**。本试验没有做 candidate-set 操纵；old KuaiLive room 10,222 同事件配对依旧是 retrospective。 | 不从 D1 推导任何 candidate-number 因果结论或作者任务 replicate。 |
| **RQ3：估计相对价值指导 constrained policy** | **中等补充**。两类不同有限样本回归构造均在 DEV 上获得相近有条件选择增益。显示 decision target 可由不同实现表达；**未强化通用最优算法**。 | 与原五政策 G5 比较的独立冻结确认保持不变；D1 只说明在 post-G5 nested DEV 两方法的实证相近性/差异。 |
| **方法创新性与 KBS 差异化** | **重新归位**。Direct 优势在 SASRec 非 budget matched，GRU4Rec 近零，不能将 algorithmic superiority 作为贡献。 | 定位为 fixed transparent Memory 的 candidate-/incumbent-relative rank value、context-sensitive labeling、frozen policy evidence；引用先前 post-hoc / two-stage L2D。 |
| **部署成本与外生调用约束** | **既有风险保持**。Direct/Two-stage 都未超过 100% Memory 的 DEV 准确率；新实验没有测实耗时/业务调用成本。 | 仅在 `stipulated invocation constraint` 下报告质量；不声称 faster/in-production efficiency。 |

**学术评价：** 新试验降低了“Direct 仅凭与简单 Difficulty 对比而成立、无法面对一个明显替代估计构造”的风险。但它也表明所考察的决策功能并非对 Direct HGB 结构独有。对 KBS 原创性的净影响是**证据更稳健、独创算法定位进一步收紧**，不能据此推断量化录用概率上升。

## 4. 最近邻已发表成果的审稿解释（原始来源）

- Narasimhan et al., *Post-hoc Estimators for Learning to Defer to an Expert*, NeurIPS 2022：https://proceedings.neurips.cc/paper_files/paper/2022/hash/bc8f76d9caadd48f77025b1c889d2e2d-Abstract.html 。已研究固定 Base 后训 expert deferral、专家成本和错误概率。本试验只是 related two-regressor comparator，不是 Narasimhan 的完整算法复现。
- Mao, Mohri and Zhong, *Regression with Multi-Expert Deferral*, ICML 2024：https://proceedings.mlr.press/v235/mao24d.html 。明确覆盖双阶段训练、多个专家和有界 regression loss，进一步限制“首次提出回归专家分配”类主张。**N5 Related Work 应增加这一有直接方法碰撞的出版物。**
- Yuan et al., *Recommender System as Slow and Fast Thinkers*, arXiv:2609.02671，2026-08-10 被 CIKM 2026 接收，会议 2026-11 才举行：https://arxiv.org/abs/2609.02671 和 https://eprints.gla.ac.uk/392708/ 。已有预算控制的快慢推荐路由；此论文研究对象不同于独立固定关系专家与后验 NDCG 标签，但我们没有 full DS-Frame head-to-head。
- Elsevier [KBS 官方范围](https://shop.elsevier.com/journals/knowledge-based-systems/0950-7051)：强调原创性、知识模型及推荐/决策支持；本实验仅使 bounded empirical contribution 更可信，不自动满足强方法创新审稿要求。

## 5. 可操作的 N5–N8 修订建议 / Claim gate

**N5：必要调整**
1. 在 Learning-to-Defer Related Work 小节准确引用 Narasimhan 2022 和 Mao 2024，以及 DS-Frame 2026；并解释 already fixed expert / candidate-conditioned event NDCG 与他们主要研究问题的相同/不同。
2. 贡献写法从 “we develop a novel utility-based gate that outperforms expert routing” 收敛为 “we assess fixed relationship knowledge through incumbent- and candidate-relative ranking utility and test its predictive use for specialist selection”; 不删除原 G5 Utility 对四个特定 DEV-frozen objective 的正确比较。
3. 若提及本试验，用一句声明“a post-G5 nested development analysis compared direct utility regression with separate estimation of both rankers' utility, yielding comparable constrained selection quality, with architecture-dependent small differences”即可；**应优先位于 Supplement，而非 Introduction 的核心贡献或 Abstract**。
4. §2 应正面说明为何这不是发表过的 generic deferral target；理论等式的线性性质意味着 two-stage 与 Direct 预测相同总体对象，不得以这种不同 label decomposition 宣称“新目标”。

**N6：相关解释**
- 将本文定位为 knowledge valuation & conditional decision rather than incremental regression trick。
- 在讨论中解释两个估计方式的近似可替代性与模型架构依赖、可能来源于有限样本误差，而非新理论优势。
- 明确 Always Memory 在 M3 的 accuracy/cost 反例与 DEV only routing-call assumption 不因 D1 消失。

**N7：推荐将 D1 作为单独探索性 Supplement 小表（作者可选）**
- 保留 2 model × 2 method 的 NDCG、calls、user-cluster CI、n=50,049/12,628，明确两个主种子和 bootstrap 次数；必要时在表注写 SAS calls 不等导致比较非 budget matched。
- 不与 S8 原 G5 六拟合 TEST CI/Holm 混表，也不将 D1 加入 G5 的原三主对比。
- 若想声称 Direct 有显著额外方法价值，先加一个真实公平的相同调用-budget nested DEV 分析作为探索，再决定有无可能获得新的 independent TEST；不因 Dev-SASRec 单项区间不含零就仓促扩大实验。

**N8：必要终验**
- Re-audit NeurIPS 2022 / ICML 2024 / DS-Frame author-year-paper status; ensure bibliography verified and distinguish heuristic Uncertainty from GUIDER.
- Independent statistical reviewer: two-architecture exploratory multiple comparisons and user-level resampling; no global significance claims.
- Submission author should decide reproducibility of event-level outputs and archival permissions; temporary Actions zip ≠ permanent public record.

## 6. 决策及尚未完成事项

**决策：N5 GO; N4 and N3 no rollback.** The registered G5 scientific results stay unchanged. N5 should treat the D1 result as a robustness/alternative-explanation boundary, not a major fourth independent experiment.

**若保留 Plan A：无需立即重训六个 Base 或执行额外 TEST；不等待下一轮新实验即可进入 N5。** 若作者希望强化对成熟 deferral/DS-Frame 的算法 SOTA 主张，则本 DEV baseline 明显不充分，须回 N2 定义有公允同成本/同专家任务基准与可用的新独立 TEST，不能用已见 G5 重新调优。

**验证状态：** 本文结论已独立读取 GitHub 存档的原始 JSON 汇总并核验 SHA256；没有对私有 event-level 用户数据进行二次重算，不能证明数据本身所有历史与源权重都完全正确。统计区间来自已保存的 2,000 次 user-cluster bootstrap，不是通过访问私有逐事件数据重新估计。
