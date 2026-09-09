# R1报表逐列字段字典

本字典是05设计的P2评审补充，静态提取固定源码列标签，再明确目标类型/单位/权限。共21个数据集，保留全部原列及workforce可选邮箱/职级。未执行产品代码。原显示拼接ID列表保持文本呈现，但查询关联必须使用独立稳定rowKey/FK；不从显示名还原关系。

规范JSON：[R1_P2_Report_Field_Dictionary.json](R1_P2_Report_Field_Dictionary.json)。来源版本、逐列位置、null/过滤/聚合/导出规则均在JSON中。所有nullable表示API允许以state表达缺证，不改变源业务必填约束；查询到0条才no_data。布尔“是否通过”未知为null，“未作答”是显示标签。

原代码的string空值不再自动当合法空文本；真实空值须以state区分。分钟以decimal保留源精度，整数金额以分并带币种。序号/年度/版本/档位即使integer也不开放sum；计数和成绩只能使用21数据集登记公式，不自动相加。所有字段均须read＋行/字段/历史约束，export/subscribe/manage另授权。

## workforce

行键：`personId`；来源：M01；时间：current；未定义比率；在职人数需status过滤后distinct personId。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|workforce.c01|工号|text|none|dataset_read_and_row_scope|
|workforce.c02|姓名|text|none|dataset_read_and_row_scope|
|workforce.c03|组织|text|none|dataset_read_and_row_scope|
|workforce.c04|岗位|text|none|dataset_read_and_row_scope|
|workforce.c05|人员状态|enum|none|dataset_read_and_row_scope|
|workforce.c06|入职日期|date|none|dataset_read_and_row_scope|
|workforce.c07|邮箱|text|none|viewEmail_and_current_row_scope|
|workforce.c08|职级|text|none|viewLevel_and_current_row_scope|

## contractCoverage

行键：`personId`；来源：M01；时间：current；coveredPersonCount / visibleActivePersonCount；覆盖多合同者仍1人。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|contractCoverage.c01|核对日期（北京时间）|date|none|dataset_read_and_row_scope|
|contractCoverage.c02|工号|text|none|dataset_read_and_row_scope|
|contractCoverage.c03|姓名|text|none|dataset_read_and_row_scope|
|contractCoverage.c04|当前组织|text|none|dataset_read_and_row_scope|
|contractCoverage.c05|人员状态|enum|none|dataset_read_and_row_scope|
|contractCoverage.c06|入职日期|date|none|dataset_read_and_row_scope|
|contractCoverage.c07|登记覆盖情况|enum|none|dataset_read_and_row_scope|
|contractCoverage.c08|覆盖当日的签署记录数|integer|count_or_ordinal|dataset_read_and_row_scope|
|contractCoverage.c09|覆盖当日的合同编号|text|none|dataset_read_and_row_scope|
|contractCoverage.c10|未来开始的签署记录数|integer|count_or_ordinal|dataset_read_and_row_scope|
|contractCoverage.c11|已过结束日的签署记录数|integer|count_or_ordinal|dataset_read_and_row_scope|
|contractCoverage.c12|终止记录数|integer|count_or_ordinal|dataset_read_and_row_scope|
|contractCoverage.c13|待登记签署草稿数|integer|count_or_ordinal|dataset_read_and_row_scope|

## contractOperations

行键：`contractId`；来源：M01；时间：event_range；签订次数按person+legalEntity+agreementCategory distinct signed/ended contractId；作废排除。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|contractOperations.c01|合同编号|text|none|dataset_read_and_row_scope|
|contractOperations.c02|工号|text|none|dataset_read_and_row_scope|
|contractOperations.c03|姓名|text|none|dataset_read_and_row_scope|
|contractOperations.c04|当前组织|text|none|dataset_read_and_row_scope|
|contractOperations.c05|人员状态|enum|none|dataset_read_and_row_scope|
|contractOperations.c06|用工主体|text|none|dataset_read_and_row_scope|
|contractOperations.c07|期限类型|enum|none|dataset_read_and_row_scope|
|contractOperations.c08|登记状态|enum|none|dataset_read_and_row_scope|
|contractOperations.c09|开始日期|date|none|dataset_read_and_row_scope|
|contractOperations.c10|原登记结束日|date|none|dataset_read_and_row_scope|
|contractOperations.c11|已登记终止日|date|none|dataset_read_and_row_scope|
|contractOperations.c12|签署登记日期|date|none|dataset_read_and_row_scope|
|contractOperations.c13|距登记结束日（日历天）|integer|calendar_days|dataset_read_and_row_scope|
|contractOperations.c14|后续续签记录|text|none|dataset_read_and_row_scope|
|contractOperations.c15|后续续签登记状态|enum|none|dataset_read_and_row_scope|
|contractOperations.c16|协议类别|enum|none|dataset_read_and_row_scope|

## recruitmentOperations

行键：`requisitionId`；来源：M12；时间：current；remaining=active?max(0,headcount-hiredApplications):null；自然人数单独distinct candidatePersonId。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|recruitmentOperations.c01|招聘需求|text|none|dataset_read_and_row_scope|
|recruitmentOperations.c02|岗位|text|none|dataset_read_and_row_scope|
|recruitmentOperations.c03|所属组织|text|none|dataset_read_and_row_scope|
|recruitmentOperations.c04|需求状态|enum|none|dataset_read_and_row_scope|
|recruitmentOperations.c05|需求版本|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c06|需求人数|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c07|累计已入职|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c08|剩余可入职|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c09|待审录用|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c10|已批准待登记接受|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c11|已接受待入职|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c12|筛选面试中|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c13|已结束候选流程|integer|count_or_ordinal|dataset_read_and_row_scope|
|recruitmentOperations.c14|需求类型|enum|none|dataset_read_and_row_scope|
|recruitmentOperations.c15|紧急程度|enum|none|dataset_read_and_row_scope|
|recruitmentOperations.c16|需求提出日期|date|none|dataset_read_and_row_scope|
|recruitmentOperations.c17|期望到岗日期|date|none|dataset_read_and_row_scope|
|recruitmentOperations.c18|工作职责|text|none|dataset_read_and_row_scope|
|recruitmentOperations.c19|任职资格|text|none|dataset_read_and_row_scope|

## attendance

行键：`shiftId`；来源：M11；时间：event_range；分钟按源班次算法；如展示覆盖率仅known coveredMinutes / known plannedMinutes并明示缺失样本。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|attendance.c01|工号|text|none|dataset_read_and_row_scope|
|attendance.c02|姓名|text|none|dataset_read_and_row_scope|
|attendance.c03|日期|date|none|dataset_read_and_row_scope|
|attendance.c04|班次|text|none|dataset_read_and_row_scope|
|attendance.c05|计划分钟|decimal|minutes|dataset_read_and_row_scope|
|attendance.c06|批准请假分钟|decimal|minutes|dataset_read_and_row_scope|
|attendance.c07|未覆盖分钟|decimal|minutes|dataset_read_and_row_scope|
|attendance.c08|状态|enum|none|dataset_read_and_row_scope|

## payrollOperations

行键：`batchId`；来源：M07；时间：current；gross/deduction/net/employer为整数分分别sum；不跨币种相加。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|payrollOperations.c01|批次编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollOperations.c02|批次名称|text|none|payroll_staff_and_batch_org_and_field|
|payrollOperations.c03|期间|text|none|payroll_staff_and_batch_org_and_field|
|payrollOperations.c04|批次组织|text|none|payroll_staff_and_batch_org_and_field|
|payrollOperations.c05|状态|enum|none|payroll_staff_and_batch_org_and_field|
|payrollOperations.c06|有效明细数|integer|count_or_ordinal|payroll_staff_and_batch_org_and_field|
|payrollOperations.c07|明细应发（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollOperations.c08|明细扣款（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollOperations.c09|明细净额（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollOperations.c10|单位承担（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|

## payrollReconciliation

行键：`paySlipId`；来源：M07；时间：current；originalCents + sum(published adjustments Cents)，按adjustmentId去重；不是支付成功。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|payrollReconciliation.c01|批次编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c02|工资条编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c03|期间|text|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c04|工号快照|text|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c05|姓名快照|text|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c06|组织快照|text|none|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c07|原应发（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c08|原扣款（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c09|原净额（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c10|原单位承担（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c11|已发布补差数|integer|count_or_ordinal|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c12|补差应发（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c13|补差扣款（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c14|补差净额（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c15|补差单位承担（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c16|对账应发（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c17|对账扣款（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c18|对账净额（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|
|payrollReconciliation.c19|对账单位承担（分）|money_cents|currency_cents|payroll_staff_and_batch_org_and_field|

## payrollAttendanceReferences

行键：`paySlipId,attendancePeriodId,frozenVersion`；来源：M07+M11；时间：current；引用分钟是各引用快照值；人数distinct personId另算，禁止引用行数作人数。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|payrollAttendanceReferences.c01|批次编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c02|工资条编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c03|计薪月份|text|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c04|工号快照|text|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c05|姓名快照|text|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c06|批次状态|enum|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c07|考勤期间编号|opaque_id|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c08|开始业务日|date|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c09|结束业务日|date|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c10|引用冻结版本|integer|count_or_ordinal|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c11|当前冻结版本|integer|count_or_ordinal|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c12|当前期间状态|enum|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c13|一致性|enum|none|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c14|引用计划分钟|decimal|minutes|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c15|引用批准请假分钟|decimal|minutes|payroll_staff_and_batch_org_and_field|
|payrollAttendanceReferences.c16|引用未覆盖分钟|decimal|minutes|payroll_staff_and_batch_org_and_field|

## performanceOperations

行键：`planId`；来源：M16；时间：current；pendingChanges/checkins按各recordId；可反馈只当前角色集合；不相加为总人数。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|performanceOperations.c01|工号|text|none|dataset_read_and_row_scope|
|performanceOperations.c02|姓名|text|none|dataset_read_and_row_scope|
|performanceOperations.c03|当前组织|text|none|dataset_read_and_row_scope|
|performanceOperations.c04|期间|text|none|dataset_read_and_row_scope|
|performanceOperations.c05|计划阶段|enum|none|dataset_read_and_row_scope|
|performanceOperations.c06|目标版本|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c07|待审目标调整|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c08|待反馈记录（所有版本）|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c09|其中本账号可反馈|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c10|其中旧目标版本记录|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c11|已反馈记录|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c12|最近提交跟进（北京时间）|timestamp|none|dataset_read_and_row_scope|
|performanceOperations.c13|活动年度|integer|count_or_ordinal|dataset_read_and_row_scope|
|performanceOperations.c14|周期分类|enum|none|dataset_read_and_row_scope|
|performanceOperations.c15|绩效类别|enum|none|dataset_read_and_row_scope|
|performanceOperations.c16|业务日期|date|none|dataset_read_and_row_scope|

## performance

行键：`resultRootId,publishedVersionId`；来源：M16；时间：current；评分与评级沿已发布源版本；不得按任意updatedAt选最大。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|performance.c01|工号|text|none|producer_sensitive_field_explicit_grant|
|performance.c02|姓名|text|none|producer_sensitive_field_explicit_grant|
|performance.c03|期间|text|none|producer_sensitive_field_explicit_grant|
|performance.c04|正式评级|enum|none|producer_sensitive_field_explicit_grant|
|performance.c05|分数|decimal|producer_declared_score|producer_sensitive_field_explicit_grant|
|performance.c06|来源|enum|none|producer_sensitive_field_explicit_grant|

## talentReview

行键：`reviewRootId,publishedVersionId`；来源：M18；时间：current；潜力/绩效档位各源字段；配置人数、采集、校准、发布分别count distinct personId。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|talentReview.c01|工号|text|none|producer_sensitive_field_explicit_grant|
|talentReview.c02|姓名|text|none|producer_sensitive_field_explicit_grant|
|talentReview.c03|期间|text|none|producer_sensitive_field_explicit_grant|
|talentReview.c04|潜力档位|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|talentReview.c05|绩效快照档位|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|talentReview.c06|盘点版本|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|talentReview.c07|原版本编号|opaque_id|none|producer_sensitive_field_explicit_grant|

## successionCoverage

行键：`positionId`；来源：M17；时间：current；incumbents按有效primary personId；successors distinct active personId per position；ready/one_year/two_years沿版本。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|successionCoverage.c01|岗位编码|text|none|producer_sensitive_field_explicit_grant|
|successionCoverage.c02|目标岗位|text|none|producer_sensitive_field_explicit_grant|
|successionCoverage.c03|所属组织|text|none|producer_sensitive_field_explicit_grant|
|successionCoverage.c04|现任人数|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|successionCoverage.c05|有效后备人数|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|successionCoverage.c06|现在可就任|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|successionCoverage.c07|预计一年|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|
|successionCoverage.c08|预计两年|integer|count_or_ordinal|producer_sensitive_field_explicit_grant|

## learning

行键：`enrollmentId`；来源：M27；时间：current；completed/enrollment分别计数；复用sourceEnrollmentId与原核验时间保留。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|learning.c01|工号|text|none|dataset_read_and_row_scope|
|learning.c02|姓名|text|none|dataset_read_and_row_scope|
|learning.c03|课程|text|none|dataset_read_and_row_scope|
|learning.c04|截止日期|date|none|dataset_read_and_row_scope|
|learning.c05|状态|enum|none|dataset_read_and_row_scope|
|learning.c06|成果核验时间|timestamp|none|dataset_read_and_row_scope|
|learning.c07|计划实例|opaque_id|none|dataset_read_and_row_scope|
|learning.c08|轮次|integer|count_or_ordinal|dataset_read_and_row_scope|
|learning.c09|完成方式|enum|none|dataset_read_and_row_scope|
|learning.c10|来源学习任务|opaque_id|none|dataset_read_and_row_scope|
|learning.c11|原核验时间|timestamp|none|dataset_read_and_row_scope|
|learning.c12|退出要求时间|timestamp|none|dataset_read_and_row_scope|
|learning.c13|退出依据|text|none|dataset_read_and_row_scope|

## learningPlanProgress

行键：`learningAssignmentId`；来源：M27；时间：current；completedRequirements / applicableRequirements；completedStages / stages分别定义，不混合权重成绩。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|learningPlanProgress.c01|工号|text|none|dataset_read_and_row_scope|
|learningPlanProgress.c02|姓名|text|none|dataset_read_and_row_scope|
|learningPlanProgress.c03|计划|text|none|dataset_read_and_row_scope|
|learningPlanProgress.c04|配置版本|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningPlanProgress.c05|实例状态|enum|none|dataset_read_and_row_scope|
|learningPlanProgress.c06|已完成要求|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningPlanProgress.c07|要求总数|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningPlanProgress.c08|已达标阶段|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningPlanProgress.c09|阶段总数|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningPlanProgress.c10|成绩状态|enum|none|producer_sensitive_field_explicit_grant|
|learningPlanProgress.c11|计划成绩|decimal|producer_declared_score|producer_sensitive_field_explicit_grant|
|learningPlanProgress.c12|缺少有效成绩的内容数|integer|producer_declared_score|producer_sensitive_field_explicit_grant|
|learningPlanProgress.c13|成绩依据记录ID|text|none|producer_sensitive_field_explicit_grant|

## learningExams

行键：`examTaskId`；来源：M27；时间：current；attemptCount=distinct attemptId；raw earned/max与percent score分开，不用任务数当作答数。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|learningExams.c01|工号|text|none|dataset_read_and_row_scope|
|learningExams.c02|姓名|text|none|dataset_read_and_row_scope|
|learningExams.c03|试卷|text|none|dataset_read_and_row_scope|
|learningExams.c04|试卷版本|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningExams.c05|学习实例|opaque_id|none|dataset_read_and_row_scope|
|learningExams.c06|开放日期|date|none|dataset_read_and_row_scope|
|learningExams.c07|截止日期|date|none|dataset_read_and_row_scope|
|learningExams.c08|状态|enum|none|dataset_read_and_row_scope|
|learningExams.c09|作答次数|integer|count_or_ordinal|dataset_read_and_row_scope|
|learningExams.c10|最后得分（百分制取整）|integer|percent_0_100|producer_sensitive_field_explicit_grant|
|learningExams.c11|是否通过|boolean|none|dataset_read_and_row_scope|
|learningExams.c12|原始得分|decimal|producer_declared_score|producer_sensitive_field_explicit_grant|
|learningExams.c13|原始总分|decimal|producer_declared_score|dataset_read_and_row_scope|
|learningExams.c14|退出要求时间|timestamp|none|dataset_read_and_row_scope|
|learningExams.c15|退出依据|text|none|dataset_read_and_row_scope|

## homework

行键：`homeworkTaskId`；来源：M27；时间：current；submissionVersion/score/reviewResult分列；passedTask比率只在明确任务分母下计算。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|homework.c01|工号|text|none|dataset_read_and_row_scope|
|homework.c02|姓名|text|none|dataset_read_and_row_scope|
|homework.c03|作业|text|none|dataset_read_and_row_scope|
|homework.c04|版本|integer|count_or_ordinal|dataset_read_and_row_scope|
|homework.c05|状态|enum|none|dataset_read_and_row_scope|
|homework.c06|开放日期|date|none|dataset_read_and_row_scope|
|homework.c07|提交截止日|date|none|dataset_read_and_row_scope|
|homework.c08|提交次数|integer|count_or_ordinal|dataset_read_and_row_scope|
|homework.c09|当前提交ID|opaque_id|none|dataset_read_and_row_scope|
|homework.c10|批阅人|text|none|dataset_read_and_row_scope|
|homework.c11|当前评分|decimal|producer_declared_score|producer_sensitive_field_explicit_grant|
|homework.c12|批阅结论|enum|none|dataset_read_and_row_scope|
|homework.c13|退出要求时间|timestamp|none|dataset_read_and_row_scope|
|homework.c14|退出依据|text|none|dataset_read_and_row_scope|

## trainingStageProgress

行键：`trainingId,personId`；来源：M27；时间：current；required course数按阶段定义；completed distinct courseId；missing task与pending task分开。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|trainingStageProgress.c01|培训项目|text|none|dataset_read_and_row_scope|
|trainingStageProgress.c02|项目状态|enum|none|dataset_read_and_row_scope|
|trainingStageProgress.c03|工号|text|none|dataset_read_and_row_scope|
|trainingStageProgress.c04|姓名|text|none|dataset_read_and_row_scope|
|trainingStageProgress.c05|人员状态|enum|none|dataset_read_and_row_scope|
|trainingStageProgress.c06|阶段总数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingStageProgress.c07|课程总数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingStageProgress.c08|已核验课程数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingStageProgress.c09|最早未完成阶段|text|none|dataset_read_and_row_scope|
|trainingStageProgress.c10|该阶段已派发未完成|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingStageProgress.c11|该阶段无有效项目任务|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingStageProgress.c12|已完成全部阶段|boolean|none|dataset_read_and_row_scope|

## trainingProgress

行键：`trainingId`；来源：M27；时间：current；participants=distinct personId(non-cancelled)；completion=completedTasks / validTasks×100，四舍五入2位；任务按enrollmentId。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|trainingProgress.c01|培训项目|text|none|dataset_read_and_row_scope|
|trainingProgress.c02|所属组织|text|none|dataset_read_and_row_scope|
|trainingProgress.c03|项目状态|enum|none|dataset_read_and_row_scope|
|trainingProgress.c04|可见报名人数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingProgress.c05|有效学习任务数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingProgress.c06|已完成任务|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingProgress.c07|待核验任务|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingProgress.c08|已取消任务|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingProgress.c09|任务完成率（%）|decimal|percent_0_100|dataset_read_and_row_scope|

## trainingRoster

行键：`enrollmentId`；来源：M27；时间：current；requiredSessions=非取消必修场次；present/absent=已verified；pending=required-present-absent。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|trainingRoster.c01|培训项目|text|none|dataset_read_and_row_scope|
|trainingRoster.c02|课程|text|none|dataset_read_and_row_scope|
|trainingRoster.c03|工号|text|none|dataset_read_and_row_scope|
|trainingRoster.c04|姓名|text|none|dataset_read_and_row_scope|
|trainingRoster.c05|人员状态|enum|none|dataset_read_and_row_scope|
|trainingRoster.c06|学习任务状态|enum|none|dataset_read_and_row_scope|
|trainingRoster.c07|必修场次数|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingRoster.c08|已核验出席|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingRoster.c09|已核验未出席|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingRoster.c10|待核验或未登记|integer|count_or_ordinal|dataset_read_and_row_scope|
|trainingRoster.c11|学习截止日|date|none|dataset_read_and_row_scope|

## instructorSchedule

行键：`sessionId`；来源：M27；时间：event_range；minutes=(endAt-startAt)/60000；cancelled effectiveMinutes=0；不当实际授课/课酬。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|instructorSchedule.c01|培训项目|text|none|dataset_read_and_row_scope|
|instructorSchedule.c02|场次|text|none|dataset_read_and_row_scope|
|instructorSchedule.c03|讲师（排期快照）|text|none|dataset_read_and_row_scope|
|instructorSchedule.c04|身份关联|enum|none|dataset_read_and_row_scope|
|instructorSchedule.c05|开始时间（北京时间）|timestamp|none|dataset_read_and_row_scope|
|instructorSchedule.c06|结束时间（北京时间）|timestamp|none|dataset_read_and_row_scope|
|instructorSchedule.c07|原排期分钟|decimal|minutes|dataset_read_and_row_scope|
|instructorSchedule.c08|有效计划分钟|decimal|minutes|dataset_read_and_row_scope|
|instructorSchedule.c09|场次状态|enum|none|dataset_read_and_row_scope|

## instructorCampaignProgress

行键：`campaignId`；来源：M27；时间：current；applications按applicationId可重报；people distinct personId另算；profiles/latestTrial/mandatoryProof分别计数。

|fieldId|保留列名|类型|单位|字段授权|
|---|---|---|---|---|
|instructorCampaignProgress.c01|认证活动|text|none|dataset_read_and_row_scope|
|instructorCampaignProgress.c02|活动组织|text|none|dataset_read_and_row_scope|
|instructorCampaignProgress.c03|报名状态|enum|none|dataset_read_and_row_scope|
|instructorCampaignProgress.c04|报名记录数|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c05|待资格复核|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c06|资格通过|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c07|资格未通过|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c08|已撤回|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c09|已关联提名|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c10|在职在用讲师|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c11|最新试讲通过的提名|integer|count_or_ordinal|dataset_read_and_row_scope|
|instructorCampaignProgress.c12|待完成必修培养关联|integer|count_or_ordinal|dataset_read_and_row_scope|

## 权限裁剪后的旧列映射

workforce的邮箱/职级是独立可选列。字典fieldId固定，旧数组偏移不固定：只有viewLevel而无viewEmail时，最后一列仍是职级，绝不能按第7列映成邮箱。兼容适配按实际columns标签与rows成对映射，或直接按employee已注册字段表达式生成目标对象；服务端先权限裁剪，再返回稳定fieldId。任何未知/重复标签拒绝映射，不猜字段。验收P3-XMOD-02。
