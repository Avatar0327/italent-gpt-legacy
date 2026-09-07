import { sqliteTable, text, integer, primaryKey } from 'drizzle-orm/sqlite-core';
export const workspaces=sqliteTable('hris_workspaces',{owner:text('owner').primaryKey(),revision:integer('revision').notNull().default(0),data:text('data').notNull(),lastMutation:text('last_mutation').notNull().default('')});
// owner is retained as the legacy column name; new records use an opaque tenant ID.
export const memberships=sqliteTable('hris_memberships',{
 userId:text('user_id').primaryKey(),tenantId:text('tenant_id').notNull().references(()=>workspaces.owner),
 role:text('role',{enum:['admin','hr','approver','employee']}).notNull(),
 employeeId:text('employee_id'),active:integer('active',{mode:'boolean'}).notNull().default(true),
});
export const auditEvents=sqliteTable('hris_audit_events',{
 tenantId:text('tenant_id').notNull().references(()=>workspaces.owner),id:text('id').notNull(),
 actorId:text('actor_id').notNull(),action:text('action').notNull(),subject:text('subject').notNull(),
 at:text('at').notNull(),revision:integer('revision').notNull(),
},t=>[primaryKey({columns:[t.tenantId,t.id]})]);
