"""Actual 1x unmuted playback with telemetry, without subjective listening claims."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import hashlib,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').exists());OUT=ROOT/'build/dawn-early-company-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
FILES=[('shot','productions/join-me-in-life/full-film/exports/Join_Me_in_Life_Dawn_Early_Company_Proof.mp4','568f194d3e2a4576262730502647748a1845098e917e84ee71fdffe665b65deb'),('context','productions/join-me-in-life/full-film/exports/Join_Me_in_Life_Dawn_Early_Company_Context_Proof.mp4','f69402b57c8fd426debf41b9d19a74508562dfe863e4204e6e49f06f78f9e2f3')]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
html='''<style>body{margin:0;background:#171717}video{display:block;width:720px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''';(OUT/'playback.html').write_text(html);runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for label,rel,h in FILES:
  assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
  for captured in ([False,True] if label=='context' else [True]):
   page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/dawn-early-company-sequence-review/playback.html');page.evaluate('async url=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false;v.volume=1;window.ac=new AudioContext();let s=ac.createMediaElementSource(v);window.an=ac.createAnalyser();an.fftSize=2048;s.connect(an);an.connect(ac.destination);window.rms=[];setInterval(()=>{let b=new Float32Array(an.fftSize);an.getFloatTimeDomainData(b);rms.push(Math.sqrt(b.reduce((a,x)=>a+x*x,0)/b.length))},100)}',base+'/'+rel);page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];ac.resume();return v.play()}');samples=[]
   targets=([.3,1.5,2.8,3.5] if label=='shot' else [2.7,3.9,5.6,7.2,7.7,10.0,13.0]) if captured else []
   for target in targets:
    page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'{label}-playback-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=90);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');samples.append({'requested':target,'before':before,'after':after,'file':name})
   page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen,audioContext:ac.state,audioRmsMaximum:Math.max(...rms),nonzeroAudioSamples:rms.filter(x=>x>0.000001).length}}''');runs.append({'label':label+('-captured' if captured else '-uninterrupted'),'source_sha256':h,'samples':samples,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/'playback.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Actual 1x unmuted execution, nonzero audio analyzer signal and inspected captures; not subjective listening or continuous human-equivalent perception.','runs':runs},indent=2)+'\n');print(json.dumps({'browser':version,'runs':[{'label':r['label'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs]},indent=2))
