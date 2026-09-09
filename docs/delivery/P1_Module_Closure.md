# 模块闭环、滚动转序及当前收口清单

生成来源：`Scope_Register.json → deliveryScope / p1Baseline / modules[].p1 / p1B`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：2026-09-09T15:43:36.730682+00:00。

当前交付为用户确认的15个HR核心模块及六类非模块基础能力；原48组历史完整保留，33组本次交付暂缓，不计完成、不阻当前P1退出。各历史证据的适用时间保持。

## 当前执行模式：模块闭环优先、按R版本滚动转序

本轮新批准执行节奏；不批准未决业务规则、内部延期或验收豁免。唯一主模块 M01；备用 未启用；实际执行 M01。仅主模块剩余必要工作全部依赖外部条件/用户决定才可启用1个备用；主模块可推进时优先回归。

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
| M01 组织员工 | R1 / primary | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M19 审批中心 | R1 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
| M48 员工自助 | R1 / queued | 进行中 | 进行中 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
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

转序就绪 0/15；独立指标，不等业务验收或生产上线。风险证据规则：核心交易、权限、生效时间、数据完整性及关键异常优先执行证据；不足时写明限制和明确项目设计，须获规则/例外批准才能转序；普通配置/静态字段允许页面、帮助与一致既有证据形成需求结论；不穷尽配置组合；每个新探索绑定closureChecklist问题ID；先判断是否改变当前需求正确性，不阻塞事项进入后续验证清单；模式调整不批准业务规则、内部延期或验收豁免；D1–D7保持，E2仅本人；P1权限设计评审不替代后续真人权限验收。


## M01完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M01-CLOSE-01 / 组织 | BP-F-REQ-01；BP-F-REQ-10；BP-F-REQ-14 | BC-F28；BC-F29；BC-F42 | 组织有效期/行政维度/停用影响、法人空适用范围和共享权限待证；R/A/B/LA不重建 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |
| M01-CLOSE-02 / 职务体系 | BP-F-REQ-01；BP-F-REQ-11 | BC-F17；BC-F31；BC-F32；BC-F33 | 职位与职务/序列/职级不同；职位同组织/跨组织重名已证，职务/职级及停用时态待证，F-SPEC-01待决 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |
| M01-CLOSE-03 / 编制 | BP-F-REQ-06 | BC-F21；BC-F40 | 源人数/比例/主兼岗占编算法和审批未证；当前按岗位人数计划不代全部编制，M09金额预算仅局部依赖 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |
| M01-CLOSE-04 / 人员 | BP-F-REQ-01；BP-F-REQ-04；BP-F-REQ-06；BP-F-REQ-12 | BC-F22；BC-F35；BC-F36；BC-F39；BC-F43 | 多入口模板、完整自定义子集、重聘匹配冲突与累计/账号边界缺口；F-SPEC-04待决 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |
| M01-CLOSE-05 / 任职 | BP-F-REQ-02；BP-F-REQ-13；BP-F-REQ-15 | BC-F03；BC-F40；BC-F41；BC-F44；BC-F45；BC-F46 | 兼职终态、借调/外派、审批路由与离职后各消费者待证；D1–D7项目设计独立，F-SPEC-02/03待决 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |
| M01-CLOSE-06 / 合同 | BP-F-REQ-05；BP-F-REQ-14 | P1-CONTRACT-LIST；P1-CONTRACT-TYPE；BC-F23；BC-F24；BC-F42 | 法人稳定关联、合同累计/续签/终止日期及历史字段权限待证；电子签仅BASE-06预留，不等真实签署 | True；核心对象/权限/时态/完整性：高风险；静态属性按证据综合 | 先复用证据与源码收窄具体问题；高风险定向补证，或形成明确产品方案和受限边界交用户批准；普通字段不穷尽组合；现有范围逐项映射，未因模式调整缩减 | 进行中 |

