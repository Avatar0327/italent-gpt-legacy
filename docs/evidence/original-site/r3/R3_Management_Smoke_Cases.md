# R3 管理端冒烟与边界执行表

本表区分已执行、配置观察、局部完成和阻塞。步骤不拆分充数，数据量不等于完成度；旧证据不冒称续跑新测。五模块完整首包仍0/5。

| ID | 模块 | 场景 | 状态 | 依据/限制 |
|---|---|---|---|---|
| M27-RC-01 | M27 | 27对象中10课程逐名复核 | REVERIFIED | 10条均存在；不作为新增业务流程用例 |
| M27-RC-02 | M27 | 空章节发布拒绝 | VERIFIED | M27-ORIGIN-013 |
| M27-RC-03 | M27 | 合法文档上传、保存、发布主流程 | VERIFIED | M27-ORIGIN-015;018 |
| M27-RC-04 | M27 | 零时长持久值 | VERIFIED | M27-ORIGIN-016 |
| M27-RC-05 | M27 | 恢复1分钟持久值 | PARTIAL | 已输入1，持久值未独立回读 |
| M27-RC-06 | M27 | 私有/不共享/游客关闭管理配置 | VERIFIED_ADMIN_ONLY | 发布前DOM控件选中状态已读；不代表多角色 |
| M27-RC-07 | M27 | 发布通知关闭 | VERIFIED | M27-ORIGIN-017 |
| M27-RC-08 | M27 | 下架/撤回发布 | ENV_BLOCKED | 只有确认窗；未取得最终成功回读 |
| M27-RC-09 | M27 | 失效/再次启用 | ENV_BLOCKED | 原站访问被自动审批阻止后未执行 |
| M27-RC-10 | M27 | 课程聚合与考试尝试分层 | CONFIG_OBSERVED | 五选项已读；实际结果需学员及考试数据 |
| M27-RC-11 | M27 | 首次学习后同步策略锁定 | DEPENDENCY_BLOCKED | 缺本轮已入职学习者和测试身份 |
| M27-RC-12 | M27 | 导入预览/正式入库两阶段 | VERIFIED_PRIOR_RUN | 前轮9条确认后逐名回读；本轮不重复导入 |
| M27-RC-13 | M27 | 无数据模板辅助页 | VERIFIED_PRIOR_RUN | 前轮正式模板文件结构已验证；不重复导出原数据 |
| M27-RC-14 | M27 | 空内容草稿保存 | VERIFIED_PRIOR_RUN | 前轮本轮课程草稿已保存 |
| M27-RC-15 | M27 | 实际计时封顶和0值排除 | DEPENDENCY_BLOCKED | 帮助规则与字段保存不可代替学员运行 |
| M27-RC-16 | M27 | 员工/主管权限及完成证书 | ROLE_BLOCKED | 不能用管理员视角代替 |
| M16-RC-01 | M16 | 活动创建、周期日期回填、空参与人 | VERIFIED_PRIOR_RUN | M16-ORIGIN-001..003 |
| M16-RC-02 | M16 | 精准/条件/方案/导入参与人入口 | CONFIG_OBSERVED | 需模板和被考核人，未加入原有人 |
| M16-RC-03 | M16 | 目标模板 | ENV_BLOCKED | 未执行续跑增量 |
| M16-RC-04 | M16 | 权重边界 | ENV_BLOCKED | 未执行 |
| M16-RC-05 | M16 | 评分规则 | ENV_BLOCKED | 未执行 |
| M16-RC-06 | M16 | 校准配置 | ENV_BLOCKED | 未执行 |
| M16-RC-07 | M16 | 退回状态 | ENV_BLOCKED | 未执行 |
| M16-RC-08 | M16 | 锁定关系 | CONFIG_OBSERVED | 配置字段已见；状态运行未测 |
| M16-RC-09 | M16 | 最终结果与历史 | DEPENDENCY_BLOCKED | 无合成被考核人/活动结果 |
| M16-RC-10 | M16 | 审批与主管权限 | ROLE_BLOCKED | 未使用管理员冒充角色 |
| M12-RC-01 | M12 | 私有库创建、共享为空、AI关闭 | VERIFIED_PRIOR_RUN | M12-ORIGIN-002 |
| M12-RC-02 | M12 | 10份简历解析确认入库 | VERIFIED_PRIOR_RUN | M12-ORIGIN-003 |
| M12-RC-03 | M12 | 本轮候选人详情及业务编号 | VERIFIED_PRIOR_RUN | C00014235/236/243 |
| M12-RC-04 | M12 | 不同邮箱经历相同疑似对 | VERIFIED_PRIOR_RUN | M12-ORIGIN-004 |
| M12-RC-05 | M12 | 01/09取消疑似9变8 | VERIFIED_PRIOR_RUN | M12-ORIGIN-005；本轮未再次取消 |
| M12-RC-06 | M12 | 取消关系重载持久性 | ENV_BLOCKED | 未重载验证 |
| M12-RC-07 | M12 | 正式待入职保存替代路径 | PARTIAL_WITH_SIDE_EFFECT | BASE-ORIGIN-002..004；未形成在职员工 |
| M12-RC-08 | M12 | 招聘需求/编制草稿 | ENV_BLOCKED | 后续原站访问全站拒绝 |
| M12-RC-09 | M12 | 职位与阶段流转 | ENV_BLOCKED | 未执行，未发布真实职位 |
| M12-RC-10 | M12 | 面试评价草稿 | ENV_BLOCKED | 未执行，未发邀请 |
| M12-RC-11 | M12 | Offer草稿 | ENV_BLOCKED | 未执行，未外发 |
| M12-RC-12 | M12 | 候选人到在职员工完整衔接 | DEPENDENCY_BLOCKED | 待入职单独新建，不冒称候选人转入职成功 |
| M12-RC-13 | M12 | 隐私及不同角色 | ROLE_BLOCKED | 无明确隔离身份 |
| M11-RC-01 | M11 | 3条固定班次新增复制回读 | VERIFIED_PRIOR_RUN | M11-ORIGIN-003 |
| M11-RC-02 | M11 | 工作日变化后的半天选项 | CONFIG_OBSERVED | M11-ORIGIN-002 |
| M11-RC-03 | M11 | 已有排班不联动提示 | CONFIG_OBSERVED | M11-ORIGIN-004；版本运行未测 |
| M11-RC-04 | M11 | 停用与引用拒绝 | ENV_BLOCKED | 未执行续跑增量 |
| M11-RC-05 | M11 | 轮班限制 | CONFIG_OBSERVED | M11-ORIGIN-005；未实测拒绝 |
| M11-RC-06 | M11 | 跨日边界 | ENV_BLOCKED | 未执行 |
| M11-RC-07 | M11 | 加班配置与补卡 | ENV_BLOCKED | 未执行 |
| M11-RC-08 | M11 | 空人员排班草稿 | ENV_BLOCKED | 未执行 |
| M11-RC-09 | M11 | 异常/月末计算 | DEPENDENCY_BLOCKED | 无本轮在职员工及打卡数据 |
| M11-RC-10 | M11 | 权限角色 | ROLE_BLOCKED | 无隔离身份 |
| M07-RC-01 | M07 | 独立组必填校验、部门范围和保存 | VERIFIED_PRIOR_RUN | M07-ORIGIN-003..004 |
| M07-RC-02 | M07 | 方案/周期/权限配置 | CONFIG_OBSERVED | M07-ORIGIN-001；方案此前取消未保存 |
| M07-RC-03 | M07 | 月中调动与个税通配置 | CONFIG_OBSERVED | M07-ORIGIN-002；未调用外部服务 |
| M07-RC-04 | M07 | 固定/变动薪资项 | ENV_BLOCKED | 未执行续跑增量 |
| M07-RC-05 | M07 | 公式与版本 | ENV_BLOCKED | 未执行 |
| M07-RC-06 | M07 | 补发补扣追溯 | ENV_BLOCKED | 未执行 |
| M07-RC-07 | M07 | 锁定/解锁/审批 | ENV_BLOCKED | 未执行 |
| M07-RC-08 | M07 | 空人员核算拒绝 | ENV_BLOCKED | 未执行 |
| M07-RC-09 | M07 | 报表和历史 | ENV_BLOCKED | 未执行 |
| M07-RC-10 | M07 | 工资对象及权限角色 | DEPENDENCY_AND_ROLE_BLOCKED | 无本轮在职员工和隔离身份 |

## M11增量 2026-09-10T14:19:17.787553+00:00

M11-RC-11/12/13已执行并回读；RC-03/04部分完成；RC-05纠正为坐班制提示。当前不能将这些用例视为有员工排班/月份结算或完整首包通过。

## M27恢复增量 2026-09-10T14:21:42.644508+00:00

M27-ORIGIN-019现更新为已验证：SMOKE02精确行状态已下架，显示状态仍显示、发布时间2026-09-10，确认窗不存在。未重复下架。此前无成功证据的结论由这次回读补齐。R3-DIFF-007（Minor，M27-SPEC-01）补充本证据；建议R3 P2设计负责人明确课程发布、下架、显示等独立状态，仍待接收。未验证失效、1分钟最终持久值、学习后锁定实际行为及多角色。首包尚未达标。

## M16增量 2026-09-10T14:23:07.383003+00:00

RC-11..17为七条已执行校验边界，RC-18仅配置观察。没有将空范围拒绝视为评分、退回、锁定或校准流程完成。模板、权重和有人员流程仍未完成，首包未达标。

## M07本次增量 2026-09-10T14:26:41.428534+00:00

RC-11默认开关只读观察；RC-12精确组查询已执行但未匹配；RC-13关闭动作缺回读且ENV阻塞。无新方案入库、无核算、无外部调用，首包未达标。
