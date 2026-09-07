# 04 绩效管理：G2首批交接包

状态：已准备，未领取；当前唯一写入者为总控。不得自行切换共享目录分支或修改源码。参考基线为包含G1集成报告的最新main，接入时核对完整SHA与项目ID appgprj_6a9e2c705cfc819180e0e5251bb025cc。不是新项目，不重复搭建。

必读：README、Ownership、Shared_Contracts、Scope_Register、G1_PreAcceptance_Report、acceptance/G2、上级Execution_Checkpoint。复用现有tests/p3-api.test.mjs及foundation-scenario；C-DEF-01撤权修复不得回退。

首批范围：绩效周期→目标确认/调整→执行反馈→自评→独立评价→发布→申诉更正及本人/档案读取。当前已有部分实现，先按module-progress核对缺口。组织绩效/复杂校准、招聘外部渠道/电子签/AI等全量未纳入子功能仍保留后续，不宣布整组完成。

候选专属路径：lib/hris/performance.ts、performance-changes.ts、performance-checkins.ts；app/performance/、performance-changes/、performance-checkins/及对应API。新增测试建议tests/g2-performance*.test.mjs；新增证据docs/delivery/G2_performance_*。以上不是当前写入授权，实际以总控下一交接记录为准。

任务：核对目标权重、周期日期与组织范围；复用正式结果与历史核定区分；将同员工目标调整/版本冲突/评价独立/发布/申诉更正串成场景；验证调动/离职/停用后当前权限及旧版本不冒充最新结果。

共享保留：development.ts、公共context/授权/持久化、migrations、主数据model、报表/壳与托管、tests/p3-api.test.mjs、runtime；变更先提交兼容方案，由总控统一处理。尤其招聘hire涉及核心员工原子写入，不能另写平行员工存储。接口继续revision和当前组织范围；无新迁移计划，确切需求出现后总控编号。

输出：需求/开发/测试/生产四维状态，规则来源与未知项，具体缺陷及修复证据，模块提交SHA与交还说明。自动化通过不代签G2业务验收。G1界面阻塞不影响本包只读盘点、方案与测试设计；编码需明确交接。单写模式未解除，不自动开代理。

启动提示词：

```text
请读取本G2工作包和最新总控文件，先只读核对当前代码、接口与已实现范围，整理首批剩余需求和组合验收场景，不重新搭建。当前尚未交接写入职责，不修改共享工作区。总控明确交接后直接按允许路径持续完成开发/必要测试，保留现有权限与C-DEF-01回归。原系统只读、仅合成测试数据；提交后交付完整SHA、证据和遗留项，统一由总控合并/发布。
```
