# R2接口schema、异常和对账设计

<a id="schema"></a>
## 版本化接口

本文件是P3拟实现的契约，不宣称接口已经存在。命令沿R1共用dispatcher及账本，命名空间`r2.<module>.<action>`；建议路由`POST /api/r2/commands`桥接相同执行器，查询`GET /api/r2/commands/{commandId}`及各域查询资源。不能另建第二套幂等回执。旧路由仅经同一安全写闸门适配；不能表达新前置则409 CLIENT_UPGRADE_REQUIRED，不能默认为旧admin全权。

命令必填：schemaVersion=1、commandId(UUID)、idempotencyKey(1–200)、action(注册枚举)、objectRef({module,objectType,rootId,versionId?})、expectedWorkspaceRevision、expectedEntityRevision（create为0）、expectedAuthorizationRevision、writerEpoch、recoveryEpoch、payload。create的rootId必须null，由服务端生成业务根并写入回执；更新必须已有rootId。模块命令表省略公共`r2.`命名空间前缀。tenant/actor从已验证会话推导，不信任payload；不接受未知字段。业务payload逐动作声明字段类型/必填/范围，指令性的审批状态和审计actor不可由客户端赋值。字符串按模块定义trim，未声明字段不隐式转换；decimal用规范十进制字符串，安全整数超限拒绝，拒绝NaN/Infinity、脚本和重复JSON键。

`Interface_Schemas.json`为关键实体及共用协议的JSON Schema，`Command_Registry.json`将业务动作逐一绑定payload和语义检查引用。schema通过只证明文档结构；日期真实有效、区间互斥、权限/回避、尺度/AST、源版本新鲜度和事务必须由P3服务端实现，不能以schema校验替代。

回执必填commandId、requestDigest、status=accepted|applied|rejected|unknown、approvalState、effectState、entityRevision、workspaceRevision、occurredAt、correlationId；可选error={code,retryable,reconciliationId}。accepted仅入队；applied表示本地指定动作已提交，不自动代表任用、人事或外发都完成。返回体不得含无权字段。unknown保留原命令键和对账入口，不显示业务成功。

保留BP-C-API-01传输边界：来源/CSRF不符403，非application/json为415，超过路由字节上限413，空体/无效JSON/重复键400，未分类服务异常503；旧兼容路由仍保持现有32768字节默认，不修改通用旧端点预算。拟新增`/api/r2/commands`显式上限256KiB，足以容纳M17模板32766个四字节字符及有界元数据；更大模板/名单走分块准备manifest，不截断字段，也不把4MiB存储块上限当命令无限预算。技术预算由P3核实际运行限额，不能改变批准字段上限。敏感响应Cache-Control: no-store，下载先完全授权再输出字节，文件名安全转义，表格导出沿R1公式注入防护。

引用类型`VersionRef`为kind=internal/external严格联合，精确字段和命令白名单见[定向契约修订](Contract_Repair.md)，禁止按缺失字段猜来源。数字版号不能替代versionId，digest不能代权限/签名。`Cell`使用{value,state,reasonCode,unit?,scaleVersion?}：value/null/not_configured/unavailable；敏感无权字段整体省略。报告可额外`state=suppressed`且不带可反推计数。日期YYYY-MM-DD，时刻UTC RFC3339；schemaVersion不支持返回426/SCHEMA_VERSION_UNSUPPORTED。

事件Envelope：eventId、schemaVersion=1、tenantId、producer、eventType、objectType、rootId、versionId、entityRevision、workspaceRevision、sourceRevision、occurredAt、effectiveAt|null、correlationId、causationId、digestAlgorithm=sha256-canonical-json-v1、digest、payload。版本发布事件还带manifestDigest和availability；撤回/停用事件指向原版本与新状态事件ID，不能修改旧payload。订阅字段按最小purpose选择，原卷/敏感原文不在通用事件中。

<a id="trust"></a>
## 签名和信任边界

内部浏览器命令依当前会话、CSRF/同源和服务端授权，客户端自报role/signature均无效。内部受信服务仍核租户、audience、purpose及授权来源；外部回调必须由配置的provider密钥和官方签名规则验证，不能因“有sha256”而信任。自有网关采用HMAC-SHA256，keyId、签名版本、timestamp、nonce、audience、tenant和canonical body digest全部入签；建议时钟窗口5分钟和nonce一次性，技术参数可在P3收紧，不能跳过鉴权。

canonical算法：按严格schema解码，重复键拒绝；仅声明字段规范化trim和UTC；对象key排序、数组顺序保留；UTF-8序列化；去除digest/signature字段；精确decimal字符串统一规范。签名验证与幂等请求摘要使用同一规范。密钥不进repo/审计；轮换双key验证窗口显式有效期，未知key或回放拒绝，不自动从请求下载公钥。恢复保留验证历史所需密钥但不恢复已撤销发送权限。provider未配置为not_configured，验证不可用为unavailable，不能用模拟成功顶替。

<a id="failure"></a>
## 失败矩阵

|状态/错误|调用方行为|服务端/责任|
|---|---|---|
|401/403、REVOKED、EXIT_FENCE|清敏感缓存，禁继续动作|当前授权重核；不自动换管理员或账号|
|404、安全不可见|不探测其他ID|不泄露跨范围存在性|
|400/422、INVALID_TRANSITION/RULE_NOT_CONFIGURED|保留草稿及具体可见错误，纠正后新请求版本|不将缺值补0、阈值补80或未评补通过|
|409、REVISION_CONFLICT/DEPENDENCY_CHANGED|重读并要求用户针对最新内容重新确认动作|同幂等键不同内容返回IDEMPOTENCY_CONFLICT，不改旧请求|
|429/503且明确未执行|有界重试同键|最多6次，指数退避上限300秒；Retry-After最多3600秒，超预算转人工对账|
|超时/连接断开/供应商unknown|查同commandId/请求键和原对象、来源回执|不换键重做；查无记录不证明外部没执行|
|EVENT_GAP|暂停该根后续投影，读取可信缺失版本或对账|不得跨gap用最新覆盖旧快照|
|DIGEST_CONFLICT/SIGNATURE_INVALID|隔离事件，禁消费/报告发布|同eventId异digest为安全冲突，保留受保护case|
|SOURCE_DISABLED|新引用拒绝；冻结在途按模块既定策略继续或显式取消|不改旧版本或向历史补新内容|
|HISTORY_UNVERIFIABLE、MIGRATION_CONFLICT|展示明确受限状态；只阻依赖对象|由数据负责人核证，不按姓名合并或补日期|

内外部失败分开：业务已applied、通知unknown时保持业务结果，通知单独对账。只有供应商保证同键幂等或明确核证未执行才可重发；否则等待人工核对。真实服务未配置保留契约和状态，当前不调用、不签署、不通知、不支付。

<a id="reconciliation"></a>
## 有界消费与对账

inbox唯一(tenant,consumer,eventId)，同digest重复返回原处理结果；异digest隔离。每根保留lastSourceRevision和有界待处理gap，旧事件只记录duplicate/stale，不回滚当前指针。应用投影、inbox、审计与receipt同事务；外部调用通过outbox，不夹在数据库事务里。对账run记录producer/consumer/schema/manifestDigest、cursor、fence、差异分类及责任，不存敏感原文。

逐键比较：根与版本是否存在、digest是否一致、引用权限/purpose、availability、当前发布指针、撤回墓碑、人员退出屏障、业务生效凭证及回执。差异分missing/stale/conflict/forbidden/unknown，不以总条数相同判一致；无权只给受保护差异码。恢复或撤权后先对账再放开调度。原始已发布历史不被当前查询值回填。

消费者版本协商保存supportedSchemaVersions和purpose；兼容minor只增加显式可忽略可选字段，major语义变化发布新schema端点/适配器。原consumer保留旧schema及原版本读，不能把新准备度映射成旧one_year或把新标准压回5级。确实不可表达返回unsupported，保留原历史入口及理由，不默删入口。

<a id="repair-001"></a>
## 001严格契约补齐

[Contract_Repair.md](Contract_Repair.md)规范五组字段、持久化关系、迁移兼容和语义拒绝；[Schema_Examples.json](Schema_Examples.json)给出合法及拒绝实例。Command_Registry.referencePolicy逐命令限制引用类型。

M26 ReportPublish必须带disclosurePlanVersionRef；服务端重新核账本版本和当前epoch。DisclosureLedgerEntry/Atom/Cell为内部严格契约，客户端不能直接写，详见[匿名修订](Anonymity_Repair.md)。
