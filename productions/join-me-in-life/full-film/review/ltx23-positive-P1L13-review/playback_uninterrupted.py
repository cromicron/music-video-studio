"""P1L13 independent review evidence; only writes ignored build/ltx23-positive-P1L13-review.
Run after reproduce.py; needs its selected proxy. Dependencies: Playwright, sandboxed Chromium.
Run under flock build/source-review-playback.lock to avoid concurrent browser-load interference.
All files are silent. Browser execution is not continuous human perception.
"""
from pathlib import Path
import hashlib,json
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film';ASSET=BASE/'assets/motion/ltx23-positive-continuation/P1/P1L13';OUT=ROOT/'build/ltx23-positive-P1L13-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=ASSET/'video-silent.mp4';EXPECTED='f847a682b3489b18ac06ff4f3c3dffe1c3a614005b68efe360ff3840049230da'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)==EXPECTED
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:672px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for key,media,targets in [('raw',VIDEO,[]),('S056',OUT/'S056-selected.mp4',[])]:
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/ltx23-positive-P1L13-review/playback.html');page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(media.relative_to(ROOT)));page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'playback-{key}-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=92);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'requested':target,'before':before,'after':after,'file':name})
  page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'key':key,'source_sha256':sha(media),'captures':captures,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/'playback-uninterrupted.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Silent clips, actual capture-free 1× browser execution; no continuous human perception or listening claim.','runs':runs},indent=2)+'\n')
print(json.dumps([{'key':r['key'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs],indent=2))
