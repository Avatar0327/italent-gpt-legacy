import test from 'node:test';
import assert from 'node:assert/strict';
import {setup,core,grant,hris,members,expect,act,request} from './support/foundation-scenario.mjs';
const history=await import('../app/api/history/route.ts');

test('F01-F04 cross-org UAT: origin-only HR cannot initiate; B-only reviewer cannot review an A employee; both A reviewers can finalize without B scope',async t=>{
 const f=await setup();t.after(()=>f.sqlite.close());
 await core({action:'position',code:'F-UAT-B',name:'合成B岗位',orgId:f.otherOrg.id,family:'验收',responsibilities:'仅合成数据',status:'启用'});
 await core({action:'grade',code:'F-T1',name:'合成T1',sequence:1,status:'启用'});
 await core({action:'grade',code:'F-T2',name:'合成T2',sequence:2,status:'启用'});
 let d=await expect(await hris.GET());const target=d.state.positions.find(x=>x.code==='F-UAT-B'),g1=d.state.grades.find(x=>x.code==='F-T1'),g2=d.state.grades.find(x=>x.code==='F-T2');
 await core({action:'employee',...f.e,positionId:f.position.id,gradeId:g1.id});
 await grant('hrAB','hr',null,[f.org.id,f.otherOrg.id]);
 await grant('hrB','hr',null,[f.otherOrg.id]);
 await grant('reviewB','approver',null,[f.otherOrg.id]);
 await grant('reviewA2','approver',null,[f.org.id]);
 async function post(command,status=200){const before=await expect(await hris.GET());return expect(await hris.POST(request('/api/hris',{revision:before.revision,command})),status);}
 const command={action:'request',kind:'transfer',employeeId:f.e.id,orgId:f.otherOrg.id,positionId:target.id,gradeId:g2.id,reason:'F01-F04合成跨组织角色核对'};
 const rows=()=>['hris_workspaces','hris_employees','hris_approvals','hris_approval_steps','hris_employment_history','hris_audit_events'].map(table=>f.sqlite.prepare('SELECT * FROM '+table+' ORDER BY rowid').all());
 let before=rows();act('hr');await post({...command,gradeId:g1.id},403);assert.deepEqual(rows(),before,'HR-A无目标组织范围时不得产生申请或审计');
 act('hrAB');await post(command,403);assert.deepEqual(rows(),before,'HR-AB无职级权限时不能变更职级');
 act('owner');d=await expect(await members.GET());await expect(await members.POST(request('/api/members',{revision:d.revision,email:'hrAB@example.com',name:'合成HR-AB',role:'hr',employeeId:null,orgScope:[f.org.id,f.otherOrg.id],viewEmail:false,viewLevel:true,active:true})));
 await core({action:'workflow',kind:'transfer',steps:[{userId:'approver',name:'来源复核'},{userId:'reviewB',name:'目标复核'}]});
 before=rows();act('hrAB');await post(command,400);assert.deepEqual(rows(),before,'B-only审批人不覆盖申请时A组织，整笔申请失败');
 act('owner');await core({action:'workflow',kind:'transfer',steps:[{userId:'approver',name:'独立复核一'},{userId:'reviewA2',name:'独立复核二'}]});
 act('hrAB');await post(command);d=await expect(await hris.GET());const approval=d.state.approvals.find(x=>x.employeeId===f.e.id&&x.status==='pending');assert.ok(approval);
 act('reviewA2');before=rows();await post({action:'decide',id:approval.id,decision:'approved'},403);assert.deepEqual(rows(),before);
 act('approver');await post({action:'decide',id:approval.id,decision:'approved'});assert.equal((await expect(await hris.GET())).state.employees.find(x=>x.id===f.e.id).orgId,f.org.id);
 act('reviewA2');await post({action:'decide',id:approval.id,decision:'approved'});d=await expect(await hris.GET());assert.ok(!d.state.employees.some(x=>x.id===f.e.id),'终审后仅A范围审批人不再可读该B员工');
 await expect(await history.GET(request('/api/history?employeeId='+f.e.id)),403);
 act('hr');assert.ok(!(await expect(await hris.GET())).state.employees.some(x=>x.id===f.e.id));
 act('hrB');assert.ok((await expect(await hris.GET())).state.employees.some(x=>x.id===f.e.id));
 act('owner');d=await expect(await hris.GET());const employee=d.state.employees.find(x=>x.id===f.e.id);assert.equal(employee.orgId,f.otherOrg.id);assert.equal(employee.positionId,target.id);assert.equal(employee.gradeId,g2.id);assert.equal(d.state.approvals.find(x=>x.id===approval.id).status,'approved');
 const h=await expect(await history.GET(request('/api/history?employeeId='+f.e.id)));assert.equal(h.items[0].toOrg,f.otherOrg.name);
});
