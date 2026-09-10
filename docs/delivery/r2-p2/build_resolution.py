"""Author-derived LIMIT responsibility, legacy reconciliation and supplemental GWT indexes."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
def read(n):return json.loads((D/n).read_text())
def put(n,x):(D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
order=['M37','M06','M26','M18','M17','M03']
units={
'M37':{
'P2_design_closed':[('根/子集/尺度及独立审批模型','m37-spec-01'),('旧五级消费者、冻结/停用和迁移策略','m37-spec-05')],
'P3_validation':[('并发版本、权重/缺值/规则组合','01'),('多角色及敏感子集的服务端授权','04'),('停用在途、迁移冲突及五域实际消费','05')],
'P4_acceptance':[('源共享UUID、深子集及真实测评来源核证','source'),('真实跨角色/跨模块、生产权限和恢复验收','runtime')]},
'M06':{
'P2_design_closed':[('类别/层级/评级/标准矩阵及回避模型','m06-spec-01'),('证书有效性、续期、停用与legacy迁移契约','m06-spec-04')],
'P3_validation':[('评分/评级与证据版本/时效','02'),('委员会阈值、回避与强制否决','04'),('目录编号并发、重复续证及授证事务故障','04'),('发展通道/地图与资格消费者实际适配','05')],
'P4_acceptance':[('来源目录/地图关联及真实旧证映射核证','source'),('完整业务多角色、跨域敏感权限及恢复验收','runtime')]},
'M26':{
'P2_design_closed':[('身份桥接/题卷/邀请/答卷不可变模型','m26-spec-01'),('阈值、差分和报告用途/授权设计','m26-spec-02'),('撤回更正、敏感历史隔离及恢复策略','m26-spec-04')],
'P3_validation':[('2/3样本、零样本及跨报告差分','02'),('四题型/套卷版本与角色重叠','03'),('撤回重交、更正发布竞争及审计故障','04'),('原卷/桥接/下载撤权与消费者失败状态','05')],
'P4_acceptance':[('源匿名/题卷深行为及旧数据映射核证','source'),('实际独立角色、隐私用途/容量/恢复验收','runtime')]},
'M18':{
'P2_design_closed':[('项目/会议/结果/九宫格与独立发布模型','m18-spec-01'),('历史版本、来源与M17建议/迁移契约','m18-spec-05')],
'P3_validation':[('九格等值/缺失、范围变更和版本漂移','02'),('会议回避、驳回撤回及更正唯一性','03'),('首次发布、关闭重开和发布并发','04'),('来源/人才池/继任不同数据集及幂等消费','05')],
'P4_acceptance':[('源工具/对象子ID/标准共享映射核证','source'),('实际校准会、多角色敏感访问/容量/恢复验收','runtime')]},
'M17':{
'P2_design_closed':[('池规则、成员区间、准备度与继任任期','m17-spec-01'),('IDP流程/模板/阶段/动态职责与核验','m17-spec-04'),('健康分母、历史映射与敏感消费边界','m17-spec-05')],
'P3_validation':[('自动入出池幂等、unknown和重入历史','01'),('目标映射、任期/到期/离职及资格有效性','02'),('指导自审、角色替换和当前授权','03'),('IDP依赖阻塞、取消/免除、退回和任务核验','04'),('健康分母/历史快照、审计失败和消费适配','05')],
'P4_acceptance':[('原IDP节点UUID、成员原单及目标目录核证','source'),('实际多角色/名单用途及容量/恢复验收','runtime')]},
'M03':{
'P2_design_closed':[('干部/任期/任用与M01生效映射','m03-spec-01'),('委员会精确评分、回避与资格前置','m03-spec-03'),('考察/述职/敏感档案及legacy迁移','m03-spec-05')],
'P3_validation':[('月末/闰年/覆盖日期及任期区间','01'),('委员会等值、缺评/弃权及精确分数','03'),('资格过期、调动失败/unknown、任用幂等','02'),('考察退回/撤回/延期/退出与年度述职','04'),('档案下载撤权、审计故障及legacy映射','06')],
'P4_acceptance':[('真实旧任用来源/类型/时间及源深规则核证','source'),('实际任免多角色、档案用途和生产恢复验收','runtime')]}}
items=[]
for m in order:
    n=0
    for phase,arr in units[m].items():
        for title,loc in arr:
            n+=1;ref=m+'_Design.md#'+(loc if phase=='P2_design_closed' else 'engineering')
            items.append({'id':f'{m}-LIMIT-01.{n:02d}','parentLimitId':m+'-LIMIT-01','title':title,'disposition':phase,
                          'designRefs':[ref],'evidenceStatus':'design_checked' if phase=='P2_design_closed' else 'not_executed',
                          'p2Blocking':False,'ownerRole':'R2 P2设计负责人' if phase=='P2_design_closed' else (m+'实施负责人+独立测试负责人' if phase=='P3_validation' else ('总控指定来源核证负责人/数据HR' if loc=='source' else '业务HR/委员会+安全+运维')),
                          'closureCriterion':'设计模型及批准需求/原验收映射通过文档检查；不表示原站事实已验证' if phase=='P2_design_closed' else ('隔离合成用例及实际适配版本、拒绝/事务证据经独立复核' if phase=='P3_validation' else ('仅对依赖真实来源迁移/接入的对象核证；无来源则隔离，不要求供应商行为覆盖本项目批准规则' if loc=='source' else '获授权环境真实多角色/用途与60分钟RPO、240分钟RTO、30天保留证据')),
                          'recommended':'按既有批准的独立产品规则实施；保留未知和局部隔离','alternative':'依赖缺失对象保持只读/未配置，继续其他范围；不得补造来源或降低控制'})
counts={p:sum(x['disposition']==p for x in items) for p in units['M37']}
put('Limit_Resolution.json',{'kind':'design_disposition_proposal_not_scope_update','originalGroupCount':6,'fullyClosedOriginalGroups':0,'originalGroupsWithP3Residual':6,'originalGroupsWithP4Residual':6,'residualGroupCountsOverlap':True,'counts':counts,'itemCount':len(items),'items':items,
    'sourcePrecedenceNote':'M06-LIMIT-01原文含“M37新模型未获需求批准”，是批准前历史残句；M37-P1-APPROVAL-R2-20260909及本次transition已批准，不作为当前待决。源文字未修改。'})
lines=['# LIMIT消解与P3/P4责任矩阵','',f'原始LIMIT为6组，完整关闭0组；6组均仍有P3和P4责任（两个6相互重叠，不能相加为12组）。拆成{len(items)}个互斥责任子项：P2设计关闭{counts["P2_design_closed"]}，转P3验证{counts["P3_validation"]}，转P4核证/验收{counts["P4_acceptance"]}。P2设计关闭不是源操作已验证。','', '|原LIMIT|P2设计关闭|P3验证|P4核证/验收|','|---|---:|---:|---:|']
for m in order:lines.append('|'+m+'-LIMIT-01|'+'|'.join(str(len(v)) for v in units[m].values())+'|')
lines+=['','逐项事实、设计引用、关闭条件和责任见Limit_Resolution.json；原文保持在Original_Limits.json。六基础运行风险单列，不额外增加原LIMIT分母。','', '原站差异并非要求产品复制所有未知行为；已批准独立规则优先。只有真实迁移/接入依赖某个未知来源ID或语义时，该对象保持隔离并核证。生产能力/隐私/恢复未验不能据设计闭环放行。']
(D/'Limit_Resolution.md').write_text('\n'.join(lines)+'\n')
requests=[]
facts={
'M37':('BC-C32～40已有最小合成链和跨入口引用；共享对象UUID/深子集/原算法未知','标准/指标/子集的真实稳定标识和版本响应；使用中改版/停用的状态及明确来源，不新建真实评测','迁移依赖这些UUID的记录；已批准本项目目录/算法设计不阻'),
'M06':('目录和标准样本已观察；深评级/委员会/证据窗口及地图实际关联未实证','类别/level/rating scheme真实ID；已知旧证期限语义与发展通道地图引用，不发新证','真实旧资格映射与M27来源可用性；新合成规则可继续'),
'M26':('当前单账号只读/历史样本；原匿名完整算法、撤回/更正及多角色未验','已有题卷/角色/邀请/报告版本与授权说明，低样本是否泄计数；仅形成只读取件任务，不索取真人答卷','旧报告迁移与用途核证；新匿名设计按已批政策继续'),
'M18':('项目/标准工具入口与样本可引用；子对象ID、校准深链和共享UUID未知','已有项目/工具/标准引用schema、结果版本与会议状态，只复用既有合成对象','依赖原工具的迁移和适配对象；本项目九格/校准设计不阻'),
'M17':('BC-C30合成成员及阶段已存；R2-RO-M17-01已确认IDP流程入口/停用状态，不能再写未发现；节点UUID/重入史未知','复用既有pool+person复合定位，核membership根/重入链、flow节点版本/目标目录ID；不重复新建计划或派通知','真实IDP/成员/目标映射；本项目新ID与流程设计可继续'),
'M03':('任期/考察/访谈样本与静态防错可引用；多评委任免/转正深链未验','既有合成任用/任期/StaffID的明确映射、实际人事生效来源及原日期规则版本；不提交任命审批','真实历史迁移/凭证核对；新独立任免设计可继续')}
for m,(fact,want,impact) in facts.items():
    requests.append({'id':'R2-SOURCE-'+m+'-01','moduleId':m,'fact':fact,'sourceRefs':[m+'-LIMIT-01','Historical_Evidence_Index.json'],
      'requestedEvidence':want,'impact':impact,'recommended':'由总控在其已授权原站窗口定向只读补证；记录对象ID/版本/时点/可见角色及摘要，取不到明确unknown',
      'alternative':'不依赖未知原站映射；受影响真实导入行quarantine，其余按已批准独立设计继续','blocksP2':False,'ownerPhase':'P4真实来源核证（必要时总控可提前只读取证）','ownerRole':'总控指定来源核证负责人','status':'request_only_not_sent_or_executed','forbidden':['本窗口CDP/浏览器','新建业务对象/任用/通知','新增访问者','真实答卷或员工资料进入设计文档']})
requests.append({'id':'R2-CAPABILITY-01','moduleId':None,'fact':'固定R1设计列明官方export/import、15分钟调度、独立安全账本/密钥尚需实证；本窗口工具仅发现DB概览/行读取，无备份/恢复专用接口，未调用业务数据读取','requestedEvidence':'获授权隔离环境的官方API可用性、调度准时、完整事务日志/对象manifest、当前deny独立性和容量耗时/费用摘要','impact':'BASE-05及六域生产开放，不阻已完成的方案/成本/责任设计','recommended':'P3共享平台能力验证；P4真实恢复/费用核算；维持A方案和60/240/30门槛','alternative':'A无法满足后量化B受控官方执行器或C预热副本价差，交所有者决定；不自行降标','blocksP2':False,'ownerPhase':'P3能力验证 / P4生产验收','ownerRole':'共享平台/安全/运维负责人','status':'request_only_not_sent_or_executed'})
put('Source_Requests.json',{'requests':requests,'count':len(requests),'newOwnerBusinessDecisionsRequired':0})
# Each historical acceptance ID is reconciled individually, without changing its source text/status.
legacy_rules=[
('BP-C-REQ-03-AC01','M26','retain','M26-REVIEW-AC06','冻结v1保留，补独立题卷版本及真实改版链'),
('BP-C-REQ-03-AC02','M26','retain_strengthen','M26-REVIEW-AC01','项目根跨角色唯一；语义拒绝保留，422/400统一错误码不当业务通过'),
('BP-C-REQ-03-AC03','M26','retain_strengthen','R2-M26-S05','scheduled/open不代当前窗口；服务端时钟边界，P3用隔离时钟'),
('BP-C-REQ-03-AC04','M26','superseded_expectation',['M26-REVIEW-AC02','M26-REVIEW-AC03','M26-REVIEW-AC04'],'低样本精确responses=2和HR默认原卷权禁止；k=3及同尺度合法均值保留'),
('BP-C-REQ-03-AC05','M26','refine_identity','M26-REVIEW-AC08','保留responseRootId，答案新version不可覆盖；close后拒绝'),
('BP-C-REQ-03-AC06','M26','superseded_expectation','M26-REVIEW-AC05','零合法非self组不能正式发布，旧可发布仅历史实现事实'),
('BP-C-REQ-03-AC07','M26','refine_idempotency','M26-REVIEW-AC09','同键同payload回原结果，异键重复发布拒绝；授权更正新版本且防差分'),
('BP-C-REQ-03-AC08','M26','retain_strengthen','R2-M26-S06','本人也须显式report audience，禁止默认所有本人published可读；原卷拒绝保留'),
('BP-C-REQ-04-BC30-1','M17','retain','M17-REVIEW-AC01','保留同池同人和字段回读证据；new membership ID由本项目明确设计，原站未知不冒证'),
('BP-C-REQ-04-BC30-2','M17','retain','M17-REVIEW-AC06','阶段/准备度独立；unknown查询同ID不能重复入池'),
('BP-C-REQ-04-BC30-3','M17','superseded_expectation','M17-REVIEW-AC07','原站同EA可存仅事实；本项目禁本人唯一指导与最终自核'),
('BP-C-REQ-04-BC30-4','M17','retain','M17-REVIEW-AC13','阶段不产生继任/资格/IDP完成，源目标未配仅阻该依赖'),
('M17-HISTORY-01','M17','approved_rule_now_explicit','M17-REVIEW-AC01','本项目新ID+previousMembershipId已批；原站真实重入模式仍请求核证'),
('M17-SCOPE-01','M17','approved_rule_now_explicit','R2-M17-S05','当前人员+池/岗位双范围及敏感字段已批，原未批准措辞为历史'),
('M17-REPORT-01','M17','retain_strengthen','M17-REVIEW-AC05','current有效性/复核/资格定义优先，active不等有效；保留历史记录'),
('M17-IDP-RECOVERY-01','M17','source_request_only',[],'原站IDP入口已确认；未核节点UUID仅转R2-SOURCE-M17-01定向来源请求，不伪作P3业务用例'),
('M17-IDP-STATE-01','M17','refine_state_model','M17-REVIEW-AC09','计划/阶段/任务各自状态和核验；取消非自动免除，M27核验不代IDP完成')]
trace=read('Requirements_Trace.json');old={a['id']:a for a in trace['acceptanceIds'] if a['kind']=='historical'}
legacy=[]
for id,m,disp,ac,note in legacy_rules:
    legacy.append({'id':id,'originalSource':old[id]['source'],'disposition':disp,'currentDesignRefs':[m+'_Design.md#engineering'],'currentAcceptanceRefs':ac if isinstance(ac,list) else [ac],'reason':note,'executionThisRun':False,'phaseResponsibility':'总控来源核证（非本窗口原站执行）' if disp=='source_request_only' else 'P3独立验证/P4业务验收'})
task_map={'C01':('Cross_Module_Contracts.md#ownership',['R2-X-01']),'C02':('Permissions.md#matrix',['R2-X-07']),'C-LIFECYCLE-REVIEW':('M03_Design.md#m03-spec-04',['R2-P3-M03-REVIEW-AC09']),'P1-C-RULES':('M03_Design.md#m03-spec-02',['R2-P3-M03-REVIEW-AC01','R2-P3-M03-REVIEW-AC05']),'C-INTERVIEW-REGISTER':('M03_Design.md#m03-spec-05',['R2-P3-M03-REVIEW-AC11','R2-M03-S04'])}
hist=[]
for task in trace['historicalTasks']:
    ref,acs=task_map[task['id']];hist.append({'id':task['id'],'criteriaIds':[x['id'] for x in task['criteria']],'originalSource':task,'designRefs':[ref],'scenarioRefs':acs,'treatment':'保留原59任务ID/状态，不计本轮复验；当前P1批准优先，映射仅供后续验收','executionThisRun':False})
put('Legacy_Acceptance_Map.json',{'acceptance':legacy,'historicalTasks':hist,'historicalAcceptanceCount':len(legacy),'historicalTaskCount':len(hist)})
print(json.dumps({'limitItems':len(items),'dispositions':counts,'sourceRequests':len(requests),'legacyAcceptance':len(legacy),'historicalTasks':len(hist)},ensure_ascii=False))
