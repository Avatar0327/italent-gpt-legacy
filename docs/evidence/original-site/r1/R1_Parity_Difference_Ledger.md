# R1三方差异与证据限制台账

## 同RUN续跑增量（优先于下方首轮历史）

DIFF-MAJOR-001：Major / NEED_OWNER_DECISION，原站管理员详情直接调动即生效；详见ALERT-MAJOR-001.md。P3仍遵守D1–D7，不计IMPLEMENTATION_DEFECT。现累计Major 1、Observation 8、Blocker/Minor 0；窄项MATCH仍1，完整模块0/4。ENV-02/03仅局部限制，正式页面继续。原站他人调动申请页延迟后已加载，不能将此前空白记为权限拒绝。

按唯一台账ID计数，ENV_BLOCKED/ROLE_BLOCKED仅计open；历史ENV-01已恢复另列。Observation为本轮8条登记（含1条已恢复环境记录）；4条纯观察未做确定差异分类。MATCH为矩阵一个窄项规则，不与3条组织重复计数。

已确认产品Blocker/Major/Minor均0；不代表未测范围没有缺陷。无已确认需求遗漏、设计遗漏、实现缺陷或需所有者变更决定。

| 编号 | 分类 / 状态 | 严重级别 | 事实与结论 | 反馈 |
|---|---|---|---|---|
| ENV-01 | ENV_BLOCKED / resolved | Observation | 输入回读及草稿隔离最初未确认。DOM快照未显示输入值，getAttribute及截图出现超时；后以只读DOM value回读成功，双标签草稿内容相等。 已恢复，本窗口查询及草稿隔离通过。不归咎其他窗口，不限制项目并发。 | 证据操作恢复记录；无需P2/P3修改 |
| ENV-02 | ENV_BLOCKED / open | Observation | 截图捕获超时。组织草稿及M19/M48页面截图出现Page.captureScreenshot timeout；仅初始组织查询截图成功。 结构化页面证据可用，但重要写入用例截图仍缺，不能宣称证据完整。 | 浏览器能力处理；P3/P4保留图像证据缺口 |
| ENV-03 | ENV_BLOCKED / open | Observation | 正式组织模板下载被Chromium阻止。组织→更多操作→导入组织→下载模板；等待download超时，iframe显示This page has been blocked by Chromium，无文件路径。 已停止后续原站写入和扩量；不绕过平台限制，不猜模板，不调用隐藏接口。三条已创建组织保留；5–10条门槛未达到。 | 需处理正式下载限制，再按现有授权恢复；不要求改变D1–D7或新增真实账号。 |
| ROLE-01 | ROLE_BLOCKED / open | Observation | 独立员工、两方审批及HR角色验收前置未齐。仅现有管理入口会话ORIGIN-ADMIN-01，两个标签共用该会话；没有验证独立员工/调出审批/调入审批身份。 管理员自助页面不能代普通员工，管理员不得自审代两方确认；P4多角色人工验收阻塞。 | P4使用现有独立授权测试身份逐角色验收；不新增真实访问者或改变账号权限。 |
| OBS-01 | 未判定（仅观察） / observed_not_dispositioned | Observation | 组织两入口表单和确认方式不同。普通新建显示设立日期、大类/多维组织等，部门行政上级空值必填；新建下级显示生效日期并二次确认新增对象。 需求已有组织时态和入口要求；此次仅补页面及当天成功证据，未确认需求/设计遗漏。不能外推根机构规则。 | P2保留入口/组织类型区分；P3复核表单映射时使用该证据，不直接改设计。 |
| OBS-02 | 未判定（仅观察） / observed_not_dispositioned | Observation | 审批管理文案不等于D7调动行为。源管理页列出转交/撤销/一键审批/流程干预说明。未对本轮业务单执行。 P2通用管理能力与D7固定不同双审批并存；P3有D7_PROTECTED。没有足够源执行证据将其定为有意差异或冲突。 | P2/P3保持D7边界；P4区分通用流程与调动。 |
| OBS-03 | 未判定（仅观察） / observed_not_dispositioned | Observation | 管理会话自助入口含他人调动。人事申请可见本人/他人调动、离职、新增兼职及三类状态列。 不代表普通员工有他人办理权限，未确认越权或需求缺陷。 | P4补独立员工与管理员逐字段/逐动作差异。 |
| OBS-04 | 未判定（仅观察） / observed_not_dispositioned | Observation | 报表任职粒度与本轮组织可选结果。目录区分当前最新任职、历史所有任职、指定时点；详情多状态/时态列；本轮ORG_001出现在部门选择器，但已选仍0，未应用筛选。 源任职行不能当人头；P2 workforce按personId去重。二者尚未取得同一批员工数值对照，不能认定统计一致或不一致。300条分页只是既有报表控件，不是本轮批量测试。 | P3保留粒度/当前版本/历史快照口径；P4以合成员工、任职、离职和历史日期手算核对。 |

## 证据和映射

- ENV-01：需求BASE-04,F-SPEC-08；任务P3-R1-02；[M01-draft-isolation-recovered.json](R1-ORIGIN-20260910-100019/M01/M01-draft-isolation-recovered.json)
- ENV-02：需求M01-LIMIT-01,M19-LIMIT-01,M48-LIMIT-01,M32-LIMIT-01；任务P3-R1-02,P3-R1-03,P3-R1-05,P3-R1-06,P3-R1-07,P3-R1-11；[Browser_Concurrency_Check.md](Browser_Concurrency_Check.md), [M01-query.jpg](R1-ORIGIN-20260910-100019/M01/M01-query.jpg)
- ENV-03：需求F-SPEC-07,BP-F-REQ-12,M32-SPEC-05；任务P3-R1-02,P3-R1-05,P3-R1-06,P3-R1-07,P3-R1-11；[M01-template-blocked.json](R1-ORIGIN-20260910-100019/M01/M01-template-blocked.json)
- ROLE-01：需求D3,D4,D5,D7,M48-SPEC-01,M48-SPEC-02,M32-SPEC-03；任务P3-R1-03,P3-R1-05,P3-R1-11；[Browser_Concurrency_Check.md](Browser_Concurrency_Check.md), [M48-application-header.json](R1-ORIGIN-20260910-100019/M48/M48-application-header.json)
- OBS-01：需求BP-F-REQ-10,F-SPEC-08；任务P3-R1-02；[M01-ORG-001-parent-required.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-001-parent-required.json), [M01-ORG-003-readback.json](R1-ORIGIN-20260910-100019/M01/M01-ORG-003-readback.json)
- OBS-02：需求D7,M19-SPEC-02；任务P3-R1-03；[M19-query.json](R1-ORIGIN-20260910-100019/M19/M19-query.json)
- OBS-03：需求M48-SPEC-01,M48-SPEC-02,M48-SPEC-03；任务P3-R1-05；[M48-application-header.json](R1-ORIGIN-20260910-100019/M48/M48-application-header.json)
- OBS-04：需求M32-SPEC-01,M32-SPEC-02,M32-SPEC-03,M32-SPEC-04；任务P3-R1-06,P3-R1-07；[M32-catalog.json](R1-ORIGIN-20260910-100019/M32/M32-catalog.json), [M32-detail-controls.json](R1-ORIGIN-20260910-100019/M32/M32-detail-controls.json), [M32-own-org-selection.json](R1-ORIGIN-20260910-100019/M32/M32-own-org-selection.json)
