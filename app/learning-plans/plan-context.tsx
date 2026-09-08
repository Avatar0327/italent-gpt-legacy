import type {DevelopmentRecord as R} from '@/lib/hris/development';

export default function PlanContext({task,records}:{task:R;records:R[]}){
 const plan=records.find(r=>r.kind==='learningAssignment'&&r.id===task.payload.learningAssignmentId);
 if(!plan)return null;
 return <div className="rounded border p-3 my-3"><h3>所属学习计划：{plan.payload.title} · v{plan.payload.version}</h3><p className="whitespace-pre-wrap text-sm mt-2">{plan.payload.description||'该计划未填写简介'}</p></div>;
}
