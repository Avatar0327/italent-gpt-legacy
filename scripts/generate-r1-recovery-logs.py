#!/usr/bin/env python3
"""Add complete-row journals for expanded R1 tables; never touch a live database."""
from pathlib import Path
import sqlite3,json,argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',default='0026_r1_expansion_recovery_log.sql');parser.add_argument('--tables',nargs='*');a=parser.parse_args()
root=Path(__file__).resolve().parents[1];db=sqlite3.connect(':memory:')
for p in sorted((root/'drizzle').glob('*.sql')):
 if p.name<a.output:db.executescript(p.read_text())
skip={'r1_recovery_changes','r1_report_query_cursors','r1_portal_cursors','r1_workflow_commit_guard','r1_adapter_guard'}
aux={'r1_report_file_intents','r1_upload_intents','r1_workflow_denials'}
output=['-- Full-row recovery journal for R1 expansion. Cursor caches and assertion tables are reconstructed/invalidated, never restored as authority.']
for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'r1_%' ORDER BY name"):
 if table in skip or a.tables and table not in a.tables:continue
 cols=list(db.execute('PRAGMA table_info("'+table+'")'));names=[c[1]for c in cols];keys=[c[1]for c in sorted(cols,key=lambda c:c[5])if c[5]]
 if 'tenant_id' not in names:raise RuntimeError(table)
 for operation in ['insert','update','delete']:
  alias='OLD' if operation=='delete' else 'NEW';tenant=f'{alias}.tenant_id';current=f'(SELECT w.last_mutation FROM hris_workspaces w JOIN r1_commands c ON c.tenant_id=w.owner AND c.token=w.last_mutation WHERE w.owner={tenant} AND c.status=\'processing\')';fallback="'aux:'" if table in aux else "'unfenced:'";token=f'coalesce({current},{fallback}||lower(hex(randomblob(16))))'
  if table=='r1_commands' and operation=='insert':token='NEW.token'
  if table=='r1_commands' and operation=='update':token=f'CASE WHEN NEW.token=(SELECT last_mutation FROM hris_workspaces WHERE owner=NEW.tenant_id) THEN NEW.token ELSE {token} END'
  rowkey='json_array('+','.join(f'{alias}."{k}"'for k in keys)+')';image='NULL' if operation=='delete' else 'json_object('+','.join("'"+c+"',"+alias+'."'+c+'"' for c in names)+')'
  revision=f'coalesce((SELECT revision FROM hris_workspaces WHERE owner={tenant}),0)'
  if table=='r1_commands' and operation=='insert':revision='NEW.workspace_revision+1'
  if a.output!='0026_r1_expansion_recovery_log.sql':output.append(f'DROP TRIGGER IF EXISTS r1_log_{table}_{operation};')
  output.append(f'''CREATE TRIGGER r1_log_{table}_{operation} AFTER {operation.upper()} ON "{table}"
BEGIN
 INSERT INTO r1_recovery_changes(tenant_id,tx_id,table_name,row_key,operation,after_image,schema_version,workspace_revision)
 VALUES({tenant},{token},'{table}',{rowkey},'{operation}',{image},coalesce((SELECT schema_version FROM r1_schema_state WHERE tenant_id={tenant}),1),{revision});
END;''')
(root/'drizzle'/a.output).write_text('\n'.join(output)+'\n');print(json.dumps({'triggers':len(output)-1,'excludedEphemeral':sorted(skip),'singleRowAuxiliary':sorted(aux)}))
