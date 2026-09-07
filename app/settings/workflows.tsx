'use client';
import {useEffect,useState} from 'react';
import {Button} from '@/components/ui/button';
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue} from '@/components/ui/select';
import type {State,Approval} from '@/lib/hris/model';
type Reviewer={userId:string|null;name:string;role:string;active:number};
const kinds={transfer:'调动申请',regularize:'转正申请',exit:'离职申请'};
export default function Workflows({members}:{members:Reviewer[]}){
 const [kind,setKind]=useState<Approval['kind']>('transfer'),[data,setData]=useState<{state:State;revision:number}|null>(null),[steps,setSteps]=useState<string[]>([]),[error,setError]=useState(''),[busy,setBusy]=useState(false),[notice,setNotice]=useState('');
 const load=async()=>{try{const r=await fetch('/api/hris',{cache:'no-store'});const d=await r.json() as {state:State;revision:number;error?:string};if(!r.ok)throw Error(d.error);setData(d);}catch(e){setError((e as Error).message);}};
 useEffect(()=>{load();},[]);useEffect(()=>{setSteps(data?.state.workflows?.[kind]?.steps.map(s=>s.userId)??[]);setNotice('');},[data,kind]);
 const reviewers=members.filter(m=>m.userId&&m.active&&['admin','approver'].includes(m.role));
 const save=async()=>{setBusy(true);setError('');setNotice('');try{const r=await fetch('/api/hris',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({revision:data?.revision,command:{action:'workflow',kind,steps:steps.map(userId=>({userId,name:reviewers.find(m=>m.userId===userId)?.name??''}))}})});const d=await r.json() as {state:State;revision:number;error?:string};if(!r.ok){if(r.status===409)await load();throw Error(d.error);}setData(d);setNotice('审批流程已保存，新申请将使用本版本。');}catch(e){setError((e as Error).message);}finally{setBusy(false);}};
 return <section className="panel mt-6 p-6"><h2 className="text-xl font-semibold">审批流程</h2><p className="text-slate-500 my-3">依次设置 1–5 级审批人。全部通过后更新员工档案；任一级驳回即结束。修改流程不影响已提交申请。</p>{error&&<p role="alert" className="text-red-700 my-3">{error}</p>}{notice&&<p role="status">{notice}</p>}<Select value={kind} onValueChange={v=>setKind(v as Approval['kind'])}><SelectTrigger className="max-w-sm" aria-label="申请类型"><SelectValue/></SelectTrigger><SelectContent>{Object.entries(kinds).map(([v,l])=><SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent></Select>
 {steps.map((id,i)=><div className="flex items-center gap-3 my-4" key={i}><span className="shrink-0">第 {i+1} 级</span><Select value={id} onValueChange={v=>setSteps(steps.map((old,j)=>j===i?v:old))}><SelectTrigger className="max-w-sm" aria-label={`第${i+1}级审批人`}><SelectValue placeholder="选择审批人"/></SelectTrigger><SelectContent>{reviewers.map(m=><SelectItem key={m.userId} value={m.userId!}>{m.name}</SelectItem>)}</SelectContent></Select><Button variant="ghost" onClick={()=>setSteps(steps.filter((_,j)=>j!==i))}>移除</Button></div>)}
 {!reviewers.length&&<p className="my-4">先添加并激活审批人，再配置流程。</p>}<div className="flex gap-3 mt-4"><Button variant="outline" disabled={steps.length>=5||busy} onClick={()=>setSteps([...steps,''])}>添加一级</Button><Button disabled={busy||!data||!steps.length||steps.some(s=>!s)||new Set(steps).size!==steps.length} onClick={save}>{busy?'保存中…':'保存流程'}</Button></div></section>;
}
