"""Render documentation views from the existing Scope_Register.json. No app/data writes."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'docs/delivery'
s=json.loads((D/'Scope_Register.json').read_text()); b=s['p1Baseline']; mods=s['modules']; pages=b['pages']
def esc(v):
 if v is None:return '未核实'
 if isinstance(v,list):v='；'.join(v)
 return str(v).replace('|','\\|').replace('\n','<br>')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(esc(c) for c in row)+' |' for row in rows)+'\n'
def link_source(path):return '['+Path(path).name+']('+str(Path('../../')/path)+')'
def page_link(p):return '[详见证据]('+str(Path('../../')/p['source'])+')：'+p['evidenceRef']
def intro(title):return f'# {title}\n\n生成来源：`Scope_Register.json → p1Baseline / modules[].p1`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：{b["updatedAt"]}。\n\n'
# Keep the whole historical register and prepend the current, source-derived view.
f=D/'Scope_Register.md';old=f.read_text();marker='<!-- P1_CURRENT_END -->'
if marker in old:old=old.split(marker,1)[1].lstrip()
head=intro('全量范围与P1证据总表（当前有效）')
head+='48组范围、59个原验收任务完整保留；本轮P1证据单元不增加验收分母。N=导航，P=局部页面/字段/说明，F=原站实际流程结果。本轮无F级结果，不执行业务取证。已开发/技术通过/人工业务与生产签署分别记录。\n\n'
head+='入口：[P1评审材料](P1_Review.md) · [页面目录](P1_Page_Catalog.md) · [字段字典](P1_Field_Dictionary.md) · [流程与边界](P1_Flows.md)。\n\n'
head+=table(['范围ID','模块','保留范围','原站证据深度','页面证据单元','当前部分实现','仍待核实/实现','生产'],[(m['id'],m['name'],m['scope'],m['p1']['sourceDepth'],'、'.join(m['p1']['pageRefs']) or 'BC-NAV-20260908（仅导航）',m['developed'],m['remaining'],m['productionAccepted']) for m in mods])
head+='\n下方为历史快照，不覆盖上述当前JSON及本轮用户决定。\n\n'+marker+'\n\n';f.write_text(head+old)
# Page catalog: explicitly separate containers/menu entries from page evidence units.
t=intro('P1页面目录与导航索引')
t+='此目录包含“已观察导航条目”和“页面证据单元”两层。导航可能是容器或同名入口，不能按条目数计作独立页面数；部分证据单元合并了列表、空表或多个页签。缺少唯一URL的页面用可重走的菜单路径定位，禁止保存带认证参数的原站URL。\n\n'
t+='角色统一限制：当前已授权账号可见；不因此证明HR、经理、员工或管理员的完整角色矩阵。列表列名也不能证明其在每个角色下均可见。\n\n'
t+='## 全量导航索引\n\n'+table(['模块ID','应用','已观察子导航（N）','页面补证情况'],[(m['id'],m['name'],'、'.join(m['p1']['navigation']),m['p1']['sourceDepth']) for m in mods])
t+='\n## 已定位页面与空表证据\n\n'
for m in mods:
 pp=[p for p in pages if p['moduleId']==m['id']]
 if not pp:continue
 t+=f'### {m["id"]} {m["name"]}\n\n'
 t+=table(['页面证据ID','路径/页面','证据等级及日期','字段观察数','状态/页签/说明','来源','未核实及受限项'],[(p['id'],p['path'],p['level']+'；'+p['observedDate'],len(p['fields']),(p['visibleStates']+'；'+p['sourceStatement']).strip('；'),page_link(p),p['unknown']) for p in pp])+'\n'
t+='## 通用页面属性边界\n\n原规划模板要求的布局、排序、错误提示、详情页签、前后置条件及权限，仅在来源明确记载时适用。没有独立证据的属性统一为未核实；未执行提交以诱发错误，不从本项目代码补写原站默认值。操作入口只证明存在。\n'
(D/'P1_Page_Catalog.md').write_text(t)
# Field dictionary: true/false/null remain distinguishable.
t=intro('P1字段字典（页面观察层）')
t+='每行是某页面某用途下的一条字段观察，重复标签不合并；本表行数不是原站唯一字段总数。存储类型一律未核实，日期/金额/ID名称不能证明数据库类型。`未核实`不代表无约束；`是/否`仅在原记录明确说明时填写。已观察选项不是未经证明的全集。\n\n敏感字段仅收录标签，不收录任何人员、证件、联系方式、薪资、访谈或成绩值。字段来源沿用其页面证据编号；筛选/列表列不附会表单必填。\n\n'
for m in mods:
 pp=[p for p in pages if p['moduleId']==m['id'] and p['fields']]
 if not pp:continue
 t+=f'## {m["id"]} {m["name"]}\n\n'
 for p in pp:
  t+=f'### {p["id"]} — {p["path"]}\n\n来源：{page_link(p)}。日期：{p["observedDate"]}；等级：{p["level"]}。\n\n'
  t+=table(['字段观察ID','标签','用途','存储类型','必填','默认观察','选项/限制'],[(f['id'],f['label'],f['context'],f['storageType'],'是' if f['required'] is True else '否' if f['required'] is False else '未核实',f['default'],('；'.join(f['options']) if f['options'] else '')+('；'+f['limit'] if f['limit'] else '') or '未核实') for f in p['fields']])+'\n'
t+='## 尚无可追溯字段字典的模块\n\n'+table(['模块','已有证据','保留缺口'],[(m['id']+' '+m['name'],'BC-NAV-20260908；'+m['p1']['sourceDepth'],m['p1']['sourceGap']) for m in mods if not m['p1']['fieldRefs']])
(D/'P1_Field_Dictionary.md').write_text(t)
# Flows: do not invent edges where the source does not establish them.
t=intro('P1流程图与流程证据边界')
t+='实线表示文档明确表达的关系，图标题区分本项目独立设计和原站页面说明；不表示本轮在原站实际执行。虚线只指向待核实内容，不用推测补成事实流程。缺少顺序依据时保留步骤表/缺口，不强画状态机。\n\n'
for flow in b['flows']:
 t+=f'## {flow["id"]} {flow["title"]}\n\n性质：**{flow["classification"]}**。范围：'+ '、'.join(flow['moduleIds'])+f'。来源：{link_source(flow["source"])}，{flow["evidence"]}。\n\n'
 if flow['mermaid']:t+='```mermaid\n'+flow['mermaid']+'\n```\n\n'
 t+=flow['notes']+'\n\n边界：'+flow['limitation']+'\n\n'
t+='## D1–D7不重新决策\n\n'+table(['决策','已确认口径'],[
('D1','批准与生效分开；北京时间生效日00:00起，由授权HR执行并记实际时间/失败恢复。'),('D2','不得新建过去日期或继续批准过期未批单；改日期终止原单并关联新单完整重审。'),('D3','跨组织发起须覆盖双方；禁止发起人和异动本人自审。'),('D4','调出→调入两级；调入审批人仅见必要摘要。'),('D5','职级变化须在发起和每级办理时可读前后值；权限缺失不能盲审。'),('D6','驳回原因必填，原单终态及关联保留，新单全程重审。'),('D7','本包固定两级不同审批者，不扩会签/分支/委托。')])
(D/'P1_Flows.md').write_text(t)
# Review report: overview + single-register difference view.
pmods=[m for m in mods if m['p1']['sourceDepth'].startswith('P')]
fields=sum(len(p['fields']) for p in pages);navcount=sum(len(m['p1']['navigation']) for m in mods)
t=intro('P1原站盘点与需求基线｜评审材料')
t+='**结论：五类评审材料已形成统一可追溯视图，保留全部48组及59项原验收任务；本稿不宣称全量典型页面、原站规则或业务/生产验收已完成。** 仅N级模块、未提交规则及受限项逐项保留，须评审其补证范围，不能自动视为通过或豁免。\n\n'
t+=f'材料包含{len(pages)}个页面/空表证据单元、{fields}条按页面和用途区分的字段观察、{navcount}个应用子导航标签；有P级局部证据的模块{len(pmods)}组，其余{48-len(pmods)}组当前以导航或到达证据为主。证据单元可能含多个页签，字段可能重名，这些数量均不是完成率或全站唯一对象数。原站F级执行证据为0。\n\n'
t+='## 本轮目标、已有成果与缺口\n\n'+table(['交付物','接手时已有成果','本轮成果','边界与缺口'],[
('模块清单','Scope_Register已有48组，Markdown部分描述滞后','按原ID补导航、页面/字段/流程引用；更新同源视图','仅N级模块不视为典型页面盘点完成'),('页面目录','各域记录分散于观察和Source_Gaps','[页面目录](P1_Page_Catalog.md)','导航容器、同名应用、真实页面证据分层；未取正文明确保留'),('字段字典','列名、空表、部分必填/选项散落','[字段字典](P1_Field_Dictionary.md)','数据库类型、未知默认/必填/权限不推断'),('流程图','页面步骤及独立实现混有历史说明','[流程图与边界](P1_Flows.md)','D1–D7独立状态机；原站说明与F级执行分开；无依据不连线'),('差异清单','各域Source_Gaps及remaining已有','本报告下方48组差异视图＋现有各域文件','已确认设计/待核实/受限分列；原实现与历史测试保留')])
t+='\n## 核对基线与成果保护\n\n'
t+='- 实际仓库：`/workspace/sites/italent-hris`；接手分支`main`；完整HEAD `72bcf4031fb4fc62d70be8a6c1ae1c491ff90714`；接手时工作区干净，仅一个检出工作树。\n- 未发现Git写锁或可读取的项目cwd运行进程；普通ps工具失败，有界/proc检查17项不可读，运行状态结论有此边界。无本轮新开发、测试、构建或发布任务。\n- 未完学习简介保留在`checkpoint/learning-description-20260908`，`f5f5b1bd9014d4b6eeb6d32da0f03e34da3bced2`；不合并、不重置。其他既有分支全部保留。\n- v112指定部署本轮只读复核`succeeded`；源码`fdc423fcba607bd5814a0672836b55536c71ecb1`；部署ID `appgdep_6aa010f1e1e481919f2a4331af5b0184`。本轮文档提交不改变在线版本。\n- F01–F04保留历史116项API、3项组件及后续5项入口渲染证据；重叠测试不相加为覆盖数，本轮未复跑。用户仅确认成员/员工可打开；按钮缺失反馈和修复后待复验继续保留。E2不增人，多角色UAT暂缓，均非继续P1前置。\n\n'
t+='## 原站证据与独立设计分类\n\n'+table(['类别','判定','例子'],[('原站事实','N导航或P页面字段/说明，并标明来源日期','BC-F04兼职表头；BC-L11审批开关说明'),('已确认独立设计','有用户明确决定，保留实现与测试','D1–D7；不能写成北森原站制度'),('其他独立实现','仓库代码/测试仅证明本项目技术行为','学分有效期、内部排期、冻结考勤引用等；不是自动获得企业签署'),('待核实','还未取得该页/规则证据，不能当故障或已通过','再入职、薪资组依赖、仅N级模块'),('受限项','存在具体访问/提取/只读边界证据','绩效流程页无内容或无权、历史占位、禁止业务提交')])
t+='\n## 按既定顺序的领域缺口\n\n'+table(['顺序','证据与本轮增量','剩余规则'],[
('组织员工','BC-F02/03＋BC-F04兼职、F05法人、F06入职、F07员工','兼岗生效/终止、法人变更、再入职/司龄、复杂字段联动'),('干部人才','US-C/BC-C既有名册访谈；本轮标准/评定/健康度/旧干部入口','身份转换、委员会、期限、敏感栏目和模型'),('学习','BC-L01–11及师资/证书/导师；学分本轮复核另见最新记录','循环/共享、多期费用、计分精度、学分授予折抵及自动调度'),('绩效','BC-P01–06、指标/模板来源；本轮组织绩效补证','手工评级、系数、多维/组织绩效、在途更新及流程权限'),('招聘','BC-R01–08','录用、Offer扣占、电子签、渠道、外部通知'),('假勤','BC-A01–08','跨班、调休/结转、企业参数、完整月报流转'),('薪酬','BC-S01–04','薪资组依赖、法人调动核算、算薪/税社保及支付'),('自助/报表/集成','BC-I01/02、自助复盘及全量导航','角色入口、指标分母、第三方字段/方向/调度/重试')])
t+='\n## 48组差异清单（同一范围台账视图）\n\n'+table(['原范围ID/模块','原站事实边界','本项目已有独立实现','待核实/未覆盖','受限与处理'],[(m['id']+' '+m['name'],m['p1']['sourceDepth']+'；'+('、'.join(m['p1']['pageRefs']) or 'BC-NAV-20260908'),m['developed'],m['remaining']+'；'+m['p1']['sourceGap'],'详见对应页面及P1-X例外；保留范围，不在本轮开发') for m in mods])
t+='\n## 例外、建议和影响\n\n'+table(['例外','性质/范围','证据','影响','建议'],[(x['id'],x['type']+'；'+x['scope'],x['evidence'],x['impact'],x['recommendation']) for x in b['exceptions']])
t+='\n## 集中评审范围\n\n此次可评审的是：48组保留范围及证据分级、页面/字段观察的对应关系、来源不混淆、待核实及例外清单。**不请求重新决定D1–D7、不请求新增访问者、不请求在原站执行业务、不请求生产签署。**\n\n建议以此作为有例外的P1盘点基线。仅N级模块的典型页与完整规则仍在同一台账待补；如要求“全量典型页均已核实”才结束P1，则本稿不满足该更高门槛，不得自动将这些项勾选通过。用户尚未批准任何新增豁免。\n\n'
t+='后续仍按原顺序补证，优先处理M01组织视图/字段规则、再入职说明与兼岗生效，再到干部人才、学习、绩效、招聘、假勤、薪酬、自助报表集成；需要业务决定时集中给出具体原站证据、建议和影响。可通过只读帮助/已授权配置说明解决的项由唯一总控继续处理，不以F01–F04人工UAT阻断。\n\n'
t+='## 文件关系与检查\n\n`Scope_Register.json`为唯一事实源；本报告、页面目录、字段字典、流程文档及Scope_Register.md顶部均由`scripts/render-p1-baseline.py`生成。原站观察和各域Source_Gaps仍为原始来源，原验收任务及accepted标志未改。本轮仅做文档结构与引用一致性检查，不把它写成业务回归测试通过。\n'
(D/'P1_Review.md').write_text(t)
print(json.dumps({'modules':len(mods),'acceptanceTasks':len(s['acceptanceTasks']),'pageEvidenceUnits':len(pages),'fieldObservations':fields,'navigationLabels':navcount,'modulesWithPartialP':len(pmods),'modulesNavigationOrArrivalOnly':48-len(pmods),'flows':len(b['flows']),'mermaidDiagrams':sum(bool(f['mermaid']) for f in b['flows'])},ensure_ascii=False))

# P1A/P1B are a newly authorized refinement. Derive all coverage/readiness rows
# from the same register; do not alter historical acceptance flags.
if 'roadmap' in s:
 r=s['roadmap']; pb=s['p1B']; names={m['id']:m['name'] for m in mods}
 stage='## 当前路标：P0–P5与P1A/P1B（本轮新增细化）\n\n'+r['introducedBy']+'。'+r['state']+'。\n\n'
 stage+=table(['阶段','输入','工作内容','交付物','退出条件','受限项','下一步'],[(x['id']+' '+x['name'],x['input'],x['work'],x['deliverables'],x['exit'],x['limits'],x['next']) for x in r['phases']])
 stage+='\n**业务包就绪与全项目P1完成分开登记。** P1A/P1B可按包衔接；需求就绪不是业务运行验收。P3仅一个主要开发包，转序前必须记录当前包结论、未通过项、依赖影响及依据。本轮主要开发包为空，暂停功能扩展。\n\n'
 plan=R/'docs/HRIS_Project_Plan.md';old=plan.read_text();start='<!-- ROADMAP_CURRENT_START -->';end='<!-- ROADMAP_CURRENT_END -->'
 if start in old:old=old.split(start)[0]+old.split(end,1)[1]
 plan.write_text(start+'\n# 当前有效项目规划细化\n\n'+stage+end+'\n\n'+old.lstrip())
 t=intro('P1A覆盖、探索深度与缺口（48组）')
 t+='同一Scope_Register视图。局部表头/空表不是完整模块；没有访问拒绝证据时不能写“无权限”。原站只读的写入验证边界不自动构成P1A退出豁免。\n\n'
 t+=table(['范围/业务包','已观察事实证据','探索深度','推断边界','访问/取证限制','尚未探索','下一步'],[(m['id']+' '+m['name']+' / '+m['businessPackage'],m['p1']['coverage']['facts'],m['p1']['sourceDepth'],m['p1']['coverage']['inferences'],m['p1']['coverage']['restricted'],m['p1']['coverage']['unexplored'],m['p1']['coverage']['next']) for m in mods])
 (D/'P1A_Coverage.md').write_text(t)
 t=intro('P1B业务包需求就绪表')
 t+='业务包是本轮规划组织方式；共享能力仅归一个主包，消费者通过依赖引用，不重复增加范围。M20项目人力纳入组织员工、M15测评中心纳入干部人才；其招聘/学习用途仍保留跨包依赖。归属待核实项保留独立占位，不影响明确包继续编写。**当前无包被登记为需求已验收。**\n\n'
 t+=table(['顺序/业务包','全部范围ID','需求规格或输入','已确认规则','待决策/待补证','验收标准','依赖','就绪及下一步'],[(p['order'],p['id']+' '+p['name']+'：'+ '、'.join(i+' '+names[i] for i in p['moduleIds']),p['spec']+'；'+p['specKind'],p['confirmedRules'],p['pending'],p['acceptance'],p['dependencies'],p['readiness']+'；'+p['next']) for p in pb['packages']])
 t+='\n## 当前首包距离就绪的条件\n\n1. 审阅当前首包规格的对象/字段、角色、审批与执行分离、错误恢复和跨包契约；D1–D7不重问。\n2. 闭合名称唯一性等实质差异；已确认规则与其他既有独立实现不得混写。\n3. 确认本包暂缓边界及验收预期，记录评审人、日期、适用版本和例外；全M01扩展范围继续保留。\n4. 多角色UAT、按钮实际复验及云端附件验证属于P3/P4未完成事项，不是P1B编写前置。\n\n'
 t+=table(['问题','依据','建议','影响/状态'],[(x['id']+' '+x['topic'],x['basis'],x['proposal'],x['impact']+'；'+x['status']) for x in pb['reviewIssues']])
 (D/'P1B_Readiness.md').write_text(t)
 t=intro('已有实现与产品需求对应')
 t+='对应当前源码静态核对；可复用是技术候选，不是当前测试或业务验收通过。历史测试只在原Verification标注的testedSourceCommit及适用范围有效，本轮未复跑。产品源码未修改。\n\n'
 t+=table(['需求','能力','处置','代码/证据','差异与限制','验收关联'],[(x['requirement'],x['capability'],x['disposition'],x['evidence'],x['gap'],x['acceptance']) for x in pb['implementationMap']])
 t+='\n## 其余全范围实现候选\n\n'+table(['原范围/业务包','可复用候选（原登记）','需补齐（原登记）','判定'],[(m['id']+' '+m['name']+' / '+m['businessPackage'],m['developed'],m['remaining'],'待逐包对P1B核验；无需求签署，不自动确认所有已有实现') for m in mods])
 (D/'P1B_Implementation_Map.md').write_text(t)
 t=intro('本项目总体PRD（P1B评审稿）')
 t+='**目标：** 在获授权可见的参考范围内，独立建设可承载真实人事业务的系统；当前仍为私有验证成果，未具备生产验收结论。该PRD不是对北森隐藏规则的还原声明。\n\n'
 t+='## 范围、角色与来源\n\n全部48组以Scope_Register.modules为准，分包见[P1B就绪表](P1B_Readiness.md)，原站证据见[P1A覆盖表](P1A_Coverage.md)。首包规格沿用[F01–F04需求基线](F01_F04_Requirements_Baseline.md)。其他包Source_Gaps仅是规格输入，不能算已完成的PRD。\n\n平台身份、企业成员、管理员/HR/经理/审批者/员工为既有独立实现；薪酬专岗属后续包现有成果。角色不是站点访问授权；E2仅所有者可访问不代表所有角色已验收。D3–D5明确首包调动边界，其他角色完整矩阵逐包确认。\n\n'
 t+='## 对象与跨模块依赖\n\n'+table(['业务对象/生产者','消费者','契约及未确定内容'],[
 ('组织/人员/岗位/职级 BP-F','所有业务包','稳定ID关联；员工状态/当前任职与历史分离；变更后权限重新计算。兼岗/法人/再入职规则未核实，不映射成单一员工状态。'),
 ('审批/任职生效 BP-F；审批中心 BP-I','干部任用、假勤、薪酬、自助待办','首包调动批准不等于生效；干部任用核对需实际生效且岗位匹配。不得用待生效记录触发薪资回算；其他消费时点须各包确认。'),
 ('标准/资格/发展 BP-C','学习、盘点、人才档案','标准/课程/计划保持版本与证据来源；缺失不补评分；跨包引用的撤销/到期传播需各包规格明确。'),
 ('招聘录用 BP-R','入职 BP-F；电子签 BP-I','录用到人员身份/岗位关联的去重、入职前置及签署结果契约待核实；不以Offer发送冒充入职完成。'),
 ('假勤 BP-A','薪酬 BP-S、报表 BP-I','引用结算期间、冻结版本与员工稳定ID；已发布结果不得静默回写。正式结转/算薪规则与回算策略未就绪。'),
 ('附件/身份/报表/同步 BP-I及首包基础','全部消费者','只开放当前授权数据；附件撤权与历史读取以当前权限为准。指标分母、字段映射、方向、调度、重试、密钥托管及外部接口待规格；相同菜单名不等于同接口。')])
 t+='\n## 功能、校验与验收\n\n首包字段、角色矩阵、页面操作、状态机、失败分支、接口对应和Given/When/Then用例见既有首包基线的“P1B当前规格补充”。按模块对象定义校验和错误行为，不把列表列名当必填项。所有包必须覆盖正常、拒绝、越权、状态变化、并发/重复、失败恢复、历史追溯和跨包影响；原台账criteria为验收归属，内部用例不增加既有59项验收分母。\n\n'
 t+='## 暂缓及退出\n\n当前暂停功能扩展；原站无业务提交、真实数据导出；不新增访问者。自动调度、复杂审批、兼岗/再入职/法人、外部真实接口及生产切换只作为未完成范围保留，不被首包排除出全项目。P1A/P1B退出与后续阶段见[原项目规划](../HRIS_Project_Plan.md)。\n\n本PRD及分包规格均待需求评审，尚无新签署。首包规则确认、首包需求就绪、首包业务验收、全项目P1完成与生产验收各自独立，不从数量推算整体进度。\n'
 (D/'P1B_PRD.md').write_text(t)
 # Update existing queue reading entry, preserving its historical content.
 qp=D/'Module_Queue.md';old=qp.read_text();marker='<!-- P1AB_QUEUE_END -->'
 if marker in old:old=old.split(marker,1)[1].lstrip()
 head='# 当前唯一执行队列：P1A/P1B\n\n源：Scope_Register.json.roadmap及Module_Queue.json。首要工作包：'+r['activeWorkPackage']+'。主要开发包：无（暂停扩展）。\n\n'+'\n'.join(f'{i+1}. {v}' for i,v in enumerate(r['nextTasks']))+'\n\n业务顺序：'+ ' → '.join(r['businessOrder'])+'；BP-UNASSIGNED保留待核实。多角色人工UAT不阻断P1；转序不得静默跳过。下方历史队列不构成本轮执行指令。\n\n'+marker+'\n\n'
 qp.write_text(head+old)
 review=D/'P1_Review.md';old=review.read_text();old=old.replace('建议以此作为有例外的P1盘点基线。','本稿为P1A评审输入，例外尚未获批准。').replace('如要求“全量典型页均已核实”才结束P1，则本稿不满足该更高门槛','按本轮明确的P1A退出条件，本稿仍需补证和例外评审')
 review.write_text('# 当前评审状态：P1A/P1B均未验收\n\nP1A/P1B为本轮新增规划细分。当前材料覆盖范围不是完成声明。\n\n- [48组P1A覆盖与缺口](P1A_Coverage.md)\n- [总体PRD](P1B_PRD.md)\n- [分包就绪及映射](P1B_Readiness.md)\n- [已有实现与需求对应](P1B_Implementation_Map.md)\n- [当前路标及阶段退出](../HRIS_Project_Plan.md)\n\n'+old)
