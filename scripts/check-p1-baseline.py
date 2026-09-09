import json,pathlib,subprocess,hashlib,datetime,re
R=pathlib.Path(__file__).resolve().parents[1];D=R/'docs/delivery';s=json.loads((D/'Scope_Register.json').read_text());old=json.loads(subprocess.check_output(['git','show','HEAD:docs/delivery/Scope_Register.json'],cwd=R))
checks=[]
approvals={x['id']:x for x in s['p1B'].get('approvalRecords',[])}
def has_approval(ref):return ref in approvals and approvals[ref].get('approved') is True

def check(v,name):
 assert v,name
 checks.append(name)
operation_by_id={x['id']:x for x in s['p1Baseline']['dataValidation']['operations']}
record_ids={x['objectId'] for x in s['p1Baseline']['dataValidation']['records']}
contract_ids={c['id'] for p in s['p1B']['packages'] for c in p['contracts']}
implementation_ids={x['requirement'] for x in s['p1B']['implementationMap']}
for page in s['p1Baseline']['pages']:
 trace=page.get('traceability')
 if not trace:continue
 check(bool(trace['operationIds']) and all(i in operation_by_id and page['id'] in operation_by_id[i]['evidence'] for i in trace['operationIds']),page['id']+'收口操作存在且关联同页证据')
 check(bool(trace['recordIds']) and set(trace['recordIds'])<=record_ids,page['id']+'收口对象存在于原记录表')
 check(bool(trace['contractIds']) and set(trace['contractIds'])<=contract_ids and set(trace['implementationRequirementIds'])<=implementation_ids,page['id']+'收口规格及实现映射有效')
 check(bool(trace['next']) and bool(trace['closedAt']) and bool(trace['kind']),page['id']+'收口时间/性质/下一步明确')
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
  check(a['p1A'] in ['in_progress','not_assessed','complete','restricted_complete'] and a['p1B'] in ['not_ready','not_assessed','ready'],m['id']+'当前P1A/P1B分别登记')
  if a['p1A'] in ['complete','restricted_complete'] or a['p1B']=='ready' or a['review'] in ['signed','restricted_signed']:
   check(bool(a.get('exitEvidence')) and has_approval(a.get('reviewRecord')),m['id']+'达到退出计数须具体证据/评审记录')
check(ds['supportModuleIds']==['M19','M48','M32'] and ds['moduleExecutionOrder'][:4]==['M01','M19','M48','M32'],'R1审批自助报表按明确顺序闭环，依赖补证不另开全量探索')
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
for m in s['modules']:
 if m['id'] not in active:continue
 details=m['p1'].get('internalScopeCoverage',[])
 check([x['originalScopeItem'] for x in details]==m['scope'].split('、'),m['id']+'原登记内部功能逐项完整，不静默删减')
 for item in details:
  check(set(item['contractIds'])<=set(contract_ids) and set(item['evidenceRefs'])<=set(pages),m['id']+'/'+item['originalScopeItem']+'规格及证据引用有效')
  check(bool(item['coverageDepth']) and bool(item['remaining']) and bool(item['next']) and item['complete'] is False and (item['requirementAccepted'] is False or has_approval(item.get('approvalRecord'))),m['id']+'/'+item['originalScopeItem']+'深度限制/下一步齐备且未伪报通过')
  if item['currentMode']=='本次子能力暂缓':check(m['id']=='M11' and item['originalScopeItem']=='AI排班','内部子能力暂缓仅限本次明确AI边界')
  else:check(bool(item['contractIds']),m['id']+'/'+item['originalScopeItem']+'保留功能有规格或受限提纲')
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
for cap in ds['baseCapabilities']:
 check(cap.get('businessAccepted') is False,cap['id']+'基础能力未代签')
 check(bool(cap.get('fieldDetails')) and all((R/x).exists() for x in cap.get('codeRefs',[])),cap['id']+'对象约束及静态证据路径齐备')
 for case in cap.get('acceptanceCases',[]):
  case_ids.append(case['id'])
  check(all(case.get(k) for k in ['given','when','then','basis','status']) and case.get('accepted') is False and case.get('executionThisRun') is False,case['id']+'基础验收条件完整且未假造执行/签署')
check(len(case_ids)==len(set(case_ids)),'细化场景ID唯一，不改变原59任务及完成分母')
check(all(x.get('decision') or x.get('status') for x in s['p1B']['reviewIssues']),'待补证、待决策及已解决事项有独立状态，不将无需即时选择当作批准')
for row in s['p1B']['implementationMap']:
 evidence=row.get('evidence')
 check(isinstance(evidence,(str,list)) and bool(evidence),row['requirement']+'实现证据结构有效')
 if isinstance(evidence,list):
  check(all(isinstance(ref,str) and len(ref.strip())>1 for ref in evidence),row['requirement']+'实现证据保留完整引用，非逐字符列表')
for m in s['modules']:
 for ref in m['p1']['pageRefs']:check(ref in pages and pages[ref]['moduleId']==m['id'],m['id']+'/'+ref+'证据归属')
for p in pages.values():check((R/p['source']).exists(),p['id']+'原始来源存在')
for p in s['p1B']['packages']:check((R/p['spec']).exists(),p['id']+'规格/输入存在')
files=list(D.glob('P1*.md'))+[R/'docs/HRIS_Project_Plan.md',D/'Scope_Register.md',D/'Module_Queue.md',D/'P1_Module_Closure.json',D/'Controller_Resume.md',R/'docs/Execution_Checkpoint.md',D/'F01_F04_Requirements_Baseline.md']
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


policy=s['roadmap']['executionPolicy'];order=s['roadmap']['moduleExecutionOrder']
expected_order=['M01','M19','M48','M32','M37','M06','M26','M18','M17','M03','M27','M16','M12','M11','M07']
check(order==expected_order and ds['moduleExecutionOrder']==order,'用户R1–R3模块顺序精确保持')
check([i for r in ds['rangeLayers'][:3] for i in r['moduleIds']]==order and set(ds['rangeLayers'][3]['moduleIds'])==all_ids-active,'R1–R4完整分区15/33')
check(policy['wipLimit']==1 and policy['backupLimit']==1 and policy['primaryModuleId'] in active,'单主模块与最多1备用')
check(policy['backupModuleId'] is None or policy.get('backupActivationEvidence'),'启用备用必须记录外部阻塞与返回条件')
check(policy['activeExecutionModuleId'] in [policy['primaryModuleId'],policy['backupModuleId']],'实际执行仅主或获准备用')
check(q['currentP1']['executionPolicy']==policy,'队列执行模式与唯一Scope一致')
for m in s['modules']:
 if m['id'] not in active:continue
 c=m['p1']['moduleClosure']
 for phase in ['p1AConclusion','p1BConclusion']:
  check(c[phase]['status'] in policy['statusVocabulary'],m['id']+phase+'结论枚举有效')
  if c[phase]['status'] in ['完整通过','受限通过']:check(has_approval(c[phase]['approvalRecord']),m['id']+phase+'通过须批准记录')
 if any(c[k]['status']=='受限通过' for k in ['p1AConclusion','p1BConclusion']):
  check(all(c.get('restrictedApproval',{}).get(k) for k in ['scope','residualRisk','revalidation','record']),m['id']+'受限批准范围风险补验齐备')
 rows=m['p1'].get('closureChecklist',[])
 if rows:
  check(set(x['scopeItem'] for x in rows)==set(m['scope'].split('、')),m['id']+'收口覆盖每个原范围')
  check(all(set(x['requirementIds'])<=set(contract_ids) and set(x['evidenceRefs'])<=set(pages) for x in rows),m['id']+'收口引用真实契约/证据')
# Persist the additional governance checks into the existing check report.
result['checks']=checks;(D/'P1AB_Document_Check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

review=next(m for m in s['modules'] if m['id']=='M01')['p1']['reviewPackage']
issue_ids={x['id'] for x in s['p1B']['reviewIssues']}
check(set(review['decisionIds'])<=issue_ids,'M01评审决定引用现有唯一待决记录')
check(review['businessAccepted'] is False and review['productionAccepted'] is False,'M01材料不代签业务/生产验收')
for case in review['acceptanceCases']:
 check(all(case.get(k) for k in ['given','when','then','basis','status']) and case['accepted'] is False and case['executionThisRun'] is False,case['id']+'M01候选验收完整且未假造执行')
 check(case['id'] not in case_ids,case['id']+'不重复契约/基础验收ID')
 case_ids.append(case['id'])
view=json.loads((D/'P1_Module_Closure.json').read_text())
check(view['moduleCount']==15 and view['primaryModuleId']==policy['primaryModuleId'] and view['backupModuleId']==policy['backupModuleId'],'机器视图同源范围/焦点')
for x in view['modules']:
 expected=all(v['value'] is True and bool(v['basis']) for v in x['conditions'].values()) and all(x[k]['status'] in ['完整通过','受限通过'] and has_approval(x[k]['approvalRecord']) for k in ['p1AConclusion','p1BConclusion']) and x['transitionReview']['approved'] is True and has_approval(x['transitionReview']['record'])
 check(x['transitionReady']==expected,x['moduleId']+'转序由真实条件和批准推导')
check(view['transitionReadyCount']==sum(x['transitionReady'] for x in view['modules']),'转序计数同源推导')
for ar in approvals.values():
 check(all(ar.get(k) for k in ['approvedBy','approvedAt','scope','source','reviewedHead','reviewedDocumentSha256','exclusions']),ar['id']+'用户批准版本与范围可追溯')
 original=json.loads(subprocess.check_output(['git','show',ar['reviewedHead']+':docs/delivery/Scope_Register.json'],cwd=R))
 original_issues={x['id']:x for x in original['p1B']['reviewIssues']}
 for iid,v in ar['approvedRecommendations'].items():
  check(v['text']==original_issues[iid]['proposal'] and hashlib.sha256(v['text'].encode()).hexdigest()==v['sha256'],iid+'推荐锁定所审版本，不扩写批准')
 expected_doc=subprocess.check_output(['git','show',ar['reviewedHead']+':'+ar['reviewedDocument']],cwd=R)
 check(hashlib.sha256(expected_doc).hexdigest()==ar['reviewedDocumentSha256'],ar['id']+'审阅文档哈希匹配')
check(view['p1ClosedCount']==view['progress']['review']['total'],'P1关闭合计同源且完整/受限分列')
check(all(not x['transitionReady'] for x in view['ranges']),'当前R版本未获整体评审，不自动启动开发')
result['checks']=checks
(D/'P1AB_Document_Check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: authoritative scope, review packet, rolling gates, recovery views, deterministic generation and unchanged product source; no business retest/signoff')
