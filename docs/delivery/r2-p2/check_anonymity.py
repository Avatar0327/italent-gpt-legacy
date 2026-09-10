"""Independent rational matrix calculation for P2 tables only."""
import hashlib
import json
from fractions import Fraction as Q
from collections import defaultdict
from pathlib import Path
D=Path(__file__).resolve().parent;cases=json.loads((D/'Anonymity_Cases.json').read_text())['cases'];results=[]
def groups(rows,key):
 g=defaultdict(set)
 for r in rows:
  vector=tuple(Q(v) for v in r['coefficients'])
  if any(vector):g[vector].add(r[key])
 return [{'signature':[str(x) for x in v],'members':sorted(m),'size':len(m)} for v,m in g.items()]
for c in cases:
 g=groups(c['rows'],'reviewer');sizes=sorted(x['size'] for x in g);assert sizes==c['expectedClassSizes'],c['id']
 values=[str(sum(Q(r['value'])*Q(r['coefficients'][i]) for r in c['rows'])) for i in range(len(c['rows'][0]['coefficients']))];assert values==c['expectedValues'],(c['id'],values)
 safe=all(x>=c['k'] for x in sizes)
 if c.get('namedMode'):safe=c['namedMode']=='unique_manager' and c['noticeNamed'] and c['uniqueManager']
 sg=groups(c.get('subjectRows',[]),'subject')
 if c.get('organization'):
  assert sorted(x['size'] for x in sg)==c['expectedSubjectClassSizes']
  safe=safe and all(x['size']>=3 for x in sg) and all(n>=c['k'] for n in c['bottomAnonymousCounts'])
 safe=safe and c.get('partitionValid',True)
 actual='publish' if safe else 'suppress';assert actual==c['expected'],c['id']
 results.append(dict(id=c['id'],classes=g,subjectClasses=sg,columnValues=values,actual=actual,expected=c['expected'],pass_=True))
out=dict(kind='P2_independent_symbolic_calculation_not_P3',count=len(results),publish=sum(r['actual']=='publish' for r in results),suppress=sum(r['actual']=='suppress' for r in results),results=results)
out['inputSha256']={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['Anonymity_Cases.json']}
(D/'evidence/repair-002-anonymity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in out.items() if k!='results'})
