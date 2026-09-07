import { getChatGPTUser } from '@/app/chatgpt-auth';
import { getDb } from '@/db';
import { workspaces } from '@/db/schema';
import { and, eq } from 'drizzle-orm';
import { applyCommand, initialState } from '@/lib/hris/model';
export const dynamic='force-dynamic';
async function context(){const user=await getChatGPTUser();if(!user)return null;const db=getDb();await db.insert(workspaces).values({owner:user.email,revision:0,data:JSON.stringify(initialState())}).onConflictDoNothing();const [row]=await db.select().from(workspaces).where(eq(workspaces.owner,user.email));return {user,db,row};}
export async function GET(){try{const c=await context();if(!c)return Response.json({error:'请先登录'}, {status:401});return Response.json({state:JSON.parse(c.row.data),revision:c.row.revision}, {headers:{'Cache-Control':'no-store'}});}catch{return Response.json({error:'数据暂时无法读取，请稍后重试'}, {status:503});}}
export async function POST(request:Request){
 const origin=request.headers.get('origin');if(origin&&new URL(request.url).origin!==origin)return Response.json({error:'请求来源无效'},{status:403});
 try{const c=await context();if(!c)return Response.json({error:'请先登录'},{status:401});const body=await request.json() as {revision?:number;command?:unknown};if(body.revision!==c.row.revision)return Response.json({error:'数据已更新，请刷新后重试'},{status:409});let next;try{next=applyCommand(JSON.parse(c.row.data),body.command);}catch(error){return Response.json({error:error instanceof Error?error.message:'参数无效'},{status:400});}
 const rows=await c.db.update(workspaces).set({data:JSON.stringify(next),revision:c.row.revision+1}).where(and(eq(workspaces.owner,c.user.email),eq(workspaces.revision,c.row.revision))).returning({revision:workspaces.revision});if(!rows.length)return Response.json({error:'数据已被其他会话更新，请刷新'},{status:409});return Response.json({state:next,revision:rows[0].revision});
 }catch{return Response.json({error:'保存失败，请重试'},{status:503});}
}
