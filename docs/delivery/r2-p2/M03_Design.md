# M03干部管理2.0详细设计

依据M03-SPEC-01～06、BP-C-REQ-01/06及M03-LIMIT-01，批准`M03-P1-APPROVAL-20260910`。任命决定、M01实际人事生效、干部任期确认是独立事实；本设计不批准任何真实任免。

<a id="m03-spec-01"></a>
## 干部身份、任期与日期

|对象|字段与主键|约束|
|---|---|---|
|cadre_identity|cadreId、personId、legacyStaffId/sourceNamespace、identityState/version|person沿M01稳定ID；StaffID数字不强转UUID、不按姓名合并|
|cadre_term|termId、cadreId、appointmentRecordId、employmentRecordId/assignmentId、typeVersion、org/positionVersion、startOn/endOn、actualEndedOn、approvalRef、effectReceiptRef|主职同人有效闭区间不重叠；兼职/挂职等按显式类型与M01任职契约，不强制所有任期主职|
|appointment_record|appointmentRecordId、decisionId、termId、actualEffectAt、sourceVersion、reconciledAt|同类任用一个sourceEffectReceipt只能用一次；决定/任期/任职ID不同|
|term_change|changeId/version、kind=renewal/dismissal/retirement/employee_exit/void/correction、reason、effective/recorded dates、independentApproval|保留原任期和来源，不删历史或回滚M01|

员工状态、干部身份（在任/免职/离职/退休等已知语义）与term planned/active/ended/voided分列，legacy registered保留登记事实。干部身份转态依据独立干部决定及所需M01真实凭证，不能因任期到日或某个考察通过自动改员工状态；多任期时不得单个任期结束覆盖仍有效其他任期。

期限输入正整数month/year或显式openEnded；计算版本`calendar-clamp-then-minus-one-day-v1`：北京时间start日先加月/年，目标日不存在先夹至目标月末，再减一日。2024-02-29+1年→2025-02-27；2026-01-31+1月→2026-02-27；2026-09-09+1年→2027-09-08。保存前预览计算结果/算法版本，授权者可explicitEndOn+reason覆盖，保留计算值和覆盖值。不使用固定365天，未知历史不套算法补日期。observation start≤due且due≤固定任期end。

<a id="m03-spec-02"></a>
## 选拔、提名、任免批准与生效

selectionActivityRoot/version冻结position/type、eligibilityPolicyVersion、M37/M06/M17来源要求、evaluationTemplateVersion、reviewerSet和M19 workflowVersion。nominationId/applicationVersion、evaluationInstanceId、appointmentDecisionId、termId分开；同person+targetKind/targetId只有一在途提名（含approved未生效/failed），拒绝/撤回后新提显式previousNominationId。本人、发起人及历史实质候选材料贡献者回避评审。

eligibilityPolicy对每项资格/后备明确required/reference，不配置required内容则not_ready；提名、批准、实际核对生效前分别保存新鲜M06 validity和M17 currentAvailability证据。reference缺失可明示继续业务审议，required expired/revoked/unknown阻该动作；不按旧快照或裸分默通过。M18/M26仅在用途许可下作证据，不自动任用。

nomination draft→submitted→under_review→approved/rejected/withdrawn/cancelled；appointmentDecision approved后effect waiting/waiting_external/applied/failed/blocked分列。涉及调动：引用同人/同目标、时间链合法、严格D1–D7审批及actual applied的M01 sourceEffectReceipt，核当前assignment确实匹配；一张receipt在同任用类型唯一，不可多次“核对”生两个任期。无须改变主职的类型必须有对应已授权M01任职事件，不造一个假调动满足字段。

M03提交核对时在同DB CAS内重核sourceVersion、资格有效性、当前人员/岗位/权限、重复receipt及term区间，然后写appointmentRecord/term和审计。M01已实际变更、M03因资格过期而blocked时保留两域真实差异，交任免负责人对账/独立纠正，不自动撤销M01或捏造M03已任命。远端生效回执无法核真实新鲜状态为unknown，不能降级approved即applied。

免职、退休、员工离职原因结束、续任、错误作废分别独立申请/批准及actualEndedOn；离职原因需要可信M01已退出事实，免职不等员工离职。续任新term+previousTermId（相邻或明确区间，不重叠），更正新version，不修改旧批准。void只标错误登记无效并保留证据，不能用作回滚已生效人事。

<a id="m03-spec-03"></a>
## 委员会和精确评分

evaluationTemplateRoot/version冻结mode=vote|total_score|indicator_score三者互斥、indicator/qualification versions、eligibleReviewerSet、recusalRefs、scale/weight/threshold/comparator及aggregationVersion；参考分不改变主模式判定。提交时、节点激活及最终决定分别核回避，缺有效评委阻流程，不由admin代所有评委。

投票ratio=passVotes/expectedEligibleReviewers，显式通过比例0<r≤100，精确ratio≥r；不默认80。经批准回避者移出分母，弃权仍在分母且非通过；缺席/未提交先判incomplete阻决议，不当弃权也不缩分母。例5人中1已批回避、1弃权、3通过：有效分母4，3/4=75%，阈值75%可通过；若1人未交则即使当前票数达到也不能最终决定。

评分每项明确min/max/step/unit/direction/allowedSet，均值、加权均值、加总三选显式；跨尺度先有转换版本。weight有限≥0且实际参与集合权重和>0，缺weight阻加权模式ready，不补0/平均。每评委必需项缺分阻其完成；计算每位评委总分后，跨全体应评有效且已完成评委按算术均值聚合。无评委/无指标/零权重为unknown阻通过，不除0；强制资格/否决项仍不能被平均掩盖。

decimal精确比较最终分≥显式threshold，显示round到配置位数不影响判断，例如79.995显示80.00仍不满足80.000；等于80.000通过。提交后票/分不可原地覆盖，更正独立新evaluationVersion并保留原决定与参与集合。

评分项可组成显式groupId/parentId树，根/组/叶分别有版本与聚合模式，无环、每个节点只一个父；按模板声明参与/排除集合逐层计算。加权模式每组先以该组参与子节点weight除该组权重和归一化，再聚合已完成子分；任一组缺必需分或权重和0即unknown向上传播，不能只在根把所有叶扁平平均。排除条件/转换版本必须已冻结，不能依据本次低分临时排除。跨评委仍按完成的应评评委最终分算术均值。模板name/org/basicInfo/evaluationTitle、通用评分项或资格指标引用与result visibility分别保存，模板管理不授结果读取。

<a id="m03-spec-04"></a>
## 考察、转正、延期与退出

observationId绑定termId/appointmentDecisionId、startOn/dueOn、objectivesVersion/templateVersion/evaluationInstanceId；active/submitted/returned/passed/extended/exit_recommended分开，overdueFlag按当前时刻派生，不到日自动转正。本人提交或撤回待审，独立评委核验，管理员不能代本人形成自述。

提前转正提交earlyReason及适用minObservationPolicyVersion；政策未配不开放该路径，不擅猜最短天数。延期新due/reason/approvalVersion，不超过固定任期，超界须先独立续任并明确新observation关联，不把旧term end往后抹。未通过可给发展/退出建议，但免职和M01结束另走授权动作，不能从exit_recommended直接改员工离职。

已批考核不可改，纠错新版本重审；员工离职或term实际结束阻新pass/extension，但有权者可终止未完任务并保留原因。过期task不能借恢复回到旧日期而重新允许转正。observation与年度述职不是同一对象，不能因已有考察范围删除年度述职。

<a id="m03-spec-05"></a>
## 周期述职与敏感档案

reportActivityRoot/version含purpose=periodic|observation、cycleId/start/end、termId/templateVersion；reportRecordRoot/version、materialManifest、reviewDecision和publication独立。唯一同term+purpose+activityCycle的报告根；换周期/任期新根，draft→submitted→independently_reviewed→published，return/withdraw/resubmit保留版本，历史来源不可篡改。

archiveSubsetRecordId/type/version分别覆盖基础、任免履历、访谈、奖励、惩处、表彰和附件；每条occurredOn（未知可明确unknown）、recordedAt、source/evidence、approvalState、audiencePolicy。新子集正文≤4000是项目技术边界，不能覆盖已有更窄字段规则；变更说明/理由5–3000沿既有干部证据边界。补录是backfilled_fact、原批准未知保持unknown，不能伪造当时流程。奖励金额/发放只消费授权外部状态、币种/整数分及sourceRef，不生成支付。

访谈独立schema保留employeeId/interviewerId/type/role/date/location/content/evidence：content trim1–200，location≤200，evidence5–3000；type=任前访谈/见习前访谈/见习期访谈，role=汇报上级/隔级上级/HRBP/下属员工/业务关联方，文字是分类而非关系授权。双方当前组织范围都必须满足，interviewer不得等于subject，操作者不得维护本人访谈；不能未来日期，离职人员历史可由当前有权HR登记。更正身份键不可改，错选须作废后另登；旧record和字节保留，作废不改变任用审批。新显式敏感动作不能扩大为通用档案read可见。

archiveRead/interviewRead/evaluationRead/nominate/review/appoint/export及敏感子集字段独立；同时核人员与岗位范围。委员会仅议程最小材料，访谈角色标签只是分类，不授M01关系权；本人仅明确开放述职/反馈，潜力、委员会讨论、原始访谈不默认公开。历史/附件下载当前授权，审计read不授原材料read。

<a id="m03-spec-06"></a>
## 生产者、旧实现和历史真实度

M37标准、M06证书、M17候选、M18盘点、M26报告均用stable root+version+sourceRevision+evaluatedAt+purpose+missingReason，不能以同名或一个分数替原证据。M19提供冻结路由，M01拥有主兼职/调动实际生效，M48仅本人获准任务/反馈，M32输出明确任期/活动/考察粒度及当前授权分母，不能隐藏访谈透过导出泄漏。

旧cadre-terms/cadres/cadre-interviews的稳定ID、任期重叠、独立基础review、访谈记录可复用。legacy registered、无details.transfer旧approved校验、简单考察completed/development_needed不足以表示正式任命/新考察流程；旧数据保留原语义及来源，禁止反向用旧允许路径削弱D1–D7。原StaffID映射、termId、调动来源/时间不改，未知前任/类型/算法/批准不补造。

<a id="engineering"></a>
## 接口、事务、迁移与恢复

|命令|payload及必要前置|原子效果|
|---|---|---|
|m03.activity.save/submit|activityVersion、target/eligibility/template/route/committee版本|冻结活动审批，缺核心规则不启动|
|m03.nomination.submit/decide|person/target、previousNominationId?、材料及sourceRefs、committeeVersion|在途占位、独立审议及appointmentDecision|
|m03.appointment.reconcile|decisionId、sourceEffectReceiptId/version、termType/日期、current eligibilityRefs|一次receipt核对、term及appointmentRecord、审计/command/outbox/恢复日志|
|m03.term.change|term/baseVersion、changeKind、actualDate、reason、independentApproval/sourceReceipt|新状态/更正/续任链，不改M01|
|m03.observation.submit/review/extend/terminate|observation/term/evalVersion、目标证据、policy/due/reason|独立考核新版本，期间/退出屏障|
|m03.report.submit/review/publish / archive.append|term/purpose/cycle、recordVersion、materialManifest/audience；子集source/occurredOn|述职或档案新版本，敏感字段与来源审计|

全部用[严格Envelope](Interfaces.md#schema)，命令必须原decisionId/idempotencyKey/digest；两次同receipt任用一成功，异payload同键冲突，响应unknown查原命令与两域receipt，不换键重复任期。权限/资格/任职/term版本同CAS重核，审计失败不写半个任命；外部结果unknown不视成功，通知失败不回滚已认定事实。

迁移先存原ID/StaffID namespace/登记事实hash，新映射/独立审批另立；重复任期、无实际生效凭证、未知类型只隔离对应新任用，不删除历史。回滚不回到旧approved即可绕生效路径，保持安全writer及前向修复。附件按subset/report/evaluation版本绑定，当前授权下载，原文不进通用审计；物理删除须无恢复点引用。

恢复核term区间/receipt唯一、跨M01已生效差异、资格现时有效性、考察/述职版本、档案墓碑和当前deny账本；恢复授权无法证明保持隔离，不复活旧任命、已撤权访问或通知。P3/P4遵守[60/240/30](Recovery_Cost_Responsibilities.md#targets)。

<a id="acceptance"></a>
## 验收夹具与责任

合成E1、M01岗位P-A/P-B、主/兼职两type；提名者H、独立评委R1～R5、任用核对A。2月29日/1月31日及明确override日期；5评委回避/弃权/缺交；精确79.995/80.000；资格批准后过期、M01approved未applied、applied但响应丢失、同receipt双核对，分别验证。

M03-REVIEW-AC01～14逐项见Acceptance_Scenarios.json。实际断言包括M01未被M03写入、无重复term、审批/后效分态、敏感字段/下载直接API拒绝及legacy登记未伪造批准。P2完整设计闭环；P3干部域/流程/人事接口负责人实施、独立测试复核；P4任免委员会、业务HR、安全和运维核真实生效链、档案用途与恢复。原站任免/考察深操作缺口只形成补证请求。
