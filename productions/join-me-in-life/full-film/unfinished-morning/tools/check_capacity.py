#!/usr/bin/env python3
"""Read account notebook statuses before a C submission; never mutate a provider."""
import argparse,concurrent.futures,csv,datetime,io,json,pathlib,subprocess
CLI='/workspace/.tools/jml-kaggle/bin/kaggle'
p=argparse.ArgumentParser();p.add_argument('--report',type=pathlib.Path,required=True);args=p.parse_args()
if args.report.exists():raise SystemExit('Preserve existing capacity evidence; choose fresh report')
rows=list(csv.DictReader(io.StringIO(subprocess.check_output([CLI,'kernels','list','--mine','--page-size','100','--csv'],text=True))))
if len(rows)>=100:raise SystemExit('Listing may be paginated; inspect complete account before submission')
def get(row):
 out=subprocess.run([CLI,'kernels','status',row['ref']],capture_output=True,text=True)
 return {'ref':row['ref'],'returncode':out.returncode,'status':out.stdout.strip(),'error':out.stderr.strip()}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(get,rows))
active=[x for x in results if any(s in x['status'] for s in ['.RUNNING','.QUEUED'])]
missing=[x for x in results if x['returncode'] and '404 Client Error' in x['error']]
failures=[x for x in results if x['returncode'] and x not in missing]
quota=json.loads(subprocess.check_output([CLI,'quota','--format','json'],text=True))
gpu=next(x for x in quota if x['resource']=='GPU')
remaining=float(gpu['remaining'].removesuffix('h'))
# Conservative: reserve the full cap for every active job plus the proposed job,
# even when some active time may already have been charged. No double-count savings.
reserved_job_hours=1.5+sum(1.5 if x['ref'].startswith('darionalis/jml-c-') else 12 for x in active)
quota_gate={'gpu_remaining_hours':remaining,'minimum_correction_reserve_hours':4,'full_caps_reserved_hours':reserved_job_hours,'remaining_after_reserved_caps':remaining-reserved_job_hours,'pass':remaining-reserved_job_hours>=4,'scope':'Read-only official quota; full5400s allowance for each active and proposed C job, conservative12h allowance for any unrelated active job; no unrelated content inspected.'}
record={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Read-only account capacity; unrelated notebook contents not inspected','active':active,'not_found':missing,'other_errors':failures,'statuses':results,'quota':quota,'quota_gate':quota_gate,'provider_admission_is_final':True,'interpretation':'A404 setup notebook is not established as active. No active-status claim is made for unreadable entries. Provider admission must still enforce account limit; no cancellation or automatic retry if rejected.'}
args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'active':active,'not_found_count':len(missing),'other_error_count':len(failures),'report':str(args.report),'quota_gate':quota_gate}))
raise SystemExit(1 if failures or len(active)>=2 or not quota_gate['pass'] else 0)
