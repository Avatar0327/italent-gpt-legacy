import {z} from 'zod';
import type {State} from './model';
import {scopedOrgs,type Member} from './authorization';
import {HttpError} from './http';
const text=z.string().trim().min(1).max(200),evidence=z.string().trim().min(5).max(4000),id=z.string().min(1).max(100);
const date=z.string().regex(/^\d{4}-\d{2}-\d{2}$/).refine(v=>{const d=new Date(v+'T00:00:00Z');return !isNaN(d.getTime())&&d.toISOString().slice(0,10)===v;});
const projectFields={name:text,orgId:id,period:text,start:date,end:date};
const question=z.object({prompt:evidence,options:z.array(text).min(2).max(6),correct:z.number().int().min(0).max(5)}).refine(q=>q.correct<q.options.length&&new Set(q.options).size===q.options.length,'选项不得重复且答案须有效');
const band=z.number().int().min(1).max(3),level=z.number().int().min(1).max(5);
export const developmentCommand=z.discriminatedUnion('action',[
 z.object({action:z.literal('project'),...projectFields}),
 z.object({action:z.literal('startProject'),id}),
 z.object({action:z.literal('closeProject'),id}),
 z.object({action:z.literal('pool'),name:text,orgId:id,criteria:evidence}),
 z.object({action:z.literal('poolMember'),poolId:id,employeeId:id,evidence}),
 z.object({action:z.literal('removePoolMember'),id,reason:evidence}),
 z.object({action:z.literal('training'),...projectFields,instructor:text,courseIds:z.array(id).min(1).max(20)}),
 z.object({action:z.literal('publishTraining'),id}),
 z.object({action:z.literal('closeTraining'),id}),
 z.object({action:z.literal('standard'),code:text,name:text,anchors:z.array(evidence).length(5)}),
 z.object({action:z.literal('requirement'),positionId:id,standardId:id,target:level}),
 z.object({action:z.literal('assessment'),employeeId:id,standardId:id,rating:level,evidence,assessedOn:date}),
 z.object({action:z.literal('performance'),employeeId:id,period:text,source:evidence,originalRating:text,band,reason:evidence,supersedes:id.optional()}),
 z.object({action:z.literal('review'),id:id.optional(),projectId:id.optional(),employeeId:id,period:text,performanceId:id.optional(),potential:band.nullable(),evidence}),
 z.object({action:z.literal('publishReview'),id}),
 z.object({action:z.literal('succession'),positionId:id,employeeId:id,readiness:z.enum(['ready','one_year','two_years']),evidence}),
 z.object({action:z.literal('closeSuccession'),id,reason:evidence}),
 z.object({action:z.literal('plan'),employeeId:id,standardId:id,target:level,title:text,actionPlan:evidence,due:date}),
 z.object({action:z.literal('cancelPlan'),id,reason:evidence}),
 z.object({action:z.literal('cancelEnrollment'),id,reason:evidence}),
 z.object({action:z.literal('submitPlan'),id,evidence}),
 z.object({action:z.literal('verifyPlan'),id,accepted:z.boolean(),evidence}),
 z.object({action:z.literal('course'),code:text,title:text,description:evidence,content:z.string().trim().min(20).max(12000),standardId:id.optional()}),
 z.object({action:z.literal('exam'),courseId:id,questions:z.array(question).min(1).max(20),passingScore:z.number().int().min(1).max(100),maxAttempts:z.number().int().min(1).max(10)}),
 z.object({action:z.literal('attemptExam'),enrollmentId:id,answers:z.array(z.number().int().min(0).max(5)).min(1).max(20)}),
 z.object({action:z.literal('publishCourse'),id}),
 z.object({action:z.literal('archiveCourse'),id}),
 z.object({action:z.literal('enroll'),trainingId:id.optional(),employeeId:id,courseId:id,planId:id.optional(),due:date}),
 z.object({action:z.literal('submitLearning'),id,evidence}),
 z.object({action:z.literal('verifyLearning'),id,accepted:z.boolean(),evidence}),
]);
export type DevelopmentCommand=z.infer<typeof developmentCommand>;
export type Kind='standard'|'requirement'|'assessment'|'performance'|'review'|'succession'|'plan'|'course'|'enrollment'|'exam'|'attempt'|'project'|'pool'|'poolMember'|'training';
export type RecordData={orgId?:string;projectId?:string;trainingId?:string;start?:string;end?:string;criteria?:string;instructor?:string;courseIds?:string[];questions?:{prompt:string;options:string[];correct?:number}[];passingScore?:number;maxAttempts?:number;examId?:string;answers?:number[];score?:number;passed?:boolean;code?:string;name?:string;anchors?:string[];version?:number;target?:number;rating?:number;evidence?:string;assessedOn?:string;period?:string;source?:string;originalRating?:string;band?:number;reason?:string;supersedes?:string;potential?:number|null;performanceId?:string;performanceSnapshot?:Record<string,unknown>;readiness?:string;title?:string;actionPlan?:string;due?:string;submittedBy?:string;submittedAt?:string;verifiedBy?:string;verifiedAt?:string;verification?:string;description?:string;content?:string;planId?:string;standardId?:string;closedReason?:string;publishedBy?:string;publishedAt?:string};
export type DevelopmentRecord={id:string;kind:Kind;employeeId:string|null;positionId:string|null;referenceId:string|null;status:string;payload:RecordData;createdBy:string;createdAt:string;updatedAt:string};
export const isTalentManager=(m:Member)=>['admin','hr','manager'].includes(m.role);
export function canReadRecord(r:DevelopmentRecord,s:State,m:Member){
 if(m.role==='admin')return true;
 if(r.kind==='standard')return true;
 if(['project','pool','training'].includes(r.kind)){const scope=scopedOrgs(s,m);if(isTalentManager(m)&&scope.has(r.payload.orgId!))return true;if(r.kind==='training'&&r.status!=='draft'){const e=s.employees.find(e=>e.id===m.employeeId);return !!e&&orgWithin(s,e.orgId,r.payload.orgId!);}return false;}
 if(r.kind==='exam')return false; // Authorize through its course in visibleRecord below.
 if(r.kind==='course')return r.status!=='draft'||m.role==='hr';
 const scope=scopedOrgs(s,m);
 if(r.kind==='requirement')return !!s.positions?.some(p=>p.id===r.positionId&&(scope.has(p.orgId)||s.employees.some(e=>e.id===m.employeeId&&e.positionId===p.id)));
 if(r.employeeId){const e=s.employees.find(e=>e.id===r.employeeId);if(!e)return false;
  if(isTalentManager(m)&&scope.has(e.orgId)){if(r.positionId&&!s.positions?.some(p=>p.id===r.positionId&&scope.has(p.orgId)))return false;return true;}
  return e.id===m.employeeId&&['plan','enrollment','assessment','attempt'].includes(r.kind);
 }
 return false;
}
export function applyDevelopment(records:DevelopmentRecord[],s:State,m:Member,input:unknown,at=new Date().toISOString()){
 const c=developmentCommand.parse(input),scope=scopedOrgs(s,m);const deny=(message:string):never=>{throw new HttpError(403,message);};const invalid=(message:string):never=>{throw new HttpError(400,message);};
 const manager=()=>{if(!isTalentManager(m))deny('没有人才管理权限');};
 const catalog=()=>{if(!['admin','hr'].includes(m.role))deny('仅管理员或人力资源人员可维护标准与课程');};
 const employee=(employeeId:string,manage=true)=>{const e=s.employees.find(e=>e.id===employeeId);if(!e||!(manage?isTalentManager(m)&&(m.role==='admin'||scope.has(e.orgId)):e.id===m.employeeId))deny('没有此员工的数据权限');if(e!.status==='离职')invalid('离职员工不能发起新的发展业务');return e!;};
 const organization=(orgId:string)=>{manager();const org=s.orgs.find(o=>o.id===orgId);if(!org||!scope.has(orgId))deny('没有此组织的数据权限');if(org!.status!=='启用')invalid('组织已停用');};
 const position=(positionId:string,requireActive=true)=>{manager();const p=s.positions?.find(p=>p.id===positionId);if(!p||!scope.has(p.orgId))deny('没有此岗位的数据权限');if(requireActive&&p!.status!=='启用')invalid('岗位已停用');return p!;};
 const get=(key:string,kind:Kind)=>{const r=records.find(r=>r.id===key&&r.kind===kind);if(!r||!visibleRecord(r,records,s,m))deny('记录不存在或没有访问权限');return r!;};
 const independent=(r:DevelopmentRecord)=>{manager();employee(r.employeeId!);if(r.employeeId===m.employeeId||r.payload.submittedBy===m.userId)deny('须由其他有权限的人员核验');};
 const create=(kind:Kind,payload:RecordData,options:Partial<DevelopmentRecord>={})=>({id:crypto.randomUUID(),kind,employeeId:null,positionId:null,referenceId:null,status:'active',payload,createdBy:m.userId,createdAt:at,updatedAt:at,...options} as DevelopmentRecord);
 const change=(r:DevelopmentRecord,status:string,payload:RecordData={})=>({...r,status,payload:{...r.payload,...payload},updatedAt:at});
 const noSelf=(employeeId:string)=>{if(employeeId===m.employeeId)deny('不能为本人作出正式人才评价');};
 switch(c.action){
 case 'project':case 'training':{organization(c.orgId);if(c.end<c.start)invalid('结束日期不能早于开始日期');if(c.action==='training'){catalog();if(new Set(c.courseIds).size!==c.courseIds.length)invalid('课程不得重复');for(const courseId of c.courseIds)if(get(courseId,'course').status!=='published')invalid('培训项目只能关联已发布课程');return create('training',{name:c.name,orgId:c.orgId,period:c.period,start:c.start,end:c.end,instructor:c.instructor,courseIds:c.courseIds},{status:'draft'});}return create('project',{name:c.name,orgId:c.orgId,period:c.period,start:c.start,end:c.end},{status:'draft'});}
 case 'startProject':case 'publishTraining':{const r=get(c.id,c.action==='startProject'?'project':'training');organization(r.payload.orgId!);if(c.action==='publishTraining'){catalog();for(const courseId of r.payload.courseIds??[])if(get(courseId,'course').status!=='published')invalid('项目课程已经停用，请先核实');}if(r.status!=='draft')invalid('项目已启动');return change(r,'active');}
 case 'closeProject':case 'closeTraining':{const r=get(c.id,c.action==='closeProject'?'project':'training');manager();if(r.status!=='active')invalid('项目未启动或已结束');if(c.action==='closeProject'&&records.some(x=>x.kind==='review'&&x.payload.projectId===r.id&&x.status==='draft'))invalid('仍有盘点草稿，完成发布后才能结束项目');if(c.action==='closeTraining'&&records.some(x=>x.kind==='enrollment'&&x.payload.trainingId===r.id&&!['completed','cancelled'].includes(x.status)))invalid('仍有学习任务未完成核验');return change(r,'closed');}
 case 'pool':{organization(c.orgId);return create('pool',{name:c.name,orgId:c.orgId,criteria:c.criteria});}
 case 'poolMember':{manager();const pool=get(c.poolId,'pool'),e=employee(c.employeeId);noSelf(e.id);if(!orgWithin(s,e.orgId,pool.payload.orgId!))invalid('候选人不属于人才池组织范围');if(records.some(r=>r.kind==='poolMember'&&r.referenceId===pool.id&&r.employeeId===e.id&&r.status==='active'))invalid('人才池已包含此成员');return create('poolMember',{evidence:c.evidence},{referenceId:pool.id,employeeId:e.id});}
 case 'removePoolMember':{const r=get(c.id,'poolMember');manager();if(r.status!=='active')invalid('该成员已退出人才池');return change(r,'closed',{closedReason:c.reason});}

 case 'standard':{catalog();const previous=records.filter(r=>r.kind==='standard'&&r.payload.code===c.code);return create('standard',{code:c.code,name:c.name,anchors:c.anchors,version:1+Math.max(0,...previous.map(r=>r.payload.version??1))});}
 case 'requirement':{position(c.positionId);get(c.standardId,'standard');return create('requirement',{target:c.target},{positionId:c.positionId,referenceId:c.standardId});}
 case 'assessment':{manager();employee(c.employeeId);noSelf(c.employeeId);get(c.standardId,'standard');if(c.assessedOn>at.slice(0,10))invalid('评估日期不能在未来');return create('assessment',{rating:c.rating,evidence:c.evidence,assessedOn:c.assessedOn},{employeeId:c.employeeId,referenceId:c.standardId});}
 case 'performance':{catalog();employee(c.employeeId);noSelf(c.employeeId);if(c.supersedes){const old=get(c.supersedes,'performance');if(old.employeeId!==c.employeeId||old.payload.period!==c.period)invalid('更正记录必须属于同一员工和期间');if(records.some(r=>r.kind==='performance'&&r.payload.supersedes===old.id))invalid('请更正最新版本');}else if(records.some(r=>r.kind==='performance'&&r.employeeId===c.employeeId&&r.payload.period===c.period))invalid('该期间已有绩效，请使用更正记录保留追溯');return create('performance',{period:c.period,source:c.source,originalRating:c.originalRating,band:c.band,reason:c.reason,supersedes:c.supersedes},{employeeId:c.employeeId,referenceId:c.supersedes??null});}
 case 'review':{manager();const employeeRow=employee(c.employeeId);noSelf(c.employeeId);if(c.projectId){const project=get(c.projectId,'project');if(project.status!=='active'||project.payload.period!==c.period||!orgWithin(s,employeeRow.orgId,project.payload.orgId!))invalid('盘点项目状态、期间或组织范围不匹配');}let performanceSnapshot:Record<string,unknown>|undefined;if(c.performanceId){const p=get(c.performanceId,'performance');if(p.employeeId!==c.employeeId||p.payload.period!==c.period)invalid('绩效员工、期间与盘点不一致');if(records.some(r=>r.kind==='performance'&&r.payload.supersedes===p.id))invalid('请使用最新绩效版本');performanceSnapshot={...p.payload};}const old=c.id?get(c.id,'review'):undefined;if(old&&(old.status!=='draft'||old.employeeId!==c.employeeId||old.payload.period!==c.period||old.payload.projectId!==c.projectId))invalid('仅可编辑同一员工、期间的草稿盘点');if(records.some(r=>r.kind==='review'&&r.employeeId===c.employeeId&&r.payload.period===c.period&&r.payload.projectId===c.projectId&&r.id!==c.id))invalid('该员工本期已有盘点');return create('review',{projectId:c.projectId,period:c.period,potential:c.potential,evidence:c.evidence,performanceId:c.performanceId,performanceSnapshot},{employeeId:c.employeeId,referenceId:c.performanceId??null,status:'draft',...(old?{id:old.id,createdBy:old.createdBy,createdAt:old.createdAt}:{})});}
 case 'publishReview':{const r=get(c.id,'review');manager();employee(r.employeeId!);noSelf(r.employeeId!);if(r.status!=='draft')invalid('盘点已发布');if(r.payload.projectId&&get(r.payload.projectId,'project').status!=='active')invalid('盘点项目已结束');if(r.referenceId&&records.some(x=>x.kind==='performance'&&x.payload.supersedes===r.referenceId))invalid('所用绩效已更正，请先编辑草稿选择最新版本');return change(r,'published',{publishedBy:m.userId,publishedAt:at});}
 case 'succession':{position(c.positionId);employee(c.employeeId);noSelf(c.employeeId);if(records.some(r=>r.kind==='succession'&&r.employeeId===c.employeeId&&r.positionId===c.positionId&&r.status==='active'))invalid('该岗位已有此候选人，请先关闭旧记录');return create('succession',{readiness:c.readiness,evidence:c.evidence},{employeeId:c.employeeId,positionId:c.positionId});}
 case 'closeSuccession':{const r=get(c.id,'succession');position(r.positionId!,false);if(r.status!=='active')invalid('候选记录已关闭');return change(r,'closed',{closedReason:c.reason});}
 case 'plan':{manager();employee(c.employeeId);get(c.standardId,'standard');if(c.due<at.slice(0,10))invalid('新计划截止日期不能早于今天');return create('plan',{title:c.title,actionPlan:c.actionPlan,target:c.target,due:c.due},{employeeId:c.employeeId,referenceId:c.standardId});}
 case 'cancelPlan':case 'cancelEnrollment':{manager();const r=get(c.id,c.action==='cancelPlan'?'plan':'enrollment');if(['completed','cancelled'].includes(r.status))invalid('已完成或取消的记录不能再次取消');if(c.action==='cancelPlan'&&records.some(x=>x.kind==='enrollment'&&x.payload.planId===r.id&&!['completed','cancelled'].includes(x.status)))invalid('请先处理关联的未完成学习任务');return change(r,'cancelled',{closedReason:c.reason});}
 case 'submitPlan':case 'submitLearning':{const r=get(c.id,c.action==='submitPlan'?'plan':'enrollment');employee(r.employeeId!,false);if(!['active','returned'].includes(r.status))invalid('当前状态不能提交');if(c.action==='submitLearning'&&r.payload.examId&&!records.some(a=>a.kind==='attempt'&&a.referenceId===r.id&&a.payload.passed))invalid('须先通过课程考试');return change(r,'submitted',{evidence:c.evidence,submittedBy:m.userId,submittedAt:at});}
 case 'verifyPlan':case 'verifyLearning':{const r=get(c.id,c.action==='verifyPlan'?'plan':'enrollment');independent(r);if(r.status!=='submitted')invalid('尚未提交核验或已经处理');if(c.action==='verifyPlan'&&c.accepted&&records.some(x=>x.kind==='enrollment'&&x.payload.planId===r.id&&!['completed','cancelled'].includes(x.status)))invalid('关联学习任务尚未全部核验完成');return change(r,c.accepted?'completed':'returned',{verification:c.evidence,verifiedBy:m.userId,verifiedAt:at});}
 case 'course':{catalog();if(c.standardId)get(c.standardId,'standard');const previous=records.filter(r=>r.kind==='course'&&r.payload.code===c.code);return create('course',{code:c.code,title:c.title,description:c.description,content:c.content,standardId:c.standardId,version:1+Math.max(0,...previous.map(r=>r.payload.version??1))},{referenceId:c.standardId??null,status:'draft'});}
 case 'exam':{catalog();const course=get(c.courseId,'course');if(course.status!=='draft')invalid('仅草稿课程可配置考试');if(records.some(r=>r.kind==='exam'&&r.referenceId===course.id))invalid('该课程版本已有考试，需调整时请创建新的课程版本');return create('exam',{questions:c.questions,passingScore:c.passingScore,maxAttempts:c.maxAttempts},{referenceId:course.id});}
 case 'attemptExam':{const enrollment=get(c.enrollmentId,'enrollment');employee(enrollment.employeeId!,false);if(!['active','returned'].includes(enrollment.status))invalid('当前学习状态不能参加考试');const exam=records.find(r=>r.id===enrollment.payload.examId&&r.kind==='exam');if(!exam)invalid('该学习任务没有考试');const attempts=records.filter(r=>r.kind==='attempt'&&r.referenceId===enrollment.id);if(attempts.some(a=>a.payload.passed))invalid('已通过此考试');if(attempts.length>=exam!.payload.maxAttempts!)invalid('已达到本课程考试次数上限');const questions=exam!.payload.questions!;if(c.answers.length!==questions.length||c.answers.some((v,i)=>v>=questions[i].options.length))invalid('请完整回答全部题目');const score=Math.round(100*c.answers.filter((v,i)=>v===questions[i].correct).length/questions.length);return create('attempt',{answers:c.answers,score,passed:score>=exam!.payload.passingScore!,examId:exam!.id},{employeeId:enrollment.employeeId,referenceId:enrollment.id,status:score>=exam!.payload.passingScore!?'passed':'failed'});}
 case 'publishCourse':case 'archiveCourse':{catalog();const r=get(c.id,'course');if(c.action==='publishCourse'){if(r.status!=='draft')invalid('仅草稿可以发布');return change(r,'published',{publishedBy:m.userId,publishedAt:at});}if(r.status!=='published')invalid('仅已发布课程可以停用');return change(r,'archived');}
 case 'enroll':{if(c.trainingId){const training=get(c.trainingId,'training'),e=s.employees.find(e=>e.id===c.employeeId);if(training.status!=='active'||!training.payload.courseIds?.includes(c.courseId)||!e||!orgWithin(s,e.orgId,training.payload.orgId!)||c.due>training.payload.end!)invalid('培训项目状态、课程、人员范围或截止日不匹配');}const self=c.employeeId===m.employeeId;employee(c.employeeId,!self);const course=get(c.courseId,'course');if(course.status!=='published')invalid('课程尚未发布或已停用');if(c.due<at.slice(0,10))invalid('学习截止日期不能早于今天');if(c.planId){const plan=get(c.planId,'plan');if(plan.employeeId!==c.employeeId||!['active','returned'].includes(plan.status))invalid('发展计划所属员工或状态无效');if(course.referenceId!==plan.referenceId)invalid('课程能力标准版本与计划不一致');}if(records.some(r=>r.kind==='enrollment'&&r.employeeId===c.employeeId&&r.referenceId===c.courseId))invalid('该员工已领取此课程版本');return create('enrollment',{trainingId:c.trainingId,due:c.due,planId:c.planId,title:course.payload.title,examId:records.find(r=>r.kind==='exam'&&r.referenceId===course.id)?.id},{employeeId:c.employeeId,referenceId:c.courseId});}
 }
}

// Compare only matching standard versions; a missing assessment is never zero.
export function competencyGaps(records:DevelopmentRecord[],state:State,member:Member){
 const scope=scopedOrgs(state,member),visible=records.filter(r=>canReadRecord(r,state,member));
 return state.employees.filter(e=>e.status!=='离职'&&(isTalentManager(member)?member.role==='admin'||scope.has(e.orgId):e.id===member.employeeId)).flatMap(e=>{
  const requirements=new Map<string,DevelopmentRecord>();
  for(const r of visible.filter(r=>r.kind==='requirement'&&r.positionId===e.positionId).sort((a,b)=>a.createdAt.localeCompare(b.createdAt))){const standard=records.find(s=>s.id===r.referenceId);if(standard?.payload.code)requirements.set(standard.payload.code,r);}
  return [...requirements.values()].map(r=>{const standard=records.find(s=>s.id===r.referenceId)!;const assessment=visible.filter(a=>a.kind==='assessment'&&a.employeeId===e.id&&a.referenceId===r.referenceId).sort((a,b)=>(b.payload.assessedOn??'').localeCompare(a.payload.assessedOn??'')||b.createdAt.localeCompare(a.createdAt))[0];return {employeeId:e.id,employeeName:e.name,positionId:e.positionId,standardId:standard.id,standardName:standard.payload.name,standardVersion:standard.payload.version,target:r.payload.target!,rating:assessment?.payload.rating??null,gap:assessment?Math.max(0,r.payload.target!-assessment.payload.rating!):null,assessedOn:assessment?.payload.assessedOn??null};});
 });
}

export function visibleRecord(r:DevelopmentRecord,records:DevelopmentRecord[],state:State,member:Member){
 if(r.kind==='poolMember'){const pool=records.find(p=>p.id===r.referenceId&&p.kind==='pool');return !!pool&&canReadRecord(pool,state,member)&&canReadRecord(r,state,member);}
 if(r.kind!=='exam')return canReadRecord(r,state,member);
 const course=records.find(c=>c.id===r.referenceId&&c.kind==='course');return !!course&&canReadRecord(course,state,member);
}
export function projectRecord(r:DevelopmentRecord,member:Member){
 if(r.kind!=='exam'||['admin','hr'].includes(member.role))return r;
 return {...r,payload:{...r.payload,questions:r.payload.questions?.map(({correct,...q})=>q)}};
}

export function orgWithin(state:State,orgId:string,ancestorId:string){
 const seen=new Set<string>();let current:string|undefined=orgId;while(current&&!seen.has(current)){if(current===ancestorId)return true;seen.add(current);current=state.orgs.find(o=>o.id===current)?.parentId;}return false;
}
