"""Verify the complete task/capability/joint closure DAG without execution."""
import json
from graphlib import TopologicalSorter
from pathlib import Path
D=Path(__file__).resolve().parent;r=json.loads((D/'Task_Dependencies.json').read_text());tasks=r['tasks'];ids={x['taskId'] for x in tasks};assert len(tasks)==len(ids)==46
schemas=json.loads((D/'Interface_Schemas.json').read_text())['$defs'];graph={}
for t in tasks:
 assert set(t['r2CompletionPredecessors'])<=ids
 assert all(x.split('/')[-1] in schemas for x in t['requiredSchemas'])
 assert t['requiredAdapters'] and t['requiredSecurityContract'] and t['status']=='proposed_not_started'
 graph[t['taskId']]=t['r2CompletionPredecessors']+['R1-CAP-'+g for g in t['requiredR1CapabilityGates']]+t['externalProducerDependencies']
for k,c in r['r1CapabilitySlots'].items():
 assert c['implementationCommitSha'] is None and c['status']=='pending_owner_freeze' and not c['capabilityOpen']
 graph['R1-CAP-'+k]=[]
for k in r['externalProducerSlots']:graph[k]=[]
graph['R3-PRODUCERS-READY']=list(r['externalProducerSlots'])
graph[r['jointClosure']['id']]=r['jointClosure']['completionPredecessors'];graph['P3-R1-10-COMPLETE']=[r['jointClosure']['id']];graph['P3-R1-11-EXIT']=['P3-R1-10-COMPLETE']
order=list(TopologicalSorter(graph).static_order());assert len(order)==len(graph)
output=dict(kind='P2_dependency_analysis_not_task_execution',r2TaskCount=46,fullGraphNodeCount=len(graph),edges=sum(map(len,graph.values())),cycles=0,topologicalOrder=order,graph=graph,allImplementationBaselinesUnfrozen=True)
(D/'evidence/repair-004-dag.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in output.items() if k not in ['graph','topologicalOrder']})
