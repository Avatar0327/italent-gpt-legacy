# 六项非模块基础能力的R2适用差异

<a id="r2-baseline-01"></a>
## 批准范围和计数

R2-BASELINE-01已批准完整四模块规格及六基础r2Assessment；M37/M06此前独立批准继续有效。六基础不变成六个新模块，不进入15模块或原6个LIMIT分母，不维护总控状态。基础设计依R1固定契约，本轮只设计R2适配，没有声称基础实现/业务/生产验收通过。

<a id="base-01"></a>
## BASE-01 身份与登录

同一personId用于M06申请、M26subject/reviewer、M18subject、M17mentor/member/successor、M03cadre；平台user、member、employee绑定分立。当前会话两次授权校验/安全epoch及退出屏障沿R1，ID参数不能选本人，原StaffID/外部码带namespace。解绑/离职阻新答卷、申请、转正/任用及职责动作，历史身份不覆写；有权历史关闭/终止仍可办理。

映射BASE-01-AC01/02及M26-REVIEW-AC10；P3需合成身份/跨租户/恢复旧绑定拒绝，P4核当前可信撤权来源；E2不增实际访问者。设计定位Architecture#objects、Permissions#authorization/recusal、Recovery#recovery。

<a id="base-02"></a>
## BASE-02 角色、组织范围和字段权限

新增明确敏感域：360桥接/原卷、潜力/九格、后备排名/退池讨论、访谈、委员会票/原材料。管理、review、publish、export不互继承；人员/岗位/池/项目及动态角色按完整grant元组求值。先授权后筛选/排序/聚合，防隐藏字段计数泄漏。历史关系不授当前权，经理/admin/HR不是所有敏感权限的总开关。

BASE-02-AC01～03和M03-REVIEW-AC11覆盖行/列/动作、历史及附件；额外M26披露账本和差分场景不以普通RBAC测试替代。P3安全/域适配负责人提供直接API拒绝矩阵；P4实际多角色/用途验收由总控安排，当前不邀请新成员。

<a id="base-03"></a>
## BASE-03 审计日志

评价/校准/规则入出池/授证/任免必须与业务版本、command receipt、outbox、恢复行日志同租户CAS提交，审计失败全回滚。旧development events完整payload不能直接沿用为通用审计；答卷桥接、评分/访谈原文放专用受控对象，通用日志只有ID/动作/版本/hash和安全引用。DB不可写不承诺同DB有失败日志。

BASE-03-AC01/02及M17-REVIEW-AC03原ID保留，另以M03审计失败/两域生效差异和自动规则逐项失败补足实际事务断言。P3证明事务和脱敏，P4安全审计人员核访问及保留政策。

<a id="base-04"></a>
## BASE-04 附件与历史版本

标准子集、题卷、答卷、报告、盘点快照、IDP成果、任期及档案附件均有不可变ownerVersion/purpose/manifest。上传先不可见字节后D1绑定，孤儿不可下载；下载前后当前授权，deny/tombstone立即阻读，物理清理必须无存续恢复点引用。旧已下载字节不能承诺召回，业务历史不等30天备份TTL。

BASE-04-AC01～04及M26-REVIEW-AC09保留，P3核撤权晚回、旧链接/历史域权限和损坏对象；P4核存储、密钥及合法材料保留。原始回执、审计摘要与内容read权分立。

<a id="base-05"></a>
## BASE-05 数据备份和异常恢复

RPO≤60分钟/RTO≤240分钟/保留30天；R2必须加入共享完整事务日志和不可变文件manifest，含M26披露账本/桥接、资格撤销、继任复核、任用receipt及当前安全deny。恢复先隔离、核签名/对象、校准当前授权、业务对账和所有者开放。平台概览可见DB工具不证明官方export/import、调度、独立密钥及恢复吞吐可用。

P2已确定能力需求、恢复状态、预算及成本公式；R1历史证据无法证明本轮平台运行能力。当前工具目录只发现数据库概览/表行读取，没有备份/恢复/定时执行专用工具；这只说明本窗口未暴露该接口，不能断言平台没有能力。未运行真实导出/恢复或读取人员行。能力实证交P3平台门槛及P4真实演练，未满足阻相关生产开放，目标不降。

BASE-05-AC01/02原ID保留。Scope中M03-REVIEW-AC14只验legacy任期未伪造批准，不能证明恢复目标；补充RECOVERY场景专门覆盖数据库+对象共同恢复点、撤权、披露账本和计时。此处是明确的覆盖补足，不修改Scope原映射。

<a id="base-06"></a>
## BASE-06 外部接口预留

六域统一VersionRef、Envelope、purpose白名单、canonical摘要、签名信任、inbox/outbox/请求墓碑及unknown对账。M37外部成就/测评、M26提醒、M03奖励支付/签署均仅接口与not_configured状态，不使用真实服务。业务状态、审批状态、通知状态分立，未配不能模拟成功；供应商unknown不盲重发。

BASE-06-AC01～03和M18-REVIEW-AC13保留，P3合成签名错误、乱序、同ID异digest、未知响应、撤权测试，P4真实集成按另外授权范围验证；不恢复33暂缓模块或独立AI。

## 责任与依赖

六基础设计应用至六模块，不建第二身份/工作流/命令/恢复引擎。R1共享能力负责人交付可用契约版本，R2各域做适配，独立测试核组合拒绝，P4业务、安全、运维各自签证。未实际联调统一realIntegration=not_executed；模块设计闭环与基础运行验证分开。

三项定向适配的具体对象、动作、角色字段和版本断言见[Foundation_Adaptations.md](Foundation_Adaptations.md)，原AC独立来源保留。
