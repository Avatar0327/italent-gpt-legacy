import {authorizeCommand,type Member} from './authorization';
import type {State} from './model';
import {visibleRecord,type DevelopmentRecord as R} from './development';
export const inboxKinds=['leave','correction','shift','plan','enrollment','instructorCertification','onboardingPlan','trainingAttendance','trainingSession','training','course'] as const;
export type InboxItem={id:string;recordId:string;domain:string;title:string;employeeName:string;action:string;href:string;updatedAt:string;due:string|null};
export function workInbox(state:State,records:R[],m:Member):InboxItem[]{
 const rows:InboxItem[]=[],hr=['admin','hr'].includes(m.role),manager=hr||m.role==='manager';
 const employee=(id:string|null)=>state.employees.find(e=>e.id===id);
 for(const a of state.approvals.filter(a=>a.status==='pending')){
  try{authorizeCommand(state,{action:'decide',id:a.id,decision:'rejected'},m);}catch{continue;}
  rows.push({id:'personnel:'+a.id,recordId:a.id,domain:'personnel',title:({transfer:'调动申请',regularize:'转正申请',exit:'离职申请'})[a.kind],employeeName:employee(a.employeeId)?.name??'—',action:'人事审批',href:'/approvals',updatedAt:a.steps?.[Math.max(0,(a.currentStep??0)-1)]?.at??a.created,due:null});
 }
 for(const r of records){
  if(!visibleRecord(r,records,state,m))continue;
  const self=r.employeeId===m.employeeId,e=employee(r.employeeId);
  const add=(domain:string,action:string,href:string,suffix='',title=r.payload.title??action)=>rows.push({id:r.kind+':'+r.id+suffix,recordId:r.id,domain,title,employeeName:e?.name??'—',action,href,updatedAt:r.updatedAt,due:r.payload.due??null});
  if(['leave','correction'].includes(r.kind)&&manager&&!self&&r.createdBy!==m.userId&&r.status==='pending'&&records.some(x=>x.id===r.referenceId&&x.kind==='shift'&&x.status==='active'))add('attendance',r.kind==='leave'?'请假审批':'补卡审批','/attendance');
  if(['plan','enrollment'].includes(r.kind)&&manager&&!self&&r.payload.submittedBy!==m.userId&&r.status==='submitted'&&e&&e.status!=='离职')add('development',r.kind==='plan'?'发展行动核验':'学习成果核验',r.kind==='plan'?'/development':'/learning');
  if(r.kind==='instructorCertification'&&hr&&!self&&r.createdBy!==m.userId&&r.status==='submitted')add('learning','讲师认证复核','/instructors');
  if(r.kind==='onboardingPlan'&&r.status==='active'&&!self){
   if(manager)for(const item of r.payload.onboardingItems??[])if(item.status==='submitted'&&item.submittedBy!==m.userId)add('onboarding','融入事项核验','/onboarding',':'+item.id,item.title);
   if(hr&&r.payload.onboardingItems?.length&&r.payload.onboardingItems.every(x=>x.status==='verified'))add('onboarding','融入计划结项','/onboarding',':close');
  }
  if(r.kind==='trainingAttendance'&&r.status==='submitted'&&manager&&!self&&r.payload.submittedBy!==m.userId){const s=records.find(x=>x.id===r.referenceId&&x.kind==='trainingSession');if(s?.status==='active'&&records.some(t=>t.id===s.referenceId&&t.kind==='training'&&t.status==='active')&&records.some(x=>x.kind==='enrollment'&&x.employeeId===r.employeeId&&x.referenceId===s.payload.sessionCourseId&&x.payload.trainingId===s.referenceId&&x.status!=='cancelled'))add('learning','培训出勤核验','/training-sessions','',s.payload.title??'培训出勤');}
 }
 return rows.sort((a,b)=>a.updatedAt.localeCompare(b.updatedAt)||a.id.localeCompare(b.id));
}
