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
 for(const who of ['owner','reviewer'])for(const op of ['catalog','identityReview','person','employment','assignmentRequest','assignmentApprove','assignmentExecute','exitRequest','exitApprove','exitExecute','contract','contractSign','contractEnd','template','subsetImport']){
  sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(tenant,who+op,who,'M01',op,'scope','["A","B"]','["record","name","email","skill"]','current',past,null);
 }
 sqlite.exec('UPDATE r1_schema_state SET features_enabled=1');
 function seed(id,kind,orgId,personId,payload,status='active',code=null){sqlite.prepare('INSERT INTO r1_m01_entities VALUES (?,?,?,?,?,?,?,?,?)').run(tenant,id,kind,personId,orgId,code,1,status,JSON.stringify(payload));}
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
 await assert.rejects(f.send(c),/范围/);f.sqlite.prepare("UPDATE r1_m01_entities SET payload=json_set(payload,'$.attributes.orgIds',json('[\"A\"]')) WHERE id='legal'").run();
 f.seed('old-contract','contract','A','person',{legalEntityId:'legal',start:'2025-01-01',end:'2025-12-30'},'signed','C1');
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
 f.sqlite.prepare("UPDATE r1_m01_entities SET payload=json_set(payload,'$.validTo','2025-12-31') WHERE id='position-a'").run();
 await assert.rejects(f.send({operation:'catalog',id:'position-a',kind:'position',code:'PA',name:'岗位',orgId:'A',parentId:'',status:'inactive',validFrom:today,validTo:null,attributes:{}}),e=>e.message==='存在受保护的未完成依赖，请联系负责人');f.sqlite.close();
});
