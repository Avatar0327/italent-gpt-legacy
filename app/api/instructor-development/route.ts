import {z} from 'zod';
import {developmentContext,visibleDevelopment,saveDevelopment} from '@/lib/hris/development-repository';
import {applyInstructorDevelopment} from '@/lib/hris/instructor-development';
import {visibleState} from '@/lib/hris/authorization';
import {json,failure,readBody} from '@/lib/hris/http';
export async function GET(){try{const ctx=await developmentContext(['instructorProfile','instructorDevelopment','enrollment']),state=visibleState(ctx.state,ctx.member);return json({records:visibleDevelopment(ctx),employees:state.employees.map(e=>({id:e.id,name:e.name,status:e.status})),revision:ctx.row.revision,role:ctx.member.role,employeeId:ctx.member.employeeId,userId:ctx.member.userId});}catch(e){return failure(e);}}
export async function POST(request:Request){try{const body=z.object({revision:z.number().int().nonnegative(),command:z.unknown()}).parse(await readBody(request)),ctx=await developmentContext(['instructorProfile','instructorDevelopment','enrollment']),r=applyInstructorDevelopment(ctx.records,ctx.state,ctx.member,body.command);await saveDevelopment(ctx,body.revision,r,'认证培养任务：'+String((body.command as {action:string}).action));return json({id:r.id,revision:body.revision+1});}catch(e){return failure(e);}}
