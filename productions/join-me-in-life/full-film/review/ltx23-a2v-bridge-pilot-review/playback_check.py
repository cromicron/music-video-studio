"""Repeat local 1x playback telemetry and captured ordinary-size playback.
Requires Playwright Python and /usr/bin/chromium. No provider calls, credentials,
external site or security bypass. Outputs remain under ignored root build/.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json,time,subprocess
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/ltx23-a2v-bridge-pilot-review'; OUT.mkdir(parents=True,exist_ok=True)
MEDIA='productions/join-me-in-life/full-film/assets/motion/ltx23-a2v-bridge-pilot/review-original-audio.mp4'
CANDIDATE='build/ltx23-a2v-bridge-pilot-review/proposed-interval.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/MEDIA.replace('review-original-audio.mp4','video-silent.mp4')),'-i',str(ROOT/'productions/join-me-in-life/full-film/assets/audio/bridge-a2v-conditioning.wav'),'-map','0:v:0','-map','1:a:0','-vf','trim=start_frame=3:end_frame=84,setpts=N/(24*TB)','-af','atrim=start=0.125:end=3.5,asetpts=PTS-STARTPTS','-r','24','-fps_mode','cfr','-video_track_timescale','24000','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','-y',str(ROOT/CANDIDATE)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,duration','-of','json',str(ROOT/CANDIDATE)]))['streams'][0]
assert int(probe['nb_read_frames'])==81 and abs(float(probe['duration'])-3.375)<1e-6,probe
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start(); base=f'http://127.0.0.1:{server.server_port}'
html='''<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#171717;color:white}video{display:block}</style><video id="v" preload="auto"></video><script>window.framesSeen=[];window.mediaEvents=[];const v=document.getElementById('v');['error','stalled','waiting','playing','ended'].forEach(e=>v.addEventListener(e,()=>mediaEvents.push({event:e,t:v.currentTime,wall:performance.now()})));function callback(now,m){framesSeen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(callback)}v.requestVideoFrameCallback(callback);</script>'''
(OUT/'playback.html').write_text(html); runs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
 version=browser.version
 for label,width,targets,media in [('native-uninterrupted',896,[],MEDIA),('ordinary-captured',672,[.25,.8,1.3,1.85,2.45,3.0,3.55,3.9],MEDIA),('proposed-source-0.125-to-3.5',672,[],CANDIDATE)]:
  page=browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1)
  page.goto(base+'/build/ltx23-a2v-bridge-pilot-review/playback.html')
  page.evaluate('async ([url,width])=>{const blob=await(await fetch(url)).blob();v.src=URL.createObjectURL(blob);v.style.width=width+"px";v.playbackRate=1;v.muted=false;}',[base+'/'+media,width])
  page.wait_for_function('v.readyState>=2'); page.evaluate('()=>{framesSeen=[];mediaEvents=[];window.wallStart=performance.now();return v.play()}')
  captures=[]
  for target in targets:
   page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
   before=page.evaluate('({time:v.currentTime,frame:framesSeen.at(-1)})')
   name=f'playback-ordinary-{target:.2f}.jpg'; page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=91)
   after=page.evaluate('({time:v.currentTime,frame:framesSeen.at(-1)})')
   captures.append({'target_time':target,'before_screenshot':before,'after_screenshot':after,'file':name})
  page.wait_for_function('v.ended',timeout=15000)
  telemetry=page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return {currentTime:v.currentTime,duration:v.duration,ended:v.ended,playbackRate:v.playbackRate,muted:v.muted,volume:v.volume,error:v.error,wallSeconds:(performance.now()-wallStart)/1000,videoWidth:v.videoWidth,videoHeight:v.videoHeight,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,quality:{totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames},events:mediaEvents,frameCallbacks:framesSeen}}''')
  runs.append({'label':label,'media':media,'captures':captures,'telemetry':telemetry}); page.close()
 browser.close()
server.shutdown()
evidence={'browser':version,'chromium_sandbox':True,'preloaded_blob':True,'source':MEDIA,'proposed_interval':{'source_start':0.125,'source_end_exclusive':3.5,'first_frame_1based':4,'last_frame_1based':84,'frames':81,'proxy_audio':'AAC from original conditioning WAV, trimmed0.125–3.5s; no subjective listening claimed','proxy_picture':'81 original silent-video frames at native24fps; explicit CFR review encoding','proxy_probe':probe},'scope':'Actual local browser playback and screenshots; no subjective listening, continuous human-equivalent perception or phoneme verification claimed. Captured run may drop frames; uninterrupted run measures cadence separately.','runs':runs}
(OUT/'playback.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'browser':version,'runs':[{'label':r['label'],**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'},'frame_callbacks':len(r['telemetry']['frameCallbacks'])} for r in runs]},indent=2))
