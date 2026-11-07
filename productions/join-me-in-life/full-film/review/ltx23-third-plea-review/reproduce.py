"""Independent S046 review evidence, written only to ignored root build/.
Requires NumPy, Pillow, FFmpeg/ffprobe, Playwright and /usr/bin/chromium.
No provider/source/config changes; no subjective listening or phoneme-sync claim.
"""
from pathlib import Path
import hashlib,json,subprocess,math,wave
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film';ASSET=BASE/'assets/motion/ltx23-performance-pilots/S046';OUT=ROOT/'build/ltx23-third-plea-review';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ASSET/'video-silent.mp4';BROWSER=ASSET/'review-original-audio.mp4';WAV=BASE/'tools/kaggle-performance23/inputs/S046-conditioning.wav';EXPECTED='6efd9acdd5f07a8ae9148de665f169660fcad8c29874b1e0a98416d133b8baa9'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
def decode(path):
 raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(raw,dtype=np.uint8).reshape(-1,512,896,3)
frames=decode(SOURCE);browser_frames=decode(BROWSER);assert len(frames)==89 and np.array_equal(frames,browser_frames)
del browser_frames
with wave.open(str(WAV)) as w:pcm=w.readframes(w.getnframes());audio_format={'samples':w.getnframes(),'sample_rate':w.getframerate(),'channels':w.getnchannels(),'sample_width_bytes':w.getsampwidth()}
review_pcm=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(ASSET/'review-original-audio.mkv'),'-map','0:a:0','-f','s16le','-'])
assert review_pcm==pcm
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(SOURCE)]))
assert not any(s['codec_type']=='audio' for s in probe['streams'])
for i,f in enumerate(frames):Image.fromarray(f).save(OUT/f'frame-{i+1:03}.png')
def sheet(items,cols,size,name):
 w,h=size;c=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(c)
 for j,(label,im) in enumerate(items):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+5,y+5),label,fill='white');im=ImageOps.contain(im,(w,h));c.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
 c.save(OUT/name,quality=92)
for first in range(0,89,6):
 sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i]).crop((85,0,896,512))) for i in range(first,min(first+6,89))],3,(811,512),f'native-{first+1:03}-{min(first+6,89):03}.jpg')
ids=[0,3,12,24,36,48,60,72,80,84,88]
sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i])) for i in ids],3,(448,256),'overview.jpg')
sheet([(f'f{i+1:03} | face/mic',Image.fromarray(frames[i]).crop((130,0,440,310))) for i in ids],4,(310,310),'face-mic-detail.jpg')
sheet([(f'f{i+1:03} | extended hand',Image.fromarray(frames[i]).crop((440,60,896,510))) for i in ids],4,(456,450),'free-hand-detail.jpg')
start=BASE.parent/'art/04_Performance/P03_Bridge_Plea.png';a01=BASE.parent/'art/00_References/A01_Approved_Character_Pair.jpg'
sheet([('P03 original',Image.open(start)),('Actual f004 / proposed start',Image.fromarray(frames[3])),('Actual f085 / proposed end',Image.fromarray(frames[84])),('Actual f089 / raw final',Image.fromarray(frames[88]))],2,(896,512),'endpoints.jpg')
sheet([('A01 male face',Image.open(a01).crop((465,0,650,220))),('P03 face',Image.open(start).crop((340,15,760,405))),*[(f'Actual f{i+1:03}',Image.fromarray(frames[i]).crop((170,10,420,235))) for i in [3,24,48,72,84,88]]],4,(300,300),'identity.jpg')
proxy=OUT/'intended-f004-085.mp4'
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(SOURCE),'-i',str(WAV),'-filter_complex','[0:v]trim=start_frame=3:end_frame=85,setpts=N/(24*TB)[v];[1:a]atrim=start_sample=6000:end_sample=170000,asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-r','24','-fps_mode','cfr','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',str(proxy)],check=True)
assert len(decode(proxy))==82
paths=[SOURCE,BROWSER,ASSET/'review-original-audio.mkv',ASSET/'render.json',ASSET/'input-fitted.png',start,a01,WAV,BASE/'tools/kaggle-performance23/inputs/S046-conditioning.json']
checks={'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'source_frames':89,'dimensions':[896,512],'fps':24,'duration_seconds':89/24,'source_audio_streams':0,'browser_picture_pixel_identical_to_silent_source':True,'mkv_decoded_pcm_exactly_equals_supplied_wav':True,'audio_format':audio_format,'input_pcm_sha256':hashlib.sha256(pcm).hexdigest(),'proposed_selection':{'zero_based_frames_end_exclusive':[3,85],'one_based_frames_inclusive':[4,85],'source_interval_seconds':[3/24,85/24],'duration_seconds':82/24,'master_interval_seconds':[215.83333333333334+3/24,219.375],'proxy_sha256':hashlib.sha256(proxy.read_bytes()).hexdigest(),'proxy_note':'Temporary CFR review proxy preserves 82 source frames and original supplied-audio samples 6000:170000; AAC is lossy, no exact PCM identity is claimed for this proxy.'},'probe':probe,'scope':'Frame/picture/audio identity facts, not anatomy, subjective listening or phoneme-sync acceptance.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
html='''<style>body{margin:0;background:#171717}video{display:block;width:672px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>'''
(OUT/'playback.html').write_text(html);runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for key,media,targets in [('raw',BROWSER,[.2,.7,1.2,1.7,2.2,2.7,3.2,3.55]),('intended',proxy,[.2,.7,1.2,1.7,2.2,2.7,3.2])]:
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1);page.goto(base+'/build/ltx23-third-plea-review/playback.html')
  page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(media.relative_to(ROOT)));page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'playback-{key}-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=91);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'requested':target,'before':before,'after':after,'file':name})
  page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'key':key,'source_sha256':hashlib.sha256(media.read_bytes()).hexdigest(),'captures':captures,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/'playback.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Actual 1× local unmuted browser telemetry plus captured screenshots; no subjective listening/continuous human-equivalent perception/phoneme-sync claim.','runs':runs},indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['hashes','probe']},indent=2));print(json.dumps([{'key':r['key'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs],indent=2))
