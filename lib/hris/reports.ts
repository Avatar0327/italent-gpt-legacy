import {HttpError} from './http';
import {latestPublishedReviews} from './review-versions';
import {z} from 'zod';
import {visibleState} from './authorization';
import {visibleDevelopment,type DevelopmentContext} from './development-repository';
import {attendanceReport} from './attendance';
export const reportQuery=z.object({dataset:z.enum(['workforce','attendance','learning','performance','talentReview','successionCoverage']).default('workforce'),from:z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),to:z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),search:z.string().max(100).default('')}).refine(q=>!q.from||!q.to||q.from<=q.to,'开始日期不能晚于结束日期');
export const reportKinds={successionCoverage:['succession'],talentReview:['review'],workforce:[],attendance:['shift','clock','correction','leaveType','leaveCredit','leave'],learning:['enrollment'],performance:['performance','performancePlan','performanceCycle']} as const;
export type Cell=string|number|null;
export function makeReport(ctx:DevelopmentContext,input:unknown){
 const q=reportQuery.parse(input),state=visibleState(ctx.state,ctx.member),records=visibleDevelopment(ctx),employee=(id:string|null)=>state.employees.find(e=>e.id===id),name=(id:string|null)=>employee(id)?.name??'',code=(id:string|null)=>employee(id)?.code??'',org=(id:string)=>state.orgs.find(o=>o.id===id)?.name??'';
 let columns:string[]=[],rows:Cell[][]=[],title='';
 if(q.dataset==='workforce'){title='员工名册';columns=['工号','姓名','组织','岗位','人员状态','入职日期'];const email=ctx.member.role==='admin'||ctx.member.viewEmail,level=ctx.member.role==='admin'||ctx.member.viewLevel;if(email)columns.push('邮箱');if(level)columns.push('职级');rows=state.employees.map(e=>{const row:Cell[]=[e.code,e.name,org(e.orgId),e.job,e.status,e.joined];if(email)row.push(e.email);if(level)row.push(e.level);return row;});}
 if(q.dataset==='attendance'){title='出勤核验';columns=['工号','姓名','日期','班次','计划分钟','批准请假分钟','未覆盖分钟','状态'];rows=attendanceReport(records).filter(r=>(!q.from||(r.date??'')>=q.from)&&(!q.to||(r.date??'')<=q.to)).map(r=>[code(r.employeeId),name(r.employeeId),r.date??'',r.name??'',r.plannedMinutes,r.approvedLeaveMinutes,r.uncoveredMinutes,r.status]);}
 if(q.dataset==='learning'){title='学习任务';columns=['工号','姓名','课程','截止日期','状态','成果核验时间'];const status:Record<string,string>={active:'进行中',submitted:'待核验',returned:'已退回',completed:'已完成',cancelled:'已取消'};rows=records.filter(r=>r.kind==='enrollment').map(r=>[code(r.employeeId),name(r.employeeId),r.payload.title??'',r.payload.due??'',status[r.status]??r.status,r.payload.verifiedAt??'']);}
 if(q.dataset==='performance'){title='正式绩效结果';columns=['工号','姓名','期间','正式评级','分数','来源'];rows=records.filter(r=>r.kind==='performance'&&r.status==='published'&&r.payload.sourcePlanId&&!records.some(x=>x.payload.supersedes===r.id)).map(r=>[code(r.employeeId),name(r.employeeId),r.payload.period??'',r.payload.originalRating??'',r.payload.score??null,r.payload.source??'']);}
 if(q.dataset==='talentReview'){title='最新人才盘点';columns=['工号','姓名','期间','潜力档位','绩效快照档位','盘点版本','原版本编号'];rows=latestPublishedReviews(records).map(r=>[code(r.employeeId),name(r.employeeId),r.payload.period??'',r.payload.potential??null,typeof r.payload.performanceSnapshot?.band==='number'?r.payload.performanceSnapshot.band:null,r.payload.version??1,r.payload.supersedes??'']);}
 if(q.dataset==='successionCoverage'){
  if(!['admin','hr','manager'].includes(ctx.member.role))throw new HttpError(403,'仅有组织管理权限的人员可查看继任覆盖');
  title='可见范围继任覆盖';columns=['岗位编码','目标岗位','所属组织','现任人数','有效后备人数','现在可就任','预计一年','预计两年'];
  rows=(state.positions??[]).filter(p=>p.status==='启用').map(p=>{
   const candidates=new Map(records.filter(r=>r.kind==='succession'&&r.positionId===p.id&&r.status==='active'&&employee(r.employeeId)?.status!=='离职'&&!!employee(r.employeeId)).map(r=>[r.employeeId,r]));
   const ready=Array.from(candidates.values());return [p.code,p.name,org(p.orgId),state.employees.filter(e=>e.status!=='离职'&&e.positionId===p.id).length,ready.length,...['ready','one_year','two_years'].map(v=>ready.filter(r=>r.payload.readiness===v).length)];
  });
 }
 if(q.search)rows=rows.filter(r=>r.some(c=>String(c??'').toLocaleLowerCase().includes(q.search.toLocaleLowerCase())));
 return {title,columns,rows,dataset:q.dataset,asOf:new Date().toISOString(),revision:ctx.row.revision};
}
export function reportCsv(columns:string[],rows:Cell[][]){const cell=(v:Cell)=>{let s=String(v??'');if(typeof v==='string'&&/^[\s\uFEFF]*[=+@-]/u.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return '\uFEFF'+[columns,...rows].map(r=>r.map(cell).join(',')).join('\r\n');}
