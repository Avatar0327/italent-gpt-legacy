// Synthetic, isolated SQLite/object rehearsal. Never connects to a deployed D1 or R2.
import {database,act,request} from '../tests/support/runtime.mjs';
import {mkdtempSync,readFileSync,readdirSync,writeFileSync,copyFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const access=await import('../app/api/access/route.ts'),hris=await import('../app/api/hris/route.ts'),dev=await import('../app/api/development/route.ts'),attachments=await import('../app/api/attachments/route.ts');
const templates=await import('../app/api/performance-templates/route.ts'),performanceApi=await import('../app/api/performance/route.ts'),members=await import('../app/api/members/route.ts');
const directory=mkdtempSync(join(tmpdir(),'hris-synthetic-recovery-'));
let live,restored;
const sha=value=>createHash('sha256').update(value).digest('hex');
const identifier=value=>'"'+value.replaceAll('"','""')+'"';
async function json(response,status=200){assert.equal(response.status,status,await response.clone().text());return response.json();}
async function core(command){const data=await json(await hris.GET());return json(await hris.POST(request('/api/hris',{revision:data.revision,command})));}
async function develop(command){const data=await json(await dev.GET());return json(await dev.POST(request('/api/development',{revision:data.revision,command})));}
async function perf(api,path,command,status=200){return json(await api.POST(request(path,{revision:(await json(await dev.GET())).revision,command})),status);}
function fingerprints(sqlite){return sqlite.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").all().map(({name})=>{const rows=sqlite.prepare('SELECT * FROM '+identifier(name)).all().map(r=>JSON.stringify(r)).sort();return {table:name,rows:rows.length,sha256:sha(JSON.stringify(rows))};});}
function bucket(objects){return {put:async(key,bytes)=>objects.set(key,new Uint8Array(bytes)),get:async key=>objects.has(key)?{body:objects.get(key)}:null,delete:async key=>objects.delete(key)};}
function objectIssues(sqlite,objects,manifest){const issues=[];for(const row of sqlite.prepare('SELECT object_key,size FROM hris_attachments WHERE deleted_at IS NULL').all()){const bytes=objects.get(row.object_key),expected=manifest.find(m=>m.key===row.object_key);if(!bytes)issues.push('missing');else if(bytes.byteLength!==row.size||!expected||sha(bytes)!==expected.sha256)issues.push('corrupt');}return issues;}
try{
 live=database(join(directory,'source.sqlite'));globalThis.p2env.DB=live.db;const objects=new Map();globalThis.p2env.BUCKET=bucket(objects);
 const migrations=readdirSync('drizzle').filter(f=>f.endsWith('.sql')).sort();for(const file of migrations)live.sqlite.exec(readFileSync('drizzle/'+file,'utf8'));
 act('owner');await json(await access.POST(request('/api/access',{action:'setup',name:'合成恢复演练企业'})));
 await core({action:'org',name:'合成恢复部门',parentId:'',city:'上海',leader:'',status:'启用'});
 const org=(await json(await hris.GET())).state.orgs[0];await core({action:'employee',code:'RECOVERY-1',name:'合成恢复员工',orgId:org.id,job:'测试岗位',level:'',joined:'2026-01-01',email:''});
 const employee=(await json(await hris.GET())).state.employees[0];
 const course=await develop({action:'course',code:'RECOVERY-COURSE',title:'合成恢复课程',description:'合成恢复演练课程描述',content:'这是一段仅用于本地恢复演练的合成课程内容，不涉及真实员工或业务资料。'});await develop({action:'publishCourse',id:course.id});await develop({action:'enroll',employeeId:employee.id,courseId:course.id,due:'2099-12-31'});
 // Persist an immutable template/cycle snapshot and a claimed-then-revoked account before the cut.
 const template=await perf(templates,'/api/performance-templates',{action:'create',title:'合成恢复文本模板',orgId:org.id,description:'验证恢复后的模板版本与快照',prompts:[{id:'proof',title:'恢复后自评依据',stage:'selfReview',required:true}]});
 await perf(templates,'/api/performance-templates',{action:'seal',id:template.id});
 const cycle=await perf(performanceApi,'/api/performance',{action:'cycle',name:'合成恢复周期',orgId:org.id,period:'RECOVERY-PERF',start:'2026-01-01',end:'2026-12-31',lowCut:60,highCut:80,lowLabel:'待改进',midLabel:'达成',highLabel:'优秀',templateId:template.id});
 await perf(performanceApi,'/api/performance',{action:'startCycle',id:cycle.id});
 const plan=await perf(performanceApi,'/api/performance',{action:'goals',employeeId:employee.id,cycleId:cycle.id,goals:[{title:'合成恢复目标',metric:'核实模板快照和已停用成员不得恢复权限',weight:100}]});
 await perf(performanceApi,'/api/performance',{action:'confirmGoals',id:plan.id});
 const grant={email:'recovery-employee@example.com',name:'合成恢复成员',role:'employee',employeeId:employee.id,orgScope:[],viewEmail:false,viewLevel:false,active:true};
 await json(await members.POST(request('/api/members',{...grant,revision:(await json(await members.GET())).revision})));
 act('recovery-employee');await json(await access.POST(request('/api/access',{action:'activate'})));await json(await dev.GET());act('owner');
 await json(await members.POST(request('/api/members',{...grant,active:false,revision:(await json(await members.GET())).revision})));
 const beforeUpload=await json(await dev.GET());const file=await json(await attachments.POST(new Request('https://hris.example/api/attachments?'+new URLSearchParams({employeeId:employee.id,revision:String(beforeUpload.revision),name:'synthetic.txt'}),{method:'POST',headers:{Origin:'https://hris.example','Content-Type':'text/plain'},body:'Synthetic recovery attachment only.'})));
 const expectedPerformance=await json(await performanceApi.GET());
 const expected=await json(await dev.GET()),before=fingerprints(live.sqlite),manifest=[...objects].map(([key,bytes])=>({key,size:bytes.byteLength,sha256:sha(bytes)}));
 // Quiescent cut: no writers during the database snapshot and object copy.
 const snapshot=join(directory,'snapshot.sqlite');live.sqlite.exec("VACUUM INTO '"+snapshot.replaceAll("'","''")+"'");const savedObjects=new Map([...objects].map(([key,bytes])=>[key,new Uint8Array(bytes)]));
 await develop({action:'course',code:'AFTER-CUT',title:'恢复点之后的记录',description:'该记录不应出现在恢复点',content:'该合成课程是在备份恢复点之后新建，恢复旧快照后应该不存在。'});assert.ok((await json(await dev.GET())).revision>expected.revision);
 live.sqlite.close();live=null;objects.clear();const start=performance.now();copyFileSync(snapshot,join(directory,'restored.sqlite'));restored=database(join(directory,'restored.sqlite'));globalThis.p2env.DB=restored.db;globalThis.p2env.BUCKET=bucket(savedObjects);
 assert.deepEqual(restored.sqlite.prepare('PRAGMA integrity_check').all().map(r=>r.integrity_check),['ok']);assert.equal(restored.sqlite.prepare('PRAGMA foreign_key_check').all().length,0);assert.deepEqual(fingerprints(restored.sqlite),before);assert.deepEqual(await json(await dev.GET()),expected);
 assert.deepEqual(await json(await performanceApi.GET()),expectedPerformance);
 act('recovery-employee');await json(await performanceApi.GET(),403);await json(await attachments.GET(request('/api/attachments?id='+file.id)),403);act('owner');
 await perf(templates,'/api/performance-templates',{action:'edit',id:template.id,title:'禁止改写已定版版本',orgId:org.id,description:'恢复后也必须保持不可变',prompts:[]},400);
 const downloaded=await attachments.GET(request('/api/attachments?id='+file.id));assert.equal(downloaded.status,200);assert.equal(await downloaded.text(),'Synthetic recovery attachment only.');assert.deepEqual(objectIssues(restored.sqlite,savedObjects,manifest),[]);
 const [key,bytes]=[...savedObjects][0];savedObjects.delete(key);assert.deepEqual(objectIssues(restored.sqlite,savedObjects,manifest),['missing']);savedObjects.set(key,new Uint8Array(bytes.byteLength));assert.deepEqual(objectIssues(restored.sqlite,savedObjects,manifest),['corrupt']);savedObjects.set(key,bytes);
 act('uninvited');assert.equal((await dev.GET()).status,403);act('owner');await develop({action:'course',code:'AFTER-RESTORE',title:'恢复后新记录',description:'恢复后验证可继续安全写入',content:'恢复后的新合成课程用于验证修订递增和事件审计仍能正常写入。'});assert.equal((await json(await dev.GET())).revision,expected.revision+1);assert.equal(restored.sqlite.prepare('SELECT count(*) AS n FROM hris_audit_events').get().n,before.find(t=>t.table==='hris_audit_events').rows+1);assert.equal(restored.sqlite.prepare('SELECT count(*) AS n FROM hris_development_events').get().n,before.find(t=>t.table==='hris_development_events').rows+1);
 const result={at:new Date().toISOString(),mode:'isolated synthetic SQLite and memory object store',passed:true,migrations:migrations.map(file=>({file,sha256:sha(readFileSync('drizzle/'+file))})),restoredRevision:expected.revision,tables:before,attachmentCount:manifest.length,checks:['table hashes equal','SQLite integrity','foreign keys','application records and revision equal','attachment download and checksum','missing object detected','corrupt object detected','uninvited user denied','frozen performance template and cycle snapshot equal','revoked claimed account remains denied for performance and attachments','restored sealed template rejects edit','post-restore audited mutation'],localRestoreAndValidationMs:Math.round((performance.now()-start)*100)/100,limitations:['No deployed D1 or R2 accessed','Quiescent synthetic snapshot only','No cloud backup scheduling, encryption, retention or region failover verified','No real enterprise RPO/RTO acceptance','Revocations after the backup cut require an independent trusted reconciliation before reopening access; not exercised here','Not all business tables contain fixture rows']};
 writeFileSync('docs/Recovery_Synthetic_Report.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({passed:true,tables:before.length,nonEmptyTables:before.filter(t=>t.rows).length,attachmentCount:manifest.length,checks:result.checks.length,report:'docs/Recovery_Synthetic_Report.json'}));
}finally{live?.sqlite.close();restored?.sqlite.close();rmSync(directory,{recursive:true,force:true});}
