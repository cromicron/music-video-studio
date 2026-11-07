# L05 quiet held-contact source review — 7 November 2026

**Retain the intended S030 portion as a source keeper with a camera limitation; reject S032 and the complete take for continuous held contact.** The earlier portion contains a readable tired blink without releasing her arm. Later, his supporting hand leaves her upper arm, points outward, and regrips. This is a new action that interrupts the established embrace, visible at ordinary viewing size. This report recommends source selection only; no actual timeline insertion or approval manifest was changed.

| Proposed use | Zero-based source frames, end exclusive | Source time | Editorial judgment |
| --- | --- | --- | --- |
| S030, master 146.916667–151.000000 s | [3,101), 98 frames | 0.125000–4.208333 s | Usable quiet eye closure and held contact, with conspicuous camera push-in/pull-back. Review the actual wide crop and joins before adoption. |
| S032, master 155.166667–159.166667 s | [101,197), 96 frames | 4.208333–8.208333 s | Reject: release, outward point, regrip and inward head lean. |
| Whole take | [0,201), 201 frames | 0.000000–8.375000 s | Reject as an uninterrupted held-contact performance. |

These proposed ranges are adjacent in the source, with no overlap or replay. Their technical validity does not rescue the second range's acting.

## What is visible

In S030, his hand stays on her outer upper arm; fingers remain legible as a grip rather than merging into her body. Her arms stay lap-directed, with passive hands when the framing shows them. Both bodies remain seated and both heads supported by their own necks. There is no new pull, embrace, stroke or head pat. She remains depleted and looks down and away; he remains concerned. No smile, reassured look toward him, role reversal or sudden recovery appears.

Her eye closure is real motion: one-based f60–69 (about 2.458–2.833 s) show closed eyelids, followed by a gradual reopening through approximately f79/3.250 s. The [native blink phases](ltx23-quiet-L05-review/blink-phases.jpg) distinguish this from a merely different encode. Small face, hair and clothing changes accompany it. **Clearly separable, naturally uneven breathing is not established:** camera enlargement and contraction dominate the apparent torso motion. No grotesque swelling or respiratory snap appears, but calling this a demonstrated breathing performance would overstate the evidence.

The camera visibly pushes in and then pulls back, including during S030. Background geometry scales with the actors. At the tighter phase his hair crown is cut off and her lap passes below the frame; the useful faces and supporting hand remain visible. The shot is readable as a moving two-shot, but it fails the locked-camera request. Hidden lap fingers cannot be certified. Any new timeline camera move must be checked against this baked-in movement.

The blocking change begins around f112/4.625 s. By f115/4.750 s his hand has lifted away. The index points outward clearly by f121/5.000 s and remains extended through approximately f147/6.083 s. He retracts and regrips around f154–155/6.375–6.417 s. Treat approximately [4.625,6.500) s as the release/gesture/regrip region, not a permissible finger adjustment. See [native contact phases](ltx23-quiet-L05-review/contact-phases.jpg) and the [S032 playback captures](ltx23-quiet-L05-review/captured-S032-1.jpg). Finger linework becomes softer during this gesture, but the decisive failure is the action itself.

He also inclines toward her hair while she keeps her eyes closed, then withdraws toward the starting composition. There is no clear kiss or head resting on his chest; nevertheless, this is a fresh interaction rather than quiet persistence. The tail restores the guide-like pose without terminal collapse. The remaining short fragments do not supply a replacement four-second S032 at natural speed.

Relative to the original M01 endpoint and fitted guide, both identities, auburn hair, his light facial hair, clothing and pendants remain recognizable. Fine freckles, iris detail and ring/finger linework are softer or variable, especially during the rejected gesture; this is not a claim of exact accessory or eye-colour invariance. There is no gross face replacement or detached head. The tired expression changes are not themselves identity failures.

## Evidence and limits

The reviewed silent MP4 is SHA-256 `ec9411f32060e3d2b5cd3ae53aedc09da552bc9c48004a1c62c7d3099cc15617`: 201 frames, 24 fps, 896×512. All 201 native frames were inspected chronologically, with additional face/contact details, guide/endpoints and ordinary-size playback captures. Error-failing full decode and all 201 frame timestamps passed; there is no audio stream.

Actual sandboxed Chromium 154.0.8037.57 playback ran at 1× and 672×384, without seeking, for the full take and both review-only trim proxies:

| Playback | Frames | Media duration | Measured wall duration | Dropped/corrupt frames; playback errors/stalls/waits |
| --- | --- | --- | --- | --- |
| Full take | 201 | 8.375000 s | 8.3989 s | 0 / 0; none |
| S030 selection | 98 | 4.083333 s | 4.1482 s | 0 / 0; none |
| S032 selection | 96 | 4.000000 s | 4.0097 s | 0 / 0; none |

[Telemetry](ltx23-quiet-L05-review/playback.json) records actual callbacks and the before/after time bounds of screenshots taken while playback continued. I inspected those captured phases and the complete native sequence; this is not a claim of human continuous perception, subjective listening or phoneme sync. The clips are silent. [S030 captures](ltx23-quiet-L05-review/captured-S030-1.jpg) show the usable earlier performance; the three full-take capture sheets are retained alongside them.

[Checks](ltx23-quiet-L05-review/checks.json) independently verify original M01 endpoint SHA-256 `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`, native 1916×1080, identical fitted start/end pixels, and matching guide records at both generation stages. [Guide versus actual endpoints](ltx23-quiet-L05-review/guide-endpoints.jpg) shows the result. Identical endpoint guidance demonstrably did not preserve contact in the middle.

The completed 201-frame technical trial does not validate unchanged longer Q2/Q3 held-contact requests. L05 offers one bounded quiet source keeper and a concrete middle-action failure; it does not establish that every longer generation must fail. Review other takes independently and change the control hypothesis before using this result to justify a larger held-contact batch. Actual S030 insertion, neighbouring cuts and full-song continuity remain unreviewed here.

Reproduction: run `python3 productions/join-me-in-life/full-film/review/ltx23-quiet-L05-review/reproduce.py` from the repository root in the existing environment with NumPy, Pillow, FFmpeg, Playwright and `/usr/bin/chromium`. It writes raw frames, full sheets, review proxies and playback evidence only to ignored `build/ltx23-quiet-L05-review/`; it makes no provider call. [Source script](ltx23-quiet-L05-review/reproduce.py). Portable evidence is a compact selection, not the full raw-frame cache.
