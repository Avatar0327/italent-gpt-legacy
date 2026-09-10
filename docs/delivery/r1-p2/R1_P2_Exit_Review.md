# R1 P2退出评审包

状态：R1 P2设计阶段通过，带明确后续验证和验收责任。批准来源：项目所有者通过本次消息批准。R1已具备转入P3交接准备的条件；P3尚未开始。

批准绑定审阅提交`65cfcf85e4fccf8cba53319deb7b87dd7f79600a`及本文件审阅前SHA256 `e88a0fdbe89efbca2b497b225df54cebb0a114509564b509d3de4cbbfb7c4d07`；先在该干净提交复跑指定检查，无错误后登记。见[所有者批准记录](R1_P2_Owner_Exit_Approval.md)。当前文件仅更新收口状态，九项设计正文及任务/用例保持已审阅版本。正文内历史待评审状态不再作为当前阶段判断。

## 评审范围与来源

R1仅M01/M19/M48/M32及BASE-01至06。启动main快照`716cd9df5f5776d050f77f57c2ad5a35c0a83882`，设计分支`design/r1-p2-20260909`。P1主线已继续R2，本包不修改其主事实源、不回退其HEAD；输入hash见[来源清单](R1_P2_Source_Manifest.json)。四模块P1受限通过及转序批准保持。

## 九项设计交付

|任务|设计文件|
|---|---|
|R1-P2-01|[R1_P2_Architecture.md](R1_P2_Architecture.md)|
|R1-P2-02|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|
|R1-P2-03|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|
|R1-P2-04|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|
|R1-P2-05|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|
|R1-P2-06|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|
|R1-P2-07|[R1_P2_Migration_Rollback.md](R1_P2_Migration_Rollback.md)|
|R1-P2-08|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|
|R1-P2-09|[R1_P2_Review_Design.md](R1_P2_Review_Design.md)|

## P2硬门槛设计证据

|门槛|设计处理|文件|后续验证|
|---|---|---|---|
|HG01|稳定ID/版本/有效期/历史不可覆盖|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-01, P3-MIG-01|
|HG02|多任职/再入职/法人合同/编制关系|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-02, P3-M01-03, P3-M01-07|
|HG03|审批/生效/通知状态分离|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-07, P3-INT-03|
|HG04|模板冻结/无路由拒绝|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01|
|HG05|管理/委托/节点审批三权分离|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-06|
|HG06|本人/直线/虚线/部门关系|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-01, P3-M48-02|
|HG07|对象/动作/范围/字段/历史交集|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-02, P3-M32-05|
|HG08|read/export/subscribe/manage分别授权|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-05, P3-M32-08|
|HG09|粒度/分子分母/null/去重/时间|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01, P3-M32-02, P3-M32-03|
|HG10|有界分页/异步导出/快照/订阅幂等|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-06, P3-M32-08|
|HG11|内外部ID/eventId/revision/digest/correlationId|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-01, P3-INT-02|
|HG12|业务失败/并发/不可写/未知分别恢复|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-M01-05, P3-INT-02|
|HG13|增量/旧字段/未知历史/回滚/重复执行|[R1_P2_Migration_Rollback.md](R1_P2_Migration_Rollback.md)|P3-MIG-01, P3-MIG-02, P3-MIG-06|
|HG14|DB附件共同点/撤权/隔离开放|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|P3-REC-01, P3-REC-02, P4-REC-06|
|HG15|RPO/RTO/30天可行性/成本/责任|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|P3-REC-04, P3-REC-05, P4-REC-06|

## LIMIT、追踪与接续

[LIMIT矩阵](R1_P2_Limit_Resolution.md)按主要关闭闸门分解37行：M01 3/5/2，M19 2/5/2，M48 2/4/2，M32 2/6/2（依次所有者关闭设计问题/P3验证/P4验收；合计9/20/8）。四个LIMIT本体没有在本分支解除。

[需求设计追踪](R1_P2_Traceability.md)覆盖70个明确需求ID；[85项原批准验收映射](R1_P2_Approved_Acceptance_Trace.md)保留原文和已批覆盖关系；[21数据集254字段](R1_P2_Report_Field_Dictionary.md)及[一致性补充](R1_P2_Consistency_Resolutions.md)补齐类型/状态。所有P3/P4用例未执行，历史测试复验数0。

[P3任务建议](R1_P2_P3_Work_Packages.md)包括11个按依赖排列任务，现形成[正式交接](R1_P2_P3_Handoff.md)及[新窗口启动提示词](R1_P2_P3_Start_Prompt.md)。交接就绪不表示本轮启动P3。[总控结构化提案](R1_P2_Controller_Proposal.json)只建议纳入材料与残余任务引用，没有回写Scope或建立第二个范围事实源。

## 真实依赖与所有者决定

[依赖/决策队列](R1_P2_Dependencies_Decisions.md)逐项指定责任和闸门。原站补证13项交P1窗口统一处理；供应商、真实R2/R3联调、真人多角色、平台恢复/调度/独立安全存储都不能冒称完成。它们不阻静态设计交付，但阻相应P3运行或P4验收。当前新增实质业务决定0；如恢复能力/实际成本触发重大差额，按08量化方案提交所有者，不降低目标。

## 所有者退出决定

项目所有者通过本次消息批准：R1 P2设计阶段通过，带明确后续验证和验收责任；R1已具备转入P3交接准备的条件；P3尚未开始。批准条件由已审阅干净提交上运行的文档检查满足。不是执行窗口自行批准，也不是第三方独立审计或生产验收。

37项风险中9项设计问题经所有者审查关闭，20项转P3运行验证、8项转P4独立业务/权限/生产验收；原站13项补证由P1总控统一处理。平台能力、生产者、供应商、真人角色及生产恢复责任不解除。业务测试及历史测试复验均为0；不能将设计检查计作运行测试。P2批准不构成部署、生产操作、真实外发或新增访问者授权。

[批准记录与原始检查结果](R1_P2_Owner_Exit_Approval.json)保存审阅SHA及来源；[两轮历史自检](R1_P2_Self_Review.md)保留当时事实；[收口核验](R1_P2_Closure_Verification.json)保存本次文档核对结果；[Git交付记录](R1_P2_Git_Record.md)登记提交推送。唯一主事实源由P1总控按提案纳入，本分支未回写。

## 实现差异与复用汇总

以下均基于来源清单与各设计文件记录的文件hash，不是现实现符合批准需求的声明。

|任务|可复用|待修改|待新增|受限|
|---|---|---|---|---|
|01|Sites/Vinext、D1/R2、CAS|全量装载/授权修订|有界任务、统一命令及投影|托管后台能力未证|
|02|原ID、目录校验、人事审批|单org/job、立即退出、旧续签条件|有效版本、多任职、法人、子集模板|原站终态/真人权限|
|03|原D7链、事务及待办|原单/实例状态投影|路由/会签/委托/管理事件|真人独立性/外域补偿|
|04|服务端成员与可见范围|角色混用、缓存与任务分类|七契约、关系/字段动作矩阵|真实生产者联调|
|05|21数据集原列、CSV安全|内存分页、发布时间链、权限裁剪列映射|字段定义、快照、job/订阅|容量与真实发送|
|06|预检schema/摘要、HTTP界限|错误分类与未知恢复|命令/inbox/outbox/回执|供应商未配置|
|07|旧JSON和规范化结构语义|旧全量迁移与兼容写入口|有界staging、映射/批次/fence|实际schema/大小/历史核证|
|08|原恢复清单/17项历史夹具思路|历史静止小数据演练|一致增量备份、安全来源/加密/隔离开放|实际平台能力/容量及值班|
|09|P1批准/范围/历史证据|追踪语义与文档一致性|评审包/原AC映射/结构化提案|P2所有者决定已登记；P3/P4运行与验收仍未完成|
