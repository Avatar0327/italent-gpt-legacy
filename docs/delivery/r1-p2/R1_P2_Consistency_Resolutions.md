# R1设计一致性补充

本文件补齐01至08交付在整体审查中的精确接口细节；不重做原六任务，不改变P1批准。以下规定是P3实现时的统一解释，历史源码行为仅是差异证据。

|项目|统一解释|验收/责任|
|---|---|---|
|审批/生效/通知状态|审批见03；effectStatus统一not_requested/waiting/waiting_external/applied/failed/cancelled/blocked。waiting_external仅已有外部契约明确需要可信回执的分支，不能把M01人工登记变外签强依赖。通知pending/sent/failed/unknown/invalidated独立|P3-INT-03、P3-M19-07；审批/接口负责人|
|任务资源缺失|job业务状态仍queued/running/ready/failed/cancelled/expired；blocked_runtime是availability/reasonCode，不能当ready，缺执行器不占运行租约|P3-M32-06；报表负责人|
|兼容客户端错误|规范machineCode=CLIENT_UPGRADE_REQUIRED，HTTP409；07的UPGRADE_REQUIRED为同义说明，不另建枚举。sourceRevision≠entityRevision≠workspaceRevision，名称不能混用|P3-MIG-06；接口负责人|
|权限版本名称|规范请求使用expectedAuthorizationRevision；authRevision/authorizationRevision为文档简写或旧输入别名，服务端归一后对同一授权水位；relationship/memberBinding变动必须推进授权水位|P3-ARC-01、P3-M48-06；权限负责人|
|稳定ID/现有列|目录和人员ID不随改名/重聘改变；报表新增rowKey/fieldId是标识补全，不用行号/显示名当ID；原列标签和值来源见字段字典|P3-M32-01；报表负责人|
|同日人事变化|有效日期按北京时间闭区间，执行记录仍带毫秒和eventSeq。同日两次主职变更只允许最终日投影一条，先前执行事件保留且当日中间区间可仅用时刻表表达；不制造结束日早于开始日的日期段|P3-XMOD-01；M01负责人|
|未知历史与未来版本|已批新目录版本不能倒写过去。legacy观察数据validFrom未知独立标识，兼容当前读不等于知道历史有效期；更正事件不可假造原时间|P3-MIG-01；数据负责人|
|在用停用与执行failed夹具|F-SPEC-08优先：approved-waiting/failed属于未完成依赖，停用须拒绝。旧BP-F-REQ-01-AC03中允许停用是历史实现差异；P3用预先存在的非法旧数据/失效外部条件验证failed，不能为制造故障放宽新停用保护|P3-M01-12、P3-M01-05；M01测试负责人|
|无关终态原单|F-SPEC-03优先：独立新事项不永久强绑；更正必须同人同类可读原单并重审。旧AC中的“未批准”不重开批准|P3-M01-06；M01负责人|
|报表日期与最新结果|current拒绝from/to，不延续旧忽略参数；只有published的supersedes替代发布结果。未来M17/M26生产者版本映射必须显式，不把ready/one_year/two_years硬映成新准备度|P3-M32-03/04/10；报表及生产者负责人|
|外发与已下载副本|新请求/续传必须当前权；合法已传出字节不能保证远程收回。屏蔽停止未来生成/发送，不删除历史。通知链接发出也不等收件人已读|P3-M32-08/09、P4-M32-01；安全/通知负责人|
|恢复和保留|附件墓碑立即拒读，物理清理受全部恢复点引用约束；导出24小时TTL不删历史/恢复依赖；独立安全ledger是授权证据，不是第二个业务或项目范围事实源|P3-REC-02/05；恢复负责人|

附加实现细节：恢复全行日志可用于一致投影的来源，但必须保留schema版本、事务和源表主键。R2/R3生产者不具备版本读取时返回不可重建，不退回全量可变读取拼快照。新增字段字典只开放类型安全的过滤操作，所有sum/avg/join均须数据集明示注册；不存在默认敏感汇总权限。
