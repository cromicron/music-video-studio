from pathlib import Path
import json,time,hashlib,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
p=Path(__file__).resolve().parent
video=p/'../../assets/motion/ltx13b-summer-pilot/video.mp4'
(p/'playback.html').write_text('<!doctype html><meta charset="utf-8"><video id="v" width="864" height="480" preload="auto" src="../../assets/motion/ltx13b-summer-pilot/video.mp4"></video>')
handler=functools.partial(SimpleHTTPRequestHandler,directory=str(p.parents[1]))
server=ThreadingHTTPServer(("127.0.0.1",0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
runs=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for rate in [1,.5]:
  page=browser.new_page(viewport={'width':900,'height':540});page.goto(f'http://127.0.0.1:{server.server_port}/review/ltx13b-summer-independent/playback.html');page.wait_for_function('v.readyState>=3')
  page.evaluate('''rate=>{window.e=[];for(const k of ['play','playing','waiting','stalled','error','ended'])v.addEventListener(k,()=>e.push({event:k,time:v.currentTime,wall:performance.now(),error:v.error?.code??null}));v.playbackRate=rate;v.muted=false;v.play();}''',rate)
  start=time.monotonic();page.wait_for_function('v.ended || v.error',timeout=30000)
  r=page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,ended:v.ended,playbackRate:v.playbackRate,muted:v.muted,error:v.error?.code??null,totalVideoFrames:v.getVideoPlaybackQuality().totalVideoFrames,droppedVideoFrames:v.getVideoPlaybackQuality().droppedVideoFrames,events:e})''');r['wall_seconds']=time.monotonic()-start;runs.append(r);page.close()
 browser.close()
(p/'playback-telemetry.json').write_text(json.dumps({'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'method':'Headless local Chromium at1x and0.5x. Technical cadence telemetry only, not subjective real-time viewing/listening. Source has no audio. Visual findings use separately inspected chronological frames and native crops.','runs':runs},indent=2)+'\n');print(json.dumps(runs))

server.shutdown()
