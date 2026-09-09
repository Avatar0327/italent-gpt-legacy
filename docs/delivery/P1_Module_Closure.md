M01当前集中评审入口：[完整范围、规则与受限边界](P1_M01_Review_Package.md)。状态：P1受限通过，需求基线已批准；批准记录：M01-P1-APPROVAL-20260909。

# 模块闭环、滚动转序及当前收口清单

生成来源：`Scope_Register.json → deliveryScope / p1Baseline / modules[].p1 / p1B`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：2026-09-09T17:23:50.064749+00:00。

当前交付为用户确认的15个HR核心模块及六类非模块基础能力；原48组历史完整保留，33组本次交付暂缓，不计完成、不阻当前P1退出。各历史证据的适用时间保持。

## 当前执行模式：模块闭环优先、按R版本滚动转序

本轮新批准执行节奏；不批准未决业务规则、内部延期或验收豁免。唯一主模块 M37；备用 未启用；实际执行 M37。仅主模块剩余必要工作全部依赖外部条件/用户决定才可启用1个备用；主模块可推进时优先回归。

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
| R2 | 未齐备：M37,M06,M26,M18,M17,M03,BASE-01,BASE-02,BASE-03,BASE-04,BASE-05,BASE-06,rangeReviewApproved | 未批准 | 未取得该R下游批准 |
| R3 | 未齐备：M27,M16,M12,M11,M07,BASE-01,BASE-02,BASE-03,BASE-04,BASE-05,BASE-06,rangeReviewApproved | 未批准 | 未取得该R下游批准 |

| 模块 | R版本/队列 | P1A判定 | P1B评审 | 转序就绪 | 未达到条件 |
|---|---|---|---|---|---|
| M01 组织员工 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M19 审批中心 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M48 员工自助 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M32 报表 | R1 / closed_restricted | 受限通过 | 受限通过 | 是 |  |
| M37 人才标准 | R2 / primary | 已完成待评审 | 已完成待评审 | 否 | implementationRulesDecided；acceptanceExecutable；dependenciesAndExceptionsResolved；p1AApproved；p1BApproved；transitionReviewApproved |
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

转序就绪 4/15；独立指标，不等业务验收或生产上线。风险证据规则：核心交易、权限、生效时间、数据完整性及关键异常优先执行证据；不足时写明限制和明确项目设计，须获规则/例外批准才能转序；普通配置/静态字段允许页面、帮助与一致既有证据形成需求结论；不穷尽配置组合；每个新探索绑定closureChecklist问题ID；先判断是否改变当前需求正确性，不阻塞事项进入后续验证清单；模式调整不批准业务规则、内部延期或验收豁免；D1–D7保持，E2仅本人；P1权限设计评审不替代后续真人权限验收。


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


## M32完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M32-CLOSE-01 / 招聘 | BP-I-REQ-02 | BC-R01；BC-R14；BC-R16 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |
| M32-CLOSE-02 / 人事 | BP-I-REQ-02 | BC-F39；BC-F45 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |
| M32-CLOSE-03 / 假勤 | BP-I-REQ-02 | BC-A04；BC-A11；BC-A12 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |
| M32-CLOSE-04 / 薪酬 | BP-I-REQ-02 | BC-S03；BC-S08 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |
| M32-CLOSE-05 / 绩效 | BP-I-REQ-02 | BC-P07；BC-P14；BC-P15 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |
| M32-CLOSE-06 / 人才等 | BP-I-REQ-02；BP-I-REQ-11 | BC-C40；BC-C30；BC-L19；BC-P1C-M32 | P1硬条件已满足；原站未知及新增实现/补验进入P2/P3/P4 | False；敏感数据/分母和时间正确性、导出/订阅外传、跨域依赖 | 明确批准六组推荐与M32-LIMIT-01，按条件核对；M32-P1-APPROVAL-20260909 | 受限通过 |


## M37完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M37-CLOSE-01 / 标准 | BP-C-REQ-07 | BC-C32；BC-C35；BC-C36；BC-C37 | 已完成所列具体需求/验收材料；五项业务规则及M37-LIMIT-01未批，原站使用中变更/权限/算法执行受限 | True；等级尺度/版本漂移/权限泄漏及缺值误判属于核心需求风险 | 集中评审明确候选与有范围受限责任；不穷尽所有组合；C32–36合成结果＋C37/40引用回读＋当前静态；不同模块批准不代批M37 | 已完成待评审 |
| M37-CLOSE-02 / 指标库 | BP-C-REQ-07 | BC-C33；BC-C34；BC-C35 | 已完成所列具体需求/验收材料；五项业务规则及M37-LIMIT-01未批，原站使用中变更/权限/算法执行受限 | True；等级尺度/版本漂移/权限泄漏及缺值误判属于核心需求风险 | 集中评审明确候选与有范围受限责任；不穷尽所有组合；C32–36合成结果＋C37/40引用回读＋当前静态；不同模块批准不代批M37 | 已完成待评审 |


## M48完整登记范围收口清单

| 问题/原范围 | 需求 | 证据 | 具体缺口 | 阻塞P1/风险 | 关闭方式与判据 | 当前状态 |
|---|---|---|---|---|---|---|
| M48-CLOSE-01 / 团队 | BP-I-REQ-01 | BC-L15；BC-P1C-M48 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-02 / 审批 | BP-I-REQ-01；BP-I-REQ-07 | BC-I10；BC-I27 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-03 / OKR | BP-P-REQ-09 |  | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-04 / 目标 | BP-I-REQ-01；BP-P-REQ-05 | P1-SELF-REVIEW；P1-GOAL | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-05 / 假勤 | BP-I-REQ-01；BP-A-REQ-01 | BC-A07；BC-A12 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-06 / 学习 | BP-I-REQ-01；BP-L-REQ-01；BP-L-REQ-06 | BC-L03；BC-L06-08；BC-L19 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |
| M48-CLOSE-07 / 发展计划 | BP-I-REQ-01；BP-C-REQ-05 | BC-C27；BC-C28 | P1硬条件已满足；原源证据差异及实现/补验责任保留到P2/P3/P4。 | False；本人/团队权限、状态、原单完整性或跨域依赖 | 用户已批准四组推荐及本模块受限边界，按现有条件核对通过；M48-P1-APPROVAL-20260909；不将批准扩为原站全部验证或实现通过 | 受限通过 |


M19当前材料：[P1受限通过，需求基线已批准](P1_M19_Review_Package.md)。批准、源取证及后续执行各自独立。

M32当前材料：[P1受限通过，需求基线已批准](P1_M32_Review_Package.md)。批准、源取证及后续执行各自独立。

M37当前材料：[已完成待评审](P1_M37_Review_Package.md)。批准、源取证及后续执行各自独立。

M48当前材料：[P1受限通过，需求基线已批准](P1_M48_Review_Package.md)。批准、源取证及后续执行各自独立。

[R1 P2完整交接](P1_R1_P2_Handoff.md) · [新窗口启动提示词](P1_R1_P2_Start_Prompt.md)：只准P2设计，不等P2退出或P3通过。
