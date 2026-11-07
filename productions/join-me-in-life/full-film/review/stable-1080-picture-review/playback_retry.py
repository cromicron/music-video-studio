"""Actual unseeked 1x playback of the 15 frozen silent cached shots, supplied audio enabled.
Writes ignored build/stable-1080-picture-review, not production data.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib, json
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/stable-1080-picture-review';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:1920px;height:1080px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.seen=[];window.events=[];['playing','ended','waiting','stalled','error'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 inventory_path=Path(__file__).resolve().parent/'cache-inventory.json'
 if not inventory_path.exists():inventory_path=ROOT/'build/final-stable-shot-cache-prep.json'
 inventory=json.loads(inventory_path.read_text())
 selected={'S001','S003','S011','S046','S053'}
 for shot in inventory['shots']:
  if shot['id'] not in selected: continue
  label=shot['id'];source=shot['path'];sha=shot['sha256'];duration=shot['frames']/24
  targets=[]
  assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==sha
  page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1);page.goto(base+'/build/stable-1080-picture-review/playback.html')
  page.evaluate('async src=>{v.src=URL.createObjectURL(await(await fetch(src)).blob());v.playbackRate=1;v.muted=true;v.volume=0}',base+'/'+source);page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.started=performance.now();seen=[];events=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('t=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');file=f'{label}-playback-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/file),type='jpeg',quality=90);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'target':target,'before':before,'after':after,'file':file})
  page.wait_for_function('v.ended');t=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-started)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'label':label,'source':source,'sha256':sha,'captures':captures,'telemetry':t});page.close();print(label,'played',flush=True)
 browser.close()
server.shutdown()
report={'browser':version,'chromium_sandbox':True,'scope':'Actual 1x playback of five affected silent cached shots without screenshot capture overhead, preloaded blobs, no seeking. Not full-film playback or music listening; no audio tracks exist.','runs':runs}
(OUT/'playback-retry.json').write_text(json.dumps(report,indent=2)+'\n')
for r in report['runs']:
 r['frame_callback_count']=len(r['telemetry'].pop('frameCallbacks'))
(OUT/'playback-retry-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps([{'label':r['label'],**r['telemetry'],'callbacks':r['frame_callback_count']} for r in runs],indent=2))
