"""Rebuild documentation-only indexes from immutable Git inputs. No product execution."""
import hashlib, json, re, subprocess
from pathlib import Path
D=Path(__file__).resolve().parent
R=D.parents[2]
BASE='22be3a7e366d6787180d4f593a30f5984c70e03a'
ORDER=['M37','M06','M26','M18','M17','M03']
def git_bytes(ref,path):
    return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=R)
def put(name,value):
    (D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(b): return hashlib.sha256(b).hexdigest()
s=json.loads(git_bytes(BASE,'docs/delivery/Scope_Register.json'))
mods={m['id']:m for m in s['modules'] if m['id'] in ORDER}
state=json.loads((D/'Design_Checkpoint.json').read_text())
done=state['completedModules']
issues=[i for i in s['p1B']['reviewIssues'] if i['id'].split('-SPEC-')[0] in ORDER or i['id']=='R2-BASELINE-01']
contracts=[c for p in s['p1B']['packages'] for c in p['contracts'] if set(c.get('currentApplicability',{}).get('moduleIds',[]))&set(ORDER)]
specs=[]; clauses=[]
for i in issues:
    approval=next(a for a in s['p1B']['approvalRecords'] if a['id']==i['approvalRecord'])
    approved=approval.get('approvedRecommendations',{}).get(i['id'],{})
    mid=next((m for m in ORDER if i['id'].startswith(m)),None)
    target=f'{mid}_Design.md#{i["id"].lower()}' if mid else 'Foundations.md#r2-baseline-01'
    rec={'id':i['id'],'sourcePointer':'/p1B/reviewIssues/'+str(s['p1B']['reviewIssues'].index(i)),
         'approvedText':i['proposal'],'approvedProposalSha256':i.get('approvedProposalSha256') or approved.get('sha256'),
         'approvalRecord':i.get('approvalRecord'),'designRefs':[target],
         'designStatus':'complete' if mid in done or (not mid and state.get('foundationsComplete')) else 'pending'}
    specs.append(rec)
    for n,txt in enumerate(x for x in re.split('[；。]',i['proposal']) if x.strip()):
        clauses.append({'id':i['id']+f'-CLAUSE-{n+1:02d}','parentId':i['id'],'text':txt,
                        'designRefs':[target],'designStatus':rec['designStatus']})
details=[]; cases={}; legacy=[]
for c in contracts:
    mids=[m for m in ORDER if m in c['currentApplicability']['moduleIds']]
    for k in ['fields','roles','lifecycle','actions','fieldDetails','roleMatrix','stateTransitions']:
        value=c.get(k)
        if not value: continue
        for n,v in enumerate(value if isinstance(value,list) else [value]):
            # Original contract wording can predate approval; retain rather than silently repair.
            details.append({'id':f'{c["id"]}/{k}/{n}','contractId':c['id'],'source':v,
                            'designRefs':[f'{m}_Design.md#engineering' for m in mids],
                            'designStatus':'complete' if all(m in done for m in mids) else 'pending',
                            'precedence':'Current approved SPEC overrides incompatible historical expectations; see Legacy_Acceptance_Map.json.'})
    for a in c.get('acceptanceCases',[]):
        cases[a['id']]={'id':a['id'],'contractId':c['id'],'moduleIds':mids,'source':a,
                        'kind':'approved_module' if a['id'] in sum([mods[m]['p1']['reviewPackage']['acceptanceCaseRefs'] for m in ORDER],[]) else 'historical',
                        'designRefs':[f'{m}_Design.md#acceptance' for m in mids],
                        'designStatus':'complete' if all(m in done for m in mids) else 'pending'}
closures=[]
for m in ORDER:
    for c in mods[m]['p1']['closureChecklist']:
        closures.append({'id':c['id'],'source':c,'designRefs':[f'{m}_Design.md#engineering'],'designStatus':'complete' if m in done else 'pending'})
bases=[]
for b in s['deliveryScope']['baseCapabilities']:
    bases.append({'id':b['id'],'source':{k:b[k] for k in ['name','scope','fieldDetails','r2Assessment'] if k in b},
                  'designRefs':['Foundations.md#'+b['id'].lower()],'designStatus':'complete' if state.get('foundationsComplete') else 'pending'})
    for a in b.get('acceptanceCases',[]):
        cases[a['id']]={'id':a['id'],'baseId':b['id'],'source':a,'kind':'approved_foundation',
                        'designRefs':['Foundations.md#'+b['id'].lower()],'designStatus':'complete' if state.get('foundationsComplete') else 'pending'}
hist_ids=['C01','C02','C-LIFECYCLE-REVIEW','P1-C-RULES','C-INTERVIEW-REGISTER']
hist=[t for t in s['acceptanceTasks'] if t.get('id') in hist_ids]
put('Requirements_Trace.json',{'kind':'derived_design_mapping_not_scope_ledger','sourceGitRef':BASE,'sourceSha256':sha(git_bytes(BASE,'docs/delivery/Scope_Register.json')),
    'specs':specs,'clauses':clauses,'contractDetails':details,'closures':closures,'foundations':bases,'acceptanceIds':list(cases.values()),'historicalTasks':hist,
    'counts':{'specs':len(specs),'clauses':len(clauses),'contractDetails':len(details),'closures':len(closures),'approvedModuleAcceptance':sum(x['kind']=='approved_module' for x in cases.values()),'historicalAcceptance':sum(x['kind']=='historical' for x in cases.values()),'foundationAcceptance':sum(x['kind']=='approved_foundation' for x in cases.values()),'historicalTasks':len(hist)}})
limits=[{**l,'moduleId':m} for m in ORDER for l in mods[m]['p1']['reviewPackage']['exceptionProposals']]
put('Original_Limits.json',{'kind':'immutable_source_extract_not_closure','sourceGitRef':BASE,'groups':limits})
relevant_approvals={x['approvalRecord'] for x in specs}|{l['approvalRecord'] for l in limits}|{'R2-P1-P2-TRANSITION-20260910'}
approvals=[a for a in s['p1B']['approvalRecords'] if a['id'] in relevant_approvals]
put('Approval_Provenance.json',{'sourceGitRef':BASE,'records':approvals})
manifest=json.loads((D/'Source_Manifest.json').read_text())
paths={x['path'] for x in manifest if x['gitRef']==BASE}
paths.update(['scripts/render-p1-baseline.py','scripts/check-p1-baseline.py','docs/delivery/P1_Module_Closure.json'])
for c in contracts: paths.update(c.get('codeRefs',[])); paths.update(c.get('reviewPacketRefs',[]))
for m in mods.values():
    paths.update(m['p1'].get('navigationEvidence',[]) if isinstance(m['p1'].get('navigationEvidence'),list) else [])
# Only valid source paths; evidence IDs/objects stay in the source evidence index below.
for p in sorted(x for x in paths if isinstance(x,str) and '/' in x):
    try: data=git_bytes(BASE,p)
    except subprocess.CalledProcessError: continue
    old=next((x for x in manifest if x['gitRef']==BASE and x['path']==p),None)
    if old is None: manifest.append({'gitRef':BASE,'path':p,'sha256':sha(data),'bytes':len(data),'readMode':'complete bytes; source/structured review','historicalOnly':'Acceptance' in p or 'Rehearsal' in p})
put('Source_Manifest.json',sorted(manifest,key=lambda x:(x['gitRef'],x['path'])))
evidence=[]
for m in ORDER:
    refs=set(mods[m]['p1'].get('pageRefs',[]))
    for page in s['p1Baseline']['pages']:
        if page.get('id') in refs or page.get('moduleId')==m:
            evidence.append({'moduleId':m,'sourcePage':page,'use':'historical input only; executionThisRun=false'})
put('Historical_Evidence_Index.json',{'sourceGitRef':BASE,'pages':evidence,'implementationMap':[x for x in s['p1B']['implementationMap'] if set(x.get('moduleIds',[]))&set(ORDER)],'executionThisRun':False})
rows=['# 需求—设计—验收追踪','',f'固定源HEAD `{BASE}`；本表为设计索引，精确逐句/字段/角色/状态及原验收ID在`Requirements_Trace.json`。所有用例本轮未执行。','', '|批准需求|设计定位|设计材料状态|','|---|---|---|']
for x in specs: rows.append('|'+x['id']+'|'+f'[{x["designRefs"][0]}]({x["designRefs"][0]})'+'|'+x['designStatus']+'|')
rows+=['','原LIMIT组保持6个；分解处置另见Limit_Resolution.json，不能将子项数替代原组分母。']
(D/'Traceability.md').write_text('\n'.join(rows)+'\n')
print(json.dumps({'inventoryCounts':json.loads((D/'Requirements_Trace.json').read_text())['counts'],'sources':len(manifest)},ensure_ascii=False))
