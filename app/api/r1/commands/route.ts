import {z} from 'zod';
import {memberContext} from '@/lib/hris/context';
import {json,failure,readBody,HttpError} from '@/lib/hris/http';
import {executeM01} from '@/lib/hris/r1-m01';
export const dynamic='force-dynamic';
const input=z.object({commandId:z.string().uuid(),idempotencyKey:z.string().min(1).max(100),action:z.string().min(1).max(100),payload:z.unknown(),expectedWorkspaceRevision:z.number().int().nonnegative(),expectedAuthorizationRevision:z.number().int().nonnegative(),expectedWriterEpoch:z.number().int().nonnegative(),expectedRecoveryEpoch:z.number().int().nonnegative()}).strict();
export async function POST(request:Request){try{
 const b=input.parse(await readBody(request)),ctx=await memberContext();
 const operation=(b.payload as {operation?:string}|null)?.operation;
 if(!operation||b.action!=='M01.'+operation)throw new HttpError(400,'命令动作与载荷不匹配','UNKNOWN_COMMAND');
 return json(await executeM01(ctx,{...b,payload:b.payload}));
}catch(e){return failure(e);}}
