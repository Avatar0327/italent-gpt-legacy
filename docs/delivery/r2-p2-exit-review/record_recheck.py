"""Record/check independent recheck handoff; writes only designated new review records.

--record materializes reviewed decisions and immutable evidence index.
--check checks saved evidence and worktree scope without writing any file.
Neither mode runs any product, network, migration, or phase operation.
"""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
PREFIX='docs/delivery/r2-p2-exit-review/'
R='bd976480fad9822ee52ecb4b00a080360772b0f3'
C='dc6dd896fbf388b70069ecb756547f85ee89d08a'
P='a7a23d6bff024f4660fd14b0c22f47a6d40d928f'
BRANCH='review/r2-p2-exit-20260910'
R1_OBS='ab28d326a6e5282ffd0f2d7176abac14922f147d'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def load(name):return json.loads((OUT/name).read_text())
def put(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--record',action='store_true')
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
if args.record==args.check:parser.error('Choose exactly one of --record / --check')
checks=[]
def test(name,ok,detail=None):checks.append(dict(check=name,passed=bool(ok),detail=detail))
test('exact review branch',git('branch','--show-current').decode().strip()==BRANCH)
test('original review ancestor retained',subprocess.run(['git','merge-base','--is-ancestor',R,'HEAD'],cwd=ROOT).returncode==0)
test('no merge commits after original review',not git('rev-list','--merges',R+'..HEAD').strip())
test('only review tracked changes',all(p.startswith(PREFIX) for p in git('diff','--name-only',R).decode().splitlines()))
untracked=git('ls-files','--others','--exclude-standard').decode().splitlines()
test('only review untracked records',all(p.startswith(PREFIX) for p in untracked))
test('inherited design tree untouched',not git('diff','--name-only',R,'--','docs/delivery/r2-p2').strip())
history=[]
for path in git('ls-tree','-r','--name-only',R,'--',PREFIX).decode().splitlines():
    if path==PREFIX+'Resume.md':continue
    old=git('show',R+':'+path)
    now=(ROOT/path).read_bytes()
    test('original independent history '+path,now==old)
    history.append(dict(path=path,gitRef=R,sha256=sha(old),bytes=len(old),unchanged=now==old))
oldresume=git('show',R+':'+PREFIX+'Resume.md')
test('Resume only append history', (OUT/'Resume.md').read_bytes().startswith(oldresume))
oldproposal=json.loads(git('show','8b3daf9270181ffe2e77015be723da8e611d83a5:docs/delivery/r2-p2/Controller_Proposal.json'))
for entry in oldproposal['fixedDesignReferences']:
    test('old fixed reference on original content '+entry['path'],entry['gitRef']=='7ff3a28c7660dac658d5243d7c4535a9c8037fc2' and sha(git('show',entry['gitRef']+':'+entry['path']))==entry['sha256'])
f=load('Recheck_Findings.json');one=load('Recheck_Round1.json');two=load('Recheck_Round2.json');gen=load('Recheck_Generation.json')
test('fixed targets all records',all(x['designContentHead']==C and x.get('packagingHead',P)==P for x in [f,one,two,gen]))
test('both independent rounds no failures',one['summary']['failed']==two['summary']['failed']==0 and all(c['passed'] for x in [one,two] for c in x['checks']))
test('exact round summaries',one['summary']['checkCount']==2199 and two['summary']['checkCount']==963)
test('generator clean 75 files',gen['passed'] and gen['filesCompared']==75 and gen['changed']==[])
test('001-004 accepted without severity downgrade',all(next(x for x in f['findings'] if x['id']==f'FINDING-{i:03d}')['status']=='accepted_closed' for i in range(1,5)))
test('counts and owner boundary',f['counts']=={'Blocker':0,'Major':0,'Minor':0,'Observation':2} and not f['ownerExitApprovalGrantedByThisReview'] and not f['p3AuthorizationGrantedByThisReview'] and not f['p3Started'] and not f['minimumP2RepairActions'] and not f['newFindings'])
test('six disputed design-level results',len(one['limits'])==6 and all(x['verificationPassed'] and x['independentDisposition']=='accepted_design_layer' and not x['riskFullyClosed'] for x in one['limits']))
for path in OUT.glob('Recheck_*.json'):
    json.loads(path.read_text())
test('review JSON parse',True)

if args.record:
    limit_document=dict(kind='independent_design_layer_LIMIT_recheck_not_total_risk_closure',designContentHead=C,packagingHead=P,acceptedBefore=9,independentlyAcceptedThisRecheck=6,acceptedP2DesignTotal=15,P3Validation=25,P4Acceptance=12,originalGroupsFullyClosed=0,originalGroupsWithP3Residual=6,originalGroupsWithP4Residual=6,residualGroupCountsOverlap=True,items=one['limits'])
    put('Recheck_Limits.json',limit_document)
    gates=json.loads(git('show',R+':'+PREFIX+'Critical_Gates.json'))['gates']
    changes={
        'M37-01':'Contract_Repair逐级字段/父子根版本和IndicatorChild严格输入补齐；LEVEL系列证据独立接受。',
        'M37-05':'Internal/External严格联合及五域内部冻结引用明确；仅成就外部来源允许。',
        'M06-01':'CatalogDraft类型配置/数值尺度/评级方案成员版本完整，TYPE系列独立接受。',
        'M26-01':'Question逐题角色/维度/指标及可见条件版本绑定明确；QUESTION系列接受。',
        'M26-03':'新旧answerAtom分行、参与/系数等价，不含答卷UUID；16例和三高风险手算通过。',
        'M26-04':'withdraw不清历史，CAS重算和分区/epoch连续；09/10例与正文一致。',
        'M18-01':'PreviousResultRef/null、精确历史发布集、同人及asOf/用途明确；HISTORY系列接受。',
        'H-10':'88定义/76动作；34例9/25及49完整Command探针；Schema与必需服务端语义分工明确。',
        'H-18':'三项Foundation_Adaptations直接规定fixture/动作/角色/字段/版本断言，原AC独立保留。',
        'H-19':'46具体依赖/Schema/adapter/安全/迁移/恢复齐全，55/165/0；P2交接缺口关闭，A/B/C实际开放仍待005。',
        'E-01':'新44固定引用核dc6dd896，包装清单核a7a23d6；旧对象分别自验，无动态清单误比。',
        'E-02':'原需求/条款/字段/关闭项/AC/任务ID及来源不变，001语义缺口独立接受关闭。',
        'E-04':'原9接受加本轮6独立接受，15/25/12互斥，6组P3/P4重叠，原组完整关闭0。',
        'E-07':'本固定设计的Blocker=0、未关闭Major=0，001至004全部独立接受；建议交所有者批准而非代签。'
    }
    records=[]
    for g in gates:
        observation=g['id'] in ['H-16','H-17']
        records.append(dict(id=g['id'],scope=g['scope'],gate=g['gate'],originalStatus=g['status'],originalFindingIds=g['findingIds'],recheckStatus='design_defined_runtime_unproved' if observation else 'accepted_design_recheck',basis=changes.get(g['id'], '原固定内容差异核对：已接受控制未删除/弱化；'+g['assessment']),designRefs=g['designRefs'],scenarioIds=g['scenarioIds'],runtimeExecuted=False))
    put('Recheck_Gates.json',dict(kind='targeted_manual_gate_decisions_plus_regression_not_new_product_execution',designContentHead=C,gateCount=56,gates=records))
    r1=[]
    for name in ['R1_P3_Resume.md','R1_P3_Checkpoint.json']:
        path='docs/delivery/r1-p3/'+name;b=git('show',R1_OBS+':'+path)
        r1.append(dict(gitRef=R1_OBS,path=path,sha256=sha(b),bytes=len(b),use='parallel_state_only_not_R2_completion_evidence'))
    core=['Independent_Recheck.md','Recheck_Findings.json','Recheck_Manual_Review.md','Recheck_P3_Baseline.md','Recheck_Commands.md','Recheck_Round1.json','Recheck_Round2.json','Recheck_Generation.json','Recheck_Input_Hashes.json','Recheck_Limits.json','Recheck_Gates.json','recheck_forward.py','recheck_reverse.py','recheck_generation.py','record_recheck.py']
    evidence=[dict(path=PREFIX+n,sha256=sha((OUT/n).read_bytes()),bytes=(OUT/n).stat().st_size) for n in core]
    input_hashes=load('Recheck_Input_Hashes.json')['inputs']
    packages={}
    for name in ['jsonschema','attrs','referencing','rpds-py','jsonschema-specifications','typing-extensions']:
        try:packages[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:packages[name]='not_in_current_interpreter; see isolated run'
    verification=dict(kind='independent_recheck_handoff_verification_no_circular_self_hash',recordedAt=datetime.now(timezone.utc).isoformat(),designContentHead=C,packagingHead=P,originalReviewHead=R,reviewBranch=BRANCH,reviewWorktree=str(ROOT),reviewHeadBeforeNewContentCommit=git('rev-parse','HEAD').decode().strip(),initialRemoteHeads={'review/r2-p2-exit-20260910':R,'design/r2-p2-20260910':P},initialReviewWorktreeClean=True,originalReviewHistory=history,sourceHashEntryCount=len(input_hashes),fixedReferenceCount=44,sourceManifestEntries=78,reviewSourceEntries=11,independentRounds=[one['summary'],two['summary']],generation={'filesCompared':75,'changed':[]},documentaryOnly=True,productTests=0,businessActions=0,ownerApproval=False,p3Started=False,p4Started=False,subagentsUsed=False,pythonVersion=platform.python_version(),isolatedDependencies=packages,r1ReadOnlyObservedSources=r1,evidenceFiles=evidence,checks=checks,failed=sum(not c['passed'] for c in checks),finalDeliveryNote='Final content/delivery commit and remote consistency supplied by subsequent Git receipt; this file excludes its own SHA and delivery receipt to prevent self-reference.')
    put('Recheck_Verification.json',verification)
else:
    recorded=load('Recheck_Verification.json')
    test('recorded handoff no failures',recorded['failed']==0)
    for entry in recorded['evidenceFiles']:
        b=(ROOT/entry['path']).read_bytes()
        test('saved independent evidence '+entry['path'],sha(b)==entry['sha256'] and len(b)==entry['bytes'])
    for entry in load('Recheck_Input_Hashes.json')['inputs']:
        b=git('show',entry['gitRef']+':'+entry['path'])
        test('saved fixed input '+entry['gitRef']+'/'+entry['path'],sha(b)==entry['sha256'] and len(b)==entry['bytes'])
    test('saved six LIMIT decisions',load('Recheck_Limits.json')['items']==one['limits'])
    test('saved 56 gates',len(load('Recheck_Gates.json')['gates'])==56)
result=dict(mode='record' if args.record else 'check',checks=len(checks),failed=sum(not c['passed'] for c in checks))
print(json.dumps(result))
for check in checks:
    if not check['passed']:print(json.dumps(check,ensure_ascii=False))
raise SystemExit(bool(result['failed']))
