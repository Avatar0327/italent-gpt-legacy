"""Render documentation views from the existing Scope_Register.json. No app/data writes."""
import json,re,subprocess
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
def ct_gap(c):
 approval=c.get('requirementApproval')
 records=[approval['record']] if approval else [m['p1']['moduleClosure']['closureRecord'] for m in mods if m['id'] in c['currentApplicability']['moduleIds'] and m['p1'].get('moduleClosure',{}).get('closureRecord')]
 if not records:return c['gap']
 return '当前适用批准：'+'、'.join(dict.fromkeys(records))+'。对应模块所批规则不再待批；原站未知、实现差异和后续补验仍保留，不扩大到其他模块。以下为历史差异原文，其中待批措辞不代表当前硬阻塞：'+c['gap']
def progress_counts():
 def counts(field,full,limited):
  f=sum(assessment(m)[field]==full and not assessment(m)['approvedRestricted'] for m in active_mods)
  r=sum(assessment(m)[field] in limited and assessment(m)['approvedRestricted'] for m in active_mods)
  return {'full':f,'restricted':r,'total':f+r}
 return {'p1A':counts('p1A','complete',['restricted_complete']), 'p1B':counts('p1B','ready',['ready']), 'review':counts('review','signed',['restricted_signed'])}
def progress_text():
 p=progress_counts()
 return '；'.join(label+' '+str(p[k]['total'])+'/15（完整'+str(p[k]['full'])+'，受限'+str(p[k]['restricted'])+'）' for k,label in [('p1A','P1A关闭'),('p1B','P1B需求就绪'),('review','P1评审关闭')])+'。受限不混入完整通过，均不代表P3测试/P4业务或生产验收。'

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
 (ds.get('deferredDisplayLabel','本次暂缓33模块'),'、'.join(m['id']+' '+m['name'] for m in deferred_mods),ds['deferredPolicy'])])
def progress_table():
 labels={'in_progress':'进行中（未达完整退出）','not_ready':'未就绪','not_signed':'待业务评审签署','complete':'完整完成','ready':'需求就绪','signed':'评审通过','not_assessed':'待判定','restricted_complete':'受限完成（仅P1）','restricted_signed':'受限评审通过（仅P1）'}
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
t+='## 原子单元收口追溯\n\n'+table(['页面/收口时间','源操作与对象记录','规格与实现对应','收口性质与下一步'],[(p['id']+'；'+p['traceability']['closedAt'],'、'.join(p['traceability']['operationIds'])+'；'+'；'.join(p['traceability']['recordIds']),'、'.join(p['traceability']['contractIds'])+'；实现表同ID：'+'、'.join(p['traceability']['implementationRequirementIds']),p['traceability']['kind']+'；'+p['traceability']['next']) for p in pages if p.get('traceability')])+'\n'
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
pmods=[m for m in mods if any(p['level'] in ['P','F'] and p['id'] in m['p1']['pageRefs'] for p in pages)]
fields=sum(len(p['fields']) for p in pages);navcount=sum(len(m['p1']['navigation']) for m in mods)
t=intro('P1原站盘点与需求基线｜评审材料')
t+='**当前范围状态：** '+progress_text()+'六类基础能力另列；模块关闭依据明确用户批准及退出条件；源证据缺口和后续验证另列，不代签业务运行验收。原48组/59项保持历史，33组暂缓不作为当前P1阻塞。\n\n'+current_scope_table()+'\n'
t+='页面/字段/导航数量仅为历史索引规模，不用于进度。完整完成/就绪/评审通过由15模块退出证据分别判定；仅见菜单、空表或单条执行成功均不足。\n\n'+progress_table()+'\n'
t+='## 本轮目标、已有成果与缺口\n\n'+table(['交付物','接手时已有成果','本轮成果','边界与缺口'],[
('模块清单','Scope_Register已有48组，Markdown部分描述滞后','按原ID补导航、页面/字段/流程引用；更新同源视图','仅N级模块不视为典型页面盘点完成'),('页面目录','各域记录分散于观察和Source_Gaps','[页面目录](P1_Page_Catalog.md)','导航容器、同名应用、真实页面证据分层；未取正文明确保留'),('字段字典','列名、空表、部分必填/选项散落','[字段字典](P1_Field_Dictionary.md)','数据库类型、未知默认/必填/权限不推断'),('流程图','页面步骤及独立实现混有历史说明','[流程图与边界](P1_Flows.md)','D1–D7独立状态机；原站说明与F级执行分开；无依据不连线'),('差异清单','各域Source_Gaps及remaining已有','本报告下方48组差异视图＋现有各域文件','已确认设计/待核实/受限分列；原实现与历史测试保留')])
t+='\n## 历史接手与部署记录（下列本轮措辞属于上轮快照，非本次复验）\n\n'
t+='- 实际仓库：`/workspace/sites/italent-hris`；接手分支`main`；完整HEAD `72bcf4031fb4fc62d70be8a6c1ae1c491ff90714`；接手时工作区干净，仅一个检出工作树。\n- 未发现Git写锁或可读取的项目cwd运行进程；普通ps工具失败，有界/proc检查17项不可读，运行状态结论有此边界。无本轮新开发、测试、构建或发布任务。\n- 未完学习简介保留在`checkpoint/learning-description-20260908`，`f5f5b1bd9014d4b6eeb6d32da0f03e34da3bced2`；不合并、不重置。其他既有分支全部保留。\n- v112指定部署本轮只读复核`succeeded`；源码`fdc423fcba607bd5814a0672836b55536c71ecb1`；部署ID `appgdep_6aa010f1e1e481919f2a4331af5b0184`。本轮文档提交不改变在线版本。\n- F01–F04保留历史116项API、3项组件及后续5项入口渲染证据；重叠测试不相加为覆盖数，本轮未复跑。用户仅确认成员/员工可打开；按钮缺失反馈和修复后待复验继续保留。E2不增人，多角色UAT暂缓，均非继续P1前置。\n\n'
t+='## 原站证据与独立设计分类\n\n'+table(['类别','判定','例子'],[('原站事实','N导航或P页面字段/说明，并标明来源日期','BC-F04兼职表头；BC-L11审批开关说明'),('已确认独立设计','有用户明确决定，保留实现与测试','D1–D7；不能写成北森原站制度'),('其他独立实现','仓库代码/测试仅证明本项目技术行为','学分有效期、内部排期、冻结考勤引用等；不是自动获得企业签署'),('待核实','还未取得该页/规则证据，不能当故障或已通过','再入职、薪资组依赖、仅N级模块'),('受限项','存在具体访问/角色/外部动作限制证据','单角色、不可用页面、外部通知/真实交易未授权；合成保存权限已明确')])
t+='\n## 按既定顺序的领域缺口\n\n'+table(['业务包','证据与当前规格','未就绪条件与下一步'],[(p['name'], '、'.join(ref for m in active_mods if m['id'] in p['moduleIds'] for ref in m['p1']['pageRefs'])+'；'+link_source(p['spec']),p['readiness']+'；'+pack_pending(p)+'；'+p['next']) for p in s['p1B']['packages'] if pack_current(p)])

t+='\n## 48组差异清单（同一范围台账视图）\n\n'+table(['原范围ID/模块','当前适用','原站事实边界','本项目已有独立实现','待核实/未覆盖','受限与处理'],[(m['id']+' '+m['name'],scope_status(m['id']),m['p1']['sourceDepth']+'；'+('、'.join(m['p1']['pageRefs']) or 'BC-NAV-20260908'),m['developed'],m['remaining']+'；'+m['p1']['sourceGap'],'详见对应页面及P1-X例外；保留范围，不在本轮开发') for m in mods])
t+='\n## 例外、建议和影响\n\n'+table(['例外','性质/范围','证据','影响','建议'],[(x['id'],x['type']+'；'+x['scope'],x['evidence'],x['impact'],x['recommendation']) for x in b['exceptions']])
t+='\n## 集中评审范围\n\n此次评审对象是当前15模块及基础能力：保留原48组历史对应、当前适用证据分级、字段/流程/权限/验收、依赖与例外。33组独立规则不作当前退出门槛。**不请求重新决定D1–D7、不请求新增访问者、原站合成权限持续有效、不请求生产签署。**\n\n建议以此作为有例外的P1盘点基线。当前15模块的典型链及完整规则仍在同一台账待补；当前仍不满足现交付范围P1A/P1B退出条件；未探索、受限、待决策与待签署均须逐项保留，不得自动勾选通过。已获批准的P1受限范围按approvalRecords逐项应用，未批准模块不继承。\n\n'
t+='后续按roadmap.moduleExecutionOrder和executionPolicy逐模块闭环；M01→M19→M48→M32及后续R顺序不重排。已授权合成操作继续，当前独立业务决定集中，局部阻塞不停止其他模块；F01–F04人工UAT不是P1编写前置。\n\n'
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
 if '<!-- MODULE_MODE_CURRENT_END -->' in old:old=old.split('<!-- MODULE_MODE_CURRENT_END -->',1)[1].lstrip()
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
 t+=table(['需求','能力','当前适用','处置','代码/证据','差异与限制','验收关联'],[(x['requirement'],x['capability'],ct_scope(x),x['disposition'],x['evidence'],ct_gap(x),x['acceptance']) for x in pb['implementationMap']])
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
 t+='## 暂缓及退出\n\n当前暂停产品功能扩展；原站仅在最新授权内操作明确标记的合成测试记录；不导出真实数据，不新增访问者。15模块内原登记的自动调度、复杂审批、兼岗/再入职/法人等继续保留；独立AI与33模块按用户决定暂缓。外部服务仅必要接口契约/状态/失败处理，供应商开通与真实交易不是P1前置；生产切换不在本轮。P1A/P1B退出与后续阶段见[原项目规划](../HRIS_Project_Plan.md)。\n\n本PRD及分包规格按模块批准记录适用；已批准模块不再列为未签署，其他模块不继承批准。首包规则确认、首包需求就绪、首包业务验收、全项目P1完成与生产验收各自独立，不从数量推算整体进度。\n'
 (D/'P1B_PRD.md').write_text(t)
 # Update existing queue reading entry, preserving its historical content.
 qp=D/'Module_Queue.md';old=qp.read_text();marker='<!-- P1AB_QUEUE_END -->'
 if marker in old:old=old.split(marker,1)[1].lstrip()
 head='# 当前唯一执行队列：P1A/P1B\n\n源：Scope_Register.json.roadmap及Module_Queue.json。首要工作包：'+r['activeWorkPackage']+'。主要开发包：无（暂停扩展）。\n\n'+'\n'.join(f'{i+1}. {v}' for i,v in enumerate(r['nextTasks']))+'\n\n业务顺序：'+ ' → '.join(r['businessOrder'])+'；BP-UNASSIGNED仅保留归属核实历史；无成员时不计业务包。多角色人工UAT不阻断P1；转序不得静默跳过。下方历史队列不构成本轮执行指令。\n\n'+marker+'\n\n'
 qp.write_text(head+old)
 review=D/'P1_Review.md';old=review.read_text();old=old.replace('建议以此作为有例外的P1盘点基线。','本稿汇总P1A批准及待评审输入；每项例外按具体批准记录，不自动扩展。').replace('如要求“全量典型页均已核实”才结束P1，则本稿不满足该更高门槛','按本轮明确的P1A退出条件，本稿仍需补证和例外评审')
 review.write_text('# 当前评审状态：按模块批准记录分别判定，全项目尚未整体验收\n\nP1A/P1B为本轮新增规划细分。当前材料覆盖范围不是完成声明。\n\n- [当前15模块P1A覆盖及33组暂缓](P1A_Coverage.md)\n- [总体PRD](P1B_PRD.md)\n- [分包就绪及映射](P1B_Readiness.md)\n- [已有实现与需求对应](P1B_Implementation_Map.md)\n- [当前路标及阶段退出](../HRIS_Project_Plan.md)\n\n'+old)

# Detailed pack specifications remain views of the same authoritative register.
if 'p1B' in s:
 pb=s['p1B']; by_id={m['id']:m for m in mods}
 for pack in pb['packages']:
  if 'contracts' not in pack:continue
  t=intro(pack['id']+' '+pack['name']+'｜产品需求规格评审稿')
  t+='**状态：'+pack['specStatus']+'。'+pack['readiness']+'。** 不以文档生成代替需求签署；本项目既有实现事实与原站事实分别列出。\n\n'
  t+='## 目标、范围和暂缓\n\n'+pack['goal']+'\n\n'
  t+=table(['原范围ID','模块','当前适用','原登记范围','原验收归属'],[(i,by_id[i]['name'],scope_status(i),by_id[i]['scope'],'、'.join(a['id'] for a in s['acceptanceTasks'] if a['moduleId']==i) or '沿用原范围登记；未新造验收任务') for i in pack['moduleIds']])
  internal=[(i,x) for i in pack['moduleIds'] if i in active_ids for x in by_id[i]['p1'].get('internalScopeCoverage',[])]
  if internal:
   t+='\n原登记内部功能逐项映射（未探索不等于暂缓；不新增验收分母）：\n\n'+table(['模块/原登记功能','当前边界','对应规格','证据及深度','具体缺口'],[(i+' / '+x['originalScopeItem'],x['currentMode'],x['contractIds'],('、'.join(x['evidenceRefs']) or '无本项详细证据，原范围仍保留')+'；'+x['coverageDepth'],x['remaining']) for i,x in internal])
  t+='\n本轮暂停产品实现、部署和新增测试访问者；原站关联数据验证依最新已确认授权执行，实际结果以同源dataValidation.operations为准。15模块内待补项继续纳入当前需求；其余成员独立需求明确历史暂缓，不列当前就绪门槛。完整历史内容保留，不代表当前主动探索。输入：'+link_source(pack['inputEvidence'])+'。\n\n'
  if pack.get('authoritativeDetail'):t+='首要子包详细需求：'+link_source(pack['authoritativeDetail'])+'；D1–D7保持已确认，不以本文件重开决策。\n\n'
  t+='## 已具体化的对象与行为契约\n\n下列“验收预期”是对已确认规则或既有实现候选行为的可执行描述，**未表示已执行或已获企业批准**。D1–D7保持原签署；新增批准须见approvalRecords和契约requirementApproval，不自动形成R版本开发批准。\n\n'
  if not pack['moduleIds']:t+='当前无未归属范围；历史三组依据见[P1B就绪表](P1B_Readiness.md)。此文件不是新增业务包或需求完成声明。\n\n'
  if not pack['contracts'] and pack['moduleIds']:t+='本组职责和对象字段尚不足以形成行为契约，先保留逐模块证据和候选归属；不以空模板冒充需求完成。\n\n'
  for ct in pack['contracts']:
   t+='### '+ct['id']+' '+ct['object']+' — '+ct['currentApplicability']['status']+'\n\n**当前适用：'+ct_scope(ct)+'**\n\n性质：'+ct['classification']+'。下表保留原契约内容；混合/暂缓部分以当前适用边界为准，不作为当前完整模块前置。\n\n'
   t+=table(['维度','规格及当前边界'],[('对象/字段/校验',ct['fields']),('角色/数据范围/字段权限',ct['roles']),('状态/审批/生效',ct['lifecycle']),('页面主要操作',ct['actions']),('验收预期（给定条件→操作→结果）',ct['acceptance']),('例外、恢复与仍缺内容',ct_gap(ct)),('静态实现/输入依据','；'.join(link_source(x) for x in ct['codeRefs']))])+'\n'
   if ct.get('requirementApproval'):t+='当前需求批准：'+ct['requirementApproval']['record']+'；'+ct['requirementApproval']['scope']+'。下方历史静态/待证措辞保留当时含义；与已批准推荐冲突时以批准记录锁定的对应模块评审包为准，不把未知源规则改成已验证。\n\n'
   if ct.get('fieldDetails'):
    t+='字段与对象细化（来源逐项区分，不用代码补原站事实）：\n\n'+table(['字段/对象','定义及关联','校验/范围','来源与状态'],[(x['field'],x['definition'],x['constraints'],x['basis']) for x in ct['fieldDetails']])+'\n'
   if ct.get('roleMatrix'):
    t+='角色与字段权限边界：\n\n'+table(['角色/身份','可读范围','可执行动作','限制与来源'],[(x['role'],x['read'],x['write'],x['boundary']) for x in ct['roleMatrix']])+'\n'
   if ct.get('stateTransitions'):
    t+='状态转换（原站与本项目现有实现分开）：\n\n'+table(['起始状态','动作','结果状态','条件/异常','证据性质'],[(x['from'],x['event'],x['to'],x['guards'],x['basis']) for x in ct['stateTransitions']])+'\n'
   if ct.get('acceptanceCases'):
    t+='可执行验收场景细化：这些是原任务下的场景，不新增验收分母；需求批准与场景执行分别登记；历史测试不视为本轮复验。\n\n'+table(['场景ID','给定条件','操作','期望/待定边界','来源与执行状态'],[(x['id'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in ct['acceptanceCases']])+'\n'
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
 t+=table(['ID/事项','现状及证据','推荐（尚待批准）','备选','阻塞范围/状态'],[(x['id']+' '+x['topic'],x['basis'],x['proposal'],x.get('alternatives',[]),x['impact']+'；'+x['status']) for x in pb['reviewIssues'] if x.get('decisionRequired',True) and not x.get('decision')])
 resolved=[x for x in pb['reviewIssues'] if not x.get('decisionRequired',True) and x.get('decision')]
 if resolved:t+='\n## 已明确的执行范围（保留历史，不重复询问）\n\n'+table(['事项','结论/时间'],[(x['id']+' '+x['topic'],x.get('decision',x['status'])+'；'+x.get('decidedAt','')) for x in resolved])
 followups=[x for x in pb['reviewIssues'] if not x.get('decisionRequired',True) and not x.get('decision')]
 if followups:t+='\n## 先补证后评审的事项（未获批准，暂不要求即时选择）\n\n'+table(['事项','现状/证据','建议及备选（均未批准）','受影响范围/下一步'],[(x['id']+' '+x['topic'],x['basis'],x['proposal']+'；备选：'+esc(x.get('alternatives',[])),x['impact']+'；'+x['status']) for x in followups])
 t+='\n## 各包具体就绪缺口\n\n'+table(['业务包','仍需满足的条件'],[(p['id']+' '+p['name'],pack_conditions(p)) for p in pb['packages'] if p['moduleIds']])
 read.write_text(t)

 f=D/'P1B_Implementation_Map.md';t=f.read_text()+'\n## 分包契约与实现证据索引\n\n此索引由同一Scope的contracts生成。源码链接只证明静态对应；原站说明或范围文件不能证明已有实现。具体复用/补齐/修改边界按对应规格的差异列评审。\n\n'
 t+=table(['业务包/需求ID','对象与规格','当前适用','证据性质','代码或来源','具体差异/待核验'],[(p['id']+'/'+c['id'],c['object']+'；'+link_source(p['spec']),ct_scope(c),c['classification'],'；'.join(link_source(x) for x in c['codeRefs']),ct_gap(c)) for p in pb['packages'] for c in p.get('contracts',[])])
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
foundation_detail='## 基础能力字段、异常与验收细化\n\n同源Scope_Register.deliveryScope.baseCapabilities；不新建模块或验收分母。批准范围以每项r1RequirementApproval/其他版本评审为准，不能跨R继承；历史测试按原版本保留，本轮未执行生产恢复、外部交易或多角色业务测试。\n\n'
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

internal_scope='\n## 当前15模块原登记内部功能覆盖（同源逐项，未代签）\n\n原始modules[].scope短语原样保持。跨模块引用只作依赖线索，不能替代本模块页面/角色证据；仅用户明确独立AI子能力暂缓，外部服务按接口边界，其余未探索功能仍在当前承诺内。下表不是新增进度台账或验收分母。\n\n'
for m in active_mods:
 internal_scope+='### '+m['id']+' '+m['name']+'\n\n'+table(['原登记功能','当前边界','规格ID','证据/深度','仍缺内容/后续'],[(x['originalScopeItem'],x['currentMode'],x['contractIds'],('、'.join(x['evidenceRefs']) or '暂无本项详细证据')+'；'+x['coverageDepth'],x['remaining']+'；'+x['next']) for x in m['p1'].get('internalScopeCoverage',[])])+'\n'
for name in ['P1A_Coverage.md','P1_Review.md']:
 f=D/name;f.write_text((f.read_text()+internal_scope).rstrip()+'\n')

if pb.get('reviewPackage'):
 rp=pb['reviewPackage']
 summary='# 当前15模块P1集中评审与恢复点\n\n生成来源：同一Scope_Register.p1B.reviewPackage及modules[].p1；'+rp['assessedAt']+'。基于已推送源码/文档提交`'+rp['basedOnHead']+'`；本报告后续提交以实际Git HEAD为准。\n\n'
 summary+=rp['status']+'。\n\n**'+progress_text()+'**\n\n'
 summary+='## 已形成的成果及实际状态\n\n'+rp['sourceProgress']+'\n\n'+rp['requirementsProgress']+'\n\n'+rp['autonomousWork']+'\n\n'+rp['foundationConclusion']+'\n\n'
 summary+='## 剩余阻塞与最小恢复动作\n\n'+table(['类型/编号','受阻动作及证据','影响范围','恢复条件'],[(x['kind']+' / '+x['id'],x['action']+'；'+x['evidence'],x['affected'],x['restore']) for x in rp['blockers']])+'\n'
 decisions=[x for x in pb['reviewIssues'] if x.get('decisionRequired',True) and not x.get('decision')]
 summary+='## 集中决策与阶段结论\n\n需选择的事项：'+'；'.join(x['id']+' '+x['topic'] for x in decisions)+'。现状、推荐、备选及影响完整见[P1B就绪与待决记录](P1B_Readiness.md)。推荐不代表已批准。R-SPEC-02/S-SPEC-01先补证后评审，不要求即时选择；D1–D7/E1/E2不重问。\n\n'+rp['gateConclusion']+'\n\n'
 summary+='## 证据、规格及测试数据入口\n\n'+table(['材料','作用'],[('[P1A覆盖与内部功能](P1A_Coverage.md)','当前15逐项证据/深度/限制与33暂缓历史'),('[总体PRD](P1B_PRD.md)','业务包入口、全局契约、六基础及外部预留'),('[需求就绪与待决记录](P1B_Readiness.md)','必要选择、先补证事项、原59适用映射'),('[已有实现对应](P1B_Implementation_Map.md)','复用/待核验/补齐/修改及历史验证版本'),('[Scope_Register.json](Scope_Register.json)','p1Baseline.dataValidation.records/operations为合成数据当前状态和逐步操作唯一事实来源；residualHistory保留过时阶段描述'),('[恢复记录](Controller_Resume.md)','实际执行点、已确认结果及连接恢复后顺序')])+'\n下方保留完整同源证据、五类交付及历史适用说明；旧阶段文字不能覆盖上面的当前范围、状态或授权。\n\n---\n\n'
 f=D/'P1_Review.md';f.write_text(summary+f.read_text())

# Recovery headers are views of the same currentRun, not another live ledger.
cr=b['currentRun']
if cr.get('currentFocus'):
 header='# 当前执行恢复点：'+cr['currentFocus']+'\n\n'
 header+='事实来源：Scope_Register.json / p1Baseline.currentRun、modules[].p1、roadmap.executionPolicy。记录时间：'+cr['latestCheckpointAt']+'。\n\n'
 header+='本单元编辑基准 HEAD：`'+cr['latestCommittedHead']+'`，分支 `'+cr['branch']+'`。该值是编辑前的已存在提交，不冒充本文件最终所属提交。恢复时用 `git log -1 --format=%H` 核实际 HEAD，`git log -1 --format=%H -- docs/delivery/Scope_Register.json` 定位本记录所属提交，`git status --short` 核当前未提交状态；同步结果以同次 push / ls-remote 核验为准。\n\n'
 header+='恢复时工作区快照：'+cr['workingTreeAtResume']+' 本单元只修改文档和同源生成/一致性脚本；提交前的修改清单不作为提交后的未提交状态。\n\n'
 header+=progress_text()+' '+ds.get('deferredDisplayLabel','33个模块本次暂缓')+'；原48范围/59任务及历史证据保留，基础六类另列。P2受限技术验收、F01–F04已有实现及历史验证、D1–D7/E1/E2原义不变。\n\n'
 header+='上一原子单元停点：'+cr.get('previousAtomicOutcome','BC-C30已完成，后续成果以原记录保持。')+'\n\n'
 header+='浏览器：'+cr['sourceBrowsingStatus']+' '+cr.get('sourceWritePolicy','既有合成测试授权按当时范围保留，具体操作服从最新本轮边界。')+'\n\n'
 if cr.get('lastVerifiedSync'):
  sync=cr['lastVerifiedSync'];header+='最近已核实同步：`'+sync['commit']+'` → `'+sync['remoteBranch']+'`；'+sync['result']+'。范围：'+sync['scope']+'。\n\n'
 if cr.get('currentUnitOutcome'):header+='本单元接续成果：'+cr['currentUnitOutcome']+'\n\n'
 header+='下一步：'+cr['next']+'\n\n'
 header+='验证范围仅文档一致性、引用、同源生成及改动边界；历史测试不记本轮复验，业务和生产验收未提升。未改产品代码、部署或访问者，未开启代理。后续历史记录只保留发生时含义，不覆盖本段当前焦点。\n\n<!-- P1_RESUME_CURRENT_END -->\n\n'
 for f in [D/'Controller_Resume.md',R/'docs/Execution_Checkpoint.md']:
  previous=f.read_text();marker='<!-- P1_RESUME_CURRENT_END -->'
  if marker in previous:previous=previous.split(marker,1)[1].lstrip()
  f.write_text(header+previous)

# Module/R transition readiness is derived, never edited as an independent percentage.
policy=s['roadmap'].get('executionPolicy')
if policy:
 def approved_review(x):
  return bool(x.get('approved') is True and x.get('record') in {a['id'] for a in pb.get('approvalRecords',[]) if a.get('approved')} and x.get('scope') and x.get('approvedAt'))
 def phase_approved(x):
  return x.get('status') in ['完整通过','受限通过'] and x.get('approvalRecord') in {a['id'] for a in pb.get('approvalRecords',[]) if a.get('approved')}
 module_closures=[]
 for mid in s['roadmap']['moduleExecutionOrder']:
  m=by_id[mid];c=m['p1']['moduleClosure'];missing=[k for k in policy['transitionConditions'] if c['conditions'][k]['value'] is not True]
  if not phase_approved(c['p1AConclusion']):missing.append('p1AApproved')
  if not phase_approved(c['p1BConclusion']):missing.append('p1BApproved')
  if not approved_review(c['transitionReview']):missing.append('transitionReviewApproved')
  if any(x['status']=='受限通过' for x in [c['p1AConclusion'],c['p1BConclusion']]) and not all((c.get('restrictedApproval') or {}).get(k) for k in ['scope','residualRisk','revalidation','record']):missing.append('restrictedApprovalDetails')
  module_closures.append({'moduleId':mid,'name':m['name'],**c,'transitionReady':not missing,'missingConditions':missing})
 range_closures=[]
 for rg in s['roadmap']['rangeGates']:
  layer=next(x for x in ds['rangeLayers'] if x['id']==rg['id']);missing=[x['moduleId'] for x in module_closures if x['moduleId'] in layer['moduleIds'] and not x['transitionReady']]
  missing+= [k for k in rg['applicableFoundationIds'] if rg['foundationReadiness'][k]['value'] is not True]
  if not approved_review(rg['review']):missing.append('rangeReviewApproved')
  range_closures.append({**rg,'moduleIds':layer['moduleIds'],'transitionReady':not missing,'missingConditions':missing})
 derived={'source':'Scope_Register.json → roadmap.executionPolicy / modules[].p1.moduleClosure / roadmap.rangeGates','generatedFromUpdatedAt':b['updatedAt'],'primaryModuleId':policy['primaryModuleId'],'backupModuleId':policy['backupModuleId'],'activeExecutionModuleId':policy['activeExecutionModuleId'],'moduleCount':15,'completeCount':sum(x['p1AConclusion']['status']=='完整通过' and phase_approved(x['p1AConclusion']) for x in module_closures),'restrictedCount':sum(x['p1AConclusion']['status']=='受限通过' and phase_approved(x['p1AConclusion']) for x in module_closures),'transitionReadyCount':sum(x['transitionReady'] for x in module_closures),'progress':progress_counts(),'p1ClosedCount':sum(x.get('p1Closed') is True and phase_approved(x['p1AConclusion']) and phase_approved(x['p1BConclusion']) and all(v['value'] is True for v in x['conditions'].values()) and approved_review(x['transitionReview']) for x in module_closures),'modules':module_closures,'ranges':range_closures}
 derived['nightReviewPipeline']=policy.get('nightReviewPipeline')
 (D/'P1_Module_Closure.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n')
 block='## 当前执行模式：模块闭环优先、按R版本滚动转序\n\n'
 block+='本轮新批准执行节奏；不批准未决业务规则、内部延期或验收豁免。唯一主模块 '+policy['primaryModuleId']+'；备用 '+str(policy['backupModuleId'] or '未启用')+'；实际执行 '+policy['activeExecutionModuleId']+'。'+policy['backupActivation']+'。\n\n'
 if policy.get('nightReviewPipeline'):
  pipe=policy['nightReviewPipeline'];block+='本次R2材料流水线：'+pipe['rule']+'；材料完成待评审 '+ '、'.join(pipe['waitingModuleIds'])+'；正式关闭焦点 '+pipe['nextFormalClosureModule']+'。[集中评审与决定清单](P1_R2_Review_Package.md)。\n\n'
 block+=table(['R版本','模块顺序','当前边界'],[(x['id']+' '+x['name'],'→'.join(x['moduleIds']),x['status']+'；'+x['note']) for x in ds['rangeLayers']])+'\n'
 block+=policy['transitionRule']+'\n\n'+policy['rangeTransitionRule']+'\n\n'
 block+=table(['版本','P1转序条件','批准进入阶段','下游实际状态'],[(x['id'],'齐备' if x['transitionReady'] else '未齐备：'+','.join(x['missingConditions']),(x.get('downstream') or {}).get('authorizedPhase','未批准'),(x.get('downstream') or {}).get('p2Status','未取得该R下游批准')) for x in range_closures])+'\n'
 block+=table(['模块','R版本/队列','P1A判定','P1B评审','转序就绪','未达到条件'],[(x['moduleId']+' '+x['name'],x['rangeId']+' / '+x['queueState'],x['p1AConclusion']['status'],x['p1BConclusion']['status'],'是' if x['transitionReady'] else '否',x['missingConditions']) for x in module_closures])+'\n'
 block+='转序就绪 '+str(derived['transitionReadyCount'])+'/15；独立指标，不等业务验收或生产上线。风险证据规则：'+ '；'.join(policy['evidencePolicy'].values())+'。\n\n'
 (D/'P1_Module_Closure.md').write_text(intro('模块闭环、滚动转序及当前收口清单')+block)
 for m in active_mods:
  rows=m['p1'].get('closureChecklist',[])
  if not rows:continue
  section='\n## '+m['id']+'完整登记范围收口清单\n\n'+table(['问题/原范围','需求','证据','具体缺口','阻塞P1/风险','关闭方式与判据','当前状态'],[(x['id']+' / '+x['scopeItem'],x['requirementIds'],x['evidenceRefs'],x['gap'],str(x['blocksP1'])+'；'+x['risk'],x['closureMethod']+'；'+x['basis'],x['status']) for x in rows])+'\n'
  f=D/'P1_Module_Closure.md';f.write_text(f.read_text()+section)
 for name in ['P1A_Coverage.md','P1B_PRD.md','P1B_Readiness.md','P1_Review.md','Module_Queue.md']:
  f=D/name;f.write_text(block+'\n---\n\n'+f.read_text())
 # The existing roadmap header is regenerated earlier; prepend only the current mode once.
 f=R/'docs/HRIS_Project_Plan.md';old=f.read_text();marker='<!-- MODULE_MODE_CURRENT_END -->'
 f.write_text(block.replace('(P1_R2_Review_Package.md)', '(delivery/P1_R2_Review_Package.md)')+'\n'+marker+'\n\n'+old)
 for f in [D/'Controller_Resume.md',R/'docs/Execution_Checkpoint.md']:
  t=f.read_text();t=t.replace('<!-- P1_RESUME_CURRENT_END -->','当前执行约束：主模块 '+policy['primaryModuleId']+'；备用 '+str(policy['backupModuleId'] or '未启用')+'；实际执行 '+policy['activeExecutionModuleId']+'。'+policy['rangeTransitionRule']+'\n\n<!-- P1_RESUME_CURRENT_END -->');f.write_text(t)

# Concise decision packet; content is owned by M01 in the existing register.
m01=by_id['M01']['p1']
if m01.get('reviewPackage'):
 review=m01['reviewPackage'];issue_by_id={x['id']:x for x in pb['reviewIssues']}
 t=intro('M01完整范围集中评审包')
 t+='材料状态：**'+review['documentStatus']+'**；基于 `'+review['basedOnHead']+'` 静态核对，准备时间 '+review['preparedAt']+'。原站新增操作为0；本轮未业务复验。\n\n'
 t+='## 本次需要判断什么\n\nM01完整范围：'+review['scope']+'。'+review['internalDeferralNote']+' F01–F04优先但不代表整个M01。\n\n'+review['confirmedRules']+'\n\n'
 t+=table(['P1层次','本次结论与仍缺条件'],[(k,v) for k,v in review['exitAssessment'].items()])+'\n'
 t+='## 已收窄或关闭的问题\n\n'+table(['问题','实际结论','证据性质/来源'],[(x['problem'],x['resolution'],x['type']+'；'+'、'.join(x['evidenceRefs']+x.get('codeRefs',[]))) for x in review['closedQuestions']])+'\n'
 t+='## 六项完整范围与退出清单\n\n'+table(['原范围','需求/已有证据','未闭合条件','关闭方式'],[(x['scopeItem'],'、'.join(x['requirementIds'])+'；'+ '、'.join(x['evidenceRefs']),x['gap'],x['closureMethod']) for x in m01['closureChecklist']])+'\n'
 t+='## 集中决定记录\n\n'+('批准记录：'+review['approvalRecord']+'；批准时间：'+review['approvedAt']+'。下列推荐原文锁定于所审版本；原文未批准/待评审措辞是历史状态，现已明确批准为M01产品规则。原站事实仍按原始证据。' if review.get('approvalRecord') else '以下推荐尚待明确批准。')+'\n\n'
 for iid in review['decisionIds']:
  x=issue_by_id[iid];t+='### '+iid+' '+x['topic']+'\n\n'+table(['维度','内容'],[('证据/现状',x['basis']),('已批准推荐（原文）' if x.get('approvalRecord') else '推荐（未批准）',x['proposal']),('备选',x.get('alternatives',[])),('影响/阻塞',x['impact']+'；当前：'+x['status'])])+'\n'
 t+='## 原站受限与后续验证责任（批准状态逐项列明）\n\n'
 for x in review['exceptionProposals']:
  t+='### '+x['id']+' — '+x['status']+'\n\n'+table(['维度','内容'],[(k,x[k]) for k in ['scope','evidence','proposal','residualRisk','revalidation']+(['approvalConclusion'] if x.get('approvalConclusion') else [])])+'\n'
 t+='## 关键流程与验收预期\n\n'+'\n'.join('- '+x for x in review['flowSummary'])+'\n\n'
 t+=table(['场景/范围','给定','操作','预期','来源/状态'],[(x['id']+' '+x['scopeItem'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in review['acceptanceCases']])+'\n'
 t+='## 获准后P2需要处理的差异\n\n'+'\n'.join('- '+x for x in review['implementationNext'])+'\n\n'+review['signoffRequest']+'\n\n完整字段、角色矩阵、版本化验收和源差异见 [首包规格](F01_F04_Requirements_Baseline.md)、[BP-F规格](P1B_BP_F_Specification.md)、[已有实现对应](P1B_Implementation_Map.md)。本包是Scope派生阅读视图，不是第二套审批台账。\n'
 (D/'P1_M01_Review_Package.md').write_text(t)
 for name in ['P1B_BP_F_Specification.md','P1B_Readiness.md','P1_Review.md','P1_Module_Closure.md']:
  f=D/name;f.write_text('M01当前集中评审入口：[完整范围、规则与受限边界](P1_M01_Review_Package.md)。状态：'+review['documentStatus']+'；批准记录：'+str(review.get('approvalRecord') or '无')+'。\n\n'+f.read_text())
 # Keep the authoritative first-package document's latest pointer ahead of historic notes.
 f=D/'F01_F04_Requirements_Baseline.md';old=f.read_text();marker='<!-- M01_REVIEW_POINTER_END -->'
 if marker in old:old=old.split(marker,1)[1].lstrip()
 f.write_text('> 当前M01闭环口径：'+review['documentStatus']+'；当前主模块'+policy['primaryModuleId']+'。六项原范围不缩减；D1–D7保持。最新批准、规则与限制见[M01评审包](P1_M01_Review_Package.md)。下方旧待审/待证措辞保留历史，具体业务推荐以获批版本为准。\n\n'+marker+'\n\n'+old)

# Consumer documentation describes the existing authoritative fields, not extra state.
if policy:
 fields=[
 ('deliveryScope.rangeLayers / moduleExecutionOrder','R1–R4分区及确切顺序；保留原48组，R4的33组暂缓，不计为已完成'),
 ('roadmap.executionPolicy','唯一主模块、最多1备用、实际执行焦点、启用依据、返回条件和焦点历史'),
 ('roadmap.executionPolicy.nightReviewPipeline / p1B.r2ReviewBundle','本轮材料准备顺序、完成及等待队列、正式关闭顺序和同源集中决定索引；准备不等关闭或转序'),
 ('deliveryScope.baseCapabilities[].r2Assessment','R2基础适用差异及用例引用；不自动继承R1批准'),
 ('p1Baseline.dataValidation.readOnlyRechecks','旧未知结果的只读后续证据、精确前后快照及剩余未知；不改原operations历史'),
 ('modules[].p1.closureChecklist','完整原登记范围逐项：需求、证据、缺口、阻塞性、关闭方式、判据；不是另一个任务分母'),
 ('modules[].p1.reviewPackage','模块集中阅读包的唯一原始内容；材料已完成待评审不等签署'),
 ('p1B.reviewIssues','业务建议、备选及影响唯一待决记录；decision为空不能展示已批准'),
 ('p1B.approvalRecords','用户明确批准的版本、文档哈希、推荐原文及哈希、范围、例外与排除项；批准不外推到其他模块'),
 ('modules[].p1.moduleClosure.p1AConclusion / p1BConclusion','分别显示五类结论；通过须approvalRecord，受限须scope/residualRisk/revalidation/record'),
 ('modules[].p1.moduleClosure.conditions','四个转序条件的value及basis；null=待判定，false=未满足，不能改为通过'),
 ('modules[].p1.moduleClosure.transitionReview','转序批准必须approved=true、record、scope、approvedAt齐备；不等生产上线批准'),
 ('roadmap.rangeGates','该R的适用基础能力及版本评审；满足后无需等待后续R全部P1完成'),
 ('roadmap.rangeGates[].downstream / p2Handoff','指定下阶段授权与P2/P3实际结论分开；R1本次仅P2设计，交接按批准记录和需求引用生成'),
 ('deliveryScope.baseCapabilities[].r1Assessment / r1RequirementApproval / recoveryTargets','六基础R1适用批准及恢复目标；不加模块分母，不将目标当云端能力实证'),
 ('modules[].p1.currentDeliveryAssessment','15模块P1A完成/P1B就绪/评审通过的既有计数口径，历史tested等字段不能替代'),
 ('p1Baseline.currentRun','恢复点、编辑基准HEAD、浏览器阻塞、最近已核实同步及下一步；实际HEAD/工作区须采集Git'),
 ('p1Baseline.dataValidation.records / operations','合成对象、关联、每次动作及结果；未知状态不能转成成功或重复提交')]
 t=intro('模块闭环字段与看板读取约定')
 t+='本轮仅事实源和文档生成调整；不改独立看板界面、不发布。独立看板消费这些同源字段，不能写回另一套状态。\n\n'
 t+=table(['事实源路径（Scope_Register.json）','读取含义'],fields)+'\n'
 t+='## 派生文件与转序计算\n\n[P1_Module_Closure.json](P1_Module_Closure.json)由scripts/render-p1-baseline.py生成。primaryModuleId/backupModuleId/activeExecutionModuleId直接取执行策略；modules[].transitionReady须四条件、两阶段批准及转序批准均满足；ranges[].transitionReady另要求本R全部模块、适用基础能力及范围评审。missingConditions给出尚缺条件。禁止手改派生布尔值。\n\ncompleteCount和restrictedCount分别是P1A完整通过、受限通过计数；progress.p1A/p1B/review各含full、restricted、total，明确分类后可显示合计；p1ClosedCount为模块P1关闭总数；transitionReadyCount独立统计。15模块分母保持，基础六类另列。结论枚举为：'+ '、'.join(policy['statusVocabulary'])+'。\n\n'
 t+='## 快照和历史证据\n\n看板快照应同时读取同一次主仓库Git HEAD、git status --porcelain及来源文件；如有未提交变更须显著标注，不能称为该HEAD已提交内容。generatedFromUpdatedAt是事实台账更新时间，不是看板采集时间；快照时间由采集方记录。部署适用版本读取实际部署证据，不从当前HEAD推断。历史技术测试保留原提交/版本，不能自动继承为本轮复验、P1通过或业务/生产验收。\n\n生成与检查命令：`python scripts/render-p1-baseline.py`，随后`python scripts/check-p1-baseline.py`。看板构建/发布失败不改变主仓库执行队列，也不阻塞其开发/部署链。\n'
 (D/'P1_Module_Closure_Fields.md').write_text(t)

if pb.get('approvalRecords'):
 t=intro('P1模块需求批准记录（非业务运行验收）')
 for ar in pb['approvalRecords']:
  t+='## '+ar['id']+'\n\n'+table(['字段','记录'],[(k,ar[k]) for k in ['approvedBy','approvedAt','timeBasis','source','reviewedHead','reviewedDocument','reviewedDocumentSha256','scope','authorization','exclusions']+(['approvedBoundaries'] if ar.get('approvedBoundaries') else [])])+'\n'
  if ar['approvedRecommendations']:t+=table(['规则','所审推荐SHA256','采用内容'],[(k,v['sha256'],v['text']) for k,v in ar['approvedRecommendations'].items()])+'\n'
 (D/'P1_Approval_Records.md').write_text(t.rstrip()+'\n')

# Other current module packets consume contract cases by reference, not copied state.
all_cases={x['id']:x for pack in pb['packages'] for ct in pack.get('contracts',[]) for x in ct.get('acceptanceCases',[])}
issue_by_id={x['id']:x for x in pb['reviewIssues']}
for m in active_mods:
 if m['id']=='M01' or not m['p1'].get('reviewPackage'):continue
 mid=m['id'];rp=m['p1']['reviewPackage'];p1=m['p1']
 t=intro(mid+' '+m['name']+'集中评审包')
 t+='状态：**'+rp['documentStatus']+'**；主模块 '+policy['primaryModuleId']+'，备用 '+str(policy['backupModuleId'] or '无')+'。\n\n准备时间 '+rp['preparedAt']+'；静态代码基准 `'+rp['basedOnHead']+'`。本轮原站未新增业务写入，历史测试未复验。\n\n'
 t+='## 完整范围与既有决定\n\n'+rp['scope']+'。'+rp['internalDeferralNote']+'\n\n'+rp['confirmedRules']+'\n\n'
 t+=table(['层次','退出条件/当前结论'],rp['exitAssessment'].items())+'\n'
 t+='## 已完成的证据与差异核对\n\n'+table(['问题','实际结论','证据性质'],[(x['problem'],x['resolution'],x['basis']) for x in rp['closedQuestions']])+'\n'
 t+='## 完整收口清单\n\n'+table(['原范围/问题','规格/证据','剩余硬条件','关闭方法'],[(x['scopeItem']+' / '+x['id'],x['requirementIds']+x['evidenceRefs'],x['gap'],x['closureMethod']) for x in p1['closureChecklist']])+'\n'
 if p1.get('consumerContracts'):
  t+='## 跨模块消费契约（批准见本包记录，不代批生产者规则）\n\n'+table(['原范围','生产者','明确消费字段','边界','证据'],[(x['scopeItem'],x['producer'],x['fields'],x['boundary'],x['evidence']) for x in p1['consumerContracts']])+'\n'
 if p1.get('datasetContracts'):
  t+='## 当前实现的数据集口径（静态证据，候选基线）\n\n下列事实不等于原站规则或本轮执行验证。指标采用及时间策略须按本包推荐评审，尚无实现的数据集仍按生产者契约保留。\n\n'+table(['数据集/原范围','生产者','一行代表什么','当前计算语义','时间/采用边界','代码来源'],[(x['datasetId']+' / '+x['scopeItem'],x['producerModuleIds'],x['rowGrain'],x['currentSemantics'],x['timeMode']+'；'+x['requirementDecision'],x['sourceHead']+'；'+'；'.join(link_source(r) for r in x['codeRefs'])) for x in p1['datasetContracts']])+'\n'
 t+='## 集中决定与版本依据\n\n'+('批准记录：'+rp['approvalRecord']+'；批准时间：'+rp['approvedAt']+'。下方推荐原文含待批措辞时只属审阅前状态，现已按该批准范围生效；原站未知不改写。' if rp.get('approvalRecord') else '下列推荐未批准，不外推其他模块已有签署。')+'\n\n'
 for iid in rp['decisionIds']:
  x=issue_by_id[iid];t+='### '+iid+' '+x['topic']+'\n\n'+table(['维度','内容'],[('现状/证据',x['basis']),('已批准推荐（所审原文）' if x.get('approvalRecord') else '推荐，未批准',x['proposal']),('备选',x['alternatives']),('影响',x['impact'])])+'\n'
 t+='## 原站限制及补验责任（按逐项批准状态）\n\n'
 for x in rp['exceptionProposals']:t+='### '+x['id']+'\n\n'+table(['维度','内容'],[(k,x[k]) for k in ['status','scope','evidence','proposal','residualRisk','revalidation']+(['approvalConclusion'] if x.get('approvalConclusion') else [])])+'\n'
 t+='## 关键流程与可执行验收预期\n\n'+'\n'.join('- '+x for x in rp['flowSummary'])+'\n\n'
 t+=table(['用例/范围','给定','动作','预期','来源及状态'],[(x['id']+' / '+x['scopeItem'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in [all_cases[i] for i in rp['acceptanceCaseRefs']]])+'\n'
 t+='## 进入P2后的复用与差异\n\n'+'\n'.join('- '+x for x in rp['implementationNext'])+'\n\n下一步：'+rp['next']+'\n\n[完整分包规格](P1B_'+m['businessPackage'].replace('-','_')+'_Specification.md) · [唯一待决与就绪表](P1B_Readiness.md) · [实现对应](P1B_Implementation_Map.md)。本包由Scope生成，不另维护进度。\n'
 if p1.get('reviewSupplement'):
  rs=p1['reviewSupplement'];t+='\n## 本轮覆盖与依赖\n\n'+rs['sourceTimes']+'\n\n'+table(['原范围','已覆盖/部分/未覆盖/受限'],rs['coverage'].items())+'\n'
  t+='\n'.join('- '+x for x in rs['dependencyContracts'])+'\n\n原站本单元：'+p1['sourceAccessThisUnit']['result']+'\n\n最小定向补证：\n\n'+'\n'.join('- '+x for x in rs['targetedEvidence'])+'\n'
 (D/('P1_'+mid+'_Review_Package.md')).write_text(t)
 for name in ['P1B_Readiness.md','P1_Review.md','P1_Module_Closure.md']:
  f=D/name;f.write_text(f.read_text()+'\n'+mid+'当前材料：['+rp['documentStatus']+'](P1_'+mid+'_Review_Package.md)。批准、源取证及后续执行各自独立。\n')

# Foundation applicability is a Scope view; it is not a parallel approval ledger.
for rg in s['roadmap']['rangeGates']:
 if not rg.get('foundationReviewPackage'):continue
 rp=rg['foundationReviewPackage'];rid=rg['id']
 t=intro(rid+'适用基础能力集中评审')
 t+='状态：**'+rp['status']+'**；准备时间 '+rp['preparedAt']+'；静态基准 `'+rp['basedOnHead']+'`。\n\n'+rp['scope']+'\n\n'
 t+='各模块及基础批准仅按原记录范围采用。基础就绪依赖其自身适用批准；原始运行验收不提升。'+('批准记录：'+rp['approvalRecord']+'。下方推荐保留所审措辞，当前已按该记录范围获批。' if rp.get('approvalRecord') else '下方推荐未批准。')+'\n\n'
 for cap in ds['baseCapabilities']:
  a=cap.get('r1Assessment')
  if not a or rid!='R1':continue
  t+='## '+cap['id']+' '+cap['name']+'\n\n'+table(['维度','内容'],[('消费者/原映射',a['consumers']+' / '+','.join(cap['originalMappings'])),('此前模块批准范围',a['approvedScope']),('此前模块批准来源',a['approvedRuleRefs']),('已批准推荐（所审原文）' if a.get('approvalRecord') else '具体推荐，未批准',a['proposal']),('当前适用批准',a.get('approvalRecord')),('审阅前剩余条件（批准见当前记录）',a['pending']),('代码/历史证据',cap['codeRefs'])])+'\n'
  t+=table(['场景','给定/动作','预期','状态'],[(x['id'],x['given']+'；'+x['when'],x['then'],x['status']+'；本轮未执行') for x in cap['acceptanceCases'] if x['id'] in a['acceptanceCaseRefs']])+'\n'
 t+='## 集中决定\n\n'
 for iid in rp['decisionIds']:
  x=issue_by_id[iid];t+='### '+iid+' '+x['topic']+'\n\n'+table(['维度','内容'],[('依据',x['basis']),('已批准推荐（所审原文）' if x.get('approvalRecord') else '推荐，未批准',x['proposal']),('备选',x['alternatives']),('影响',x['impact']),('当前批准',x.get('approvalRecord'))])+'\n'
 t+='## 转序条件\n\n'+rp['next']+' 当前版本批准：'+str(rg['review'].get('record') or '未批准')+'；获准阶段：'+str((rg.get('downstream') or {}).get('authorizedPhase','未批准'))+'。P2退出、P3测试和业务/生产验收必须独立记录。\n'
 filename='P1_'+rid+'_Foundation_Review.md';(D/filename).write_text(t)
 for name in ['P1_Review.md','P1B_Readiness.md','P1_M32_Review_Package.md']:
  f=D/name;f.write_text(f.read_text()+'\n['+rid+'六基础适用及集中决定]('+filename+')：'+rp['status']+'，不增加模块分母。\n')

# R-specific P2 handoff consumes approved packets, contracts and historical evidence.
for rg in s['roadmap']['rangeGates']:
 h=rg.get('p2Handoff')
 if not h:continue
 rid=rg['id'];hm=[by_id[mid] for mid in h['moduleIds']];hc=[x for x in ds['baseCapabilities'] if x['id'] in h['baseCapabilityIds']]
 armap={x['id']:x for x in pb['approvalRecords']};cts={x['id']:x for pack in pb['packages'] for x in pack['contracts']}
 handoff_name='P1_'+rid+'_P2_Handoff.md';prompt_name='P1_'+rid+'_P2_Start_Prompt.md'
 t=intro(rid+' P1关闭与P2设计交接')
 t+='交接状态：'+h['status']+'；准备时间 '+h['preparedAt']+'；编辑基准 `'+h['basedOnHead']+'`。本文件所属最终提交由 `git log -1 --format=%H -- docs/delivery/'+handoff_name+'` 查询；当前源码和未提交状态须启动时重新核实。\n\n'
 t+='**P1转序批准：'+h['entryDecision']+'；仅准P2设计。P2退出未批准、P3未开始，本窗口未修改产品或执行P3测试。**\n\n'
 t+='## 范围与批准版本\n\n'+table(['模块/基础','完整适用范围','批准记录','准确结论'],[(m['id']+' '+m['name'],m['scope'],m['p1']['moduleClosure']['closureRecord'],'P1受限通过；具体风险不豁免') for m in hm]+[(x['id']+' '+x['name'],x['scope'],x['r1RequirementApproval']['record'],'R1适用需求基线已批准，运行/生产未验收') for x in hc])+'\n'
 t+=table(['批准记录','审阅HEAD','所审材料/哈希','批准范围'],[(x['id'],x['reviewedHead'],x['reviewedDocument']+' / '+x['reviewedDocumentSha256'],x['scope']) for x in [armap[i] for i in h['approvalRecordIds']]])+'\n'
 t+='完整批准条款与哈希见[P1_Approval_Records.md](P1_Approval_Records.md)，原推荐不得重新解释扩大。\n\n不在本阶段范围内：\n\n'+'\n'.join('- '+x for x in h['exclusions'])+'\n\n'
 t+='## 受限结论与后续责任\n\n'+table(['模块','批准限制','残余风险','P2/P3/P4补验'],[(m['id'],m['p1']['moduleClosure']['restrictedApproval']['scope'],m['p1']['moduleClosure']['restrictedApproval']['residualRisk'],m['p1']['moduleClosure']['restrictedApproval']['revalidation']) for m in hm])+'\n'
 t+='六基础具体字段和故障用例见[P1_R1_Foundation_Review.md](P1_R1_Foundation_Review.md)。原站实测、静态代码与已批准产品设计仍分列；供应商未配置/单账号限制不被写成已完成联调。\n\n'
 t+='## P2必须解决的设计差异\n\n'+table(['任务/方面','批准约束与现状','必须交付','复用/核对代码'],[(x['id']+' '+x['area'],x['constraint'],x['deliverable'],'；'.join(link_source(p) for p in x['codeRefs'])) for x in h['designWorklist']])+'\n'
 t+='## 需求与现有实现追踪\n\n以下只取R1或基础的适用部分，混合契约中的其他模块未获本次开发授权。当前所审批准优先，静态事实不自动成为实现符合声明。\n\n'
 t+=table(['需求','对象/范围','当前适用','现有路径','必须核对差异'],[(x['id'],x['object'],ct_scope(x),'；'.join(link_source(p) for p in x['codeRefs']),ct_gap(x)) for x in [cts[i] for i in h['contractIds']]])+'\n'
 t+='## 可执行验收用例（需求获批，执行结果不预填）\n\n'
 seen=set()
 for m in hm:
  rp=m['p1']['reviewPackage'];cases=rp.get('acceptanceCases') or [all_cases[i] for i in rp['acceptanceCaseRefs']]
  cases=[x for x in cases if x['id'] not in seen];seen.update(x['id'] for x in cases)
  t+='### '+m['id']+'\n\n'+table(['ID','给定','操作','预期','依据/执行状态'],[(x['id'],x['given'],x['when'],x['then'],x['basis']+'；'+x['status']) for x in cases])+'\n'
 for cap in hc:
  t+='### '+cap['id']+'\n\n'+table(['ID','给定','操作','预期','执行状态'],[(x['id'],x['given'],x['when'],x['then'],x['status']) for x in cap['acceptanceCases']])+'\n'
 t+='## 历史技术与部署证据\n\n'+table(['证据','原日期/适用版本','验证范围','本轮复验'],[(link_source(x['path']),x['observedRecordDate']+' / '+x['version'],x['scope'],'否') for x in pb['validationEvidence'] if x['path'] in h['validationEvidencePaths']])+'\n'
 t+='其他历史入口：'+'；'.join(link_source(p) for p in h['historicalEvidenceRefs'])+'。P2_Acceptance原记录为2026-09-07受限底座/首链技术证据，不是当前R1设计通过；无完整测试SHA的记录明确保留未知。\n\n'
 dep=json.loads((D/'Deployment_Evidence.json').read_text());v=dep['verified']
 t+='已记录的适用私有部署：v'+str(v['version'])+'，源码 `'+v['commit']+'`，部署ID `'+v['deploymentId']+'`，原时间 '+v['time']+'，原终态 '+v['status']+'。本轮未重新发布或继承为业务/生产通过；当前Git HEAD不等于部署源码。\n\n'
 t+='## P2退出、协作与后续\n\n'+'\n'.join('- '+x for x in h['p2ExitConditions'])+'\n\n'+h['collaborationBoundary']+'\n\n不得重复询问：\n\n'+'\n'.join('- '+x for x in h['doNotReask'])+'\n\n'+h['next']+'\n\n可直接使用的完整启动提示词：['+prompt_name+']('+prompt_name+')。\n'
 (D/handoff_name).write_text(t)
 prompt='# '+rid+' P2设计窗口启动提示词\n\n以下整段可作为新执行窗口首条指令。授权来源为本窗口已批准的'+h['entryDecision']+'；不代表当前已启动新窗口。\n\n'
 prompt+='请接续现有iTalent项目，只承担R1 P2设计复核与交接，不重新开发。主仓库参考路径`/workspace/sites/italent-hris`。\n\n先只读核对实际分支、HEAD、工作区、未结束操作与最新Controller_Resume.md、Execution_Checkpoint.md；以当前Scope_Register.json为唯一事实源，读取`docs/delivery/'+handoff_name+'`、四模块评审包、基础评审、批准记录、PRD、实现对应与历史验证。已知交接编辑基准为`'+h['basedOnHead']+'`，如有后续进度接续最新，不回退或重做。\n\n'
 prompt+='已批准R1范围为M01组织员工、M19审批中心、M48员工自助、M32报表及BASE-01至06。四模块P1受限关闭和基础需求获批；R1获准进入P2设计，绝不代表P2/P3已通过。15模块及33暂缓、原48编号和59任务原义不变；R2/R3完整生产者实现不在本窗口，只保留已批准消费契约和未配置/不可用状态。\n\n'
 prompt+='本窗口只读现有产品代码/数据结构/测试并编写设计，不修改产品代码、业务数据库、原站数据或部署，不运行P3测试、不新增访问者、不启动代理。复用现有技术底座，完整设计架构、数据、权限、接口、迁移和异常，按交接R1-P2-01至09顺序保持一个主要设计任务；完成一个任务直接继续下一个。\n\n'
 prompt+='P1总控继续R2并唯一维护Scope与生成视图。先核对是否有正在写入的工作；在隔离工作树/设计分支保存P2文档，保留其他修改，不重置/强推/合并未完分支，不同时改主Scope。设计结论以有证据、版本及引用的提案交总控纳入，不建立第二套手工状态台账。可按完整设计单元提交和推送设计分支，保持引用主事实源；不向主分支并行写入状态。\n\n'
 prompt+='不重问已批准D1–D7、E1/E2、M01 F-SPEC-01至08/SCOPE-DEP-01/M01-BASELINE-01、M19/M48/M32的SPEC及LIMIT、R1六基础和恢复目标。D7调动仍独立两级，管理权不代审批权。RPO≤1小时、RTO≤4小时、保留30天及加密/可追溯/隔离验权后所有者开放均为批准目标；P2要核云端方案、成本、执行/复核责任和可信当前授权来源。无法经济实现时提交量化差异与成本备选，不能降低目标或声称当前平台已支持。\n\n'
 prompt+='采用已批准字段/权限/状态/验收基线，按实现版本逐项列可复用、待修改、待新增、受限及依赖。需要迁移的只写增量兼容/完整性/幂等/回滚与历史保护方案，不执行迁移，不继承旧空库结论。外部服务未配置不阻契约设计；报表不得以模拟联调代真实；当前权限覆盖历史/聚合/附件/链接，导出与订阅独立授权。\n\n'
 prompt+='历史测试只说明原记录版本；无完整SHA保持未知，不重写为本轮复验。P2先完成设计追踪和可执行验收计划；P3合成运行及P4多人权限/跨域/生产准备仍需独立验证。浏览器不可用只阻需要源补证的部分，不阻静态设计；不重复批准事项，不无限取证。新增实质业务规则/权限/范围或无法经济实现的目标才集中提交决定，先继续其他可执行工作。\n\n'
 prompt+='交付架构/数据/权限/接口/迁移/异常说明、逐需求实现差异与验收矩阵、恢复目标方案和成本/责任、残余风险与P3任务建议、可恢复检查点。对照交接的P2退出条件形成独立设计评审；未获P2退出评审批准，不能进入P3开发测试，更不能发布或宣称业务/生产验收。完成实质单元保存提交并继续，最终集中报告结论、版本、真实硬阻塞与待批准项。\n'
 (D/prompt_name).write_text(prompt)
 for name in ['P1_Review.md','P1_Module_Closure.md','P1B_Readiness.md']:
  f=D/name;f.write_text(f.read_text()+'\n['+rid+' P2完整交接]('+handoff_name+') · [新窗口启动提示词]('+prompt_name+')：只准P2设计，不等P2退出或P3通过。\n')

# R2 owner review is another read view of Scope, never a second status ledger.
rb=pb.get('r2ReviewBundle')
if rb:
 rms=[by_id[mid] for mid in rb['moduleIds']]
 issues={x['id']:x for x in pb['reviewIssues']}
 t=intro('R2集中评审总包')
 t+='状态：**'+rb['status']+'**。准备时间 '+rb['preparedAt']+'；编辑基准 `'+rb['basedOnHead']+'`。'+rb['scopeNote']+'\n\n'
 t+='本文件最终所属提交：`'+rb['syncEvidence']['finalCommitResolution']+'`。该提交与工作区须实际读取；编辑基准不是最终HEAD，文档不是本轮测试或业务签署。\n\n'
 t+=progress_text()+'\n\n主模块 '+policy['primaryModuleId']+'；备用 '+str(policy['backupModuleId'] or '无')+'；等待评审 '+'→'.join(rb['formalClosureOrder'])+'。R1获准P2设计的事实保持，R2尚未获准下游阶段。\n\n'
 t+='## 本轮已批准与关闭\n\n'+table(['模块','原完整范围','批准记录','P1A / P1B / 模块结论','转序'],[(mid+' '+by_id[mid]['name'],by_id[mid]['scope'],by_id[mid]['p1']['moduleClosure']['closureRecord'],'受限通过 / 受限通过 / P1受限关闭','模块转序就绪，不等R2版本已转序') for mid in rb['approvedModuleIds']])+'\n\nM37先关闭提交eabc9d2，M06后关闭提交3e0c0d5。批准的原文、所审版本和哈希见[P1_Approval_Records.md](P1_Approval_Records.md)，不重复征求批准。\n\n'
 t+='## 四模块材料与真实剩余条件\n\n'+table(['模块/完整范围','材料入口','当前结论','还缺什么'],[(m['id']+' '+m['scope'],'['+m['name']+'](P1_'+m['id']+'_Review_Package.md)',m['p1']['reviewPackage']['documentStatus'],'业务推荐及本模块LIMIT未批准；'+ '、'.join(m['p1']['reviewPackage']['decisionIds'])) for m in rms])+'\n'
 t+='各包已含逐范围覆盖、原站适用时间、静态实现版本、流程和差异、Given/When/Then用例；对象字段、角色矩阵、状态及消费者契约详见[BP-C规格](P1B_BP_C_Specification.md)。原站部分行为未执行、独立多角色未验；材料齐备不能据此代批。\n\n'
 t+='## 一次可决定的推荐清单\n\n共 '+str(len(rb['decisionIds']))+' 项，其中22项模块业务选择及1项完整基线/六基础R2适用确认；另有下方4项LIMIT。可逐项改选，未决定只阻塞对应范围。\n\n'
 t+=table(['ID','主题','影响','不决定的后果'],[(iid,issues[iid]['topic'],issues[iid]['impact'],issues[iid].get('ifUndecided','对应需求和适用基线保持待评审')) for iid in rb['decisionIds']])+'\n'
 for iid in rb['decisionIds']:
  x=issues[iid];t+='### '+iid+' '+x['topic']+'\n\n'+table(['维度','内容'],[('现状与证据',x['basis']),('推荐，尚未批准',x['proposal']),('备选',x['alternatives']),('影响',x['impact']),('不决定的后果',x.get('ifUndecided','对应基线保持待评审，不签关闭')),('当前状态',x['status'])])+'\n'
 t+='## 四项受限申请及责任\n\n接受限制只限P1需求，不能免除P2设计、P3实现验证或P4独立权限/业务/生产验收。\n\n'
 for m in rms:
  for x in m['p1']['reviewPackage']['exceptionProposals']:
   t+='### '+x['id']+' — 未批准\n\n'+table(['维度','内容'],[(k,x[k]) for k in ['scope','evidence','proposal','residualRisk','revalidation']])+'\n'
 t+='## 六项基础能力的R2适用差异\n\nR1已批准基线和恢复目标不重问；R2新增敏感对象、权限及消费者的适用差异由R2-BASELINE-01确认，不增加15模块分母。\n\n'
 t+=table(['能力','R2差异','当前状态','可执行用例引用'],[(c['id']+' '+c['name'],c['r2Assessment']['delta'],c['r2Assessment']['status'],c['r2Assessment']['acceptanceCaseRefs']+c['r2Assessment']['historicalBaseCaseRefs']) for c in ds['baseCapabilities']])+'\n'
 t+='## 全局一致性审查\n\n'+table(['维度','核对结论','约束/残余'],rb['consistencyFindings'])+'\n'
 t+='## 最小定向补证与恢复后的行动\n\n云浏览器已恢复部分只读访问，不再把CDP旧超时当成统一阻塞。以下执行链需相应测试写入或独立身份条件；本轮不写原站、不新增访问者。批准LIMIT后可按责任延后验证，不因此无限扩展P1。\n\n'
 for m in rms:
  rs=m['p1']['reviewSupplement'];t+='### '+m['id']+'\n\n'+rs['sourceTimes']+'\n\n'+m['p1']['sourceAccessThisUnit']['result']+'\n\n'+'\n'.join('- '+v for v in rs['targetedEvidence'])+'\n\n'
 t+='## 合成记录与操作遗留\n\n下表除明确只读回查外均为原记录的最后已知状态，不能当成本轮全量复验。没有新建、清理、启停或发送消息。业务UUID未知保持未知，操作结果不明先查后做。\n\n'
 t+=table(['模块/对象','标记','最后已知状态','关联/证据','留存'],[(r['moduleId']+' / '+r['objectId'],r['marker'],r['status'],r['relations']+'；'+r['evidence'],r['retention']) for r in b['dataValidation']['records'] if r['moduleId'] in rb['moduleIds']+rb['approvedModuleIds']])+'\n'
 for r in b['dataValidation'].get('readOnlyRechecks',[]):
  t+='只读补记 '+r['id']+'（'+r['recordedAt']+'）：'+r['method']+'。'+r['after']['status']+'。剩余：'+r['remaining']+'。旧operations记录不改写；证据见['+r['pageRef']+'后续回查](../P1_Source_Observations_20260907.md)。\n\n'
 t+='## 提交、同步与并行保护\n\n'+table(['提交','实质单元','远端核实'],[(x['sha'],x['subject'],'已逐单元核实一致' if x['remoteVerified'] else '待核实') for x in rb['commits']])+'\n'
 t+=table(['维度','证据'],rb['syncEvidence'].items())+'\n'+table(['并行保护','实际核对'],rb['parallelEvidence'].items())+'\n'
 t+='最终汇编提交在完成同源生成、引用/范围/文档检查后保存并推送；最终HEAD、远端及工作区以交付报告和实际Git为准。没有进入P2树；不能把注册HEAD检查扩张为对另一窗口全量工作的证明。\n\n'
 t+='## 下一恢复点\n\n'+rb['next']+'\n\n'+rb['stopBasis']+'\n\n可一次发送的[所有者批准草稿](P1_R2_Approval_Draft.md)仅供审阅复制，未发送、未批准。继续时先核对main实际HEAD/工作区及恢复文档，按M26→M18→M17→M03逐模块条件判定，不自动提升R2版本或业务/生产验收。\n'
 if rb.get('approved'):
  archived=subprocess.check_output(['git','show',rb['reviewedHead']+':docs/delivery/P1_R2_Review_Package.md'],cwd=R,text=True)
  t=intro('R2集中评审批准与顺序关闭记录')+'当前状态：'+rb['status']+'。所审版本 `'+rb['reviewedHead']+'`；SHA-256 `'+rb['reviewedDocumentSha256']+'`。所有者已明确批准全部推荐及四LIMIT，下游P2/P3未批准。\n\n'+progress_text()+'\n\n'
  t+=table(['模块','P1A','P1B','关闭记录'],[(m['id'],m['p1']['moduleClosure']['p1AConclusion']['status'],m['p1']['moduleClosure']['p1BConclusion']['status'],m['p1']['moduleClosure'].get('closureRecord')) for m in rms])+'\n当前焦点：'+policy['primaryModuleId']+'。\n\n以下完整保留所审版本原文，其中待批、6/15和旧焦点仅表示审阅时历史状态，不覆盖以上当前事实。\n\n---\n\n'+archived
 (D/'P1_R2_Review_Package.md').write_text(t)
 draft=intro('R2所有者集中批准草稿（未发送、未批准）')
 draft+='请先审阅[R2集中评审包](P1_R2_Review_Package.md)。以下文字供所有者明确采纳或修改；文件存在和生成检查通过不构成批准。采用时应引用实际审阅提交 `git log -1 --format=%H -- docs/delivery/P1_R2_Review_Package.md`，锁定推荐原文与哈希。\n\n---\n\n'
 draft+='我已审阅上述提交的R2集中评审包及所引用的M26、M18、M17、M03完整规格，批准该版本下列推荐作为产品需求基线：\n\n'
 for m in rms:draft+='- '+m['id']+'：'+'、'.join(m['p1']['reviewPackage']['decisionIds'])+'。\n'
 draft+='- R2-BASELINE-01：上述四模块完整范围内已具体化的字段、权限、状态、异常、契约和验收预期，以及六项基础能力的R2适用差异；保留R1恢复目标及其尚未实证的边界。\n\n'
 draft+='批准 '+'、'.join(rb['exceptionIds'])+' 所列P1受限边界、残余风险和P2/P3/P4补验责任。该批准仅关闭需求阶段，不代表功能已实现、测试通过、多角色业务验收或生产验收完成；不新增访问者，不豁免D1–D7。\n\n'
 draft+='请按M26→M18→M17→M03顺序写回唯一事实源并独立计算退出条件。符合条件的记录受限通过、模块转序就绪；不符合的仅列批准后真实硬阻塞。M37/M06及R1既有批准保持。不得凭此自动批准R2进入P2/P3、进入R3探索、扩大15模块范围、外发数据或执行生产交易。R2版本转序仍按适用基础和范围评审条件另行判定并报告。\n\n'
 draft+='若有以下改选，以我明确填写的ID和替代内容为准，其余不得自行扩大解释：〔所有者填写，或明确无改选〕。\n'
 if rb.get('approved'):draft='> 所有者已批准该草稿对应全部推荐，无改选；以下为历史草稿，不重复请求批准。当前逐模块登记见R2集中评审包。\n\n'+draft
 (D/'P1_R2_Approval_Draft.md').write_text(draft)
 for name in ['P1_Review.md','P1B_Readiness.md','P1_Module_Closure.md']:
  f=D/name;f.write_text(f.read_text()+'\nR2当前集中入口：[四模块完整材料、23项推荐及四项限制](P1_R2_Review_Package.md)；[批准草稿](P1_R2_Approval_Draft.md)。各模块按实际批准单独判定，计数从Scope推导。\n')
