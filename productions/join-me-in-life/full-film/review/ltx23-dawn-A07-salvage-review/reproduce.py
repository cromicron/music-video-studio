"""A07 exact first-89-frame salvage review evidence; only writes ignored build/ltx23-dawn-A07-salvage-review.
Dependencies: numpy, Pillow, FFmpeg/ffprobe, Playwright, sandboxed Chromium.
All files are silent. Browser execution is not continuous human perception.
"""
from pathlib import Path
import hashlib,json,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film';ASSET=BASE/'assets/motion/ltx23-dawn-pilots/A07';OUT=ROOT/'build/ltx23-dawn-A07-salvage-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=ASSET/'video-silent.mp4';EXPECTED='1eb004c3e7306da55b479af550481c0fbbb7cf269913e9db16e2ccdc3fc90582'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)==EXPECTED
raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(VIDEO),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,np.uint8).reshape(-1,512,896,3);assert len(frames)==169
np.save(OUT/'frames.npy',frames)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_frames','-show_entries','frame=best_effort_timestamp_time:stream=codec_type,width,height,r_frame_rate,nb_frames','-of','json',str(VIDEO)]))
assert not any(s['codec_type']=='audio' for s in probe['streams'])
times=[float(f['best_effort_timestamp_time']) for f in probe['frames']]
assert len(times)==169 and max(abs(t-i/24) for i,t in enumerate(times))<1e-5
render=json.loads((ASSET/'render.json').read_text());source=BASE/'assets/dawn_together_refined_v2_candidate.png'
assert sha(source)==render['manifest']['start_image_sha256']==render['manifest']['end_image_sha256']
start=np.asarray(Image.open(ASSET/'start-fitted.png').convert('RGB'));end=np.asarray(Image.open(ASSET/'end-fitted.png').convert('RGB'))
assert np.array_equal(start,end)
assert hashlib.sha256(start.tobytes()).hexdigest()==render['input_fitting']['start']['rgb_sha256']
assert len(render['image_guides'])==4
for guide in render['image_guides']:assert guide['rgb_sha256']==render['input_fitting']['start']['rgb_sha256']

def sheet(items,cols,size,name):
 w,h=size;c=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(c)
 for j,(label,im) in enumerate(items):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+5,y+5),label,fill='white');im=ImageOps.contain(im,size);c.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
 c.save(OUT/name,quality=93)
for first in range(0,169,6):
 sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i])) for i in range(first,min(first+6,169))],2,(896,512),f'native-{first+1:03}-{min(first+6,169):03}.jpg')
ids=[0,3,24,48,72,96,112,136,160,168]
sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i])) for i in ids],4,(448,256),'overview.jpg')
sheet([('Original corrected dawn v2',Image.open(source)),('Fitted start/end guide',Image.fromarray(start)),('Actual f001',Image.fromarray(frames[0])),('Actual f169',Image.fromarray(frames[168]))],2,(896,512),'guide-endpoints.jpg')
for i in ids:Image.fromarray(frames[i]).save(OUT/f'frame-{i+1:03}.jpg',quality=95)
sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i])) for i in [86,90,108,113,122,130,144,152,160]],3,(448,256),'crossing-phases.jpg')
sheet([('Fitted guide | native hands',Image.fromarray(start).crop((330,320,615,475)))]+[(f'f{i+1:03} | {i/24:.3f}s | native hands',Image.fromarray(frames[i]).crop((330,320,615,475))) for i in [0,48,84,136,160]],3,(285,155),'hand-phases.jpg')
sheet([(f'f{i+1:03} | {i/24:.3f}s | native faces',Image.fromarray(frames[i]).crop((250,80,550,270))) for i in [0,24,48,84,144,160]],3,(300,190),'face-phases.jpg')
sheet([(f'f{i+1:03} | zero index {i} | {i/24:.6f}s',Image.fromarray(frames[i])) for i in [86,87,88,89,90,91]],2,(896,512),'native-boundaries.jpg')
sheet([(f'f{i+1:03} | index {i} | left edge',Image.fromarray(frames[i]).crop((0,0,160,512))) for i in range(84,92)],8,(160,512),'entry-boundaries-left.jpg')
sheet([(f'f{i+1:03} | {i/24:.6f}s',Image.fromarray(frames[i]).crop((190,70,650,475))) for i in [0,3,12,24,48,72,84,88]],4,(460,405),'early-motion-phases.jpg')
segments=[]
for key,lo,hi in [('S053',0,89)]:
 path=OUT/f'{key}-selected.mp4'
 subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(VIDEO),'-vf',f'trim=start_frame={lo}:end_frame={hi},setpts=N/(24*TB)','-an','-r','24','-fps_mode','cfr','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(path)],check=True)
 segments.append({'shot':key,'frames_zero_based_end_exclusive':[lo,hi],'source_seconds':[lo/24,hi/24],'duration_seconds':(hi-lo)/24,'proxy_sha256':sha(path)})
checks={'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [VIDEO,ASSET/'render.json',ASSET/'start-fitted.png',ASSET/'end-fitted.png',source]},'frames':169,'fps':24,'dimensions':[896,512],'duration_seconds':169/24,'audio_streams':0,'guide_pixels_identical':True,'guide_rgb_sha256':hashlib.sha256(start.tobytes()).hexdigest(),'four_guide_records_both_stages_verified':True,'source_native_dimensions':list(Image.open(source).size),'timestamps':times,'segments':segments,'guide_scope':'Source hashes, fitted pixels and render records verified; do not establish adherence or motion quality.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
proxy=OUT/'S053-selected.mp4'
selected_raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(proxy),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
selected=np.frombuffer(selected_raw,np.uint8).reshape(-1,512,896,3);assert len(selected)==89
mae=np.abs(selected.astype(np.int16)-frames[:89].astype(np.int16)).mean(axis=(1,2,3))
selected_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(proxy)]))
selected_times=[float(f['best_effort_timestamp_time']) for f in selected_probe['frames']]
assert len(selected_times)==89 and max(abs(t-i/24) for i,t in enumerate(selected_times))<1e-5
trim_validation={'source_sha256':sha(VIDEO),'review_proxy_sha256':sha(proxy),'source_frames_zero_based_end_exclusive':[0,89],'frame_count':len(selected),'fps':24,'duration_seconds':89/24,'timestamps':selected_times,'mae_against_corresponding_original_frames':mae.tolist(),'mae_mean':float(mae.mean()),'mae_max':float(mae.max()),'first_source_rgb_sha256':hashlib.sha256(frames[0].tobytes()).hexdigest(),'last_included_source_rgb_sha256':hashlib.sha256(frames[88].tobytes()).hexdigest(),'first_excluded_source_rgb_sha256':hashlib.sha256(frames[89].tobytes()).hexdigest(),'scope':'Lossy encode correspondence and exact frame range, not independent anatomy or movement acceptance.'}
(OUT/'trim-verification.json').write_text(json.dumps(trim_validation,indent=2)+'\n')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:672px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for key,media,targets in [('S053',OUT/'S053-selected.mp4',[.08,.5,1,1.5,2,2.5,3,3.55])]:
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/ltx23-dawn-A07-salvage-review/playback.html');page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(media.relative_to(ROOT)));page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'playback-{key}-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=92);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'requested':target,'before':before,'after':after,'file':name})
  page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'key':key,'source_sha256':sha(media),'captures':captures,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/'playback.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Silent clips, actual 1× browser execution and captures; no continuous human perception or listening claim.','runs':runs},indent=2)+'\n')
for run in runs:
 for b in range(0,len(run['captures']),4):
  caps=run['captures'][b:b+4];sheet([(f'{run["key"]} request {c["requested"]:.2f}s | actual {c["before"]["time"]:.3f}..{c["after"]["time"]:.3f}s',Image.open(OUT/c['file'])) for c in caps],2,(672,384),f'captured-{run["key"]}-{b//4+1}.jpg')
print(json.dumps([{'key':r['key'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs],indent=2))
