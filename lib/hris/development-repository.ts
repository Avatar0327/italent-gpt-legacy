import {memberContext} from './context';
import {HttpError} from './http';
import type {State} from './model';
import {visibleRecord,projectRecord,type DevelopmentRecord} from './development';
export async function developmentContext(){
 const ctx=await memberContext();if(!ctx.row||ctx.row.storageVersion!==1)throw new HttpError(409,'请先完成企业数据迁移');
 const result=await ctx.db.batch([
  ctx.db.prepare('SELECT id,kind,employee_id AS employeeId,position_id AS positionId,reference_id AS referenceId,status,payload,created_by AS createdBy,created_at AS createdAt,updated_at AS updatedAt FROM hris_development_records WHERE tenant_id=? ORDER BY created_at,id').bind(ctx.member.tenantId),
  ctx.db.prepare('SELECT revision FROM hris_workspaces WHERE owner=?').bind(ctx.member.tenantId),
 ]);
 // Core scope and extension documents must describe the same revision. A concurrent
 // personnel move or role change invalidates the complete read, including downloads.
 if((result[1].results[0] as {revision:number})?.revision!==ctx.row.revision)throw new HttpError(409,'数据或权限已变化，请刷新');
 const records=(result[0].results as (Omit<DevelopmentRecord,'payload'>&{payload:string})[]).map(v=>({...v,payload:JSON.parse(v.payload)})) as DevelopmentRecord[];
 return {...ctx,state:JSON.parse(ctx.row.data) as State,records};
}
export type DevelopmentContext=Awaited<ReturnType<typeof developmentContext>>;
export function visibleDevelopment(ctx:DevelopmentContext){return ctx.records.filter(r=>visibleRecord(r,ctx.records,ctx.state,ctx.member)).map(r=>projectRecord(r,ctx.member));}
// Every state mutation and audit event share one revision-guarded D1 transaction.
// Callbacks receive a fresh, unique token; zero CAS changes make all later writes no-ops.
export async function commitExtension(ctx:DevelopmentContext,revision:number,action:string,subject:string,statements:(token:string)=>D1PreparedStatement[]){
 if(revision!==ctx.row.revision)throw new HttpError(409,'数据已更新，请刷新后重试');
 const {db,member:m}=ctx,token=crypto.randomUUID(),at=new Date().toISOString();
 const result=await db.batch([
  db.prepare('UPDATE hris_workspaces SET revision=revision+1,last_mutation=? WHERE owner=? AND revision=? AND storage_version=1 AND EXISTS (SELECT 1 FROM hris_memberships WHERE user_id=? AND tenant_id=? AND active=1 AND role=?)').bind(token,m.tenantId,revision,m.userId,m.tenantId,m.role),
  ...statements(token),
  db.prepare('INSERT INTO hris_audit_events(tenant_id,id,actor_id,action,subject,at,revision) SELECT owner,?,?,?,?,?,revision FROM hris_workspaces WHERE owner=? AND last_mutation=?').bind(token,m.userId,action,subject,at,m.tenantId,token),
 ]);if(!result[0].meta.changes)throw new HttpError(409,'数据或权限已变化，请刷新');
}
export async function saveDevelopment(ctx:DevelopmentContext,revision:number,r:DevelopmentRecord,action:string){
 await commitExtension(ctx,revision,action,`${r.kind} · ${r.id}`,token=>[
 ctx.db.prepare('INSERT INTO hris_development_records(tenant_id,id,kind,employee_id,position_id,reference_id,status,payload,created_by,created_at,updated_at) SELECT owner,?,?,?,?,?,?,?,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=? ON CONFLICT(tenant_id,id) DO UPDATE SET status=excluded.status,reference_id=excluded.reference_id,payload=excluded.payload,updated_at=excluded.updated_at').bind(r.id,r.kind,r.employeeId,r.positionId,r.referenceId,r.status,JSON.stringify(r.payload),r.createdBy,r.createdAt,r.updatedAt,ctx.member.tenantId,token),
 ctx.db.prepare('INSERT INTO hris_development_events(tenant_id,id,record_id,revision,action,actor_id,at,snapshot) SELECT owner,?,?,revision,?,?,?,? FROM hris_workspaces WHERE owner=? AND last_mutation=?').bind(token,r.id,action,ctx.member.userId,r.updatedAt,JSON.stringify(r),ctx.member.tenantId,token),
 ]);
}
