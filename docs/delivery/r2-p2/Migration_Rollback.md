# R2迁移、兼容与回滚设计

<a id="mapping"></a>
## 来源与逐域映射

继承固定R1迁移控制（migration_run/map/issue/batch、writerEpoch、租约fence、逐键摘要及恢复行日志），新增R2映射版本，不另建互相竞争的租户迁移器。`storage_version=1`是旧CAS条件，不直接改为2；R2域schemaVersion与租户feature gate单列。P2不读取真实人员行、不执行DDL/迁移，实际表/容量/孤儿数量均待P3隔离及P4生产核实。

|旧记录|确定性可复用|禁止推定及隔离|
|---|---|---|
|standard id/code/version/anchors|原id作为legacyVersionId保留，原五anchors及内容摘要完整存档；经核验同code同历史链才映射一个root|同名/同code不能自动合根；新library/indicator/child ID只标migration_generated，不声称原站UUID；缺尺度/purpose为not_configured|
|qualification_standard/application/certification|原记录/员工/版本/证据ID、已记录certNo/日期/撤销状态；保留旧validUntil空值的legacy政策解释|新规则validityMode必须显式；旧空值不补未来日期或伪造审批/续期；等级/指标不可靠映射进issue|
|feedback project/invite/response/report|原ID、角色文字、题目1–5版本、最后可见答卷内容和报告摘要|旧覆盖过的答卷中间版本标unknown，不能重建；旧HR权限不迁入原卷grant；低样本旧报告转legacy_restricted，原字节保留但当前公开禁读|
|talent project/review/review_version|原项目/人员/已发布版本/更正链、九宫格原值及原尺度|未存会议/首次复核凭证为legacy_observed；新九宫格不重算覆盖旧结果，缺绩效/潜力轴为unrated|
|talent pool/member/succession/IDP|池/成员/继任/计划原ID、旧状态及ready/one_year/two_years原枚举版本|旧出池重入链只有明确证据才连previousMembershipId；不从时间猜；旧IDP单行动不伪造已核验阶段，组织/岗位目标不混|
|cadre/term/nomination/observation/interview|原person/term/记录ID、日期、登记状态、已知证据；StaffID留namespace|registered不是已批准任命；无transfer.details不能降级认approved即applied；旧期间重叠隔离当前任用，原记录不删|
|attachments/events/audits|原key、摘要、版本归属、墓碑、原时间和actor；合法当前字段裁剪|缺字节/摘要不符不标可下载；旧敏感全payload事件隔离专用历史访问域，不复制到新通用审计|

每mapping键为tenant+sourceTable+sourceKey+mappingVersion+ordinal，记录sourceDigest、sourceRevision、targetRoot/version、confidence、issueId、observedAt。原历史证据与推导目标分列；一对多新对象不会变成“已在原站确认”。来源重复/环/跨租户/未知版本/敏感归属不明都进quarantine，只有受影响动作阻断，其他对象继续。

<a id="cutover"></a>
## 有界切换与冲突处理

阶段inventoried→expanded→writers_guarded→backfilling→reconciling→read_switched→features_enabled→monitored，任一步可paused/failed。先兼容写闸门覆盖全部旧API、后台、上传和批处理；旧客户端无法满足新授权和版本条件时禁写。每批建议100行、≤80语句、≤4MiB取实际小值，稳定主键seek，游标/目标/映射/回执同事务。租约接管增加fence；旧fence提交拒绝。

回填核source revision+digest；源改变整批不提交，重读局部分区；不能先推进cursor再补数据。迁移发现已发布旧报告会违反新匿名要求，先为该报告建立deny tombstone再切读，保留原字节在限制历史域，不用等待全租户回填完成才堵泄漏。桥接写在同事务双写可表达旧投影和新模型；不可表达的新子对象只写新模型，旧路由返回CLIENT_UPGRADE_REQUIRED，不丢弃新字段。

切读逐键验证源→目标覆盖、所有旧历史哈希、标准引用版本、证书有效性口径、匿名披露范围、发布指针、成员任期区间、干部实际生效凭证、附件归属及当前权限。只比较总数不足。当前与历史查询固定schemaEpoch/workspaceRevision/permissionDigest，不能混读不同修订组装假快照。没有历史源版本支持则HISTORY_UNVERIFIABLE。

<a id="rollback"></a>
## 回滚与修复

|阶段/故障|可执行设计|不可做|
|---|---|---|
|扩表/回填尚未启新业务|关新feature/read，保留桥接写闸门、映射和新表；回兼容只读或已验证兼容写|不DROP，不回退不识别epoch的旧writer|
|批次超时unknown|查同batch回执、游标及source digest；同键接续|不另起run覆盖成功行|
|新模型已产生有效业务|前向修复，或在隔离环境按可信恢复点重放完整事务并对账恢复点后命令|不把新报告/任期/多阶段IDP降回旧五级/单状态写模型|
|身份/来源映射冲突|冻结相关新动作，受控人工核证后新增mapping版本；保留旧映射/原因|不按名字合并、不改原ID、伪造有效日期或原审批|
|业务已生效但消费者未确认|保留生产者事实，重建投影/对账回执|不自动回滚M01人事、不重复任用|
|恢复后权限旧/外部unknown|保持隔离，先当前deny账本校准、外发fence和逐单对账|不恢复旧HR原卷权限、不重发未知通知|

恢复点后的合法写入先登记reconciliation manifest，不能无声丢弃；旧客户端下载副本不能用回滚回收。DDL可重入但不假设全DDL事务回滚，逐步摘要及成功状态分开记录。源档案业务保留期限沿来源政策；30天是恢复窗口，不是允许删历史的依据。

责任：P3迁移负责人写隔离迁移器/合成冲突夹具，模块负责人验证语义、安全负责人验证撤权及敏感隔离；P4数据HR核真实冲突、运维核恢复和容量，所有者批准生产切换。本轮没有执行这些动作。
