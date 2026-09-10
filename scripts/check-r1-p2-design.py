#!/usr/bin/env python3
"""Read-only checks of R1 P2 documents. --render updates derived design trace only.
Never imports product code, executes product tests, opens databases or calls services.
"""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs/delivery/r1-p2'
p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--complete',action='store_true');p.add_argument('--review-ready',action='store_true');a=p.parse_args()
def read(n):return json.loads((OUT/n).read_text())
idx=read('R1_P2_Design_Index.json');source=read('R1_P2_Source_Manifest.json');errors=[]
def need(ok,msg):
 if not ok:errors.append(msg)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def digest(data):return hashlib.sha256(data).hexdigest()
need(git('branch','--show-current')==idx['branch'],'wrong design branch')
need(not idx['p3Started'],'P3 must remain unstarted in this design delivery')
approval=None
if idx['p2ExitApproved']:
 # This is a record of the owner's explicit message, not a self-approval path.
 reviewed='65cfcf85e4fccf8cba53319deb7b87dd7f79600a'
 review_path='docs/delivery/r1-p2/R1_P2_Exit_Review.md'
 review_sha='e88a0fdbe89efbca2b497b225df54cebb0a114509564b509d3de4cbbfb7c4d07'
 record='R1_P2_Owner_Exit_Approval.json'
 need((OUT/record).exists(),'owner approval record missing')
 if (OUT/record).exists():
  approval=read(record)
  need(approval['approvalId']=='R1-P2-EXIT-OWNER-20260910','unexpected approval identity')
  need(approval['source']['description']=='项目所有者通过本次消息批准','approval source misrepresented')
  need(approval['reviewed']['head']==reviewed and approval['reviewed']['exitReviewPath']==review_path and approval['reviewed']['exitReviewSha256']==review_sha,'owner approval applied to different reviewed content')
  need(digest(blob(reviewed,review_path))==review_sha,'reviewed exit document digest differs')
  need(git('merge-base',reviewed,'HEAD')==reviewed,'reviewed commit not ancestor')
  pre=approval['precondition']
  need(pre['head']==reviewed and pre['cleanWorkingTree'] and pre['result']['passed'] and not pre['result']['errors'],'original conditional approval check not satisfied')
  need(pre['result']['kind']=='P2_document_check_not_business_test' and approval['source']['command']=='python scripts/check-r1-p2-design.py --complete --review-ready','wrong approval precondition')
  need(pre['checkerSha256']==digest(blob(reviewed,'scripts/check-r1-p2-design.py')),'precondition checker not the reviewed version')
  need(approval['p2ExitApproved'] and approval['p3HandoffReady'] and not approval['p3Started'] and not approval['p3ExecutionAuthorizedByThisRecord'],'approval phase boundary changed')
  need(all(v==0 for v in approval['executionCounts'].values()),'design checks counted as runtime execution')
  old_idx=json.loads(blob(reviewed,'docs/delivery/r1-p2/R1_P2_Design_Index.json'))
  old_idx.update(p2ExitApproved=True,ownerExitApprovalRecord=record)
  need(idx==old_idx,'unreviewed design index/case changes')
  old_manifest_bytes=blob(reviewed,'docs/delivery/r1-p2/R1_P2_Artifact_Manifest.json')
  need(digest(old_manifest_bytes)==approval['reviewed']['artifactManifestSha256'],'reviewed bundle identity differs')
  administrative={'R1_P2_Exit_Review.md','R1_P2_Checkpoint.md','R1_P2_Git_Record.md','R1_P2_Design_Index.json','R1_P2_Limit_Resolution.json','R1_P2_Limit_Resolution.md','R1_P2_Controller_Proposal.json','R1_P2_P3_Work_Packages.md','R1_P2_Dependencies_Decisions.md','check-r1-p2-design.py'}
  protected=[f for f in json.loads(old_manifest_bytes)['files'] if Path(f['path']).name not in administrative]
  need(approval['unchangedReviewedArtifacts']==protected,'approval protection inventory changed')
  for f in protected:
   need(digest((ROOT/f['path']).read_bytes())==f['sha256'],'unreviewed substantive change '+f['path'])
else:
 need('ownerExitApprovalRecord' not in idx,'approval record and index disagree')
need(git('merge-base',idx['baseline'],'HEAD')==idx['baseline'],'design not based on recorded snapshot')
for f in source['files']:
 need((ROOT/f['path']).exists(),'missing source '+f['path'])
 need(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'],'source changed '+f['path'])
changed=set(git('diff','--name-only',idx['baseline']).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines())
for f in changed:need(f.startswith('docs/delivery/r1-p2/') or f=='scripts/check-r1-p2-design.py','out of scope write '+f)
nums=[t['number'] for t in idx['tasks']]
need(nums==list(range(1,len(nums)+1)),'task sequence has gaps')
if a.complete:need(nums==list(range(1,10)),'all nine designs required')
caseids=[];rows=[]
for t in idx['tasks']:
 doc=OUT/t['document'];need(doc.exists(),'missing design '+t['document'])
 for heading in ['批准依据与版本','当前实现与复用判定','正常与失败场景及P3建议','本阶段执行边界']:need('## '+heading in doc.read_text(),'missing section '+t['id']+heading)
 for e in t['evidence']:need(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256'],'implementation evidence changed '+e['path'])
 for c in t['cases']:
  caseids.append(c['id']);need(c['execution']=='not_executed','case falsely executed '+c['id'])
  for k in ['given','when','then','evidence','owner','gate']:need(bool(c[k]),'incomplete case '+c['id']+k)
 for req in t['requirements']:
  cs=[c['id'] for c in t['cases'] if req in c['requirements']]
  need(bool(cs),'no validation case '+req+' in '+t['id'])
  rows.append((req,t['document'],t['id'],','.join(cs)))
need(len(caseids)==len(set(caseids)),'duplicate case ID')
if a.render:
 text='# 需求—设计—P3/P4验收追踪\n\n本表由设计索引生成，只记录本分支设计覆盖，不改变P1批准/项目阶段。用例全部未执行；P4/评审用例不冒称P3运行。\n\n|批准需求|设计文档|任务|验收设计|\n|---|---|---|---|\n'
 for r,d,t,c in rows:text+=f'|{r}|[{d}]({d})|{t}|{c}|\n'
 (OUT/'R1_P2_Traceability.md').write_text(text)
for doc in OUT.glob('*.md'):
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
  if re.match(r'\w+://',target) or target.startswith('#'):continue
  path=target.split('#')[0];need((doc.parent/path).exists(),f'broken link {doc.name}: {target}')
metrics={}
if a.complete:
 coverage=read('R1_P2_Requirement_Coverage.json')
 requirements={r for t in idx['tasks'] for r in t['requirements']}
 need(set(coverage['requiredIds'])<=requirements,'approved requirement missing from design')
 handoff=(ROOT/'docs/delivery/P1_R1_P2_Handoff.md').read_text()
 bp=set(re.findall(r'BP-[A-Z]-REQ-\d+',handoff))
 need({r['id'] for r in coverage['contracts']}==bp,'handoff BP coverage differs')
 need(bp<=set(coverage['requiredIds']),'BP missing required inventory')
 scope=json.loads((ROOT/'docs/delivery/Scope_Register.json').read_text())
 expected_ac={c['id'] for p in scope['p1B']['packages'] for r in p.get('contracts',[]) if r['id'] in bp for c in r.get('acceptanceCases',[])}
 for m in ['M01','M19','M48','M32']:
  expected_ac.update(re.findall(m+r'-REVIEW-AC\d+', (ROOT/f'docs/delivery/P1_{m}_Review_Package.md').read_text()))
 expected_ac.update(re.findall(r'BASE-\d+-AC\d+', (ROOT/'docs/delivery/P1_R1_Foundation_Review.md').read_text()))
 atr=read('R1_P2_Approved_Acceptance_Trace.json')['records']
 need({r['id'] for r in atr}==expected_ac,'original acceptance IDs lost or invented')
 case_by_id={c['id']:c for t in idx['tasks'] for c in t['cases']}
 for r in atr:
  for k in ['given','when','originalThen','targetExpected','owner','gate']:need(bool(r[k]),'acceptance missing '+r['id']+k)
  need(r['execution']=='not_executed','source case falsely run '+r['id'])
  need(bool(r['plannedCases']) and set(r['plannedCases'])<=set(caseids),'source case unmapped '+r['id'])
  for d in r['designDocuments']:need((OUT/d).exists(),'source case doc missing '+d)
  need(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'acceptance source hash '+r['id'])
 risks=read('R1_P2_Limit_Resolution.json')['risks'];riskids=[r['riskId'] for r in risks]
 need(len(set(riskids))==len(risks),'duplicate LIMIT risk')
 counts={}
 dependencies=read('R1_P2_Dependencies_Decisions.json');depids={d['id'] for d in dependencies['dependencies']}
 for r in risks:
  need(r['module'] in ['M01','M19','M48','M32'] and r['originalLimit']==r['module']+'-LIMIT-01','risk outside R1')
  for k in ['originalItem','risk','severity','evidence','p2Handling','p3Synthetic','p4Acceptance','owner','latestGate','status','designDocuments']:need(bool(r[k]),'incomplete risk '+r['riskId']+k)
  need(r['primaryDisposition'] in ['P2','P3','P4'],'invalid disposition')
  counts.setdefault(r['module'],{'P2':0,'P3':0,'P4':0})[r['primaryDisposition']]+=1
  for k in ['p3Synthetic','p4Acceptance']:
   need(r[k]['execution']=='not_executed','risk validation falsely run')
   need(bool(r[k]['caseIds']) and set(r[k]['caseIds'])<=set(caseids),'risk case missing '+r['riskId'])
  for d in r['designDocuments']:need((OUT/d).exists(),'risk document missing '+d)
  need(not r['sourceEvidenceNeeded'] or r['sourceEvidenceRequest'] in depids,'risk missing targeted evidence')
 need(set(counts)=={'M01','M19','M48','M32'},'four LIMITs not covered')
 if approval:
  original_risks=json.loads(blob(reviewed,'docs/delivery/r1-p2/R1_P2_Limit_Resolution.json'))
  for r in original_risks['risks']:
   if r['primaryDisposition']=='P2':r.update(status='owner_design_review_closed',closureApprovalId=approval['approvalId'],closureRecord=record)
  need(read('R1_P2_Limit_Resolution.json')==original_risks,'LIMIT semantics/cases changed beyond owner design closure')
  for key,phase,count in [('ownerClosedDesignRiskIds','P2',9),('remainingP3RiskIds','P3',20),('remainingP4RiskIds','P4',8)]:
   expected=[r['riskId'] for r in risks if r['primaryDisposition']==phase]
   need(approval['riskDisposition'][key]==expected and len(expected)==count,'owner risk disposition differs '+phase)
  need(approval['sourceEvidenceRequests']==[d['id'] for d in dependencies['dependencies'] if d['id'].startswith('SRC-')] and len(approval['sourceEvidenceRequests'])==13,'source evidence responsibility changed')
 datasets=read('R1_P2_Report_Datasets.json')['datasets'];dids={d['datasetId'] for d in datasets}
 src=(ROOT/'lib/hris/reports.ts').read_text()
 expected_ds=set(re.findall(r"'([^']+)'",re.search(r'dataset:z.enum\(\[([^\]]+)',src)[1]))
 need(dids==expected_ds and len(datasets)==21,'dataset catalog changed')
 fs=read('R1_P2_Report_Field_Dictionary.json')['fields'];fids=[f['fieldId'] for f in fs]
 need(len(set(fids))==len(fs),'duplicate report fieldId')
 need({f['datasetId'] for f in fs}==dids,'dataset missing field dictionary')
 for f in fs:
  for k in ['label','type','unit','nullPolicy','sourceField','accessPolicy','exportRule']:need(bool(f[k]),'incomplete field '+f['fieldId']+k)
  need(f['type'] in ['text','enum','date','timestamp','integer','decimal','money_cents','opaque_id','boolean'],'invalid field type')
  need(hashlib.sha256((ROOT/f['sourcePath']).read_bytes()).hexdigest()==f['sourceSha256'],'field source changed')
 work=read('R1_P2_P3_Work_Packages.json');taskids=[t['id'] for t in work['tasks']];owned=[]
 for t in work['tasks']:
  need(t['status']=='proposed_not_authorized' and t['execution']=='not_executed','P3 elevated')
  need(set(t['dependsOn'])<=set(taskids[:taskids.index(t['id'])]),'P3 dependency cycle/order error')
  need(set(t['caseIds'])<=set(caseids),'P3 unknown case')
  need(set(t['approvedAcceptanceSubcases'])<=expected_ac,'P3 unknown approved subcase')
  owned.extend(t['caseIds'])
 need({c for t in work['tasks'] for c in t['approvedAcceptanceSubcases']}==expected_ac,'original acceptance subcases lack P3 task responsibility')
 need(set(owned)=={c for c in caseids if c.startswith('P3-')} and len(owned)==len(set(owned)),'P3 cases need one primary implementation owner')
 links=read('R1_P2_Producer_Integration_Cases.json')['cases']
 need(len(links)==22 and len({c['id'] for c in links})==22,'producer integration coverage')
 need({c['id'] for c in links}==set(next(t for t in work['tasks'] if t['id']=='P3-R1-10')['integrationCaseIds']),'unassigned producer integration scenario')
 for c in links:
  for k in ['given','when','then','evidence','owner','gate']:need(bool(c[k]),'incomplete integration '+c['id'])
  need(c['execution']=='not_executed','integration falsely run')
 for f in fs:
  if f['datasetId']=='workforce':need('employee.' in f['sourceField'],'workforce positional field mapping')
 gates=read('R1_P2_Hard_Gates.json')['gates'];need(len(gates)==15,'hard gate count')
 for g in gates:need((OUT/g['document']).exists() and set(g['caseIds'])<=set(caseids),'hard gate broken '+g['id'])
 proposal=read('R1_P2_Controller_Proposal.json');need(proposal['status']=='proposed_not_applied','proposal falsely applied')
 if approval:
  payload=proposal['operations'][0]['payload']
  need(payload['approvalId']==approval['approvalId'] and payload['approvalSource']==approval['source']['description'] and payload['approvalState']=='owner_approved_with_followup_responsibilities','controller proposal lost owner decision')
  need(payload['implementationState']=='not_started' and not payload['p3Started'] and payload['businessTestsRun']==0 and payload['historicalTestRevalidations']==0,'controller proposal elevated execution')
  handoff=(OUT/'R1_P2_P3_Handoff.md').read_text()
  for t in work['tasks']:
   need(f"|{t['id']}|{t['title']}|{', '.join(t['dependsOn']) if t['dependsOn'] else 'P2批准已满足；另由所有者启动P3窗口'}|" in handoff,'handoff dependency changed '+t['id'])
  for r in risks:
   if r['primaryDisposition'] in ['P3','P4']:need(handoff.count('|'+r['riskId']+'|')==1,'handoff residual missing/duplicated '+r['riskId'])
  for doc in ['R1_P2_P3_Handoff.md','R1_P2_P3_Start_Prompt.md']:
   body=(OUT/doc).read_text()
   for phrase in ['P3尚未开始','项目所有者通过本次消息批准','85','254','P3-R1-01']:
    need(phrase in body,'handoff boundary/inventory missing '+doc+':'+phrase)
 need(not dependencies['newBusinessDecisions'],'new business decision requires owner review')
 metrics={'uniqueRequirements':len(coverage['requiredIds']),'originalAcceptanceScenarios':len(atr),'limitRisks':len(risks),'limitDispositionCounts':counts,'datasets':len(datasets),'reportFields':len(fs),'p3Tasks':len(taskids),'p3Cases':len(owned),'hardGates':len(gates),'producerIntegrationScenarios':len(links)}
 if approval:
  for key,value in metrics.items():need(value==approval['precondition']['result'][key],'approved inventory drift '+key)
if a.review_ready:
 need(a.complete,'review-ready requires complete')
 reviews=read('R1_P2_Self_Review_Results.json')
 need([r['round'] for r in reviews['rounds']]==[1,2],'two reviews required')
 need(all(r['passed'] and not r['remainingDesignDefects'] for r in reviews['rounds']),'review has unresolved design defects')
 expected_state='状态：R1 P2设计阶段通过，带明确后续验证和验收责任' if approval else '状态：具备提交独立评审条件'
 need(expected_state in (OUT/'R1_P2_Exit_Review.md').read_text(),'review pack state inconsistent')
 if approval:
  closure=read('R1_P2_Closure_Verification.json')
  need(closure['kind']=='P2_closure_document_verification_not_runtime_tests','closure check kind changed')
  need([r['round'] for r in closure['rounds']]==[1,2],'two closure document checks required')
  need(all(r['result']['passed'] and not r['result']['errors'] and not r['remainingDesignDefects'] for r in closure['rounds']),'closure defects remain')
  need(closure['businessTestsRun']==0 and closure['historicalTestRevalidations']==0,'closure checks miscounted as business tests')
  bundle=read('R1_P2_Artifact_Manifest.json')
  expected_files={str(f.relative_to(ROOT)) for f in OUT.iterdir() if f.is_file() and f.name!='R1_P2_Artifact_Manifest.json'}|{'scripts/check-r1-p2-design.py'}
  need({f['path'] for f in bundle['files']}==expected_files and len(bundle['files'])==len(expected_files),'closure bundle inventory incomplete')
  for f in bundle['files']:
   data=(ROOT/f['path']).read_bytes()
   need(digest(data)==f['sha256'] and len(data)==f['bytes'],'closure artifact digest differs '+f['path'])
print(json.dumps({'kind':'P2_document_check_not_business_test','baseline':idx['baseline'],'tasks':len(nums),'designCases':len(caseids),'requirementDesignLinks':len(rows),'sourceFiles':len(source['files']),**metrics,'errors':errors,'passed':not errors},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
