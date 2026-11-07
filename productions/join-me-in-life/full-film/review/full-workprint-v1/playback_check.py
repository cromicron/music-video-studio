"""Actual 1x local browser playback; telemetry is not subjective listening."""
from pathlib import Path
import functools, hashlib, json, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
VIDEO=FILM/'exports/Join_Me_in_Life_Full_Hybrid_Workprint_v1.mp4'
EXPECTED='f5f43c7adfae9a7820c873a69c86564ad0123b2eba86e353c824b4b764dbd5fc'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==EXPECTED
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(SimpleHTTPRequestHandler,directory=str(FILM)))
threading.Thread(target=server.serve_forever,daemon=True).start()
captures=[]
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        version=browser.version
        page=browser.new_page(viewport={'width':960,'height':540},device_scale_factor=1)
        page.goto(f'http://127.0.0.1:{server.server_port}/exports/{VIDEO.name}')
        page.wait_for_function('document.querySelector("video").readyState>=3')
        page.evaluate('''()=>{
          const v=document.querySelector('video'); window.v=v;
          document.body.style='margin:0;background:black';
          v.style='position:absolute;left:0;top:0;width:960px;height:540px';
          v.controls=false;v.loop=false;v.preload='auto';v.muted=false;v.volume=1;
          v.currentTime=0;v.playbackRate=1;window.events=[];window.callbacks=[];
          for (const name of ['play','playing','waiting','stalled','error','ended'])
            v.addEventListener(name,()=>events.push({event:name,time:v.currentTime,wall:performance.now(),error:v.error?.code??null}));
          function callback(now,m){callbacks.push({time:m.mediaTime,frames:m.presentedFrames});if(!v.ended)v.requestVideoFrameCallback(callback)}
          v.requestVideoFrameCallback(callback);v.play();
        }''')
        wall=time.monotonic()
        for target in [3.0,40.0,75.0,110.0,140.0,175.0,210.0,240.0,275.0]:
            page.wait_for_function('(t)=>v.currentTime>=t',arg=target,timeout=50000)
            before=page.evaluate('v.currentTime')
            file=f'playback-{target:.1f}s.jpg'
            page.locator('video').screenshot(path=str(HERE/file),type='jpeg',quality=87)
            after=page.evaluate('v.currentTime')
            captures.append({'file':file,'requested_time':target,'capture_time_bracket':[before,after]})
            print(f'Playback reached {after:.3f}s', flush=True)
        page.wait_for_function('v.ended || v.error',timeout=50000)
        result=page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,
           ended:v.ended,rate:v.playbackRate,muted:v.muted,volume:v.volume,
           error:v.error?.code??null,totalFrames:v.getVideoPlaybackQuality().totalVideoFrames,
           droppedFrames:v.getVideoPlaybackQuality().droppedVideoFrames,
           corruptedFrames:v.getVideoPlaybackQuality().corruptedVideoFrames,
           elementBounds:{width:v.getBoundingClientRect().width,height:v.getBoundingClientRect().height},
           events,callbacks})''')
        result.update(wall_seconds=time.monotonic()-wall,browser=version,sha256=EXPECTED,captures=captures,
            method='Local Chromium 1x playback with audio enabled; captured 960x540 player stills. No human-equivalent continuous audiovisual viewing or subjective listening claimed.')
        browser.close()
finally:
    server.shutdown()
(HERE/'playback.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='callbacks'},indent=2))
