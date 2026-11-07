# L01 window close-up — independent crop review

Reviewed 7 November 2026 UTC. **Pass the exact fixed-crop derivative for S003 source `[3,157)`: 154 frames / 6.416667 seconds at natural 24 fps.** It excludes the rejected reflected-eye acting throughout the selected interval, while her actual face, neck and shoulders remain coherent and emotionally withdrawn. It is usable as a close-up at ordinary 960×540 edit size. No further crop, retiming, loop or repair is required for this recommendation. Actual insertion and neighboring cuts remain separate.

This accepts a bounded editorial remedy, **not the original full-width take or a repaired reflection**. The [frozen full-width rejection](ltx23-quiet-L01-review.md) remains valid.

## Exact reviewed picture

| Item | Identity / scope |
| --- | --- |
| [Fixed-crop source](../assets/motion/ltx23-quiet-window-closeup/video-silent.mp4) | SHA-256 `5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20`; 672×378, 161 frames, 24/1 fps, silent |
| [Original source](../assets/motion/ltx23-quiet-pilots/L01/video-silent.mp4) | SHA-256 `e90f0c8b2ed56367fe04399109dc7a95a030aacc56e158964a46bac610ef743a`; 896×512 |
| Locked crop | Original pixels `x=224, y=0, width=672, height=378`; full original cadence |
| Selected interval | Zero-based frames 3–156 inclusive; source time `[0.125000,6.541667)` |

All 161 derivative frames were inspected in sequence, with every native face/neck and left-edge crop checked. That covers the 154 retained frames, three head frames and four tail frames. [Portable evidence index](ltx23-window-closeup-review/README.md) and [original crop boundaries](ltx23-window-closeup-review/original-crop-boundaries.jpg) retain the scope.

## Reflection exclusion and close-up judgment

**The faulty reflected eyes stay out.** No reflected eye, eyelid, nose or mouth becomes readable inside this crop, including the original mismatch around f49–89. The left edge is not completely free of reflected anatomy: dark hair, an ear/earring, a rear-cheek edge and neck/shoulder fragments remain, most clearly early and during the return. Those fragments do not carry an independently readable facial expression or reveal the closed-eye/open-eye contradiction. At 960×540 they read as a dim peripheral reflection behind her hair, without competing with her actual face. Describe this as exclusion of the faulty facial features, not removal of every part of the reflected head. [Early edge detail](ltx23-window-closeup-review/left-edge-000-031.jpg), [core mismatch interval](ltx23-window-closeup-review/left-edge-064-095.jpg), [return edge](ltx23-window-closeup-review/left-edge-096-127.jpg).

**Her larger movement works in this framing.** Approximately f12–32 close the eyes as she begins to straighten; f33–60 reopen them into a more frontal three-quarter pose. She keeps looking down/away, then makes a second slow closure around f90–104 and lowers/turns back through f105–132. The final portion settles without a visible reset. Head, neck, collar and shoulder change together; the hair follows the pose rather than exposing a detached neck or abrupt body jump. These structural changes are real acting, not compression noise. The slow two-phase rhythm reads as depleted inward attention, with no smile, reassuring response or address to the viewer. It exceeds the original single-blink instruction, but is physically and emotionally usable under the accepted editorial scope.

**Identity remains stable.** Auburn hair, green/hazel eyes, freckles, earring, facial proportions and black clothing remain consistent with the source character. Face shape changes with the turn; I found no persistent replacement identity, round childlike face, blue-eye drift or conspicuous facial-anatomy failure. Minor line softness/redraw is visible when enlarged. At the actual 960×540 display size, the face and expression remain legible. [Playback near the raised pose](ltx23-window-closeup-review/playback-2.00.jpg), [second closure](ltx23-window-closeup-review/playback-4.00.jpg), [native selected end](ltx23-window-closeup-review/native-156.jpg).

**Framing is deliberate and tight.** The original crown already intersects the upper boundary; her rise maintains that source limitation. The derivative begins at original row zero and adds no top crop. The eyes, nose, chin, neck and upper shoulder connections stay inside the picture throughout. The lower pendant, arms and body are intentionally outside or intersect the lower framing; that is not missing anatomy. This is not a full-head/full-body composition. Keep this locked view and assess any additional crop or camera move separately.

**Background limitation:** Small distant passersby remain visible in the right doorway around f64–96 and again roughly f130–149. They are unrequested secondary movement, inherited from the original. They do not cross her face or disrupt the room layout and do not block this close-up recommendation; their continuity with adjoining shots still needs checking. Chairs, window edge and doorway remain stable.

## Technical checks and perceptual limits

All 161 derivative frames have the same-index original crop as their closest source frame in the independent comparison. Maximum per-frame mean absolute RGB error against the original crop is 1.655/255, consistent with re-encoding. Every PTS agrees with index / 24 within one microsecond. These checks support the locked crop and preserved cadence; they do not establish acting quality. [Source/crop checks](ltx23-window-closeup-review/source-evidence.json), [reproduction script](ltx23-window-closeup-review/reproduce.py).

Chromium 154.0.8037.57 actually played the exact full derivative once at **1×, displayed 960×540**, ending at 6.708333 s in 6.715 wall seconds. It reported 161 total frames, zero dropped/corrupted frames, no error and no waiting/stalled event. [Playback telemetry](ltx23-window-closeup-review/playback.json), [browser reproduction script](ltx23-window-closeup-review/playback_check.py).

The visual judgment comes from sequential inspected native frames and ordinary-size captured pictures, with actual browser execution documented separately. This is not a claim of human-equivalent continuous audiovisual perception. The clip is silent; no subjective listening or audio-sync judgment is claimed. No production asset, provider, configuration, approval record or prior review was changed.
