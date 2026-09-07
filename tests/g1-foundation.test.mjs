import {test} from 'node:test';
import assert from 'node:assert/strict';
import {setup,send,get,core,grant,expect,hris,dev,act,request,anchors,due} from './support/foundation-scenario.mjs';
const profiles=await import('../app/api/cadre-profiles/route.ts');

test('G1 X01：同一人员从组织岗位到盘点计划、考试学习核验与档案回流，调动后撤销旧组织访问',async t=>{
 const {sqlite,e,other,org,otherOrg,position}=await setup();t.after(()=>sqlite.close());
 await core({action:'employee',...e,positionId:position.id});
 const before=(await expect(await hris.GET())).state.employees.find(x=>x.id===e.id);
 const standard=await send({action:'standard',code:'G1-ABILITY',name:'合成问题解决能力',anchors});
 await send({action:'requirement',positionId:position.id,standardId:standard.id,target:3});
 await send({action:'assessment',employeeId:e.id,standardId:standard.id,rating:2,evidence:'合成案例表明可以独立处理常规任务',assessedOn:'2026-01-01'});
 const review=await send({action:'review',employeeId:e.id,period:'G1-SYNTHETIC',potential:null,evidence:'合成盘点暂未形成潜力证据，不猜测评级'});
 await send({action:'publishReview',id:review.id});
 const plan=await send({action:'plan',employeeId:e.id,standardId:standard.id,target:3,title:'合成能力提升行动',actionPlan:'完成案例考试与实践成果，由独立经理核验',due});
 const course=await send({action:'course',code:'G1-COURSE',title:'合成问题解决课程',standardId:standard.id,description:'配合相同标准版本的发展行动',content:'阅读合成问题案例，参加考试，并提交改善实践成果以供独立核验。'});
 await send({action:'exam',courseId:course.id,questions:[{prompt:'怎样处理合成案例中的问题？',options:['记录证据并核实','忽略证据直接猜测'],correct:0}],passingScore:100,maxAttempts:2});
 await send({action:'publishCourse',id:course.id});
 const enrollment=await send({action:'enroll',employeeId:e.id,planId:plan.id,courseId:course.id,due});
 async function readProfile(status=200){return expect(await profiles.GET(request('/api/cadre-profiles?employeeId='+e.id)),status);}
 act('manager');let p=await readProfile();assert.ok(p.sections.find(x=>x.key==='reviews').items.some(x=>x.id===review.id));
 assert.equal(p.sections.find(x=>x.key==='learning').items.find(x=>x.id===enrollment.id).status,'进行中');
 await expect(await profiles.GET(request('/api/cadre-profiles?employeeId='+other.id)),403);
 act('employee');await send({action:'submitLearning',id:enrollment.id,evidence:'未通过考试，成果提交应被阻断'},400);
 await send({action:'attemptExam',enrollmentId:enrollment.id,answers:[0]});
 await send({action:'submitLearning',id:enrollment.id,evidence:'合成案例已完成考试与实践材料'});
 await send({action:'submitPlan',id:plan.id,evidence:'合成发展行动已完成，等待核验'});
 await send({action:'verifyLearning',id:enrollment.id,accepted:true,evidence:'不能由本人核验本人的学习'},403);
 act('manager');await send({action:'verifyPlan',id:plan.id,accepted:true,evidence:'学习未核验前计划不得结项'},400);
 await send({action:'verifyLearning',id:enrollment.id,accepted:true,evidence:'独立检查合成考试与实践材料符合要求'});
 await send({action:'verifyPlan',id:plan.id,accepted:true,evidence:'核实关联课程和发展实践均已完成'});
 p=await readProfile();for(const [key,id] of [['plans',plan.id],['learning',enrollment.id]])assert.equal(p.sections.find(x=>x.key===key).items.find(x=>x.id===id).status,'已完成');
 assert.deepEqual(p.sections.find(x=>x.key==='qualifications').items,[]);
 act('owner');assert.deepEqual((await expect(await hris.GET())).state.employees.find(x=>x.id===e.id),before);
 // Approved transfer changes the live organization scope; old history grants no access.
 await grant('reviewerAll','approver',null,[org.id,otherOrg.id]);
 await core({action:'position',code:'G1-TARGET',name:'合成目标岗位',orgId:otherOrg.id,family:'合成验证',responsibilities:'合成调动目标岗位',status:'启用'});
 const target=(await expect(await hris.GET())).state.positions.find(x=>x.code==='G1-TARGET');
 await core({action:'workflow',kind:'transfer',steps:[{userId:'reviewerAll',name:'合成独立审批人'}]});
 await core({action:'request',employeeId:e.id,kind:'transfer',orgId:otherOrg.id,positionId:target.id,reason:'合成调动用于核实旧组织访问撤销'});
 const pending=(await expect(await hris.GET())).state.approvals.find(x=>x.employeeId===e.id&&x.status==='pending');
 act('reviewerAll');await core({action:'decide',id:pending.id,decision:'approved'});
 act('manager');await readProfile(403);assert.ok(!(await get()).records.some(r=>r.id===plan.id||r.id===enrollment.id));
 await expect(await dev.GET(request('/api/development?id='+enrollment.id)),403);
 await grant('managerB','manager',null,[otherOrg.id]);act('managerB');p=await readProfile();assert.equal(p.employee.org,otherOrg.name);
 assert.equal(p.sections.find(x=>x.key==='learning').items.find(x=>x.id===enrollment.id).status,'已完成');
});
