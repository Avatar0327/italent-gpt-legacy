M01当前集中评审入口：[完整范围、规则与受限边界](P1_M01_Review_Package.md)。状态：P1受限通过，需求基线已批准；批准记录：M01-P1-APPROVAL-20260909。

# 模块闭环、滚动转序及当前收口清单

生成来源：`Scope_Register.json → deliveryScope / p1Baseline / modules[].p1 / p1B`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：2026-09-09T16:53:50.674271+00:00。

当前交付为用户确认的15个HR核心模块及六类非模块基础能力；原48组历史完整保留，33组本次交付暂缓，不计完成、不阻当前P1退出。各历史证据的适用时间保持。

## 当前执行模式：模块闭环优先、按R版本滚动转序

本轮新批准执行节奏；不批准未决业务规则、内部延期或验收豁免。唯一主模块 M48；备用 未启用；实际执行 M48。仅主模块剩余必要工作全部依赖外部条件/用户决定才可启用1个备用；主模块可推进时优先回归。

| R版本 | 模块顺序 | 当前边界 |
|---|---|---|
| R1 核心底座 | M01→M19→M48→M32 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R2 人才管理 | M37→M06→M26→M18→M17→M03 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R3 HR专业领域 | M27→M16→M12→M11→M07 | 当前承诺，按模块闭环滚动；用户本轮明确顺序；不是此前已有分层，不批准未决业务规则或内部缩减 |
| R4 本次交付暂缓 | M02→M04→M05→M08→M09→M10→M13→M14→M15→M20→M21→M22→M23→M24→M25→M28→M29→M30→M31→M33→M34→M35→M36→M38→M39→M40→M41→M42→M43→M44→M45→M46→M47 | 暂缓；其余33组退出当前P1退出条件/主动探索。历史代码/证据/数据/验收/隔离成果保留；只准为保留模块引用已有前置或最小公共配置，不顺带恢复完整独立模块。 |

四项条件均true且有证据；P1A结论及P1B评审均完整通过或获明确受限批准；transitionReview.approved=true且有批准范围/日期/记录才可转序。受限通过自身不足以转序。

R1/R2/R3本版本所有模块转序就绪、适用基础能力要求已评审可实施且版本评审明确允许P2/P3，才转序；不要求后续R版本全部完成P1。P4业务和生产验收独立。

| 模块 | R版本/队列 | P1A判定 | P1B评审 | 转序就绪 | 未达到条件 |
|---|---|---|---|---|---|
| M01 组织员工 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M19 审批中心 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M48 员工自助 | R1 / primary | 已完成待评审 | 已完成待评审 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M32 报表 | R1 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M37 人才标准 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M06 任职资格 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M26 360度评估 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M18 在线盘点 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M17 继任与发展 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M03 干部管理2.0 | R2 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M27 学习管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M16 绩效管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M12 招聘管理系统 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M11 假勤管理 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M07 薪酬社保 | R3 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |

转序就绪 2/15；独立指标，不等业务验收或生产上线。风险证据规则：核心交易、权限、生效时间、数据完整性及关键异常优先执行证据；不足时写明限制和明确项目设计，须获规则/例外批准才能转序；普通配置/静态字段允许页面、帮助与一致既有证据形成需求结论；不穷尽配置组合；每个新探索绑定closureChecklist问题ID；先判断是否改变当前需求正确性，不阻塞事项进入后续验证清单；模式调整不批准业务规则、内部延期或验收豁免；D1–D7保持，E2仅本人；P1权限设计评审不替代后续真人权限验收。


## M01完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M01-CLOSE-01 / 组织 | BP-F-REQ-01；BP-F-REQ-10；BP-F-REQ-14 | BC-F28；BC-F29；BC-F42 | P1硬阻塞已关闭；原缺口保留为后续差异验证：组织时态/停用依赖采用源规则或批准候选；法人空范围及合同/薪资引用采用批准策略 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |
| M01-CLOSE-02 / 职务体系 | BP-F-REQ-01；BP-F-REQ-11 | BC-F17；BC-F31；BC-F32；BC-F33 | P1硬阻塞已关闭；原缺口保留为后续差异验证：目录重名与有效区间策略批准；职务/序列/职级范围模型及管理权限批准 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |
| M01-CLOSE-03 / 编制 | BP-F-REQ-06 | BC-F21；BC-F40 | P1硬阻塞已关闭；原缺口保留为后续差异验证：主兼借派占编及人数版本政策批准；金额预算是否强阻断和未接通状态批准 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |
| M01-CLOSE-04 / 人员 | BP-F-REQ-01；BP-F-REQ-04；BP-F-REQ-06；BP-F-REQ-12 | BC-F22；BC-F35；BC-F36；BC-F39；BC-F43 | P1硬阻塞已关闭；原缺口保留为后续差异验证：重聘身份/冲突/任期/司龄与恢复边界批准；独立入口模板、人员子集/导入/字段权限基线批准 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |
| M01-CLOSE-05 / 任职 | BP-F-REQ-02；BP-F-REQ-13；BP-F-REQ-15 | BC-F03；BC-F40；BC-F41；BC-F44；BC-F45；BC-F46 | P1硬阻塞已关闭；原缺口保留为后续差异验证：故障留痕与同事项原单关联的边界批准；主兼职和离职日期、在途流程及消费者状态策略批准 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |
| M01-CLOSE-06 / 合同 | BP-F-REQ-05；BP-F-REQ-14 | P1-CONTRACT-LIST；P1-CONTRACT-TYPE；BC-F23；BC-F24；BC-F42 | P1硬阻塞已关闭；原缺口保留为后续差异验证：法人ID/日期/续签/计次版本策略批准；外部电子签仅契约边界、失败及历史权限批准 | False；核心对象/权限/时态/完整性未证部分待明确规则及有范围例外批准 | 所引用规则已由用户批准；源未知按M01-LIMIT-01有范围接受。后续P2/P3/P4验证责任不删除。；M01-P1-APPROVAL-20260909；完整原登记功能未缩减，F01–F04不代整个M01。 | 受限通过 |


## M19完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M19-CLOSE-01 / 流程管理 | BP-I-REQ-07 | BC-P1C-M19；BC-I10；BC-I27 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；权限/业务回写/异常为高风险 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M19-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M19-CLOSE-02 / 管理员委托 | BP-I-REQ-07 |  | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；权限/业务回写/异常为高风险 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M19-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |


## M48完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M48-CLOSE-01 / 团队 | BP-I-REQ-01 | BC-L15；BC-P1C-M48 | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-01,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-02 / 审批 | BP-I-REQ-01；BP-I-REQ-07 | BC-I10；BC-I27 | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-03 / OKR | BP-P-REQ-09 |  | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-04 / 目标 | BP-I-REQ-01；BP-P-REQ-05 | P1-SELF-REVIEW；P1-GOAL | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-05 / 假勤 | BP-I-REQ-01；BP-A-REQ-01 | BC-A07；BC-A12 | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-06 / 学习 | BP-I-REQ-01；BP-L-REQ-01；BP-L-REQ-06 | BC-L03；BC-L06-08；BC-L19 | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |
| M48-CLOSE-07 / 发展计划 | BP-I-REQ-01；BP-C-REQ-05 | BC-C27；BC-C28 | 本项消费字段/权限/行为/验收候选已明确；尚需M48-SPEC-02,M48-SPEC-03,M48-SPEC-04及M48-LIMIT-01评审，源详细/独立角色执行未证。 | True；本人/团队权限、状态、原单完整性或跨域依赖 | 按同源消费契约/候选与受限边界集中评审；不要求为了P1穷尽源配置或先完成R2/R3全部实现；原七项完整保留；未批准不得记就绪或跨域业务通过 | 已完成待评审 |


M19当前材料：[P1受限通过，需求基线已批准](P1_M19_Review_Package.md)。批准、源取证及后续执行各自独立。

M48当前材料：[备用模块材料已完成待评审](P1_M48_Review_Package.md)。批准、源取证及后续执行各自独立。
