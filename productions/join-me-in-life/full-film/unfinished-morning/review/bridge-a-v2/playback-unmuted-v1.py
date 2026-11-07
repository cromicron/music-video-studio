from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,json,base64,hashlib
D=Path(__file__).resolve().parent
A=D.parents[1]/'exports'
runs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--enable-automation'],ignore_default_args=['--mute-audio'])
 launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')
 assert '--mute-audio' not in launch['arguments']
 for shot,frames in [('C26',130),('C27',128),('C28',133),('C33',198),('C34',190)]:
  src=A/(shot+'_Bridge_Diagnostic_v1.mp4');out=src
  page=b.new_page(viewport={'width':960,'height':600});page.set_content('<video id="v" width="896"></video>')
  page.evaluate('''data=>{v.src='data:video/mp4;base64,'+data;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''',base64.b64encode(out.read_bytes()).decode())
  page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.start=performance.now();return v.play()}')
  for t in [.05,.25,.6,1,1.8,2.6,3.4,4.2,frames/24-.15]:
   page.wait_for_function('t=>v.currentTime>=t',arg=t);page.screenshot(path=str(D/f'{shot}-unmuted-insertion-playback-{t}.jpg'))
  page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
  runs.append({'shot':shot,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'playback_derivative_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'telemetry':tele});page.close()
 b.close()
(D/'playback-unmuted-v1.json').write_text(json.dumps({'browser':b.version,'actual_browser_command_line':launch,'ignored_default_args':['--mute-audio'],'scope':'Actual1x original-song diagnostic execution with browser mute default removed and command line inspected. DOM volume1/mutedfalse. This does not establish physical sound-device output or subjective hearing/phoneme sync. Exact bridge diagnostic keeper, browser launch verified.','runs':runs},indent=2)+'\n')
print(json.dumps(runs,indent=2))
