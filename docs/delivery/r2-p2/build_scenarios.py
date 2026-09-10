"""Supplemental failure/contract GWT proposals; no business test execution."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
rows=[]
def add(id,task,refs,g,w,t):
    rows.append({'id':id,'taskId':task,'requirementRefs':refs,'given':g,'when':w,'then':t,
      'fixturePolicy':'仅P3获准后使用隔离合成租户T-A/T-B和测试时钟；无真人/真实外发/新增访问者',
      'expectedEvidence':['固定输入及源版本/时点/权限摘要','命令回执、业务前后hash及不可变事件差分','拒绝字段/副作用和对账状态断言；独立测试复核'],
      'executionStatus':'not_run'})
modules={
'M37':[
('03','STD v1已发布；两独立审批v2/v3均基于root revision7','同时以expectedRevision7发布','仅一个published指针推进；另一409；旧v1 digest不变，同键重试回原版本'),
('02','同尺度数值2/4、权重0/1；另有必需null及带环AND节点','分别计算/发布规则','合法加权结果4；必需null返回unknown不缩分母；环拒发布；不得跨维度求总分'),
('05','消费者A已冻结v1，B草稿将引用v1；与停用事件争同revision','停用先提交，再提交B；A继续办理','B拒新引用，A保留原v1并告警；v2不会替换A；显式取消才改变A状态'),
('04','用户X曾获面试问题export，已生成v1附件；安全账本现已撤权','旧链接下载与晚到缓存响应返回','前后权限复核拒绝字节；缓存不复活；通用审计无问题原文')],
'M06':[
('01','目录counter=41；两请求同对象/编号规则；同父sort=1两不同目录项','并发分配编码并读取展示顺序','编码唯一可跳号不复用；sort允许同号、以稳定ID排序；标准levelOrder重复仍拒绝'),
('01','channel v1的QL→M27资源R1未配置，另一QL2映射已核验R2','显示发展通道/简卡/学习地图并点击引用','未配置明确空态；合法资源只授权导航；不自动创建课程任务/资格证'),
('04','证据与标准同version、窗口截止D；证书validUntil D，当前23:59:59+08及次日00:00各一组','查有效性并尝试续期授证/任用消费','D内valid，次日expired；证据窗口独立检查；新续证不覆旧证，双续期一在途'),
('05','授证事务成功但响应丢失，证书C已存在；随后撤销审计写失败','同幂等键查询/重试，再查询撤销状态','同证书C无重复；撤销事务全回滚，仍显示原有效性及明确失败，不冒已撤销')],
'M26':[
('02','ABC三人合法报告已披露；新报告同cohort只A改分；另有ABC与ABD交叠','分别提更正发布及第二cohort发布','changedContributorSet和差集小于3，受影响分数/人数/补集全部抑制，不因cohort相同放行'),
('02','两个待发布报告共享disclosureRevision9，各自单独检查似合法、合并可隔离一人','两个发布并发使用revision9','一提交后另一409重读披露账本，重检识别泄漏而抑制；不能都按旧账本通过'),
('03','套卷四题型，选择题无重复option，条件隐藏文本；另有required rating与显式NA政策','提交错误选项/越step/超3000文本及合法隐藏/NA答卷','错误类型拒绝；隐藏与NA保留原因不计0；只有冻结角色适用题入分母'),
('01','HR H仅projectManage，审计X有定时rawResponseRead但无导出；桥接在独立域','H查原卷/通用事件，X到期前后查及尝试导出','H无身份关联/原卷；日志无payload；X仅时限范围可读，export拒，到期立即拒')],
'M18':[
('03','同result v1，两会议各一更正；提案C、复核R、发布P；C试自审','并发提交/审核/发布并以过期base重试','每原结果一在途；C拒，R与P分离；BASE_SUPERSEDED拒，不修改M16/M26源'),
('01','scope v1含E1/E2，E2调动后v2授权排除并加入E3','查看v1真实快照与v2当前分析','v1原组织/人数/来源保持；v2当前权限裁剪；不得用新人员名单替旧范围'),
('02','lowCut40/highCut70，四值39.5/40/69.5/70，另1缺轴与ordinal无映射','计算九格及人数','档位low/mid/mid/high；缺轴unrated，无映射null；九格人数+未评定=授权范围总数'),
('04','项目step2保存失败，最后step3可见；closed项目有已发布v1','读取checkpoint、直接calibrate，再经reopen审批操作','step2无成功receipt不冒保存；终态写拒；合法reopen新revision和新结果版本，旧v1不变')],
'M17':[
('01','启用规则run1输入3人，其中E2资格unknown，E3写审计失败；E1已提交回执','接管过期租约后同周期重跑','E1不重复入池；E2无入出动作；E3无半成员；旧fence不能提交，逐项partial可对账'),
('03','导师A已失当前关系，B授权交接后接受；A有旧待核验请求，本人为成果贡献者','旧A晚交verify、本人verify和新B合法verify','A和本人拒，B按当前独立职责办理；已完成旧核验记录不换人'),
('04','IDP阶段S2依赖S1，S1必需T1 cancelled未获waiver，选修min1未完成','尝试开S2/完成计划，再获授权waiver和独立选修核验','先拒；满足新版要求后才推进；取消不自动等完成，旧submission和审批保留'),
('05','关键岗位4/覆盖3/now2；池人数3 expected2；到期cohort4含完成1、授权终止1、未完2','以同asOf/definition求指标并再用零分母夹具','覆盖75%、就绪50%、池150%、逾期2/4=50%；零分母null；终止不缩已确定cohort')],
'M03':[
('01','2024-02-29加1年、2026-01-31加1月；授权override有/无reason','预览并保存任期/超界考察期','分别2025-02-27、2026-02-27；无理由覆盖拒；考察超任期拒，历史未知不套算法'),
('03','阈值80.000，精确79.995及80.000；5评委1回避1弃权3通过；另1未交','显示舍入并最终决议','79.995显示80仍不通过，80精确通过；3/4到75%；未交阻决议，不当弃权或减分母'),
('02','同M01 actual applied receipt R、同任用类型，两次不同command；资格在第二次前过期','并发核对后查询两域与同键重试','一张receipt只一任期，重复拒/同键原结果；M01事实保留，当前资格失效不补M03成功'),
('05','档案访谈v1及discipline附件，用户只有archiveRead，后授权interviewRead但无export，再撤权','直接历史/下载/更正作废查询','基础read不能见敏感子集；read不代export；撤权旧链接拒，作废保留原ID/history且不影响任用')]
}
for m,arr in modules.items():
    for n,(spec,g,w,t) in enumerate(arr,1):add(f'R2-{m}-S{n:02d}',f'P3-R2-{m}-{spec}',[m+'-SPEC-'+spec],g,w,t)
tasks=[]
def task(id,title,ref,requirements,owner):
    tasks.append({'id':id,'title':title,'moduleId':None,'requirementRefs':requirements,'designRefs':[ref],'ownerRole':owner,'phase':'P3','status':'proposed_not_started','dependencies':['R2 P2退出与P3准入另获所有者批准','对应R1契约实现版本确认'],'deliverables':['隔离实现/适配','可复核正反例和故障证据'],'scenarioIds':[]})
task('P3-R2-COM-01','共用CAS、审计、回执及有界作业','Architecture.md#transaction',['R2-BASELINE-01','BASE-03'],'共享事务负责人+独立测试负责人')
task('P3-R2-COM-02','严格schema、信任及事件对账','Interfaces.md#trust',['BASE-06'],'共享接口/安全负责人')
task('P3-R2-COM-03','增量迁移、兼容与冲突隔离','Migration_Rollback.md#cutover',['R2-BASELINE-01','BASE-04'],'迁移负责人+六域数据负责人')
task('P3-R2-COM-04','恢复平台能力与R2安全恢复','Recovery_Cost_Responsibilities.md#recovery',['BASE-05'],'共享平台/安全/运维负责人')
task('P3-R2-X-01','M37版本到盘点、发展及旧消费者','Cross_Module_Contracts.md#consumption',['M37-SPEC-05','M18-SPEC-05','M17-SPEC-06','C01-AC1'],'M37/M18/M17接口负责人')
task('P3-R2-X-02','资格、准备度和任用生效','M03_Design.md#m03-spec-02',['M06-SPEC-05','M17-SPEC-02','M03-SPEC-02'],'M06/M17/M03与M01接口负责人')
task('P3-R2-X-03','匿名报告跨域、撤权与导出','Permissions.md#anonymity',['M26-SPEC-02','M26-SPEC-05','BASE-02'],'M26/M18/M32安全接口负责人')
task('P3-R2-X-04','门户、档案和报表版本消费','Cross_Module_Contracts.md#catalog',['M17-SPEC-05','M03-SPEC-06','C02-AC1'],'M48/M32既有接口与R2负责人')
common=[
('01',['BASE-03'],'命令C同时写业务/审计/outbox/完整行日志；分别在审计、receipt、CAS注入故障','重试原键并检查数据库快照','每次全提交或全无业务效果；DB不可写不承诺库内失败日志；同键只一个成功receipt'),
('01',['BASE-03'],'批量报告分3块，前2块已存，租约fence7过期由8接管','旧worker提交第3块/ready，新worker从cursor接续','旧fence拒；未完整manifest不可读，最终权限和hash校验后一次ready，无半报告'),
('02',['BASE-06'],'同事件ID同/异digest、sourceRevision缺口；外部签名错误/过期nonce/key','消费与对账、重复回调','同digest去重，异digest隔离；gap阻投影；签名/nonce错误不写业务；不取latest跳历史'),
('02',['BASE-06'],'命令含未知字段、重复JSON键、超安全整数/非法decimal；另一供应商回执unknown','解码提交及网络恢复后的同键查询','schema严格拒非法输入；hash不代签名；unknown未证不重发，业务/通知分态'),
('03',['BASE-04'],'旧标准同code冲突、旧任期重叠、旧360低样本报告；source digest变化','分批迁移预演到read_switch','原hash/ID不变；冲突局部隔离；旧低样本先deny；游标只随原子batch回执推进'),
('03',['BASE-04'],'新多级标准/多阶段IDP已产生事实；旧writer不认识epoch，worker lease过期','尝试回旧写版及旧fence继续回填','旧写全部被闸门拒；保留新模型和映射，前向修复/只读，不DROP或覆盖新事实'),
('04',['BASE-05'],'15分钟行日志及对象manifest；数据库点T与文件点T-70分钟，某答卷hash损坏','核定恢复点及拟开放','不能选数据库T冒RPO达标；共同可恢复点超过60分钟为违标，损坏对象隔离，相关报告不开'),
('04',['BASE-05'],'备份旧HR有原卷权，当前deny已撤；披露账本块缺失、证书恢复时已过期','隔离恢复并计时到owner_approved/opened','当前deny先行；原卷/报告禁用，证书expired；补齐前不开放；RTO含审批且≤240分钟才可报告达标，保留30天证据')]
for n,(tid,refs,g,w,t) in enumerate(common,1):add(f'R2-COM-{n:02d}','P3-R2-COM-'+tid,refs,g,w,t)
cross=[
('01',['C01-AC1','M37-SPEC-05','M18-SPEC-05','M17-SPEC-06'],'M37 v1→M18已发布r1→M17建议→显式创建IDP；随后标准v2发布','查询整链与已有IDP，再消费重复M18事件','全链仍指v1/r1，IDP不重复且不自动发课；v2不覆盖旧证据，真实集成状态须留证'),
('01',['M37-SPEC-03','M06-SPEC-03'],'M06申请/M26卷/M18项目/M17模板/M03活动均冻结standard v1；标准停用','逐域继续在途并新建引用','在途原版本带警示，显式取消才终止；五域新引用均拒；旧5级consumer可读旧schema，新6级不可静默压5级'),
('02',['M06-SPEC-04','M17-SPEC-02','M03-SPEC-02'],'资格C截至D；M17 now且未到复核时点，M03决定已批准未生效','D+1读取now覆盖并尝试任用核对','now覆盖按资格失效排除/说明；M03阻生效；M18历史盘点不被改写，证书原certified事实保留'),
('02',['M03-SPEC-02','BASE-06'],'M01 applied可信receipt已写但M03响应unknown；另一仅approved未applied','查原命令/两域receipt并重试','已提交M03回原term，不重复；未applied拒；无法确认保持unknown，不撤销M01或伪造M03完成'),
('03',['M26-SPEC-05','M18-SPEC-05','BASE-02'],'M18和M32获准消费M26已发布报告；报告后被撤权/纠错，旧链接及缓存尚在','直接源/消费端查询和下载','当前访问均拒或字段省略；不得从原卷/旧缓存重算；已作合法业务决定只保留受控证据引用并独立更正'),
('03',['M26-SPEC-02','BASE-04'],'M32只reportExport、cohort ABC与ABD；job已生成2块后安全epoch变','请求两报表合并与旧job下载','沿M26披露账本抑制差分；权限变更使旧job不可ready/下载，orphan不暴露字节'),
('04',['C02-AC1','M03-SPEC-06','M17-SPEC-06'],'本人E有IDP/学习核验反馈、干部年度述职待审；档案读者无interviewRead；通知unknown','通过M48/干部档案读取并处理源任务','仅获准计划/学习/述职字段；无访谈/排名；审批待审不当已发布，动作回源且unknown查原键，不生成二套业务状态'),
('04',['M17-SPEC-05','M18-SPEC-05'],'M32有岗位4、组织2、池3人，当前与旧snapshot来源不同；无综合健康权重','按各dataset查询并请求current带历史asOf','岗位/组织/池分母不混；current历史筛选拒，真实snapshot固定源并当前裁权；综合指数not_configured不补总分')]
for n,(tid,refs,g,w,t) in enumerate(cross,1):add(f'R2-X-{n:02d}','P3-R2-X-'+tid,refs,g,w,t)
(D/'Supplemental_Scenarios.json').write_text(json.dumps({'tasks':tasks,'scenarios':rows},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'supplementalTasks':len(tasks),'supplementalScenarios':len(rows)}))
