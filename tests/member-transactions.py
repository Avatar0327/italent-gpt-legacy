import sqlite3,re
from pathlib import Path
c=sqlite3.connect(':memory:');c.execute('PRAGMA foreign_keys=ON')
for f in sorted(Path('drizzle').glob('*.sql')):c.executescript(f.read_text())
source=Path('app/api/access/route.ts').read_text()
queries=re.findall(r"db\.prepare\('([^']+)'\)",source)
setup=[q for q in queries if q.startswith('INSERT INTO') and 'SELECT' not in q]
def bootstrap(tenant,user):
 with c:
  c.execute(setup[0],(tenant,'{"orgs":[],"employees":[],"approvals":[],"audit":[]}'))
  c.execute(setup[1],('primary',tenant,user,'企业','now'))
  c.execute(setup[2],(user,tenant,'admin'))
  c.execute(setup[3],(user+'@example.com',tenant,'管理员','admin',user,'now'))
  c.execute(setup[4],(tenant,'setup-event',user,'初始化','企业','now'))
bootstrap('tenant-a','admin-a')
try:bootstrap('orphan-tenant','intruder')
except sqlite3.IntegrityError:pass
else:raise AssertionError('Second initialization must fail')
assert c.execute('SELECT count(*) FROM hris_workspaces').fetchone()[0]==1
member_source=Path('app/api/members/route.ts').read_text()
member_queries=re.findall(r'db\.prepare\("([^"\n]+)"\)',member_source)+re.findall(r"db\.prepare\('([^']+)'\)",member_source)
update=next(q for q in member_queries if q.startswith('UPDATE hris_workspaces'))
grant=next(q for q in member_queries if q.startswith('INSERT INTO hris_access_grants'))
sync=next(q for q in member_queries if q.startswith('UPDATE hris_memberships'))
audit=next(q for q in member_queries if q.startswith('INSERT INTO hris_audit_events'))
def save(revision,event,email,active,employee=None,actor='admin-a'):
 with c:
  changed=c.execute(update,(event,'tenant-a',revision,actor,'tenant-a')).rowcount
  c.execute(grant,(email,'测试成员','employee',employee,active,'now','tenant-a',event))
  c.execute(sync,('employee',employee,active,'tenant-a',email,'tenant-a','tenant-a',event))
  c.execute(audit,(event,actor,'配置成员',email,'now','tenant-a',event))
 return changed
assert save(0,'grant1','employee@example.com',1,'e1')==1
assert save(0,'stale','stale@example.com',1)==0
assert c.execute('SELECT count(*) FROM hris_access_grants').fetchone()[0]==2
activate=next(q for q in queries if q.startswith('INSERT INTO hris_memberships') and 'SELECT' in q)
claim=next(q for q in queries if q.startswith('UPDATE hris_access_grants'))
with c:
 assert c.execute(activate,('member-a','employee@example.com')).rowcount==1
 assert c.execute(claim,('member-a','now','employee@example.com','member-a')).rowcount==1
with c:assert c.execute(activate,('attacker','employee@example.com')).rowcount==0
assert save(1,'disable','employee@example.com',0,'e1')==1
assert c.execute('SELECT active FROM hris_memberships WHERE user_id=?',('member-a',)).fetchone()[0]==0
assert save(2,'enable','employee@example.com',1,'e1')==1
try:save(3,'duplicate','other@example.com',1,'e1')
except sqlite3.IntegrityError:pass
else:raise AssertionError('Duplicate active employee must fail')
assert c.execute('SELECT revision FROM hris_workspaces').fetchone()[0]==3
assert save(3,'unauthorized','attacker@example.com',1,actor='member-a')==0
print('SQLite: one-time setup rollback, member CAS, identity claiming, disable propagation, employee uniqueness and admin gate passed')
