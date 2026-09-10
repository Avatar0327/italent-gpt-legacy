"""Rebuild documentary sources and run P2-only probes; no product imports or API requests."""
import subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
for name in ['build_inventory.py','build_scenarios.py','build_schemas.py','check_schema_examples.py','check_anonymity.py','build_resolution.py','build_handoff.py','check_foundation_adaptations.py','check_dependencies.py','check_repair.py']:
 subprocess.run([sys.executable,str(D/name)],check=True)
