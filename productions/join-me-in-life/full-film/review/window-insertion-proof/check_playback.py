from pathlib import Path
import json,time,hashlib,threading,functools,sys
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
p=Path(__file__).resolve().parent
(p/'playback.html').write_text('<!doctype html><video id=video width=960 height=540 preload=auto></video>')
names=['Join_Me_in_Life_Window_Closeup_Proof','Join_Me_in_Life_Window_Closeup_Context_Proof']
server=ThreadingHTTPServer(("127.0.0.1",0),functools.partial(SimpleHTTPRequestHandler,directory=str(p.parents[1])))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for name in names:
  video=p.parents[1]/'exports'/f'{name}.mp4'
  page=browser.new_page(viewport={'width':1000,'height':600})
  page.goto(f'http://127.0.0.1:{server.server_port}/review/window-insertion-proof/playback.html')
  page.evaluate("name=>document.querySelector('video').src='../../exports/'+name+'.mp4'",name)
  page.wait_for_function('document.querySelector("video").readyState>=3')
  page.evaluate("()=>{window.v=document.querySelector('video');window.e=[];for(const k of ['play','playing','waiting','stalled','error','ended'])v.addEventListener(k,()=>e.push({event:k,time:v.currentTime,wall:performance.now(),error:v.error?.code??null}));v.currentTime=0;v.playbackRate=1;v.muted=false;v.play();}")
  start=time.monotonic();page.wait_for_function('v.ended || v.error',timeout=45000)
  result=page.evaluate('()=>({duration:v.duration,currentTime:v.currentTime,ended:v.ended,playbackRate:v.playbackRate,muted:v.muted,error:v.error?.code??null,totalVideoFrames:v.getVideoPlaybackQuality().totalVideoFrames,droppedVideoFrames:v.getVideoPlaybackQuality().droppedVideoFrames,events:e})')
  result.update(name=name,sha256=hashlib.sha256(video.read_bytes()).hexdigest(),wall_seconds=time.monotonic()-start);results.append(result);page.close()
 browser.close()
server.shutdown()
(p/'playback-telemetry.json').write_text(json.dumps({'method':'Headless local Chromium1x unmuted. Technical cadence only, not subjective real-time viewing or listening. Visual findings use inspected chronological frames and crops.','runs':results},indent=2)+'\n')
print(json.dumps(results))
