"""Actual 1x context playback; fresh captures/telemetry stay under root build/."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json,hashlib
root=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
out=root/'build/quiet-insertion-sequence-review';out.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));Thread(target=srv.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{srv.server_port}'
(out/'playback.html').write_text('''<!doctype html><style>body{margin:0;background:#171717}video{display:block;width:960px;height:540px}</style><video id="v" preload="auto"></video><script>window.framesSeen=[];window.events=[];const v=document.getElementById('v');['error','stalled','waiting','playing','ended'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){framesSeen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb);</script>''')
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for label,name,sha,targets in [('arrival-context','Arrival_Chorus_Context','eede37caeb2f083b7decd6fed8297d3228383ed39162c328c5d97ef721efa698',[4.1,4.4,7.7,10.4,10.7,14.4,14.7,18.5]),('held-context','Held_Contact_Context','f3874cfaf2116ae66f8fec4cf5b65881657d591cfb38772e1ab067da4c317230',[4.1,4.4,6.5,8.2,8.5,12.4,12.7,16.2])]:
  src=f'productions/join-me-in-life/full-film/exports/Join_Me_in_Life_{name}_Proof.mp4'
  assert hashlib.sha256((root/src).read_bytes()).hexdigest()==sha
  page=browser.new_page(viewport={'width':1040,'height':700},device_scale_factor=1);page.goto(base+'/build/quiet-insertion-sequence-review/playback.html')
  page.evaluate('async src=>{v.src=URL.createObjectURL(await(await fetch(src)).blob());v.playbackRate=1;v.muted=false}',base+'/'+src);page.wait_for_function('v.readyState>=2')
  page.evaluate('()=>{framesSeen=[];events=[];window.started=performance.now();v.play()}');samples=[]
  for t in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=t);before=page.evaluate('({time:v.currentTime,frame:framesSeen.at(-1)})')
   name=f'{label}-playback-{t:.2f}.jpg';page.locator('video').screenshot(path=str(out/name),type='jpeg',quality=86);samples.append({'target':t,'beforeScreenshot':before,'file':name})
  page.wait_for_function('v.ended')
  telemetry=page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,ended:v.ended,playbackRate:v.playbackRate,muted:v.muted,error:v.error,wallSeconds:(performance.now()-started)/1000,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,totalFrames:v.getVideoPlaybackQuality().totalVideoFrames,droppedFrames:v.getVideoPlaybackQuality().droppedVideoFrames,corruptedFrames:v.getVideoPlaybackQuality().corruptedVideoFrames,events:events,frameCallbacks:framesSeen})''')
  runs.append({'label':label,'source':src,'sha256':sha,'samples':samples,'telemetry':telemetry});page.close()
 version=browser.version;browser.close()
srv.shutdown()
(out/'playback.json').write_text(json.dumps({'browser':version,'scope':'Actual player execution with captured pictures. No human-equivalent continuous viewing or subjective listening claimed; supplied audio enabled.','preloadedBlob':True,'runs':runs},indent=2)+'\n')
print(json.dumps([{**{'label':r['label']},**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs],indent=2))
