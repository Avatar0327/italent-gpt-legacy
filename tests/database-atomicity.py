"""Exercise the actual API statements against SQLite, including transaction rollback."""
import sqlite3,re
from pathlib import Path
c=sqlite3.connect(':memory:')
c.execute('PRAGMA foreign_keys=ON')
for p in sorted(Path('drizzle').glob('*.sql')): c.executescript(p.read_text())
c.execute('INSERT INTO hris_workspaces(owner,data) VALUES (?,?)',('tenant-a','{}'))
c.execute('INSERT INTO hris_workspaces(owner,data) VALUES (?,?)',('tenant-b','{}'))
c.execute('INSERT INTO hris_memberships(user_id,tenant_id,role,active) VALUES (?,?,?,1)',('user-a','tenant-a','admin'))
c.commit()
source=Path('app/api/hris/route.ts').read_text()
update=re.search(r"prepare\('(UPDATE hris_workspaces[^']+)'\)",source)[1]
audit=re.search(r"prepare\('(INSERT INTO hris_audit_events[^']+)'\)",source)[1]
def write(revision,token,actor='user-a'):
 with c:
  count=c.execute(update,('{"updated":true}',token,'tenant-a',revision,'user-a','tenant-a','admin')).rowcount
  c.execute(audit,(token,actor,'save','subject','2026-09-07','tenant-a',token))
 return count
assert write(0,'event-a')==1
assert write(0,'event-stale')==0
assert c.execute('SELECT count(*) FROM hris_audit_events').fetchone()[0]==1
assert c.execute('SELECT revision FROM hris_workspaces WHERE owner=?',('tenant-b',)).fetchone()[0]==0
try: write(1,'event-rollback',None)
except sqlite3.IntegrityError: pass
else: raise AssertionError('Audit failure must fail transaction')
assert c.execute('SELECT revision,last_mutation FROM hris_workspaces WHERE owner=?',('tenant-a',)).fetchone()==(1,'event-a')
print('SQLite: migrations, stale-write audit suppression, tenant separation and audit rollback passed')
