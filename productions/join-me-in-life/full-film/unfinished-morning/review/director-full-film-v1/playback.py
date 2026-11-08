from pathlib import Path
import argparse, functools, hashlib, http.server, json, threading
from playwright.sync_api import sync_playwright

ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('sha256');a=ap.parse_args()
root=Path.cwd();src=Path(a.source).resolve();D=Path(__file__).resolve().parent
h=hashlib.sha256()
with src.open('rb') as f:
 for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
assert h.hexdigest()==a.sha256,'Source hash mismatch'
class QuietHandler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8884),functools.partial(QuietHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
plan=json.loads((D.parents[1]/'story/shot-plan-v1.json').read_text())
bounds=[(s['id'],s['start_frame'],s['end_frame_exclusive']) for s in plan['shots']]
bounds=[(i,{'C12':2202,'C13':2404}.get(i,s),{'C11':2202,'C12':2404}.get(i,e)) for i,s,e in bounds]
times=[]
for shot,s,e in bounds:
 for label,t in [('start',s/24+.12),('mid',(s+e)/48),('end',e/24-.12)]:times.append((shot,label,t))
cap=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,ignore_default_args=['--mute-audio'],args=['--enable-automation','--autoplay-policy=no-user-gesture-required'])
 launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')['arguments'];assert '--mute-audio' not in launch
 (D/'launch-args.json').write_text(json.dumps({'mute_flag_present':False,'args':launch},indent=2)+'\n')
 page=b.new_page(viewport={'width':960,'height':540});page.goto('http://127.0.0.1:8884/');page.set_content('<style>body{margin:0;background:black}video{width:960px;height:540px;object-fit:contain}</style><video id="v"></video>')
 page.evaluate('''url=>{v.src=url;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''','http://127.0.0.1:8884/'+str(src.relative_to(root)))
 page.wait_for_function('v.readyState>=3');page.evaluate('()=>{window.start=performance.now();return v.play()}')
 for shot,label,t in times:
  page.wait_for_function('t=>v.currentTime>=t',arg=t)
  before=page.evaluate('v.currentTime');name=f'{shot}-{label}-{t:.3f}.jpg';page.screenshot(path=str(D/name),quality=85)
  after=page.evaluate('v.currentTime');cap.append({'shot':shot,'phase':label,'requested_seconds':t,'observed_before':before,'observed_after':after,'image':name})
  if label=='end':print(shot,round(after,3),flush=True)
 page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
 version=b.version;b.close()
server.shutdown()
(D/'playback.json').write_text(json.dumps({'schema':'jml-director-global-playback/v1','source':str(src),'source_sha256':a.sha256,'browser':version,'scope':'Uninterrupted 1x exact-candidate execution with actual unmuted launch; chronological sampled visual inspection required separately. No subjective hearing, every-frame inspection or phoneme claim.','telemetry':tele,'captures':cap},indent=2)+'\n')
print(json.dumps(tele,indent=2))
