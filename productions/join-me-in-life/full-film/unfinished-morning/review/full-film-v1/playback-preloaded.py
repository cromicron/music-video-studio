from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,sys,time,http.server,threading,functools
D=Path(__file__).resolve().parent
P=D.parents[1]
src=Path(sys.argv[1]).resolve(); expected=sys.argv[2]
assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
edit=json.loads((P/'tools/editor/edit-v015.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(src.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/{src.name}'
checks=[]
for s in edit['shots']:
 start=s['start_frame']/24;end=s['end_frame_exclusive']/24
 checks.extend([(start+.12,s['id']+'-entry'),((start+end)/2,s['id']+'-middle'),(end-.12,s['id']+'-exit')])
checks=[(0.12,'light-start'),(277.5,'light-end')];captures=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--enable-automation'],ignore_default_args=['--mute-audio'])
 launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine');assert '--mute-audio' not in launch['arguments']
 page=b.new_page(viewport={'width':1000,'height':620})
 page.set_content('<body style="margin:0;background:#000"><video id="v" width="960"></video></body>')
 page.evaluate('''url=>{v.src=url;v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''',url)
 page.wait_for_function('v.readyState>=3');page.evaluate('''async()=>{v.pause();const bytes=await fetch(v.src).then(r=>r.blob());v.src=URL.createObjectURL(bytes);v.load()}''');page.wait_for_function('v.readyState>=4');page.evaluate('()=>{window.start=performance.now();return v.play()}')
 for t,label in checks:
  page.wait_for_function('t=>v.currentTime>=t',arg=t,timeout=20000)
  observed=page.evaluate('v.currentTime');f=D/f'playback-preloaded-{label}.jpg';page.screenshot(path=str(f),quality=82)
  captures.append({'requested_seconds':t,'actual_before_screenshot_seconds':observed,'path':str(f)})
  (D/'playback-preloaded-progress.json').write_text(json.dumps({'source_sha256':expected,'last':captures[-1],'completed_captures':len(captures)}))
 page.wait_for_function('v.ended');tele=page.evaluate('()=>({duration:v.duration,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
 version=b.version;b.close()
server.shutdown()
r={'source':str(src),'sha256':expected,'browser':version,'actual_browser_command_line':launch,'ignored_default_args':['--mute-audio'],'telemetry':tele,'captures':captures,'limits':'Actual whole-film1x execution and screenshot evidence. Captures require separate visual inspection. Does not establish subjective hearing, physical speaker output, exact phoneme sync or viewing every native decoded frame. Screenshot observed times are not exact frame indices.'}
f=D/'playback-preloaded-v2.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(tele))
