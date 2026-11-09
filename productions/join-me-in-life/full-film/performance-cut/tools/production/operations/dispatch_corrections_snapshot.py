from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,time,shutil
r=Path('/workspace/music-video-studio');p=r/'productions/join-me-in-life/full-film/performance-cut';cli='/workspace/.tools/jml-kaggle/bin/kaggle';config=r/'build/jml-p-correction-release-routing-v1.json'
def now():return datetime.now(timezone.utc).isoformat()
def read(f):return json.loads(Path(f).read_text())
def sha(f):
 with Path(f).open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def run(args):
 c=subprocess.run(args,cwd=r,capture_output=True,text=True)
 if c.returncode:raise RuntimeError('Bounded correction operation failed '+repr(args)+' '+c.stdout+' '+c.stderr)
 return c
def assert_release(j):
 release=p/j['release'];assert sha(release)==j['release_sha256'];rel=read(release);assert rel['kernel']=='darionalis/jml-p-'+j['slug'] and rel['expected_execution_version']==j['version'];return rel
def watcher(j):
 obs=r/f"build/jml-p-{j['tag']}-observer-v1.json";assert not obs.exists();log=obs.with_suffix('.log')
 with log.open('ab') as f:proc=subprocess.Popen(['python3',str(p/'tools/production/watch_jobs.py'),f"darionalis/jml-p-{j['slug']}/{j['version']}",'--report',str(obs),'--poll-seconds','60','--timeout-seconds','6200'],cwd=r,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 routing=p/f"research/operations-{j['tag']}-monitor-routing-v1.json";assert not routing.exists();routing.write_text(json.dumps({'observed_utc':now(),'scope':'Read-only exact submitted-version observer, no provider mutation','job':f"darionalis/jml-p-{j['slug']}/{j['version']}",'pid':proc.pid,'observer':str(obs.relative_to(r)),'log':str(log.relative_to(r)),'poll_seconds':60,'timeout_seconds':6200},indent=2)+'\n');print(json.dumps({'event':'correction_observer_started','tag':j['tag'],'pid':proc.pid}),flush=True)
def retain(j):
 rec=p/f"research/operations-{j['tag']}-retention-v1.json"
 if rec.exists():assert read(rec)['state']=='technically_verified_retained_for_independent_motion_review';return
 rel=assert_release(j);pre=read(p/rel['predeployment']['file']);bundle=r/pre['local_bundle'];assert sha(bundle/'package-lock.json')==rel['package_lock_sha256'];quota=run([cli,'quota']).stdout;qp=p/f"research/operations-{j['tag']}-postcompletion-quota.txt";assert not qp.exists();qp.write_text(quota);dest=r/f"build/jml-p-{j['slug']}-results-v{j['version']}";assert not dest.exists(),'Partial prior download: inspect manually, never regenerate';dest.mkdir();ref=f"darionalis/jml-p-{j['slug']}/{j['version']}";run([cli,'kernels','output',ref,'--path',str(dest),'--page-size','100','--quiet']);res=dest/('jml-p-performance-results' if j['kind']=='a2v' else 'jml-ltx-story23-results');assert (res/'job.json').is_file();verification=p/f"research/operations-{j['tag']}-output-verification-v1.json";tool=p/('tools/production/performance/verify_download.py' if j['kind']=='a2v' else 'tools/production/verify_completed_batch.py');run(['python3',str(tool),'--bundle',str(bundle),'--results',str(res),'--expected-lock',rel['package_lock_sha256'],'--report',str(verification)]);v=read(verification);assert v['all_takes_technically_verified'];target=p/f"assets/motion/{j['tag']}-v{j['version']}";assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(res,target);files=[{'file':str(f.relative_to(r)),'sha256':sha(f),'bytes':f.stat().st_size}for f in sorted(target.rglob('*'))if f.is_file()];raw={}
 for t in v['takes']:
  sid=t.get('take_id',t.get('shot_id'));video=target/sid/'video-silent.mp4';assert sha(video)==t['video_sha256'];raw[sid]={'path':str(video.relative_to(r)),'sha256':sha(video),'frames':t['frames']}
 d={'schema':'jml-performance-cut-output-retention/v1','observed_utc':now(),'state':'technically_verified_retained_for_independent_motion_review','provider_job':ref,'directory':str(target.relative_to(r)),'files':files,'technical_verification':{'file':str(verification.relative_to(r)),'sha256':sha(verification)},'raw_video_paths':raw,'whole_job_seconds':v['whole_job_seconds'],'quota_after_raw':quota,'quota_scope':'Actual account snapshot after completion; other authorized job may still accrue. Aggregate debit cannot be attributed to this job alone.','creative_acceptance':'Pending new independent actual motion/song/contact and root adoption; not an automatic correction success.'};rec.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'event':'correction_retained_verified','job':ref,'retention':str(rec.relative_to(r)),'technical_report':str(verification.relative_to(r)),'raw_videos':raw,'quota':quota}),flush=True)
def observer_active(tag,ref):
 obs=r/f'build/jml-p-{tag}-observer-v1.json';assert obs.exists(),'Submitted job lacks watcher; inspect, never resubmit'
 try:d=read(obs)
 except json.JSONDecodeError:return True
 terms=d.get('terminal',[])
 if terms:
  assert len(terms)==1 and terms[0]['job']==ref and terms[0]['status']=='COMPLETE',('Unexpected remote terminal: report root, no generation retry',terms)
  return False
 assert time.time()-obs.stat().st_mtime<180,('Stale local watcher, inspect actual provider without resubmitting',obs)
 return True
end=time.monotonic()+4*3600
while time.monotonic()<end:
 cfg=read(config);jobs=cfg['jobs'];assert len({j['tag'] for j in jobs})==len(jobs)<=2;active=[];base_retained=[]
 for group in ['a','b']:
  tag='instruments-'+group;ref=f'darionalis/jml-p-instruments-{group}/2'
  if observer_active(tag,ref):active.append(ref)
  rec=p/f'research/operations-{tag}-retention-v1.json'
  if rec.exists():
   try:done=read(rec)
   except json.JSONDecodeError:continue
   assert done['state']=='technically_verified_retained_for_independent_motion_review';proof=r/done['technical_verification']['file'];assert sha(proof)==done['technical_verification']['sha256'];base_retained.append(ref)
 completed=[]
 for j in jobs:
  assert_release(j);sp=p/f"research/operations-{j['tag']}-submission-v1.json"
  if not sp.exists():continue
  sub=read(sp);assert sub.get('execution_private_code_mount_verified'),'Ambiguous correction attempt: report root, never repeat'
  ref=f"darionalis/jml-p-{j['slug']}/{j['version']}"
  if observer_active(j['tag'],ref):active.append(ref)
  else:retain(j);completed.append(j['tag'])
 if len(completed)==cfg.get('expected_total_jobs',2):print(json.dumps({'event':'all_released_corrections_retained','observed_utc':now()}),flush=True);break
 for j in jobs:
  if (p/f"research/operations-{j['tag']}-submission-v1.json").exists():continue
  if len(active)>=2 or not base_retained:break
  c=run(['python3','/tmp/pcut_launch_correction.py',j['tag']]);print(c.stdout.strip(),flush=True);watcher(j);active.append(f"darionalis/jml-p-{j['slug']}/{j['version']}")
 time.sleep(30)
else:raise TimeoutError('Local correction dispatcher expired; provider jobs were not canceled or retried')
