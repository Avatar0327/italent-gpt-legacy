# M37人才标准详细设计

设计输入：M37-SPEC-01～05、BP-C-REQ-07及M37-LIMIT-01，批准`M37-P1-APPROVAL-R2-20260909`。本模块设计闭环，不代表已实现或P2退出批准。

<a id="m37-spec-01"></a>
## 稳定对象、字段和子集

|对象|字段、唯一性与约束|根/版本关系|
|---|---|---|
|indicator_library|libraryId、name(trim 1–200)、type=ability/potential/experience、description≤500、classification可空、availability|libraryRoot稳定；内容变更新libraryVersion，已有指标后type不得原地变更|
|indicator|indicatorId、libraryId、code/name(trim 1–200)、definition≤500、aliases、versionId|code在同库trim后区分大小写唯一（停用不释放）；name可重名，选择显示库/类型/code/version；改名不换ID|
|indicator_child|childId、indicatorId、subset=level/behavior/development_suggestion/interview_question、sort、description|每子集独立ID；sort正整数、同父同子集唯一；level说明必填≤500，其余必填≤4000；级数不固定5|
|talent_standard|standardRootId、versionId、name 1–200、classification/modelLabel/elementLabel可空、purposeReadiness|标准与指标库不同根，不自动建M38模型或M06资格；发布版本不可改|
|standard_line|referenceLineId、standardVersionId、dimension=ability/potential/experience/achievement、indicatorVersionRef或externalAchievementRef、target、weight|成就须显式source/type/version，不映射为潜力或绩效；引用精确子版本，禁止跨租户或只按名引用|

已有record.id按原version保留。能证实同code的合法连续版本才形成root mapping，名称相同不是证据；结构未知保留legacyAnchors和来源，不伪称原站共享对象UUID已核实。库、指标、子集各有稳定根/不可变内容版本；标准发布snapshot包含完整依赖VersionRef及digest，单独目录更新不漂移旧标准。

<a id="m37-spec-02"></a>
## 目标、尺度和组合算法

target为numeric/ordinal/boolean/enum/none的有标签联合类型。numeric显式min/max/step/unit/direction且min<max、step>0，值在范围且落步长；decimal精确计算。ordinal指向真实levelId集合及顺序，不把“第几级”当通用数；boolean只能true/false，enum选项稳定ID，none为未设目标，null表示缺值而非0。库与标准可供只读目录发布，但相应用途计算须purposeReadiness=ready，所需字段/规则缺失为not_configured并阻该用途提交。

weight默认1、有限且≥0，0明确排除聚合；至少一项正权重才允许求加权均值。仅在同量纲、同尺度转换版本的数值集合按sum(value×weight)/sum(weight)求值；不跨能力/潜力/经历/成就求未经定义的总分。必需输入缺失返回null+missing_required，不能用已有项缩分母蒙混通过。非必需项的排除/NA分母策略须在该purpose规则版本显式定义。

达标规则采用版本化AND/OR AST，叶节点引用referenceLineId及明确比较符；禁止环、未定义节点、任意脚本、不同单位直接比较。序数先有明确映射才能算均值，默认只保留等级/分布；文本不自动计分。规则发布校验可达叶子、类型一致、至少一个有效条件；unconfigured/unknown均不得判通过。技术AST限制沿R1有界解析，可收紧复杂度但不得静默丢条件。

<a id="m37-spec-03"></a>
## 审批、版本与停用

draft→submitted→approved→published；submitted可withdrawn/rejected，修改产生新的内容及申请版本重新走独立M19审核。发布核当前publish权、非本人/材料贡献人审核完成、依赖版本和semanticDigest一致；已批准内容又改变则拒绝。库/指标的语义改动同样新版本及独立审核，不能通过“改描述”绕变更目标含义。

显示性排序/分类调整仅在内容语义摘要相同且独立displayPublish授权时允许管理者发布新版本；算法、指标含义、等级、权重、用途或读者范围变化均不在此例外。完整contentDigest和semanticDigest同时留存，例外动作独立审计。

availability=active/disabled由独立状态事件记录，停用不改已发布版本字节。新引用读取published+active并在提交CAS再核；已启动的M06/M26/M18/M17/M03消费继续冻结旧版本、标source_disabled，业务负责人可另走显式取消。指标停用阻新选入其他标准，但已发布标准依赖旧指标快照不被破坏。撤回未发布内容不影响旧published；更正发布新version+supersedes，不物理删历史或伪造原审批。

<a id="m37-spec-04"></a>
## 范围与角色

read/use/manage/review/publish/export独立动作，默认不共享。目录read不当然授权业务use，业务use只返回该purpose需要的指标/尺度，不授完整库；面试问题和发展建议用显式purpose白名单及敏感字段grant。HR/管理员可获得目录管理授权但不默认有审核/导出，经理只有声明范围，本人没有隐式标准全库权。审核排除subject（如针对指定对象）、提交者和历史实质贡献人；撤权对历史和下载同样生效。采用[完整grant元组](Permissions.md#authorization)，不靠前端隐藏。

<a id="m37-spec-05"></a>
## 消费、证据和旧实现差异

五消费者读取`standardSnapshot`：标准根/版本、lineId、维度、库/指标/子集版本、typedTarget、weight、ruleVersion、purposeReadiness、availability及digest。M37只给定义和计算契约，不写任何人的能力结果、证书、盘点格、继任准备度或任命。需要外部成就/测评时保留sourceNamespace/externalId/版本/签名及not_configured，不发真实测评、不恢复独立AI。

旧`development.ts`固定5 anchors、create即active和all-member canRead只能作legacy读取证据，须替换新版写路径；旧消费者保留精确旧版本和原5anchors schema，无法表达新增子集则明确unsupported，不把新标准压成5级。同名代码冲突隔离，来源UUID未知形成结构化补证请求，不阻已批准稳定ID设计。

<a id="engineering"></a>
## 命令、事务、迁移和恢复

|命令|payload必填与前置|同事务输出|
|---|---|---|
|m37.library.create / indicator.create|上述字段；父库版本、唯一code、合法type|根/版本、索引占位、审计/receipt|
|m37.version.edit|rootId、baseVersionId、patch白名单；draft或新修订；childIds/sort全约束|新内容版本，原版保留|
|m37.standard.submit|standardVersionId、purpose规则、依赖manifest、workflowTemplateVersion|冻结申请版本、M19实例、材料贡献人集合|
|m37.standard.review / publish|applicationVersion/decision/reason或approvedVersionId；独立角色、无语义漂移|审批/发布事件、当前指针、outbox、恢复行日志|
|m37.availability.change|objectType/rootId、expected availability、target、reason|停用状态事件；新引用屏障，不批量覆写消费者|
|m37.snapshot.query / export|精确VersionRef、purpose、字段白名单|仅当前授权投影；下载按版本及export重核|

所有命令使用[公共严格Envelope](Interfaces.md#schema)和[原子CAS](Architecture.md#transaction)。并发同库同code只一成功；同根两发布只有一个expectedRevision成功；同键异payload冲突，unknown查同receipt。文件先不可见写入再绑定，失败孤儿无下载权；版本事件审计不泄露敏感子集文本。

迁移依[逐域映射](Migration_Rollback.md#mapping)：原ID和五anchors完整保留，新增ID标migration_generated，版本冲突只阻相关根。回滚关闭新写能力、保持兼容只读/桥接writer，不能删除新子集或回滚至旧全库可读路径。恢复必须包含全部子版本、引用manifest、发布/停用事件、审计和当前安全屏障，达标证据归P3/P4。[恢复目标与责任](Recovery_Cost_Responsibilities.md#targets)全部适用。

<a id="acceptance"></a>
## P3可执行验收与责任

合成夹具：租户T-A/T-B；目录L-ABILITY/L-POTENTIAL；指标I-01在两库可同code，同库重复拒绝；稳定STD-ROOT的v1/v2，v1含3级、v2含6级；独立管理H、复核R、发布P，消费者E与撤权用户X。所有ID是隔离测试符号，P3由服务端分配真实测试UUID，不访问真人。

原M37-REVIEW-AC01～12逐一保留GWT并映射至`Acceptance_Scenarios.json`（随模块生成）；额外覆盖并发发布、停用/引用竞争、unknown及历史子集下载撤权。断言需查对象版本/当前指针/审计/回执/consumer digest，不能只断言HTTP200或界面存在。

P2：以上对象、尺度、生命周期、范围及契约设计关闭。P3：标准实施负责人+独立测试负责人实现五项SPEC并验证合成数据、迁移冲突及消费兼容。P4：业务标准负责人核真实用途和跨角色，安全/运维核敏感子集和恢复。原站子集保存、共享UUID等未核事实保留补证责任，不宣称等同本设计已执行。
