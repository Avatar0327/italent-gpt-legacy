# 原批准验收逐项映射

原验收场景保留且不增加项目原验收分母；P3实施须把每行Given/When/目标预期做为对应任务子场景，不只执行一个总冒烟用例。原文及hash/Given/When详见[结构化追踪](R1_P2_Approved_Acceptance_Trace.json)。列出的用例均未执行。历史待批措辞由已批准SPEC覆盖，不重询问。

|原验收ID|原要求及现目标|设计|P3用例/子场景载体|
|---|---|---|---|
|BASE-01-AC01|拒绝，不因平台允许访问或历史业务关联放行；未绑定employee不能凭姓名自动匹配员工|[R1_P2_Architecture.md](R1_P2_Architecture.md), [R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-ARC-01, P3-M48-01|
|BASE-01-AC02|须先对账当前撤权，应用/附件仍拒绝；无可信当前授权来源时保持隔离，不能从备份恢复旧访问权|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|P3-REC-02|
|BASE-02-AC01|允许的申请摘要不派生A目录/历史/附件权，viewLevel撤销时职级变更办理拒绝；D3–D5既有规则不重问|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BASE-02-AC02|readConsistent核修订变化409，不以先读成功继续输出；每个动作重验当前权，原角色实例不替真人跨角色验收|[R1_P2_Architecture.md](R1_P2_Architecture.md)|P3-ARC-01|
|BASE-02-AC03|非薪酬专岗拒绝；本人投影与管理权不同，单位承担/原来源不因本人名义开放|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-05|
|BASE-03-AC01|不出现业务成功而无同事务审计；后续刷新核实际revision/对象。数据库外独立故障留痕并未实现，不代签D1例外|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-02|
|BASE-03-AC02|普通字段变更有审计不必产生任职历史；任职变更按实际成功时点产生历史，不拿两类条数相等作正确标准|[R1_P2_Migration_Rollback.md](R1_P2_Migration_Rollback.md)|P3-MIG-01|
|BASE-04-AC01|本人只employee附件；经理不因有名册范围获得员工文件，HR按范围；猜ID不能跳过归属/可见性/当前revision检查|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-06|
|BASE-04-AC02|当前拒绝，旧版本资料保留；新增版本须独立关联，具体复制/来源策略待各模块，不能把普通删除当历史版本替换|[R1_P2_Migration_Rollback.md](R1_P2_Migration_Rollback.md)|P3-MIG-04|
|BASE-04-AC03|不返回可用附件成功；孤儿只在存储维护对账中识别/清理，不向业务列表泄露；生产孤儿扫描策略未实现，需后续设计|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-06|
|BASE-04-AC04|业务读不可达，返回deleted:true/cleanupPending:true；保留删除审计，不因物理残存恢复对外访问|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-06|
|BASE-05-AC01|识别missing/corrupt并阻相应可用声明，不仅核DB元数据；不运行线上恢复或访问真实附件|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|P3-REC-01|
|BASE-05-AC02|先按可信当前授权对账，已处理一级不能重放；后续按当前D1两级与待生效规则办理，旧即时生效测试不能自动证明现定日执行|[R1_P2_Backup_Recovery.md](R1_P2_Backup_Recovery.md)|P3-REC-03|
|BASE-06-AC01|当前主数据预检分别duplicate/conflict/gap；缺映射mapping_required；ready仍DRY_RUN_ONLY，不写任何员工或身份|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-01|
|BASE-06-AC02|记录未配置与待适配契约，不声称已完成外部交易，也不以取得供应商服务阻当前P1；只阻依赖外部真实结果的后续执行分支|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-04|
|BASE-06-AC03|先以业务关联/外部查询核结果，重复相同回执不重复生效，变内容冲突留痕；无可信结果保持unknown，不能自动重付/重签或返回success|[R1_P2_Interfaces_Exceptions.md](R1_P2_Interfaces_Exceptions.md)|P3-INT-03|
|BP-F-REQ-01-AC01|F-SPEC-01已批准：同组织有效区间重叠职位trim同名拒绝，跨组织允许；按新规则测试实现差异已修复。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-01|
|BP-F-REQ-01-AC02|F-SPEC-01/08已批准：职级名称可重复，code唯一；组织同父名唯一，稳定ID与有效区间不变。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-01|
|BP-F-REQ-01-AC03|F-SPEC-08已批准：未完成引用阻停用；旧非法目标只作为历史合成夹具检查执行failed和恢复，不放宽停用。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-01|
|BP-F-REQ-02-AC01|400拒绝且持久attempts不变；到10日00:00后才进入尝试校验，实际成功时刻单独记录；本轮不修改源/系统时钟|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-02-AC02|第一次可HTTP200但execution=failed、attempts增1、员工/任职历史不变；重试成功applied/实际时间，不能用HTTP200提示已生效|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-02-AC03|503整事务回滚，attempts/员工/历史不承诺变更；读取同审批ID/revision确认再重试，不以日志缺失断定业务未生效。独立故障日志能力尚未有保证|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-02-AC04|读取确定原成功；旧revision409/新revision重复状态400均不新增历史，计划/批准/执行事实不抹除。无通用自动重试服务|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-02-AC05|F-SPEC-03已批准：独立新事项无在途时不被无关终态永久强绑；更正原事项才强关联并重审。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-02-AC06|合法更正新单从一级且新审批快照；另一员工/类型/不可读拒绝；原单不复活、不改原日和历史结论|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|BP-F-REQ-04-AC01|F-SPEC-04/05已批准：未来离职未执行不冒已退出；执行退出后同稳定person新建雇佣段并核幂等，不自动恢复账号。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-02|
|BP-F-REQ-04-AC02|不得任意自动合并A/B；集中补证及评审冲突消解/复核/恢复，账号访问另行校验，不能继承过去角色|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-02|
|BP-F-REQ-04-AC03|F-SPEC-04/06明确司龄与合同计次；薪税累计由生产者另定，未知历史不补零。|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-02|
|BP-I-REQ-01-AC01|本人请求仅EA相关，批阅任务可含EB但仍重验当前授权；payslipCount只EA非取消且批次published条数，不是工资金额或支付次数|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-03|
|BP-I-REQ-01-AC02|先awaiting_publish后corrected；保留原申诉ID，不能把approved误报更正已生效或删除旧结果|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-03|
|BP-I-REQ-01-AC03|聚合任务消失但源业务仍按开放窗口允许修改；动作必须重新校验当前状态，待办有无不是唯一授权依据|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-03|
|BP-I-REQ-01-AC04|当前不应凭对象一行标已生成或完成本人采集任务；需源业务实例ID/启动结果明确后补映射，不新增人类访问者|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-03|
|BP-I-REQ-02-AC01|剩余可入职2、待审录用2、已接受待入职1分别展示；不是3-所有在途人数，也不自动证明最终入职容量或预算通过|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|BP-I-REQ-02-AC02|draft不挤掉R1；R2发布后排除R1；历史仍可追溯，不能只按updatedAt选择最新任意状态|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|BP-I-REQ-02-AC03|班次/引用/工资各按自身行粒度统计，不声称员工数3或P1完成率；空金额/缺覆盖保留null|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|BP-I-REQ-02-AC04|M32-SPEC-02已批准：current拒绝不支持的from/to；event_range按各自dateField，快照只能真实snapshotId。|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|BP-I-REQ-02-AC05|旧revision/事务异常不能返回成功CSV；合法导出为文本公式前加单引号并引用转义，数值负数保持数值；本轮不实际导出个人明细|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|BP-I-REQ-07-AC01|items/total只含过滤后项，counts仍全可见域计数；点击后版本/权限需业务接口重核|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01, P3-M19-03|
|BP-I-REQ-07-AC02|任务可存在以供处理，API批准拒绝过期；待办不自动删除业务、改日期或跳级|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01, P3-M19-03|
|BP-I-REQ-07-AC03|待办为来源变化待退回或核对，不能按approved直接发；原批次/工资保持，来源修正后仍需明确重审链|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01, P3-M19-03|
|BP-I-REQ-07-AC04|必须分别明确管理委托与节点办理、有效期/范围/双方当前权限/原代理审计，旧办理人不能持旧链接越权；尚未知原规则的地方不造默认继承，D7首包不扩转交|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01, P3-M19-03|
|BP-I-REQ-11-AC01|M32-SPEC-05已批准：生成/发送/下载逐收件人按当前权交集；撤权阻后续，旧快照重核；源未知仍非源事实。|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-08|
|BP-I-REQ-11-AC02|M32-SPEC-05已批准：订阅版本+周期+收件人+渠道去重；unknown先查，屏蔽不删历史。|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-08|
|M01-REVIEW-AC01|拒绝并显示权限内依赖摘要；旧版本和已结束引用不改；无引用时按批准时态产生新版本|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-12|
|M01-REVIEW-AC02|按批准F-SPEC-01拒绝前者/允许后者，其他目录按各自规则；不以名称替代ID|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-01|
|M01-REVIEW-AC03|按批准占编规则计算增量并校验，失败人员/任职/占用均不变；金额服务未接通显示未校验而非通过|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-03|
|M01-REVIEW-AC04|冲突进入人工核对不自动合并；选定稳定身份后新增任职段，历史保留，账号不恢复；同批重试不重复人|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-02|
|M01-REVIEW-AC05|新增重复拒绝；未获字段修改权限导入仍拒绝；授权更新形成新版本及批次行号，旧记录可追溯|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-08|
|M01-REVIEW-AC06|业务failed保留次数且任职不变；409/503先读同ID/revision再决定重试；不误记成功或重复执行|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-05|
|M01-REVIEW-AC07|按批准F-SPEC-03独立事项不永久强绑，改日更正强制可读原单并两级重审；两类均保留审计|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-06|
|M01-REVIEW-AC08|按批准日期/类型结束有效区间并保留ID/历史；主档、成员消费和人数分列，终态不从列表消失推定|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-10|
|M01-REVIEW-AC09|停用禁新引用；旧法人快照保持；合同比较连续日与稳定ID，改版不重复计，自动政策未启用不自行转换/终止|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-07|
|M01-REVIEW-AC10|每条服务端入口再核数据/字段权限；D3–D5独立要求保持，P1签设计不勾选真人跨角色验收|[R1_P2_M01_Data_History.md](R1_P2_M01_Data_History.md)|P3-M01-04|
|M19-EXECUTION-LIST-01|M19-SPEC-04及M01消费者已批准：审批、执行waiting/failed分列；零待办不等生效。|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01, P3-M19-03|
|M19-REVIEW-AC01|仍按v1节点/审批约束，原业务ID不变，v2只供后续新实例|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01|
|M19-REVIEW-AC02|重复返回原实例；缺配置拒绝且不造无审批自动完成|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-01|
|M19-REVIEW-AC03|旧人被拒；新人仍校验当前范围/本人排除/字段；历史身份和理由保留，D7调动一律不走此动作|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-03|
|M19-REVIEW-AC04|前者全单保持原态并显示失败；后者拒绝流程直回滚，引导原业务更正，不抹历史|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-04|
|M19-REVIEW-AC05|仅可办单一次提交；其余逐项失败且无敏感泄漏；重试不重复推进节点|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-05|
|M19-REVIEW-AC06|仅交集数据可读，其余拒绝；不能自审或提高成员角色|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-06|
|M19-REVIEW-AC07|服务器拒绝，业务与流程不变，记录可提交的拒绝审计；存储失败不虚称已留痕|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-06|
|M19-REVIEW-AC08|先查回执、不重复发；旧节点待发事件失效，业务不因通知失败倒退；当前测试不实发消息|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-07|
|M19-REVIEW-AC09|显示审批与执行两态，待办0不写已生效；动作重验D1–D7和M01已批约束|[R1_P2_M19_Workflow_Transactions.md](R1_P2_M19_Workflow_Transactions.md)|P3-M19-07|
|M32-REVIEW-AC01|按各行主键及M01已批规则分母去重，名册total不冒在职数，兼职不额外当人头|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|M32-REVIEW-AC02|自然人/申请/需求人数分列，当前剩余2仅当前候选口径，不能证明金额预算通过|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-02|
|M32-REVIEW-AC03|按班次日期包含边界，未知分钟为null不补0，不冒充已发布月报|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-02|
|M32-REVIEW-AC04|工资条/引用粒度各自计数，金额整数分，发布不标支付，按当前工资权限投影|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-02|
|M32-REVIEW-AC05|草稿不替换正式，发布替代链可追溯；旧记录仍当前权限下可读，缺评分不补0|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-04|
|M32-REVIEW-AC06|零仅当前可见无后备，配置1不等已评分1；不外推源准备度或人才算法|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-01|
|M32-REVIEW-AC07|0分母比率null，缺成绩null；报名按记录、人按去重，不把指标相加|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-02|
|M32-REVIEW-AC08|不支持的时间参数明确拒绝，不默默忽略/伪造历史；已有快照重验当前权限|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-03|
|M32-REVIEW-AC09|全部服务端拒绝越界，计数/错误不泄漏隐藏数据，旧下载链接也重验|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-05|
|M32-REVIEW-AC10|超同步上限走明确有界任务或阻并提示，不截断；冲突不返回文件；文本安全转义、负数仍数值|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-06|
|M32-REVIEW-AC11|非法字段/表达式拒绝且不新版本；零分母输出null/原因，不假成功|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-07|
|M32-REVIEW-AC12|各自权限投影，撤权者阻发送；不共用全量附件，unknown先查回执；本轮只设计用例|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-08|
|M32-REVIEW-AC13|显示未配置/不可用且完整目录保留，不用模拟结果报真实联调或评分|[R1_P2_M32_Reports_Jobs.md](R1_P2_M32_Reports_Jobs.md)|P3-M32-10|
|M48-REVIEW-AC01|只授权直线对象及字段，不能读虚线/间接或敏感内容|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-02|
|M48-REVIEW-AC02|不返回全员/假本人数据，清对应缓存、禁止办理|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-01|
|M48-REVIEW-AC03|更正待发布与待审批分开；他人批阅不冒充本人学习任务，原ID可追溯|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-03|
|M48-REVIEW-AC04|已配置只展示原指标/单位和允许动作，不自动计绩效分；未接明示未配置，完整范围/后续联调责任保留|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-04|
|M48-REVIEW-AC05|遵守原模块动作限制和原版本，不能门户绕过调整或把申诉批准当发布|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-05|
|M48-REVIEW-AC06|未知不是0；动作409刷新、不双提交，日期/额度由M11按批准规则验证|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-05|
|M48-REVIEW-AC07|消失不等锁定/已完成；修改/批阅按源有效期/角色/版本再核，不绕放行|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-05|
|M48-REVIEW-AC08|显示不可办理原因，不默认推进阶段或重开计划，关联原计划/阶段/行动ID|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-05|
|M48-REVIEW-AC09|相应旧数据清除、附件直接链接拒绝；服务故障不展示假0或成功|[R1_P2_M48_Authorization_Consumers.md](R1_P2_M48_Authorization_Consumers.md)|P3-M48-06|
