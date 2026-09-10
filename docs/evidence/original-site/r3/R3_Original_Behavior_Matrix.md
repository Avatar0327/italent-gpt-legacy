# R3 原站行为矩阵

当前共52项；原站观察不代表复刻实现通过。runtime_verified仅对应描述中实际运行部分；帮助文本、权限和有人员行为不外推。历史转录修正在JSON及Source_Observations保留。

|证据ID|模块|主题|原站行为|需求ID|证据类型|运行验证|
|---|---|---|---|---|---|---|
| M27-ORIGIN-001 | M27 | 页面结构 | 课程表单分基本信息、课程内容、学习规则、课程激励、可学范围、学习资料、本课概要；标题/所属部门/所属目录必填 | M27-SPEC-01 | page_observed | False |
| M27-ORIGIN-002 | M27 | 课程内容生效 | 添加课件/课程/问卷/考试/作业必须保存或提交；直接退出不保存添加内容 | M27-SPEC-01 | page_help_observed | False |
| M27-ORIGIN-003 | M27 | 时长上限 | 文档/图文/URL/云文档课件单次学习时长按配置课件时长封顶；配置0不计学习时长 | M27-SPEC-04 | page_help_observed | False |
| M27-ORIGIN-004 | M27 | 学习后锁定 | 课件进度同步/不同步选项提示：本课程有学员学习后无法再次修改 | M27-SPEC-02 | page_help_observed | False |
| M27-ORIGIN-005 | M27 | 课程成绩聚合 | 不设置；所有考试最高分；所有考试成绩平均；每场考试最高分之和/场数；指定考试最高分 | M27-SPEC-03 | page_options_observed | False |
| M27-ORIGIN-006 | M27 | 共享与公开 | 管理员共享只授使用而不授编辑；学员公开决定课程中心可检索；不公开仍可通过学习计划/培训项目/岗位学习学习 | M27-SPEC-01 | page_help_observed | False |
| M27-ORIGIN-007 | M27 | 默认可见范围 | 本次新建课程默认不共享管理员、公开且公司全员可见、游客关闭；已改本轮草稿为不公开 | M27-SPEC-01 | default_and_form_change_observed | False |
| M27-ORIGIN-008 | M27 | 奖励与签名 | 额外积分输入提示0~1000；签名有无需/电子签/手写；证书与勋章独立配置 | M27-SPEC-05 | page_options_observed | False |
| M27-ORIGIN-009 | M27 | 空内容草稿 | 不添加课件可保存；本次新课程列表状态未发布，学习人数0 | M27-SPEC-01 | saved_record_readback | True |
| M27-ORIGIN-010 | M27 | 导入规则 | 一次最多5000；支持新增/更新/新增或更新；空格不处理/清空；课程ID空或不匹配新增，匹配更新，自定义ID无效；部门空默认操作者管理单元 | M27-SPEC-06 | page_help_observed | False |
| M27-ORIGIN-011 | M27 | 模板参考信息 | 模板选择不含数据仍附带课程、课件、部门等辅助参考页；本轮重新生成仅含虚构课程主表后上传 | M27-SPEC-01 | download_structure_observed | True |
| M27-ORIGIN-012 | M27 | 导入两阶段 | 上传导入后先出现九条预览并分配ID；仍需确认导入，预览ID不等于业务落库证据 | M27-SPEC-06 | import_preview_observed | True |
| M16-ORIGIN-001 | M16 | 活动字段和层级 | 活动含组织/向下公开/组织绩效影响分布/异常处理人类型和指定人/锁定考核关系；员工绩效与组织绩效、目标、OKR独立菜单 | M16-SPEC-01 | page_options_observed | False |
| M16-ORIGIN-002 | M16 | 周期日期联动 | 选择2026年度、第三季度后自动填入2026-07-01至2026-09-30；日期仍作为独立字段展示 | M16-SPEC-01 | form_change_readback | True |
| M16-ORIGIN-003 | M16 | 空活动创建与参与人分离 | 本轮活动保存后详情页无被考核人；添加被考核人有精准/条件/方案/导入，精准添加要求模板和人员 | M16-SPEC-01 | saved_activity_detail_observed | True |
| BASE-ORIGIN-001 | BASE | 新增员工隐含合同依赖 | 电子邮箱/入职日期/部门/试用标志必填；邀请激活默认否；公司默认已带出且保存提示劳动合同期限类型必填。未生成签署；表单保存被拒绝 | M12-SPEC-05 | validation_rejected | True |
| M12-ORIGIN-001 | M12 | 候选人创建入口 | 应聘者支持单个/批量/系统模板/成绩导入；手工姓名必填；关联职位和人才库至少一项；渠道必填 | M12-SPEC-01 | page_options_observed | False |
| M12-ORIGIN-002 | M12 | 独立个人库 | 个人库名称最多50字；共享部门/共享人可空；AI推荐默认关闭；本轮个人库已保存，不共享 | M12-SPEC-06 | saved_record_readback | True |
| M12-ORIGIN-003 | M12 | 批量简历解析 | 批量最多500文件、单文件不超过50M为页面提示；本轮10份UTF8虚构txt已提交并在指定私有库逐条回查，姓名保留前缀、性别保密、学历本科 | M12-SPEC-06 | ten_records_readback | True |
| M11-ORIGIN-001 | M11 | 班次配置结构 | 固定/弹性/自由班次；日期工作日/节假日/公休日；手动/工作日历日期设置；统计天数与工作分钟数分开 | M11-SPEC-01 | page_options_observed | False |
| M11-ORIGIN-002 | M11 | 半天分割策略 | 按工作时长一半、固定时点、首个休息时段开始三种；工作日选定后本轮分割字段曾清空，需重新选择 | M11-SPEC-01 | form_change_observed | True |
| M11-ORIGIN-003 | M11 | 日班保存和复制 | 当日09:00-17:00计算480分钟；本轮SMOKE01和02保存并精确名称回查，仅本轮组织且不下级共享；复制保留配置并添加副本后缀 | M11-SPEC-01 | saved_record_readback | True |
| M11-ORIGIN-004 | M11 | 已有排班不自动联动 | 修改安排加班不会影响已有排班，需重新排班；生效考勤档案/考勤档案规则使用的班次不支持停用（页面提示） | M11-SPEC-01 | page_help_observed | False |
| M11-ORIGIN-005 | M11 | 特定人员使用限制 | 页面实际提示不支持坐班制员工使用：工作/取卡范围超24小时、间歇、安排加班、统计天数非1、非工作日班次；尚未实测拒绝。前次记录误写轮班制，现按原页面纠正。 | M11-SPEC-01 | page_help_observed | False |
| M07-ORIGIN-001 | M07 | 发薪方案依赖 | 新方案要求适用薪资组、周期、方案使用权限；结果来源系统计算；税款所属期在发薪活动维护；独立组未建前本轮方案未保存 | M07-SPEC-01 | page_options_observed | False |
| M07-ORIGIN-002 | M07 | 跨组月中调动与算税 | 方案有个税通算税是/否；月中调动可分别独立核算或调入方核算全月；本轮尚未核算及调用个税通 | M07-SPEC-02; M07-SPEC-03 | page_options_observed | False |
| M07-ORIGIN-003 | M07 | 薪资组部门作用域 | 薪资组有编码、名称、上级、状态、对应部门；本轮新组织可被部门选择器检索，不等于已创建可用薪资组 | M07-SPEC-01 | form_selection_observed | False |
| M07-ORIGIN-004 | M07 | 上级薪资组必填及独立组落库 | 缺上级保存拒绝；选择默认根组作为引用，仅关联本轮部门且不含下级后保存；精确过滤回读启用行。未创建核算活动。 | M07-SPEC-01 | validation_and_save_readback | True |
| M12-ORIGIN-004 | M12 | 不同姓名邮箱的疑似匹配 | SMOKE01(C00014235)提示9个疑似；展开确认SMOKE09(C00014243)为84%疑似，两者邮箱不同、经历相同。仅证明此对结果，未推导算法、阈值或其余8对明细。 | M12-SPEC-01; M12-SPEC-06 | comparison_panel_observed | True |
| M12-ORIGIN-005 | M12 | 取消疑似与局部计数刷新 | 只对本轮01与09点取消疑似；确认提示取消后不再判定两人为疑似；确认是后比较窗9变8，详情头部当时仍9。未合并删除，持久抑制和重载一致性待测。 | M12-SPEC-01; M12-SPEC-06 | action_confirmed_by_panel_readback | True |
| M12-ORIGIN-006 | M12 | 原始简历预览环境限制 | 本轮txt已解析并显示标准字段；详情原始简历预览显示This page has been blocked by Chromium。未绕过浏览器限制；不归因于招聘业务规则。 | M12-SPEC-06 | browser_preview_error_observed | True |
| M27-ORIGIN-013 | M27 | 空章节发布校验 | SMOKE02在私有、未发布且1章0节时点发布，原站明确拒绝：当前课程章节无内容无法发布，请添加内容! | M27-SPEC-01 | validation_rejected | True |
| M27-ORIGIN-014 | M27 | 正式课件上传入口 | 上传课件先打开上传面板，点击点此上传才出现文件选择器。页面支持PDF等文档，提示文档300MB、音视频10GB、Scorm1.2 ZIP 1GB；上限未实测。 | M27-SPEC-01 | upload_ui_help_observed | False |
| M27-ORIGIN-015 | M27 | 上传、元数据确认、转码和课程保存分层 | 一页虚构PDF上传完成后需确认标题/所属部门/目录；确认后课程为1章1节、文档转码完成，默认1分钟、1学分；课程保存后重新编辑仍有本轮课件。 | M27-SPEC-01; M27-SPEC-06 | upload_and_saved_record_readback | True |
| M27-ORIGIN-016 | M27 | 零分钟可以持久保存 | 把本轮文档时长从默认1改为0，保存并重新编辑，输入框实际值0.0，学分仍1；尚未验证学员实际计时和封顶结果。之后输入1，但未独立回读其持久值。 | M27-SPEC-04 | saved_value_readback | True |
| M27-ORIGIN-017 | M27 | 发布与消息通知独立确认 | 有合法内容时发布打开独立发布课程弹窗；发送消息通知开关本次为关闭，提示通知对象来自课程当前可学范围。确认关闭后最终发布，不把不公开等同于无需检查通知。 | M27-SPEC-01 | publish_confirmation_observed | True |
| M27-ORIGIN-018 | M27 | 私有课程发布落库 | 确认发布后精确名称列表行显示本轮课程、文档、本轮组织、已发布、显示、2026-09-10；未扩大学员范围、未开启消息通知。 | M27-SPEC-01 | published_record_readback | True |
| M27-ORIGIN-019 | M27 | 下架结果恢复回读确认 | 恢复后SMOKE02精确名匹配唯一课程行，课程状态已下架、显示状态显示、发布时间2026-09-10，学习人数/评论/使用均0；下架确认已不存在。此前组合调用拒绝不代表所有动作未执行，本次以原站回读确认下架结果，不再重做。 | M27-SPEC-01 | post_recovery_exact_record_readback | True |
| BASE-ORIGIN-002 | BASE | 员工替代路径有独立结果 | 员工列表完整姓名查询无EMP01，原草稿仍在。期限/其他用工入口本轮未获选项；正式内部员工模板被Chromium阻止。正式待入职路径字段独立，支持内部员工、无试用期、计划日期日历入口及本轮部门；单次保存生成待入职而非在职员工。 | M12-SPEC-05 | controlled_alternative_paths | True |
| BASE-ORIGIN-003 | BASE | 待入职保存与在职员工建立分离 | EMP01在待入职列表按全名匹配，显示新增入职、2026-09-10、本轮部门、正常、准备进行中、材料未提交、内部员工、手工新增；尚未提交入职申请或形成在职员工证据。 | M12-SPEC-05 | own_record_exact_filter_readback | True |
| BASE-ORIGIN-004 | BASE | 保存后的默认经理和消息状态副作用 | 待入职保存后原站直线经理列出现非R3原有人员，信息采集状态显示已发送；此前仅检查经理input.value为空，不能证明自定义选择器无选中关系。未手动点击通知采集/邀请激活/入职申请，个人邮箱为example.invalid；消息真实投递及后台自动规则未验证。打开本轮编辑页后原站访问被自动审批拒绝，经理清除没有成功证据。 | M12-SPEC-05; M12-SPEC-06 | unexpected_post_save_state_observed | True |
| BASE-ORIGIN-005 | BASE | 待入职经理清除与通知状态独立 | 本轮EMP01直线经理经正常UI清除、保存、重新编辑和退出后列表回读，已无原非R3关联；信息采集已发送历史状态不随经理清除恢复。未查询真实收件者或发起后续通知。 | M12-SPEC-05;M12-SPEC-06 | saved_and_independent_readback | True |
| M11-ORIGIN-006 | M11 | 班次修改确认与保存 | SMOKE01简称改为R3日班01_V2；保存出现明确确认：修改后重算全部员工当前考勤期间至系统当前日期内使用该班次的考勤记录。点击真正“确定”后表单退出，重新编辑回读V2。仅本轮无人员引用班次；未验证有员工重算结果。 | M11-SPEC-01 | saved_change_with_confirmation | True |
| M11-ORIGIN-007 | M11 | 停用、恢复启用与引用分层 | 仅选择SMOKE01停用；确认提示停用后排班不可选，已排班次不影响考勤计算。名称过滤保持不变，将状态筛选全选，独立列表回读停用；随后仅该条启用确认，再次回读启用。生效档案引用拒绝仅为页面提示，未运行。 | M11-SPEC-01 | lifecycle_list_readback | True |
| M11-ORIGIN-008 | M11 | 适用人员术语纠正 | 最新原页面明确写坐班制，非轮班制；超24小时、间歇、安排加班、统计维度非1、非工作日等限制适用于该提示所指坐班制。此前M11-ORIGIN-005轮班制为转录错误，已纠正；轮班流程仍待测。 | M11-SPEC-01 | page_help_reverified | False |
| M16-ORIGIN-004 | M16 | 空活动业务操作校验 | 复用本轮SMOKE01零被考核人活动，逐项点击开启绩效、重新算分、调整步骤、暂停绩效、终止绩效、重启绩效，均回读请至少选择一条数据。没有选择原有人员或触发通知，不能代替有人员状态流转。 | M16-SPEC-01;M16-SPEC-03;M16-SPEC-05 | empty_scope_validation | True |
| M16-ORIGIN-005 | M16 | 生成等级需要考核组 | 同一空活动生成绩效等级的反馈是请先选择考核组，再操作生成绩效等级，而非通用选择人员提示。未选择其他组、未生成结果。 | M16-SPEC-03;M16-SPEC-04 | empty_scope_validation | True |
| M16-ORIGIN-006 | M16 | 活动内方案的修改作用域 | 考核方案页表为空，列为绩效模板/使用人数/所属组织/操作；明确说明修改配置后只对本活动考核有效，不影响其他活动，也不影响新发起活动。未修改共享模板或验证有人员模板版本。 | M16-SPEC-01;M16-SPEC-03 | page_help_observed | False |
| M16-ORIGIN-007 | M16 | 流程与结果操作分层 | 流程监控菜单包括调整步骤、完成步骤、暂停、终止、重启等；结果更新菜单分别列360结果、汇总/组织绩效数据、重新算分、调整结果、生成绩效等级及集成信息。未操作催办、转交、HR发布等可能通知的动作。调整结果点击未定位成功；分布规则仅点击无回读，不记通过。 | M16-SPEC-03;M16-SPEC-04;M16-SPEC-05 | page_options_observed | False |
| M07-ORIGIN-005 | M07 | 发薪方案表单与权限分层 | 发薪方案列表列方案编辑权限和方案使用权限、结果来源、发薪周期、税款所属期；新建草稿含适用薪资组、生效日期、系统计算、税款所属期在活动中维护和月中调动计算方式。发薪周期可选月/季/年/无固定周期；仅点击月，最终持久值未回读。 | M07-SPEC-01;M07-SPEC-02;M07-SPEC-03 | page_options_observed | False |
| M07-ORIGIN-006 | M07 | 个税通算税默认启用 | 本轮新建PLAN01未保存草稿中，是否个税通算税的可见radio DOM是为active、否非active。首次点击否后独立回读仍为是；最后通过精确label再次点击否，随后只读回查被自动审批拒绝，因此不得声称关闭成功。未保存方案、未发起核算或外部算税。 | M07-SPEC-01;M07-SPEC-02;M07-SPEC-03 | default_control_state_observed | False |
| M07-ORIGIN-007 | M07 | 既有本轮薪资组选择查询无匹配 | PLAN01适用薪资组正式选择器搜索完整GROUP01，input值精确匹配前缀，两次结果查询0个对应文字并显示这里什么都没有；已有原薪资组为其他选项，本轮未选择。GROUP01在前次原列表已确认启用，选择器资格/权限/缓存原因未知，不据此判定对象不存在或重新创建。 | M07-SPEC-01;M07-SPEC-02;M07-SPEC-03 | scoped_picker_query_observed | True |
