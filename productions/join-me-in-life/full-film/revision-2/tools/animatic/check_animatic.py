#!/usr/bin/env python3
"""Check exact decoded pictures, cadence, audio evidence and browser playback readiness."""
import argparse
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import struct
import subprocess
import threading
from urllib.parse import quote


def read(path): return json.loads(Path(path).read_text())
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def packets(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_packets',
                             '-show_entries', 'packet=pts_time,duration_time,data_hash',
                             '-show_data_hash', 'sha256', '-of', 'json', str(path)],
                            check=True, capture_output=True, text=True)
    return json.loads(result.stdout)['packets']
def picture_hashes(inputs, evidence):
    result = subprocess.run(['ffmpeg', '-v', 'error', *inputs, '-map', '0:v:0', '-an',
                             '-fps_mode', 'passthrough', '-f', 'framehash', '-hash', 'sha256', '-'],
                            check=True, capture_output=True, text=True)
    evidence.write_text(result.stdout)
    return [line.rsplit(',', 1)[-1].strip() for line in result.stdout.splitlines()
            if line and not line.startswith('#')]
def mp4_boxes(path):
    boxes = []
    with path.open('rb') as f:
        while header := f.read(8):
            size, kind = struct.unpack('>I4s', header)
            if size == 1: size = struct.unpack('>Q', f.read(8))[0]; skip = size-16
            else: skip = size-8
            boxes.append(kind.decode('ascii'))
            if size == 0: break
            f.seek(skip, 1)
    return boxes


def browser_check(video, output):
    from playwright.sync_api import sync_playwright
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *_): pass
        def send_head(self):
            path = Path(self.translate_path(self.path))
            if not path.is_file(): return super().send_head()
            size = path.stat().st_size
            start, end = 0, size-1
            requested = self.headers.get('Range')
            if requested:
                match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested)
                if not match or not any(match.groups()): self.send_error(416); return None
                a, b = match.groups()
                start, end = (int(a), min(int(b), end) if b else end) if a else (max(0,size-int(b)),end)
                if start > end or start >= size: self.send_error(416); return None
            source = path.open('rb'); source.seek(start)
            self.remaining_bytes = end-start+1
            self.send_response(206 if requested else 200)
            self.send_header('Content-Type', self.guess_type(str(path)))
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(self.remaining_bytes))
            if requested: self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            return source
        def copyfile(self, source, outputfile):
            if not hasattr(self, 'remaining_bytes'): return super().copyfile(source, outputfile)
            try:
                while self.remaining_bytes:
                    block = source.read(min(1024*1024, self.remaining_bytes))
                    if not block: break
                    outputfile.write(block); self.remaining_bytes -= len(block)
            except (BrokenPipeError, ConnectionResetError):
                pass  # Browser cancels old range requests when seeking/closing.
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(video.parent)))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                                 args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
            page = browser.new_page(viewport={'width':1280, 'height':760})
            base = f'http://127.0.0.1:{server.server_port}'
            page.goto(base)
            page.set_content('<body style="margin:0;background:black"><video id="v" controls playsinline style="width:100vw;height:100vh" src="'+base+'/'+quote(video.name)+'"></video></body>')
            page.wait_for_function('document.querySelector("video").readyState >= 2', timeout=60000)
            metadata = page.evaluate('''() => {const v=document.querySelector('video');return {duration:v.duration,width:v.videoWidth,height:v.videoHeight,readyState:v.readyState,error:v.error&&v.error.code,playbackRate:v.playbackRate}}''')
            samples = []
            # Include the corrected doorway, refusal, incomplete rise, mask and arrival.
            for at in [0, 80.5, 155.5, 180.3, 205, 249.5, 275]:
                sample = page.evaluate('''async (at) => {const v=document.querySelector('video'); v.pause();v.currentTime=at;
                  await new Promise((resolve,reject)=>{v.addEventListener('seeked',resolve,{once:true});setTimeout(()=>reject(new Error('seek timeout')),15000)});
                  const first=v.currentTime;await v.play(); await new Promise(r=>setTimeout(r,1200));v.pause();
                  return {seek:at,first,last:v.currentTime,advanced:v.currentTime-first,error:v.error&&v.error.code,readyState:v.readyState,rate:v.playbackRate,decodedFrames:v.getVideoPlaybackQuality().totalVideoFrames};}''', at)
                if sample['error'] or sample['advanced'] < .5 or sample['rate'] != 1 or abs(sample['first']-at) > .1:
                    raise ValueError('Browser playback or requested seek failed: '+repr(sample))
                samples.append(sample)
            page.screenshot(path=str(output.with_suffix('.browser.png')))
            browser.close()
            return {'passed':True, 'browser':'system Chromium via Playwright', 'metadata':metadata, 'samples':samples,
                    'scope':'Actual normal-rate opening/seek/play readiness; not a full creative or listening review.'}
    finally:
        server.shutdown(); server.server_close()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video', required=True, type=Path)
    p.add_argument('--config', required=True, type=Path)
    p.add_argument('--work-dir', required=True, type=Path)
    p.add_argument('--report', required=True, type=Path)
    args = p.parse_args()
    if args.report.exists() or args.report.with_suffix('.browser.png').exists():
        raise ValueError('Existing review evidence is preserved; choose a new report path')
    config = read(args.config)
    manifest = read(args.video.with_suffix('.manifest.json'))
    if sha(args.video) != manifest['output_sha256']: raise ValueError('Output differs from rendered manifest')
    paths = []
    for shot in config['shots']:
        paths.append((args.work_dir/(shot['id']+'.mp4')).resolve())
    if any("'" in str(path) for path in paths): raise ValueError('Ambiguous source path')
    concat = args.work_dir/'verification-concat.txt'
    concat.write_text(''.join(f"file '{path}'\n" for path in paths))
    expected = picture_hashes(['-f', 'concat', '-safe', '0', '-i', str(concat)], args.work_dir/'source-pictures.framehash')
    actual_pictures = picture_hashes(['-i', str(args.video)], args.work_dir/'output-pictures.framehash')
    if expected != actual_pictures: raise ValueError('Assembled decoded pictures differ from the exact source exposures')
    actual = packets(args.video)
    timestamps = sorted(float(p['pts_time']) for p in actual)
    if len(timestamps) != 6667 or any(abs(t-i/24) > .00001 for i,t in enumerate(timestamps)):
        raise ValueError('Picture frame extent or continuous 24fps cadence differs')
    if any(abs(float(p['duration_time'])-1/24) > .00001 for p in actual): raise ValueError('Wrong frame duration')
    boxes = mp4_boxes(args.video)
    if boxes.index('moov') > boxes.index('mdat'): raise ValueError('Fast-start metadata missing')
    if manifest['technical_validation']['full_decode'] != 'passed': raise ValueError('Full decode did not pass')
    waveform = manifest['audio']['waveform_check']
    if waveform['correlation'] < .995 or abs(waveform['offset_seconds']) > .03: raise ValueError('Original audio mismatch')
    report = {'schema':'jml-v2-storyboard-technical-check/v1','status':'technical_pass_planning_animatic_only',
              'video':str(args.video.resolve()),'video_sha256':sha(args.video), 'config_sha256':sha(args.config),
              'story_revision':config['story_revision'], 'shot_plan_sha256':config['shot_plan_sha256'],
              'exact_ordered_decoded_picture_sha256_match':True,'all_6667_frame_timestamps_checked':True,
              'comparison_note':'Decoded picture hashes avoid false differences from MP4 concat inserting H.264 parameter NALs at clip starts.',
              'source_framehash_file':str((args.work_dir/'source-pictures.framehash').resolve()),
              'output_framehash_file':str((args.work_dir/'output-pictures.framehash').resolve()),
              'fps':24,'frames':6667,'narrative_shots':49,'stationary_endpoint_exposures':len(config['shots']),
              'faststart':True,'full_decode':'passed','original_song_waveform':waveform,
              'no_caption_title_or_camera_motion':True,'normal_speed_full_story_review_performed':False,
              'generated_motion_or_final_film_approval':False}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    report['browser_playback'] = browser_check(args.video.resolve(), args.report.resolve())
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='browser_playback'},indent=2))
