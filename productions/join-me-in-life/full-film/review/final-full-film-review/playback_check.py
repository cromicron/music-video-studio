"""Full unseeked 1x audio-enabled playback, serialized by the caller's flock."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import gzip,hashlib,json,time

HERE=Path(__file__).resolve().parent;FILM=HERE.parent.parent;ROOT=FILM.parents[2]
OUT=ROOT/'build/final-full-film-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=ROOT/'build/Join_Me_in_Life_Full_Music_Video_QC.mp4'
EXPECTED='ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==EXPECTED
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:1920px;height:1080px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime,wall:performance.now()})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
captures=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
        version=browser.version;page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
        page.goto(base+'/build/final-full-film-review/playback.html')
        page.evaluate('async url=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false;v.volume=1}',base+'/build/'+VIDEO.name)
        page.wait_for_function('v.readyState>=3');page.evaluate('async()=>{window.ac=new AudioContext();window.analyser=ac.createAnalyser();analyser.fftSize=512;let src=ac.createMediaElementSource(v);src.connect(analyser);analyser.connect(ac.destination);await ac.resume();window.wallStart=performance.now();events=[];seen=[];return v.play()}')
        started=time.monotonic()
        for target in [3,16,46,62,92,114.5,123,136.5,150,159,179,198,205,209,213,217.5,221,233,245,263,274.8,276.8]:
            page.wait_for_function('t=>v.currentTime>=t',arg=target,timeout=50000)
            before=page.evaluate('({t:v.currentTime,dropped:v.getVideoPlaybackQuality().droppedVideoFrames})')
            filename=f'playback-{target:06.1f}s.jpg';page.locator('video').screenshot(path=str(OUT/filename),type='jpeg',quality=88,timeout=15000)
            after=page.evaluate('()=>{let a=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(a);return {t:v.currentTime,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,audioContext:ac.state,audioRms:Math.sqrt(a.reduce((s,x)=>s+x*x,0)/a.length)}}')
            captures.append({'file':filename,'target_seconds':target,'before':before,'after':after})
            print(json.dumps({'playback_reached':after['t'],'dropped':after['dropped']}),flush=True)
        page.wait_for_function('v.ended || v.error',timeout=60000)
        tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
        browser.close()
finally:server.shutdown()
result={'video_sha256':EXPECTED,'browser':version,'chromium_sandbox':True,'playback_lock':'build/source-review-playback.lock','unseeked':True,'telemetry':tele,'captures':captures,'scope':'Actual full-length 1x audio-enabled browser playback and selected captures. No human-equivalent continuous audiovisual viewing, subjective listening or phoneme-sync claim.'}
with gzip.open(OUT/'playback-full.json.gz','wt') as f:json.dump(result,f)
summary={**result,'telemetry':{k:v for k,v in tele.items() if k!='frameCallbacks'},'frame_callback_count':len(tele['frameCallbacks'])}
(OUT/'playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2),flush=True)
