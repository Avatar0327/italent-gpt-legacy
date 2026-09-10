import {database,act,request} from './support/runtime.mjs';
import {readdirSync,readFileSync} from 'node:fs';
import test from 'node:test';
import assert from 'node:assert/strict';
const {memberContext}=await import('../lib/hris/context.ts');
const {makeEnvelope,receiveEvent,adapterCatalog,requireExternalResult,SimulatedAdapter,deliveryAction,verifyCallback}=await import('../lib/hris/r1-integration.ts');
const {canonical}=await import('../lib/hris/r1-command.ts');
const access=await import('../app/api/access/route.ts');
const commands=await import('../app/api/r1/commands/route.ts');
const hris=await import('../app/api/hris/route.ts');
const attachments=await import('../app/api/attachments/route.ts');
async function fixture(){const x=database();for(const f of readdirSync('drizzle').filter(f=>f.endsWith('.sql')).sort())x.sqlite.exec(readFileSync('drizzle/'+f,'utf8'));globalThis.p2env.DB=x.db;act('owner');assert.equal((await access.POST(request('/api/access',{action:'setup',name:'接口隔离合成'}))).status,200);return {...x,ctx:await memberContext()};}
const source={source:'M01',mappingVersion:1,schemaVersion:1,mode:'internal',version:'r1-20260910'};
const base={schemaVersion:1,eventId:'event-1',eventType:'assignment.applied',source:'M01',internalId:'assignment',externalId:null,entityRevision:1,workspaceRevision:1,definitionVersion:'v1',sourceRevision:0,sequence:1,mappingVersion:1,occurredAt:'2026-09-10T00:00:00Z',effectiveAt:'2026-09-10T00:00:00Z',correlationId:'command',causationId:'approval',digestAlgorithm:'sha256-canonical-json-v1',payload:{personId:'synthetic-person'}};
function intent(c,payload){const s=c.member.securityStamp,id=crypto.randomUUID();return {commandId:id,idempotencyKey:id,action:'inbox.consume',payload,expectedWorkspaceRevision:c.row.revision,expectedAuthorizationRevision:s.authorizationRevision,expectedWriterEpoch:s.writerEpoch,expectedRecoveryEpoch:s.recoveryEpoch};}
test('P3-INT-01: normalized envelope, durable duplicate, digest conflict and sequence gap',async()=>{
 const f=await fixture(),e=await makeEnvelope(base);let c=f.ctx;
 assert.equal((await receiveEvent(f.db,c.member,intent(c,e),e,source,()=>[])).status,'committed');
 c=await memberContext();assert.equal((await receiveEvent(f.db,c.member,intent(c,e),e,source,()=>[])).status,'duplicate');
 const changed=await makeEnvelope({...base,payload:{personId:'other'}});await assert.rejects(receiveEvent(f.db,c.member,intent(c,changed),changed,source,()=>[]),/不同内容/);
 const gap=await makeEnvelope({...base,eventId:'gap',sequence:3});assert.equal((await receiveEvent(f.db,c.member,intent(c,gap),gap,source,()=>[])).status,'gap');
 await assert.rejects(receiveEvent(f.db,c.member,intent(c,e),e,{...source,mappingVersion:2},()=>[]),/映射/);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_inbox').get().n,1);f.sqlite.close();
});
test('P3-INT-02: inbox projection and receipt roll back together under injected audit failure',async()=>{
 const f=await fixture(),e=await makeEnvelope(base),c=f.ctx;f.sqlite.exec("CREATE TRIGGER inject_integration_audit BEFORE INSERT ON hris_audit_events BEGIN SELECT RAISE(ABORT,'injected failure'); END");
 await assert.rejects(receiveEvent(f.db,c.member,intent(c,e),e,source,()=>[]),/injected failure/);
 assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_inbox').get().n,0);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_source_cursors').get().n,0);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_commands').get().n,0);f.sqlite.close();
});
test('P3-INT-03: explicitly simulated unknown delivery is queried and not blindly resent',async()=>{
 let intercepted=0;const adapter=new SimulatedAdapter(async()=>{intercepted++;return 'unknown';});
 assert.equal((await adapter.send('notification',{nodeId:'node'})).state,'unknown');assert.equal(deliveryAction('unknown',false,false),'query_receipt');
 await adapter.send('notification',{nodeId:'node'});assert.equal(intercepted,1);assert.equal(adapter.query('notification').mode,'simulated');
 await adapter.receipt('notification',{nodeId:'node'},'sent');await adapter.receipt('notification',{nodeId:'node'},'sent');await assert.rejects(adapter.receipt('notification',{nodeId:'other'},'sent'),/冲突/);
 assert.equal(deliveryAction('pending',true,false),'invalidate');assert.equal(adapter.attempts.length,1);
 const key=await crypto.subtle.importKey('raw',new Uint8Array(32).fill(7),{name:'HMAC',hash:'SHA-256'},false,['sign','verify']);const body={receiptId:'r1',state:'sent'};
 const signature=[...new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(canonical(body))))].map(x=>x.toString(16).padStart(2,'0')).join('');await verifyCallback(body,signature,key);await assert.rejects(verifyCallback({...body,state:'failed'},signature,key),/签名/);
});
test('P3-INT-04: six external adapters stay unconfigured; internal signed/published does not imply external success',()=>{
 assert.equal(adapterCatalog().length,6);for(const a of adapterCatalog()){assert.equal(a.realIntegration,'not_executed');assert.throws(()=>requireExternalResult(a.id,'signed'),e=>e.machineCode==='ADAPTER_NOT_CONFIGURED');}
});
test('P3-INT-05: unknown command and forged tenant cannot choose an unregistered producer',async()=>{
 const f=await fixture(),c=f.ctx,b=intent(c,{operation:'activateFutureProducer'});
 let r=await commands.POST(request('/api/r1/commands',{...b,tenantId:'forged'}));assert.equal(r.status,400);
 r=await commands.POST(request('/api/r1/commands',b));assert.equal(r.status,400);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_commands').get().n,0);f.sqlite.close();
});
test('P3-INT-06: unknown DB commit preserves uploaded bytes; tombstone refuses download and queues cleanup',async()=>{
 const f=await fixture();let c=await memberContext();let response=await hris.POST(request('/api/hris',{revision:c.row.revision,command:{action:'org',name:'文件合成组织',parentId:'',city:'上海',leader:'',status:'启用'}}));assert.equal(response.status,200);
 c=await memberContext();const org=JSON.parse(c.row.data).orgs[0].id;response=await hris.POST(request('/api/hris',{revision:c.row.revision,command:{action:'employee',code:'FILE1',name:'文件合成员工',orgId:org,job:'测试岗位',level:'',joined:'2026-01-01',email:''}}));assert.equal(response.status,200);
 c=await memberContext();const employeeId=JSON.parse(c.row.data).employees[0].id,objects=new Map();let deletes=0;
 globalThis.p2env.BUCKET={put:async(k,b)=>objects.set(k,b),get:async k=>objects.has(k)?{body:objects.get(k)}:null,delete:async()=>{deletes++;throw Error('synthetic object service unavailable');}};
 let lost=false;globalThis.p2env.DB={prepare:q=>f.db.prepare(q),batch:async statements=>{const r=await f.db.batch(statements);if(!lost&&statements.some(s=>s.sql.includes('INSERT INTO hris_attachments'))){lost=true;throw Error('response lost after SQLite commit');}return r;}};
 const upload=new Request('https://hris.example/api/attachments?'+new URLSearchParams({employeeId,revision:String(c.row.revision),name:'synthetic.txt'}),{method:'POST',headers:{Origin:'https://hris.example','Content-Type':'text/plain'},body:'synthetic attachment'});
 response=await attachments.POST(upload);assert.equal(response.status,503);assert.equal(objects.size,1);assert.equal(deletes,0);
 const file=f.sqlite.prepare('SELECT id FROM hris_attachments').get();assert.ok(file);globalThis.p2env.DB=f.db;
 response=await attachments.GET(request('/api/attachments?id='+file.id));assert.equal(response.status,200);assert.equal(await response.text(),'synthetic attachment');
 c=await memberContext();response=await attachments.DELETE(request('/api/attachments',{id:file.id,revision:c.row.revision}));assert.equal(response.status,200);assert.equal((await response.json()).cleanupPending,true);
 assert.equal((await attachments.GET(request('/api/attachments?id='+file.id))).status,404);assert.equal(f.sqlite.prepare('SELECT count(*) n FROM r1_object_cleanup').get().n,1);assert.equal(objects.size,1);assert.equal(deletes,0);f.sqlite.close();
});
