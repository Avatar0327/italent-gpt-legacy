import {z} from 'zod';
import {HttpError} from './http';
import {businessDate} from './business-time';
import {commitCommand,securityStamp,digest,type CommandIntent} from './r1-command';
import {authorizeTuple} from './r1-authorization';
import {scopedOrgs,type Member} from './authorization';
import type {State} from './model';

const id=z.string().min(1).max(100),text=z.string().trim().min(1).max(200);
const date=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(s=>{const d=new Date(s+'T00:00:00Z');return !isNaN(+d)&&d.toISOString().slice(0,10)===s;});
const interval={validFrom:date,validTo:date.nullable()};
const catalogKind=z.enum(['org','position','job','job_family','grade','legal_entity']);
const subsetKind=z.enum(['education','employment','family','appraisal','training','reward','certificate','project','skill','language','custom']);
const field=z.object({code:id,type:z.enum(['text','number','date','enum','attachment']),required:z.boolean(),default:z.union([z.string(),z.number(),z.null()]),uniqueKey:z.boolean(),readActions:z.array(id).min(1),writeActions:z.array(id).min(1),options:z.array(text).optional(),unit:z.string().optional(),precision:z.number().int().min(0).max(6).optional()}).strict();
export const m01Input=z.discriminatedUnion('operation',[
 z.object({operation:z.literal('catalog'),id:id.optional(),kind:catalogKind,code:text,name:text,orgId:z.string(),parentId:z.string(),status:z.enum(['active','inactive']),...interval,attributes:z.object({abbr:z.string().max(100).optional(),city:z.string().max(100).optional(),jobId:id.optional(),familyId:id.optional(),gradeMinId:id.optional(),gradeMaxId:id.optional(),sequence:z.number().int().min(0).max(999).optional(),establishedOn:date.optional(),newType:z.enum(['New','Backfill']).optional(),responsibilities:z.string().max(4000).optional(),orgIds:z.array(id).optional(),extraPersonIds:z.array(id).optional()}).strict()}).strict(),
 z.object({operation:z.literal('identityReview'),personId:id,candidateIds:z.array(id).min(1),reason:text,evidenceRef:id}).strict(),
 z.object({operation:z.literal('person'),code:text,name:text,orgId:id,templateId:id,entryType:z.enum(['employee_create','prehire','onboard']),fields:z.record(z.unknown())}).strict(),
 z.object({operation:z.literal('employment'),personId:id,orgId:id,identityReviewId:id,predecessorId:id.nullable(),startOn:date,employmentType:z.enum(['employee','internship','retired_rehire'])}).strict(),
 z.object({operation:z.literal('assignmentRequest'),personId:id,employmentId:id,orgId:id,positionId:id,type:z.enum(['primary','part_time','secondment','expatriate']),homePrimaryId:id.nullable(),...interval,reviewerId:id,reason:text}).strict(),
 z.object({operation:z.literal('assignmentApprove'),id}).strict(),z.object({operation:z.literal('assignmentExecute'),id}).strict(),
 z.object({operation:z.literal('exitRequest'),personId:id,orgId:id,lastWorkingOn:date,reviewerId:id,reason:text}).strict(),z.object({operation:z.literal('exitApprove'),id}).strict(),z.object({operation:z.literal('exitExecute'),id}).strict(),
 z.object({operation:z.literal('contract'),id:id.optional(),personId:id,orgId:id,legalEntityId:id,number:text,agreementCategory:z.enum(['labor','service','internship']),contractType:z.enum(['fixed','open','project']),start:date,end:date.nullable(),renewalOf:id.nullable(),fields:z.record(z.union([z.string().max(1000),z.null()]))}).strict(),
 z.object({operation:z.literal('contractSign'),id,signedOn:date,evidence:text}).strict(),z.object({operation:z.literal('contractEnd'),id,endedOn:date,evidence:text}).strict(),
 z.object({operation:z.literal('template'),id:id.optional(),orgId:id,kind:subsetKind,entryType:z.enum(['employee_create','prehire','onboard','subset']),fields:z.array(field).min(1).max(20)}).strict(),
 z.object({operation:z.literal('subsetImport'),personId:id,orgId:id,templateId:id,templateVersion:z.number().int().positive(),batchId:id,rowNo:z.number().int().positive(),attemptVersion:z.number().int().positive(),mode:z.enum(['create','update']),recordId:id.nullable(),fields:z.record(z.unknown())}).strict(),
]);
export type M01Input=z.infer<typeof m01Input>;
export type Entity={id:string;kind:string;personId:string|null;orgId:string|null;code:string|null;revision:number;status:string;payload:Record<string,any>};
export const overlaps=(a:{validFrom:string;validTo:string|null},b:{validFrom:string;validTo:string|null})=>a.validFrom<=(b.validTo??'9999-12-31')&&b.validFrom<=(a.validTo??'9999-12-31');
export const nextDay=(day:string)=>new Date(Date.parse(day+'T00:00:00Z')+86400000).toISOString().slice(0,10);
export function tenure(segments:{startOn:string|null;lastWorkingOn:string|null;status:string;employmentType:string}[],asOf:string){
 const ranges: [number,number][]=[];
 for(const s of segments){if(s.employmentType==='internship')continue;if(!s.startOn||s.status==='ended'&&!s.lastWorkingOn)return {days:null,years:null,reasonCode:'HISTORY_UNVERIFIABLE'};if(s.status==='cancelled'||s.startOn>asOf)continue;ranges.push([Date.parse(s.startOn),Date.parse(s.lastWorkingOn&&s.lastWorkingOn<asOf?s.lastWorkingOn:asOf)]);}
 ranges.sort((a,b)=>a[0]-b[0]);const merged:[number,number][]=[];for(const [a,b] of ranges){const last=merged.at(-1);if(last&&a<=last[1]+86400000)last[1]=Math.max(last[1],b);else merged.push([a,b]);}
 const days=merged.reduce((n,[a,b])=>n+(b-a)/86400000+1,0);return {days,years:Math.round(days/365*100)/100,reasonCode:null};
}
function invalid(message:string,code='INVALID_INPUT'):never{throw new HttpError(400,message,code);}
const parse=(r:any):Entity=>({...r,payload:JSON.parse(r.payload)});
const select='SELECT id,kind,person_id AS personId,org_id AS orgId,code,revision,status,payload FROM r1_m01_entities';
export async function m01Entity(db:D1Database,tenant:string,entityId:string){const r=await db.prepare(select+' WHERE tenant_id=? AND id=?').bind(tenant,entityId).first();if(!r)throw new HttpError(404,'记录不存在或不可见','NOT_FOUND_OR_NOT_VISIBLE');return parse(r);}
async function rows(db:D1Database,tenant:string,kind:string,personId?:string){const r=await db.prepare(select+' WHERE tenant_id=? AND kind=?'+(personId?' AND person_id=?':'')+' ORDER BY id LIMIT 201').bind(tenant,kind,...(personId?[personId]:[])).all();if(r.results.length>200)throw new HttpError(503,'需要有界版本查询计划','BOUNDED_QUERY_REQUIRED');return r.results.map(parse);}
export function m01Write(db:D1Database,tenant:string,token:string,e:Entity,commandId:string,at:string){
 return [db.prepare(`INSERT INTO r1_m01_entities(tenant_id,id,kind,person_id,org_id,code,revision,status,payload) SELECT owner,?,?,?,?,?,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=? ON CONFLICT(tenant_id,id) DO UPDATE SET revision=excluded.revision,status=excluded.status,payload=excluded.payload,org_id=excluded.org_id`).bind(e.id,e.kind,e.personId,e.orgId,e.code,e.revision,e.status,JSON.stringify(e.payload),tenant,token),
 db.prepare('INSERT INTO r1_m01_versions(tenant_id,entity_id,version,workspace_revision,command_id,recorded_at,valid_from,valid_to,history_quality,payload) SELECT owner,?,?,revision,?,?,?,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=?').bind(e.id,e.revision,commandId,at,e.payload.validFrom??e.payload.startOn??null,e.payload.validTo??e.payload.lastWorkingOn??null,e.payload.historyQuality??'known',JSON.stringify(e),tenant,token)];
}
function templateValues(template:Entity,input:Record<string,unknown>,mode:'create'|'update',old:Record<string,unknown>={}){
 const output:Record<string,unknown>={};const definitions=template.payload.fields as z.infer<typeof field>[];
 if(Object.keys(input).some(k=>!definitions.some(f=>f.code===k)))invalid('模板未声明字段');
 for(const f of definitions){const value=Object.hasOwn(input,f.code)?input[f.code]:mode==='update'?old[f.code]:f.default;
 if(value===null||value===undefined){if(f.required)invalid('缺少必填字段');output[f.code]=null;continue;}
 if(f.type==='number'){if(typeof value!=='number'||!Number.isFinite(value)||!f.unit||f.precision===undefined||Math.abs(value*10**f.precision-Math.round(value*10**f.precision))>1e-6)invalid('数值单位或精度无效');}
 else if(typeof value!=='string'||value.length>1000)invalid('字段类型或长度无效');
 else if(f.type==='date'&&!date.safeParse(value).success)invalid('日期无效');
 else if(f.type==='enum'&&!f.options?.includes(value))invalid('枚举值无效');
 output[f.code]=typeof value==='string'?value.trim():value;
 }return output;
}
/** The current member, tenant and actual execution time are server-derived. */
export async function executeM01(ctx:{db:D1Database;member:Member;row:{revision:number;data:string}},intent:CommandIntent){
 const c=m01Input.parse(intent.payload),{db,member:m}=ctx,tenant=m.tenantId,at=new Date().toISOString(),today=businessDate(at),stamp=await securityStamp(db,tenant);
 if(!stamp.featuresEnabled)throw new HttpError(409,'新能力等待迁移与恢复核验','FEATURE_NOT_READY');
 const state=JSON.parse(ctx.row.data) as State,scope=scopedOrgs(state,m);
 if(!['hr','admin'].includes(m.role))throw new HttpError(403,'仅授权HR办理','FORBIDDEN');
 const changes:Entity[]=[],extra:((token:string)=>D1PreparedStatement[])[]=[],result:Record<string,unknown>={};
 const get=(entityId:string)=>m01Entity(db,tenant,entityId);
 const make=(kind:string,orgId:string|null,personId:string|null,payload:Record<string,any>,status='active',code:string|null=null):Entity=>({id:crypto.randomUUID(),kind,orgId,personId,payload,status,code,revision:1});
 const revise=(e:Entity,payload:Record<string,any>,status=e.status):Entity=>({...e,revision:e.revision+1,status,payload:{...e.payload,...payload}});
 const authorize=async(orgId:string,personId:string,fieldName='record')=>{if(!scope.has(orgId))throw new HttpError(403,'没有此组织办理权限','FORBIDDEN');await authorizeTuple(db,m,{objectType:'M01',action:c.operation,orgId,personId,field:fieldName,historyMode:'current'});};
 const activeCatalog=async(entityId:string,kind:string)=>{const e=await get(entityId);if(e.kind!==kind||e.status!=='active'||!e.payload.validFrom||e.payload.validFrom>today||e.payload.validTo&&e.payload.validTo<today)invalid('目标目录当前不可用','TARGET_INVALID');return e;};
 if('orgId' in c)await authorize(c.orgId,'personId' in c?c.personId:'');
 if('id' in c&&c.id&&!['catalog','template','contract'].includes(c.operation)){const e=await get(c.id);await authorize(e.orgId??'',e.personId??'');if(e.personId&&await db.prepare('SELECT 1 FROM r1_exit_fences WHERE tenant_id=? AND person_id=?').bind(tenant,e.personId).first())invalid('人员已退出，后续办理已阻断','BLOCKED_BY_EXIT');}
 if('personId' in c&&!['employment','identityReview'].includes(c.operation)){const fence=await db.prepare('SELECT person_id FROM r1_exit_fences WHERE tenant_id=? AND person_id=?').bind(tenant,c.personId).first();if(fence)invalid('人员已退出，后续办理已阻断','BLOCKED_BY_EXIT');}
 switch(c.operation){
 case 'catalog':{
  if(c.validFrom<today||c.validTo&&c.validTo<c.validFrom)invalid('目录有效日期无效');
  const old=c.id?await get(c.id):null;if(old&&old.kind!==c.kind)invalid('不能改变目录类型');
  if(old&&old.orgId&&old.orgId!==c.orgId)await authorize(old.orgId,'');
  const all=await rows(db,tenant,c.kind);
  if(all.some(e=>e.id!==c.id&&e.code===c.code))invalid('编码已存在');
  if(c.kind==='position'&&c.attributes.establishedOn&&c.attributes.establishedOn>c.validFrom)invalid('设立日期晚于生效日期');
  if(c.kind==='position'&&c.attributes.gradeMinId&&c.attributes.gradeMaxId){const a=await get(c.attributes.gradeMinId),b=await get(c.attributes.gradeMaxId);if(a.kind!=='grade'||b.kind!=='grade'||a.payload.attributes.familyId!==b.payload.attributes.familyId||a.payload.attributes.sequence>b.payload.attributes.sequence)invalid('职级上下限无效');}
  if(all.some(e=>e.id!==c.id&&e.payload.name===c.name&&overlaps(e.payload as any,c)&&((c.kind==='position'&&e.orgId===c.orgId)||(c.kind==='org'&&e.payload.parentId===c.parentId))))invalid('同范围有效区间名称冲突');
  if(old&&overlaps(old.payload as any,c))invalid('有效版本区间重叠；请明确后续版本起止');
  const e=old?revise(old,c,c.status):make(c.kind,c.orgId,null,c,c.status,c.code);
  if(c.parentId){let parent=c.parentId,seen=new Set([e.id]);while(parent){if(seen.has(parent))invalid('目录上下级形成环');seen.add(parent);const p=all.find(x=>x.id===parent);if(!p)invalid('上级目录不存在');parent=overlaps(p.payload as any,c)?p.payload.parentId:'';}}
  if(c.status==='inactive'){
   const refs=await db.prepare("SELECT 1 FROM r1_m01_entities WHERE tenant_id=? AND id<>? AND status IN ('active','pending','approved','waiting','failed') AND (org_id=? OR json_extract(payload,'$.positionId')=? OR json_extract(payload,'$.parentId')=?) LIMIT 1").bind(tenant,e.id,e.id,e.id,e.id).first();
   if(refs)invalid('存在受保护的未完成依赖，请联系负责人','PROTECTED_DEPENDENCY');
  }
  changes.push(e);break;
 }
 case 'identityReview':{
  const person=await get(c.personId);if(person.kind!=='person')invalid('非人员身份');await authorize(person.orgId??'',person.id);
  if(new Set(c.candidateIds).size!==1||c.candidateIds[0]!==c.personId)invalid('多标识冲突，需身份复核','IDENTITY_REVIEW_REQUIRED');
  changes.push(make('identity_review',person.orgId,person.id,{...c,reviewerId:m.userId,reviewedAt:at},'confirmed'));break;
 }
 case 'template':{
  if(new Set(c.fields.map(f=>f.code)).size!==c.fields.length)invalid('模板字段重复');
  for(const f of c.fields)if(f.type==='number'&&(!f.unit||f.precision===undefined)||f.type==='enum'&&!f.options?.length)invalid('模板类型配置不完整');
  const old=c.id?await get(c.id):null;if(old&&old.kind!=='template')invalid('模板类型错误');
  changes.push(old?revise(old,c,'published'):make('template',c.orgId,null,c,'published'));break;
 }
 case 'person':{
  const template=await get(c.templateId);if(template.kind!=='template'||template.status!=='published'||template.orgId!==c.orgId||template.payload.entryType!==c.entryType)invalid('入口模板未配置','TEMPLATE_NOT_CONFIGURED');
  for(const f of template.payload.fields)await authorize(c.orgId,'',f.code);
  const values=templateValues(template,c.fields,'create');changes.push(make('person',c.orgId,null,{...c,fields:values,templateVersion:template.revision,invite:false},'draft',c.code));break;
 }
 case 'employment':{
  const person=await get(c.personId),review=await get(c.identityReviewId);if(person.kind!=='person'||review.kind!=='identity_review'||review.personId!==person.id||review.status!=='confirmed')invalid('缺少已核实的稳定身份','IDENTITY_REVIEW_REQUIRED');
  if(c.predecessorId){const old=await get(c.predecessorId);if(old.kind!=='employment'||old.personId!==person.id||old.status!=='ended'||old.payload.lastWorkingOn>=c.startOn)invalid('前任期无效');}
  if((await rows(db,tenant,'employment',person.id)).some(e=>['pending','active'].includes(e.status)))invalid('已有未结束雇佣段');
  changes.push(make('employment',c.orgId,person.id,{...c,accountRestored:false,lastWorkingOn:null},'pending'));break;
 }
 case 'assignmentRequest':case 'exitRequest':{
  const person=await get(c.personId);if(person.kind!=='person')invalid('人员不存在');
  const reviewer=await db.prepare('SELECT user_id AS userId,tenant_id AS tenantId,role,employee_id AS employeeId,org_scope AS orgScope,view_email AS viewEmail,view_level AS viewLevel,active FROM hris_memberships WHERE tenant_id=? AND user_id=? AND active=1').bind(tenant,c.reviewerId).first<Member>();
  if(!reviewer||reviewer.userId===m.userId||reviewer.employeeId===person.id||!['hr','admin'].includes(reviewer.role)||!scopedOrgs(state,reviewer).has(c.orgId))invalid('缺少独立且覆盖范围的审核HR');
  if(c.operation==='assignmentRequest'){const employment=await get(c.employmentId);if(employment.kind!=='employment'||employment.personId!==person.id||!['pending','active'].includes(employment.status)||c.validTo&&c.validTo<c.validFrom)invalid('雇佣或任职区间无效');if(c.type!=='primary'&&!c.homePrimaryId)invalid('非主职必须关联派出主职');}
  const pending=await db.prepare("SELECT 1 FROM r1_m01_entities WHERE tenant_id=? AND person_id=? AND kind IN ('assignment_request','exit_request') AND status IN ('pending','approved','failed') LIMIT 1").bind(tenant,person.id).first();if(pending)invalid('已有在途人事事项');
  changes.push(make(c.operation==='assignmentRequest'?'assignment_request':'exit_request',c.orgId,person.id,{...c,createdBy:m.userId,attempts:0,effectStatus:'waiting'},'pending'));break;
 }
 case 'assignmentApprove':case 'exitApprove':{
  const e=await get(c.id);if(e.kind!==(c.operation==='assignmentApprove'?'assignment_request':'exit_request')||e.status!=='pending'||e.payload.reviewerId!==m.userId||e.payload.createdBy===m.userId||e.personId===m.employeeId)invalid('审核角色或原单状态无效');changes.push(revise(e,{approvedBy:m.userId,approvedAt:at},'approved'));break;
 }
 case 'assignmentExecute':{
  const e=await get(c.id),p=e.payload;if(e.kind!=='assignment_request'||!['approved','failed'].includes(e.status))invalid('原单非已批准待执行');
  if(today<p.validFrom)invalid('未到生效日期，不增加尝试');
  let failure:string|null=null;
  try{const position=await activeCatalog(p.positionId,'position');await activeCatalog(p.orgId,'org');if(position.orgId!==p.orgId)invalid('职位不属于目标组织');
   const assignments=await rows(db,tenant,'assignment',e.personId!);
   if(assignments.some(a=>a.status==='active'&&overlaps(a.payload as any,p as {validFrom:string;validTo:string|null})&&(p.type==='primary'&&a.payload.type==='primary'||a.payload.type===p.type&&a.payload.positionId===p.positionId)))invalid('存在重叠任职');
   if(p.type!=='primary'){const home=await get(p.homePrimaryId);if(home.kind!=='assignment'||home.personId!==e.personId||home.status!=='active'||home.payload.type!=='primary')invalid('派出主职无效');}
   if(p.type==='primary'){const plans=await db.prepare("SELECT payload FROM hris_development_records WHERE tenant_id=? AND kind='staffingPlan' AND position_id=? AND status='approved' AND json_extract(payload,'$.start')<=? AND json_extract(payload,'$.end')>=? LIMIT 201").bind(tenant,p.positionId,today,today).all();if(plans.results.length>200)invalid('编制版本待核');
    const active=plans.results.map((x:any)=>JSON.parse(x.payload)).filter((x:any,_i:number,a:any[])=>!a.some(y=>y.supersedes===x.id));
    const usage=await db.prepare("SELECT COUNT(*) n FROM r1_m01_entities WHERE tenant_id=? AND kind='assignment' AND status='active' AND json_extract(payload,'$.type')='primary' AND json_extract(payload,'$.positionId')=?").bind(tenant,p.positionId).first<{n:number}>();
    if(active.length&&usage!.n>=Math.min(...active.map((x:any)=>x.headcount)))invalid('目标编制已满');
   }
  }catch(error){if(!(error instanceof HttpError)||error.status>=500)throw error;failure=error.message;}
  changes.push(revise(e,{attempts:p.attempts+1,lastAttemptAt:at,effectStatus:failure?'failed':'applied',failure,appliedAt:failure?null:at},failure?'failed':'applied'));
  if(failure){result.effectStatus='failed';result.reasonCode='BUSINESS_FAILED';break;}
  const assignment=make('assignment',e.orgId,e.personId,{...p,validFrom:today,appliedAt:at,occupancy:p.type==='primary'?1:0,approvalId:e.id});changes.push(assignment);
  const employment=await get(p.employmentId);if(employment.status==='pending')changes.push(revise(employment,{actualStartedAt:at},'active'));
  result.assignmentId=assignment.id;result.effectStatus='applied';break;
 }
 case 'exitExecute':{
  const e=await get(c.id);if(e.kind!=='exit_request'||e.status!=='approved')invalid('退出原单不可执行');if(today<nextDay(e.payload.lastWorkingOn))invalid('未到最后工作日次日');
  const employment=await rows(db,tenant,'employment',e.personId!),assignments=await rows(db,tenant,'assignment',e.personId!);
  if(employment.length+assignments.length>30)throw new HttpError(503,'需有界退出计划','BOUNDED_QUERY_REQUIRED');
  changes.push(revise(e,{appliedAt:at,effectStatus:'applied',cleanupStatus:'pending'},'applied'));
  for(const x of [...employment,...assignments].filter(x=>x.status==='active'))changes.push(revise(x,{lastWorkingOn:e.payload.lastWorkingOn,validTo:today,endedAt:at,occupancy:0},'ended'));
  extra.push(token=>[db.prepare('INSERT INTO r1_exit_fences(tenant_id,person_id,effective_at,command_id) SELECT owner,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=?').bind(e.personId,at,intent.commandId,tenant,token)]);
  extra.push(token=>[db.prepare("INSERT INTO r1_exit_cleanup(tenant_id,person_id,business_type,business_id) SELECT e.tenant_id,e.person_id,e.kind,e.id FROM r1_m01_entities e JOIN hris_workspaces w ON w.owner=e.tenant_id WHERE e.tenant_id=? AND e.person_id=? AND e.id<>? AND e.status IN ('pending','approved','failed') AND w.last_mutation=? ON CONFLICT DO NOTHING").bind(tenant,e.personId,e.id,token)]);
  result.cleanupStatus='pending';break;
 }
 case 'contract':{
  const legal=await activeCatalog(c.legalEntityId,'legal_entity'),attrs=legal.payload.attributes;
  if(!attrs.orgIds?.includes(c.orgId)&&!attrs.extraPersonIds?.includes(c.personId))invalid('法人适用范围未配置或不匹配');
  if(c.end&&c.end<c.start||c.contractType==='fixed'&&!c.end||c.contractType==='open'&&c.end)invalid('合同期限无效');
  const contracts=await rows(db,tenant,'contract',c.personId);
  if(contracts.some(e=>e.id!==c.id&&e.code===c.number.toLowerCase()))invalid('合同编号已存在');
  if(c.renewalOf){const old=await get(c.renewalOf);if(old.kind!=='contract'||old.personId!==c.personId||old.payload.legalEntityId!==c.legalEntityId||!['signed','ended'].includes(old.status)||!old.payload.end&&!old.payload.endedOn||c.start!==nextDay(old.payload.endedOn??old.payload.end))invalid('续签必须同人同法人且相邻日');}
  const old=c.id?await get(c.id):null;if(old&&(old.kind!=='contract'||old.personId!==c.personId||old.status!=='draft'))invalid('仅同人草稿可修订');
  const payload={...c,legalVersion:legal.revision,legalName:legal.payload.name,externalSigningStatus:'not_configured',createdBy:old?.payload.createdBy??m.userId};
  changes.push(old?revise(old,payload):make('contract',c.orgId,c.personId,payload,'draft',c.number.toLowerCase()));break;
 }
 case 'contractSign':case 'contractEnd':{
  const e=await get(c.id);if(e.kind!=='contract')invalid('非合同对象');
  if(c.operation==='contractSign'){if(e.status!=='draft'||c.signedOn>today)invalid('签署登记状态或日期无效');const contracts=await rows(db,tenant,'contract',e.personId!);
   if(contracts.some(x=>x.id!==e.id&&x.payload.legalEntityId===e.payload.legalEntityId&&['signed','ended'].includes(x.status)&&overlaps({validFrom:x.payload.start,validTo:x.payload.endedOn??x.payload.end},{validFrom:e.payload.start,validTo:e.payload.end})))invalid('同人同法人存在重叠已签合同');changes.push(revise(e,{...c,signRecordedBy:m.userId},'signed'));
  }else{if(e.status!=='signed'||m.userId===e.payload.createdBy||m.employeeId===e.personId||c.endedOn>today||c.endedOn<e.payload.start||e.payload.end&&c.endedOn>e.payload.end)invalid('终止须由独立HR核有效日期');changes.push(revise(e,{...c,endedBy:m.userId},'ended'));}break;
 }
 case 'subsetImport':{
  const t=await get(c.templateId);if(t.kind!=='template'||t.status!=='published'||t.revision!==c.templateVersion||t.orgId!==c.orgId||t.payload.entryType!=='subset')invalid('模板版本已变化','REVISION_CONFLICT');
  for(const name of Object.keys(c.fields))await authorize(c.orgId,c.personId,name);
  const inputDigest=await digest(c),receipt=await db.prepare('SELECT request_digest AS requestDigest,entity_id AS entityId FROM r1_import_receipts WHERE tenant_id=? AND batch_id=? AND row_no=? AND attempt_version=?').bind(tenant,c.batchId,c.rowNo,c.attemptVersion).first<{requestDigest:string;entityId:string}>();
  if(receipt){if(receipt.requestDigest!==inputDigest)throw new HttpError(409,'同批次行内容冲突','IDEMPOTENCY_CONFLICT');return {commandId:intent.commandId,status:'committed',result:{ids:[receipt.entityId]},workspaceRevision:ctx.row.revision,replayed:true};}
  const old=c.recordId?await get(c.recordId):null;if(c.mode==='update'&&(!old||old.kind!=='subset'||old.personId!==c.personId||old.payload.templateId!==t.id))invalid('更新对象不匹配');
  const values=templateValues(t,c.fields,c.mode,old?.payload.fields),keys=t.payload.fields.filter((f:any)=>f.uniqueKey).map((f:any)=>f.code);
  const existing=await rows(db,tenant,'subset',c.personId);if(keys.length&&existing.some(e=>e.id!==old?.id&&e.status==='active'&&e.payload.templateId===t.id&&keys.every((k:string)=>e.payload.fields[k]===values[k])))invalid('子集唯一键重复');
  const payload={...c,fields:values};const row=old?revise(old,payload):make('subset',c.orgId,c.personId,payload);changes.push(row);
  extra.push(token=>[db.prepare('INSERT INTO r1_import_receipts SELECT owner,?,?,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=?').bind(c.batchId,c.rowNo,c.attemptVersion,inputDigest,row.id,tenant,token)]);break;
 }
 }
 result.ids=changes.map(e=>e.id);
 return commitCommand(db,m,stamp,intent,token=>[...changes.flatMap(e=>m01Write(db,tenant,token,e,intent.commandId,at)),...extra.flatMap(fn=>fn(token))],result);
}
