import {z} from 'zod';
import {HttpError} from './http';
import {scopedOrgs,type Member} from './authorization';
import {isTalentManager,orgWithin,visibleRecord,type DevelopmentRecord} from './development';
import type {State} from './model';
const id=z.string().min(1).max(100),text=z.string().trim().min(1).max(200),evidence=z.string().trim().min(5).max(4000),date=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>{const d=new Date(v+'T00:00:00Z');return !isNaN(d.getTime())&&d.toISOString().slice(0,10)===v;});
const goal=z.object({title:text,metric:evidence,weight:z.number().int().min(1).max(100)}),score=z.number().min(0).max(100).multipleOf(0.01);
export const performanceCommand=z.discriminatedUnion('action',[
 z.object({action:z.literal('cycle'),name:text,orgId:id,period:text,start:date,end:date,lowCut:score,highCut:score,lowLabel:text,midLabel:text,highLabel:text}),
 z.object({action:z.literal('startCycle'),id}),z.object({action:z.literal('closeCycle'),id}),
 z.object({action:z.literal('goals'),id:id.optional(),employeeId:id,cycleId:id,goals:z.array(goal).min(1).max(20)}),
 z.object({action:z.literal('confirmGoals'),id}),
 z.object({action:z.literal('selfReview'),id,evidence}),
 z.object({action:z.literal('evaluate'),id,scores:z.array(score).min(1).max(20),evidence}),
 z.object({action:z.literal('returnPerformance'),id,evidence}),
 z.object({action:z.literal('cancelPerformance'),id,evidence}),
 z.object({action:z.literal('publishPerformance'),id,evidence,supersedes:id.optional()}),
]);
export function applyPerformance(records:DevelopmentRecord[],state:State,member:Member,input:unknown,at=new Date().toISOString()){
 const c=performanceCommand.parse(input),scope=scopedOrgs(state,member);
 const invalid=(message:string):never=>{throw new HttpError(400,message);},deny=(message:string):never=>{throw new HttpError(403,message);};
 const manager=()=>{if(!isTalentManager(member))deny('没有绩效管理权限');};
 const hr=()=>{if(!['admin','hr'].includes(member.role))deny('仅管理员和HR可配置周期及发布结果');};
 const employee=(id:string)=>{const e=state.employees.find(e=>e.id===id);if(!e||!(isTalentManager(member)?scope.has(e.orgId):e.id===member.employeeId))deny('没有此员工的数据权限');return e!;};
 const get=(id:string,kind:DevelopmentRecord['kind'])=>{const r=records.find(r=>r.id===id&&r.kind===kind);if(!r||!visibleRecord(r,records,state,member))deny('记录不存在或没有访问权限');return r!;};
 const independent=(r:DevelopmentRecord)=>{manager();employee(r.employeeId!);if(r.employeeId===member.employeeId)deny('不能确认、评价或发布本人的绩效');};
 const cycle=(r:DevelopmentRecord)=>{const p=get(r.referenceId!,'performanceCycle');if(p.status!=='active')invalid('绩效周期未启动或已结束');return p;};
 const published=(r:DevelopmentRecord)=>records.some(x=>x.kind==='performance'&&x.payload.sourcePlanId===r.id);
 const make=(kind:DevelopmentRecord['kind'],payload:DevelopmentRecord['payload'],extra:Partial<DevelopmentRecord>={})=>({id:crypto.randomUUID(),kind,payload,employeeId:null,positionId:null,referenceId:null,status:'draft',createdBy:member.userId,createdAt:at,updatedAt:at,...extra} as DevelopmentRecord);
 const change=(r:DevelopmentRecord,status:string,payload:DevelopmentRecord['payload']={})=>({...r,status,payload:{...r.payload,...payload},updatedAt:at});
 switch(c.action){
 case 'cycle':{hr();const org=state.orgs.find(o=>o.id===c.orgId);if(!org||!scope.has(c.orgId))deny('没有此组织的管理权限');if(org!.status!=='启用'||c.end<c.start||c.lowCut>=c.highCut)invalid('请检查组织状态、日期及评级阈值');if(new Set([c.lowLabel,c.midLabel,c.highLabel]).size!==3)invalid('评级名称不能重复');return make('performanceCycle',{name:c.name,orgId:c.orgId,period:c.period,start:c.start,end:c.end,lowCut:c.lowCut,highCut:c.highCut,lowLabel:c.lowLabel,midLabel:c.midLabel,highLabel:c.highLabel});}
 case 'startCycle':{hr();const r=get(c.id,'performanceCycle');if(r.status!=='draft')invalid('周期已经启动');return change(r,'active');}
 case 'closeCycle':{hr();const r=get(c.id,'performanceCycle');if(r.status!=='active')invalid('周期尚未启动或已结束');if(records.some(x=>x.kind==='performancePlan'&&x.referenceId===r.id&&x.status!=='cancelled'&&!published(x)))invalid('仍有未发布或未取消的绩效计划');return change(r,'closed');}
 case 'goals':{const e=employee(c.employeeId),cy=get(c.cycleId,'performanceCycle');if(e.status==='离职'||cy.status!=='active'||!orgWithin(state,e.orgId,cy.payload.orgId!))invalid('员工状态或周期范围不符合要求');if(c.goals.reduce((sum,g)=>sum+g.weight,0)!==100)invalid('目标权重合计必须等于100%');const old=c.id?get(c.id,'performancePlan'):undefined;if(old&&(old.status!=='draft'||old.employeeId!==e.id||old.referenceId!==cy.id))invalid('仅可修改本人或管理范围内同一周期的草稿');if(records.some(r=>r.kind==='performancePlan'&&r.employeeId===e.id&&r.referenceId===cy.id&&r.id!==c.id))invalid('此员工已建立本周期计划');return make('performancePlan',{period:cy.payload.period,goals:c.goals},{employeeId:e.id,referenceId:cy.id,...(old?{id:old.id,createdBy:old.createdBy,createdAt:old.createdAt}:{})});}
 case 'confirmGoals':{const r=get(c.id,'performancePlan');independent(r);cycle(r);if(r.status!=='draft')invalid('仅草稿目标可以确认');return change(r,'confirmed',{confirmedBy:member.userId,confirmedAt:at});}
 case 'selfReview':{const r=get(c.id,'performancePlan');if(r.employeeId!==member.employeeId)deny('仅员工本人可提交自评');cycle(r);if(r.status!=='confirmed')invalid('目标未确认或已提交自评');return change(r,'submitted',{selfEvidence:c.evidence,selfReviewedAt:at});}
 case 'returnPerformance':{const r=get(c.id,'performancePlan');independent(r);cycle(r);if(published(r)||!['submitted','evaluated'].includes(r.status))invalid('当前阶段不能退回');return change(r,'confirmed',{verification:c.evidence,scores:undefined,score:undefined,evaluation:undefined,evaluatedBy:undefined,evaluatedAt:undefined});}
 case 'evaluate':{const r=get(c.id,'performancePlan');independent(r);cycle(r);if(r.status!=='submitted')invalid('须先由员工提交自评');if(c.scores.length!==r.payload.goals!.length)invalid('请对每项目标评分');const weighted=Math.round(c.scores.reduce((sum,v,i)=>sum+v*r.payload.goals![i].weight,0))/100;return change(r,'evaluated',{scores:c.scores,score:weighted,evaluation:c.evidence,evaluatedBy:member.userId,evaluatedAt:at});}
 case 'cancelPerformance':{const r=get(c.id,'performancePlan');independent(r);if(published(r)||r.status==='cancelled')invalid('已发布或取消的绩效计划不能取消');return change(r,'cancelled',{closedReason:c.evidence});}
 case 'publishPerformance':{hr();const r=get(c.id,'performancePlan');independent(r);const cy=cycle(r);if(r.status!=='evaluated'||published(r))invalid('尚未完成评价或已发布');const previous=records.filter(x=>x.kind==='performance'&&x.employeeId===r.employeeId&&x.payload.period===r.payload.period);if(previous.length&&!c.supersedes)invalid('此员工本期已有绩效，需明确选择被替代的历史记录');if(c.supersedes){const old=get(c.supersedes,'performance');if(old.employeeId!==r.employeeId||old.payload.period!==r.payload.period||records.some(x=>x.payload.supersedes===old.id))invalid('仅可替代同员工同期间的最新历史记录');}const total=r.payload.score!,band=total<cy.payload.lowCut!?1:total<cy.payload.highCut!?2:3;const rating=band===1?cy.payload.lowLabel:band===2?cy.payload.midLabel:cy.payload.highLabel;return make('performance',{period:r.payload.period,source:'正式绩效周期：'+cy.payload.name,originalRating:rating,band,score:total,reason:c.evidence,sourcePlanId:r.id,supersedes:c.supersedes,performanceSnapshot:{cycle:{...cy.payload},plan:{...r.payload}}},{employeeId:r.employeeId,referenceId:r.id,status:'published'});}
 }
}
