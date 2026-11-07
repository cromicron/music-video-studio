# First chorus — contained insertion and context v2

Reviewed 2026-11-07. **Scoped visual pass for the exact v2 insertion and its current S013→S014→S015 cuts.** The full available source picture survives the fit, the side padding is symmetric, and the selected 98 frames run once in order without a new hold, reset or camera move. The [frozen source review](ltx23-first-chorus-review.md), including native crown grazing, softer facial/accessory detail and the generated camera/gesture departures, remains unchanged.

| Reviewed v2 file | Picture | SHA-256 |
| --- | --- | --- |
| [Contained S014](../exports/Join_Me_in_Life_First_Chorus_Contain_Proof_v2.mp4) | 98 frames, 4.083333 s | `5588132a1628cb760703167e4b2d7a415c30684bd883ec828605b9d7d5fb15e1` |
| [S013–S015 context](../exports/Join_Me_in_Life_First_Chorus_Context_Proof_v2.mp4) | 348 frames, 14.500 s | `6bed5d22f2f93929cbb6310848e1836cc3891d3b8b2bb5a46d9fa40ea8906114` |

Both are 960×540 at 24 fps. The insertion uses source `[3,101)` from hash `8756ad09d45ecfe47bb2a4cead5f5184d3bd4a4561cbc27e9495cdb6170a0252`, exactly master 66.500–70.583333. Frame numbers below are zero-based; interval ends are exclusive.

**Framing:** [Contained source reference versus encoded picture](first-chorus-sequence-review/expected-vs-encoded.jpg) preserves the original top/bottom and lateral boundaries. V2 scales the full 896×512 image to 944×540 and pads 8 pixels on each side. The decoded column profile independently locates those 8-pixel borders; minor codec ringing does not mean the padding is mathematically zero in every RGB sample. The narrow bars are unobtrusive at ordinary viewing size. There is no additional push, vertical crop, concealed shoe, severed hand or tightened body framing. [Early tight crown](first-chorus-sequence-review/normal-insertion-f09.jpg) and [last selected picture](first-chorus-sequence-review/normal-insertion-f97.jpg) retain the available source boundary. **Containment does not restore hair already grazing the native edge**; complete crown preservation was not achieved by the generated source and is not claimed here. V2 corrects v1's asymmetric padding; this final verdict is bound to v2.

**Cadence and interval:** Every one of the 98 insertion pictures has the expected source frame 3–100 as its nearest image after the same containment transform. The comparison is lossy-image matching, not byte identity with the generated original. Decoded PTS follow `i/24` within ffprobe's decimal precision. The 98 decoded picture hashes inside the context proof match the standalone insertion **98/98 exactly**. Together these checks and the chronological picture inspection show no frame cycle, cloned lead/tail, reversed motion, pose reset or added camera animation. The new shot begins on source f3 and cuts after f100; it does not include the unused source tail.

**Actual neighboring cuts:** [Exact cut frames](first-chorus-sequence-review/context-cuts.jpg) and [context overview](first-chorus-sequence-review/context-overview.jpg) show:

| Context frames | Master interval | Editorial finding |
| --- | --- | --- |
| f0–148 / S013 | 60.291667–66.500 | Apprehensive arrival portrait and door grip lead into the appeal. |
| f149–246 / S014 | 66.500–70.583333 | Immediate cut to the wide singer. His existing lean, microphone grip and open palm enter cleanly; it reads as a change of scene, not a failed physical match-cut or a repeated reach. The source performance continues through the cut. |
| f247–347 / S015 | 70.583333–74.791667 | Cut from his still-open appeal to her down/away, withdrawn window portrait. No recovery smile or reciprocal gesture is introduced; the unresolved direction survives. |

The S013/S015 pictures in this proof are still artwork. This review clears their present **cut relationship** to S014; it does not approve their future quiet-motion replacements, certify new door action, or mark those neighboring shots as completed animation. Replacing either neighbor requires checking the changed seam.

**Playback telemetry, separately:** An independent Chromium 154.0.8037.57 run played the exact v2 context at 1×, displayed 960×540 with supplied audio enabled. It reached 14.500 seconds in approximately 14.613 wall seconds, reported 348 total video frames, zero dropped/corrupted frames, no media error and no waiting/stalled event. It supplied 347 frame callbacks, not substituted for decoded frame count. [Player telemetry](first-chorus-sequence-review/playback.json) and captured normal-size views support execution and visual inspection. No human-equivalent continuous audiovisual perception, subjective listening or phoneme-sync claim is made. Original-master audio alignment was not independently rerun; the [author's render manifest](../exports/Join_Me_in_Life_First_Chorus_Context_Proof_v2.manifest.json) reports correlation 0.999701 and zero measured lag. That remains technical alignment evidence, not a listening review.

[Independent encoded checks](first-chorus-sequence-review/encoded-checks.json), compact JPEGs, and [frame](first-chorus-sequence-review/reproduce_frames.py)/[playback](first-chorus-sequence-review/playback_check.py) scripts are retained beside this report. Reproduction writes only to ignored root `build/first-chorus-sequence-review/`. Provisional v1 evidence remains in its ignored build subfolder and the original v1 exports remain intact. No source, frozen source report, configuration, editor or provider state was changed by this review.
