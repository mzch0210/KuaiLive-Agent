# N12 Rev2.2-R1 E4 | 唯一科学措辞修订与源差异记录

**2026-10-20｜E4-L1 SCIENTIFIC_MICROEDIT_COMPLETE / E5_CI_PENDING。** E2 已裁定 RQ2 不需正文增补；E3 已裁定 C1/C2/C4 原文充分且 C3 图内措辞有一处范围过强。本 E4 只按 E3 授权修改一个 TikZ Figure 1 节点，不重新写论证或修改冻表。

- 分支：`kbs-n12-single-thesis-restructure-plan-20261014`
- E3 审计文件：`N12_C8V_REV2_2_E3_RESIDUAL_RISK_AND_CLAIM_SCOPE_2026-10-20.md`，审计提交 `d09fc3ed2df6e001341e7879be1f0d88a6c82bd5`
- E4 科学源码提交：`8f6d7bd4756536c1e4079ba498bd1b6e92e6e98b`
- `main.tex` Git blob：`c713811acf5c6c47df3e5cb34ee8a7af5cc4ff5e` → `71eae8475db4730951ff3c78971e14104a7ee515`
- 修改前正文锚点：Figure 1（`fig:knowledge-value-chain`）、RQ3 branch node，原第 74 行。

```diff
- Authentic history versus valid historical nulls};
+ Authentic history versus constrained historical randomizations};
```

**理由**：H2 同 4,096 事件的三个 Null 保留时间/作者活跃/closed-hour 等实际约束，但原 TRAIN-only Popularity margin 的 cohort-specific prereveal 验收 **NOT VERIFIED**。图内 `valid` 易被读成全部原定验收通过；`constrained historical randomizations` 准确陈述已实现随机化性质，而不冒充补过原始事前子门槛。

**没有修改**：Abstract、Introduction contributions、Methods、RQ2、RQ3 Results 表、正文 Figure caption、Discussion、Conclusion、Highlights、BibTeX、S1–S10、任何统计数值或 CI、任何训练/DEV/TEST 数据、模型、样本、threshold。E2 主文本 L0 判断保持有效，E3 C1/C2/C4 不重复补充限制。保留 Always Memory 不受限更准与旧 gate 更慢、H1 F/S calls 不等、corrected-S 未跑、RQ3 复合扰动等负面边界。

**E5 不得提前宣布 PASS**：该 `main.tex` 推送应触发 N12 C8V/C7 双 PDF 构建工作流，须检查所有实际新 head SHA 相关成功状态、运行 ID、主文和 supplement 工件以及人工必要的图文审核。若因图框溢出或 CI 合法保护而失败，先查实际 logs，不能删除语义守卫或退回不准确措辞。更新此 E4 记录只是文档提交，不作为 E5 新科学源版本。

**E4 判定**：PASS_ONE_L1_EDIT / NO_NEW_RESULTS / HANDOFF_E5。外部真实人审及责任作者最终决定 PENDING，KBS 未投稿。
