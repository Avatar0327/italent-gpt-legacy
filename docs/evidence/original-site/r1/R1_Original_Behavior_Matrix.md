# R1 原站行为矩阵（同RUN续跑）

RUN_ID：R1-ORIGIN-20260910-100019。完整验证/批量/P3完整对照均0/4。矩阵66项：30项窄范围已观察（含失败和限制，不等于通过）、18组合部分观察、18未执行。MATCH3仅组织ID稳定、当前人数粒度、退出次日边界；后两项P3静态对照，不等于动态复刻验收。10个主动创建对象、2员工，30–50/100–500未执行。

实际输入、记录ID、角色、时间精度、设计SHA和P3映射详见JSON及证据。D1–D7不变，P1不重开；原站差异不自动覆盖批准目标。多条用例关联同一Major仅计台账ID一次。

所有者决定：直接调动为 INTENTIONAL_DIFFERENCE，历史 Major 1、待决 Major 0；独立申请/撤回观察不扩大为批准。

| 用例 | 模块 | 执行状态 | 实际结果 | 分类 | 证据 |
|---|---|---|---|---|---|
| M32-ORG-SELECT-LIMIT | M32 | observed | ORG002经候选文字/完整行/CUA点击仍已选0，已取消；当前2员工结果没有应用组织条件，不能判组织过滤缺陷。 | ENV_BLOCKED | [M32-org-filter.json](R1-ORIGIN-20260910-100019/M32/M32-org-filter.json)；[M32-org-selector-limit.json](R1-ORIGIN-20260910-100019/M32/M32-org-selector-limit.json) |
| M01-ORG-003-EDIT-STOP | M01 | observed | 同UUID备注持久化，名称/代码/归属/日期不变；操作记录仅设立18:34:09，变更记录仅1版本，编辑审计未取得。停用包含全体职位人员迁移，未核完整影响清单而取消，未实际停用。 | 待判定 | [M01-ORG-003-edit-presubmit.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-edit-presubmit.json)；[M01-ORG-003-edit-result.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-edit-result.json)；[M01-ORG-003-edit-history.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-edit-history.json)；[M01-ORG-003-stop-preview.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-stop-preview.json) |
| M32-TWO-EMP-001 | M32 | observed | 仅EMP001+EMP002及今天入职，正式1、试用1、合计2，各人数1；未来离职和撤回转正申请未提前改变当前人数。非分页或批量通过。 | 待判定 | [M32-two-employees.json](R1-ORIGIN-20260910-100019/M32/M32-two-employees.json) |
| M19-REG-002 | M19 | observed | 转正业务9737bceb/流程fb06f86c已审批中后撤回；审计21:57提交/22:03撤回，同实例申请人开始节点。独立审批、重提/改期未执行，员工仍试用；摘要离职字段错位。 | 待判定 | [M01-REG-002-presubmit.json](R1-ORIGIN-20260910-100019/M01/M01-REG-002-presubmit.json)；[M19-REG-002-row.json](R1-ORIGIN-20260910-100019/M19/M19-REG-002-row.json)；[M19-REG-002-detail.json](R1-ORIGIN-20260910-100019/M19/M19-REG-002-detail.json)；[M19-REG-002-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-REG-002-recall-audit.json) |
| M01-EMP-002 | M01 | observed | 第二员工创建成功66ea978b；试用期限/预计结束必填。入职9/1早于本轮组织9/10被拒，不改组织历史；改9/10后试用结束10/9。日期重置邮箱工号已纠正。 | 待判定 | [M01-EMP-002-readback.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-readback.json)；[M01-EMP-002-probation-validation.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-probation-validation.json)；[M01-EMP-002-org-date-validation.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-org-date-validation.json)；[M01-EMP-002-corrected.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-corrected.json)；[M01-EMP-002-probation-entry.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-probation-entry.json) |
| M19-REQUEST-001 | M19 | observed | 提交后审批中；开始→直接上级→HR访谈→结束，未由管理员代审 | 待判定 | [M19-TRANSFER-REQUEST-001-presubmit.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-presubmit.json)；[M19-TRANSFER-REQUEST-001-detail.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-detail.json) |
| M19-RECALL-001 | M19 | observed | 源撤回同UUID返回开始；重提/改期/新原单关系未执行 | 待判定 | [M19-TRANSFER-REQUEST-001-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-recall-audit.json) |
| M48-ADMIN-STATE-001 | M48 | observed | 管理员能看到本轮申请待处理；非独立员工视角 | ROLE_BLOCKED | [M48-admin-own-request-state.json](R1-ORIGIN-20260910-100019/M48/M48-admin-own-request-state.json) |
| M32-OWN-ORACLE-001 | M32 | observed | 1人、2历史任职、1当前主职，当前花名册人数1。与已批在职人数distinct personId及P3静态每人员一行窄项一致；不含动态复刻验收 后续扩为2名本轮员工，正式1/试用1，仍按同一窄项人数规则计一次MATCH。 | MATCH | [M32-own-employee-history.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-history.json)；[M32-own-employee-current.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-current.json)；[M32-two-employees.json](R1-ORIGIN-20260910-100019/M32/M32-two-employees.json) |
| M32-DATE-EMPTY-001 | M32 | observed | 明天空数据、今天恢复本轮1人，不代历史快照 | 待判定 | [M32-date-empty.json](R1-ORIGIN-20260910-100019/M32/M32-date-empty.json) |
| M32-EXPORT-001 | M32 | observed | Chromium blocked，未取得文件，未绕过 | ENV_BLOCKED | [M32-own-employee-history.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-history.json) |
| M32-SUB-DRAFT-001 | M32 | observed | 观察权限/快照选项，取消，无保存无发送 | 待判定 | [M32-subscription-draft.json](R1-ORIGIN-20260910-100019/M32/M32-subscription-draft.json) |
| M01-EXIT-001 | M01 | observed | 最后工作日9/10→离职任职9/11未来生效，当前仍正式且报表1人；与P1/P2次日边界和P3 exitExecute日期校验静态窄项一致；未执行次日HR/自动作业，未再入职 | MATCH | [M01-EXIT-001-presubmit.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-presubmit.json)；[M01-EXIT-001-warning.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-warning.json)；[M01-EXIT-001-history.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-history.json)；[M01-EXIT-001-ID-report.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-ID-report.json) |
| M01-JOB-001 | M01 | observed | ORG_002下保存JOB_001，列表精确重读1条，在岗0兼职0 | 待判定 | [M01-continuation-smoke.json](R1-ORIGIN-20260910-100019/M01/M01-continuation-smoke.json) |
| M01-JOB-002 | M01 | observed | 空名称/所属组织提交被必填拒绝；补齐ORG_003及JOB_002后保存并精确回读 | 待判定 | [M01-JOB-002.json](R1-ORIGIN-20260910-100019/M01/M01-JOB-002.json) |
| M01-EMP-001 | M01 | observed | 草稿去除默认既有经理/公司，邀请否、身份证号/手机空，邮箱必填拒绝后补虚构邮箱保存，在职列表唯一结果 | 待判定 | [M01-EMP-001.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-001.json) |
| M01-EMP-001-ASSIGNMENT | M01 | observed | 正式/主职/生效中；入职-新增入职；今日开始，经理为空 | 待判定 | [M01-EMP-001-assignment.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-001-assignment.json) |
| M01-TRANSFER-001 | M01 | observed | ORG_002/JOB_001至ORG_003/JOB_002今日直接调动保存生效，原入职历史保留；本次UI未两级审批/单独HR执行 | INTENTIONAL_DIFFERENCE | [M01-TRANSFER-001.json](R1-ORIGIN-20260910-100019/M01/M01-TRANSFER-001.json)；[Owner_Decision_DIFF_MAJOR_001_20260910.json](Owner_Decision_DIFF_MAJOR_001_20260910.json) |
| M01-ORG-001 | M01 | observed | 保存后完整名称查询找到稳定UUID d1d541ab-92f9-4fce-80c6-aa5687433175；启用日期2026-09-10；父级为测试租户根 | 待判定 | [M01-ORG-001-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-readback.json) |
| M01-ORG-002 | M01 | observed | 保存后完整名称查询找到稳定UUID db7df096-624b-4d1e-ab4e-0552a56f052c；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | 待判定 | [M01-ORG-002-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-002-readback.json) |
| M01-ORG-003 | M01 | observed | 保存后完整名称查询找到稳定UUID a7b55bd7-0ef2-44a0-9d29-6259fe053da3；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | 待判定 | [M01-ORG-003-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-readback.json) |
| M01-PARITY-01 | M01 | observed | 原站三条组织保存后可按完整名称重读UUID，子组织路径保留本轮父级；P2要求稳定ID及父子关联；P3 r1-m01.ts的catalog/make/m01Write/m01Entity持久化并回读ID及parentId，catalog acceptance合成测试覆盖父子创建。仅此窄项一致。 | MATCH | [M01-ORG-003-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-readback.json) |
| M01-FIELD-01 | M01 | observed | 大类为部门且行政上级为空时，确定后显示必填，表单保留；补选父级后首条组织保存。不能外推为所有组织类型均禁止根节点。 | 待判定 | [M01-ORG-001-parent-required.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-parent-required.json) |
| M01-AUDIT-01 | M01 | observed | 组织操作记录保留设立事件、业务日期2026-09-10、操作时间2026-09-10 18:27:04及本会话操作人；只证明该次设立审计，不证明历史不可改或失败原子性。 | 待判定 | [M01-ORG-001-audit.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-audit.json) |
| M01-IMPORT-01 | M01 | observed | 正式菜单下载模板后download等待超时，主iframe显示This page has been blocked by Chromium；无下载文件，无导入执行。 | ENV_BLOCKED | [M01-template-blocked.json](R1-ORIGIN-20260910-100019/M01/M01-template-blocked.json) |
| M19-QUERY-01 | M19 | observed | 标题前缀与审批中条件下空集；页面展示催办/转交/撤销/一键审批及流程干预说明，摘要与审批状态列可见。未执行管理动作，不能据此覆盖D7。 | 待判定 | [M19-query.json](R1-ORIGIN-20260910-100019/M19/M19-query.json) |
| M48-ENTRY-01 | M48 | observed | 存在本人/他人调动、离职和新增兼职申请入口，任职/人员/审批状态分列。此为原管理会话，非独立员工；未打开或办理既有人员申请。 | ROLE_BLOCKED | [M48-application-header.json](R1-ORIGIN-20260910-100019/M48/M48-application-header.json) |
| M32-CATALOG-01 | M32 | observed | 目录分别描述最新一条任职、全部历史任职含兼职、指定时点在职；部分报表标示异步且需运行更新。目录文案不是数值口径实测。 | 待判定 | [M32-catalog.json](R1-ORIGIN-20260910-100019/M32/M32-catalog.json) |
| M32-INPUT-01 | M32 | observed | input.value确认本轮前缀，人员候选为空，选择器取消；原报表380条属于既有数据，非本轮批量。 | 待判定 | [M32-input-readback.json](R1-ORIGIN-20260910-100019/M32/M32-input-readback.json) |
| M32-ORG-01 | M32 | observed | 本轮ORG_001在部门搜索结果中可见；点击后已选组织仍0，取消选择器。未应用组织筛选，未取得空报表0行，不能称对账通过。 | 待判定 | [M32-own-org-selection.json](R1-ORIGIN-20260910-100019/M32/M32-own-org-selection.json) |
| M01-PENDING-ORG-LIFECYCLE | M01 | partially_observed | 新增三组织、ORG003备注编辑已验；停用预览含整体迁移，未执行停用/迁移 | 待判定 | [M01-ORG-003-edit-result.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-edit-result.json)；[M01-ORG-003-stop-preview.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-stop-preview.json) |
| M01-PENDING-ORG-UNIQUE | M01 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M01-PENDING-POSITION | M01 | partially_observed | 新增2职位、名称/组织必填已验；编辑/停用/唯一性未验 | 待判定 | [M01-continuation-smoke.json](R1-ORIGIN-20260910-100019/M01/M01-continuation-smoke.json)；[M01-JOB-002.json](R1-ORIGIN-20260910-100019/M01/M01-JOB-002.json) |
| M01-PENDING-EMP-CREATE | M01 | partially_observed | 创建1员工、邮箱必填、邀请账号否；其他创建入口未验 | 待判定 | [M01-EMP-001.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-001.json) |
| M01-PENDING-EMP-IMPORT | M01 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M01-PENDING-ASSIGN | M01 | partially_observed | 主职及调动2条任职历史已验；兼职/多任职未验 | ROLE_BLOCKED | [M01-EMP-001-assignment.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-001-assignment.json)；[M01-TRANSFER-001.json](R1-ORIGIN-20260910-100019/M01/M01-TRANSFER-001.json) |
| M01-PENDING-JOIN-REGULARIZE | M01 | partially_observed | 2员工分别正式/试用；转正正式申请已提交撤回，维护入口未保存；审批/实际生效未验 | ROLE_BLOCKED | [M01-EMP-002-readback.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-readback.json)；[M19-REG-002-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-REG-002-recall-audit.json) |
| M01-PENDING-TRANSFER | M01 | partially_observed | 直接调动生效；他人调动申请另行提交并撤回；独立两方审批未验 | ROLE_BLOCKED | [M01-TRANSFER-001.json](R1-ORIGIN-20260910-100019/M01/M01-TRANSFER-001.json)；[M19-TRANSFER-REQUEST-001-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-recall-audit.json) |
| M01-PENDING-EXIT-REHIRE | M01 | partially_observed | 最后工作日9/10→离职任职9/11未来生效，当前仍正式且报表1人；与P1/P2次日边界和P3 exitExecute日期校验静态窄项一致；未执行次日HR/自动作业，未再入职 | 待判定 | [M01-EXIT-001-presubmit.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-presubmit.json)；[M01-EXIT-001-warning.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-warning.json)；[M01-EXIT-001-history.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-history.json)；[M01-EXIT-001-ID-report.json](R1-ORIGIN-20260910-100019/M01/M01-EXIT-001-ID-report.json) |
| M01-PENDING-LEGAL | M01 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M01-PENDING-FIELDS | M01 | partially_observed | 职位/邮箱/试用期限/试用结束必填、入职早于组织生效被拒已验；未覆盖全字段、长度、格式、重复 | 待判定 | [M01-EMP-002-probation-validation.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-probation-validation.json)；[M01-EMP-002-org-date-validation.json](R1-ORIGIN-20260910-100019/M01/M01-EMP-002-org-date-validation.json) |
| M01-PENDING-HISTORY-ATTACH | M01 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M01-PENDING-CONCURRENCY | M01 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M19-PENDING-SEQUENTIAL | M19 | partially_observed | 原站路线开始→直接上级→HR访谈→结束；无独立两方审批实操 | ROLE_BLOCKED | [M19-TRANSFER-REQUEST-001-detail.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-detail.json) |
| M19-PENDING-DELEGATION | M19 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M19-PENDING-REJECT | M19 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M19-PENDING-WITHDRAW | M19 | partially_observed | 20:44提交/20:52撤回；同业务和流程UUID回到开始。未重提/改期 | ROLE_BLOCKED | [M19-TRANSFER-REQUEST-001-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-recall-audit.json) |
| M19-PENDING-EFFECT | M19 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M19-PENDING-RECOVERY | M19 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M19-PENDING-SUMMARY | M19 | partially_observed | 调动摘要含离职字段标签；敏感职级及独立角色可见性未验 | ROLE_BLOCKED | [M19-TRANSFER-REQUEST-001-detail.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-detail.json) |
| M48-PENDING-PROFILE | M48 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M48-PENDING-ATTACH | M48 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M48-PENDING-APPLICATION | M48 | partially_observed | 管理员申请人工作台显示本轮申请待处理；非独立员工验收 | ROLE_BLOCKED | [M48-admin-own-request-state.json](R1-ORIGIN-20260910-100019/M48/M48-admin-own-request-state.json) |
| M48-PENDING-BOUNDARY | M48 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M48-PENDING-SEVEN | M48 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| M32-PENDING-ORACLE | M32 | partially_observed | 独立手算1员工=当前花名册1人、任职历史2行、当前主职1；全指标及批量未验 | 待判定 | [M32-own-employee-history.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-history.json)；[M32-own-employee-current.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-current.json) |
| M32-PENDING-TIME | M32 | partially_observed | 入职日期明天空数据、今天1人；历史快照未验 | 待判定 | [M32-date-empty.json](R1-ORIGIN-20260910-100019/M32/M32-date-empty.json) |
| M32-PENDING-PAGING | M32 | not_executed | 未执行，不以计划预期充当实际结果 | ENV_BLOCKED |  |
| M32-PENDING-EXPORT | M32 | partially_observed | 本轮筛选结果正式下载被Chromium阻止；无文件，不绕过 | ENV_BLOCKED | [M32-own-employee-history.json](R1-ORIGIN-20260910-100019/M32/M32-own-employee-history.json) |
| M32-PENDING-SUBSCRIBE | M32 | partially_observed | 订阅草稿字段读取后取消；未创建订阅或推送 | ROLE_BLOCKED | [M32-subscription-draft.json](R1-ORIGIN-20260910-100019/M32/M32-subscription-draft.json) |
| M32-PENDING-DATA-EDGE | M32 | not_executed | 未执行，不以计划预期充当实际结果 | ROLE_BLOCKED |  |
| E2E-SUCCESS | E2E | partially_observed | 组织→职位→员工→直接调动→历史/报表局部链，不能替代双审批/执行HR/独立员工，完整未通过 | ROLE_BLOCKED | [M01-TRANSFER-001.json](R1-ORIGIN-20260910-100019/M01/M01-TRANSFER-001.json)；[M32-two-employees.json](R1-ORIGIN-20260910-100019/M32/M32-two-employees.json) |
| E2E-REJECT | E2E | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |  |
| E2E-WITHDRAW | E2E | partially_observed | 两张申请提交→审批中→申请人撤回→管理员工作台/报表未提前生效；新单重提和独立员工未验 | ROLE_BLOCKED | [M19-TRANSFER-REQUEST-001-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-TRANSFER-REQUEST-001-recall-audit.json)；[M19-REG-002-recall-audit.json](R1-ORIGIN-20260910-100019/M19/M19-REG-002-recall-audit.json)；[M32-two-employees.json](R1-ORIGIN-20260910-100019/M32/M32-two-employees.json) |
| E2E-REDATE | E2E | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |  |
| E2E-FAILURE | E2E | not_executed | 整链未执行；首段组织创建不得折算成链通过 | ROLE_BLOCKED |  |
