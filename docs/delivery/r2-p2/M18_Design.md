# M18在线盘点详细设计

依据M18-SPEC-01～05、BP-C-REQ-08及共享BP-C-REQ-04，批准`M18-P1-APPROVAL-20260910`。盘点只拥有本域评定和发布，不能改M16绩效、M26答卷、M06资格或M17成员事实。

<a id="m18-spec-01"></a>
## 项目、范围和保存进度

projectRootId/versionId、name(trim1–200)、scenarioId/version、categoryId/version、year（明确业务年度）、startOn/endOn（合法自然日且end≥start）、orgScopeSnapshot、M37standardVersion、toolContractVersion、templateVersion、workflowVersion、schemeVersion独立字段。scenario/category/org必选，未知来源不可用名字占位。saveCheckpoint记录stepId、savedRevision、savedAt及校验结果，不以走到最后一步推定前面已落库。

subjectRecordId唯一(tenant,projectRootId,stablePersonId)，保留org/position/assignment版本及评价关系快照；员工同项目跨改版不变subject根。启动核当前可纳入人员范围并冻结scopeManifest/evaluatorRelations，员工随后调动/离职只改变当前办理许可，不覆写原范围/统计分母。新增/排除对象须project新revision、reason、批准来源和差异manifest，原快照仍可按版本追溯；排除不是删除历史答卷。

previousResultRef={producer,resultRoot/version,asOf,selectedFieldIds,purpose}必须用户显式选择且可读；仅显示参考，不预填为本次已评定。缺真实历史版本HISTORY_UNVERIFIABLE，不能把当前结果换时间当上次。

<a id="m18-spec-02"></a>
## 维度、就绪状态与九宫格

dimensionAssessment(lineId,subjectRecordId,resultVersion,dimension,sourceVersionRef,scaleVersion,targetVersion,ruleVersion,collectedState,calculationReadiness,Cell)。能力/潜力/经历/成就各自来源与单位独立，绩效轴可通过显式M16已发布来源配置，不自动将成就当绩效。采集未开始/部分/完成与计算not_configured/ready/blocked分列，无来源/规则/权限/样本为null及安全原因，缺权字段省略；不填0或中档。

gridDefinitionRoot/version：xAxis=performance、yAxis=potential为已批初始方案，轴source/scale/mappingVersion、bandLabels、lowCut/highCut必须项目显式批准冻结。数值lowCut<highCut：x<lowCut为low，lowCut≤x<highCut为mid，x≥highCut为high；超来源尺度范围拒绝，不夹到最近格。逆向尺度先依显式direction mapping转轴值，不静默颠倒。ordinal必须显式levelId→band映射，不能把等级作等距数值平均。

任一轴缺失则gridCell=null+unrated，与九格外单列；九格人数=sum(合法九格各distinct subject)，未评定人数单列，授权范围总人数=九格人数+未评定人数，其他维度不强压二轴。当前权限裁剪后重算可见分母，不露原全量人数。无强制比例、排名淘汰或自动任用；方案改阈值形成新version，不重写旧published grid。

<a id="m18-spec-03"></a>
## 校准会、独立复核和更正

meetingRoot/version、agendaId、subjectRecordId/baseResultVersion、participantRole/scope、calibrationProposalId/proposalVersion分别稳定；participantRole=convener/participant/scribe/reviewer/publisher按显式grant，召集或记录不继承review/publish。每proposal保留oldValue/newValue（typed Cell）、sourceVersions、reason、evidenceRefs、dissentRecords、decisionVersion、recusalRefs及贡献人历史集合。

subject及提案提交者/实质材料贡献者不得review；publisher与reviewer不同并具当前组织/字段权。consensus模式记录明确的有效参与者确认及未解决异议；vote模式显式threshold/comparator/denominator/eligibleSet/minEligible/quorum及回避处理，缺参数/缺应评提交/回避后不足阻决议。多数票不得覆盖必需证据缺失或强制否决；异议保留处理决定和责任，不因会议结束自动消失。

每原resultRoot只一在途更正（包括approved未发布），proposal冻结basePublishedVersion；新版本已被另一合法published更正取代时旧提案返回BASE_SUPERSEDED，不准发布。rejected/withdrawn保留历史，重提新proposalVersion+previousProposalId。校准只形成M18新resultVersion，不能回写M16/M26原始结果。会议closed是会议终态，结果仍可waiting_review/publish，不能串成一个“完成”。

<a id="m18-spec-04"></a>
## 发布和当前可见性

项目draft→approved→active→collection_closed→closed，approved由M19独立流程、active为授权业务启动；关闭前显式核未结采集/更正/发布事项，不能靠后台清空。在途事项可明确终止并留原因，不能悄悄视完成。subject collection/evaluation/computation状态与project不同步推定。

首次结果draft→submitted→reviewed→published；更正复用独立复核→另一有权者发布。无首次review凭证不能publish，旧实现creator可发布不得复用。已published字节不可编辑，current指针只由新published supersedes切换，draft/approved不能遮盖旧正式版。withdrawPublication独立授权、理由、状态事件和下载deny，保留受控历史；更正处理中是否仍可见旧版由已批撤回动作决定，不能自动假定所有域与M26报告同策略。

closed项目纠错先reopen申请独立批准，生成projectRevision和允许的修订范围，不在终态直接createReview/calibrate。向下公开、共享组织、本人报告分别audiencePolicy版本；默认本人不可见潜力/九格/任用讨论，发展反馈是独立批准的字段投影，不因经理关系自动开放。历史、聚合、附件和导出当前授权，待审批不能冒正式结果。

<a id="m18-spec-05"></a>
## 消费和分析边界

输出publishedResultSnapshot={resultRoot/version,project/subject/period,scopeManifest,standardVersion,axis/ruleVersions,sourceRefs,Cells,purpose,audience,sourceRevision,digest}。M17收到suggestionId及结果引用，经自身授权业务动作或显式已批准自动规则才生成有效成员/候选；M18撤回不擅自删M17已作决定。

盘点页的池分析保留M17 pool/member/version/asOf读取入口，继任地图分positionId数据集和orgId数据集，缺一种不得用另一分母顶替。M06只读当前有效性并保留evaluatedAt；九格不授证。M26只消费已开放且用途允许的抑制结果，源撤权不穿透去原卷；M48仅获准本人任务/反馈；M32沿同版本/范围/null口径，current与真实snapshot明确分开。

通知与发布分态，未配置明确not_configured；M19只管路由批准，业务发布由M18适配器计划同事务效果。六基础全部适用，未知查原command/result ID，不靠模拟通知成功标盘点完成。

<a id="engineering"></a>
## 接口、事务、迁移与恢复

|命令|payload与检查|效果|
|---|---|---|
|m18.project.save/submit/start|projectVersion、保存step、范围/模板/规则manifest；日期和授权|保存回执或独立批准后启动冻结|
|m18.subject.reviseScope|projectRevision、add/exclude personRefs、reason、approvalRef|新scope版本，原subject/history保留|
|m18.assessment.collect/compute|subject/resultVersion、dimension、typedSourceRefs/Cell、ruleVersion|采集与就绪分列；不更改来源|
|m18.meeting.save / calibration.submit|meeting/agenda、baseResultVersion、proposal值/证据/异议、participantSet|更正唯一占位、冻结复核申请|
|m18.result.review/publish/withdraw|resultVersion、独立decisionRef、basePublishedVersion、audience/reason|版本指针、可见状态、outbox、审计/receipt|
|m18.project.close/reopen|projectVersion、未结事项处置或reopenApproval、reason|明确终态/新修订，不删结果|

使用[共用Envelope及失败码](Interfaces.md#schema)。旧revision拒绝、同键重复只一版本；两会议改同结果只一在途，发布与撤回竞争在同CAS核base、auth、源及project revision。大范围manifest分块不可见准备、最终同CAS发布，不让消费者读半个项目快照。业务/审计/回执/日志失败全回滚，通知unknown仅通知对账。

旧review-versions/development的原ID、已发布版本/更正链可复用；project简单状态、固定九格映射、首次自发布和closed仍可更正须改变。迁移旧published保留legacy_review_provenance=unknown，不补首次复核；新更正必须新流程。旧九格保持旧gridDefinition，缺轴不伪造重算；同项目重复人、丢失源版本、坏supersedes隔离局部对象。回滚不回旧允许自审写路径，保持当前安全闸门与新版本只读。

附件归属明确meeting/proposal/resultVersion；参会权不授原始证据下载，当前行列动作和审计隔离沿[权限设计](Permissions.md#files)。恢复须有范围/会议/结果/发布manifest、建议收件去重和当前安全账本；回到备份后不重新发布旧通知、不用当前M17池重造历史盘点分析。[60/240/30](Recovery_Cost_Responsibilities.md#targets)保持。

<a id="acceptance"></a>
## 验收夹具与责任

合成项目PRJ-1、员工E1/E2/E3、scope v1/v2；四维分别有效/缺失/无权来源；数值轴lowCut=40、highCut=70测试39.5/40/69.5/70，缺一个轴必须unrated。提案人C、复核R、发布P不同；两会议同时更正同base，closed项目直接写拒绝，合法reopen新revision可继续。

M18-REVIEW-AC01～13逐项见Acceptance_Scenarios.json；核九格及未评定人数等式、首次独立复核、显式current指针、M17建议未自动成员、历史source digest未变。P2设计闭环；P3盘点实施与独立测试负责人落实，M17/M32共同核接口；P4业务校准委员会/安全/运维验真实角色、用途和恢复。原站校准/撤回深操作未知只形成结构化补证。

<a id="repair-001"></a>
## 001契约定向对齐

previousResultRef由project.create/save明确写入项目版本，引用历史发布集并按稳定person匹配，只作参考。 完整字段与拒绝条件见[Contract_Repair.md](Contract_Repair.md)，其规范替换旧版简写中的歧义，其余已通过独立评审内容保持。
