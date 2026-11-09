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
server=http.server.ThreadingHTTPServer(('127.0.0.1',8891),functools.partial(QuietHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
edit_path=root/'productions/join-me-in-life/full-film/performance-cut/edit/edit-v009.json'
edit_sha=hashlib.sha256(edit_path.read_bytes()).hexdigest()
assert edit_sha=='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
times=[('OPEN','check',30),('SUMMER','check',125),('PLEAS','check',214),('END','check',276)]
cap=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,ignore_default_args=['--mute-audio'],args=['--enable-automation','--autoplay-policy=no-user-gesture-required'])
 launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')['arguments'];assert '--mute-audio' not in launch
 (D/'launch-args.json').write_text(json.dumps({'mute_flag_present':False,'args':launch},indent=2)+'\n')
 page=b.new_page(viewport={'width':960,'height':540});page.set_default_timeout(360000);page.goto('http://127.0.0.1:8891/');page.set_content('<style>body{margin:0;background:black}video{width:960px;height:540px;object-fit:contain}</style><video id="v"></video>')
 page.evaluate('''async url=>{const r=await fetch(url);const blob=await r.blob();window.loadedBytes=blob.size;v.src=URL.createObjectURL(blob);v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''','http://127.0.0.1:8891/'+str(src.relative_to(root)))
 page.wait_for_function('v.readyState>=3');loaded_bytes=page.evaluate('window.loadedBytes');assert loaded_bytes==src.stat().st_size;page.evaluate('()=>{window.start=performance.now();return v.play()}')
 for shot,label,t in times:
  page.wait_for_function('t=>v.currentTime>=t',arg=t)
  before=page.evaluate('v.currentTime');name=f'{shot}-{label}-{t:.3f}.jpg';page.screenshot(path=str(D/name),quality=85)
  after=page.evaluate('v.currentTime');cap.append({'shot':shot,'phase':label,'requested_seconds':t,'observed_before':before,'observed_after':after,'image':name})
  print(shot,round(after,3),flush=True)
 page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
 version=b.version;b.close()
server.shutdown()
(D/'playback.json').write_text(json.dumps({'schema':'mercy-in-minor-director-full-master-playback/v1','source':str(src),'source_sha256':a.sha256,'edit':str(edit_path),'edit_sha256':edit_sha,'browser':version,'scope':'Low-overhead 1x exact-candidate execution after complete compressed-input preload; actual unmuted launch verified; only four screenshots. Separate exact-master 45-cut, chronological shot and targeted-native evidence retained. This records complete 1x execution plus four observed captured moments; it does not itself claim continuous human-equivalent visual/hearing perception. No subjective hearing, every-frame inspection or phoneme claim.','telemetry':tele,'captures':cap,'compressed_input_fully_preloaded':True,'loaded_blob_bytes':loaded_bytes,'manual_seeking_or_pause':False,'expected_picture_frames':6667,'default_wait_timeout_ms':360000,'input_bytes':src.stat().st_size},indent=2)+'\n')
print(json.dumps(tele,indent=2))
