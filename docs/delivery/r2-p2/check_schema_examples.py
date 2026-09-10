"""Full Draft202012 schema validation + explicit synthetic reference oracles; no product calls."""
import json,copy
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
D=Path(__file__).resolve().parent
S=json.loads((D/'Interface_Schemas.json').read_text());E=json.loads((D/'Schema_Examples.json').read_text());F=E['fixture']
Draft202012Validator.check_schema(S)
def guards(x,mode):
 errors=[]
 def walk(v):
  if isinstance(v,dict):
   if v.get('kind')=='internal' and 'versionId' in v and v not in F['internalVersions']:errors.append('SOURCE_VERSION_OR_TYPE_MISMATCH')
   if v.get('kind')=='external' and v not in F['externalCaptures']:errors.append('EXTERNAL_CAPTURE_UNTRUSTED')
   for y in v.values():walk(y)
  elif isinstance(v,list):
   for y in v:walk(y)
 walk(x)
 if mode=='new_indicator' and any(x.get(k) is not None for k in ['childId','childVersionId','indicatorVersionRef','levelId','levelVersionRef']):errors.append('CREATE_PARENT_OR_ID_CONFLICT')
 if mode=='catalog' and x.get('evaluationMode')=='rating':
  r=x['ratingSelection'];allowed=F['ratingSchemeLevels'].get(r['ratingSchemeVersionRef']['versionId'],[])
  if not set(r['levelIds'])<=set(allowed):errors.append('RATING_LEVEL_VERSION_MISMATCH')
 if mode=='questionnaire':
  roles=x['roleVersionRefs'];std={r['versionId'] for r in x['standardVersionRefs']}
  for q in x['questions']:
   if any(r not in roles for r in q['roleApplicability']['roleVersionRefs']):errors.append('QUESTION_ROLE_NOT_IN_QUESTIONNAIRE')
   dim=F['dimensionMembers'].get(q['dimension']['versionId'],{})
   if dim.get('standardVersionId') not in std or not {r['versionId'] for r in q['indicatorVersionRefs']}<=set(dim.get('indicatorVersionIds',[])):errors.append('DIMENSION_INDICATOR_VERSION_MISMATCH')
 if mode=='history' and x.get('previousResultRef'):
  p=x['previousResultRef'];h=F['historicalResults'].get(p['resultVersionRef']['versionId'])
  if not h or h['projectRootId']==F['currentProjectRootId'] or h['periodEnd']>x['startOn'] or not h['publishedAt']<=p['asOf']<=F['serverNow']:errors.append('HISTORY_UNVERIFIABLE')
 return errors
results=[]
for c in E['cases']:
 schema={'$schema':S['$schema'],'$defs':S['$defs'],'$ref':'#/$defs/'+c['schema']}
 errs=[e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(c['instance'])]
 semantic=[] if errs else guards(c['instance'],c['semanticGuard'])
 actual='reject' if errs or semantic else 'accept'
 results.append(dict(id=c['id'],group=c['group'],expected=c['expected'],actual=actual,schemaErrors=errs,semanticErrors=semantic,pass_=actual==c['expected']))
assert all(r['pass_'] for r in results),[r for r in results if not r['pass_']]
out=dict(kind='P2_document_schema_and_fixture_checks_not_P3',validator='jsonschema 4.23.0 / Draft202012Validator + FormatChecker',metaSchemaValid=True,count=len(results),accepted=sum(r['actual']=='accept' for r in results),rejected=sum(r['actual']=='reject' for r in results),results=results)
(D/'evidence/repair-001-schema.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k!='results'})
