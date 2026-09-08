# 已有实现与产品需求对应

生成来源：`Scope_Register.json → p1Baseline / modules[].p1 / p1B`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：2026-09-08T17:44:36.829263+00:00。

对应当前源码静态核对；可复用是技术候选，不是当前测试或业务验收通过。历史测试只在原Verification标注的testedSourceCommit及适用范围有效，本轮未复跑。产品源码未修改。

| 需求 | 能力 | 处置 | 代码/证据 | 差异与限制 | 验收关联 |
|---|---|---|---|---|---|
| F01.1 | 组织树、同级重名/循环和停用保护 | 可复用 | lib/hris/model.ts；lib/hris/authorization.ts | 已有独立实现，组织字段必填与在用保护仍需规格评审 | UAT-01/02 |
| F01.2 | 岗位/职级目录及引用 | 待核验 | lib/hris/model.ts | 旧文档写编码/名称唯一，代码校验编码唯一；名称唯一性未获明确确认，不擅自新增限制 | UAT-03；重复编码与重复名称分别验收 |
| F01.3 | 员工字段与普通编辑保护 | 可复用 | lib/hris/model.ts；app/api/hris/route.ts | 新增试用、可空关联和自由文本回退为既有独立实现，待业务规格评审；不能视作原站字段规则 | UAT-04 |
| F01.4/F03 | D1–D7定日调动与两级审批 | 可复用 | lib/hris/personnel-transfer.ts；lib/hris/model.ts；app/api/hris/route.ts | 仅确认首包设计；当前静态对应，不宣称本轮回归或UAT已通过 | UAT-06/07/08/10 |
| F03.3 | 执行失败与事务回滚 | 需补齐 | app/api/hris/route.ts；tests/f01-f04-transfer-roles.test.mjs | 需求须区分业务校验失败持久留痕、事务失败整体回滚、结果不明先读取；额外失败日志持久化未获新授权，不新增实现 | UAT-08/12；D1异常契约 |
| F02 | 身份/当前范围/职级防盲审 | 可复用 | lib/hris/authorization.ts；lib/hris/repository.ts | D3–D5适用；其他五角色权限仍为既有独立设计候选，E2多人验证暂缓 | UAT-05/09 |
| F04 | 附件、当前权限与历史审计 | 待核验 | app/api/attachments/route.ts；app/api/history/route.ts；docs/delivery/F04_Closure_Verification.json | 历史R2替身证据，云端合成附件及跨角色实操未完成 | UAT-11/12 |
| F01–F04 UI | 按钮缺失反馈与入口修复 | 待核验 | docs/delivery/F01_F04_Entry_UI_Verification.json | v112有修复及渲染证据，用户复验尚缺；若复验失败才定位需修改产品项 | UAT-01–12的可达入口 |
| F01.4/F03 历史描述 | 终审即时调动/三类均1–5级 | 需修改 | docs/delivery/F01_F04_Requirements_Baseline.md | 修正文档当前口径；即时生效仅属转正/离职既有实现，调动固定两级且批准生效分离；不改产品代码 | 需求一致性审查 |
| M01 扩展 | 兼岗、法人、再入职、合同/编制联动 | 需补齐 | docs/P1_Source_Observations_20260907.md | 先补P1A/P1B，保留全量；不是本轮新增功能任务 | 待按完整M01规格定义 |
| F04.1 | 附件分页与物理清理 | 需补齐 | app/api/attachments/route.ts | 列表最多200条且无翻页游标；物理删除失败仅cleanupPending标记。先明确需求，不把当前限制当完整能力或本轮开发任务 | F04/UAT-11：超限、撤权、墓碑及清理状态；全量分页待规格 |
| BP-F-REQ-01 | 组织/岗位/职级/员工 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/model.ts；lib/hris/authorization.ts；app/api/hris/route.ts | F-SPEC-01仅岗位/职级名称；兼岗/再入职/法人不是普通员工编辑 | 已有关联在职员工/启用子组织或岗位的组织，申请停用应拒绝且原数据不变；相同组织名在同父节点拒绝；不同父节点按当前规则核对，不推广成全局唯一 |
| BP-F-REQ-02 | F03调动原单和执行记录 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/model.ts；tests/f01-f04-transfer-roles.test.mjs | D1–D7已确认；F-SPEC-02/03仅异常边界和关联宽度待审 | 批准后档案不变；北京时间生效日00:00前拒绝执行；业务校验失败保留原因及计划日；恢复后记实际时间。审计故障整个事务回滚并刷新核对；旧revision拒绝 |
| BP-F-REQ-03 | 项目人力（M20） | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Scope_Register.json | M20未独立实现；项目归属BP-F不等于可按任职调动替代 | 待取得项目与工时表单后才能定义工时重叠、合计、审批、薪资影响场景；当前不设虚构通过预期 |
| BP-C-REQ-01 | 干部任期/提名/任用 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/cadre-terms.ts；lib/hris/cadres.ts | 原站四状态干部身份不可用registered/ended一对一替代；委员会/任期算法/复杂任用类型未就绪 | 已有生效任期重叠时登记拒绝；已批准未生效调动不能核对任用；岗位不匹配拒绝；员工离职前不能登记离职原因结束任期 |
| BP-C-REQ-02 | 任职资格标准及认证 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/qualification.ts | 认证委员会、类别层级及有效期政策需原站与企业基线；现有整数尺度非原站标准 | 新标准版本不得覆盖旧认证依据；相同版本已有有效认证/待审申请时拒绝重复；不达目标或证据版本错误不能认证 |
| BP-C-REQ-03 | 360项目/关系/答卷/报告 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/feedback.ts；lib/hris/development.ts | 阈值/匿名性是独立策略待确认；提醒、题型、完整活动运营未覆盖 | 草稿后不能改名单；重复评估人+被评人拒绝；本人关系不匹配拒绝；同事/下属低于阈值返回suppressed与null均值，自评/上级阈值1；不把无响应记0 |
| BP-C-REQ-04 | 盘点/继任/标准模型 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Cadre_Learning_Source_Gaps.md；docs/delivery/Scope_Register.json | 当前仅重用已有范围描述；多维模型/健康度/测評题库及评分未可验收 | 后续评审必须证明正式绩效快照来源/版本；撤销或新版本不能静默覆盖旧九宫格；无绩效不自动补最低档 |
| BP-L-REQ-01 | 学习配置与实例 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/learning-plan-definitions.ts；lib/hris/learning-plan-model.ts | 自动循环不是已实现；共享管理员与可学范围、完成实例重开、跨轮更新待明确；当前main学习配置未含原站简介字段；既有learning-description隔离分支f5f5b1bd9014d4b6eeb6d32da0f03e34da3bced2保留未合并，不计main已实现 | 已定版配置直接改动拒绝；跨组织试卷/作业引用拒绝；新版本不自动改旧实例；取消/退出要求不伪造完成；固定模式起点按计划日期，非加入日 |
| BP-L-REQ-02 | 阶段窗口与任务放行 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/learning-plan-definitions.ts；lib/hris/learning-requirements.ts | 自然日含首日和顺序晚开启的原站精确算法尚未核实，当前策略需评审 | 有序阶段的考试/作业提交放行不等于通过；未完成必修不满足结项；晚核验不得伪造按期提交；无法完成的数量门槛配置拒绝 |
| BP-L-REQ-03 | 计划成绩 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/learning-grades.ts；lib/hris/learning-grade-evidence.ts | 缺失分母、精度、通过过滤及多审批人聚合为候选政策，原站选项存在不能证明算法完整一致 | 缺少有效成绩时pending与null，不能补0/100；按每次考试平均与每场最高平均给出不同期望；无成绩课程不能获得虚构权重成绩 |
| BP-L-REQ-04 | 学分、撤销、到期 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/learning-credits.ts | 折抵、企业到期算法、积分和自动发证尚未确认；不得将本项目整数单位当原站字段类型 | 同课程版本重复授予拒绝；允许循环重复的完整新轮且非旧成果复用才可新授；撤销不删除原记录；到期日当天仍有效 |
| BP-L-REQ-05 | AI陪练（M28） | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Scope_Register.json | 没有独立实现，不以现有学习考试代替 | 先明确评分输入和可复现版本，再制定正常/无音频/低置信度/人工复核场景；暂不能给出评分通过阈值 |
| BP-P-REQ-01 | 绩效周期/计划/结果 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/performance.ts；lib/hris/performance-availability.ts | 组织绩效、关系锁定、强制分布、申诉时间窗及多维流程未就绪 | 活动有效且员工在当前范围才能继续；待审调整阻断自评；发布不覆盖原结果；未经审核的更正不能成为正式结果 |
| BP-P-REQ-02 | 绩效等级与尺度 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/performance-ratings.ts | 原站连续区间说明与现实现允许空隙但发布拒绝存在差异；纯手工等级/系数及在途更新未实现 | 边界只可匹配一个等级；区间缺口不自动发布；新方案不替换旧活动；总分非百分制按活动范围校验 |
| BP-P-REQ-03 | 目标数量/权重检查与指标引用 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Performance_Source_Gaps.md；lib/hris/performance.ts | 小数权重/算术求和/完整模块权重与定量自动下发未覆盖 | 仅提示超出建议值不阻断通用合法目标；强制违反拒绝；指标改版不改旧目标快照；同一记录多次引用不能冒计多人 |
| BP-R-REQ-01 | 需求/招聘职位/候选人 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/recruitment.ts；lib/hris/recruitment-jobs.ts | 原站允许职位或人才库入口，当前必须有需求，无法覆盖独立人才库；外部来源/门户未实现 | 不同需求的职位版本不能关联；有候选引用的职位改版不能覆盖旧版；需求关闭不能遗留活动候选；邮件权限撤销后不能写邮箱 |
| BP-R-REQ-02 | 面试/评价/录用入职 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/recruitment.ts；lib/hris/recruitment-evaluations.ts | 面试日历/通知、电子签回执、Offer占编与跨法人/再入职接口未就绪 | 待进行排期阻断录用；未推荐推进不允许录用；未接受或尚未到入职日拒绝入职；重复入职不重复建员工或计数 |
| BP-R-REQ-03 | 推荐/校园/外推/AI/RPA周边 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Recruitment_Source_Gaps.md；docs/delivery/Scope_Register.json | 周边7组未独立实现，不能用核心招聘自动验收覆盖 | 待定义归因/去重/结算依据后制定重复推荐、撤回录用、跨来源冲突及重试场景；AI评分阈值不可编造 |
| BP-A-REQ-01 | 班次/打卡/补卡/请假 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/attendance.ts | 弹性/轮班/设备/加班调休未实现；分钟规则是本项目候选 | 跨班请假当前拒绝；已批准用量与待审批预留分开，超余额不能再申请；重复/反序打卡拒绝；修改后旧版本审批拒绝 |
| BP-A-REQ-02 | 结算期间与冻结版本 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/attendance-periods.ts；lib/hris/attendance-locks.ts | 原站冻结/发布/确认/封存为独立列，不能用当前两个状态冒充完整原站月报 | 有待审批/未覆盖时不能冻结；冻结阻止来源写；重新开放后工资待发布引用失效；重冻不覆盖旧快照 |
| BP-A-REQ-03 | 假期/调休结算 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Attendance_Source_Gaps.md | 企业参数、自动结转和申诉待决策/补证 | 必须先取得授予、折算单位、过期和跨年规则，再给出边界日与结转预期；现阶段不虚构额度公式 |
| BP-S-REQ-01 | 人工核定工资批次与工资条 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/payroll.ts；lib/hris/payroll-access.ts | 仅人工核定值，自动算薪/税社保/支付均未实现，不能以发布工资条冒称发薪 | 同员工同月非取消条目重复拒绝；贡献者即使移除所改条目仍不可复核；净额负数拒绝；发布前不能在本人自助看到工资条 |
| BP-S-REQ-02 | 冻结考勤引用/来源变化 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/payroll-attendance.ts | 没有自动由考勤计算工资公式；补差与重核策略需业务评审 | 来源开放/版本或时间变化后提交复核发布返回冲突；不能沿用旧复核；已发布后来源变化不静默改工资结果 |
| BP-S-REQ-03 | 薪资组/预算成本/凭证/福利/佣金 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Payroll_Source_Gaps.md；docs/delivery/Scope_Register.json | M09/M10/M33/M42无独立实现；原48组不删减 | 先明确各子模块来源、期间和对账基准，才能定义重算/冲销/重复任务/缺失科目等可执行预期 |
| BP-I-REQ-01 | 员工自助/统一待办 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | app/api/self-service/route.ts；lib/hris/work-inbox.ts | 日程/日报/完整OKR/消息发送未实现；独立M43任务不等于当前聚合待办 | 已取消任务不继续展示可办理；待审目标调整阻断自评入口；本人申诉已批准待发布应显示awaiting_publish；原模块撤权即拒绝直接URL办理 |
| BP-I-REQ-02 | 报表与指标分母 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/reports.ts；app/api/reports/route.ts | 设计器/大规模查询/历史组织快照未就绪；每数据集必须独立定义分母，不能统一套人员数 | 无字段权时表头/单元格不出现该字段；学习缺分保持null；绩效旧版本不重复计为当前；合同覆盖登记不能证明电子签法律有效或实际在岗；旧revision导出拒绝，审计失败不得返回CSV（本轮未执行导出） |
| BP-I-REQ-03 | 实名调查/问卷与360共用模板边界 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/surveys.ts；lib/hris/feedback.ts | 员工调查/北森问卷/问卷调查三组不合并，匿名、复杂题型、报告行动计划未完成 | 单选越界/缺题拒绝；撤回不计有效回应；未开放/超日期不能提交；实名不能在文案宣传匿名；360分组压制另按阈值 |
| BP-I-REQ-04 | 主数据同步契约预检 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | lib/hris/integration-preflight.ts | 鉴权、密钥托管、真实endpoint、调度、事务回执和队列均未实现；重试函数不是后台重试服务 | 相同eventId同内容为duplicate；内容不同conflict；缺前序gap；映射缺失/多义不生成可提交结论；ready不得宣称已更新员工 |
| BP-I-REQ-05 | 工作台/电子签/会议/文化/翻译等周边 | 待核验/可复用候选；差异需补齐，未授权本轮改产品 | docs/delivery/Integration_Source_Gaps.md；docs/delivery/Scope_Register.json | 周边多组只有入口；保留候选接口与证据不足，不能泛化当前自助实现 | 取得配置证据后再定义冲突、重复回执、撤销、时间窗口和访问边界；任何未探索动作不标成可用 |
| BP-L-REQ-06 | 独立考试与作业批阅 | 可复用候选/需补齐；未业务签署 | lib/hris/learning-homework.ts；lib/hris/learning-exam-definitions.ts | 填空/简答/排序、随机抽题、多级批阅、附件/AI批阅及外部通知尚未实现；原站可选题型不证明当前已支持 | 两种试卷题目结构必须且只能提供一种；已定版不可编辑；作业批阅旧submissionId拒绝，评分为空不补0；批阅后返回可重交且次数受限；人员异动/撤权后不能沿用旧任务授权 |
| BP-R-REQ-04 | 招聘创建请求恢复与内部接口 | 可复用候选/接口契约待评审 | app/api/recruitment/route.ts；lib/hris/http.ts | 不是原站API说明，不提供外部渠道幂等契约；通用版本冲突不等于所有命令自动幂等 | 网络结果未知后同键重试只返回原记录，不重复创建；修改命令仍用同键拒绝；撤权后原键也不能恢复越权记录；其他动作传创建键拒绝 |
| BP-C-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/qualifications/route.ts；app/api/cadres/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-L-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/learning-homework/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-P-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/performance/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-R-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/recruitment/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-A-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/attendance/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-S-API-01 | 内部读取/命令接口 | 可复用候选/外部接口另待补齐 | app/api/payroll/route.ts；lib/hris/http.ts | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 | 非法请求来源403、非JSON415、超过各路由body上限413、格式400；权限拒绝不得带出数据；事务故障不返回成功。业务HttpError按实际状态返回，未分类异常503 |
| BP-I-REQ-06 | 独立任务对象（M43） | 需补齐；不可拿聚合待办充当独立任务 | docs/P1_Source_Observations_20260907.md | M43独立任务未实现，现有work-inbox只是其他模块办理入口汇总，不替代该对象 | 待补任务规则后检验负责人和参与人可见/可写区别、历史进展是否追加保留、截止/优先级与完成定义；当前不编造通过预期 |
| BP-C-REQ-05 | 原站发展计划阶段与执行人（M17） | 需补齐；原简单行动不可替代完整阶段流程 | docs/P1_Source_Observations_20260907.md；docs/delivery/Cadre_Learning_Source_Gaps.md | 指导角色、跨阶段审批、模板变化及状态恢复未核实/未独立覆盖 | 先确认模板阶段开启规则、执行人解析、退回与变动恢复，才能定义步骤完成和阶段切换预期；现有简单发展行动不可冒充整套模板流程 |

## 其余全范围实现候选

| 原范围/业务包 | 可复用候选（原登记） | 需补齐（原登记） | 判定 |
|---|---|---|---|
| M01 组织员工 / BP-F | 组织人员、教育/工作/项目经历、岗位职级、入转调离、编制、协议类别、合同覆盖及续签报表、自定义字段分组及状态必填检查；合同自定义文本字段版本与续签继承快照 | 复杂跨字段联动、兼岗、复杂再入职及法人变更 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M02 人才评定 / BP-C | 未独立实现 | 评定过程、记录、活动设置、统计分析 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M03 干部管理2.0 / BP-C | 跨模块人才档案、提名审议、调动任用核对、考察述职；独立主职任期登记、更正/结束/作废、历史与档案衔接；干部访谈记录登记、更正、作废及受控历史 | 干部四状态名册、任用类型扩展与期限自动计算、档案子集、委员会及原站详细提交规则 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M04 HRBP工作台 / BP-I | 未独立实现 | 员工、录用入职、任职、绩效、分析 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M05 标签库 / BP-I | 未独立实现 | 企业标签库、北森标签库、应用设置 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M06 任职资格 / BP-C | 标准版本、能力证据、独立认证、到期与撤销 | 任职类别层级及复杂认证委员会 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M07 薪酬社保 / BP-S | 核定工资录入、独立复核、工资条、异议及补差、批次办理与已发布对账；冻结考勤聚合引用、版本失效阻断及发布后异常提示；来源变化核对待办与引用版本报表 | 自动核算、税社保、薪资档案、支付及企业规则验证 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M08 我的填报 / BP-I | 未独立实现 | 我发起的填报 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M09 预算成本 / BP-S | 未独立实现 | 预算、成本、统计分析 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M10 财务凭证 / BP-S | 未独立实现 | 任务管理、设置 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M11 假勤管理 / BP-A | 固定班次、打卡、补卡版本核验及撤回、请假、人工余额及覆盖报表；单人期间预览/手动冻结/重新开放/快照版本及假勤写保护；版本化固定班次及最多20条原子派班快照；假种组织/分钟上下限/制度说明及历史快照、停止新增 | 弹性轮班、设备接入、加班/调休、跨班请假、自动结转、年度多组织期间、自动执行、员工确认/申诉及完整发布/封存 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M12 招聘管理系统 / BP-R | 需求修订审批和运营报表、候选人、面试序号、录用退回与版本确认和原子入职；需求草稿/显式提交/旧待审兼容、类型紧急程度与职责资格字段、列表筛选和报表；保存并提交原子操作、创建请求网络重试恢复；内部招聘职位草稿/启用/版本/归档及候选来源冻结；四档评价表版本/冻结逐项评分/显式结论及创建重试；内部单人排期/冲突/指定评价/原子完成及历史 | 渠道门户、简历解析、面试日历、电子签和AI能力 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M13 面试官工作台 / BP-R | 未独立实现 | 筛选简历、面试、Offer审批、题库 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M14 AI人才库 / BP-R | 未独立实现 | 人才地图、智能分类、多维分析 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M15 测评中心 / BP-C | 未独立实现 | 项目、人才、方案、活动、考试 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M16 绩效管理 / BP-P | 目标权重与独立调整、执行跟进、自评、独立评价、结果发布、申诉与更正；同组织等级方案版本、开闭区间与非百分制、周期和申诉冻结快照、人才三档显式映射；活动分类/筛选/报表与启动前草稿编辑；单维文本模板版本/活动快照、自评与管理文本阶段必填和答案隔离；具体记录待办/自助入口v101；可选目标数量及整数权重范围、目标调整后旧回答清空已私有发布v102；同组织定性指标版本与目标引用快照已开发待验证发布 | 完整OKR、组织绩效、多级校准审批和企业申诉时限；手工等级、绩效系数、不参与考核、活动在途规则更新、组织公开与考核关系锁定；完整模板模块、多维/小数权重、附件与动态权限、指标自动下发；定量指标公式、完成值来源、共享分类树、指定评价人 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M17 继任与发展 / BP-C | 盘点、人才池、后备提名、继任覆盖报表、发展计划与学习衔接 | 复杂梯队、健康度模型和带教管理 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M18 在线盘点 / BP-C | 标准、盘点项目、潜力校准、九宫格快照、人才池及继任记录 | 校准会议及委员会、报告模板和多维模型 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M19 审批中心 / BP-I | 人事顺序审批、独立复核、撤回及历史；指定面试及薪酬来源变化待办 | 管理员委托、复杂条件分支及其他模块待办汇集 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M20 项目人力管理 / BP-F | 未独立实现 | 项目、人员、工时、统计 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M21 文化激励 / BP-I | 未独立实现 | 活动、企业文化、榜样、商城、勋章、动态 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M22 电子签 / BP-I | 未独立实现 | 认证、签署、印章、场景设置 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M23 推荐运营中心 / BP-R | 未独立实现 | 奖金、积分、推荐记录 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M24 校园大使管理 / BP-R | 未独立实现 | 人员、推荐、奖金、积分、规则 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M25 外部推荐管理 / BP-R | 未独立实现 | 人员、推荐、奖金、积分、规则 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M26 360度评估 / BP-C | 指定评估人、量表答卷、分组阈值与冻结报告 | 多种题型、提醒催办与完整活动运营 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M27 学习管理 / BP-L | 课程考试、培训申请与任务核对、课程阶段、显式批量派课、取消恢复与进度报表、项目、出勤、学分有效期、课程认证、活动报名、内部名册、试讲、培养派课与关联、培训带教、证书及报表、必修/选修数量门槛与派课/结项/报表统一判断、三模式学习配置草稿/定版/版本历史、首轮独立学习实例/原子派发/结项与窗口控制、跨计划课程实例隔离/同版本已完成进度复用/跨实例学分去重；独立实例课程要求快照、阶段选必修门槛及顺序、结项关闭未完成选修；阶段延迟开放、独立单选试卷版本与任务作答/取消、课程/考试混合计划、配置成绩与档案回流；固定日期起点修正、阶段内顺序/考试提交放行、显式循环新轮与按配置重复学分；独立单选/多选/判断、题目分值与漏选分、原始分及百分制追溯；独立作业版本/指定批阅/提交版本/转交撤权、混合计划要求与循环、HR台账及档案；考试与作业内容权重、缺失待定及成绩依据追溯；未完成实例内容更新预览/追加移除替换/阶段及成绩调整，原核验与学分保留、版本链防重和新增课程同步；显式自然日阶段提交期限/超期及截止后独立核验 | 人工题/排序及题库随机抽题、其他活动成绩来源及小数权重、阶段期限精确规则对照与其他活动顺序例外、自动循环调度/积分奖励及循环同步细则、已退出内容重新加入、完成重开、循环更新与批量异步运营；完整培养编排与批量自动派课、证书样式与自动发证、导师认证及组织关系同步、外聘讲师、完整班级运营、学分折抵及企业到期规则对照；作业多级批阅、附件、AI及优秀作业/奖励 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M28 AI陪练 / BP-L | 未独立实现 | 计划、剧本、话术库、质检、评分、角色库 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M29 员工调查 / BP-I | 实名问卷模板、发布名单、答卷及统计 | 匿名模式、完整调查报告与行动计划 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M30 北森问卷 / BP-I | 未独立实现 | 问卷管理 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M31 问卷调查 / BP-I | 实名量表和单选、模板版本、填报撤回与结项 | 复杂题型、分类、条件跳转及匿名模式 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M32 报表 / BP-I | 当前权限范围报表、分页查询和审计导出；工资考勤引用版本核对 | 自助设计器、完整领域覆盖、大规模查询与历史快照 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M33 森福利 / BP-S | 未独立实现 | 账户、福利、财务、合规、设置 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M34 AI面试官 / BP-R | 未独立实现 | 面试、企业题库、答疑知识库、看板 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M35 主数据同步 / BP-I | 未独立实现 | 任务、配置、规则、映射、开放应用、接口 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M36 北森iTalent / BP-I | 未独立实现 | 人力报告设置 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M37 人才标准 / BP-C | 能力标准版本、行为锚点及岗位要求 | 复杂指标组合、多维模型和标准审批机制 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M38 人才模型 / BP-C | 未独立实现 | 人才模型、角度码 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M39 会议管理 / BP-I | 未独立实现 | 预定、会议、会议室、日志 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M40 经理团队分析 / BP-I | 未独立实现 | 团队人事看板 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M41 数字人才 / BP-C | 未独立实现 | 搜索、AI选人、对比、标签 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M42 佣金管理 / BP-S | 未独立实现 | 方案、计算、结果、提成提点规则 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M43 任务 / BP-I | 未独立实现 | 任务信息、任务列表 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M44 RPA招聘助手 / BP-R | 未独立实现 | 个人/企业RPA、历史记录 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M45 干部管理 / BP-C | 未独立实现 | 任前管理、任职管理 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M46 职称管理 / BP-C | 未独立实现 | 职称管理 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M47 翻译工作台 / BP-I | 未独立实现 | 翻译、导入导出、日志 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |
| M48 员工自助 / BP-I | 本人档案、融入计划、假勤、学习、问卷、工资和申请进度 | 日程、日报、完整OKR与统一消息 | 待逐包对P1B核验；无需求签署，不自动确认所有已有实现 |

## 分包契约与实现证据索引

此索引由同一Scope的contracts生成。源码链接只证明静态对应；原站说明或范围文件不能证明已有实现。具体复用/补齐/修改边界按对应规格的差异列评审。

| 业务包/需求ID | 对象与规格 | 证据性质 | 代码或来源 | 具体差异/待核验 |
|---|---|---|---|---|
| BP-F/BP-F-REQ-01 | 组织/岗位/职级/员工；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [model.ts](../../lib/hris/model.ts)；[authorization.ts](../../lib/hris/authorization.ts)；[route.ts](../../app/api/hris/route.ts) | F-SPEC-01仅岗位/职级名称；兼岗/再入职/法人不是普通员工编辑 |
| BP-F/BP-F-REQ-02 | F03调动原单和执行记录；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [model.ts](../../lib/hris/model.ts)；[f01-f04-transfer-roles.test.mjs](../../tests/f01-f04-transfer-roles.test.mjs) | D1–D7已确认；F-SPEC-02/03仅异常边界和关联宽度待审 |
| BP-F/BP-F-REQ-03 | 项目人力（M20）；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Scope_Register.json](../../docs/delivery/Scope_Register.json) | M20未独立实现；项目归属BP-F不等于可按任职调动替代 |
| BP-F/BP-F-REQ-04 | 再入职身份、司龄与签订次数；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 原站配置说明事实与项目未实现边界；产品策略待需求评审 | [model.ts](../../lib/hris/model.ts)；[module-progress.ts](../../lib/hris/module-progress.ts)；[P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md) | 保留完整M01后续需求，不阻塞D1–D7；身份/司龄/合同计次选择尚未确认，不能借普通员工新增完成再入职 撤销纠错与不可手动入口清单仍未知；初始默认仅帮助出处，不作为本项目要求。 |
| BP-F/BP-F-REQ-05 | 合同协议、法人关联及合同字段版本；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 本项目既有实现静态事实及原站配置差异；除已确认范围外待产品评审 | [workforce.ts](../../lib/hris/workforce.ts)；[contract-fields.ts](../../lib/hris/contract-fields.ts)；[contract-field-model.ts](../../lib/hris/contract-field-model.ts)；[development.ts](../../lib/hris/development.ts) | BC-F23/24原站报表连续判定和显式renewalOf不同；法人文本不能支持法人停用/改名/多主体历史；电子签、到期自动任务、次数累计/日期连续缺口保留 |
| BP-F/BP-F-REQ-06 | 岗位编制与员工经历子集；[P1B_BP_F_Specification.md](../../docs/delivery/P1B_BP_F_Specification.md) | 既有实现静态候选；原站子集说明仅作差异依据 | [workforce.ts](../../lib/hris/workforce.ts)；[employee-experiences.ts](../../lib/hris/employee-experiences.ts) | BC-F22原站按配置唯一键控制新增与导入更新；本项目固定复合键和三类经历不是可配置子集/全量导入。兼职占编和项目人力工时不由主职人数替代。 |
| BP-C/BP-C-REQ-01 | 干部任期/提名/任用；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [cadre-terms.ts](../../lib/hris/cadre-terms.ts)；[cadres.ts](../../lib/hris/cadres.ts) | 原站四状态干部身份不可用registered/ended一对一替代；委员会/任期算法/复杂任用类型未就绪；BC-C10原站选拔/述职评价表及评分项是独立配置，当前提名布尔审议与考察证据不覆盖评价表/多评委汇总。 |
| BP-C/BP-C-REQ-02 | 任职资格标准及认证；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [qualification.ts](../../lib/hris/qualification.ts) | 认证委员会、类别层级及有效期政策需原站与企业基线；现有整数尺度非原站标准 |
| BP-C/BP-C-REQ-03 | 360项目/关系/答卷/报告；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [feedback.ts](../../lib/hris/feedback.ts)；[development.ts](../../lib/hris/development.ts) | 阈值/匿名性是独立策略待确认；提醒、题型、完整活动运营未覆盖；修订答卷的完整历史与是否允许管理员读原答卷须产品评审，不能以均值抑制宣称匿名。；BC-C15原站全局最多90角色、套卷最多15且模板勾选继承，当前固定四类无角色配置/套卷版本，不得一对一映射。 |
| BP-C/BP-C-REQ-04 | 盘点/继任/标准模型；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Cadre_Learning_Source_Gaps.md](../../docs/delivery/Cadre_Learning_Source_Gaps.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | 当前仅重用已有范围描述；多维模型/健康度/测評题库及评分未可验收 |
| BP-C/BP-C-API-01 | 内部读取/命令接口；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/qualifications/route.ts)；[route.ts](../../app/api/cadres/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-C/BP-C-REQ-05 | 原站发展计划阶段与执行人（M17）；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 原站局部结构事实；产品工作流需求受限，未批准默认规则 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[Cadre_Learning_Source_Gaps.md](../../docs/delivery/Cadre_Learning_Source_Gaps.md) | 指导角色、跨阶段审批、模板变化及状态恢复未核实/未独立覆盖 |
| BP-C/BP-C-REQ-06 | 选拔/述职评价表、投票与评分；[P1B_BP_C_Specification.md](../../docs/delivery/P1B_BP_C_Specification.md) | 原站空表/配置事实及已有实现差异；需求未就绪 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[cadres.ts](../../lib/hris/cadres.ts) | 已用帮助缩小算法未知；得分阈值相等、缺评/弃权分母、0除/舍入及评分版本仍待核实/业务评审；当前干部实现不覆盖评价模板/评分汇总。 |
| BP-L/BP-L-REQ-01 | 学习配置与实例；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [learning-plan-definitions.ts](../../lib/hris/learning-plan-definitions.ts)；[learning-plan-model.ts](../../lib/hris/learning-plan-model.ts) | 自动循环不是已实现；共享管理员与可学范围、完成实例重开、跨轮更新待明确；当前main学习配置未含原站简介字段；既有learning-description隔离分支f5f5b1bd9014d4b6eeb6d32da0f03e34da3bced2保留未合并，不计main已实现；BC-L14历史框架断连已由BC-L22恢复；原站关闭全公司共享/可见开关不撤销存量对象权限及表单默认值；当前课程依可读published版本选择，考试/作业须同组织sealed，不声称共享权限统一。 |
| BP-L/BP-L-REQ-02 | 阶段窗口与任务放行；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [learning-plan-definitions.ts](../../lib/hris/learning-plan-definitions.ts)；[learning-requirements.ts](../../lib/hris/learning-requirements.ts) | 自然日含首日和顺序晚开启的原站精确算法尚未核实，当前策略需评审 |
| BP-L/BP-L-REQ-03 | 计划成绩；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [learning-grades.ts](../../lib/hris/learning-grades.ts)；[learning-grade-evidence.ts](../../lib/hris/learning-grade-evidence.ts) | 缺失分母、精度、通过过滤及多审批人聚合为候选政策，原站选项存在不能证明算法完整一致；BC-L19考试档案有六来源且仅勾选后新数据，不回补历史；当前报表直接读可见考试任务和尝试，不是同一归档机制。；BC-L20/21学习成绩等级另有名称/最低/最高配置，59.9仅既有示例，不与绩效区间或计划成绩精度自动共用。 |
| BP-L/BP-L-REQ-04 | 学分、撤销、到期；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [learning-credits.ts](../../lib/hris/learning-credits.ts) | 折抵、企业到期算法、积分和自动发证尚未确认；不得将本项目整数单位当原站字段类型 |
| BP-L/BP-L-REQ-05 | AI陪练（M28）；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Scope_Register.json](../../docs/delivery/Scope_Register.json) | 没有独立实现，不以现有学习考试代替 |
| BP-L/BP-L-REQ-06 | 独立考试与作业批阅；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [learning-homework.ts](../../lib/hris/learning-homework.ts)；[learning-exam-definitions.ts](../../lib/hris/learning-exam-definitions.ts) | 填空/简答/排序、随机抽题、多级批阅、附件/AI批阅及外部通知尚未实现；原站可选题型不证明当前已支持 |
| BP-L/BP-L-API-01 | 内部读取/命令接口；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/learning-homework/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-L/BP-L-REQ-07 | 培训场次、讲师排期与出勤核验；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目当前实现静态事实；产品要求及验收预期待评审，非原站规则 | [training-sessions.ts](../../lib/hris/training-sessions.ts)；[instructor-assignment.ts](../../lib/hris/instructor-assignment.ts) | 自由文本讲师/地点身份去重与稳定ID不同；学员时间冲突、课时/费用/课酬、重复核验历史及离职传播未完整定义；与BP-A员工考勤分开。 |
| BP-L/BP-L-REQ-08 | 内部讲师名册与课程授课认证；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目当前实现静态事实；产品要求及验收预期待评审，非原站规则 | [instructor-directory.ts](../../lib/hris/instructor-directory.ts)；[instructors.ts](../../lib/hris/instructors.ts)；[instructor-development.ts](../../lib/hris/instructor-development.ts)；[instructor-trials.ts](../../lib/hris/instructor-trials.ts) | 原站讲师等级/晋升/课酬标准、停用对已排课程处理未知；按字面称为认证不表示外部资格认证。 |
| BP-L/BP-L-REQ-09 | 培训导师、师徒关系、辅导记录与出师；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目当前实现静态事实；产品要求及验收预期待评审，非原站规则 | [mentoring.ts](../../lib/hris/mentoring.ts) | 当前出师申请未要求等待结束日，最少辅导频次/成果标准及出师提前条件为候选政策待确认；离职不自动完成或删除关系，跨包恢复待定义。 |
| BP-L/BP-L-REQ-10 | 内部学习证书模板、依据与发放；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 本项目当前实现静态事实；产品要求及验收预期待评审，非原站规则 | [certificates.ts](../../lib/hris/certificates.ts) | 来源在发放后变化的失效传播、证书下载签章/外部验证接口、补发和历史到期续期未完整定义；内部证书与学分/讲师授课资格不等价。 |
| BP-L/BP-L-REQ-11 | 培训活动费用同步与课酬模式；[P1B_BP_L_Specification.md](../../docs/delivery/P1B_BP_L_Specification.md) | 原站配置事实与需求缺口；不得从模式名编造算法 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[training-sessions.ts](../../lib/hris/training-sessions.ts)；[payroll.ts](../../lib/hris/payroll.ts) | 费用同步和四种课酬计算未在已读培训/授课模型形成完整可复用合同；预算/实际不能混写，跨包消费者和错误恢复未就绪。 |
| BP-P/BP-P-REQ-01 | 绩效周期/计划/结果；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [performance.ts](../../lib/hris/performance.ts)；[performance-availability.ts](../../lib/hris/performance-availability.ts) | 组织绩效、关系锁定、强制分布、申诉时间窗及多维流程未就绪 |
| BP-P/BP-P-REQ-02 | 绩效等级与尺度；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [performance-ratings.ts](../../lib/hris/performance-ratings.ts) | 原站连续区间说明与现实现允许空隙但发布拒绝存在差异；纯手工等级/系数及在途更新未实现；BC-P14/15原站未评分可按0或均摊，权限不可见/无法评价脚注要求均摊；当前完整scores数组强制逐项有数，尚无这些状态表达。 |
| BP-P/BP-P-REQ-03 | 目标数量/权重检查与指标引用；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [Performance_Source_Gaps.md](../../docs/delivery/Performance_Source_Gaps.md)；[performance.ts](../../lib/hris/performance.ts) | 小数权重/算术求和/完整模块权重与定量自动下发未覆盖 |
| BP-P/BP-P-API-01 | 内部读取/命令接口；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/performance/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-P/BP-P-REQ-04 | 兼职目标与兼职绩效上下文；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 原站帮助事实与本项目未覆盖差异，业务需求待确认 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[performance.ts](../../lib/hris/performance.ts)；[performance-availability.ts](../../lib/hris/performance-availability.ts) | M01兼职对象与BP-P任职上下文双向依赖；源文档限制PIP/试用期/组织绩效及电子签/旧团队，不擅自扩范围；数据搜索计划日期非已交付证据。 |
| BP-P/BP-P-REQ-05 | 目标调整与员工进展反馈；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目当前静态实现候选；未复测、未业务签署，不作为原站规则 | [performance-changes.ts](../../lib/hris/performance-changes.ts)；[performance-checkins.ts](../../lib/hris/performance-checkins.ts)；[performance-availability.ts](../../lib/hris/performance-availability.ts) | “活动周期内”在当前函数中是active状态及范围校验，未比较当天与start/end，不能宣称日期自动封锁；目标调整后旧submitted跟进的反馈未另校验basePlanVersion，须明确按旧快照反馈还是关闭重建，不自动认定当前目标进展。 |
| BP-P/BP-P-REQ-06 | 正式绩效结果、申诉与更正版本；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 本项目当前静态实现候选；未复测、未业务签署，不作为原站规则 | [performance.ts](../../lib/hris/performance.ts)；[performance-ratings.ts](../../lib/hris/performance-ratings.ts) | 原站申诉角色/时限与多维系数未完整观察；当前更正发布者只排除审核人和员工本人，不自动排除原评价/发布者，是否需更严隔离待需求评审；跨人才盘点、奖金/报表旧快照如何传播需明确。 |
| BP-P/BP-P-REQ-07 | 多维结果、缺评算分与系数绑定；[P1B_BP_P_Specification.md](../../docs/delivery/P1B_BP_P_Specification.md) | 原站配置/示例事实及产品缺口；推导用例未执行/签署 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[performance-ratings.ts](../../lib/hris/performance-ratings.ts)；[performance.ts](../../lib/hris/performance.ts) | 现有scores逐项必填，未表达未评/无法评价；多维、强分、系数及公式未可复用覆盖。源配置不是本项目批准，异常/精度与金额消费者待评审。 |
| BP-R/BP-R-REQ-01 | 需求/招聘职位/候选人；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [recruitment.ts](../../lib/hris/recruitment.ts)；[recruitment-jobs.ts](../../lib/hris/recruitment-jobs.ts) | 原站允许职位或人才库入口，当前必须有需求，无法覆盖独立人才库；外部来源/门户未实现；BC-R14原站系统级查重条件与当前同需求邮箱去重不同，原站重复关系≠自动合并，R-SPEC-01需同时定义自然人/申请/库关系及去重处理。 |
| BP-R/BP-R-REQ-02 | 面试/评价/录用入职；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [recruitment.ts](../../lib/hris/recruitment.ts)；[recruitment-evaluations.ts](../../lib/hris/recruitment-evaluations.ts) | 面试日历/通知、电子签回执、Offer占编与跨法人/再入职接口未就绪；无排期的普通/结构化评价仍有独立路径，不能把指定面试人/结束时间限制泛化为所有评价。 |
| BP-R/BP-R-REQ-03 | 推荐/校园/外推/AI/RPA周边；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Recruitment_Source_Gaps.md](../../docs/delivery/Recruitment_Source_Gaps.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | 周边7组未独立实现，不能用核心招聘自动验收覆盖 |
| BP-R/BP-R-REQ-04 | 招聘创建请求恢复与内部接口；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [route.ts](../../app/api/recruitment/route.ts)；[http.ts](../../lib/hris/http.ts) | 不是原站API说明，不提供外部渠道幂等契约；通用版本冲突不等于所有命令自动幂等 |
| BP-R/BP-R-API-01 | 内部读取/命令接口；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/recruitment/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-R/BP-R-REQ-05 | 面试排期与冻结评价表；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 本项目当前静态实现候选；未复测、未业务签署，不作为原站规则 | [interview-schedule.ts](../../lib/hris/interview-schedule.ts)；[recruitment-status.ts](../../lib/hris/recruitment-status.ts)；[recruitment.ts](../../lib/hris/recruitment.ts) | 代码未拒绝创建已过去时间的排期；冲突扫描所有scheduled而非仅appointmentLive，失效候选排期未取消仍可能占时段。是否允许补录/过期自动释放需评审；未实现外部日历、通知、会议室预订和可核验视频接口。 |
| BP-R/BP-R-REQ-06 | 入职后候选信息权限与员工身份同步；[P1B_BP_R_Specification.md](../../docs/delivery/P1B_BP_R_Specification.md) | 原站局部配置证据及现有实现差异；具体权限策略待补证和业务评审 | [recruitment.ts](../../lib/hris/recruitment.ts)；[development.ts](../../lib/hris/development.ts)；[P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md) | BC-R16只证明原站配置语义，不授权本项目新增角色或对离职者扩大数据访问；与F-SPEC-04身份连续性共同受限，不阻断内部招聘需求链路规格。 |
| BP-A/BP-A-REQ-01 | 班次/打卡/补卡/请假；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [attendance.ts](../../lib/hris/attendance.ts) | 弹性/轮班/设备/加班调休未实现；分钟规则是本项目候选 |
| BP-A/BP-A-REQ-02 | 结算期间与冻结版本；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [attendance-periods.ts](../../lib/hris/attendance-periods.ts)；[attendance-locks.ts](../../lib/hris/attendance-locks.ts) | 原站冻结/发布/确认/封存为独立列，不能用当前两个状态冒充完整原站月报；期间记录本身不是逐版本不可变归档，审计或外部引用不等于完整历史期间可重放，不作“所有旧期间快照均保留”承诺。；BC-A11已补配置流程次序/发布条件/自动与反向操作依赖，但选项当前值及业务结果未核实，不再仅凭月报列名推断。 |
| BP-A/BP-A-REQ-03 | 假期/调休结算；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Attendance_Source_Gaps.md](../../docs/delivery/Attendance_Source_Gaps.md) | 企业参数、自动结转和申诉待决策/补证 |
| BP-A/BP-A-API-01 | 内部读取/命令接口；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/attendance/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-A/BP-A-REQ-04 | 固定班次定义与批量派班；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 本项目静态实现候选；未本轮复验，非原站事实或已批准要求 | [shift-definitions.ts](../../lib/hris/shift-definitions.ts)；[attendance.ts](../../lib/hris/attendance.ts)；[route.ts](../../app/api/attendance/route.ts) | 不含多段休息/弹性/自动排班/复杂节假日与轮班；历史班次秒精度与请假整分钟冲突显式阻断。 |
| BP-A/BP-A-REQ-05 | 假种快照、年度额度与补卡版本；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 本项目静态实现候选；未本轮复验，非原站事实或已批准要求 | [attendance.ts](../../lib/hris/attendance.ts)；[attendance-locks.ts](../../lib/hris/attendance-locks.ts) | 无自动授假、法定标准、工龄折算、过期、跨年结转或加班转调休公式；源字段/法律规则不能由现有人工分钟模型推导。冻结锁仅班次及引用的打卡/补卡/请假，不锁独立额度登记或假种配置。 |
| BP-A/BP-A-REQ-06 | 月报完整处理流程与自动任务；[P1B_BP_A_Specification.md](../../docs/delivery/P1B_BP_A_Specification.md) | 原站配置证据驱动的候选需求；未签署，未实现完整流程 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[attendance-periods.ts](../../lib/hris/attendance-periods.ts) | 源页面配置已观察，执行顺序和异常时点尚未验证；现有周期快照可复用，发布/员工确认/审批/封存/自动任务需补齐，未经批准不实现。 |
| BP-S/BP-S-REQ-01 | 人工核定工资批次与工资条；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [payroll.ts](../../lib/hris/payroll.ts)；[payroll-access.ts](../../lib/hris/payroll-access.ts) | 仅人工核定值，自动算薪/税社保/支付均未实现，不能以发布工资条冒称发薪 |
| BP-S/BP-S-REQ-02 | 冻结考勤引用/来源变化；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [payroll-attendance.ts](../../lib/hris/payroll-attendance.ts) | 没有自动由考勤计算工资公式；补差与重核策略需业务评审 |
| BP-S/BP-S-REQ-03 | 薪资组/预算成本/凭证/福利/佣金；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Payroll_Source_Gaps.md](../../docs/delivery/Payroll_Source_Gaps.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | M09/M10/M33/M42无独立实现；原48组不删减 |
| BP-S/BP-S-API-01 | 内部读取/命令接口；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 本项目接口静态事实；候选验收契约待评审 | [route.ts](../../app/api/payroll/route.ts)；[http.ts](../../lib/hris/http.ts) | 这些是本项目接口，原站外部endpoint/认证/错误/回调尚未取得；分页、重试和大批量能力不由GET存在推定 |
| BP-S/BP-S-REQ-04 | 工资异议、补差与对账；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 本项目当前静态实现候选；未业务复验/签署，不作为原站规则 | [payroll-adjustments.ts](../../lib/hris/payroll-adjustments.ts)；[payroll-reports.ts](../../lib/hris/payroll-reports.ts)；[payroll-access.ts](../../lib/hris/payroll-access.ts) | 当前补差允许带符号净额且未检查累计净额非负；这与初始工资条净额非负是不同边界，是否允许应追回净欠款需业务评审，不能擅自加限制。没有支付/退款回执，补差发布不代表资金已调整；补差并未强制关联新考勤期间。 |
| BP-S/BP-S-REQ-05 | 薪酬管理范围与历史主体；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 本项目静态实现候选，待源权限补证及评审 | [payroll-access.ts](../../lib/hris/payroll-access.ts)；[payroll-reports.ts](../../lib/hris/payroll-reports.ts)；[payroll-attendance.ts](../../lib/hris/payroll-attendance.ts)；[development.ts](../../lib/hris/development.ts) | 历史人员/薪资组、跨法人和人员授权需按原站BC-S08等补证，不能认定当前批次组织策略已获批准；范围与字段权限/下载另需明确。 |
| BP-S/BP-S-REQ-06 | 薪资档案与任职事件联动；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站局部规则与本项目差异规格，待补证/评审 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[model.ts](../../lib/hris/model.ts)；[workforce.ts](../../lib/hris/workforce.ts)；[payroll.ts](../../lib/hris/payroll.ts) | 不把BC-S09配置候选写成D1既有批准扩展；F01–04首包差异与完整薪资档案后续范围分开，自动算薪仍未实现。 |
| BP-S/BP-S-REQ-07 | 人力预算预估、占用和Offer/入职校验；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站配置证据及实现差异候选，未签署 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[recruitment.ts](../../lib/hris/recruitment.ts)；[model.ts](../../lib/hris/model.ts) | BC-S11配置说明已读，当前仅headcount/组织编制人数约束，无金额预算预估；涉及BP-R/BP-F调用边界，完整预算M09需补齐，不宣称当前首包自动占预算。 |
| BP-S/BP-S-REQ-08 | 财务凭证类型、切分及分摊来源；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站局部配置证据；具体计算/接口契约尚受限，未验收 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | M10未有独立实现；工资发布/工资对账不等同财务凭证或外部入账。BC-S12/13只能确定配置对象，执行规则受限。 |
| BP-S/BP-S-REQ-09 | 佣金输入、计算过程和结果；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站结构证据及逐项受限需求，未业务评审 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | M42独立实现缺失；现有人工工资可作为后续接收候选但无确认接口或自动生成工资项目；产品级与部门级多维度需补证。 |
| BP-S/BP-S-REQ-10 | 福利积分账户与离职/异常处理；[P1B_BP_S_Specification.md](../../docs/delivery/P1B_BP_S_Specification.md) | 原站局部配置证据及受限需求，未签署 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | M33无独立实现；积分≠学分≠工资现金，原站企业账户不是当前组织目录。完整规则和访问范围待补证，不伪装已就绪。 |
| BP-I/BP-I-REQ-01 | 员工自助/统一待办；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [route.ts](../../app/api/self-service/route.ts)；[work-inbox.ts](../../lib/hris/work-inbox.ts) | 日程/日报/完整OKR/消息发送未实现；独立M43任务不等于当前聚合待办 |
| BP-I/BP-I-REQ-02 | 报表与指标分母；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [reports.ts](../../lib/hris/reports.ts)；[route.ts](../../app/api/reports/route.ts) | 设计器/大规模查询/历史组织快照未就绪；每数据集必须独立定义分母，不能统一套人员数 |
| BP-I/BP-I-REQ-03 | 实名调查/问卷与360共用模板边界；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [surveys.ts](../../lib/hris/surveys.ts)；[feedback.ts](../../lib/hris/feedback.ts) | 员工调查/北森问卷/问卷调查三组不合并，匿名、复杂题型、报告行动计划未完成 |
| BP-I/BP-I-REQ-04 | 主数据同步契约预检；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 本项目既有实现静态事实；转为产品要求待评审 | [integration-preflight.ts](../../lib/hris/integration-preflight.ts) | 鉴权、密钥托管、真实endpoint、调度、事务回执和队列均未实现；重试函数不是后台重试服务 |
| BP-I/BP-I-REQ-05 | 工作台/电子签/会议/文化/翻译等周边；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 原站局部证据及原范围/差异输入；具体产品规则待补证，不声称已实现 | [Integration_Source_Gaps.md](../../docs/delivery/Integration_Source_Gaps.md)；[Scope_Register.json](../../docs/delivery/Scope_Register.json) | 周边多组只有入口；保留候选接口与证据不足，不能泛化当前自助实现 |
| BP-I/BP-I-REQ-06 | 独立任务对象（M43）；[P1B_BP_I_Specification.md](../../docs/delivery/P1B_BP_I_Specification.md) | 原站局部字段事实及受限产品需求；无独立实现 | [P1_Source_Observations_20260907.md](../../docs/P1_Source_Observations_20260907.md) | M43独立任务未实现，现有work-inbox只是其他模块办理入口汇总，不替代该对象 |

## 历史验证适用版本索引

当前仅读原验证记录，不复跑、不汇总通过数量。baseCommit只作测试前上下文，不能冒充测试代码快照。部分文件哈希不能证明完整环境/依赖相同。

| 原记录/时间 | 版本定位 | 原适用范围 | 本轮状态 |
|---|---|---|---|
| [Cadre_Interview_Verification.json](../../docs/delivery/Cadre_Interview_Verification.json)；2026-09-08T11:39:29.631504+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 当前全部业务测试，明确排除旧Worker渲染环境测试；含干部访谈共享权限、绩效提示、自助与聚合 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Contract_Fields_Verification.json](../../docs/delivery/Contract_Fields_Verification.json)；2026-09-08T11:54:46.629532+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 合同字段继承及既有合同/基础/报表权限/看板关联回归，非全量复测 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Controller_Lifecycle_Verification.json](../../docs/delivery/Controller_Lifecycle_Verification.json)；2026-09-08T10:44:34.710709+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 组织员工、干部、学习及既有P3 API关联回归 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Controller_Regression_Verification.json](../../docs/delivery/Controller_Regression_Verification.json)；2026-09-08T10:58:43.305486+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 本轮领域/API及聚合回归；明确排除旧rendered-html.test.mjs，其Node/cloudflare运行时问题仍未通过 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Dashboard_Verification.json](../../docs/delivery/Dashboard_Verification.json)；2026-09-08T10:11:36.120150+00:00 | sourceCommit=523fa165ff34c69d7c417ee5a8bb78a234ed378f | 合成数据综合回归，含看板聚合；不代替人工业务验收 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [F01_F04_Closure_Verification.json](../../docs/delivery/F01_F04_Closure_Verification.json)；2026-09-08T12:11:02.862468+00:00 | testedCommit=a54381363e52c513fb79bc1a227368dad8bedab9 | F01–F04核心组织员工/权限/审批与存储；附件复用既有P3技术证据，本批未冒称全量回归 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [F01_F04_Decisions_Verification.json](../../docs/delivery/F01_F04_Decisions_Verification.json)；2026-09-08T13:21:05.083631+00:00 | testedSourceCommit=3d690cbbd6336c6de8b76a06fa4459700b1e3a88 | D1–D7首包必要实现：原子生效/日期/失败恢复/来源目标授权/职级防盲审/驳回重审；关联P2/P3/G1回归，仅合成SQLite/R2替身，不代替真人UAT或生产验收 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [F01_F04_Entry_UI_Verification.json](../../docs/delivery/F01_F04_Entry_UI_Verification.json)；2026-09-08T13:41:50.733266+00:00 | testedSourceCommit=fdc423fcba607bd5814a0672836b55536c71ecb1 | 首包入口/空筛选恢复/既有审批组件真实React渲染；无后端业务或权限修改，未重复全量API回归；非浏览器交互或人工UAT | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [F01_F04_Role_Arrangement_Verification.json](../../docs/delivery/F01_F04_Role_Arrangement_Verification.json)；2026-09-08T12:32:08.406906+00:00 | 原记录无完整测试快照SHA；不得据日期补造 | 跨组织发起者/审批者/字段权限安排及关联回归，合成数据；不改变产品行为，不代替UAT | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [F04_Closure_Verification.json](../../docs/delivery/F04_Closure_Verification.json)；2026-09-08T12:11:49.230054+00:00 | testedCommit=a54381363e52c513fb79bc1a227368dad8bedab9 | 仅附件、历史读取与成员目录撤权一致性选中场景；未执行其他P3场景 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [G2_performance_Verification.json](../../docs/delivery/G2_performance_Verification.json)；原记录未给统一时间 | applicationAndTestCommit=9d3d416769a7ab28945261d231e1a29eeaaf50da | 详见原记录；不能由文件名推断全部覆盖 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Goal_Advisory_Verification.json](../../docs/delivery/Goal_Advisory_Verification.json)；2026-09-08T11:18:48.824215+00:00 | 原记录无完整测试快照SHA；不得据日期补造 | 绩效范围提示与强制、模板快照、周期生命周期、指标引用和权限关联回归 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Indicator_Usage_Verification.json](../../docs/delivery/Indicator_Usage_Verification.json)；2026-09-08T10:49:54.452632+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 指标版本引用、待审/发布分离、去重与当前HR范围隔离；关联目录回归 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Scope_Execution_Verification.json](../../docs/delivery/Scope_Execution_Verification.json)；2026-09-08T11:18:48.824647+00:00 | 原记录无完整测试快照SHA；不得据日期补造 | 看板聚合、验收签署门槛和无执行证据的保守分类 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
| [Self_Report_Verification.json](../../docs/delivery/Self_Report_Verification.json)；2026-09-08T11:12:08.452507+00:00 | 原记录仅有部分文件哈希；没有完整测试快照SHA | 自助离职入口、报表调动撤权、P3既有接口及看板聚合；非全量测试 | 未复跑；未代签业务；仅引用原JSON哈希，不把当前文件一致当重新运行 |
