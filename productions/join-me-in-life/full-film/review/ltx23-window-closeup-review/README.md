# L01 fixed-crop close-up evidence

Frame numbers are zero based at 24 fps. Source selection is [3,157), or f3–156 inclusive. Full-frame overviews use 336×189 panels; face/neck and left-edge crops retain native pixels. Actual browser captures are 960×540. No duplicate video or raw PNG frame files are included.

## Every source frame

### Full-frame overviews

- [all-frames-000-015.jpg](all-frames-000-015.jpg)
- [all-frames-016-031.jpg](all-frames-016-031.jpg)
- [all-frames-032-047.jpg](all-frames-032-047.jpg)
- [all-frames-048-063.jpg](all-frames-048-063.jpg)
- [all-frames-064-079.jpg](all-frames-064-079.jpg)
- [all-frames-080-095.jpg](all-frames-080-095.jpg)
- [all-frames-096-111.jpg](all-frames-096-111.jpg)
- [all-frames-112-127.jpg](all-frames-112-127.jpg)
- [all-frames-128-143.jpg](all-frames-128-143.jpg)
- [all-frames-144-159.jpg](all-frames-144-159.jpg)
- [all-frames-160-160.jpg](all-frames-160-160.jpg)

### Native face and neck

- [face-000-023.jpg](face-000-023.jpg)
- [face-024-047.jpg](face-024-047.jpg)
- [face-048-071.jpg](face-048-071.jpg)
- [face-072-095.jpg](face-072-095.jpg)
- [face-096-119.jpg](face-096-119.jpg)
- [face-120-143.jpg](face-120-143.jpg)
- [face-144-160.jpg](face-144-160.jpg)

### Native reflection boundary

- [left-edge-000-031.jpg](left-edge-000-031.jpg)
- [left-edge-032-063.jpg](left-edge-032-063.jpg)
- [left-edge-064-095.jpg](left-edge-064-095.jpg)
- [left-edge-096-127.jpg](left-edge-096-127.jpg)
- [left-edge-128-159.jpg](left-edge-128-159.jpg)
- [left-edge-160-160.jpg](left-edge-160-160.jpg)

## Selected complete frames, playback and provenance

- [native-003.jpg](native-003.jpg)
- [native-049.jpg](native-049.jpg)
- [native-089.jpg](native-089.jpg)
- [native-124.jpg](native-124.jpg)
- [native-156.jpg](native-156.jpg)
- [original-crop-boundaries.jpg](original-crop-boundaries.jpg)
- [playback-0.20.jpg](playback-0.20.jpg)
- [playback-2.00.jpg](playback-2.00.jpg)
- [playback-4.00.jpg](playback-4.00.jpg)
- [playback-6.30.jpg](playback-6.30.jpg)
- [source-evidence.json](source-evidence.json)
- [playback.json](playback.json)

- [playback-1.00.jpg](playback-1.00.jpg)

- [playback-3.00.jpg](playback-3.00.jpg)

- [playback-5.00.jpg](playback-5.00.jpg)

## Reproduce

- [Decode, crop provenance and evidence](reproduce.py)
- [Actual 1× browser playback](playback_check.py)

Run either Python script from any directory. Fresh outputs are written beneath ignored root `build/ltx23-window-closeup-review/`; production sources and frozen reviews are not changed. FFmpeg/ffprobe, Pillow, NumPy, Playwright and `/usr/bin/chromium` are used.
