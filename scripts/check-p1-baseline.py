import json,pathlib,subprocess,hashlib,datetime,re
R=pathlib.Path(__file__).resolve().parents[1];D=R/'docs/delivery';s=json.loads((D/'Scope_Register.json').read_text());old=json.loads(subprocess.check_output(['git','show','HEAD:docs/delivery/Scope_Register.json'],cwd=R))
checks=[]
def check(v,name):
 assert v,name
 checks.append(name)
check(len(s['modules'])==48 and len(s['acceptanceTasks'])==59,'48组和59原任务保留')
ds=s['deliveryScope']
expected={'M01','M19','M48','M32','M03','M06','M17','M18','M26','M37','M12','M16','M27','M11','M07'}
active=set(ds['currentModuleIds']); all_ids={m['id'] for m in s['modules']}
check(len(ds['currentModuleIds'])==15 and active==expected,'当前15模块与用户已确认清单完全一致')
check(len(all_ids-active)==33 and active<=all_ids,'原48分为当前15和暂缓33，无删除/重复')
caps={x['id'] for x in ds['baseCapabilities']}
check(caps=={'BASE-01','BASE-02','BASE-03','BASE-04','BASE-05','BASE-06'},'六类非模块基础能力完整且不增加模块分母')
check(all(x['scope'] and x['acceptance'] and x['status'] for x in ds['baseCapabilities']),'基础能力范围/验收预期/状态齐备')
mapped=ds['acceptanceApplicability']
check(len(mapped)==59 and {x['taskId'] for x in mapped}=={a['id'] for a in s['acceptanceTasks']},'原59任务逐条有当前适用映射，不删分母')
for x in mapped:
 a=next(a for a in s['acceptanceTasks'] if a['id']==x['taskId'])
 check(x['originalModuleId']==a['moduleId'] and x['criteriaIds']==[c['id'] for c in a['criteria']],x['taskId']+'保留原任务归属及criteria关联')
 check(set(x['currentModuleIds'])<=active and set(x['baseCapabilityIds'])<=caps and x['status'] in ['保留','部分适用','本次交付暂缓'],x['taskId']+'当前适用范围合法')
for m in s['modules']:
 a=m['p1']['currentDeliveryAssessment']
 check(a['assessmentAt'] and a['basis'],m['id']+'当前判断有时间与依据')
 if m['id'] not in active:
  check(a['p1A']=='deferred' and a['p1B']=='deferred' and '本次交付暂缓' in m['p1']['coverage']['next'],m['id']+'退出当前主动探索/完成条件')
 else:
  check(a['p1A'] in ['in_progress','not_assessed','complete'] and a['p1B'] in ['not_ready','not_assessed','ready'],m['id']+'当前P1A/P1B分别登记')
  if a['p1A']=='complete' or a['p1B']=='ready' or a['review']=='signed':
   check(bool(a.get('exitEvidence')) and bool(a.get('reviewRecord')),m['id']+'达到退出计数须具体证据/评审记录')
check(ds['supportModuleIds']==['M19','M48','M32'] and 'BP-I' not in ds['businessOrder'],'审批自助报表随链同步，不排最后')
q=json.loads((D/'Module_Queue.json').read_text())
check(q['currentP1']['nextTasks']==s['roadmap']['nextTasks'] and q['currentP1']['businessOrder']==ds['businessOrder'],'唯一队列与Scope当前顺序和下一步一致')
for dep in ds['dependencies']:
 check(set(dep['consumerModuleIds'])<=active and set(dep['deferredProviderIds'])<=(all_ids-active),dep['id']+'当前消费者/暂缓提供者精确映射')
check([m['id'] for m in s['modules']]==[m['id'] for m in old['modules']],'原范围ID及顺序保持')
for a,b in zip(s['modules'],old['modules']):
 for k in ['id','name','scope','requirements','developed','tested','productionAccepted']:check(a[k]==b[k],a['id']+' '+k+'保留')
for a,b in zip(s['acceptanceTasks'],old['acceptanceTasks']):
 check(a==b,a['id']+'原验收全文/条件/维度/accepted保持')
ids=[i for p in s['p1B']['packages'] for i in p['moduleIds']]
check(len(ids)==48 and len(set(ids))==48 and set(ids)=={m['id'] for m in s['modules']},'全量业务包映射无重复遗漏')
pages={p['id']:p for p in s['p1Baseline']['pages']}
check(len(pages)==len(s['p1Baseline']['pages']),'页面证据ID无重复')
for m in s['modules']:
 check(isinstance(m['p1']['coverage']['facts'],list) and all(ref in pages or ref.startswith('BC-NAV') for ref in m['p1']['coverage']['facts']),m['id']+'事实引用类型与有效性')
 check(m['businessPackage'] in [p['id'] for p in s['p1B']['packages'] if m['id'] in p['moduleIds']],m['id']+'分包双向一致')
 check(m['p1']['coverage']['accepted'] is False,m['id']+'未代签P1')
contract_ids=[c['id'] for p in s['p1B']['packages'] for c in p.get('contracts',[])]
check(len(contract_ids)==len(set(contract_ids)),'分包需求契约ID唯一')
for p in s['p1B']['packages']:
 check(p['accepted'] is False,p['id']+'未代签需求')
 for c in p.get('contracts',[]):
  check(all((R/x).exists() for x in c['codeRefs']),c['id']+'实现证据路径存在')
  app=c['currentApplicability']
  check(app['status'] in ['保留','部分适用','本次交付暂缓'] and set(app['moduleIds'])<=active and set(app['baseCapabilityIds'])<=caps,c['id']+'历史契约当前适用明确')
case_ids=[]
for pack in s['p1B']['packages']:
 for contract in pack['contracts']:
  for case in contract.get('acceptanceCases',[]):
   case_ids.append(case['id'])
   check(all(case.get(k) for k in ['given','when','then','basis','status']),case['id']+'验收场景条件/动作/预期/来源完整')
   check(case.get('accepted') is False and case.get('executionThisRun') is False,case['id']+'候选场景未代签或假造本轮业务执行')
  if any(contract.get(k) for k in ['fieldDetails','roleMatrix','stateTransitions','acceptanceCases']):
   check(contract['currentApplicability']['status']!='本次交付暂缓',contract['id']+'本轮细化仅当前范围/基础，不扩暂缓独立规格')
check(len(case_ids)==len(set(case_ids)),'细化场景ID唯一，不改变原59任务及完成分母')
for row in s['p1B']['implementationMap']:
 evidence=row.get('evidence')
 check(isinstance(evidence,(str,list)) and bool(evidence),row['requirement']+'实现证据结构有效')
 if isinstance(evidence,list):
  check(all(isinstance(ref,str) and len(ref.strip())>1 for ref in evidence),row['requirement']+'实现证据保留完整引用，非逐字符列表')
for m in s['modules']:
 for ref in m['p1']['pageRefs']:check(ref in pages and pages[ref]['moduleId']==m['id'],m['id']+'/'+ref+'证据归属')
for p in pages.values():check((R/p['source']).exists(),p['id']+'原始来源存在')
for p in s['p1B']['packages']:check((R/p['spec']).exists(),p['id']+'规格/输入存在')
files=list(D.glob('P1*.md'))+[R/'docs/HRIS_Project_Plan.md',D/'Scope_Register.md',D/'Module_Queue.md']
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run(['python','scripts/render-p1-baseline.py'],cwd=R,check=True,capture_output=True)
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
check(before==after,'重复生成一致')
for p in files:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if ':' in target or target.startswith('#'):continue
  check((p.parent/target.split('#')[0]).exists(),p.name+'链接'+target)
changed=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
check(all(p.startswith('docs/') or p in ['scripts/render-p1-baseline.py','scripts/check-p1-baseline.py'] for p in changed),'未改产品源码/测试/依赖/配置')
result={'completedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'scope':'文档完整性/引用/生成一致性；非业务回归、原站取证、需求签署或UAT','result':'passed','checks':checks,'notes':['对当前HEAD核对原48组及59原验收条件/标志未改变','本检查仅验证文档结构；是否新增原站观察以带来源与观察时间的记录为准，不能由脚本推断','D1历史测试源3d690cbbd6336c6de8b76a06fa4459700b1e3a88；入口渲染源fdc423fcba607bd5814a0672836b55536c71ecb1；本轮未复测'],'businessAccepted':False,'productionAccepted':False}
(D/'P1AB_Document_Check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: scope, acceptance flags, package mapping, page attribution, links, deterministic generation and unchanged product source')
