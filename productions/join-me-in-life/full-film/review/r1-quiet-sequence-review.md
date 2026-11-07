# R1 quiet insertions and current sequence joins — 2026-11-07

**Verdict: PASS the three exact motion insertions; REQUIRE FIX at two outgoing joins before passing these context sequences.** This independent outside review follows the retained Be Ambitious review requirement. It does not reopen the accepted source acting verdicts or authorize generation. Source/config/provider/approval records were not changed.

Reviewed config SHA-256: `89b6606ee95ddec4026493e548ea821bebb56886b6e59431063cc5ae1a8ae22b`. All frame indices below are zero-based; ranges exclude their endpoint. Proofs are 960×540 at 24 fps.

| Export in `exports/` (prefix `Join_Me_in_Life_`) | Frames | SHA-256 |
|---|---:|---|
| `Waiting_Correction_Proof.mp4` | 132 | `1fd2f4b81592fdb8702322410840a55d9a4065469224383cbce628d080bbd978` |
| `Waiting_Correction_Context_Proof.mp4` | 415 | `b1f61bd2b17ec7e05596d0add089902a17cb300c14e86dc239c9c83ed577e4f8` |
| `Held_Correction_S030_Proof.mp4` | 98 | `41fe5fb16d18732537cb44f55eafd8351c53527810f63eaf489d5cf9b55fbd0c` |
| `Held_Correction_S032_Proof.mp4` | 96 | `7a3f1b928cc6a2f44dfa90c21c2712f027bedd990235c7dc2afc885804aa0725` |
| `Held_Correction_Context_Proof.mp4` | 495 | `8fa53bf00a736e054331c54f0cb37fbe91a602f44d2eacacb3013eba2937fdf9` |

## Exact insertion and containment: PASS

An independent frame-index trim reconstruction with the renderer's actual CRF 18/veryfast settings matches **every decoded RGB frame exactly**: 132/132 S019, 98/98 S030, 96/96 S032, maximum mean absolute RGB error 0. All five exports decode fully without errors. Each standalone proof also exactly matches its context slice.

| Shot | Accepted source frames | Master frames | Context frames | Result |
|---|---|---|---|---|
| S019 | R1L04 `[3,135)` | `[2141,2273)` | waiting `[147,279)` | PASS |
| S030 | R1L05 `[3,101)` | `[3526,3624)` | held `[102,200)` | PASS |
| S032 | R1L05 `[101,197)` | `[3724,3820)` | held `[300,396)` | PASS |

The reconstruction explicitly uses `scale=944:540:flags=lanczos,pad=960:540:8:0`, so the entire native 896×512 source is contained with 8-pixel sides, no extra zoom/crop, no duplicate interval, no added lead/end hold and no change to 24 fps cadence. Source hashes are R1L04 `664552573bc9da7d8c4da90bbf9978f80c3eb45435be4d3336ffb03270d51e51` and R1L05 `0a8e44b2dbc7c5038ecc0667214aae0375b3f0e2e5320fc7996a1f00ea3be24b`.

Encoded phases preserve the source verdicts: S019's arms stay down toward separate own laps; S030/S032 keep outer-upper-arm contact and passive lower hands. His brief outward glance then return remains coherent anxious attention across the exterior interruption. Her gaze remains withdrawn; no pointing, new embrace, hand release/regrip, cure or identity replacement appears. Native crown/finger edge tightness and softer generated detail remain source limitations, not added insertion defects. See the [R1L04](ltx23-correction-R1L04-review.md) and [R1L05](ltx23-correction-R1L05-review.md) reviews for the full source assessment.

## Actual cuts

| Join | Master first frame after cut | Judgment |
|---|---:|---|
| S018 corridor → S019 waiting | 2141 / 89.208333 s | PASS: clear change of composition; no blank frame or added crop. |
| S019 generated waiting → S020 existing drawing | 2273 / 94.708333 s | **REQUIRE FIX:** contained image changes abruptly to full-width art in the same composition; border/scale and face/line detail reset. |
| S029 performance → S030 held | 3526 / 146.916667 s | PASS: legible scene change; frightened contact is already established. |
| S030 held → S031 exterior | 3624 / 151.000000 s | PASS: intended exterior interruption. |
| S031 exterior → S032 held | 3724 / 155.166667 s | PASS: contact and posture continue. Source f100 resumes as f101 after the exterior, without replay. |
| S032 generated held → S033 existing still | 3820 / 159.166667 s | **REQUIRE FIX:** side padding disappears and the same composition expands/sharpens with a small face/linework reset. |

The two failures are visible in the [native adjacent-frame pairs](r1-quiet-sequence-review/outgoing-joins-native.jpg), particularly S019→S020. The picture goes from a 944-pixel contained width to the following art's full 960-pixel width. The resulting edge/scale pop accompanies the generated-to-original detail change. These are actual same-composition cut defects, not automatic rejection because a source prompt omitted a distinct blink/breath.

**Specific correction:** match the following S020 drawing and S033 still to the fitted-guide/contained canvas, including padding and picture placement, while preserving S020's existing eye-exposure timing, all shot boundaries and accepted motion. Do not crop the accepted motion to make it fill the screen or add a hold to conceal the cut. Re-render these two short seams and check the remaining face/linework reset after the geometry correction; this review does not pre-approve the result. A later S033 motion replacement requires a fresh seam review.

## Playback and evidence limits

Both full context exports actually played unseeked at **1×** in sandboxed Chromium 154.0.8037.57, with audio enabled, unmuted and volume 1. Waiting: 17.291667 s media / 17.3907 s wall, 415 total frames; held: 20.625 s media / 20.7783 s wall, 495 total frames. Both reached `ended` with zero dropped/corrupt frames, no playback error and no waiting/stalled events. Frame callbacks recorded 414 and 494 frames respectively; the browser's playback-quality counters cover all 415/495 frames. Actual-playback screenshots and separately decoded native cut/phase frames were inspected.

This is instrumented real-time playback plus visual frame inspection, **not a claim of continuous human viewing or subjective listening**. Audio correlation is the separately identified author-manifest result: 0.999475–0.999802 at zero offset against master `0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb`. It supports technical alignment only.

Compact [encoded checks](r1-quiet-sequence-review/encoded-checks.json), [playback summary](r1-quiet-sequence-review/playback-summary.json), compressed full callback telemetry, overviews, phase sheets and [other joins/contact continuity](r1-quiet-sequence-review/other-joins-and-held-continuity.jpg) are retained in the adjacent folder with [SHA-256 inventory](r1-quiet-sequence-review/evidence-sha256.json). `reproduce.py`, `playback.py` and `retain_evidence.py` reproduce that evidence from these hash-bound exports; raw frames, captures and reconstruction videos remain in ignored `build/r1-quiet-sequence-review/`. No provider calls were made.
