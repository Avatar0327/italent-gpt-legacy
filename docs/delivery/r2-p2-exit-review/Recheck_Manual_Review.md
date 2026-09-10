# 定向实质审查与手工复算

唯一设计内容dc6dd896fbf388b70069ecb756547f85ee89d08a，包装a7a23d6bff024f4660fd14b0c22f47a6d40d928f。以下是独立判断，不是作者自检摘录，不是产品测试。原批准范围以固定main 22be3a7及原独立评审bd976480保留的来源为准。

## 001 五组契约逐项判断

|对象组与批准来源|规范写入/持久化/版本|禁止组合与核验结论|
|---|---|---|
|VersionRef；M37-SPEC-05|Contract_Repair“引用联合与来源守卫”；Internal/External两支封闭，内部复合根/版本核revision/digest，外部不可变capture+信任契约/asOf；Command_Registry逐动作白名单|禁止缺kind推断；external仅standard.create/edit的achievement来源；审批/角色/尺度/资格/材料/历史结果必须内部；外部材料先隔离归档，不能直接塞入材料。76条绑定全查，完整Command补测create/edit四维和嵌套绕路，未发现旁路|
|IndicatorChild；M37-SPEC-01；BP-C-REQ-07/fieldDetails/2|“M37 IndicatorChild逐等级持久化”：child根/子版本、父指标根/版本、subset/name/sort、等级根/版本及逐级alias/elementText；create空ID同事务绑定并返回位置→ID映射|逐级字段不从指标aliases或标准elementLabel继承；非等级alias/elementText只能空；等级自身ref=null，其他子集等级ID/ref成对且同父精确版本；同父同子集排序唯一、修改新版本。结构与必需语义守卫共同可执行|
|CatalogDraft；M06-SPEC-01/02；BP-C-REQ-02/fieldDetails/1|“M06目录、指标类型、资格级别和评级方案”：indicator_type自身持久isCommon、稳定说明行、evaluationMode与数值尺度/评级选择；indicator固定type版本，标准冻结indicator→type→scheme链|numeric/rating/not_configured互斥；非type禁止type配置；评级方案M06 rating_scheme及方案内level，不能换qualification_level；版本不存在/成员不匹配拒绝；未配置不能认证。数值min<max、step>0/precision一致由服务端语义核|
|Question/QuestionnaireDraft；M26-SPEC-01/03|“M26每题适用与维度”：questionnaire_question_binding含套卷/题版本、order、roleRefs、dimensionRef、indicatorRefs、visibility；M37标准维度子对象的根、版本及manifest生成方式明确|角色为整卷角色子集；维度归整卷指定标准；指标归精确维度manifest；条件仅引用更前且对该角色可见题；旧conditionAst与新AST不一致拒绝；不按整卷列表猜题目关系；项目仍冻结旧卷|
|PreviousResultRef/ReviewProject；M18-SPEC-01/05|“M18 previousResultRef”：项目create/save显式null或一份已发布历史结果集根/版本/asOf/字段/purpose；同person映射|非M18 published_result、当前项目自引用、时间倒置、内外purpose冲突、白名单外字段拒绝；原集无该人时null+NO_PREVIOUS_SUBJECT；仅参考，不填当前评定或自动创建M17成员|

接口对象Schema与服务端语义守卫必须一起实现。`Interfaces.md`“版本化接口”本身明示这种分工，因此错误版本等10个反例由独立查表oracle拒绝，不要求JSON Schema能访问数据库。没有把Schema的结构接收解释为业务批准/发布/生效。

更改的新必填字段没有许可旧客户端静默补造：Contract_Repair末段规定adapter、unknown隔离、保留原字节/ID/版本；回滚不得删除新字段恢复弱校验。新增维度为原M37标准内子对象，不是扩展独立模块。权限、审批、来源与事务模型均仍为实现前必须遵守的P2约束。

## 002 匿名手工复算

匿名未知量是单题值状态的answerAtom，不是整卷UUID。旧值和新值形成不同矩阵行；未改变的题继续复用同一行。等价关系仅比较全部已披露及候选cell的参与/精确系数向量，计不同评委，不计行数。

|高风险例|独立手算|判定|
|---|---|---|
|ANON-01 ABC首次|A=2、B=4、C=6，每行向量(1/3)，同一类{A,B,C}大小3；均值(2+4+6)/3=4|满足k=3，可发布该单元；仍需授权与独立审核|
|ANON-03 A改答|A旧(1/3,0)，A新(0,1/3)，B/C均(1/3,1/3)；类分别{A旧}=1、{A新}=1、{B,C}=2。旧均值4、新均值5，3×(5−4)=3即A的变化量|不足组涉及新列，抑制新发布；不能删旧A行或旧列|
|ANON-05A 前两报表|111和110在前两列都表现11，合为4人；10、01分别6人；00忽略。各表10人、均值3|类[4,6,6]均达标，可发布第二份|
|ANON-05B 三重交叠|111只X0=1；110/101/011/100/010/001各3；每表仍10、两两交集4且差集6，但完整向量把X0隔成单人|类[1,3,3,3,3,3,3]，第三份抑制；两两合格不能替代全矩阵|
|ANON-06A/B 系数组合|前两列ABC与DEF各3；第三列使A为(1/6,1/9,1/11)，BC为(1/6,1/9,2/11)，DEF为(1/6,2/9,2/11)|前者[3,3]允许，后者[1,2,3]抑制；只看参与bit不够|

其余逐项复算：02两人抑制；04由ABC变ABD得到[2,1,1]抑制；07A三个subject、各三卷允许，07B subject只有2抑制，07C一个subject只有2卷也抑制；08A邀请前明确具名的唯一上级允许具名非self报告，08B仅self抑制，08C匿名上级事后具名抑制；09撤回旧报告后仍保留旧列，等同03抑制；10虽然三人同类，分区映射失效仍抑制。全部16行和精确数值在两轮JSON记录内。

额外去重核验：同一人有三个不同atom但相同系数，distinct reviewer仍为1，不会凑成k=3。组织底层卷数由原始行的subject/reviewer重新算出，不只读取作者给定的bottomAnonymousCounts。

实质控制逐项接受：

- responseVersion/lineage、answerAtom/previousAtom、reportDisclosureVersion、稳定reviewer/subject伪名和linkDomain职责分开；断链/孤儿/未知旧披露拒绝，伪名/矩阵restricted，不进入普通HR/M32。
- 聚合计全部历史及候选列，跨受众/用途保守并集；角色不临时合并，变化的题义/尺度不自动重开域。分布选项/补集及one-hot关联另入控制；未登记非线性聚合不能沿用线性证明。
- 组织subject≥3与每个底层匿名reviewer≥k独立核；named不填匿名分母，邀请notice与唯一关系版本为前置；具名可见还需单独受众/字段权。
- 抑制失败新列及派生总计后重算，必要单元全无则REPORT_NOT_PUBLISHABLE；不能向响应泄露抑制人数、分数或可相减总计。
- ledgerRevision及auth/writer/recovery epoch CAS；报告、账本、分区、审计、receipt、恢复日志原子。冲突必须重算，unknown查原键。P3仍需实际故障与并发证据。
- withdraw只加deny，不删已下载约束；epoch继承分区和历史，不是预算重置。账本缺失只可在当前仍有权且未撤回时返回同一个已登记的字节相同Cell；否则不可新披露。保留期满也不能清空防差分责任。

上述结论限所定义发布矩阵和固定关联约束。真实用户知情、外部先验、实际隔离部署和实现完整性继续是005/006及P3/P4责任，不在本轮冒称实证。

## 003 三项基础能力桌面演练

|场景|执行定义和角色|可判定断言|适配结论|
|---|---|---|---|
|BASE-02-AC03|T-A、REP1-v1已发布，仅E1获developmentSummary；H仅邀请管理、L仅名册；RAW-A-v1及bridge restricted，authRev10。按actions直接请求投影、原卷、未授权字段|E1只得summary；越权整字段请求拒绝，H/L不获本人报告；两个版本字节保持，审计无答案/身份桥|可执行的P3差异定义；非“替换对象”口号；not_run|
|BASE-03-AC02|CT1-v1 category草稿及CERT1-v1有效；H仅改目录name，独立R撤证。H以完整CatalogDraft/expectedEntityRevision1编辑，R用新revision/新键撤证，再同键重发|CT1-v2+一次内容审计/receipt，不写M01任职历史或改证书；一条撤销状态事件，CERT1-v1授证字节保留；同键不多增事件；禁止改person/issuedAt/actor，审计失败原子回滚|内容版本和资格业务历史按语义分别计数；输入、角色、时点与结果明确；not_run|
|BASE-04-AC02|REP1-v1 published/B1→OBJ-A；v2 draft无绑定；H仅草稿manage/bind和旧版read。尝试解绑/替换已发布B1，再对v2新bind OBJ-B，回读旧B1|已发布绑定不可变，定义预期409 IMMUTABLE_VERSION；v2独立B2且仍draft，v1/B1/OBJ-A不变；新绑定不继承旧受众，无权下载拒绝；墓碑先禁读，恢复点引用字节不清理|明确版本复制/来源策略、字段和拒绝断言；实际共享adapter由A冻结，不声称有运行路由；not_run|

这些是P2的合成fixture定义，不是已准备好的产品数据库。ID及a/b重复字符摘要是符号夹具值；P3物化实际字节/版本时应按平台契约生成并固定一致的真实摘要，不能把符号常量当真实附件SHA256证据。本轮没有上传对象，也没有声称这些常量验证过实际文件。

三项原AC文字/basis在originalFoundationGwt保留，逐字反查Scope和Requirements_Trace；新适配直接进入原138场景，而非只存在孤立说明。后续步骤必须遵守已批准当前授权/对象可见性和共享adapter的固定失败顺序；不得为了得到某个错误码放宽任何grant。

## 004 与原已接受内容的回归

46项任务逐一阅读并核对taskId、完成前置、R1能力、Schema、adapter、安全、迁移/恢复、纯领域子片段、所有者授权和完成条件，逐项结果保存在Recheck_Round1.taskReviews。A/B/C与R3槽位明确未开放，缺依赖返回blocked_dependency。全图由两份数据入口、两种算法分别核得55/165/0。

原56门禁逐项关联到新内容与原场景，见Recheck_Gates.json。原受影响门禁M37-01/05、M06-01、M26-01/03/04、M18-01、H-10/18/19、E-02/04/07按本轮新证据判断；其余按固定差异确认控制未删除或削弱。没有把原Review_Round1/2当独立结论。

完整原批准文字、条款、合同字段、关闭项、AC及历史任务身份保持。Architecture、Migration_Rollback、Recovery_Cost_Responsibilities、原LIMIT、来源清单/请求、批准和历史AC映射与旧包装字节一致。Permissions仅增加受控匿名谱系说明，Interfaces只替换引用联合简写并增加修复入口，其失败/信任/对账规则保留。M17/M03仅内部引用澄清，领域控制未变。

没有把重要数据模型、服务端权限、事务/幂等、不可逆迁移、隐私或任免/资格联动移交P4再决定。P3承担实现与故障验证，P4承担真实来源、角色、容量/成本/恢复核证；未知真实来源依赖的对象先隔离，不先迁移再补证。
