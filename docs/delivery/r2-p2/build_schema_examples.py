"""Minimal document fixtures. Not API/product tests."""
import json,copy
from pathlib import Path
D=Path(__file__).resolve().parent
def vr(p='M37',o='indicator',r='I1',purpose='assessment'):
 return dict(kind='internal',producer=p,objectType=o,rootId=r,versionId=r+'-v1',sourceRevision=1,digest='a'*64,capturedAt='2026-09-10T00:00:00Z',purpose=purpose)
ext=dict(kind='external',sourceNamespace='synthetic-achievement',externalId='EXT1',objectType='achievement',externalVersion='capture1',asOf='2026-09-01T00:00:00Z',digest='b'*64,capturedAt='2026-09-10T00:00:00Z',purpose='assessment',trustContractVersionRef=vr('COMMON','trust_contract','TC1'))
child=dict(childId=None,childVersionId=None,indicatorVersionRef=None,subset='level',subsetName='能力等级',sort=1,description='一级说明',levelId=None,levelVersionRef=None,alias='L1',elementText='能完成基础任务')
cat=dict(kind='indicator_type',code='ABILITY',name='能力评分',parentId=None,sort=1,targetKind=None,targetId=None,isCommon=True,descriptionRows=[dict(rowId=None,sort=1,text='按能力证据评分')],evaluationMode='numeric',numericScale=dict(min='0',max='10',step='0.5',precision=1,unit='point',direction='higher'),ratingSelection=None)
question=dict(questionVersionRef=vr('M26','question','Q1'),type='rating',title='协作表现',required=True,allowSkip=False,allowNA=False,scaleVersionRef=vr('M37','scale','S1'),roleApplicability=dict(roleVersionRefs=[vr('M26','role_definition','PEER')],scope='listed_roles_only'),dimension=vr('M37','standard_dimension','DIM1'),indicatorVersionRefs=[vr()],visibility=dict(kind='always'))
questionnaire=dict(name='协作问卷',questions=[question],roleVersionRefs=[vr('M26','role_definition','PEER')],standardVersionRefs=[vr('M37','talent_standard','STD1')],aggregationPolicyVersionRef=vr('M26','aggregation_policy','AG1'))
prev=dict(kind='historical_result',resultVersionRef=vr('M18','published_result','RESULT1','historical_reference_only'),asOf='2026-08-01T00:00:00Z',selectedFieldIds=['potentialBand'],purpose='historical_reference_only',relationship='same_person_previous_project')
project=dict(name='年度盘点',scenarioVersionRef=vr('M18','scenario','SC1'),categoryVersionRef=vr('M18','category','CA1'),year=2026,startOn='2026-09-01',endOn='2026-09-30',orgScope=dict(orgIds=['ORG1'],includeDescendants=False,personIds=['E1'],positionIds=[]),standardVersionRef=vr('M37','talent_standard','STD1'),toolContractVersionRef=vr('M18','tool_contract','TOOL1'),templateVersionRef=vr('M18','template','T1'),workflowVersionRef=vr('M19','workflow','WF1'),schemeVersionRef=vr('M18','scheme','SCH1'),saveStepId='history',previousResultRef=prev)
cases=[]
def case(id,group,schema,value,expect,why,guard='references'):
 cases.append(dict(id=id,group=group,schema=schema,instance=value,expected=expect,expectedReason=why,semanticGuard=guard))
for id,group,schema,v,guard in [('REF-IN','VersionRef','VersionRef',vr(),'references'),('REF-EXT','VersionRef','VersionRef',ext,'references'),('LEVEL','IndicatorChild','IndicatorChild',child,'new_indicator'),('TYPE','CatalogDraft','CatalogDraft',cat,'catalog'),('QUESTION','QuestionnaireDraft','QuestionnaireDraft',questionnaire,'questionnaire'),('HISTORY','ReviewProject','ReviewProject',project,'history')]:
 case(id+'-VALID',group,schema,v,'accept','strict fields and exact fixture version',guard)
 bad=copy.deepcopy(v);bad['unapprovedField']='x';case(id+'-EXTRA',group,schema,bad,'reject','unknown field',guard)
 bad=copy.deepcopy(v)
 if group=='VersionRef':
  if id=='REF-IN': bad['versionId']='wrong-version'
  else: bad['externalVersion']='wrong-version'
 elif group=='IndicatorChild':bad['indicatorVersionRef']=vr();bad['indicatorVersionRef']['versionId']='wrong-version'
 elif group=='CatalogDraft':bad['evaluationMode']='rating';bad['numericScale']=None;bad['ratingSelection']=dict(ratingSchemeVersionRef=vr('M06','rating_scheme','RS1'),levelIds=['qualification-level-not-rating'])
 elif group=='QuestionnaireDraft':bad['questions'][0]['dimension']['versionId']='wrong-version'
 else:bad['previousResultRef']['resultVersionRef']['versionId']='wrong-version'
 case(id+'-VERSION',group,schema,bad,'reject','wrong version or scheme membership',guard)
 bad=copy.deepcopy(v)
 if group=='VersionRef':
  if id=='REF-IN':bad['producer']='M03'
  else:bad['sourceNamespace']='untrusted-source'
 elif group=='IndicatorChild':bad['indicatorVersionRef']=vr('M06','indicator','I1')
 elif group=='CatalogDraft':bad['evaluationMode']='rating';bad['numericScale']=None;bad['ratingSelection']=dict(ratingSchemeVersionRef=vr('M06','qualification_level','QL1'),levelIds=['L1'])
 elif group=='QuestionnaireDraft':bad['questions'][0]['roleApplicability']['roleVersionRefs']=[vr('M26','role_definition','MANAGER')]
 else:bad['previousResultRef']['resultVersionRef']['producer']='M26'
 case(id+'-SOURCE',group,schema,bad,'reject','wrong source/type/role membership',guard)
# Representative approved optional modes and explicit absence remain valid.
rating=copy.deepcopy(cat);rating.update(evaluationMode='rating',numericScale=None,ratingSelection=dict(ratingSchemeVersionRef=vr('M06','rating_scheme','RS1'),levelIds=['RL1']))
case('TYPE-RATING-VALID','CatalogDraft','CatalogDraft',rating,'accept','rating scheme distinct from qualification level','catalog')
none=copy.deepcopy(project);none['previousResultRef']=None;case('HISTORY-NONE-VALID','ReviewProject','ReviewProject',none,'accept','explicit no prior result','history')
no_kind=vr();del no_kind['kind'];case('REF-NO-KIND','VersionRef','VersionRef',no_kind,'reject','never infer source')
refs=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('kind')=='internal' and 'versionId' in x and x not in refs:refs.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for c in cases:
 if c['expected']=='accept':walk(c['instance'])
fixture=dict(internalVersions=refs,externalCaptures=[ext],ratingSchemeLevels={'RS1-v1':['RL1']},dimensionMembers={'DIM1-v1':dict(standardVersionId='STD1-v1',indicatorVersionIds=['I1-v1'])},historicalResults={'RESULT1-v1':dict(projectRootId='OLD-PROJECT',periodEnd='2026-07-01',publishedAt='2026-07-31T00:00:00Z',personIds=['E1'])},currentProjectRootId='NEW-PROJECT',serverNow='2026-09-10T00:00:00Z')
(D/'Schema_Examples.json').write_text(json.dumps(dict(kind='P2_document_fixtures_not_product_execution',fixture=fixture,cases=cases),ensure_ascii=False,indent=2)+'\n')
