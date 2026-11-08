#!/usr/bin/env python3
"""Actual joined story excerpts, complete1x original-song playback; not full film."""
import base64,hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
CONFIG=[('recognition','Recognition_C26_C32.mp4',766,[130,258,391,472,584,667]),('ending','Private_Ending_C37_O04.mp4',444,[64,254])]
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def main():
 out=HERE/'playback-v1.json';assert not out.exists();runs=[]
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--enable-automation'],ignore_default_args=['--mute-audio'])
  launch=b.new_browser_cdp_session().send('Browser.getBrowserCommandLine');assert '--mute-audio' not in launch['arguments']
  for name,file,frames,joins in CONFIG:
   src=ROOT/'build/performance-cut-story-context-v1'/file;target=HERE/name;target.mkdir(exist_ok=False)
   page=b.new_page(viewport={'width':960,'height':540});page.set_content('<body style="margin:0;background:#000"><video id="v" width="960" height="540"></video></body>')
   page.evaluate('''d=>{v.src='data:video/mp4;base64,'+d;v.muted=false;v.volume=1;v.playbackRate=1;v.controls=false;window.events=[];['waiting','stalled','error','ended'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));}''',base64.b64encode(src.read_bytes()).decode())
   page.wait_for_function('v.readyState>=4',timeout=60000);page.evaluate('()=>{window.started=performance.now();return v.play()}')
   times=sorted(set([.2,frames/24-.12]+[x/24-.09 for x in joins]+[x/24+.12 for x in joins]+([11.5,15.8,20.8,25.6] if name=='recognition' else [13,15.6,17.6])))
   captures=[]
   for i,t in enumerate(times):
    page.wait_for_function('t=>v.currentTime>=t',arg=t,timeout=20000);fn=target/f'playback-{i:02d}.jpg';page.screenshot(path=str(fn),quality=90);captures.append({'target_seconds':t,'file':str(fn.relative_to(ROOT)),'sha256':sha(fn)})
   page.wait_for_function('v.ended',timeout=20000)
   telemetry=page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,width:v.videoWidth,height:v.videoHeight,wallSeconds:(performance.now()-started)/1000,quality:(q=>({total:q.totalVideoFrames,dropped:q.droppedVideoFrames,corrupted:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality()),events})''')
   assert telemetry['ended'] and telemetry['error'] is None and telemetry['rate']==1 and not telemetry['muted'] and telemetry['volume']==1
   assert telemetry['quality']['corrupted']==0 and not any(e['event'] in ['waiting','stalled','error'] for e in telemetry['events'])
   runs.append({'name':name,'file':str(src.relative_to(ROOT)),'sha256':sha(src),'expected_picture_frames':frames,'local_joins':joins,'telemetry':telemetry,'captures':captures});page.close()
  version=b.version;b.close()
 out.write_text(json.dumps({'schema':'jml-story-context-actual-playback/v1','scope':'Two actual joined excerpts, not complete-film acceptance','browser':version,'actual_launch':launch,'runs':runs,'limits':'Instrumented original-song placement/unmuted browser1x is not subjective human listening or exact phoneme assessment.'},indent=2)+'\n');print(json.dumps({'runs':2,'drops':[r['telemetry']['quality']['dropped'] for r in runs]}))
if __name__=='__main__':main()
