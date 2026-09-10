# R3 原站行为矩阵

运行：R3-ORIGIN-20260910-103900。41项分层观察，29条确认对象；完整首包0/5。实际操作、页面说明和未完成确认分别记录，未作复刻、角色或P4验收。

| ID | 模块 | 观察 | 层级 | P1依据 | 本行实际验证 |
|---|---|---|---|---|---|
| M27-ORIGIN-001 | M27 | 课程表单分基本信息、课程内容、学习规则、课程激励、可学范围、学习资料、本课概要；标题/所属部门/所属目录必填 | page_observed | M27-SPEC-01 | 否 |
| M27-ORIGIN-002 | M27 | 添加课件/课程/问卷/考试/作业必须保存或提交；直接退出不保存添加内容 | page_help_observed | M27-SPEC-01 | 否 |
| M27-ORIGIN-003 | M27 | 文档/图文/URL/云文档课件单次学习时长按配置课件时长封顶；配置0不计学习时长 | page_help_observed | M27-SPEC-04 | 否 |
| M27-ORIGIN-004 | M27 | 课件进度同步/不同步选项提示：本课程有学员学习后无法再次修改 | page_help_observed | M27-SPEC-02 | 否 |
| M27-ORIGIN-005 | M27 | 不设置；所有考试最高分；所有考试成绩平均；每场考试最高分之和/场数；指定考试最高分 | page_options_observed | M27-SPEC-03 | 否 |
| M27-ORIGIN-006 | M27 | 管理员共享只授使用而不授编辑；学员公开决定课程中心可检索；不公开仍可通过学习计划/培训项目/岗位学习学习 | page_help_observed | M27-SPEC-01 | 否 |
| M27-ORIGIN-007 | M27 | 本次新建课程默认不共享管理员、公开且公司全员可见、游客关闭；已改本轮草稿为不公开 | default_and_form_change_observed | M27-SPEC-01 | 否 |
| M27-ORIGIN-008 | M27 | 额外积分输入提示0~1000；签名有无需/电子签/手写；证书与勋章独立配置 | page_options_observed | M27-SPEC-05 | 否 |
| M27-ORIGIN-009 | M27 | 不添加课件可保存；本次新课程列表状态未发布，学习人数0 | saved_record_readback | M27-SPEC-01 | 是，仅本行 |
| M27-ORIGIN-010 | M27 | 一次最多5000；支持新增/更新/新增或更新；空格不处理/清空；课程ID空或不匹配新增，匹配更新，自定义ID无效；部门空默认操作者管理单元 | page_help_observed | M27-SPEC-06 | 否 |
| M27-ORIGIN-011 | M27 | 模板选择不含数据仍附带课程、课件、部门等辅助参考页；本轮重新生成仅含虚构课程主表后上传 | download_structure_observed | M27-SPEC-01 | 是，仅本行 |
| M27-ORIGIN-012 | M27 | 上传导入后先出现九条预览并分配ID；仍需确认导入，预览ID不等于业务落库证据 | import_preview_observed | M27-SPEC-06 | 是，仅本行 |
| M16-ORIGIN-001 | M16 | 活动含组织/向下公开/组织绩效影响分布/异常处理人类型和指定人/锁定考核关系；员工绩效与组织绩效、目标、OKR独立菜单 | page_options_observed | M16-SPEC-01 | 否 |
| M16-ORIGIN-002 | M16 | 选择2026年度、第三季度后自动填入2026-07-01至2026-09-30；日期仍作为独立字段展示 | form_change_readback | M16-SPEC-01 | 是，仅本行 |
| M16-ORIGIN-003 | M16 | 本轮活动保存后详情页无被考核人；添加被考核人有精准/条件/方案/导入，精准添加要求模板和人员 | saved_activity_detail_observed | M16-SPEC-01 | 是，仅本行 |
| BASE-ORIGIN-001 | BASE | 电子邮箱/入职日期/部门/试用标志必填；邀请激活默认否；公司默认已带出且保存提示劳动合同期限类型必填。未生成签署；表单保存被拒绝 | validation_rejected | M12-SPEC-05 | 是，仅本行 |
| M12-ORIGIN-001 | M12 | 应聘者支持单个/批量/系统模板/成绩导入；手工姓名必填；关联职位和人才库至少一项；渠道必填 | page_options_observed | M12-SPEC-01 | 否 |
| M12-ORIGIN-002 | M12 | 个人库名称最多50字；共享部门/共享人可空；AI推荐默认关闭；本轮个人库已保存，不共享 | saved_record_readback | M12-SPEC-06 | 是，仅本行 |
| M12-ORIGIN-003 | M12 | 批量最多500文件、单文件不超过50M为页面提示；本轮10份UTF8虚构txt已提交并在指定私有库逐条回查，姓名保留前缀、性别保密、学历本科 | ten_records_readback | M12-SPEC-06 | 是，仅本行 |
| M11-ORIGIN-001 | M11 | 固定/弹性/自由班次；日期工作日/节假日/公休日；手动/工作日历日期设置；统计天数与工作分钟数分开 | page_options_observed | M11-SPEC-01 | 否 |
| M11-ORIGIN-002 | M11 | 按工作时长一半、固定时点、首个休息时段开始三种；工作日选定后本轮分割字段曾清空，需重新选择 | form_change_observed | M11-SPEC-01 | 是，仅本行 |
| M11-ORIGIN-003 | M11 | 当日09:00-17:00计算480分钟；本轮SMOKE01和02保存并精确名称回查，仅本轮组织且不下级共享；复制保留配置并添加副本后缀 | saved_record_readback | M11-SPEC-01 | 是，仅本行 |
| M11-ORIGIN-004 | M11 | 修改安排加班不会影响已有排班，需重新排班；生效考勤档案/考勤档案规则使用的班次不支持停用（页面提示） | page_help_observed | M11-SPEC-01 | 否 |
| M11-ORIGIN-005 | M11 | 页面提示不支持轮班制员工使用：工作/取卡范围超24小时、间歇、安排加班、统计天数非1、非工作日班次；尚未实测拒绝 | page_help_observed | M11-SPEC-01 | 否 |
| M07-ORIGIN-001 | M07 | 新方案要求适用薪资组、周期、方案使用权限；结果来源系统计算；税款所属期在发薪活动维护；独立组未建前本轮方案未保存 | page_options_observed | M07-SPEC-01 | 否 |
| M07-ORIGIN-002 | M07 | 方案有个税通算税是/否；月中调动可分别独立核算或调入方核算全月；本轮尚未核算及调用个税通 | page_options_observed | M07-SPEC-02; M07-SPEC-03 | 否 |
| M07-ORIGIN-003 | M07 | 薪资组有编码、名称、上级、状态、对应部门；本轮新组织可被部门选择器检索，不等于已创建可用薪资组 | form_selection_observed | M07-SPEC-01 | 否 |
| M07-ORIGIN-004 | M07 | 缺上级保存拒绝；选择默认根组作为引用，仅关联本轮部门且不含下级后保存；精确过滤回读启用行。未创建核算活动。 | validation_and_save_readback | M07-SPEC-01 | 是，仅本行 |
| M12-ORIGIN-004 | M12 | SMOKE01(C00014235)提示9个疑似；展开确认SMOKE09(C00014243)为84%疑似，两者邮箱不同、经历相同。仅证明此对结果，未推导算法、阈值或其余8对明细。 | comparison_panel_observed | M12-SPEC-01; M12-SPEC-06 | 是，仅本行 |
| M12-ORIGIN-005 | M12 | 只对本轮01与09点取消疑似；确认提示取消后不再判定两人为疑似；确认是后比较窗9变8，详情头部当时仍9。未合并删除，持久抑制和重载一致性待测。 | action_confirmed_by_panel_readback | M12-SPEC-01; M12-SPEC-06 | 是，仅本行 |
| M12-ORIGIN-006 | M12 | 本轮txt已解析并显示标准字段；详情原始简历预览显示This page has been blocked by Chromium。未绕过浏览器限制；不归因于招聘业务规则。 | browser_preview_error_observed | M12-SPEC-06 | 是，仅本行 |
| M27-ORIGIN-013 | M27 | SMOKE02在私有、未发布且1章0节时点发布，原站明确拒绝：当前课程章节无内容无法发布，请添加内容! | validation_rejected | M27-SPEC-01 | 是，仅本行 |
| M27-ORIGIN-014 | M27 | 上传课件先打开上传面板，点击点此上传才出现文件选择器。页面支持PDF等文档，提示文档300MB、音视频10GB、Scorm1.2 ZIP 1GB；上限未实测。 | upload_ui_help_observed | M27-SPEC-01 | 否 |
| M27-ORIGIN-015 | M27 | 一页虚构PDF上传完成后需确认标题/所属部门/目录；确认后课程为1章1节、文档转码完成，默认1分钟、1学分；课程保存后重新编辑仍有本轮课件。 | upload_and_saved_record_readback | M27-SPEC-01; M27-SPEC-06 | 是，仅本行 |
| M27-ORIGIN-016 | M27 | 把本轮文档时长从默认1改为0，保存并重新编辑，输入框实际值0.0，学分仍1；尚未验证学员实际计时和封顶结果。之后输入1，但未独立回读其持久值。 | saved_value_readback | M27-SPEC-04 | 是，仅本行 |
| M27-ORIGIN-017 | M27 | 有合法内容时发布打开独立发布课程弹窗；发送消息通知开关本次为关闭，提示通知对象来自课程当前可学范围。确认关闭后最终发布，不把不公开等同于无需检查通知。 | publish_confirmation_observed | M27-SPEC-01 | 是，仅本行 |
| M27-ORIGIN-018 | M27 | 确认发布后精确名称列表行显示本轮课程、文档、本轮组织、已发布、显示、2026-09-10；未扩大学员范围、未开启消息通知。 | published_record_readback | M27-SPEC-01 | 是，仅本行 |
| M27-ORIGIN-019 | M27 | 只选择本轮SMOKE02，更多操作下架后出现是否要执行此操作确认；最终确认与经理清除组合操作被自动审批拒绝，未获得下架成功回读。保留最后确认状态已发布。 | action_confirmation_observed_not_completed | M27-SPEC-01 | 否 |
| BASE-ORIGIN-002 | BASE | 员工列表完整姓名查询无EMP01，原草稿仍在。期限/其他用工入口本轮未获选项；正式内部员工模板被Chromium阻止。正式待入职路径字段独立，支持内部员工、无试用期、计划日期日历入口及本轮部门；单次保存生成待入职而非在职员工。 | controlled_alternative_paths | M12-SPEC-05 | 是，仅本行 |
| BASE-ORIGIN-003 | BASE | EMP01在待入职列表按全名匹配，显示新增入职、2026-09-10、本轮部门、正常、准备进行中、材料未提交、内部员工、手工新增；尚未提交入职申请或形成在职员工证据。 | own_record_exact_filter_readback | M12-SPEC-05 | 是，仅本行 |
| BASE-ORIGIN-004 | BASE | 待入职保存后原站直线经理列出现非R3原有人员，信息采集状态显示已发送；此前仅检查经理input.value为空，不能证明自定义选择器无选中关系。未手动点击通知采集/邀请激活/入职申请，个人邮箱为example.invalid；消息真实投递及后台自动规则未验证。打开本轮编辑页后原站访问被自动审批拒绝，经理清除没有成功证据。 | unexpected_post_save_state_observed | M12-SPEC-05; M12-SPEC-06 | 是，仅本行 |

管理端冒烟完成度见R3_Management_Smoke_Cases.md；逐行时间和来源见同名JSON。

| BASE-ORIGIN-005 | BASE | 待入职经理清除成功，历史采集状态独立 | M12-SPEC-05/06 | 已保存并独立回读；非在职员工 |
