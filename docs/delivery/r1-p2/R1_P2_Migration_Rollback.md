# R1 P2增量迁移与回滚设计

任务：R1-P2-07。状态：设计完成，待独立评审；不是P2批准或P3验证。

## 批准依据与版本

基准源码/事实源：`716cd9df5f5776d050f77f57c2ad5a35c0a83882`。批准需求：`BASE-01`、`BASE-02`、`BASE-03`、`BASE-04`、`BASE-05`、`F-SPEC-04`、`F-SPEC-05`、`F-SPEC-06`、`F-SPEC-08`、`M01-LIMIT-01`、`M19-LIMIT-01`、`M48-LIMIT-01`、`M32-LIMIT-01`。批准原文及优先级以 [批准记录](../P1_Approval_Records.md) 为准；原文中的历史待批措辞不重开已批准决定。

## 当前实现与复用判定

- **待修改**：[规范化迁移与CAS](../../../lib/hris/repository.ts)；基准文件 SHA-256 `d29c455ce153d7231728c7821d3571ad92ae60edf6b1811d478dcb6a2f1a1249`。原storage_version=1守卫必须兼容；全量读取/写入不能用于无界回填。
- **可复用**：[最新已登记迁移](../../../drizzle/0009_spotty_redwing.sql)；基准文件 SHA-256 `215b7578ceb3213235fc80d6aab2c7792d02dbcccfd67fd116450db3a0dab858`。approvals.details增列必须纳入版本清单。
- **受限**：[历史恢复说明](../../../docs/Recovery_Rehearsal.md)；基准文件 SHA-256 `325fa3054d03a99be4261a048a6cdcfda49a374a5218e4b7cd276abd0da94088`。历史合成演练不是本轮验证，更不证明生产云端容量。

## 迁移对象、版本与事实边界

延续[总体架构](R1_P2_Architecture.md)、[M01对象](R1_P2_M01_Data_History.md)、[接口](R1_P2_Interfaces_Exceptions.md)。启动基线包括 `drizzle/0000` 至 `0009`，不是历史演练仅到0008的版本。2026-09-09通过Sites只读数据库概览确认DB绑定返回19张业务表、未截断；该接口没有提供行数、字段、容量或迁移日志。因此只能证明表名集合存在，不能继承历史空库结论，也不能断言0009已执行。本轮不扫描真实人员行。

现有 `storage_version=1` 是旧写入CAS前置条件，不能直接升为2。新增独立 `r1_schema_state(tenant_id PK, schema_version, writer_epoch, phase, source_revision, verified_revision, features_enabled, revision)`；DDL版本由平台迁移清单记录，租户业务回填版本由此表记录，两者不能混为一谈。全部新对象采用tenant复合外键，旧 `memberships.user_id`、`access_grants.email` 的全局主键暂保留；不借迁移改变成员跨租户限制。

新增迁移控制表为**业务迁移实施设计**，不是第二套项目范围事实源：

|对象|键及关键字段|不可破坏的约束|
|---|---|---|
|migration_run|tenant+runId；planVersion、源码SHA、DDL摘要、phase、expectedEpoch、cursor、leaseUntil、fence、counts、manifestDigest|同租户只一有效写入迁移；租约接管递增fence，过期执行者不能推进|
|migration_map|tenant+sourceTable+sourceKey+mappingVersion；sourceRevision、sourceDigest、targetKind/Id、confidence、issueId|同源同版本唯一；同digest重入无效果，源变化重读；一对多目标用子映射ordinal唯一|
|migration_issue|tenant+issueId；原始引用、reasonCode、影响对象/动作、解决人、证据、revision|unknown/conflict不自动合并，不向无权人员暴露原始敏感值|
|migration_batch|runId+phase+cursorDigest；from/to、rowCount、input/outputDigest、fence、commitId|目标写入、映射、批次回执、游标在同一D1事务提交|

所有原快照、审计、合同附件、审批签名与事件历史保持不可覆盖。迁移产生 `migration_observation`，不冒充过去的业务动作；`recordedAt` 为实际回填时间，`validFrom` 缺证时null并标 `unknown_before_observation`，不得以1970年、入职日或迁移日替代未知有效开始日期。

## 旧字段映射与兼容读取

|旧来源|新目标及确定性映射|未知/冲突处理与兼容边界|
|---|---|---|
|employees.id/code/name/email|personId保持原id；code为可变外部业务编号；资料初始观察版本保留原值及摘要|不按姓名/手机号/同名工号自动合人；多标识命中不同人进入identity_conflict，限制重聘执行|
|employees.joined/status|employmentSegment初始迁移段，以migration_map固定生成ID；joined作为已知入职字段证据|单个日期不能推算全部历史司龄；历史中断、实习段未知则司龄显示不完整，不给精确合计|
|employees.org_id/job/level + employee_positions|当前主职assignment的已知组织/岗位/职级引用；字符串原样保存legacyLabel|position/grade真实ID存在才链接；名称相同不自动映射。非主职段缺证不生成；缺起始日期仅当前兼容投影可读，未经HR核证不能用于追溯时点判断|
|orgs/positions/grades|稳定目录ID原样复用；已知当前状态形成observed版本；新增职位有效唯一规则|旧重复名称、循环、失效引用记录issue；不改名、不删引用；相关新增/变更拒绝，其他组织继续迁移|
|employment_history|原id/event/at/from/to/actor原样保留并链接personId|at是记录/执行证据，不当然等于业务有效日；缺from字段不补造；原actor未知保持legacy-unattributed|
|workflows/workflow_steps|kind+version冻结模板映射，实例保留实际步骤快照|历史模板缺失只保留instance快照，禁止重新选最新模板；需要重新路由须新申请版本|
|approvals/steps/assignment_requests/details|approvalId保持；流程decision、业务execution及notification分列；原单链保留|completed仅有审批事实不能推定所有外部后效成功；原业务证据不足标unknown，禁止重执行终态；D7旧两节点和权限保持|
|development_records/events中的合同|contractId/版本/签署状态保留，雇主文字另存legacyEmployerLabel|有明确法人ID才映射；缺证由合同负责人核验，不以同名法人猜测。计次按已确认person+法人+类别；未知项提示不完整|
|memberships/access_grants|原账号绑定、active、角色、orgScope、viewEmail/viewLevel保留；转换为显式grant tuple|不能把manager旧角色自动授权所有关系；不新增export/subscribe/manage；admin兼容权仅原既有对象，新增敏感能力须显式授权|
|attachments|原key、owner引用、visibility、size、类型、deleted状态；版本元数据和digest按实际对象校验补齐|缺对象/摘要不符进入quarantine，不建立“可下载”新版本；墓碑不消失；原始字节不修改|
|development其余记录/报表快照|保持生产者原ID、rawStatus、revision、版本化映射；快照按原manifest读取|未发布更正不覆盖已发布结果；缺快照数据不可用当天当前值填过去；未知状态禁动作|
|workspaces.data (storage_version=0)|保存原JSON摘要及只读归档；验证结构后按明确旧迁移路径转规范化1，再进行R1回填|不能先改storage_version使旧JSON失去读取路径；旧迁移异常不推进R1阶段|

兼容读遵循每对象 `migration_map + sourceRevision`：verified且新投影完整时读新；否则读受当前权限裁剪的旧投影并显式 `legacy_partial`。一次查询固定schemaEpoch与workspaceRevision；混合新旧若无法证明同一修订则409重读，不双计同一person。列表稳定游标包含版本/权限摘要。旧客户端只得到当前主职投影及 `additionalAssignments` 数量，不接收无权兼职详情；旧全对象PUT不能抹除新字段，所有写入经命令适配器，未映射对象与不可表达动作返回 `UPGRADE_REQUIRED` 或 `MIGRATION_CONFLICT`。

## 扩展、回填、切换与中断状态机

`inventoried → expanded → writers_guarded → backfilling → reconciling → read_switched → features_enabled → monitored`；各阶段可paused/failed，按最后已提交批次接续。不是“启动即完成”。

1. P3隔离环境先采集实际DDL/迁移列表、19张及新增表行数/主键摘要、孤儿、租户分布、业务版本、附件清单、DB字节和待办分布。真实生产只在P4安排获批后执行；证据受限访问，设计文件只存摘要，不录真实个人数据。
2. 创建只增不删的新表/索引及空控制记录；先核DDL摘要与现存同名表，存在但不兼容返回 `SCHEMA_DRIFT`，禁止 `IF EXISTS` 掩盖不同定义。DDL本身单独可重入、记录成功，不假设所有DDL在业务事务内回滚。
3. 发布桥接写入器前默认新功能关闭。所有Web/API/定时任务/管理/上传/生产者入口在**同一租户CAS**检查writerEpoch、authRevision和迁移状态；所有旧实例失去写权。旧版本不能理解新epoch时必须由路由/维护写闸门挡住，不能只依赖新代码自觉检查。P3证明覆盖率100%后才回填。
4. 桥接写入器对可表达字段在同事务双写旧投影、新对象、映射及恢复日志；不采用两个独立事务的“最终补齐”。未回填对象先按映射规则建立最低当前版本再写，历史未知仍保留。不能安全映射时仅该对象写阻断，其他对象继续。
5. 按固定主键键序、有界批次回填（默认100行、每事务≤80条语句，实际低者优先），不用OFFSET。源内容、revision和digest在CAS提交时核对；并发变化则本批不提交，重读新源，不覆写新事实。批量插入分块使D1参数/SQL长度受控，边界由P3实际限额测试确认。
6. 对账无关键差异且恢复检查点可用，按租户切读；先观察旧读/新读的可见对象及字段集合差异。差异只存去标识计数/摘要，不绕过当前权限“影子回显”。
7. 启用前HR确认未解决issue只影响哪些局部功能；未完成身份/法人/历史核证的对象保持有明确原因的受限动作。不能为赶进度填默认日期、默认法人或自动合并。
8. 最后进入监测；旧字段保留，删除旧列不纳R1本方案。任何清理另走变更评审和可恢复性证明，30天恢复目标不是业务历史只保留30天。

## 对账、异常与回滚边界

验收至少比较：源到目标1:1/1:N映射覆盖及唯一性；全部源历史哈希不变；主职有效区间互斥和占编1/非主职0；合同版本/计次；原审批节点、终态、D7链；当前账号与字段授权；附件引用/墓碑/字节；21报表行键和授权范围内聚合；R2/R3未配置时显式状态。不能以总行数相同代替逐键对账。

|故障/阶段|恢复动作|不可执行边界|
|---|---|---|
|事务失败/数据库不可写|该批全部无效；外部监测记录runId/批次，不承诺DB必有失败审计|不先推进cursor，不转业务成功|
|网络超时结果未知|查询batch回执及run revision；已提交续下一批，未确定只复用同批idempotency key|不新建run重跑全部，不凭无响应删新表|
|worker中断/租约过期|新执行者CAS取得更大fence，从最后回执恢复；旧fence所有写拒绝|不依赖进程内锁|
|source revision冲突|读最新源重新计算该批；累计冲突过限暂停该分区并告知迁移负责人|不修改旧revision绕过CAS|
|expanded/回填阶段回滚|关闭新读/功能，保留所有新增表/映射；桥接写入器继续保护数据，回到兼容读|不DROP表，不回退到不识别epoch的旧写入器|
|新能力未启用且无新事实|经新旧逐键对账，可在保持写闸门下切回已验证桥接版本|不是任意历史代码都安全|
|已出现多任职/新合同版本/新路由|采用前向修复或新模型兼容只读；需恢复时使用隔离恢复方案并保留恢复点后的命令/回执供对账|禁止旧程序写覆盖；不可无声丢弃切换后有效业务|
|待办恢复/外部结果未知|保留instance版本/receiptId，建立出站恢复fence，先对账后恢复调度|不重新发支付/签署/订阅，不重放已处理节点|

执行责任：迁移实施负责人编写P3迁移器和合成夹具；数据库负责人执行/保留批次证据；数据HR负责人核身份/法人/历史；安全复核人核当前权限；所有者批准P4生产切换。设计不预先授予生产执行权。

## 正常与失败场景及P3建议

以下仅为可执行验收设计，全部未运行。P3须在P2退出获批后使用隔离合成数据；P4独立人类角色和生产验收不由本表替代。

### P3-MIG-01

- 需求：F-SPEC-04、F-SPEC-05、F-SPEC-06、F-SPEC-08。
- 给定：含旧JSON租户、规范化租户和未知有效日期/同名法人
- 操作：分批回填两遍
- 预期：personId不变、未知不猜测、确定性映射不重复，源历史摘要不变
- 证据产物：隔离迁移逐键差异和源/目标manifest
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-02

- 需求：BASE-03、M01-LIMIT-01。
- 给定：100行源在回填中并发变更，某批提交后丢响应
- 操作：中断、接管、重复同批请求
- 预期：CAS失败无半批、结果未知查回执，旧fence拒绝，cursor不漏不重复
- 证据产物：批次回执/租约和故障注入时序
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-03

- 需求：BASE-01、BASE-02、M48-LIMIT-01。
- 给定：迁移前后有撤权账号与仅直线权经理
- 操作：读兼容投影和写旧API
- 预期：撤权保持，字段和关系授权不扩大，新能力无默认授权
- 证据产物：双投影授权集合对账
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-04

- 需求：BASE-04、BASE-05、M32-LIMIT-01。
- 给定：21数据集、合同/快照附件、墓碑、缺对象
- 操作：切读并比对逐键及附件摘要
- 预期：不双计、不填补假历史、损坏对象隔离、缺快照不可用
- 证据产物：21数据集oracle与对象manifest差异
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-05

- 需求：M19-LIMIT-01、BASE-03。
- 给定：D7一审在途、终态审批、外部结果未知
- 操作：迁移/恢复后查询并重复旧请求
- 预期：模板/节点签名保持，终态不重放，未知外部调用不盲重试
- 证据产物：审批实例/命令回执前后对照
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-06

- 需求：BASE-05、F-SPEC-05。
- 给定：切换后新增多任职，旧客户端只有org字段
- 操作：要求回退与旧PUT
- 预期：旧写被挡，前向修复/兼容只读保全新事实；无drop操作
- 证据产物：回滚演练方案执行记录与不丢事实校验
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-MIG-07

- 需求：BASE-05、BASE-03。
- 给定：实际DDL偏离0009或某旧写入口未受epoch控制
- 操作：执行前置核查
- 预期：SCHEMA_DRIFT/WRITER_NOT_FENCED阻止回填，仅修复前置条件后接续
- 证据产物：DDL清单、入口审计和闸门结果
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

## 本阶段执行边界

本任务只修改P2设计及一致性材料；未运行产品测试、迁移、备份恢复、外部交易或原站操作；不改变业务代码、数据库、部署、访问者及主事实源。所有技术默认均为设计参数，不能覆盖已批准业务规则。
