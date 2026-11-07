# P2L08 — continued held-contact source review

7 November 2026. Independent animation/editor review under the retained Be Ambitious outside-review requirement. **PASS both intended intervals**, at natural 24 fps and full-image contain framing:

| Use | Zero-based source, end exclusive | One-based frames | Source seconds | Duration |
| --- | --- | --- | --- | --- |
| S042 | `[3,101)` | 4–101 | 0.125000–4.208333 | 98 frames / 4.083333 s |
| S043 | `[101,199)` | 102–199 | 4.208333–8.291667 | 98 frames / 4.083333 s |

These are consecutive, non-overlapping parts of one performance, proposed for master 199.708333–207.875000 seconds with the split at 203.791667. Preserve their natural continuity: no replay, loop, retiming, reverse, extra endpoint hold or additional crop is cleared. Actual insertion, adjacent cuts and original-song context need separate review.

The [reviewed silent source](../assets/motion/ltx23-positive-continuation/P2/P2L08/video-silent.mp4) is SHA-256 `2fd984ecef9bb36675d21ab595ec2b5c8f69e4a583131be424820dad0a5d6f17`: 209 frames, 896×512, 24 fps, 8.708333 seconds. All 209 frames, including handles, were inspected chronologically. The successful longer runtime is technical evidence for this completed take, not automatic acceptance of other takes.

## Contact, expression and deviations

His bare grip hand maintains the established outer-upper-arm contact throughout all 209 frames. It follows her slight shoulder changes while remaining attached to the same sleeve area. Finger contours soften through the middle but remain a plausible curled grip, with no release, point, regrip, new reach, pull, stroke, head pat or second embrace. His other hand stays on his own thigh. The ring belongs to that thigh hand, not the supporting hand; it becomes partly hidden by the native lower crop through the middle and reappears as the composition returns. Her hands stay passive in her own lap. Both bodies stay seated and both heads self-supported. [Contact phases](ltx23-positive-P2L08-review/contact-phases.jpg) and [lap phases](ltx23-positive-P2L08-review/lap-phases.jpg) preserve the visible limits rather than claiming complete hidden-finger anatomy.

The main deviation is his **coherent anxious outward look**. Beginning around f13–21 / 0.5–0.833 seconds, his chin rises and his head rotates away from watching her. By roughly f33–37 / 1.333–1.5 seconds, his gaze is outward toward picture left, with raised inner brows and a slightly parted mouth. That frightened attention persists through roughly f80–85 / 3.292–3.5 seconds. He then lowers his gaze/head and turns back toward her, substantially returning by about f133 / 5.5 seconds. The mouth opens somewhat more near 2.3–3.0 seconds before settling; it does not present a repeated syllabic performance. This exceeds the requested small inhalation and jaw tightening, but remains plausible anxious checking, consistent in kind with the [accepted R1L05 deviation](ltx23-correction-R1L05-review.md). It is not a confident rescue pose, reassurance from her, or an anatomical snap. Its motivation within the song remains an edit-context question. [Native gaze phases](ltx23-positive-P2L08-review/gaze-phases.jpg) retain the change explicitly.

She remains depleted, looking down and away throughout. Near f181–183 / 7.5–7.583 seconds her eyelids are closed; they reopen through approximately f189–193 / 7.833–8.0 seconds. The [native eyelid sequence](ltx23-positive-P2L08-review/eyelid-phases.jpg) establishes this brief tired blink. His lids narrow during the downward return, but a distinct full blink is not established. Neither character provides a confidently separable, naturally uneven breath cycle; do not substitute the generated head/torso movement for verified respiration. No smile, reciprocal gaze, new head rest, emotional cure or role reversal occurs.

Both identities, auburn hair, his light facial hair, clothes and pendants remain recognizable. Fine facial/accessory detail varies and the grip is softer in the middle, without gross identity replacement or disconnected anatomy. Small camera/background drift remains; his raised hair grazes/clips the native top edge, and the native lower edge obscures distal lap fingers. These inherited/animated framing limits are visible at ordinary size. Preserve the complete image with contain scaling; the source is not cleared for a tighter crop or added push.

## Source boundaries

At S042→S043, source f101 is immediately followed by f102; the downward head return, grip and background continue without a restart. The [native consecutive boundary](ltx23-positive-P2L08-review/continuous-boundary.jpg) supports using both successive ranges once.

The preceding [P2L07](ltx23-positive-P2L07-review.md) selected f99 and this take's first selected f4 retain compatible seated poses, held contact, lap hands and downward attention. **PASS source-pose compatibility**, with a small generation-to-generation face/linework and background-position reset visible in the [boundary sheet](ltx23-positive-P2L08-review/source-boundary.jpg). This is not approval of S041→S042 or any other actual edit cut. Rendered scale, exposure, cadence and song context still require a new sequence review.

## Verification and actual playback

Error-failing full decode, all 209 timestamps, 24 fps cadence, dimensions and zero audio streams passed. [Checks](ltx23-positive-P2L08-review/checks.json) retain source/render/guide/provenance hashes, exact manifest equality with the take template and selected proxy hashes. Original M01 endpoint SHA-256 `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10` matches both inputs; fitted start/end pixels and all four guide records match. [Guide/endpoints](ltx23-positive-P2L08-review/guide-endpoints.jpg) preserve that evidence. The [old quiet L05 release/point/regrip failure](ltx23-quiet-L05-review.md) was checked as a specific failure to look for, not attributed to this new source.

Actual sandboxed Chromium 154.0.8037.57 played the source and both review-only trims at 1×, 672×384, without seeking:

| Playback | Frames | Media duration | Wall duration | Dropped / corrupt |
| --- | --- | --- | --- | --- |
| Full source, captured | 209 | 8.708333 s | 8.7220 s | 0 / 0 |
| S042, captured | 98 | 4.083333 s | 4.1077 s | 0 / 0 |
| S043, captured | 98 | 4.083333 s | 4.0970 s | 3 / 0 |
| S043, serialized capture-free confirmation | 98 | 4.083333 s | 4.1085 s | 0 / 0 |

All runs ended without media error, stall or waiting event. The initial three presentation drops are preserved in the [captured-run summary](ltx23-positive-P2L08-review/playback-summary.json); a separate run under the shared playback lock removed screenshot work and completed with zero drops ([confirmation](ltx23-positive-P2L08-review/playback-capture-free-summary.json)). This does not retrospectively change the initial run or attribute its cause conclusively. Full decoded frames remained available for visual review regardless of browser presentation.

I inspected the complete chronological sequence, native face/contact/lap details, guide/endpoints, boundary frames and actual [S042](ltx23-positive-P2L08-review/captured-S042-1.jpg) / [S043](ltx23-positive-P2L08-review/captured-S043-1.jpg) captures. This is instrumented playback plus frame/capture inspection, not continuous human-equivalent visual perception, subjective hearing, audio sync or phoneme-sync verification. Both source and proxies are silent.

Reproduce using [reproduce.py](ltx23-positive-P2L08-review/reproduce.py) under `flock build/source-review-playback.lock` from the repository root. [confirm_playback.py](ltx23-positive-P2L08-review/confirm_playback.py), under the same lock, repeats only the capture-free S043 check and preserves initial telemetry. Both require the existing NumPy/Pillow/FFmpeg/Playwright/Chromium environment and write to this take's ignored build directory. After both take reproductions, [the compact-evidence script](ltx23-positive-P2L07-review/retain_evidence.py) verifies the hashes and rebuilds the retained folders. No provider, source, production configuration or approval manifest was changed.
