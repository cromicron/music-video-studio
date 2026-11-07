"""Scoped technical playback of the encoded 1080p preflight; not listening evidence."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import functools
import hashlib
import json
import threading
import time
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
VIDEO = REPO / "build/production-1080-preflight.mp4"
(HERE / "playback.html").write_text('<!doctype html><video id="v" width="1920" height="1080" preload="auto"></video>')
server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(SimpleHTTPRequestHandler, directory=str(REPO)))
threading.Thread(target=server.serve_forever, daemon=True).start()
runs = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
    for name, start, stop in [("opening", 0, 6.5), ("S014 contained first chorus", 66.5, 1694 / 24)]:
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(f"http://127.0.0.1:{server.server_port}/" + str((HERE / "playback.html").relative_to(REPO)))
        # Fetch the complete local file into a seekable Blob. Python's simple
        # server does not support HTTP byte ranges; no media transcoding occurs.
        page.evaluate("async()=>{window.v=document.querySelector('video');v.src=URL.createObjectURL(await(await fetch('/build/production-1080-preflight.mp4')).blob())}")
        page.wait_for_function("v.readyState >= 3")
        page.evaluate("s=>{v.currentTime=s}", start)
        page.wait_for_function("s=>!v.seeking && Math.abs(v.currentTime-s)<.05 && v.readyState>=3", arg=start)
        page.evaluate("stop=>{window.events=[];window.done=false;window.before=v.getVideoPlaybackQuality();for(const k of ['playing','waiting','stalled','error'])v.addEventListener(k,()=>events.push({event:k,time:v.currentTime,error:v.error?.code??null})); const tick=()=>{if(v.currentTime>=stop){v.pause();window.done=true}else{v.requestVideoFrameCallback(tick)}};v.requestVideoFrameCallback(tick);v.playbackRate=1;v.muted=false;v.play()}", stop)
        begun = time.monotonic()
        page.wait_for_function("done || v.error", timeout=30000)
        result = page.evaluate("()=>({currentTime:v.currentTime,playbackRate:v.playbackRate,muted:v.muted,error:v.error?.code??null,width:v.videoWidth,height:v.videoHeight,totalVideoFrames:v.getVideoPlaybackQuality().totalVideoFrames-before.totalVideoFrames,droppedVideoFrames:v.getVideoPlaybackQuality().droppedVideoFrames-before.droppedVideoFrames,events})")
        result.update(name=name, target_start_seconds=start, target_stop_seconds=stop, wall_seconds=time.monotonic()-begun)
        runs.append(result)
        page.close()
    browser.close()
server.shutdown()
result = {"scope": "Two selected spans of exact complete encoded preflight at 1x, unmuted, in headless Chromium. Technical telemetry, not subjective listening or human-equivalent whole-film review.", "delivery_method": "Exact local MP4 fetched into seekable Blob; no transcoding. Initial direct-URL attempt timed out at seek because the simple local HTTP server did not serve byte ranges; this is the corrected harness run.", "output_sha256": hashlib.sha256(VIDEO.read_bytes()).hexdigest(), "runs": runs}
(HERE / "playback-telemetry.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
