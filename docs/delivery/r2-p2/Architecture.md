# R2共用架构设计 v1

<a id="authority"></a>
## 基线、权威与复用

main启动HEAD为`22be3a7e366d6787180d4f593a30f5984c70e03a`且启动时干净。R2仅有P2准入授权`R2-P1-P2-TRANSITION-20260910`。权威顺序为冻结Scope及其批准记录、被批准的推荐原文和验收预期、生成源、固定历史证据；本设计作技术展开，不以旧代码或生成文档残留“待批”文字反转批准。33个其他模块和独立AI不在设计范围。

R1 P2固定输入为`e15237281ff19f04f08a354fd9455c518b24ae47`（所有者退出记录`R1-P2-EXIT-OWNER-20260910`）。复用其M01稳定person/任职版本、M19流程适配器、M48授权消费、M32数据集、共同CAS/命令账本、迁移屏障和恢复安全账本。固定设计可引用不等于R1 P3已经交付；P3开始前以契约探测和版本证据验证依赖，缺失则`blocked_dependency`，不在R2分叉另建身份/审批/权限引擎。

当前静态可复用：`development_records/events`稳定记录ID和历史、`development-repository.ts`租户revision CAS、资格证据筛选、360邀请去重、盘点发布引用、人才池/继任/IDP、干部任期/提名/考察基本入口。必须改造：固定五级标准、资格1–5硬编码、HR默认原卷访问、低样本精确计数、首次盘点发布自审、简化准备度/IDP、任用旧approved降级校验。旧审计快照含完整payload，不能复用于360答卷及敏感档案通用审计。这里只定位设计差异，没有产品修改。

<a id="objects"></a>
## 共用对象与版本

|对象/字段|设计约束|
|---|---|
|tenantId、personId|所有PK/FK/唯一约束带tenant；personId沿M01旧employee.id，不按姓名、StaffID、邮箱或账号合并；成员绑定与雇佣事实分开|
|rootId、versionId|root稳定UUID；每次已提交内容版本独立UUID；历史ID原样保存；versionNumber为根内单调展示序号，不能作外键|
|entityRevision、workspaceRevision|非负安全整数；前者对象CAS，后者沿R1租户CAS。客户端提交expected值，409重读；不得另建一个不同步的R2租户revision|
|definitionVersion、schemaVersion|业务模板/字典/算法版本与通信schema版本分列；不得因schema升级换业务根ID|
|sourceRef|producer、objectType、rootId、versionId、sourceRevision、digest、capturedAt、purpose；引用不可只存显示名、latest或数字序号|
|validFrom/validTo、recordedAt|自然日Asia/Shanghai闭区间；空结束显式openEnded；事件时刻RFC3339 UTC。实际记录时间不得回填为未知历史发生时间|
|effectiveAt、approvalId|批准事实与业务实际生效分开；plannedOn不是已生效证据；发布日期、有效日期及下载授权分别核验|
|supersedesVersionId、previousObjectId|更正链与重入/续期链不同；同根更正禁止环和跨租户，重入另对象不覆盖前段|
|historyQuality、provenance|verified/legacy_observed/unknown/conflict；历史未知不得补造版本、审批者、来源UUID或日期|

新业务表按域规范化，保留兼容读投影；不是继续全量JSON读改写。逻辑DDL在P3落实，P2不执行建表。每表至少索引(tenant,rootId,versionId)、(tenant,personId,status,id)、主要父对象及稳定游标；区间冲突在同租户CAS内校验，普通唯一索引不能独自证明无重叠。参数约束在模块字典和严格接口schema双向一致。

批准资料中的employeeId/stableEmployeeId与本包personId/stablePersonId均指M01稳定employee.id，不是账号或StaffID；接口明确一个canonical字段并保留旧字段适配，重复传两个别名且不同值拒绝。M26 projectId映射projectRootId、reviewerBindingId为独立reviewer_binding的bindingId，均通过已核ID映射而非同名合并。M03来源employmentRecordId保持来源namespace及原ID，明确映射至M01 assignmentId才可作任职凭证；M01 employmentId表示雇佣段，二者不得因英文相似混用。所有这些是本项目兼容字段说明，不能伪称原站未知UUID已经匹配。

<a id="lifecycle"></a>
## 状态、批准与生效

业务对象分开保存`contentState`、`approvalState`、`effectState`、`availability`，不强制所有对象拥有相同枚举。共用审批状态pending/approved/rejected/withdrawn/cancelled，业务后效not_requested/waiting/waiting_external/applied/failed/cancelled/blocked，通知pending/sent/failed/unknown/invalidated。模块流程表列举合法跃迁，未列举动作返回INVALID_TRANSITION。

独立复核采用M19冻结模板及实例，业务适配器实现loadBusinessSnapshot、validateStart、validateDecision、planLocalEffect、canCancel、planLocalCancel、projectStatus。适配器返回同一事务SQL计划，不自行commit/调用网络。实例唯一(tenant,businessType,businessId,applicationVersion)。节点激活解析候选人，动作时再核当前授权和回避；没有合格人则blocked，不自动给管理员、不把缺评视同意。委员会阈值由业务模板定义，不能套通用any通过。

提交冻结本次全部内容、材料贡献人历史集合和审批模板版本；新增材料/换评委/更改规则需要新applicationVersion，旧终态保留。申请人、本人和实质材料贡献人不得审核自己的内容。委员会回避单独留原因、替补/分母变化和批准版本；已经投票的退回或重组不能静默覆盖旧票。显示性标准调整的窄例外仅依M37-SPEC-03，须证明semanticDigest不变且独立动作授权，不扩到其他模块。

M03任用消费者永不替M01改任职：批准任用决定、M01按D1–D7完成实际生效、M03核对生效凭证是不同事实。M06资格、M18盘点、M17继任均不自动产生人事决定。M26报告授权、M18发布、M03归档由各域掌握。

<a id="transaction"></a>
## 事务、并发与作业

每次写入按顺序执行：认证及当前安全epoch → 当前grant元组授权 → 版本/状态/回避/源依赖检查 → 单一租户CAS → 业务新版本、不可变事件、脱敏审计、outbox、command receipt、恢复行日志同事务提交。任何失败全部回滚。DB不可写时不承诺同库一定记录失败；外部运行监测只记命令ID/错误码，不泄露敏感内容。

事务提交条件包括expectedWorkspaceRevision、expectedEntityRevision、expectedAuthorizationRevision、schema/writerEpoch、recoveryEpoch、exitFence及所用依赖版本。依赖属同DB时在事务内重核；远端状态无法证实足够新时为unknown，强前置业务阻生效。数据预读不能绕CAS，角色名匹配不能代authRevision。资格恰好过期以事务所捕获的服务端授权/业务时刻判定，跨日长作业最终再核。

幂等命令以tenant+actor+actionNamespace+idempotencyKey唯一，digest包含全部payload和预期版本；相同键同内容返回原回执，异内容冲突。终态保留去重墓碑，不因普通作业TTL释放业务键。超时先查commandId或相同请求键，unknown不得换键重做。审计与业务写入都失败的命令由可信账本查询核实，查无记录不自动等于外部未执行。

大批次采用父job及逐项命令，显式部分成功/拒绝/未知；租约接管增加fence，过期执行者不得推进游标。每事务建议≤80语句、每块≤4MiB、查询50默认/200上限，P3根据实际D1限额收紧。批量发布先冻结完整manifest、逐块准备不可见版本，最后CAS发布manifest指针；消费者只读完整ready manifest，不能读半份报告。不是无界单事务，也不承诺跨服务分布式原子提交。

<a id="ownership"></a>
## 阶段责任与设计闭环

P2负责人负责对象、规则、schema、失败处理、映射和设计自检；模块逐项闭环后才提升下一模块。本目录状态只说明设计材料成熟度。P3域实施负责人落实DDL/服务/迁移器，独立测试负责人按合成GWT留证，共享能力负责人证明R1适配版本及原子性。P4业务HR、隐私/安全、运维分别核真实角色、用途、恢复和生产切换；所有者独立批准P2退出及后续准入。具体姓名未在当前资料授权绑定，以岗位责任交接，不邀请新成员。

闭环标准：对应全部已批准SPEC、字段/角色/状态、原验收ID有追踪；共用能力有适用条款；迁移和旧消费者处置明确；剩余证据缺口有影响范围及P3/P4责任；无必须由所有者新决定的未决核心规则。设计闭环不表示LIMIT整组消失或实现通过。
