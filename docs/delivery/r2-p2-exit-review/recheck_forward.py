"""Independent fixed-object P2 recheck, round 1. Never imports product/designer code.

Run in an isolated Python environment containing jsonschema 4.23.0.
Only --record writes, exclusively to new Recheck_* review evidence files.
No network, checkout, database, business test, or phase authorization.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
D = 'docs/delivery/r2-p2/'
CONTENT = 'dc6dd896fbf388b70069ecb756547f85ee89d08a'
PACKAGE = 'a7a23d6bff024f4660fd14b0c22f47a6d40d928f'
OLD_CONTENT = '7ff3a28c7660dac658d5243d7c4535a9c8037fc2'
OLD = '8b3daf9270181ffe2e77015be723da8e611d83a5'
REVIEW = 'bd976480fad9822ee52ecb4b00a080360772b0f3'
BASE = '22be3a7e366d6787180d4f593a30f5984c70e03a'
checks, hashes = [], {}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def blob(ref, path):
    b = git('show', ref + ':' + path)
    hashes[(ref, path)] = dict(gitRef=ref, path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
    return b

def no_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError('Duplicate JSON key: ' + k)
        obj[k] = v
    return obj

def read(name, ref=CONTENT):
    return json.loads(blob(ref, D + name), object_pairs_hook=no_duplicates)

def check(name, condition, detail=None):
    row = dict(check=name, passed=bool(condition))
    if detail is not None:
        row['detail'] = detail
    checks.append(row)

def verify_ref(item, label):
    b = blob(item['gitRef'], item['path'])
    check(label, hashlib.sha256(b).hexdigest() == item['sha256'] and ('bytes' not in item or len(b) == item['bytes']))

for ref in [CONTENT, PACKAGE, OLD_CONTENT, OLD, REVIEW]:
    check('commit readable ' + ref, git('cat-file', '-t', ref).strip() == b'commit')
check('package is direct content child', git('rev-parse', PACKAGE + '^').decode().strip() == CONTENT)
check('old package ancestor of repaired content', subprocess.run(['git', 'merge-base', '--is-ancestor', OLD, CONTENT], cwd=ROOT).returncode == 0)
changed = git('diff', '--name-only', OLD, PACKAGE).decode().splitlines()
check('repair net diff exclusively authorized documentation', all(p.startswith(D) for p in changed), changed)
commits = git('rev-list', '--reverse', OLD + '..' + PACKAGE).decode().splitlines()
for commit in commits:
    names = git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
    check('per-commit authorized scope ' + commit, all(p.startswith(D) for p in names), names)
wrapper_files = git('diff', '--name-only', CONTENT, PACKAGE).decode().splitlines()
check('wrapper content separation', set(wrapper_files) == {D + n for n in ['Artifact_Manifest.json', 'Commit_Register.json', 'Commit_Register.md', 'Controller_Proposal.json', 'Design_Checkpoint.json', 'Repair_Delivery_Record.json', 'Resume.md', 'evidence/repair-final-packaging.json']})
proposal = read('Controller_Proposal.json', PACKAGE)
check('fixed content in final proposal', proposal['designContentHead'] == CONTENT)
refs = proposal['fixedDesignReferences']
check('44 unique fixed content references', len(refs) == len({x['path'] for x in refs}) == 44 and all(x['gitRef'] == CONTENT for x in refs))
for item in refs:
    verify_ref(item, 'proposal fixed hash ' + item['path'])
for ref in [CONTENT, PACKAGE, OLD_CONTENT, OLD]:
    manifest = read('Artifact_Manifest.json', ref)['artifacts']
    check('manifest unique/excludes itself ' + ref, len(manifest) == len({i['path'] for i in manifest}) and all(i['path'] != D + 'Artifact_Manifest.json' and '/evidence/' not in i['path'] for i in manifest))
    for item in manifest:
        verify_ref(dict(item, gitRef=ref), 'own-object artifact hash ' + ref + '/' + item['path'])
    files = git('ls-tree', '-r', '--name-only', ref, '--', D).decode().splitlines()
    check('manifest complete ' + ref, {i['path'] for i in manifest} == {p for p in files if p != D + 'Artifact_Manifest.json' and '/evidence/' not in p})
sources = read('Source_Manifest.json')
check('78 source entries', len(sources) == 78)
for i in sources:
    verify_ref(i, 'original source hash ' + i['path'])
repair = read('Repair_Record.json')
check('11 independent review sources', len(repair['sources']) == 11)
for i in repair['sources']:
    verify_ref(i, 'repair review source hash ' + i['path'])
delivery = read('Repair_Delivery_Record.json', PACKAGE)
check('repair delivery fixed object mapping', delivery['reviewHead'] == REVIEW and delivery['priorFinalHead'] == OLD and delivery['priorContentHead'] == OLD_CONTENT and delivery['newFixedContentHead'] == CONTENT and delivery['fixedReferenceCount'] == 44)
check('repair six content commits exact Git ancestry', [r['head'] for r in delivery['contentCommits']] == commits[:-1] and commits[-1] == PACKAGE)
check('repair findings not self-accepted', all(repair['findings']['R2-EXIT-00'+str(i)] == 'design_repaired_pending_independent_recheck' for i in range(1,5)) and repair['independentAcceptedP2ItemsBeforeRepair'] == 9 and len(repair['affectedP2Items']) == 6 and delivery['limitAccounting']['independentAcceptedAfterRepair'] is None)
for ref in [CONTENT, PACKAGE]:
    for path in git('ls-tree', '-r', '--name-only', ref, '--', D).decode().splitlines():
        if path.endswith('.json'):
            json.loads(blob(ref, path), object_pairs_hook=no_duplicates)
check('all fixed JSON parse with duplicate-key rejection', True)

# Independent structural validator and semantic lookup oracle. Designer scripts are NOT imported.
S = read('Interface_Schemas.json')
E = read('Schema_Examples.json')
F = E['fixture']
Draft202012Validator.check_schema(S)
check('Draft 2020-12 metaschema', True)
def walk(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for k, v in value.items():
            yield from walk(v, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, path + (i,))

def identity(v):
    keys = ['producer', 'objectType', 'rootId', 'versionId'] if v['kind'] == 'internal' else ['sourceNamespace', 'objectType', 'externalId', 'externalVersion']
    return tuple(v.get(k) for k in keys)

catalogs = {kind: {identity(v): v for v in values} for kind, values in [('internal', F['internalVersions']), ('external', F['externalCaptures'])]}
def semantic(x, mode):
    errors = []
    for path, v in walk(x):
        if v.get('kind') in catalogs:
            if catalogs[v['kind']].get(identity(v)) != v:
                errors.append('EXACT_SOURCE_MANIFEST_MISMATCH:' + str(path))
    if mode == 'new_indicator':
        if any(x[k] is not None for k in ['childId', 'childVersionId', 'indicatorVersionRef', 'levelId', 'levelVersionRef']):
            errors.append('NEW_CHILD_SERVER_BOUND_IDS')
    if mode == 'catalog' and x.get('evaluationMode') == 'numeric':
        scale = x['numericScale']
        mn, mx, step = (Decimal(scale[k]) for k in ['min', 'max', 'step'])
        if not mn < mx or step <= 0 or any(v != v.quantize(Decimal(1).scaleb(-scale['precision'])) for v in [mn, mx, step]):
            errors.append('NUMERIC_SCALE_RELATION')
    if mode == 'catalog' and x.get('evaluationMode') == 'rating':
        r = x['ratingSelection']
        levels = F['ratingSchemeLevels'].get(r['ratingSchemeVersionRef']['versionId'], [])
        if not set(r['levelIds']).issubset(levels):
            errors.append('RATING_LEVEL_MEMBERSHIP')
    if mode == 'questionnaire':
        prior = set()
        standards = {identity(v) for v in x['standardVersionRefs']}
        for q in x['questions']:
            qid = q['questionVersionRef']['versionId']
            if qid in prior:
                errors.append('DUPLICATE_QUESTION')
            if any(role not in x['roleVersionRefs'] for role in q['roleApplicability']['roleVersionRefs']):
                errors.append('ROLE_NOT_IN_QUESTIONNAIRE')
            dim = F['dimensionMembers'].get(q['dimension']['versionId'], {})
            if not any(v[-1] == dim.get('standardVersionId') for v in standards) or not {v['versionId'] for v in q['indicatorVersionRefs']}.issubset(dim.get('indicatorVersionIds', [])):
                errors.append('DIMENSION_MANIFEST_MEMBERSHIP')
            vis = q['visibility']
            if vis['kind'] == 'conditional' and not set(vis['dependsOnQuestionVersionIds']).issubset(prior):
                errors.append('VISIBILITY_DAG_ORDER')
            if 'conditionAst' in q and q['conditionAst'] != vis.get('conditionAst'):
                errors.append('LEGACY_VISIBILITY_CONFLICT')
            prior.add(qid)
    if mode == 'history' and x['previousResultRef'] is not None:
        p = x['previousResultRef']
        h = F['historicalResults'].get(p['resultVersionRef']['versionId'])
        if not h or h['projectRootId'] == F['currentProjectRootId'] or h['periodEnd'] > x['startOn'] or not h['publishedAt'] <= p['asOf'] <= F['serverNow']:
            errors.append('HISTORY_BOUNDARY_OR_PUBLICATION')
    return errors

def validate(schema, instance, mode='references'):
    v = Draft202012Validator({'$schema': S['$schema'], '$defs': S['$defs'], '$ref': '#/$defs/' + schema}, format_checker=FormatChecker())
    errors = [{'path': list(e.absolute_path), 'validator': e.validator, 'message': e.message} for e in v.iter_errors(instance)]
    guards = semantic(instance, mode) if not errors else []
    return dict(actual='reject' if errors or guards else 'accept', schemaErrors=errors, semanticErrors=guards)

schema_results = []
for c in E['cases']:
    result = dict(id=c['id'], schema=c['schema'], expected=c['expected'], **validate(c['schema'], c['instance'], c['semanticGuard']))
    schema_results.append(result)
    check('schema example ' + c['id'], result['actual'] == c['expected'])
check('34 distinct schema examples / 9 accepted 25 rejected', len(schema_results) == len({c['id'] for c in schema_results}) == 34 and Counter(c['actual'] for c in schema_results) == {'accept': 9, 'reject': 25})

# ALL 76 action bindings: no generic payload escape and external union reachability.
registry = read('Command_Registry.json')['commands']
bindings = {c['if']['properties']['action']['const']: c['then']['properties'] for c in S['$defs']['Command']['allOf']}
check('76 exact command bindings', len(registry) == len(bindings) == len(S['$defs']['Command']['properties']['action']['enum']) == 76)
def reaches_external(name, seen=None):
    seen = set() if seen is None else seen
    if name in seen:
        return False
    seen.add(name)
    if name == 'ExternalVersionRef':
        return True
    return any(reaches_external(v['$ref'].split('/')[-1], seen) for _, v in walk(S['$defs'][name]) if '$ref' in v)

command_results = []
for r in registry:
    action = r['action']
    exceptional = action in ['r2.m37.standard.create', 'r2.m37.standard.edit']
    exposed = reaches_external(r['payloadSchema'].split('/')[-1])
    policy = r['referencePolicy']
    ok = bindings[action]['payload']['$ref'] == r['payloadSchema'] and policy['defaultKind'] == 'internal' and bool(policy['externalAllowedPaths']) == exceptional and exposed == exceptional
    check('full command policy ' + action, ok)
    command_results.append(dict(action=action, payloadSchema=r['payloadSchema'], referencePolicy=policy, externalReachable=exposed, passed=ok))

cases_by_id = {c['id']: c for c in E['cases']}
complete_probes = []
def command_probe(label, instance, expected):
    result = validate('Command', instance)
    complete_probes.append(dict(id=label, expected=expected, **result))
    check('supplemental complete Command ' + label, result['actual'] == expected)

basecmd = cases_by_id['REF-COMMAND-VALID']['instance']
external = F['externalCaptures'][0]
internal = F['internalVersions'][0]
for action in ['r2.m37.standard.create', 'r2.m37.standard.edit']:
    for dimension in ['ability', 'potential', 'experience', 'achievement']:
        for kind, ref in [('internal', internal), ('external', external)]:
            cmd = copy.deepcopy(basecmd)
            cmd['action'] = action
            if action.endswith('.edit'):
                cmd['objectRef']['rootId'], cmd['expectedEntityRevision'] = 'STD-EDIT', 1
            cmd['payload']['lines'][0].update(dimension=dimension, sourceVersionRef=copy.deepcopy(ref))
            command_probe(action + '/' + dimension + '/' + kind, cmd, 'accept' if kind == 'internal' or dimension == 'achievement' else 'reject')
cmd = copy.deepcopy(basecmd)
cmd['payload']['purposeRuleVersionRefs'] = [copy.deepcopy(external)]
command_probe('external purpose-rule bypass', cmd, 'reject')
cmd = copy.deepcopy(basecmd)
cmd['payload']['lines'][0]['sourceVersionRef']['trustContractVersionRef'] = copy.deepcopy(external)
command_probe('external trust-contract bypass', cmd, 'reject')
for caseid, actions, module in [('TYPE-VALID', ['r2.m06.catalog.create', 'r2.m06.catalog.edit'], 'M06'), ('TYPE-RATING-VALID', ['r2.m06.catalog.create'], 'M06'), ('QUESTION-VALID', ['r2.m26.questionnaire.create'], 'M26'), ('HISTORY-VALID', ['r2.m18.project.create', 'r2.m18.project.save'], 'M18')]:
    for action in actions:
        cmd = copy.deepcopy(basecmd)
        cmd.update(action=action, payload=copy.deepcopy(cases_by_id[caseid]['instance']))
        cmd['objectRef'].update(module=module, objectType=caseid.split('-')[0].lower(), rootId=None if action.endswith('.create') else 'EDIT-ROOT')
        cmd['expectedEntityRevision'] = 0 if action.endswith('.create') else 1
        command_probe(caseid + '/' + action + '/valid-control', cmd, 'accept')
        for path, v in list(walk(cmd['payload'])):
            if v.get('kind') != 'internal':
                continue
            mutated = copy.deepcopy(cmd)
            parent = mutated['payload']
            for key in path[:-1]:
                parent = parent[key]
            parent[path[-1]] = copy.deepcopy(external)
            command_probe(caseid + '/' + action + '/external-at-' + '/'.join(map(str, path)), mutated, 'reject')

# Rational coefficient grouping, independent of answer/atom IDs and designer checker.
anon = read('Anonymity_Cases.json')['cases']
def partitions(rows, key):
    buckets = defaultdict(set)
    for row in rows:
        coeff = tuple(Fraction(v) for v in row['coefficients'])
        if any(coeff):
            buckets[coeff].add(row[key])
    return [dict(signature=[str(x) for x in signature], members=sorted(members), size=len(members)) for signature, members in sorted(buckets.items())]

anon_results = []
for c in anon:
    groups = partitions(c['rows'], 'reviewer')
    n = len(c['rows'][0]['coefficients'])
    values = [str(sum(Fraction(r['coefficients'][i]) * Fraction(r['value']) for r in c['rows'])) for i in range(n)]
    subject_groups = partitions(c.get('subjectRows', []), 'subject')
    bottom = defaultdict(set)
    for r in c['rows']:
        if any(Fraction(v) for v in r['coefficients']):
            bottom[r['subject']].add(r['reviewer'])
    reasons = []
    if c.get('namedMode'):
        if c['namedMode'] != 'unique_manager' or not c.get('noticeNamed') or not c.get('uniqueManager'):
            reasons.append('NAMED_BOUNDARY_OR_NO_NONSELF')
    elif not groups or min(g['size'] for g in groups) < c['k']:
        reasons.append('REVIEWER_EQUIVALENCE_UNDER_K')
    if c.get('subjectRows') and (not subject_groups or min(g['size'] for g in subject_groups) < 3 or min(map(len, bottom.values())) < c['k']):
        reasons.append('ORGANIZATION_SUBJECT_OR_BOTTOM_K')
    if c.get('partitionValid') is False:
        reasons.append('CONTINUITY_PARTITION_INVALID')
    actual = 'suppress' if reasons else 'publish'
    result = dict(id=c['id'], classes=groups, subjectClasses=subject_groups, bottomCountsIndependentlyFromRows={s:len(v) for s,v in bottom.items()}, columnValues=values, actual=actual, expected=c['expected'], reasons=reasons)
    anon_results.append(result)
    check('anonymity case ' + c['id'], actual == c['expected'] and sorted(g['size'] for g in groups) == sorted(c['expectedClassSizes']) and values == c['expectedValues'])
check('16 unique anonymity cases / 5 publish 11 suppress', len(anon_results) == len({r['id'] for r in anon_results}) == 16 and Counter(r['actual'] for r in anon_results) == {'publish':5, 'suppress':11})

# Graph built from task inputs, with Kahn rather than designer graphlib.
dep = read('Task_Dependencies.json')
verify_ref(dep['reviewSource'], 'dependency independent prior source')
tasks = read('P3_Work_Packages.json')['tasks']
taskmap = {t['id']:t for t in tasks}
oldrecs = json.loads(blob(REVIEW, 'docs/delivery/r2-p2-exit-review/P3_Sequencing_Recommendations.json'))
olddeps = {t['taskId']:t for t in oldrecs['tasks']}
graph = {t['taskId']:set(t['r2CompletionPredecessors']) | {'R1-CAP-' + k for k in t['requiredR1CapabilityGates']} | set(t['externalProducerDependencies']) for t in dep['tasks']}
for k in dep['r1CapabilitySlots']:
    graph['R1-CAP-' + k] = set()
for k in dep['externalProducerSlots']:
    graph[k] = set()
graph['R3-PRODUCERS-READY'] = set(dep['externalProducerSlots'])
graph[dep['jointClosure']['id']] = set(dep['jointClosure']['completionPredecessors'])
graph['P3-R1-10-COMPLETE'] = {dep['jointClosure']['id']}
graph['P3-R1-11-EXIT'] = {'P3-R1-10-COMPLETE'}
check('graph no missing nodes', all(p in graph for ps in graph.values() for p in ps))
pending = {t:set(p) for t,p in graph.items()}
order = []
while pending:
    ready = sorted(t for t, ps in pending.items() if not ps)
    if not ready:
        break
    order.extend(ready)
    for t in ready:
        del pending[t]
    for ps in pending.values():
        ps.difference_update(ready)
check('55 nodes 165 distinct edges acyclic', len(graph) == 55 and sum(map(len,graph.values())) == 165 and not pending)
task_reviews = []
for t in dep['tasks']:
    tid = t['taskId']
    ok = t == taskmap[tid]['dependencies'] and t['status'] == 'proposed_not_started' and t['r2CompletionPredecessors'] == olddeps[tid]['recommendedR2CompletionPredecessors'] and t['requiredR1CapabilityGates'] == olddeps[tid]['requiredR1CapabilityGates']
    ok &= all(ref.split('/')[-1] in S['$defs'] for ref in t['requiredSchemas']) and bool(t['requiredSchemas'])
    ok &= all(bool(t[k]) for k in ['requiredAdapters','requiredSecurityContract','requiredMigrationOrRecovery','completionCondition','independentStartCondition'])
    ok &= t['baselineSlots'] == ['R1-' + k for k in t['requiredR1CapabilityGates']]
    check('46-task complete dependency review ' + tid, ok)
    task_reviews.append(dict(taskId=tid, passed=ok, dependencies=t))
check('46 unique task coverage', len(task_reviews) == len({t['taskId'] for t in task_reviews}) == 46)
for k,s in dep['r1CapabilitySlots'].items():
    check('owner slot remains unfilled ' + k, s['status'] == 'pending_owner_freeze' and not s['capabilityOpen'] and s['independentEvidenceRefs'] == [] and all(s[f] is None for f in ['implementationCommitSha','schemaVersion','adapterVersion','securityEpochContractVersion','writerEpochContractVersion','recoveryEpochContractVersion','migrationVersion','rollbackCommitSha']))

# Regression: immutable approved sources, trace IDs, exact phase state, source-only requests.
trace, before = read('Requirements_Trace.json'), read('Requirements_Trace.json', OLD)
for section,count in [('specs',33),('clauses',295),('contractDetails',149),('closures',24),('foundations',6),('acceptanceIds',111),('historicalTasks',5)]:
    rows, previous = trace[section], before[section]
    check('trace unique identity/count ' + section, len(rows) == len({x['id'] for x in rows}) == count and [x['id'] for x in rows] == [x['id'] for x in previous])
    for a,b in zip(rows, previous):
        check('source meaning retained ' + section + '/' + a['id'], all(a.get(k) == b[k] for k in ['source','approvedText','approvedProposalSha256','approvalRecord','text','parentId'] if k in b))
check('AC 78+16+17 distinct', Counter(x['kind'] for x in trace['acceptanceIds']) == {'approved_module':78,'approved_foundation':16,'historical':17})
scope = json.loads(blob(BASE, 'docs/delivery/Scope_Register.json'))
for spec in trace['specs']:
    obj = scope
    for token in spec['sourcePointer'].strip('/').split('/'):
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    check('33 approved source direct pointer ' + spec['id'], obj['id'] == spec['id'] and obj['proposal'] == spec['approvedText'] and obj['approvalRecord'] == spec['approvalRecord'] and hashlib.sha256(obj['proposal'].encode()).hexdigest() == spec['approvedProposalSha256'])
    derived = [c['text'] for c in trace['clauses'] if c['parentId'] == spec['id']]
    check('independent approved clause split ' + spec['id'], derived == [v for v in re.split('[；。]', obj['proposal']) if v.strip()])

scenarios = read('Acceptance_Scenarios.json')['scenarios']
scenario_ids = {s['id'] for s in scenarios}
oldsc = {s['id']:s for s in read('Acceptance_Scenarios.json', OLD)['scenarios']}
adaptations = read('Foundation_Adaptations.json')['adaptations']
foundation_reviews = []
for sid, a in adaptations.items():
    s = next(s for s in scenarios if s['id'] == sid)
    original = next(x['source'] for x in trace['acceptanceIds'] if sid == 'R2-P3-' + x['id'])
    ok = all(s[k] == v for k,v in a.items()) and all(a.get(k) for k in ['fixture','actions','actors','allowedFields','forbiddenFields','given','when','then','expectedVersions']) and s['originalFoundationGwt'] == {k:original[k] for k in ['given','when','then','basis']} and a['executionStatus'] == 'not_run'
    check('foundation adaptation direct executable definition ' + sid, ok)
    foundation_reviews.append(dict(scenarioId=sid, passed=ok, actions=a['actions'], actors=a['actors'], expectedVersions=a['expectedVersions'], productExecuted=False))
check('3 concrete foundation adaptations', len(foundation_reviews) == 3)
for s in scenarios:
    ok = s['executionStatus'] == 'not_run' and s['taskId'] in taskmap and bool(s['expectedEvidence']) and all(s[k] for k in ['given','when','then'])
    if s['id'] not in adaptations:
        ok &= all(s[k] == oldsc[s['id']][k] for k in ['given','when','then'])
    check('138 scenario state/source/forward task ' + s['id'], ok)
check('138 original scenario IDs', len(scenarios) == len(scenario_ids) == 138 and scenario_ids == set(oldsc))
for t in tasks:
    check('task scenario reverse mapping ' + t['id'], t['status'] == 'proposed_not_started' and t['scenarioIds'] == [s['id'] for s in scenarios if s['taskId'] == t['id']] and bool(t['scenarioIds']))
for section in ['specs','clauses','contractDetails','closures','foundations','acceptanceIds']:
    for r in trace[section]:
        check('trace scenario closure ' + r['id'], set(r['scenarioIds']).issubset(scenario_ids) and bool(r['scenarioIds'] or r.get('evidenceRequestIds')))
for n in ['Architecture.md','Migration_Rollback.md','Recovery_Cost_Responsibilities.md','Original_Limits.json','Legacy_Acceptance_Map.json','Source_Manifest.json','Source_Requests.json','Approval_Provenance.json']:
    check('accepted regression byte preserved ' + n, blob(CONTENT,D+n) == blob(OLD,D+n))
requests = read('Source_Requests.json')['requests']
check('7 external requests only', len(requests) == 7 and all(r['status'] == 'request_only_not_sent_or_executed' for r in requests))
check('no approval/status lifting', not proposal['p2ExitApproved'] and not proposal['p3Entered'] and not proposal['productModified'] and not proposal['deployed'] and not repair['r2P3Started'] and proposal['changesToCanonicalLedger'] == [] and all(not m['p2ExitApproved'] and not m['implementationAccepted'] for m in proposal['moduleStates']))
check('60/240/30 targets unproved', proposal['recoveryTargets'] == {'rpoMinutes':60,'rtoMinutes':240,'retentionDays':30,'runtimeProvenThisRun':False})

# Six disputed LIMITs: recomputed probe results + exact design-input/evidence objects + future roles.
limits = read('Limit_Resolution.json')
oldlimits = {x['id']:x for x in read('Limit_Resolution.json', OLD)['items']}
check('52 mutually exclusive responsibilities', len(limits['items']) == len({x['id'] for x in limits['items']}) == 52 and Counter(x['disposition'] for x in limits['items']) == {'P2_design_closed':15,'P3_validation':25,'P4_acceptance':12})
check('0 complete groups / 6 overlapping residual groups', limits['fullyClosedOriginalGroups'] == 0 and limits['originalGroupsWithP3Residual'] == limits['originalGroupsWithP4Residual'] == 6 and limits['residualGroupCountsOverlap'])
limit_results = []
probe_lookup = {r['id']:r for r in schema_results + anon_results}
for item in limits['items']:
    if item['disposition'] != 'P2_design_closed':
        check('unchanged later responsibility ' + item['id'], item == oldlimits[item['id']])
    if 'repairProof' not in item:
        continue
    p = item['repairProof']
    evidence = read(p['evidencePath'])
    evidence_hash = hashlib.sha256(blob(CONTENT,D+p['evidencePath'])).hexdigest()
    inputs = {n:hashlib.sha256(blob(CONTENT,D+n)).hexdigest() for n in evidence['inputSha256']}
    probes = [probe_lookup[i] for i in p['documentProbeIds']]
    future = [x for x in limits['items'] if x['parentLimitId'] == item['parentLimitId'] and x['disposition'] != 'P2_design_closed']
    ok = evidence_hash == p['evidenceSha256'] and inputs == evidence['inputSha256'] and all(r['actual'] == r['expected'] for r in probes) and {'P3_validation','P4_acceptance'}.issubset(x['disposition'] for x in future) and all(x['ownerRole'] and x['closureCriterion'] for x in future)
    check('disputed LIMIT independently recomputed ' + item['id'], ok)
    groups = {r.get('schema') for r in probes}
    mappings = [dict(specId=s['id'], mapping=m) for s in trace['specs'] for m in s.get('targetedRepairMappings',[]) if set(m['exampleIds']) & set(p['documentProbeIds'])]
    if item['repairFindingId'] == 'R2-EXIT-002':
        mappings = [dict(specId='M26-SPEC-02', scenarios=[s['id'] for s in scenarios if s.get('anonymityOracleRef')])]
    limit_results.append(dict(id=item['id'], verificationPassed=ok, independentDisposition='accepted_design_layer' if ok else 'not_accepted', documentProbeIds=p['documentProbeIds'], inputSha256=inputs, designerEvidence=dict(gitRef=CONTENT,path=D+p['evidencePath'],sha256=evidence_hash), designRefs=item['designRefs'], requirementMappings=mappings, futureResponsibilities=future, riskFullyClosed=False))
check('exactly six re-proposed LIMITs verified', len(limit_results) == 6 and all(r['verificationPassed'] for r in limit_results))

summary = dict(checkCount=len(checks), failed=sum(not c['passed'] for c in checks), schema=Counter(r['actual'] for r in schema_results), anonymity=Counter(r['actual'] for r in anon_results), commands=len(command_results), supplementalCompleteCommandProbes=len(complete_probes), adaptations=len(foundation_reviews), taskCount=len(task_reviews), graphNodes=len(graph), graphEdges=sum(map(len,graph.values())), graphCycles=0 if not pending else None, disputedLimits=len(limit_results))
output = dict(kind='independent_P2_fixed_object_documentary_recheck_round1_not_product_test', designContentHead=CONTENT, packagingHead=PACKAGE, originalIndependentReviewHead=REVIEW, validator='jsonschema '+importlib.metadata.version('jsonschema')+' Draft202012Validator+FormatChecker; independently written semantic oracle', summary=summary, checks=checks, schemaResults=schema_results, commandPolicyReview=command_results, supplementalCompleteCommandProbes=complete_probes, anonymityResults=anon_results, foundationReviews=foundation_reviews, taskReviews=task_reviews, dependencyGraph={k:sorted(v) for k,v in graph.items()}, topologicalOrder=order, limits=limit_results)
if argparse.ArgumentParser().parse_known_args()[1] == ['--record']:
    (OUT/'Recheck_Round1.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    (OUT/'Recheck_Input_Hashes.json').write_text(json.dumps(dict(kind='immutable_Git_inputs_not_circular_self_hashes', inputs=sorted(hashes.values(),key=lambda r:(r['gitRef'],r['path']))),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary, ensure_ascii=False))
for c in checks:
    if not c['passed']:
        print(json.dumps(c,ensure_ascii=False))
raise SystemExit(1 if summary['failed'] else 0)
