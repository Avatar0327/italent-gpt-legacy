import { commandSchema, type State } from './model.ts';
export type Member = {userId:string;tenantId:string;role:'admin'|'hr'|'manager'|'approver'|'employee';employeeId:string|null;active:boolean|number;orgScope?:string|string[];viewEmail?:boolean|number;viewLevel?:boolean|number};
export class AccessError extends Error {}
export function requireMember(member:Member|null|undefined):asserts member is Member {
 if(!member?.active||!['admin','hr','manager','approver','employee'].includes(member.role))throw new AccessError('尚未配置有效的企业成员权限，请联系系统管理员');
}
export function scopedOrgs(state:State,member:Member){
 if(member.role==='admin')return new Set(state.orgs.map(o=>o.id));
 let roots:unknown=member.orgScope??[];if(typeof roots==='string'){try{roots=JSON.parse(roots);}catch{roots=[];}}
 const scope=new Set<string>(Array.isArray(roots)?roots.filter((v):v is string=>typeof v==='string'):[]);
 let changed=true;while(changed){changed=false;for(const o of state.orgs)if(o.parentId&&scope.has(o.parentId)&&!scope.has(o.id)){scope.add(o.id);changed=true;}}
 return scope;
}
export function permittedEmployeeIds(state:State,member:Member){
 const scope=scopedOrgs(state,member);
 const assigned=new Set(state.approvals.filter(a=>a.steps?.some(s=>s.userId===member.userId)).map(a=>a.employeeId));
 return new Set(state.employees.filter(e=>member.role==='admin'||(member.role==='employee'?e.id===member.employeeId:scope.has(e.orgId)&&(member.role!=='approver'||assigned.has(e.id)))).map(e=>e.id));
}
export function visibleState(state:State,member:Member):State {
 requireMember(member);if(member.role==='admin')return state;
 const ids=permittedEmployeeIds(state,member),scope=scopedOrgs(state,member);
 const employees=state.employees.filter(e=>ids.has(e.id)).map(e=>({...e,email:member.viewEmail?e.email:'',level:member.viewLevel?e.level:''}));
 const approvals=state.approvals.filter(a=>ids.has(a.employeeId)&&(member.role!=='approver'||a.steps?.some(s=>s.userId===member.userId)));
 const allowedOrgs=new Set(member.role==='employee'?employees.map(e=>e.orgId):[...scope]);
 return {employees,orgs:state.orgs.filter(o=>allowedOrgs.has(o.id)).map(o=>({...o,parentId:allowedOrgs.has(o.parentId)?o.parentId:'',leader:member.role==='employee'?'':o.leader})),approvals,audit:[],workflows:undefined};
}
export function authorizeCommand(state:State,input:unknown,member:Member){
 requireMember(member);const c=commandSchema.parse(input);const scope=scopedOrgs(state,member);
 const allowedEmployee=(id:string)=>{const e=state.employees.find(e=>e.id===id);return !!e&&(member.role==='admin'||(member.role==='employee'?e.id===member.employeeId:scope.has(e.orgId)));};
 if(c.action==='workflow'){if(member.role!=='admin')throw new AccessError('仅管理员可配置流程');
 }else if(c.action==='withdraw'){
 const a=state.approvals.find(a=>a.id===c.id);if(!a||a.createdBy!==member.userId||!allowedEmployee(a.employeeId))throw new AccessError('仅具有数据权限的申请人可撤回');
 }else if(c.action==='decide'){
 if(!['admin','manager','approver'].includes(member.role))throw new AccessError('没有审批权限');
 const a=state.approvals.find(a=>a.id===c.id);
 if(!a||!allowedEmployee(a.employeeId))throw new AccessError('没有此员工的数据权限');
 if(a.steps?.length&&a.steps[a.currentStep??0]?.userId!==member.userId)throw new AccessError('尚未轮到当前审批人');
 if(!a.createdBy||a.createdBy===member.userId||a.employeeId===member.employeeId)throw new AccessError('不能审批本人申请、本人异动或缺少申请人记录的历史申请');
 }else if(c.action==='request'){
 if(member.role==='approver'||!allowedEmployee(c.employeeId))throw new AccessError('没有此员工的申请权限');
 if(c.kind==='transfer'&&member.role!=='admin'&&!scope.has(c.orgId))throw new AccessError('没有调入组织的数据权限');
 }else if(c.action==='employee'){
 if(!['admin','hr'].includes(member.role)||!scope.has(c.orgId)||(c.id&&!allowedEmployee(c.id)))throw new AccessError('没有此员工或组织的维护权限');
 const old=state.employees.find(e=>e.id===c.id);
 for(const field of ['email','level'] as const){const allowed=member.role==='admin'||(field==='email'?member.viewEmail:member.viewLevel);if(!allowed){if(c[field]&&c[field]!==old?.[field])throw new AccessError('没有该字段的修改权限');c[field]=old?.[field]??'';}}
 }else{
 const old=state.orgs.find(o=>o.id===c.id);
 if(member.role==='hr'&&old&&old.parentId&&!scope.has(old.parentId)&&c.parentId==='')c.parentId=old.parentId;
 if(!['admin','hr'].includes(member.role)||(member.role!=='admin'&&((c.id&&!scope.has(c.id))||(!c.id&&!scope.has(c.parentId))||(old&&c.parentId!==old.parentId&&!scope.has(c.parentId)))))throw new AccessError('没有此组织的维护权限');
 }
 return c;
}
