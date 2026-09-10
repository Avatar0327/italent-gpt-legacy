# 给独立评审窗口的精确复核范围

原评审固定bd976480fad9822ee52ecb4b00a080360772b0f3，原被审包装8b3daf9270181ffe2e77015be723da8e611d83a5，原内容7ff3a28c7660dac658d5243d7c4535a9c8037fc2。新内容与包装引用见最终Controller_Proposal及Repair_Delivery_Record；本内容文件不嵌自身SHA。

|发现|新内容复核文件/指针|必须满足的复核条件|
|---|---|---|
|001|Contract_Repair；Interface_Schemas.$defs VersionRef/InternalVersionRef/ExternalVersionRef/IndicatorChild/CatalogDraft/Question/QuestionnaireDraft/PreviousResultRef/ReviewProject；Command_Registry.commands[*].referencePolicy；Schema_Examples|五组批准字段规范对象/持久化/版本/来源可唯一决定；各支封闭；34个实例按预期9接受25拒绝，尤其完整Command仅achievement允许外部来源；trace中targetedRepairMappings与原AC下targetedRepairAssertions一致|
|002|M26_Design.repair-002；Anonymity_Repair/Cases/Calculation；DisclosureAtom/Cell/LedgerEntry/Plan/SubjectContribution及ReportPublish.disclosurePlanVersionRef|逐格独立重算16例5可发布11抑制；首报ABC同类3，改A新旧atom分别1，三重111类1；组织双阈值、named边界、撤回和epoch连续性一致|
|003|Foundation_Adaptations；Acceptance_Scenarios中的R2-P3-BASE-02-AC03/03-AC02/04-AC02与originalFoundationGwt；build_foundation_adaptations/repair_handoff|原AC/basis不变，R2夹具直接确定动作/角色/字段/版本结果；桌面表三项不当产品执行|
|004|Task_Dependencies；P3_Work_Packages.tasks[*].dependencies；build_dependencies|46任务逐项前置、schema/adapter/security/migration/recovery字段齐全；A/B/C均pending_owner_freeze；全图55节点165边无环；R1-10真实联合收口不循环|
|六项LIMIT|M37-LIMIT-01.01、M06-LIMIT-01.01、M26-LIMIT-01.01/.02、M18-LIMIT-01.01/.02的repairProof|逐个核probe ID和当前输入/证据SHA；9原接受+6重提，不把重提视独立认可；P3 25/P4 12逐字段保持，原整组关闭0|

执行范围限文档生成/解析、Draft202012验证、符号矩阵、桌面表、拓扑、来源/哈希及反查。rebuild_repair.py需隔离jsonschema==4.23.0；check_rebuild.py验证生成无漂移；check_design.py检查全部文档。切勿运行产品或P3业务测试。新schema实例探针34与原P3场景138分母分开，后者全部not_run。

相关受影响原门禁：M37-01/05、M06-01、M26-01/03/04、M18-01、H-10/18/19、E-02/04/07。其他已通过设计控制保持，M17/M03仅共用引用澄清；005/006继续未来责任。复核应检查变更没有反向破坏原已接受控制，但不必重做其他六模块领域设计。
