"""Independent read-only R2 P2 document audit. No product imports or execution.

Only writes evidence below this review directory. Generator reproduction runs on
temporary copies, uses immutable git show, and never changes reviewed documents.
"""
from pathlib import Path
import collections, hashlib, json, os, re, subprocess, sys, tempfile
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DESIGN = ROOT / 'docs/delivery/r2-p2'
BASE = '22be3a7e366d6787180d4f593a30f5984c70e03a'
FIXED = '7ff3a28c7660dac658d5243d7c4535a9c8037fc2'
FINAL = '8b3daf9270181ffe2e77015be723da8e611d83a5'
R1 = 'e15237281ff19f04f08a354fd9455c518b24ae47'
MODS = ['M37', 'M06', 'M26', 'M18', 'M17', 'M03']
ENV = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0', 'PYTHONDONTWRITEBYTECODE': '1'}
checks = []
reads = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=ENV)

def blob(ref, path):
    data = git('show', f'{ref}:{path}')
    reads[(ref, path)] = {'gitRef': ref, 'path': path, 'sha256': sha(data), 'bytes': len(data)}
    return data

def obj(ref, path):
    return json.loads(blob(ref, path), object_pairs_hook=unique_pairs)

def unique_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('Duplicate JSON key: ' + k)
        d[k] = v
    return d

def read(name):
    return obj(FINAL, 'docs/delivery/r2-p2/' + name)

def check(id, ok, detail=None):
    checks.append({'id': id, 'ok': bool(ok), 'detail': detail})

def put(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def duplicate_ids(rows, key='id'):
    return [k for k, n in collections.Counter(x[key] for x in rows).items() if n > 1]

def anchor(ref):
    p, _, a = ref.partition('#')
    f = DESIGN / p
    return f.is_file() and (not a or f'id="{a}"' in f.read_text())

def snapshot_worktrees():
    result = []
    for block in git('worktree', 'list', '--porcelain').decode().strip().split('\n\n'):
        fields = dict(line.split(' ', 1) for line in block.splitlines() if ' ' in line)
        cwd = fields['worktree']
        status = subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=cwd, env=ENV).decode()
        fields['status'] = status
        result.append(fields)
    return result

start = datetime.now(timezone.utc).isoformat()
check('final-is-direct-child-of-fixed', git('rev-parse', FINAL+'^').decode().strip() == FIXED)
check('base-is-ancestor', subprocess.run(['git','merge-base','--is-ancestor',BASE,FINAL],cwd=ROOT,env=ENV).returncode == 0)
changed = git('diff', '--name-only', BASE, FINAL).decode().splitlines()
check('design-change-boundary', all(p.startswith('docs/delivery/r2-p2/') for p in changed), changed)
packaging = git('diff', '--name-only', FIXED, FINAL).decode().splitlines()
body = ['Architecture.md','Cross_Module_Contracts.md','Permissions.md','Interfaces.md','Interface_Schemas.json','Migration_Rollback.md','Recovery_Cost_Responsibilities.md','Foundations.md','Requirements_Trace.json','Acceptance_Scenarios.json','P3_Work_Packages.json'] + [m+'_Design.md' for m in MODS]
check('fixed-design-body-unchanged', all(blob(FIXED,'docs/delivery/r2-p2/'+n) == blob(FINAL,'docs/delivery/r2-p2/'+n) for n in body), packaging)

# Parse all JSON with duplicate-key rejection and hash every reviewed package file.
files = git('ls-tree','-r','--name-only',FINAL,'docs/delivery/r2-p2').decode().splitlines()
for path in files:
    data = blob(FINAL,path)
    if path.endswith('.json'):
        json.loads(data, object_pairs_hook=unique_pairs)
check('all-package-json-parses-without-duplicate-keys', True, len(files))
proposal = read('Controller_Proposal.json')
for x in proposal['fixedDesignReferences']:
    check('proposal-fixed-hash:'+x['path'], x['gitRef'] == FIXED and sha(blob(x['gitRef'],x['path'])) == x['sha256'])
for ref in [FIXED, FINAL]:
    manifest = obj(ref, 'docs/delivery/r2-p2/Artifact_Manifest.json')
    check('artifact-paths-unique:'+ref, not duplicate_ids(manifest['artifacts'],'path'))
    for x in manifest['artifacts']:
        data = blob(ref,x['path'])
        check('artifact-hash:'+ref+':'+x['path'], sha(data) == x['sha256'] and len(data) == x['bytes'])
    check('artifact-no-self-or-evidence:'+ref, all('/evidence/' not in x['path'] and not x['path'].endswith('/Artifact_Manifest.json') for x in manifest['artifacts']))
sources = read('Source_Manifest.json')
check('source-ref-paths-unique',len({(x['gitRef'],x['path']) for x in sources}) == len(sources))
for x in sources:
    data = blob(x['gitRef'],x['path'])
    check('source-hash:'+x['gitRef']+':'+x['path'],sha(data) == x['sha256'] and len(data) == x['bytes'])

scope = obj(BASE,'docs/delivery/Scope_Register.json')
trace = read('Requirements_Trace.json')
ap = read('Approval_Provenance.json')['records']
ap_source = {x['id']:x for x in scope['p1B']['approvalRecords']}
for a in ap:
    check('approval-exact-source:'+a['id'],a == ap_source[a['id']])
    if a.get('reviewedDocument') and a.get('reviewedDocumentSha256'):
        check('approval-reviewed-hash:'+a['id'],sha(blob(a['reviewedHead'],a['reviewedDocument'])) == a['reviewedDocumentSha256'])
check('trace-scope-digest',trace['sourceSha256'] == sha(blob(BASE,'docs/delivery/Scope_Register.json')))
source_specs = [x for x in scope['p1B']['reviewIssues'] if x['id'].split('-SPEC-')[0] in MODS or x['id'] == 'R2-BASELINE-01']
check('approved-spec-set', {x['id'] for x in source_specs} == {x['id'] for x in trace['specs']})
source_clauses = []
for spec in trace['specs']:
    src = next(x for x in source_specs if x['id'] == spec['id'])
    approved = ap_source[spec['approvalRecord']].get('approvedRecommendations',{}).get(spec['id'],{})
    check('spec-exact-source:'+spec['id'],spec['approvedText'] == src['proposal'] and spec['approvedProposalSha256'] == sha(src['proposal'].encode()))
    if approved:
        check('spec-approval-content:'+spec['id'], approved['text'] == spec['approvedText'] and approved['sha256'] == spec['approvedProposalSha256'])
    for n, text in enumerate(v for v in re.split('[；。]',src['proposal']) if v.strip()):
        source_clauses.append((spec['id']+f'-CLAUSE-{n+1:02d}',spec['id'],text))
check('all-295-clauses-exact',source_clauses == [(x['id'],x['parentId'],x['text']) for x in trace['clauses']])
mods = {m['id']:m for m in scope['modules'] if m['id'] in MODS}
contracts = [c for p in scope['p1B']['packages'] for c in p['contracts'] if set(c.get('currentApplicability',{}).get('moduleIds',[])) & set(MODS)]
details = {}
ac_occurrences = collections.defaultdict(list)
for c in contracts:
    for key in ['fields','roles','lifecycle','actions','fieldDetails','roleMatrix','stateTransitions']:
        v = c.get(key)
        if not v: continue
        for n,item in enumerate(v if isinstance(v,list) else [v]):
            details[f'{c["id"]}/{key}/{n}'] = item
    for a in c.get('acceptanceCases',[]): ac_occurrences[a['id']].append(a)
check('149-details-exact-source',details == {x['id']:x['source'] for x in trace['contractDetails']})
check('24-closures-exact-source',{c['id']:c for m in mods.values() for c in m['p1']['closureChecklist']} == {x['id']:x['source'] for x in trace['closures']})
for b in scope['deliveryScope']['baseCapabilities']:
    for a in b.get('acceptanceCases',[]): ac_occurrences[a['id']].append(a)
check('acceptance-repeated-ids-do-not-conflict',all(all(row == rows[0] for row in rows) for rows in ac_occurrences.values()))
check('acceptance-exact-source-set',set(ac_occurrences) == {x['id'] for x in trace['acceptanceIds']})
for x in trace['acceptanceIds']:check('acceptance-source:'+x['id'],x['source'] == ac_occurrences[x['id']][0])
module_acs = {a for m in mods.values() for a in m['p1']['reviewPackage']['acceptanceCaseRefs']}
check('approved-module-AC-set',{x['id'] for x in trace['acceptanceIds'] if x['kind']=='approved_module'} == module_acs)
for g in ['specs','clauses','contractDetails','closures','foundations','acceptanceIds','historicalTasks']:
    check('unique:'+g,not duplicate_ids(trace[g]))
    if g != 'historicalTasks': check('design-refs:'+g,all(all(anchor(r) for r in x['designRefs']) for x in trace[g]))
sc = read('Acceptance_Scenarios.json')['scenarios']; tasks = read('P3_Work_Packages.json')['tasks']
sid = {x['id']:x for x in sc}; tid = {x['id']:x for x in tasks}
check('unique-scenarios',not duplicate_ids(sc));check('unique-tasks',not duplicate_ids(tasks))
check('all-scenarios-not-run',all(x['executionStatus']=='not_run' for x in sc))
check('all-tasks-not-started',all(x['status']=='proposed_not_started' for x in tasks))
check('all-GWT-evidence-exists',all(all(x.get(k) for k in ['given','when','then','expectedEvidence']) for x in sc))
check('scenario-task-links',all(x['taskId'] in tid and x['id'] in tid[x['taskId']]['scenarioIds'] for x in sc))
check('task-scenario-links',all(x['scenarioIds'] and all(s in sid and sid[s]['taskId']==x['id'] for s in x['scenarioIds']) for x in tasks))
for x in trace['acceptanceIds']:
    if x['kind']!='historical':
        y=sid['R2-P3-'+x['id']]
        check('GWT-source-preserved:'+x['id'],all(y[k]==x['source'][k] for k in ['when','then']) and (y['given']==x['source']['given'] or x['kind']=='approved_foundation' and y['given'].startswith(x['source']['given'])))
for g in ['specs','clauses','contractDetails','closures','foundations','acceptanceIds']:
    check('trace-scenario-resolution:'+g,all((x.get('scenarioIds') and all(s in sid for s in x['scenarioIds'])) or (x.get('legacyDisposition')=='source_request_only' and x.get('evidenceRequestIds')==['R2-SOURCE-M17-01']) for x in trace[g]))
legacy=read('Legacy_Acceptance_Map.json')
check('legacy-17-set',{x['id'] for x in legacy['acceptance']} == {x['id'] for x in trace['acceptanceIds'] if x['kind']=='historical'})
for x in legacy['acceptance']:
    check('legacy-original:'+x['id'],x['originalSource']==ac_occurrences[x['id']][0])
    check('legacy-refs:'+x['id'],all(r in sid or r in module_acs for r in x['currentAcceptanceRefs']))
for x in legacy['historicalTasks']:
    s=next(t for t in scope['acceptanceTasks'] if t['id']==x['id'])
    check('legacy-task:'+x['id'],x['originalSource']==s and x['criteriaIds']==[c['id'] for c in s['criteria']] and all(r in sid for r in x['scenarioRefs']))
original=read('Original_Limits.json')['groups']; limits=read('Limit_Resolution.json')
check('LIMIT-original-exact',{x['id']:x for x in original}=={x['id']:{**x,'moduleId':m} for m,mod in mods.items() for x in mod['p1']['reviewPackage']['exceptionProposals']})
check('LIMIT-unique',not duplicate_ids(limits['items']))
dispositions=dict(collections.Counter(x['disposition'] for x in limits['items']))
check('LIMIT-counts',dispositions==limits['counts']=={'P2_design_closed':15,'P3_validation':25,'P4_acceptance':12})
for m in MODS:
    items=[x for x in limits['items'] if x['parentLimitId']==m+'-LIMIT-01']
    check('LIMIT-phases:'+m, {'P3_validation','P4_acceptance'} <= {x['disposition'] for x in items} and all(x['ownerRole'] and x['closureCriterion'] for x in items))
counts={'modules':len(mods),'specs':len(source_specs),'clauses':len(source_clauses),'contractDetails':len(details),'closures':len(trace['closures']),'moduleAC':len(module_acs),'foundationAC':sum(x['kind']=='approved_foundation' for x in trace['acceptanceIds']),'historicalAC':len(legacy['acceptance']),'historicalTasks':len(legacy['historicalTasks']),'historicalCriteria':sum(len(x['criteriaIds']) for x in legacy['historicalTasks']),'tasks':len(tasks),'scenarios':len(sc),'LIMITgroups':len(original),'LIMITitems':len(limits['items']),'dispositions':dispositions}
expected={'modules':6,'specs':33,'clauses':295,'contractDetails':149,'closures':24,'moduleAC':78,'foundationAC':16,'historicalAC':17,'historicalTasks':5,'historicalCriteria':5,'tasks':46,'scenarios':138,'LIMITgroups':6,'LIMITitems':52}
check('independent-counts',all(counts[k]==v for k,v in expected.items()),counts)
check('approval-stage-boundary',proposal['p2ExitApproved'] is False and proposal['p3Entered'] is False and proposal['proposalOnly'] is True and proposal['registeredInController'] is False)

# Generation byte equality. Never run original checker: it writes the source manifest/evidence.
generation=[]
with tempfile.TemporaryDirectory(prefix='r2-p2-review-',dir='/workspace/scratch/a94fcceed57f') as tmp:
    td=Path(tmp)/'docs/delivery/r2-p2';td.mkdir(parents=True)
    for f in DESIGN.iterdir():
        if f.is_file(): (td/f.name).write_bytes(blob(FINAL,'docs/delivery/r2-p2/'+f.name))
    before={f.name:sha(f.read_bytes()) for f in td.iterdir() if f.is_file()}
    genenv={**ENV,'GIT_DIR':git('rev-parse','--absolute-git-dir').decode().strip()}
    for name in ['build_inventory.py','build_resolution.py','build_scenarios.py','build_schemas.py','build_handoff.py']:
        run=subprocess.run([sys.executable,str(td/name)],cwd=tmp,env=genenv,capture_output=True,text=True)
        generation.append({'script':name,'exitCode':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
    drift=[n for n,h in before.items() if sha((td/n).read_bytes())!=h]
check('generation-reproduction',not drift and all(x['exitCode']==0 for x in generation),{'drift':drift,'runs':generation})

# All 69 schemas and 76 conditional bindings read, checked structurally without a product test.
schema=read('Interface_Schemas.json'); registry=read('Command_Registry.json'); defs=schema['$defs']; errors=[]
def walk(v,path=''):
    if isinstance(v,dict):
        if '$ref' in v and (not v['$ref'].startswith('#/$defs/') or v['$ref'][8:] not in defs): errors.append(path+' unresolved '+v['$ref'])
        if v.get('type')=='object':
            if not set(v.get('required',[]))<=set(v.get('properties',{})):errors.append(path+' required outside properties')
            if v.get('additionalProperties') is not False and path!='/Command/properties/payload':errors.append(path+' open object')
        if 'pattern' in v:re.compile(v['pattern'])
        for k,w in v.items():walk(w,path+'/'+k)
    elif isinstance(v,list):
        for i,w in enumerate(v):walk(w,path+'/'+str(i))
walk(defs)
check('schema-local-structure',not errors,errors)
check('schema-registry-action-set',defs['Command']['properties']['action']['enum']==[x['action'] for x in registry['commands']])
for c,condition in zip(registry['commands'],defs['Command']['allOf']):
    p=condition['then']['properties'];check('schema-binding:'+c['action'],condition['if']['properties']['action']['const']==c['action'] and p['payload']['$ref']==c['payloadSchema'] and p['objectRef']['properties']['module']['const']==c['module'])

# Exact content repeat counts are not semantic coverage; report them separately.
family_only=[x['id'] for x in trace['clauses'] if x['scenarioIds']==next(s for s in trace['specs'] if s['id']==x['parentId'])['scenarioIds']]
put('Mechanical_Verification.json',{'kind':'independent_document_checks_not_product_tests','startedAt':start,'finishedAt':datetime.now(timezone.utc).isoformat(),'reviewedFinalHead':FINAL,'fixedDesignHead':FIXED,'sourceMain':BASE,'sharedR1Design':R1,'counts':counts,'checks':checks,'checkCount':len(checks),'failedChecks':[x for x in checks if not x['ok']],'familyInheritedClauseMappings':family_only,'note':'Structural count/ref success does not conclude semantic design completeness.'})
put('Read_Hash_Manifest.json',{'kind':'complete_bytes_and_json_parse_inventory','objects':list(reads.values()),'objectCount':len(reads),'excludes':['this review manifest itself','all review output hashes to avoid cycles'],'note':'Manual semantic review and samples are separately recorded; hashing historical product files is not running tests.'})
put('Worktree_Observation.json',{'observedAt':datetime.now(timezone.utc).isoformat(),'worktrees':snapshot_worktrees(),'note':'R1 concurrent state is read-only observation, not R2 completion evidence.'})
print(json.dumps({'counts':counts,'checks':len(checks),'failed':[x['id'] for x in checks if not x['ok']],'generationDrift':drift,'readObjects':len(reads)},ensure_ascii=False))
