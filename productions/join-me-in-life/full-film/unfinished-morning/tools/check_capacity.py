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
record={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Read-only account capacity; unrelated notebook contents not inspected','active':active,'not_found':missing,'other_errors':failures,'statuses':results,'provider_admission_is_final':True,'interpretation':'A404 setup notebook is not established as active. No active-status claim is made for unreadable entries. Provider admission must still enforce account limit; no cancellation or automatic retry if rejected.'}
args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'active':active,'not_found_count':len(missing),'other_error_count':len(failures),'report':str(args.report)}))
raise SystemExit(1 if failures or len(active)>=2 else 0)
