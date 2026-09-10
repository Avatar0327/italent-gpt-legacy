"""R2-EXIT-001 strict contract repair; design generator, no product imports."""
def apply(defs, obj, ref, arr, enum, text, nullable):
    # Existing domain references are internal unless explicitly permitted below.
    def internalize(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k=='$ref' and x=='#/$defs/VersionRef': v[k]='#/$defs/InternalVersionRef'
                else: internalize(x)
        elif isinstance(v,list):
            for x in v: internalize(x)
    internalize(defs)
    original=defs.pop('VersionRef')
    original['properties']['kind']={'const':'internal'};original['required'].append('kind')
    defs['InternalVersionRef']=original
    defs['ExternalVersionRef']=obj({'kind':{'const':'external'},'sourceNamespace':text(100),'externalId':ref('Id'),'objectType':text(80),'externalVersion':text(200),'asOf':ref('Instant'),'digest':ref('Digest'),'capturedAt':ref('Instant'),'purpose':ref('Purpose'),'trustContractVersionRef':ref('InternalVersionRef')})
    defs['VersionRef']={'oneOf':[ref('InternalVersionRef'),ref('ExternalVersionRef')]}
    def typed(producer,kind):
        return {'allOf':[ref('InternalVersionRef'),{'properties':{'producer':{'const':producer},'objectType':{'const':kind}}}]}
    defs['IndicatorVersionRef']=typed('M37','indicator')
    defs['LevelVersionRef']=typed('M37','indicator_level')
    defs['DimensionVersionRef']=typed('M37','standard_dimension')
    defs['RoleVersionRef']=typed('M26','role_definition')
    defs['IndicatorChild']=obj({'childId':nullable(ref('Id')),'childVersionId':nullable(ref('Id')),'indicatorVersionRef':nullable(ref('IndicatorVersionRef')),'subset':enum('level','behavior','development_suggestion','interview_question'),'subsetName':ref('Name'),'sort':ref('PositiveInteger'),'description':text(4000),'levelId':nullable(ref('Id')),'levelVersionRef':nullable(ref('LevelVersionRef')),'alias':text(200,0),'elementText':text(500,0)})
    defs['IndicatorChild']['allOf']=[{'if':{'properties':{'subset':{'const':'level'}}},'then':{'properties':{'description':text(500),'levelVersionRef':{'type':'null'}}},'else':{'properties':{'alias':{'const':''},'elementText':{'const':''}}}}]
    defs['StandardLine']['properties']['sourceVersionRef']=ref('VersionRef')
    defs['StandardLine']['allOf']=[{'if':{'properties':{'dimension':{'const':'achievement'}}},'then':{'properties':{'sourceVersionRef':ref('VersionRef')}},'else':{'properties':{'sourceVersionRef':ref('IndicatorVersionRef')}}}]
    defs['DescriptionRow']=obj({'rowId':nullable(ref('Id')),'sort':ref('PositiveInteger'),'text':ref('Description')})
    defs['NumericScaleConfig']=obj({'min':ref('Decimal'),'max':ref('Decimal'),'step':ref('Decimal'),'precision':{'type':'integer','minimum':0,'maximum':18},'unit':text(40),'direction':enum('higher','lower')})
    defs['RatingSelection']=obj({'ratingSchemeVersionRef':typed('M06','rating_scheme'),'levelIds':arr('Id',1)})
    catalog=defs['CatalogDraft']; catalog['properties'].update({'isCommon':ref('Boolean'),'descriptionRows':arr('DescriptionRow'),'evaluationMode':enum('numeric','rating','not_configured'),'numericScale':nullable(ref('NumericScaleConfig')),'ratingSelection':nullable(ref('RatingSelection')),'indicatorTypeVersionRef':typed('M06','indicator_type'),'qualificationLevelVersionRef':typed('M06','qualification_level')})
    config=['isCommon','descriptionRows','evaluationMode','numericScale','ratingSelection']
    catalog['allOf']=[{'if':{'properties':{'kind':{'const':'indicator_type'}}},'then':{'required':config},'else':{'not':{'anyOf':[{'required':[x]} for x in config]}}}, {'if':{'properties':{'kind':{'const':'indicator'}}},'then':{'required':['indicatorTypeVersionRef']},'else':{'not':{'required':['indicatorTypeVersionRef']}}}]
    for mode in ['numeric','rating','not_configured']:
        catalog['allOf'].append({'if':{'required':['evaluationMode'],'properties':{'evaluationMode':{'const':mode}}},'then':{'properties':{'numericScale':ref('NumericScaleConfig') if mode=='numeric' else {'type':'null'},'ratingSelection':ref('RatingSelection') if mode=='rating' else {'type':'null'}}}})
    defs['QuestionApplicability']=obj({'roleVersionRefs':{'type':'array','items':ref('RoleVersionRef'),'minItems':1,'uniqueItems':True},'scope':{'const':'listed_roles_only'}})
    defs['QuestionVisibility']={'oneOf':[obj({'kind':{'const':'always'}}),obj({'kind':{'const':'conditional'},'conditionAst':ref('RuleAst'),'dependsOnQuestionVersionIds':arr('Id',1)})]}
    question=defs['Question']; question['properties'].update({'roleApplicability':ref('QuestionApplicability'),'dimension':ref('DimensionVersionRef'),'indicatorVersionRefs':{'type':'array','items':ref('IndicatorVersionRef'),'minItems':1,'uniqueItems':True},'visibility':ref('QuestionVisibility')});question['required']+=['roleApplicability','dimension','indicatorVersionRefs','visibility']
    # Legacy conditionAst retained; if present it must equal visibility.conditionAst, never guessed.
    defs['QuestionnaireDraft']['properties']['roleVersionRefs']={'type':'array','items':ref('RoleVersionRef'),'minItems':1,'uniqueItems':True}
    defs['PreviousResultRef']=obj({'kind':{'const':'historical_result'},'resultVersionRef':typed('M18','published_result'),'asOf':ref('Instant'),'selectedFieldIds':{'type':'array','items':enum('ability','potential','experience','achievement','performanceBand','potentialBand','gridCell','publishedAt'),'minItems':1,'uniqueItems':True},'purpose':{'const':'historical_reference_only'},'relationship':{'const':'same_person_previous_project'}})
    defs['ReviewProject']['properties']['previousResultRef']=nullable(ref('PreviousResultRef'));defs['ReviewProject']['required'].append('previousResultRef')

def bind(commands):
    for c in commands:
        c['referencePolicy']={'defaultKind':'internal','externalAllowedPaths':['payload.lines[].sourceVersionRef (dimension=achievement only)'] if c['action'] in ['r2.m37.standard.create','r2.m37.standard.edit'] else [],'guard':'Interfaces.md#repair-001','missingKind':'reject; never infer'}
        if c['payloadSchema'].split('/')[-1] in ['IndicatorDraft','CatalogDraft','QuestionnaireDraft','ReviewProject','StandardDraft']:
            c['repairFindingRefs']=['R2-EXIT-001']
            c['semanticGuardRef']='Contract_Repair.md'
