"""Capture-free 1x original-song context playback; serialize with shared flock."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import hashlib,json

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
ROOT=FILM.parents[2]
OUT=ROOT/'build/positive-window-sequence-review'
OUT.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'exports/Join_Me_in_Life_Positive_Window_Context_Proof.mp4'
SHA='dfece1dd258e0da59a2d58fe468670a76447a3ab17bdd3ab1d9afd5f436791d2'
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
    page.goto(base+'/build/positive-window-sequence-review/playback.html')
    page.evaluate('async url=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false;v.volume=1}',base+'/'+str(VIDEO.relative_to(ROOT)))
    page.wait_for_function('v.readyState>=2')
    page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
    page.wait_for_function('v.ended',timeout=60000)
    tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
    browser.close()
server.shutdown()
full={'browser':version,'chromium_sandbox':True,'video_sha256':SHA,'capture_free':True,'requested_lock':'build/source-review-playback.lock','telemetry':tele,'scope':'Actual audio-enabled 1x browser execution; visual judgment comes from separately inspected encoded frames. No human-equivalent continuous viewing, subjective listening or phoneme-sync claim.'}
(OUT/'playback-full.json').write_text(json.dumps(full,indent=2)+'\n')
summary={**full,'telemetry':{k:v for k,v in tele.items() if k!='frameCallbacks'},'frame_callback_count':len(tele['frameCallbacks'])}
(OUT/'playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
