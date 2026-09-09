#!/usr/bin/env python3
"""Read-only checks of R1 P2 documents. --render updates derived design trace only.
Never imports product code, executes product tests, opens databases or calls services.
"""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs/delivery/r1-p2'
p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--complete',action='store_true');a=p.parse_args()
def read(n):return json.loads((OUT/n).read_text())
idx=read('R1_P2_Design_Index.json');source=read('R1_P2_Source_Manifest.json');errors=[]
def need(ok,msg):
 if not ok:errors.append(msg)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
need(git('branch','--show-current')==idx['branch'],'wrong design branch')
need(not idx['p2ExitApproved'] and not idx['p3Started'],'unauthorized phase elevation')
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
print(json.dumps({'kind':'P2_document_check_not_business_test','baseline':idx['baseline'],'tasks':len(nums),'designCases':len(caseids),'requirementDesignLinks':len(rows),'sourceFiles':len(source['files']),'errors':errors,'passed':not errors},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
