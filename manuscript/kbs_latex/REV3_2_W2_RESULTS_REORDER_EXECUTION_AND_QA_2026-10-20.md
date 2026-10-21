# Rev3.2 W2 — Results 主线重排与技术核查

**2026-10-20 | EDIT_APPLIED / STATIC EXACT-TABLE EQUALITY PASS / FINAL DUAL-PDF QA PENDING.**

## 1. 当前 W2 科学源

- \`main.tex\` 编辑 commit \`9e1e5d68ad920a2642294e16c43a1cacfe1ebd27\`；更新后 blob \`2cc59f4ca166f0777313630ed2cc6cffa6897196\`。
- 基准 frozen science commit \`a686cd07ce80f8d4090aae720c0e583f39f73176\`；历史 Rev3.0 C7/C8V dual PDFs SUCCESS，但**不能替代新源 PDF QA**。
- 同步科学安全门结构迁移的 commits：C6 \`54114ffc333cd2794a70421958041051fe32b9a6\`、C8V semantic \`3bd31f976550e363faa41e60c24c0f870d800c4f\`、C7 workflow \`278cb261eb42f13b828d7e90cc15812f924204a6\`、C8V workflow \`2dc0e5fd559ff2c1c76f00d33de0633885fc656e\`。
- 未改 \`main.tex\` Results 前、Discussion 后的全部文本；未改 \`kbs_references.bib\`、Supplement、Highlights、模型或数据；仅 W2 结果段落重排与衔接句有变。

## 2. 新六小节论证顺序（非新增实验）
1. RQ1：已有 Twitch、KuaiLive room 同一批事件历史/候选条件性价值，带出标签监管问题。
2. RQ2：紧跟直接说明同采集期**额外 30,000 事件** F-supervised vs 原 uncorrected S-supervised完整冻结政策全F NDCG，H1表原样保留、call数原样保留，F/S未严格同调用。
3. How Supervision Reallocates Historical Knowledge Calls：**已有**50,049 DEV的G2 switch/Full-only/S-only分析单独成节，而非新的H1机制中介或独立TEST。
4. Frozen Base-Relative Selection Across Tasks and Incumbents：原 Twitch 44,221 TEST 和 M3 47,575 TEST（six fits shared cohort）的Utility-vs-comparators原表原样后置；Twitch DEV feature ablation从G2拆出，归为辅助证据。
5. RQ3：原4096嵌套H2真实关系对closed-hour等 composite null 仍独立并行，与RQ2不构成因果中介。
6. Operational Conditions：原DEV quota、Always Memory无约束更准及测得旧pointwise Utility延迟更高作为应用条件。

## 3. 静态科学完整性预检查（已执行，范围如实限定）

GitHub更新前在同一源码文本上逐一检查：**主文9个\`table\`环境（其中Results原7张）文字逐字符未改变**；Results Twitch \`fig:results-evidence-states\` 原图source完整不变；正文所引用的关键负面事实句 \`not an experimentally isolated equal-resource effect\` 仍保留；新全文全部LaTeX labels无重复；Results恰好六小节，H1 table源位置早于Twitch/M3原先对照表；Results以外文本未改。源代码数字并未重新估算，CI尚未证明最终版PDF可读。

### 既有守卫为何需要修订

原 C6/C7/C8V 误把**固定四个Results小节旧叙事**作为固定科研真相，W2批准的顺序是六节，故精确修改 C6 的\`subs\`列表，并增加H1在旧Twitch表之前的结构断言；两个workflow相应调整要求的标题；C8V semantic仅将\`r2\`提取范围从旧RQ2→RQ3缩小到 RQ2→原始选择器节结尾，以同时覆盖H1+G2，不把5.4计算成该policy-change比较。**其他全部公式、历史列、数值、Calls、样本、先例及超额claim守卫仍在，并未关闭审计。**

## 4. 当前新建的真实工作流（运行结果不提前宣告）

- [C7 #39429571240](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39429571240) — W2调整后结构守卫分支commit \`278cb261...\`；记录本文件时 PENDING。
- [C8V #39429583687](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39429583687) — W2最终守卫分支commit \`2dc0e5fd...\`；记录本文件时 PENDING。
- 中间守卫提交的部分CI因concurrency被cancelled；不将CANCELLED视为失败或SUCCESS。后续需以**最新完整源码和审计文件**相同SHA重新核对C7/C8V jobs、引用/公式和两份PDF真实工件。
- 若后续CI在 \`n12_c6_scientific_contract.py\`、\`n12_c8v_scientific_semantics_audit.py\`的冻结科学守卫失败，不得为求绿色静默关停；按最小科学source变更与相容性修复逐项核查。

## 5. 编辑质量与下一阶段门槛

W2更改是**证据展示次序**和少量标题、段落衔接：不代表更有效corrected-S已经实验，无法宣称新增KBS原创新发现。后续优先阅读编译PDF中的Results：H1是否在RQ1后不远处清晰展示、两张旧selection表是否被后置、G2的DEV性质及H2 parallel事实是否仍醒目，绝不可用机器数字守卫替代人类实际通篇连贯性评估。

**W2状态**：source edit complete, static numeric/table preservation PASS, final C7/C8V+PDF inspection NOT YET VERIFIED。W3尚未开始；NI-1g NO-GO、原G5/H1已揭盲、PR #6 Draft、KBS Author signoff PENDING。
