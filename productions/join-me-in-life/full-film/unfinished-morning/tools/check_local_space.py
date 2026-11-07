#!/usr/bin/env python3
"""Read-only disk capacity preflight; never delete files."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--path',type=Path,default=Path.cwd())
p.add_argument('--minimum-free-gib',type=float,default=4)
p.add_argument('--report',type=Path)
a=p.parse_args()
if a.report and a.report.exists():p.error('Preserve existing evidence; choose a fresh report')
u=shutil.disk_usage(a.path)
j={'observed_utc':datetime.now(timezone.utc).isoformat(),'path':str(a.path.resolve()),'free_bytes':u.free,'free_gib':u.free/1024**3,'minimum_free_gib':a.minimum_free_gib,'pass':u.free>=a.minimum_free_gib*1024**3,'action_if_low':'Pause large local downloads/staging and advise root. No automatic deletion; provider jobs remain untouched.'}
if a.report:
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j))
raise SystemExit(0 if j['pass'] else 1)
