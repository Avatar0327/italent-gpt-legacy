"""Proof-based re-proposal of the six disputed P2 items; independent acceptance not presumed."""
import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
PROOFS={
'M37-LIMIT-01.01':('R2-EXIT-001',['LEVEL-VALID','LEVEL-EXTRA','LEVEL-VERSION','LEVEL-SOURCE','LEVEL-MISSING','REF-COMMAND-VALID','REF-COMMAND-SOURCE'],'逐等级alias/elementText/subsetName及父指标/level/version规范持久化，来源联合按命令限制；旧尺度与独立审核保持','Contract_Repair.md'),
'M06-LIMIT-01.01':('R2-EXIT-001',['TYPE-VALID','TYPE-RATING-VALID','TYPE-EXTRA','TYPE-VERSION','TYPE-SOURCE','TYPE-MISSING','TYPE-EXACT-VERSION'],'指标类型isCommon/说明行/评分模式及数值尺度、评级方案精确版本；资格级别不混用，目录与标准冻结链确定','Contract_Repair.md'),
'M26-LIMIT-01.01':('R2-EXIT-001',['QUESTION-VALID','QUESTION-EXTRA','QUESTION-VERSION','QUESTION-SOURCE','QUESTION-MISSING'],'逐题角色/维度/指标版本和条件显示绑定闭合，套卷列表不再推断逐题关系，原卷/邀请根不改','Contract_Repair.md'),
'M26-LIMIT-01.02':('R2-EXIT-002',['ANON-01','ANON-02','ANON-03','ANON-04','ANON-05A','ANON-05B','ANON-06A','ANON-06B','ANON-07A','ANON-07B','ANON-07C','ANON-08A','ANON-08B','ANON-08C','ANON-09','ANON-10'],'答卷ID/单题atom谱系/报告版本/关联伪名与向量分组严格分离；首报放行、差分及双阈值拒绝，账本epoch不清历史','Anonymity_Repair.md'),
'M18-LIMIT-01.01':('R2-EXIT-001',['HISTORY-VALID','HISTORY-EXTRA','HISTORY-MISSING'],'项目create/save明确previousResultRef或null；历史发布集根/版本/asOf/字段白名单/用途和关系严格可表达','Contract_Repair.md'),
'M18-LIMIT-01.02':('R2-EXIT-001',['HISTORY-VALID','HISTORY-NONE-VALID','HISTORY-VERSION','HISTORY-SOURCE'],'历史项目同人映射和精确版本核验，不预填为当前评定、不向M17自动生效；历史未知隔离及旧版本保留','Contract_Repair.md')}
def apply(items):
 accepted=[]
 for x in items:
  if x['id'] not in PROOFS:
   if x['disposition']=='P2_design_closed':x['independentReviewDisposition']='accepted_design_layer_at_bd976480';accepted.append(x['id'])
   continue
  finding,ids,why,design=PROOFS[x['id']];filename='repair-002-anonymity.json' if finding.endswith('002') else 'repair-001-schema.json';p=D/'evidence'/filename;data=json.loads(p.read_text());by={r['id']:r for r in data['results']};ok=all(i in by and by[i]['pass_'] for i in ids)
  x.update(independentReviewDisposition='not_accepted_before_repair; awaiting_new_independent_recheck',repairFindingId=finding,p2Blocking=not ok,evidenceStatus='design_repaired_document_verified_pending_independent_recheck' if ok else 'repair_open',repairProof=dict(designRef=design,criterion=why,documentProbeIds=ids,evidencePath='evidence/'+filename,evidenceSha256=hashlib.sha256(p.read_bytes()).hexdigest(),result='design_close_reproposed' if ok else 'not_closed',independentlyAcceptedThisRepair=False),closureCriterion=why+'；P3实际实现与P4真实核证责任不关闭。')
  x['designRefs'].append(design)
 return dict(independentAcceptedBeforeRepair=len(accepted),disputedBeforeRepair=len(PROOFS),repairReproposedP2Closed=sum(x.get('repairProof',{}).get('result')=='design_close_reproposed' for x in items),independentAcceptedAfterRepair=None,meaning='9原独立接受+6本轮逐项证明后重新提请关闭；15为设计负责人提案，独立复核/所有者批准尚未发生')
