# 定向返修整体自检第一轮

范围：001–004及其直接依赖；独立评审bd976480原判断为验收标准，不重做已接受模块。结论：本轮设计方复核通过，可提交第二轮反查；不等独立评审接受或所有者批准。

|检查域|重新核对结果|证据|
|---|---|---|
|五组严格输入与批准语义|内部/外部kind联合、逐等级字段、指标类型配置、每题映射、历史参考均有规范持久化和版本关系；命令白名单限制外部路径|Contract_Repair、Interface_Schemas、Command_Registry|
|来源与版本正反例|34实例：9合法、25拒绝；含未知字段、缺必填、错误来源/版本/评级级别及完整Command的外部引用路径反例；Draft202012元schema通过|evidence/repair-001-schema.json|
|M26版本和匿名|不可变整卷ID不入分组签名；answerAtom谱系保留改答差分；稳定伪名跨披露关联，参与/系数向量及组织双阈值决定分组|Anonymity_Repair、Anonymity_Calculation|
|匿名正反表|16组独立有理数计算，5发布、11抑制；首次ABC=4合法，改A后5与4差分拒绝；两两可过的第三重交叠拒绝；撤回不清旧列|evidence/repair-002-anonymity.json|
|当前授权/审批与生效|修订字段不从role名推授权；外部不冒审批/资格/人事回执；M26 plan绑定当前账本/epoch，仍独立审阅发布|Permissions、Interfaces、各模块原控制及定向补充|
|三基础AC|原GWT/basis保留；报告投影/原卷、目录改名/证书撤销、报告版本附件各有夹具、角色、动作、字段和版本结果|evidence/repair-003-desktop.json|
|任务依赖|46任务绑定具体schema/adapter及A/B/C；55全图节点、165边、无环；所有实现槽位待冻结，R1-10与真实R2/R3联合收口|evidence/repair-004-dag.json|
|迁移/回滚/恢复|新必填来源不足隔离；不复制父级alias到逐级、不把整卷列表当逐题、不造历史；固定分区或账本不可核不新披露；旧版本及独立deny保持|Contract_Repair、Anonymity_Repair；既有Migration/Recovery不降标|
|LIMIT|原接受9+本轮6逐项重提；每项有确切探针ID和证据SHA；25P3/12P4保留，整组0|Limit_Resolution|

本轮扩大定向断言以覆盖缺必填和完整Command白名单，补M37维度子对象生成/归属及匿名SubjectContribution/DisclosurePlan严格契约。移除未获来源支撑的数值precision=18上限，保留明确非负精度和尺度一致校验。一次检查脚本编辑出现括号错误，已修正后完整重建；不得以失败运行作为通过证据。001误跟踪的两个本目录Python缓存已在003删除，目录ignore防复现。

整体文档检查1007项、反向追踪773项无失败；上述为文档核验，产品执行次数0，138场景not_run。旧Review_Round1/2保持历史原文，不充当本轮证据。
