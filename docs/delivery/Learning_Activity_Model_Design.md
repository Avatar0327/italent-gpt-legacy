# 下一批：计划活动、成绩与完成要求模型

状态：设计准备，未开发。依据BC-L03/04/05和当前C1/C2代码；不能直接把课程内考试当成原站计划内独立考试活动。

## 依赖顺序
1. 学习内容要求版本：requirementId稳定、版本不可变，类型course/exam/assignment/mentoring/offlineAssessment；保留旧courseIds到course要求的兼容映射。
2. 独立考试定义与任务：examDefinition版本包含试题/通过线/次数规则；examAssignment绑定员工+计划实例+requirementId；attempt仅引用自己的examAssignment，题目正确答案仅管理权限读取。
3. 实例要求完成投影：逐requirement读取课程核验、考试、作业、带教或线下考核证据；明确哪些是必修、阶段最少数量、时间及顺序。不同证据类型不互相冒充。
4. 计划总成绩：独立于要求完成。规则版本区分none、allHighest、allAttemptsAverage、eachExamHighestAverage、specifiedExamHighest、contentWeighted。
5. 内容版本迁移：未完成实例迁移保留旧要求/任务；已完成实例默认不变，显式重开独立留痕。迁移、成绩重算和奖励不能分散提交导致部分状态。

## 成绩算法的已知与未知
BC-L05只确认四种考试汇总选项名称。allAttemptsAverage与eachExamHighestAverage的分母不同，不能合并成一个average。未作答场次是否计零、是否包含未通过尝试、指定考试是否允许多选、缺失权重、舍入精度、课程内考试是否参与计划成绩、历史同步是否复用计划成绩均待核实。设计保存每个来源和计算参数；缺失成绩先标记未定，禁止自动当零或宣称已计算最终成绩。

contentWeighted需先确认每种活动允许的成绩来源，不能给无考试课程编造100分。源任务完成不等于取得满分；学分、学习完成率、成绩为独立指标。

## 后续代码改造清单
- learning-plan-definitions/model：活动要求版本与输入互斥校验，兼容既有课程清单。
- learning-assignments及API：原子生成异类任务；容量按总写入条数计算，不把21条上限当无限批量。
- development/visibility：独立考试和成绩字段投影、当前成员/组织范围、退出后的历史权限。
- training-stages、任务派发、实例结项：采用统一requirement完成投影，未派发要求仍在分母中。
- 课程学习/考试UI、self-service、work-inbox、reports、cadre-profiles：同批区分原始完成、历史复用、活动考试与课程内考试，避免展示与可办理性不一致。
- learning-credits：仍不把完成率或成绩直接转化为奖励；循环重复奖励另有冻结规则。

## 必须保留的验收
旧普通报名和培训阶段链路、实例考试隔离、C-DEF-01、调动/离职、撤权、重复/旧修订、审计失败回滚、20课程容量、整体取消恢复、历史来源和去重全部保留。新增多考试各两次成绩的合成反例，确保两种平均确实不同；缺失成绩不静默归零。通过自动化后仍需界面与人工业务预验收，生产验收单列。

该设计不删除任何全量范围，不创建新聊天或移交写入者；当前总控继续拥有共享文件与合并发布职责。
