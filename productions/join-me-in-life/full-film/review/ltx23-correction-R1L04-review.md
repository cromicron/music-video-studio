# R1L04 — quiet waiting correction source review

7 November 2026. Independent animation/editor review under the retained Be Ambitious outside-review requirement. This completes the interrupted review; its saved technical evidence was not a prior acceptance.

**PASS the exact S019 source interval `[3,135)`**, zero-based and end-exclusive: one-based frames 4–135, source 0.125–5.625 seconds, **132 consecutive frames / 5.5 seconds at natural 24 fps**. Use once with full-image contain framing. No loop, retiming, reversal, added hold or enlarged close-up is cleared. The exact insertion, preceding/following cuts and original-song playback remain separate gates.

The [reviewed silent source](../assets/motion/ltx23-quiet-corrections/R1W/R1L04/video-silent.mp4) is SHA-256 `664552573bc9da7d8c4da90bbf9978f80c3eb45435be4d3336ffb03270d51e51`, 145 frames, 896×512, 24 fps, 6.041667 seconds. This verdict does not rehabilitate the [original L04](ltx23-quiet-L04-review.md), whose hand-to-mouth/palm/forward-address performance remains rejected.

## What the correction actually does

Both characters remain separately seated throughout all 145 frames. Their forearms stay directed into their own laps; the intervening chair/body gap remains. Neither arm rises, crosses the gap or initiates contact. There is no hand-to-mouth motion, offered palm, new embrace, point or head support by the other person. **The native lower edge cuts off most fingers and lap contact**, so this verifies the visible forearm/resting support and absence of a gesture, not unseen finger anatomy. His visible wrist/hand tops remain at the lower edge; her striped sleeves stay down and attached.

His inward, tense brow and attention toward her survive the full keeper. He makes a small head/neck adjustment and his lips part slightly before settling. He does not turn to address the viewer or become reassuring/confident. She keeps her head inclined and gaze down and away, with slow eyelid narrowing and reopening, a small head/shoulder settling and slight hair/clothing movement. Her lowered-eye phase is most apparent around 1–3.5 seconds. She does not smile, answer him, comfort him or appear cured. The [native face phases](ltx23-correction-R1L04-review/face-phases.jpg) show this progression.

This is restrained real character motion rather than a repeated still or a camera-only move. It is also **less specific than the prompt**: a complete brief blink by him is not established, her eyelid change is sustained, and a separately identifiable natural breathing cycle cannot be confidently isolated from the small pose changes. His slight mouth opening is not literal adherence to an unchanged resting mouth. Those limits do not undermine the quiet, frightened waiting action required for this slot; do not describe the take as a verified breathing/blinking demonstration or lip-synced speech.

The composition is much steadier than the rejected acting take. Fine background/linework drift remains; it is not a pixel-locked plate. Faces, necks, shoulders and lowered forearms remain coherent, with no identity switch, floating head, extra limb or obvious body detachment. Auburn hair, light facial hair, wardrobe and pendants remain recognizable. Fine facial/iris/accessory detail softens during motion; exact freckles or colour invariance are not certified. His crown has little native clearance and the hands are already cut by the lower edge, so preserve the whole image and do not add a timeline push/crop. The inspected head/tail handles show no new gross failure, but this acceptance is limited to the stated interval.

## Evidence and playback

I inspected every decoded frame chronologically in all-frame sheets, then the native face/full-frame phases and three captures from the running keeper. The compact [overview](ltx23-correction-R1L04-review/overview.jpg), [native phases](ltx23-correction-R1L04-review/native-phases.jpg) and keeper captures at [1.5 s](ltx23-correction-R1L04-review/keeper-playback-1.50.jpg), [3.5 s](ltx23-correction-R1L04-review/keeper-playback-3.50.jpg) and [4.5 s](ltx23-correction-R1L04-review/keeper-playback-4.50.jpg) retain the decisive phases. Chronological frame/capture inspection is not a claim of continuous human-equivalent viewing.

The interrupted review had already completed error-failing full decode, frame count, source/guide checks and actual sandboxed Chromium **154.0.8037.57** playback at 1×, native 896×512, without seeking. I recovered that evidence and revalidated the actual source/proxy hashes instead of rerunning completed successful checks. All runs ended; no corrupt frame or media error was reported.

| Playback | Frames | Media / wall seconds | Dropped frames | Other playback events |
| --- | --- | --- | --- | --- |
| Full, with captures | 145 | 6.041667 / 6.0592 | 1 | No wait or stall |
| Keeper, with captures | 132 | 5.500000 / 5.6218 | 6 | One `waiting`/`playing` pair near 4.562 s |
| Full, without captures | 145 | 6.041667 / 6.0610 | 0 | No wait or stall |
| Keeper, without captures | 132 | 5.500000 / 5.5143 | 0 | No wait or stall |

The clean uncaptured runs establish uninterrupted technical playback; they do not erase the screenshot-run drops. See [full captured telemetry](ltx23-correction-R1L04-review/playback-summary.json), [keeper captured telemetry](ltx23-correction-R1L04-review/keeper-playback-summary.json), [full uncaptured telemetry](ltx23-correction-R1L04-review/uncaptured-playback-summary.json), [keeper uncaptured telemetry](ltx23-correction-R1L04-review/keeper-uncaptured-playback-summary.json), [resumed hash verification](ltx23-correction-R1L04-review/resume-verification.json) and [source checks](ltx23-correction-R1L04-review/checks.json). There is no audio stream: no subjective listening, audio sync or phoneme-sync claim is made here.

[Comparison checks](ltx23-correction-R1L04-review/comparison-checks.json) confirm unchanged seed 49, dimensions, frame count/rate, source/endpoint hashes, fitted pixels, guide records, conditioning and recorded step schedule against original L04. Positive wording changed; measured elapsed times naturally differ. This is evidence for this corrected take, not proof that wording alone will solve every later shot.

Reproduce raw evidence with [reproduce.py](ltx23-correction-R1L04-review/reproduce.py), then [playback_check.py](ltx23-correction-R1L04-review/playback_check.py) with the original four combinations of `--keeper` and `--uncaptured`. [verify_resume.py](ltx23-correction-R1L04-review/verify_resume.py) verifies the recovered playback files and both correction comparison records. Raw frames/callbacks and review-only trim remain in ignored `build/ltx23-correction-R1L04-review/`; no provider, production configuration or approval record was changed by this review.
