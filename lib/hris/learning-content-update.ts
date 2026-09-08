import {z} from 'zod';
import {visibleRecord,applyDevelopment,type DevelopmentRecord as R} from './development';
import {scopedOrgs,type Member} from './authorization';
import type {State} from './model';
import {HttpError} from './http';
import {businessDate} from './business-time';
import {learningRequirements,learningRequirementProgress,learningAssignmentCurrent,learningStageStartsOn} from './learning-requirements';
import {learningGrade} from './learning-grades';
import {learningAssignmentKey} from './learning-plan-model';
import {applyLearningExamTask} from './learning-exam-tasks';
import {applyHomework} from './learning-homework';
const id=z.string().min(1).max(100);
export const contentUpdateSchema=z.object({assignmentId:id,definitionId:id,homeworkReviewers:z.record(id,id).optional()}).strict();
function canonical(value:unknown):string {if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';if(value&&typeof value==='object')return '{'+Object.entries(value).filter(([,v])=>v!==undefined).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>JSON.stringify(k)+':'+canonical(v)).join(',')+'}';return JSON.stringify(value)??'null';}
export function previewLearningContentUpdate(records:R[],state:State,m:Member,input:unknown,at=new Date().toISOString()){
 const c=contentUpdateSchema.parse(input),scope=scopedOrgs(state,m);
 const assignment=records.find(r=>r.id===c.assignmentId&&r.kind==='learningAssignment'),target=records.find(r=>r.id===c.definitionId&&r.kind==='learningDefinition');
 if(!['admin','hr'].includes(m.role)||!assignment||!target||!visibleRecord(assignment,records,state,m)||!visibleRecord(target,records,state,m)||!scope.has(assignment.payload.orgId!)||!scope.has(target.payload.orgId!))throw new HttpError(403,'没有此学习内容更新的管理权限');
 const before=learningRequirements(assignment),after=learningRequirements(target),same=(a:typeof before[number],b:typeof before[number])=>a.id===b.id&&a.kind===b.kind&&a.resourceId===b.resourceId;
 const retained=before.filter(a=>after.some(b=>same(a,b))),removed=before.filter(a=>!after.some(b=>same(a,b))),added=after.filter(a=>!before.some(b=>same(a,b)));
 const blockers:string[]=[];
 if(assignment.status!=='active')blockers.push('仅进行中的实例可更新；已结项及取消记录默认保留');
 if(!learningAssignmentCurrent(assignment,state))blockers.push('人员须在原启用组织且未离职');
 if(target.status!=='sealed'||target.payload.definitionRootId!==assignment.payload.definitionRootId||target.payload.orgId!==assignment.payload.orgId||(target.payload.version??0)<=(assignment.payload.version??0))blockers.push('目标须为同计划、同组织的后续定版版本');
 if(canonical(target.payload.learningMode)!==canonical(assignment.payload.learningMode))blockers.push('本批内容更新保持学习模式、时间和进度同步规则；模式变更另行处理');
 if(assignment.payload.learningMode?.mode==='recurring')blockers.push('循环实例内容更新仍待后续实现');
 if(assignment.payload.due!<businessDate(at))blockers.push('本批不更新已到期实例，避免新增任务绕过原期限');
 if(removed.length)blockers.push('本批支持追加内容和调整阶段/成绩；移除或替换内容待历史退出机制完成');
 if(added.some(r=>r.kind==='course')&&assignment.payload.learningMode?.progressSync)blockers.push('新增课程的历史同步更新仍待后续实现，不能静默改为重新学习');
 const tasks=records.filter(r=>['enrollment','learningExamTask','homeworkTask'].includes(r.kind)&&r.payload.learningAssignmentId===assignment.id);
 if(tasks.length!==before.length||before.some(r=>tasks.filter(t=>t.referenceId===r.resourceId&&t.employeeId===assignment.employeeId&&t.kind===(r.kind==='course'?'enrollment':r.kind==='exam'?'learningExamTask':'homeworkTask')&&(!t.payload.learningRequirementId||t.payload.learningRequirementId===r.id)).length!==1))blockers.push('原实例要求与任务绑定不完整或重复，须先修复');
 const key=learningAssignmentKey(target.id,assignment.employeeId!,assignment.payload.round??1);
 if(records.some(r=>r.kind==='learningAssignment'&&r.id!==assignment.id&&(r.payload.assignmentKey===key||r.employeeId===assignment.employeeId&&(r.payload.round??1)===(assignment.payload.round??1)&&r.payload.contentDefinitionHistoryIds?.includes(target.id))))blockers.push('员工已有目标版本的本轮实例，禁止合并或重复派发');
 const projected:R={...assignment,referenceId:target.id,payload:{...assignment.payload,title:target.payload.title,version:target.payload.version,assignmentKey:key,courseIds:target.payload.courseIds,examIds:target.payload.examIds,homeworkIds:target.payload.homeworkIds,learningRequirements:after,trainingStages:target.payload.trainingStages,gradeRule:target.payload.gradeRule}};
 if(projected.payload.trainingStages?.some(s=>learningStageStartsOn(projected,s)>projected.payload.due!))blockers.push('新阶段开放日不得超过实例原截止日');
 const newHomework=added.filter(r=>r.kind==='homework').map(r=>r.resourceId),reviewers=c.homeworkReviewers??{};
 if(Object.keys(reviewers).some(k=>!newHomework.includes(k)))blockers.push('批阅人仅可为本次新增作业指定，已有批阅人通过独立转交办理');
 for(const r of added){const resource=records.find(x=>x.id===r.resourceId&&x.kind===(r.kind==='course'?'course':r.kind==='exam'?'learningExamDefinition':'homeworkDefinition'));if(!resource||!visibleRecord(resource,records,state,m)||resource.status!==(r.kind==='course'?'published':'sealed'))blockers.push('新增内容版本不可用');if(r.kind==='homework'){const reviewer=state.employees.find(e=>e.id===reviewers[r.resourceId]);if(!reviewer||reviewer.id===assignment.employeeId||reviewer.status==='离职'||reviewer.orgId!==assignment.payload.orgId)blockers.push('每项新增作业须指定原组织在职的独立批阅人');}}
 return {assignmentId:assignment.id,fromDefinitionId:assignment.referenceId!,toDefinitionId:target.id,fromVersion:assignment.payload.version,toVersion:target.payload.version,retained,added,removed,blockers:[...new Set(blockers)],canApply:blockers.length===0,beforeProgress:learningRequirementProgress(assignment,records),afterProgress:learningRequirementProgress(projected,records),beforeGrade:learningGrade(assignment,records),afterGrade:learningGrade(projected,records),projected};
}
export function applyLearningContentUpdate(records:R[],state:State,m:Member,input:unknown,evidence:string,at=new Date().toISOString()):R[]{
 const c=contentUpdateSchema.parse(input),reason=z.string().trim().min(5).max(3000).parse(evidence),p=previewLearningContentUpdate(records,state,m,c,at);
 if(!p.canApply)throw new HttpError(400,p.blockers.join('；'));
 const assignment:R={...p.projected,updatedAt:at,payload:{...p.projected.payload,homeworkReviewers:{...p.projected.payload.homeworkReviewers,...c.homeworkReviewers},contentDefinitionHistoryIds:[...new Set([...(p.projected.payload.contentDefinitionHistoryIds??[]),p.fromDefinitionId,p.toDefinitionId])],contentUpdateFromId:p.fromDefinitionId,contentUpdatedBy:m.userId,contentUpdatedAt:at,contentUpdateEvidence:reason}};
 const base=records.map(r=>r.id===assignment.id?assignment:r),result:R[]=[assignment];
 for(const r of p.added){const context=[...base,...result.slice(1)];if(r.kind==='course')result.push(applyDevelopment(context,state,m,{action:'enroll',assignmentId:assignment.id,employeeId:assignment.employeeId,courseId:r.resourceId,due:assignment.payload.due},at));else if(r.kind==='exam')result.push(...applyLearningExamTask(context,state,m,{action:'assign',assignmentId:assignment.id,employeeId:assignment.employeeId,examId:r.resourceId,start:assignment.payload.start,due:assignment.payload.due},at));else result.push(...applyHomework(context,state,m,{action:'assign',assignmentId:assignment.id,employeeId:assignment.employeeId,definitionId:r.resourceId,reviewerEmployeeId:c.homeworkReviewers![r.resourceId],start:assignment.payload.start,due:assignment.payload.due},at));}
 return result;
}
