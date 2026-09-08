import './support/runtime.mjs';
import {test} from 'node:test';
import assert from 'node:assert/strict';
const {courseRequirements,learningRequirementProgress,learningAssignmentCurrent}=await import('../lib/hris/learning-requirements.ts');
test('requirement completion rejects borrowed identities, duplicates and missing evidence while preserving legacy assignments',()=>{
 const assignment={id:'plan',employeeId:'learner',payload:{courseIds:['course']}};
 const task={id:'task',kind:'enrollment',employeeId:'learner',referenceId:'course',status:'completed',payload:{learningAssignmentId:'plan',verifiedBy:'reviewer',verifiedAt:'2026-09-08T00:00:00Z'}};
 assert.equal(learningRequirementProgress(assignment,[task]).complete,true);
 for(const tasks of [[],[task,{...task,id:'duplicate'}],[{...task,employeeId:'other'}],[{...task,payload:{...task.payload,verifiedAt:undefined}}],[{...task,payload:{...task.payload,learningRequirementId:'wrong'}}],[{...task,status:'cancelled'}]])assert.equal(learningRequirementProgress(assignment,tasks).complete,false);
 const snapshot={...assignment,payload:{...assignment.payload,learningRequirements:courseRequirements(['course'])}};
 assert.equal(learningRequirementProgress(snapshot,[task]).complete,true);
 assert.equal(learningRequirementProgress({...snapshot,payload:{...snapshot.payload,learningRequirements:[]}},[task]).complete,false);
 assert.equal(learningRequirementProgress({...snapshot,payload:{...snapshot.payload,learningRequirements:[{id:'exam',kind:'exam',resourceId:'course'}]}},[task]).complete,false);
 assert.deepEqual(courseRequirements(['new','course'],[{id:'stable',kind:'course',resourceId:'course'}]),[{id:'course:new',kind:'course',resourceId:'new'},{id:'stable',kind:'course',resourceId:'course'}]);
});

test('assignment progression retains history but stops for exit, transfer or disabled organization',()=>{
 const assignment={employeeId:'learner',payload:{orgId:'org'}};
 const state={employees:[{id:'learner',orgId:'org',status:'正式'}],orgs:[{id:'org',status:'启用'}]};
 assert.equal(learningAssignmentCurrent(assignment,state),true);
 for(const employee of [null,{id:'learner',orgId:'org',status:'离职'},{id:'learner',orgId:'other',status:'正式'}])assert.equal(learningAssignmentCurrent(assignment,{...state,employees:employee?[employee]:[]}),false);
 assert.equal(learningAssignmentCurrent(assignment,{...state,orgs:[{id:'org',status:'停用'}]}),false);
});
