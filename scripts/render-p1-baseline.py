"""Render documentation views from the existing Scope_Register.json. No app/data writes."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'docs/delivery'
s=json.loads((D/'Scope_Register.json').read_text()); b=s['p1Baseline']; mods=s['modules']; pages=b['pages']
# The original 48 module IDs and 59 tasks remain historical facts. Current
# delivery applicability is derived exclusively from this same register.
ds=s['deliveryScope']; active_ids=set(ds['currentModuleIds'])
active_mods=[m for m in mods if m['id'] in active_ids]
deferred_mods=[m for m in mods if m['id'] not in active_ids]
def scope_status(mid):return '当前交付' if mid in active_ids else '本次交付暂缓（历史保留）'
def assessment(m):return m['p1']['currentDeliveryAssessment']
def pack_current(pack):return [i for i in pack['moduleIds'] if i in active_ids]
def pack_conditions(pack):
 current=pack_current(pack)
 if not current:
  return ['本包无当前独立交付模块；历史规格与缺口保留，不阻当前15模块P1退出。'] if pack['moduleIds'] else []
 return [m['id']+' '+m['name']+'：'+assessment(m)['basis'] for m in mods if m['id'] in current]+['六类基础能力与必要接口单列核验；33暂缓模块不阻当前退出。']
def pack_pending(pack):return '；'.join(pack_conditions(pack)) or '当前无未归属模块。'
def ct_scope(c):
 a=c['currentApplicability']
 return a['status']+'；'+('、'.join(a['moduleIds']+a['baseCapabilityIds']) or '无当前独立要求')+'；'+a['note']
def progress_text():
 return ('P1A完成 '+str(sum(assessment(m)['p1A']=='complete' for m in active_mods))+'/15；'
         'P1B需求就绪 '+str(sum(assessment(m)['p1B']=='ready' for m in active_mods))+'/15；'
         'P1评审通过 '+str(sum(assessment(m)['review']=='signed' for m in active_mods))+'/15。'
         '批准的受限结论 '+str(sum(assessment(m)['approvedRestricted'] for m in active_mods))+'项，单列不混入完整通过。')

def esc(v):
 if v is None:return '未核实'
 if isinstance(v,list):v='；'.join(v)
 return str(v).replace('|','\\|').replace('\n','<br>')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(esc(c) for c in row)+' |' for row in rows)+'\n'
def link_source(path):return '['+Path(path).name+']('+str(Path('../../')/path)+')'
def page_link(p):return '[详见证据]('+str(Path('../../')/p['source'])+')：'+p['evidenceRef']
def intro(title):return f'# {title}\n\n生成来源：`Scope_Register.json → deliveryScope / p1Baseline / modules[].p1 / p1B`。本文是同一台账的阅读视图，不独立维护范围或验收状态。更新时间：{b["updatedAt"]}。\n\n当前交付为用户确认的15个HR核心模块及六类非模块基础能力；原48组历史完整保留，33组本次交付暂缓，不计完成、不阻当前P1退出。各历史证据的适用时间保持。\n\n'
def current_scope_table():
 return table(['范围','模块ID及名称','当前边界'],[
 ('当前15模块','、'.join(m['id']+' '+m['name'] for m in active_mods),ds['internalBoundary']),
 ('本次暂缓33模块','、'.join(m['id']+' '+m['name'] for m in deferred_mods),ds['deferredPolicy'])])
def progress_table():
 labels={'in_progress':'进行中（未达完整退出）','not_ready':'未就绪','not_signed':'待业务评审签署','complete':'完整完成','ready':'需求就绪','signed':'评审通过','not_assessed':'待判定'}
 return table(['模块/主包','P1A','P1B','P1评审','具体缺口/判断依据','待决定项'],[(m['id']+' '+m['name']+' / '+m['businessPackage'],labels.get(assessment(m)['p1A'],assessment(m)['p1A']),labels.get(assessment(m)['p1B'],assessment(m)['p1B']),labels.get(assessment(m)['review'],assessment(m)['review']),assessment(m)['basis'],assessment(m)['blockingIssueIds']) for m in active_mods])

# Keep the whole historical register and prepend the current, source-derived view.
f=D/'Scope_Register.md';old=f.read_text();marker='<!-- P1_CURRENT_END -->'
if marker in old:old=old.split(marker,1)[1].lstrip()
head=intro('原48组历史范围与当前15模块P1总表')
head+=current_scope_table()+'\n'+progress_text()+'\n\n'
head+='48组范围、59个原验收任务完整保留；本轮P1证据单元不增加验收分母。N=导航，P=局部页面/字段/说明，F=原站实际流程结果。F级只由实际执行证据判定，拟定场景不算结果；当前数据验证边界见P1_Review。已开发/技术通过/人工业务与生产签署分别记录。\n\n'
head+='入口：[P1评审材料](P1_Review.md) · [页面目录](P1_Page_Catalog.md) · [字段字典](P1_Field_Dictionary.md) · [流程与边界](P1_Flows.md)。\n\n'
head+=table(['范围ID','模块','当前适用','原登记范围','原站证据深度','页面证据单元','当前部分实现','仍待核实/实现','生产'],[(m['id'],m['name'],scope_status(m['id']),m['scope'],m['p1']['sourceDepth'],'、'.join(m['p1']['pageRefs']) or 'BC-NAV-20260908（仅导航）',m['developed'],m['remaining'],m['productionAccepted']) for m in mods])
head+='\n下方为历史快照，不覆盖上述当前JSON及本轮用户决定。\n\n'+marker+'\n\n';f.write_text(head+old)
# Page catalog: explicitly separate containers/menu entries from page evidence units.
t=intro('P1页面目录与导航索引')
t+='此目录包含“已观察导航条目”和“页面证据单元”两层。导航可能是容器或同名入口，不能按条目数计作独立页面数；部分证据单元合并了列表、空表或多个页签。缺少唯一URL的页面用可重走的菜单路径定位，禁止保存带认证参数的原站URL。\n\n'
t+='角色统一限制：当前已授权账号可见；不因此证明HR、经理、员工或管理员的完整角色矩阵。列表列名也不能证明其在每个角色下均可见。\n\n'
t+='## 全量导航索引\n\n'+table(['模块ID','应用','当前适用','已观察子导航（N）','页面补证情况'],[(m['id'],m['name'],scope_status(m['id']),'、'.join(m['p1']['navigation']),m['p1']['sourceDepth']) for m in mods])
t+='\n## 已定位页面与空表证据\n\n'
for m in mods:
 pp=[p for p in pages if p['moduleId']==m['id']]
 if not pp:continue
 t+=f'### {m["id"]} {m["name"]} — {scope_status(m["id"])}\n\n'
 t+=table(['页面证据ID','路径/页面','证据等级及日期','字段观察数','状态/页签/说明','来源','未核实及受限项'],[(p['id'],p['path'],p['level']+'；'+p['observedDate'],len(p['fields']),(p['visibleStates']+'；'+p['sourceStatement']).strip('；'),page_link(p),p['unknown']) for p in pp])+'\n'
t+='## 通用页面属性边界\n\n原规划模板要求的布局、排序、错误提示、详情页签、前后置条件及权限，仅在来源明确记载时适用。没有独立证据的属性统一为未核实；仅具体执行记录可证明已诱发的校验结果；没有执行证据的不从本项目代码补写原站默认值。操作入口只证明存在。\n'
(D/'P1_Page_Catalog.md').write_text(t)
# Field dictionary: true/false/null remain distinguishable.
t=intro('P1字段字典（页面观察层）')
t+='每行是某页面某用途下的一条字段观察，重复标签不合并；本表行数不是原站唯一字段总数。存储类型一律未核实，日期/金额/ID名称不能证明数据库类型。`未核实`不代表无约束；`是/否`仅在原记录明确说明时填写。已观察选项不是未经证明的全集。\n\n敏感字段仅收录标签，不收录任何人员、证件、联系方式、薪资、访谈或成绩值。字段来源沿用其页面证据编号；筛选/列表列不附会表单必填。\n\n'
for m in mods:
 pp=[p for p in pages if p['moduleId']==m['id'] and p['fields']]
 if not pp:continue
 t+=f'## {m["id"]} {m["name"]} — {scope_status(m["id"])}\n\n'
 for p in pp:
  t+=f'### {p["id"]} — {p["path"]}\n\n来源：{page_link(p)}。日期：{p["observedDate"]}；等级：{p["level"]}。\n\n'
  t+=table(['字段观察ID','标签','用途','界面控件类型','原站声明类型/来源','存储类型','必填','默认观察','选项/限制'],[(f['id'],f['label'],f['context'],f.get('controlType'),('；'.join(v for v in [f.get('sourceType'),f.get('dataSource')] if v) or None),f['storageType'],'是' if f['required'] is True else '否' if f['required'] is False else '界面必填标记；服务端未核实' if f.get('uiRequired') is True else '未核实',f['default'],('；'.join(f['options']) if f['options'] else '')+('；'+f['limit'] if f['limit'] else '') or '未核实') for f in p['fields']])+'\n'
t+='## 尚无可追溯字段字典的模块\n\n'+table(['模块','已有证据','保留缺口'],[(m['id']+' '+m['name'],'BC-NAV-20260908；'+m['p1']['sourceDepth'],m['p1']['sourceGap']) for m in mods if not m['p1']['fieldRefs']])
(D/'P1_Field_Dictionary.md').write_text(t)
# Flows: do not invent edges where the source does not establish them.
t=intro('P1流程图与流程证据边界')
t+='实线表示文档明确表达的关系，图标题区分本项目独立设计和原站页面说明；是否执行以各条合成操作记录为准，图本身不证明执行。虚线只指向待核实内容，不用推测补成事实流程。缺少顺序依据时保留步骤表/缺口，不强画状态机。\n\n'
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
t+='**当前范围状态：** '+progress_text()+'六类基础能力另列；当前15模块均有局部证据及未关闭缺口，未代签任何业务评审。原48组/59项保持历史，33组暂缓不作为当前P1阻塞。\n\n'+current_scope_table()+'\n'
t+='页面/字段/导航数量仅为历史索引规模，不用于进度。完整完成/就绪/评审通过由15模块退出证据分别判定；仅见菜单、空表或单条执行成功均不足。\n\n'+progress_table()+'\n'
t+='## 本轮目标、已有成果与缺口\n\n'+table(['交付物','接手时已有成果','本轮成果','边界与缺口'],[
('模块清单','Scope_Register已有48组，Markdown部分描述滞后','按原ID补导航、页面/字段/流程引用；更新同源视图','仅N级模块不视为典型页面盘点完成'),('页面目录','各域记录分散于观察和Source_Gaps','[页面目录](P1_Page_Catalog.md)','导航容器、同名应用、真实页面证据分层；未取正文明确保留'),('字段字典','列名、空表、部分必填/选项散落','[字段字典](P1_Field_Dictionary.md)','数据库类型、未知默认/必填/权限不推断'),('流程图','页面步骤及独立实现混有历史说明','[流程图与边界](P1_Flows.md)','D1–D7独立状态机；原站说明与F级执行分开；无依据不连线'),('差异清单','各域Source_Gaps及remaining已有','本报告下方48组差异视图＋现有各域文件','已确认设计/待核实/受限分列；原实现与历史测试保留')])
t+='\n## 历史接手与部署记录（下列本轮措辞属于上轮快照，非本次复验）\n\n'
t+='- 实际仓库：`/workspace/sites/italent-hris`；接手分支`main`；完整HEAD `72bcf4031fb4fc62d70be8a6c1ae1c491ff90714`；接手时工作区干净，仅一个检出工作树。\n- 未发现Git写锁或可读取的项目cwd运行进程；普通ps工具失败，有界/proc检查17项不可读，运行状态结论有此边界。无本轮新开发、测试、构建或发布任务。\n- 未完学习简介保留在`checkpoint/learning-description-20260908`，`f5f5b1bd9014d4b6eeb6d32da0f03e34da3bced2`；不合并、不重置。其他既有分支全部保留。\n- v112指定部署本轮只读复核`succeeded`；源码`fdc423fcba607bd5814a0672836b55536c71ecb1`；部署ID `appgdep_6aa010f1e1e481919f2a4331af5b0184`。本轮文档提交不改变在线版本。\n- F01–F04保留历史116项API、3项组件及后续5项入口渲染证据；重叠测试不相加为覆盖数，本轮未复跑。用户仅确认成员/员工可打开；按钮缺失反馈和修复后待复验继续保留。E2不增人，多角色UAT暂缓，均非继续P1前置。\n\n'
t+='## 原站证据与独立设计分类\n\n'+table(['类别','判定','例子'],[('原站事实','N导航或P页面字段/说明，并标明来源日期','BC-F04兼职表头；BC-L11审批开关说明'),('已确认独立设计','有用户明确决定，保留实现与测试','D1–D7；不能写成北森原站制度'),('其他独立实现','仓库代码/测试仅证明本项目技术行为','学分有效期、内部排期、冻结考勤引用等；不是自动获得企业签署'),('待核实','还未取得该页/规则证据，不能当故障或已通过','再入职、薪资组依赖、仅N级模块'),('受限项','存在具体访问/角色/外部动作限制证据','单角色、不可用页面、外部通知/真实交易未授权；合成保存权限已明确')])
t+='\n## 按既定顺序的领域缺口\n\n'+table(['业务包','证据与当前规格','未就绪条件与下一步'],[(p['name'], '、'.join(ref for m in active_mods if m['id'] in p['moduleIds'] for ref in m['p1']['pageRefs'])+'；'+link_source(p['spec']),p['readiness']+'；'+pack_pending(p)+'；'+p['next']) for p in s['p1B']['packages'] if pack_current(p)])

t+='\n## 48组差异清单（同一范围台账视图）\n\n'+table(['原范围ID/模块','当前适用','原站事实边界','本项目已有独立实现','待核实/未覆盖','受限与处理'],[(m['id']+' '+m['name'],scope_status(m['id']),m['p1']['sourceDepth']+'；'+('、'.join(m['p1']['pageRefs']) or 'BC-NAV-20260908'),m['developed'],m['remaining']+'；'+m['p1']['sourceGap'],'详见对应页面及P1-X例外；保留范围，不在本轮开发') for m in mods])
t+='\n## 例外、建议和影响\n\n'+table(['例外','性质/范围','证据','影响','建议'],[(x['id'],x['type']+'；'+x['scope'],x['evidence'],x['impact'],x['recommendation']) for x in b['exceptions']])
t+='\n## 集中评审范围\n\n此次评审对象是当前15模块及基础能力：保留原48组历史对应、当前适用证据分级、字段/流程/权限/验收、依赖与例外。33组独立规则不作当前退出门槛。**不请求重新决定D1–D7、不请求新增访问者、原站合成权限持续有效、不请求生产签署。**\n\n建议以此作为有例外的P1盘点基线。当前15模块的典型链及完整规则仍在同一台账待补；当前仍不满足现交付范围P1A/P1B退出条件；未探索、受限、待决策与待签署均须逐项保留，不得自动勾选通过。用户尚未批准任何新增豁免。\n\n'
t+='后续按当前同源队列推进保留模块，组织员工→干部人才→学习→绩效→招聘→假勤→薪酬；M19/M48/M32随链同步。已授权合成操作继续，当前独立业务决定集中，局部阻塞不停止其他模块；F01–F04人工UAT不是P1编写前置。\n\n'
t+='## 文件关系与检查\n\n`Scope_Register.json`为唯一事实源；本报告、页面目录、字段字典、流程文档及Scope_Register.md顶部均由`scripts/render-p1-baseline.py`生成。原站观察和各域Source_Gaps仍为原始来源，原验收任务及accepted标志未改。本轮仅做文档结构与引用一致性检查，不把它写成业务回归测试通过。\n'
(D/'P1_Review.md').write_text(t)
print(json.dumps({'modules':len(mods),'acceptanceTasks':len(s['acceptanceTasks']),'pageEvidenceUnits':len(pages),'fieldObservations':fields,'navigationLabels':navcount,'modulesWithPartialP':len(pmods),'modulesNavigationOrArrivalOnly':48-len(pmods),'flows':len(b['flows']),'mermaidDiagrams':sum(bool(f['mermaid']) for f in b['flows'])},ensure_ascii=False))

# P1A/P1B are a newly authorized refinement. Derive all coverage/readiness rows
# from the same register; do not alter historical acceptance flags.
if 'roadmap' in s:
 r=s['roadmap']; pb=s['p1B']; names={m['id']:m['name'] for m in mods}
 stage='## 当前路标：P0–P5与P1A/P1B（用户新增细化）\n\n'+r['introducedBy']+'。'+r['state']+'。\n\n'
 stage+=current_scope_table()+'\n'+progress_text()+'\n\n'
 stage+=table(['阶段','输入','工作内容','交付物','退出条件','受限项','下一步'],[(x['id']+' '+x['name'],x['input'],x['work'],x['deliverables'],x['exit'],x['limits'],x['next']) for x in r['phases']])
 stage+='\n**业务包就绪与全项目P1完成分开登记。** P1A/P1B可按包衔接；需求就绪不是业务运行验收。P3仅一个主要开发包，转序前必须记录当前包结论、未通过项、依赖影响及依据。本轮主要开发包为空，暂停功能扩展。\n\n'
 plan=R/'docs/HRIS_Project_Plan.md';old=plan.read_text();start='<!-- ROADMAP_CURRENT_START -->';end='<!-- ROADMAP_CURRENT_END -->'
 if start in old:old=old.split(start)[0]+old.split(end,1)[1]
 plan.write_text(start+'\n# 当前有效项目规划细化\n\n'+stage+end+'\n\n'+old.lstrip())
 t=intro('P1A当前15模块覆盖与缺口；33组历史暂缓')
 t+=progress_text()+'\n\n'+progress_table()+'\n'
 t+='同一Scope_Register视图。局部表头/空表不是完整模块；没有访问拒绝证据时不能写“无权限”。原站测试操作授权不自动构成P1A退出豁免。\n\n'
 t+=table(['范围/业务包','已观察事实证据','探索深度','推断边界','访问/取证限制','尚未探索','下一步'],[(m['id']+' '+m['name']+' / '+m['businessPackage'],m['p1']['coverage']['facts'],m['p1']['sourceDepth'],m['p1']['coverage']['inferences'],m['p1']['coverage']['restricted'],m['p1']['coverage']['unexplored'],m['p1']['coverage']['next']) for m in active_mods])
 t+='\n## 33组本次交付暂缓（不计完成、不阻当前退出）\n\n'+table(['原ID/模块','历史证据','已有深度/缺口','后续'],[(m['id']+' '+m['name'],m['p1']['pageRefs'],m['p1']['sourceDepth']+'；'+m['p1']['sourceGap'],m['p1']['coverage']['next']) for m in deferred_mods])
 (D/'P1A_Coverage.md').write_text(t)
 t=intro('P1B业务包需求就绪表')
 t+='业务包是本轮规划组织方式；共享能力仅归一个主包，消费者通过依赖引用，不重复增加范围。历史48组主包映射不改；M20/M15等当前暂缓成员保留历史映射且退出当前包就绪门槛。M19/M48/M32由BP-I主责，随各业务链同步；空占位不增加包或模块分母。**当前无包被登记为需求已验收。**\n\n'
 t+=table(['顺序/业务包','全部范围ID','需求规格或输入','已确认规则','待决策/待补证','验收标准','依赖','就绪及下一步'],[(p['order'],p['id']+' '+p['name']+'：'+ '、'.join(i+' '+names[i]+'（'+scope_status(i)+'）' for i in p['moduleIds']),p['spec']+'；'+p['specKind'],p['confirmedRules'],pack_pending(p),p['acceptance'],p['dependencies'],p['readiness']+'；'+p['next']) for p in pb['packages']])
 t+='\n## 当前首包距离就绪的条件\n\n1. 审阅当前首包规格的对象/字段、角色、审批与执行分离、错误恢复和跨包契约；D1–D7不重问。\n2. 闭合名称唯一性等实质差异；已确认规则与其他既有独立实现不得混写。\n3. 确认本包暂缓边界及验收预期，记录评审人、日期、适用版本和例外；全M01扩展范围继续保留。\n4. 多角色UAT、按钮实际复验及云端附件验证属于P3/P4未完成事项，不是P1B编写前置。\n\n'
 t+='待决策事项统一见下方最小必要决策记录；推荐不作为批准要求。\n\n'
 (D/'P1B_Readiness.md').write_text(t)
 t=intro('已有实现与产品需求对应')
 t+='对应当前源码静态核对；可复用是技术候选，不是当前测试或业务验收通过。历史测试只在原Verification标注的testedSourceCommit及适用范围有效，本轮未复跑。产品源码未修改。\n\n'
 t+=table(['需求','能力','当前适用','处置','代码/证据','差异与限制','验收关联'],[(x['requirement'],x['capability'],ct_scope(x),x['disposition'],x['evidence'],x['gap'],x['acceptance']) for x in pb['implementationMap']])
 t+='\n## 原48组实现候选与当前适用（历史资产保留）\n\n'+table(['原范围/业务包','当前适用','可复用候选（原登记）','需补齐（原登记）','判定'],[(m['id']+' '+m['name']+' / '+m['businessPackage'],scope_status(m['id']),m['developed'],m['remaining'],'待逐包对P1B核验；无需求签署，不自动确认所有已有实现') for m in mods])
 (D/'P1B_Implementation_Map.md').write_text(t)
 t=intro('本项目总体PRD（P1B评审稿）')
 t+='**目标：** 在获授权可见的参考范围内，独立建设可承载真实人事业务的系统；当前仍为私有验证成果，未具备生产验收结论。该PRD不是对北森隐藏规则的还原声明。\n\n'
 t+='## 范围、角色与来源\n\n原48组历史以Scope_Register.modules为准，当前15及暂缓33由deliveryScope明确，分包见[P1B就绪表](P1B_Readiness.md)，原站证据见[P1A覆盖表](P1A_Coverage.md)。首包规格沿用[F01–F04需求基线](F01_F04_Requirements_Baseline.md)。其他包Source_Gaps仅是规格输入，不能算已完成的PRD。\n\n平台身份、企业成员、管理员/HR/经理/审批者/员工为既有独立实现；薪酬专岗属后续包现有成果。角色不是站点访问授权；E2仅所有者可访问不代表所有角色已验收。D3–D5明确首包调动边界，其他角色完整矩阵逐包确认。\n\n'
 t+='## 对象与跨模块依赖\n\n'+table(['业务对象/生产者','消费者','契约及未确定内容'],[
 ('组织/人员/岗位/职级 BP-F','所有业务包','稳定ID关联；员工状态/当前任职与历史分离；变更后权限重新计算。兼职/法人/未来离职已有合成执行局部证据，再入职和完整规则仍受限，不映射成单一员工状态。'),
 ('审批/任职生效 BP-F；审批中心 BP-I','干部任用、假勤、薪酬、自助待办','首包调动批准不等于生效；干部任用核对需实际生效且岗位匹配。不得用待生效记录触发薪资回算；其他消费时点须各包确认。'),
 ('标准/资格/发展 BP-C','学习、盘点、人才档案','标准/课程/计划保持版本与证据来源；缺失不补评分；跨包引用的撤销/到期传播需各包规格明确。'),
 ('招聘录用 BP-R','入职 BP-F；电子签 BP-I','录用到人员身份/岗位关联的去重、入职前置及签署结果契约待核实；不以Offer发送冒充入职完成。'),
 ('假勤 BP-A','薪酬 BP-S、报表 BP-I','引用结算期间、冻结版本与员工稳定ID；已发布结果不得静默回写。正式结转/算薪规则与回算策略未就绪。'),
 ('附件/身份/报表/同步 BP-I及首包基础','全部消费者','只开放当前授权数据；附件撤权与历史读取以当前权限为准。指标分母、字段映射、方向、调度、重试、密钥托管及外部接口待规格；相同菜单名不等于同接口。')])
 t+='\n## 功能、校验与验收\n\n首包字段、角色矩阵、页面操作、状态机、失败分支、接口对应和Given/When/Then用例见既有首包基线的“P1B当前规格补充”。按模块对象定义校验和错误行为，不把列表列名当必填项。所有包必须覆盖正常、拒绝、越权、状态变化、并发/重复、失败恢复、历史追溯和跨包影响；原台账criteria为验收归属，内部用例不增加既有59项验收分母。\n\n'
 t+='## 暂缓及退出\n\n当前暂停产品功能扩展；原站仅在最新授权内操作明确标记的合成测试记录；不导出真实数据，不新增访问者。15模块内原登记的自动调度、复杂审批、兼岗/再入职/法人等继续保留；独立AI与33模块按用户决定暂缓。外部服务仅必要接口契约/状态/失败处理，供应商开通与真实交易不是P1前置；生产切换不在本轮。P1A/P1B退出与后续阶段见[原项目规划](../HRIS_Project_Plan.md)。\n\n本PRD及分包规格均待需求评审，尚无新签署。首包规则确认、首包需求就绪、首包业务验收、全项目P1完成与生产验收各自独立，不从数量推算整体进度。\n'
 (D/'P1B_PRD.md').write_text(t)
 # Update existing queue reading entry, preserving its historical content.
 qp=D/'Module_Queue.md';old=qp.read_text();marker='<!-- P1AB_QUEUE_END -->'
 if marker in old:old=old.split(marker,1)[1].lstrip()
 head='# 当前唯一执行队列：P1A/P1B\n\n源：Scope_Register.json.roadmap及Module_Queue.json。首要工作包：'+r['activeWorkPackage']+'。主要开发包：无（暂停扩展）。\n\n'+'\n'.join(f'{i+1}. {v}' for i,v in enumerate(r['nextTasks']))+'\n\n业务顺序：'+ ' → '.join(r['businessOrder'])+'；BP-UNASSIGNED仅保留归属核实历史；无成员时不计业务包。多角色人工UAT不阻断P1；转序不得静默跳过。下方历史队列不构成本轮执行指令。\n\n'+marker+'\n\n'
 qp.write_text(head+old)
 review=D/'P1_Review.md';old=review.read_text();old=old.replace('建议以此作为有例外的P1盘点基线。','本稿为P1A评审输入，例外尚未获批准。').replace('如要求“全量典型页均已核实”才结束P1，则本稿不满足该更高门槛','按本轮明确的P1A退出条件，本稿仍需补证和例外评审')
 review.write_text('# 当前评审状态：P1A/P1B均未验收\n\nP1A/P1B为本轮新增规划细分。当前材料覆盖范围不是完成声明。\n\n- [当前15模块P1A覆盖及33组暂缓](P1A_Coverage.md)\n- [总体PRD](P1B_PRD.md)\n- [分包就绪及映射](P1B_Readiness.md)\n- [已有实现与需求对应](P1B_Implementation_Map.md)\n- [当前路标及阶段退出](../HRIS_Project_Plan.md)\n\n'+old)

# Detailed pack specifications remain views of the same authoritative register.
if 'p1B' in s:
 pb=s['p1B']; by_id={m['id']:m for m in mods}
 for pack in pb['packages']:
  if 'contracts' not in pack:continue
  t=intro(pack['id']+' '+pack['name']+'｜产品需求规格评审稿')
  t+='**状态：'+pack['specStatus']+'。'+pack['readiness']+'。** 不以文档生成代替需求签署；本项目既有实现事实与原站事实分别列出。\n\n'
  t+='## 目标、范围和暂缓\n\n'+pack['goal']+'\n\n'
  t+=table(['原范围ID','模块','当前适用','原登记范围','原验收归属'],[(i,by_id[i]['name'],scope_status(i),by_id[i]['scope'],'、'.join(a['id'] for a in s['acceptanceTasks'] if a['moduleId']==i) or '沿用原范围登记；未新造验收任务') for i in pack['moduleIds']])
  t+='\n本轮暂停产品实现、部署和新增测试访问者；原站关联数据验证依最新已确认授权执行，实际结果以同源dataValidation.operations为准。15模块内待补项继续纳入当前需求；其余成员独立需求明确历史暂缓，不列当前就绪门槛。完整历史内容保留，不代表当前主动探索。输入：'+link_source(pack['inputEvidence'])+'。\n\n'
  if pack.get('authoritativeDetail'):t+='首要子包详细需求：'+link_source(pack['authoritativeDetail'])+'；D1–D7保持已确认，不以本文件重开决策。\n\n'
  t+='## 已具体化的对象与行为契约\n\n下列“验收预期”是对已确认规则或既有实现候选行为的可执行描述，**未表示已执行或已获企业批准**。仅D1–D7保持既有签署；其他候选约束不得直接用作新开发授权。\n\n'
  if not pack['moduleIds']:t+='当前无未归属范围；历史三组依据见[P1B就绪表](P1B_Readiness.md)。此文件不是新增业务包或需求完成声明。\n\n'
  if not pack['contracts'] and pack['moduleIds']:t+='本组职责和对象字段尚不足以形成行为契约，先保留逐模块证据和候选归属；不以空模板冒充需求完成。\n\n'
  for ct in pack['contracts']:
   t+='### '+ct['id']+' '+ct['object']+' — '+ct['currentApplicability']['status']+'\n\n**当前适用：'+ct_scope(ct)+'**\n\n性质：'+ct['classification']+'。下表保留原契约内容；混合/暂缓部分以当前适用边界为准，不作为当前完整模块前置。\n\n'
   t+=table(['维度','规格及当前边界'],[('对象/字段/校验',ct['fields']),('角色/数据范围/字段权限',ct['roles']),('状态/审批/生效',ct['lifecycle']),('页面主要操作',ct['actions']),('验收预期（给定条件→操作→结果）',ct['acceptance']),('例外、恢复与仍缺内容',ct['gap']),('静态实现/输入依据','；'.join(link_source(x) for x in ct['codeRefs']))])+'\n'
   if ct.get('fieldDetails'):
    t+='字段与对象细化（来源逐项区分，不用代码补原站事实）：\n\n'+table(['字段/对象','定义及关联','校验/范围','来源与状态'],[(x['field'],x['definition'],x['constraints'],x['basis']) for x in ct['fieldDetails']])+'\n'
   if ct.get('roleMatrix'):
    t+='角色与字段权限边界：\n\n'+table(['角色/身份','可读范围','可执行动作','限制与来源'],[(x['role'],x['read'],x['write'],x['boundary']) for x in ct['roleMatrix']])+'\n'
   if ct.get('stateTransitions'):
    t+='状态转换（原站与本项目现有实现分开）：\n\n'+table(['起始状态','动作','结果状态','条件/异常','证据性质'],[(x['from'],x['event'],x['to'],x['guards'],x['basis']) for x in ct['stateTransitions']])+'\n'
   if ct.get('acceptanceCases'):
    t+='可执行验收场景细化：这些是原任务下的场景，不新增验收分母；候选要求未批准，历史测试不视为本轮复验。\n\n'+table(['场景ID','给定条件','操作','期望/待定边界','来源与执行状态'],[(x['id'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in ct['acceptanceCases']])+'\n'
  t+='## 当前模块及历史成员原站证据（当前适用逐项标明）\n\n每个模块均保留页面、字段、角色/状态、依赖/接口四类证据边界。未探索不是无权限；没有提交验证也不能推断规则通过。\n\n'
  for mid in pack['moduleIds']:
   m=by_id[mid]; pp=[p for p in pages if p['moduleId']==mid]
   t+='### '+mid+' '+m['name']+' — '+scope_status(mid)+'\n\n'
   t+='页面与主要入口：'+ '、'.join(m['p1']['navigation'])+'。当前探索深度：'+m['p1']['sourceDepth']+'。\n\n'
   if pp:t+=table(['证据/观察时间','实际页面与操作','字段属性边界','角色/状态/跨模块线索与限制'],[(p['id']+'；'+p.get('observedAt',p['observedDate']),p['path']+'；'+p['operations'],('、'.join(f['label'] for f in p['fields']) or '未取得字段')+'；完整类型/必填/默认/枚举/校验/可见性逐字段见P1_Field_Dictionary',p['sourceStatement']+'；'+p['unknown']+'；'+page_link(p)) for p in pp])+'\n'
   else:t+='仅导航证据`'+m['p1']['navigationEvidence']+'`；尚未取得该模块字段/空表/说明，不能借相似应用补证。\n\n'
   t+=table(['维度','具体需求缺口及处置'],[('字段类型/必填/默认/枚举/校验/关联',m['p1']['sourceGap']+'；按实际页逐属性补证，不把字段名解释为数据库类型'),('角色、状态、审批、生效与异常',m['remaining']+'；未核实部分不设置默认批准/自动恢复'),('跨模块及外部接口','见下方包依赖；具体endpoint/认证/请求响应/错误与重试没有证据则待核实，不从导航“接口”推断已接通'),('既有实现可复用候选',m['developed']),('限制与下一步',scope_status(mid)+'；'+m['p1']['coverage']['restricted']+'；'+m['p1']['coverage']['next'])])+'\n'
  t+='## 依赖、接口及验收归属\n\n业务包依赖：'+('、'.join(pack['dependencies']) or '尚未确认跨包输入，仍核对全局契约')+'。公共身份、稳定ID、当前权限、版本/时间、字段缺失与状态分离见[总体PRD](P1B_PRD.md)。上游未就绪只阻塞对应消费契约，其他需求继续。内部源码路径证明已存在的适配行为，不作为原站外部接口证据。\n\n'
  api_paths=sorted({v for ct in pack['contracts'] for v in ct['codeRefs'] if v.startswith('app/api/')})
  if api_paths:t+='已读内部接口：'+ '；'.join(link_source(v) for v in api_paths)+'。\n\n'
  t+=table(['原任务','验收条件（原样保留）','当前规则/验证状态'],[(a['id']+' '+a['title'],'；'.join(c['text'] for c in a['criteria']),'原accepted保持；本稿不代签，历史测试按原版本') for a in s['acceptanceTasks'] if a['moduleId'] in pack['moduleIds']])+'\n'
  t+='## 就绪、待决策与下一步\n\n'+pack['currentScopeNote']+'。'+pack_pending(pack)+'。'+pack['next']+'。\n\n需求就绪需要：受影响对象字段和行为无未决歧义；角色/字段范围、状态与恢复、跨包契约及验收预期经过评审；如有例外，记录授权、范围和影响。当前缺少上述完整评审，不满足转入新开发包条件。人工多角色UAT暂缓不阻止本稿继续细化。\n'
  if pack_conditions(pack):t+='\n'+table(['具体就绪条件'],[(v,) for v in pack_conditions(pack)])+'\n'
  (R/pack['spec']).write_text(t.rstrip()+'\n')
 prd=D/'P1B_PRD.md';t=prd.read_text().replace('其他包Source_Gaps仅是规格输入，不能算已完成的PRD。','各包已有同源生成的规格评审稿；其中仅导航部分明确列出受限原因，不计为完整需求就绪。原Source_Gaps继续作为证据输入。')
 t+='\n## 业务包规格入口\n\n'+table(['包','规格','状态'],[(p['id'],link_source(p['spec']),p['readiness']) for p in pb['packages']])
 if pb.get('globalContracts'):
  t+='\n## 全局术语与跨包一致性契约（评审稿）\n\n'+table(['对象/术语','生产者→消费者','当前适用','统一语义/候选约束','证据与限制'],[(x['term'],x['dependency'],x['currentApplicability'],x['contract'],x['evidence']) for x in pb['globalContracts']])
 prd.write_text(t)
 read=D/'P1B_Readiness.md';t=read.read_text();t+='\n## 最小必要决策记录（同源，不新建台账）\n\n'
 t+=table(['ID/事项','现状及证据','推荐（未批准）','备选','阻塞范围/状态'],[(x['id']+' '+x['topic'],x['basis'],x['proposal'],x.get('alternatives',[]),x['impact']+'；'+x['status']) for x in pb['reviewIssues'] if x.get('decisionRequired',True)])
 resolved=[x for x in pb['reviewIssues'] if not x.get('decisionRequired',True) and x.get('decision')]
 if resolved:t+='\n## 已明确的执行范围（保留历史，不重复询问）\n\n'+table(['事项','结论/时间'],[(x['id']+' '+x['topic'],x.get('decision',x['status'])+'；'+x.get('decidedAt','')) for x in resolved])
 followups=[x for x in pb['reviewIssues'] if not x.get('decisionRequired',True) and not x.get('decision')]
 if followups:t+='\n## 先补证后评审的事项（未获批准，暂不要求即时选择）\n\n'+table(['事项','现状/证据','建议及备选（均未批准）','受影响范围/下一步'],[(x['id']+' '+x['topic'],x['basis'],x['proposal']+'；备选：'+esc(x.get('alternatives',[])),x['impact']+'；'+x['status']) for x in followups])
 t+='\n## 各包具体就绪缺口\n\n'+table(['业务包','仍需满足的条件'],[(p['id']+' '+p['name'],pack_conditions(p)) for p in pb['packages'] if p['moduleIds']])
 read.write_text(t)

 f=D/'P1B_Implementation_Map.md';t=f.read_text()+'\n## 分包契约与实现证据索引\n\n此索引由同一Scope的contracts生成。源码链接只证明静态对应；原站说明或范围文件不能证明已有实现。具体复用/补齐/修改边界按对应规格的差异列评审。\n\n'
 t+=table(['业务包/需求ID','对象与规格','当前适用','证据性质','代码或来源','具体差异/待核验'],[(p['id']+'/'+c['id'],c['object']+'；'+link_source(p['spec']),ct_scope(c),c['classification'],'；'.join(link_source(x) for x in c['codeRefs']),c['gap']) for p in pb['packages'] for c in p.get('contracts',[])])
 f.write_text(t)

 if pb.get('validationEvidence'):
  f=D/'P1B_Implementation_Map.md';t=f.read_text()+'\n## 历史验证适用版本索引\n\n当前仅读原验证记录，不复跑、不汇总通过数量。baseCommit只作测试前上下文，不能冒充测试代码快照。部分文件哈希不能证明完整环境/依赖相同。\n\n'
  t+=table(['原记录/时间','版本定位','原适用范围','本轮状态'],[(link_source(v['path'])+'；'+str(v['observedRecordDate']),v['version'],v['scope'],'未复跑；未代签业务；'+v['hashReference']) for v in pb['validationEvidence']]);f.write_text(t)
 assignment=[m for m in mods if m.get('assignmentReview')]
 if assignment:
  f=D/'P1B_Readiness.md';t=f.read_text()+'\n## 原三组归属核实\n\n'+table(['范围','当前主包/候选','证据','影响/状态'],[(m['id']+' '+m['name'],m['businessPackage']+'；候选：'+'、'.join(m['assignmentReview']['candidates']),m['assignmentReview']['basis'],m['assignmentReview']['impact']+'；'+m['assignmentReview']['status']) for m in assignment]);f.write_text(t)

if b.get('currentRun'):
  f=D/'P1_Review.md';t=f.read_text();current=b['currentRun'];t=t.replace('P1A/P1B为本轮新增规划细分。当前材料覆盖范围不是完成声明。','P1A/P1B为用户新增规划细分。当前材料覆盖范围不是完成声明。\n\n当前接续分支：'+current['branch']+'；开始HEAD：'+current['startHead']+'。本次接续原站观察/授权合成测试及业务包规格；实际数据操作见本报告同源记录，未修改产品代码、部署或访问者。下方历史接手/部署段保留原适用时间，不算本轮复验。');f.write_text(t)

# Proposed source-site data validation is another view of the existing scope.
# It is never counted as executed evidence or approved product requirements.
if b.get('dataValidation'):
 v=b['dataValidation']
 section='\n## 原站关联数据验证准备（用户2026-09-09新增要求）\n\n'
 section+=v['authorizationBoundary']+'\n\n目标：'+v['target']+'。状态：'+v['status']+'。'+v['environment']+'。\n\n'
 section+='平台访问：'+v['platformAccess']+'\n\n数据约定候选：'+v['dataPolicy']+'\n\n尚缺信息：'+v['unresolved']+'\n\n'
 if v.get('markerCompatibility'):section+='测试标记兼容：'+v['markerCompatibility']+'\n\n'
 section+=table(['数据集','拟建对象/数量上限','候选值','前置关系','具体边界'],[(x['id'],x['objects'],x['values'],x['dependency'],x['limit']) for x in v['datasets']])
 section+='\n'+table(['场景/范围','关联数据/证据','跨页面步骤','需要观察的事实','影响/恢复边界','实际执行状态'],[(x['id']+' '+','.join(x['moduleIds']),','.join(x['datasets'])+'；'+','.join(x['evidenceRefs']),x['chain'],x['verify'],x['effects']+'；'+x['recovery'],x['status']+'；'+x.get('currentApplicability','按当前范围核实')) for x in v['scenarios']])
 section+='\n### 合成测试对象及实际操作\n\n'
 section+=table(['对象ID','模块/类型','标记/关联','当前状态','证据/保留原因'],[(x['objectId'],x['moduleId']+' / '+x['objectType'],x['marker']+'；'+x['relations'],x['status'],x['evidence']+'；'+x['retention']) for x in v.get('records',[])])
 section+='\n'+table(['操作/时间','对象/关联','前置及动作','实际结果','证据/后续'],[(x['id']+'；'+x['at'],x['objectRefs'],x['before']+' → '+x['action'],x['after'],x['evidence']+'；'+x['next']) for x in v.get('operations',[])])
 section+='\n遗留数据：'+('；'.join(v.get('residuals',[])) or '尚无已确认创建的测试记录；不以入口点击声称保存成功')+'。\n'
 section+='\n'+v['recording']+'\n\n'+v['continuation']+'\n\n'+v['laterPackages']+'\n\n**场景设计不增加原59项验收任务。仅下述实际操作结果可以提供F级证据，拟建数据或原站说明不能代替执行结果。**\n'
 for name in ['P1_Review.md','P1B_BP_F_Specification.md']:
  f=D/name;t=f.read_text().replace('原站合成权限持续有效、','新增原站数据验证边界见下文、')
  f.write_text(t+section)
 note='\n## 当前原站数据验证边界\n\n'+v['authorizationBoundary']+' 完整数据集与场景见[P1评审材料](P1_Review.md)；范围澄清见[P1B就绪与待决记录](P1B_Readiness.md)。\n'
 for name in ['P1A_Coverage.md','P1B_PRD.md','P1B_Readiness.md']:
  f=D/name;f.write_text(f.read_text()+note)

# Current scope, dependency and acceptance applicability are authoritative views,
# not a second register. No counts are inferred from documents or source tests.
scope_intro='## 当前交付范围变更及统计口径\n\n'+ds['changeId']+'；'+ds['authorizedAt']+'。'+ds['authorization']+'\n\n'+current_scope_table()+'\n'+progress_text()+'\n\n'
foundation='## 保留的非模块基础能力（不重复计入15模块）\n\n'+table(['能力/原映射','当前最小范围','验收预期（未代签）','证据/原任务','状态'],[(x['id']+' '+x['name']+' / '+','.join(x['originalMappings']),x['scope'],x['acceptance'],x['evidence'],x['status']) for x in ds['baseCapabilities']])
foundation_detail='## 基础能力字段、异常与验收细化\n\n同源Scope_Register.deliveryScope.baseCapabilities；不新建模块或验收分母。全部候选待评审，历史测试按原版本保留，本轮未执行生产恢复、外部交易或多角色业务测试。\n\n'
for cap in ds['baseCapabilities']:
 if not cap.get('fieldDetails'):continue
 foundation_detail+='### '+cap['id']+' '+cap['name']+'\n\n'
 foundation_detail+=table(['对象/字段','定义','约束与限制','依据'],[(x['field'],x['definition'],x['constraints'],x['basis']) for x in cap['fieldDetails']])+'\n'
 if cap.get('interfaceReservations'):
  foundation_detail+=table(['预留服务','当前消费者','原模块/最小映射','成功及失败边界','限制'],[(x['service'],x['producers'],x['mapping'],x['completion'],x['limits']) for x in cap['interfaceReservations']])+'\n'
 foundation_detail+=table(['场景ID','给定','操作','预期/待定边界','依据与执行状态'],[(x['id'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in cap.get('acceptanceCases',[])])+'\n'
 foundation_detail+='静态/历史证据：'+'；'.join(link_source(x) for x in cap.get('codeRefs',[]))+'。\n\n'
dependencies='## 保留模块对暂缓模块的依赖与替代\n\n以下不代表暂缓完整模块恢复；未核实依赖不强行分类为重复功能。只有必须完整独立模块且会改变业务门槛的问题集中决定。\n\n'+table(['依赖/消费者','原提供模块','关系','当前最小边界','替代及影响','状态/证据'],[(x['id']+' / '+','.join(x['consumerModuleIds']),x['deferredProviderIds'],x['relation'],x['boundary'],x['alternative'],x['status']+'；'+x['evidence']) for x in ds['dependencies']])
acceptance='## 原59项验收的当前适用映射（原义与标志保持）\n\n保留/部分适用/本次暂缓按每项语义判定，不仅按原moduleId删分母。历史任务原文不改：历史只读措辞只描述原观察时点，新合成授权单独登记。任务可能跨模块或基础能力关联，不能把同一条算成多个已通过任务。无原独立任务的模块由当前规格补验收预期，但不捏造历史签署。\n\n'+table(['原任务/原模块','适用结论','当前模块/基础','原criteria ID','适用部分与限制'],[(x['taskId']+' / '+x['originalModuleId'],x['status'],x['currentModuleIds']+x['baseCapabilityIds'],x['criteriaIds'],x['note']) for x in ds['acceptanceApplicability']])
for name in ['P1B_PRD.md','P1_Review.md']:
 f=D/name;f.write_text(f.read_text()+'\n'+scope_intro+'\n'+foundation+'\n'+foundation_detail+'\n'+dependencies)
f=D/'P1B_Readiness.md';f.write_text(f.read_text()+'\n'+scope_intro+'\n'+progress_table()+'\n'+acceptance)
f=R/'docs/HRIS_Project_Plan.md';t=f.read_text();t=t.replace('<!-- ROADMAP_CURRENT_END -->',foundation+'\n'+dependencies+'\n<!-- ROADMAP_CURRENT_END -->');f.write_text(t)

f=D/'P1B_Readiness.md';f.write_text(f.read_text()+'\n## 当前模块与原验收任务的可追溯关系\n\n'+table(['当前模块','原任务关联及性质'],[(m['id']+' '+m['name'],['{}：{}'.format(x['taskId'],x['relation']) for x in assessment(m)['acceptanceRefs']]) for m in active_mods]))
