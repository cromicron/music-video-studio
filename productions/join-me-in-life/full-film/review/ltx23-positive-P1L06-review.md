# P1L06 — later held-contact source review

7 November 2026. Independent source review under the retained Be Ambitious outside-review gate. **PASS both exact proposed intervals**, at natural 24 fps with full-image contain framing.

| Intended use | Zero-based, end-exclusive source frames | One-based frames | Source seconds | Judgment |
| --- | --- | --- | --- | --- |
| S033 | `[3,102)` | 4–102 | 0.125000–4.250000 | **PASS**, 99 frames / 4.125 s |
| S034 | `[102,198)` | 103–198 | 4.250000–8.250000 | **PASS**, 96 frames / 4.000 s |

These are successive parts of one coherent performance, with no overlap, repeat or missing source frame. Use each once. No additional crop, retiming, reversal, loop or endpoint hold is cleared. This verdict is about the source; the actual S032→S033 join from accepted R1L05, S033→S034 framing and outgoing edit cuts still require separate review with the original song.

The [reviewed silent source](../assets/motion/ltx23-positive-continuation/P1/P1L06/video-silent.mp4) is SHA-256 `7f411bf2fde1955369b2856cd7542d3ef8dd488680483537a62ee01ae11aa8ac`: 209 frames, 896×512, 24 fps, 8.708333 s. No unusable action/anatomy interval was found inside either proposed selection. The unused head `[0,3)` and tail `[198,209)` were inspected, but are not extra approved coverage. No partial salvage is needed.

## Contact and acting

His visible bare hand maintains its grip on her outer upper arm through the entire take. Thumb and curled fingers stay at the sleeve/arm contact while her shoulder shifts slightly; there is no release, pointing finger, regrip, reach, stroke, head pat, pull or second embrace. His other hand remains on his own thigh. Her forearms stay lap-directed and her hands remain passive in her own lap. Both heads remain self-supported, with no collapse, head rest or kiss. [Native contact/lap phases](ltx23-positive-P1L06-review/contact-lap-phases.jpg) include both selection boundaries, the central motion and the tail.

The grip hand is bare in the original M01 guide as well. The silver ring detail belongs to his other, thigh-resting hand; it becomes partly hidden by the native lower image edge during the central phase and reappears later. That is not evidence of a missing ring on the grip hand. Fine finger lines soften, and hidden lower fingers cannot be certified, but no new fused or disconnected hand shape is visible.

He lifts and rotates his head outward from about one-based f17 / 0.667 s, looks anxiously past picture left/front through approximately f80–85 / 3.3–3.5 s, then lowers his head and returns toward her by roughly f121–133 / 5.0–5.5 s. His brows stay raised inward/tense and his mouth is slightly parted at the height of the check. This is a coherent frightened check and inward pause, consistent with the scoped deviation already accepted in [R1L05](ltx23-correction-R1L05-review.md); it is not literal uninterrupted watching of her. It does not become confident reassurance, singing or a new interaction. His eyes visibly close during the lowering around f93–108, rather than supplying only the prompt's chest-breath movement. See [native head/eye phases](ltx23-positive-P1L06-review/gaze-eyelid-phases.jpg).

She stays depleted and down/away throughout both intervals. Her eyelids lower gradually, remain narrowed/closed-looking for an extended phase, and reopen late; do not market this as one clearly isolated brief tired blink. [Native eyelid detail](ltx23-positive-P1L06-review/her-eyelid-detail.jpg) preserves that limitation. Small hair, head, shoulder and cloth changes are real; a separately countable shallow-breath/exhale cycle is not established. No smile, returned reassuring gaze, reversal of comfort or recovery appears.

## Framing and identity

The drawn identities, auburn hair, his light facial hair, black wardrobe and pendants remain recognizable. Fine iris/freckle/finger linework varies in sharpness; no gross identity substitution, duplicated body or neck break appears. The head turn exposes different facial angles coherently.

There is mild generated composition/background drift, so the locked-camera prompt is not perfectly met. During the raised-head phase his crown approaches/grazes the native upper border, and lap/thigh fingers are tight at the bottom. The [original/fitted guide and actual endpoints](ltx23-positive-P1L06-review/guide-endpoints.jpg) show that edge tightness already belongs to this source setup; the changing visibility accompanies the head/pose motion rather than a new missing skull or detached fingers. Faces and upper-arm contact remain readable. Preserve the whole 896×512 image with contain scaling; do not amplify the tight framing with another crop or push.

## Evidence, playback and limits

I inspected all 209 decoded frames chronologically in full-sequence sheets, then native face/grip/lap phases, guide/endpoints and screenshots captured while actual playback continued. [Overview](ltx23-positive-P1L06-review/overview.jpg), [S033 captures](ltx23-positive-P1L06-review/captured-S033-1.jpg) and [S034 captures](ltx23-positive-P1L06-review/captured-S034-1.jpg) preserve the decision evidence. This is frame/capture inspection, not a claim of continuous human-equivalent visual perception.

Error-failing full decode, all frame timestamps and the silent-stream check pass. Sandboxed Chromium 154.0.8037.57 played the full source and both trim proxies at 1×, displayed at 672×384, without seeking:

| Run | Frames | Media duration | Measured wall duration | Dropped frames |
| --- | --- | --- | --- | --- |
| Full source, capture run | 209 | 8.708333 s | 8.7376 s | 0 |
| S033, capture run | 99 | 4.125000 s | 4.1437 s | 0 |
| S034, capture run | 96 | 4.000000 s | 4.0207 s | 1 |
| S034, one capture-free replay | 96 | 4.000000 s | 4.0109 s | 0 |

Every run ended with zero corrupt frames and no media error, stall or waiting event. The first S034 presentation drop occurred during concurrent screenshot playback; it remains in the record. One replay without screenshots, serialized under the shared playback lock, completed cleanly. [Capture telemetry summary](ltx23-positive-P1L06-review/playback-summary.json), [complete compressed callbacks](ltx23-positive-P1L06-review/playback-full.json.gz) and [capture-free replay](ltx23-positive-P1L06-review/S034-capture-free-playback.json) bind this evidence to the actual source/proxy hashes. The clips are silent; no listening, audio-sync or phoneme-sync claim is made.

[Checks](ltx23-positive-P1L06-review/checks.json) independently verify source and guide hashes, all 209 timestamps, identical fitted start/end pixels and all four guide records. Original M01 endpoint SHA-256 is `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, 1916×1080. Correct guide records do not themselves establish intermediate motion quality; the [earlier quiet L05 failure](ltx23-quiet-L05-review.md) remains rejected in its later interval.

Reproduce with [reproduce.py](ltx23-positive-P1L06-review/reproduce.py), then [retain_evidence.py](ltx23-positive-P1L06-review/retain_evidence.py); the separate [capture-free script](ltx23-positive-P1L06-review/playback_capture_free.py) repeats only S034 when needed. Raw frames, native full sheets and proxies live in ignored `build/ltx23-positive-P1L06-review/`. No provider operation, edit configuration or adoption record was changed by this review.
