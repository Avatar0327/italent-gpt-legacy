import {z} from 'zod';
import {applyDevelopment,visibleRecord,type DevelopmentRecord as R} from './development';
import {learningWindow,learningAssignmentKey} from './learning-plan-model';
import {businessDate} from './business-time';
import {scopedOrgs,type Member} from './authorization';
import type {State} from './model';
import {HttpError} from './http';
const id=z.string().min(1).max(100);
const command=z.discriminatedUnion('action',[
 z.object({action:z.literal('assign'),definitionId:id,employeeId:id}).strict(),
 z.object({action:z.literal('closeAssignment'),id}).strict(),
 z.object({action:z.literal('cancelAssignment'),id,evidence:z.string().trim().min(5).max(3000)}).strict(),
 z.object({action:z.literal('restoreAssignment'),id,evidence:z.string().trim().min(5).max(3000)}).strict(),
]);
export function applyLearningAssignment(records:R[],state:State,m:Member,input:unknown,at=new Date().toISOString()):R[]{
 const c=command.parse(input),scope=scopedOrgs(state,m);
 const deny=():never=>{throw new HttpError(403,'没有此员工学习实例的管理权限');};
 const fail=(text:string):never=>{throw new HttpError(400,text);};
 if(!['admin','hr'].includes(m.role))deny();
 if(c.action!=='assign'){
  const r=records.find(r=>r.kind==='learningAssignment'&&r.id===c.id);
  if(!r||!visibleRecord(r,records,state,m)||!scope.has(r.payload.orgId!))deny();
  const tasks=records.filter(t=>t.kind==='enrollment'&&t.payload.learningAssignmentId===r!.id);
  if(c.action==='cancelAssignment'){
   if(r!.status!=='active')fail('仅进行中的实例可以取消');
   return [{...r!,status:'cancelled',updatedAt:at,payload:{...r!.payload,evidence:c.evidence}},...tasks.filter(t=>t.status!=='completed').map(t=>({...t,status:'cancelled',updatedAt:at,payload:{...t.payload,closedReason:c.evidence,assignmentCancelled:true,assignmentPreviousStatus:t.status}}))];
  }
  if(c.action==='restoreAssignment'){
   if(r!.status!=='cancelled')fail('仅已取消实例可整体恢复');
   const employee=state.employees.find(e=>e.id===r!.employeeId);
   if(!employee||employee.status==='离职'||employee.orgId!==r!.payload.orgId||!state.orgs.some(o=>o.id===employee.orgId&&o.status==='启用'))fail('恢复须为原组织在职员工');
   const config=r!.payload.learningMode!;
   if((config.mode==='fixed'||!config.allowOverdue)&&businessDate(at)>r!.payload.due!)fail('实例已超过允许学习期限，不能恢复');
   for(const task of tasks.filter(t=>t.payload.assignmentCancelled&&t.payload.assignmentPreviousStatus!=='cancelled'))if(!records.some(course=>course.kind==='course'&&course.id===task.referenceId&&course.status==='published'))fail('恢复任务的课程版本须仍已发布');
   return [{...r!,status:'active',updatedAt:at,payload:{...r!.payload,evidence:c.evidence}},...tasks.filter(t=>t.payload.assignmentCancelled).map(t=>({...t,status:t.payload.assignmentPreviousStatus==='cancelled'?'cancelled':'active',updatedAt:at,payload:{...t.payload,assignmentCancelled:false,restorationEvidence:c.evidence}}))];
  }
  if(r!.status!=='active')fail('仅进行中的实例可结项');if(businessDate(at)<r!.payload.start!)fail('计划尚未开始，不能提前结项');
  if(tasks.length!==r!.payload.courseIds!.length||r!.payload.courseIds!.some(course=>!tasks.some(t=>t.referenceId===course&&t.status==='completed'&&t.payload.verifiedBy)))fail('须完成全部课程的独立核验后结项，取消任务不视为完成');
  return [{...r!,status:'completed',updatedAt:at}];
 }
 const definition=records.find(r=>r.id===c.definitionId&&r.kind==='learningDefinition'),employee=state.employees.find(e=>e.id===c.employeeId);
 if(!definition||!visibleRecord(definition,records,state,m)||!employee||!scope.has(employee.orgId)||!scope.has(definition.payload.orgId!)||employee.orgId!==definition.payload.orgId)deny();
 if(employee!.status==='离职')fail('离职员工不能分派新学习');
 if(definition!.status!=='sealed'||!state.orgs.some(o=>o.id===definition!.payload.orgId&&o.status==='启用'))fail('计划须已定版且组织启用');
 const config=definition!.payload.learningMode!;
 if(config.mode==='recurring')fail('循环轮次尚未接入派发，请使用周期或起止时间配置');
 const key=learningAssignmentKey(definition!.id,c.employeeId,1);
 if(records.some(r=>r.kind==='learningAssignment'&&r.payload.assignmentKey===key))fail('此员工已获得该计划版本的首轮实例');
 const window=learningWindow(config,businessDate(at));
 if(window.due<businessDate(at))fail('计划已经结束，不能分派');
 const assignment:R={id:crypto.randomUUID(),kind:'learningAssignment',employeeId:c.employeeId,positionId:null,referenceId:definition!.id,status:'active',createdBy:m.userId,createdAt:at,updatedAt:at,payload:{title:definition!.payload.title,orgId:definition!.payload.orgId,courseIds:[...definition!.payload.courseIds!],learningMode:config,version:definition!.payload.version,definitionRootId:definition!.payload.definitionRootId,assignmentKey:key,round:1,start:window.start,due:window.due}};
 const result:R[]=[assignment];
 for(const courseId of assignment.payload.courseIds!){
  const task=applyDevelopment([...records,...result],state,m,{action:'enroll',assignmentId:assignment.id,employeeId:c.employeeId,courseId,due:window.due},at);
  const source=config.progressSync?records.filter(r=>r.kind==='enrollment'&&r.employeeId===c.employeeId&&r.referenceId===courseId&&r.status==='completed'&&r.payload.verifiedBy&&r.payload.verifiedAt&&!r.payload.sourceEnrollmentId&&visibleRecord(r,records,state,m)&&(!r.payload.examId||records.some(a=>a.kind==='attempt'&&a.referenceId===r.id&&a.payload.passed))).sort((a,b)=>(b.payload.verifiedAt??'').localeCompare(a.payload.verifiedAt??'')||a.id.localeCompare(b.id))[0]:undefined;
  const sourceExam=source?.payload.examId?records.find(a=>a.kind==='attempt'&&a.referenceId===source.id&&a.payload.passed):undefined;
  result.push(source?{...task,status:'completed',payload:{...task.payload,sourceEnrollmentId:source.id,sourceVerifiedBy:source.payload.verifiedBy,sourceVerifiedAt:source.payload.verifiedAt,sourceExamAttemptId:sourceExam?.id,verifiedBy:source.payload.verifiedBy,verifiedAt:source.payload.verifiedAt,verification:'引用同员工同课程版本已独立核验的完成记录；未创建本次考试记录'}}:task);
 }
 return result;
}
