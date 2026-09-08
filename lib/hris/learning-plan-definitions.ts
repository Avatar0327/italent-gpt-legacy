import {z} from 'zod';
import {learningModeSchema} from './learning-plan-model';
import {scopedOrgs,type Member} from './authorization';
import {visibleRecord,type DevelopmentRecord as R} from './development';
import type {State} from './model';
import {HttpError} from './http';
const id=z.string().min(1).max(100),title=z.string().trim().min(1).max(200);
const fields={title,orgId:id,config:learningModeSchema,courseIds:z.array(id).min(1).max(20)};
const schema=z.discriminatedUnion('action',[
 z.object({action:z.literal('create'),...fields}).strict(),
 z.object({action:z.literal('edit'),id,...fields}).strict(),
 z.object({action:z.literal('seal'),id}).strict(),
 z.object({action:z.literal('revise'),id}).strict(),
 z.object({action:z.literal('archive'),id}).strict(),
]);
export function applyLearningDefinition(records:R[],state:State,member:Member,input:unknown,at=new Date().toISOString()):R{
 const c=schema.parse(input),scope=scopedOrgs(state,member);
 const deny=():never=>{throw new HttpError(403,'没有此学习计划配置的管理权限');};
 const fail=(message:string):never=>{throw new HttpError(400,message);};
 if(!['admin','hr'].includes(member.role))deny();
 const old=c.action==='create'?undefined:records.find(r=>r.kind==='learningDefinition'&&r.id===c.id);
 if(c.action!=='create'&&(!old||!visibleRecord(old,records,state,member)))deny();
 const orgId=c.action==='create'||c.action==='edit'?c.orgId:old!.payload.orgId!;
 if(!scope.has(orgId))deny();
 if(!state.orgs.some(o=>o.id===orgId&&o.status==='启用'))fail('计划组织须为启用状态');
 if(c.action==='archive'){
  if(old!.status==='archived')fail('配置已归档');
  return {...old!,status:'archived',updatedAt:at};
 }
 if(c.action==='revise'){
  if(old!.status!=='sealed')fail('仅已定版配置可创建后续版本');
  const root=old!.payload.definitionRootId!;
  const family=records.filter(r=>r.kind==='learningDefinition'&&r.payload.definitionRootId===root);
  if(family.some(r=>r.status==='draft'))fail('此计划已有草稿版本，请先处理');
  if(family.some(r=>(r.payload.version??0)>(old!.payload.version??0)))fail('请从最新版本创建后续版本');
  return {...old!,id:crypto.randomUUID(),status:'draft',referenceId:old!.id,createdBy:member.userId,createdAt:at,updatedAt:at,payload:{...old!.payload,version:(old!.payload.version??1)+1}};
 }
 if(old&&old.status!=='draft')fail('已定版或归档配置不能修改，请创建后续版本');
 const courseIds=c.action==='seal'?old!.payload.courseIds!:c.courseIds;
 if(new Set(courseIds).size!==courseIds.length)fail('课程不得重复');
 for(const courseId of courseIds){const course=records.find(r=>r.id===courseId&&r.kind==='course');if(!course||!visibleRecord(course,records,state,member))deny();if(course!.status!=='published')fail('仅可选用已发布课程版本');}
 if(c.action==='seal')return {...old!,status:'sealed',updatedAt:at};
 if(old&&old.payload.orgId!==c.orgId)fail('版本所属组织不可更换，请独立新建计划');
 if(old?.referenceId){const previous=records.find(r=>r.id===old.referenceId&&r.kind==='learningDefinition');if(!previous||previous.payload.learningMode?.progressSync!==c.config.progressSync)fail('已定版计划的进度同步设置不可更改');}
 const key=old?.id??crypto.randomUUID();
 return {id:key,kind:'learningDefinition',employeeId:null,positionId:null,referenceId:old?.referenceId??null,status:'draft',createdBy:old?.createdBy??member.userId,createdAt:old?.createdAt??at,updatedAt:at,payload:{title:c.title,orgId:c.orgId,learningMode:c.config,courseIds:c.courseIds,definitionRootId:old?.payload.definitionRootId??key,version:old?.payload.version??1}};
}
