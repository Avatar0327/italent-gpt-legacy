# 关键门禁全查记录

共56项：六模块30项、横向19项、退出7项。全部逐项阅读判断；JSON引用经独立核对。这里的“设计满足”不代表实现、业务或恢复测试通过；同一Major被多个门禁引用，发现数量只计一次。

|门禁|范围/问题|判断|证据与理由|设计章节|未来验收引用|
|---|---|---|---|---|---|
|M37-01|M37：根对象、版本及逐等级子集字段|缺口（R2-EXIT-001）|根/子版本明确；等级alias/elementText未落实到严格输入|M37_Design.md#m37-spec-01|R2-P3-M37-REVIEW-AC01, R2-P3-M37-REVIEW-AC02|
|M37-02|M37：尺度、权重、缺值与组合|设计满足|精确decimal、同量纲、正权重、mandatory缺值不缩分母，序数不隐式均值|M37_Design.md#m37-spec-02|R2-P3-M37-REVIEW-AC03, R2-P3-M37-REVIEW-AC04, R2-P3-M37-REVIEW-AC05|
|M37-03|M37：子集与用途权限|设计满足|read/use/export各自授权，面试问题和发展建议白名单，历史当前裁权|M37_Design.md#m37-spec-04|R2-P3-M37-REVIEW-AC09, R2-M37-S04|
|M37-04|M37：审批、发布、停用及在途版本|设计满足|语义摘要防审批后改文，显示例外有边界；停用阻新用，旧在途不自动取消|M37_Design.md#m37-spec-03|R2-P3-M37-REVIEW-AC06, R2-P3-M37-REVIEW-AC07, R2-M37-S01|
|M37-05|M37：五个消费者精确版本|部分满足（R2-EXIT-001）|M06/M26/M18/M17/M03均冻结同根版本；外部引用字段需修正schema|M37_Design.md#m37-spec-05, Cross_Module_Contracts.md#catalog|R2-X-01, R2-X-02|
|M06-01|M06：类别、级别、指标、评分与评级对象|缺口（R2-EXIT-001）|独立类别/资格级别/评级级别已定义；指标类型配置输入未完整承载|M06_Design.md#m06-spec-01, M06_Design.md#m06-spec-02|R2-P3-M06-REVIEW-AC01, R2-P3-M06-REVIEW-AC03|
|M06-02|M06：委员会、贡献者回避、缺评与阈值|设计满足|冻结eligible set，全部应评明确票/弃权；缺评不缩分母，否决/unknown阻认证|M06_Design.md#m06-spec-04|R2-P3-M06-REVIEW-AC08, R2-P3-M06-REVIEW-AC09|
|M06-03|M06：有效期、续证、撤销与失效|设计满足|截止D含当日、D+1派生expired；同旧证唯一续证，旧证不覆写，撤销独立权限|M06_Design.md#m06-spec-04|R2-P3-M06-REVIEW-AC10, R2-M06-S03, R2-X-03|
|M06-04|M06：发布启停与授证原子性|设计满足|批准和issued分态，提交CAS重核、重复占位、证书/审计/receipt原子|M06_Design.md#m06-spec-03, M06_Design.md#engineering|R2-P3-M06-REVIEW-AC04, R2-P3-M06-REVIEW-AC05, R2-COM-01|
|M06-05|M06：资格结论不替代任用|设计满足|certificateSnapshot保留evaluatedAt和current validity；M03独立决定并重核|M06_Design.md#m06-spec-05, Cross_Module_Contracts.md#ownership|R2-P3-M06-REVIEW-AC12, R2-X-03, R2-X-04|
|M26-01|M26：问卷、邀请、答卷和报告版本|部分满足（R2-EXIT-001）|根/版本及项目跨角色邀请唯一明确；逐题适用角色/维度输入关系缺口|M26_Design.md#m26-spec-01, M26_Design.md#m26-spec-03|R2-P3-M26-REVIEW-AC01, R2-P3-M26-REVIEW-AC06, R2-P3-M26-REVIEW-AC07|
|M26-02|M26：匿名身份映射隔离|设计满足|运营/答卷/桥表分别授权，不进入通用事件、日志、URL或M32 join|Permissions.md#anonymity, M26_Design.md#m26-spec-01|R2-P3-M26-REVIEW-AC02, R2-M26-S04|
|M26-03|M26：低样本、差分及跨报告组合推断|缺口（R2-EXIT-002）|阈值、补集、历史披露账本正确设门，但源答案版本参与签名含义不能唯一执行|M26_Design.md#m26-spec-02, Permissions.md#anonymity|R2-P3-M26-REVIEW-AC03, R2-P3-M26-REVIEW-AC04, R2-M26-S01, R2-M26-S02, R2-M26-S07|
|M26-04|M26：报告授权、撤权、更正与重发布|部分满足（R2-EXIT-002）|旧链接deny、重新授权及旧披露约束保留；更正匿名决定依赖002修正|M26_Design.md#m26-spec-04, Permissions.md#recusal|R2-P3-M26-REVIEW-AC09, R2-X-05, R2-X-06|
|M26-05|M26：原卷/文本和零样本报告|设计满足|零合格非self组不得发布；原文需独立脱敏，HR无默认原卷权，低样本无精确人数|M26_Design.md#m26-spec-02, Permissions.md#anonymity|R2-P3-M26-REVIEW-AC05, R2-M26-S03, R2-M26-S06|
|M18-01|M18：对象、项目、评价、会议与历史来源|缺口（R2-EXIT-001）|范围快照和对象子ID独立；previousResultRef无严格输入结构|M18_Design.md#m18-spec-01|R2-P3-M18-REVIEW-AC01, R2-P3-M18-REVIEW-AC04|
|M18-02|M18：绩效/潜力轴映射及缺失|设计满足|映射/阈值版本固定；边界等值确定；缺失和unknown不补0或强制落格|M18_Design.md#m18-spec-02|R2-P3-M18-REVIEW-AC05, R2-M18-S03|
|M18-03|M18：校准回避、驳回与重开|设计满足|参与/评价/复核/发布职责区分，利益冲突剔除有版本，重开不改旧发布|M18_Design.md#m18-spec-03|R2-P3-M18-REVIEW-AC06, R2-P3-M18-REVIEW-AC07, R2-P3-M18-REVIEW-AC08, R2-M18-S01|
|M18-04|M18：发布快照和当前受众|设计满足|首次发布和更正均独立审批，完整manifest后一次发布，历史查询重核当前权限|M18_Design.md#m18-spec-04|R2-P3-M18-REVIEW-AC09, R2-P3-M18-REVIEW-AC10, R2-M18-S04|
|M18-05|M18：盘点不自动改变池/任用|设计满足|只给来源或建议，M17/M03各自命令产生有效成员或任用事实|M18_Design.md#m18-spec-05, Cross_Module_Contracts.md#ownership|R2-P3-M18-REVIEW-AC11, R2-P3-M18-REVIEW-AC12, R2-X-01|
|M17-01|M17：池规则、成员有效区间及重入历史|设计满足|规则版本/评估点/幂等键明确，区间互斥；重入新ID+previousMembershipId|M17_Design.md#m17-spec-01|R2-P3-M17-REVIEW-AC01, R2-P3-M17-REVIEW-AC02, R2-P3-M17-REVIEW-AC03, R2-M17-S01|
|M17-02|M17：继任任期、准备度词典及版本|设计满足|任期/复核/人员/岗位/资格共同决定当前有效；准备度不是资格或任命|M17_Design.md#m17-spec-02|R2-P3-M17-REVIEW-AC04, R2-P3-M17-REVIEW-AC05, R2-P3-M17-REVIEW-AC06, R2-X-03|
|M17-03|M17：IDP职责、动态角色与自核回避|设计满足|本人不能唯一指导/最终核验，动态解析失败阻节点，替换留版本历史|M17_Design.md#m17-spec-03|R2-P3-M17-REVIEW-AC07, R2-P3-M17-REVIEW-AC08, R2-M17-S02|
|M17-04|M17：模板、阶段、任务依赖及取消|设计满足|模板版本、阶段/任务DAG、必需任务核验、免除须独立授权；学习完成不自动IDP完成|M17_Design.md#m17-spec-04|R2-P3-M17-REVIEW-AC09, R2-P3-M17-REVIEW-AC10, R2-M17-S03|
|M17-05|M17：组织健康分母和历史口径|设计满足|岗位/组织/池分母分列，distinct人员、current有效性及真实snapshot分开；无综合权重not_configured|M17_Design.md#m17-spec-05|R2-P3-M17-REVIEW-AC11, R2-P3-M17-REVIEW-AC12, R2-M17-S04, R2-X-08|
|M03-01|M03：干部身份、任期、任职与任免记录|设计满足|person/cadre/term/assignment/appointment独立，闭区间、月末闰年算法和重叠检查明确|M03_Design.md#m03-spec-01|R2-P3-M03-REVIEW-AC01, R2-P3-M03-REVIEW-AC02, R2-M03-S01|
|M03-02|M03：委员会评分、弃权/缺评与等值|设计满足|票数及精确数值分开，缺评阻完成，弃权计明确分母；等值按冻结比较符，不用显示舍入|M03_Design.md#m03-spec-03|R2-P3-M03-REVIEW-AC05, R2-P3-M03-REVIEW-AC06, R2-P3-M03-REVIEW-AC07, R2-M03-S02|
|M03-03|M03：考察延期、转正、退出与撤回|设计满足|到期不自动转正；独立结论、退回新申请版本；结束/撤回不反写真实人事历史|M03_Design.md#m03-spec-04|R2-P3-M03-REVIEW-AC08, R2-P3-M03-REVIEW-AC09|
|M03-04|M03：述职、奖惩、访谈及敏感档案|设计满足|周期/版本及敏感动作字段独立；附件下载和历史同受当前授权，档案read不代interviewRead|M03_Design.md#m03-spec-05, Permissions.md#matrix|R2-P3-M03-REVIEW-AC10, R2-P3-M03-REVIEW-AC11, R2-P3-M03-REVIEW-AC12, R2-M03-S04|
|M03-05|M03：M01实际生效与资格失效联动|设计满足|批准不当applied；M01可信receipt后核对，unknown查同键；资格到期在各决定点重核；不自动撤销已发生M01事实|M03_Design.md#m03-spec-02, Cross_Module_Contracts.md#consumption|R2-P3-M03-REVIEW-AC03, R2-P3-M03-REVIEW-AC04, R2-M03-S03, R2-X-03, R2-X-04|
|H-01|横向：稳定ID、根/版本与时间区间|设计满足|租户复合键、稳定person、UUID版本、展示序号不作FK，历史未知不补造|Architecture.md#objects|R2-COM-05, R2-X-02|
|H-02|横向：行级/列级/动作授权及组合grant|设计满足|完整grant各自求对象字段再并集；不得拼角色A范围与角色B字段|Permissions.md#authorization|R2-X-05, R2-X-06, R2-X-07|
|H-03|横向：当前权限与历史权限分离|设计满足|历史快照仅解释历史，deny先行，缓存带authRevision/epoch，敏感数据无stale回退|Permissions.md#authorization, Permissions.md#recusal|R2-COM-08, R2-X-05|
|H-04|横向：自审、利益冲突和回避|设计满足|历史实质贡献者冻结，改派有理由版本，不足合格人数blocked，D7不委托干预|Permissions.md#recusal, Architecture.md#lifecycle|R2-P3-M06-REVIEW-AC08, R2-P3-M18-REVIEW-AC07, R2-M17-S02|
|H-05|横向：审批与业务生效分离|设计满足|M19返回本地事务计划不自行commit/network；生产者拥有决定权|Architecture.md#lifecycle, Cross_Module_Contracts.md#ownership|R2-X-03, R2-X-04, R2-X-07|
|H-06|横向：CAS、并发、幂等和unknown|设计满足|共用租户revision；expected auth/writer/recovery/fence；同键异payload冲突、墓碑不释放，未知不换键|Architecture.md#transaction|R2-COM-01, R2-COM-04|
|H-07|横向：乱序、重放、gap和对账|设计满足|事件同ID同digest去重，异digest隔离，跳号阻投影，不取latest掩盖缺口|Interfaces.md#reconciliation, Interfaces.md#failure|R2-COM-03|
|H-08|横向：业务/审计/receipt/outbox/恢复日志原子性|设计满足|同事务全部提交或全无业务效果；DB故障不能承诺同库失败日志必写|Architecture.md#transaction|R2-COM-01|
|H-09|横向：有界作业、租约与部分报告|设计满足|fence接管、cursor原子推进，准备不可见、完整manifest最终一次ready|Architecture.md#transaction|R2-COM-02|
|H-10|横向：严格schema与版本|缺口（R2-EXIT-001）|69定义/76动作结构引用成立；5组核心语义输入不一致，结构核验不能代替此项|Interfaces.md#schema, Interface_Schemas.json|R2-COM-04|
|H-11|横向：签名、信任与失败分态|设计满足|hash不作签名；nonce/key/时窗/来源核对；not_configured/unknown不写成成功|Interfaces.md#trust, Interfaces.md#failure|R2-COM-03, R2-COM-04|
|H-12|横向：跨模块撤权与对账|设计满足|旧链接/缓存不能绕源撤权；已合法决定保留受控引用，独立更正，不重算原卷|Cross_Module_Contracts.md#consumption, Permissions.md#recusal|R2-X-05, R2-X-06|
|H-13|横向：迁移、兼容与隔离|设计满足|保留原ID/哈希/五anchors/旧证策略；冲突隔离；新写epoch阻旧writer；未知来源不合并|Migration_Rollback.md#mapping, Migration_Rollback.md#cutover|R2-COM-05, R2-COM-06|
|H-14|横向：不可逆迁移与回滚|设计满足|有新事实后只读或前向修复，不DROP新模型、不恢复旧弱权限写路径|Migration_Rollback.md#rollback|R2-COM-06|
|H-15|横向：附件、下载、删除墓碑及敏感日志|设计满足|不可见对象先写再绑定；orphan无读权；下载两端重核；墓碑先禁读，恢复点引用字节保留，日志不含原文|Permissions.md#files|R2-COM-05, R2-X-06, R2-M03-S04|
|H-16|横向：RPO≤60/RTO≤240/保留30天|待实证（R2-EXIT-006）|目标未提升；共同可恢复点，RTO计至owner开放，缺披露账本或当前deny不得开放|Recovery_Cost_Responsibilities.md#targets, Recovery_Cost_Responsibilities.md#recovery|R2-COM-07, R2-COM-08|
|H-17|横向：供应商/平台未验证不冒达标|待实证（R2-EXIT-006）|托管作业/密钥/备份日志/成本待核；真实测评/签署/通知均仅契约|Recovery_Cost_Responsibilities.md#cost, Interfaces.md#failure|R2-COM-04, R2-COM-07|
|H-18|横向：六基础差异场景适用性|需修订（R2-EXIT-003）|16基础AC原文未丢；三项只追加R2对象句，仍留薪酬/课程操作需明确映射|Foundations.md, Acceptance_Scenarios.json|R2-P3-BASE-02-AC03, R2-P3-BASE-03-AC02, R2-P3-BASE-04-AC02|
|H-19|横向：P3任务可排程与R1依赖|需修订（R2-EXIT-004, R2-EXIT-005）|有46任务和双向场景引用，缺固定实现SHA/明确依赖图；本评审给完整建议|P3_Work_Packages.json, Architecture.md#authority|R2-X-07, R2-X-08|
|E-01|退出：固定设计/最终包装来源|满足|11固定引用按7ff3对象核；两份动态清单各在自身HEAD核，78源引用校验|Controller_Proposal.json, Artifact_Manifest.json, Source_Manifest.json|独立来源/数量记录|
|E-02|退出：数量、唯一性与批准追踪|部分满足（R2-EXIT-001）|6/33/295/149/24/78/16/17/5核算一致；语义未全闭合|Requirements_Trace.json, Approval_Provenance.json|独立来源/数量记录|
|E-03|退出：46任务及138场景状态|满足|任务均proposed_not_started；场景均not_run；存在文件不等通过|P3_Work_Packages.json, Acceptance_Scenarios.json|独立来源/数量记录|
|E-04|退出：6组LIMIT及52互斥责任|部分满足（R2-EXIT-001, R2-EXIT-002）|完整0；P3/P4各6组重叠；15/25/12正确，6个P2关闭标签暂不接受|Original_Limits.json, Limit_Resolution.json|独立来源/数量记录|
|E-05|退出：无历史测试/R1在制证据冒认|满足|历史计数和旧状态限定来源，R1当前实现未作为本次设计完成证据|Historical_Test_Provenance.json, Exit_Review.md, Resume.md|独立来源/数量记录|
|E-06|退出：产品/部署/准入/审批边界|满足|原设计59改动均仅文档及检查脚本；proposalOnly且未批准P2退出/P3进入；本评审仅新增评审文件|Controller_Proposal.json, Resume.md|独立来源/数量记录|
|E-07|退出：Blocker=0及未处置Major=0|不满足（R2-EXIT-001, R2-EXIT-002）|Blocker为0，未处置Major为2，不能建议所有者批准退出|Exit_Review.md|独立来源/数量记录|
