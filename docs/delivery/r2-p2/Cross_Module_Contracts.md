# R2生产者与消费者契约 v1

<a id="ownership"></a>
## 单一业务决定权

|生产者→消费者|传递内容与冻结点|消费者责任/禁止推定|
|---|---|---|
|M37→M06/M26/M18/M17/M03|standardRootId/versionId、维度引用行、indicator/library/scale版本、算法就绪及purpose投影；消费单提交/启动时冻结|新引用必须published且active；历史/在途用原版本，停用只告警或显式取消；不得取latest覆盖|
|M06→M18/M17/M03|certificateId、personId、standardRoot/version、资格等级版本、issued/expiry/revocation、validityStatus/reason、evaluatedAt和sourceRevision|资格是事实/前置证据；M18独立盘点、M17独立入池及准备度、M03独立任用；强前置在实际生效再次核|
|M26→M18/M17/M06/M03|明确用途和受众下的已发布reportRoot/version、允许聚合Cell、匿名policyVersion、cohortManifestDigest；不含桥接和原卷|无报告/抑制/撤权为typed null或禁字段，不能用自评分替非本人报告，不自动决定资格、任用或潜力档位|
|M18→M17|publishedReviewRoot/version、project/snapshot、人员ID、四维来源、九宫格版本、校准依据的允许摘要、suggestionId|只建议；由M17已批准规则/独立审批产生membership或succession；回撤建议不暗删已生效成员|
|M17→M03|successionId、targetKind/targetId、任期/有效窗口、readinessVersion/assessment/due、证据引用及当前可用性|不把候选=任命；M03按自身显式eligibilityPolicy核；旧one_year不得转新3–6月|
|M01→六模块|稳定person、employment/assignment、组织/岗位、当前绑定/退出屏障；必要版本和当前授权关系|不复制维护人事事实；人员离职禁新动作，历史不删；M03实际任用只认可信生效凭证|
|六模块↔M19|冻结businessSnapshot及审批模板；validate/planEffect适配器；审批、后效和通知分列|流程引擎不生产资格/分数/任用政策；D7严格保留|
|六模块→M48|业务root/version、rawStatus、mappingVersion、允许字段、allowedActions及源回执|入口/待办不自建业务状态，实际动作回生产者；撤权清缓存，未知状态禁办理|
|M18/M17及六模块授权摘要→M32|dataset/definitionVersion、rowKey、sourceManifest、Cell/单位/分母、timeMode、purpose|源授权后统计，不拼匿名底层数据；current不能伪装任意历史snapshot|
|M27→M17（已有接口边界）|经核验learningRecordId/version、要求映射、核验人/时间、撤回状态|IDP按冻结任务规则消费；进度100%不是核验通过，不新增M27设计范围|
|M16/外部成就→M18/M37（已有接口边界）|来源类型、发布版本、尺度/单位、允许用途和签名状态|未接为not_configured，不自造绩效结果或启动M38/独立测评|

<a id="catalog"></a>
## 事件与数据集目录

所有事件采用[接口Envelope](Interfaces.md#schema)，事件发布并不授予数据读取权。事件最小payload含VersionRef、状态变更及安全对象引用；消费者再按purpose受控读取。

|事件类型|根与有序流|主要消费者|
|---|---|---|
|r2.m37.standard.published / availability.changed|standardRootId，entityRevision|五模块标准引用及M32目录|
|r2.m06.certification.issued / revoked / validity.changed|certificateId，entityRevision；到期按规则派生事件只一次|M18/M17/M03|
|r2.m26.report.published / withdrawn / access.changed|reportRootId，entityRevision|获授权消费域、M48/M32|
|r2.m18.review.published / corrected / withdrawn|reviewRootId，entityRevision|M17建议收件及M32|
|r2.m17.membership.changed / succession.assessed / idp.verified|各业务root，分流不可混序|M03、M48/M32及授权档案|
|r2.m03.appointment.reconciled / term.changed / report.released|appointmentRecordId/termId/reportRootId|授权档案、M48/M32；不反写M01任职|

M32原`talentReview`行键(reviewRootId,publishedVersionId)保持，仅已发布更正替代当前指针；M18另提供projectSnapshot、meetingVersion和gridDefinitionVersion。原`successionCoverage`按positionId及旧准备度字典保持历史schema；新版按targetKind/targetId/definitionVersion区分岗位与组织，不混分母。新增poolSaturation、readyCoverage、idpOverdue定义另立datasetDefinitionVersion，不能覆盖原21目录和历史报表。具体公式见M17，未准备就绪时目录保留not_configured。

<a id="consumption"></a>
## 消费、撤回与竞争

消费记录consumerReferenceId绑定生产者精确版本、消费业务版本、目的、源revision、capturedAt与安全策略版本；同consumer对象重复事件不得重复创成员、任期或任务。源停用/报告撤回后：当前新读取即时权限收紧；已有业务决定保留其当时证据引用，标source_withdrawn并交业务责任人决定更正，不自动撤销跨域合法决定。需要新决议时显式supersedes链，不能借对账擦掉历史。

在途标准被停用仍按批准冻结版本继续且告警；业务负责人可显式取消，不能把停用等同所有消费者取消。M06证书revoked/expired作为当前有效性与标准停用不同：对要求有效资格的任用/ready校验必须阻断。M26报告撤回或撤权不能借历史引用继续获取原报告内容；业务审计只保留合法取得时的最小证据引用及可授权摘要。

同DB提交核依赖revision和当前时间；跨域异步投影允许标明延迟，只用于展示，强资格/任用前置必须读取可信生产者最新状态。外部无法核实返回unknown并阻关键动作。生产者重启/恢复后先校验recoveryEpoch和连续sourceRevision，再恢复消费。旧consumer不可表达新版对象时unsupported而非扁平化丢失。

本包接口约定供后续R1/R2 P3负责人联合验证，不登记其他Release完成。R2所有可用性初始为design_only、realIntegration=not_executed。
