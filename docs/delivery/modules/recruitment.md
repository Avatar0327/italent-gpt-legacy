# 05 招聘管理：G2首批交接包

状态：已准备，未领取；当前唯一写入者为总控。不得自行切换共享目录分支或修改源码。参考基线为包含G1集成报告的最新main，接入时核对完整SHA与项目ID appgprj_6a9e2c705cfc819180e0e5251bb025cc。不是新项目，不重复搭建。

必读：README、Ownership、Shared_Contracts、Scope_Register、G1_PreAcceptance_Report、acceptance/G2、上级Execution_Checkpoint。复用现有tests/p3-api.test.mjs及foundation-scenario；C-DEF-01撤权修复不得回退。

首批范围：需求修订审批→候选人→面试→录用退回/批准/接受→原子入职→员工档案与历史。当前已有部分实现，先按module-progress核对缺口。组织绩效/复杂校准、招聘外部渠道/电子签/AI等全量未纳入子功能仍保留后续，不宣布整组完成。

候选专属路径：lib/hris/recruitment.ts；app/recruitment/、app/api/recruitment/。新增测试建议tests/g2-recruitment*.test.mjs；新增证据docs/delivery/G2_recruitment_*。以上不是当前写入授权，实际以总控下一交接记录为准。

任务：核对岗位/编制/组织依赖；同一候选人串通需求审批、面试、录用版本退回及再次批准、接受、入职；重放hire不得重复建档，事务失败不得留下部分员工/历史；调动和停用后的办理范围重新校验。

共享保留：development.ts、公共context/授权/持久化、migrations、主数据model、报表/壳与托管、tests/p3-api.test.mjs、runtime；变更先提交兼容方案，由总控统一处理。尤其招聘hire涉及核心员工原子写入，不能另写平行员工存储。接口继续revision和当前组织范围；无新迁移计划，确切需求出现后总控编号。

输出：需求/开发/测试/生产四维状态，规则来源与未知项，具体缺陷及修复证据，模块提交SHA与交还说明。自动化通过不代签G2业务验收。G1界面阻塞不影响本包只读盘点、方案与测试设计；编码需明确交接。单写模式未解除，不自动开代理。

启动提示词：

```text
请读取本G2工作包和最新总控文件，先只读核对当前代码、接口与已实现范围，整理首批剩余需求和组合验收场景，不重新搭建。当前尚未交接写入职责，不修改共享工作区。总控明确交接后直接按允许路径持续完成开发/必要测试，保留现有权限与C-DEF-01回归。原系统只读、仅合成测试数据；提交后交付完整SHA、证据和遗留项，统一由总控合并/发布。
```
