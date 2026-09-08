import {z} from 'zod';
import type {DevelopmentRecord as R} from './development';
import {learningRequirements} from './learning-requirements';
const policy={attempts:z.enum(['all','passed']),decimals:z.number().int().min(0).max(2)};
export const learningGradeRuleSchema=z.discriminatedUnion('mode',[
 z.object({mode:z.literal('none')}).strict(),
 z.object({mode:z.literal('allHighest'),...policy}).strict(),
 z.object({mode:z.literal('allAttemptsAverage'),...policy}).strict(),
 z.object({mode:z.literal('eachExamHighestAverage'),...policy}).strict(),
 z.object({mode:z.literal('specifiedExamHighest'),examId:z.string().min(1).max(100),...policy}).strict(),
]);
export type LearningGradeRule=z.infer<typeof learningGradeRuleSchema>;
export function learningGrade(assignment:R,records:R[]){
 const parsed=learningGradeRuleSchema.safeParse(assignment.payload.gradeRule??{mode:'none'});
 const pending=(missingExamIds:string[]=[])=>({state:'pending' as const,score:null,missingExamIds,attemptIds:[] as string[]});
 if(!parsed.success)return pending();
 const rule=parsed.data;
 if(rule.mode==='none')return {state:'not_configured' as const,score:null,missingExamIds:[],attemptIds:[] as string[]};
 const examIds=rule.mode==='specifiedExamHighest'?[rule.examId]:assignment.payload.examIds??[];
 if(!examIds.length||new Set(examIds).size!==examIds.length||examIds.some(id=>!assignment.payload.examIds?.includes(id)))return pending(examIds);
 const requirements=learningRequirements(assignment),groups=examIds.map(examId=>{
  const requirement=requirements.find(r=>r.kind==='exam'&&r.resourceId===examId);
  const tasks=records.filter(r=>r.kind==='learningExamTask'&&r.payload.learningAssignmentId===assignment.id&&r.employeeId===assignment.employeeId&&r.referenceId===examId&&r.payload.learningRequirementId===requirement?.id);
  const task=requirement&&tasks.length===1?tasks[0]:undefined;
  return {examId,attempts:task?records.filter(r=>r.kind==='learningExamAttempt'&&r.referenceId===task.id&&r.employeeId===assignment.employeeId&&r.payload.examId===examId&&Number.isFinite(r.payload.score)&&r.payload.score!>=0&&r.payload.score!<=100&&(rule.attempts==='all'||r.payload.passed===true)):[]};
 });
 const missing=groups.filter(g=>!g.attempts.length).map(g=>g.examId);
 if(missing.length)return pending(missing);
 const attempts=groups.flatMap(g=>g.attempts),scores=attempts.map(a=>a.payload.score!),mean=(values:number[])=>values.reduce((a,b)=>a+b,0)/values.length;
 const raw=rule.mode==='allAttemptsAverage'?mean(scores):rule.mode==='eachExamHighestAverage'?mean(groups.map(g=>Math.max(...g.attempts.map(a=>a.payload.score!)))):Math.max(...scores);
 const factor=10**rule.decimals,score=Math.round((raw+Number.EPSILON)*factor)/factor;
 return {state:assignment.status==='completed'?'final' as const:'provisional' as const,score,missingExamIds:[],attemptIds:attempts.map(a=>a.id).sort()};
}
