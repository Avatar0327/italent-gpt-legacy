import { z } from 'zod';
import type { State } from './model.ts';
export const grantSchema=z.object({email:z.string().trim().email().max(254).transform(s=>s.toLowerCase()),name:z.string().trim().min(1).max(100),role:z.enum(['admin','hr','approver','employee']),employeeId:z.string().max(100).nullable(),active:z.boolean(),revision:z.number().int().nonnegative()});
export function validateGrant(input:z.infer<typeof grantSchema>,state:State,selfEmail:string){
 if(input.email===selfEmail.toLowerCase()&&(!input.active||input.role!=='admin'))throw Error('不能停用自己或移除自己的管理员权限');
 if(input.role==='employee'&&!input.employeeId)throw Error('员工角色必须关联员工档案');
 if(input.employeeId&&!state.employees.some(e=>e.id===input.employeeId&&e.status!=='离职'))throw Error('请选择有效的在职员工档案');
}
