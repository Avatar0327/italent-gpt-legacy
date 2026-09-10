# M17继任与发展详细设计

依据M17-SPEC-01～06、BP-C-REQ-04/05，批准`M17-P1-APPROVAL-20260910`。完整保留人才池、自动规则、继任、IDP模板/流程、组织健康及分析入口，不用旧简化状态压缩批准范围。

<a id="m17-spec-01"></a>
## 人才池、成员任期与自动规则

poolRootId/version、name(trim1–200，技术输入边界)、categoryId/version、orgScope、sharingPolicyVersion、expectedCount（空或正安全整数）、entryRuleVersion/exitRuleVersion分别保存；空预计人数不是0。membershipId关联poolRoot/personId、enteredAt/exitedAt、stageVersion、previousMembershipId和源批准/规则run；时刻区间[enteredAt,exitedAt)可空结束，相邻出池重入可同一时刻，重叠同池同人拒绝。自然日展示不抹掉实际时刻。

stage字典至少保留new_in_pool/developing/exited，与active/closed关系、readiness及IDP状态分开；阶段改变新event/version，不推自动培养完成。跨池用途可并存，出池留下旧membership及reason，新入池新ID、显式关联同人同池previousMembership；不能重开原ID抹去中断。旧来源缺入出精确时间标unknown，不拿迁移时间假造有效开始。

默认人工entry/exit申请→M19独立review→apply；subject/提交者/实质材料贡献人回避。自动能力保留：ruleRoot/version冻结作用范围、AND/OR AST、输入版本/缺值策略、cadence/timezone、reviewOwner、effectMode=proposal_only|approved_auto_effect和启用批准。完整配置且有ruleExecute才可运行；未配置、disabled、依赖unknown均不自动入也不自动出。不可把M18推荐事件直接当无规则入池许可。

自动job键(ruleVersion,scheduledOccurrence,scopeDigest)，逐人命令键(jobId,personId,action)，同批输入manifest冻结；每人的成员变更/审计/回执同事务。批次显式partial/failed/unknown，不因某行失败半建其成员；源变化触发重核或该行blocked，不能使用旧资格强行入池。规则新版本不重跑已处理旧周期，不自动任命/调薪/消息外发。

<a id="m17-spec-02"></a>
## 准备度、继任任期和当前有效性

readinessDefinitionRoot/version含code/name/businessMeaning/timeRange及calendarUnit/anchorPolicy，now单独语义。保留源“3~6个月”“6~12个月”“12-24个月”与自定义“RN1年内继任”“推荐后续使用”标签，未知业务含义标未配置；legacy ready/one_year/two_years保留原字典版本，不按显示顺序或培养进度转换。时间档是预计发展窗口，不是保证任命日期。

successionId关联targetKind/targetId、personId、startOn/endOn（北京时间闭区间）、readinessVersion、assessmentAt、nextReviewAt、reviewerId、evidenceRefs、policyVersion、status。岗位候选targetKind=position且稳定M01 positionId必须存在；组织继任若有显式org目标是独立数据集/政策，不把岗位树节点冒org。无目标选择不可提交，不按名字新建岗位。同人同目标有效区间不重叠，允许同岗多人、同人多岗；结束不早于开始。

候选draft→submitted→reviewed→active→closed/voided，审批与实际登记effect分列；active只原始关系状态，currentAvailability另核人员在职、目标启用、有效区间、当前政策及nextReviewAt。asOf≥nextReviewAt派生review_due，不算“当前就绪”。now必须满足明确岗位要求、所要求M06资格当前valid及独立准备度审议；要求/证据unknown不自动now。离职或岗位停用停止新推荐，旧记录留unavailableReason，有权者仍可close，不能因新建规则拒绝所有历史关闭。

<a id="m17-spec-03"></a>
## 指导角色、动态关系和回避

poolRole与idpRole各有独立roleDefinition/version，不按同名合并。源池五种：直线经理、间接经理、部门HRBP、部门负责人、其他人；源IDP九种另含导师、第三级/第四级/第五级主管。虚线等已批准关系通过显式M01关系kind映射，不因源选项没有就用名称猜。roleResolverVersion指向实际M01 assignment/relationship版本；未配置部门HRBP、导师或层级链则blocked_relationship，不能回退admin。

mentorRelationId保存personId、roleVersion、resolvedMentorPersonIds、effectiveInterval、responsibility、completionMode=all|any及handoffVersion；其他人必须显式选当前合法身份。本人不得为唯一指导人或最终核验者；本人可制订/提交，verify排本人、提交者及该次成果实质编制者。多指导人哪位负责coach、哪位verify及all/any必须完整，不因一个同意当全部完成。

关系变更先重核当前授权，需换指导人时授权交接新version，旧人停止新动作、新人明确接受必要职责；已完成核验保留原执行人/授权时点，不重写。无法解析或无人接手只阻依赖节点，其他计划可继续。源同EA可保存自指导是历史事实，已批准项目规则明确不采用其自核语义。

<a id="m17-spec-04"></a>
## IDP流程、模板和阶段任务

flowRoot/version、templateRoot/version、planId/version、stageId、taskId、assignmentId独立；plan title1–200、personId、templateVersion、mentor role/bindings、startOn/endOn必填，start≤end；原来源仅UI必填不能冒已验证服务端规则，此处是批准范围的接口具体化。模板冻结flow节点/顺序/并行DAG、职责、required deliverables、dueRule、electiveMinCount和waiverPolicy；停用阻新实例，旧计划不自动终止。

plan draft→submitted→approved→active→completed，另有paused/terminated；批准与生效分态。stage blocked→open→in_review→verified，task blocked/open/draft/submitted/returned/verified/waived/cancelled；逾期overdueFlag与这些状态分列。阶段/任务截止须在计划范围，延期需明确批准的extensionPolicy和新版本；依赖DAG无环、强前置未verified/授权waived则后续不能open。不能从阶段顺序整数直接推唯一串行。

提交成果新submissionVersion；待审可withdraw、退回再提保留旧版本；verify独立角色核完整材料和当前权限。阶段完成需所有required verified或获批准的明确waiver，选修verified数≥显式electiveMinCount；cancelled默认不视满足，免除须授权原因且调整requirementsVersion。计划完成需所有适用阶段verified，不因到期自动完成。

延期/改任务/换导师留新planVersion及依赖影响清单，已verified内容不无痕重写；影响已完成阶段的新要求须显式重新开启该阶段/计划修订并独立批准。paused禁新普通提交，terminated保留终止原因和历史；resume须当前人员、任务权限及职责解析完整，不重新用旧授权。M27只消费真实verified learning版本及要求映射，100%进度不算核验；来源撤回标证据失效并触发本域复核，不自动授资格或改readiness。

<a id="m17-spec-05"></a>
## 组织健康、池分析与分母

metricDefinitionRoot/version含rowGrain、scopePolicy、sourceVersions、timeMode、numeratorAST、denominatorAST、unit、nullPolicy、rounding；关键岗位清单显式按M01 stable positionId配置并经授权发布。每结果返回asOf、generatedAt、visibleScopeDigest、definitionVersion、sourceManifest、numerator/denominator/Cell及缺失原因，数字只在授权允许时返回。

|指标|分子|分母及时间|缺值/边界|
|---|---|---|---|
|关键岗位覆盖|至少1条current有效后备的关键岗位distinct positionId|当前适用且授权可见关键岗位distinct positionId|多候选只计一岗；关键清单未配为not_configured|
|就绪覆盖|至少1名now、资格valid、未到nextReviewAt的有效后备岗位数|同一关键岗位分母|review_due不计就绪，不从培养进度推now|
|池饱和度|指定asOf有效成员distinct personId|该poolVersion明确expectedCount|可>100%；预计人数空为not_configured；不能拿全部员工当分母|
|计划逾期率|同一到期cohort中deadline<asOf且未completed、未authorized_terminated的计划数|发布定义指定统计期[from,to]且截止≤asOf的应到期已生效plan根数|同plan多版本只按cutoff有效deadline一次；已授权终止从分子排除但原应到期计划仍在同cohort分母，不能人为缩小分母|

current查询只当前时点，不接受任意历史日期；历史asOf必须真实保存snapshotId及来源版本，缺历史HISTORY_UNVERIFIABLE。池时点人数依真实membership区间，不用今天active回填。分母0→null+no_applicable_data，不记0%；资格/人员源不可核导致候选有效性未知时另标unknown、对应比率不可冒精确值。显示百分比按显式2位小数，判定仍精确数值。

综合健康指数保留定义/版本/配置入口；维度/权重模型未批准为not_configured，不编总分、不自动评价个人。M32沿这些definition，旧successionCoverage保留旧schema/原三档历史，新岗位与组织不同dataset，不互作分母。

<a id="m17-spec-06"></a>
## 授权、生产者契约与遗留差异

pool manage/memberRead/ruleExecute、succession nominate/review/close、plan coach/verify、healthRead/export分别授予；池及人员范围都要满足，继任人员组织与目标岗位范围都要满足，再核字段/当前关系，不笛卡尔拼角色。共享/向下公开显式policy；默认本人看不到候选排名、潜力、退出讨论，只看明确行动/反馈。

M18发布结果只引用具体版本作为建议，M37定义和M06有效性分开；M03独立审批任用，M48本人投影，M19独立节点，M32按版本指标。建议消费+去重不自动跨域入池，只有M17自身显式approved_auto_effect规则可以产生自动成员效果。真实通知仅保留契约，未配显示不可用。

旧development.ts的池成员ID、出池保留、稳定继任/IDP可复用；缺previousMembership链、固定三准备度、无任期/复核、简单actionPlan和取消学习即满足需要新模型。迁移原三档、成员ID、源五候选文字和角色目录分开保留，未知原单/日期/关系不补造；已完成旧IDP只记旧核验事实，不编出不存在的阶段和导师确认。

<a id="engineering"></a>
## 接口、事务和恢复

|命令|payload/前置|事务效果|
|---|---|---|
|m17.pool.save / rule.publish/enable|poolVersion、scope/expectedCount、规则AST/时区周期/复核责任/effectMode及独立approval|池/规则版本，不自动运行未启规则|
|m17.membership.apply/exit/reenter|pool/person、intent、previousMembershipId?/reason、独立approval或可信ruleRun|区间唯一、成员新版本/历史、审计/receipt|
|m17.succession.nominate/assess/close|targetKind/ID、person、区间、readinessVersion、assessment/nextReview、evidence、policy|候选及准备度新版本；close允许合法历史清理|
|m17.mentor.handoff|relation/baseVersion、newMentorRefs、职责/all-any、reason|当前权限及关系核验、新交接版本|
|m17.idp.submit/start/taskSubmit/verify/extend/pause/resume/terminate|plan/stage/task/submission版本、template/flow、typed deliverables、dependency/evidence及reason|独立流程、任务/阶段不变量、不可变核验历史|
|m17.health.query/snapshot|datasetDefinition、scope、current或snapshotId、period|授权后有界分母与sourceManifest，不强制全量内存|

共用[严格schema及失败矩阵](Interfaces.md#schema)。成员入出并发、双续任、任务verify/withdraw竞争均以同CAS核版本，重试同键无重复；unknown查membership/plan/command，不先补造新root。自动任务租约fence、输入manifest/逐项回执可对账，先业务+审计+恢复行日志原子落库再异步消费。附件按plan/task/submission和当前coach/verify/download授权，不因曾是导师一直可读。

回滚保持新模型只读/桥接writer，不能用旧active/closed覆盖新阶段或任期。恢复核池成员区间、规则run去重、候选review_due、IDP任务依赖/核验及健康snapshot，先当前权限账本再开放；恢复后时钟重新计算过期/逾期，不将过期资格变valid。完整[迁移](Migration_Rollback.md#rollback)和[60/240/30责任](Recovery_Cost_Responsibilities.md#responsibility)适用。

<a id="acceptance"></a>
## 夹具、验收与责任

合成池POOL-A/B、预计人数2与null；E退出再入POOL-A新membership（同一person），同岗POS-1两候选及同人POS-2；readiness now/3–6month/legacy one_year互不转换。IDP两个并行阶段、第三阶段依赖前两，required T1及elective最少1；本人C提交、独立V核验，多导师all/any两套显式配置。健康样例关键岗4、覆盖3、就绪2；池3/预计2=150%，分母0返回null。

M17-REVIEW-AC01～14逐项见Acceptance_Scenarios.json，另针对自动unknown、出池重入并发、任务取消未获免除、快照与当前源混用补验。P2完整设计关闭；P3人才发展域负责人、共享流程/报表负责人和独立测试负责人实施；P4业务人才委员会/隐私/运维核真实角色、规则及恢复。原站IDP流程节点UUID和旧出池链未知只形成补证请求，不再把已确认流程入口存在列未发现。
