"""Source identity and desktop decision tables; never calls a business action."""
import json
from pathlib import Path
D=Path(__file__).resolve().parent
A=json.loads((D/'Foundation_Adaptations.json').read_text())['adaptations'];T=json.loads((D/'Requirements_Trace.json').read_text());S={s['id']:s for s in json.loads((D/'Acceptance_Scenarios.json').read_text())['scenarios']}
walkthroughs=[
 {'id':'R2-P3-BASE-02-AC03','steps':[{'actor':'E1','action':'read developmentSummary','decision':'allow only developmentSummary','versions':'unchanged'},{'actor':'E1/H/L','action':'read answers/bridgeReviewer/anonymousMean','decision':'403 absent exact field grant','versions':'unchanged'},{'actor':'H/L','action':'read E1 feedback','decision':'403 absent reportRead','versions':'unchanged'}]},
 {'id':'R2-P3-BASE-03-AC02','steps':[{'actor':'H','action':'catalog.edit name','decision':'new CT1-v2 + audit + receipt','versions':'no certificate or M01 assignment history'},{'actor':'R','action':'certification.revoke','decision':'one revocation event at commit time','versions':'CERT1-v1 immutable, validity revoked'},{'actor':'R','action':'repeat same key','decision':'original receipt','versions':'no second revocation'},{'actor':'H','action':'change issuedAt/personId/auditActor','decision':'reject','versions':'unchanged'}]},
 {'id':'R2-P3-BASE-04-AC02','steps':[{'actor':'H','action':'unbind or replace B1 on published REP1-v1','decision':'409 IMMUTABLE_VERSION','versions':'B1/OBJ-A-v1 unchanged'},{'actor':'H','action':'bind OBJ-B-v1 to draft REP1-v2','decision':'new B2 under draft grant','versions':'v1 still OBJ-A-v1, v2 draft only'},{'actor':'H','action':'download old B1','decision':'allow only under current old-version grant','versions':'no audience inheritance for B2'}]}]
for row in walkthroughs:
 a=A[row['id']];s=S[row['id']];src=next(x['source'] for x in T['acceptanceIds'] if 'R2-P3-'+x['id']==row['id'])
 assert s['originalFoundationGwt']=={k:src[k] for k in ['given','when','then','basis']}
 assert all(a.get(k) for k in ['fixture','actions','actors','allowedFields','forbiddenFields','expectedVersions','given','when','then','inheritance'])
 assert s['executionStatus']=='not_run' and s['fixture']==a['fixture']
 row['desktopConclusion']='fixture/actions/role fields/version results explicit; source retained; ready for independent P2 recheck'
(D/'evidence/repair-003-desktop.json').write_text(json.dumps(dict(kind='P2_document_desktop_review_not_P3_execution',count=3,walkthroughs=walkthroughs),ensure_ascii=False,indent=2)+'\n');print('3 source-preserving desktop tables checked; P3 execution=0')
