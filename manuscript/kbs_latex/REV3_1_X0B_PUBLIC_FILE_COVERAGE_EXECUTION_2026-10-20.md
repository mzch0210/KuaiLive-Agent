# Rev3.1 X0-B — KuaiRec 真实文件级元数据审计执行记录

**2026-10-20 | PUBLIC DATA AUDIT LAUNCHED / REAL AGGREGATE RESULTS PENDING / X1 AND X2 HOLD.**

## 已完成的实际工作

1. 联网核查官方 KuaiRec README 的版本、下载源、small/big 矩阵和 item_daily_features 字段（https://github.com/chongminggao/KuaiRec, https://zenodo.org/records/18164998），确认`user_id`/`video_id`/`date`/`timestamp`与daily `author_id`/`upload_dt`等字段；官方用户/视频/反馈密度数据不等于本仓库实际复算。
2. 创建公开数据文件审计脚本 `analysis/kbs_plan_c/rev31_x0b_kuairec_coverage_only.py`，**仅读取元数据列**、不读取watch_ratio等监督标签，也不训练任何Base/Memory或执行旧M3 TEST。审计指标：small/big真实用户交集、small用户中存在更早big作者关系历史的覆盖率、视频作者/上传时间映射、small pair密度及重复、上传日期与观测时间的一致性、daily metadata多版本冲突率、时序可能泄漏的区域。
3. GitHub Actions `.github/workflows/kbs-n12-rev31-x0b-kuairec-metadata-audit.yml` 对应新run [#39409500462](https://github.com/mzch0210/KuaiLive-Agent/actions/runs/39409500462)，科学审计代码 SHA起点 a0441aade845...，workflows commit `45934fd50d7dfba5efdc28ba01134683fe3f0286`；本文件写入时run **IN_PROGRESS**。没有拿到最终聚合JSON前不得写`REAL_DATA_PASS`。
4. 首次本地通过Python直接联Zenodo失败：container的网络DNS不可用；因此转用有网络的 GitHub runner。必须从官方Zenodo record API `files[].checksum` 获取 MD5，并与下载ZIP完整文件校验，不使用未核实的静态MD5字面值，未取到可信官方checksum立即停止。
5. Workflow只上传`x0b_metadata_aggregates.json`，原始用户ID、原始日志、ZIP或未经许可派生关系边**绝不上传 artifacts**。ZIP仍仅在runner临时盘，用户文件路径不外传。

## 结果尚未允许推断的事项

- 尚未完成：真实ZIP通过MD5、CSV能完全解析、完整`small/big`用户交集、实际pre-first-small历史支持、作者映射一致性、历史时间戳与视频发行有效性、反馈缺失是否能区分被屏蔽作者、数据版权/作者许可。
- X0仅评价**元数据覆盖**；数据的“观看反馈来自谁、何时观测”不等于可用来提供真正的完整在线决策真值。`small_matrix`近完整是事后离线代理；`item_daily_features`同日聚合不能无条件作为当天早期决策Z。
- 本报告X0-B不评价 KuaiRand随机曝光propensity/ESS；这一项仍独立HOLD，不能以KuaiRec通过代替KuaiRand也通过。
- RecSys 2025已利用KuaiRec近完整矩阵研究日志/曝光/采样策略对**模型排名比较**的影响。即使X0B数据显示关系历史充足，也只有**历史Memory调用政策的固定资源完整反馈决策损失**这种可严格区分的估计量才可能成为候选新增科研对象，仍需与deferral先例逐项去重。

## 执行裁决

**X0-B REAL FILE COVERAGE = RUNNING/NOT YET VERIFIED; X0 OVERALL HOLD; X1/X2 NOT AUTHORIZED; REV3.0 P5 AUTHOR GO/REDIRECT/HOLD仍独立可决定。**

后续若本runner success，应读取 job logs 和仅聚合 artifact JSON，按实际统计对历史覆盖/上传日期/用户交集给明确PASS、FAIL或CONDITIONAL，发现代码统计或字段假设错误则修正并重新精确验证；即使SUCCESS也不代表原创性PASS。如果run失败，必须记录下载/MD5/schema/内存或计算失败的实际job step，不能硬编覆盖统计，也不能以旧README数字代替测量。

不修改 `manuscript/kbs_latex/main.tex`、Supplement、`kbs_references.bib`或既有G5/H1/Rev3.0科学结果。
