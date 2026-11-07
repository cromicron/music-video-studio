# P2L11 — independent indoor-dawn source review

**PASS for S050 `[3,99)` and S051 `[99,194)` at 24 fps**, including their continuous 191-frame source progression. The scene sustains exhausted company: his worried head settles through a long closed-eye pause, while her attention remains down/away toward the window. No cure, romantic lift, reversed comfort or added arm-around gesture appears. This is a frozen independent **source** verdict dated 2026-11-07, applying the repository's [Be Ambitious](../../../../.agents/skills/be-ambitious/SKILL.md) raw-material review standard. It does not approve the actual edit joins, soundtrack or complete film.

Reviewed [actual silent video](../assets/motion/ltx23-positive-continuation/P2/P2L11/video-silent.mp4), SHA-256 **`f7a168bcb68d4678fd39aea91b8f6aeadcf6aa14103c32b96175ba7a8015f703`**: **896×512, 201 frames, 24 fps, 8.375 s, zero audio streams**. All frame labels below and in this evidence are **zero-based**; intervals exclude their end.

| Delivery | Exact source interval | Length | Source verdict |
| --- | --- | --- | --- |
| S050; timeline `[5561,5657)` | `[3,99)`; `[0.125,4.125)` s | 96 frames / 4 s | **PASS**, with native crown-graze limitation below. |
| S051; timeline `[5657,5752)` | `[99,194)`; `[4.125,8.083333)` s | 95 frames / 3.958333 s | **PASS**, with coherent distant passerby and fine-detail limits below. |
| Continuous source check | `[3,194)` | 191 frames / 7.958333 s | **PASS** as one unbroken progression; f98→f99 contains no source restart. |

All recommendations require **full-image contain at native 24 fps**, without added zoom, retime, loop or endpoint hold. The 10 unused handle frames were inspected but are not added to the requested deliveries.

The actual [original S06 guide](../../art/03_Story/S06_Still_Here_At_Dawn.png) shows **both forearms angled down toward their own laps**. It contains no visible arm wrapped around a shoulder or the earlier outer-arm-contact pose. That is the state tested here. Across every decoded frame the forearms retain ownership and downward placement; both bodies remain supported by their chairs, and each head stays supported by its own neck. Their close shoulder spacing does not turn into a new embrace. Hands and wrists mostly fall below the source's lower edge, so an unseen finger grip, wristband or contact path cannot be certified or invented. [Native forearm/support phases](ltx23-positive-P2L11-review/hands-support.jpg) · [source/guide/actual endpoints](ltx23-positive-P2L11-review/guides-endpoints.jpg).

Approximately f0–35, he turns and raises his head slightly toward the front while keeping the concerned brow. His eyelids lower around f36–48; the sustained closed/near-closed-eye pause continues through roughly f139 as the head and shoulders settle. It reads as tired inward attention, not an unmotivated frozen blink or recovery. Around f140–168 he reopens his eyes and returns toward her/window, still worried; he does not smile. Her eyelids and head gradually lower through the middle, with a serious mouth and gaze directed away. A discrete fully closed female blink or isolated breathing cycle is not clearly established; the coherent limited movement is sufficient for the scene. She never lifts a romantic gaze to him or takes over comforting him. [Overview](ltx23-positive-P2L11-review/overview.jpg) · [native facial phases](ltx23-positive-P2L11-review/identity-phases.jpg).

A01/A02 and the original S06 were visually compared. Both retain their adult drawn facial structure, hair and wardrobe. Her auburn hair and freckles remain recognizable; the small irises render muted gray-green, cooler than the guide's warmer hazel, without a sustained bright-blue or round-faced redesign. Small facial/freckle lines soften in movement, particularly his late turn, and sharpen near the endpoint. This does not support a claim that every fine line or iris-color nuance is preserved. [Guide/actual eye comparison, 4× nearest-neighbor display only](ltx23-positive-P2L11-review/eye-comparison.jpg).

**Native framing limitation:** during his early/middle head lift, roughly f24–72 (1–3 s), upper hair strands graze and briefly clip the source's top image boundary. The forehead/face remain visible, and the action is supported head movement, not body lifting. This modest native crown graze is accepted for full-image contain, with no additional top crop; it is not a claim of generous headroom. [Crown phases](ltx23-positive-P2L11-review/crown-phases.jpg).

A distant corridor passerby is visible behind the chairs from approximately f114–159 (4.75–6.63 s), within S051. Native sequential crops establish the entrance: a foot first appears beyond the doorway/post, followed by the body; he walks continuously behind the chairs and exits the right edge. It is not a one-frame apparition, teleport or foreground interruption. His small face/clothing soften, but the walk and chair occlusion remain understandable. The pair neither respond nor lose the scene's unresolved focus. Window mullions, chairs, doorway, exterior skyline and pale lighting remain spatially stable otherwise. [Native corridor phases](ltx23-positive-P2L11-review/corridor-phases.jpg).

Verification combined all **201 chronological native actor crops**, all-frame full-image sheets, native crown/forearm/face/background phases, the complete passerby entrance/exit, source/reference comparisons, and inspected browser captures. Error-failing FFmpeg decode, constant 24 fps timestamps and silent-stream checks passed. [Hashes/checks](ltx23-positive-P2L11-review/checks.json) pin S06 SHA-256 `09a04d5fdc90152550372722789c1c464239f3f16cae3ad03da63d5fecf74774`, fitted guides, references, provenance and render record. The start/end fitted pixels match, with RGB SHA-256 `0958981177129680f5ed6dd3f03fe16d3b6233d7f94975f53cba1af4dad452e4`; four guide records cover both generation stages. Guide/decode success does not establish a motion-quality pass by itself.

Sandboxed Chromium **154.0.8037.57** actually played preloaded bytes at **1×, 896×512, full-image contain**. Capture-free runs were serialized with `build/source-review-playback.lock`:

| Played source/proxy | Player frames | Wall time | Drops / corrupt frames / errors / waits / stalls |
| --- | ---: | ---: | --- |
| Full take | 201 | 8.3954 s | 0 / 0 / 0 / 0 / 0 |
| Exact S050 | 96 | 4.0072 s | 0 / 0 / 0 / 0 / 0 |
| Exact S051 | 95 | 3.9665 s | 0 / 0 / 0 / 0 / 0 |
| Continuous `[3,194)` | 191 | 7.9652 s | 0 / 0 / 0 / 0 / 0 |

No initial failed/dropped runs were omitted. Separate captured full/continuous runs likewise completed 201/191 frames with zero reported drops/errors/waits. [Capture-free summary](ltx23-positive-P2L11-review/uncaptured-playback-summary.json) · [captured summary](ltx23-positive-P2L11-review/captured-playback-summary.json) · [continuous tired pause](ltx23-positive-P2L11-review/captured-continuous-S050-S051-2.39.jpg) · [continuous ending](ltx23-positive-P2L11-review/captured-continuous-S050-S051-7.61.jpg). Compressed full callback/event logs remain with the evidence; callback counts can differ from the player's decoded-frame count.

These are actual browser execution records plus chronological image inspection, not continuous human-equivalent viewing or subjective listening. The source is silent. The consecutive f98→f99 source transition was inspected; the rendered S050/S051 boundary, neighboring shots and final music timing were not supplied to this reviewer and are not cleared here.

Reproduce from the repository root with Python, numpy, Pillow, FFmpeg/ffprobe, Playwright and `/usr/bin/chromium`:

```sh
python3 productions/join-me-in-life/full-film/review/ltx23-positive-P2L11-review/reproduce.py
flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/ltx23-positive-P2L11-review/playback_check.py --uncaptured
flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/ltx23-positive-P2L11-review/playback_check.py
```

Exhaustive sheets, arrays and consecutive-frame review proxies remain in ignored `build/ltx23-positive-P2L11-review/`; compact evidence/scripts are retained beside this report. Only this new report and its matching evidence folder were authored for this take. No provider submission, source, editor configuration, approval record or previous review was changed. **Verdicts frozen for the pinned source and exact intervals above.**
