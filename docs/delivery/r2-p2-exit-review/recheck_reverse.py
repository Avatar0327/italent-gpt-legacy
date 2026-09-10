"""Second independent overall recheck. Does not import/read round-1 implementation/results.

Uses inverse source reconstruction, DFS cycle detection, pairwise rational row
equivalence, and separately evaluated schema/fixture predicates. P2 documents only.
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path
from jsonschema import FormatChecker, validators

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
D = 'docs/delivery/r2-p2/'
C = 'dc6dd896fbf388b70069ecb756547f85ee89d08a'
P = 'a7a23d6bff024f4660fd14b0c22f47a6d40d928f'
OLD = '8b3daf9270181ffe2e77015be723da8e611d83a5'
R = 'bd976480fad9822ee52ecb4b00a080360772b0f3'
B = '22be3a7e366d6787180d4f593a30f5984c70e03a'
checks = []
def raw(ref, path):
    return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
def doc(name, ref=C):
    return json.loads(raw(ref,D+name))
def test(name, value, detail=None):
    checks.append(dict(check=name,passed=bool(value),detail=detail))
def descend(x):
    if isinstance(x,dict):
        yield x
        for v in x.values():
            yield from descend(v)
    elif isinstance(x,list):
        for v in x:
            yield from descend(v)
def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)

# Inverse provenance: source -> approved records/fields/ACs, not package counters.
scope = json.loads(raw(B,'docs/delivery/Scope_Register.json'))
trace = doc('Requirements_Trace.json')
mods = ['M37','M06','M26','M18','M17','M03']
contracts = [c for p in scope['p1B']['packages'] for c in p['contracts'] if set(c.get('currentApplicability',{}).get('moduleIds',[])) & set(mods)]
details = {}
for contract in contracts:
    for key in ['fields','roles','lifecycle','actions','fieldDetails','roleMatrix','stateTransitions']:
        values = contract.get(key,[])
        values = values if isinstance(values,list) else [values]
        for i,value in enumerate(values):
            details[f'{contract["id"]}/{key}/{i}'] = value
test('149 independently extracted field/role/state entries', len(details)==149 and details=={r['id']:r['source'] for r in trace['contractDetails']})
original_acs = {a['id']:a for c in contracts for a in c.get('acceptanceCases',[])}
original_acs.update({a['id']:a for b in scope['deliveryScope']['baseCapabilities'] for a in b.get('acceptanceCases',[])})
test('111 source acceptance entries exact',original_acs=={a['id']:a['source'] for a in trace['acceptanceIds']})
approved_ids = []
closures = []
for m in scope['modules']:
    if m['id'] in mods:
        approved_ids.extend(m['p1']['reviewPackage']['acceptanceCaseRefs'])
        closures.extend(m['p1']['closureChecklist'])
test('78 approved module ACs no double counting',len(approved_ids)==len(set(approved_ids))==78 and set(approved_ids)=={a['id'] for a in trace['acceptanceIds'] if a['kind']=='approved_module'})
test('24 internal closure sources',len(closures)==24 and {a['id']:a for a in closures}=={a['id']:a['source'] for a in trace['closures']})
approved_records={a['id']:a for a in scope['p1B']['approvalRecords']}
for s in trace['specs']:
    record=approved_records[s['approvalRecord']]
    test('approved record exists '+s['id'],bool(record))
    if s['id'] in record.get('approvedRecommendations',{}):
        test('approved recommendation digest '+s['id'],record['approvedRecommendations'][s['id']]['sha256']==s['approvedProposalSha256'])

# Recompute 34 cases with independent traversal/list manifest selection.
schema=doc('Interface_Schemas.json')
validator_class=validators.validator_for(schema)
validator_class.check_schema(schema)
examples=doc('Schema_Examples.json')
fixture=examples['fixture']
internal={canonical(x) for x in fixture['internalVersions']}
external={canonical(x) for x in fixture['externalCaptures']}
schema_rows=[]
for c in reversed(examples['cases']):
    v=validator_class(dict(schema, **{'$ref':'#/$defs/'+c['schema']}),format_checker=FormatChecker())
    errors=list(v.iter_errors(c['instance']))
    x=c['instance']; semantic_ok=True
    if not errors:
        semantic_ok=all(canonical(o) in (internal if o['kind']=='internal' else external) for o in descend(x) if o.get('kind') in ['internal','external'])
        if c['semanticGuard']=='new_indicator':
            semantic_ok &= all(x[k] is None for k in ['childId','childVersionId','indicatorVersionRef','levelId','levelVersionRef'])
        if c['semanticGuard']=='catalog' and x.get('ratingSelection'):
            r=x['ratingSelection']; semantic_ok &= all(i in fixture['ratingSchemeLevels'].get(r['ratingSchemeVersionRef']['versionId'],[]) for i in r['levelIds'])
        if c['semanticGuard']=='questionnaire':
            for q in x['questions']:
                d=fixture['dimensionMembers'].get(q['dimension']['versionId'],{})
                semantic_ok &= all(r in x['roleVersionRefs'] for r in q['roleApplicability']['roleVersionRefs']) and d.get('standardVersionId') in [r['versionId'] for r in x['standardVersionRefs']] and all(r['versionId'] in d.get('indicatorVersionIds',[]) for r in q['indicatorVersionRefs'])
        if c['semanticGuard']=='history' and x['previousResultRef']:
            h=x['previousResultRef']; source=fixture['historicalResults'].get(h['resultVersionRef']['versionId'])
            semantic_ok &= bool(source and source['projectRootId'] != fixture['currentProjectRootId'] and source['periodEnd'] <= x['startOn'] and source['publishedAt'] <= h['asOf'] <= fixture['serverNow'])
    result='accept' if not errors and semantic_ok else 'reject'
    test('reverse schema '+c['id'],result==c['expected'])
    schema_rows.append(dict(id=c['id'],actual=result,structuralErrors=len(errors),semanticPredicate=bool(semantic_ok) if not errors else 'not_evaluated'))
test('reverse schema counts',Counter(r['actual'] for r in schema_rows)=={'accept':9,'reject':25})
for o in descend(schema):
    if '$ref' in o:
        test('schema target '+o['$ref'],o['$ref'].startswith('#/$defs/') and o['$ref'].split('/')[-1] in schema['$defs'])
# Trace backwards from union use: a complete inventory of locations, not registry trust.
union_uses=[]
def locations(x,path=()):
    if isinstance(x,dict):
        if x.get('$ref')=='#/$defs/VersionRef':
            union_uses.append('/'.join(path))
        for k,v in x.items(): locations(v,path+(str(k),))
    elif isinstance(x,list):
        for i,v in enumerate(x): locations(v,path+(str(i),))
locations(schema)
test('external union occurs only StandardLine source and achievement guard',set(union_uses)=={'$defs/StandardLine/properties/sourceVersionRef','$defs/StandardLine/allOf/0/then/properties/sourceVersionRef'},union_uses)
test('non-achievement exact typed internal source',schema['$defs']['StandardLine']['allOf'][0]['else']['properties']['sourceVersionRef']=={'$ref':'#/$defs/IndicatorVersionRef'})

# Pairwise equality with cross-multiplication, not hash bucketing from round 1.
def same_vector(a,b):
    return len(a)==len(b) and all(Fraction(x).numerator*Fraction(y).denominator == Fraction(y).numerator*Fraction(x).denominator for x,y in zip(a,b))
def classes(rows,who):
    unassigned=list(range(len(rows))); answer=[]
    while unassigned:
        first=unassigned.pop(0)
        if not any(Fraction(x) for x in rows[first]['coefficients']):continue
        equal=[i for i in unassigned if same_vector(rows[first]['coefficients'],rows[i]['coefficients'])]
        unassigned=[i for i in unassigned if i not in equal]
        persons={rows[i][who] for i in [first]+equal}
        answer.append(dict(size=len(persons),members=sorted(persons),signature=rows[first]['coefficients']))
    return answer
anon_rows=[]
for c in reversed(doc('Anonymity_Cases.json')['cases']):
    groups=classes(c['rows'],'reviewer')
    subject=classes(c.get('subjectRows',[]),'subject')
    values=[]
    for column in zip(*[r['coefficients'] for r in c['rows']]):
        values.append(str(sum(Fraction(coef)*Fraction(row['value']) for coef,row in zip(column,c['rows']))))
    if c.get('namedMode'):
        eligible=c['namedMode']=='unique_manager' and c.get('noticeNamed') and c.get('uniqueManager')
    else:
        eligible=bool(groups) and all(g['size']>=c['k'] for g in groups)
    if c.get('organization'):
        subjects={r['subject'] for r in c['rows']}
        bottom=[len({r['reviewer'] for r in c['rows'] if r['subject']==s and any(Fraction(x) for x in r['coefficients'])}) for s in subjects]
        eligible &= all(g['size']>=3 for g in subject) and all(n>=c['k'] for n in bottom)
        test('organization recomputed lower threshold '+c['id'],sorted(bottom)==sorted(c['bottomAnonymousCounts']) and sorted(g['size'] for g in subject)==c['expectedSubjectClassSizes'])
    eligible &= c.get('partitionValid',True)
    result='publish' if eligible else 'suppress'
    test('reverse privacy '+c['id'],result==c['expected'] and sorted(g['size'] for g in groups)==c['expectedClassSizes'] and values==c['expectedValues'])
    anon_rows.append(dict(id=c['id'],actual=result,classes=groups,columnValues=values))
test('reverse privacy 5/11',Counter(x['actual'] for x in anon_rows)=={'publish':5,'suppress':11})
duplicate=[dict(reviewer='A',coefficients=['1/3']) for i in range(3)]
test('three atoms of one person never count as three people',classes(duplicate,'reviewer')[0]['size']==1)
manual={x['id']:x for x in anon_rows}
test('manual ABC first size3', [g['size'] for g in manual['ANON-01']['classes']]==[3])
test('manual old/new A separately singleton',[g['size'] for g in manual['ANON-03']['classes']]==[1,1,2] and 3*(Fraction(manual['ANON-03']['columnValues'][1])-Fraction(manual['ANON-03']['columnValues'][0]))==3)
test('manual triple111 singleton',next(g for g in manual['ANON-05B']['classes'] if all(Fraction(x)>0 for x in g['signature']))['size']==1)

# Independent DFS graph from P3 work packages (not Task_Dependencies task rows).
pack=doc('P3_Work_Packages.json')['tasks']; deps=doc('Task_Dependencies.json')
edges=[]
for t in pack:
    d=t['dependencies']
    edges.extend((t['id'],s) for s in d['r2CompletionPredecessors'])
    edges.extend((t['id'],'R1-CAP-'+s) for s in d['requiredR1CapabilityGates'])
    edges.extend((t['id'],s) for s in d['externalProducerDependencies'])
edges.extend(('R3-PRODUCERS-READY',p) for p in deps['externalProducerSlots'])
edges.extend((deps['jointClosure']['id'],p) for p in deps['jointClosure']['completionPredecessors'])
edges.extend([('P3-R1-10-COMPLETE',deps['jointClosure']['id']),('P3-R1-11-EXIT','P3-R1-10-COMPLETE')])
nodes=set(sum(([a,b] for a,b in edges),[])); active=set(); finished=set(); cycles=[]
def visit(n):
    if n in active:cycles.append(n);return
    if n in finished:return
    active.add(n)
    for a,b in edges:
        if a==n:visit(b)
    active.remove(n);finished.add(n)
for n in sorted(nodes):visit(n)
test('independent DFS 55/165/0',len(nodes)==55 and len(edges)==len(set(edges))==165 and not cycles)
test('no R2 task waits on R1-10 complete',[a for a,b in edges if a.startswith('P3-R2-') and b in ['P3-R1-10-COMPLETE','P3-R1-11-EXIT']]==[])
for key,slot in deps['r1CapabilitySlots'].items():
    test('owner freeze closed '+key,slot['status']=='pending_owner_freeze' and not slot['capabilityOpen'] and slot['implementationCommitSha'] is None and not slot['independentEvidenceRefs'])

# Reverse repaired assertions, LIMIT inputs and immutable scope/states.
scenarios=doc('Acceptance_Scenarios.json')['scenarios']; scenario_by={s['id']:s for s in scenarios}
for a in trace['specs']:
    for m in a.get('targetedRepairMappings',[]):
        test('repair source->probe->scenario '+a['id']+'/'+m['group'],bool(m['exampleIds']) and all(i in {c['id'] for c in examples['cases']} for i in m['exampleIds']) and all(s in scenario_by for s in m['scenarioIds']))
for sid,a in doc('Foundation_Adaptations.json')['adaptations'].items():
    s=scenario_by[sid]
    test('adaptation fieldwise direct binding '+sid,all(a[k]==s[k] for k in a) and s['originalFoundationGwt']=={k:original_acs[sid.removeprefix('R2-P3-')][k] for k in ['given','when','then','basis']})
    test('adaptation decidable steps roles fields versions '+sid,all(a.get(k) for k in ['fixture','actions','actors','allowedFields','forbiddenFields','expectedVersions','given','when','then']) and a['adaptationReview']=='P2_desktop_only_not_business_execution')
limits=doc('Limit_Resolution.json')['items']
lookup={x['id']:x['actual'] for x in schema_rows+anon_rows}
for l in limits:
    if 'repairProof' not in l:continue
    proof=l['repairProof']; evidence=doc(proof['evidencePath']); bs=raw(C,D+proof['evidencePath'])
    test('LIMIT reverse hash/probes '+l['id'],hashlib.sha256(bs).hexdigest()==proof['evidenceSha256'] and all(hashlib.sha256(raw(C,D+n)).hexdigest()==h for n,h in evidence['inputSha256'].items()) and all(next(r for r in evidence['results'] if r['id']==p)['actual']==lookup[p] for p in proof['documentProbeIds']))
    test('LIMIT later responsibilities '+l['id'],{x['disposition'] for x in limits if x['parentLimitId']==l['parentLimitId']}=={'P2_design_closed','P3_validation','P4_acceptance'})
test('138 not executed / 46 not started',len(scenarios)==138 and all(s['executionStatus']=='not_run' for s in scenarios) and len(pack)==46 and all(t['status']=='proposed_not_started' for t in pack))
test('52 exclusive 15/25/12',Counter(l['disposition'] for l in limits)=={'P2_design_closed':15,'P3_validation':25,'P4_acceptance':12})
test('7 source requests stay request_only',len(doc('Source_Requests.json')['requests'])==7 and all(s['status']=='request_only_not_sent_or_executed' for s in doc('Source_Requests.json')['requests']))

# Regress all original 56 gate references. Retained findings history is not rewritten.
gates=json.loads(raw(R,'docs/delivery/r2-p2-exit-review/Critical_Gates.json'))['gates']
gate_rows=[]
for g in gates:
    refs_ok=True
    for ref in g['designRefs']:
        name,_,anchor=ref.partition('#')
        text=raw(C,D+name).decode()
        refs_ok &= not anchor or f'id="{anchor}"' in text or '# '+anchor in text
    test('original gate source/scenario still present '+g['id'],refs_ok and set(g['scenarioIds'])<=set(scenario_by))
    gate_rows.append(dict(id=g['id'],gate=g['gate'],originalStatus=g['status'],originalFindings=g['findingIds'],designRefs=g['designRefs'],scenarioIds=g['scenarioIds'],referenceIntegrity=bool(refs_ok)))
for name in ['Architecture.md','Migration_Rollback.md','Recovery_Cost_Responsibilities.md','Original_Limits.json','Approval_Provenance.json','Legacy_Acceptance_Map.json']:
    test('untouched accepted boundary '+name,raw(C,D+name)==raw(OLD,D+name))
for entry in doc('Controller_Proposal.json',P)['fixedDesignReferences']:
    test('reverse fixed proposal '+entry['path'],entry['gitRef']==C and hashlib.sha256(raw(C,entry['path'])).hexdigest()==entry['sha256'])
for ref in [C,P]:
    for entry in doc('Artifact_Manifest.json',ref)['artifacts']:
        bs=raw(ref,entry['path'])
        test('reverse own-HEAD manifest '+ref+'/'+entry['path'],len(bs)==entry['bytes'] and hashlib.sha256(bs).hexdigest()==entry['sha256'])
proposal=doc('Controller_Proposal.json',P)
test('unproved target and no phase authority',not proposal['p2ExitApproved'] and not proposal['p3Entered'] and proposal['recoveryTargets']=={'rpoMinutes':60,'rtoMinutes':240,'retentionDays':30,'runtimeProvenThisRun':False})
summary=dict(checkCount=len(checks),failed=sum(not c['passed'] for c in checks),schema=Counter(r['actual'] for r in schema_rows),anonymity=Counter(r['actual'] for r in anon_rows),nodes=len(nodes),edges=len(edges),cycles=len(cycles),originalGates=len(gate_rows))
out=dict(kind='second_independent_P2_document_review_no_round1_imports_no_product_execution',designContentHead=C,packagingHead=P,summary=summary,checks=checks,schemaResults=schema_rows,anonymityResults=anon_rows,graphEdges=edges,originalGateRegression=gate_rows)
if '--record' in argparse.ArgumentParser().parse_known_args()[1]:
    (OUT/'Recheck_Round2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary))
for c in checks:
    if not c['passed']:print(json.dumps(c,ensure_ascii=False))
raise SystemExit(bool(summary['failed']))
