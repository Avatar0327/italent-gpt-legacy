# 三项基础AC的R2定向适配

原始AC及basis保留在Requirements_Trace和Acceptance_Scenarios.originalFoundationGwt；下列不构成执行通过。附件动作是R1共享adapter的P2操作名，待A槽位冻结绑定实际接口；不能据此宣称已有运行路由。

## R2-P3-BASE-02-AC03

继承BASE-02-AC03本人投影不授管理/原始来源权；原薪酬、单位承担字段仍在originalFoundationGwt，本R2以报告反馈/匿名原卷/桥接替代具体对象，不改变原R1AC。

Given：T-A中E1只具REP1-v1的developmentSummary字段reportRead；H只有PROJECT1邀请管理，L只有E1名册read；匿名原卷RAW-A-v1与桥表均restricted，authRevision=10。

When：E1请求获准发展反馈；E1/H/L分别直接请求RAW-A-v1.answers及REP1-v1的anonymousMean/bridgeReviewer；H与L请求该本人反馈。

Then：E1反馈仅返回developmentSummary；无原卷/桥表/均值字段权限的整字段请求403，H/L反馈403，不能借本人或管理名义放行。REP1-v1和RAW-A-v1字节及版本保持；安全审计不含答案/评委映射。

允许字段：developmentSummary (E1 only)。禁止字段：answers, bridgeReviewer, anonymousMean (no matching field grant)。

夹具、动作、角色及每个版本预期逐字段见Foundation_Adaptations.json。
## R2-P3-BASE-03-AC02

继承BASE-03-AC02审计与业务历史按语义分别计数；员工普通字段/任职历史原AC保留，R2改为目录展示字段内容版本与证书撤销历史，不要求两类条数相等。

Given：CT1-v1为category草稿，完整CatalogDraft如fixture；H仅能改name，CERT1-v1已合法授E1且有效；独立R具revoke，不是本人/原申请贡献者；初始workspaceRevision=20。

When：H以CT1 root和完整payload将name改为新名称，其余字段原样，expectedEntityRevision=1；读成功receipt后R以businessVersionId=CERT1-v1、reason=资格材料失效提交certification.revoke，使用最新revision和新幂等键；再以同键重发撤销。

Then：改名创建CT1-v2、内容审计和一次applied receipt，不新增certificate或M01任职历史；CERT1-v1授证字节保留。撤销成功时生成独立revocation事件一次，current validity=revoked，revokedAt为服务端提交时刻；同键重发同receipt不多增历史。未授权改issuedAt/personId/actor拒绝；审计失败则相应业务状态无变更。

允许字段：catalog.name (changed field only), ReasonAction.businessVersionId, ReasonAction.reason。禁止字段：issuedAt, personId, approvalState, auditActor, certificate history on catalog edit。

夹具、动作、角色及每个版本预期逐字段见Foundation_Adaptations.json。
## R2-P3-BASE-04-AC02

继承BASE-04-AC02已发布附件不可改及新版本独立关联；原course AC保留。R2明确报告v1/v2与B1/B2：默认不复制附件绑定，需要新bind；复用同object字节也须新binding及当前授权，不复制读权限。

Given：REP1-v1已published且B1绑定OBJ-A-v1；REP1-v2是同根独立draft、更正来源指v1。H仅具草稿管理/绑定及旧报告read，OBJ-B-v1不可见准备对象，两对象合成摘要固定。

When：通过R1共享附件adapter依次解绑或替换REP1-v1.B1；然后为REP1-v2创建新绑定B2指OBJ-B-v1，再读取旧版B1。

Then：前两请求409 IMMUTABLE_VERSION，旧binding/digest/对象字节不变；第三请求创建B2并仅使v2草稿关联可见，v1仍读OBJ-A-v1，不能覆盖B1或冒充发布。新附件不继承旧版受众；沿当前grant及v2 owner范围，任何无权下载403。删除草稿绑定先墓碑禁读，物理回收不得破坏旧版或恢复点引用。

允许字段：ownerVersionId (draft only), objectVersionId, purpose, expectedOwnerRevision, bindingId (draft unbind only)。禁止字段：overwrite object bytes, published owner binding change, source reviewer identity, set published state。

夹具、动作、角色及每个版本预期逐字段见Foundation_Adaptations.json。
