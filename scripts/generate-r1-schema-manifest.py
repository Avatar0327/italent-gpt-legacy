#!/usr/bin/env python3
"""Derive the exact schema contract from committed SQL in a fresh synthetic SQLite database."""
from pathlib import Path
import sqlite3,json,hashlib
root=Path(__file__).resolve().parents[1];db=sqlite3.connect(':memory:')
for p in sorted((root/'drizzle').glob('*.sql')):db.executescript(p.read_text())
objects=[{'type':r[0],'name':r[1],'table':r[2],'sql':r[3]} for r in db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ORDER BY type,name")]
tables=[]
for obj in objects:
 if obj['type']!='table':continue
 columns=list(db.execute('PRAGMA table_info("'+obj['name']+'")'));tables.append({'name':obj['name'],'columns':[r[1]for r in columns],'keys':[r[1]for r in sorted(columns,key=lambda r:r[5])if r[5]],'tenantColumn':'owner' if obj['name']=='hris_workspaces' else 'tenant_id' if any(r[1]=='tenant_id'for r in columns) else None})
files=[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted((root/'drizzle').glob('*.sql'))]
(root/'lib/hris/r1-schema-manifest.ts').write_text('// Generated from local synthetic SQLite; no production schema was accessed.\nexport const schemaObjects='+json.dumps(objects,ensure_ascii=False,separators=(',',':'))+';\nexport const schemaTables='+json.dumps(tables,separators=(',',':'))+';\nexport const migrationFiles='+json.dumps(files,separators=(',',':'))+';\n')
print(json.dumps({'tables':len(tables),'objects':len(objects),'ddlFiles':len(files)}))
