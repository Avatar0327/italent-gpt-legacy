"""Generate proposed P3 work and GWT cases, never execute them."""
import json,re
from pathlib import Path
D=Path(__file__).resolve().parent
def read(n):return json.loads((D/n).read_text())
def put(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
t=read('Requirements_Trace.json');state=read('Design_Checkpoint.json');done=state['completedModules']
tasks=[];scenarios=[]
for spec in t['specs']:
    m=spec['id'][:3]
    if m not in done:continue
    tasks.append({'id':'P3-R2-'+spec['id'].replace('-SPEC-','-'),'moduleId':m,'requirementRefs':[spec['id']],
                  'title':spec.get('topic',spec['approvedText'][:60]), 'designRefs':spec['designRefs'],
                  'ownerRole':m+'实施负责人；独立测试负责人复核','phase':'P3','status':'proposed_not_started',
                  'dependencies':['R1共同身份/权限/事务/流程契约适配验证'],'deliverables':['规范化对象及API适配','合成正反例与事务/权限证据','兼容/迁移差异报告'],'scenarioIds':[]})
for a in t['acceptanceIds']:
    if a['kind']!='approved_module' or not all(m in done for m in a['moduleIds']):continue
    m=a['id'][:3];src=a['source']; refs=re.findall(r'M\d{2}-SPEC-\d{2}',src.get('basis',''))
    refs=[r for r in refs if r.startswith(m)] or [m+'-SPEC-01']
    task='P3-R2-'+refs[0].replace('-SPEC-','-')
    scenarios.append({'id':'R2-P3-'+a['id'],'requirementRefs':[a['id']]+refs,'moduleId':m,'taskId':task,
      'fixture':m+'_Design.md#acceptance; 隔离合成租户/员工/授权者，保持源案例的数量、时点和角色条件',
      'given':src['given'],'when':src['when'],'then':src['then'],
      'executionSteps':['按Given构造精确根/版本及当前grant，记录初始revision与源digest','以指定角色直接调用模块命令/查询，不靠UI隐藏；施加When条件','读取版本、回执及授权投影，逐条核对Then；失败时核无未授权副作用'],
      'expectedEvidence':['请求/响应schema、版本和权限摘要（脱敏）','业务前后版本及事件/command receipt；拒绝时不变量保持','原验收ID映射和独立复核记录'],
      'executionStatus':'not_run','historicalExecutionIsNotCurrentEvidence':True})
if state.get('foundationsComplete'):
    for b in t['foundations']:
        tasks.append({'id':'P3-R2-'+b['id'],'moduleId':None,'requirementRefs':[b['id']],'title':b['source']['name']+' R2差异验证','designRefs':b['designRefs'],'ownerRole':'共享基础负责人+安全/独立测试负责人','phase':'P3','status':'proposed_not_started','dependencies':['R1对应基础契约已验证'],'deliverables':['R2敏感对象适配及拒绝证据'],'scenarioIds':[]})
    for a in t['acceptanceIds']:
        if a['kind']!='approved_foundation':continue
        src=a['source'];scenarios.append({'id':'R2-P3-'+a['id'],'requirementRefs':[a['id'],a['baseId']],'taskId':'P3-R2-'+a['baseId'],'given':src['given']+'；对象替换为R2标准/答卷/盘点/继任/任期合成记录','when':src['when'],'then':src['then'],'expectedEvidence':['当前授权与恢复安全epoch','接口响应/脱敏审计/对象摘要及拒绝证明'],'executionStatus':'not_run'})
if (D/'Supplemental_Scenarios.json').exists():
    supplement=read('Supplemental_Scenarios.json')
    tasks+=supplement.get('tasks',[])
    scenarios+=supplement.get('scenarios',[])
for task in tasks:task['scenarioIds']=[x['id'] for x in scenarios if x['taskId']==task['id']]
task_by_id={x['id']:x for x in tasks}
def matching(refs):
    return [x['id'] for x in scenarios if x['id'] in refs or set(refs)&(set(x['requirementRefs'])|set(task_by_id[x['taskId']]['requirementRefs']))]
for spec in t['specs']:
    spec['scenarioIds']=matching([spec['id']]);spec['taskIds']=[x['id'] for x in tasks if spec['id'] in x['requirementRefs']]
for clause in t['clauses']:
    parent=next(x for x in t['specs'] if x['id']==clause['parentId']);clause['scenarioIds']=parent['scenarioIds'];clause['coverageNote']='Parent approved policy scenario family; implementation proof still required per clause.'
for detail in t['contractDetails']:
    refs=[a['id'] for a in t['acceptanceIds'] if a.get('contractId')==detail['contractId']]
    detail['scenarioIds']=matching(refs)
    if not detail['scenarioIds']:
        mods=[r[:3] for r in detail['designRefs']];detail['scenarioIds']=[x['id'] for x in scenarios if any(m in x.get('taskId','') for m in mods)]
for closure in t['closures']:closure['scenarioIds']=matching(closure['source'].get('decisionIds',[]))
for foundation in t['foundations']:foundation['scenarioIds']=matching([foundation['id']])
for a in t['acceptanceIds']:a['scenarioIds']=matching([a['id']])
if (D/'Legacy_Acceptance_Map.json').exists():
    old={x['id']:x for x in read('Legacy_Acceptance_Map.json')['acceptance']}
    for a in t['acceptanceIds']:
        if a['id'] in old:
            a['scenarioIds']=matching(old[a['id']]['currentAcceptanceRefs']);a['legacyDisposition']=old[a['id']]['disposition']
            if old[a['id']]['disposition']=='source_request_only':
                a['scenarioIds']=[];a['evidenceRequestIds']=['R2-SOURCE-M17-01']
import runpy
runpy.run_path(str(D/"build_foundation_adaptations.py"))
runpy.run_path(str(D/"build_dependencies.py"))
from repair_handoff import apply
apply(t,tasks,scenarios)
put('Requirements_Trace.json',t)
put('P3_Work_Packages.json',{'kind':'proposal_only_not_execution_or_controller_ledger','count':len(tasks),'tasks':tasks})
put('Acceptance_Scenarios.json',{'kind':'executable_test_design_not_run','count':len(scenarios),'scenarios':scenarios})
lines=['# P3任务与可执行验收建议','',f'任务{len(tasks)}项，场景{len(scenarios)}项；均未开始/未执行。只有所有者批准P2退出及P3准入后才可实施。精确Given/When/Then与证据要求见Acceptance_Scenarios.json。','', '|任务|需求|场景数|责任|','|---|---|---:|---|']
for x in tasks:lines.append('|'+x['id']+'|'+','.join(x['requirementRefs'])+'|'+str(len(x['scenarioIds']))+'|'+x['ownerRole']+'|')
(D/'P3_Handoff.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'tasks':len(tasks),'scenarios':len(scenarios),'tasksWithoutScenarios':[x['id'] for x in tasks if not x['scenarioIds']]},ensure_ascii=False))

with (D/"P3_Handoff.md").open("a") as f:
 f.write("\n46项任务完成依赖、纯领域启动边界和A/B/C待冻结槽位见[Task_Dependencies.md](Task_Dependencies.md)。R1-10与实际R2/R3生产者联合收口，不把全部R1退出设为循环前置。全部138场景仍not_run，P3未启动。\n")

with (D/"P3_Handoff.md").open("a") as f:
 f.write("\n001–004修订待独立复核；LIMIT52责任子项仍15个P2设计关闭提案（原独立接受9+本轮逐项重提6）、25个P3验证、12个P4核证，原6组完整关闭0。005/006观察保留。P2修复不等实现/业务验收通过。\n")
