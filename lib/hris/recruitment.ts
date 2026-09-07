import {z} from 'zod';
import type {State} from './model';
import {scopedOrgs,type Member} from './authorization';
import {HttpError} from './http';
import {visibleRecord,type DevelopmentRecord as R} from './development';
const id=z.string().min(1).max(100),text=z.string().trim().min(1).max(200),evidence=z.string().trim().min(5).max(4000),date=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>{const d=new Date(v+'T00:00:00Z');return !isNaN(d.getTime())&&d.toISOString().slice(0,10)===v;});
export const recruitmentCommand=z.discriminatedUnion('action',[
 z.object({action:z.literal('requisition'),positionId:id,title:text,headcount:z.number().int().min(1).max(10000),reason:evidence}),
 z.object({action:z.literal('approveRequisition'),id}),z.object({action:z.literal('closeRequisition'),id,reason:evidence}),
 z.object({action:z.literal('candidate'),requisitionId:id,name:text,email:z.string().trim().email().max(200).or(z.literal('')),source:evidence}),
 z.object({action:z.literal('interview'),candidateId:id,rating:z.number().int().min(1).max(5),recommendation:z.enum(['advance','reject']),evidence}),
 z.object({action:z.literal('offer'),id,joined:date,gradeId:id.optional(),evidence}),
 z.object({action:z.literal('approveOffer'),id}),
 z.object({action:z.literal('acceptOffer'),id,evidence}),
 z.object({action:z.literal('rejectCandidate'),id,reason:evidence}),
 z.object({action:z.literal('hire'),id,code:text}),
]);
export function applyRecruitment(records:R[],state:State,member:Member,input:unknown,at=new Date().toISOString()){
 const c=recruitmentCommand.parse(input),scope=scopedOrgs(state,member);
 const invalid=(message:string):never=>{throw new HttpError(400,message);},deny=(message:string):never=>{throw new HttpError(403,message);};
 const hr=()=>{if(!['admin','hr'].includes(member.role))deny('仅管理员或HR可维护招聘业务');};
 const approver=(createdBy:string)=>{if(!['admin','manager'].includes(member.role)||createdBy===member.userId)deny('招聘审批须由其他有权限的管理人员完成');};
 const position=(id:string)=>{const p=state.positions?.find(p=>p.id===id);if(!p||!scope.has(p.orgId))deny('没有此岗位的数据权限');if(p!.status!=='启用')invalid('岗位已停用');return p!;};
 const get=(id:string,kind:R['kind'])=>{const r=records.find(r=>r.id===id&&r.kind===kind);if(!r||!visibleRecord(r,records,state,member))deny('记录不存在或没有访问权限');return r!;};
 const req=(r:R)=>{const q=get(r.referenceId!,'requisition');if(q.status!=='active')invalid('招聘需求未批准或已关闭');return q;};
 const make=(kind:R['kind'],payload:R['payload'],extra:Partial<R>={})=>({id:crypto.randomUUID(),kind,payload,employeeId:null,positionId:null,referenceId:null,status:'draft',createdBy:member.userId,createdAt:at,updatedAt:at,...extra} as R);
 const change=(r:R,status:string,payload:R['payload']={})=>({...r,status,payload:{...r.payload,...payload},updatedAt:at});
 let record:R,employeeInput:Record<string,unknown>|undefined;
 switch(c.action){
 case 'requisition':{hr();position(c.positionId);record=make('requisition',{title:c.title,headcount:c.headcount,reason:c.reason},{positionId:c.positionId});break;}
 case 'approveRequisition':{const r=get(c.id,'requisition');approver(r.createdBy);position(r.positionId!);if(r.status!=='draft')invalid('需求已经处理');record=change(r,'active',{approvedBy:member.userId,approvedAt:at});break;}
 case 'closeRequisition':{hr();const r=get(c.id,'requisition');if(!['draft','active'].includes(r.status))invalid('需求已经关闭');if(records.some(x=>x.kind==='candidate'&&x.referenceId===r.id&&!['hired','rejected'].includes(x.status)))invalid('仍有在途候选人，请先完成或结束招聘流程');record=change(r,'closed',{closedReason:c.reason});break;}
 case 'candidate':{hr();const q=get(c.requisitionId,'requisition');position(q.positionId!);if(q.status!=='active')invalid('需求须先通过审批');if(member.role!=='admin'&&!member.viewEmail&&c.email)deny('没有联系邮箱维护权限');if(c.email&&records.some(r=>r.kind==='candidate'&&r.referenceId===q.id&&r.payload.email?.toLowerCase()===c.email.toLowerCase()&&r.status!=='rejected'))invalid('此需求已有相同邮箱的候选人');record=make('candidate',{name:c.name,email:c.email,source:c.source},{positionId:q.positionId,referenceId:q.id,status:'screening'});break;}
 case 'interview':{if(!['admin','hr','manager'].includes(member.role))deny('没有面试评价权限');const r=get(c.candidateId,'candidate');req(r);if(!['screening','interviewed'].includes(r.status))invalid('当前阶段不能记录面试');record=make('interview',{rating:c.rating,recommendation:c.recommendation,evidence:c.evidence},{positionId:r.positionId,referenceId:r.id,status:'recorded'});break;}
 case 'offer':{hr();const r=get(c.id,'candidate');req(r);position(r.positionId!);if(!['screening','interviewed'].includes(r.status))invalid('当前阶段不能发起录用');const interviews=records.filter(x=>x.kind==='interview'&&x.referenceId===r.id).sort((a,b)=>b.createdAt.localeCompare(a.createdAt));if(!interviews.length||interviews[0].payload.recommendation!=='advance')invalid('须有最近一次建议推进的面试评价');if(c.gradeId){if(member.role!=='admin'&&!member.viewLevel)deny('没有职级字段维护权限');if(!state.grades?.some(g=>g.id===c.gradeId&&g.status==='启用'))invalid('目标职级不存在或已停用');}record=change(r,'offered',{joined:c.joined,gradeId:c.gradeId,evidence:c.evidence,offeredBy:member.userId,offeredAt:at});break;}
 case 'approveOffer':{const r=get(c.id,'candidate');approver(r.payload.offeredBy??r.createdBy);req(r);if(r.status!=='offered')invalid('当前阶段不能审批录用');record=change(r,'approved',{approvedBy:member.userId,approvedAt:at});break;}
 case 'acceptOffer':{hr();const r=get(c.id,'candidate');req(r);if(r.status!=='approved')invalid('须先完成录用审批');record=change(r,'accepted',{acceptanceEvidence:c.evidence,acceptanceRecordedBy:member.userId,acceptanceRecordedAt:at});break;}
 case 'rejectCandidate':{hr();const r=get(c.id,'candidate');if(['hired','rejected'].includes(r.status))invalid('候选流程已经结束');record=change(r,'rejected',{closedReason:c.reason});break;}
 case 'hire':{hr();const r=get(c.id,'candidate'),q=req(r),p=position(r.positionId!);if(r.status!=='accepted')invalid('须先登记候选人接受录用的依据');if(records.filter(x=>x.kind==='candidate'&&x.referenceId===q.id&&x.status==='hired').length>=q.payload.headcount!)invalid('招聘需求人数已满');if(r.payload.joined!>at.slice(0,10))invalid('尚未到计划入职日期');employeeInput={action:'employee',code:c.code,name:r.payload.name!,email:r.payload.email??'',orgId:p.orgId,positionId:p.id,gradeId:r.payload.gradeId??null,job:p.name,level:'',joined:r.payload.joined!};record=change(r,'hired',{hiredBy:member.userId,hiredAt:at});break;}
 }
 return {record,employeeInput};
}
