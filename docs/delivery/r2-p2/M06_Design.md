# M06任职资格详细设计

依据M06-SPEC-01～05、BP-C-REQ-02及M06-LIMIT-01，批准`M06-P1-APPROVAL-R2-20260909`。资格目录/尺度/证书归M06，M37只提供引用定义，M01保留人事决定权。

<a id="m06-spec-01"></a>
## 目录、发展通道与稳定ID

独立对象categoryClassification、qualificationCategory、hierarchy、qualificationLevel、indicatorType、qualificationIndicator、ratingScheme、developmentChannel、learningMap均有rootId/versionId/state；分类树与指标类型树分别核parent FK和全路径无环，不能跨树混父。类别关联{targetKind:job|position,targetId,sourceVersion}可空，空是未配置，不代表全岗位适用。级别目录独立，标准显式categoryId+levelIds，不按名称/排序归类。

名称/编码trim后1–200字，编码在各对象目录内区分大小写唯一、停用不复用；重名显示编码/层级。展示sort正整数，同父可同号，以stableId作稳定次序；标准内部levelOrder必须明确唯一，不能拿展示顺序推资格大小。自动编号键(tenant,objectKind,ruleVersion,prefix)原子计数及已发编码占位，失败可跳号，不重用；规则升级新版本，不建M35引擎。

发展通道有channelRoot/version、hierarchyRefs、cardFields和learningMapVersion；学习地图显式levelId→M27 resource/plan VersionRef及用途。显示层级/简卡和地图分别有配置版本，不自动派课或授资格；未映射项not_configured并保留入口。来源资源撤回按当前授权隐藏操作，不删原地图版本。

<a id="m06-spec-02"></a>
## 标准矩阵、评级及认证就绪

qualificationStandard(rootId/versionId,categoryId,levelRefs,indicatorRefs,entryPolicyVersion,validityPolicyVersion,certificationReadiness)；requirementLine(lineId,standardVersionId,levelId,indicatorVersionRef,descriptionSnapshot,target,mandatory,ruleVersion)，唯一(standardVersion,levelId,indicatorId)，每level×indicator明确是否适用。首次引入说明保存快照，以后指标改文不漂移。

numericTarget={min,max,step,unit,direction,comparator,threshold}采用精确decimal字符串，范围/步长合法；未知不补100或1–5。ratingTarget={ratingSchemeVersion,ratingLevelId,passLevelIds}，评级方案每级独立ratingLevelId、name、唯一正整数order、可空description，至少一级；使用中方案新版本。任职层级/编号与评级级别不同，不自动映射。通用指标只是可被多标准选用，不授全员权限或自动必达。

catalogPublished与certificationReadiness分开；规则缺项可保存目录但不能认证。默认全部必达；组合须冻结AND/OR及阈值/强制否决规则版本。每证据evaluationId/version引用同indicator、standardVersion、level和明确证据窗口，来源不可核/过期/缺必需项为unknown，不能false降成0后平均。显式unlimited证据窗口可以使用，不能沿旧窗口隐式继承。评分取比较精确值，显示舍入不改结论。

<a id="m06-spec-03"></a>
## 发布、停用和在途

标准及影响评定的目录/评级方案draft→submitted→approved→published，M19独立审核，冻结类别/级别/指标/评级/说明/准入策略及贡献人集合。rejected/withdrawn后的修订重新提交，新applicationVersion；已published字节不可改。availability active/disabled另存事件。

新申请仅用已发布、启用、规则完整版本；选择后提交前停用在同CAS被发现则拒绝。目录/指标停用提供当前授权内依赖清单，无权只显示受保护依赖；阻新选入，已有标准冻结快照不失效。标准停用阻新申请，在途已提交申请按旧版继续、显示风险，可经独立有权操作逐单终止；既有证书只通过自身有效期/撤销规则失效。草稿升级需用户显式选择新版本并重验材料，不自动latest。

<a id="m06-spec-04"></a>
## 申请、委员会、授证和有效性

applicationId与applicationVersion独立；personId、standardRoot/version、targetLevelId、submitter、proxyAuthorityRef、materialVersionRefs、contributorIds、previousCertificationId、intent=ordinary|renewal。本人或具有proxyApply及对象范围HR提交；评审者需资格/级别/组织范围节点权，并排除本人、提交者、全部历史材料贡献者，admin/manager角色名不授权。

冻结reviewerSet、decisionMode=all|threshold、minEligibleCount、quorum与threshold（阈值模式必填）、mandatoryRequirements、hardVetoRules和recusalRefs。all须全部应评有效评委明确通过；threshold须全体应评提交明确票/弃权后按已配置分母和阈值计算，不因未交或回避偷偷缩分母。回避变更独立批准后形成新set版本；不足minEligibleCount或quorum阻完成。任何必达未满足/unknown或强制否决成立，即使投票达标也不能认证。门槛是实例显式配置，不能自动选一个默认百分比。

申请draft→submitted→under_review→approved/rejected/withdrawn/cancelled；approved→effect waiting→issued或failed/blocked。授证同事务再核当前成员/人员、标准冻结许可、证据窗口和重复键；生成certificateId/certNo、issuedAt、validityPolicySnapshot、evidenceManifest，业务+审计+回执同commit。业务已issued而通知unknown不撤销授证。

validityMode=fixed_until|fixed_duration|long_term须显式：fixed_until有效截至日必须≥issued北京日；fixed_duration需要明确duration/unit及日期算法版本，缺算法不就绪，不能擅自套M03月末政策；long_term仍可revoked。截止D含当日，Asia/Shanghai D+1的00:00起派生expired，原授证状态certified保留。保留issuedAt、validUntil、revokedAt、revocationReason和evaluatedAt；当前validityStatus=valid|expired|revoked|unknown，不把certified当永久有效。

普通重复键为(tenant,person,qualificationRoot,targetLevel)，已有pending/approved-waiting或有效证均拒绝，不因标准换版绕过；续认证明确引用同人同根同level旧证，唯一在途(previousCertificationId)，新申请/证不覆盖旧证。续证是否提前生效由新显式validity策略和批准内容决定，未设不自行累计时长。撤销由范围内revoke独立HR留原因并排本人/授证申请贡献者，变更新状态事件保留原证据；撤销失败不报成功。新评分不会重算旧授证结论，不自动调薪/升职/改职级。

<a id="m06-spec-05"></a>
## 权限、消费与旧实现

read/use/manage/review/publish/export、proxyApply、applicationReview、revoke、selfResultRead独立。组织∩类别∩level及敏感材料字段按[grant元组](Permissions.md#authorization)计算，本人只能本人结果及关联标准最小投影，不能借标准read查他人评估。历史、附件、导出按当前权限；离职/解绑禁新申请与认证办理，已授证事实保留受控追溯。

certificateSnapshot返回certificateId、personId、standardRoot/version、qualificationLevel版本、issuedAt、validUntil、revokedAt、validityStatus/reason、evaluatedAt、sourceRevision/digest。M18可参考但独立盘点，M17按自身入池/ready规则决定，M03按eligibilityPolicy在提名/批准/实际生效重核；M48/M32不能从raw certified计算有效人数。来源不可用或版本不兼容为unknown/not_configured，强前置阻办理。

旧qualification.ts的1–5要求、仅按version防重、申请creator排除、admin直发布都须改造；可信证据筛选、稳定ID及撤销记录可复用。旧validUntil为空按原长期语义保留legacyValidityPolicy，不伪称用户选择了新long_term，也不能从旧值推新证永久。旧M37五级引用保留原schema，类别/续证关联/原批准未知不补造。

<a id="engineering"></a>
## 接口、异常、迁移与恢复

|命令|关键payload与条件|原子效果|
|---|---|---|
|m06.catalog.create/edit|kind、root/baseVersion、code/name/parent/sort、explicit targetRef；树/编码检查|新目录版本、编号占位、审计回执|
|m06.standard.submit/review/publish|standardVersion、矩阵manifest、policy versions、workflow/applicationVersion|冻结审批及发布版本；无自审|
|m06.application.submit|personId、standardVersion、targetLevel、intent、materialRefs、previousCertificationId?|申请+重复占位+M19实例|
|m06.application.decide/issue|applicationVersion、node/committeeVersion、decision/reason；最终证据与时间重核|审批与授证分态；证书唯一及consumer outbox|
|m06.certification.revoke|certificateId、expectedRevision、reason、独立权限|撤销事件及当前有效性，不覆原证|
|m06.validity.query|certificateId/purpose、asOfMode=current或真实snapshotId|当前授权Cell及sourceRevision；无历史证据不能任意asOf|

严格Envelope、签名、错误码沿[接口](Interfaces.md#schema)。并发普通/续期/撤销同租户CAS防重复；同请求键结果未知先查，不换键补授；到期与任用竞争以事务时刻和sourceRevision核，跨日长作业重新验证。附件先写不可见对象再同事务绑定，当前材料权/revoke/download单独核。

迁移保留原标准/申请/证书ID和历史证据，未知类别/旧长期策略/冲突level进入局部issue，新认证就绪前人工核证；不覆盖旧数字尺度。回滚保留新模型及写闸门，已发新证前向修复不删证。恢复核全部证书/续证链/撤销墓碑/command receipt与当前时间，恢复旧备份不能复活过期或撤销证。P3证据与P4责任沿[恢复设计](Recovery_Cost_Responsibilities.md#responsibility)。

<a id="acceptance"></a>
## 验收夹具与责任

合成T-A/T-B、员工E、代办H、独立评委R1/R2、回避贡献者C；标准QR的v1/v2、独立level QL与ratingLevel RL（相同名称但不同ID）、数值尺度0–10步长0.5及评级方案。固定时钟D=2026-09-30 23:59:59+08:00与D+1 00:00验证到期；证据缺失、过窗和显式unlimited分别构造；同旧证双续期并发只一在途。

M06-REVIEW-AC01～13逐一见Acceptance_Scenarios.json；必须验证实际对象、精确有效性、重复占位及独立回避，不能以历史合成测试代本轮复验。P2完整规则/接口关闭；P3资格域实施+独立测试负责人验证；P4业务资格委员会核真实角色和有效窗口，安全/运维核敏感材料及恢复。原站评分、委员会细节和多角色实操未知保持限定补证，不反转已批准政策。

<a id="repair-001"></a>
## 001契约定向对齐

indicator_type的isCommon、说明行及numeric/rating配置写入目录内容版本，评级方案与资格级别不可互换。 完整字段与拒绝条件见[Contract_Repair.md](Contract_Repair.md)，其规范替换旧版简写中的歧义，其余已通过独立评审内容保持。
