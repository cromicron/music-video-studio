# Stable 1080 cache picture review — 2026-11-07

**Scoped PASS: no new final-resolution framing or compositing correction is required for these 44 cache files.** This independent outside review follows the retained Be Ambitious review requirement. It checks the final-size picture rendering of already selected material; it does not replace source judgments, approve new holds/joins, or approve the full film or music synchronization.

The exact [44-file inventory](stable-1080-picture-review/cache-inventory.json) has SHA-256 `06b5081dc8f8bb571cca297d65decc65f2113a1947a3c8f2b5d0bcc4be5c1e32`. It records every cache path and video hash under repository-root `build/production-1080-cache`. Config: `ff0a2d0e310c558d5c3105a7c62165ea483ce14e610ec233e59fa44ba21d24ce`; editor 1.6.2; CRF 18. All 44 files are **1920×1080, 24 fps, silent**, totaling 5,136 frames. Inventory hashes, frame counts, dimensions and decoding through the last selected frame passed.

Whole-frame first/middle/end views were inspected for every listed shot, covering both camera extremes. The evidence generator extracted 229 selected frames, including exposure, action and hold-boundary phases; native inspection concentrated on faces, crowns, hands, feet, drawing patches and branding. This is sampled picture inspection, not a claim to have visually examined all 5,136 individual frames. [Nine overview sheets](stable-1080-picture-review/overview-01.jpg), native details and selected phase sheets are retained; all sampled indices appear in [cache checks](stable-1080-picture-review/cache-checks.json).

## Exact motion intervals and geometry

Independent integer-frame reconstructions match **all 1,585 decoded frames of all 13 motion cache shots exactly**, including the existing lead/endpoint frames. This validates the actual output intervals, natural cadence and declared framing rather than inferring them from endpoints. Zero-based ranges exclude their endpoint.

| Shot | Source interval | Output frames | Framing / existing holds |
|---|---|---:|---|
| S003 | `[3,157)` | 154 | Whole 672×378 reviewed derivative, scaled directly to 1920×1080 |
| S011 | `[3,135)` | 132 | Fixed fill |
| S013 | `[3,152)` | 149 | Whole-image contain |
| S014 | `[3,101)` | 98 | Whole-image contain |
| S019 | `[3,135)` | 132 | Whole-image contain |
| S025 | `[0,48)` | 111 | Fixed fill; existing 63-frame lead |
| S026 | `[48,120)` | 72 | Fixed fill; follows S025's source portion without replay |
| S028 | `[0,121)` | 291 | Fixed fill; existing 92-frame lead and 78-frame endpoint |
| S030 | `[3,101)` | 98 | Whole-image contain |
| S032 | `[101,197)` | 96 | Whole-image contain |
| S044 | `[3,84)` | 81 | Fixed fill |
| S046 | `[3,85)` | 82 | Fixed fill |
| S053 | `[0,89)` | 89 | Whole-image contain |

For the six 896×512 **contained** sources, this FFmpeg build resolves the scale to **1892×1080, with 14 pixels on each side**. This is not a simple doubling of the 960 proof's 944-pixel picture and 8-pixel sides; the divisible-by-four rounding differs. The entire available source remains present, including its inherited thin top/bottom edge strips. No extra camera move or crop is introduced.

The 896×512 **fill** sources scale to 1920×1097 before the established centered crop to 1080; S028's 1916×1080 source scales to 1920×1082 before its centered crop. S003's reviewed 16:9 derivative receives no further crop. These are the configured fixed render geometries, not the camera zoom values retained in motion-shot metadata. [Resolved geometry](stable-1080-picture-review/resolved-geometry.json) and [source hashes/full-frame comparisons](stable-1080-picture-review/interval-checks.json) retain the measurements.

**S020:** all 136 cached frames are identical to the independently reviewed 1080 closeup proof `d0c3a6963324d53a6581b3ef137858968773fd821fdab01071062fb40c177704`. Its [closeup review](r1-waiting-closeup-review.md), including the intact but tight crown, neck/shoulder framing and registered blink, carries over to this exact picture. Its cache file hash differs because the cache is silent.

## Picture findings

- **S001 branding:** the native [logo/title phases](stable-1080-picture-review/branding-native.jpg) are legible and fully within the image. The paired fade appears over the original backdrop without a black rectangle, displaced title or clipped flourish. The clean frame before and after the fade remains correct.
- **S003 / S013 / S019 / S030 / S032:** the reviewed faces and support/contact remain readable at 1080. The window closeup's inherited crown cut and faint rear reflection fragments remain; no rejected reflected eye/mouth is newly exposed. Door-bar grip, down-directed waiting arms and held upper-arm contact remain within their approved source framing. Tight crowns and lower hand/finger limits are inherited, not repaired or newly certified. See [S003 native picture](stable-1080-picture-review/S003-native.jpg) and [held native picture](stable-1080-picture-review/held-native.jpg).
- **S011 / S014:** the walker and alternating support stay inside the picture; shoe/footprint softness remains source detail. The contained performer retains crown, microphone, reaching hand and both shoes; no additional push cuts them off. [Native playback capture](stable-1080-picture-review/S014-native-playback.jpg).
- **S025/S026 / S028:** the summer faces, earbud hand, wire and resting hands stay legible across the retained source split. The embrace's approaching hand and settled support retain their original framing. The cache preserves the existing holds exactly; this is not a new judgment of their duration or soundtrack placement.
- **S044 / S046 / S053:** the source limitations are plainly visible when enlarged: grainy/soft moving palm, finger and ring detail in the pleas, and softer dawn face/lap-hand linework. Raised plea hands leave the top as already recorded in their source approvals; offscreen fingers are not certified. Faces, microphone grips and visible wrist/arm connections remain readable. This final-size render adds no new defect requiring a framing change. [S044 native playback detail](stable-1080-picture-review/S044-native-playback.jpg).
- **Drawn exposures:** S016/S021/S024 [eye patches](stable-1080-picture-review/drawn-eye-details.jpg) and S023/S027/S029 [mouth poses](stable-1080-picture-review/drawn-mouth-detail-A.jpg) remain registered without a new rectangular seam, duplicate mouth or displaced feature. S029's second plate was also checked in [native detail](stable-1080-picture-review/drawn-mouth-detail-B.jpg). These remain supplied exposure animation, not newly generated body motion or verified phoneme-complete sync.
- **Other stable shots:** the sampled stationary doorway, seated-wide, room, corridor, exterior, empty-stage and dawn views preserve their whole-frame compositions at both camera extremes. Faces/hands remain intact where present; S017's feet stay inside its closest framing. No unintended blank edge, logo leakage or final-size crop fault was found.

## Actual silent playback and scope

Fifteen individual cached shots—S001 and the 14 focus shots including S020—actually played unseeked at 1×, **displayed at native 1920×1080**, in sandboxed Chromium 154.0.8037.57. They totaled 1,877 frames / 78.208333 seconds and all reached `ended`. There are no audio streams, so no listening or new music judgment is claimed.

The initial run, which captured native-size screenshots, had presentation drops in S001/S003/S011/S046/S053 and brief waiting events in the last two. Only those five were repeated without capture overhead. S003/S011/S046/S053 then completed with zero drops/corruption/errors/waits. Together with the ten originally clean runs, **14 of the 15 shots have a clean native-size run**. S001 completed both times but reported 1 and then 4 dropped presentation frames, with no corruption/error/wait; its sampled picture and fade pass, but flawless browser presentation is not claimed. Both original and retry telemetry are preserved, rather than replacing the initial evidence.

This is real instrumented playback plus inspected native/captured frames, not continuous human viewing. It is not full-film playback. The 14 pending IDs in the frozen inventory remain outside this review, and **S032→S033 remains open** for its actual replacement. Source/provider/configuration/approval records and all caches were left untouched.

Compact [evidence hashes](stable-1080-picture-review/evidence-sha256.json), frozen plan/inventory, checks, telemetry and generation scripts are retained beside this report. Raw extracted frames, native captures and independent reconstructions remain in ignored `build/stable-1080-picture-review/`. No provider calls were made.
