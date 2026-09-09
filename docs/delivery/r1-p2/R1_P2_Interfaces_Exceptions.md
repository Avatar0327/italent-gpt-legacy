# R1内部事件、外部接口与异常矩阵

任务：R1-P2-06。状态：设计完成，待独立评审；不是P2批准或P3验证。

## 批准依据与版本

基准源码/事实源：`716cd9df5f5776d050f77f57c2ad5a35c0a83882`。批准需求：`BASE-03`、`BASE-04`、`BASE-06`、`BP-I-REQ-03`、`BP-I-REQ-04`、`BP-I-REQ-05`、`BP-I-REQ-08`、`BP-I-REQ-12`、`BP-S-REQ-07`、`BP-S-REQ-08`、`BP-S-REQ-12`、`M19-SPEC-04`、`M48-SPEC-03`、`M32-SPEC-05`。批准原文及优先级以 [批准记录](../P1_Approval_Records.md) 为准；原文中的历史待批措辞不重开已批准决定。

## 当前实现与复用判定

- **可复用**：[外部主数据预检](../../../lib/hris/integration-preflight.ts)；基准文件 SHA-256 `73baf42daffaaa136c2e1f23f4f6cd7e4c3f6c568e95c2891b7e01f325a2da35`。严格schema/命名空间/映射版本/摘要/sequence/retry建议保留；ready仍DRY_RUN_ONLY，当前没有网络或写入。
- **可复用**：[HTTP故障与输入界限](../../../lib/hris/http.ts)；基准文件 SHA-256 `32de84dc1331a5b8ad553cd2efcdef0d8e6f454ffdd9b48f6e38b017232b170e`。32KiB JSON上限、Origin、类型、400/403/413/415/503保持；需补machine reason、command状态查询。
- **受限**：[原适配契约](../../../docs/delivery/Integration_Adapter_Contract.md)；基准文件 SHA-256 `e76c9663b208f9737fba282456dc1c9581a346874454b3e024b228e5625dc1b7`。历史合成预验不能证明供应商接通；不恢复M35同步/删除执行引擎。
- **待新增**：[核心提交](../../../lib/hris/repository.ts)；基准文件 SHA-256 `d29c455ce153d7231728c7821d3571ad92ae60edf6b1811d478dcb6a2f1a1249`。同事务outbox/inbox/commandReceipt和授权版本防护尚缺；必须增量补。

## 内外部ID和事件信封

```json
{
  "schemaVersion": 1,
  "eventId": "opaque-event-id",
  "eventType": "assignment.applied",
  "tenantId": "server-derived",
  "source": "M01",
  "internalId": "stable-assignment-id",
  "externalId": null,
  "entityRevision": 3,
  "workspaceRevision": 108,
  "definitionVersion": "assignment-v2",
  "sourceRevision": 107,
  "occurredAt": "2026-09-09T10:00:00.000Z",
  "effectiveAt": "2026-09-09T10:00:00.000Z",
  "correlationId": "root-command-id",
  "causationId": "approval-decision-event-id",
  "digestAlgorithm": "sha256-canonical-json-v1",
  "digest": "computed-from-normalized-content",
  "payload": {"personId":"stable-person-id","assignmentVersionId":"v3"}
}
```

示例为结构示意，不是实际事件。internalId永远指本项目稳定对象；externalId只在指定source namespace映射且不得充当内部FK。外部tenant不可信，从服务身份配置导出；source namespace=(tenant,provider/sourceId)。sequence是外部实体事件顺序，entityRevision是内部乐观锁，workspaceRevision是整体一致序号，不能互换。correlationId贯穿命令→领域事件→流程→通知→查询，不能充当授权令牌。

digest先严格schema校验及字段定义的trim/UTC归一，再按对象key字典序、数组原顺序、JSON字符串转义序列化UTF-8，用SHA-256。数值仅安全整数或schema声明的decimal字符串，拒绝NaN/Infinity；未声明的大小写/Unicode不自动归一；null、缺省、0语义按schema分别保留。digest不含自身/签名，不把同来源不同schema或mappingVersion混成相同内容。内部信封固定规范版本；外部预检延续现有canonical实现，不偷换历史digest算法。

## 请求与查询接口（拟新增，非现有可调用承诺）

| 入口/版本 | 输入与权限 | 输出及边界 |
|---|---|---|
| POST /api/r1/commands | commandId、idempotencyKey、action、businessId、expectedWorkspace/Entity/AuthRevision、payload；会话鉴权和Origin | commandReceipt；同步提交200或显式业务failed；需后台的202+jobId，accepted不等业务成功 |
| GET /api/r1/commands/{commandId} | 当前命令/对象读取权，tenant会话派生 | received/processing/committed/rejected/unknown和原结果；查不到不推定未提交，不泄露跨租户对象 |
| POST /api/r1/workflows/start、/instances/{id}/actions | M19原单版本+模板版本+nodeRevision，动作/独立性重验 | 实例/业务/通知三状态；D7来自原单类型，不能由客户端改adapter绕过 |
| GET /api/r1/self-service/{entry} | 七项受控enum、合法本人/团队关系、cursor | sourceVersion/mappingVersion/allowedActions/reasonCode/fieldStates；未接明确不可用 |
| GET /api/r1/reports/{datasetId} | definitionVersion、timeMode、注册过滤/字段、cursor | rows+stable rowKey+sourceManifest+current auth；不支持的日期拒绝 |
| POST /api/r1/report-jobs；GET /{jobId}；GET /{jobId}/download | read/export分别授权、创建idempotencyKey | queued/running/ready等，download最后重验，不公共暴露R2 key |
| /api/r1/subscriptions/{id}/actions | subscribe/manage独立，revision/acceptTransfer/block | 管理责任变更不复制data grant；不在本轮发送消息 |
| /api/r1/adapters/{source}/preflight | 明确服务namespace/schema/mapping，只允许配置的适配器 | profile仍DRY_RUN_ONLY；供应商未接not_configured，不产生外部成功 |

旧/api/hris等路由保持兼容，但所有业务写在P3升级后接同一命令/授权闸门，不并存可绕过新规则的旧写入口。旧客户端未带新必需版本时409 CLIENT_UPGRADE_REQUIRED，读取只安全可表示字段；未知新多任职不压平成覆盖写入。

## 内部生产与消费事件清单

| 生产者 / event | 消费者 | 幂等键与效果 | 不可跨越的边界 |
|---|---|---|---|
| M01 catalog.version_published、assignment.applied、employment.ended | M19资格重核、M48投影失效、M32新generation、未来M07/M11 | consumerId+eventId；投影写及inbox同事务 | 计划/批准事件不当已生效；不触发追溯薪资重算 |
| BASE permission.changed、binding.changed、recovery.epoch_changed | 全R1 API/job/download | authRevision/epoch递增，取消旧缓存/租约 | 权限必须同步最终判定，不等异步事件送达才撤权 |
| M19 node.activated/changed、approval.decided、effect.changed | M01原域适配、M48清单、M32流程报告、通知 | nodeRevision/generation、实例与原单版本 | 已办历史不重放，管理权不变审批权 |
| M32 export.ready、subscription.occurrence_created | 下载服务/通知适配器 | jobId/manifestDigest；订阅版本+周期+接收人+渠道 | ready不等sent，sent不等read；下载仍当前权 |
| R2/R3 producer.record_changed/published/retired | M48/M32 | producer contractVersion+sourceRecordId+revision | 接入前校验schema和来源授权；未配置不能由mock宣布联调通过 |

内部outbox与业务同事务提交；worker至少一次投递。inbox UNIQUE(tenant,consumerId,eventId)，同digest重放返回原结果；异digest conflict进入隔离。投影结果与inbox同事务，不能先标消费成功再写结果。事件序号缺失先请求缺口/重新建立经核实的版本基线，不能自动跳过；deadLetter须有owner/reason/nextAction/关闭闸门。

## 外部接口的最小保留范围

| 适配领域/对应BP | 输入与回执结构 | 未配置/模拟边界 |
|---|---|---|
| 人员主数据 BP-I-REQ-04 | externalPersonId/orgId、mappingVersion、sequence、profile允许字段；receipt eventId/digest/committedRevision | 原预检保留，M35完整同步/删除仍暂缓；不自动建人/改任职/授角色 |
| 电子签 BP-I-REQ-05/08 | internal contractId/version、legalEntityId、templateVersion、最小认证字段引用、externalEnvelopeId、signerExternalId、receiptId/state/evidenceDigest | 只契约；人工签署登记不等verified external signed；无endpoint/密钥不调用，无真实签署 |
| 外部测评/360公共模板 BP-I-REQ-03 | templateId/version、assessmentInvitationId、externalAttemptId、consent/visibility引用、resultVersion/status | M26只消费其已批模板/结果；M15/M29完整业务不恢复；实名/匿名及阈值由生产者，未定不发布敏感汇总 |
| 金额预算 BP-S-REQ-07 | requestId、period、org/legalEntityId、currency、amountCents、holdId/expiry、revision、checkState | 人数检查独立；未接not_checked；明确强阻断链禁止假通过，不恢复M09 |
| 财务/支付 BP-S-REQ-08/12 | payrollBatch/adjustmentId、sourceVersion、period/currency、voucherRef/paymentOrderRef、receiptId/status | 无会计/税务/社保算法，金额单位来自M07；外部paid/posted只按可信回执，不由published推定 |
| 标签/对象引用 BP-I-REQ-12 | labelId/version/source、relationId、personId、effective interval/revokeRef | 仅当前人才消费者稳定引用；M05/M41完整标签引擎仍暂缓，不按名称合并或自动打标 |
| M19/M32通知 | eventId、templateVersion、recipient existing memberId、channel、opaque secure link、providerRequestId/receiptId | 默认最小化链接，无敏感明细附件；测试只消息拦截，不实发 |

供应商协议需在接入任务给出认证方式、签名字段、时间窗、nonce、查询语义、重放/乱序规则及实际版本。推荐TLS并使用provider规定签名，不能拿digest替认证；本项目自有接收代理可HMAC-SHA256/签名认证并按keyId轮换，密钥由服务运行环境保管不入DB明文/设计文档/日志。未完成验签的回调只隔离，不能生成可信回执。建议自有nonce重放窗5分钟只是技术参数，供应商更严格时遵其要求；历史重放须独立管理通道并验原事件，不靠关验签解决。

## 命令幂等、回执、重试和未知结果

commandLedger唯一(tenant,actor/action namespace,idempotencyKey)，存requestDigest、commandId、状态、lease/fence、业务ID、结果引用、createdAt/updatedAt。received/processing只证明接收，业务同事务写committed及审计/outbox，确定业务拒绝可记rejected；数据库不可写时不能保证ledger成功落库。永久历史关联仅存必要ID/digest与结果墓碑，敏感完整payload不无限留存；归档后相同键返回原结果摘要或IDEMPOTENCY_ARCHIVED，不再执行。

同键同内容：已committed返回原结果；processing返回202+query；已确定rejected返回原拒绝。修正业务输入或用户重新授权重试需新intentRevision且关联旧commandId，不能修改原键的digest。unknown先从权威提交记录查询；查不到只表示尚无可信结果（原请求可能仍在飞行），不得新键再提交。内部服务器可在相同键、相同内容和唯一ledger/fence保护下恢复原命令；外部unknown只有供应商确认未执行或保证相同键幂等才允许原键重试，否则人工对账。

已确认未产生外效的临时错误可参考现integrationRetryDecision：attempt1–6、408/429/5xx或无状态建议重试；尊重Retry-After≤3600秒、指数delay≤300秒，并加受控抖动与nextAttemptAt。该函数不是unknown可盲重发许可证。401/403停止至权限恢复，409重读并核对，400/422纠正契约；超过6次进入角色负责的处理队列，最后关闭闸门为该外部链验收/P4上线前，不无限自动重试。

## HTTP、业务与异常矩阵

| 条件 | HTTP / machineCode | 持久结果 / 用户表现 | 下一步 / 责任 |
|---|---|---|---|
| 正常同步业务提交 | 200 COMMITTED | 结果与revision/审计一致 | 消费原结果；领域执行者 |
| 后台受理 | 202 ACCEPTED | 仅job/命令接收，不算生效 | GET原job；任务执行者 |
| 可提交业务失败（M01目标无效/满编） | 200 BUSINESS_FAILED + execution=failed | attempt/原因落库，任职不变 | 修正前置后新意图显式执行；HR |
| 提前/过期批准/非法参数 | 400 INVALID_INPUT/NOT_ELIGIBLE | 不增attempt，不造成功审计 | 修参数/按原单重审；申请人 |
| 未认证 | 401 UNAUTHENTICATED | 清敏感缓存 | 合法登录；当前用户 |
| 当前权/委托/字段不足 | 403 FORBIDDEN | 不输出隐藏数据/计数 | 刷当前授权；权限负责人，不自动扩权 |
| 不可见ID | 404 NOT_FOUND_OR_NOT_VISIBLE（端点既有403可兼容） | 不确认跨租户对象存在 | 当前授权下查原单 |
| revision/相同键异内容/来源冲突 | 409 REVISION_CONFLICT/IDEMPOTENCY_CONFLICT | 无部分变更 | 读同ID及版本；禁覆盖历史 |
| 格式/超限 | 413 BODY_TOO_LARGE、415 UNSUPPORTED_MEDIA | 拒绝上传/提交 | 合法分批/支持格式 |
| 库读取/写入/审计异常 | 503 STORAGE_UNAVAILABLE | 不承诺业务或失败审计已持久化 | 查询原命令和revision；执行/恢复负责人 |
| 外部未配置 | 503 ADAPTER_NOT_CONFIGURED，读取catalog可200 availability=not_configured | 不伪造外部成功 | 供应商接入任务，不阻其他设计 |
| 请求/外部响应丢失 | HTTP不可判定；outcome=unknown | 保留关联ID，不能报失败未生效 | 先查可信回执，仍未知则隔离该意图；集成负责人 |
| 通知明确失败 | 业务原HTTP保持；delivery.failed | 不倒退审批/业务/快照 | 有界重试/诊断；通知负责人 |
| 批量部分失败 | 200 batchStatus=partial + items | 每单独立结果，禁止全批成功提示 | 查询后仅明确可重办项，保留成功项 |

## 附件与异常恢复协议

上传先put不可变对象→D1同事务关联/审计；失败则对象orphan inaccessible；补偿delete失败进cleanupJob而非伪成功。逻辑删除先D1 tombstone+审计→R2物理清理；后者失败显示cleanupPending。新M19流程/M32快照归属objectType受控枚举，绑定原版本，10MiB单附件/MIME约束保持；导出大文件使用第05块协议不能绕单附件策略。恢复时DB和对象manifest共同校验，tombstone/撤权记录恢复后也不可访问；不自动补发outbox未知交易。

## 正常与失败场景及P3建议

以下仅为可执行验收设计，全部未运行。P3须在P2退出获批后使用隔离合成数据；P4独立人类角色和生产验收不由本表替代。

### P3-INT-01

- 需求：BASE-03、BASE-06、BP-I-REQ-04。
- 给定：同namespace映射v1，eventId同内容/异内容/缺前序/旧无回执；mappingVersion改变
- 操作：调用预检和拟定inbox处理
- 预期：duplicate只同摘要；冲突隔离；gap不跳，stale不假成功；mapping不符优先；ready仍DRY_RUN_ONLY
- 证据产物：canonical样本/digest、sequence与回执矩阵
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-INT-02

- 需求：BASE-03、BASE-06。
- 给定：同一command两个并发请求，已收到但响应丢失；审计失败样本
- 操作：同键查询及相同内容恢复，另试换payload
- 预期：最多一次业务效果；无回执不判未提交；异内容409；审计失败全回滚
- 证据产物：command ledger/fence、业务/审计/outbox差分
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-INT-03

- 需求：M19-SPEC-04、M32-SPEC-05、BASE-06。
- 给定：供应商收到请求但响应超时，两个相同回调和一个异内容回调
- 操作：查回执，重复回调，人工恢复入口
- 预期：unknown先查不重发；同回执不重复生效，异内容隔离；消息失败不倒退业务
- 证据产物：消息拦截器与inbox/outbox证据
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-INT-04

- 需求：BP-I-REQ-05、BP-I-REQ-08、BP-S-REQ-07、BP-S-REQ-08、BP-S-REQ-12。
- 给定：电子签/预算/支付/财务均未配置，内部合同signed与工资published
- 操作：查询外部状态并尝试依赖外部成功推进
- 预期：not_configured/not_checked；强预算链拒绝；登记/发布不当外部签署/付款/入账；没有真实网络副作用
- 证据产物：适配catalog与拒绝回执、网络拦截计数0
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-INT-05

- 需求：BP-I-REQ-03、BP-I-REQ-12、M48-SPEC-03。
- 给定：模板/标签同名不同ID，旧权限撤销，新生产者rawStatus未注册
- 操作：读取消费/旧模板与标签引用
- 预期：ID/version不按名称合并；撤权拒绝；未定匿名/评分不发布；33暂缓不启引擎
- 证据产物：稳定引用映射与能力状态
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

### P3-INT-06

- 需求：BASE-04。
- 给定：R2上传成功D1失败且删除再次失败；另样本tombstone后delete失败
- 操作：读业务列表/猜ID下载/恢复清理
- 预期：孤儿不可达；逻辑删除后仍不可达且cleanupPending；清理不复活访问
- 证据产物：对象hash、metadata/tombstone和cleanup记录
- 责任：R1 P3实施及测试负责人；关闭闸门：P3该任务验收；状态：未执行。

## 全包一致性补充

本任务随最终评审补齐的字段、状态、旧验收优先级和迁移边界，统一见[R1_P2_Consistency_Resolutions.md](R1_P2_Consistency_Resolutions.md)。这些是设计自检修正，不重开P1批准或重做任务。

## 本阶段执行边界

本任务只修改P2设计及一致性材料；未运行产品测试、迁移、备份恢复、外部交易或原站操作；不改变业务代码、数据库、部署、访问者及主事实源。所有技术默认均为设计参数，不能覆盖已批准业务规则。
