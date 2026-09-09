## 当前执行模式：模块闭环优先、按R版本滚动转序

本轮新批准执行节奏；不批准未决业务规则、内部延期或验收豁免。唯一主模块 M03；备用 未启用；实际执行 M03。仅主模块剩余必要工作全部依赖外部条件/用户决定才可启用1个备用；主模块可推进时优先回归。

| R版本 | 模块顺序 | 当前边界 |
|---|---|---|
| R1 核心底座 | M01→M19→M48→M32 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R2 人才管理 | M37→M06→M26→M18→M17→M03 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R3 HR专业领域 | M27→M16→M12→M11→M07 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R4 本次交付暂缓 | M02→M04→M05→M08→M09→M10→M13→M14→M15→M20→M21→M22→M23→M24→M25→M28→M29→M30→M31→M33→M34→M35→M36→M38→M39→M40→M41→M42→M43→M44→M45→M46→M47 | 暂缓；其余33组退出当前P1退出条件/主动探索。历史代码/证据/数据/验收/隔离成果保留；只准为保留模块引用已有前置或最小公共配置，不顺带恢复完整独立模块。 |

四项条件均true且有证据；P1A结论及P1B评审均完整通过或获明确受限批准；transitionReview.approved=true且有批准范围/日期/记录才可转序。受限通过自身不足以转序。

每R所有模块和适用基础P1条件齐备且版本评审明确批准才进入指定下阶段；R1本次仅准P2设计，P2独立退出评审后才可P3，不继承历史技术验收。P4业务/生产验收独立。

| 版本 | P1转序条件 | 批准进入阶段 | 下游实际状态 |
|---|---|---|---|
| R1 | 齐备 | P2 | 已获准进入，待独立设计执行与评审 |
| R2 | 未齐备：M26,M18,M17,M03,BASE-01,BASE-02,BASE-03,BASE-04,BASE-05,BASE-06,rangeReviewApproved | 未批准 | 未取得该R下游批准 |
| R3 | 未齐备：M27,M16,M12,M11,M07,BASE-01,BASE-02,BASE-03,BASE-04,BASE-05,BASE-06,rangeReviewApproved | 未批准 | 未取得该R下游批准 |

| 模块 | R版本/队列 | P1A判定 | P1B评审 | 转序就绪 | 未达到条件 |
|---|---|---|---|---|---|
| M01 组织员工 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M19 审批中心 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M48 员工自助 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M32 报表 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M37 人才标准 | R2 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M06 任职资格 | R2 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M26 360度评估 | R2 / waiting_owner_review | 已完成待评审 | 已完成待评审 | 否 | implementationRulesDecided；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M18 在线盘点 | R2 / waiting_owner_review | 已完成待评审 | 已完成待评审 | 否 | implementationRulesDecided；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M17 继任与发展 | R2 / waiting_owner_review | 已完成待评审 | 已完成待评审 | 否 | implementationRulesDecided；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M03 干部管理2.0 | R2 / primary | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M27 学习管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M16 绩效管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M12 招聘管理系统 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M11 假勤管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M07 薪酬社保 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |

转序就绪 6/15；独立指标，不等业务验收或生产上线。风险证据规则：核心交易、权限、生效时间、数据完整性及关键异常优先执行证据；不足时写明限制和明确项目设计，须获规则/例外批准才能转序；普通配置/静态字段允许页面、帮助与一致既有证据形成需求结论；不穷尽配置组合；每个新探索绑定closureChecklist问题ID；先判断是否改变当前需求正确性，不阻塞事项进入后续验证清单；模式调整不批准业务规则、内部延期或验收豁免；D1–D7保持，E2仅本人；P1权限设计评审不替代后续真人权限验收。


---

# 当前唯一执行队列：P1A/P1B

源：Scope_Register.json.roadmap及Module_Queue.json。首要工作包：M03唯一主模块；夜间材料等待队列M26,M18,M17。主要开发包：无（暂停扩展）。

1. M03唯一主模块：选拔任用/档案/考察期/述职，复用任期493a9f87证据，核对独立审批、生效和敏感权限

业务顺序：BP-F → BP-I → BP-C → BP-L → BP-P → BP-R → BP-A → BP-S；BP-UNASSIGNED仅保留归属核实历史；无成员时不计业务包。多角色人工UAT不阻断P1；转序不得静默跳过。下方历史队列不构成本轮执行指令。

<!-- P1AB_QUEUE_END -->

# 当前有效：P1唯一总控（2026-09-08T14:14:15.632554+00:00）

当前聊天唯一执行与文档写入者；只读原站并整理P1，暂停新功能，不启用历史模块分工、分支领取或代理。保留48组与既有分支。Module_Queue.json v4、Controller_Resume.md和P1_Review.md为当前入口；F01–F04人工验收不是前置。以下均为历史，不授予其他聊天写入权。

---

# 后续模块队列与激活规则

## 当前生效：单聊天连续执行 / H004-R

用户已确认回归单聊天；04已明确交还写入职责。总控核对干净分支后将 ca5f82af7fee4a29789ba969ea070a5cd3544307 快进合入main，无冲突。本聊天为唯一代码、共享接口及文档写入者和合并发布者。H005–H008不再向其他聊天自动激活，预建分支与全量范围保留，由总控依次处理。以下旧交接/自动激活描述仅为历史，以本节及Module_Queue.json v2为准。

H004报告122/122、类型检查和构建通过；总控复测另记，人工业务与生产未验收。当前重点：绩效展示一致性，然后干部/学习原站证据与逐项差异，先做深再扩展。


总控为唯一合并/发布者。当前写入令牌：H004 / 04绩效管理；本轮提交和分支推送完成后生效。H005–H008已预分配责任及路径，但queued不授予当前写入权。01–03均已交还。此规则覆盖旧交接包“未领取需再次批准”的描述。

| 模块 | 交接 | 已预建分支名称 | 状态 | 批次 |
|---|---|---|---|---|
| 04 绩效管理 | H004 | `delivery/performance` | active | G2 |
| 05 招聘管理 | H005 | `delivery/recruitment` | queued | G2 |
| 06 假勤管理 | H006 | `delivery/attendance` | queued | G3 |
| 07 薪酬管理 | H007 | `delivery/payroll` | queued | G3 |
| 08 自助报表与集成 | H008 | `delivery/integration` | queued | G3/G4准备 |

## 为什么分支存在也不能在同一目录同时写

本机worktree可隔离，但当前所有聊天使用同一检出目录；受管预览明确每容器只允许一个。不能将不同分支名当成独立运行环境。此轮不宣称已实现并行代码开发，也不启动代理。其他模块可在聊天内并行只读分析。未来独立目录/测试输出与专属文件隔离核实后可调整，现有优先级不变。

## 当前H004接手

04读取最新队列为active后，检查无他人未提交修改，切换已存在的delivery/performance即可开发。接入路径/SHA不一致先定位并恢复原仓库，不重建，不再人为增加“报告后等待批准”的一轮。总控推送本交接后暂停应用写入，直至04明确交还。

## H005–H008后续激活（总控执行，无需用户重新审批）

1. 前包提交并明确交还，核对允许路径与必要测试，合入main；失败项修复或明确不影响下一包的边界。
2. 激活下一包之前更新其预建分支到最新main：仅在该分支没有独立提交且未被检出时允许快进调整；否则保留提交、检查差异并合并，不强制覆盖。
3. 更新本队列status/writer及Ownership/检查点，记录实际激活基线，再推送主线和对应分支。
4. 下一聊天读取active后直接执行。用户只需转递工作完成/新交接提示，不重新确认相同授权；不得按时间或看到前聊天结束就自动认为职责交还。

G1界面环境阻塞不影响绩效/招聘专属代码的开发。假勤→薪酬之间有冻结数据与修订契约依赖；未具备时先推进薪酬已核定录入/复核流程，不能冒称自动算薪完成。G2/G3业务验收与G4生产验收仍分开。
