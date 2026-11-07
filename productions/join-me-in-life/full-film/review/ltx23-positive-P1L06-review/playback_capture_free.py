"""Repeat only S034 without screenshots after one capture-run presentation drop.
Coordinate through build/source-review-playback.lock. Keeps original telemetry.
"""
from pathlib import Path
import hashlib,json,fcntl
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
RAW=ROOT/'build'/HERE.name
VIDEO=RAW/'S034-selected.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=json.loads((RAW/'checks.json').read_text());assert sha(VIDEO)==next(s['proxy_sha256'] for s in checks['segments'] if s['shot']=='S034')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
with (ROOT/'build/source-review-playback.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/'+HERE.name+'/playback.html');page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(VIDEO.relative_to(ROOT)));page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');page.wait_for_function('v.ended');tele=page.evaluate("""()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}""");browser.close()
 srv.shutdown()
record={'browser':version,'chromium_sandbox':True,'source_sha256':sha(VIDEO),'scope':'One 1x S034 proxy replay without seeking or screenshots, serialised under shared lock; original capture-run drop retained.','telemetry':tele}
(HERE/'S034-capture-free-playback.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in tele.items() if k!='frameCallbacks'},indent=2))
