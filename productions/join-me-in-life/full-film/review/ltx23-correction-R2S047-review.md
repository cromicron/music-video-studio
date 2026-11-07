# R2S047 — downward-attention correction source review

7 November 2026. Independent source review under the retained Be Ambitious outside-review gate. **PASS the complete proposed S047 interval `[3,102)`**, zero-based and end-exclusive: one-based frames 4–102, source 0.125000–4.250000 seconds, **99 frames / 4.125 seconds at natural 24 fps**. Her head and attention remain down/away, her hands stay passive in her lap, and his established upper-arm grip persists.

Use once with full-image contain framing. No extra crop, retiming, looping, reversal or added hold is cleared. This is a source verdict, not adoption or an approval of the actual S046→S047→S048 cuts and fourth-plea song context. No unusable action/anatomy range was found within `[3,102)`; no partial salvage is needed. Head `[0,3)` and tail `[102,113)` were also inspected but are not additional approved coverage.

The [reviewed silent source](../assets/motion/ltx23-positive-corrections/R2S/R2S047/video-silent.mp4) is SHA-256 `ede1c44f5c74f57eee8afdb3852db03df567396e22b565d638618899b3eac688`: 113 frames, 896×512, 24 fps, 4.708333 seconds.

## Corrected reaction and contact

Her head remains bowed and angled down/away throughout all 113 frames. There is no chin lift or gaze rotation toward him, including the later half and return toward the endpoint. The returned mutual-facing look that failed [P1L09's proposed S047](ltx23-positive-P1L09-review.md) is absent. [Native gaze phases](ltx23-correction-R2S047-review/gaze-phases.jpg) show the source start, all main phases, selected endpoint and unused tail. Her head remains supported by her own neck; she does not rest it on him, recover, smile, reassure him or initiate contact.

Her lips part from roughly one-based f13 / 0.500 s, stay slightly open through the central phase, and settle back toward the initial shape by about f97–102 / 4.0–4.208 s. The small mouth opening and shoulder/head settling read as an exhausted exhale-like movement. This is a deviation from literally constant resting mouth shapes; it does not form repeated speech/singing shapes or turn into a response directed at him. The [native eye/mouth detail](ltx23-correction-R2S047-review/her-eyelid-detail.jpg) preserves it. Her eyes remain heavy and lowered, without a clearly demonstrated full blink. A separately countable breathing cycle in both people is not established and is not required for this scoped pass.

He keeps watching her with tense brows and a subdued mouth. His small head/shoulder adjustments remain coherent and worried; there is no broad outward scan, confident savior pose or collapse. Both bodies remain chair-supported. The quiet motion is visible in their faces, head positions, hair and shoulder/cloth settling; it is not merely a different encode of the guide.

His visible **bare hand stays on her outer upper arm** throughout. Thumb and curled fingers remain connected to the same sleeve/arm region. There is no release, point, regrip, fresh reach, pull, head pat, stroke or second embrace. His other hand remains on his own thigh, while her forearms and hands remain passive in her own lap. [Native contact/lap phases](ltx23-correction-R2S047-review/contact-lap-phases.jpg) show the entire performance and exact selection boundaries. The original grip hand is bare; silver ring detail belongs to his thigh-resting hand. Fine lines soften and lower fingers remain partly hidden at the native edge, so hidden anatomy is not certified. No new hand fusion, detachment or accessory transfer is visible.

## Identity and framing

Auburn hair, his light facial hair, both faces, wardrobe and pendants remain recognizable. Fine iris, freckles and finger linework vary in sharpness. There is no gross identity replacement, duplicated person, reflected double, detached neck or unexplained limb movement. The windows do not introduce a new character/reflection action.

Small composition/background drift remains; perfectly locked camera behavior is not established. His crown is tight near the native top edge and the lower hand/finger edges are tight below, as in the [original/fitted guide and actual endpoints](ltx23-correction-R2S047-review/guide-endpoints.jpg). This is limited source framing, not a newly missing skull or severed hand. The faces and upper-arm contact stay readable. Preserve the entire source image with contain scaling and add no further push or crop.

## Evidence and playback

I inspected all 113 decoded frames chronologically in full-sequence sheets, then native gaze/eye/mouth and contact/lap phases, guide/endpoints and actual browser captures. The compact [overview](ltx23-correction-R2S047-review/overview.jpg) and [S047 playback captures](ltx23-correction-R2S047-review/captured-S047-1.jpg) preserve the decision evidence. This is frame/capture inspection, not a claim of continuous human-equivalent visual perception.

Error-failing full decode, all 113 timestamps and the silent-stream check pass. Actual sandboxed Chromium **154.0.8037.57** playback ran at 1× and 672×384 without seeking. Runs used a unique local port/browser instance and the shared `build/source-review-playback.lock`:

| Playback | Frames | Media duration | Measured wall duration |
| --- | --- | --- | --- |
| Full source | 113 | 4.708333 s | 4.7285 s |
| Exact S047 trim proxy | 99 | 4.125000 s | 4.1441 s |

Both ended with **zero dropped/corrupt frames**, no media error, no stall and no waiting event. [Telemetry summary](ltx23-correction-R2S047-review/playback-summary.json) and [complete compressed callbacks](ltx23-correction-R2S047-review/playback-full.json.gz) retain source/proxy hashes and screenshot time bounds. These are silent clips; there is no subjective listening, original-song audio-sync or phoneme-sync claim.

[Checks](ltx23-correction-R2S047-review/checks.json) independently verify the actual source hash, all timestamps, identical fitted start/end pixels and all four guide records, including frame indices 0/112 at both stages. Original M01 endpoint is SHA-256 `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, 1916×1080.

[Comparison checks](ltx23-correction-R2S047-review/comparison-checks.json) confirm that seed 49, dimensions/rate, original and fitted guides, model lock, applied patches and step schedule match P1L09. Recorded environment settings differ only in available host memory. **Both the positive prompt and duration changed**: explicit whole-shot downward attention and 113 rather than 225 frames. The better result therefore does not isolate a single cause or prove that wording alone fixed the previous failure. The earlier P1L09 rejection remains frozen.

Reproduce with [reproduce.py](ltx23-correction-R2S047-review/reproduce.py), [retain_evidence.py](ltx23-correction-R2S047-review/retain_evidence.py) and [compare_settings.py](ltx23-correction-R2S047-review/compare_settings.py). Raw frames, full native sheets and the review proxy live in ignored `build/ltx23-correction-R2S047-review/`. No provider or Git operation was performed; production configuration and adoption records were not changed.
