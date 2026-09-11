# R1原站行为矩阵

当前共76条用例记录；observed含局部失败事实，不等于通过。完整模块0/4，E2E0/5。各项完整字段以同名JSON为准。

| 用例 | 模块 | 范围 | 执行 | 实际结果 | 分类 |
|---|---|---|---|---|---|
| M32-SEP11-EXPLICIT-DATE-ATTEMPT | M32 | 固定姓名日期报表尝试 | observed | 两人已选择，日期控件超时，未确认筛选应用，未取得报表结果 | ENV_BLOCKED |
| M19-TRANSFER-SEP11-TERMINATED | M19 | 撤回原调动终止后效 | observed | 原业务作废，原流程已终止；系统9/11 01:15撤销，理由离职发起后自动终止 | 待处置；不判缺陷 |
| M01-EXIT-SEP11-STATE | M01 | 实际离职状态及区间 | observed | 离职人员唯一命中；离职任职生效中；同personId和退出UUID；执行人/审计未知 | 待处置；不判缺陷 |
| R1-SEP11-FRESH-QUERY-GATE | M01 | 9月11日新服务器查询恢复门槛 | observed | 两次新导航均未取得业务结果；组织main空、控件0，当前请求日志Failed to fetch。9/11日期条件已达；实际离职/终止/报表/再入职仍未知，不能沿用旧DOM。 | ENV_BLOCKED |
| M32-RESUME-SORT-001 | M32 | 两人报表图表和排序尝试 | observed | 旧页面DOM仍EMP002试用1、EMP001正式1，总2；截图柱图2。姓名表头语义/可见坐标点击超时，行序未变，不判排序通过或缺陷。 | ENV_BLOCKED |
| M19-RESUME-RECALL-002 | M19 | 两张撤回原单只读回查 | observed | 调动与转正均仍同流程开始节点，审计分别20:44/20:52、21:57/22:03，编辑未出现新表单；未重提/代审。 | 待处置；不判缺陷 |
| R1-RESUME-ENV-001 | M01 | 恢复身份与独立业务区加载 | observed | 测试管理员身份标识正常；职位新查询业务区持续空白并记录请求超时；未重复创建组织。 | ENV_BLOCKED |
| M32-ORG-SELECT-LIMIT | M32 | 本轮组织条件未选中 | observed | ORG002经候选文字/完整行/CUA点击仍已选0，已取消；当前2员工结果没有应用组织条件，不能判组织过滤缺陷。 | ENV_BLOCKED |
| M01-ORG-003-EDIT-STOP | M01 | 本轮组织备注编辑、审计显示和停用预览 | observed | 同UUID备注持久化，名称/代码/归属/日期不变；操作记录仅设立18:34:09，变更记录仅1版本，编辑审计未取得。停用包含全体职位人员迁移，未核完整影响清单而取消，未实际停用。 | 待处置；不判缺陷 |
| M32-TWO-EMP-001 | M32 | 两名本轮员工正式与试用人数 | observed | 仅EMP001+EMP002及今天入职，正式1、试用1、合计2，各人数1；未来离职和撤回转正申请未提前改变当前人数。非分页或批量通过。 | 待处置；不判缺陷 |
| M19-REG-002 | M19 | 正式转正申请提交撤回与原单审计 | observed | 转正业务9737bceb/流程fb06f86c已审批中后撤回；审计21:57提交/22:03撤回，同实例申请人开始节点。独立审批、重提/改期未执行，员工仍试用；摘要离职字段错位。 | 待处置；不判缺陷 |
| M01-EMP-002 | M01 | 试用员工新增与跨组织日期必填边界 | observed | 第二员工创建成功66ea978b；试用期限/预计结束必填。入职9/1早于本轮组织9/10被拒，不改组织历史；改9/10后试用结束10/9。日期重置邮箱工号已纠正。 | 待处置；不判缺陷 |
| M19-REQUEST-001 | M19 | 调动申请提交与源路线 | observed | 提交后审批中；开始→直接上级→HR访谈→结束，未由管理员代审 | 待处置；不判缺陷 |
| M19-RECALL-001 | M19 | 撤回原单及审计 | observed | 源撤回同UUID返回开始；重提/改期/新原单关系未执行 | 待处置；不判缺陷 |
| M48-ADMIN-STATE-001 | M48 | 管理员申请人工作台状态 | observed | 管理员能看到本轮申请待处理；非独立员工视角 | ROLE_BLOCKED |
| M32-OWN-ORACLE-001 | M32 | 当前人员与历史任职粒度手算 | observed | 1人、2历史任职、1当前主职，当前花名册人数1。与已批在职人数distinct personId及P3静态每人员一行窄项一致；不含动态复刻验收 后续扩为2名本轮员工，正式1/试用1，仍按同一窄项人数规则计一次MATCH。 | MATCH |
| M32-DATE-EMPTY-001 | M32 | 今天与明天入职日期筛选 | observed | 明天空数据、今天恢复本轮1人，不代历史快照 | 待处置；不判缺陷 |
| M32-EXPORT-001 | M32 | 仅本轮正式下载 | observed | Chromium blocked，未取得文件，未绕过 | ENV_BLOCKED |
| M32-SUB-DRAFT-001 | M32 | 订阅草稿只读并取消 | observed | 观察权限/快照选项，取消，无保存无发送 | 待处置；不判缺陷 |
| M01-EXIT-001 | M01 | 离职必填、次日未来版本及人数不提前改变 | observed | 最后工作日9/10→离职任职9/11未来生效，当前仍正式且报表1人；与P1/P2次日边界和P3 exitExecute日期校验静态窄项一致；未执行次日HR/自动作业，未再入职 | MATCH |
| M01-JOB-001 | M01 | 职位正式新增与UUID | observed | ORG_002下保存JOB_001，列表精确重读1条，在岗0兼职0 | 待处置；不判缺陷 |
| M01-JOB-002 | M01 | 职位第二组织新增与必填拒绝 | observed | 空名称/所属组织提交被必填拒绝；补齐ORG_003及JOB_002后保存并精确回读 | 待处置；不判缺陷 |
| M01-EMP-001 | M01 | 员工正式新增及邮箱必填 | observed | 草稿去除默认既有经理/公司，邀请否、身份证号/手机空，邮箱必填拒绝后补虚构邮箱保存，在职列表唯一结果 | 待处置；不判缺陷 |
| M01-EMP-001-ASSIGNMENT | M01 | 主职及入职历史 | observed | 正式/主职/生效中；入职-新增入职；今日开始，经理为空 | 待处置；不判缺陷 |
| M01-TRANSFER-001 | M01 | 管理员直接调动立即生效 | observed | ORG_002/JOB_001至ORG_003/JOB_002今日直接调动保存生效，原入职历史保留；本次UI未两级审批/单独HR执行 | INTENTIONAL_DIFFERENCE |
| M01-ORG-001 | M01 | 合成组织保存及完整名称重读 | observed | 保存后完整名称查询找到稳定UUID d1d541ab-92f9-4fce-80c6-aa5687433175；启用日期2026-09-10；父级为测试租户根 | 待处置；不判缺陷 |
| M01-ORG-002 | M01 | 合成组织保存及完整名称重读 | observed | 保存后完整名称查询找到稳定UUID db7df096-624b-4d1e-ab4e-0552a56f052c；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | 待处置；不判缺陷 |
| M01-ORG-003 | M01 | 合成组织保存及完整名称重读 | observed | 保存后完整名称查询找到稳定UUID a7b55bd7-0ef2-44a0-9d29-6259fe053da3；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | 待处置；不判缺陷 |
| M01-PARITY-01 | M01 | 稳定标识与父子关系保存（窄项三方对照） | observed | 原站三条组织保存后可按完整名称重读UUID，子组织路径保留本轮父级；P2要求稳定ID及父子关联；P3 r1-m01.ts的catalog/make/m01Write/m01Entity持久化并回读ID及parentId，catalog acceptance合成测试覆盖父子创建。仅此窄项一致。 | MATCH |
| M01-FIELD-01 | M01 | 普通新建行政上级空值校验 | observed | 大类为部门且行政上级为空时，确定后显示必填，表单保留；补选父级后首条组织保存。不能外推为所有组织类型均禁止根节点。 | 待处置；不判缺陷 |
| M01-AUDIT-01 | M01 | 新组织设立审计只读 | observed | 组织操作记录保留设立事件、业务日期2026-09-10、操作时间2026-09-10 18:27:04及本会话操作人；只证明该次设立审计，不证明历史不可改或失败原子性。 | 待处置；不判缺陷 |
| M01-IMPORT-01 | M01 | 正式组织导入模板下载 | observed | 正式菜单下载模板后download等待超时，主iframe显示This page has been blocked by Chromium；无下载文件，无导入执行。 | ENV_BLOCKED |
| M19-QUERY-01 | M19 | 审批本轮标题筛选及管理说明 | observed | 标题前缀与审批中条件下空集；页面展示催办/转交/撤销/一键审批及流程干预说明，摘要与审批状态列可见。未执行管理动作，不能据此覆盖D7。 | 待处置；不判缺陷 |
| M48-ENTRY-01 | M48 | 原管理会话下的人事申请入口 | observed | 存在本人/他人调动、离职和新增兼职申请入口，任职/人员/审批状态分列。此为原管理会话，非独立员工；未打开或办理既有人员申请。 | ROLE_BLOCKED |
| M32-CATALOG-01 | M32 | 报表目录口径文案 | observed | 目录分别描述最新一条任职、全部历史任职含兼职、指定时点在职；部分报表标示异步且需运行更新。目录文案不是数值口径实测。 | 待处置；不判缺陷 |
| M32-INPUT-01 | M32 | 姓名选择器前缀回读与空候选 | observed | input.value确认本轮前缀，人员候选为空，选择器取消；原报表380条属于既有数据，非本轮批量。 | 待处置；不判缺陷 |
| M32-ORG-01 | M32 | 新组织进入报表部门选择器 | observed | 本轮ORG_001在部门搜索结果中可见；点击后已选组织仍0，取消选择器。未应用组织筛选，未取得空报表0行，不能称对账通过。 | 待处置；不判缺陷 |
| M01-PENDING-ORG-LIFECYCLE | M01 | 组织编辑、更名、停用与在用保护 | partially_observed | 新增三组织、ORG003备注编辑已验；停用预览含整体迁移，未执行停用/迁移 | 待处置；不判缺陷 |
| M01-PENDING-ORG-UNIQUE | M01 | 同父重名、不同父重名及编码重复 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M01-PENDING-POSITION | M01 | 岗位新增、编辑、停用及上下级 | partially_observed | 新增2职位、名称/组织必填已验；编辑/停用/唯一性未验 | 待处置；不判缺陷 |
| M01-PENDING-EMP-CREATE | M01 | 员工新增及三入口模板 | partially_observed | 创建1员工、邮箱必填、邀请账号否；其他创建入口未验 | 待处置；不判缺陷 |
| M01-PENDING-EMP-IMPORT | M01 | 员工正式导入5–10、30–50、100–500 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M01-PENDING-ASSIGN | M01 | 主职、兼职、多任职及占用 | partially_observed | 主职及调动2条任职历史已验；兼职/多任职未验 | ROLE_BLOCKED |
| M01-PENDING-JOIN-REGULARIZE | M01 | 入职、转正流程 | partially_observed | 2员工分别正式/试用；转正正式申请已提交撤回，维护入口未保存；审批/实际生效未验 | ROLE_BLOCKED |
| M01-PENDING-TRANSFER | M01 | 调动计划日、实际生效和日期重审 | partially_observed | 直接调动生效；他人调动申请另行提交并撤回；独立两方审批未验 | ROLE_BLOCKED |
| M01-PENDING-EXIT-REHIRE | M01 | 离职、再入职与身份连续性 | partially_observed | 9/11新查询确认人员离职、退出任职生效中；旧雇佣段ID/结束审计和正式再入职未完成 | 待处置；不判缺陷 |
| M01-PENDING-LEGAL | M01 | 法人组织归属与空范围 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M01-PENDING-FIELDS | M01 | 必填、长度、格式、空值及重复值 | partially_observed | 职位/邮箱/试用期限/试用结束必填、入职早于组织生效被拒已验；未覆盖全字段、长度、格式、重复 | 待处置；不判缺陷 |
| M01-PENDING-HISTORY-ATTACH | M01 | 附件、历史版本、原单与审计 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M01-PENDING-CONCURRENCY | M01 | 并发修改和重复提交 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M19-PENDING-SEQUENTIAL | M19 | 顺序审批、两方独立与禁止自审 | partially_observed | 原站路线开始→直接上级→HR访谈→结束；无独立两方审批实操 | ROLE_BLOCKED |
| M19-PENDING-DELEGATION | M19 | 管理员委托、接受与撤销 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M19-PENDING-REJECT | M19 | 同意、驳回和驳回原因 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M19-PENDING-WITHDRAW | M19 | 撤回、重提和修改日期重审 | partially_observed | 20:44提交/20:52撤回；同业务和流程UUID回到开始。未重提/改期 | ROLE_BLOCKED |
| M19-PENDING-EFFECT | M19 | 审批完成与HR执行生效分离 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M19-PENDING-RECOVERY | M19 | 重复点击、超时、执行失败恢复 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M19-PENDING-SUMMARY | M19 | 摘要字段、职级变化与原新单追溯 | partially_observed | 调动摘要含离职字段标签；敏感职级及独立角色可见性未验 | ROLE_BLOCKED |
| M48-PENDING-PROFILE | M48 | 本人资料可见和可改字段 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M48-PENDING-ATTACH | M48 | 自助附件上传下载替换 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M48-PENDING-APPLICATION | M48 | 自助申请进度历史撤回驳回重提 | partially_observed | 管理员申请人工作台显示本轮申请待处理；非独立员工验收 | ROLE_BLOCKED |
| M48-PENDING-BOUNDARY | M48 | 本人/他人、脱敏及管理员差异 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M48-PENDING-SEVEN | M48 | 七入口可用、无权、未配置和异常 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| M32-PENDING-ORACLE | M32 | 指标口径与明细一致性 | partially_observed | 独立手算1员工=当前花名册1人、任职历史2行、当前主职1；全指标及批量未验 | 待处置；不判缺陷 |
| M32-PENDING-TIME | M32 | 组织日期筛选、当前值与历史快照 | partially_observed | 入职日期明天空数据、今天1人；历史快照未验 | 待处置；不判缺陷 |
| M32-PENDING-PAGING | M32 | 分页排序及100–500行显示 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |
| M32-PENDING-EXPORT | M32 | 导出内容、空导出与大文件 | partially_observed | 本轮筛选结果正式下载被Chromium阻止；无文件，不绕过 | ENV_BLOCKED |
| M32-PENDING-SUBSCRIBE | M32 | 订阅、权限过滤与投递 | partially_observed | 订阅草稿字段读取后取消；未创建订阅或推送 | ROLE_BLOCKED |
| M32-PENDING-DATA-EDGE | M32 | 空/重复/失效组织/离职/跨组织边界 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |
| E2E-SUCCESS | E2E | R1端到端成功路径 | partially_observed | 组织→职位→员工→直接调动→历史/报表局部链，不能替代双审批/执行HR/独立员工，完整未通过 | ROLE_BLOCKED |
| E2E-REJECT | E2E | R1端到端驳回路径 | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |
| E2E-WITHDRAW | E2E | R1端到端撤回路径 | partially_observed | 两张申请提交→审批中→申请人撤回→管理员工作台/报表未提前生效；新单重提和独立员工未验 | ROLE_BLOCKED |
| E2E-REDATE | E2E | R1端到端改日期后新单重审路径 | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |
| E2E-FAILURE | E2E | R1端到端执行失败与恢复路径 | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |
| M32-SEP11-CURRENT-EXPLICIT | M32 | 两人固定9月11日当前口径 | observed | 固定两姓名+两日期9/11实际应用，名册1行/1人，EMP002试用主职任职中；EMP001未入在职口径。 | 待处置；不判缺陷 |
| M32-SEP10-HISTORICAL-EXPLICIT | M32 | 两人固定9月10日历史口径 | observed | 固定两姓名+两日期9/10实际应用，3任职行/2distinct人员；EMP001正式2历史主职行，EMP002试用1行。不可按行数计3人。 | 待处置；不判缺陷 |
| M32-SEP11-ALL-HISTORY | M32 | 再入职前全部任职历史 | observed | 两姓名历史任职表4行/2人；当前标识主职2行含离职结束行，实际在职主职1行。表无日期筛选，不充当历史快照。 | 待处置；不判缺陷 |
