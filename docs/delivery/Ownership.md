# 文件归属与写入交接

当前模式：串行代码交接。当前唯一写入者/合并者/发布者：本总控聊天。基础、干部、学习包已书面派发，尚无聊天领取；不冒称有人正在执行。

| 范围 | 责任角色 | 文件 |
|---|---|---|
| 共享基础与模型 | 总控暂兼基础负责人 | lib/hris/model.ts、authorization.ts、context.ts、repository.ts、development.ts、development-repository.ts、http.ts、member-rules.ts；migrations/全部 |
| 公共接口与壳 | 总控 | app/api/development/route.ts、app/hris.tsx、app/chatgpt-auth.ts、components/、app/globals.css、package文件、构建及托管配置 |
| 共用测试与报表 | 总控 | tests/p3-api.test.mjs、tests/support/、lib/hris/reports.ts、app/reports/、范围进度文件 |
| 基础模块候选 | 01基础（领取后） | app/api/hris/、members/、access/、attachments/；组织员工相关专属文件，领取前列明实际路径 |
| 干部专属候选 | 02干部（领取后） | lib/hris/cadres.ts、cadre-profiles.ts、qualification.ts；app/cadres/、cadre-profiles/、qualifications/及对应API |
| 学习专属候选 | 03学习（领取后） | lib/hris/training-*.ts、learning-credits.ts；app/learning/、training-requests/、training-sessions/、learning-credits/及对应API |
| 交付与验收记录 | 总控汇总，模块提议 | docs/delivery/及Execution_Checkpoint.md |

接入规则：新聊天先只读核对项目ID、完整SHA、工作区干净状态、交接文件；报告给总控。总控保存交接点并释放写入职责后，新聊天才能作为串行接手者写代码。它只交付提交和证据，总控恢复后统一合并/验证/发布。未领取时无模块写入权限分配。

即使本机worktree探针通过，也不宣布跨聊天隔离通过。未经核实前，其他聊天只做资料盘点、方案或补丁建议，不触碰活动检出目录。Sites技能的站点所有者规则继续适用；不将站点编辑/发布委派给生成的子代理。本轮不创建代理。

合并流程：核对基线→检查允许路径/共享变更→记录兼容性→串行合并→必要集成验证→更新台账→总控私有发布。保留原提交；不重置或覆盖他人未提交修改。数据库迁移由总控统一编号和测试。凭据不得写入交接文件。
