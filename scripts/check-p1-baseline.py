import json,pathlib,subprocess,hashlib,datetime,re
R=pathlib.Path(__file__).resolve().parents[1];D=R/'docs/delivery';s=json.loads((D/'Scope_Register.json').read_text());old=json.loads(subprocess.check_output(['git','show','HEAD:docs/delivery/Scope_Register.json'],cwd=R))
checks=[]
def check(v,name):
 assert v,name
 checks.append(name)
check(len(s['modules'])==48 and len(s['acceptanceTasks'])==59,'48组和59原任务保留')
check([m['id'] for m in s['modules']]==[m['id'] for m in old['modules']],'原范围ID及顺序保持')
for a,b in zip(s['modules'],old['modules']):
 for k in ['id','name','scope','developed','productionAccepted']:check(a[k]==b[k],a['id']+' '+k+'保留')
for a,b in zip(s['acceptanceTasks'],old['acceptanceTasks']):
 check(a['id']==b['id'] and a['criteria']==b['criteria'],a['id']+'验收条件和accepted保留')
ids=[i for p in s['p1B']['packages'] for i in p['moduleIds']]
check(len(ids)==48 and len(set(ids))==48 and set(ids)=={m['id'] for m in s['modules']},'全量业务包映射无重复遗漏')
pages={p['id']:p for p in s['p1Baseline']['pages']}
check(len(pages)==len(s['p1Baseline']['pages']),'页面证据ID无重复')
for m in s['modules']:
 check(isinstance(m['p1']['coverage']['facts'],list) and all(ref in pages or ref.startswith('BC-NAV') for ref in m['p1']['coverage']['facts']),m['id']+'事实引用类型与有效性')
 check(m['businessPackage'] in [p['id'] for p in s['p1B']['packages'] if m['id'] in p['moduleIds']],m['id']+'分包双向一致')
 check(m['p1']['coverage']['accepted'] is False,m['id']+'未代签P1')
for p in s['p1B']['packages']:
 check(p['accepted'] is False,p['id']+'未代签需求')
 for c in p.get('contracts',[]):
  check(all((R/x).exists() for x in c['codeRefs']),c['id']+'实现证据路径存在')
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
result={'completedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'scope':'文档完整性/引用/生成一致性；非业务回归、原站取证、需求签署或UAT','result':'passed','checks':checks,'notes':['对当前HEAD核对原48组及59原验收条件/标志未改变','本轮有新增原站只读观察，观察和归档时间分别记录；未执行业务提交','D1历史测试源3d690cbbd6336c6de8b76a06fa4459700b1e3a88；入口渲染源fdc423fcba607bd5814a0672836b55536c71ecb1；本轮未复测'],'businessAccepted':False,'productionAccepted':False}
(D/'P1AB_Document_Check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: scope, acceptance flags, package mapping, page attribution, links, deterministic generation and unchanged product source')
