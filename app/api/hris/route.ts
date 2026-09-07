import {memberContext as context} from '@/lib/hris/context';
import {commitState} from '@/lib/hris/repository';
import {HttpError} from '@/lib/hris/http';
import { applyCommand, type State } from '@/lib/hris/model';
import { scopedOrgs, visibleState, authorizeCommand, AccessError, type Member } from '@/lib/hris/authorization';
export const dynamic='force-dynamic';
const headers={'Cache-Control':'no-store'};
function json(body:unknown,status=200){return Response.json(body,{status,headers});}
export async function GET(){try{const c=await context();if(!c)return json({error:'请先登录'},401);return json({state:visibleState(JSON.parse(c.row.data),c.member),revision:c.row.revision,role:c.member.role,userId:c.member.userId,storageVersion:c.row.storageVersion,permissions:{viewEmail:c.member.role==='admin'||!!c.member.viewEmail,viewLevel:c.member.role==='admin'||!!c.member.viewLevel}});}catch(e){if(e instanceof HttpError)return json({error:e.message},e.status);if(e instanceof AccessError)return json({error:e.message},403);return json({error:'数据暂时无法读取，请稍后重试'},503);}}
export async function POST(request:Request){
 const origin=request.headers.get('origin');if(!origin||new URL(request.url).origin!==origin)return json({error:'请求来源无效'},403);
 if(!request.headers.get('content-type')?.toLowerCase().startsWith('application/json'))return json({error:'请求格式无效'},415);
 try{
 const c=await context();if(!c)return json({error:'请先登录'},401);
 // Stream the request with a hard cap before decoding JSON.
 const reader=request.body?.getReader();if(!reader)return json({error:'请求为空'},400);
 const chunks:Uint8Array[]=[];let size=0;while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>32768){await reader.cancel();return json({error:'请求内容过大'},413);}chunks.push(value);}
 const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
 let body;try{body=JSON.parse(new TextDecoder().decode(bytes));}catch{return json({error:'请求格式无效'},400);}
 if(!body||!Number.isSafeInteger(body.revision)||body.revision<0)return json({error:'版本号无效'},400);
 if(c.row.storageVersion!==1)return json({error:'请由管理员先完成数据升级'},409);
 if(body.revision!==c.row.revision)return json({error:'数据已更新，请刷新后重试'},409);
 let next:State;try{const state=JSON.parse(c.row.data);const command=authorizeCommand(state,body.command,c.member);
 if(command.action==='workflow'||command.action==='request'){const steps=command.action==='workflow'?command.steps:state.workflows?.[command.kind]?.steps;for(const step of steps??[]){const reviewer=await c.db.prepare("SELECT m.user_id,m.employee_id,m.role,m.org_scope AS orgScope,g.name FROM hris_memberships m JOIN hris_access_grants g ON g.claimed_by=m.user_id AND g.tenant_id=m.tenant_id WHERE m.user_id=? AND m.tenant_id=? AND m.active=1 AND m.role IN ('admin','manager','approver')").bind(step.userId,c.member.tenantId).first<{user_id:string;employee_id:string|null;name:string;role:Member['role'];orgScope:string}>();if(!reviewer)throw Error('流程审批人必须是已激活的有效管理员或审批人');if(command.action==='workflow')step.name=reviewer.name;if(command.action==='request'&&reviewer.role!=='admin'&&!scopedOrgs(state,{...c.member,role:reviewer.role,orgScope:reviewer.orgScope}).has(state.employees.find((e:State['employees'][number])=>e.id===command.employeeId)?.orgId??''))throw Error('审批人的组织权限不覆盖该员工，请先调整流程或成员授权');if(command.action==='request'&&reviewer.employee_id===command.employeeId)throw Error('流程审批人不能审批本人异动');}}
 next=applyCommand(state,command,new Date().toISOString(),c.member.userId);}catch(e){if(e instanceof AccessError)throw e;return json({error:e instanceof Error?e.message:'参数无效'},400);}
 const saved=await commitState(c.db,c.member,c.row.revision,JSON.parse(c.row.data),next);
 if(!saved)return json({error:'权限或数据已变化，请刷新'},409);
 return json({state:visibleState(next,c.member),revision:c.row.revision+1,role:c.member.role,userId:c.member.userId,storageVersion:c.row.storageVersion,permissions:{viewEmail:c.member.role==='admin'||!!c.member.viewEmail,viewLevel:c.member.role==='admin'||!!c.member.viewLevel}});
 }catch(e){if(e instanceof HttpError)return json({error:e.message},e.status);if(e instanceof AccessError)return json({error:e.message},403);return json({error:'保存失败，请重试'},503);}
}
