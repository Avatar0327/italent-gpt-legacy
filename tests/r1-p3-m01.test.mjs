import {database,act,request} from './support/runtime.mjs';
import {readdirSync,readFileSync} from 'node:fs';
import test from 'node:test';
import assert from 'node:assert/strict';
const {executeM01,m01Entity,tenure}=await import('../lib/hris/r1-m01.ts');
const {memberContext}=await import('../lib/hris/context.ts');
const {businessDate}=await import('../lib/hris/business-time.ts');
const access=await import('../app/api/access/route.ts');
const today=businessDate(),past='2020-01-01';
async function fixture(){
 const {sqlite,db}=database();for(const f of readdirSync('drizzle').filter(f=>f.endsWith('.sql')).sort())sqlite.exec(readFileSync('drizzle/'+f,'utf8'));
 globalThis.p2env.DB=db;act('owner');assert.equal((await access.POST(request('/api/access',{action:'setup',name:'M01隔离合成企业'}))).status,200);
 const c=await memberContext(),tenant=c.member.tenantId;
 // Fixture setup precedes tested commands; never use an existing/production DB.
 sqlite.exec('DROP TRIGGER r1_guard_hris_orgs_insert; DROP TRIGGER r1_guard_hris_memberships_insert');
 sqlite.prepare("INSERT INTO hris_orgs(tenant_id,id,name,city,leader,status) VALUES (?,'A','合成A','上海','','启用'),(?,'B','合成B','上海','','启用')").run(tenant,tenant);
 sqlite.prepare("INSERT INTO hris_memberships(user_id,tenant_id,role,org_scope,view_email,view_level,active) VALUES ('reviewer',?,'hr','[\"A\",\"B\"]',1,1,1)").run(tenant);
 for(const who of ['owner','reviewer'])for(const op of ['catalog','identityReview','identityBind','contractField','person','employment','assignmentRequest','assignmentApprove','assignmentExecute','exitRequest','exitApprove','exitExecute','exitCleanup','contract','contractSign','contractEnd','template','subsetImport']){
  sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(tenant,who+op,who,'M01',op,'scope','["A","B"]','["record","name","email","skill"]','current',past,null);
 }
 sqlite.exec('UPDATE r1_schema_state SET features_enabled=1');
 function seed(id,kind,orgId,personId,payload,status='active',code=null){sqlite.prepare('INSERT INTO r1_m01_entities VALUES (?,?,?,?,?,?,?,?,?)').run(tenant,id,kind,personId,orgId,code,1,status,JSON.stringify(payload));sqlite.prepare('INSERT INTO r1_m01_versions VALUES (?,?,?,?,?,?,?,?,?,?)').run(tenant,id,1,0,'fixture',new Date().toISOString(),payload.validFrom??null,payload.validTo??null,'known',JSON.stringify({id,kind,personId,orgId,code,revision:1,status,payload}));}
 seed('A','org','A',null,{name:'合成A',parentId:'',validFrom:past,validTo:null,attributes:{}},'active','A');seed('B','org','B',null,{name:'合成B',parentId:'',validFrom:past,validTo:null,attributes:{}},'active','B');
 seed('position-a','position','A',null,{name:'岗位',orgId:'A',validFrom:past,validTo:null,attributes:{}},'active','PA');seed('position-b','position','B',null,{name:'岗位',orgId:'B',validFrom:past,validTo:null,attributes:{}},'active','PB');
 seed('person','person','A',null,{name:'合成人员'},'active','E1');seed('review','identity_review','A','person',{},'confirmed');
 const send=async(payload,key=crypto.randomUUID())=>{const ctx=await memberContext(),s=ctx.member.securityStamp;return executeM01(ctx,{commandId:key,idempotencyKey:key,action:'M01.'+payload.operation,payload,expectedWorkspaceRevision:ctx.row.revision,expectedAuthorizationRevision:s.authorizationRevision,expectedWriterEpoch:s.writerEpoch,expectedRecoveryEpoch:s.recoveryEpoch});};
 return {sqlite,db,tenant,send,seed};
}
test('P3-M01-01: same org overlapping position name rejects, cross org permits, future cycles reject',async()=>{
 const f=await fixture(),base={operation:'catalog',kind:'position',code:'P2',name:'岗位',orgId:'A',parentId:'',status:'active',validFrom:today,validTo:null,attributes:{}};
 await assert.rejects(f.send(base),/名称冲突/);await f.send({...base,orgId:'B',name:'另一岗位'});
 f.seed('future-b','org','A',null,{name:'未来乙旧版',parentId:'',validFrom:past,validTo:'2026-12-31',attributes:{}},'active','FB');
 f.seed('future-a','org','A',null,{name:'未来甲',parentId:'future-b',validFrom:'2027-01-01',validTo:null,attributes:{}},'active','FA');
 await assert.rejects(f.send({operation:'catalog',id:'future-b',kind:'org',code:'FB',name:'未来乙',orgId:'A',parentId:'future-a',status:'active',validFrom:'2027-01-01',validTo:null,attributes:{}}),/环/);f.sqlite.close();
});
test('P3-M01-02: identity conflicts do not merge; stable rehire and tenure exclude gaps/internship',async()=>{
 const f=await fixture();await assert.rejects(f.send({operation:'identityReview',personId:'person',candidateIds:['person','other'],reason:'核验身份',evidenceRef:'synthetic-evidence'}),/冲突/);
 f.seed('ended','employment','A','person',{startOn:'2020-02-28',lastWorkingOn:'2020-03-01'},'ended');
 const r=await f.send({operation:'employment',personId:'person',orgId:'A',identityReviewId:'review',predecessorId:'ended',startOn:today,employmentType:'retired_rehire'});
 const e=await m01Entity(f.db,f.tenant,r.result.ids[0]);assert.equal(e.personId,'person');assert.equal(e.payload.accountRestored,false);
 assert.equal(tenure([{startOn:'2020-02-28',lastWorkingOn:'2020-03-01',status:'ended',employmentType:'employee'},{startOn:'2020-02-29',lastWorkingOn:'2020-03-01',status:'ended',employmentType:'employee'},{startOn:'2021-01-01',lastWorkingOn:'2021-01-10',status:'ended',employmentType:'internship'}],today).days,3);f.sqlite.close();
});
test('P3-M01-03: independent HR approves part time; it consumes zero additional headcount',async()=>{
 const f=await fixture();f.seed('employment','employment','A','person',{startOn:past},'active');f.seed('primary','assignment','A','person',{type:'primary',positionId:'position-a',validFrom:past,validTo:null,occupancy:1});
 let r=await f.send({operation:'assignmentRequest',personId:'person',employmentId:'employment',orgId:'B',positionId:'position-b',type:'part_time',homePrimaryId:'primary',validFrom:today,validTo:null,reviewerId:'reviewer',reason:'合成兼职申请'});const id=r.result.ids[0];
 await assert.rejects(f.send({operation:'assignmentApprove',id}),/审核角色/);act('reviewer');await f.send({operation:'assignmentApprove',id});act('owner');r=await f.send({operation:'assignmentExecute',id});
 assert.equal((await m01Entity(f.db,f.tenant,r.result.assignmentId)).payload.occupancy,0);assert.equal((await m01Entity(f.db,f.tenant,'primary')).payload.occupancy,1);f.sqlite.close();
});
test('P3-M01-07: legal scope, same legal ID and adjacent renewal dates; immutable versions',async()=>{
 const f=await fixture();f.seed('legal','legal_entity','A',null,{name:'法人旧名',validFrom:past,validTo:null,attributes:{orgIds:[]}},'active','LE');
 const c={operation:'contract',personId:'person',orgId:'A',legalEntityId:'legal',number:'C2',agreementCategory:'labor',contractType:'fixed',start:'2026-01-01',end:'2026-12-31',renewalOf:null,fields:{}};
 await assert.rejects(f.send(c),/范围/);f.seed('legal-scoped','legal_entity','A',null,{name:'法人旧名',validFrom:past,validTo:null,attributes:{orgIds:['A']}},'active','LE-S');c.legalEntityId='legal-scoped';
 f.seed('old-contract','contract','A','person',{legalEntityId:'legal-scoped',start:'2025-01-01',end:'2025-12-30'},'signed','C1');
 await assert.rejects(f.send({...c,renewalOf:'old-contract'}),/相邻日/);
 const r=await f.send({...c,start:'2025-12-31',renewalOf:'old-contract'});assert.equal((await m01Entity(f.db,f.tenant,r.result.ids[0])).payload.legalName,'法人旧名');
 assert.throws(()=>f.sqlite.exec('UPDATE r1_m01_versions SET payload=\'{}\''),/IMMUTABLE_HISTORY/);f.sqlite.close();
});
test('P3-M01-08: subset row key is idempotent across transport command IDs and explicit null survives',async()=>{
 const f=await fixture();const t=await f.send({operation:'template',orgId:'A',kind:'skill',entryType:'subset',fields:[{code:'skill',type:'text',required:false,default:'未配置',uniqueKey:false,readActions:['read'],writeActions:['update']}]});
 const p={operation:'subsetImport',personId:'person',orgId:'A',templateId:t.result.ids[0],templateVersion:1,batchId:'batch',rowNo:1,attemptVersion:1,mode:'create',recordId:null,fields:{skill:null}};
 const a=await f.send(p),b=await f.send(p);assert.deepEqual(a.result.ids,b.result.ids);assert.equal((await m01Entity(f.db,f.tenant,a.result.ids[0])).payload.fields.skill,null);f.sqlite.close();
});
test('P3-M01-09: missing or wrong entry template blocks person creation and never activates accounts',async()=>{
 const f=await fixture();const t=await f.send({operation:'template',orgId:'A',kind:'custom',entryType:'prehire',fields:[{code:'email',type:'text',required:true,default:null,uniqueKey:false,readActions:['read'],writeActions:['update']}]});
 const p={operation:'person',code:'P-new',name:'合成待入职',orgId:'A',templateId:t.result.ids[0],entryType:'prehire',fields:{}};await assert.rejects(f.send(p),/必填/);
 const before=f.sqlite.prepare('SELECT count(*) n FROM hris_memberships').get().n;const r=await f.send({...p,fields:{email:'fixture@example.invalid'}});assert.equal((await m01Entity(f.db,f.tenant,r.result.ids[0])).payload.invite,false);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM hris_memberships').get().n,before);f.sqlite.close();
});
test('P3-M01-10: exit fence rejects later approvals and queues all 101 cleanup items',async()=>{
 const f=await fixture();f.seed('employment','employment','A','person',{startOn:past},'active');f.seed('exit','exit_request','A','person',{lastWorkingOn:'2026-01-01',reviewerId:'reviewer'},'approved');
 for(let i=0;i<101;i++)f.seed('work-'+i,'assignment_request','A','person',{reviewerId:'reviewer',createdBy:'owner'},'pending');
 await f.send({operation:'exitExecute',id:'exit'});assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_exit_cleanup').get().n,101);
 act('reviewer');await assert.rejects(f.send({operation:'assignmentApprove',id:'work-1'}),/退出/);f.sqlite.close();
});
test('P3-M01-12: protected waiting dependency blocks disable without exposing identity',async()=>{
 const f=await fixture();f.seed('waiting','assignment_request','A','person',{positionId:'position-a'},'approved');
 // Non-overlapping next version exercises dependency rather than an interval conflict.
 
 await assert.rejects(f.send({operation:'catalog',id:'position-a',closePreviousVersion:1,kind:'position',code:'PA',name:'岗位',orgId:'A',parentId:'',status:'inactive',validFrom:today,validTo:null,attributes:{}}),e=>e.message==='存在受保护的未完成依赖，请联系负责人');f.sqlite.close();
});
test('P3-M01-11: explicit strong budget policy blocks effect; absent provider never reports budget passed',async()=>{
 const f=await fixture();f.seed('employment','employment','A','person',{startOn:past},'active');
 f.seed('request','assignment_request','A','person',{personId:'person',employmentId:'employment',orgId:'A',positionId:'position-a',type:'primary',validFrom:today,validTo:null,attempts:0},'approved');
 f.seed('budget','budget_policy','A',null,{strongBlocking:true});
 const r=await f.send({operation:'assignmentExecute',id:'request'});assert.equal(r.result.effectStatus,'failed');assert.match((await m01Entity(f.db,f.tenant,'request')).payload.failure,/金额预算/);
 assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_m01_entities WHERE kind='assignment'").get().n,0);f.sqlite.close();
});
test('temporal versions: future publication preserves today and old bytes, all interval cuts reject historical hidden cycles',async()=>{
 const f=await fixture();const {catalogTimeline,temporalCatalogCheck}=await import('../lib/hris/r1-temporal.ts');
 const before=f.sqlite.prepare("SELECT payload FROM r1_m01_versions WHERE entity_id='position-a'").get().payload;
 await f.send({operation:'catalog',id:'position-a',closePreviousVersion:1,kind:'position',code:'PA',name:'岗位未来名',orgId:'A',parentId:'',status:'active',validFrom:'2027-01-01',validTo:null,attributes:{}});
 const timeline=await catalogTimeline(f.db,f.tenant,'position');assert.equal(timeline.find(v=>v.id==='position-a'&&v.payload.validFrom<=today).payload.name,'岗位');
 assert.equal(f.sqlite.prepare("SELECT payload FROM r1_m01_versions WHERE entity_id='position-a' AND version=1").get().payload,before);
 const node=(id,parent,from,to)=>({id,kind:'org',personId:null,orgId:'A',code:id,revision:1,status:'active',payload:{name:id,parentId:parent,validFrom:from,validTo:to}});
 assert.throws(()=>temporalCatalogCheck([node('x','y','2027-01-01','2027-03-31'),node('x','','2027-04-01',null),node('y','x','2027-01-01','2027-02-01'),node('y','','2027-02-02',null)],'org'),/时态环/);f.sqlite.close();
});
test('exit generation: rehire enables only new segment; cleanup resumes and unsupported domains retain blocked receipts',async()=>{
 const f=await fixture();f.seed('old-employment','employment','A','person',{startOn:past},'active');f.seed('exit','exit_request','A','person',{lastWorkingOn:'2026-01-01'},'approved');
 for(let i=0;i<101;i++)f.seed('todo-'+String(i).padStart(3,'0'),i===100?'unsupported':'assignment_request','A','person',{employmentId:'old-employment',reviewerId:'reviewer',createdBy:'owner'},'pending');
 await f.send({operation:'exitExecute',id:'exit'});
 const e=await f.send({operation:'employment',personId:'person',orgId:'A',identityReviewId:'review',predecessorId:'old-employment',startOn:today,employmentType:'employee'});
 const payload={operation:'assignmentRequest',personId:'person',employmentId:e.result.ids[0],orgId:'A',positionId:'position-a',type:'primary',homePrimaryId:null,validFrom:today,validTo:null,reviewerId:'reviewer',reason:'已复核重聘'};
 await assert.rejects(f.send({...payload,employmentId:'old-employment'}),/代次/);
 const r=await f.send(payload);act('reviewer');await f.send({operation:'assignmentApprove',id:r.result.ids[0]});await assert.rejects(f.send({operation:'assignmentApprove',id:'todo-001'}),/代次/);act('owner');await f.send({operation:'assignmentExecute',id:r.result.ids[0]});
 for(let i=0;i<6;i++)await f.send({operation:'exitCleanup',personId:'person',orgId:'A',limit:20});
 assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_exit_cleanup WHERE status='cancelled'").get().n,100);
 assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_exit_cleanup WHERE status='blocked_by_exit'").get().n,1);
 assert.equal((await m01Entity(f.db,f.tenant,r.result.ids[0])).status,'applied');
 assert.equal((await f.send({operation:'exitCleanup',personId:'person',orgId:'A',limit:20})).result.processed,0);f.sqlite.close();
});
test('command replay runs before stale business-state validation and does not create a second employment',async()=>{
 const f=await fixture(),c=await memberContext(),s=c.member.securityStamp,key=crypto.randomUUID(),payload={operation:'employment',personId:'person',orgId:'A',identityReviewId:'review',predecessorId:null,startOn:today,employmentType:'employee'};
 const intent={commandId:key,idempotencyKey:key,action:'M01.employment',payload,expectedWorkspaceRevision:c.row.revision,expectedAuthorizationRevision:s.authorizationRevision,expectedWriterEpoch:s.writerEpoch,expectedRecoveryEpoch:s.recoveryEpoch};
 const a=await executeM01(c,intent),b=await executeM01(await memberContext(),intent);assert.equal(b.replayed,true);assert.deepEqual(a.result.ids,b.result.ids);assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_m01_entities WHERE kind='employment'").get().n,1);f.sqlite.close();
});
test('server identity candidates: forged candidate list cannot hide a second identifier match; protected keys contain no raw values',async()=>{
 const f=await fixture();f.seed('other-person','person','B',null,{name:'另一合成人员'},'ended','E2');
 await f.send({operation:'identityBind',personId:'person',orgId:'A',identifiers:[{type:'document',value:'SYNTHETIC-DOC-A'},{type:'email',value:'shared@example.invalid'}],evidenceRef:'fixture-review-A'});
 await f.send({operation:'identityBind',personId:'other-person',orgId:'B',identifiers:[{type:'document',value:'SYNTHETIC-DOC-B'},{type:'email',value:'shared@example.invalid'}],evidenceRef:'fixture-review-B'});
 await assert.rejects(f.send({operation:'identityReview',personId:'person',candidateIds:['person'],identifiers:[{type:'document',value:'SYNTHETIC-DOC-A'},{type:'document',value:'SYNTHETIC-DOC-B'}],reason:'隔离冲突核验',evidenceRef:'fixture-conflict'}),/身份复核/);
 await assert.rejects(f.send({operation:'identityReview',personId:'person',candidateIds:['person'],identifiers:[{type:'email',value:'shared@example.invalid'}],reason:'邮件只是线索',evidenceRef:'fixture-shared'}),/身份复核/);
 const r=await f.send({operation:'identityReview',personId:'person',candidateIds:['person'],identifiers:[{type:'document',value:'SYNTHETIC-DOC-A'}],reason:'独立核验证件',evidenceRef:'fixture-confirm'});assert.equal((await m01Entity(f.db,f.tenant,r.result.ids[0])).status,'confirmed');
 assert.ok(!JSON.stringify(f.sqlite.prepare('SELECT * FROM r1_identity_keys').all()).includes('SYNTHETIC-DOC'));assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_m01_entities WHERE kind='person'").get().n,2);f.sqlite.close();
});
test('contract field roots survive revisions and inheritance; explicit null clears; stable contract counts exclude unknown and cancelled',async()=>{
 const f=await fixture(),{contractCounts}=await import('../lib/hris/r1-personnel-data.ts');f.seed('legal','legal_entity','A',null,{name:'合成法人',validFrom:past,validTo:null,attributes:{orgIds:['A']}},'active','LE');
 const definition=await f.send({operation:'contractField',orgId:'A',code:'note',name:'合同说明',inheritPrevious:true,status:'active'}),field=definition.result.ids[0];
 for(const who of ['owner','reviewer'])f.sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(f.tenant,who+'contract-fields',who,'M01','contract','scope','["A"]',JSON.stringify([field]),'current',past,null);
 const base={operation:'contract',personId:'person',orgId:'A',legalEntityId:'legal',number:'C-01',agreementCategory:'labor',contractType:'fixed',start:'2026-01-01',end:'2026-12-31',renewalOf:null,fields:{[field]:'历史原值'}};
 const first=(await f.send(base)).result.ids[0];await f.send({operation:'contractSign',id:first,signedOn:today,evidence:'隔离人工登记'});
 const hash=f.sqlite.prepare('SELECT payload FROM r1_m01_versions WHERE entity_id=? ORDER BY version').all(first);
 await f.send({operation:'contractField',id:field,orgId:'A',code:'note',name:'合同说明新版',inheritPrevious:true,status:'active'});
 const second=(await f.send({...base,number:'C-02',start:'2027-01-01',end:'2027-12-31',renewalOf:first,fields:{}})).result.ids[0];let c=await m01Entity(f.db,f.tenant,second);assert.equal(c.payload.fieldSnapshots[0].value,'历史原值');assert.equal(c.payload.fieldSnapshots[0].sourceContractId,first);assert.equal(c.payload.fieldSnapshots[0].sourceFieldVersion,1);assert.equal(c.payload.fieldSnapshots[0].version,2);
 await f.send({...base,id:second,number:'C-02',start:'2027-01-01',end:'2027-12-31',renewalOf:first,fields:{[field]:null}});c=await m01Entity(f.db,f.tenant,second);assert.equal(c.payload.fieldSnapshots[0].value,null);await f.send({operation:'contractSign',id:second,signedOn:today,evidence:'隔离登记第二份'});
 assert.deepEqual(f.sqlite.prepare('SELECT payload FROM r1_m01_versions WHERE entity_id=? ORDER BY version').all(first),hash);
 const a=await m01Entity(f.db,f.tenant,first),b=await m01Entity(f.db,f.tenant,second),count=contractCounts([a,b,{...b,revision:1},{...a,id:'cancelled',status:'cancelled'},{...a,id:'unknown',payload:{legalEntityId:'legal'}}]);assert.equal(count.groups[0].count,2);assert.deepEqual(count.unknownIds,['unknown']);assert.equal(count.automaticOpenEnded,false);assert.equal(count.automaticTermination,false);f.sqlite.close();
});
test('ten subset types plus custom preserve field versions, reject missing field permission and enforce exact decimal precision',async()=>{
 const f=await fixture();for(const kind of ['education','employment','family','appraisal','training','reward','certificate','project','skill','language','custom']){
  const t=(await f.send({operation:'template',orgId:'A',kind,entryType:'subset',fields:[{code:'skill',type:'number',unit:'小时',precision:2,required:false,default:null,uniqueKey:true,readActions:['read'],writeActions:['update']}]})).result.ids[0];
  const row={operation:'subsetImport',personId:'person',orgId:'A',templateId:t,templateVersion:1,batchId:'types-'+kind,rowNo:1,attemptVersion:1,mode:'create',recordId:null,fields:{skill:'1.25'}};
  const r=await f.send(row);await assert.rejects(f.send({...row,rowNo:2,fields:{skill:'1.256'}}),/精度/);await assert.rejects(f.send({...row,rowNo:3}),/唯一键/);
  await f.send({...row,rowNo:4,mode:'update',recordId:r.result.ids[0],fields:{skill:null}});assert.equal((await m01Entity(f.db,f.tenant,r.result.ids[0])).revision,2);
 }
 const t=(await f.send({operation:'template',orgId:'A',kind:'custom',entryType:'subset',fields:[{code:'protected',type:'text',required:false,default:null,uniqueKey:false,readActions:['read'],writeActions:['update']}]})).result.ids[0];
 await assert.rejects(f.send({operation:'subsetImport',personId:'person',orgId:'A',templateId:t,templateVersion:1,batchId:'denied',rowNo:1,attemptVersion:1,mode:'create',recordId:null,fields:{protected:'不得落库'}}),/字段权限/);f.sqlite.close();
});
test('M01 paged reads enforce field tuples and reject a cursor after permission revision changes',async()=>{
 const f=await fixture(),{readM01}=await import('../lib/hris/r1-m01-read.ts');
 f.seed('person-2','person','A',null,{name:'另一个合成人员',email:'hidden@example.invalid',fields:{email:'hidden@example.invalid',skill:'可见字段'}},'active','E2');
 f.sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(f.tenant,'read-only','owner','M01','read','scope','["A"]','["record","skill"]','current',past,null);
 const first=await readM01(await memberContext(),new URLSearchParams('kind=person&limit=1'));assert.equal(first.items.length,1);assert.ok(first.nextCursor);
 const second=await readM01(await memberContext(),new URLSearchParams({kind:'person',limit:'1',cursor:first.nextCursor}));assert.equal(second.items[0].payload.email,undefined);assert.equal(second.items[0].payload.fields.email,undefined);assert.equal(second.items[0].payload.fields.skill,'可见字段');
 f.sqlite.prepare("UPDATE r1_permission_grants SET fields='[]' WHERE id='read-only'").run();await assert.rejects(readM01(await memberContext(),new URLSearchParams({kind:'person',limit:'1',cursor:first.nextCursor})),/重新读取/);f.sqlite.close();
});
test('client unknown result retains exact command identity and resolves through the receipt without a second send',async()=>{
 const {clientIntent,sendClientCommand,queryClientCommand}=await import('../lib/hris/r1-client-command.ts');
 const intent=clientIntent({revision:7,securityStamp:{authorizationRevision:3,writerEpoch:1,recoveryEpoch:2,openGate:1,phase:'features_enabled',featuresEnabled:1}},'person',{operation:'person',code:'fixture'});let sends=0;
 const lost=await sendClientCommand(intent,async()=>{sends++;throw Error('synthetic lost response');});assert.equal(lost.state,'unknown');assert.equal(lost.commandId,intent.commandId);
 const found=await queryClientCommand(intent.commandId,async url=>{assert.ok(url.endsWith(intent.commandId));return Response.json({status:'committed',commandId:intent.commandId,result:'{}'});});assert.equal(found.state,'committed');assert.equal(sends,1);
});
