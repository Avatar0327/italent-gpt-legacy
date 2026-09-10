# R2 P2设计与交接

设计基线：`22be3a7e366d6787180d4f593a30f5984c70e03a`，进入授权：`R2-P1-P2-TRANSITION-20260910`。本目录是独立设计分支的交付物，不维护Scope、总控看板或正式阶段批准。P1为15/15受限关闭、0/15完整通过；本包不能提升为P2退出、P3测试、P4业务或生产验收通过。

顺序：共用架构 → M37 → M06 → M26 → M18 → M17 → M03 → 六项非模块基础差异 → 两轮整体复核。实际完成单元见`Design_Checkpoint.json`；未完成单元不作为可用设计承诺。

## 设计入口

- [总体架构](Architecture.md)：对象、版本、审批、生效和R1依赖。
- [权限与敏感数据](Permissions.md)：行、列、动作、回避及匿名隔离。
- [接口与异常](Interfaces.md)：命令、事件、签名、unknown和对账。
- [跨模块契约](Cross_Module_Contracts.md)：生产者决定权和旧消费者兼容。
- [迁移与回滚](Migration_Rollback.md)：保持原ID、隔离冲突、不伪造历史。
- [恢复、成本和责任](Recovery_Cost_Responsibilities.md)：60分钟/240分钟/30天及能力闸门。

六模块、基础差异及两轮自检已经完成。完整取件见[退出评审材料](Exit_Review.md)、[需求追踪](Traceability.md)、[P3任务建议](P3_Handoff.md)、[LIMIT责任](Limit_Resolution.md)及[恢复检查点](Resume.md)。结构化总控提案为`Controller_Proposal.json`，未写入Scope或看板。`Source_Manifest.json`固定实际Git对象及SHA256；`Requirements_Trace.json`是基于冻结Scope的只读设计映射，源字段中的历史“未批准”措辞须结合该源的当前批准记录解释，不能重新要求批准。

[完整设计提交及同步记录](Commit_Register.md)保留10个设计提交；另有最终交接提交固定该清单和提案，完整传输HEAD以Git分支及最终回交为准。

## 本轮执行边界

只写本分支本目录。未运行产品代码、P3业务测试、数据库迁移、恢复演练、部署、真实服务或原站浏览器；未新增访问者或启动子代理。文档检查仅验证设计材料、引用、哈希、范围和计数，不证明设计已实现。历史测试各保留原HEAD与时间，不记本轮复验。

设计采用R1已批准共享契约，固定读取`e15237281ff19f04f08a354fd9455c518b24ae47`的`docs/delivery/r1-p2/`对象；R1 P3实际可用性仍需后续联合交接验证。本包不修改R1设计或实现。
