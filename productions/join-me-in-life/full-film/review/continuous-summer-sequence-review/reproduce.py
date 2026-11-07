"""Focused independent summer insertion check; outputs only ignored root build/.
Requires FFmpeg/ffprobe, NumPy, Pillow, Playwright and /usr/bin/chromium.
No provider/config/source edits. No listening or phoneme-sync claim.
"""
from pathlib import Path
import hashlib,json,subprocess,math
import numpy as np
from PIL import Image,ImageDraw
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film';OUT=ROOT/'build/continuous-summer-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
SOURCES={
 'proof':('exports/Join_Me_in_Life_Continuous_Summer_Proof.mp4','bac1fdcfe19b9b0c832aa11a60c11773abdb893824d5f60a0875dbd2c33b3f41'),
 'context':('exports/Join_Me_in_Life_Continuous_Summer_Context_Proof.mp4','c58d1d3d8f869167bdd7fe3b4f924b9821ea7dbab63dd19a59ebddeb79d74cac'),
 'source':('assets/motion/ltx23-summer-pilot/video-silent.mp4','f0d49f36d944932141aedacd49233fcd49d89e286f1ba239462d82b01cec1f57')}
for p,h in SOURCES.values():assert hashlib.sha256((BASE/p).read_bytes()).hexdigest()==h
source_review=BASE/'review/ltx23-summer-pilot-review.md';review_sha=hashlib.sha256(source_review.read_bytes()).hexdigest()
assert review_sha=='6ad7686d1a41100e4b10e06b34079a3dd12de35637748fdc0c859b06d3f20f29'
def decode(key,vf=None):
 cmd=['ffmpeg','-v','error','-xerror','-i',str(BASE/SOURCES[key][0]),'-map','0:v:0']
 if vf:cmd+=['-vf',vf]
 raw=subprocess.check_output(cmd+['-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(raw,dtype=np.uint8).reshape(-1,540,960,3)
scale='scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1,format=yuv420p,setparams=colorspace=bt709:range=limited'
proof=decode('proof');context=decode('context');source=decode('source',scale)
assert len(proof)==183 and len(context)==385 and len(source)==145
source_indices=[0]*63+list(range(120))
mae=[float(np.abs(proof[i].astype(np.float32)-source[j].astype(np.float32)).mean()) for i,j in enumerate(source_indices)]
context_mae=[float(np.abs(proof[i].astype(np.float32)-context[i+90].astype(np.float32)).mean()) for i in range(183)]
assert max(mae)<5 and max(context_mae)<3
pts={}
for key,count in [('proof',183),('context',385)]:
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(BASE/SOURCES[key][0])]))
 times=[float(f['best_effort_timestamp_time']) for f in j['frames']]
 assert len(times)==count and max(abs(t-i/24) for i,t in enumerate(times))<1e-5
 pts[key]={'frames':count,'duration_seconds':count/24,'maximum_timestamp_error_seconds':max(abs(t-i/24) for i,t in enumerate(times))}
checks={'source_hashes':SOURCES,'source_review_sha256':review_sha,'dimensions':[960,540],'fps':24,'timing':pts,'source_indices_zero_based':source_indices,'expected_source_scale_filter':scale,'source_frame_mae_mean':float(np.mean(mae)),'source_frame_mae_max':max(mae),'proof_vs_context_mae_max':max(context_mae),'per_frame_source_mae':mae,'interpretation':'Every proof frame compared to expected scaled source: 63 added lead frames then source0..119. Lossy encodes/color conversions prevent pixel identity. Context matching uses frames90..272. This correspondence is not a subjective motion or audio judgement.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
def sheet(items,cols,size,name):
 w,h=size;c=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(c)
 for j,(label,im) in enumerate(items):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+5,y+5),label,fill='white');c.paste(im.resize((w,h)),(x,y+24))
 c.save(OUT/name,quality=91)
sheet([(f'proof f{i+1} | {i/24:.3f}s',Image.fromarray(proof[i])) for i in [0,62,63,64,75,87,99,110,111,123,135,147,159,171,182]],3,(480,270),'wide-sequence.jpg')
sheet([(f'context f{i+1} | master {114.5+i/24:.3f}s',Image.fromarray(context[i])) for i in [88,89,90,91,272,273,274,292,293,384]],2,(480,270),'context-cuts.jpg')
sheet([(f'proof f{i+1} | source f{source_indices[i]+1}',Image.fromarray(proof[i]).crop((135,0,720,540))) for i in [61,62,63,64,109,110,111,112]],4,(585,540),'native-boundaries.jpg')
for first in range(0,112,28):
 sheet([(f'S027 f{i+1} | master {125.875+i/24:.3f}s',Image.fromarray(context[i+273]).crop((285,0,515,240))) for i in range(first,min(first+28,112))],7,(230,240),f'performance-faces-{first+1:03}-{min(first+28,112):03}.jpg')
for i in [0,110,111,135,182]:Image.fromarray(proof[i]).save(OUT/f'proof-{i+1:03}.jpg',quality=94)
for i in [0,89,90,272,273,384]:Image.fromarray(context[i]).save(OUT/f'context-{i+1:03}.jpg',quality=94)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
html='''<style>body{margin:0;background:#171717}video{display:block;width:672px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>'''
(OUT/'playback.html').write_text(html);runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required']);version=browser.version
 for key,targets in [('proof',[.5,2.4,2.9,4.5,4.8,5.6,7.35]),('context',[3.5,3.9,6.2,6.6,8.2,8.6,11.2,11.6,12.3,15.8])]:
  page=browser.new_page(viewport={'width':1000,'height':600},device_scale_factor=1);page.goto(base+'/build/continuous-summer-sequence-review/playback.html')
  page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str((BASE/SOURCES[key][0]).relative_to(ROOT)))
  page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}');captures=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target);before=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');name=f'playback-{key}-{target:.2f}.jpg';page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=91);after=page.evaluate('({time:v.currentTime,frame:seen.at(-1)})');captures.append({'requested':target,'before':before,'after':after,'file':name})
  page.wait_for_function('v.ended');tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''');runs.append({'key':key,'source_sha256':SOURCES[key][1],'captures':captures,'telemetry':tele});page.close()
 browser.close()
srv.shutdown();(OUT/'playback.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Actual1xlocal browser telemetry plus captured screenshots; no subjective listening/continuous human-equivalent perception/phoneme-sync claim.','runs':runs},indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['source_indices_zero_based','per_frame_source_mae']},indent=2));print(json.dumps([{'key':r['key'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs],indent=2))
