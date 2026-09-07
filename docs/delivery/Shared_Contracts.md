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
4. 已有同员工/课程版本记录时拒绝再次enroll；取消使用restoreEnrollment并保留原任务和考试次数。历史跨项目复用尚未实现，不能视为接口能力。
5. submitLearning要求通过关联考试；verifyLearning须独立核验，接受前检查强制出勤；完成状态completed。verifyPlan接受前检查关联未完成且未取消的学习任务。
6. cadreProfile通过当前可见records聚合plans和learning。回流是读取现有权威记录，不另复制完成标记；不自动升级资格或职级。
7. 学分使用既有learning-credits接口，不把档案展示触发当成授予事件；来源与去重规则继续以领域代码为准。

共享热点：development.ts、app/api/development/route.ts、development-repository.ts被人才和学习共同使用，只能由当前总控/被明确交接的基础负责人单写。没有消息总线、跨服务事件系统或新自动派课协议，不为本批增建。

下一步：基础F-G0-02把以上契约逐项映射现有测试；模块只补确切缺口。任何新字段先记录请求/响应示例、旧数据处理、权限和消费者，再由总控合入。
