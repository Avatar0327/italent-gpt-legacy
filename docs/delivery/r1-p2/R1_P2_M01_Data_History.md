# M01数据、稳定身份与有效历史设计

任务：R1-P2-02。状态：设计完成，待独立评审；不是P2批准或P3验证。

## 批准依据与版本

基准源码/事实源：`716cd9df5f5776d050f77f57c2ad5a35c0a83882`。批准需求：`D1`、`D2`、`D3`、`D4`、`D5`、`D6`、`D7`、`F-SPEC-01`、`F-SPEC-02`、`F-SPEC-03`、`F-SPEC-04`、`F-SPEC-05`、`F-SPEC-06`、`F-SPEC-07`、`F-SPEC-08`、`SCOPE-DEP-01`、`M01-BASELINE-01`、`BP-F-REQ-01`、`BP-F-REQ-02`、`BP-F-REQ-04`、`BP-F-REQ-05`、`BP-F-REQ-06`、`BP-F-REQ-10`、`BP-F-REQ-11`、`BP-F-REQ-12`、`BP-F-REQ-13`、`BP-F-REQ-14`、`BP-F-REQ-15`。批准原文及优先级以 [批准记录](../P1_Approval_Records.md) 为准；原文中的历史待批措辞不重开已批准决定。

## 当前实现与复用判定

- **待修改**：[当前目录、员工与审批模型](../../../lib/hris/model.ts)；基准文件 SHA-256 `0261ebfe42dc0227d7889b9bb4e190f0e4b120d86c9b0093fd497d1b1b7a9480`。Employee只有单orgId/job/level；目录无有效区间；exit终审即时改状态，必须按F-SPEC-05调整。
- **可复用**：[D1至D7执行快照](../../../lib/hris/personnel-transfer.ts)；基准文件 SHA-256 `5eba784136a5682dab2557322525446a392dc170b09c6f4ead2d68208ac190a6`。source/target、eligibleAt、waiting/failed/applied/cancelled和实际执行字段保留；新增事项归因与任职ID。
- **待修改**：[编制与合同](../../../lib/hris/workforce.ts)；基准文件 SHA-256 `63ea24a9d415d9036f90c4e81da748035495bf4e334c57f454293f4e98f7855a`。当前占用按员工单岗位，法人自由文本；renewalOf只要求晚于旧结束，须改为同法人且相邻日。
- **可复用**：[合同字段](../../../lib/hris/contract-fields.ts)；基准文件 SHA-256 `d4285a1633739adf695fb28c8b82a99d2233d3d46e519007cd4fc391dea9d514`。20项/组织、文本1000字、继承与显式null保留；新版本必须保留原root及来源。
- **待新增**：[人员经历](../../../lib/hris/employee-experiences.ts)；基准文件 SHA-256 `c6ac695274484fc9cc38c85a15ff258c7bdb52688cc680538c60cc2c46572558`。三类固定经历扩为十类加自定义子集，模板版本和导入逐行回执缺失。

## 对象关系、主键与字段

所有下列表的逻辑主键/外键都带tenant_id，id为服务端生成的不透明UUID文本（旧ID原样保留），revision为非负安全整数，日期严格YYYY-MM-DD，时刻RFC3339 UTC；显示统一北京时间。下表是逻辑设计，P3再写DDL，不在本轮建表。

| 对象 | 关键字段与关联 | 不变量/索引 |
|---|---|---|
| person | personId=旧employee.id；code、name、身份核实来源、profileRevision | 工号按既有精确唯一；手机号/邮箱不唯一身份键；(tenant,personId)永久不复用 |
| identityEvidence / identityReview | personId、identifierType、受保护值/摘要、候选ID、reviewer、reason、status | 原始证件不进公开索引；多候选冻结提交；复核权限交M01管理员/授权HR，当前只设计不查真人 |
| employment | employmentId、personId、hireEventId、employmentType、startOn、lastWorkingOn、status、predecessorEmploymentId | 同人多段雇佣；状态candidate/pending/active/ended/cancelled；首次入职/重聘不是新person |
| assignment | assignmentId、employmentId、personId、type=primary/part_time/secondment/expatriate、homePrimaryId、orgId、positionId、jobId、gradeId | 多任职为独立对象；借派引用派出主职；主职同日唯一；同人同类型同目标有效闭区间不重叠 |
| assignmentVersion | assignmentId、versionId、validFrom/validTo、recordedAt、eventId、supersedesVersionId、approvalId、executionId | 旧行不可修改；当前选择“已执行且未被后续更正取代”的版本；原批准与计划日期独立保留 |
| catalogEntity / catalogVersion | kind=org/position/job/job_family/grade/legal_entity；entityId；versionId；code、name、abbr、status、validFrom/validTo、supersedes、recordedAt | 稳定对象与显示版本分离；目录类型分立；有效区间不重叠；旧版本哈希受保护 |
| orgVersion | parentOrgId、city、leaderAssignmentRef、HRBPRef（显式配置时） | parent稳定ID；根parentId为空；有效时点行政树不成环；无映射的历史leader文本保留，不猜人 |
| positionVersion | orgId、jobId、familyId、gradeMinId/MaxId、parentPositionId、dottedParentPositionId、establishedOn、effectiveOn、responsibilities、newType、keyPosition | 设立日≤首次生效日；职级上下限同适用序列且min≤max；New/Backfill保留枚举，不转布尔；未配置关系不默认开放权限 |
| legalEntityVersion / legalScope | legalEntityId、code/name/abbr、有效期；orgRootIds/includeDescendants、extraPersonIds | 空范围=未配置；适用人=(组织集合∪附加人员)∩操作者数据权；停用禁新引用；旧合同快照不漂移 |
| workforcePlan / occupancyEvent | planId/positionId、start/end、headcount、supersedes、approval；assignmentId/personId、delta、effectiveAt、eventId | 已批准同岗位同期间版本唯一；主职1，兼职/接收借派0；派出主职仍1；增量占用与生效同事务 |
| contract / contractVersion | contractId、personId、legalEntityId、legalVersionId、agreementCategory、contractType、number、start/end/endedOn、signedOn、renewalOf、evidenceRef、fieldSnapshots | 一份合同多版本；编号按旧规则不分大小写唯一且作废不释放；同人同法人重叠已签合同仍拒绝；新版本不重复计次 |
| subsetDefinition / templateVersion | subsetId、kind、字段类型/权限/必填/default/uniqueKey、definitionVersion；entryType=employee_create/prehire/onboard | 十类教育/工作/家庭/考核/培训/奖励/证书/项目/技能/语言及custom；三入口独立模板，无配置字段不猜默认 |
| subsetRecord / importRow | recordId、personId、subsetId、versionId、payload；batchId、rowNo、digest、resultId、status/error | key=(person,subset,已声明字段精确trim值)；批次行幂等；记录历史不可覆盖 |

普通人员字段仍沿旧输入边界：code/name/orgId/job 1–100字；level≤100；email为空或合法邮箱；组织name/city 1–100、leader≤100；position code/name/orgId/family 1–100、职责≤4000；grade sequence整数0–999。这些兼容字段不替代新对象ID。新模板未声明的类型、默认、范围或读写权保持未配置，发布模板必须补全明示约束；不能据北森样本把所有员工入口邮箱改成必填。

## 有效时间、记录时间与不可覆盖历史

- 人事业务有效日期是北京时间自然日闭区间[from,to]；open-ended表示未确定结束，null不等9999日期事实。区间重叠判定：a.from≤b.to且b.from≤a.to（空结束仅在比较时视为无穷）。相邻合法区间后一段from=前一段to+1天。
- 目录发布新增版本从北京时间当天或未来生效，不能直接回填过去；按版本有效日期投影。历史更正用correction事件引用旧version及理由/证据，新版本记录本次recordedAt，不改旧行。若业务追溯调整需要新增政策，进入决策队列，本设计不默认追溯。
- 调动D1仍保留effectiveOn/eligibleAt/approvedAt与appliedAt；成功任职事实以实际执行时刻为准，延迟执行不倒写员工已在计划日调入。按日统计取实际appliedAt的北京日，完整时刻历史用于同日多变更顺序；日末在职/占用唯一，不把同日操作事件数当任职人数。
- 任职版本另保留计划区间与appliedAt，未执行版本不能在当前人事投影中自动成为事实。离职最后工作日次日为计划生效边界，到期授权HR执行；延期执行必须明确“计划离职/待执行”，当前授权先依成员停用/关系到期收紧，不能据计划推定业务已完成。历史报告若请求计划日实际状态，按已知事实/未知区分，不回溯编造。
- 退出、编制释放、任职结束、权限失效和各在途业务逐单取消的事实分开；领域对象事件不可删除。没有可靠历史起止/类型时标historyQuality=unknown并保留legacyObservedAt；不从joined一字段编造所有任期。

## 目录唯一性、关系与停用算法

编码trim后区分大小写、全目录唯一；职位name trim后在同组织且有效区间重叠时唯一，跨组织允许；职级名可重复但显示编码。组织沿现有同父名称唯一，按版本覆盖全部受影响有效区间切点校验，而不是只核今天。职位/组织树校验并集有效区间每个切点，防未来A→B、B→A形成时态循环。目录改名/改归属也检查前后区间，不只新建检查。

停用在拟生效时点读取依赖：有效人员任职、启用下级/岗位、pending及approved-waiting/failed和其他未完成引用；任一阻断。已结束引用保留当时快照。无权依赖仅显示“存在受保护依赖/联系相应负责人”，不暴露人数/姓名/组织名称。依赖查询与提交用同revision；并发新增引用会使CAS失败，不能先查空再无锁停用。

## 人员新建、再入职与纠错边界

新建人员草稿与待入职employment分别保存，发起/批准/办理入职状态分列；member创建/平台邀请都不是保存副作用。普通员工编辑继续禁止绕过任职变化申请。转正保留既有合法试用前置和模板审批，不把调动固定两级套到转正。

再入职：提供可读历史人员ID及identityReviewId→核实身份→新employment/predecessor→独立assignment申请/审批/HR执行。多个标识冲突返回IDENTITY_REVIEW_REQUIRED与权限安全caseId，不自动挑人/合并；同幂等键同内容复用结果。手机号/邮箱仅候选线索；稳定person保持，账号/角色/字段权不恢复。错误链接若尚未执行可取消草稿并留事件；已执行不允许批量重绑/物理合并，先冻结受影响后续办理并提交有来源的纠错提案，当前无自动不可逆merge命令。

司龄按经确认的非实习任期自然日含首尾、区间并集去重累计；离职间隔排除、闰日1天、退休返聘前任期计入；存days，展示round(days/365,2)。活动任期只累计至asOf；缺开始/结束（应已结束但无结束）或身份冲突为待核，不能补0。权益/法定口径和薪资另由生产者处理。

## 任职、调动、离职与编制事务

D7调动仍HR覆盖A+B发起→调出审批者→不同调入审批者→approved/waiting→到期授权HR执行；申请人/员工本人不得审批，职级变化前后值必须可见，模板禁止分支/会签/委托/转交/干预。sourceAssignmentId/sourceVersion冻结到原单，并核旧快照匹配。

新建/变更/结束主兼职、借调/外派由范围HR申请，另一覆盖相关组织的HR独立审核，不复用调动两级；审核者不得为申请人或员工本人，未配置合格人阻启动。所有类型起止和实际执行分开，借调/外派不隐式覆盖主职。

execute事务：当前权限与日期→原单approved且waiting/failed→原任职版本未变→目标目录时态/占用→单一CAS写execution、任职新事件/日投影、编制delta、主档兼容投影、审计/outbox/回执。可提交业务失败只记failed/attempt/reason，人员历史/占用不变；提前/非法/越权不增attempt；CAS409、DB503或断网未知先查原命令/原单，不承诺同故障事务留痕。

离职有界执行：事务写person的业务退出事实、employment/assignment终止事件与“effectiveAt后不再有效”的全局屏障、占用释放、审计/outbox；不用在一个Worker事务枚举无限在途原单。屏障使全部后续提交即时拒绝；独立有界cancelWork逐单调用原域取消适配并留原因/失败。业务不支持安全取消的原单保持历史及blocked_by_exit，责任转原域核销；不伪称已取消。未生成逐单回执前，退出详情显示“人员已退出、关联事项清理中/失败”，不静默成功全部。退出与审批竞争受同租户CAS及exitFence约束。

F-SPEC-03：新事项intent=independent|correction，correction必须previousApprovalId同人同类可读终态并一级重审；independent需独立原因，不因任意历史终态强绑。pending或approved/waiting/failed互斥始终执行。新建编制0–100000、已批准同岗位区间不重叠；调整须同岗位同期间最新批准单。减少占用不因原已超编而阻断。金额预算未接显示not_checked；若现企业已配置强阻断而服务不可用，该链返回EXTERNAL_BUDGET_REQUIRED，不冒通过，不启M09。

## 合同与字段版本

法人空范围禁新合同引用；启用合法法人快照绑定contractVersion；停用/改名不改变旧显示。续签需同person、同legalEntity、有效旧已签/终止合同且new.start=coalesce(old.endedOn,old.end)+1日；间隔合同可作为独立合同登记，不伪标续签。签署登记日期不得未来、合同日期和fixed/open校验保留；协议类型未知历史不自动推成labor，未知计次不混入数字。

计次=count(distinct contractId)，分组person+legalEntity+agreementCategory，status signed/ended纳入、cancelled排除；改版一次、重聘累计。合同终止保留现有独立办理与本人/创建人限制。第三次自动转无固定、到期自动终止保持关闭；只能未来明确政策版本启用。人工signEvidence是登记事实，externalSigningStatus可为not_configured，绝不宣称已电子签。

合同字段继续20项/组织、文本≤1000、rootId/version/code/sourceContractId/sourceFieldVersion；省略只按当前有效定义及inheritPrevious继承同root旧值，显式null代表清空，归档定义不改历史字段快照。合同附件10MiB与既有MIME集，新增流程/快照归属分别显式objectType，不能通过泛型ownerId绕权限。

## 子集、模板、导入与迁移接口

十类+custom每类独立definitionVersion；字段type=text/number/date/enum/attachment、required/default/uniqueKey/readActions/writeActions必须声明。自定义数值精度/单位由模板显式配置；未定义不转字符串凑成功。新增重复拒绝；显式update且有员工及每字段写权才新增记录版本。batchId+rowNo为幂等键，digest含模板版本/输入/模式；同键异内容冲突，修正失败行用attemptVersion并关联原行；成功行不能被整批重跑覆盖。先预检后逐行事务，返回成功/拒绝/未知，不以HTTP200代表全批成功。

迁移只写方案：保留personId，org/job/level兼容字段为新主职投影；无positionId的job文字保留legacy_unmapped，不按名字自动建同名目录；法人文本需映射清单人工复核，未知保留。完整批次、中断与回滚见第07设计。索引建议：(tenant,personId,type,validFrom)、(tenant,orgId,validFrom,entityId)、(tenant,code)、(tenant,legalEntityId,personId,agreementCategory)、(tenant,batchId,rowNo)；区间冲突仍需在同CAS内校验，不能假称普通唯一索引可处理区间。

## 正常与失败场景及P3建议

以下仅为可执行验收设计，全部未运行。P3须在P2退出获批后使用隔离合成数据；P4独立人类角色和生产验收不由本表替代。

### P3-M01-01

- 需求：F-SPEC-01、F-SPEC-08、BP-F-REQ-01、BP-F-REQ-10、BP-F-REQ-11。
- 给定：A/B组织各职位J同名不同码，A内历史已结束同名，未来区间交叉
- 操作：分别建A重叠、B同名、A不重叠版本，再构造未来上下级环
- 预期：拒绝A重叠及未来环；允许B与不重叠名称复用；ID不复用，职级重名显示编码
- 证据产物：时间切点表、版本行和拒绝回执
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-02

- 需求：F-SPEC-04、BP-F-REQ-04。
- 给定：两个历史person各命中一个标识，另有已核实人任期跨闰日且账号撤权
- 操作：先冲突重聘，再用经核实身份重复同键入职
- 预期：冲突不合并；确认后同person新增单一employment；累计任期去重不含间隔/实习，账号不恢复
- 证据产物：identityReview、任期天数手算基准、幂等与权限差分
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-03

- 需求：F-SPEC-05、BP-F-REQ-06、BP-F-REQ-13。
- 给定：主职A满1，兼B、借派C；有效期各已批准，另一个HR审核
- 操作：执行兼职/借派；尝试同类型同目标重叠；再调动主职到满编B
- 预期：兼/接收借派占0而A占1；重叠拒绝；满编调动failed且历史/占用不变；减少占用可执行
- 证据产物：占用事件、assignment版本及事务对比
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-04

- 需求：D1、D2、D3、D4、D5、D6、D7、F-SPEC-02、BP-F-REQ-02。
- 给定：A到B未来调动，申请HR覆盖A+B，两个独立审批人，第二人只B
- 操作：越级/自审/撤viewLevel/过期批准/提前执行分别尝试，再合法批准到期执行
- 预期：均按D1–D7拒绝非法操作且提前不增次数；第二人只原单必要摘要；合法终审只waiting，到期HR一次applied；不能自动执行
- 证据产物：审批/执行三时间、字段投影及历史增量
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-05

- 需求：F-SPEC-02、D1。
- 给定：到期已批准单目标业务失效，第二样本审计写入异常，第三样本响应丢失
- 操作：执行后查同commandId/approvalId
- 预期：业务failed可提交并记次数；审计失败全回滚；未知先查一次成功结果不重复任职/占编
- 证据产物：数据库提交边界、客户端未知回执和query结果
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-06

- 需求：F-SPEC-03、D2、D6。
- 给定：员工有无关历史终止调动且无在途；另有需要改日的原单
- 操作：提交independent与correction；并发再开第二在途
- 预期：independent可新建且理由留痕；correction必须有效可读原单并两级重审；并发一单成功一单拒绝
- 证据产物：事项ID、原单关联、CAS与审计
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-07

- 需求：F-SPEC-06、BP-F-REQ-05、BP-F-REQ-14。
- 给定：法人空范围/后启用/改名/停用；合同C1已签，C2重聘后续签
- 操作：尝试空范围新引用、跨法人续签、隔日续签、合法相邻续签、同合同改版
- 预期：前3拒绝；合法续签保旧法人快照；改版计次一次；无协议历史待核；第三次自动政策关闭
- 证据产物：合同/法人版本、计次明细、人工登记/外部状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-08

- 需求：F-SPEC-07、BP-F-REQ-06、M01-BASELINE-01。
- 给定：十类与custom字段模板齐备，新增/待入职/入职模板不同；已有子集行且某字段不可写
- 操作：显式update导入混合成功、拒绝、响应丢失行并重跑批次
- 预期：成功行一次；无字段权逐行拒绝；未知查原行；显式null不被默认或继承吞掉，所有旧版本保留
- 证据产物：batch行回执、template版本、记录前后哈希
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-09

- 需求：BP-F-REQ-12、F-SPEC-07。
- 给定：未配置待入职模板必填/默认，另有完整模板且invite=false
- 操作：先提交不完整模板，再保存person/prehire并办理入职
- 预期：缺模板配置阻发布/提交且理由明确；三个ID和状态分列；无外部邀请/无新增访问者
- 证据产物：入口模板快照、person/employment/approval关联、消息拦截记录
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-10

- 需求：BP-F-REQ-15、F-SPEC-05。
- 给定：最后工作日D，主兼任职各1且有101个在途事项，部分域不支持取消
- 操作：D+1授权HR执行并并发审批，清理任务中断重启
- 预期：退出屏障原子生效，后续审批拒绝；逐单清理进度/失败可追踪，不删历史或称全部成功；重复不重复释放编制
- 证据产物：exitFence、101项cancelWork、失败适配回执
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-11

- 需求：SCOPE-DEP-01。
- 给定：已有人数编制规则；金额预算未配置和企业显式强阻断两种夹具
- 操作：分别办理入职/占用
- 预期：未配置显示未校验；强阻断依赖缺失则该链拒绝，不以人数通过冒充金额通过
- 证据产物：金额检查status/原因和编制delta
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-M01-12

- 需求：F-SPEC-08、BP-F-REQ-10。
- 给定：目录拟停用，有当前HR不可见的approved waiting引用
- 操作：停用并同时新建引用
- 预期：拒绝且仅受保护依赖摘要；并发防漏；历史快照哈希不变
- 证据产物：停用拒绝脱敏结果、CAS、版本哈希
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

## 本阶段执行边界

本任务只修改P2设计及一致性材料；未运行产品测试、迁移、备份恢复、外部交易或原站操作；不改变业务代码、数据库、部署、访问者及主事实源。所有技术默认均为设计参数，不能覆盖已批准业务规则。
