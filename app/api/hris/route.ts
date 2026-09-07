import { getChatGPTUser } from '@/app/chatgpt-auth';
import { env } from 'cloudflare:workers';
import { applyCommand, type State } from '@/lib/hris/model';
import { requireMember, visibleState, authorizeCommand, AccessError, type Member } from '@/lib/hris/authorization';
export const dynamic='force-dynamic';
const headers={'Cache-Control':'no-store'};
function json(body:unknown,status=200){return Response.json(body,{status,headers});}
async function context(){
 const user=await getChatGPTUser();if(!user)return null;
 const db=env.DB;if(!db)throw Error('DB unavailable');
 const member=await db.prepare('SELECT user_id AS userId,tenant_id AS tenantId,role,employee_id AS employeeId,active FROM hris_memberships WHERE user_id = ?').bind(user.id).first<Member>();
 requireMember(member);
 const row=await db.prepare('SELECT data,revision FROM hris_workspaces WHERE owner = ?').bind(member.tenantId).first<{data:string;revision:number}>();
 if(!row)throw Error('Tenant unavailable');return {db,member,row};
}
export async function GET(){try{const c=await context();if(!c)return json({error:'请先登录'},401);return json({state:visibleState(JSON.parse(c.row.data),c.member),revision:c.row.revision,role:c.member.role});}catch(e){if(e instanceof AccessError)return json({error:e.message},403);return json({error:'数据暂时无法读取，请稍后重试'},503);}}
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
 if(body.revision!==c.row.revision)return json({error:'数据已更新，请刷新后重试'},409);
 let next:State;try{const state=JSON.parse(c.row.data);const command=authorizeCommand(state,body.command,c.member);next=applyCommand(state,command,new Date().toISOString(),c.member.userId);}catch(e){if(e instanceof AccessError)throw e;return json({error:e instanceof Error?e.message:'参数无效'},400);}
 const event=next.audit[0];
 // D1 batch is transactional. The mutation token prevents an audit entry on a failed CAS.
 const results=await c.db.batch([
 c.db.prepare('UPDATE hris_workspaces SET data = ?,revision = revision + 1,last_mutation = ? WHERE owner = ? AND revision = ?').bind(JSON.stringify(next),event.id,c.member.tenantId,c.row.revision),
 c.db.prepare('INSERT INTO hris_audit_events (tenant_id,id,actor_id,action,subject,at,revision) SELECT owner,?,?,?,?,?,revision FROM hris_workspaces WHERE owner = ? AND last_mutation = ?').bind(event.id,c.member.userId,event.action,event.subject,event.at,c.member.tenantId,event.id),
 ]);
 if(!results[0].meta.changes)return json({error:'数据已被其他会话更新，请刷新'},409);
 return json({state:visibleState(next,c.member),revision:c.row.revision+1,role:c.member.role});
 }catch(e){if(e instanceof AccessError)return json({error:e.message},403);return json({error:'保存失败，请重试'},503);}
}
