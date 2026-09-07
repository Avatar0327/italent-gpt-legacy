# 公共接口契约 SC-1

基于本轮核查代码记录现状，不声明新增服务。变更必须附版本、调用方影响和兼容处理，由总控唯一合并。

| 契约 | 现有实现 | 必须保留的约束 |
|---|---|---|
| 身份和租户 | context.ts / authorization.ts / repository.ts | tenantId来自已认证成员；客户端不能指定他人租户；成员停用拦截 |
| 主数据 | model.ts 的 State/Employee/Org/Position/Grade | employeeId/orgId/positionId/gradeId用内部ID；姓名/工号不可作为跨模块关系键 |
| 读取 | developmentContext、visibleDevelopment、projectRecord | 按当前角色/组织/字段过滤；不能直接将完整records返回客户端 |
| 写入 | POST /api/development {revision,command} | 当前修订号；返回{id,revision}，批量派课返回{ids,count,revision} |
| 一致性 | readConsistent / commitExtension | 修订变化409；业务、历史与审计共同事务；冲突刷新后显式重新提交，不盲目重试 |
| 多记录 | saveDevelopmentMany | 最多20条、唯一ID、一修订原子提交；不拆成部分成功 |
| 历史 | GET /api/development?id=ID&page=N | 当前权限再校验；分页；保留原始事件快照；历史不增加当前权限 |
| 错误 | http.ts | {error:string}；401未登录、403拒绝、400格式、409冲突、413大小、415类型、503未分类失败 |
| 请求 | readBody | 同源Origin、application/json、最大32768字节；不绕过统一处理 |
| 时间 | business-time.ts及领域现有函数 | 保持北京时间业务日期；事件UTC时间；不混用浏览器本地时区 |
| 附件 | /api/attachments | 服务端读取R2、元数据权限和下载后修订检查；不分享原始存储地址 |

## 人才—学习既有链路

1. 发展计划 kind=plan，employeeId 关联员工，referenceId 关联能力标准版本。
2. enroll 命令使用 employeeId/courseId/due，可选planId/trainingId。planId必须属于同一员工、状态active或returned；课程referenceId必须等于计划referenceId。课程必须published。
3. enrollment.referenceId是课程版本ID；payload.planId是计划ID，payload.trainingId是培训项目ID；不能互换，也不能用模糊名称关联。
4. 已有同员工/课程版本记录时拒绝再次enroll；取消后恢复使用restoreEnrollment并保留原任务和考试次数。历史跨项目复用尚未实现，不能视为接口能力。
5. submitLearning要求通过关联考试；verifyLearning须独立核验，接受前检查强制出勤；完成状态completed。verifyPlan接受前检查关联未完成且未取消的学习任务。
6. cadreProfile通过当前可见records聚合plans和learning。回流是读取现有权威记录，不另复制完成标记；不自动升级资格或职级。
7. 学分使用既有learning-credits接口，不把档案展示触发当成授予事件；来源与去重规则继续以领域代码为准。

共享热点：development.ts、app/api/development/route.ts、development-repository.ts被人才和学习共同使用，只能由当前总控/被明确交接的基础负责人单写。没有消息总线、跨服务事件系统或新自动派课协议，不为本批增建。

下一步：基础F-G0-02把以上契约逐项映射现有测试；模块只补确切缺口。任何新字段先记录请求/响应示例、旧数据处理、权限和消费者，再由总控合入。


## H001证据澄清（不改变SC-1业务语义）

逐项代码/测试映射见[G0_Evidence_Map.md](G0_Evidence_Map.md)，合成场景见[G1_Foundation_Plan.md](G1_Foundation_Plan.md)。本轮新增5项测试，连同既有109项共114/114通过。

- 历史page从1开始，每页20项，以第21项判断hasMore；原事件快照经过当前权限投影才返回。
- 未授权人员读取草稿课程或其他不可见记录可能先收到403；可见记录的状态/关联错误为400。业务校验发生在保存CAS之前，不将409描述为所有错误请求的固定优先结果。
- 计划允许active/returned状态派课；submitted/completed/cancelled不允许。课程同code不代表同版本，必须比较referenceId内部ID。
- 盘点与计划目前共享employeeId，计划referenceId指向能力标准；没有已实现的reviewId外键或自动计划生成协议。
- 本轮仅澄清现状并补证据，未改变公共请求/响应、领域规则或旧数据，不要求消费者迁移。

## H002 干部实例与待决议项（不改变SC-1）

执行提交`5bf8b9385fb4cb326880df7e3d1d2fc4bc183eb6`。planId/employeeId/标准版本与学习关联的实际合成ID、引用断言见[G1_Cadre_Delivery.md](G1_Cadre_Delivery.md)及测试输出H002_SC1_INSTANCE。盘点到计划仍为同员工显式办理，无reviewId外键；完成仅聚合权威记录。

离职后当前组织HR/经理及未停用本人保留既有计划/学习历史读取，属于现有实现，企业保留策略未核实。C-DEF-01：保留离职员工关联的active=false请求被member-rules在职校验阻断，400且账号仍active；具体证据和最小兼容修复建议见交付记录。总控修复前不作完整撤权或G1通过结论。

## C-DEF-01成员停用契约修正
显式active=false允许保留同租户既有离职员工关联；active=true仍要求在职，缺失档案仍拒绝。保持CAS和审计，无新增字段或迁移；不代表离职自动停用制度已确认。

## H004-R 绩效生命周期可操作提示
三个绩效GET接口新增兼容字段livePlanIds，仅列当前成员可见且在职、属于活动周期组织、未取消及未形成结果的计划ID。该字段是生命周期提示，不是角色授权；各命令继续独立校验身份、状态、修订及原子写入。仅返回已有可见ID，不暴露额外组织或人员字段。页面、待办、自助及报表统一使用同一生命周期判断。历史调整仍可拒绝/撤回，申诉更正保持原规则。

## 干部任期登记
新增cadreTerm记录及/api/cadre-terms GET/POST，写入仍为{revision,command}，不改变其他API。register/correct/end/void保存事件历史，关联员工ID和任用岗位ID。HR/admin写且不能本人，经理按当前双组织范围读；结束/作废仅登记，不自动改变人事主数据或发送通知。干部档案消费同记录，作废不展示当前条目、历史仍受当前权限保护。无表结构迁移。
