# M32数据集、设计器、快照与异步任务设计

任务：R1-P2-05。状态：设计完成，待独立评审；不是P2批准或P3验证。

## 批准依据与版本

基准源码/事实源：`716cd9df5f5776d050f77f57c2ad5a35c0a83882`。批准需求：`M32-SPEC-01`、`M32-SPEC-02`、`M32-SPEC-03`、`M32-SPEC-04`、`M32-SPEC-05`、`M32-SPEC-06`、`BP-I-REQ-02`、`BP-I-REQ-11`。批准原文及优先级以 [批准记录](../P1_Approval_Records.md) 为准；原文中的历史待批措辞不重开已批准决定。

## 当前实现与复用判定

- **待修改**：[21数据集与CSV](../../../lib/hris/reports.ts)；基准文件 SHA-256 `1149817a3d9792d91b15cc03e4af21a934c7f11299cc1dba04b0a46aa1800f09`。行粒度可复用但缺稳定rowKey/定义版本；performance筛选任意supersedes而非仅published，违反已批准发布链语义，列P3修复。
- **可复用**：[薪酬报表](../../../lib/hris/payroll-reports.ts)；基准文件 SHA-256 `0621acfa2dc5fc9cc7d0f7786b385eb882a314946d7246901f43544d8f969b1b`。按批次组织当前专岗、整数分安全求和与工资条×考勤引用保留；额外export/subscribe动作需补。
- **待修改**：[报表API](../../../app/api/reports/route.ts)；基准文件 SHA-256 `cfc75d5572ec21a59cbc36f66d3eac29cc4074aa0b10115ae1ac17b6df55ee33`。GET全量装载再切50行、POST超过10000拒绝；现无异步执行器，不可记数据库分页已完成。
- **待新增**：[报表UI](../../../app/reports/workspace.tsx)；基准文件 SHA-256 `126d946b092cfeb9ce6cfa6a8a242ba0bff36b9245fa32feaaa875346b49d03a`。保持21目录及三类日期控件；新增设计器、历史模式、job状态与独立动作入口。

## 数据集定义与类型体系

设计目录见[R1_P2_Report_Datasets.json](R1_P2_Report_Datasets.json)，21个datasetId保持。所有已有列按所引reports/payroll-reports基准源码列数组和原计算语义保留；下面明确行键与增量差异。P3发布每个datasetDefinitionVersion必须包含完整fieldId/label/type/unit/nullPolicy/sourceField/accessPolicy、rowKey、allowedJoins、sortKeys、timeModes、metric表达式及sourceSchemaVersions；未注册字段不能进查询。M01新版字段绑定稳定ID，legacy名称只展示。下表定义不授权M07/M16等生产者新算法。

类型：opaque_id/text/enum/date/timestamp/integer/decimal/money_cents/boolean；money_cents使用安全整数并携带currency，不同币种拒绝sum；日期和分钟不能跨单位聚合；百分率明确倍率及舍入2位。无适用比率写not_applicable，不为每表强造完成率。全表原数据列不会因生成本设计而删除。

单元格为{value,state,reasonCode}：state=value（包括真0）、null（业务缺值）、not_configured（规则/服务没配置）、forbidden（该列整体不返回，不能暴露行级秘密）、unavailable（来源故障）；no_data为查询行集状态而非单元格0。分母0或不可核→ratio=null+zero_denominator/unknown_denominator；count(*)不等count(field)，sum已知值须同时回knownCount/missingCount，缺值不能暗补0。null与0在CSV附数据字典/必要的状态列可区分。

|数据集 / 生产者|稳定行键 / 粒度|分子分母、去重与单位|缺失值 / 时间|
|---|---|---|---|
|workforce / M01|personId；当前可见人员，含离职；按personId去重|未定义比率；在职人数需status过滤后distinct personId|不完整任职/字段为null+reason；current：none|
|contractCoverage / M01|personId；当前可见在职person，左联已登记合同，保留无合同者|coveredPersonCount / visibleActivePersonCount；覆盖多合同者仍1人|分母0→null；待核身份/日期计unknownCoverage，不当未覆盖0；current：businessDate(now)|
|contractOperations / M01|contractId；每合同登记，含草稿/作废；版本不重复成多份合同|签订次数按person+legalEntity+agreementCategory distinct signed/ended contractId；作废排除|endedOn优先end，空结束筛选不命中；法人/协议未知待核；event_range：coalesce(endedOn,end)|
|recruitmentOperations / M12|requisitionId；每招聘需求；应聘关系candidateApplicationId计阶段|remaining=active?max(0,headcount-hiredApplications):null；自然人数单独distinct candidatePersonId|headcount未知不得用0推算；非active remaining=null；current：none|
|attendance / M11|shiftId；每人每有效班次核验；不等月度期间记录|分钟按源班次算法；如展示覆盖率仅known coveredMinutes / known plannedMinutes并明示缺失样本|缺打卡/冲突的uncoveredMinutes=null，不补0；不自动发布月报；event_range：shift.businessDate|
|payrollOperations / M07|batchId；每可见批次；有效工资条按paySlipId去重|gross/deduction/net/employer为整数分分别sum；不跨币种相加|未配置项目数值沿已批M07；未知/不可用单列，安全整数溢出拒绝；current：none|
|payrollReconciliation / M07|paySlipId；每已发布工资条；旧原值+published补差事件|originalCents + sum(published adjustments Cents)，按adjustmentId去重；不是支付成功|来源缺失/未知回执不填0或支付已完成；current：none|
|payrollAttendanceReferences / M07+M11|paySlipId,attendancePeriodId,frozenVersion；每工资条×冻结考勤引用，非员工数|引用分钟是各引用快照值；人数distinct personId另算，禁止引用行数作人数|当前来源不可见/不存在为unavailable/null；原冻结值保留；current：none|
|performanceOperations / M16|planId；每员工计划；各版本跟进单独状态计数|pendingChanges/checkins按各recordId；可反馈只当前角色集合；不相加为总人数|未发布结果/缺业务日期null，不填低分；current：none|
|performance / M16|resultRootId,publishedVersionId；仅当前有效published结果；同发布更正链1行|评分与评级沿已发布源版本；不得按任意updatedAt选最大|score缺失null；新draft不能替代旧published；current：none|
|talentReview / M18|reviewRootId,publishedVersionId；未被另一个已published supersedes替代的review|潜力/绩效档位各源字段；配置人数、采集、校准、发布分别count distinct personId|缺采集/评分null；等级不当M17准备度；current：none|
|successionCoverage / M17|positionId；每可见启用岗位；现任与后备分开|incumbents按有效primary personId；successors distinct active personId per position；ready/one_year/two_years沿版本|0仅当前可见范围无有效后备；未知准备度单列；current：none|
|learning / M27|enrollmentId；每课程任务含历史复用/取消，任务不等人|completed/enrollment分别计数；复用sourceEnrollmentId与原核验时间保留|未核验时间/无成绩null，取消不完成；current：none|
|learningPlanProgress / M27|learningAssignmentId；每学习计划实例|completedRequirements / applicableRequirements；completedStages / stages分别定义，不混合权重成绩|denominator0→null；grade.not_configured/pending/provisional/final与score分列；current：none|
|learningExams / M27|examTaskId；每独立考试任务；attempt作为子记录|attemptCount=distinct attemptId；raw earned/max与percent score分开，不用任务数当作答数|未答score/earned/max null；次数0是真0；current：none|
|homework / M27|homeworkTaskId；每独立作业任务，当前submissionId/version引用|submissionVersion/score/reviewResult分列；passedTask比率只在明确任务分母下计算|未评分null；未留reviewer快照明确未知，不编姓名；current：none|
|trainingStageProgress / M27|trainingId,personId；每培训项目×有非取消任务的人员；不是所有应参训人|required course数按阶段定义；completed distinct courseId；missing task与pending task分开|未完成阶段名可null仅所有阶段完成；分母0比率null；current：none|
|trainingProgress / M27|trainingId；每培训项目|participants=distinct personId(non-cancelled)；completion=completedTasks / validTasks×100，四舍五入2位；任务按enrollmentId|validTasks0→ratio null；已取消数与有效任务分开；current：none|
|trainingRoster / M27|enrollmentId；员工×课程任务记录，重复参加用enrollmentId区别|requiredSessions=非取消必修场次；present/absent=已verified；pending=required-present-absent|未登记/待核验不当absent；人员与场次分母分离；current：none|
|instructorSchedule / M27|sessionId；每培训场次|minutes=(endAt-startAt)/60000；cancelled effectiveMinutes=0；不当实际授课/课酬|未关联内部讲师明确unlinked，不猜person；event_range：Asia/Shanghai(startAt)|
|instructorCampaignProgress / M27|campaignId；每讲师认证活动|applications按applicationId可重报；people distinct personId另算；profiles/latestTrial/mandatoryProof分别计数|交叉指标不求和为总人；未有有效证据不判通过；current：none|

## 当前15模块覆盖和分阶段消费

| 来源 | R1必须保留的目录/契约 | 生产者缺失时 |
|---|---|---|
| M01、M19、M48、M32 | 人事/合同/编制；流程审批与执行状态；入口及报表定义自身元数据 | R1实施任务逐项验证，不用其他模块进度代完成 |
| M03干部、M06资格、M17继任发展、M18盘点、M26 360、M37人才标准 | 稳定record/person/position/standardVersion、评价/发布/继任状态、已批准口径；360匿名/样本政策沿M26 | catalog entry存在，availability=not_configured或unavailable；指标未知不发布0/满分；不重建干部/资格/360算法 |
| M12招聘、M16绩效目标OKR、M27学习、M11假勤、M07薪酬 | 上述21数据集及OKR对象/KR进展、组织绩效/兼职绩效来源声明 | 每个适配标producerVersion、contractEvidence、realIntegration=not_executed；联调责任归生产者与M32 |
| 33暂缓来源 | 原目录ID和历史映射 | 保留deferred标签，不建立独立数据链；电子测评只接口状态 |

无已批准数值算法的新增目录定义只保存接口字段/单位/版本和不可用原因，禁止发布计算型definition。M32不把元数据目录行数写成15模块业务验收数。

## 时间、当前授权与真实快照

每定义支持current或event_range；snapshot是对已保存真实snapshotId的读取能力，不接受任意历史日期重建。current拒绝非空from/to/asAt；event_range允许from≤to、北京业务日含边界，空事件日期不命中有界筛选。API严格拒绝未知参数，不能只在UI隐藏。asOf更名含义为generatedAt，旧字段兼容保留但标不是业务截止时点。

snapshot对象含snapshotId、tenant、datasetId/definitionVersion、businessCutoff、generatedAt、sourceRevisionManifest、rowKeySchema、rowCount、chunkRefs、contentDigest、createdBy、purpose、status。status building→ready或failed，ready必须所有块哈希一致且定义/源版本清单完整。没有真实该时点数据返回SNAPSHOT_NOT_FOUND/HISTORY_UNVERIFIABLE，不拿当前数据换generatedAt造历史。

快照固定数值但不固定访问权：每次按生产者当前访问策略校验row及field。M01人事历史用当前person可见范围交history权限；工资历史用原批次对象及其组织快照作为受保护对象，仍核现在该批次组织的专岗授权；旧任职关系本身不授历史权限。聚合从当前获准行重算，返回visibleScope与recomputedForAuthorization，不暴露原全量total。仅有汇总权的人不得钻取行，未配置敏感匿名/小样本策略的汇总不开放，不自行设阈值。

## 声明式设计器与SQL编译边界

reportDefinition为stable definitionId，draft可编辑，publish时生成不可变version/digest，retired阻新job。选择字段、类型化过滤、分组/排序、sum/count/countDistinct/min/max/avg和显式分子分母；关联只注册稳定FK和cardinality（1:1/1:N），1:N必须声明去重/先聚合策略，禁止人数被联接放大。禁止任意SQL、脚本、跨租户join、隐藏字段的过滤/排序/分组/公式及推测。公式AST做类型/单位检查、复杂度上限（设计预算50表达式、深度8、5个注册join），超限明确错误，可P3调参，不能静默截结果。

字段权限在生成查询计划前检查，先行/列授权后聚合；没有字段使用权返回FIELD_NOT_ALLOWED且不泄露字段值/命中数。零分母在合法公式求值时返回null原因；类型/单位不兼容阻发布。schemaVersion与producer版本不匹配返回DATASET_VERSION_UNSUPPORTED，不以旧schema默算。

## 有界读取、索引和一致性执行

新增按域规范化read model，不继续调用全量developmentContext后切片。索引为(tenant,dataset,definitionVersion,generation,sortValue,rowKey)及(rowPersonId/currentPolicyKey)，过滤/授权键入SQL，cursor由服务端签名绑定tenant/user/authRevision、definitionVersion/filterDigest/generation/lastSort/lastKey。默认50，最大200，SQL LIMIT pageSize+1，稳定次序由排序值+唯一rowKey补足。不得仅把offset换cursor仍在内存makeReport全表。

当前多页用projectionGeneration引用固定sourceRevisionManifest；生产者更新新generation，已开页面可继续同generation但每页重核当前授权。若无固定generation实现，则revision变化返回409要求从头，禁止跨版本拼快照。分页total只有可安全有界统计时给exact；否则totalState=unknown，始终可游标继续，不冒称完整总量。计数与查行同策略；seek索引P3 EXPLAIN必须无未约束全表扫描。

投影生成从不可变事件重放至cutoff，或读有界实体版本validAtRevision；现旧表缺版本的域不能用多次不一致SELECT凑snapshot。迁移回填后无对应历史者标不可重建；真实快照只从具备一致版本的来源生成。未完成投影的目标current查询可明示延迟与sourceRevision，不能假“实时”。

## 导出与文件可用性的原子边界

保留同步≤10000行路径但额外受字节/内存/权限预算；超行或预计文件超过8MiB转异步，不能截断。exportJob主键jobId；唯一(tenant,requester,idempotencyKey)，请求digest包括definitionVersion、filter、columns、snapshot/generation。同键同内容返回原job，同键异内容409。状态queued/running/ready/failed/cancelled/expired，另记generation、leaseOwner/leaseUntil、fencingToken、chunkCursor、attempt/reason、resultManifest。

执行器每块≤4MiB、行≤200，逐块校验当前export与字段权，并写不可变R2对象；D1记录每块hash/rowRange后续跑。租约重抢递增fence，旧worker不得提交新块/ready。所有块完成后最终权限重核+同事务审计+ready manifest发布；审计/CAS失败文件保持不可下载的orphan/暂存。文件下载只通过鉴权API，ready并有current read+export才可；被撤字段则重裁生成新的授权结果或拒绝，不直接给旧全量文件。不得发可绕过验权的公开R2 URL。

取消/过期后tombstone使文件不可读，物理清理延后由维护job；导出jobTTL设计24小时、孤儿隔离48小时后无引用才清；这些不是业务历史保留期限，恢复/审计/附件原历史不得随TTL删。全部job/块的sourceManifest可追踪，unknown响应查询jobId而非重复入队。CSV string以危险前缀= + - @和前置空白防公式注入，number负数仍数值；空值导出带状态列/定义说明。

## 订阅、转交、屏蔽与投递

subscription字段：id、ownerId、recipientIds、dataset/definitionVersion、columns/filter、snapshotMode、timezone、frequency/localSendTime、startAt/endAt、revision、status、channel。frequency及时区必须显式，不擅定业务周期；调度计算UTC occurrenceAt并保存当地时间及offset，DST重复时刻同一周期仅一次，缺失时刻需定义显式策略（未指定阻配置，不猜提前/顺延）。默认推荐Asia/Shanghai只作界面预填，用户保存显式值后生效。

每次生成/发送/读取核owner与recipient当前各自对象字段权取交集，并要求owner subscribe、recipient相应read，导出文件另要export。不共用管理员全量快照或明细附件；默认发送需登录的报表链接。幂等键(subscriptionId,subscriptionVersion,occurrenceAt,recipientId,channel)，每人独立snapshot/resultManifest和delivery状态。

转交managementOwnership只能已有具manage权成员明确接受后原子变更owner/revision，历史owner/投递保留；不转数据/导出权。新增收件人独立核授权，E2不创建访问者。屏蔽/过期即时阻新生成及最终发送，已运行job末次检查subscriptionRevision；旧pending通知作废，sent不可保证收回。unknown只查供应商回执，未证未发送前不得盲重发；通知failed不改变snapshot ready或业务事实。真实外发附件若未来要求，需另获明确范围决定，本方案不启用。

## 容量与失败预算

100万行×平均1KiB≈0.95GiB，已超过128MiB isolate，故全量内存方案排除。chunk 200×平均1KiB≈0.2MiB，最坏4MiB；同时最多两块、序列化/缓冲预算≤32MiB，余量给权限与运行时。每租户并行export worker初值1，任务有界抢占，避免租户CAS争用；P3以实际row宽/并发/SQL计划验证，不能从估算宣称性能达标。无后台执行能力则job维持blocked_runtime，完整设计继续，平台依赖见恢复/决策包。

## 正常与失败场景及P3建议

以下仅为可执行验收设计，全部未运行。P3须在P2退出获批后使用隔离合成数据；P4独立人类角色和生产验收不由本表替代。

### P3-M32-01

- 需求：M32-SPEC-01、BP-I-REQ-02。
- 给定：同person多任职/重聘、两份合同，另人无合同；跨数据集任务/岗位/引用多行
- 操作：核21数据集行键、人数、单位和比率
- 预期：行键唯一；person去重；多合同不重复覆盖人；0分母与unknown为null；不把引用/任务行当人数
- 证据产物：21数据集固定夹具与独立手算oracle
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-02

- 需求：M32-SPEC-01、M32-SPEC-06。
- 给定：工资条多冻结考勤引用，招聘候选多应聘关系，培训无有效任务
- 操作：查询工资/招聘/学习
- 预期：钱用整数分、引用不计人数、应聘关系与自然人分列；任务完成比率null，未配置指标不虚构
- 证据产物：各源rowId、单位、denominator与null状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-03

- 需求：M32-SPEC-02。
- 给定：current dataset带日期；event_range边界当天/空日期；不存在快照
- 操作：执行三种查询；对照真实快照
- 预期：current非法参数拒绝；事件含边界且空不命中；无快照不伪造；generatedAt非业务截止
- 证据产物：API错误矩阵与snapshotManifest
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-04

- 需求：M32-SPEC-01、M32-SPEC-02。
- 给定：绩效旧published，新draft.supersedes旧；人才review同样结构
- 操作：依次读current、发布新版本、读旧snapshot
- 预期：draft不隐藏旧published；新发布才替换；旧快照值和发布链可追溯
- 证据产物：发布版本链和基准源码差异验证
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-05

- 需求：M32-SPEC-03。
- 给定：有汇总read无export/明细/敏感field；旧快照全量但当前撤权
- 操作：导出、drill、排序/筛选隐藏字段及旧URL下载
- 预期：服务端拒绝；聚合重裁当前可见范围且不泄露原总数；未定敏感小样本政策不发布
- 证据产物：策略元组、SQL授权计划及泄漏否定结果
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-06

- 需求：M32-SPEC-04。
- 给定：10001行，跨页发生源更新；异常大单行；两个worker租约抢占
- 操作：完整分页/异步导出，旧fence完成、审计失败
- 预期：固定generation或409重查，无丢/重行；大行明确失败；旧worker不能ready；审计失败不可下载
- 证据产物：query plan、cursor链、job fence、manifest/hash
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-07

- 需求：M32-SPEC-04。
- 给定：设计器非法SQL/隐藏field/单位混算/1:N人数膨胀与合法零分母公式
- 操作：发布并求值
- 预期：非法定义不发布；1:N必须先去重/聚合；合法零分母null原因；完整列注册无遗漏
- 证据产物：AST类型结果、字段字典与非法计划拒绝
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-08

- 需求：M32-SPEC-05、BP-I-REQ-11。
- 给定：两收件人范围不同，owner转交未接受；生成后撤一人/屏蔽，外部unknown
- 操作：调度重入、接受转交、最终投递及查询回执
- 预期：每周期每人每渠道唯一；未接受不转，转交不扩权；撤权屏蔽不发送；unknown先查；历史投递不抹掉
- 证据产物：subscription revision、recipient manifests、消息拦截器
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-09

- 需求：M32-SPEC-03、M32-SPEC-04。
- 给定：文本以空白=、@或-开始，数值为-100分，null与0并存；导出响应丢失
- 操作：生成并按jobId恢复下载
- 预期：文本转义而number保持负数；null状态可区分；同键不重建，当前export重核
- 证据产物：CSV字节样本、数据字典、job查询记录
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M32-10

- 需求：M32-SPEC-06。
- 给定：当前15全部生产者目录，R2/R3适配未接，33暂缓映射存在
- 操作：逐目录查数据
- 预期：全范围保留，未接明确not_configured/unavailable；不生成模拟业绩、不算真实联调，暂缓不恢复引擎
- 证据产物：producer capability目录与逐项联调状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

## 全包一致性补充

本任务随最终评审补齐的字段、状态、旧验收优先级和迁移边界，统一见[R1_P2_Consistency_Resolutions.md](R1_P2_Consistency_Resolutions.md)。这些是设计自检修正，不重开P1批准或重做任务。

## 本阶段执行边界

本任务只修改P2设计及一致性材料；未运行产品测试、迁移、备份恢复、外部交易或原站操作；不改变业务代码、数据库、部署、访问者及主事实源。所有技术默认均为设计参数，不能覆盖已批准业务规则。
