import {HttpError} from './http';
import {scopedOrgs} from './authorization';
import {visibleDevelopment,type DevelopmentContext} from './development-repository';
import {latestPublishedReviews} from './review-versions';
import {businessDate} from './workforce';
import type {DevelopmentRecord as R} from './development';
export const cadreProfileKinds=['cadreTerm','employeeExperience','cadreNomination','cadreObservation','qualificationApplication','succession','review','performance','plan','enrollment'] as const;
export type ProfileItem={id:string;title:string;status:string;detail:string;date:string;href:string};
export type CadreProfile={employee:{id:string;code:string;name:string;org:string;job:string;status:string};sections:{key:string;title:string;items:ProfileItem[]}[];revision:number;asOf:string};
const states:Record<string,string>={submitted:'待审议 / 核验',approved:'已批准',rejected:'未通过',withdrawn:'已撤回',appointed:'任用已核对',active:'进行中',returned:'待补充',completed:'已完成',development_needed:'需继续发展',closed:'已关闭',cancelled:'已取消',certified:'已认证',revoked:'已撤销',published:'已发布'};
export function cadreProfile(ctx:DevelopmentContext,employeeId:string,at=new Date().toISOString()):CadreProfile{
 const m=ctx.member,e=ctx.state.employees.find(e=>e.id===employeeId);
 if(!['admin','hr','manager'].includes(m.role)||!e||!scopedOrgs(ctx.state,m).has(e.orgId))throw new HttpError(403,'没有此员工的人才档案管理权限');
 const records=visibleDevelopment(ctx).filter(r=>r.employeeId===e.id),latest=latestPublishedReviews(records),perf=records.filter(r=>r.kind==='performance'&&(r.status==='published'||!r.payload.sourcePlanId&&r.status==='active')&&!records.some(x=>x.kind==='performance'&&x.payload.supersedes===r.id));
 const item=(r:R,title:string,detail:string,href:string,status=states[r.status]??r.status):ProfileItem=>({id:r.id,title,status,detail,date:r.payload.due??r.payload.validUntil??businessDate(r.updatedAt),href});
 const section=(key:string,title:string,items:ProfileItem[])=>({key,title,items:items.sort((a,b)=>b.date.localeCompare(a.date)||a.id.localeCompare(b.id))});
 return {employee:{id:e.id,code:e.code,name:e.name,org:ctx.state.orgs.find(o=>o.id===e.orgId)?.name??'',job:e.job,status:e.status},revision:ctx.row.revision,asOf:at,sections:[
  ...(['admin','hr'].includes(m.role)?[section('experiences','已登记人员经历',records.filter(r=>r.kind==='employeeExperience'&&r.status==='active').map(r=>item(r,r.payload.title??'人员经历',`${({education:'教育',employment:'工作',project:'项目'})[r.payload.experienceCategory!]??'经历'} · ${r.payload.institution??''} · ${r.payload.startMonth??''} 至 ${r.payload.ongoing?'今':r.payload.endMonth??''}`,'/employee-experiences','资料登记，未代表外部核验')))]:[]),
  section('terms','干部任期登记',records.filter(r=>r.kind==='cadreTerm'&&r.status!=='voided').map(r=>item(r,r.payload.targetPositionName??'任用岗位',`${r.payload.cadreTerm?.start??''} 至 ${r.payload.cadreTerm?.actualEnd??r.payload.cadreTerm?.expectedEnd??'未登记结束日期'}`,'/cadre-terms',r.status==='ended'?'已结束':'已登记'))),
  section('nominations','选拔与任用',records.filter(r=>r.kind==='cadreNomination').map(r=>item(r,r.payload.targetPositionName??'目标岗位',r.status==='appointed'?'已核对正式调动记录':'提名记录不等同于正式任职','/cadres'))),
  section('observations','任职考察',records.filter(r=>r.kind==='cadreObservation').map(r=>item(r,r.payload.targetPositionName??'任职考察',r.payload.objectives??'未登记考察目标','/cadres'))),
  section('qualifications','内部任职资格',records.filter(r=>r.kind==='qualificationApplication').map(r=>item(r,r.payload.name??'资格认证',r.payload.certificateNumber??'未登记证书编号','/qualifications',r.status==='certified'&&r.payload.validUntil&&r.payload.validUntil<businessDate(at)?'已到期':states[r.status]??r.status))),
  section('succession','后备梯队',records.filter(r=>r.kind==='succession').map(r=>item(r,ctx.state.positions?.find(p=>p.id===r.positionId)?.name??'目标岗位',({ready:'现在可就任',one_year:'预计一年',two_years:'预计两年'})[r.payload.readiness??'']??'未评定','/development'))),
  section('reviews','最新人才盘点',latest.map(r=>item(r,r.payload.period??'盘点期间',`潜力：${r.payload.potential===1?'低':r.payload.potential===2?'中':r.payload.potential===3?'高':'未评定'} · 版本 ${r.payload.version??1}`,'/development'))),
  section('performance','最新核定绩效',perf.map(r=>item(r,r.payload.period??'绩效期间',`${r.payload.originalRating??'未评级'} · ${r.payload.sourcePlanId?'正式考核结果':'历史核定录入'}`,r.payload.sourcePlanId?'/performance':'/development'))),
  section('plans','发展行动',records.filter(r=>r.kind==='plan').map(r=>item(r,r.payload.title??'发展计划',`目标等级：${r.payload.target??'未评定'}`,'/development'))),
  section('learning','学习任务',records.filter(r=>r.kind==='enrollment').map(r=>item(r,r.payload.title??'学习任务',r.status==='completed'?(r.payload.sourceEnrollmentId?'引用历史核验完成 · 原核验 '+r.payload.sourceVerifiedAt:'成果已通过核验'):'以学习模块当前办理状态为准','/learning'))),
 ]};
}
