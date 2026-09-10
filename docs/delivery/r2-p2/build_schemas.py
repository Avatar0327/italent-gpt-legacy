"""Strict documentation schemas and action bindings. Never installs API routes."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
def obj(p,required=None):return {'type':'object','properties':p,'required':list(p) if required is None else required,'additionalProperties':False}
def ref(n):return {'$ref':'#/$defs/'+n}
def arr(n,minimum=0):return {'type':'array','items':ref(n),'minItems':minimum}
def enum(*v):return {'type':'string','enum':list(v)}
def text(mx=200,mn=1):return {'type':'string','minLength':mn,'maxLength':mx}
def nullable(v):return {'anyOf':[v,{'type':'null'}]}
defs={
'Id':text(200),'Uuid':{'type':'string','format':'uuid'},'Revision':{'type':'integer','minimum':0,'maximum':9007199254740991},
'PositiveInteger':{'type':'integer','minimum':1,'maximum':9007199254740991},'Digest':{'type':'string','pattern':'^[a-f0-9]{64}$'},
'Date':{'type':'string','format':'date','pattern':'^\\d{4}-\\d{2}-\\d{2}$'},'Instant':{'type':'string','format':'date-time','pattern':'Z$'},
'Decimal':{'type':'string','pattern':'^(?:0|-?(?:[1-9][0-9]*(?:\\.[0-9]*[1-9])?|0\\.[0-9]*[1-9]))$'},'Boolean':{'type':'boolean'},
'Name':text(200),'Description':text(4000,0),'Reason':text(3000,5),'Purpose':text(100),
}
defs['VersionRef']=obj({'producer':text(40),'objectType':text(80),'rootId':ref('Id'),'versionId':ref('Id'),'sourceRevision':ref('Revision'),'digest':ref('Digest'),'capturedAt':ref('Instant'),'purpose':ref('Purpose')})
defs['ObjectRef']=obj({'module':enum('M37','M06','M26','M18','M17','M03'),'objectType':text(80),'rootId':nullable(ref('Id')),'versionId':ref('Id')},['module','objectType','rootId'])
defs['Scope']=obj({'orgIds':arr('Id'),'includeDescendants':ref('Boolean'),'personIds':arr('Id'),'positionIds':arr('Id')})
defs['Scale']=obj({'kind':enum('numeric','ordinal','boolean','enum'),'min':ref('Decimal'),'max':ref('Decimal'),'step':ref('Decimal'),'unit':text(40),'direction':enum('higher','lower'),'levelIds':arr('Id'),'mappingVersionRef':ref('VersionRef')},['kind'])
defs['Target']={'oneOf':[
 obj({'kind':{'const':'numeric'},'scaleVersionRef':ref('VersionRef'),'comparator':enum('eq','gte','lte','gt','lt'),'value':ref('Decimal')}),
 obj({'kind':{'const':'ordinal'},'schemeVersionRef':ref('VersionRef'),'targetLevelId':ref('Id'),'passLevelIds':arr('Id',1)}),
 obj({'kind':{'const':'boolean'},'value':ref('Boolean')}),
 obj({'kind':{'const':'enum'},'optionId':ref('Id'),'definitionVersionRef':ref('VersionRef')}),
 obj({'kind':{'const':'none'}})]}
defs['Cell']=obj({'state':enum('value','null','not_configured','unavailable','suppressed'),'value':{'type':['string','number','boolean','null']},'reasonCode':text(100),'unit':text(40),'scaleVersionRef':ref('VersionRef')},['state','value','reasonCode'])
defs['Cell']['allOf']=[{'if':{'properties':{'state':{'enum':['null','not_configured','unavailable','suppressed']}}},'then':{'properties':{'value':{'type':'null'}}}}]
defs['RuleNode']=obj({'nodeId':ref('Id'),'op':enum('AND','OR','eq','gte','lte','gt','lt','in'),'children':arr('Id'),'lineId':ref('Id'),'target':ref('Target')},['nodeId','op'])
defs['RuleAst']=obj({'ruleRootId':ref('Id'),'versionId':ref('Id'),'rootNodeId':ref('Id'),'nodes':arr('RuleNode',1)})
defs['Material']=obj({'objectVersionRef':ref('VersionRef'),'classification':enum('ordinary','sensitive','restricted'),'contributorPersonIds':arr('Id'),'attachmentVersionRefs':arr('VersionRef')})
defs['Committee']=obj({'mode':enum('all','threshold','consensus','vote','total_score','indicator_score'),'reviewerPersonIds':arr('Id',1),'recusalVersionRefs':arr('VersionRef'),'minEligible':ref('PositiveInteger'),'quorum':ref('PositiveInteger'),'threshold':ref('Decimal'),'denominatorPolicyVersionRef':ref('VersionRef'),'hardVetoRuleVersionRef':ref('VersionRef')},['mode','reviewerPersonIds','recusalVersionRefs','minEligible','quorum'])
defs['ApprovalAction']=obj({'applicationVersionId':ref('Id'),'nodeVersionId':ref('Id'),'decision':enum('approve','reject','abstain'),'reason':ref('Reason')})
defs['SubmitAction']=obj({'businessVersionId':ref('Id'),'workflowTemplateVersionRef':ref('VersionRef'),'materialManifest':arr('Material')})
defs['PublishAction']=obj({'businessVersionId':ref('Id'),'approvalDecisionRef':ref('VersionRef'),'basePublishedVersionId':nullable(ref('Id')),'audiencePolicyVersionRef':ref('VersionRef'),'manifestDigest':ref('Digest')})
defs['ReasonAction']=obj({'businessVersionId':ref('Id'),'reason':ref('Reason'),'approvalRef':ref('VersionRef')},['businessVersionId','reason'])
defs['AvailabilityAction']=obj({'businessVersionId':ref('Id'),'target':enum('active','disabled'),'reason':ref('Reason')})
defs['LibraryDraft']=obj({'name':ref('Name'),'type':enum('ability','potential','experience'),'description':text(500,0),'classificationId':nullable(ref('Id'))})
defs['IndicatorChild']=obj({'childId':nullable(ref('Id')),'subset':enum('level','behavior','development_suggestion','interview_question'),'sort':ref('PositiveInteger'),'description':text(4000)})
defs['IndicatorChild']['allOf']=[{'if':{'properties':{'subset':{'const':'level'}}},'then':{'properties':{'description':text(500)}}}]
defs['IndicatorDraft']=obj({'libraryVersionRef':ref('VersionRef'),'code':ref('Name'),'name':ref('Name'),'definition':text(500,0),'aliases':arr('Name'),'children':arr('IndicatorChild')})
defs['StandardLine']=obj({'referenceLineId':nullable(ref('Id')),'dimension':enum('ability','potential','experience','achievement'),'sourceVersionRef':ref('VersionRef'),'target':ref('Target'),'weight':ref('Decimal'),'mandatory':ref('Boolean')})
defs['StandardDraft']=obj({'name':ref('Name'),'classificationId':nullable(ref('Id')),'modelLabel':text(200,0),'elementLabel':text(200,0),'lines':arr('StandardLine',1),'purposeRuleVersionRefs':arr('VersionRef')})
defs['CatalogDraft']=obj({'kind':enum('category_classification','category','hierarchy','qualification_level','indicator_type','indicator'),'code':ref('Name'),'name':ref('Name'),'parentId':nullable(ref('Id')),'sort':ref('PositiveInteger'),'targetKind':nullable(enum('job','position')),'targetId':nullable(ref('Id'))})
defs['QualificationLine']=obj({'lineId':nullable(ref('Id')),'levelId':ref('Id'),'indicatorVersionRef':ref('VersionRef'),'descriptionSnapshot':ref('Description'),'target':ref('Target'),'mandatory':ref('Boolean')})
defs['ValidityPolicy']=obj({'mode':enum('fixed_until','fixed_duration','long_term'),'untilOn':ref('Date'),'duration':ref('PositiveInteger'),'unit':enum('day','month','year'),'datePolicyVersionRef':ref('VersionRef')},['mode'])
defs['ValidityPolicy']={'oneOf':[obj({'mode':{'const':'fixed_until'},'untilOn':ref('Date')}),obj({'mode':{'const':'long_term'}}),obj({'mode':{'const':'fixed_duration'},'duration':ref('PositiveInteger'),'unit':enum('day','month','year'),'datePolicyVersionRef':ref('VersionRef')})]}
defs['QualificationDraft']=obj({'name':ref('Name'),'categoryVersionRef':ref('VersionRef'),'levelVersionRefs':arr('VersionRef',1),'lines':arr('QualificationLine',1),'entryPolicyVersionRef':ref('VersionRef'),'validityPolicy':ref('ValidityPolicy'),'evidenceWindowPolicyVersionRef':ref('VersionRef'),'ruleVersionRef':ref('VersionRef')})
defs['QualificationApplication']=obj({'personId':ref('Id'),'standardVersionRef':ref('VersionRef'),'targetLevelId':ref('Id'),'intent':enum('ordinary','renewal'),'previousCertificationId':nullable(ref('Id')),'materials':arr('Material'),'proxyAuthorityRef':ref('VersionRef')},['personId','standardVersionRef','targetLevelId','intent','previousCertificationId','materials'])
defs['QuestionOption']=obj({'optionId':ref('Id'),'label':ref('Name')})
defs['Question']=obj({'questionVersionRef':ref('VersionRef'),'type':enum('rating','single_choice','multiple_choice','text'),'title':ref('Name'),'required':ref('Boolean'),'allowSkip':ref('Boolean'),'allowNA':ref('Boolean'),'scaleVersionRef':ref('VersionRef'),'options':arr('QuestionOption'),'minSelected':ref('Revision'),'maxSelected':ref('PositiveInteger'),'maxLength':{'type':'integer','minimum':1,'maximum':3000},'conditionAst':ref('RuleAst')},['questionVersionRef','type','title','required','allowSkip','allowNA'])
defs['QuestionnaireDraft']=obj({'name':ref('Name'),'questions':arr('Question',1),'roleVersionRefs':arr('VersionRef',1),'standardVersionRefs':arr('VersionRef'),'aggregationPolicyVersionRef':ref('VersionRef')})
defs['FeedbackProject']=obj({'name':ref('Name'),'questionnaireVersionRef':ref('VersionRef'),'subjectPersonIds':arr('Id',1),'startAt':ref('Instant'),'endAt':ref('Instant'),'anonymousThreshold':{'type':'integer','minimum':3},'noticeVersionRef':ref('VersionRef'),'audiencePolicyVersionRef':ref('VersionRef')})
defs['Invite']=obj({'subjectId':ref('Id'),'reviewerPersonId':ref('Id'),'roleVersionRef':ref('VersionRef'),'noticeVersionRef':ref('VersionRef'),'replacesInviteId':nullable(ref('Id')),'reason':ref('Reason')})
defs['Answer']=obj({'questionVersionId':ref('Id'),'state':enum('answered','skipped','not_applicable','not_presented'),'numericValue':ref('Decimal'),'optionIds':arr('Id'),'textValue':text(3000,0),'reasonCode':text(100)},['questionVersionId','state'])
defs['ResponseSubmit']=obj({'inviteId':ref('Id'),'collectionVersionId':ref('Id'),'baseResponseVersionId':nullable(ref('Id')),'questionnaireVersionRef':ref('VersionRef'),'answers':arr('Answer',1)})
defs['ReportPublish']=obj({'reportVersionId':ref('Id'),'reviewDecisionRef':ref('VersionRef'),'sourceManifestDigest':ref('Digest'),'suppressionManifestDigest':ref('Digest'),'audiencePolicyVersionRef':ref('VersionRef'),'expectedDisclosureRevision':ref('Revision'),'purpose':ref('Purpose')})
defs['ReviewProject']=obj({'name':ref('Name'),'scenarioVersionRef':ref('VersionRef'),'categoryVersionRef':ref('VersionRef'),'year':{'type':'integer','minimum':1,'maximum':9999},'startOn':ref('Date'),'endOn':ref('Date'),'orgScope':ref('Scope'),'standardVersionRef':ref('VersionRef'),'toolContractVersionRef':ref('VersionRef'),'templateVersionRef':ref('VersionRef'),'workflowVersionRef':ref('VersionRef'),'schemeVersionRef':ref('VersionRef'),'saveStepId':ref('Id')})
defs['Axis']=obj({'kind':enum('performance','potential'),'sourceVersionRef':ref('VersionRef'),'scaleVersionRef':ref('VersionRef'),'mappingVersionRef':ref('VersionRef'),'lowCut':ref('Decimal'),'highCut':ref('Decimal'),'bandLabels':{'type':'array','items':ref('Name'),'minItems':3,'maxItems':3}})
defs['GridDefinition']=obj({'xAxis':ref('Axis'),'yAxis':ref('Axis'),'approvalRef':ref('VersionRef')})
defs['Calibration']=obj({'meetingVersionId':ref('Id'),'agendaId':ref('Id'),'subjectRecordId':ref('Id'),'basePublishedVersionId':ref('Id'),'dimension':text(40),'oldValue':ref('Cell'),'proposedValue':ref('Cell'),'materials':arr('Material'),'dissentRefs':arr('VersionRef'),'reason':ref('Reason')})
defs['PoolDraft']=obj({'name':ref('Name'),'categoryId':ref('Id'),'orgScope':ref('Scope'),'sharingPolicyVersionRef':ref('VersionRef'),'expectedCount':nullable(ref('PositiveInteger')),'entryRuleVersionRef':nullable(ref('VersionRef')),'exitRuleVersionRef':nullable(ref('VersionRef'))})
defs['PoolRule']=obj({'poolVersionRef':ref('VersionRef'),'ruleAst':ref('RuleAst'),'scope':ref('Scope'),'cadence':text(100),'timezone':text(100),'reviewOwnerPersonId':ref('Id'),'effectMode':enum('proposal_only','approved_auto_effect'),'approvalRef':ref('VersionRef')})
defs['Membership']=obj({'poolId':ref('Id'),'personId':ref('Id'),'previousMembershipId':nullable(ref('Id')),'stageVersionRef':ref('VersionRef'),'approvalOrRuleRunRef':ref('VersionRef'),'reason':ref('Reason')})
defs['Succession']=obj({'targetKind':enum('position','org'),'targetId':ref('Id'),'personId':ref('Id'),'startOn':ref('Date'),'endOn':nullable(ref('Date')),'readinessVersionRef':ref('VersionRef'),'assessmentAt':ref('Instant'),'nextReviewAt':ref('Instant'),'reviewerPersonId':ref('Id'),'eligibilityPolicyVersionRef':ref('VersionRef'),'materials':arr('Material')})
defs['Mentor']=obj({'personId':ref('Id'),'roleVersionRef':ref('VersionRef'),'mentorPersonIds':arr('Id',1),'responsibility':enum('coach','verify','coach_and_verify'),'completionMode':enum('all','any'),'relationshipVersionRefs':arr('VersionRef'),'reason':ref('Reason')})
defs['IdpTemplate']=obj({'name':ref('Name'),'orgId':ref('Id'),'categoryId':ref('Id'),'description':text(32766,0),'shareDownward':ref('Boolean'),'flowVersionRef':ref('VersionRef'),'requirementVersionRef':ref('VersionRef'),'availability':enum('active','disabled')})
defs['IdpPlan']=obj({'title':ref('Name'),'personId':ref('Id'),'templateVersionRef':ref('VersionRef'),'startOn':ref('Date'),'endOn':ref('Date'),'mentorAssignments':arr('Mentor',1)})
defs['IdpTaskAction']=obj({'planVersionId':ref('Id'),'stageId':ref('Id'),'taskId':ref('Id'),'submissionVersionId':nullable(ref('Id')),'materials':arr('Material'),'decision':enum('submit','verify','return','withdraw','waive','cancel'),'reason':ref('Reason')})
defs['TermDraft']=obj({'personId':ref('Id'),'cadreId':ref('Id'),'typeVersionRef':ref('VersionRef'),'orgVersionRef':ref('VersionRef'),'positionVersionRef':ref('VersionRef'),'startOn':ref('Date'),'endOn':nullable(ref('Date')),'openEnded':ref('Boolean'),'duration':ref('PositiveInteger'),'unit':enum('month','year'),'datePolicyVersionRef':ref('VersionRef'),'explicitOverrideReason':ref('Reason')},['personId','cadreId','typeVersionRef','orgVersionRef','positionVersionRef','startOn','endOn','openEnded','datePolicyVersionRef'])
defs['Nomination']=obj({'activityVersionRef':ref('VersionRef'),'personId':ref('Id'),'targetId':ref('Id'),'previousNominationId':nullable(ref('Id')),'materials':arr('Material'),'eligibilityVersionRefs':arr('VersionRef')})
defs['Appointment']=obj({'appointmentDecisionId':ref('Id'),'sourceEffectReceiptVersionRef':ref('VersionRef'),'term':ref('TermDraft'),'eligibilityVersionRefs':arr('VersionRef')})
defs['EvaluationDraft']=obj({'name':ref('Name'),'orgId':ref('Id'),'basicInfo':ref('Description'),'evaluationTitle':ref('Name'),'committee':ref('Committee'),'mode':enum('vote','total_score','indicator_score'),'itemTreeVersionRef':ref('VersionRef'),'aggregationVersionRef':ref('VersionRef'),'threshold':ref('Decimal'),'comparator':{'const':'gte'}})
defs['ObservationAction']=obj({'observationId':ref('Id'),'termId':ref('Id'),'evaluationVersionId':ref('Id'),'actionKind':enum('submit','withdraw','review','extend','terminate','early_application'),'newDueOn':ref('Date'),'policyVersionRef':ref('VersionRef'),'materials':arr('Material'),'reason':ref('Reason')},['observationId','termId','evaluationVersionId','actionKind','materials','reason'])
defs['InterviewDraft']=obj({'personId':ref('Id'),'interviewerPersonId':ref('Id'),'type':enum('任前访谈','见习前访谈','见习期访谈'),'role':enum('汇报上级','隔级上级','HRBP','下属员工','业务关联方'),'occurredOn':ref('Date'),'location':text(200,0),'content':text(200),'evidence':ref('Reason')})
defs['TermChange']=obj({'termVersionId':ref('Id'),'changeKind':enum('renewal','dismissal','retirement','employee_exit','void','correction'),'actualOn':ref('Date'),'reason':ref('Reason'),'approvalRef':ref('VersionRef'),'sourceEffectReceiptRef':ref('VersionRef'),'newTerm':ref('TermDraft')},['termVersionId','changeKind','actualOn','reason','approvalRef'])
defs['DateChange']=obj({'businessVersionId':ref('Id'),'newEndOn':ref('Date'),'reason':ref('Reason'),'approvalRef':ref('VersionRef'),'dependencyImpactManifestDigest':ref('Digest')})
defs['ReportQuery']=obj({'datasetId':ref('Id'),'definitionVersionId':ref('Id'),'timeMode':enum('current','snapshot'),'snapshotId':ref('Id'),'purpose':ref('Purpose'),'fieldIds':arr('Id'),'cursor':text(4000),'pageSize':{'type':'integer','minimum':1,'maximum':200}},['datasetId','definitionVersionId','timeMode','purpose','fieldIds','pageSize'])
commands=[]
def cmd(action,payload,mode,anchor):commands.append({'action':'r2.'+action,'module':action[:3].upper(),'payloadSchema':'#/$defs/'+payload,'operation':mode,'semanticDesignRef':anchor,'implementationStatus':'design_only'})
direct={
'm37':[('library.create','LibraryDraft','create'),('indicator.create','IndicatorDraft','create'),('standard.create','StandardDraft','create'),('standard.edit','StandardDraft','update')],
'm06':[('catalog.create','CatalogDraft','create'),('catalog.edit','CatalogDraft','update'),('standard.create','QualificationDraft','create'),('application.submit','QualificationApplication','create')],
'm26':[('questionnaire.create','QuestionnaireDraft','create'),('project.create','FeedbackProject','create'),('invite.revise','Invite','update'),('response.submit','ResponseSubmit','update'),('report.publish','ReportPublish','update')],
'm18':[('project.create','ReviewProject','create'),('project.save','ReviewProject','update'),('grid.save','GridDefinition','update'),('calibration.submit','Calibration','create')],
'm17':[('pool.create','PoolDraft','create'),('rule.publish','PoolRule','update'),('membership.apply','Membership','create'),('membership.reenter','Membership','create'),('succession.nominate','Succession','create'),('mentor.handoff','Mentor','update'),('template.create','IdpTemplate','create'),('idp.create','IdpPlan','create'),('idp.taskAction','IdpTaskAction','update')],
'm03':[('nomination.submit','Nomination','create'),('appointment.reconcile','Appointment','update'),('evaluation.create','EvaluationDraft','create'),('evaluation.save','EvaluationDraft','update'),('observation.action','ObservationAction','update'),('interview.create','InterviewDraft','create'),('interview.correct','InterviewDraft','update')]
}
for m,items in direct.items():
    for action,payload,mode in items:cmd(m+'.'+action,payload,mode,m.upper()+'_Design.md#engineering')
for m,root in [('m37','standard'),('m06','standard'),('m26','project'),('m18','result'),('m17','idp'),('m03','report')]:
    for action,payload in [('submit','SubmitAction'),('review','ApprovalAction'),('publish','PublishAction'),('withdraw','ReasonAction')]:
        if action=='publish' and m in ['m26','m17']:continue
        if any(x['action']=='r2.'+m+'.'+root+'.'+action for x in commands):continue
        cmd(m+'.'+root+'.'+action,payload,'update',m.upper()+'_Design.md#engineering')
for m,actions in {'m37':['availability.change'],'m06':['availability.change','certification.revoke'],'m26':['project.open','project.close','project.reopen','response.withdraw','report.withdraw'],'m18':['project.start','project.close','project.reopen','result.withdrawPublication'],'m17':['membership.exit','succession.close','idp.start','idp.extend','idp.pause','idp.resume','idp.terminate'],'m03':['term.change','interview.cancel']}.items():
    for action in actions:cmd(m+'.'+action,{'availability.change':'AvailabilityAction','term.change':'TermChange','idp.extend':'DateChange'}.get(action,'ReasonAction'),'update',m.upper()+'_Design.md#engineering')
base={'schemaVersion':{'const':1},'commandId':ref('Uuid'),'idempotencyKey':text(200),'action':enum(*[c['action'] for c in commands]),'objectRef':ref('ObjectRef'),'expectedWorkspaceRevision':ref('Revision'),'expectedEntityRevision':ref('Revision'),'expectedAuthorizationRevision':ref('Revision'),'writerEpoch':ref('Revision'),'recoveryEpoch':ref('Revision'),'payload':{'type':'object'}}
command=obj(base)
command['allOf']=[{'if':{'properties':{'action':{'const':c['action']}}},'then':{'properties':{'payload':ref(c['payloadSchema'].split('/')[-1]),'objectRef':{'properties':{'module':{'const':c['module']},'rootId':{'type':'null'} if c['operation']=='create' else ref('Id')}},**({'expectedEntityRevision':{'const':0}} if c['operation']=='create' else {})}}} for c in commands]
defs['Command']=command
defs['Event']=obj({'eventId':ref('Uuid'),'schemaVersion':{'const':1},'tenantId':ref('Id'),'producer':text(40),'eventType':text(100),'objectType':text(80),'rootId':ref('Id'),'versionId':ref('Id'),'entityRevision':ref('Revision'),'workspaceRevision':ref('Revision'),'sourceRevision':ref('Revision'),'occurredAt':ref('Instant'),'effectiveAt':nullable(ref('Instant')),'correlationId':ref('Id'),'causationId':ref('Id'),'digestAlgorithm':{'const':'sha256-canonical-json-v1'},'digest':ref('Digest'),'payload':obj({'sourceVersionRef':ref('VersionRef'),'rawStatus':text(80),'purpose':ref('Purpose'),'availability':enum('active','disabled','withdrawn'),'manifestDigest':ref('Digest')},['sourceVersionRef','rawStatus','purpose'])})
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:italent:r2:p2:interfaces:v1','$ref':'#/$defs/Command','$defs':defs,'description':'P2 design only. Semantic guards and current authorization mandatory; no running API claim.'}
(D/'Interface_Schemas.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n')
(D/'Command_Registry.json').write_text(json.dumps({'schemaVersion':1,'kind':'key_action_contracts_design_only','count':len(commands),'commands':commands,'querySchema':'#/$defs/ReportQuery','unregisteredActions':'P3 must register an equally strict payload before exposure; no generic arbitrary command passthrough'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'definitions':len(defs),'commandBindings':len(commands)}))
