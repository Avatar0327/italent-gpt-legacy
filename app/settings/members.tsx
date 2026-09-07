'use client';
import {useEffect,useState,type FormEvent} from 'react';
import Link from 'next/link';
import Workflows from './workflows';
import {Button} from '@/components/ui/button';
import {Input} from '@/components/ui/input';
import {Table,TableBody,TableCell,TableHead,TableHeader,TableRow} from '@/components/ui/table';
import {Dialog,DialogContent,DialogHeader,DialogTitle,DialogDescription} from '@/components/ui/dialog';
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue} from '@/components/ui/select';
import {Switch} from '@/components/ui/switch';
import {Skeleton} from '@/components/ui/skeleton';
type Role='admin'|'hr'|'approver'|'employee';
type Member={email:string;name:string;role:Role;employeeId:string|null;active:number;userId:string|null};
type Access={email:string;role:Role|null;canSetup:boolean;canActivate:boolean;company:string|null};
type Data={members:Member[];revision:number;employees:{id:string;name:string;status:string}[]};
const roles:Record<Role,string>={admin:'系统管理员',hr:'人事管理员',approver:'审批人',employee:'员工'};
const fresh=()=>({email:'',name:'',role:'employee' as Role,employeeId:null as string|null,active:1,userId:null});
export default function Members(){
 const [access,setAccess]=useState<Access|null>(null),[data,setData]=useState<Data|null>(null),[name,setName]=useState(''),[error,setError]=useState(''),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false),[form,setForm]=useState<Member|null>(null),[editing,setEditing]=useState(false);
 const get=async<T,>(path:string):Promise<T>=>{const r=await fetch(path,{cache:'no-store'});const d=await r.json() as T&{error?:string};if(!r.ok)throw Error(d.error);return d;};
 const load=async()=>{setError('');try{const a=await get<Access>('/api/access');setAccess(a);setData(a.role==='admin'?await get<Data>('/api/members'):null);}catch(e){setError((e as Error).message);}};
 useEffect(()=>{load();},[]);
 const post=async(path:string,body:unknown)=>{setBusy(true);setError('');setNotice('');try{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const d=await r.json() as {error?:string};if(!r.ok){if(r.status===409)await load();throw Error(d.error);}setForm(null);await load();setNotice('已保存');}catch(e){setError((e as Error).message);}finally{setBusy(false);}};
 const submit=(e:FormEvent)=>{e.preventDefault();if(form&&data)post('/api/members',{...form,active:!!form.active,revision:data.revision});};
 return <main className="main-content mx-auto max-w-6xl"><div className="page-head"><div><Link className="text-link" href="/">返回导航台</Link><h1>企业与成员管理</h1></div><Button variant="outline" onClick={load} disabled={busy}>刷新</Button></div>
 {error&&<div className="panel error" role="alert">{error}</div>}{notice&&<p role="status" className="my-4 text-green-700">{notice}</p>}
 {!access&&!error&&<Skeleton className="h-64"/>}
 {access?.canSetup&&<section className="panel p-6 max-w-xl"><h2 className="text-xl font-semibold mb-4">开通企业空间</h2><p className="mb-4 text-slate-600">创建空白企业后，您将成为系统管理员。组织和员工可在导航台中新增。</p><form onSubmit={e=>{e.preventDefault();post('/api/access',{action:'setup',name});}}><label className="field"><span>企业名称</span><Input value={name} onChange={e=>setName(e.target.value)} required minLength={2} maxLength={100}/></label><Button className="mt-4" disabled={busy}>创建企业</Button></form></section>}
 {access?.canActivate&&<section className="panel p-6"><h2 className="text-xl font-semibold">激活企业成员</h2><p className="my-4">使用当前账号 {access.email} 接受管理员已配置的成员授权。</p><Button disabled={busy} onClick={()=>post('/api/access',{action:'activate'})}>激活我的访问权限</Button></section>}
 {access&&!access.role&&!access.canSetup&&!access.canActivate&&<section className="panel p-6"><h2>尚未开通访问权限</h2><p className="my-4">当前账号：{access.email}。请由企业管理员添加该邮箱并启用成员。</p></section>}
 {access?.role&&access.role!=='admin'&&<section className="panel p-6"><p>当前角色：{roles[access.role]}。成员管理仅向系统管理员开放。</p><Link className="text-link" href="/">进入工作台</Link></section>}
 {data&&<section className="panel"><div className="section-head"><div><h2>{access?.company??'企业成员'}</h2><p className="text-slate-500 mt-2">配置系统内权限。成员还需获得本站访问权，再使用对应邮箱登录并激活。</p></div><Button onClick={()=>{setEditing(false);setForm(fresh());}}>添加成员</Button></div><Table><TableHeader><TableRow>{['成员','角色','关联员工','状态','操作'].map(t=><TableHead key={t}>{t}</TableHead>)}</TableRow></TableHeader><TableBody>{data.members.map(m=><TableRow key={m.email}><TableCell><b>{m.name}</b><p className="text-slate-500">{m.email}</p></TableCell><TableCell>{roles[m.role]}</TableCell><TableCell>{data.employees.find(e=>e.id===m.employeeId)?.name??'未关联'}</TableCell><TableCell>{!m.active?'已停用':m.userId?'已激活':'待激活'}</TableCell><TableCell><Button variant="ghost" onClick={()=>{setEditing(true);setForm({...m});}}>编辑</Button></TableCell></TableRow>)}</TableBody></Table></section>}
 {data&&<Workflows members={data.members}/>}
 <Dialog open={!!form} onOpenChange={open=>!open&&!busy&&setForm(null)}><DialogContent><DialogHeader><DialogTitle>{editing?'编辑成员':'添加成员'}</DialogTitle><DialogDescription>员工角色仅可查看本人档案与申请。审批人可查看企业人员并处理审批。</DialogDescription></DialogHeader>{form&&<form onSubmit={submit} className="edit-form"><label className="field"><span>姓名</span><Input value={form.name} required maxLength={100} onChange={e=>setForm({...form,name:e.target.value})}/></label><label className="field"><span>登录邮箱</span><Input type="email" value={form.email} required disabled={editing} onChange={e=>setForm({...form,email:e.target.value})}/></label><div className="field"><span>角色</span><Select value={form.role} onValueChange={v=>setForm({...form,role:v as Role})}><SelectTrigger aria-label="角色"><SelectValue/></SelectTrigger><SelectContent>{Object.entries(roles).map(([v,l])=><SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent></Select></div><div className="field"><span>关联员工</span><Select value={form.employeeId??'none'} onValueChange={v=>setForm({...form,employeeId:v==='none'?null:v})}><SelectTrigger aria-label="关联员工"><SelectValue/></SelectTrigger><SelectContent><SelectItem value="none">不关联</SelectItem>{data?.employees.filter(e=>e.status!=='离职').map(e=><SelectItem key={e.id} value={e.id}>{e.name}</SelectItem>)}</SelectContent></Select></div><label className="flex items-center gap-3"><Switch checked={!!form.active} onCheckedChange={v=>setForm({...form,active:Number(v)})}/>启用成员</label><div className="form-actions"><Button type="button" variant="outline" onClick={()=>setForm(null)} disabled={busy}>取消</Button><Button disabled={busy}>{busy?'保存中…':'保存'}</Button></div></form>}</DialogContent></Dialog>
 </main>;
}
