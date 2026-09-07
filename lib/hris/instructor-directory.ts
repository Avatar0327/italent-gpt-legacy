import {z} from 'zod';
import {HttpError} from './http';
import {scopedOrgs,type Member} from './authorization';
import {visibleRecord,type DevelopmentRecord as R} from './development';
import type {State} from './model';
const id=z.string().min(1).max(100),evidence=z.string().trim().min(5).max(2000);
const command=z.discriminatedUnion('action',[
 z.object({action:z.literal('nominate'),employeeId:id,title:z.string().trim().min(1).max(100),description:z.string().trim().min(5).max(1000),evidence}),
 z.object({action:z.literal('review'),id,accepted:z.boolean(),evidence}),
 z.object({action:z.literal('withdraw'),id,evidence}),
 z.object({action:z.literal('suspend'),id,evidence})
]);
export function applyInstructorDirectory(records:R[],state:State,member:Member,input:unknown,at=new Date().toISOString()):R{
 const c=command.parse(input),scope=scopedOrgs(state,member),hr=['admin','hr'].includes(member.role);
 const deny=(message:string):never=>{throw new HttpError(403,message);},fail=(message:string):never=>{throw new HttpError(400,message);};
 if(!hr)deny('仅有权限的HR可办理内部讲师名册');
 const employee=(employeeId:string)=>{const e=state.employees.find(e=>e.id===employeeId);if(!e||!scope.has(e.orgId))deny('没有此员工的讲师名册权限');return e!;};
 if(c.action==='nominate'){
  const e=employee(c.employeeId);if(e.status==='离职')fail('离职员工不能提名为内部讲师');
  const previous=records.filter(r=>r.kind==='instructorProfile'&&r.employeeId===e.id);
  if(previous.some(r=>['submitted','active'].includes(r.status)))fail('此员工已有待复核或在用的讲师记录');
  const latest=previous.sort((a,b)=>(b.payload.version??1)-(a.payload.version??1))[0];
  return {id:crypto.randomUUID(),kind:'instructorProfile',employeeId:e.id,positionId:null,referenceId:null,status:'submitted',createdBy:member.userId,createdAt:at,updatedAt:at,payload:{name:e.name,title:c.title,description:c.description,evidence:c.evidence,version:(latest?.payload.version??0)+1,...(latest?{supersedes:latest.id}:{})}};
 }
 const r=records.find(r=>r.kind==='instructorProfile'&&r.id===c.id);if(!r||!visibleRecord(r,records,state,member))deny('讲师记录不存在或没有访问权限');const record=r!,e=employee(record.employeeId!);
 const change=(status:string,payload:R['payload']):R=>({...record,status,updatedAt:at,payload:{...record.payload,...payload}});
 if(c.action==='withdraw'){if(record.createdBy!==member.userId)deny('仅提名人可撤回');if(record.status!=='submitted')fail('仅待复核提名可撤回');return change('withdrawn',{closedReason:c.evidence});}
 if(e.id===member.employeeId)deny('不能复核或停用本人的讲师身份');
 if(c.action==='review'){
  if(record.createdBy===member.userId)deny('须由其他HR独立复核提名');if(record.status!=='submitted')fail('提名已经处理');
  if(c.accepted){if(e.status==='离职')fail('员工已离职，不能通过讲师提名');if(records.some(x=>x.kind==='instructorProfile'&&x.id!==record.id&&x.employeeId===e.id&&x.status==='active'))fail('员工已有在用的讲师记录');}
  return change(c.accepted?'active':'rejected',{verification:c.evidence,verifiedBy:member.userId,verifiedAt:at});
 }
 if(record.status!=='active')fail('仅在用的讲师记录可以停用');return change('suspended',{closedReason:c.evidence,revokedBy:member.userId,revokedAt:at});
}
