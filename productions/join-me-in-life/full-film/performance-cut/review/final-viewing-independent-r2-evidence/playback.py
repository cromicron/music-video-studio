"""Actual complete-film pass, adapted from retained C preloaded workflow. No seeking or creative auto-acceptance."""
from pathlib import Path
import json,hashlib,time,http.server,threading,functools,sys
from playwright.sync_api import sync_playwright
D=Path(__file__).resolve().parent;R=Path('/workspace/music-video-studio');P=R/'productions/join-me-in-life/full-film/performance-cut'
configuration=Path(sys.argv[1]).resolve();cfg=json.loads(configuration.read_text())
assert cfg['source_role']=='accepted_viewing_copy' and cfg['source']['file']
assert cfg.get('ready_for_playback') is True, 'Actual frozen technical/native/browser checks and explicit root go required before playback'
S=Path(cfg['source']['file']);S=S if S.is_absolute() else R/S
expected=cfg['source']['sha256']
assert S!=R/'build/performance-cut-final-v1/Join_Me_in_Life_Movie_and_Band.mp4', 'Viewing pass must bind actual derivative'
assert cfg['master']['sha256']=='fabe33c576aaa0473e82c6ed755e884e3b6bc9103f392551138f6527099f2fdb'
assert cfg['edit']['sha256']=='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
assert sha(S)==expected and S.stat().st_size==cfg['source']['bytes']
for item in cfg.get('additional_provenance',[]):
 fp=Path(item['file']);fp=fp if fp.is_absolute() else R/fp;assert sha(fp)==item['sha256'], item['file']
for key in ['edit','master_review','technical_verification']:
 item=cfg[key];fp=Path(item['file']);fp=fp if fp.is_absolute() else R/fp;assert sha(fp)==item['sha256'], key
output=D/'playback-v1.json';assert not output.exists()
ep=Path(cfg['edit']['file']);ep=ep if ep.is_absolute() else R/ep;e=json.loads(ep.read_text());assert len(e['shots'])==46
checks=[(.12,'start')]+[((s['start_frame']+s['end_frame_exclusive'])/48,s['id']+'-middle') for s in e['shots']]+[(277.6,'final-tail')]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def end_headers(self):self.send_header('Access-Control-Allow-Origin','*');super().end_headers()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(S.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/{S.name}'
captures=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--enable-automation'],ignore_default_args=['--mute-audio'])
  launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine');assert '--mute-audio' not in launch['arguments']
  page=b.new_page(viewport={'width':1100,'height':650});page.set_content('<body style="margin:0;background:#000"><video id="v" width="1080"></video></body>')
  size=page.evaluate('''async url=>{const blob=await fetch(url).then(r=>r.blob());v.src=URL.createObjectURL(blob);v.muted=false;v.volume=1;v.playbackRate=1;v.preload='auto';v.load();return blob.size;}''',url)
  assert size==S.stat().st_size
  page.wait_for_function('v.readyState>=4',timeout=60000)
  baseline=page.evaluate('''()=>({readyState:v.readyState,time:v.currentTime,duration:v.duration,quality:(q=>({total:q.totalVideoFrames,dropped:q.droppedVideoFrames,corrupted:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality())})''')
  assert baseline['time']==0 and abs(baseline['duration']-6667/24)<.05
  assert page.evaluate('v.videoWidth')==cfg['source']['width'] and page.evaluate('v.videoHeight')==cfg['source']['height']
  page.evaluate('''()=>{window.events=[];window.rvfc=[];['waiting','stalled','error','ended','seeking','seeked','ratechange'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime,wall:performance.now()})));const cb=(now,m)=>{rvfc.push([m.mediaTime,m.presentedFrames,now]);if(!v.ended)v.requestVideoFrameCallback(cb)};v.requestVideoFrameCallback(cb);window.started=performance.now();return v.play();}''')
  for target,label in checks:
   page.wait_for_function('t=>v.currentTime>=t',arg=target,timeout=30000)
   observed=page.evaluate('v.currentTime');file=D/f'playback-{label}.jpg';page.screenshot(path=str(file),quality=86)
   captures.append({'label':label,'requested_seconds':target,'actual_before_screenshot_seconds':observed,'file':str(file),'sha256':sha(file)})
   (D/'playback-progress.json').write_text(json.dumps({'source_sha256':expected,'last':captures[-1],'captures':len(captures)}))
  page.wait_for_function('v.ended',timeout=15000)
  tele=page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,rate:v.playbackRate,muted:v.muted,volume:v.volume,width:v.videoWidth,height:v.videoHeight,ended:v.ended,error:v.error,wallSeconds:(performance.now()-started)/1000,quality:(q=>({total:q.totalVideoFrames,dropped:q.droppedVideoFrames,corrupted:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality()),events:events,rvfcCount:rvfc.length,rvfcFirst:rvfc[0],rvfcLast:rvfc[rvfc.length-1],rvfcMaxMediaGap:rvfc.slice(1).reduce((m,x,i)=>Math.max(m,x[0]-rvfc[i][0]),0)})''')
  callbacks=page.evaluate('rvfc');(D/'presented-frame-callbacks-v1.json').write_text(json.dumps(callbacks)+'\n')
  version=b.version;b.close()
 record={'schema':'jml-independent-complete-viewing-copy-playback/v1','source_role':cfg['source_role'],'configuration':str(configuration),'configuration_sha256':sha(configuration),'master':cfg['master'],'master_review':cfg['master_review'],'technical_verification':cfg['technical_verification'],'additional_provenance':cfg.get('additional_provenance',[]),'source':str(S),'sha256':expected,'bytes':S.stat().st_size,'preloaded_bytes':size,'edit_sha256':sha(ep),'browser':version,'actual_browser_command_line':launch,'ignored_default_args':['--mute-audio'],'baseline':baseline,'telemetry':tele,'captures':captures,'limits':'Actual VIEWING COPY derivative full1x execution; this is not another master playback or a repeat source/45-cut approval. Actual full1x execution with no seeking, preloaded whole-file bytes and actual unmuted launch. Captures and decoded framing/cut proofs require separate visual inspection. This is not subjective hearing, physical speaker-output certification, viewing every native frame, or exact notes/phoneme synchronization.'}
 output.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(tele))
finally:server.shutdown()
