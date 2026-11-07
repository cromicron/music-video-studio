# Waiting deliberate closeup V4 — independent review, 2026-11-07

**PASS S020's exact stationary closeup, S019→S020 and S020→S021, with tight but intact crown framing.** The distinct composition resolves the previously failed same-composition reset. This scoped outside review follows the retained Be Ambitious review requirement. The [V2/V3 failure](r1-waiting-seam-v2-review.md) remains frozen; it does not become a pass retroactively.

Config SHA-256: `ff0a2d0e310c558d5c3105a7c62165ea483ce14e610ec233e59fa44ba21d24ce`. Both proofs use editor 1.6.2 and 24 fps.

| Exact proof | Scope | SHA-256 |
|---|---|---|
| `exports/Join_Me_in_Life_Waiting_Correction_Context_Proof_v4.mp4` | 960×540, S018–S022, 649 frames; master `[1994,2643)` | `bddab2a000823c2298679bb698be43c80daa36cee8ab8316ad5578dcbfbf7a10` |
| Repository-root `build/r1-waiting-closeup-1080.mp4` | 1920×1080, S020, 136 frames; master `[2273,2409)` | `d0c3a6963324d53a6581b3ef137858968773fd821fdab01071062fb40c177704` |

## Framing and performance

S020 uses the original waiting artwork/eye exposures with fixed zoom 2.0 and center `(0.67,0.25)`. The [actual 1080 frame](r1-waiting-closeup-review/1080-native-000.jpg) and [native crown crop](r1-waiting-closeup-review/1080-native-crown.jpg) retain the complete visible crown outline. Its tallest tips have very little headroom; this exact framing passes, with no room implied for a further push. His face, chin, ear and neck remain visible. The lower edge crosses the neck base/upper chest; shoulder contours continue naturally beyond the portrait's lower corners. There is no cut through his face or chin. The small red-hair fragment at lower left belongs to her established offscreen position.

The closeup reads as anxious attention toward picture-left, where she sits. His worried eyes, tense brows and parted mouth do not become direct address or recovery. The existing tear detail is clearer at this size; it is part of the original drawing, not a newly animated event. Hair and facial lines remain legible at the actual 1080 render. This is an enlarged source-art crop, not a claim of newly generated native detail.

The [native 1080 eye phases](r1-waiting-closeup-review/1080-eye-phases-native.jpg) show the retained short blink: open at S020 f64–65, a one-frame blend at f66, closed f67–69, one-frame reopening blend f70, open again f71–72. Both lids remain registered; no local patch edge or displaced facial feature appears. These are supplied drawing exposures. The body, hair and camera remain stationary; this shot is not counted as new generated body motion.

## Joins and unchanged motion

| Boundary, zero-based master frames | Result |
|---|---|
| S019→S020, f2272→2273 / 94.708333 s | **PASS.** The clear two-person view → face closeup cut makes the sharper drawing/detail change intentional. It no longer presents the V2/V3 near-identical composition with a facial reset. His gaze remains directed toward her. |
| S020→S021, f2408→2409 / 100.375 s | **PASS.** The return to the original wider artwork restores both people and her withdrawn gaze without implying new physical action, embrace or cure. |
| S021→S022, f2546→2547 / 106.125 s | **PASS.** The further wider seated composition remains legible. |

[Native cut pairs](r1-waiting-closeup-review/v4-joins-native.jpg) retain the evidence. All 279 S018/S019 encoded frames and all 96 S022 frames are identical to V3. The accepted R1L04 interval, its full-image containment, cadence and all timeline boundaries are unchanged. The 136-frame closeup retains S020's existing duration and eye timing; it adds no time or endpoint hold. Both new proof files decode completely without errors.

## Playback and review limits

The whole V4 context actually played unseeked at **1×**, audio enabled/unmuted at volume 1, in sandboxed Chromium 154.0.8037.57. It reached `ended`: 27.041667 s media / 27.181 s wall, 649 video frames, 648 frame callbacks, zero dropped/corrupt frames and no error/waiting/stalled events. Native cut/eye/1080 detail frames and actual playback captures were inspected, including the [closeup](r1-waiting-closeup-review/waiting-v4-playback-11.80.jpg) and [return](r1-waiting-closeup-review/waiting-v4-playback-17.50.jpg).

This is instrumented normal-speed playback plus frame inspection, **not continuous human viewing or subjective listening**. The separately attributed author-manifest audio correlation is 0.9997643014 at zero offset. [Checks](r1-waiting-closeup-review/checks.json), [playback summary](r1-waiting-closeup-review/playback-summary.json), compressed full callbacks, frozen manifests, reproduction scripts and the [SHA-256 inventory](r1-waiting-closeup-review/evidence-sha256.json) are retained beside this report. Raw evidence remains in ignored `build/r1-waiting-closeup-review/`.

This closes the reviewed waiting joins for the hashes above, not the full film. **S032→S033 remains open** for the actual replacement footage. No source/config/provider changes were made by the reviewer.
