# R1 P2退出评审包

状态：待两轮整体自检完成后提交独立评审。P2退出未批准，P3未开始。

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

[LIMIT矩阵](R1_P2_Limit_Resolution.md)按主要关闭闸门分解37行：M01 3/5/2，M19 2/5/2，M48 2/4/2，M32 2/6/2（依次P2设计处理/P3验证/P4验收）。四个LIMIT本体没有在本分支解除。

[需求设计追踪](R1_P2_Traceability.md)覆盖70个明确需求ID；[85项原批准验收映射](R1_P2_Approved_Acceptance_Trace.md)保留原文和已批覆盖关系；[21数据集254字段](R1_P2_Report_Field_Dictionary.md)及[一致性补充](R1_P2_Consistency_Resolutions.md)补齐类型/状态。所有P3/P4用例未执行，历史测试复验数0。

[P3任务建议](R1_P2_P3_Work_Packages.md)包括11个按依赖排列任务。[总控结构化提案](R1_P2_Controller_Proposal.json)只建议纳入材料与残余任务引用，没有回写Scope或建立第二个范围事实源。

## 真实依赖与所有者决定

[依赖/决策队列](R1_P2_Dependencies_Decisions.md)逐项指定责任和闸门。原站补证13项交P1窗口统一处理；供应商、真实R2/R3联调、真人多角色、平台恢复/调度/独立安全存储都不能冒称完成。它们不阻静态设计交付，但阻相应P3运行或P4验收。当前新增实质业务决定0；如恢复能力/实际成本触发重大差额，按08量化方案提交所有者，不降低目标。

## 独立评审决定栏

评审对象：最终推送设计提交及本包。请独立评审记录评审人、时间、完整SHA、意见、受限项接受边界、补正项与是否批准P2退出。未收到明确批准前，任何P3开发/迁移/测试/部署均不由本包授权。

本执行窗口只提出“具备提交评审条件”的材料就绪判断，不代作批准。两轮自检与修正记录见[R1_P2_Self_Review.md](R1_P2_Self_Review.md)，实际提交推送见[R1_P2_Git_Record.md](R1_P2_Git_Record.md)。
