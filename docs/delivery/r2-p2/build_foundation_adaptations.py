"""Three source-preserving concrete R2 desktop fixtures."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
A={}
A['R2-P3-BASE-02-AC03']=dict(
 fixture=dict(tenant='T-A',subject='E1',manager='L',hr='H',report={'rootId':'REP1','versionId':'REP1-v1','state':'published','audience':['E1'],'fields':{'developmentSummary':'协作建议','anonymousMean':'4'}},rawResponse={'rootId':'RAW-A','versionId':'RAW-A-v1','bridgeReviewer':'A','answers':['2']},grants=[{'actor':'E1','object':'REP1-v1','action':'reportRead','fields':['developmentSummary']},{'actor':'H','object':'PROJECT1','action':'manageInvites','fields':['inviteStatus']},{'actor':'L','object':'E1','action':'rosterRead','fields':['name','org']}],authorizationRevision=10),
 actions=['M26.report.query(REP1-v1,purpose=development_feedback,fields=[developmentSummary])','M26.response.query(RAW-A-v1,fields=[answers])','M26.report.query(REP1-v1,fields=[anonymousMean,bridgeReviewer])'],actors=['E1','H','L'],allowedFields=['developmentSummary (E1 only)'],forbiddenFields=['answers','bridgeReviewer','anonymousMean (no matching field grant)'],
 given='T-A中E1只具REP1-v1的developmentSummary字段reportRead；H只有PROJECT1邀请管理，L只有E1名册read；匿名原卷RAW-A-v1与桥表均restricted，authRevision=10。',
 when='E1请求获准发展反馈；E1/H/L分别直接请求RAW-A-v1.answers及REP1-v1的anonymousMean/bridgeReviewer；H与L请求该本人反馈。',
 then='E1反馈仅返回developmentSummary；无原卷/桥表/均值字段权限的整字段请求403，H/L反馈403，不能借本人或管理名义放行。REP1-v1和RAW-A-v1字节及版本保持；安全审计不含答案/评委映射。',
 expectedVersions={'REP1-v1':'unchanged','RAW-A-v1':'unchanged','authorizationRevision':10},
 inheritance='继承BASE-02-AC03本人投影不授管理/原始来源权；原薪酬、单位承担字段仍在originalFoundationGwt，本R2以报告反馈/匿名原卷/桥接替代具体对象，不改变原R1AC。')
A['R2-P3-BASE-03-AC02']=dict(
 fixture=dict(tenant='T-A',catalog={'rootId':'CT1','versionId':'CT1-v1','state':'draft','kind':'category','name':'旧名称','code':'C1','parentId':None,'sort':1,'targetKind':None,'targetId':None},certificate={'rootId':'CERT1','versionId':'CERT1-v1','personId':'E1','issuedAt':'2026-08-01T00:00:00Z','validityStatus':'valid'},actors={'H':'catalog.manage, name only','R':'certification.revoke; independent of E1/applicant/material contributors'},now='2026-09-10T01:00:00Z',workspaceRevision=20),
 actions=['r2.m06.catalog.edit','r2.m06.certification.revoke'],actors=['H','R'],allowedFields=['catalog.name (changed field only)','ReasonAction.businessVersionId','ReasonAction.reason'],forbiddenFields=['issuedAt','personId','approvalState','auditActor','certificate history on catalog edit'],
 given='CT1-v1为category草稿，完整CatalogDraft如fixture；H仅能改name，CERT1-v1已合法授E1且有效；独立R具revoke，不是本人/原申请贡献者；初始workspaceRevision=20。',
 when='H以CT1 root和完整payload将name改为新名称，其余字段原样，expectedEntityRevision=1；读成功receipt后R以businessVersionId=CERT1-v1、reason=资格材料失效提交certification.revoke，使用最新revision和新幂等键；再以同键重发撤销。',
 then='改名创建CT1-v2、内容审计和一次applied receipt，不新增certificate或M01任职历史；CERT1-v1授证字节保留。撤销成功时生成独立revocation事件一次，current validity=revoked，revokedAt为服务端提交时刻；同键重发同receipt不多增历史。未授权改issuedAt/personId/actor拒绝；审计失败则相应业务状态无变更。',
 expectedVersions={'catalog':'CT1-v1 retained; new CT1-v2','certificate':'CERT1-v1 retained; one revocation state event','M01assignmentHistory':'no new row'},
 inheritance='继承BASE-03-AC02审计与业务历史按语义分别计数；员工普通字段/任职历史原AC保留，R2改为目录展示字段内容版本与证书撤销历史，不要求两类条数相等。')
A['R2-P3-BASE-04-AC02']=dict(
 fixture=dict(tenant='T-A',reportVersions=[{'rootId':'REP1','versionId':'REP1-v1','state':'published','attachmentBindingId':'B1','objectVersionId':'OBJ-A-v1','digest':'a'*64},{'rootId':'REP1','versionId':'REP1-v2','state':'draft','supersedesVersionId':'REP1-v1','attachmentBindingId':None}],objects=[{'id':'OBJ-A-v1','digest':'a'*64,'bytesFixture':'synthetic old report'},{'id':'OBJ-B-v1','digest':'b'*64,'bytesFixture':'synthetic corrected draft'}],actor='H',grants=['reportDraftManage REP1-v2','attachmentBind REP1-v2','reportRead REP1-v1','attachmentRead OBJ-A-v1 within REP1-v1'],denied=['mutatePublished','publish','rawResponseRead']),
 actions=['shared.attachment.unbind(ownerVersionId=REP1-v1,bindingId=B1)','shared.attachment.replace(ownerVersionId=REP1-v1,bindingId=B1,newObjectVersionId=OBJ-B-v1)','shared.attachment.bind(ownerVersionId=REP1-v2,objectVersionId=OBJ-B-v1,purpose=report_draft)'],actors=['H'],allowedFields=['ownerVersionId (draft only)','objectVersionId','purpose','expectedOwnerRevision','bindingId (draft unbind only)'],forbiddenFields=['overwrite object bytes','published owner binding change','source reviewer identity','set published state'],
 given='REP1-v1已published且B1绑定OBJ-A-v1；REP1-v2是同根独立draft、更正来源指v1。H仅具草稿管理/绑定及旧报告read，OBJ-B-v1不可见准备对象，两对象合成摘要固定。',
 when='通过R1共享附件adapter依次解绑或替换REP1-v1.B1；然后为REP1-v2创建新绑定B2指OBJ-B-v1，再读取旧版B1。',
 then='前两请求409 IMMUTABLE_VERSION，旧binding/digest/对象字节不变；第三请求创建B2并仅使v2草稿关联可见，v1仍读OBJ-A-v1，不能覆盖B1或冒充发布。新附件不继承旧版受众；沿当前grant及v2 owner范围，任何无权下载403。删除草稿绑定先墓碑禁读，物理回收不得破坏旧版或恢复点引用。',
 expectedVersions={'REP1-v1':'immutable and remains published','REP1-v2':'draft with own B2 only','OBJ-A-v1':'unchanged; retained for history/recovery','B1':'unchanged'},
 inheritance='继承BASE-04-AC02已发布附件不可改及新版本独立关联；原course AC保留。R2明确报告v1/v2与B1/B2：默认不复制附件绑定，需要新bind；复用同object字节也须新binding及当前授权，不复制读权限。')
for a in A.values():a['executionStatus']='not_run';a['adaptationReview']='P2_desktop_only_not_business_execution'
(D/'Foundation_Adaptations.json').write_text(json.dumps(dict(kind='P2_concrete_adaptations_source_preserved',adaptations=A),ensure_ascii=False,indent=2)+'\n')
lines=['# 三项基础AC的R2定向适配','','原始AC及basis保留在Requirements_Trace和Acceptance_Scenarios.originalFoundationGwt；下列不构成执行通过。附件动作是R1共享adapter的P2操作名，待A槽位冻结绑定实际接口；不能据此宣称已有运行路由。','']
for id,a in A.items():
 lines+=['## '+id,'',a['inheritance'],'','Given：'+a['given'],'','When：'+a['when'],'','Then：'+a['then'],'','允许字段：'+', '.join(a['allowedFields'])+'。禁止字段：'+', '.join(a['forbiddenFields'])+'。','', '夹具、动作、角色及每个版本预期逐字段见Foundation_Adaptations.json。']
(D/'Foundation_Adaptations.md').write_text('\n'.join(lines)+'\n')
