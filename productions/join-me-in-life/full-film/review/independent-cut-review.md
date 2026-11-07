# Independent review of the full-song animatic

> Latest follow-up: the repaired export with SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb` was independently checked below. All three specific composition/continuity defects reported in the earlier encode are now closed. The finished-animation target remains unmet. Earlier contact sheets retain their original encode provenance.

Reviewed 6 November 2026 by the audio/story reviewer, independently of the editor. This record covers the encoded file with SHA-256:

`cf009e2e39c5033372ec567f82a311cd81ee09df7a3b3fbe2a94bdeff68b2233`

**Result: coherent full-song animatic; not an acceptable finished animated music video.** The reviewed encode has zero generated-video seconds and 277.792 seconds of still artwork with camera movement according to its manifest, consistent with the inspected images. This is a useful planning cut and preserves the full song. It does not meet the user's actual character-animation/movement goal. Further free-generation/access work can continue from it.

## Review coverage and limits

I checked the file hash, the corrected source references in its manifest, all **58 shot midpoints**, **20 selected cut boundaries** with the exact frame before and after, opening/title samples, and four final-fade/last-frame samples. The temporal contact sheets contain 105 samples in total; two additional full-size frames were inspected for edge framing.

- Shot midpoints: [1–20](corrected-cut-midpoints-1.jpg), [21–40](corrected-cut-midpoints-2.jpg), [41–58](corrected-cut-midpoints-3.jpg).
- Exact cut/title/ending samples: [sheet 1](corrected-cut-joins-1.jpg), [sheet 2](corrected-cut-joins-2.jpg), [sheet 3](corrected-cut-joins-3.jpg).
- Full-size framing evidence: [chorus endpoint](chorus-full-body-last-frame.png), [bridge endpoint](bridge-tight-last-frame.png).

This was **sequential frame review, not normal-speed audiovisual playback**. I did not listen to the encoded cut or inspect every one of its 6,667 frames. The root technical validator handles full decode, frame count and audio alignment separately. No technical or frame-sampling result should be represented as complete natural-motion or lip-sync approval.

## What works in the reviewed encode

- The night hospital → interrupted room → journey/arrival → waiting-room sequence is intelligible. The supplied characters remain recognizable in the still art and the hospital scene remains emotionally unresolved.
- The revised room images are actually present in the manifest and visible in the encode. The night bed is made, the morning bed can be untidy, and mug handles retain their direction. The stronger source detail is visible in the room inserts.
- The warm summer memory is clearly separated by wardrobe/palette from the winter hospital scene. It returns at a musically plausible structural point; precise lyric sync still needs listening.
- The four bridge pleas have distinct shot beats. The first uses the open-mouth plea drawing rather than delaying visual intensity until a later scream.
- The corrected dawn progression keeps the characters inside through S051, establishes the courtyard in S052, then shows them outside in S053. The earlier outside–inside–outside reversal is gone. Empty-room inserts afterward can read as a parallel ordinary-life motif, not teleportation.
- S050 → S051 matches image framing at the cut. No visible camera reset appeared in the sampled boundary frames.
- The ending retains the full musical tail and uses a restrained final image. The sampled final fade darkens progressively and reaches an almost-black last frame; it does not cut off on an unrelated shot or unplanned blank picture.
- None of the reviewed frames silently introduces the rejected LTX pilot or the old defective embrace/summer motion clips.

## Specific changes still recommended

1. **S014, approximately 70.54 s: top of hair is cropped.** At the end of the nominal full-body chorus shot, the upward edge cuts the top of his hair while the shoes are also close to the bottom. Reduce the maximum zoom for this full-body source or provide enough source overscan; do not solve it by stretching the figure. Review the other uses of `chorus_performance` under the same policy.
2. **S046, approximately 219.33 s: the pleading hand is cropped through the palm/fingers at the lower edge.** This weakens the action's important gesture. Use a gentler crop that preserves both the full extended hand and the hair; shifting the camera downward alone can trade this for a chopped head. See the linked full-size endpoint frame.
3. **S025 → S026, approximately 122.458 s: small same-angle position jump.** Both segments use the same unchanged summer drawing, but zoom jumps from 1.075 to 1.13 and centre from (0.5, 0.5) to (0.57, 0.43). No fresh action motivates the jump. Make S026 start from S025's exact camera endpoint and glide to the closer view, or make a genuinely different shot. This keeps the roughly 8.5-second memory passage continuous.

These are concrete composition/continuity fixes within the animatic. Resolving them does not turn still-camera footage into character animation.

## Why the finished-video target still fails

There are 58 segments but only 18 distinct still sources. `her_window` is reused eight times for about 37.6 seconds, and the uninterrupted waiting-room image at S028 lasts about 12.1 seconds. During those holds, expressions, breathing, hands, clothing and background movement do not develop. Snow stays fixed in the image while the camera moves. The singer is a held drawing with no actual sung articulation, and the journey is a held stride rather than a walk/run. No face warp is introduced, but there is also no demonstrated natural character performance to approve.

The remaining seven small board crops are still approximately 550 × 306 pixels, enlarged into the 960 × 540 export. Their detail varies visibly against the larger existing art and corrected room images. That is acceptable for staging review; it is below the requested finished-film quality.

The next substantive improvement is to replace selected holds with short, clean, correctly motivated actions and then re-review them at normal speed with the real audio. Start with a quiet window portrait, the arrival, one memory action, and the bridge plea. Preserve the existing rejection evidence and count approved actual motion separately from holds and camera-only movement. The final judgement must remain against the user's complete-video goal, not against the easier fact that a full-length file exists.


## Final repaired export: targeted independent verification

Verified exact file SHA-256 on 6 November 2026:

`d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`

I extracted **19 exact frames from this final MP4**, covering first/last frames of S014, S029, S033, S044 and S046; the S025/S026 boundary and S026 endpoint; and the late indoor/courtyard/outdoor progression. See [final repair contact sheet](final-repair-frames.jpg). I additionally viewed the encoded [S014 endpoint](final-S014-last.png), [S046 endpoint](final-S046-last.png), [S025 last frame](final-S025-last.png), and [S026 first frame](final-S026-first.png) at native 960 × 540 size.

**All three requested framing/continuity corrections are confirmed in the encoded result.**

| Correction | Independent observation |
| --- | --- |
| Chorus full-body framing, S014/S029/S033 | Hair top and both shoes are inside the frame at the reviewed first/last frames. The figure no longer touches/crosses the upper edge as in the earlier S014 endpoint. Small margins are deliberate, but the prior crop is removed. |
| Pleading-hand framing, S044/S046 | Both sampled endpoints retain the full extended hand, visible fingers and hair. The earlier cut through the palm/fingers is removed. S046 remains a slightly closer composition than S044 without sacrificing the gesture. |
| Summer S025 → S026 | The camera starts S026 at S025's endpoint. The independently rendered pre-encode PNGs are byte-identical. Actual MP4 boundary frames retain the same geometry; an integer-shift comparison has its minimum error at zero horizontal/vertical offset. The decoded images are not byte-identical after compression (RGB MAE 3.05/255, RMSE 4.52/255, PSNR 35.03 dB), so the exact-byte claim applies only to the pre-encode PNGs. The earlier positional jump is absent in the inspected boundary pair. |
| Late chronology | S050/S051 still remain indoors; the S050/S051 boundary matches. S052 establishes the empty courtyard and S053 then places the characters outside. The earlier direct outside–inside–outside reversal has not returned. |

The revised camera scale still uses the same still illustrations. This pass closes the specified composition defects; it does **not** establish character movement, natural singing, animation quality, or a finished music video. No additional source anatomy correction is implied by showing an existing hand fully inside frame.

The broad story/order observations from the previous review remain applicable to unchanged material. The earlier contact sheets show the previous encode and are retained as before/after evidence; the final repair sheet above is the evidence for this hash. This reviewer did not repeat the whole-cut sample extraction or perform normal-speed audiovisual playback. The root's separate full playback/technical check should be recorded separately rather than recast as this reviewer's listening judgement. The accepted scope remains a reviewed full-length animatic, with final animated performance still outstanding.
