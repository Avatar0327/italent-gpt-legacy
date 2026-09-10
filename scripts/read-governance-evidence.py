"""Read-only, allowlisted, commit-consistent governance evidence. No build hooks."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'docs/delivery/Scope_Register.json',
    'docs/delivery/Controller_Resume.md',
    'docs/Execution_Checkpoint.md',
    'docs/HRIS_Project_Plan.md',
    'docs/P2_Acceptance.md',
    'docs/delivery/F01_F04_Business_Acceptance.md',
)

def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(ROOT), *args],
                                   stderr=subprocess.PIPE, timeout=30)

def allowed(path):
    p = Path(path)
    return path in REQUIRED or (
        path.startswith('docs/') and p.suffix in {'.md', '.json'} and
        ('acceptance' in path.lower() or 'deploy' in path.lower() or
         (path.startswith('docs/delivery/P1') and '/' not in path[len('docs/delivery/'):]))
    )

def snapshot():
    head = git('rev-parse', '--verify', 'HEAD').decode().strip()
    branch = git('branch', '--show-current').decode().strip()
    if branch != 'main':
        raise ValueError('SOURCE_BRANCH_MISMATCH')
    status = git('status', '--porcelain=v1', '-z')
    paths = git('ls-tree', '-r', '--name-only', head).decode().splitlines()
    selected = sorted(p for p in paths if allowed(p))
    if not set(REQUIRED) <= set(selected):
        raise ValueError('REQUIRED_EVIDENCE_MISSING')
    files = []
    for path in selected:
        raw = git('show', head + ':' + path)
        files.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
                      'bytes': len(raw), 'content': raw.decode('utf-8')})
    if git('rev-parse', 'HEAD').decode().strip() != head or git('status', '--porcelain=v1', '-z') != status:
        raise ValueError('SOURCE_CHANGED_DURING_READ')
    manifest = json.dumps([(f['path'], f['sha256']) for f in files], separators=(',', ':')).encode()
    return {'schemaVersion': 'italent-governance-evidence/1', 'ok': True,
            'observedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source': {'head': head, 'branch': branch, 'workingTreeDirty': bool(status),
                       'contentBasis': 'committed_HEAD_only', 'remoteHead': None,
                       'remoteStatus': 'not_checked_no_repository_credential'},
            'version': head + ':' + hashlib.sha256(manifest).hexdigest(),
            'businessTestsRerun': False, 'deploymentTriggered': False,
            'deploymentApplicability': 'Use dated deployment evidence; HEAD is not a deployed version.',
            'files': files}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        json.dump(snapshot(), sys.stdout, ensure_ascii=False)
        sys.stdout.write('\n')
    except (ValueError, subprocess.SubprocessError, UnicodeError) as exc:
        code = str(exc) if isinstance(exc, ValueError) else 'SOURCE_READ_FAILED'
        json.dump({'schemaVersion': 'italent-governance-evidence/1', 'ok': False,
                   'error': code, 'retainLastSuccessfulSnapshot': True,
                   'currentHeadVerified': False}, sys.stdout)
        sys.stdout.write('\n')
        sys.exit(1)
