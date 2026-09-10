"""Produce independent review records from immutable documents, never product code.

The human-readable judgments below are review conclusions, not automated proof.
Only the sibling review directory is written. No original generator is modified.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, os, subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
FINAL = '8b3daf9270181ffe2e77015be723da8e611d83a5'
FIXED = '7ff3a28c7660dac658d5243d7c4535a9c8037fc2'
BASE = '22be3a7e366d6787180d4f593a30f5984c70e03a'
R1 = 'e15237281ff19f04f08a354fd9455c518b24ae47'
R1P3 = '4fd20b23ab6ff7458c506e053520171dab031d45'
ENV = {**os.environ, 'GIT_OPTIONAL_LOCKS':'0', 'GIT_TERMINAL_PROMPT':'0'}

def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, env=ENV)
def data(path, ref=FINAL):
    return git('show', ref+':'+path)
def read(name):
    return json.loads(data('docs/delivery/r2-p2/'+name))
def put(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def md(name, lines):
    (OUT/name).write_text('\n'.join(lines)+'\n')
def sha(value):
    return hashlib.sha256(value).hexdigest()

trace = read('Requirements_Trace.json')
scenarios = read('Acceptance_Scenarios.json')['scenarios']
scenario = {s['id']:s for s in scenarios}
tasks = read('P3_Work_Packages.json')['tasks']
limits = read('Limit_Resolution.json')
findings = json.loads((OUT/'Findings.json').read_text())

# Closed-schema property comparison is a document proof, not an API invocation.
defs=read('Interface_Schemas.json')['$defs']
probe_specs=[
 ('VersionRef',['sourceNamespace','externalId'],'Interfaces.md#schema'),
 ('IndicatorChild',['alias','elementText'],'Requirements_Trace.json:BP-C-REQ-07/fieldDetails/2'),
 ('CatalogDraft',['isCommon','descriptionRows','evaluationMode'],'Requirements_Trace.json:BP-C-REQ-02/fieldDetails/1'),
 ('Question',['roleApplicability','dimension','indicatorVersionRefs'],'M26_Design.md#m26-spec-03'),
 ('ReviewProject',['previousResultRef'],'M18_Design.md#m18-spec-01')]
probes=[]
for name, fields, source in probe_specs:
    s=defs[name]
    probes.append({'schemaPointer':'/$defs/'+name,'requiredSemanticFields':fields,
        'source':source,'allowedProperties':list(s['properties']),
        'additionalProperties':s['additionalProperties'],
        'fieldsNotExpressibleHere':[f for f in fields if f not in s['properties']],
        'conclusion':'需明确字段本体或等价关系；闭合结构不能携带这些属性',
        'findingId':'R2-EXIT-001'})
identities=[{'reviewer':x,'sourceAnswerVersion':'V'+x,'coefficient':'1/3','participates':True} for x in 'ABC']
classes={}
for x in identities:
    key=(x['participates'],x['coefficient'],x['sourceAnswerVersion'])
    classes.setdefault(str(key),[]).append(x['reviewer'])
put('Semantic_Probes.json',{'kind':'document_property_comparison_and_symbolic_walkthrough_not_product_tests',
 'gitRef':FINAL,'schemaSha256':sha(data('docs/delivery/r2-p2/Interface_Schemas.json')),
 'schemaProbes':probes,'M26LiteralInterpretation':{'assumption':'源答案版本指不可变答卷版本ID，完整签名按值相等分组',
 'k':3,'input':identities,'classes':classes,'classSizes':[len(v) for v in classes.values()],
 'literalOutcome':'首报全部小于k，与合法三人发布AC冲突；其他解释需要设计明确',
 'source':'M26_Design.md#m26-spec-02 line 31','findingId':'R2-EXIT-002'}})

# All 33 approved recommendations were semantically read; each judgment is explicit.
judgments={
 'M37':['根/版本/子集明确；逐等级alias/elementText未落实严格输入（001）','目标联合类型、精确权重、缺值及有界规则已定义','独立审核、语义摘要、停用和在途冻结规则可指导实现','用途/敏感子集与read/use/review/publish/export分离','五消费者冻结版本明确；外部引用字段与schema冲突（001）'],
 'M06':['树、目录、编号和发展通道已定义；指标类型字段输入缺口（001）','数值/评级及就绪条件明确；指标类型配置不能由通用catalog输入完整表达（001）','审批/发布和启停分态，在途与旧证不自动撤销','委员会回避/缺评、证据窗口、授证有效期/续证/撤销边界可指导实现','组织/类别/级别权限与消费者当前有效性明确；资格不自动任用'],
 'M26':['稳定邀请/身份桥与角色重叠可追踪；题目适用角色关系需与003对应schema补齐（001）','低样本、组合推断和账本范围有设计；签名版本维度存在关键歧义（002）','四题型/题卷/条件DAG明确；逐题角色和维度映射未在严格输入表达（001）','撤回/重交/更正及授权撤销保留旧版与披露历史','用途投影、撤权和消费者错误状态明确；匿名决定依赖002修正'],
 'M18':['对象/范围快照和保存进度明确；previousResultRef输入缺口（001）','轴映射/阈值等值/缺失不落格规则明确','参会/校准/审核分权，利益回避和重开保留版本','首次发布与更正均独立批准，受众当前重裁','只向M17提供来源或建议，不自动入池/继任/任用；精确历史选择受001影响'],
 'M17':['互斥有效区间、自动规则幂等和新ID重入历史明确','准备度词典、继任任期/复核/资格有效性明确','导师和核验人动态解析，不允许本人唯一指导或最终自核','模板/阶段/任务DAG和取消不等免除、退回及M27证据边界明确','健康指标有独立分母/时间/去重和null，历史需真实快照','池/人员/岗位多范围及敏感投影明确，历史来源未知保持隔离'],
 'M03':['干部/任期/assignment/任免记录独立，含边界日期算法','先独立任免批准再由M01实际人事生效；unknown不补造成功','委员会全应评、弃权/缺评分开；精确等值与否决/资格前置明确','延期/转正/退出/撤回各有独立版本和决定，不自动转正','述职/奖惩/访谈敏感附件与当期权限分离，不改任期事实','生产者消费、跨日资格重核与旧数据隔离明确'],
 'R2-BASELINE-01':['六模块/六基础及E2/D1–D7/恢复目标边界明确；基础场景映射Minor见003']}
requirements=[]
for s in trace['specs']:
    if '-SPEC-' in s['id']:
        m,n=s['id'].split('-SPEC-'); judgment=judgments[m][int(n)-1]
    else:
        m='BASE';judgment=judgments[s['id']][0]
    issues=[]
    if '（001）' in judgment:issues.append('R2-EXIT-001')
    if '（002）' in judgment:issues.append('R2-EXIT-002')
    if 'Minor见003' in judgment:issues.append('R2-EXIT-003')
    requirements.append({'id':s['id'],'approvalRecord':s['approvalRecord'],
      'approvedProposalSha256':s['approvedProposalSha256'],'designRefs':s['designRefs'],
      'p3TaskIds':sorted({scenario[i]['taskId'] for i in s['scenarioIds']}),
      'scenarioIds':s['scenarioIds'],
      'p4ResponsibilityIds':[x['id'] for x in limits['items'] if x['disposition']=='P4_acceptance' and (m=='BASE' or x['parentLimitId'].startswith(m))],
      'assessment':judgment,'findings':issues,
      'evidenceRequirement':'P3记录精确版本/请求/当前权限/副作用及独立复核；P4按LIMIT责任核真实环境；本评审均未执行'})
assert len(requirements)==33
put('Requirement_Review.json',{'kind':'independent_all_approved_spec_review','items':requirements,
 'count':33,'note':'295条款是原文按分号/句号确定拆分；149条契约逐值反查。家族级scenario引用不能证明逐字段断言完整。'})
lines=['# 批准需求逐项独立审查','','全部33项均反查批准原文、设计锚点、P3任务和后续证据责任；下表是设计判断，不是执行通过。', '', '|需求|批准|独立判断|P3任务|P4责任|','|---|---|---|---|---|']
for x in requirements:
    lines.append('|'+ '|'.join([x['id'],x['approvalRecord'],x['assessment'],', '.join(x['p3TaskIds']),', '.join(x['p4ResponsibilityIds'])])+'|')
lines+=['','完整scenario IDs、设计引用及原文SHA见Requirement_Review.json。',
 '78项模块AC、16项基础AC、17项历史AC分别以源ID去重；17项历史AC的旧预期与当前批准预期逐项比较，M17-IDP-RECOVERY-01仅转来源核证，不伪造产品场景。',
 '5项历史父任务及各1项criterion原样保留，不把旧accepted/development/testing状态当本轮证据。',
 '24项内部关闭清单是原Scope的P1受限条目来源，不等于本次独立接受24项P2关闭。',
 '295项拆分条款全部继承父需求的整组场景引用；149项字段/角色/状态也多为模块整组映射。数量和引用完整，但R2-EXIT-001证明其中仍存在未落实的字段关系。',
 '138项场景全部not_run；46项任务全部proposed_not_started。设计状态未提升、没有测试通过数量。']
md('Requirement_Review.md',lines)

limit_rows=[]
for x in limits['items']:
    related=[f['id'] for f in findings['findings'] if x['id'] in f['limitItems']]
    if x['disposition']=='P2_design_closed':
        result='不接受当前设计关闭声明，须留在P2修订' if related else '阶段正确，设计层可接受；不等于原LIMIT整组关闭'
        boundary='实现前模型/安全/事务规则必须确定，不能以未来合成或真实验收替代设计决策'
    elif x['disposition']=='P3_validation':
        result='P3责任分配正确；对应P2缺口修复后才具备实施/验证条件'
        boundary='验证已定义的服务端权限、事务、迁移及隐私约束，不是到P3才决定规则'
    else:
        result='P4责任分配正确，需保持真实来源隔离和未执行'
        boundary='真实旧记录/供应商差异未知仅影响对应迁移或接入；不可逆转换前先核证，不可先迁移后等P4补证' if '核证' in x['title'] else '真实多角色/环境容量/恢复验收不能用管理员操作或本地合成数据替代'
    limit_rows.append({**x,'independentAssessment':result,'phaseBoundary':boundary,'findingIds':related})
put('Limit_Review.json',{'originalGroups':6,'fullyClosedGroups':0,'groupsWithP3':6,'groupsWithP4':6,
 'overlap':True,'counts':dict(Counter(x['disposition'] for x in limit_rows)),
 'independentlyDisputedP2Items':[x['id'] for x in limit_rows if x['findingIds']],
 'items':limit_rows,'note':'不修改原52项计数；15个P2标签中6项当前关闭不被独立评审接受。其余9项仅设计层接受，6组均未完整关闭。'})
lines=['# LIMIT 52项逐项阶段审查','','原始6组完整关闭0；6组均有P3和P4责任，两者重叠，不能相加。52互斥子项=15设计关闭标签+25待P3验证+12待P4核证/验收。',
 '独立复核不改原标签：15项中6项因001/002暂不接受设计关闭；其余9项设计层可接受。','','|子项|标题|原阶段|独立判断|必须保留的边界|','|---|---|---|---|---|']
for x in limit_rows:
    lines.append('|'+ '|'.join([x['id'],x['title'],x['disposition'],x['independentAssessment']+('：'+','.join(x['findingIds']) if x['findingIds'] else ''),x['phaseBoundary']])+'|')
lines+=['','每项原责任人、关闭标准和设计引用完整保留于Limit_Review.json。',
 '关键阶段全查：数据模型和服务端授权在P2确定；并发/CAS/幂等/原子副作用在P2确定；迁移不破坏旧数据的策略在P2确定；匿名隔离/防差分在P2确定；M03→M01实际生效及M06资格有效性重检在P2确定。',
 '25项P3责任是上述规则的实施和隔离证据，不是免除P2设计。12项P4责任没有授权先做不可逆迁移、先泄漏敏感资料或先进行实际任免。']
md('Limit_Review.md',lines)

lines=['# 独立发现清单','','结论：不通过。Blocker 0；Major 2；Minor 2；Observation 2。全部为独立复核结果，未用设计窗口Review_Round1/2替代。']
for f in findings['findings']:
    lines+=['', '## '+f['id']+'｜'+f['severity']+'｜'+f['title'], '', '状态：'+f['status']+'。阻止P2退出：'+str(f['blocksExit'])+'。', '', '位置：']
    for loc in f['locations']:
        lines.append('- '+json.dumps(loc,ensure_ascii=False))
    lines+=['','证据：']+['- '+e for e in f['evidence']]
    lines+=['','影响：'+f['impact']]
    if f.get('qualification'):lines+=['','判断边界：'+f['qualification']]
    lines+=['','修复或后续责任：']+['- '+e for e in f['requiredFix']]
    lines+=['','复核方法：'+f['recheck']]
md('Findings.md',lines)

# Twelve approved text backchecks against original six reviewed packages.
samples=[]
approval={x['id']:x for x in read('Approval_Provenance.json')['records']}
for m in ['M37','M06','M26','M18','M17','M03']:
    selected=[s for s in trace['specs'] if s['id'].startswith(m+'-')]
    for s in [selected[0],selected[-1]]:
        a=approval[s['approvalRecord']];b=data(a['reviewedDocument'],a['reviewedHead'])
        text=s['approvedText']
        samples.append({'module':m,'specId':s['id'],'approvalId':a['id'],
         'reviewedHead':a['reviewedHead'],'reviewedDocument':a['reviewedDocument'],
         'documentSha256':sha(b),'matchesApprovedDocumentSha256':sha(b)==a['reviewedDocumentSha256'],
         'approvedText':text,'approvedTextFoundVerbatim':text in b.decode(),
         'backcheck':'原评审包→批准记录→Scope批准proposal→P2追踪；不是仅对生成器输出自证'})
assert all(x['approvedTextFoundVerbatim'] and x['matchesApprovedDocumentSha256'] for x in samples)
put('Source_Review_Samples.json',{'sampleCount':12,'items':samples})

# Snapshot of a specifically read legal R1 commit; concurrent work is never edited.
rp=Path('/workspace/sites/italent-hris-r1-p3-20260910')
r1_files=[]
for name in ['R1_P3_Resume.md','R1_P3_Checkpoint.json']:
    p='docs/delivery/r1-p3/'+name;b=data(p,R1P3)
    r1_files.append({'path':p,'gitRef':R1P3,'sha256':sha(b),'bytes':len(b)})
put('R1_Baseline_Observation.json',{'recordedAt':datetime.now(timezone.utc).isoformat(),
 'initialObservedHead':'375a412fb2100c670f78c496e3c9e492649e5291',
 'reviewedCommittedHead':R1P3,'currentObservedHead':git('rev-parse','HEAD',cwd=rp).decode().strip(),
 'currentStatus':git('status','--porcelain=v1',cwd=rp).decode(),
 'readObjects':r1_files,'preservedLaterCommits':git('log','--format=%H %s','375a412fb2100c670f78c496e3c9e492649e5291..'+R1P3).decode().splitlines(),
 'interpretation':'01–06本地实施验证完成待独立复核；07部分；08/09/10/11未收口。恢复记录为R1窗口声明，未复跑。',
 'role':'只读基线/排序建议；不得作为R2 P2完成证据'})

proposal=read('Controller_Proposal.json');mechanical=json.loads((OUT/'Mechanical_Verification.json').read_text())
lines=['# 哈希、来源与核验命令记录','','被审最终HEAD：`'+FINAL+'`；固定设计内容HEAD：`'+FIXED+'`。最终HEAD是固定HEAD的直接子提交。',
 '启动main：`'+BASE+'`；R1共享设计：`'+R1+'`。',
 '设计从main到最终HEAD共59个变更文件，全部位于docs/delivery/r2-p2。固定到最终仅9个包装/检查证据文件变化，核心设计正文不变。',
 '', '## 固定引用11项', '', '|路径|验证Git对象|SHA256|','|---|---|---|']
for x in proposal['fixedDesignReferences']:lines.append('|'+x['path']+'|'+x['gitRef']+'|'+x['sha256']+'|')
lines+=['','固定Artifact_Manifest在固定HEAD逐项核；最终包装Artifact_Manifest在最终HEAD逐项核。没有把最终动态清单字节与固定清单哈希混比。',
 '两个清单均排除自身和evidence，未发现循环哈希；Source_Manifest的78个来源引用全部存在，SHA256/字节数一致；7项批准记录与Scope原记录一致，含6模块批准及进入P2批准。',
 '33项批准原文逐项与Scope及批准记录比对；12项（每模块首末SPEC）反查原评审包原文和批准时所读包SHA。',
 '638项独立文档检查无失败；5个生成器在临时副本重建无字节漂移。未发现手改派生数量、重复ID、失效锚点或状态提升。',
 '', '## 已执行的核验类别', '', '|命令/方式|结果与范围|','|---|---|',
 '|git worktree list --porcelain；git status --porcelain=v1；git branch -vv；git rev-parse HEAD|先查真实工作树、归属、分支、HEAD及跟踪；原设计干净，R1在制修改保留|',
 '|git worktree add -b review/r2-p2-exit-20260910 <独立路径> '+FINAL+'|创建本窗口独立工作树；原分支不修改|',
 '|git merge-base --is-ancestor；git rev-parse <final>^；git diff --name-only <base> <final>|父子关系及文档范围核对|',
 '|git show <精确SHA>:<文件>；hashlib.sha256(bytes)|186个Git对象阅读/解析与来源清单验证；详见Read_Hash_Manifest.json|',
 '|python docs/delivery/r2-p2-exit-review/verify_review.py|638项只读文档核验；非产品测试|',
 '|临时目录副本顺序运行build_inventory/build_resolution/build_scenarios/build_schemas/build_handoff.py|5个生成器均成功；输出与最终包无字节漂移；只读Git对象|',
 '|JSON duplicate-key拒绝解析、ID去重、引用及GWT比对|33/295/149/24/78/16/17/5/46/138和52责任子项均独立核算|',
 '|python docs/delivery/r2-p2-exit-review/record_audit.py|闭合schema属性比对、符号分组表、来源反查和独立结论记录|',
 '|git ls-remote <已授权仓库> <design-ref> <review-ref>|首次无凭据读失败；普通Sites仓库凭据读成功，设计远端精确等于最终HEAD，评审远端初始不存在；后续推送见提交记录|',
 '', '未直接运行check_design.py：该脚本会重写被评审清单/证据，且检查设计分支名。独立脚本核其必要不变量并复建纯文档生成源，避免改动被审材料。',
 'JSON Schema做了全部本地引用、required、封闭对象、正则及76个条件动作绑定核对；环境无jsonschema库，未声称通过第三方完整元schema验证。明确的属性缺失反例不依赖该库。',
 '未运行npm、产品单元/业务测试、构建、迁移、部署、浏览器/CDP或真实接口；历史TAP中的116/98/247/123等计数仅来源，均不计本轮执行。',
 '评审产物不嵌入自身最终Git SHA，不制造循环哈希。最终提交和远端一致性由Git提交图及最终答复报告。']
md('Hash_Source_Commands.md',lines)
print(json.dumps({'reviewRecords':'written','schemaDocumentProbes':len(probes),'requirements':len(requirements),'limits':len(limit_rows),'sourceSamples':len(samples),'findings':findings['counts']},ensure_ascii=False))
