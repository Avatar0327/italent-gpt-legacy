"""Author-specified rational tables with independent expected partitions."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
cases=[]
def row(k,coeff,value='3',subject='E1',atom=None):return dict(atomId=atom or k+'-q-v1',reviewer=k,subject=subject,coefficients=coeff,value=value)
def add(id,title,rows,sizes,expected,why,**extra):cases.append(dict(id=id,title=title,k=3,rows=rows,expectedClassSizes=sorted(sizes),expected=expected,manualReason=why,**extra))
add('ANON-01','三名首次合法发布',[row('A',['1/3'],'2'),row('B',['1/3'],'4'),row('C',['1/3'],'6')],[3],'publish','ABC同向量(1/3)，人数3；(2+4+6)/3=4。',expectedValues=['4'])
add('ANON-02','两名必须抑制',[row('A',['1/2'],'2'),row('B',['1/2'],'4')],[2],'suppress','AB同类但2<3；内部均值3不得披露。',expectedValues=['3'])
correct=[row('A',['1/3','0'],'2'),row('A',['0','1/3'],'5',atom='A-q-v2'),row('B',['1/3','1/3'],'4'),row('C',['1/3','1/3'],'6')]
add('ANON-03','同一人修改重新发布',correct,[1,1,2],'suppress','A旧(1/3,0)1人，A新(0,1/3)1人，BC(1/3,1/3)2人；新均值5减旧4=1，得A变化3。',expectedValues=['4','5'])
add('ANON-04','成员ABC改ABD',[row('A',['1/3','1/3'],'2'),row('B',['1/3','1/3'],'4'),row('C',['1/3','0'],'6'),row('D',['0','1/3'],'8')],[2,1,1],'suppress','AB交集2，C退出1，D新增1，三个类均不足。',expectedValues=['4','14/3'])
triple=[]
for group,bits,n in [('X','111',1),('AB','110',3),('AC','101',3),('BC','011',3),('A','100',3),('B','010',3),('C','001',3)]:
 for i in range(n):triple.append(row(group+str(i),['1/10' if b=='1' else '0' for b in bits]))
add('ANON-05A','交叠前两报告可发布',[dict(r,coefficients=r['coefficients'][:2]) for r in triple],[4,6,6],'publish','两个报告各10，交集X+AB=4，两差各6，全部≥3。',expectedValues=['3','3'])
add('ANON-05B','第三重交叠必须拒绝',triple,[1,3,3,3,3,3,3],'suppress','三报告各10，两两交集4差6，但111类只有X1；其余六类各3。',expectedValues=['3','3','3'])
weighted=[row(k,['1/6','1/9' if k in 'ABC' else '2/9']) for k in 'ABCDEF']
add('ANON-06A','可组合推断的安全三人子组',weighted,[3,3],'publish','两个向量分别ABC/DEF各3，可解两个三人均值仍满足阈值。',expectedValues=['3','3'])
add('ANON-06B','跨报告组合新增单人系数',[dict(r,coefficients=r['coefficients']+['1/11' if r['reviewer']=='A' else '2/11']) for r in weighted],[1,2,3],'suppress','第三报告区分A与BC，类A1/BC2/DEF3；不能以每份名义n=6放行。',expectedValues=['3','3','3'])
for id,n,counts,out,sizes in [('ANON-07A',3,[3,3,3],'publish',[3]),('ANON-07B',2,[3,3],'suppress',[2]),('ANON-07C',3,[3,3,2],'suppress',[3])]:
 rows=[row(f'E{s}R{i}',[f'1/{sum(counts)}'],subject=f'E{s}') for s,c in enumerate(counts) for i in range(c)]
 add(id,'组织人数与答卷双阈值',rows,[sum(counts)],out,'subject签名人数='+str(n)+'；底层各subject有效匿名卷数='+str(counts)+'；两个门禁都必须满足。',organization=True,subjectRows=[dict(subject=f'E{s}',coefficients=[f'1/{n}']) for s in range(n)],expectedSubjectClassSizes=sizes,bottomAnonymousCounts=counts,expectedValues=['3'])
add('ANON-08A','明确具名唯一上级可作为非self组',[row('L',['1'],'4')],[1],'publish','具名notice与唯一关系已冻结，无匿名数据，非self组成立；仍要独立受众。',namedMode='unique_manager',noticeNamed=True,uniqueManager=True,expectedValues=['4'])
add('ANON-08B','仅self不能正式发布',[row('E1',['1'],'4')],[1],'suppress','self具名不适用k，但无非self组，正式报告拒绝。',namedMode='self',noticeNamed=True,uniqueManager=False,expectedValues=['4'])
add('ANON-08C','匿名上级不得事后具名',[row('L',['1'],'4')],[1],'suppress','noticeNamed=false，不能使用唯一上级例外。',namedMode='unique_manager',noticeNamed=False,uniqueManager=True,expectedValues=['4'])
add('ANON-09','撤回旧报告不清除历史',correct,[1,1,2],'suppress','旧报告虽然withdrawn，矩阵旧列仍在；同ANON-03拒绝。',withdrawnColumns=[0],expectedValues=['4','5'])
add('ANON-10','固定分区映射失效',[row(k,['1/3']) for k in 'ABC'],[3],'suppress','数值分组满足但来源更改无法证明原partition映射，拒绝新披露；不得切epoch清账本。',partitionValid=False,expectedValues=['3'])
(D/'Anonymity_Cases.json').write_text(json.dumps(dict(kind='P2_symbolic_fixtures_not_P3',algorithm='coefficient-equivalence-with-answer-lineage-v2',cases=cases),ensure_ascii=False,indent=2)+'\n')
lines=['# M26 匿名逐格手算表','','下列是作者预期；check_anonymity.py从输入行独立计算，不导入分组实现或产品。所有算出的低样本值仅存在合成P2夹具，正式响应不得泄露。','','|例|手算分组与理由|预期|','|---|---|---|']
for c in cases:lines.append('|'+c['id']+'|'+c['manualReason']+'|'+c['expected']+'|')
for c in cases:
 lines+=['','## '+c['id']+' '+c['title'],'','|atom / 评委 / subject|值|各披露列系数（0表示不参与）|','|---|---:|---|']
 for r in c['rows']:lines.append('|'+r['atomId']+' / '+r['reviewer']+' / '+r['subject']+'|'+r['value']+'|'+', '.join(r['coefficients'])+'|')
 lines+=['','逐列手算值：'+', '.join(c['expectedValues'])+'；非零等价类distinct评委数：'+str(c['expectedClassSizes'])+'。历史列即使撤回也保留。']
(D/'Anonymity_Calculation.md').write_text('\n'.join(lines)+'\n')
