# 阅读与复核覆盖记录

评审对象固定为8b3daf9270181ffe2e77015be723da8e611d83a5；设计内容固定为7ff3a28c7660dac658d5243d7c4535a9c8037fc2。完整字节读取、JSON解析与哈希记录见Read_Hash_Manifest.json；逐项实质判断见Requirement_Review和Critical_Gates。本记录不把哈希成功等同于实质通过。

|材料|阅读/复核方法|结果落点|
|---|---|---|
|Exit_Review.md、Architecture.md、Cross_Module_Contracts.md、Permissions.md、Interfaces.md|完整读取；逐条核决策权、时态、事务及权限边界|Critical_Gates 56项|
|Migration_Rollback.md、Recovery_Cost_Responsibilities.md、Foundations.md|完整读取；对不可逆风险、当前deny和实际开放条件逐条推演|Limit_Review 52项；003/006|
|M37/M06/M26/M18/M17/M03_Design.md|六份完整读取；按对象、规则、权限、状态、异常、迁移和验收逐模块审查|30个模块门禁及33个批准需求判断|
|Interface_Schemas.json、Command_Registry.json|完整解析69个定义和76个动作；展开本地引用、封闭对象、required、正则、全部条件绑定；与正文关键输入双向比较|Mechanical_Verification；Semantic_Probes；001|
|Requirements_Trace.json|完整解析；33项原文全部阅读；295条按原文确定拆分逐条比对；149项字段/角色/状态源值全部核对；24关闭条目及6基础逐项读取|Requirement_Review；源文本去重与锚点核验|
|Acceptance_Scenarios.json|完整解析；94项批准GWT全部读取，44项补充场景与其生成源逐项读取；全部任务和证据字段核验|138项未执行，003及关键门禁场景引用|
|P3_Work_Packages.json|全部46项读取，任务/场景双向唯一链接与状态核；通用重复依赖文字归并检查，不忽略不同任务内容|004；46项独立排序建议|
|Original_Limits.json、Limit_Resolution.json|6组原文及52子项全部读取；每项阶段、所有者、标准及来源核验|15/25/12；6项P2声明暂不接受|
|Legacy_Acceptance_Map.json|17项原GWT及当前处置、5个父任务和5个criterion全部读取反查|原事实保留，当前批准优先，来源请求不冒产品用例|
|Source_Requests.json、Source_Manifest.json|完整读取/解析；全部78个ref/path/SHA/byte逐对象核验|未核原站UUID/流程节点等维持局部来源责任|
|Artifact_Manifest.json、Approval_Provenance.json、Controller_Proposal.json|完整解析；两份清单分别在其对应HEAD核验；7批准记录与Scope逐值相同；11固定引用全部核|无失效来源、循环哈希或固定/动态混比|
|Review_Round1.md、Review_Round2.md、Resume.md|完整读取；仅作为设计窗口自检输入；不继承其结论|两项独立Major来自重新交叉核对|
|build_inventory.py、build_resolution.py、build_scenarios.py、build_schemas.py、build_handoff.py、check_design.py|完整读取；前5脚本仅在临时副本复建；最后脚本因写清单/证据未直接执行|无生成漂移；独立638项核验替代盲信自检|
|Historical_Test_Provenance.json及历史证据索引|完整解析并读取历史状态限定；历史TAP只作为源引用|未复跑、未计入当前R2证据|

## 来源反查

P1最终关闭材料、P1_R2_P2_Handoff及Scope中的批准记录/需求/契约/验收预期已读取。六模块原评审包按固定批准对象读取相关章节；每模块首末SPEC共12项反查原文出现在批准时评审包，并验证整个评审包SHA。33批准文本、149契约和111个源AC记录均做源值全量对照。抽样不是用来替代关键规则全查；关键规则另有56项独立门禁。

R1共享Architecture、Interfaces_Exceptions、Consistency_Resolutions及11个P3工作包完整读取；M01时态身份、M19事务适配/D7、M48消费授权、M32当前/快照与字段数据集、迁移/回滚/备份和恢复目标按本次依赖反查。R1固定来源14份文件均有Git对象SHA核验。R1 P3真实工作树只读观察，恢复记录按最新覆盖段解读；在制文件保留，未作为设计完成证据。

对于重复生成段（例如所有条款继承父场景族、模块关闭项共同风险描述），完整结构逐项解析，语义相同文本归并阅读，不把重复引用多计为独立验收断言。没有将“JSON能解析”或“生成器无错”当作设计完整性的充分条件。
