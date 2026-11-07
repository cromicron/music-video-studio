# Final whole-film outside review evidence

Frozen 2026-11-07 for candidate SHA-256 `ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09`. The parent report is `../final-full-film-review.md`.

Run from the repository root with FFmpeg/ffprobe, Python, numpy, Pillow, Playwright and `/usr/bin/chromium`:

```sh
python3 productions/join-me-in-life/full-film/review/final-full-film-review/reproduce.py
python3 productions/join-me-in-life/full-film/review/final-full-film-review/verify_audio.py
flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/final-full-film-review/playback_check.py
```

Each script checks its frozen input hashes. `reproduce.py` independently decodes the whole video/audio and checks every video timestamp, then streams selected RGB frames only. Its optional `--reuse-decode` resumes selected extraction from the existing frame-hash cache; use the default command for a fresh full-decode reproduction. `playback_check.py` preloads the actual file and plays without seeking, at 1×, audio enabled, using an ephemeral local port and isolated sandboxed Chromium context. Its individual progress waits are under 60 seconds and its overall operation allows the full film to finish. Screenshots can affect presentation drops; the recorded three drops are retained. Browser presentation, objective audio signal and waveform checks are separate from subjective hearing or human continuous viewing.

Generated larger sheets, 58 selected native JPEG frames, 22 native browser captures, the HTML harness and working logs remain in ignored `build/final-full-film-review/`. No full raw frame dump is retained. The checked-in evidence folder is approximately 10 MB. `retain_evidence.py` reproduces the compact selection from that build cache, but should not be rerun against a frozen evidence folder when preserving its exact inventory.

The report's visual inspection includes all 497 selected thumbnail frames, native detail from the 37 exact frames named in `inspection-index.json`, five native browser captures and all 22 captures in sheets. The remaining extracted native frames are not claimed as separately inspected at native size. A full successful decode and 1× playback do not constitute individual visual inspection of every final picture.

Files retained here:

- `frozen-manifest.json` / `frozen-edit.json`: exact candidate inputs, not the later working configuration.
- `checks.json` / `full-video.framemd5.gz`: independent stream, frame count, contiguous-shot, cadence and selected-frame records.
- `audio-check.json`: original take-49 alignment, duration and ending-level evidence.
- `playback-summary.json` / `playback-full.json.gz`: actual full-length 1× run, drops, errors, events, signal measurements and complete frame-callback telemetry.
- `inspection-index.json`: actual visual coverage and explicit limits.
- `prior-review-hashes.json`: 32 unchanged source/sequence/native reports, including the separate final 1080 equality report.
- `chronology-01.jpg` through `chronology-15.jpg`: all 58 shots at first/middle/last frame, reduced to compact viewing aids.
- `embrace-01.jpg` through `embrace-04.jpg`, `pleas-01.jpg` through `pleas-05.jpg`, selected key-cut sheets and native contact/performance/dawn crops: representative dense and native inspection evidence. Exact complete generated phase/cut sample lists are in `checks.json` and can be reproduced.
- `branding-01.jpg` / `final-fade-01.jpg`: opening overlay and closing fade phases.
- `playback-captures-01.jpg` / `playback-captures-02.jpg`: all 22 real browser captures, with time brackets retained in telemetry.
- `verdict.json` / `evidence-sha256.json`: scoped result and file inventory. JPEG viewing aids do not establish decoded-picture equality; the independently frozen final 1080 report owns that equality evidence.

No provider calls, source/configuration edits, approval-record edits or Git operations were made. The scripts only write to this assigned evidence folder or the separate ignored build cache.
