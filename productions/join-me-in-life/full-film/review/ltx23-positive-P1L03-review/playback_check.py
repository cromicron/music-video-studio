"""Actual 1x source and exact selected-interval playback; writes ignored build only."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import hashlib, json, subprocess

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
NAME = Path(__file__).resolve().parent.name
TAKE = NAME.split('-')[-2]
SPECS = {
    'P1L02': (121, 116, '24312a9d5272083d1c3f248837d63f0b61b8be1a051b6b99c5de2d092cdad53b'),
    'P1L03': (113, 104, '14753d944afdd0ab41db66401ae694ee45c496f1392eb6913d0bbd4da369f2cc'),
}
count, stop, expected = SPECS[TAKE]
OUT = ROOT / 'build' / NAME
OUT.mkdir(parents=True, exist_ok=True)
MEDIA = ROOT / f'productions/join-me-in-life/full-film/assets/motion/ltx23-positive-continuation/P1/{TAKE}/video-silent.mp4'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest() == expected
proxy = OUT / 'selected.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-y', '-i', str(MEDIA), '-an', '-vf', f'trim=start_frame=3:end_frame={stop},setpts=N/(24*TB)', '-r', '24', '-fps_mode', 'cfr', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(proxy)], check=True)
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_streams', '-of', 'json', str(proxy)]))['streams'][0]
assert int(probe['nb_read_frames']) == stop - 3

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

srv = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
Thread(target=srv.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{srv.server_port}'
html = '''<style>body{margin:0;background:#171717}video{display:block}</style><video id="v" preload="auto"></video><script>const v=document.getElementById('v');window.events=[];window.seen=[];['playing','ended','error','stalled','waiting'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,t:v.currentTime})));function cb(now,m){seen.push({wall:now,t:m.mediaTime,presented:m.presentedFrames});v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb)</script>'''
(OUT / 'playback.html').write_text(html)
runs = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, chromium_sandbox=True, args=['--autoplay-policy=no-user-gesture-required'])
    version = browser.version
    specs = [('full-native-uninterrupted', MEDIA, 896, []), ('selected-ordinary-uninterrupted', proxy, 960, []), ('selected-ordinary-captured', proxy, 960, [0.2, 0.9, 1.7, 2.5, 3.4, 4.0])]
    for label, media, width, targets in specs:
        page = browser.new_page(viewport={'width': 960, 'height': 600}, device_scale_factor=1)
        page.goto(base + f'/build/{NAME}/playback.html')
        page.evaluate('async([url,width])=>{v.src=URL.createObjectURL(await(await fetch(url)).blob());v.style.width=width+"px";v.playbackRate=1;v.muted=false}', [base + '/' + str(media.relative_to(ROOT)), width])
        page.wait_for_function('v.readyState>=2')
        page.evaluate('()=>{window.wallStart=performance.now();events=[];seen=[];return v.play()}')
        samples = []
        for target in targets:
            page.wait_for_function('(t)=>v.currentTime>=t', arg=target)
            before = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            name = f'playback-{target:.2f}.jpg'
            page.locator('video').screenshot(path=str(OUT / name), type='jpeg', quality=93)
            after = page.evaluate('({time:v.currentTime,frame:seen.at(-1)})')
            samples.append({'requested': target, 'before': before, 'after': after, 'file': name})
        page.wait_for_function('v.ended')
        tele = page.evaluate('''()=>{let q=v.getVideoPlaybackQuality();return{ended:v.ended,time:v.currentTime,duration:v.duration,rate:v.playbackRate,muted:v.muted,error:v.error,displayWidth:v.getBoundingClientRect().width,displayHeight:v.getBoundingClientRect().height,wallSeconds:(performance.now()-wallStart)/1000,totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames,events,frameCallbacks:seen}}''')
        runs.append({'label': label, 'played_file': str(media.relative_to(ROOT)), 'played_sha256': hashlib.sha256(media.read_bytes()).hexdigest(), 'samples': samples, 'telemetry': tele})
        page.close()
    browser.close()
srv.shutdown()
data = {'browser': version, 'source_sha256': expected, 'source_audio_streams': 0, 'selected_source_frames_zero_based': [3, stop], 'scope': 'Actual silent 1x browser execution and captured pictures; no human-equivalent continuous viewing or listening claimed.', 'runs': runs}
(OUT / 'playback-full.json').write_text(json.dumps(data, indent=2) + '\n')
for run in data['runs']:
    run['telemetry'].pop('frameCallbacks')
(OUT / 'playback-summary.json').write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps(data, indent=2))
