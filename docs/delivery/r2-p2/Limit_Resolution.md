# LIMIT消解与P3/P4责任矩阵

原始LIMIT为6组，完整关闭0组；6组均仍有P3和P4责任（两个6相互重叠，不能相加为12组）。拆成52个互斥责任子项：P2设计关闭15，转P3验证25，转P4核证/验收12。P2设计关闭不是源操作已验证。

|原LIMIT|P2设计关闭|P3验证|P4核证/验收|
|---|---:|---:|---:|
|M37-LIMIT-01|2|3|2|
|M06-LIMIT-01|2|4|2|
|M26-LIMIT-01|3|4|2|
|M18-LIMIT-01|2|4|2|
|M17-LIMIT-01|3|5|2|
|M03-LIMIT-01|3|5|2|

逐项事实、设计引用、关闭条件和责任见Limit_Resolution.json；原文保持在Original_Limits.json。六基础运行风险单列，不额外增加原LIMIT分母。

原站差异并非要求产品复制所有未知行为；已批准独立规则优先。只有真实迁移/接入依赖某个未知来源ID或语义时，该对象保持隔离并核证。生产能力/隐私/恢复未验不能据设计闭环放行。

## 独立评审后六项重新提请关闭

原52项阶段标签不改分母。独立评审仅接受9项；下列6项已有逐项文档证据，设计负责人重新提请P2关闭，仍待独立复核。P3=25/P4=12、原组完整关闭0均保持。

|子项|发现|重新提请依据|文档探针|
|---|---|---|---|
|M37-LIMIT-01.01|R2-EXIT-001|逐等级alias/elementText/subsetName及父指标/level/version规范持久化，来源联合按命令限制；旧尺度与独立审核保持|LEVEL-VALID, LEVEL-EXTRA, LEVEL-VERSION, LEVEL-SOURCE, LEVEL-MISSING, REF-COMMAND-VALID, REF-COMMAND-SOURCE|
|M06-LIMIT-01.01|R2-EXIT-001|指标类型isCommon/说明行/评分模式及数值尺度、评级方案精确版本；资格级别不混用，目录与标准冻结链确定|TYPE-VALID, TYPE-RATING-VALID, TYPE-EXTRA, TYPE-VERSION, TYPE-SOURCE, TYPE-MISSING, TYPE-EXACT-VERSION|
|M26-LIMIT-01.01|R2-EXIT-001|逐题角色/维度/指标版本和条件显示绑定闭合，套卷列表不再推断逐题关系，原卷/邀请根不改|QUESTION-VALID, QUESTION-EXTRA, QUESTION-VERSION, QUESTION-SOURCE, QUESTION-MISSING|
|M26-LIMIT-01.02|R2-EXIT-002|答卷ID/单题atom谱系/报告版本/关联伪名与向量分组严格分离；首报放行、差分及双阈值拒绝，账本epoch不清历史|ANON-01, ANON-02, ANON-03, ANON-04, ANON-05A, ANON-05B, ANON-06A, ANON-06B, ANON-07A, ANON-07B, ANON-07C, ANON-08A, ANON-08B, ANON-08C, ANON-09, ANON-10|
|M18-LIMIT-01.01|R2-EXIT-001|项目create/save明确previousResultRef或null；历史发布集根/版本/asOf/字段白名单/用途和关系严格可表达|HISTORY-VALID, HISTORY-EXTRA, HISTORY-MISSING|
|M18-LIMIT-01.02|R2-EXIT-001|历史项目同人映射和精确版本核验，不预填为当前评定、不向M17自动生效；历史未知隔离及旧版本保留|HISTORY-VALID, HISTORY-NONE-VALID, HISTORY-VERSION, HISTORY-SOURCE|
