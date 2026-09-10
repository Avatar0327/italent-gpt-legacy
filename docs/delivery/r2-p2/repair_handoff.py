"""Deterministic targeted overlays; retains source GWT and all original IDs."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
def apply(t,tasks,scenarios):
 mapping={
 'VersionRef':(['M37-SPEC-05'],['R2-X-02'],'StandardDraft','r2.m37.standard.create'),
 'IndicatorChild':(['M37-SPEC-01'],['R2-P3-M37-REVIEW-AC01','R2-P3-M37-REVIEW-AC02'],'IndicatorDraft','r2.m37.indicator.create'),
 'CatalogDraft':(['M06-SPEC-01','M06-SPEC-02'],['R2-P3-M06-REVIEW-AC01','R2-P3-M06-REVIEW-AC03'],'CatalogDraft','r2.m06.catalog.create'),
 'QuestionnaireDraft':(['M26-SPEC-01','M26-SPEC-03'],['R2-P3-M26-REVIEW-AC06','R2-P3-M26-REVIEW-AC07'],'QuestionnaireDraft','r2.m26.questionnaire.create'),
 'ReviewProject':(['M18-SPEC-01','M18-SPEC-05'],['R2-P3-M18-REVIEW-AC01','R2-P3-M18-REVIEW-AC04'],'ReviewProject','r2.m18.project.create')}
 examples=json.loads((D/'Schema_Examples.json').read_text())
 for group,(specs,acs,schema,command) in mapping.items():
  link={'findingId':'R2-EXIT-001','group':group,'schemaRef':'Interface_Schemas.json#/$defs/'+schema,'command':command,'designRef':'Contract_Repair.md','exampleIds':[x['id'] for x in examples['cases'] if x['group']==group],'scenarioIds':acs}
  for item in t['specs']+t['clauses']:
   if item.get('id') in specs or item.get('parentId') in specs:item.setdefault('targetedRepairMappings',[]).append(link)
  for item in t['contractDetails']:
   if (group=='IndicatorChild' and item['id']=='BP-C-REQ-07/fieldDetails/2') or (group=='CatalogDraft' and item['id']=='BP-C-REQ-02/fieldDetails/1'):item['targetedRepairMappings']=[link];item['scenarioIds']=acs
  for s in scenarios:
   if s['id'] in acs:
    s.setdefault('targetedRepairAssertions',[]).append(dict(group=group,command=command,fixtureRef='Schema_Examples.json',given='采用该group全部合成fixture及精确版本manifest；manage有权角色H，独立复核R与发布P，无真人',when='逐一提交合法输入；再单独注入各反例的非法字段、版本、来源/角色关系',then='合法字段逐字段回读一致，新版本绑定准确；反例必须拒绝且无业务版本/发布/receipt applied副作用；正例仍需原审批，不因schema通过自动发布',exampleIds=link['exampleIds']))
 if (D/'Foundation_Adaptations.json').exists():
  adaptations=json.loads((D/'Foundation_Adaptations.json').read_text())['adaptations']
  for s in scenarios:
   if s['id'] in adaptations:
    src=next(a['source'] for a in t['acceptanceIds'] if 'R2-P3-'+a['id']==s['id']);s['originalFoundationGwt']={k:src[k] for k in ['given','when','then','basis']};s.update(adaptations[s['id']])
 if (D/'Task_Dependencies.json').exists():
  deps=json.loads((D/'Task_Dependencies.json').read_text());by={x['taskId']:x for x in deps['tasks']}
  for task in tasks:task['dependencies']=by[task['id']]
 if (D/'Anonymity_Cases.json').exists():
  for s in scenarios:
   if s['id'] in ['R2-P3-M26-REVIEW-AC04','R2-M26-S01','R2-M26-S02','R2-M26-S07']:
    s['anonymityOracleRef']='Anonymity_Cases.json';s['normativeAlgorithmRef']='Anonymity_Repair.md';s['targetedPrivacyAssertions']='逐格核coefficient向量、不同protectedReviewer数、subject数及历史账本；首报ABC允许，AB/单人改答/成员变化/三重交叠/线性组合/撤回重发/分区错均按表拒绝，不能以全抑制满足正例。'
