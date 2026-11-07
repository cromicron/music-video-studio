"""Actual local 1x context playback; no provider/account access or source changes."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import hashlib,json
HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
ROOT=FILM.parents[2]
OUT=ROOT/'build/walk-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'exports/Join_Me_in_Life_Snow_Walk_Context_Proof.mp4'
SHA='df686da204c4f07f3023680f4f5f24713fe69fdc379e9ea9db37a1ef7119aa7a'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==SHA
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:960px;height:540px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
 version=browser.version
 page=browser.new_page(viewport={'width':960,'height':540},device_scale_factor=1)
 page.goto(base+'/build/walk-sequence-review/playback.html')
 page.evaluate('async url=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false;v.volume=1}',base+'/'+str(VIDEO.relative_to(ROOT)))
 page.wait_for_function('v.readyState>=2')
 page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
 samples=[]
 for target in [4.6,4.9,6.5,8.5,10.16,10.4,14.6,19.0]:
  page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
  before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
  name=f'playback-{target:.2f}.jpg'
  page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=89)
  after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
  samples.append({'requested_seconds':target,'before':before,'after':after,'file':name})
 page.wait_for_function('v.ended')
 tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
 browser.close()
server.shutdown()
full={'browser':version,'chromium_sandbox':True,'video_sha256':SHA,'samples':samples,'telemetry':tele,'scope':'Actual audio-enabled browser execution and captured images; no continuous human-equivalent viewing or subjective listening claim.'}
(OUT/'playback.json').write_text(json.dumps(full,indent=2)+'\n')
summary={**full,'telemetry':{k:v for k,v in tele.items() if k!='frameCallbacks'},'frame_callback_count':len(tele['frameCallbacks'])}
(HERE/'playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for target in [6.5,8.5,14.6]:
 name=f'playback-{target:.2f}.jpg';(HERE/name).write_bytes((OUT/name).read_bytes())
print(json.dumps(summary,indent=2))
