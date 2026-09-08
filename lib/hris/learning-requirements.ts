import type {DevelopmentRecord as R} from './development';
import type {State} from './model';

// v1 deliberately supports course requirements only. Course-embedded exams
// remain evidence of the course, not independent plan activities.
export type LearningRequirement={id:string;kind:'course';resourceId:string};
export function courseRequirements(courseIds:string[],previous:LearningRequirement[]=[]):LearningRequirement[]{
 return courseIds.map(resourceId=>({id:previous.find(r=>r.kind==='course'&&r.resourceId===resourceId)?.id??`course:${resourceId}`,kind:'course',resourceId}));
}
export function learningRequirements(record:R):LearningRequirement[]{
 return record.payload.learningRequirements??courseRequirements(record.payload.courseIds??[]);
}
export function learningAssignmentCurrent(assignment:R,state:State){
 const employee=state.employees.find(e=>e.id===assignment.employeeId);
 return !!employee&&employee.status!=='离职'&&employee.orgId===assignment.payload.orgId&&state.orgs.some(o=>o.id===employee.orgId&&o.status==='启用');
}
export function learningRequirementProgress(assignment:R,records:R[]){
 const requirements=learningRequirements(assignment),courseIds=assignment.payload.courseIds??[];
 const valid=requirements.length>0&&requirements.length===courseIds.length&&new Set(requirements.map(r=>r.id)).size===requirements.length&&new Set(requirements.map(r=>r.resourceId)).size===requirements.length&&requirements.every(r=>r.kind==='course'&&courseIds.includes(r.resourceId));
 const tasks=records.filter(r=>r.kind==='enrollment'&&r.payload.learningAssignmentId===assignment.id);
 const items=requirements.map(requirement=>{
  const matches=tasks.filter(t=>t.referenceId===requirement.resourceId);
  const task=matches.length===1?matches[0]:undefined;
  const bound=!!task&&task.employeeId===assignment.employeeId&&(!task.payload.learningRequirementId||task.payload.learningRequirementId===requirement.id);
  const complete=bound&&task.status==='completed'&&!!task.payload.verifiedBy&&!!task.payload.verifiedAt;
  return {requirementId:requirement.id,resourceId:requirement.resourceId,taskId:bound?task.id:null,complete,verifiedBy:complete?task.payload.verifiedBy:null,verifiedAt:complete?task.payload.verifiedAt:null,sourceEnrollmentId:complete?task.payload.sourceEnrollmentId??null:null};
 });
 const stages=(assignment.payload.trainingStages??[]).map(stage=>{
  const optional=new Set(stage.optionalCourseIds??[]),required=stage.courseIds.filter(id=>!optional.has(id));
  const done=(ids:string[])=>ids.filter(id=>items.some(i=>i.resourceId===id&&i.complete)).length;
  const requiredMinimum=stage.requiredMinimum??required.length,optionalMinimum=stage.optionalMinimum??optional.size;
  return {title:stage.title,courseIds:stage.courseIds,required:done(required),optional:done([...optional]),requiredMinimum,optionalMinimum,complete:done(required)>=requiredMinimum&&done([...optional])>=optionalMinimum};
 });
 return {items,stages,total:requirements.length,completed:items.filter(i=>i.complete).length,complete:valid&&tasks.length===requirements.length&&(stages.length?stages.every(s=>s.complete):items.every(i=>i.complete))};
}
export function learningStageOpen(task:R,records:R[]){
 if(!task.payload.learningAssignmentId)return true;
 const assignment=records.find(r=>r.kind==='learningAssignment'&&r.id===task.payload.learningAssignmentId);
 if(!assignment||assignment.status!=='active')return false;
 if(!assignment.payload.trainingStages?.length||!assignment.payload.learningMode?.orderedStages)return true;
 const stages=learningRequirementProgress(assignment,records).stages;
 const index=stages.findIndex(stage=>stage.courseIds.includes(task.referenceId!));
 return index>=0&&stages.slice(0,index).every(stage=>stage.complete);
}
