import {z} from 'zod';
import {developmentContext,visibleDevelopment,saveDevelopment} from '@/lib/hris/development-repository';
import {applyPerformance} from '@/lib/hris/performance';
import {json,failure,readBody} from '@/lib/hris/http';
export async function GET(){try{const ctx=await developmentContext(['performanceCycle', 'performancePlan', 'performance']);return json({records:visibleDevelopment(ctx).filter(r=>['performanceCycle','performancePlan','performance'].includes(r.kind)),revision:ctx.row.revision,role:ctx.member.role,employeeId:ctx.member.employeeId,userId:ctx.member.userId});}catch(e){return failure(e);}}
export async function POST(request:Request){try{const body=z.object({revision:z.number().int().nonnegative(),command:z.unknown()}).parse(await readBody(request));const ctx=await developmentContext(['performanceCycle', 'performancePlan', 'performance']),record=applyPerformance(ctx.records,ctx.state,ctx.member,body.command);await saveDevelopment(ctx,body.revision,record,'绩效：'+String((body.command as {action:string}).action));return json({id:record.id,revision:body.revision+1});}catch(e){return failure(e);}}
