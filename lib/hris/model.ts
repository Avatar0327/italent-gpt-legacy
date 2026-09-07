import { z } from 'zod';
export type Org = {id:string;name:string;parentId:string;city:string;leader:string;status:string};
export type Employee = {id:string;code:string;name:string;orgId:string;job:string;level:string;joined:string;status:string;email:string};
export type ApprovalStep={userId:string;name:string;decision?:'approved'|'rejected';at?:string};
export type Workflow={version:number;steps:{userId:string;name:string}[]};
export type Approval = {id:string;employeeId:string;kind:'transfer'|'regularize'|'exit';orgId:string;reason:string;status:'pending'|'approved'|'rejected'|'withdrawn';steps?:ApprovalStep[];currentStep?:number;workflowVersion?:number;created:string;createdBy?:string;decidedBy?:string;decided?:string};
export type Audit = {id:string;action:string;subject:string;at:string;actorId?:string};
export type State = {orgs:Org[];employees:Employee[];approvals:Approval[];audit:Audit[];workflows?:Partial<Record<Approval['kind'],Workflow>>};
const text=z.string().trim().min(1).max(100);
const isoDate=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>!Number.isNaN(Date.parse(v))&&new Date(v).toISOString().startsWith(v),'日期无效');
export const commandSchema=z.discriminatedUnion('action',[
 z.object({action:z.literal('employee'),id:z.string().optional(),code:text,name:text,orgId:text,job:text,level:z.string().trim().max(100),joined:isoDate,email:z.union([z.literal(''),z.string().email()])}),
 z.object({action:z.literal('org'),id:z.string().optional(),name:text,parentId:z.string(),city:text,leader:z.string().max(100),status:z.enum(['启用','停用'])}),
 z.object({action:z.literal('request'),employeeId:text,kind:z.enum(['transfer','regularize','exit']),orgId:z.string(),reason:z.string().trim().min(2).max(500)}),
 z.object({action:z.literal('workflow'),kind:z.enum(['transfer','regularize','exit']),steps:z.array(z.object({userId:text,name:text})).min(1).max(5).refine(v=>new Set(v.map(s=>s.userId)).size===v.length,'审批人不能重复')}),
 z.object({action:z.literal('withdraw'),id:text}),
 z.object({action:z.literal('decide'),id:text,decision:z.enum(['approved','rejected'])}),
]);
export function initialState():State {
 const orgs=[{id:'o1',name:'星海科技集团',parentId:'',city:'上海',leader:'陈予安',status:'启用'},...['人力资源中心','产品研发中心','商业运营中心','财务管理中心'].map((name,i)=>({id:'o'+(i+2),name,parentId:'o1',city:['上海','深圳','北京','上海'][i],leader:['林知夏','周启明','沈远舟','许清禾'][i],status:'启用'}))];
 const names=['林知夏','周启明','沈远舟','许清禾','陈予安','苏以宁','陆景行','江念初','顾星河','温书言','程见微','叶明川'];
 return {orgs,employees:names.map((name,i)=>({id:'e'+(i+1),code:'HX'+String(1001+i),name,orgId:'o'+(2+i%4),job:['人才发展经理','产品经理','区域运营经理','财务分析师'][i%4],level:['P6','P7','P6','P5'][i%4],joined:`2026-0${1+i%8}-01`,status:i>8?'试用':'正式',email:`demo${i+1}@example.com`})),approvals:[{id:'a1',employeeId:'e10',kind:'regularize',orgId:'o3',reason:'试用期目标完成，申请转正。',status:'pending',created:'2026-09-07T08:30:00.000Z'},{id:'a2',employeeId:'e7',kind:'transfer',orgId:'o2',reason:'参与集团人才发展项目，申请内部调动。',status:'pending',created:'2026-09-06T10:00:00.000Z'}],audit:[]};
}
export function applyCommand(previous:State, input:unknown, now=new Date().toISOString(), actorId?:string):State {
 const c=commandSchema.parse(input);const s=structuredClone(previous);const id=()=>crypto.randomUUID();let subject='';
 const activeOrg=(key:string)=>{const o=s.orgs.find(x=>x.id===key&&x.status==='启用');if(!o)throw Error('请选择有效的启用组织');return o;};
 if(c.action==='workflow'){
 s.workflows??={};s.workflows[c.kind]={version:(s.workflows[c.kind]?.version??0)+1,steps:c.steps};subject=c.kind;
 }else if(c.action==='withdraw'){
 const a=s.approvals.find(a=>a.id===c.id);if(!a||a.status!=='pending'||!actorId||a.createdBy!==actorId)throw Error('仅申请人可以撤回待审批申请');a.status='withdrawn';a.decided=now;a.decidedBy=actorId;subject=a.employeeId;
 }else if(c.action==='employee'){
 activeOrg(c.orgId);if(s.employees.some(e=>e.code===c.code&&e.id!==c.id))throw Error('员工编号已存在');
 const old=c.id?s.employees.find(e=>e.id===c.id):null;if(c.id&&!old)throw Error('员工不存在');
 if(old&&old.orgId!==c.orgId)throw Error('在职人员组织变更请提交调动审批');
 if(old?.status==='离职')throw Error('离职人员不可直接编辑');
 const {action,...data}=c;const e={...data,id:old?.id??id(),status:old?.status??'试用'};s.employees=old?s.employees.map(x=>x.id===old.id?e:x):[e,...s.employees];subject=c.name;
 }else if(c.action==='org'){
 const old=s.orgs.find(o=>o.id===c.id);if(c.id&&!old)throw Error('组织不存在');if(c.parentId)activeOrg(c.parentId);
 const seen=new Set([c.id]);let parent=c.parentId;while(parent){if(seen.has(parent))throw Error('上级组织不能形成循环');seen.add(parent);parent=s.orgs.find(o=>o.id===parent)?.parentId??'';}
 if(s.orgs.some(o=>o.name===c.name&&o.parentId===c.parentId&&o.id!==c.id))throw Error('同级组织名称已存在');
 if(c.status==='停用'&&(s.employees.some(e=>e.orgId===c.id&&e.status!=='离职')||s.orgs.some(o=>o.parentId===c.id&&o.status==='启用')||s.approvals.some(a=>a.orgId===c.id&&a.status==='pending')))throw Error('组织存在在职员工、启用下级或待审批调动，不能停用');
 const {action,...data}=c;const o={...data,id:old?.id??id()};s.orgs=old?s.orgs.map(x=>x.id===old.id?o:x):[...s.orgs,o];subject=c.name;
 }else if(c.action==='request'){
 const e=s.employees.find(e=>e.id===c.employeeId);if(!e||e.status==='离职')throw Error('员工不存在或已离职');if(s.approvals.some(a=>a.employeeId===e.id&&a.status==='pending'))throw Error('该员工已有待处理的人事申请');
 if(c.kind==='regularize'&&e.status!=='试用')throw Error('仅试用员工可申请转正');if(c.kind==='transfer'){activeOrg(c.orgId);if(c.orgId===e.orgId)throw Error('目标组织与当前组织相同');}
 const workflow=s.workflows?.[c.kind];if(actorId&&!workflow)throw Error('请先由管理员配置该类型审批流程');if(workflow?.steps.some(step=>step.userId===actorId))throw Error('申请人不能同时是本流程审批人');
 s.approvals.unshift({steps:workflow?structuredClone(workflow.steps):undefined,currentStep:workflow?0:undefined,workflowVersion:workflow?.version,id:id(),employeeId:e.id,kind:c.kind,orgId:c.kind==='transfer'?c.orgId:e.orgId,reason:c.reason,status:'pending',created:now,createdBy:actorId});subject=e.name;
 }else{
 const a=s.approvals.find(a=>a.id===c.id);if(!a||a.status!=='pending')throw Error('审批不存在或已处理，请刷新');if(actorId&&(!a.createdBy||a.createdBy===actorId))throw Error('不能审批本人申请或缺少申请人记录的历史申请');const e=s.employees.find(e=>e.id===a.employeeId);if(!e||e.status==='离职')throw Error('关联员工状态已变化');
 let finished=true;if(a.steps?.length){const step=a.steps[a.currentStep??0];if(!actorId||step.userId!==actorId)throw Error('尚未轮到当前审批人');step.decision=c.decision;step.at=now;if(c.decision==='approved'&&(a.currentStep??0)<a.steps.length-1){a.currentStep=(a.currentStep??0)+1;finished=false;}}
 if(finished&&c.decision==='approved'){if(a.kind==='transfer'){activeOrg(a.orgId);e.orgId=a.orgId;}if(a.kind==='regularize'){if(e.status!=='试用')throw Error('员工已非试用状态');e.status='正式';}if(a.kind==='exit')e.status='离职';}if(finished){a.status=c.decision;a.decided=now;a.decidedBy=actorId;}subject=e.name;
 }
 s.audit.unshift({id:id(),action:{workflow:'配置审批流程',withdraw:'撤回人事申请',employee:'保存员工档案',org:'保存组织',request:'发起人事申请',decide:'处理人事审批'}[c.action],subject,at:now,actorId});return s;
}
