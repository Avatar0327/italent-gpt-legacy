import { getChatGPTUser } from '@/app/chatgpt-auth';
import { env } from 'cloudflare:workers';
import { requireMember, type Member } from './authorization';
import { HttpError } from './http';
export async function identity(){const user=await getChatGPTUser();if(!user)throw new HttpError(401,'请先登录');if(!env.DB)throw Error('DB unavailable');return {user,db:env.DB};}
export async function memberContext(admin=false){
 const {user,db}=await identity();
 const member=await db.prepare('SELECT user_id AS userId,tenant_id AS tenantId,role,employee_id AS employeeId,active FROM hris_memberships WHERE user_id=?').bind(user.id).first<Member>();
 requireMember(member);if(admin&&member.role!=='admin')throw new HttpError(403,'仅系统管理员可管理成员');
 const row=await db.prepare('SELECT data,revision FROM hris_workspaces WHERE owner=?').bind(member.tenantId).first<{data:string;revision:number}>();
 if(!row)throw Error('Tenant unavailable');return {user,db,member,row};
}
