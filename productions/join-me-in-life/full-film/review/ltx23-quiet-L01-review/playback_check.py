"""Actual silent 1x browser playback; output only ignored build/."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import argparse,hashlib,json,subprocess
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file());OUT=ROOT/'build/ltx23-quiet-L01-review';OUT.mkdir(parents=True,exist_ok=True)
MEDIA='productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-pilots/L01/video-silent.mp4'
parser=argparse.ArgumentParser();parser.add_argument('--selected',action='store_true');args=parser.parse_args()
assert hashlib.sha256((ROOT/MEDIA).read_bytes()).hexdigest()=='e90f0c8b2ed56367fe04399109dc7a95a030aacc56e158964a46bac610ef743a'
prefix=''
runspec=[('native-uninterrupted',896,[]),('ordinary-captured',672,[.3,.9,1.5,2.1,2.7,3.3,3.9,4.5,5.1,5.8,6.4])]
if args.selected:
 proxy=OUT/'selected-0.125-6.541667.mp4'
 subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(ROOT/MEDIA),'-an','-vf','trim=start_frame=3:end_frame=157,setpts=N/(24*TB)','-r','24','-fps_mode','cfr','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(proxy)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_streams','-of','json',str(proxy)]))['streams'][0]
 assert int(probe['nb_read_frames'])==154 and abs(float(probe['duration'])-154/24)<.000001
 MEDIA=str(proxy.relative_to(ROOT));prefix='selected-';runspec=[('selected-ordinary-uninterrupted',672,[]),('selected-ordinary-captured',672,[.2,.8,1.4,2,2.6,3.2,3.8,4.4,5.2,6.1])]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
html='''<style>body{margin:0;background:#171717}video{display:block}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''';(OUT/'playback.html').write_text(html);runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
 version=browser.version
 for label,width,targets in runspec:
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/ltx23-quiet-L01-review/playback.html');page.evaluate('async([url,width])=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.style.width=width+"px";v.playbackRate=1;v.muted=false}',[base+'/'+MEDIA,width]);page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');samples=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'{prefix}playback-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=90);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');samples.append({'requested':target,'before':before,'after':after,'file':name})
  page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'label':label,'samples':samples,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/(prefix+'playback.json')).write_text(json.dumps({'browser':version,'chromium_sandbox':True,'source_sha256':'e90f0c8b2ed56367fe04399109dc7a95a030aacc56e158964a46bac610ef743a','source_audio_streams':0,'source_interval_seconds':[.125,157/24] if args.selected else [0,161/24],'source_frames_1based':[4,157] if args.selected else [1,161],'played_file':MEDIA,'played_file_sha256':hashlib.sha256((ROOT/MEDIA).read_bytes()).hexdigest(),'scope':'Actual local1x browser execution and captured screenshots; not continuous human-equivalent viewing, subjective listening or phoneme-sync assessment.','runs':runs},indent=2)+'\n')
print(json.dumps({'browser':version,'runs':[{'label':r['label'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs]},indent=2))
