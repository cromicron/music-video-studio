from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,hashlib
D=Path(__file__).resolve().parent
A=D.parents[1]/'exports'
runs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--enable-automation'],ignore_default_args=['--mute-audio'])
 launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')
 assert '--mute-audio' not in launch['arguments']
 for shot in ['C21','C22','C23','C24','C25','C20-C26']:
  src=A/(f'{shot}_Middle_C_Diagnostic_v1.mp4' if shot!='C20-C26' else 'C20_C26_Middle_C_Unbound_Diagnostic_v1.mp4')
  page=b.new_page(viewport={'width':960,'height':550});page.set_content('<video id="v" width="896"></video>')
  page.evaluate('''data=>{v.src='data:video/mp4;base64,'+data;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''',base64.b64encode(src.read_bytes()).decode())
  page.wait_for_function('v.readyState>=3');duration=page.evaluate('v.duration');page.evaluate('()=>{window.start=performance.now();return v.play()}')
  times=[.1,1,2,3,4,5,duration-.15] if shot!='C20-C26' else [.2,4,8.05,8.3,11,14.4,14.6,17,20.25,20.5,24,27.25,27.5,31,34.25,34.5,38,40.45,40.7,43,45.8]
  captures=[]
  for t in sorted(set(times)):
   if t>=duration:continue
   page.wait_for_function('t=>v.currentTime>=t',arg=t)
   actual=page.evaluate('v.currentTime');name=f'{shot}-playback-{t:.2f}.jpg';page.screenshot(path=str(D/name));captures.append({'requested':t,'actual':actual,'path':str(D/name)})
  page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
  runs.append({'shot':shot,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'telemetry':tele,'captures':captures});page.close()
  (D/'playback-unmuted-v1.json').write_text(json.dumps({'browser':b.version,'actual_browser_command_line':launch,'ignored_default_args':['--mute-audio'],'scope':'Actual1x original-song diagnostic execution, inspected browser captures. No subjective hearing/physical sound device/phoneme sync/every-frame human watching claimed.','runs':runs},indent=2)+'\n')
 b.close()
print(json.dumps([{'shot':x['shot'],'telemetry':x['telemetry']} for x in runs],indent=2))
