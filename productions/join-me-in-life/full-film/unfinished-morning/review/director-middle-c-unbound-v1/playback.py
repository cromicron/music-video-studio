from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,json,base64,hashlib
D=Path(__file__).resolve().parent
A=D.parents[1]/'exports'
import http.server,threading
server=http.server.ThreadingHTTPServer(('127.0.0.1',8883),http.server.SimpleHTTPRequestHandler)
threading.Thread(target=server.serve_forever,daemon=True).start()
runs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,ignore_default_args=['--mute-audio'],args=['--enable-automation','--autoplay-policy=no-user-gesture-required'])
 launch_args=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')['arguments']
 (D/'launch-args.json').write_text(json.dumps({'mute_flag_present':'--mute-audio' in launch_args,'args':launch_args},indent=2))
 for shot in ['C20-C26']:
  src=A/'C20_C26_Middle_C_Unbound_Diagnostic_v1.mp4'; out=src
  page=b.new_page(viewport={'width':960,'height':600});page.goto('http://127.0.0.1:8883/');page.set_content('<video id="v" width="896"></video>')
  page.evaluate('''data=>{v.src=data;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''','http://127.0.0.1:8883/'+str(out.relative_to(Path.cwd())))
  page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.start=performance.now();return v.play()}')
  for t in [0.2, 3, 6, 8, 8.3, 10, 12, 14.3, 14.6, 16, 18, 20.2, 20.5, 22, 24, 26, 27.2, 27.5, 29, 31, 33, 34.2, 34.5, 36, 38, 40.4, 40.7, 42, 44, 45.8]:
   page.wait_for_function('t=>v.currentTime>=t',arg=t);page.screenshot(path=str(D/f'{shot}-playback-{t}.jpg'))
  page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
  runs.append({'shot':shot,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'playback_derivative_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'telemetry':tele});page.close()
 b.close()
(D/'playback.json').write_text(json.dumps({'browser':b.version,'scope':'Actual 1x audio-enabled browser execution and sampled screenshots; not subjective listening or exact phoneme synchronization assessment. UNBOUND middle sequence diagnostic, original-song AAC transport. No subjective listening claim.','runs':runs},indent=2)+'\n')
print(json.dumps(runs,indent=2))
