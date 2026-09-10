"""Render origin evidence only. Never execute product tests or change phase approvals."""
import json
from pathlib import Path
from collections import Counter

D = Path(__file__).resolve().parent

def read(name, default):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else default

def write(name, value):
    (D / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

run = read('run.json', {})
observations = read('Observations.json', [])
differences = read('Differences.json', [])
assert len({x['id'] for x in observations}) == len(observations)
assert len({x['id'] for x in differences}) == len(differences)
allowed = {'MATCH', 'REQUIREMENT_GAP', 'DESIGN_GAP', 'IMPLEMENTATION_DEFECT', 'INTENTIONAL_DIFFERENCE', 'ROLE_BLOCKED', 'ENV_BLOCKED', 'NEED_OWNER_DECISION'}
assert all(x['classification'] in allowed for x in observations + differences)

for row in observations:
    for ref in row.get('evidence', []):
        assert (D / ref).is_file(), f'Missing evidence: {ref}'
for row in differences:
    for ref in row.get('evidence', []):
        assert ref in {x['id'] for x in observations}, f'Missing observation: {ref}'

write('R2_Original_Behavior_Matrix.json', {'runId': run['runId'], 'observations': observations, 'notProductTests': True})
write('R2_Parity_Difference_Ledger.json', {'runId': run['runId'], 'differences': differences, 'counts': dict(Counter(x['classification'] for x in differences)), 'severityCounts': dict(Counter(x['severity'] for x in differences))})

def cell(v):
    return str(v).replace('|', '\\|').replace('\n', '<br>')

lines = ['# R2 原站行为对照', '', '原站本轮实测单列；P1/P2设计断言不冒充原站事实，旧实现静态证据不冒充R2 P3。', '', '|编号|模块|操作与原站结果|P1|P2|旧实现/四方对照|分类|', '|---|---|---|---|---|---|---|']
for x in observations:
    lines.append('|' + '|'.join(cell(x.get(k, '')) for k in ['id', 'module', 'actual', 'p1', 'p2', 'implementation', 'classification']) + '|')
(D / 'R2_Original_Behavior_Matrix.md').write_text('\n'.join(lines) + '\n')
lines = ['# R2 差异台账', '', '只统计下列实际登记项；零缺陷发现不等全部相同。环境/角色阻塞与业务缺陷分别解释。', '', '|编号|模块|分类|级别|依据与影响|处置及责任|', '|---|---|---|---|---|---|']
for x in differences:
    lines.append('|' + '|'.join(cell(x.get(k, '')) for k in ['id', 'module', 'classification', 'severity', 'finding', 'disposition']) + '|')
(D / 'R2_Parity_Difference_Ledger.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'observations': len(observations), 'differences': len(differences), 'check': 'evidence_structure_only'}, ensure_ascii=False))
