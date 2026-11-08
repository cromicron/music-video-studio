#!/usr/bin/env python3
"""Run three complete followup keeper/song insertions at1x; record launch and presentation evidence."""
import base64
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def main():
    output = HERE / 'playback-v1.json'
    assert not output.exists(), 'Preserve prior playback record'
    runs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
            args=['--autoplay-policy=no-user-gesture-required', '--enable-automation'],
            ignore_default_args=['--mute-audio'])
        launch = browser.new_browser_cdp_session().send('Browser.getBrowserCommandLine')
        assert '--mute-audio' not in launch['arguments']
        for take, seconds in [('O02', 212/24), ('B01', 207/24), ('B04', 84/24)]:
            source = HERE / take / (take + '-keeper-original-song.mp4')
            page = browser.new_page(viewport={'width': 960, 'height': 570})
            page.set_content('<body style="margin:0;background:#000"><video id="v" width="896" controls></video></body>')
            page.evaluate('''data=>{v.src='data:video/mp4;base64,'+data; v.muted=false;v.volume=1;v.playbackRate=1;
                window.events=[];['waiting','stalled','error','ended'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));}''', base64.b64encode(source.read_bytes()).decode())
            page.wait_for_function('v.readyState>=4', timeout=60000)
            page.evaluate('()=>{window.started=performance.now();return v.play()}')
            for index, target in enumerate([0.2, 1, 2, 3, 4, seconds - 0.15]):
                if target >= seconds:
                    continue
                page.wait_for_function('t=>v.currentTime>=t', arg=target, timeout=20000)
                page.screenshot(path=str(HERE / take / f'playback-{index:02d}.jpg'), quality=92)
            page.wait_for_function('v.ended', timeout=20000)
            telemetry = page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,rate:v.playbackRate,
                muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,width:v.videoWidth,height:v.videoHeight,
                wallSeconds:(performance.now()-started)/1000,quality:(q=>({total:q.totalVideoFrames,dropped:q.droppedVideoFrames,
                corrupted:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality()),events:events})''')
            assert telemetry['ended'] and telemetry['error'] is None
            assert telemetry['rate'] == 1 and not telemetry['muted'] and telemetry['volume'] == 1
            assert telemetry['width'] == 896 and telemetry['height'] == 512
            assert telemetry['quality']['corrupted'] == 0
            assert not [e for e in telemetry['events'] if e['event'] in ['waiting', 'stalled', 'error']]
            runs.append({'take': take, 'file': str(source), 'sha256': sha(source), 'telemetry': telemetry})
            page.close()
        record = {'scope': 'Three complete source-keeper/song derivatives at natural1x, not final joined film acceptance',
                  'browser': browser.version, 'actual_launch': launch, 'runs': runs,
                  'limits': 'Actual unmuted launch and presentation timing are instrumented evidence; no subjective human listening, exact note/fingering or phoneme claim.'}
        browser.close()
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'runs': len(runs), 'drops': [r['telemetry']['quality']['dropped'] for r in runs]}))


if __name__ == '__main__':
    main()
