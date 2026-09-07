import { commandSchema, type State } from './model.ts';
export type Member = {userId:string;tenantId:string;role:'admin'|'hr'|'approver'|'employee';employeeId:string|null;active:boolean|number};
export class AccessError extends Error {}
export function requireMember(member:Member|null|undefined):asserts member is Member {
 if(!member?.active||!['admin','hr','approver','employee'].includes(member.role))throw new AccessError('尚未配置有效的企业成员权限，请联系系统管理员');
}
export function visibleState(state:State, member:Member):State {
 requireMember(member);
 if(member.role==='admin'||member.role==='hr')return state;
 if(member.role==='approver')return {...state,audit:[]};
 const employees=state.employees.filter(e=>e.id===member.employeeId);
 return {employees,orgs:state.orgs.filter(o=>employees.some(e=>e.orgId===o.id)),approvals:state.approvals.filter(a=>a.employeeId===member.employeeId),audit:[]};
}
export function authorizeCommand(state:State,input:unknown,member:Member){
 requireMember(member);const c=commandSchema.parse(input);
 if(c.action==='workflow'){if(member.role!=='admin')throw new AccessError('仅管理员可配置流程');
 }else if(c.action==='withdraw'){const a=state.approvals.find(a=>a.id===c.id);if(!a||a.createdBy!==member.userId)throw new AccessError('仅申请人可撤回');
 }else if(c.action==='decide'){
  if(!['admin','approver'].includes(member.role))throw new AccessError('没有审批权限');
  const a=state.approvals.find(a=>a.id===c.id);
  if(a?.steps?.length&&a.steps[a.currentStep??0]?.userId!==member.userId)throw new AccessError('尚未轮到当前审批人');
  if(a&&(!a.createdBy||a.createdBy===member.userId||a.employeeId===member.employeeId))throw new AccessError('不能审批本人申请、本人异动或缺少申请人记录的历史申请');
 }else if(c.action==='request'){
  if(member.role==='approver'||(member.role==='employee'&&c.employeeId!==member.employeeId))throw new AccessError('没有此员工的申请权限');
 }else if(!['admin','hr'].includes(member.role))throw new AccessError('没有维护档案或组织的权限');
 return c;
}
