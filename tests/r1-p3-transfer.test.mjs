import test from 'node:test';
import assert from 'node:assert/strict';
import {setup,core,grant,hris,expect,act,request} from './support/foundation-scenario.mjs';
const {memberContext}=await import('../lib/hris/context.ts');
const route=await import('../app/api/r1/commands/route.ts');
const {businessDate}=await import('../lib/hris/business-time.ts');
async function fixture(t){
 const f=await setup();t.after(()=>f.sqlite.close());
 await core({action:'position',code:'R1-B',name:'合成B岗',orgId:f.otherOrg.id,family:'技术',responsibilities:'R1合成',status:'启用'});
 await core({action:'employee',...f.e,positionId:f.position.id});
 await grant('r1-hr','hr',null,[f.org.id,f.otherOrg.id]);await grant('r1-b','approver',null,[f.otherOrg.id]);
 await core({action:'workflow',kind:'transfer',steps:[{userId:'approver',name:'来源审核'},{userId:'r1-b',name:'目标审核'}]});
 const ctx=await memberContext(),tenant=ctx.member.tenantId;f.tenant=tenant;
 const state=JSON.parse(ctx.row.data);f.target=state.positions.find(p=>p.code==='R1-B');
 for(const who of ['owner','r1-hr','approver','r1-b'])for(const action of ['request','decide','withdraw','executeTransfer','cancelTransfer','workflow']){
  const scopes=who==='approver'?[f.org.id]:who==='r1-b'?[f.otherOrg.id]:[f.org.id,f.otherOrg.id];
  f.sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(tenant,who+action,who,'M01','transfer.'+action,'scope',JSON.stringify(scopes),'["record","level"]','current','2020-01-01',null);
 }
 const seed=(id,kind,orgId,personId,payload,status='active')=>f.sqlite.prepare('INSERT INTO r1_m01_entities VALUES (?,?,?,?,?,?,?,?,?)').run(tenant,id,kind,personId,orgId,null,1,status,JSON.stringify(payload));f.seed=seed;
 for(const o of state.orgs)seed(o.id,'org',o.id,null,{name:o.name,parentId:o.parentId,validFrom:'2020-01-01',validTo:null,attributes:{}});
 for(const p of state.positions)seed(p.id,'position',p.orgId,null,{name:p.name,orgId:p.orgId,validFrom:'2020-01-01',validTo:null,attributes:{}});
 seed('r1-person','person',f.org.id,null,{});seed('segment','employment',f.org.id,f.e.id,{startOn:'2026-01-01'});
 seed('primary','assignment',f.org.id,f.e.id,{type:'primary',employmentId:'segment',positionId:f.position.id,validFrom:'2026-01-01',validTo:null,occupancy:1});
 f.sqlite.exec('UPDATE r1_schema_state SET features_enabled=1');
 f.intent=async command=>{const c=await memberContext(),s=c.member.securityStamp,key=crypto.randomUUID();return {commandId:key,idempotencyKey:key,action:'M01.transfer',payload:{operation:'transfer',command},expectedWorkspaceRevision:c.row.revision,expectedAuthorizationRevision:s.authorizationRevision,expectedWriterEpoch:s.writerEpoch,expectedRecoveryEpoch:s.recoveryEpoch};};
 f.post=async(command,status=200)=>expect(await route.POST(request('/api/r1/commands',await f.intent(command))),status);
 f.request={action:'request',kind:'transfer',employeeId:f.e.id,orgId:f.otherOrg.id,positionId:f.target.id,effectiveOn:businessDate(),intent:'independent',reason:'合成独立调动事项'};
 f.submit=async extra=>{act('r1-hr');return (await f.post({...f.request,...extra})).result.approvalId;};
 f.approve=async id=>{act('approver');await f.post({action:'decide',id,decision:'approved'});act('r1-b');await f.post({action:'decide',id,decision:'approved'});};
 f.state=async()=>JSON.parse((await memberContext()).row.data);
 f.snapshot=()=>['hris_workspaces','hris_employees','hris_approvals','hris_approval_steps','r1_m01_entities','r1_m01_versions','r1_occupancy_events','r1_commands','r1_outbox','hris_employment_history','hris_audit_events'].map(table=>f.sqlite.prepare('SELECT * FROM '+table+' ORDER BY rowid').all());
 return f;
}
test('P3-M01-04 new D7 endpoint: second reviewer scope is target only; approval waits, atomic effect changes primary and compatibility once',async t=>{
 const f=await fixture(t),id=await f.submit();act('r1-b');await f.post({action:'decide',id,decision:'approved'},403);
 const publicView=await expect(await hris.GET());assert.ok(!publicView.state.employees.some(e=>e.id===f.e.id));assert.ok(publicView.state.approvals.some(a=>a.id===id));
 await f.approve(id);act('r1-hr');let state=await f.state();assert.equal(state.employees.find(e=>e.id===f.e.id).orgId,f.org.id);assert.equal(state.approvals.find(a=>a.id===id).details.transfer.execution,'waiting');
 const intent=await f.intent({action:'executeTransfer',id});const a=await expect(await route.POST(request('/api/r1/commands',intent)));assert.equal(a.result.effectStatus,'applied');
 const b=await expect(await route.POST(request('/api/r1/commands',intent)));assert.equal(b.replayed,true);assert.equal(a.result.assignmentId,b.result.assignmentId);
 state=await f.state();assert.equal(state.employees.find(e=>e.id===f.e.id).orgId,f.otherOrg.id);assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_m01_entities WHERE kind='assignment' AND status='active'").get().n,1);
 assert.equal(f.sqlite.prepare("SELECT status FROM r1_m01_entities WHERE id='primary'").get().status,'ended');
 assert.deepEqual(f.sqlite.prepare('SELECT delta FROM r1_occupancy_events ORDER BY delta').all().map(x=>x.delta),[-1,1]);
});
test('P3-M01-05 new D7 endpoint: early execution has no attempt; audit exception rolls back both models and same key can safely retry',async t=>{
 t.mock.timers.enable({apis:['Date'],now:Date.parse('2026-09-10T15:59:59Z')});const f=await fixture(t),id=await f.submit({effectiveOn:'2026-09-11'});await f.approve(id);act('r1-hr');
 let snapshot=f.snapshot();await f.post({action:'executeTransfer',id},400);assert.deepEqual(f.snapshot(),snapshot);
 t.mock.timers.setTime(Date.parse('2026-09-10T16:00:00Z'));const intent=await f.intent({action:'executeTransfer',id});
 f.sqlite.exec("CREATE TRIGGER r1_test_audit_fail BEFORE INSERT ON hris_audit_events BEGIN SELECT RAISE(ABORT,'synthetic audit failure'); END");snapshot=f.snapshot();await expect(await route.POST(request('/api/r1/commands',intent)),503);assert.deepEqual(f.snapshot(),snapshot);f.sqlite.exec('DROP TRIGGER r1_test_audit_fail');
 await expect(await route.POST(request('/api/r1/commands',intent)));assert.equal((await f.state()).approvals.find(a=>a.id===id).details.transfer.attempts,1);
});
test('P3-M01-06 new D7 endpoint: unrelated terminal history permits independent intent; correction restarts both reviewers; parallel requests share CAS',async t=>{
 const f=await fixture(t),first=await f.submit();act('r1-hr');await f.post({action:'withdraw',id:first});
 const independent=await f.submit();assert.equal((await f.state()).approvals.find(a=>a.id===independent).details.previousApprovalId,undefined);await f.post({action:'withdraw',id:independent});
 const corrected=await f.submit({intent:'correction',previousApprovalId:first});assert.equal((await f.state()).approvals.find(a=>a.id===corrected).currentStep,0);await f.post({action:'withdraw',id:corrected});
 const one=await f.intent(f.request),two=await f.intent(f.request);const results=await Promise.all([route.POST(request('/api/r1/commands',one)),route.POST(request('/api/r1/commands',two))]);assert.deepEqual(results.map(r=>r.status).sort(),[200,409]);
});
test('same-day transfers retain exact event time and one day-end primary instead of invalid negative date intervals',async t=>{
 const f=await fixture(t),first=await f.submit();await f.approve(first);act('r1-hr');const firstEffect=await f.post({action:'executeTransfer',id:first});
 act('owner');await f.post({action:'workflow',kind:'transfer',steps:[{userId:'r1-b',name:'调出B'},{userId:'approver',name:'调入A'}]});
 const second=await f.submit({orgId:f.org.id,positionId:f.position.id});act('r1-b');await f.post({action:'decide',id:second,decision:'approved'});act('approver');await f.post({action:'decide',id:second,decision:'approved'});act('r1-hr');await f.post({action:'executeTransfer',id:second});
 const ended=JSON.parse(f.sqlite.prepare('SELECT payload FROM r1_m01_entities WHERE id=?').get(firstEffect.result.assignmentId).payload);assert.equal(ended.validFrom,ended.validTo);assert.equal(ended.dayProjectionExcluded,true);assert.ok(ended.effectiveToAt>=ended.effectiveFromAt);
 assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_m01_entities WHERE kind='assignment' AND status='active'").get().n,1);
 assert.equal(f.sqlite.prepare('SELECT sum(delta) n FROM r1_occupancy_events WHERE position_id=?').get(f.target.id).n,0);
});
test('D7 business failure commits only attempt and reason; primary history and occupancy remain unchanged',async t=>{
 const f=await fixture(t),id=await f.submit();await f.approve(id);act('r1-hr');f.seed('budget','budget_policy',f.otherOrg.id,null,{strongBlocking:true});
 const before=f.sqlite.prepare('SELECT * FROM r1_m01_versions').all();const r=await f.post({action:'executeTransfer',id});assert.equal(r.result.effectStatus,'failed');
 assert.deepEqual(f.sqlite.prepare('SELECT * FROM r1_m01_versions').all(),before);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_occupancy_events').get().n,0);
 const a=(await f.state()).approvals.find(a=>a.id===id);assert.equal(a.status,'approved');assert.equal(a.details.transfer.attempts,1);assert.match(a.details.transfer.failure,/金额预算/);
});
