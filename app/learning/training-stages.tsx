'use client';
import {useState,type FormEvent} from 'react';
import {Button} from '@/components/ui/button';
import {Input} from '@/components/ui/input';
import type {DevelopmentRecord as R} from '@/lib/hris/development';

export default function TrainingStages({training,records,busy,send}:{training:R;records:R[];busy:boolean;send:(command:Record<string,unknown>)=>unknown}){
 const [stages,setStages]=useState(training.payload.trainingStages??[{title:'第一阶段',courseIds:training.payload.courseIds??[]}]);
 const courses=records.filter(r=>r.kind==='course'&&r.status==='published');
 function submit(e:FormEvent){e.preventDefault();send({action:'trainingStages',id:training.id,stages});}
 return <form onSubmit={submit} className="rounded border p-4 space-y-4"><h3 className="font-semibold">配置课程阶段</h3><p className="text-sm text-slate-500">启动后阶段配置冻结。前一阶段全部课程通过独立成果核验后，才能安排下一阶段；同一阶段内课程可同时学习。已有非项目学习记录不会自动计入。</p>{stages.map((stage,index)=><fieldset key={index} className="border rounded p-3 space-y-3" disabled={busy}><legend className="px-2">阶段 {index+1}</legend><Input required maxLength={200} aria-label={`阶段${index+1}名称`} value={stage.title} onChange={e=>setStages(stages.map((s,i)=>i===index?{...s,title:e.target.value}:s))}/><label className="block text-sm">课程版本（可多选）<select multiple required aria-label={`阶段${index+1}课程`} className="mt-2 w-full rounded border p-2 min-h-24" value={stage.courseIds} onChange={e=>{const courseIds=Array.from(e.target.selectedOptions,o=>o.value);setStages(stages.map((s,i)=>i===index?{...s,courseIds}:s));}}>{courses.map(c=><option key={c.id} value={c.id} disabled={stages.some((s,i)=>i!==index&&s.courseIds.includes(c.id))}>{c.payload.title} · V{c.payload.version??1}</option>)}</select></label>{stages.length>1&&<Button type="button" size="sm" variant="outline" onClick={()=>setStages(stages.filter((_,i)=>i!==index))}>移除此阶段</Button>}</fieldset>)}<div className="flex gap-2"><Button type="button" variant="outline" disabled={busy||stages.length>=10} onClick={()=>setStages([...stages,{title:`阶段 ${stages.length+1}`,courseIds:[]}])}>添加阶段</Button><Button type="submit" disabled={busy}>保存阶段配置</Button></div></form>;
}
