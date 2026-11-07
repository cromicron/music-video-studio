#!/usr/bin/env python3
"""Read-only exact-version provider watcher; returns when any listed job is terminal."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import time

CLI = '/workspace/.tools/jml-kaggle/bin/kaggle'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jobs', nargs='+')
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--poll-seconds', type=int, default=45)
    parser.add_argument('--timeout-seconds', type=int, default=6000)
    args = parser.parse_args()
    if args.report.exists() or not 10 <= args.poll_seconds <= 60:
        parser.error('Fresh report and10–60second poll required')
    if any(not re.fullmatch(r'darionalis/jml-c-[a-z0-9-]+/[1-9][0-9]*', job) for job in args.jobs):
        parser.error('Explicit C notebook versions required')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    record = {'scope':'Read-only statuses; no submission/retry/cancellation or output access','jobs':args.jobs,'events':[]}
    last = {}
    deadline = time.monotonic() + args.timeout_seconds
    while time.monotonic() < deadline:
        terminal = []
        for job in args.jobs:
            result = subprocess.run([CLI,'kernels','status',job],capture_output=True,text=True,timeout=30)
            if result.returncode:
                raise RuntimeError('Provider status failed; operator must inspect: '+job+' '+result.stderr)
            match = re.search(r'KernelWorkerStatus\.([A-Z_]+)', result.stdout)
            if not match:
                raise RuntimeError('Unrecognized provider status: '+result.stdout)
            status = match.group(1)
            if last.get(job) != status:
                event = {'observed_utc':datetime.now(timezone.utc).isoformat(),'job':job,'status':status}
                record['events'].append(event); print(json.dumps(event),flush=True); last[job]=status
            if status not in ('RUNNING','QUEUED','NEW','INITIALIZING'):
                terminal.append({'job':job,'status':status})
        record['last_checked_utc']=datetime.now(timezone.utc).isoformat()
        record['terminal']=terminal
        args.report.write_text(json.dumps(record,indent=2)+'\n')
        if terminal:
            return
        time.sleep(args.poll_seconds)
    raise TimeoutError('Observer timed out; provider jobs were not cancelled')

if __name__ == '__main__':
    main()
