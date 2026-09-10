# M26 360度评估详细设计

依据M26-SPEC-01～05、BP-C-REQ-03及BP-I-REQ-03适用边界，批准`M26-P1-APPROVAL-20260910`。匿名保护、HR原卷隔离和发布条件按批准新规则设计，原站未知保留；原surveys命名问卷不能充当匿名360底座。

<a id="m26-spec-01"></a>
## 身份、角色和邀请

|对象|稳定身份与字段|不变量|
|---|---|---|
|role_definition|roleRootId/versionId、name、relationshipKind、namedDisclosure、availability|name trim 1–18、同目录唯一；最多90角色/套卷15；停用保留已用版本|
|feedback_project / subject|projectRoot/version、subjectId、personId、orgSnapshot、collectionVersion|同项目同person一subject；数据主体身份不取显示名|
|reviewer_binding / invite|bindingId、inviteId、project/subject、reviewerPersonId、roleVersion、noticeVersion、status|同项目根+subject+reviewer只有一个有效邀请；self iff reviewer=subject；角色冲突开放前显式处理|
|response_bridge|inviteId、opaqueResponseRootId、restrictedKeyRef|独立受控表/权限域；普通HR、报告服务和M32不得join身份桥接|
|response_version|opaqueResponseRootId/versionId、subjectId、roleVersion、questionnaireVersion、answers、submittedAt、state|只最新submitted有效；旧版本保留受控历史；不要在通用事件暴露invite或reviewer映射|

邀请创建前展示冻结noticeVersion及用途：本人组和明确披露具名的唯一上级不宣称匿名，其余按分组阈值匿名。角色改名/停用不修改既有承诺；开放后角色替换必须显式修订及重新确认承诺，不能把匿名邀请改具名并继续使用旧答卷。已解绑/离职/撤权禁止新答；既有合法答卷按冻结样本政策保留，质量剔除需授权原因和阈值重算，不按当前在职名单无声删卷。

HR可管理邀请/发送状态，不默认原卷或桥接。受控审计例外要求独立批准{purpose,objectRange,fields,validFrom,expiresAt,approver}，不得由申请者自批、不得向主体/普通经理透露评委关联；过期即时撤权。数据隔离与审计脱敏采用[共用敏感设计](Permissions.md#anonymity)。P2不新增实际评委账号/访问者。

<a id="m26-spec-02"></a>
## 统计、抑制及报告授权

聚合输入为冻结collectionVersion内每invite最新有效submitted答卷，按不同reviewer去重，撤回/未完成不计；题目隐藏、NA及缺答分开原因，不视0。数值仅同question/scale版本、相同单位及显式聚合策略可比；ordinal默认分布，中位数/均值须明确转换版本。文本不自动量化，原话默认不发布，发布人工脱敏摘要另有审核版本。

匿名组有效评委数≥k，k为活动显式阈值且k≥3。计数服务内部可算n，面向用户低样本输出{state:suppressed,reason:insufficient_sample}，不带n、分数、原话或可相减总计；不能与别组静默合并。具名self/唯一经理组单列，不能凑匿名分母；个人报告至少一个合法非self组。组织报告去重subject≥3且每底层匿名组同样满足门槛，定义版本与被授权cohort固定。

报告reportRootId/versionId含project/collection版本、questionnaire/role/M37/aggregationPolicy版本、sourceManifest、cohortDigest、suppressionManifest、disclosureLedgerRevision、reviewDecisionRef、audiencePolicyVersion、purpose和contentDigest。先独立审阅、再另一有权者发布，排主体/内容贡献者自审；HR管理不等reportRead，主体/团队/HR分别显式开放清单。published只改变该版本指针，下载还需current read/export。

防差分具体执行：仅注册固定聚合维度，无任意人员筛选；披露账本按租户跨接收者累积（保守假设可联结），比较新旧cohort、交集/差集/补集和changedContributorSet。任一非空差集或可隔离的改变贡献人数<k，则抑制相应统计及依赖总计；相同cohort但只改一人答案也不能因集合相同放行。不能证明组合安全时拒绝该单元发布，允许其余安全固定单元。账本检查与published指针同CAS，两个并发报告不能各自用旧账本放行。P4隐私复核评委知情范围，不能宣称所有外部先验下绝对匿名。

匿名等价类按[Anonymity_Repair.md](Anonymity_Repair.md)确定算法：不可变答卷版本ID仅作来源，分组使用完整历史披露的参与/精确系数向量；更正由新旧answerAtom分行保留版本差分。受控伪名关联、组织双阈值、固定安全分区和epoch连续性均为必需，禁止实现者另选分组算法。首次合法ABC放行；不足样本、更正单人、成员变化、三重交叠及组合推断按逐格表抑制；撤回不清账本。

<a id="m26-spec-03"></a>
## 题库、套卷与字段校验

questionRoot/version支持rating、single_choice、multiple_choice、text有标签联合类型；title trim1–200、text answer≤3000（项目设计上限）、required、allowSkip/allowNA、optionIds、conditionalAST、length/minSelected/maxSelected按题型声明。rating显式min/max/step/unit/direction；单选恰一个有效optionId，多选去重且在明确min/max范围，text不收option；未知字段/类型拒绝。ordinal引用实际levelId，不硬编码1–5；选项ID不是分数。

questionnaireRoot/version冻结questionVersionRefs、顺序（同卷唯一）、roleApplicability、dimension/M37 indicatorVersionRefs和aggregationPolicyVersion；条件分支DAG只引用已可求值的前置答案，无环、不可引用不可见秘密字段，未呈现题记录not_presented及规则节点，不算漏答。所有角色所需必填题必须可达；角色启用不得丢题。规则/尺度/必需映射不完整阻open，题库停用不改已冻结卷。

<a id="m26-spec-04"></a>
## 活动、答卷与更正状态

项目draft→approved→scheduled/open→closed，独立M19路由；scheduled到startAt才open，endAt为排他的服务端时刻截止，界面明示结束时点；start<end且所有时刻UTC存储/北京时间显示。保存不等开放，到期只是停止收集，不自动发布报告。取消保留原因及所有已产生邀请/答卷历史。

开放前可新修订名单/套卷；开放后新增/替换reviewer走revision并保持原invite/tombstone/答案，角色唯一约束按项目根。替换后的邀请不能继承旧人的答案；本次规则仍用冻结题版本。答题者在open窗口内保存draft、submit、withdraw、resubmit，每次新responseVersion，稳定root不变；withdraw后不计分，close后锁定所有写。写前后校验绑定、exitFence、collectionVersion和当前窗口，迟到请求不能用客户端时钟补交。

纠错重开申请独立审批，生成新collectionVersion；已发布旧报告current状态correction_pending并立即阻旧链接对外读取，合法历史管理员仍受controlled history权。重开只能显式纳入旧有效答案引用/新作答，不伪造旧版本补答，改变题规则需新的套卷版本及不可比较标记。新报告关联supersedesVersionId，重新审阅/发布/阈值和历史披露检查；不能反复重开发布差分。撤回已发布报告生成withdrawal事件和下载deny，业务消费域仅保留其合法证据引用并自主处理更正，不自动删其他域结论。

<a id="m26-spec-05"></a>
## 消费、故障和旧数据

M37提供指标/尺度VersionRef；M26只输出已发布、授权、抑制后的报告版本/Cell/缺失原因，不传原卷或身份映射，不自动改能力评级、资格或任用。M48仅本人邀请/完成状态及显式开放的本人报告，M32用同policy和披露账本，不能另算低样本。所有查询与下载当前授权，撤权清敏感缓存、使晚回响应无效；临时故障unavailable而非0。

旧feedback.ts固定四角色和1–5量表、HR可读原卷、精确responses数、零答卷发布与覆盖旧答卷均存在差异。迁移保留旧ID/角色/题目/原报告字节，未保存的中间答卷版本unknown，不构造历史；旧低样本报告只在受控legacy历史域存证，默认当前不可公开。原有邀请去重可复用但扩到跨角色项目根唯一。提醒接口保留not_configured/queued/sent/failed/unknown，不在P2发送或使用真人。

<a id="engineering"></a>
## 接口、事务与恢复

|命令|payload/关键前置|效果|
|---|---|---|
|m26.role.save / questionnaire.save|root/baseVersion、严格题型/角色字段、DAG和尺度版本|不可变内容版本；发布条件预检|
|m26.project.submit/approve/open/close|projectVersion、reviewerManifest、noticeVersion、时间窗及templateVersion|独立流程/冻结collection、状态事件|
|m26.invite.revise|projectRevision、subject、reviewerBinding、roleVersion、replaceInviteId?/reason|项目根唯一邀请、旧邀请墓碑与新版本|
|m26.response.submit/withdraw|inviteId、collectionVersion、baseResponseVersion、questionnaireVersion、typedAnswers|本人校验；新答卷版本与桥接受控事务；审计不含答案|
|m26.report.review/publish/withdraw|reportVersion、source/suppression manifest、audience/purpose、expectedDisclosureRevision|披露账本+发布指针+审计/回执原子变更|
|m26.project.reopen|closedProjectVersion、correctionReason、independentApprovalRef|新收集版本、旧报告对外deny，保留历史|

采用[严格Envelope](Interfaces.md#schema)。提交/撤回竞争同CAS只有一个先成功，另409重读；两次同键submit返回同responseVersion，异payload冲突；响应unknown查询原命令，不新增一卷。报告多块先building不可见，校验全部hash/当前权限/披露账本后一次ready manifest发布。审计失败不准ready；桥接或答卷不得半提交。外部通知失败与答卷/报告业务状态分开。

附件只归属questionVersion/responseVersion/reportVersion及用途域，下载重核原卷或report权限，不能用普通附件read旁路。加密存储、桥接访问日志、独立密钥和数据恢复沿[敏感设计](Permissions.md#files)。迁移与回滚不得回到旧HR默认可读路径；恢复必须同时还原题/答卷版本、桥接、抑制manifest和历史披露账本，缺任一则保持相关报告禁用。安全deny账本独立核验后才开放，不能从备份复活旧报告令牌。

<a id="acceptance"></a>
## P3夹具、验收和责任

合成主体E、self=E、明确具名唯一经理L、匿名同事A/B/C/D，独立HR管理H（无原卷权）、审计X（有期授权）、报告复核R/发布P。k=3；n=0/2/3和一卷withdraw分别测试；同cohort只改A答案、cohort由ABC变ABD以及并发两个报告测试差分拒绝。四题型及隐藏题/NA均有实际字段夹具。

M26-REVIEW-AC01～12原GWT及后续补充用例见Acceptance_Scenarios.json。证据须显示API没有被抑制字段/计数、不同角色的直接查询拒绝、桥接不进审计、版本与披露账本CAS结果；不只验证均值。P2完成独立设计；P3测评域/共享安全/独立测试负责人实施验证；P4隐私、业务HR及运维核实际多角色匿名承诺和恢复。源站算法与权限深操作未核只形成定向补证请求，不使用CDP。

<a id="repair-001"></a>
## 001契约定向对齐

每题角色、维度和指标精确版本写入套卷题绑定，整卷列表不能推断逐题关联；条件显示与适用角色取AND。 完整字段与拒绝条件见[Contract_Repair.md](Contract_Repair.md)，其规范替换旧版简写中的歧义，其余已通过独立评审内容保持。

<a id="repair-002"></a>
## 002匿名规范和证据

[Anonymity_Repair.md](Anonymity_Repair.md)、[Anonymity_Calculation.md](Anonymity_Calculation.md)及[Anonymity_Cases.json](Anonymity_Cases.json)是本模块精确匿名规则与P3预期来源。P2符号核验不等产品测试；P3/P4责任保持。
