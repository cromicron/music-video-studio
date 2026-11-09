from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,re,sys,time
repo=Path('/workspace/music-video-studio');p=repo/'productions/join-me-in-life/full-film/performance-cut';cli='/workspace/.tools/jml-kaggle/bin/kaggle'
def now():return datetime.now(timezone.utc).isoformat()
def read(x):return json.loads(Path(x).read_text())
def sha(x):
 with Path(x).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def call(args):
 c=subprocess.run([cli]+args,capture_output=True,text=True)
 if c.returncode:raise RuntimeError('Official CLI read failed '+repr(args)+' '+c.stderr+' '+c.stdout)
 return c
terminal={'COMPLETE','ERROR','CANCEL_ACKNOWLEDGED','CANCELLED','CANCELED'}
legacy404={'darionalis/join-me-in-life-gpu-check','darionalis/notebook511d1535d5'}
known_versions={'darionalis/jml-p-pilot-01':2,'darionalis/jml-p-followup-01':2,'darionalis/jml-p-vocals-01':2,'darionalis/jml-p-instruments-a':1,'darionalis/jml-p-instruments-b':1}
for group in ['a','b']:
 attempted=p/f'research/operations-instruments-{group}-submission-v1.json'
 if attempted.exists():
  j=read(attempted)
  if not j.get('execution_private_code_mount_verified'):raise RuntimeError('Existing incomplete attempt requires manual inspection: '+str(attempted))
  known_versions[j['notebook']]=j['execution_version']
def status(ref):
 target=ref+'/'+str(known_versions[ref]) if ref in known_versions else ref
 c=subprocess.run([cli,'kernels','status',target],capture_output=True,text=True);out=c.stdout+c.stderr;m=re.search(r'has status "(?:KernelWorkerStatus\.)?([A-Z_]+)"',out)
 if m:return {'ref':ref,'queried':target,'status':m.group(1),'observed_utc':now(),'evidence':'fresh_official_status'}
 if ('404' in out or 'Not Found' in out) and ref in legacy404:return {'ref':ref,'queried':target,'status':'NOT_FOUND','observed_utc':now(),'evidence':'fresh_official404_no_active_inactive_inference'}
 raise RuntimeError(ref+': unresolved fresh status '+out)
def account():
 cachepath=repo/'build/jml-p-account-status-cache-v1.json'
 if cachepath.exists():cache=read(cachepath)
 else:
  baseline={r['ref']:r for r in read('/tmp/pcut-account-kernels-before-next.json')};s=read(p/'research/operations-vocals01-submission-v1.json')
  cache={x['ref']:{'last_run_time':baseline[x['ref']]['lastRunTime'],'status':x['status'],'observed_utc':s['preexecution_utc'],'evidence':'earlier_complete_account_status_scan_before_vocals_push'} for x in s['account_statuses_before']}
 fresh=json.loads(call(['kernels','list','--mine','--page-size','100','--format','json']).stdout)
 assert len(fresh)<100,'Pagination may be incomplete'
 rows=[]
 for x in fresh:
  ref=x['ref'];old=cache.get(ref);changed=not old or old['last_run_time']!=x['lastRunTime'];needs=changed or old['status'] not in terminal|{'NOT_FOUND'}
  if needs:
   row=status(ref);time.sleep(0.8)
  else:
   row=dict(old);row['ref']=ref;row['evidence']='cached_terminal_or_historical404_with_unchanged_latest_run_time';row['cache_source_observed_utc']=old.get('observed_utc')
  row['last_run_time']=x['lastRunTime'];rows.append(row)
 cachepath.write_text(json.dumps({r['ref']:r for r in rows},indent=2)+'\n')
 active=[r for r in rows if r['status'] not in terminal|{'NOT_FOUND'}]
 return {'observed_utc':now(),'owned_latest_run_metadata':fresh,'statuses':rows,'reported_active':active,'legacy404_scope':'Two unchanged historical unreadable refs are retained explicitly; no active/inactive inference for404. Provider admission remains final.','list_limitations':'Only populated ref/latestRunTime fields used. Official SDK current_version_number/privacy/GPU list fields are unsupported defaults, not proof.'}
def cells(nb):return [(c['cell_type'],''.join(c['source']) if isinstance(c['source'],list) else c['source']) for c in nb['cells']]

config=read(repo/'build/jml-p-correction-release-routing-v1.json')
for job in config['jobs']:
 ident='darionalis/jml-p-'+job['slug'];sp=p/f"research/operations-{job['tag']}-submission-v1.json"
 if sp.exists():
  prior=read(sp)
  if not prior.get('execution_private_code_mount_verified'):raise RuntimeError('Ambiguous existing correction submission; inspect, never resubmit')
  known_versions[ident]=prior['execution_version']
 else:known_versions[ident]=job['version']-1
job=next(x for x in config['jobs'] if x['tag']==sys.argv[1]);release=p/job['release'];assert sha(release)==job['release_sha256'];rel=read(release);assert rel['status']=='released_for_one_exact_job_when_actual_account_slot_free';ident='darionalis/jml-p-'+job['slug'];assert rel['kernel']==ident and rel['expected_execution_version']==job['version']
prepath=p/rel['predeployment']['file'];assert sha(prepath)==rel['predeployment']['sha256'];pre=read(prepath);bundle=repo/pre['local_bundle'];kernel=bundle.with_name(bundle.name+'-kernel');assert sha(p/rel['plan']['file'])==rel['plan']['sha256'];assert sha(bundle/'package-lock.json')==rel['package_lock_sha256'];assert pre['no_run_version']+1==job['version'];assert sha(kernel/'private-diagnostic.ipynb')==pre['notebook_source_sha256'] and sha(kernel/'kernel-metadata.json')==pre['kernel_metadata_sha256']
for name,h in read(bundle/'package-lock.json')['files'].items():assert sha(bundle/name)==h,name
recordpath=p/f"research/operations-{job['tag']}-submission-v1.json";assert not recordpath.exists(),'Prior attempt exists; never blindly retry'
a=account();assert len(a['reported_active'])<2,('No free account slot',a['reported_active']);quota=call(['quota']);m=re.search(r'GPU\s+[0-9.]+h\s+([0-9.]+)h',quota.stdout);assert m;remaining=float(m.group(1));assert remaining>=1.5,'Unexpectedly low actual quota for bounded correction; report root'
out={'schema':'jml-performance-cut-bounded-submission/v1','authority':str(release.relative_to(p)),'release_record_sha256':sha(release),'preexecution_utc':now(),'quota_before_raw':quota.stdout,'quota_remaining_before_hours':remaining,'account_preflight':a,'notebook':ident,'dataset':pre['dataset'],'dataset_version':pre['dataset_version'],'package_lock_sha256':rel['package_lock_sha256'],'plan_sha256':rel['plan']['sha256'],'takes':rel['takes'],'provider_cap_seconds':5400,'automatic_retries':0,'new_cash_eur':0,'state':'attempt_recorded_before_single_submission'};recordpath.write_text(json.dumps(out,indent=2)+'\n');qp=p/f"research/operations-{job['tag']}-preexecution-quota.txt";assert not qp.exists();qp.write_text(quota.stdout)
c=subprocess.run([cli,'kernels','push','--path',str(kernel),'--timeout','5400','--accelerator','NvidiaTeslaT4'],capture_output=True,text=True);out.update({'submission_utc':now(),'submission_returncode':c.returncode,'submission_stdout':c.stdout.strip(),'submission_stderr':c.stderr.strip()});recordpath.write_text(json.dumps(out,indent=2)+'\n');match=re.search(r'Kernel version (\d+) successfully pushed',c.stdout);assert c.returncode==0 and match,'Ambiguous submission, inspect actual remote; no automatic retry';version=int(match.group(1));assert version==job['version'] and 'https://www.kaggle.com/code/'+ident in c.stdout;out.update({'actual_execution_version':version,'submission_recognized':True,'state':'submitted_once_waiting_actual_output'});recordpath.write_text(json.dumps(out,indent=2)+'\n')
e=repo/f"build/jml-p-{job['slug']}-execution-v{version}-readback";assert not e.exists();e.mkdir();call(['kernels','pull',ident+'/'+str(version),'--metadata','--path',str(e)]);meta=read(e/'kernel-metadata.json');assert meta['id']==ident and meta['is_private'] is True and meta['machine_shape']=='NvidiaTeslaT4' and meta['dataset_sources']==[pre['dataset']];assert cells(read(e/(ident.split('/')[1]+'.ipynb')))==cells(read(kernel/'private-diagnostic.ipynb'));known_versions[ident]=version;state=status(ident);out.update({'execution_private_code_mount_verified':True,'execution_version':version,'execution_status_first_observed':state['status'],'execution_verified_utc':now()});recordpath.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'event':'correction_submitted_once','job':ident+'/'+str(version),'actual_status':state['status'],'record':str(recordpath.relative_to(repo)),'quota_remaining_hours':remaining,'active_before':a['reported_active']}),flush=True)
