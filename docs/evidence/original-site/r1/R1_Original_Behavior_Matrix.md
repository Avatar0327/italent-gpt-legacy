# R1原站行为矩阵

RUN_ID：R1-ORIGIN-20260910-100019。P2：e15237281ff19f04f08a354fd9455c518b24ae47。P3结束对照快照：25eff27ea5b9320a7dfa5c2df7287d760c8d2688。

observed是局部事实；MATCH仅窄项；not_executed绝非验证通过；按模块完整范围完成计0/4。JSON保存每个重要用例的时间、角色、输入、步骤、状态、ID、证据、重现边界及三方映射。

| 用例 | 模块 / 内容 | 实际原站结果 | 批准需求 | P2设计 / P3用例 | 判定 |
|---|---|---|---|---|---|
| M01-ORG-001 | M01 / 合成组织保存及完整名称重读 | 保存后完整名称查询找到稳定UUID d1d541ab-92f9-4fce-80c6-aa5687433175；启用日期2026-09-10；父级为测试租户根 | BP-F-REQ-01,BP-F-REQ-10,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01 | 待完整三方判定（仅观察） |
| M01-ORG-002 | M01 / 合成组织保存及完整名称重读 | 保存后完整名称查询找到稳定UUID db7df096-624b-4d1e-ab4e-0552a56f052c；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | BP-F-REQ-01,BP-F-REQ-10,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01 | 待完整三方判定（仅观察） |
| M01-ORG-003 | M01 / 合成组织保存及完整名称重读 | 保存后完整名称查询找到稳定UUID a7b55bd7-0ef2-44a0-9d29-6259fe053da3；启用日期2026-09-10；路径显示本轮ORG_001为行政父级 | BP-F-REQ-01,BP-F-REQ-10,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01 | 待完整三方判定（仅观察） |
| M01-PARITY-01 | M01 / 稳定标识与父子关系保存（窄项三方对照） | 原站三条组织保存后可按完整名称重读UUID，子组织路径保留本轮父级；P2要求稳定ID及父子关联；P3 r1-m01.ts的catalog/make/m01Write/m01Entity持久化并回读ID及parentId，catalog acceptance合成测试覆盖父子创建。仅此窄项一致。 | BP-F-REQ-01,BP-F-REQ-10,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01 | MATCH |
| M01-FIELD-01 | M01 / 普通新建行政上级空值校验 | 大类为部门且行政上级为空时，确定后显示必填，表单保留；补选父级后首条组织保存。不能外推为所有组织类型均禁止根节点。 | BP-F-REQ-10,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01 | 待完整三方判定（仅观察） |
| M01-AUDIT-01 | M01 / 新组织设立审计只读 | 组织操作记录保留设立事件、业务日期2026-09-10、操作时间2026-09-10 18:27:04及本会话操作人；只证明该次设立审计，不证明历史不可改或失败原子性。 | BP-F-REQ-10,F-SPEC-08,BASE-04 | R1_P2_M01_Data_History.md / P3-M01-01 | 待完整三方判定（仅观察） |
| M01-IMPORT-01 | M01 / 正式组织导入模板下载 | 正式菜单下载模板后download等待超时，主iframe显示This page has been blocked by Chromium；无下载文件，无导入执行。 | BP-F-REQ-10,F-SPEC-07 | R1_P2_M01_Data_History.md / P3-M01-08,P3-M01-09 | ENV_BLOCKED |
| M19-QUERY-01 | M19 / 审批本轮标题筛选及管理说明 | 标题前缀与审批中条件下空集；页面展示催办/转交/撤销/一键审批及流程干预说明，摘要与审批状态列可见。未执行管理动作，不能据此覆盖D7。 | M19-SPEC-01,M19-SPEC-02,M19-SPEC-04,D7 | R1_P2_M19_Workflow_Transactions.md / P3-M19-03,P3-M19-04,P3-M19-07 | 待完整三方判定（仅观察） |
| M48-ENTRY-01 | M48 / 原管理会话下的人事申请入口 | 存在本人/他人调动、离职和新增兼职申请入口，任职/人员/审批状态分列。此为原管理会话，非独立员工；未打开或办理既有人员申请。 | M48-SPEC-01,M48-SPEC-02,M48-SPEC-03,BP-I-REQ-01 | R1_P2_M48_Authorization_Consumers.md / P3-M48-01,P3-M48-02,P3-M48-03 | ROLE_BLOCKED |
| M32-CATALOG-01 | M32 / 报表目录口径文案 | 目录分别描述最新一条任职、全部历史任职含兼职、指定时点在职；部分报表标示异步且需运行更新。目录文案不是数值口径实测。 | M32-SPEC-01,M32-SPEC-02,M32-SPEC-04,BP-I-REQ-02 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-02,P3-M32-04 | 待完整三方判定（仅观察） |
| M32-INPUT-01 | M32 / 姓名选择器前缀回读与空候选 | input.value确认本轮前缀，人员候选为空，选择器取消；原报表380条属于既有数据，非本轮批量。 | M32-SPEC-01,M32-SPEC-03 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-07 | 待完整三方判定（仅观察） |
| M32-ORG-01 | M32 / 新组织进入报表部门选择器 | 本轮ORG_001在部门搜索结果中可见；点击后已选组织仍0，取消选择器。未应用组织筛选，未取得空报表0行，不能称对账通过。 | M32-SPEC-01,M32-SPEC-03,F-SPEC-08 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-07 | 待完整三方判定（仅观察） |
| M01-PENDING-ORG-LIFECYCLE | M01 / 组织编辑、更名、停用与在用保护 | 未执行，不以计划预期充当实际结果 | F-SPEC-08,BP-F-REQ-01 | R1_P2_M01_Data_History.md / P3-M01-01,P3-M01-12 | ENV_BLOCKED |
| M01-PENDING-ORG-UNIQUE | M01 / 同父重名、不同父重名及编码重复 | 未执行，不以计划预期充当实际结果 | F-SPEC-01,F-SPEC-08,BP-F-REQ-01 | R1_P2_M01_Data_History.md / P3-M01-01 | ENV_BLOCKED |
| M01-PENDING-POSITION | M01 / 岗位新增、编辑、停用及上下级 | 未执行，不以计划预期充当实际结果 | BP-F-REQ-11,F-SPEC-01,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-01,P3-M01-12 | ENV_BLOCKED |
| M01-PENDING-EMP-CREATE | M01 / 员工新增及三入口模板 | 未执行，不以计划预期充当实际结果 | BP-F-REQ-12,F-SPEC-07 | R1_P2_M01_Data_History.md / P3-M01-09 | ENV_BLOCKED |
| M01-PENDING-EMP-IMPORT | M01 / 员工正式导入5–10、30–50、100–500 | 未执行，不以计划预期充当实际结果 | F-SPEC-07,BP-F-REQ-12 | R1_P2_M01_Data_History.md / P3-M01-08,P3-M01-09 | ENV_BLOCKED |
| M01-PENDING-ASSIGN | M01 / 主职、兼职、多任职及占用 | 未执行，不以计划预期充当实际结果 | F-SPEC-05,BP-F-REQ-06 | R1_P2_M01_Data_History.md / P3-M01-03 | ROLE_BLOCKED |
| M01-PENDING-JOIN-REGULARIZE | M01 / 入职、转正流程 | 未执行，不以计划预期充当实际结果 | BP-F-REQ-12,F-SPEC-07 | R1_P2_M01_Data_History.md / P3-M01-09,P3-M19-01 | ROLE_BLOCKED |
| M01-PENDING-TRANSFER | M01 / 调动计划日、实际生效和日期重审 | 未执行，不以计划预期充当实际结果 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03 | R1_P2_M01_Data_History.md / P3-M01-04,P3-M01-05,P3-M01-06 | ROLE_BLOCKED |
| M01-PENDING-EXIT-REHIRE | M01 / 离职、再入职与身份连续性 | 未执行，不以计划预期充当实际结果 | F-SPEC-04,F-SPEC-05 | R1_P2_M01_Data_History.md / P3-M01-02,P3-M01-10 | ROLE_BLOCKED |
| M01-PENDING-LEGAL | M01 / 法人组织归属与空范围 | 未执行，不以计划预期充当实际结果 | F-SPEC-06 | R1_P2_M01_Data_History.md / P3-M01-07 | ENV_BLOCKED |
| M01-PENDING-FIELDS | M01 / 必填、长度、格式、空值及重复值 | 未执行，不以计划预期充当实际结果 | F-SPEC-01,F-SPEC-07 | R1_P2_M01_Data_History.md / P3-M01-08,P3-M01-09 | ENV_BLOCKED |
| M01-PENDING-HISTORY-ATTACH | M01 / 附件、历史版本、原单与审计 | 未执行，不以计划预期充当实际结果 | BASE-03,BASE-04,F-SPEC-08 | R1_P2_M01_Data_History.md / P3-M01-12,P3-INT-05 | ENV_BLOCKED |
| M01-PENDING-CONCURRENCY | M01 / 并发修改和重复提交 | 未执行，不以计划预期充当实际结果 | F-SPEC-02,BASE-04 | R1_P2_M01_Data_History.md / P3-M01-04,P3-M01-12 | ENV_BLOCKED |
| M19-PENDING-SEQUENTIAL | M19 / 顺序审批、两方独立与禁止自审 | 未执行，不以计划预期充当实际结果 | D3,D4,D5,D7,M19-SPEC-02 | R1_P2_M19_Workflow_Transactions.md / P3-M19-01,P3-M19-02 | ROLE_BLOCKED |
| M19-PENDING-DELEGATION | M19 / 管理员委托、接受与撤销 | 未执行，不以计划预期充当实际结果 | M19-SPEC-03 | R1_P2_M19_Workflow_Transactions.md / P3-M19-06 | ROLE_BLOCKED |
| M19-PENDING-REJECT | M19 / 同意、驳回和驳回原因 | 未执行，不以计划预期充当实际结果 | D6,M19-SPEC-02 | R1_P2_M19_Workflow_Transactions.md / P3-M19-02 | ROLE_BLOCKED |
| M19-PENDING-WITHDRAW | M19 / 撤回、重提和修改日期重审 | 未执行，不以计划预期充当实际结果 | D2,D6,F-SPEC-03 | R1_P2_M19_Workflow_Transactions.md / P3-M19-04,P3-M01-05 | ROLE_BLOCKED |
| M19-PENDING-EFFECT | M19 / 审批完成与HR执行生效分离 | 未执行，不以计划预期充当实际结果 | D1,D2,M19-SPEC-04 | R1_P2_M19_Workflow_Transactions.md / P3-M19-07,P3-M01-04 | ROLE_BLOCKED |
| M19-PENDING-RECOVERY | M19 / 重复点击、超时、执行失败恢复 | 未执行，不以计划预期充当实际结果 | D1,F-SPEC-02,M19-SPEC-04 | R1_P2_M19_Workflow_Transactions.md / P3-M19-05,P3-M19-07 | ROLE_BLOCKED |
| M19-PENDING-SUMMARY | M19 / 摘要字段、职级变化与原新单追溯 | 未执行，不以计划预期充当实际结果 | D5,D6,M19-SPEC-02 | R1_P2_M19_Workflow_Transactions.md / P3-M19-02,P3-M19-07 | ROLE_BLOCKED |
| M48-PENDING-PROFILE | M48 / 本人资料可见和可改字段 | 未执行，不以计划预期充当实际结果 | M48-SPEC-01,M48-SPEC-02 | R1_P2_M48_Authorization_Consumers.md / P3-M48-01,P3-M48-02 | ROLE_BLOCKED |
| M48-PENDING-ATTACH | M48 / 自助附件上传下载替换 | 未执行，不以计划预期充当实际结果 | M48-SPEC-02,BASE-03 | R1_P2_M48_Authorization_Consumers.md / P3-M48-02,P3-INT-05 | ROLE_BLOCKED |
| M48-PENDING-APPLICATION | M48 / 自助申请进度历史撤回驳回重提 | 未执行，不以计划预期充当实际结果 | M48-SPEC-03,M48-SPEC-04,BP-I-REQ-01 | R1_P2_M48_Authorization_Consumers.md / P3-M48-03,P3-M48-05,P3-M48-07 | ROLE_BLOCKED |
| M48-PENDING-BOUNDARY | M48 / 本人/他人、脱敏及管理员差异 | 未执行，不以计划预期充当实际结果 | M48-SPEC-01,M48-SPEC-02 | R1_P2_M48_Authorization_Consumers.md / P3-M48-01,P3-M48-02,P3-M48-06 | ROLE_BLOCKED |
| M48-PENDING-SEVEN | M48 / 七入口可用、无权、未配置和异常 | 未执行，不以计划预期充当实际结果 | M48-SPEC-03,M48-SPEC-04 | R1_P2_M48_Authorization_Consumers.md / P3-M48-04,P3-M48-05,P3-M48-07 | ROLE_BLOCKED |
| M32-PENDING-ORACLE | M32 / 指标口径与明细一致性 | 未执行，不以计划预期充当实际结果 | M32-SPEC-01,M32-SPEC-02,BP-I-REQ-02 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-02 | ENV_BLOCKED |
| M32-PENDING-TIME | M32 / 组织日期筛选、当前值与历史快照 | 未执行，不以计划预期充当实际结果 | M32-SPEC-03,M32-SPEC-04 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-04 | ENV_BLOCKED |
| M32-PENDING-PAGING | M32 / 分页排序及100–500行显示 | 未执行，不以计划预期充当实际结果 | M32-SPEC-03,M32-SPEC-05 | R1_P2_M32_Reports_Jobs.md / P3-M32-06,P3-M32-07 | ENV_BLOCKED |
| M32-PENDING-EXPORT | M32 / 导出内容、空导出与大文件 | 未执行，不以计划预期充当实际结果 | M32-SPEC-05 | R1_P2_M32_Reports_Jobs.md / P3-M32-06,P3-M32-08 | ENV_BLOCKED |
| M32-PENDING-SUBSCRIBE | M32 / 订阅、权限过滤与投递 | 未执行，不以计划预期充当实际结果 | M32-SPEC-06 | R1_P2_M32_Reports_Jobs.md / P3-M32-09 | ROLE_BLOCKED |
| M32-PENDING-DATA-EDGE | M32 / 空/重复/失效组织/离职/跨组织边界 | 未执行，不以计划预期充当实际结果 | M32-SPEC-01,M32-SPEC-03 | R1_P2_M32_Reports_Jobs.md / P3-M32-01,P3-M32-07 | ROLE_BLOCKED |
| E2E-SUCCESS | E2E / R1端到端成功路径 | 整链未执行；首段组织创建不得折算成链通过 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03,M48-SPEC-03,M32-SPEC-01 | R1_P2_Approved_Acceptance_Trace.md / P3-XMOD-01 | ROLE_BLOCKED |
| E2E-REJECT | E2E / R1端到端驳回路径 | 整链未执行；首段组织创建不得折算成链通过 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03,M48-SPEC-03,M32-SPEC-01 | R1_P2_Approved_Acceptance_Trace.md / P3-XMOD-01 | ROLE_BLOCKED |
| E2E-WITHDRAW | E2E / R1端到端撤回路径 | 整链未执行；首段组织创建不得折算成链通过 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03,M48-SPEC-03,M32-SPEC-01 | R1_P2_Approved_Acceptance_Trace.md / P3-XMOD-01 | ROLE_BLOCKED |
| E2E-REDATE | E2E / R1端到端改日期后新单重审路径 | 整链未执行；首段组织创建不得折算成链通过 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03,M48-SPEC-03,M32-SPEC-01 | R1_P2_Approved_Acceptance_Trace.md / P3-XMOD-01 | ROLE_BLOCKED |
| E2E-FAILURE | E2E / R1端到端执行失败与恢复路径 | 整链未执行；首段组织创建不得折算成链通过 | D1,D2,D3,D4,D5,D6,D7,F-SPEC-02,F-SPEC-03,M48-SPEC-03,M32-SPEC-01 | R1_P2_Approved_Acceptance_Trace.md / P3-XMOD-01 | ROLE_BLOCKED |

实际证据：
- M01-ORG-001：[M01-ORG-001-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-readback.json)
- M01-ORG-002：[M01-ORG-002-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-002-readback.json)
- M01-ORG-003：[M01-ORG-003-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-readback.json)
- M01-PARITY-01：[M01-ORG-003-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-readback.json)
- M01-FIELD-01：[M01-ORG-001-parent-required.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-parent-required.json)
- M01-AUDIT-01：[M01-ORG-001-audit.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-audit.json)
- M01-IMPORT-01：[M01-template-blocked.json](R1-ORIGIN-20260910-100019/M01/M01-template-blocked.json)
- M19-QUERY-01：[M19-query.json](R1-ORIGIN-20260910-100019/M19/M19-query.json)
- M48-ENTRY-01：[M48-application-header.json](R1-ORIGIN-20260910-100019/M48/M48-application-header.json)
- M32-CATALOG-01：[M32-catalog.json](R1-ORIGIN-20260910-100019/M32/M32-catalog.json)
- M32-INPUT-01：[M32-input-readback.json](R1-ORIGIN-20260910-100019/M32/M32-input-readback.json)
- M32-ORG-01：[M32-own-org-selection.json](R1-ORIGIN-20260910-100019/M32/M32-own-org-selection.json)
