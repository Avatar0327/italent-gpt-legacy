import {payrollReport} from './payroll-reports';
import {latestInstructorTrial} from './instructor-trials';
import {instructorDevelopmentProof} from './instructor-development';
import {businessDate} from './workforce';
import {HttpError} from './http';
import {latestPublishedReviews} from './review-versions';
import {z} from 'zod';
import {visibleState} from './authorization';
import {visibleDevelopment,type DevelopmentContext} from './development-repository';
import {attendanceReport} from './attendance';
const validDate=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>{const d=new Date(v+'T00:00:00Z');return !Number.isNaN(d.getTime())&&d.toISOString().slice(0,10)===v;},'日期无效');
export const reportQuery=z.object({dataset:z.enum(['payrollOperations','payrollReconciliation','recruitmentOperations','performanceOperations','instructorCampaignProgress','workforce','attendance','learning','performance','talentReview','successionCoverage','instructorSchedule','trainingProgress','trainingRoster']).default('workforce'),from:validDate.optional(),to:validDate.optional(),search:z.string().max(100).default('')}).refine(q=>!q.from||!q.to||q.from<=q.to,'开始日期不能晚于结束日期');
export const reportKinds={payrollOperations:['payBatch','paySlip','payAdjustment'],payrollReconciliation:['payBatch','paySlip','payAdjustment'],recruitmentOperations:['requisition','candidate'],performanceOperations:['performancePlan','performanceCycle','performance','performanceGoalChange','performanceCheckin'],instructorCampaignProgress:['instructorCampaign','instructorApplication','instructorProfile','instructorTrial','instructorDevelopment','enrollment'],trainingRoster:['training','trainingSession','trainingAttendance','enrollment'],instructorSchedule:['training','trainingSession','enrollment'],trainingProgress:['training','enrollment'],successionCoverage:['succession'],talentReview:['review'],workforce:[],attendance:['shift','clock','correction','leaveType','leaveCredit','leave'],learning:['enrollment'],performance:['performance','performancePlan','performanceCycle']} as const;
export type Cell=string|number|null;
export function makeReport(ctx:DevelopmentContext,input:unknown){
 const q=reportQuery.parse(input),state=visibleState(ctx.state,ctx.member),records=visibleDevelopment(ctx),employee=(id:string|null)=>state.employees.find(e=>e.id===id),name=(id:string|null)=>employee(id)?.name??'',code=(id:string|null)=>employee(id)?.code??'',org=(id:string)=>state.orgs.find(o=>o.id===id)?.name??'';
 let columns:string[]=[],rows:Cell[][]=[],title='';
 if(q.dataset==='payrollOperations'||q.dataset==='payrollReconciliation'){({title,columns,rows}=payrollReport(ctx,q.dataset));}
 if(q.dataset==='workforce'){title='员工名册';columns=['工号','姓名','组织','岗位','人员状态','入职日期'];const email=ctx.member.role==='admin'||ctx.member.viewEmail,level=ctx.member.role==='admin'||ctx.member.viewLevel;if(email)columns.push('邮箱');if(level)columns.push('职级');rows=state.employees.map(e=>{const row:Cell[]=[e.code,e.name,org(e.orgId),e.job,e.status,e.joined];if(email)row.push(e.email);if(level)row.push(e.level);return row;});}
 if(q.dataset==='attendance'){title='出勤核验';columns=['工号','姓名','日期','班次','计划分钟','批准请假分钟','未覆盖分钟','状态'];rows=attendanceReport(records).filter(r=>(!q.from||(r.date??'')>=q.from)&&(!q.to||(r.date??'')<=q.to)).map(r=>[code(r.employeeId),name(r.employeeId),r.date??'',r.name??'',r.plannedMinutes,r.approvedLeaveMinutes,r.uncoveredMinutes,r.status]);}
 if(q.dataset==='learning'){title='学习任务';columns=['工号','姓名','课程','截止日期','状态','成果核验时间'];const status:Record<string,string>={active:'进行中',submitted:'待核验',returned:'已退回',completed:'已完成',cancelled:'已取消'};rows=records.filter(r=>r.kind==='enrollment').map(r=>[code(r.employeeId),name(r.employeeId),r.payload.title??'',r.payload.due??'',status[r.status]??r.status,r.payload.verifiedAt??'']);}
 if(q.dataset==='performance'){title='正式绩效结果';columns=['工号','姓名','期间','正式评级','分数','来源'];rows=records.filter(r=>r.kind==='performance'&&r.status==='published'&&r.payload.sourcePlanId&&!records.some(x=>x.payload.supersedes===r.id)).map(r=>[code(r.employeeId),name(r.employeeId),r.payload.period??'',r.payload.originalRating??'',r.payload.score??null,r.payload.source??'']);}
 if(q.dataset==='recruitmentOperations'){
  if(!['admin','hr','manager'].includes(ctx.member.role))throw new HttpError(403,'仅有组织管理权限的人员可查看招聘需求进度');
  title='可见范围招聘需求进度';columns=['招聘需求','岗位','所属组织','需求状态','需求版本','需求人数','累计已入职','剩余可入职','待审录用','已批准待登记接受','已接受待入职','筛选面试中','已结束候选流程'];
  const statuses:Record<string,string>={draft:'待审批',returned:'待修订',active:'招聘中',closed:'已关闭'};
  rows=records.filter(r=>r.kind==='requisition').map(q=>{const p=state.positions?.find(p=>p.id===q.positionId),candidates=records.filter(r=>r.kind==='candidate'&&r.referenceId===q.id),count=(status:string)=>candidates.filter(r=>r.status===status).length,hired=count('hired');return [q.payload.title??'',p?.name??'',org(p?.orgId??''),statuses[q.status]??q.status,q.payload.version??1,q.payload.headcount??null,hired,q.status==='active'?Math.max(0,(q.payload.headcount??0)-hired):null,count('offered'),count('approved'),count('accepted'),count('screening')+count('interviewed'),count('rejected')];});
 }
 if(q.dataset==='performanceOperations'){
  if(!['admin','hr','manager'].includes(ctx.member.role))throw new HttpError(403,'仅有组织管理权限的人员可查看绩效办理报表');
  title='可见范围绩效办理';columns=['工号','姓名','当前组织','期间','计划阶段','目标版本','待审目标调整','待反馈记录（所有版本）','其中本账号可反馈','其中旧目标版本记录','已反馈记录','最近提交跟进（北京时间）'];
  const statuses:Record<string,string>={draft:'待目标确认',confirmed:'待本人自评',submitted:'待管理者评价',evaluated:'待结果发布',cancelled:'已取消'};
  rows=records.filter(r=>r.kind==='performancePlan').map(p=>{
   const published=records.some(r=>r.kind==='performance'&&r.status==='published'&&r.payload.sourcePlanId===p.id),logs=records.filter(r=>r.kind==='performanceCheckin'&&r.referenceId===p.id),pending=logs.filter(r=>r.status==='submitted'),live=p.status==='confirmed'&&!!employee(p.employeeId)&&employee(p.employeeId)?.status!=='离职'&&records.some(c=>c.kind==='performanceCycle'&&c.id===p.referenceId&&c.status==='active')&&!published,last=logs.map(r=>r.payload.submittedAt??r.createdAt).sort().at(-1);
   return [code(p.employeeId),name(p.employeeId),org(employee(p.employeeId)?.orgId??''),p.payload.period??'',published?'结果已发布':statuses[p.status]??p.status,p.payload.version??1,records.filter(r=>r.kind==='performanceGoalChange'&&r.referenceId===p.id&&r.status==='submitted').length,pending.length,live&&p.employeeId!==ctx.member.employeeId?pending.filter(r=>r.createdBy!==ctx.member.userId).length:0,pending.filter(r=>r.payload.basePlanVersion!==(p.payload.version??1)).length,logs.filter(r=>r.status==='acknowledged').length,last?new Date(last).toLocaleString('sv-SE',{timeZone:'Asia/Shanghai',hour12:false}):null];
  });
 }
 if(q.dataset==='talentReview'){title='最新人才盘点';columns=['工号','姓名','期间','潜力档位','绩效快照档位','盘点版本','原版本编号'];rows=latestPublishedReviews(records).map(r=>[code(r.employeeId),name(r.employeeId),r.payload.period??'',r.payload.potential??null,typeof r.payload.performanceSnapshot?.band==='number'?r.payload.performanceSnapshot.band:null,r.payload.version??1,r.payload.supersedes??'']);}
 if(q.dataset==='successionCoverage'){
  if(!['admin','hr','manager'].includes(ctx.member.role))throw new HttpError(403,'仅有组织管理权限的人员可查看继任覆盖');
  title='可见范围继任覆盖';columns=['岗位编码','目标岗位','所属组织','现任人数','有效后备人数','现在可就任','预计一年','预计两年'];
  rows=(state.positions??[]).filter(p=>p.status==='启用').map(p=>{
   const candidates=new Map(records.filter(r=>r.kind==='succession'&&r.positionId===p.id&&r.status==='active'&&employee(r.employeeId)?.status!=='离职'&&!!employee(r.employeeId)).map(r=>[r.employeeId,r]));
   const ready=Array.from(candidates.values());return [p.code,p.name,org(p.orgId),state.employees.filter(e=>e.status!=='离职'&&e.positionId===p.id).length,ready.length,...['ready','one_year','two_years'].map(v=>ready.filter(r=>r.payload.readiness===v).length)];
  });
 }
 if(q.dataset==='instructorCampaignProgress'){
  if(!['admin','hr'].includes(ctx.member.role))throw new HttpError(403,'仅有权限HR可查看认证活动进度');
  title='可见范围认证活动进度';columns=['认证活动','活动组织','报名状态','报名记录数','待资格复核','资格通过','资格未通过','已撤回','已关联提名','在职在用讲师','最新试讲通过的提名','待完成必修培养关联'];
  const states:Record<string,string>={draft:'草稿',published:'已发布',closed:'已停止报名',cancelled:'已取消'};
  rows=records.filter(r=>r.kind==='instructorCampaign').map(c=>{const applications=records.filter(a=>a.kind==='instructorApplication'&&a.referenceId===c.id),profiles=records.filter(p=>p.kind==='instructorProfile'&&applications.some(a=>a.id===p.payload.instructorApplicationId));return [c.payload.title??'',org(c.payload.orgId!),states[c.status]??c.status,applications.length,...['submitted','approved','rejected','withdrawn'].map(s=>applications.filter(a=>a.status===s).length),profiles.length,profiles.filter(p=>p.status==='active'&&employee(p.employeeId)?.status!=='离职'&&!!employee(p.employeeId)).length,profiles.filter(p=>{const t=latestInstructorTrial(records,p.id);return t?.status==='published'&&t.payload.passed;}).length,profiles.filter(p=>p.status==='submitted').flatMap(p=>instructorDevelopmentProof(records,p.id)).filter(p=>p.mandatory&&p.status!=='completed').length];});
 }
 if(q.dataset==='instructorSchedule'||q.dataset==='trainingProgress'||q.dataset==='trainingRoster'){
  if(!['admin','hr','manager'].includes(ctx.member.role))throw new HttpError(403,'仅有组织管理权限的人员可查看培训管理报表');
  const trainings=records.filter(r=>r.kind==='training');
  const statuses:Record<string,string>={draft:'未发布',active:'进行中',closed:'已结束',cancelled:'已取消'};
  if(q.dataset==='instructorSchedule'){
   title='可见范围授课安排';columns=['培训项目','场次','讲师（排期快照）','身份关联','开始时间（北京时间）','结束时间（北京时间）','原排期分钟','有效计划分钟','场次状态'];
   const stamp=(s:string)=>new Date(s).toLocaleString('sv-SE',{timeZone:'Asia/Shanghai',hour12:false});
   rows=records.filter(r=>r.kind==='trainingSession'&&(!q.from||businessDate(r.payload.startAt!)>=q.from)&&(!q.to||businessDate(r.payload.startAt!)<=q.to)).map(r=>{
    const minutes=(Date.parse(r.payload.endAt!)-Date.parse(r.payload.startAt!))/60000;
    return [trainings.find(t=>t.id===r.referenceId)?.payload.name??'',r.payload.title??'',r.payload.instructor??'',r.payload.instructorEmployeeId?'已关联内部员工及认证快照':'未关联内部员工',stamp(r.payload.startAt!),stamp(r.payload.endAt!),minutes,r.status==='cancelled'?0:minutes,statuses[r.status]??r.status];
   });
  }else if(q.dataset==='trainingRoster'){
   title='可见范围班级学员名册';columns=['培训项目','课程','工号','姓名','人员状态','学习任务状态','必修场次数','已核验出席','已核验未出席','待核验或未登记','学习截止日'];
   const taskStatus:Record<string,string>={active:'进行中',submitted:'待成果核验',returned:'待补充成果',completed:'已完成'};
   rows=records.filter(r=>r.kind==='enrollment'&&r.status!=='cancelled'&&trainings.some(t=>t.id===r.payload.trainingId)).map(r=>{
    const required=records.filter(s=>s.kind==='trainingSession'&&s.referenceId===r.payload.trainingId&&s.payload.sessionCourseId===r.referenceId&&s.payload.mandatory&&s.status!=='cancelled');
    let present=0,absent=0;for(const session of required){const attendance=records.find(a=>a.kind==='trainingAttendance'&&a.referenceId===session.id&&a.employeeId===r.employeeId&&a.status==='verified');if(attendance?.payload.present===true)present++;if(attendance?.payload.present===false)absent++;}
    return [trainings.find(t=>t.id===r.payload.trainingId)?.payload.name??'',r.payload.title??'',code(r.employeeId),name(r.employeeId),employee(r.employeeId)?.status??'',taskStatus[r.status]??r.status,required.length,present,absent,required.length-present-absent,r.payload.due??''];
   });
  }else{
   title='可见范围培训项目进度';columns=['培训项目','所属组织','项目状态','可见报名人数','有效学习任务数','已完成任务','待核验任务','已取消任务','任务完成率（%）'];
   rows=trainings.map(t=>{const all=records.filter(r=>r.kind==='enrollment'&&r.payload.trainingId===t.id),valid=all.filter(r=>r.status!=='cancelled'),completed=valid.filter(r=>r.status==='completed').length;return [t.payload.name??'',org(t.payload.orgId!),statuses[t.status]??t.status,new Set(valid.map(r=>r.employeeId)).size,valid.length,completed,valid.filter(r=>r.status==='submitted').length,all.length-valid.length,valid.length?Math.round(completed/valid.length*10000)/100:null];});
  }
 }
 if(q.search)rows=rows.filter(r=>r.some(c=>String(c??'').toLocaleLowerCase().includes(q.search.toLocaleLowerCase())));
 return {title,columns,rows,dataset:q.dataset,asOf:new Date().toISOString(),revision:ctx.row.revision};
}
export function reportCsv(columns:string[],rows:Cell[][]){const cell=(v:Cell)=>{let s=String(v??'');if(typeof v==='string'&&/^[\s\uFEFF]*[=+@-]/u.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return '\uFEFF'+[columns,...rows].map(r=>r.map(cell).join(',')).join('\r\n');}
