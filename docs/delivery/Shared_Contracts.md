# 公共接口契约 SC-1

基于本轮核查代码记录现状，不声明新增服务。变更必须附版本、调用方影响和兼容处理，由总控唯一合并。

| 契约 | 现有实现 | 必须保留的约束 |
|---|---|---|
| 身份和租户 | context.ts / authorization.ts / repository.ts | tenantId来自已认证成员；客户端不能指定他人租户；成员停用拦截 |
| 主数据 | model.ts 的 State/Employee/Org/Position/Grade | employeeId/orgId/positionId/gradeId用内部ID；姓名/工号不可作为跨模块关系键 |
| 读取 | developmentContext、visibleDevelopment、projectRecord | 按当前角色/组织/字段过滤；不能直接将完整records返回客户端 |
| 写入 | POST /api/development {revision,command} | 当前修订号；返回{id,revision}，批量派课返回{ids,count,revision} |
| 一致性 | readConsistent / commitExtension | 修订变化409；业务、历史与审计共同事务；冲突刷新后显式重新提交，不盲目重试 |
| 多记录 | saveDevelopmentMany | 最多20条、唯一ID、一修订原子提交；不拆成部分成功 |
| 历史 | GET /api/development?id=ID&page=N | 当前权限再校验；分页；保留原始事件快照；历史不增加当前权限 |
| 错误 | http.ts | {error:string}；401未登录、403拒绝、400格式、409冲突、413大小、415类型、503未分类失败 |
| 请求 | readBody | 同源Origin、application/json、最大32768字节；不绕过统一处理 |
| 时间 | business-time.ts及领域现有函数 | 保持北京时间业务日期；事件UTC时间；不混用浏览器本地时区 |
| 附件 | /api/attachments | 服务端读取R2、元数据权限和下载后修订检查；不分享原始存储地址 |

## 人才—学习既有链路

1. 发展计划 kind=plan，employeeId 关联员工，referenceId 关联能力标准版本。
2. enroll 命令使用 employeeId/courseId/due，可选planId/trainingId。planId必须属于同一员工、状态active或returned；课程referenceId必须等于计划referenceId。课程必须published。
3. enrollment.referenceId是课程版本ID；payload.planId是计划ID，payload.trainingId是培训项目ID；不能互换，也不能用模糊名称关联。
4. 已有同员工/课程版本记录时拒绝再次enroll；取消后恢复使用restoreEnrollment并保留原任务和考试次数。历史跨项目复用尚未实现，不能视为接口能力。
5. submitLearning要求通过关联考试；verifyLearning须独立核验，接受前检查强制出勤；完成状态completed。verifyPlan接受前检查关联未完成且未取消的学习任务。
6. cadreProfile通过当前可见records聚合plans和learning。回流是读取现有权威记录，不另复制完成标记；不自动升级资格或职级。
7. 学分使用既有learning-credits接口，不把档案展示触发当成授予事件；来源与去重规则继续以领域代码为准。

共享热点：development.ts、app/api/development/route.ts、development-repository.ts被人才和学习共同使用，只能由当前总控/被明确交接的基础负责人单写。没有消息总线、跨服务事件系统或新自动派课协议，不为本批增建。

下一步：基础F-G0-02把以上契约逐项映射现有测试；模块只补确切缺口。任何新字段先记录请求/响应示例、旧数据处理、权限和消费者，再由总控合入。


## H001证据澄清（不改变SC-1业务语义）

逐项代码/测试映射见[G0_Evidence_Map.md](G0_Evidence_Map.md)，合成场景见[G1_Foundation_Plan.md](G1_Foundation_Plan.md)。本轮新增5项测试，连同既有109项共114/114通过。

- 历史page从1开始，每页20项，以第21项判断hasMore；原事件快照经过当前权限投影才返回。
- 未授权人员读取草稿课程或其他不可见记录可能先收到403；可见记录的状态/关联错误为400。业务校验发生在保存CAS之前，不将409描述为所有错误请求的固定优先结果。
- 计划允许active/returned状态派课；submitted/completed/cancelled不允许。课程同code不代表同版本，必须比较referenceId内部ID。
- 盘点与计划目前共享employeeId，计划referenceId指向能力标准；没有已实现的reviewId外键或自动计划生成协议。
- 本轮仅澄清现状并补证据，未改变公共请求/响应、领域规则或旧数据，不要求消费者迁移。

## H002 干部实例与待决议项（不改变SC-1）

执行提交`5bf8b9385fb4cb326880df7e3d1d2fc4bc183eb6`。planId/employeeId/标准版本与学习关联的实际合成ID、引用断言见[G1_Cadre_Delivery.md](G1_Cadre_Delivery.md)及测试输出H002_SC1_INSTANCE。盘点到计划仍为同员工显式办理，无reviewId外键；完成仅聚合权威记录。

离职后当前组织HR/经理及未停用本人保留既有计划/学习历史读取，属于现有实现，企业保留策略未核实。C-DEF-01：保留离职员工关联的active=false请求被member-rules在职校验阻断，400且账号仍active；具体证据和最小兼容修复建议见交付记录。总控修复前不作完整撤权或G1通过结论。

## C-DEF-01成员停用契约修正
显式active=false允许保留同租户既有离职员工关联；active=true仍要求在职，缺失档案仍拒绝。保持CAS和审计，无新增字段或迁移；不代表离职自动停用制度已确认。

## H004-R 绩效生命周期可操作提示
三个绩效GET接口新增兼容字段livePlanIds，仅列当前成员可见且在职、属于活动周期组织、未取消及未形成结果的计划ID。该字段是生命周期提示，不是角色授权；各命令继续独立校验身份、状态、修订及原子写入。仅返回已有可见ID，不暴露额外组织或人员字段。页面、待办、自助及报表统一使用同一生命周期判断。历史调整仍可拒绝/撤回，申诉更正保持原规则。

## 干部任期登记
新增cadreTerm记录及/api/cadre-terms GET/POST，写入仍为{revision,command}，不改变其他API。register/correct/end/void保存事件历史，关联员工ID和任用岗位ID。HR/admin写且不能本人，经理按当前双组织范围读；结束/作废仅登记，不自动改变人事主数据或发送通知。干部档案消费同记录，作废不展示当前条目、历史仍受当前权限保护。无表结构迁移。

## B1/B2 学习实例契约增量
learningAssignment引用不可变learningDefinition版本；enrollment的learningAssignmentId/learningDefinitionId和窗口/组织快照由服务器生成，原enroll命令不接受客户端自造关联。首轮派发、结项、整体取消/恢复在/api/learning-assignments下执行，统一revision+command包。saveDevelopmentMany默认20条不变；本入口显式21条（实例+最多20任务）。整体取消用assignmentCancelled及assignmentPreviousStatus保留原任务状态，实例恢复不重置考试、已完成课程或学分。普通员工不访问管理接口，通过既有学习页读取本人任务。课程原唯一性保持；重复课程、循环轮次及历史同步尚未开放。

## C1/C2 接口变更
enroll新增可选assignmentId，须匹配有效learningAssignment的员工、课程和冻结截止日，不能与trainingId/planId混用；仅此路径实例内唯一。assign支持relative/fixed的progressSync：记录sourceEnrollmentId/sourceVerifiedBy/sourceVerifiedAt/sourceExamAttemptId。GET学习实例增加attempt依赖用于核实来源考试，投影继续遵守原权限。courseCreditAlreadyGranted统一前后端课程版本去重。旧任务恢复保留原ID，关联实例的恢复继续校验原实例与冻结期限。

## SC-2 学习活动兼容增量（2026-09-08）

- 保留旧courseIds与enrollment，新增examIds/learningExamDefinition/learningExamTask/learningExamAttempt；courseIds与examIds合计最多20。
- learningRequirements: {id,kind:course|exam,resourceId}[]，要求ID在相同资源版本下跨配置版本稳定，实例冻结独立快照。旧实例只读映射，无批量迁移。
- /api/learning-plans新增stages命令与可选examIds；/api/learning-exams管理试卷版本；/api/learning-exam-tasks管理独立或计划内任务。全局revision与审计事务沿用SC-1。
- 必須按任务ID隔离尝试、按原始核验来源追溯课程。完成投影使用learningRequirementProgress，开放使用learningStageOpen及当前人员/日期判断，不能将所有completed状态直接相加。
- 试卷管理限admin/hr当前组织；学员仅接收有权任务的去答案paper。独立考试台账限admin/hr；人才档案仍沿用其角色范围。
- 单选等权百分制取整、通过停止重考为当前独立规则；未核实为原站完整算法。计划总成绩暂未生成。

SC-2成绩增量：gradeRule随定义版本和实例冻结；learningGrade输出state/score/missingExamIds/attemptIds，not_configured与pending的score均为null，provisional和final保留真实0分。只使用本实例requirementId绑定的考试任务与尝试。final仅代表实例已结项；不表示生产或业务已验收。规则保存端点沿用/api/learning-plans的grading命令。

### SC-1 学习阶段窗口和顺序补充（BC-L08）

固定日期模式的 startAfterDays 以 learningMode.start 为起点；relative 以实例加入业务日为起点，0表示当天。原有 relative 数据不变；修正已有 fixed 实例投影，不重写历史完成记录。

阶段增加可选 orderedTasks / examSubmissionUnlock，默认 false。顺序按冻结的 trainingStages[].courseIds（混合资源ID）排列，全部前置要求完成后放行；显式启用考试例外时，可用同实例、同员工、同要求绑定任务的有效作答放行，允许该次作答未及格。例外不改变 requirement 完成状态、实例结项门槛或学分。阶段例外不能在 orderedTasks=false 时设为 true。当前选修任务也遵循前置顺序；原站跳过选修的具体语义待核实。未支持的作业、面授、辅导、线下考核放行例外保留后续，不能映射为课程完成。

### SC-1 独立客观题结构补充

独立试卷可使用 objectiveQuestions（single/multiple/trueFalse，prompt/options/correct[]/points/partialPoints），与旧 questions 二选一。旧单选版本保留每题1分的解释，旧客户端不能把含objectiveQuestions的草稿降级覆盖。定版版本和已有作答不变。新答案使用数组集合，拒绝重复/越界及不完整作答；单选判断只能一项。多选全对满分、未选错但未选全按显式partialPoints、含错误项零分；本批仅整数题目分值，未声称原站全部计分一致。

作答快照保留 objectiveAnswers、earnedPoints、maxPoints 和 score（取整百分制）。通过与否使用原始分比例交叉相乘，不能因显示舍入达到及格线而误通过；计划成绩仍使用其明确的百分制聚合契约。对学员试卷投影去掉correct，答案只留在有权限的定义端，历史尝试沿用本人/范围隔离。独立考试报表追加原始得分和总分，不改旧列位置。

未实现：填空/简答/排序、人工阅卷、题库/随机抽题/导入、完整补考及原站评分尺度。上述全部仍在范围中。

### SC-1 独立作业及计划绑定（BC-L09）

homeworkDefinition保存草稿/定版/后续版本/归档和作业要求、最大提交次数。homeworkTask冻结内容版本，指定同组织在职且非本人的reviewerEmployeeId，homeworkSubmission按提交版本留存正文与批阅证据。每次提交/批阅双记录原子保存；重复批阅及旧提交不能覆盖当前版本。转交通过当前任务控制全部提交及历史入口权限，旧批阅人立即撤权。单作业取消使用homeworkPreviousStatus，整单取消使用assignmentPreviousStatus，两者不得覆盖。

首批为一名指定人员独立批阅，评分可选且不自动决定通过；最大提交次数由HR配置，退回后在期限/次数内可重交。已提交的作业允许指定人员在提交截止后批阅，但仍检查人员/组织和实例/阶段门槛；这是明确内部策略，未宣称原站默认。取消状态也可由HR转交批阅人，便于原批阅人调动/离职后的恢复，不解除取消。

learningDefinition.homeworkIds为可选追加字段，旧客户端省略时保留；资源合计1–20，阶段资源恰好覆盖一次。requirement.kind=homework，ID稳定，版本/实例冻结；派发必须提供homeworkReviewers资源ID→员工ID映射。全部资源与实例仍最多21条原子写入。完成须当前提交的通过证据、正确任务/人员关联和一致核验人/时间，不借用另一实例或把提交当完成。

阶段homeworkSubmissionUnlock可在orderedTasks=true时明确启用：本实例存在有效作业提交可放行后续任务，批阅是否通过仍控制要求完成和实例结项。其他活动例外不混用。循环下一轮重新生成作业，不复用旧提交，默认沿用上轮各作业的当前批阅人，也可显式替换；人员无效则整单拒绝。归档定义不接新派发，已派发内容版本保持。

保留未实现范围：多级/多名批阅、富文本附件约束、AI批阅、抄送、优秀作业、作业学分奖励、内容权重成绩与完整企业退回规则；不得用课程或作业通过代替这些功能完成。

### SC-1 内容权重首批（BC-L10）

contentWeighted显式配置items(requirementId,source,weight)，支持examHighest/examAverage/homeworkLatest，正整数百分比合计100且要求ID唯一。仅引用本定义有实际分数来源的考试/作业；不把无成绩课程完成映射满分。定版及实例冻结；更换所引用资源清单清空相关规则。

考试按本实例的有效作答取分；作业只取当前提交已批阅的评分，重新提交未批阅时保持待定。attempts=all/passed明确控制是否计入未通过记录，decimals明确舍入0–2位；这些缺失/纳入/精度政策为内部显式选择，不声称源站默认。无有效分或缺少任何加权项不重归一化、不静默计零。保留missingRequirementIds和evidenceIds供追溯；attemptIds仍仅考试尝试，兼容旧消费者。

计划成绩按各活动已记录的百分制计算，原始分另外保留；课程成绩、带教/线下考核等其他来源和小数权重未支持。批阅独立性同时检查员工身份与提交账号，重新绑定员工不能让同账号审批自己的提交。


## 内容更新增量契约（BC-L03部分实现）

POST /api/learning-content-update: {revision, action:"preview"|"apply", command:{assignmentId,definitionId,homeworkReviewers?}, evidence?}。preview不写入，返回差异、阻止原因、更新前后完成与成绩投影；apply重新检查全部权限/版本/人员及资源，不信任客户端预览。全局revision CAS、实例与新增任务及审计原子保存，最多21条；审计失败不得部分更新。

首批仅同族后续定版、模式/日期/同步不变、未过期且非循环的active实例；已有要求必须全部保留，追加课程仅在progressSync=false时支持，追加考试/作业复用独立派发校验。原任务不改写；目标定义、旧定义链、更新人/时间/依据保存在实例与不可变事件中。contentDefinitionHistoryIds防止已迁移版本再次本轮派发。不得用这组字段替代真实数据迁移审批；这里只操作授权的本系统合成学习实例。
