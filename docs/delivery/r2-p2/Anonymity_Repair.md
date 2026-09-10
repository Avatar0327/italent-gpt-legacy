# R2-EXIT-002 匿名等价类与披露账本规范

本规范替换M26旧文“签名包含源答案版本”的歧义；核心算法在P2确定。Anonymity_Cases.json保存逐行有理数矩阵，Anonymity_Calculation.md保存手算，check_anonymity.py独立由矩阵重新计算；仅为P2符号核验，不是产品隐私测试。

## 对象和关联边界

|概念|确定含义与持久化|
|---|---|
|responseVersionId|单个不可变整卷版本ID，各评委各不相同；仅来源manifest和身份隔离域使用，绝不拼入跨人等价类签名|
|responseLineageId|同邀请/同评价者的稳定答卷根，版本previousResponseVersionId形成无环单链；改答新增版本，撤回留墓碑|
|answerAtomId|同lineage的同question语义/尺度下单题值版本。无变化重新提交可保留旧atom；值、缺失状态、尺度或题义变化产生新atom并保留previousAtom。不能以response整卷改版强迫未改题生成新值，也不能将已改答案伪作旧atom|
|reportDisclosureVersionId|每次真正对外释放的不可变report版本；下载/页面/M32投影/组织汇总都登记对应cell与时间，不因受众不同分开预算|
|protectedReviewerKey|受控关联服务HMAC(tenant,stableReviewerPersonId,domain)产生的稳定伪名，跨邀请/项目/改答可关联；普通HR、报表服务和日志看不到。key轮换需受控等价映射，失联禁披露|
|protectedSubjectKey|被评价者同样稳定伪名，用于组织双阈值；不以组织/项目ID代主体|
|linkDomainId|租户内可关联题义/尺度与同一被评价人的保守关联域。用途、组织、题目改名、套卷改版不能自动另开域；明确证明无关联才独立。没有可信语义映射即拒绝新增可重叠报告，不能猜不相关|
|participationSignature|某answerAtom在全部已披露及候选cell中系数是否非零的0/1向量|
|coefficientSignature|同一顺序全部cell的精确约分有理数向量；0保留。系数包含权重/均值分母/转换；签名不含reviewerKey、atomId、responseVersionId或修订序号|
|securityPartitionId|由首次合法披露形成并冻结的安全原子分区manifest。后续可细分，但每个非空新原子仍须满足门槛；不能更换ID逃离旧分区|
|disclosureEpoch|同一历史账本连续性标识，版本迁移/重建可升epoch但必须继承全部约束及partition ancestry，不是隐私预算重置。security/auth/recovery epoch分别表示当前裁权/恢复屏障，亦不清账本|

身份桥接只交给独立匿名处理服务，其凭最小purpose读取伪名与atom，不把personId/inviteId映射下发M32/普通报告服务。报告消费者仅接收批准的Cell、manifest摘要及授权状态。伪名、atom谱系、系数矩阵和分区manifest本身属于restricted，不能外露人数小类或使主体追评委。

## 确定算法

1. 先冻结当前集合：每有效邀请仅最新submitted答卷；按protectedReviewerKey去重，同role notice、同题义/尺度/用途方可聚合，NA/隐藏/撤回不计入。实名行另走明确具名投影，绝不凑匿名k。匿名阈值为显式k≥3。
2. 取同linkDomain及其有交叠/可转换域的**全部历史已披露cell**，跨受众、跨用途保守并集。每个数值统计可表示为固定answerAtom未知量的线性组合，矩阵行=answerAtom、列=cell、元素=精确有理数系数。未参与为0。旧版本继续是旧变量；更正新增变量行，旧行在新列系数0，新行在旧列0。相同未变atom跨报告复用同一行。公开分母/有效人数作为额外可披露计数cell纳入同样门禁；不输出未经登记的旁路总计。
3. 按(参与向量,精确系数向量)相等分组；忽略全0行。每非空组计算不同protectedReviewerKey数，必须≥k，不能数atom数/答卷版本数。组中同一人多个atom仍只算1人。既有已披露列不可删除。该规则保证对任何这些列的线性组合，同组每人的系数保持相等；新值或差分若仅涉及1/2人则必形成不足组，拒绝。
4. 组织报告另做被评价者贡献矩阵：行是subject在该题义/尺度下的来源快照谱系，列是拟披露及历史组织cell，系数由组织聚合方案确定；每非空等价类≥3个不同protectedSubjectKey。每个底层subject匿名单元仍通过reviewer k，组织3人不能替代每人3卷，反之亦然。不把多个版本算多个subject。
5. 均值/加权和只用已批准的精确映射。分布每个选项及补集计数均转成indicator atom纳入矩阵；选项间one-hot约束也作为固定关联，任一非空选择组合类不足k则抑制整组分布及总计。中位数、任意百分位、任意筛选、未登记非线性指标不支持该证明路径：返回suppressed+unsupported_safe_aggregation；原文默认不发布，人工脱敏摘要走既有独立审核，不以数值k证明文本匿名。序数无批准转换只允许满足上述分布门禁，不擅自求均值。
6. 候选报告按cell稳定ID排序，在完整候选矩阵上检查。失败类涉及的所有新列及其派生总计统一抑制；历史列保留。重算剩余新列直至无新增抑制。所有业务必要单元被抑制或无合法非self组时不发布正式报告，返回REPORT_NOT_PUBLISHABLE；其余安全单元可发布，不输出抑制单元人数、均值、差值或可推断的总计。若集合完全相同、atom和系数相同，重复披露不增信息，但仍需当前授权。
7. 以expectedDisclosureRevision+当前auth/recovery/writer epoch做CAS，账本新增cell/分区细化/报告指针/审计/receipt/恢复日志同事务。并发冲突重读账本并重算，不能沿旧判定重试。失败无发布指针；unknown查询原命令，不能换键生成新披露。账本包括已撤回/已下载报告，业务withdraw只加deny，约束不删除。

本算法是对指定发布矩阵和固定关联约束的保守防组合推断设计，不声称阻止所有外部先验推断；P4继续核知情范围和真实角色。不能将“外部先验未知”用作放宽本矩阵规则的理由。

## 固定安全分区与降级

固定分区由受控服务在首次披露前按批准cohort及来源manifest生成，每原子至少k评委（组织还需subject≥3），同时固化atom谱系和允许聚合函数。后续只能发布这些安全原子的整块组合，且仍检查新/旧atom差异；新角色/成员/尺度、部分人员改答或不可证实的分区映射均不得直接切新epoch发布。完整账本不可读时，禁止新统计披露；仅可在当前权限和source未撤回前提下重返同一个已登记的字节相同旧Cell，或返回suppressed/unavailable。重开更正已deny旧报告时，不能用此降级返旧值。

分区不满足的处理是确定的：抑制失败原子及所有依赖总计，若无合法必要单元则拒绝正式发布。不得临时合并匿名角色凑人数、把匿名转具名、删版本维度、重置账本、使用新project/purpose/epoch逃避历史。撤回/保留期满可删除原文依据既有策略，但需保留不可反解的安全约束、伪名连续性和拒绝标记；无法保留时永久封禁该关联域的新重叠披露，不能以30天备份保留期清空防差分责任。

## self与唯一上级的明确例外

只有邀请前noticeVersion已明确具名且角色为self（reviewer=subject）或经关系版本证明的唯一上级，才走named模式：不适用匿名k，不进入匿名均值、不参与匿名分母。返回具名分项需独立report audience/字段权限。匿名经理邀请不能事后改named；多上级不能套唯一上级例外。仅self无合法非self组仍不能发布正式个人报告；一个明确具名唯一上级是合法非self组，可以在其他既有审批和授权条件齐备时发布具名报告，但不得因此释放任何不足k匿名单元。组织含named数据也不绕subject≥3门槛。

## 严格账本数据契约

Interface_Schemas的DisclosureAtom/DisclosureCell/DisclosureLedgerEntry为服务端受控内部持久化契约，禁止客户端写伪名/分组。ReportPublish新增disclosurePlanVersionRef指向匿名服务已计算的内部计划；发布核计划的reportVersion、sourceManifest、privacy policy及ledgerRevision和当前请求一致。参与/系数签名由服务端重算，客户端摘要不作信任依据。原卷版本与atom.previousAtom必须可核且无环；孤儿atom/断谱系/未知旧披露拒绝。修订/迁移保留旧披露约束和旧ID，不编造旧未保存版本；旧不安全报告只在受控历史域留证，无法核旧公开范围则封禁关联域新披露。
