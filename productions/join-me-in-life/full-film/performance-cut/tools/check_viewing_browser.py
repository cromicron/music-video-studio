#!/usr/bin/env python3
"""Adapted retained C browser check: actual current-cut targets or real short proof."""
import argparse
import functools
import hashlib
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--file', type=Path, required=True)
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--segments', type=Path, help='JSON rows: label,start_seconds,duration_seconds')
    ap.add_argument('--excerpt-proof', action='store_true', help='Real short proof only, not a full-film check')
    a = ap.parse_args()
    source = a.file.resolve()
    assert not a.output.exists() and not a.output.with_suffix('.jpg').exists(), 'Preserve previous browser evidence'
    a.output.parent.mkdir(parents=True, exist_ok=True)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == a.sha256
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(source.parent)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/{source.name}'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                args=['--autoplay-policy=no-user-gesture-required', '--enable-automation'],
                ignore_default_args=['--mute-audio'])
            launch = browser.new_browser_cdp_session().send('Browser.getBrowserCommandLine')
            assert '--mute-audio' not in launch['arguments']
            page = browser.new_page(viewport={'width':1000,'height':620})
            page.set_content('<body style="margin:0;background:#000"><video id="v" width="960" controls></video></body>')
            size = page.evaluate('''async url => {const data=await fetch(url).then(r=>r.blob());
                v.src=URL.createObjectURL(data); v.muted=false; v.volume=1; v.playbackRate=1;
                window.events=[]; ['error','waiting','stalled','ended'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));
                v.load(); return data.size;}''', url)
            assert size == source.stat().st_size
            page.wait_for_function('v.readyState>=4', timeout=60000)
            actual_duration=page.evaluate('v.duration')
            if a.excerpt_proof:
                assert 0<actual_duration<277, 'Excerpt check cannot stand in for the full film'
            else:
                assert abs(actual_duration-277.791667)<0.05, 'Full check requires actual complete movie'
            if a.segments:
                configuration=json.loads(a.segments.read_text())
            elif a.excerpt_proof:
                assert actual_duration<=12, 'Supply short seek/play segments for longer excerpts'
                configuration=[['complete_real_excerpt',0,actual_duration+0.1]]
            else:
                configuration=[['opening_order',0,3],['verse_order',35,3],['full_band',67,3],
                    ['summer',121,3],['recognition',203,3],['first_plea',208,3],
                    ['late_band',243,3],['quiet_guitar',255,3],['tearful_ending',274.5,4]]
            segments=[]
            for label, target, duration in configuration:
                assert 0<=target<actual_duration and 2<duration<=12
                page.evaluate('(t)=>{v.pause();window.seekStart=performance.now();v.currentTime=t;}', target)
                page.wait_for_function('t=>!v.seeking&&v.readyState>=3&&Math.abs(v.currentTime-t)<0.08',arg=target,timeout=30000)
                before=page.evaluate('()=>({time:v.currentTime,seekMilliseconds:performance.now()-seekStart,quality:(q=>({totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality())})')
                page.evaluate('()=>{events=[];window.playStart=performance.now();return v.play()}')
                page.wait_for_function('end=>v.ended||v.currentTime>=end',arg=target+duration,timeout=15000)
                page.evaluate('v.pause()')
                after=page.evaluate('()=>({time:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight,rate:v.playbackRate,muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,wallSeconds:(performance.now()-playStart)/1000,quality:(q=>({totalVideoFrames:q.totalVideoFrames,droppedVideoFrames:q.droppedVideoFrames,corruptedVideoFrames:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality()),events:events})')
                assert after['error'] is None and after['rate']==1 and not after['muted'] and after['volume']==1
                assert after['width']==1920 and after['height']==1080
                assert not [e for e in after['events'] if e['event'] in ['waiting','stalled','error']]
                assert after['quality']['corruptedVideoFrames']==0
                assert after['time'] > target+2
                segments.append({'label':label,'requested_start':target,'requested_duration':duration,'before':before,'after':after})
            assert segments[-1]['after']['ended']
            screenshot=a.output.with_suffix('.jpg')
            page.screenshot(path=str(screenshot),quality=85)
            version=browser.version
            browser.close()
        record={'schema':'jml-performance-delivery-browser-check/v1','full_film':not a.excerpt_proof,'scope':'technical_excerpt' if a.excerpt_proof else 'brief_complete_delivery_samples','file':str(a.file),'sha256':a.sha256,
                'preloaded_bytes':size,'browser':version,'actual_browser_command_line':launch,
                'ignored_default_args':['--mute-audio'],'segment_configuration':configuration,'segments':segments,'final_tail_capture':str(screenshot),
                'result':'PASS_BRIEF_ACTUAL_BROWSER_SEEK_AND_PLAYBACK',
                'limits':'Actual configured short seek/play samples; excerpt mode is not a completed-film check. This is not another uninterrupted whole-film review. Actual unmuted browser launch is verified; no subjective hearing, physical speaker output or external hosted-player readiness is claimed.'}
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({'result':record['result'],'segments':len(segments),'ended':segments[-1]['after']['ended']}))
    finally:
        server.shutdown()


if __name__=='__main__':
    main()
