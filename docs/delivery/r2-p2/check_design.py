"""Documentation gates only. Does not import, test, build or mutate product code."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
D=Path(__file__).resolve().parent; R=D.parents[2]
BASE='22be3a7e366d6787180d4f593a30f5984c70e03a'
ORDER=['M37','M06','M26','M18','M17','M03']
ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True);ap.add_argument('--final',action='store_true');args=ap.parse_args()
errors=[];checks=[]
def check(ok,msg):
    checks.append({'check':msg,'ok':bool(ok)})
    if not ok: errors.append(msg)
def git(*a):return subprocess.check_output(['git',*a],cwd=R).decode().strip()
def read(n):return json.loads((D/n).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
state=read('Design_Checkpoint.json');done=state['completedModules']
check(done==ORDER[:len(done)],'single main module order, no skipped promotion')
check(state.get('activeModule') in [None,ORDER[len(done)] if len(done)<6 else None],'at most next module active')
check(git('branch','--show-current')=='design/r2-p2-20260910','owned design branch')
check(state['startHead']==BASE,'registered startup baseline')
changed=set(git('diff','--name-only',BASE).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines())
check(all(p.startswith('docs/delivery/r2-p2/') for p in changed),'all writes within authorized directory')
for x in read('Source_Manifest.json'):
    data=subprocess.check_output(['git','show',x['gitRef']+':'+x['path']],cwd=R)
    check(digest(data)==x['sha256'] and len(data)==x['bytes'],'source hash '+x['path']+'@'+x['gitRef'][:8])
t=read('Requirements_Trace.json')
check(t['counts']['specs']==33,'33 adopted SPEC/BASELINE requirements retained')
check(t['counts']['approvedModuleAcceptance']==78,'78 approved module acceptance IDs retained')
check(t['counts']['foundationAcceptance']==16,'16 foundation acceptance IDs retained separately')
check(t['counts']['historicalAcceptance']==17,'17 historical acceptance IDs retained separately')
for x in t['specs']:
    check(digest(x['approvedText'].encode())==x['approvedProposalSha256'],'approved recommendation hash '+x['id'])
for a in read('Approval_Provenance.json')['records']:
    if a.get('reviewedDocument') and a.get('reviewedDocumentSha256'):
        data=subprocess.check_output(['git','show',a['reviewedHead']+':'+a['reviewedDocument']],cwd=R)
        check(digest(data)==a['reviewedDocumentSha256'],'owner reviewed document hash '+a['id'])
for group in ['specs','clauses','contractDetails','closures','foundations','acceptanceIds']:
    ids=[x['id'] for x in t[group]];check(len(ids)==len(set(ids)),group+' IDs unique')
    for x in t[group]:
        if x['designStatus']=='complete':
            for ref in x['designRefs']:
                p,_,anchor=ref.partition('#'); f=D/p
                check(f.exists() and (not anchor or f'id="{anchor}"' in f.read_text()),'resolved design reference '+x['id']+' -> '+ref)
        elif args.final: check(False,'unfinished mapping '+x['id'])
for f in D.glob('*.json'):json.loads(f.read_text())
check(True,'all top-level JSON parsed')
if (D/'Acceptance_Scenarios.json').exists():
    scenarios=read('Acceptance_Scenarios.json')['scenarios']; ids=[x['id'] for x in scenarios]
    check(len(ids)==len(set(ids)),'executable scenario IDs unique')
    check(all(x.get('given') and x.get('when') and x.get('then') and x.get('expectedEvidence') and x.get('executionStatus')=='not_run' for x in scenarios),'GWT, evidence and not_run on every scenario')
    if args.final:
        acs={r for x in scenarios for r in x.get('requirementRefs',[])}
        check(all(x['id'] in acs for x in t['acceptanceIds'] if x['kind']!='historical'),'all approved ACs have executable scenarios')
if (D/'Limit_Resolution.json').exists():
    l=read('Limit_Resolution.json');items=l['items'];groups=read('Original_Limits.json')['groups']
    check({x['parentLimitId'] for x in items}=={x['id'] for x in groups},'all six original LIMIT groups decomposed')
    check(len({x['id'] for x in items})==len(items),'LIMIT subitems unique')
    check(all(x['disposition'] in ['P2_design_closed','P3_validation','P4_acceptance'] for x in items),'LIMIT dispositions exclusive')
    check(l['counts']=={k:sum(x['disposition']==k for x in items) for k in ['P2_design_closed','P3_validation','P4_acceptance']},'LIMIT disposition counts computed')
if args.final:
    check(done==ORDER and state.get('foundationsComplete'),'all six modules and foundations design complete')
    check(state['p2ExitApproved'] is False and state['p3Entered'] is False,'no P2 exit approval or P3 entry')
    lm=read('Legacy_Acceptance_Map.json')
    check({x['id'] for x in lm['acceptance']}=={x['id'] for x in t['acceptanceIds'] if x['kind']=='historical'},'all historical ACs individually reconciled')
    check(len(lm['historicalTasks'])==5,'five historical task criteria mapped')
    tasks=read('P3_Work_Packages.json')['tasks']; tids={x['id'] for x in tasks}
    check(len(tids)==len(tasks),'P3 work package IDs unique')
    check(all(x['taskId'] in tids for x in scenarios),'all scenarios have accountable P3 task')
    check(all(x.get('scenarioIds') and set(x['scenarioIds'])<=set(ids) for x in tasks),'each P3 task has actual scenario IDs')
    check(all(x['status']=='proposed_not_started' for x in tasks),'P3 tasks proposed, not started')
# Hash core design inputs; evidence and manifests are excluded to avoid self-referential hashes.
artifacts=[{'path':f.relative_to(R).as_posix(),'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size} for f in sorted(D.rglob('*')) if f.is_file() and 'evidence' not in f.parts and f.name not in ['Artifact_Manifest.json'] and '__pycache__' not in f.parts]
(D/'Artifact_Manifest.json').write_text(json.dumps({'scope':'core design artifacts; excludes this manifest and evidence output to avoid circular hashes','artifacts':artifacts},ensure_ascii=False,indent=2)+'\n')
e=D/'evidence';e.mkdir(exist_ok=True)
result={'unit':args.unit,'type':'documentation_only','productTestsRun':False,'atHeadBeforeCommit':git('rev-parse','HEAD'),'sourceHead':BASE,'artifactManifestSha256':digest((D/'Artifact_Manifest.json').read_bytes()),'checks':checks,'checkCount':len(checks),'errorCount':len(errors),'errors':errors,'result':'pass' if not errors else 'fail'}
(e/(args.unit+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['unit','checkCount','errorCount','errors','result']},ensure_ascii=False))
raise SystemExit(bool(errors))
