"""Review exact S044 wide insertion; rebuild evidence in ignored root build/.
Requires Pillow, NumPy, FFmpeg/ffprobe, Playwright Python and Chromium.
No provider/config edits. Not a subjective listening or phoneme-sync check.
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
BASE=ROOT/'productions/join-me-in-life/full-film'; OUT=ROOT/'build/first-scream-sequence-review'; OUT.mkdir(parents=True,exist_ok=True)
MEDIA=BASE/'exports/Join_Me_in_Life_First_Scream_A2V_Proof.mp4'
SOURCE=BASE/'assets/motion/ltx23-a2v-bridge-pilot/video-silent.mp4'
EXPECTED='62e0300a732c43aee6304cd711f083f6fd197ead38a96bac086fc77f65ed9e90'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest()==EXPECTED
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='9a1420423a8be5e0401e172376e41255e723b2274a87748b5d6857d381959fe5'
def decode(p,vf=None):
 cmd=['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0']
 if vf:cmd+=['-vf',vf]
 raw=subprocess.check_output(cmd+['-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(raw,dtype=np.uint8).reshape(-1,540,960,3)
a=decode(MEDIA)
scale='scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1,format=yuv420p,setparams=colorspace=bt709:range=limited'
r=decode(SOURCE,scale)
assert len(a)==81 and len(r)==97
mae=np.abs(a.astype(np.float32)-r[3:84].astype(np.float32)).mean(axis=(1,2,3))
# All source candidates at small size help detect a reset/incorrect section, while
# expected-frame full-size error measures the actual rescale/crop correspondence.
small=lambda frames:np.stack([np.asarray(Image.fromarray(f).resize((160,90)),dtype=np.float32) for f in frames])
as_,rs=small(a),small(r)
dist=np.abs(as_[:,None]-rs[None,:]).mean(axis=(2,3,4))
nearest=dist.argmin(axis=1)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_streams','-show_format','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(MEDIA)]))
times=[float(f['best_effort_timestamp_time']) for f in probe['frames']]
assert len(times)==81 and max(abs(t-i/24) for i,t in enumerate(times))<1e-5
assert float(mae.max())<5,'Rescaled source correspondence failed'
rows=[{'output_frame_1based':i+1,'expected_source_frame_1based':i+4,'timestamp_seconds':times[i],'expected_source_full_size_mae':float(mae[i]),'nearest_small_source_frame_1based':int(nearest[i]+1)} for i in range(81)]
evidence={'output_sha256':EXPECTED,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'frames':81,'fps':24,'duration_seconds':81/24,'dimensions':[960,540],'source_frames_1based_inclusive':[4,84],'source_interval_seconds':[.125,3.5],'expected_scale_filter':scale,'expected_frame_mae_mean':float(mae.mean()),'expected_frame_mae_max':float(mae.max()),'nearest_small_exact_index_matches':int(np.sum(nearest==np.arange(3,84))),'no_reset_or_hold_evidence':'Every output frame compared against its expected consecutively advancing source frame; lossy compression prevents pixel equality. Near-held source poses can have ambiguous nearest-small-frame matches.','frames_evidence':rows,'audio_scope':'Root delivery manifest reports original master correlation0.9995922026043556 offset0; this focused picture review does not independently repeat waveform analysis or claim listening.'}
(OUT/'checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
ids=[0,12,24,30,36,42,54,66,80]; canvas=Image.new('RGB',(1440,882),'#171717');d=ImageDraw.Draw(canvas)
for j,i in enumerate(ids):
 x,y=(j%3)*480,(j//3)*294;d.text((x+5,y+5),f'proof f{i+1} | source f{i+4} | {i/24:.3f}s',fill='white');canvas.paste(Image.fromarray(a[i]).resize((480,270)),(x,y+24))
canvas.save(OUT/'wide-sequence.jpg',quality=91)
for i in [0,30,80]:Image.fromarray(a[i]).save(OUT/f'proof-{i+1:03}.jpg',quality=94)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
html='''<video id="v" preload="auto" style="width:960px"></video><script>const v=document.getElementById('v');window.events=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));</script>''';(OUT/'playback.html').write_text(html)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
 page=browser.new_page(viewport={'width':1000,'height':600},device_scale_factor=1);page.goto(base+'/build/first-scream-sequence-review/playback.html')
 page.evaluate('async (url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(MEDIA.relative_to(ROOT)))
 page.wait_for_function('v.readyState>=2');page.evaluate('()=>{window.wallStart=performance.now();return v.play()}');page.wait_for_function('v.ended')
 tele=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events}}''')
 (OUT/'playback.json').write_text(json.dumps({'browser':browser.version,'chromium_sandbox':True,'source_sha256':EXPECTED,'scope':'Actual1xlocal browser telemetry; no subjective listening/continuous perception/phoneme-sync claim.','telemetry':tele},indent=2)+'\n');browser.close()
srv.shutdown()
print(json.dumps({k:v for k,v in evidence.items() if k!='frames_evidence'},indent=2));print(json.dumps(tele,indent=2))
