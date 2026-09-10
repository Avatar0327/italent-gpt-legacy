#!/usr/bin/env python3
"""Record fresh local evidence against a committed source; never mark a design case complete from test counts."""
import argparse,datetime,hashlib,json,pathlib,subprocess,re
p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--tests',nargs='+',required=True);p.add_argument('--typecheck',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];out=root/'docs/delivery/r1-p3';sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
if subprocess.run(['git','diff','--quiet','HEAD','--','app','lib','db','drizzle','tests','scripts'],cwd=root).returncode:raise SystemExit('Commit source before recording exact-source evidence')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();run='r1-p3-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');r={'runId':run,'sourceSha':sha,'taskId':a.task,'startedAt':now(),'environment':'local node:sqlite real SQL transactions; isolated fixture identities and simulated external adapters; no cloud, production, original-site or real external effects','fixtureVersion':'synthetic R1 tests at sourceSha; fixed scenario values, independently generated opaque UUIDs','fullTaskComplete':False,'independentReview':'pending','inputs':{},'checks':[]}
for f in a.tests+['tests/support/runtime.mjs']:
 path=root/f;r['inputs'][f]=hashlib.sha256(path.read_bytes()).hexdigest()
cmds=[('tests',['node','--test',*a.tests])]
if a.typecheck:cmds.append(('types',['node','node_modules/typescript/bin/tsc','--noEmit','--pretty','false']))
if a.build:cmds.append(('build',['node','/root/.codex/plugins/cache/openai-curated-remote/sites/0.1.56/scripts/build-site.mjs']))
for name,cmd in cmds:
 try:x=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60);code=x.returncode;log=x.stdout
 except subprocess.TimeoutExpired as e:code=124;log=str(e.stdout or '')+'\nTIMEOUT: not passed\n'
 file=out/'evidence'/f'{run}-{name}.log';file.write_text(log);r['checks'].append({'name':name,'command':cmd,'exitCode':code,'log':str(file.relative_to(out)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
 if name=='tests':r['testSummary']={k:int(v) for k,v in re.findall(r'(tests|pass|fail|skipped|cancelled) (\d+)',log)}
 if code:break
if a.build:(root/'lib/delivery/evidence.json').write_bytes(subprocess.check_output(['git','show','HEAD:lib/delivery/evidence.json'],cwd=root))
r['finishedAt']=now();file=out/'evidence'/f'{run}.json';file.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');ref=str(file.relative_to(out))
f=out/'R1_P3_Checkpoint.json';d=json.loads(f.read_text());task=next(t for t in d['tasks'] if t['id']==a.task);task['evidence'].append(ref);task['implementationSha']=sha;d['lastVerifiedSourceSha']=sha;d['latestRun']=ref;f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False));raise SystemExit(any(c['exitCode'] for c in r['checks']))
