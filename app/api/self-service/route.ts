import {developmentContext,visibleDevelopment} from '@/lib/hris/development-repository';
import {visibleState} from '@/lib/hris/authorization';
import {json,failure} from '@/lib/hris/http';
export async function GET(){try{const ctx=await developmentContext(),state=visibleState(ctx.state,ctx.member),all=visibleDevelopment(ctx),records=all.filter(r=>r.employeeId===ctx.member.employeeId),employee=state.employees.find(e=>e.id===ctx.member.employeeId)??null;
 const tasks=records.filter(r=>(['plan','enrollment'].includes(r.kind)&&['active','returned'].includes(r.status))||(r.kind==='performancePlan'&&r.status==='confirmed')).map(r=>({id:r.id,title:r.payload.title??(r.kind==='performancePlan'?`${r.payload.period} 绩效自评`:'发展行动'),due:r.payload.due??'',kind:r.kind,href:r.kind==='enrollment'?'/learning':r.kind==='performancePlan'?'/performance':'/development'}));
 const requests=records.filter(r=>['leave','correction'].includes(r.kind)).map(r=>({id:r.id,kind:r.kind,title:r.kind==='leave'?'请假申请':'补卡申请',status:r.status,at:r.updatedAt,href:'/attendance'}));
 return json({employee,tasks,requests,payslipCount:records.filter(r=>r.kind==='paySlip'&&r.status!=='cancelled'&&ctx.records.some(b=>b.id===r.referenceId&&b.status==='published')).length,revision:ctx.row.revision});}catch(e){return failure(e);}}
