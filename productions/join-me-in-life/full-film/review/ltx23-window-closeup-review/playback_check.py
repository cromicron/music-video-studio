"""Exercise the exact window close-up source at 1x/960x540; save telemetry to root build/."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json,hashlib
root=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
out=root/'build/ltx23-window-closeup-review';out.mkdir(parents=True,exist_ok=True)
src='productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-window-closeup/video-silent.mp4'
assert hashlib.sha256((root/src).read_bytes()).hexdigest()=='5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
Thread(target=srv.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{srv.server_port}'
html='''<!doctype html><style>body{margin:0;background:#171717}video{display:block;width:960px;height:540px}</style><video id="v" preload="auto"></video><script>window.framesSeen=[];window.mediaEvents=[];const v=document.getElementById('v');['error','stalled','waiting','playing','ended'].forEach(e=>v.addEventListener(e,()=>mediaEvents.push({event:e,t:v.currentTime,wall:performance.now()})));function callback(now,m){framesSeen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(callback)}v.requestVideoFrameCallback(callback);</script>'''
(out/'playback.html').write_text(html)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 page=browser.new_page(viewport={'width':1040,'height':700},device_scale_factor=1)
 page.goto(base+'/build/ltx23-window-closeup-review/playback.html')
 page.evaluate('async src=>{v.src=URL.createObjectURL(await(await fetch(src)).blob());v.playbackRate=1;v.muted=false}',base+'/'+src)
 page.wait_for_function('v.readyState>=2')
 page.evaluate('()=>{window.framesSeen=[];window.mediaEvents=[];window.wallStart=performance.now();v.play()}')
 samples=[]
 for target in [.2,1,2,3,4,5,6.3]:
  page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
  before=page.evaluate('({time:v.currentTime,frame:framesSeen.at(-1)})')
  path=out/f'playback-{target:.2f}.jpg'
  page.locator('video').screenshot(path=str(path),type='jpeg',quality=88)
  samples.append({'target':target,'beforeScreenshot':before,'file':path.name})
 page.wait_for_function('v.ended')
 telemetry=page.evaluate('''()=>({currentTime:v.currentTime,duration:v.duration,ended:v.ended,paused:v.paused,playbackRate:v.playbackRate,muted:v.muted,error:v.error,wallSeconds:(performance.now()-wallStart)/1000,videoWidth:v.videoWidth,videoHeight:v.videoHeight,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,quality:{totalVideoFrames:v.getVideoPlaybackQuality().totalVideoFrames,droppedVideoFrames:v.getVideoPlaybackQuality().droppedVideoFrames,corruptedVideoFrames:v.getVideoPlaybackQuality().corruptedVideoFrames},events:mediaEvents,frameCallbacks:framesSeen})''')
 version=browser.version
 browser.close()
srv.shutdown()
result={'source':src,'browser':version,'preloadedBlob':True,'scope':'Actual browser execution and captured images only; not a claim of human-equivalent continuous visual perception. Source is silent; no subjective listening claimed.','samples':samples,'telemetry':telemetry}
(out/'playback.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in telemetry.items() if k!='frameCallbacks'},indent=2))
