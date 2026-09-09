# M48权限矩阵与七项业务消费契约

任务：R1-P2-04。状态：设计完成，待独立评审；不是P2批准或P3验证。

## 批准依据与版本

基准源码/事实源：`716cd9df5f5776d050f77f57c2ad5a35c0a83882`。批准需求：`M48-SPEC-01`、`M48-SPEC-02`、`M48-SPEC-03`、`M48-SPEC-04`、`BP-I-REQ-01`、`BP-P-REQ-09`、`BASE-01`、`BASE-02`、`BASE-04`。批准原文及优先级以 [批准记录](../P1_Approval_Records.md) 为准；原文中的历史待批措辞不重开已批准决定。

## 当前实现与复用判定

- **待修改**：[自助聚合API](../../../app/api/self-service/route.ts)；基准文件 SHA-256 `49142604b1851b51a112611fd911ebf44a589de5b210883dbbc4749c68b7f952`。已有本人过滤和原域状态映射；tasks包含他人作业批阅，完整团队/OKR适配缺失。
- **待修改**：[自助页面](../../../app/self-service/workspace.tsx)；基准文件 SHA-256 `ac8fe56d655c8879f187719bc55190378d6bd1d9143e24a61609bd7ac2a68c88`。Data漏revision，awaiting_publish计待批，读取失败保留旧data。
- **待修改**：[角色与可见范围](../../../lib/hris/authorization.ts)；基准文件 SHA-256 `a05aa4a6264495289b9512bc54f416d38881e905aaa0fa45f96624c1b50abcca`。单role+orgScope不能区分直线/虚线/间接/部门负责人；admin短路必须服从动作及敏感域约束。
- **可复用**：[附件归属与当前权](../../../app/api/attachments/route.ts)；基准文件 SHA-256 `bc5f8cf99908aa2f1cb9e010695c0f32a56b6503d57d783de0137e7fcb8ef21b`。本人visibility与经理不可借名册读文件保留；新增对象归属需逐型授权。

## 权限对象与决策顺序

permissionGrant记录tenant、grantId、memberId/roleId、objectType、action、relationType、scopeRoot/includeDescendants、fieldAllowlist、historyMode、validFrom/To、revision。memberRole为多个角色关联，不以role字符串拼接。relationship记录relationId、managerPersonId、subjectPersonId或departmentId、type=direct/indirect/dotted/department_head、assignmentId及validFrom/To、sourceVersion；“直线职位上下级”只作建立显式关系的来源，不能未经授权自动扩为所有下级访问。

服务端先验证平台登录、当前企业active成员与恢复隔离闸门，再确定当前member.employeeId（稳定personId）。未绑定返回binding_missing，不接受客户端employeeId改变本人；多绑定冲突拒绝并转管理员核对。重聘/调动/离职不会自动新增平台访问权。

对单个(action,object,row,field,historyMode)逐条权限求值：每个适用角色先求对象/动作/关系/组织/字段/历史的交集，再对允许的元组取并集，最后交敏感域及独立性约束。禁止把角色A对象范围与角色B字段白名单做笛卡尔乘积。显式敏感字段禁止/域发布限制优先；无明确grant为拒绝。管理委托额外取委托双方当前允许元组与委托范围交集。read/export/subscribe/manage各独立，不能由read推出其他三项。

权限快照含authorizationRevision、relationshipRevision、memberBindingRevision、workspaceRevision；任何角色/组织/字段/绑定/关系/恢复epoch变化使旧投影与动作令牌失效。权限证据不包含原敏感值，前端allowedActions仅帮助展示，服务端动作必须再次求值。

## 角色、关系、动作、字段与历史矩阵

| 身份/关系 | 对象范围 | 读取/字段 | 写入及管理 | 历史/附件 |
|---|---|---|---|---|
| 本人 | 当前唯一绑定person | M01本人开放字段；生产者本人已发布结果 | 仅M01模板明示自助字段申请；各域返回的本人动作 | 当前仍有本人历史权；employee附件且归属本人；不开放HR材料 |
| 直线经理 | 明确direct有效关系 | 该grant开放团队字段 | 原域明确经理动作；不因经理可调动/改工资 | 当前direct与history grant交集；经理名册权不派生员工附件权 |
| 间接经理 | 显式indirect grant+关系 | 仅该间接范围/字段 | 仅明示动作 | 不继承直线或虚线权 |
| 虚线经理 | 明确dotted有效关系 | 虚线专用白名单 | 不继承直线审批/维护 | 旧虚线关系不能永久看历史 |
| 部门负责人 | 授权department及显式includeDescendants | 部门范围开放字段 | 原域允许动作 | 不因组织树存在就扩全部下级/其他关系 |
| HR | 当前授权组织范围 | 人员常规/已授敏感字段 | M01范围维护/任职发起执行；新F-SPEC-05独立HR审核需显式动作 | 当前组织+history；HR附件需归属/范围 |
| M19节点审批者 | 指派节点涉及对象及必要摘要 | 调入B仅原单摘要，D5职级必要值不可隐藏后盲审 | 仅当前节点decide，不能因管理委托代签 | 无默认原员工历史/附件权 |
| 管理员/受托管理员 | 明示管理动作与范围 | 依对象/字段/域策略 | 管理和配置不免独立性；委托只交集 | 不因admin绕过薪酬专岗/未发布评估或汇总匿名策略 |
| 薪酬编辑/复核专岗 | 沿原payroll专岗及独立贡献者约束 | 已授工资管理字段 | 不扩本人自助为管理；M48只链接原域 | 原工资快照按当前专岗与批次组织规则 |

敏感字段类别最低包括证件/手机/薪酬/未发布成绩/360答卷/HR附件。默认不向团队开放。viewEmail/viewLevel作为旧授权映射保留其真实范围，不自动代表全部通讯字段/所有人才结果授权。多角色合并必须逐字段逐对象计算；详情、搜索建议、排序、筛选、计数、图表、导出、订阅、错误消息、历史及附件走同一决策服务。

## 七项消费协议

统一请求：tenant从会话派生；subject由本人绑定或合法团队关系解析；businessType/businessId、cycleId或period、sourceRevision、commandId/idempotencyKey、sourceVersion、action、payload。统一响应：availability、stableEmployeeId、businessId/type、cycle/period、rawStatus、displayStatus、mappingVersion、approvalStatus/effectStatus/publicationStatus、allowedActions、reasonCode、effectiveAt、sourceRevision/definitionVersion、observedAt、authorizationRevision、fields及fieldStates。可用状态available/no_data/not_configured/unavailable/forbidden彼此不同；forbidden不返回对象存在性和隐藏计数。

| 入口 | 生产者及稳定关联 | 原域动作消费（须allowedActions） | 关键状态与恢复 |
|---|---|---|---|
| 团队 | M01 person/assignment/relationship；BASE-02 | list/detail/history（自助不建关系或成员） | relationship无配置≠空团队；解除关系清缓存；当前权裁剪历史 |
| 审批 | M19 instance/nodeRevision；M01 originalApplicationId | 发起/提交/批准/驳回/撤回/执行分别走原域 | 本人申请/本人任务/他人授权办理分开；approved+waiting≠生效 |
| OKR | M16 objectiveId/keyResultId/cycleId/ownerId/alignmentTargetId；metric name/unit/baseline/target/current/direction | create/edit/align/updateProgress/review | 无评分/权重不算分；同目标/KR版本进展历史；未接not_configured，非绩效goal换标签 |
| 目标 | M16 planId/cycleId/planVersion、checkinId/appealId/resultPublicationId | create/edit/submit/withdraw/checkin/selfAssess/review/appeal | pending调整阻自评；approved申诉显示awaiting_publish；原已发布结果不被草稿盖掉 |
| 假勤 | M11 recordId/personId/periodId、shiftId/leaveId/correctionId、余额值/单位/sourceRevision | clockIn/requestLeave/requestCorrection/edit/submit/withdraw | 余额unknown≠0；源校验日期/额度；旧revision409先读原ID |
| 学习 | M27 assignmentId/taskId/attemptId/submissionId/planInstanceId、阶段/日期/成绩状态 | start/answer/submit/editPermittedAnswer/submitHomework/reviewHomework | 本人学习与授权批阅他人分列；分数null不补0；阶段未开放拒绝；任务消失不等完成 |
| 发展计划 | M17 planId/stageId/actionId/mentorRelationId、目标/日期/feedbackId | create/edit/submit/withdraw/updateAction/mentorFeedback | 依生产者阶段/角色/窗口；不能门户推进、重开或绕过失效模板 |

原站“我的档案”不能作为全团队权限事实；既有M26反馈邀请等已存在任务按真实businessType及生产者适配保留，不能冒充M27学习成绩；33暂缓调查等历史入口保留映射但不启动新独立引擎。工资条数量继续是已发布条数，不当薪酬金额/发薪成功。

R2/R3的算法不由本包批准：registry按producerId、contractVersion、capabilities、configurationState、integrationEvidenceRef登记适配能力，缺真实实现只返回未配置/不可用与负责人/恢复条件。R1合成mock只证明协议及门户授权；真实联调状态始终not_executed，完整业务验收由生产者就绪后执行。新rawStatus没有映射时显示“状态暂不可解释”并禁动作，保留原值与版本给有权诊断，不默认映成成功。

## 任务列表与状态投影

taskKey=(businessType,businessId,action,nodeRevision或sourceRevision)，不是新业务记录ID。列表分self_tasks、self_requests、authorized_others、team；同一个原单可能在不同合法视图出现但各自计数不相加为人数。授权他人任务保留subject和原域角色，不写“我的学习完成”。awaiting_publish单列待发布；waiting/failed执行单列；原状态与映射版本可追踪。

每个列表有pageSize=20默认窗口、nextCursor、hasMore、visibleTotal或totalState=unknown；不把20条当全部。卡片计数与列表同过滤同版本，统计对象明确。cursor含user/tenant/partition/filterDigest/sourceManifest/authRevision，篡改或权限改变拒绝。不能用原单搜索命中数推测没有权限的人数。

## 错误、缓存与下载

| 结果 | 页面行为 | 再提交边界 |
|---|---|---|
| binding_missing | 说明需关联，清本人资料/任务，不显示全员fallback | 不可通过参数选人 |
| 401/403、解绑、字段撤权 | 清对应请求和共享缓存，取消在途读取、撤销object URL；页面重新取当前权 | 所有旧允许动作失效；旧下载需服务端再验 |
| 409 | 显示版本变化，丢弃跨版本合并结果，重新读取原单 | 用户核新内容后新意图提交，不盲写覆盖 |
| 503/网络故障（读） | 首次显示不可用；已有非敏感摘要可标observedAt，仅安全白名单保留 | 敏感字段立即清；禁办理，不能填0 |
| 网络结果未知（写） | 保留commandId+businessId并显示待核 | query同命令；无权查询保持不可核，不能换身份/新键重发 |
| producer_not_configured | 保留入口/范围、原因和恢复条件 | 无mock业绩、无可执行按钮 |

前端避免旧请求晚返回覆盖新授权：每次授权版本变化提升requestGeneration并abort旧请求；返回时检查generation与authRevision匹配，不匹配丢弃。Cache-Control:no-store；不持久缓存敏感数据到localStorage。附件按objectType+id+version查归属和当前字段/可见性；列表与直接下载相同策略，不暴露R2 key或可绕过授权的公共链接。下载开始前最终验权，已合法传出字节不可保证收回，后续请求/续传必须重验。

## 正常与失败场景及P3建议

以下仅为可执行验收设计，全部未运行。P3须在P2退出获批后使用隔离合成数据；P4独立人类角色和生产验收不由本表替代。

### P3-M48-01

- 需求：M48-SPEC-01、BASE-01、BASE-02。
- 给定：本人绑定P1，客户端传P2；再解绑/重聘且无新授权
- 操作：读取本人、旧缓存与带P2参数详情
- 预期：只会话绑定P1；参数不能换本人；解绑清数据，重聘不恢复账号
- 证据产物：API投影、浏览器缓存状态和绑定revision
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-02

- 需求：M48-SPEC-01、BASE-02。
- 给定：同人有直线A、虚线B、部门C不含子部门，字段权各不同
- 操作：读A/B/C及间接D，尝试混用A字段权到B
- 预期：每对象字段逐元组并集再敏感交集；D拒绝；薪资/证件/答卷无授权不可读/筛选/计数
- 证据产物：角色关系字段矩阵和直接API否定结果
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-03

- 需求：M48-SPEC-02、BP-I-REQ-01。
- 给定：25条本人任务，2条他人批阅，申诉approved未发布
- 操作：看卡片并翻页/打开原单
- 预期：本人/授权他人分列；20条带hasMore且能续页；awaiting_publish不计待审批；同源计数
- 证据产物：两页ID去重、四分区计数和原单状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-04

- 需求：M48-SPEC-03、BP-P-REQ-09。
- 给定：OKR有KR值/单位/方向但无权重评分，M16适配未接和可用各一组
- 操作：显示进展/对齐及更新动作
- 预期：未接明示not_configured；可用显示原指标，只调用允许动作；不自动绩效计分
- 证据产物：OKR请求/响应contractVersion和禁算断言
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-05

- 需求：M48-SPEC-03。
- 给定：目标pending调整、假勤余额未知、学习未开放阶段、IDP未开放行动
- 操作：分别自评、请假、答题、行动提交
- 预期：均由原域校验，unknown非0，不能绕阶段；有allowedActions正常路径仍保留源版本与原ID
- 证据产物：四个producer请求回执和原数据差分
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-06

- 需求：M48-SPEC-04、BASE-04。
- 给定：页面有敏感字段与旧附件URL；旧请求晚回，随后401/403或撤字段
- 操作：刷新、旧请求返回和旧URL下载
- 预期：清缓存/禁办理，晚回不恢复敏感数据；下载拒绝；503只可保留带时点非敏感摘要
- 证据产物：请求generation、缓存和下载状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M48-07

- 需求：M48-SPEC-03、M48-SPEC-04。
- 给定：七入口正常合成适配，再返回新rawStatus/409和写响应丢失
- 操作：逐项消费并按commandId查询恢复
- 预期：七项完整保留；未知映射不可办；409重新确认；未知查询而非重复提交；mock不标真实联调
- 证据产物：七入口契约矩阵、原单关联与模拟标识
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

## 本阶段执行边界

本任务只修改P2设计及一致性材料；未运行产品测试、迁移、备份恢复、外部交易或原站操作；不改变业务代码、数据库、部署、访问者及主事实源。所有技术默认均为设计参数，不能覆盖已批准业务规则。
