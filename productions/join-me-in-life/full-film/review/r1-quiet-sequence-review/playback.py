"""Actual unseeked 1x playback of the two R1 contexts, supplied audio enabled.
Writes ignored build/r1-quiet-sequence-review, not production data.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib, json
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/r1-quiet-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:960px;height:540px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.seen=[];window.events=[];['playing','ended','waiting','stalled','error'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for label,name,sha,targets in [
  ('waiting-context','Waiting_Correction_Context','b1f61bd2b17ec7e05596d0add089902a17cb300c14e86dc239c9c83ed577e4f8',[6.0,6.3,8.5,11.5,11.8,14.0,17.0]),
  ('held-context','Held_Correction_Context','8fa53bf00a736e054331c54f0cb37fbe91a602f44d2eacacb3013eba2937fdf9',[4.1,4.4,6.0,8.2,8.5,12.4,12.7,16.4,16.6,20.3]),
 ]:
  source=f'productions/join-me-in-life/full-film/exports/Join_Me_in_Life_{name}_Proof.mp4';assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==sha
  page=browser.new_page(viewport={'width':1000,'height':600},device_scale_factor=1);page.goto(base+'/build/r1-quiet-sequence-review/playback.html')
  page.evaluate('async src=>{v.src=URL.createObjectURL(await(await fetch(src)).blob());v.playbackRate=1;v.muted=false;v.volume=1}',base+'/'+source);page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.started=performance.now();seen=[];events=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('t=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');file=f'{label}-playback-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/file),type='jpeg',quality=90);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'target':target,'before':before,'after':after,'file':file})
  page.wait_for_function('v.ended');t=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-started)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'label':label,'source':source,'sha256':sha,'captures':captures,'telemetry':t});page.close()
 browser.close()
server.shutdown()
report={'browser':version,'chromium_sandbox':True,'scope':'Actual full 1x context playback, supplied audio enabled, preloaded blob, no seeking. Captures/frame inspection is not continuous human viewing or subjective listening.','runs':runs}
(OUT/'playback.json').write_text(json.dumps(report,indent=2)+'\n')
for r in report['runs']:
 r['frame_callback_count']=len(r['telemetry'].pop('frameCallbacks'))
(OUT/'playback-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([{'label':r['label'],**r['telemetry'],'callbacks':r['frame_callback_count']} for r in runs],indent=2))
