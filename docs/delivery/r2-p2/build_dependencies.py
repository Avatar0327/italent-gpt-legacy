"""Adopt fixed independent review DAG; freeze slots remain unfilled, never moving R1 HEAD."""
import json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
H='bd976480fad9822ee52ecb4b00a080360772b0f3';path='docs/delivery/r2-p2-exit-review/P3_Sequencing_Recommendations.json';raw=subprocess.check_output(['git','show',H+':'+path]);review=json.loads(raw)
capabilities={}
semantics={
'A':['trusted identity/person binding and exitFence','current complete row/action/field grant; deny wins','tenant CAS + entity/auth revision + atomic audit/receipt/outbox/recovery journal','M19 transaction-plan adapter, independent review','immutable owner-version attachment binding + current download authorization','source event schema, digest/signature verification and inbox dedupe'],
'B':['M48 producer authorized projection and current source fallback','M32 exact source snapshot/current fields; no anonymous recomputation','bounded job lease/fence/cursor and atomic ready manifest','download revoke and no stale sensitive bytes; subscription capability conditional'],
'C':['migration source mapping/cursor and conflict quarantine','writer cutover epoch and read-only/forward repair rollback','full transaction journal + attachment manifest + independent deny/key continuity','common recovery point; RPO<=60min RTO<=240min retention30d; owner open gate']}
for k,g in review['gates'].items():
 capabilities[k]=dict(title=g['title'],r1TaskIds=g['r1TaskIds'],status='pending_owner_freeze',implementationCommitSha=None,p2ContractSource='e15237281ff19f04f08a354fd9455c518b24ae47',schemaVersion=None,adapterVersion=None,securityEpochContractVersion=None,writerEpochContractVersion=None,recoveryEpochContractVersion=None,migrationVersion=None,independentEvidenceRefs=[],rollbackCommitSha=None,capabilityOpen=False,requiredSemantics=semantics[k],releaseCondition='所有者填写完整实现SHA及全部版本槽位，独立证据覆盖requiredSemantics，批准能力开放/回退范围；P2设计来源不替代实现基线')
module_schemas={
'M37':[['LibraryDraft','IndicatorDraft','IndicatorChild'],['StandardDraft','Target','RuleAst'],['SubmitAction','PublishAction','AvailabilityAction'],['Scope','Material'],['VersionRef','StandardLine','Event']],
'M06':[['CatalogDraft','NumericScaleConfig','RatingSelection'],['QualificationDraft','QualificationLine','Target'],['PublishAction','AvailabilityAction'],['QualificationApplication','Committee','ValidityPolicy'],['VersionRef','Event']],
'M26':[['FeedbackProject','Invite'],['DisclosureAtom','DisclosureCell','DisclosureLedgerEntry'],['QuestionnaireDraft','Question','QuestionApplicability'],['ResponseSubmit','ReportPublish'],['ReportQuery','Event']],
'M18':[['ReviewProject','PreviousResultRef'],['Axis','GridDefinition','Cell'],['Calibration','Committee'],['PublishAction','ReviewProject'],['PreviousResultRef','ReportQuery','Event']],
'M17':[['PoolDraft','PoolRule','Membership'],['Succession','ValidityPolicy'],['Mentor'],['IdpTemplate','IdpPlan','IdpTaskAction'],['ReportQuery','Cell'],['Scope','Event']],
'M03':[['TermDraft'],['Appointment','TermChange'],['EvaluationDraft','Committee'],['ObservationAction','DateChange'],['InterviewDraft','Material'],['VersionRef','Event']]}
other={'BASE-01':['Invite','Mentor'],'BASE-02':['Scope','ReportQuery'],'BASE-03':['CatalogDraft','ReasonAction','Event'],'BASE-04':['Material','VersionRef'],'BASE-05':['DisclosureLedgerEntry','Event'],'BASE-06':['Event','Command'],'COM-01':['Command','Event'],'COM-02':['VersionRef','Command','Event'],'COM-03':['VersionRef','DisclosureLedgerEntry'],'COM-04':['DisclosureLedgerEntry','Event'],'X-01':['StandardLine','PreviousResultRef'],'X-02':['ValidityPolicy','Appointment'],'X-03':['ReportPublish','DisclosureLedgerEntry'],'X-04':['ReportQuery','IdpTaskAction']}
domain_algorithms={'M37-01':'目录/子集字段及唯一性','M37-02':'尺度/精确权重/规则AST','M06-01':'目录树/指标类型/编号','M06-02':'矩阵/评级/证据窗口','M06-04':'委员会分母/有效期/续期','M26-01':'邀请唯一/角色适用','M26-02':'固定匿名矩阵/谱系/分区','M26-03':'四题型及条件DAG','M18-01':'范围及历史关系校验','M18-02':'轴映射/等值/null','M17-01':'池规则/区间/重入','M17-02':'准备度/任期','M17-03':'动态职责及回避校验','M17-04':'IDP阶段任务DAG','M17-05':'健康分母/去重','M03-01':'日期/闰年/区间','M03-03':'精确评分/缺评/弃权','M03-04':'考察日期','M03-05':'述职/敏感档案字段','COM-02':'严格schema及事件格式守卫'}
tasks=[]
for r in review['tasks']:
 id=r['taskId'];short=id.removeprefix('P3-R2-');m=short[:3];names=module_schemas[m][int(short[-2:])-1] if m in module_schemas else other[short]
 gates=r['requiredR1CapabilityGates'];adapters=[]
 if 'A' in gates:adapters+=['A.current_grant','A.command_transaction_receipt','A.identity_exitFence']
 if m in module_schemas:adapters+=[m+'.domain_adapter']
 if short in ['M37-03','M06-03','M06-04','M26-04','M18-03','M18-04','M17-03','M17-04','M03-02','M03-03','M03-04']:adapters+=['A.M19_transaction_plan']
 if short in ['M03-01','M03-02','M03-04','X-02']:adapters+=['A.M01_actual_assignment_receipt']
 if short in ['BASE-04','M03-05','M26-04']:adapters+=['A.attachment_owner_binding_download']
 if 'B' in gates:adapters+=['B.M32_snapshot_field_projection','B.M48_authorized_projection','B.export_download_lease']
 if 'C' in gates:adapters+=['C.migration_quarantine_writer_fence','C.restore_current_deny_disclosure_ledger']
 ext=[]
 if short in ['M17-04','M17-06','X-04']:ext+=['R3-M27-learning-evidence']
 if short in ['M18-01','M18-02','M18-05','X-01']:ext+=['R3-M16-performance-source']
 tasks.append(dict(taskId=id,r2CompletionPredecessors=r['recommendedR2CompletionPredecessors'],requiredR1CapabilityGates=gates,baselineSlots=['R1-'+g for g in gates],requiredSchemas=['Interface_Schemas.json#/$defs/'+n for n in names],requiredAdapters=adapters,requiredSecurityContract=['current authorization revision and deny','writer/recovery epoch and exitFence'] if 'A' in gates else ['current deny and writer/recovery epoch inherited via C'],requiredMigrationOrRecovery='C: conflict quarantine, full journal/object manifests, independent deny/disclosure continuity' if 'C' in gates else 'A/B changes must already participate in full journal; C needed before migration/recovery closure',independentSlice=domain_algorithms.get(short),independentStartCondition='另获所有者P2退出/P3准入；纯函数使用冻结P2文档和合成输入，可在A/B/C未就绪时实施但不能关闭整任务' if short in domain_algorithms else '无独立完成路径；按前置任务及共享能力实施适配',completionCondition='全部R2完成前置+对应R1槽位冻结并有独立证据+本任务实际领域适配与原场景证据；仅桩或文档不能结项',externalProducerDependencies=ext,externalProducerStatus='pending_release_owner_freeze' if ext else 'not_applicable',missingDependencyBehavior='blocked_dependency；未配置反例可验证，不能当真实消费已成功',status='proposed_not_started'))
joint=dict(id='JOINT-R1-10-R2-R3',completionPredecessors=['P3-R2-X-01','P3-R2-X-02','P3-R2-X-03','P3-R2-X-04','R3-PRODUCERS-READY','R1-CAP-A','R1-CAP-B','R1-CAP-C'],rule='R1-10接口就绪由A/B能力交付；真实R2/R3生产者分别先实现再联合取证。R2 X完成不依赖R1-10整任务通过，R1-10整体验收消费联合证据。R1-11退出在联合门禁之后且仍满足自身所有要求。',status='not_authorized_not_started',ownerRole='R1集成负责人+R2/R3生产者负责人+独立复核，所有者放行')
out=dict(kind='proposed_dependency_graph_not_execution',reviewSource=dict(gitRef=H,path=path,sha256=hashlib.sha256(raw).hexdigest()),r1CapabilitySlots=capabilities,tasks=tasks,jointClosure=joint,externalProducerSlots={x:dict(status='pending_release_owner_freeze',implementationCommitSha=None,schemaVersion=None,evidenceRefs=[]) for x in ['R3-M27-learning-evidence','R3-M16-performance-source']})
(D/'Task_Dependencies.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
lines=['# 46项P3任务依赖与能力冻结槽位','','本文件只作设计交接；当前P3未授权、全部任务未开始。A/B/C全部pending_owner_freeze，implementationCommitSha及版本字段为空，绝不能把移动中R1 HEAD填作可用基线。P2契约来源e15237281ff19f04f08a354fd9455c518b24ae47仅设计依据。','','A对应R1-01/02/03/04，B对应05/06/07，C对应08/09；每槽位包含schema/adapter/security/writer/recovery/migration版本、独立证据和回退SHA。所需字段必须在放行前填齐。B的托管后台能力未验证则订阅保持关闭；C仍需60/240/30实证。','','|任务|R2完成前置|R1能力|可独立的纯领域部分（另须准入）|','|---|---|---|---|']
for t in tasks:lines.append('|'+t['taskId']+'|'+(', '.join(t['r2CompletionPredecessors']) or '无整项前置')+'|'+','.join(t['requiredR1CapabilityGates'])+'|'+(t['independentSlice'] or '共享稳定后完成适配')+'|')
lines+=['','每任务精确schema、adapter、安全epoch和迁移恢复条件见Task_Dependencies.json。上表为完成前置，不能把模型供给依赖倒置成全部任务串行等待。M37-05等五域消费收口后置。','','联合收口：'+joint['rule'],'','R3-M16/M27槽位同样待各自所有者冻结；不进入其工作树，也不以历史/桩替代实际生产者。缺失来源只能关闭明确not_configured行为的局部断言，整任务仍blocked_dependency。']
(D/'Task_Dependencies.md').write_text('\n'.join(lines)+'\n')
