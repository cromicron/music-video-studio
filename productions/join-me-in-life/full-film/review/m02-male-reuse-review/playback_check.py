"""Repeat local 1x browser checks; writes fresh telemetry, not the archived verdict.
Requires ffmpeg, Playwright for Python, and /usr/bin/chromium.
Media bytes are preloaded into a browser Blob to isolate cadence from HTTP buffering.
Run from any directory; generated proxy/snapshots stay under root build/.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json, subprocess
root=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
out=root/'build/m02-male-reuse-review'
out.mkdir(parents=True, exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
Thread(target=srv.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{srv.server_port}'
html='''<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#171717;color:white;font:16px sans-serif}video{display:block}p{margin:8px}</style><video id="v" preload="auto"></video><p id="caption"></p><script>window.framesSeen=[]; window.mediaEvents=[]; const v=document.getElementById('v'); ['error','stalled','waiting','playing','ended'].forEach(e=>v.addEventListener(e,()=>mediaEvents.push({event:e,t:v.currentTime,wall:performance.now()})));function callback(now,m){framesSeen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(callback)}v.requestVideoFrameCallback(callback);</script>'''
(out/'playback.html').write_text(html)
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for label,src,width,start,end in [
  ('m02-male-960','productions/join-me-in-life/full-film/assets/motion/m02-male-reuse-candidate/M02_Male_0-2s_16x9.mp4',960,0,None),
]:
  page=browser.new_page(viewport={'width':1040,'height':810},device_scale_factor=1)
  page.goto(base+'/build/m02-male-reuse-review/playback.html')
  page.evaluate('async ([src,w])=>{const data=await (await fetch(src)).blob();v.src=URL.createObjectURL(data);v.style.width=w+"px";v.playbackRate=1;v.muted=false;}',[base+'/'+src,width])
  page.wait_for_function('v.readyState>=2')
  if start:
   page.evaluate('(t)=>v.currentTime=t',start)
   page.wait_for_function('!v.seeking')
  page.evaluate('(label)=>caption.textContent=label+" | 1x / 24 fps source"',label)
  page.evaluate('()=>{window.framesSeen=[];window.mediaEvents=[];window.wallStart=performance.now();v.play()}')
  samples=[]
  if label=='m02-male-960':
   for target in [0.05,0.35,0.75,1.2,1.65,1.9]:
    page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
    seen=page.evaluate('({time:v.currentTime,frame:framesSeen.at(-1)})')
    path=out/f'playback-sequence-{target:.2f}.jpg'
    page.locator('video').screenshot(path=str(path),type='jpeg',quality=88)
    samples.append({'target':target,'beforeScreenshot':seen,'file':path.name})
  if end:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=end)
   page.evaluate('v.pause()')
  else:page.wait_for_function('v.ended')
  telemetry=page.evaluate('''()=>({currentTime:v.currentTime,duration:v.duration,ended:v.ended,paused:v.paused,playbackRate:v.playbackRate,muted:v.muted,error:v.error,wallSeconds:(performance.now()-wallStart)/1000,videoWidth:v.videoWidth,videoHeight:v.videoHeight,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,quality:v.getVideoPlaybackQuality().toJSON?v.getVideoPlaybackQuality().toJSON():{totalVideoFrames:v.getVideoPlaybackQuality().totalVideoFrames,droppedVideoFrames:v.getVideoPlaybackQuality().droppedVideoFrames,corruptedVideoFrames:v.getVideoPlaybackQuality().corruptedVideoFrames},events:mediaEvents,frameCallbacks:framesSeen})''')
  runs.append({'label':label,'src':src,'requestedStart':start,'requestedEnd':end,'samples':samples,'telemetry':telemetry})
  (out/'playback-in-progress.json').write_text(json.dumps(runs,indent=2)+'\n')
  page.close()
 version=browser.version
 browser.close()
srv.shutdown()
(out/'playback.json').write_text(json.dumps({'browser':version,'preloadedBlob':True,'scope':'Browser execution and captured frames only; no human-equivalent continuous viewing or subjective listening claimed. Derived source has no audio stream; no subjective listening is claimed.','runs':runs},indent=2)+'\n')
print(json.dumps({'browser':version,'runs':[{**{k:v for k,v in r.items() if k not in ['telemetry','samples']},'telemetry':{k:v for k,v in r['telemetry'].items() if k not in ['frameCallbacks']},'callbacks':len(r['telemetry']['frameCallbacks'])} for r in runs]},indent=2))
