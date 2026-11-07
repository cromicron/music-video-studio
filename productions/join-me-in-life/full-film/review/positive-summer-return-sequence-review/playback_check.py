"""Pinned context, actual unseeked 1x playback with its AAC audio enabled.
Serialize using flock build/source-review-playback.lock. Use --uncaptured for
the capture-free measurement. No listening or whole-film approval is inferred.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import argparse,gzip,hashlib,json
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
OUT=ROOT/'build'/HERE.name;OUT.mkdir(parents=True,exist_ok=True)
SUMMER='summer' in HERE.name
checks=json.loads((HERE/'checks.json').read_text())
VIDEO=ROOT/checks['context_path']
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==checks['context_sha256']
parser=argparse.ArgumentParser();parser.add_argument('--uncaptured',action='store_true');args=parser.parse_args()
prefix='uncaptured' if args.uncaptured else 'captured'
targets=[] if args.uncaptured else ([4.8,5.45,7.8,10.1,10.55,14.9] if SUMMER else [3.8,4.4,6,8,8.35,10.1,11.8,12.3,15.4])
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:960px;height:540px;object-fit:contain}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
    page=browser.new_page(viewport={'width':1000,'height':600},device_scale_factor=1)
    page.goto(base+f'/build/{HERE.name}/playback.html')
    page.evaluate('async url=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false;v.volume=1}',base+'/'+str(VIDEO.relative_to(ROOT)))
    page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
    samples=[]
    for target in targets:
        page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
        before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'playback-{target:.2f}.jpg'
        page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=92)
        after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
        samples.append({'requested':target,'before':before,'after':after,'file':name})
        (HERE/name).write_bytes((OUT/name).read_bytes())
    page.wait_for_function('v.ended')
    telemetry=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,audioDecodedByteCount:v.webkitAudioDecodedByteCount,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
    page.close();browser.close()
srv.shutdown()
full={'browser':version,'chromium_sandbox':True,'source_sha256':checks['context_sha256'],'source':checks['context_path'],'capture_free':args.uncaptured,'scope':'Actual preloaded, unseeked 1x context playback with audio enabled; execution and inspected captures are not subjective hearing or continuous human-equivalent viewing.','samples':samples,'telemetry':telemetry}
text=json.dumps(full,indent=2)+'\n';(OUT/f'{prefix}-playback.json').write_text(text)
with gzip.open(HERE/f'{prefix}-playback.json.gz','wt') as f:f.write(text)
summary={**full,'telemetry':{k:v for k,v in telemetry.items() if k!='frameCallbacks'},'frame_callback_count':len(telemetry['frameCallbacks'])}
(HERE/f'{prefix}-playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
