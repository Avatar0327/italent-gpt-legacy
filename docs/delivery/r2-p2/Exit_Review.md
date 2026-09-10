# R2 P2退出评审材料

结论：001至004已完成设计定向返修，提请独立窗口复核。原独立评审结论“不通过”未被本窗口撤销；只有复核接受后再交所有者决定P2退出。005/006继续open_future_responsibility；所有者尚未批准，本窗口没有进入R2 P3。

进入授权`R2-P1-P2-TRANSITION-20260910`；main启动与最终只读核验均为`22be3a7e366d6787180d4f593a30f5984c70e03a`，干净；R1共享设计固定`e15237281ff19f04f08a354fd9455c518b24ae47`。P1仍0/15完整通过、15/15受限关闭，未提升任何实现/业务/生产验收。

|顺序|模块|P2材料状态|原模块验收ID数|
|---:|---|---|---:|
|1|M37 人才标准|设计闭环|12|
|2|M06 任职资格|设计闭环|13|
|3|M26 360度评估|设计闭环|12|
|4|M18 在线盘点|设计闭环|13|
|5|M17 继任与发展|设计闭环|14|
|6|M03 干部管理2.0|设计闭环|14|

共用架构沿R1身份/权限/CAS/审批/恢复，不重复建引擎。跨域保留M37精确版本；资格与任用决定分开；M26匿名/受众/差分/撤权；M18会议及发布快照；M17成员/任期/IDP和分母；M03审批与M01实际生效及敏感档案；历史ID、旧版本消费者及未知来源不被覆盖或伪造。

## 评审取件

- [总体架构](Architecture.md)、[跨模块契约](Cross_Module_Contracts.md)、[权限及敏感数据](Permissions.md)、[接口及异常](Interfaces.md)。
- [M37](M37_Design.md)、[M06](M06_Design.md)、[M26](M26_Design.md)、[M18](M18_Design.md)、[M17](M17_Design.md)、[M03](M03_Design.md)、[六基础差异](Foundations.md)。
- [迁移/回滚](Migration_Rollback.md)、[恢复/成本/责任](Recovery_Cost_Responsibilities.md)。
- [需求追踪](Traceability.md)、[P3交接建议](P3_Handoff.md)、[LIMIT责任](Limit_Resolution.md)。
- [第一轮自检](Review_Round1.md)、[第二轮反查](Review_Round2.md)、[恢复检查点](Resume.md)。

精确结构化数据：Requirements_Trace.json、Acceptance_Scenarios.json、P3_Work_Packages.json、Original_Limits.json、Limit_Resolution.json、Legacy_Acceptance_Map.json、Source_Requests.json、Interface_Schemas.json、Command_Registry.json、Source_Manifest.json和Artifact_Manifest.json。核心文件hash清单排除自身和evidence输出，避免循环hash；每单元证据应在所属提交读取对应manifest，不能用当前manifest比旧检查。

## 数量和剩余责任

33项批准需求、295条拆分条款、149项契约字段/角色/状态、24内部关闭项；78模块+16基础批准AC，另17历史AC、5历史父任务/criterion。46个P3任务建议、138个未执行GWT（78+16+44补充），场景跨引用不重复计数。1个原站IDP历史查询转来源请求，不作为P3运行场景。

原6组LIMIT完整关闭0；6组均有P3和P4剩余责任，两项计数相互重叠。52个责任子项中P2设计关闭15、转P3验证25、转P4核证/验收12。设计关闭不表示原站/实现已验证，基础运行依赖不混入6组分母。

7个结构化补证请求（六模块各1、平台能力1）均为request_only，未发送或执行。平台官方备份/恢复/调度、独立安全账本与密钥的实际能力尚未本轮验证；A方案需求/预算/公式及备选设计完整，保持RPO≤60分钟、RTO≤240分钟和30天，不宣称达标。若P3证明A/B不满足且需新增显著成本，量化后由所有者决定；本轮没有证据要求提前新选择。

P3强闸门：R1共享契约实际版本可用；规范化对象/严格schema/服务端权限/原子事务/完整日志与回执；合成边界、乱序、撤权、未知/对账和迁移隔离证据。P4强闸门：真实来源映射、多角色/隐私用途、容量/成本、可信当前权限与完整恢复计时/保留验证、所有者生产开放。相关证据缺失只能保持对应对象/功能受限，不默示通过。

## 所有者最小待办及执行声明

新增业务/架构/成本决定0项。后续先由独立窗口定向复核，再请所有者审阅具体包并独立决定R2 P2退出；R2 P3需另行明确准入，不能由本建议自动启动。总控仅收到结构化登记提案，本窗口未修改Scope、总控状态或项目看板。

产品修改0、数据库迁移0、P3业务测试0、部署0、真实员工/测评/签署/通知/支付/税务操作0、访问者增加0、浏览器/CDP0、子代理0。没有merge/cherry-pick/rebase/reset/强推；main/P1/R1 P2/P3/R3工作树无本窗口文件修改。仅曾把自建文档生成脚本误写到拼写错误的空目录，已移回本目录并删除误建空目录，未触及其他工作树或产品。

## 定向返修复核包

[Repair_Record.json](Repair_Record.json)固定独立评审bd976480全文来源。001见[Contract_Repair.md](Contract_Repair.md)及34个schema文档实例（9合法/25拒绝）；002见[Anonymity_Repair.md](Anonymity_Repair.md)及16组逐格手算（5发布/11抑制）；003见[Foundation_Adaptations.md](Foundation_Adaptations.md)；004见[Task_Dependencies.md](Task_Dependencies.md)：46任务、55完整节点、165边、无环。以上均是文档/符号检查，138场景全部not_run，实施通过数0。

LIMIT原15项P2标签中，独立评审此前只接受9项；本轮对M37.01、M06.01、M26.01/.02、M18.01/.02提供精确schema/探针/版本哈希证明，重新提请6项设计关闭，15是设计方提案，独立新签收尚无。25项P3、12项P4逐字段保持原责任，原6组完整关闭仍0。

新两轮整体复核见Repair_Review_Round1.md和Repair_Review_Round2.md；原Review_Round1/2作为被审历史记录保留，不用其旧结论替代本轮返修复核。原11笔提交保留，本轮全部提交及固定内容/包装引用见Git及Repair_Delivery_Record.json（包装时生成）。
