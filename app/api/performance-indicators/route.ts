import {z} from 'zod';
import {developmentContext,visibleDevelopment,saveDevelopment} from '@/lib/hris/development-repository';
import {applyPerformanceIndicator} from '@/lib/hris/performance-indicators';
import {json,failure,readBody} from '@/lib/hris/http';
export async function GET(){try{const c=await developmentContext(['performanceIndicator'],['admin','hr','manager','employee']);return json({records:visibleDevelopment(c),revision:c.row.revision,role:c.member.role});}catch(e){return failure(e);}}
export async function POST(request:Request){try{const b=z.object({revision:z.number().int().nonnegative(),command:z.unknown()}).strict().parse(await readBody(request,32768)),c=await developmentContext(['performanceIndicator'],['admin','hr']),r=applyPerformanceIndicator(c.records,c.state,c.member,b.command);await saveDevelopment(c,b.revision,r,'绩效指标：'+String((b.command as {action:string}).action));return json({id:r.id,revision:b.revision+1});}catch(e){return failure(e);}}
