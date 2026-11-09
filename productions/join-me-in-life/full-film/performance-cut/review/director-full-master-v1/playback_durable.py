from pathlib import Path
import argparse,datetime,functools,hashlib,http.server,json,threading,time,traceback
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('sha256');a=ap.parse_args()
D=Path(__file__).resolve().parent/'continuous-pass-v2';D.mkdir(exist_ok=True)
root=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').exists())
src=(root/a.source).resolve();edit=root/'productions/join-me-in-life/full-film/performance-cut/edit/edit-v009.json'
def save(name,value):
 tmp=D/(name+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(D/name)
def progress(state,**extra):save('progress.json',{'state':state,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra})
class QuietHandler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=None;b=None;result=None
try:
 progress('VALIDATING_INPUT')
 assert src.stat().st_size==196409309
 assert hashlib.sha256(src.read_bytes()).hexdigest()==a.sha256
 editsha=hashlib.sha256(edit.read_bytes()).hexdigest();assert editsha=='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
 server=http.server.ThreadingHTTPServer(('127.0.0.1',8891),functools.partial(QuietHandler,directory=str(root)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 captures=[];times=[('OPEN',30),('SUMMER',125),('PLEAS',214),('END',276)];captureindex=0
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,ignore_default_args=['--mute-audio'],args=['--enable-automation','--autoplay-policy=no-user-gesture-required'])
  launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine')['arguments'];assert '--mute-audio' not in launch
  save('launch-args.json',{'mute_flag_present':False,'args':launch})
  page=b.new_page(viewport={'width':960,'height':540});page.set_default_timeout(360000)
  page.goto('http://127.0.0.1:8891/');page.set_content('<style>body{margin:0;background:black}video{width:960px;height:540px;object-fit:contain}</style><video id="v"></video>')
  progress('PRELOADING_COMPLETE_COMPRESSED_INPUT')
  page.evaluate('''async url=>{const r=await fetch(url);if(!r.ok)throw Error('fetch '+r.status);const blob=await r.blob();window.loadedBytes=blob.size;v.src=URL.createObjectURL(blob);v.muted=false;v.volume=1;v.playbackRate=1;window.ev=[];['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>ev.push({event:e,t:v.currentTime})));}''','http://127.0.0.1:8891/'+str(src.relative_to(root)))
  page.wait_for_function('v.readyState>=3');loaded=page.evaluate('window.loadedBytes');assert loaded==src.stat().st_size
  page.evaluate('()=>{window.start=performance.now();return v.play()}');wall=time.monotonic();lastheart=-10
  while True:
   snapshot=page.evaluate('()=>({t:v.currentTime,ended:v.ended,error:v.error,muted:v.muted,volume:v.volume,rate:v.playbackRate,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
   if snapshot['error']:raise RuntimeError('Actual media error '+str(snapshot))
   if snapshot['t']-lastheart>=10:
    progress('PLAYING_1X',**snapshot);lastheart=snapshot['t']
   if captureindex<len(times) and snapshot['t']>=times[captureindex][1]:
    label,t=times[captureindex];name=f'{label}-check-{t:.3f}.jpg';before=page.evaluate('v.currentTime');page.screenshot(path=str(D/name),quality=85);after=page.evaluate('v.currentTime');captures.append({'shot':label,'requested_seconds':t,'observed_before':before,'observed_after':after,'image':name});save('captures.json',captures);captureindex+=1
   if snapshot['ended']:break
   if time.monotonic()-wall>360:raise TimeoutError('Complete playback did not end within360s')
   page.wait_for_timeout(250)
  telemetry=page.evaluate('()=>({duration:v.duration,currentTime:v.currentTime,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-start)/1000,width:v.videoWidth,height:v.videoHeight,quality:{total:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,corrupted:v.getVideoPlaybackQuality().corruptedVideoFrames},events:ev})')
  result={'schema':'mercy-in-minor-director-full-master-playback/v1','source':str(src),'source_sha256':a.sha256,'edit':str(edit),'edit_sha256':editsha,'browser':b.version,'scope':'Complete uninterrupted1x actual master execution after full compressed-input preload, actual unmuted launch verified, four captured moments and lightweight heartbeat. Separate actual-master45cut/chronological/native inspection is required. No subjective hearing, every-frame visual or perfect phoneme claim.','telemetry':telemetry,'captures':captures,'compressed_input_fully_preloaded':True,'loaded_blob_bytes':loaded,'input_bytes':src.stat().st_size,'manual_seeking_or_pause':False,'expected_picture_frames':6667,'actual_launch_mute_flag_present':False,'launch_record':'launch-args.json','earlier_attempt':'../attempt-01-environment-interrupted/interruption.json'}
  save('ended-before-cleanup.json',result)
  b.close();b=None
 server.shutdown();server.server_close();server=None
 result['browser_and_server_closed']=True;save('playback.json',result);progress('COMPLETE_BROWSER_SERVER_CLOSED',**telemetry)
 print(json.dumps(telemetry,indent=2),flush=True)
except BaseException as exc:
 save('error.json',{'state':'INCOMPLETE_NO_PASS','error':str(exc),'type':type(exc).__name__,'traceback':traceback.format_exc()})
 raise
finally:
 if b is not None:
  try:b.close()
  except Exception:pass
 if server is not None:
  server.shutdown();server.server_close()
