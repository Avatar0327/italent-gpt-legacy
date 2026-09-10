"""Prove byte-identical regeneration, independently of generated count declarations."""
import hashlib,json,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def snapshot():return {p.relative_to(D).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in D.rglob('*') if p.is_file() and 'evidence' not in p.parts and '__pycache__' not in p.parts and p.name!='Artifact_Manifest.json'}
before=snapshot();subprocess.run([sys.executable,str(D/'rebuild_repair.py')],check=True);after=snapshot();changed=[n for n in before.keys()|after.keys() if before.get(n)!=after.get(n)]
out=dict(kind='P2_document_generation_drift_check',filesCompared=len(after),changed=changed,pass_=not changed)
(D/'evidence/repair-generation-drift.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');assert not changed,changed;print(out)
