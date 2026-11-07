# Positive window insertions: S009–S016 sequence review

**Verdict: PASS for the exact S010/S015 insertions and their current surrounding cuts in the pinned context proof.** Reviewed independently on 2026-11-07 using the retained Be Ambitious outside-review method. No placement or cut correction is required. This is scoped sequence acceptance, not whole-film acceptance or approval of future replacement neighbours.

The reviewed [context proof](../exports/Join_Me_in_Life_Positive_Window_Context_Proof.mp4) contains 898 frames at 960×540, 24 fps: master frames `[998,1896)`, or 41.583333–79.000000 seconds. Its duration is 37.416667 seconds. Frame ranges here are zero-based and half-open.

| Pinned input | SHA-256 |
|---|---|
| Context MP4 | `dfece1dd258e0da59a2d58fe468670a76447a3ab17bdd3ab1d9afd5f436791d2` |
| [Frozen render manifest](positive-window-sequence-review/frozen-manifest.json) | `fb30d7dbfb0a1ba8188e887adf4e23bfa313dae53f9f607e4f29c2c46ae1a82e` |
| [Frozen edit configuration](positive-window-sequence-review/frozen-edit.json) | `8422bf9fb4849e02e1ead09148b4615538c4a3780d13161f4f598e94932f7bb6` |

The frozen configuration matches the manifest's recorded configuration hash. Later changes to the shared live configuration do not extend or invalidate this review of these exact pictures; changed window settings or neighbouring pictures require their own seam review.

| Insertion | Raw source frames | Context frames | Master frames / seconds | Exact comparison |
|---|---|---|---|---|
| S010 / P1L02 | `[3,116)` | `[101,214)` | `[1099,1212)` / 45.791667–50.500000 | 113/113 decoded pictures match |
| S015 / P1L03 | `[3,104)` | `[696,797)` | `[1694,1795)` / 70.583333–74.791667 | 101/101 decoded pictures match |

Both comparisons independently trim the original sources by integer frame index and reconstruct the containment. The entire 896×512 image becomes 944×540, centred between eight-pixel side bars in the 960×540 frame. Every inserted decoded picture matches that reconstruction. There is no added crop, push, lead-in, endpoint hold, loop, reverse or retiming. Both sources play at their natural 24 fps; all 898 context video timestamps agree with frame index divided by 24 within 0.34 microseconds. See [checks](positive-window-sequence-review/checks.json) and [reproduction code](positive-window-sequence-review/reproduce.py).

All 214 inserted output frames were inspected in contact sheets. Native output face/reflection phases were checked at the starting pose, raised head, closing eyes, sustained closure and ending pose. These retain the source findings: coherent head/chest movement, connected neck and shoulders, stable hair/clothing, and a reflection that follows her face and eyelids. The larger head rise and longer closure remain acceptable depleted movement. There is no smile, recovery, direct viewer address or new anatomical failure. Intermediate facial softness and cooler/desaturated iris detail remain visible; this does not establish a persistent replacement of her gray-green/olive eyes. Native crown intersection is inherited from the raw picture, with no additional clipping by this placement. The [P1L02](ltx23-positive-P1L02-review.md) and [P1L03](ltx23-positive-P1L03-review.md) source reports remain frozen and retain their detailed identity and limitation findings.

| Actual cut | Inspection and result |
|---|---|
| [S009→S010, local 100→101](positive-window-sequence-review/cut-101.jpg) | The doorway portrait changes to a clearly different seated/window composition. Adult identity, auburn hair, striped sleeves, pendant and lowered attention carry across. No accidental pose jump within the same composition. |
| [S010→S011, local 213→214](positive-window-sequence-review/cut-214.jpg) | Her eyes have reopened downward after the inward closure. The switch to his snowy approach develops the waiting/arrival story; it does not make her head rise read as relief. No held or repeated window tail. |
| [S014→S015, local 695→696](positive-window-sequence-review/cut-696.jpg) | The performance cut returns to her inward, seated attention. The restrained window passage remains emotionally distinct from his pleading gesture. No viewer-facing response is introduced. |
| [S015→S016, local 796→797](positive-window-sequence-review/cut-797.jpg) | The sustained closure cuts to a wider two-person hospital view with her eyes lowered/open and both faces still anxious. The wider viewpoint and his newly visible presence make this a scene progression rather than a same-shot eyelid discontinuity. Neither face suggests that his arrival has cured her distress. |

Six frames on either side of each of those four cuts were inspected, alongside the exact native boundary frames. The other three cuts and first/middle/last pictures of all eight shots were also inspected. The snow, hospital exterior, frightened arrival, performance and waiting-room geography remain legible. S016's existing drawn blink exposures retain the same worried baseline expression. Its quieter motion and the still/camera treatment of S009/S012 are inherited material, not newly generated window motion. See the [sequence overview](positive-window-sequence-review/sequence-overview.jpg), [S010 face phases](positive-window-sequence-review/S010-native-face-phases.jpg), [S015 face phases](positive-window-sequence-review/S015-native-face-phases.jpg) and [S016 exposures](positive-window-sequence-review/S016-exposure-phases.jpg).

The established walking, arrival and chorus sources, source intervals, holds and framing match their previously reviewed manifests. All 149 arrival pictures are decoded-picture-identical to the earlier proof. Walking and chorus encodes differ slightly: same-index 240×135 RGB mean absolute errors are approximately 1.192/255 and 1.088/255 respectively; maximum per-frame means are below 1.335/255. Their source selections and visible actions are unchanged. This review does not erase their prior limitations or claim those two encodes are pixel-identical.

The complete proof executed once at actual 1× with the original-song audio enabled, volume 1, unmuted, at a 960×540 browser display. Playback was serialized with `build/source-review-playback.lock`, used an independent browser process and build directory, and ran capture-free. Chromium reported 898 total frames, zero dropped/corrupted frames, no initial drops, no media error and no waiting/stalled event; 37.416667 seconds of media took 37.5162 seconds wall time. There were 897 video-frame callbacks; full decoding independently established all 898 pictures. [Playback telemetry](positive-window-sequence-review/playback-summary.json) records the limits honestly: visual judgments come from encoded-frame inspection, not a claim of human-equivalent continuous viewing or subjective listening.

Independent decoded-waveform comparison against the original `track-49.mp3` at master offset 41.583333 seconds gives correlation **0.999768 at zero offset** in a ±0.1-second search. See [audio check](positive-window-sequence-review/audio-check.json). This establishes the original-song excerpt and alignment; it does not certify phoneme sync or subjective musical phrasing.

The [evidence index](positive-window-sequence-review/README.md) contains reproduction commands, and [verdict.json](positive-window-sequence-review/verdict.json) binds this report and compact evidence to the exact sources, export, manifest and configuration. Original source-review hashes remain `65571eddd8eb7b895b31c3c4d73bfdbba5ef9943a483eef80e43c813e471a845` (P1L02) and `8ce27b2b6b513d5fb02c79302c4f9d224a58003eebda30fa00694bff7bbcb3f7` (P1L03).
