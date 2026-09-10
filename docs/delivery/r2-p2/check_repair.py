"""Reverse trace and repair provenance checks; documents only."""
import json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;old='8b3daf9270181ffe2e77015be723da8e611d83a5'
def read(n):return json.loads((D/n).read_text())
def before(n):return json.loads(subprocess.check_output(['git','show',old+':docs/delivery/r2-p2/'+n]))
checks=[]
def check(ok,label):
 checks.append(dict(check=label,pass_=bool(ok)));assert ok,label
R=read('Repair_Record.json')
for x in R['sources']:
 b=subprocess.check_output(['git','show',x['gitRef']+':'+x['path']]);check(hashlib.sha256(b).hexdigest()==x['sha256'] and len(b)==x['bytes'],'review source '+x['path'])
t=read('Requirements_Trace.json');oldT=before('Requirements_Trace.json')
for group in ['specs','clauses','contractDetails','closures','foundations','acceptanceIds']:
 check([x['id'] for x in t[group]]==[x['id'] for x in oldT[group]],'original IDs '+group)
 for a,b in zip(t[group],oldT[group]):
  for k in ['source','approvedText','approvedProposalSha256']:
   if k in b:check(a[k]==b[k],group+'/'+a['id']+' source '+k)
s=read('Acceptance_Scenarios.json')['scenarios'];oldS={x['id']:x for x in before('Acceptance_Scenarios.json')['scenarios']};check(len(s)==138 and {x['id'] for x in s}==set(oldS),'138 original scenario IDs preserved')
for x in s:
 check(x['executionStatus']=='not_run',x['id']+' not_run')
 if x['id'] not in read('Foundation_Adaptations.json')['adaptations']:
  check(all(x[k]==oldS[x['id']][k] for k in ['given','when','then']),x['id']+' original GWT retained')
for x in t['specs']:
 if x.get('targetedRepairMappings'):
  for p in x['targetedRepairMappings']:
   check(set(p['scenarioIds'])<=set(oldS),'repair scenarios '+x['id'])
   check(p['command'] in {c['action'] for c in read('Command_Registry.json')['commands']},'repair command '+x['id'])
   check(set(p['exampleIds'])<={c['id'] for c in read('Schema_Examples.json')['cases']},'repair examples '+x['id'])
l=read('Limit_Resolution.json');oldL={x['id']:x for x in before('Limit_Resolution.json')['items']}
check(l['itemCount']==52 and l['fullyClosedOriginalGroups']==0,'LIMIT denominator and original closed groups')
check(l['counts']=={'P2_design_closed':15,'P3_validation':25,'P4_acceptance':12},'52 exclusive original phase labels')
check(l['repairAccounting']['independentAcceptedBeforeRepair']==9 and l['repairAccounting']['repairReproposedP2Closed']==6,'9 accepted + 6 proven re-proposals')
for x in l['items']:
 if x['disposition']!='P2_design_closed':check(x==oldL[x['id']],x['id']+' P3/P4 responsibility unchanged')
 if 'repairProof' in x:
  p=x['repairProof'];b=(D/p['evidencePath']).read_bytes();e=json.loads(b)
  check(hashlib.sha256(b).hexdigest()==p['evidenceSha256'],x['id']+' evidence hash')
  check(all(hashlib.sha256((D/n).read_bytes()).hexdigest()==h for n,h in e['inputSha256'].items()),x['id']+' current input evidence')
check(all(R['findings']['R2-EXIT-00'+str(i)]=='open_future_responsibility' for i in [5,6]),'observations 005/006 open')
check(not R['ownerP2ExitApproved'] and not R['r2P3Started'],'no approval or P3')
check(len(read('P3_Work_Packages.json')['tasks'])==46,'46 tasks unchanged')
for task in read('P3_Work_Packages.json')['tasks']:
 dep=next(x for x in read('Task_Dependencies.json')['tasks'] if x['taskId']==task['id']);check(task['dependencies']==dep,task['id']+' exact dependency binding')
changed=subprocess.check_output(['git','diff','--name-only',old]).decode().splitlines();check(all(p.startswith('docs/delivery/r2-p2/') for p in changed),'repair only authorized directory')
out=dict(kind='P2_reverse_trace_not_product_test',count=len(checks),errors=0,checks=checks)
(D/'evidence/repair-reverse-trace.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({'reverseChecks':len(checks),'errors':0})
