# R1L05 — sustained contact correction source review

7 November 2026. Independent animation/editor review under the retained Be Ambitious outside-review requirement. This completes the interrupted review; its saved technical evidence was not a prior acceptance.

**PASS both intended source intervals**, at natural 24 fps with full-image contain framing:

| Use | Zero-based, end-exclusive source frames | One-based frames | Source seconds | Duration |
| --- | --- | --- | --- | --- |
| S030 | `[3,101)` | 4–101 | 0.125–4.208333 | 98 frames / 4.083333 s |
| S032 | `[101,197)` | 102–197 | 4.208333–8.208333 | 96 frames / 4.000000 s |

These are successive, non-overlapping parts of one performance. Use each once; no loop, retiming, reversal, extra endpoint hold or enlarged close-up is cleared. S031 intervenes in the edit, so source continuity does not automatically approve those actual cuts. Review the exact placements and original-song playback separately.

The [reviewed silent source](../assets/motion/ltx23-quiet-corrections/R1H/R1L05/video-silent.mp4) is SHA-256 `0a8e44b2dbc7c5038ecc0667214aae0375b3f0e2e5320fc7996a1f00ea3be24b`, 201 frames, 896×512, 24 fps, 8.375 seconds. The [original L05](ltx23-quiet-L05-review.md) retains its earlier limited S030 acceptance and rejected later release/point/regrip; this is a new source verdict.

## Contact, performance and framing

His visible hand maintains the pictured grip on her outer upper arm throughout all 201 frames. The thumb and curled fingers remain attached to the same sleeve/arm region while her shoulder settles. The arm stays behind her. There is **no release, outward index point, regrip, new reach/pull, stroke or second embrace**, including the former failure region around one-based f112–155 / 4.625–6.417 seconds. The [native contact phases](ltx23-correction-R1L05-review/contact-phases.jpg) cover that region. His other hand stays on his own thigh; her forearms and hands remain passive in her lap. The lower native edge partly clips their lower fingers and intermittently obscures his ring, so hidden fine anatomy cannot be certified. Both bodies remain chair-supported and both heads self-supported; there is no head rest, kiss, collapse or duplicated person.

The principal prompt deviation is a coherent **outward head/gaze check**. Starting around f17 / 0.667 s, he raises his chin and rotates away from looking down at her toward an offscreen point to picture left. The outward orientation is clear by f25 / 1 s, persists through roughly f80 / 3.292 s, and then returns; by f109–113 / 4.5–4.667 s he is looking down toward her again. He does not maintain the prompt's uninterrupted watch of her. His lifted inner brows, slightly parted mouth and tense face still read as frightened concern, not a confident savior or a direct-address performance. The [native gaze phases](ltx23-correction-R1L05-review/gaze-phases.jpg) retain this deviation explicitly. Accept it as anxious checking for this source, while checking its motivation and screen direction in the actual cut.

She remains depleted, looking down and away rather than back at him or at the viewer. Small head, shoulder, hair and eyelid changes are visible; her eyelids narrow further around 3.5–4.3 s and reopen. **A fully shut brief blink is not established**, and neither character supplies a confidently isolatable breathing cycle. The [eyelid detail](ltx23-correction-R1L05-review/eyelid-phases.jpg) prevents the old take's clearer blink from being attributed to this correction. Real quiet motion exists in the head turn/return and her restrained settling; do not advertise literal blink/breath-prompt compliance. There is no smile, reassurance from her, reversed emotional role or recovery resolution.

The former large push-in/pull-back is absent. Small background/composition drift and softened linework remain; this is not a perfectly locked camera. His raised crown grazes the native upper edge during the outward look and the lap/fingers are tight below. Preserve the entire image with contain scaling and add no crop or push. Faces and the supporting hand remain readable. Auburn hair, light facial hair, clothing and pendants remain recognizable throughout; fine freckles, iris, ring and finger lines vary in sharpness. There is no gross identity replacement or anatomical break. The tail returns toward the established pose without a terminal collapse, but the acceptance stops at source frame 197 as specified.

## Evidence and playback

I inspected every decoded frame chronologically in full-sequence sheets, then native full frames, contact, face/gaze and eyelid phases, guide/endpoints and actual browser captures. The compact [overview](ltx23-correction-R1L05-review/overview.jpg), [guide/endpoints](ltx23-correction-R1L05-review/guide-endpoints.jpg), [S030 captures](ltx23-correction-R1L05-review/captured-S030-1.jpg) and [S032 captures](ltx23-correction-R1L05-review/captured-S032-1.jpg) preserve the decision evidence. This is frame/capture inspection, not a claim of continuous human-equivalent visual perception.

The interrupted review had already completed error-failing full decode, all 201 timestamp checks, guide verification and actual sandboxed Chromium **154.0.8037.57** playback at 1×, displayed at 672×384 without seeking. I recovered these completed runs, checked their source/proxy hashes, and finished the visual verdict instead of repeating successful playback. All three ended with zero dropped/corrupt frames, no media error, no stall and no waiting event:

| Playback | Frames | Media duration | Measured wall duration |
| --- | --- | --- | --- |
| Full source | 201 | 8.375000 s | 8.3931 s |
| S030 proxy | 98 | 4.083333 s | 4.0978 s |
| S032 proxy | 96 | 4.000000 s | 4.0129 s |

[Compact telemetry](ltx23-correction-R1L05-review/playback-summary.json) retains run/capture time bounds, frame counts and the raw evidence hash; complete callbacks remain in the ignored cache. [Checks](ltx23-correction-R1L05-review/checks.json) retain exact source/proxy/guide hashes, dimensions, every timestamp and the identical fitted start/end verification. The original M01 endpoint is SHA-256 `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, 1916×1080. Identical guide records do not by themselves establish the observed contact preservation. The clips are silent; there is no subjective listening, audio-sync or phoneme-sync claim.

[Comparison checks](ltx23-correction-R1L05-review/comparison-checks.json) confirm unchanged seed 49, dimensions, frame count/rate, source/endpoint hashes, fitted pixels, guides, conditioning and recorded step schedule against original L05. Positive wording changed; measured elapsed times differ. The successful corrected contact is evidence for these two ranges, not automatic approval of other held-contact generations or longer runtimes.

Reproduce the source checks, native sheets, trim proxies and browser telemetry with [reproduce.py](ltx23-correction-R1L05-review/reproduce.py). Then [retain_evidence.py](ltx23-correction-R1L05-review/retain_evidence.py) verifies source/proxy hashes and rebuilds compact evidence from ignored `build/ltx23-correction-R1L05-review/`. The companion [resume verification script](ltx23-correction-R1L04-review/verify_resume.py) writes both correction comparison records. No provider, production configuration or approval record was changed by this review.
