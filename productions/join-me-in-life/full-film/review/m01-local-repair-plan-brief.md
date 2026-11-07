# Original M01: local hand repair preparation

7 November 2026. **A local hand/wrist repair is a reasonable first test; a clean result has not yet been demonstrated.** Preserve the original uninterrupted action and the good faces, rather than regenerating the couple. No mask, source edit, generation or provider call was made for this inspection.

Source: [M01_Embrace.mp4](../../current/assets/M01_Embrace.mp4), SHA256 `bb6e21e887c5b86d815c1b2638896f2b2612471238d3dd2ee798b586418d5246`. Independently probed: **1916×1080, 24 fps, 121 frames, 121/24 = 5.041667 s, no audio**. Time base is `1/12288`; every source frame advances 512 ticks. Frame indices below are **zero-based raw source indices**, unlike the edit's one-based frames. The [machine-readable plan](m01-local-repair-plan.json) supplies both conventions, timestamps, R4/full-song positions and 24 individually inspected hand/forearm ROIs.

## The specific repair

| Raw source frames | Source interval | Finding / treatment |
| --- | --- | --- |
| f24–32 | 1.000–1.333 s, sampled frame times | Keep as lead-in context. The hand rises from his lap with readable fingers. |
| f33–38 | 1.375–1.583 s | Softer hand/wrist on ascent. Optional transition repair; no confirmed extra digit justifies wholesale replacement. |
| **f39–51** | **1.625–2.125 s frame times; displayed through 2.166667 s** | **Core target.** Rounded/merging finger and knuckle shapes, soft palm and unstable drawn definition as the hand passes over/behind the crown and descends left of her face. Worst loss of finger definition is visible around f43–50. |
| f52–53 | 2.167–2.208 s | Finger separation returns. Optional taper into original picture. |
| f54–56 | 2.250–2.333 s | Clearer original hand; preserve as joining references. These are near-contact approach poses, not proof that the wrapping grip has already finished. |
| f60–88 | 2.500–3.667 s, inspected keyframes | Original grip is clear by f60; retain the actual pull and settling. |

The combined **candidate** repair envelope is f33–53 inclusive: **[1.375, 2.25) s, 21 frames / 0.875 s**. The core is [1.625, 2.166667) s. Neither envelope means repainting every pixel or automatically modifying every transition frame. Some blur is natural in this fast movement; the aim is coherent anatomy and matching drawn detail, not an unnaturally sharp hand in every frame.

The [native ROI sheets](m01-local-repair/roi-final-native-01.jpg) show yellow hand/wrist and cyan forearm boxes; sheets [2](m01-local-repair/roi-final-native-02.jpg), [3](m01-local-repair/roi-final-native-03.jpg) and [4](m01-local-repair/roi-final-native-04.jpg) continue chronologically. Coordinates are manually inspected **bounding regions, not segmentation masks or exact anatomical landmarks**. They include safety margin and good pixels. Do not fill their rectangular union.

The most important occlusion is f40–48. Foreground hair crosses the arm; at f42 only a separate small forearm fragment remains to image-right of her hair. In f43–46 that forearm is hidden, as the [native occlusion strip](m01-local-repair/occluded-forearm-native.jpg) confirms. Do not invent a visible connection through her hair or paint her face. The visible wrist/forearm returns on image-left around f48–49. Keep every original foreground strand, both faces, her body/lap hands and his body/shoulder path protected. Any later mask needs contour-level inspection, including the blur halo and the original occluding strands.

## What a hand repair can and cannot solve

The [whole-action context](m01-local-repair/full-action-context.jpg) and every f24–64 show the original single reach leading into contact, pull and held aftermath. Her gaze remains down-left/away; her hands stay passive. There is no sustained crown pat, second reach/reset or new mutual reassurance in this inspected sequence. These strengths distinguish this source from the rejected newly generated hospital take.

**The high overhead arc remains.** It is a fast sweep behind her head. Cleaning the hand cannot lower the trajectory or change the shoulder/elbow choreography. If an actual normal-speed repaired preview still makes that arc look unnatural, a hand-only patch will not suffice; a broader arm/occlusion/background change would need separate justification and review. This plan does not authorize that expansion or hide the movement with a cutaway.

Keep all 121 original frames available as context. If a shorter context is required, f24–88 inclusive is **65 frames**, spanning [1.000, 3.708333) s: lead-in, whole arc, clear fingers, grip and pull. These context frames are not permission to regenerate their good pixels. Preserve 24 fps and original timing; record any required model resampling and composite against the original outside the actual repaired region. Do not freeze, loop, reverse or stretch the action.

R4 places the movie at **Short 34–39 s** (full-song **134.373–139.373 s**). Both adjacent schedule entries use `video_t0=34`, so their 36.5 s split is continuous playback. Preserve the surrounding 30.167–42.083 s passage and original pull/aftermath. Source f120 starts at 5.0 s and is outside the five-second action interval R4 uses. The candidate repair envelope maps to Short [35.375, 36.250) s, or full-song [135.748, 136.623) s.

## Evidence and acceptance limits

Inspected all 41 decoded source frames f24–64 in chronological whole-frame contacts, f32–56 coordinate grids, native-pixel hand/forearm crops for every f33–56, the native occlusion strip, and full-action keyframes through f120. [All 121 frame timestamps](m01-local-repair/source-frame-times.json) were probed. This is sequential-frame source analysis, **not perceptual normal-speed playback or listening approval**. The silent source does not permit a lip-sync claim.

A repaired candidate must pass actual normal-speed review in the edit plus dense frames: stable hand ownership/digits/wrist, original hair occlusion, unchanged faces/away gaze, same one contact→pull→held aftermath, and clean f32→repair→f54–64 joins. Do not force five exposed digits into an originally curled/occluded pose. No new jewelry, head pat, second push, camera reset or off-patch drift is acceptable. A successful encode or attractive endpoint is insufficient.
