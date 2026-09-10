import {database,act,request} from './support/runtime.mjs';
import {readdirSync,readFileSync} from 'node:fs';
import test from 'node:test';
import assert from 'node:assert/strict';
const {executeWorkflow}=await import('../lib/hris/r1-workflow.ts');
const {validateDefinition,resolveNode,resolveDecisions}=await import('../lib/hris/r1-workflow-model.ts');
const {memberContext}=await import('../lib/hris/context.ts');
const access=await import('../app/api/access/route.ts');
const definition=(extra={})=>({businessType:'synthetic.review',adapterVersion:'fixture-v1',entry:'review',fields:{},nodes:[{id:'review',type:'review',assignees:['a','b'],passPolicy:'all',rejectPolicy:'any_reject',next:'end'},{id:'end',type:'end'}],interventionTargets:['review'],notificationTemplateVersion:1,...extra});
async function fixture(){
 const {sqlite,db}=database();for(const f of readdirSync('drizzle').filter(f=>f.endsWith('.sql')).sort())sqlite.exec(readFileSync('drizzle/'+f,'utf8'));
 globalThis.p2env.DB=db;act('owner');assert.equal((await access.POST(request('/api/access',{action:'setup',name:'流程隔离合成'}))).status,200);const t=(await memberContext()).member.tenantId;
 sqlite.exec('DROP TRIGGER r1_guard_hris_memberships_insert');
 for(const who of ['a','b','c','delegate'])sqlite.prepare("INSERT INTO hris_memberships(user_id,tenant_id,role,employee_id,org_scope,view_email,view_level,active) VALUES (?,?,'hr',?,'[\"A\"]',1,1,1)").run(who,t,who+'-person');
 for(const who of ['owner','a','b','c','delegate'])for(const action of ['configure','start','decide','manage.transfer','manage.intervene','manage.revoke','withdraw','remind','read'])sqlite.prepare('INSERT INTO r1_permission_grants VALUES (?,?,?,?,?,?,?,?,?,?,?)').run(t,who+action,who,'M19',action,'scope','["A"]','["record","grade"]','current','2020-01-01',null);
 sqlite.exec('UPDATE r1_schema_state SET features_enabled=1; CREATE TABLE synthetic_workflow_source(id TEXT PRIMARY KEY,status TEXT NOT NULL,revision INTEGER NOT NULL)');
 const seed=(id='source')=>sqlite.prepare("INSERT INTO synthetic_workflow_source VALUES (?,'pending',1)").run(id);seed();
 const adapter={version:'fixture-v1',async loadBusinessSnapshot(id){const r=sqlite.prepare('SELECT * FROM synthetic_workflow_source WHERE id=?').get(id);if(!r)throw Error('source missing');return {businessType:'synthetic.review',businessId:id,applicationVersion:1,revision:r.revision,orgId:'A',personId:'subject',initiatorId:'owner',title:'合成契约测试原单',values:{},requiredFields:['record','grade'],status:r.status};},async validateStart(s){assert.equal(s.status,'pending');},async validateDecision(s){assert.equal(s.status,'pending');},async planLocalEffect(s){return {status:'applied',statements:token=>[db.prepare("UPDATE synthetic_workflow_source SET status='applied',revision=revision+1 WHERE id=? AND EXISTS(SELECT 1 FROM hris_workspaces WHERE owner=? AND last_mutation=?)").bind(s.businessId,t,token)]};},async canCancel(s){return s.status==='pending';},async planLocalCancel(s){return token=>[db.prepare("UPDATE synthetic_workflow_source SET status='cancelled',revision=revision+1 WHERE id=? AND EXISTS(SELECT 1 FROM hris_workspaces WHERE owner=? AND last_mutation=?)").bind(s.businessId,t,token)];}};
 const registry={'synthetic.review':adapter};
 const intent=async(payload)=>{const ctx=await memberContext(),s=ctx.member.securityStamp,key=crypto.randomUUID();return {ctx,command:{commandId:key,idempotencyKey:key,action:'M19.'+payload.operation,payload,expectedWorkspaceRevision:ctx.row.revision,expectedAuthorizationRevision:s.authorizationRevision,expectedWriterEpoch:s.writerEpoch,expectedRecoveryEpoch:s.recoveryEpoch}};};
 const send=async p=>{const {ctx,command}=await intent(p);return executeWorkflow(ctx,command,registry);};
 const get=id=>sqlite.prepare('SELECT * FROM r1_workflow_instances WHERE id=?').get(id);
 const target=id=>{const i=get(id),n=sqlite.prepare('SELECT * FROM r1_workflow_nodes WHERE id=?').get(i.current_node_id);return {id,expectedRevision:i.revision,generation:i.generation,nodeRevision:n.revision};};
 const start=async(id='source',d=definition())=>{await send({operation:'publish',id:'template',orgId:'A',definition:d});return (await send({operation:'start',templateId:'template',businessType:'synthetic.review',businessId:id,applicationVersion:1})).result.instanceId;};
 return {sqlite,db,t,send,intent,get,target,start,seed,adapter,registry};
}
test('P3-M19-01: graph/type validation, null/missing/multiple routes and no implicit auto pass',async()=>{
 const d=definition();assert.throws(()=>validateDefinition({...d,nodes:[{...d.nodes[0],next:'review'},d.nodes[1]]}),/环/);assert.throws(()=>validateDefinition({...d,businessType:'personnel.transfer'}),/D7/);
 const branch={id:'route',type:'branch',routes:[{when:{op:'gt',field:'amount',value:0},next:'review'},{when:{op:'lt',field:'amount',value:10},next:'review'}]},r=validateDefinition({...d,entry:'route',fields:{amount:'number'},nodes:[branch,...d.nodes]});
 assert.throws(()=>resolveNode(r,'route',{}),/缺失/);assert.throws(()=>resolveNode(r,'route',{amount:null}),/没有/);assert.throws(()=>resolveNode(r,'route',{amount:5}),/多条/);assert.equal(resolveNode(r,'route',{amount:15}).id,'review');
 const f=await fixture();await assert.rejects(f.start('source',{...d,entry:'route',nodes:[{id:'route',type:'branch',routes:[{when:{op:'isNull',field:'x'},next:'end'},{when:{op:'eq',field:'x',value:1},next:'review'}]},...d.nodes],fields:{x:'number'}}),/缺失/);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_workflow_instances').get().n,0);f.sqlite.close();
});
test('P3-M19-01: application dedup, immutable template v1 continues after v2 publication',async()=>{
 const f=await fixture(),id=await f.start();const replay=await f.send({operation:'start',templateId:'template',businessType:'synthetic.review',businessId:'source',applicationVersion:1});assert.equal(replay.result.instanceId,id);
 const v2=definition();v2.nodes[0].assignees=['c'];await f.send({operation:'publish',id:'template',orgId:'A',definition:v2});assert.equal(JSON.parse(f.get(id).template_payload).templateVersion,1);
 act('a');await f.send({operation:'decide',...f.target(id),decision:'approved',reason:'合成'});assert.equal(f.get(id).approval_status,'pending');act('b');await f.send({operation:'decide',...f.target(id),decision:'approved',reason:'合成'});assert.equal(f.get(id).effect_status,'applied');assert.throws(()=>f.sqlite.exec("UPDATE r1_workflow_templates SET digest='changed'"),/IMMUTABLE/);f.sqlite.close();
});
test('P3-M19-02: all/any and reject policies are explicit and order-independent for same collected votes',async()=>{
 const n=definition().nodes[0],votes=[{actorId:'a',decision:'approved'},{actorId:'b',decision:'rejected'}];for(const passPolicy of ['all','any'])for(const ordered of [votes,[...votes].reverse()]){assert.equal(resolveDecisions({...n,passPolicy},ordered),'rejected');assert.equal(resolveDecisions({...n,passPolicy,rejectPolicy:'block_for_review'},ordered),'blocked');}
 const f=await fixture(),id=await f.start();act('a');const first=await f.intent({operation:'decide',...f.target(id),decision:'approved',reason:'合成'});act('b');const competing=await f.intent({operation:'decide',...f.target(id),decision:'rejected',reason:'合成'});await executeWorkflow(first.ctx,first.command,f.registry);await assert.rejects(executeWorkflow(competing.ctx,competing.command,f.registry),/版本/);await f.send({operation:'decide',...f.target(id),decision:'rejected',reason:'刷新后拒绝'});assert.equal(f.get(id).approval_status,'rejected');assert.equal(f.sqlite.prepare('SELECT status FROM synthetic_workflow_source').get().status,'pending');f.sqlite.close();
});
test('P3-M19-03: transfer and intervention invalidate old node tokens, preserve actual decisions',async()=>{
 const f=await fixture(),id=await f.start();act('a');await f.send({operation:'decide',...f.target(id),decision:'approved',reason:'原审核'});act('owner');const old=f.target(id);await f.send({operation:'transferNode',...old,assignees:['c'],reason:'合成转交'});act('b');await assert.rejects(f.send({operation:'decide',...old,decision:'approved',reason:'旧链接'}),/版本/);act('owner');const {nodeRevision,...target}=f.target(id);await f.send({operation:'intervene',...target,targetNode:'review',reason:'退回许可节点'});assert.equal(f.get(id).generation,2);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_workflow_decisions').get().n,1);assert.equal(f.sqlite.prepare("SELECT count(*) n FROM r1_workflow_nodes WHERE status='skipped_by_intervention'").get().n,1);assert.ok(f.sqlite.prepare("SELECT count(*) n FROM r1_workflow_notifications WHERE status='invalidated'").get().n>=2);f.sqlite.close();
});
test('P3-M19-04: domain cancellation SQL failure rolls back workflow/audit/receipt, success cancels both',async()=>{
 const f=await fixture(),id=await f.start(),before=f.sqlite.prepare('SELECT count(*) n FROM r1_commands').get().n;const {nodeRevision,...target}=f.target(id);
 f.sqlite.exec("CREATE TRIGGER synthetic_cancel_fail BEFORE UPDATE ON synthetic_workflow_source BEGIN SELECT RAISE(ABORT,'cancel_fault'); END");await assert.rejects(f.send({operation:'revokeFlow',...target,reason:'合成撤销'}),/cancel_fault/);assert.equal(f.get(id).approval_status,'pending');assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_commands').get().n,before);
 f.sqlite.exec('DROP TRIGGER synthetic_cancel_fail');await f.send({operation:'revokeFlow',...target,reason:'复验'});assert.equal(f.get(id).approval_status,'cancelled');assert.equal(f.sqlite.prepare('SELECT status FROM synthetic_workflow_source').get().status,'cancelled');f.sqlite.close();
});
test('P3-M19-06: delegation acceptance, intersection, no approval/proxy, revocation and commit-time expiry',async()=>{
 const f=await fixture(),id=await f.start(),base={operation:'createDelegation',delegateId:'delegate',actions:['manage.transfer'],businessTypes:['synthetic.review'],scope:['A'],fields:['record','grade'],startAt:Date.now()-1000,endAt:Date.now()+100000};
 await assert.rejects(f.send({...base,delegateId:'owner'}),/自委托/);const r=await f.send(base),delegationId=r.result.delegationId;await assert.rejects(f.send(base),/重叠/);act('delegate');await assert.rejects(f.send({operation:'transferNode',...f.target(id),assignees:['c'],reason:'未接受',delegationId}),/无效/);
 await f.send({operation:'acceptDelegation',id:delegationId,expectedRevision:1,reason:'接受'});await assert.rejects(f.send({operation:'decide',...f.target(id),decision:'approved',reason:'委托不授审批',delegationId}),/不授予/);
 f.sqlite.prepare("UPDATE r1_permission_grants SET fields='[\"record\"]' WHERE member_id='owner' AND action='manage.transfer'").run();await assert.rejects(f.send({operation:'transferNode',...f.target(id),assignees:['c'],reason:'原管理人少字段',delegationId}),/权限/);
 f.sqlite.prepare("UPDATE r1_permission_grants SET fields='[\"record\",\"grade\"]' WHERE member_id='owner' AND action='manage.transfer'").run();
 f.sqlite.prepare('UPDATE r1_admin_delegations SET end_at=? WHERE id=?').run(Date.now()+120,delegationId);const attempt=await f.intent({operation:'transferNode',...f.target(id),assignees:['c'],reason:'提交时过期',delegationId}),batch=f.db.batch;
 f.db.batch=async statements=>{if(statements.some(s=>s.sql.includes('INSERT INTO r1_workflow_commit_guard')))await new Promise(r=>setTimeout(r,160));return batch(statements);};await assert.rejects(executeWorkflow(attempt.ctx,attempt.command,f.registry),/提交时已过期/);f.db.batch=batch;assert.equal(f.get(id).revision,1);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_workflow_commit_guard').get().n,0);f.sqlite.close();
});
