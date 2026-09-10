"""Run inspected DOCUMENT generators in a disposable fixed-commit archive only.

Independent reviews above do not rely on these generators' claimed pass results.
This script verifies reproducibility; writes only temp docs and Recheck_Generation.json.
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
C='dc6dd896fbf388b70069ecb756547f85ee89d08a'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
temporary=Path(tempfile.mkdtemp(prefix='r2-recheck-generation-',dir='/workspace/scratch/a94fcceed57f'))
archive=git('archive',C,'docs/delivery/r2-p2')
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(temporary,filter='data')
D=temporary/'docs/delivery/r2-p2'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),GIT_WORK_TREE=str(temporary))
def snapshot():
    return {str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in D.rglob('*') if p.is_file() and 'evidence' not in p.parts and p.name!='Artifact_Manifest.json'}
before=snapshot(); runs=[]
for name in ['build_inventory.py','build_scenarios.py','build_schemas.py','check_schema_examples.py','check_anonymity.py','build_resolution.py','build_handoff.py','check_foundation_adaptations.py','check_dependencies.py']:
    result=subprocess.run([sys.executable,str(D/name)],env=env,cwd=temporary,text=True,capture_output=True)
    runs.append(dict(script=name,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    if result.returncode:break
after=snapshot()
changed=[p for p in sorted(before.keys()|after.keys()) if before.get(p)!=after.get(p)]
out=dict(kind='isolated_fixed_object_document_generator_rebuild_not_business_tests',designContentHead=C,temporaryDirectory=str(temporary),filesCompared=len(after),changed=changed,runs=runs,before=before,after=after,passed=not changed and all(r['exitCode']==0 for r in runs))
(OUT/'Recheck_Generation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['runs','before','after']},ensure_ascii=False))
for r in runs:
    if r['exitCode']:print(json.dumps(r,ensure_ascii=False))
raise SystemExit(not out['passed'])
