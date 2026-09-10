import {z} from 'zod';
export const reportCommandInput=z.object({commandId:z.string().uuid(),idempotencyKey:z.string().min(1).max(100),expectedWorkspaceRevision:z.number().int().nonnegative(),expectedAuthorizationRevision:z.number().int().nonnegative(),expectedWriterEpoch:z.number().int().nonnegative(),expectedRecoveryEpoch:z.number().int().nonnegative(),payload:z.unknown()}).strict();
