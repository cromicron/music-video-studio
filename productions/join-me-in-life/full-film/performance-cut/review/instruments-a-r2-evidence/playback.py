#!/usr/bin/env python3
"""Complete actual instrument keeper/song selections; no automatic creative verdict."""
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
    assert not output.exists(), 'Preserve previous playback evidence'
    takes = ['B02', 'B06_A', 'B06_B', 'B07', 'B11']
    assert all((HERE / take / 'inspection-aids.json').is_file() for take in takes), 'Wait for all actual outputs'
    runs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
            args=['--autoplay-policy=no-user-gesture-required', '--enable-automation'],
            ignore_default_args=['--mute-audio'])
        launch = browser.new_browser_cdp_session().send('Browser.getBrowserCommandLine')
        assert '--mute-audio' not in launch['arguments']
        for take in takes:
            aid = json.loads((HERE / take / 'inspection-aids.json').read_text())
            source = HERE / take / (take + '-keeper-original-song.mp4')
            assert sha(source) == aid['review_sha256']
            seconds = (aid['keeper'][1] - aid['keeper'][0]) / 24
            page = browser.new_page(viewport={'width': 960, 'height': 570})
            page.set_content('<body style="margin:0;background:#000"><video id="v" width="896" controls></video></body>')
            page.evaluate('''data=>{v.src='data:video/mp4;base64,'+data;v.muted=false;v.volume=1;v.playbackRate=1;
                window.events=[];['waiting','stalled','error','ended'].forEach(e=>v.addEventListener(e,()=>events.push({event:e,time:v.currentTime})));}''', base64.b64encode(source.read_bytes()).decode())
            page.wait_for_function('v.readyState>=4', timeout=60000)
            page.evaluate('()=>{window.started=performance.now();return v.play()}')
            for index, target in enumerate([0.15, seconds * .18, seconds * .36, seconds * .54, seconds * .72, seconds - 0.1]):
                page.wait_for_function('t=>v.currentTime>=t', arg=target, timeout=20000)
                page.screenshot(path=str(HERE / take / f'playback-{index:02d}.jpg'), quality=92)
            page.wait_for_function('v.ended', timeout=20000)
            telemetry = page.evaluate('''()=>({duration:v.duration,currentTime:v.currentTime,rate:v.playbackRate,
                muted:v.muted,volume:v.volume,ended:v.ended,error:v.error,width:v.videoWidth,height:v.videoHeight,
                wallSeconds:(performance.now()-started)/1000,quality:(q=>({total:q.totalVideoFrames,dropped:q.droppedVideoFrames,
                corrupted:q.corruptedVideoFrames}))(v.getVideoPlaybackQuality()),events:events})''')
            assert telemetry['ended'] and telemetry['error'] is None
            assert telemetry['rate'] == 1 and not telemetry['muted'] and telemetry['volume'] == 1
            assert (telemetry['width'], telemetry['height']) == (896, 512)
            assert telemetry['quality']['corrupted'] == 0
            assert not [e for e in telemetry['events'] if e['event'] in ['waiting', 'stalled', 'error']]
            runs.append({'take': take, 'file': str(source), 'sha256': sha(source), 'telemetry': telemetry})
            page.close()
        record = {'scope': 'Five actual instrument selections at1x with original song, including B06 early and late placements; no joined or whole-film acceptance',
                  'browser': browser.version, 'actual_launch': launch, 'runs': runs,
                  'limits': 'Instrumented unmuted playback and visual inspection do not establish subjective human hearing, exact note/fingering or beat synchronization.'}
        browser.close()
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'runs': len(runs), 'drops': [r['telemetry']['quality']['dropped'] for r in runs]}))


if __name__ == '__main__':
    main()
