"""Actual native-size silent 1x browser playback, adapted from R1L04 review.
Use --uncaptured for capture-free runs; serialize those using the shared shell
flock build/source-review-playback.lock. Run reproduce.py first.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import argparse, gzip, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'studio.json').is_file())
OUT = ROOT/'build'/HERE.name
TAKE = HERE.name.split('-')[2]
parser = argparse.ArgumentParser()
parser.add_argument('--uncaptured',action='store_true')
args = parser.parse_args()
checks = json.loads((HERE/'checks.json').read_text())
VIDEO = ROOT/f'productions/join-me-in-life/full-film/assets/motion/ltx23-positive-continuation/P2/{TAKE}/video-silent.mp4'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO) == checks['hashes'][str(VIDEO.relative_to(ROOT))]
prefix = 'uncaptured' if args.uncaptured else 'captured'
specs = [('full',VIDEO,[0,checks['frames']])]
if args.uncaptured:
    specs += [(s['shot'],OUT/f'{s["shot"]}-selected.mp4',s['source_frames_zero_based_end_exclusive']) for s in checks['segments']]
else:
    key = 'S037' if TAKE == 'P2L10' else 'continuous-S050-S051'
    s = next(s for s in checks['segments'] if s['shot'] == key)
    specs += [(key,OUT/f'{key}-selected.mp4',s['source_frames_zero_based_end_exclusive'])]

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
srv = ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=srv.serve_forever,daemon=True).start()
base = f'http://127.0.0.1:{srv.server_port}'
(OUT/'playback.html').write_text('''<style>body{margin:0;background:#171717}video{display:block;width:896px;height:512px;object-fit:contain}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>''')
runs = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
    version = browser.version
    for key,media,interval in specs:
        page = browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1)
        page.goto(base+f'/build/{HERE.name}/playback.html')
        page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(media.relative_to(ROOT)))
        page.wait_for_function('v.readyState>=2')
        page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
        samples = []
        duration = (interval[1]-interval[0])/24
        targets = [] if args.uncaptured else [0.4,duration*.30,duration*.60,duration-.35]
        for target in targets:
            page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
            before = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            name = f'{prefix}-{key}-{target:.2f}.jpg'
            page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=92)
            after = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            samples.append({'requested':target,'before':before,'after':after,'file':name})
            (HERE/name).write_bytes((OUT/name).read_bytes())
        page.wait_for_function('v.ended')
        telemetry = page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
        runs.append({'label':key,'played_file':str(media.relative_to(ROOT)),'played_file_sha256':sha(media),'source_interval_zero_based_end_exclusive':interval,'samples':samples,'telemetry':telemetry})
        page.close()
    browser.close()
srv.shutdown()
scope = 'Actual silent native-size 1x browser execution plus chronological native image inspection; not continuous human-equivalent viewing, subjective listening, phoneme-sync or final-edit approval.'
full = {'take':TAKE,'browser':version,'chromium_sandbox':True,'source_sha256':sha(VIDEO),'source_audio_streams':0,'scope':scope,'runs':runs}
text = json.dumps(full,indent=2)+'\n'
(OUT/f'{prefix}-playback.json').write_text(text)
with gzip.open(HERE/f'{prefix}-playback.json.gz','wt') as f: f.write(text)
summary = {**full,'runs':[{**r,'telemetry':{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'},'frame_callback_count':len(r['telemetry']['frameCallbacks'])} for r in runs]}
(HERE/f'{prefix}-playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
