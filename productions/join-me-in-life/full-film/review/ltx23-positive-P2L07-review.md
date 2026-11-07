# P2L07 — quiet held-contact source review

7 November 2026. Independent animation/editor review under the retained Be Ambitious outside-review requirement. **PASS S041 source `[3,99)`**, 96 consecutive frames / 4.000000 seconds, at natural 24 fps with full-image contain framing. This is one-based f4–99, source 0.125000–4.125000 seconds, proposed for master 195.708333–199.708333 seconds. No crop, retiming, replay, reverse or extra endpoint hold is cleared. Exact insertion, adjoining cuts and original-song context still require separate review.

The [reviewed silent source](../assets/motion/ltx23-positive-continuation/P2/P2L07/video-silent.mp4) is SHA-256 `c6b99b860c588e5eb7e1aa7b8dd14d7b02500f7964e1b8548dd7e4d6e66c160b`: 105 frames, 896×512, 24 fps, 4.375 seconds. All 105 frames, including the unselected handles, were inspected chronologically. This report makes no provider call or adoption/configuration change.

## Contact and quiet acting

His bare grip hand stays on the same outer-upper-arm region throughout. Thumb, curled fingers and sleeve remain connected as her shoulder makes small settling movements. There is no new reach, release, point, regrip, squeeze/pull, head pat or embrace. His other hand remains on his own thigh; its silver ring remains visible where the native lower edge permits. Her hands stay passive together in her own lap. Both heads remain self-supported and both bodies chair-supported, without a head rest or reversed comfort role. [Native contact phases](ltx23-positive-P2L07-review/contact-phases.jpg) and [lap phases](ltx23-positive-P2L07-review/lap-phases.jpg) retain those distinctions.

She remains withdrawn, with lowered eyes directed away from him. Her head subtly rises/settles, her eyelids change a little, and her mouth parts slightly around the middle before returning toward its depleted resting shape. He watches her with tense brows and restrained head/face changes. These small movements are readable quiet acting, not a fresh interaction or recovery. There is no reassuring smile, reciprocal attention or confident-savior pose. The slight mouth change departs from the prompt's fixed resting shape but does not form a repeated talking/singing performance. [Native face phases](ltx23-positive-P2L07-review/gaze-phases.jpg) preserve the actual change.

A fully shut blink or an independently isolatable breath-pause/exhale cycle is **not established**. Subtle shoulder, hair and head motion exists, but it should not be advertised as literal compliance with every breath instruction. The absence of a full blink is not an acceptance failure for this quiet passage.

Identities, auburn hair, his light facial hair, black clothing, her striped sleeves and pendants remain recognizable. Fine freckles, iris detail and finger/ring linework soften or vary slightly; unseen distal fingers below the native image cannot be certified. No gross face replacement, extra limb or detached support appears. The crown and lower fingers remain tight in the inherited composition. Small background/linework drift prevents a claim of a perfectly locked camera, but there is no disruptive push/pull. Preserve the complete image; this is not approval for a larger close-up.

## Adjacent source compatibility

The selected final P2L07 frame is zero-based 98 / one-based f99. Compared with P2L08's selected first frame, zero-based 3 / f4, the seated arrangement, held arm, lap hands and downward attention are compatible: no new action is needed to bridge the poses. The [native boundary sheet](ltx23-positive-P2L08-review/source-boundary.jpg) also shows a small face/linework and background-position reset between independent generations. **PASS pose compatibility only**; this does not approve the exact S041→S042 cut. The actual full-image insertions, scale, exposure and movement on each side must be reviewed in the assembled edit. [P2L08 has its own source verdict](ltx23-positive-P2L08-review.md).

## Verification and playback limits

Error-failing FFmpeg decode, all 105 timestamps, dimensions/rate and absence of audio passed. [Checks](ltx23-positive-P2L07-review/checks.json) retain source/render/guide/provenance hashes, exact object equality with the submitted take template, segment/proxy hashes and all timestamps. Original M01 endpoint SHA-256 `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, 1916×1080, matches both manifest inputs; fitted start/end RGB is identical and all four guide records match. [Guide/endpoints](ltx23-positive-P2L07-review/guide-endpoints.jpg) show the actual result. Matching guides alone are not the basis for this contact verdict; the [older L05 failure](ltx23-quiet-L05-review.md) and [accepted R1L05 correction](ltx23-correction-R1L05-review.md) were read before judging these frames.

Actual sandboxed Chromium 154.0.8037.57 ran the silent source and review-only trim at 1×, 672×384, without seeking:

| Playback | Frames | Media duration | Wall duration | Dropped / corrupt |
| --- | --- | --- | --- | --- |
| Full source | 105 | 4.375000 s | 4.3932 s | 0 / 0 |
| S041 proxy | 96 | 4.000000 s | 4.0068 s | 0 / 0 |

Both ended with no media error, stall or waiting event. [Telemetry summary](ltx23-positive-P2L07-review/playback-summary.json) retains capture time bounds and the raw telemetry hash. I inspected the complete chronology, native face/hand phases, full frames, guides and [ordinary-size playback captures](ltx23-positive-P2L07-review/captured-S041-1.jpg). Instrumented playback plus those visual inspections is not continuous human-equivalent perception, subjective listening, audio sync or phoneme-sync verification; these files are silent.

Reproduce from the repository root with `flock build/source-review-playback.lock python3 productions/join-me-in-life/full-film/review/ltx23-positive-P2L07-review/reproduce.py`. The [script](ltx23-positive-P2L07-review/reproduce.py) uses NumPy, Pillow, FFmpeg, Playwright and `/usr/bin/chromium`, writing raw evidence only to its own ignored build directory. After both take scripts complete, [retain_evidence.py](ltx23-positive-P2L07-review/retain_evidence.py) verifies hashes and rebuilds both compact folders. No source was modified or generated for this review.
