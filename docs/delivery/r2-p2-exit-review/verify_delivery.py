"""Verify review artifact consistency and unchanged reviewed worktrees; no product tests."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, os, re, subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
FINAL='8b3daf9270181ffe2e77015be723da8e611d83a5'
ENV={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}
def git(*args,cwd=ROOT):
    return subprocess.check_output(['git',*args],cwd=cwd,env=ENV)
def parse_pairs(pairs):
    result={}
    for k,v in pairs:
        if k in result:raise ValueError('duplicate key '+k)
        result[k]=v
    return result
def load(p):return json.loads(p.read_text(),object_pairs_hook=parse_pairs)
def sha(b):return hashlib.sha256(b).hexdigest()
errors=[]
files=list(OUT.glob('*.json'))
for p in files:load(p)
findings=load(OUT/'Findings.json');actual=Counter(f['severity'] for f in findings['findings'])
if {k:actual[k] for k in findings['counts']}!=findings['counts']:errors.append('severity counts')
gates=load(OUT/'Critical_Gates.json');scenarios={x['id']:x for x in load(ROOT/'docs/delivery/r2-p2/Acceptance_Scenarios.json')['scenarios']}
for x in gates['gates']:
    for s in x['scenarioIds']:
        if s not in scenarios:errors.append('gate scenario '+s)
    for r in x['designRefs']:
        n,_,a=r.partition('#');p=ROOT/'docs/delivery/r2-p2'/n
        if not p.is_file() or (a and 'id="'+a+'"' not in p.read_text()):errors.append('gate ref '+r)
for p in OUT.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if not link.startswith(('http:','https:','sandbox:','#')) and not (p.parent/link.split('#')[0]).is_file():errors.append('markdown link '+str(p)+':'+link)
tasks=load(OUT/'P3_Sequencing_Recommendations.json')['tasks']
graph={t['taskId']:t['recommendedR2CompletionPredecessors'] for t in tasks}
old={t['id'] for t in load(ROOT/'docs/delivery/r2-p2/P3_Work_Packages.json')['tasks']}
if set(graph)!=old:errors.append('task set differs')
visited=set();active=set()
def visit(n):
    if n not in graph:errors.append('unresolved dependency '+n);return
    if n in active:errors.append('cycle '+n);return
    if n in visited:return
    active.add(n)
    for d in graph[n]:visit(d)
    active.remove(n);visited.add(n)
for n in graph:visit(n)
limits=load(OUT/'Limit_Review.json')
if len(limits['items'])!=52 or len(limits['independentlyDisputedP2Items'])!=6:errors.append('LIMIT count')
if len(load(OUT/'Requirement_Review.json')['items'])!=33:errors.append('requirement count')
if any(s['executionStatus']!='not_run' for s in scenarios.values()):errors.append('scenario status')

original=Path('/workspace/sites/italent-hris-r2-p2-20260910')
original_files=git('ls-tree','-r','--name-only',FINAL,'docs/delivery/r2-p2').decode().splitlines()
changed_original=[]
for name in original_files:
    b=git('show',FINAL+':'+name)
    if (original/name).read_bytes()!=b or (ROOT/name).read_bytes()!=b:changed_original.append(name)
if changed_original:errors.append('reviewed files changed')
review_changed=git('diff','--name-only',FINAL).decode().splitlines()
review_untracked=git('ls-files','--others','--exclude-standard').decode().splitlines()
if any(not x.startswith('docs/delivery/r2-p2-exit-review/') for x in review_changed+review_untracked):errors.append('review write boundary')
worktrees=[]
for path in ['/workspace/sites/italent-hris',str(original),'/workspace/sites/italent-hris-r1-p2-20260909','/workspace/sites/italent-hris-r1-p3-20260910',str(ROOT)]:
    w={'path':path,'branch':git('branch','--show-current',cwd=path).decode().strip(),
       'head':git('rev-parse','HEAD',cwd=path).decode().strip(),
       'status':git('status','--porcelain=v1',cwd=path).decode()}
    up=subprocess.run(['git','rev-parse','--abbrev-ref','@{upstream}'],cwd=path,env=ENV,capture_output=True,text=True)
    w['upstream']=up.stdout.strip() if up.returncode==0 else None
    worktrees.append(w)
expected=[('22be3a7e366d6787180d4f593a30f5984c70e03a','main'),(FINAL,'design/r2-p2-20260910'),('e15237281ff19f04f08a354fd9455c518b24ae47','design/r1-p2-20260909')]
for w,(head,branch) in zip(worktrees,expected):
    if w['head']!=head or w['branch']!=branch or w['status']:errors.append('protected worktree state '+w['path'])
if worktrees[-1]['branch']!='review/r2-p2-exit-20260910':errors.append('review branch')
r1=worktrees[3];r1records=[]
for name in ['R1_P3_Resume.md','R1_P3_Checkpoint.json']:
    path='docs/delivery/r1-p3/'+name;b=git('show',r1['head']+':'+path)
    if name.endswith('.json'):json.loads(b,object_pairs_hook=parse_pairs)
    r1records.append({'path':path,'gitRef':r1['head'],'sha256':sha(b),'bytes':len(b)})
    if name.endswith('.md'):r1_resume=b.decode()
result={'kind':'review_delivery_document_checks_not_product_tests','observedAt':datetime.now(timezone.utc).isoformat(),
 'reviewedHead':FINAL,'reviewCommitAtObservation':worktrees[-1]['head'],
 'reviewWorktreeStatusBeforeFinalCommit':worktrees[-1]['status'],
 'reviewedFileCount':len(original_files),'reviewedFileByteChanges':changed_original,
 'reviewChangedPaths':review_changed,'reviewUntrackedPaths':review_untracked,
 'reviewJsonFilesParsed':len(files),'gates':len(gates['gates']),'taskRecommendationNodes':len(visited),'dependencyCycles':0 if not any('cycle' in e for e in errors) else 'see errors',
 'findingCounts':findings['counts'],'errors':errors,'worktrees':worktrees,
 'R1LatestCommittedRecords':r1records,'R1LatestResumeExcerpt':r1_resume[-3300:],
 'note':'时间点快照；R1并行修改保留。最终推送及干净状态在完成提交后另查；本文件不内嵌自身最终提交SHA。'}
(OUT/'Final_Verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'errors':errors,'reviewedFilesUnchanged':len(original_files),'gates':len(gates['gates']),'tasks':len(visited),'r1LatestHead':r1['head'],'r1LatestResumeExcerpt':r1_resume[-700:]},ensure_ascii=False))
if errors:raise SystemExit(1)
