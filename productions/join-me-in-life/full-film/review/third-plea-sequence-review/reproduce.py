"""Independent actual S046/four-plea proof review; outputs only ignored build/.
Requires NumPy, Pillow, FFmpeg/ffprobe, Playwright and sandboxed Chromium.
No provider/config changes. Browser execution is not subjective listening.
"""
from pathlib import Path
import hashlib, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE = ROOT/'productions/join-me-in-life/full-film'
OUT = ROOT/'build/third-plea-sequence-review'
OUT.mkdir(parents=True, exist_ok=True)
PROOF = BASE/'exports/Join_Me_in_Life_Third_Plea_Proof.mp4'
CONTEXT = BASE/'exports/Join_Me_in_Life_Four_Pleas_Context_Proof.mp4'
SOURCE = BASE/'assets/motion/ltx23-performance-pilots/S046/video-silent.mp4'
REVIEW = BASE/'review/ltx23-third-plea-review.md'
hashes = {
    PROOF:'1d00346a028d91c3dc660f9041e8be84ac6aea6430367c6050856778467c953e',
    CONTEXT:'513798b11449a2b6405850f125901cea024bc4feb4f7a84a92b6de37c21c08e5',
    SOURCE:'6efd9acdd5f07a8ae9148de665f169660fcad8c29874b1e0a98416d133b8baa9',
    REVIEW:'f40b1f5da7c3a95d65da61b353ef890ef8a933a058c1f2b9c48bbceabfa5ab40',
}
for path, expected in hashes.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path

def decode(path, vf=None):
    cmd = ['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0']
    if vf: cmd += ['-vf',vf]
    raw = subprocess.check_output(cmd+['-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
    return np.frombuffer(raw,dtype=np.uint8).reshape(-1,540,960,3)

scale = 'scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1,format=yuv420p,setparams=colorspace=bt709:range=limited'
a = decode(PROOF)
c = decode(CONTEXT)
s = decode(SOURCE,scale)
assert (len(a),len(c),len(s)) == (82,571,89)
mae = [float(np.abs(x.astype(np.float32)-y.astype(np.float32)).mean()) for x,y in zip(a,s[3:85])]
context_mae = [float(np.abs(x.astype(np.float32)-y.astype(np.float32)).mean()) for x,y in zip(a,c[292:374])]
assert max(mae) < 5
timestamps = {}
for label, path, count in [('proof',PROOF,82),('context',CONTEXT,571)]:
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)]))
    t = [float(f['best_effort_timestamp_time']) for f in probe['frames']]
    assert len(t) == count and max(abs(v-i/24) for i,v in enumerate(t)) < 1e-5
    timestamps[label] = t

def sheet(items, cols, size, name):
    w,h = size
    canvas = Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717')
    d = ImageDraw.Draw(canvas)
    for j,(label,im) in enumerate(items):
        x,y = j%cols*w,j//cols*(h+24)
        d.text((x+5,y+5),label,fill='white')
        im = ImageOps.contain(im,size)
        canvas.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
    canvas.save(OUT/name,quality=92)

proof_ids = [0,12,24,36,42,48,60,72,81]
sheet([(f'S046 proof f{i+1} | source f{i+4}',Image.fromarray(a[i])) for i in proof_ids],3,(480,270),'wide-sequence.jpg')
for i in [0,24,42,48,81]: Image.fromarray(a[i]).save(OUT/f'proof-{i+1:03}.jpg',quality=94)
manifest = json.loads(CONTEXT.with_suffix('.manifest.json').read_text())
start = manifest['coverage']['start_frame']
shots = [{k:v for k,v in shot.items() if k in ['id','start_frame','end_frame_exclusive','purpose']} for shot in manifest['shots']]
for shot in shots:
    shot['context_zero_based_frames'] = [shot['start_frame']-start,shot['end_frame_exclusive']-start]
    lo,hi = shot['context_zero_based_frames']
    ids = [lo,(lo+hi-1)//2,hi-1]
    sheet([(f'{shot["id"]} context f{i+1} | master {(start+i)/24:.3f}s',Image.fromarray(c[i])) for i in ids],3,(480,270),f'{shot["id"]}-progression.jpg')
cut_ids = [97,98,178,179,291,292,373,374,472,473]
sheet([(f'context f{i+1} | master {(start+i)/24:.3f}s',Image.fromarray(c[i])) for i in cut_ids],2,(672,378),'cuts.jpg')
context_ids = list(range(0,571,24))+[570]
for block in range(0,len(context_ids),9):
    ids = context_ids[block:block+9]
    sheet([(f'context f{i+1} | {i/24:.3f}s',Image.fromarray(c[i])) for i in ids],3,(480,270),f'context-{block//9+1}.jpg')
checks = {
    'hashes':{str(k.relative_to(ROOT)):v for k,v in hashes.items()},
    'proof':{'frames':82,'dimensions':[960,540],'fps':24,'duration_seconds':82/24,'source_frames_zero_based_end_exclusive':[3,85],
             'master_seconds':[5183/24,5265/24],'expected_scale_filter':scale,'expected_source_mae_mean':float(np.mean(mae)),'expected_source_mae_max':max(mae),'per_frame_mae':mae},
    'context':{'frames':571,'dimensions':[960,540],'fps':24,'duration_seconds':571/24,'master_seconds':[4891/24,5462/24],
               'S046_zero_based_frames_end_exclusive':[292,374],'S046_pixel_identical_to_standalone_proof':bool(np.array_equal(a,c[292:374])),
               'S046_vs_standalone_mae_mean':float(np.mean(context_mae)),'S046_vs_standalone_mae_max':max(context_mae),'shots':shots},
    'timestamps':timestamps,
    'audio_scope':'Delivery manifest reports original-master correlations 0.9995348572 / 0.9995722907, both zero lag. Not independently repeated here; not subjective listening or phoneme-sync proof.',
    'scope':'Exact decode, timestamps and all-frame expected-source correspondence, plus human-readable visual evidence. Lossy source correspondence does not prove anatomy.',
}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
del a,c,s

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
srv = ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=srv.serve_forever,daemon=True).start()
base = f'http://127.0.0.1:{srv.server_port}'
html = '''<style>body{margin:0;background:#171717}video{display:block;width:672px}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));function cb(now,m){seen.push({wall:now,time:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>'''
(OUT/'playback.html').write_text(html)
runs = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True,args=['--autoplay-policy=no-user-gesture-required'])
    version = browser.version
    for key,media,targets in [('proof',PROOF,[.2,.8,1.4,2.2,3.1]),('context',CONTEXT,[3.8,4.3,5.3,6.9,7.6,10.5,12,12.4,13.4,14.5,15.3,15.8,18.5,19.5,20.2,23])]:
        page = browser.new_page(viewport={'width':960,'height':600},device_scale_factor=1)
        page.goto(base+'/build/third-plea-sequence-review/playback.html')
        page.evaluate('async(url)=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.playbackRate=1;v.muted=false}',base+'/'+str(media.relative_to(ROOT)))
        page.wait_for_function('v.readyState>=2')
        page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
        captures = []
        for target in targets:
            page.wait_for_function('(t)=>v.currentTime>=t',arg=target)
            before = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            name = f'playback-{key}-{target:05.2f}.jpg'
            page.locator('video').screenshot(path=str(OUT/name),type='jpeg',quality=91)
            after = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            captures.append({'requested':target,'before':before,'after':after,'file':name})
        page.wait_for_function('v.ended')
        tele = page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,currentTime:v.currentTime,duration:v.duration,playbackRate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
        runs.append({'key':key,'source_sha256':hashes[media],'captures':captures,'telemetry':tele})
        page.close()
    browser.close()
srv.shutdown()
(OUT/'playback.json').write_text(json.dumps({'browser':version,'chromium_sandbox':True,'scope':'Actual 1× unmuted browser execution and captures, not subjective listening or continuous human-equivalent perception.','runs':runs},indent=2)+'\n')
for run in runs:
    for block in range(0,len(run['captures']),4):
        captures = run['captures'][block:block+4]
        sheet([(f'{run["key"]} requested {cap["requested"]:.2f}s | actual {cap["before"]["time"]:.3f}..{cap["after"]["time"]:.3f}s',Image.open(OUT/cap['file'])) for cap in captures],2,(672,378),f'captured-{run["key"]}-{block//4+1}.jpg')
print(json.dumps({'proof_mae_mean':checks['proof']['expected_source_mae_mean'],'proof_mae_max':max(mae),'context_S046_pixel_equal':checks['context']['S046_pixel_identical_to_standalone_proof'],'playback':[{**{'key':r['key']},**{k:v for k,v in r['telemetry'].items() if k!='frameCallbacks'}} for r in runs]},indent=2))
