from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,json,base64,hashlib
D=Path(__file__).resolve().parent
A=D.parents[1]/'exports'
runs=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
 for shot in ['C01']:
  src=A/'C01_Opening_Diagnostic_v1.mp4'; out=src
  page=b.new_page(viewport={'width':960,'height':600});page.set_content('<video id="v" width="896"></video>')
  page.evaluate('''data=>{v.src='data:video/mp4;base64,'+data;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''',base64.b64encode(out.read_bytes()).decode())
  page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.start=performance.now();return v.play()}')
  for t in [.3,.7,1.1,1.5,1.9,2.3,2.7,3.5,4.4,5.4,6.5,7.7]:
   page.wait_for_function('t=>v.currentTime>=t',arg=t);page.screenshot(path=str(D/f'{shot}-playback-{t}.jpg'))
  page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
  runs.append({'shot':shot,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'playback_derivative_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'telemetry':tele});page.close()
 b.close()
(D/'playback.json').write_text(json.dumps({'browser':b.version,'scope':'Actual 1x audio-enabled browser execution and sampled screenshots; not subjective listening or exact phoneme synchronization assessment. Editor diagnostic exact192-frame keeper, original-song AAC transport. No subjective listening claim.','runs':runs},indent=2)+'\n')
print(json.dumps(runs,indent=2))
