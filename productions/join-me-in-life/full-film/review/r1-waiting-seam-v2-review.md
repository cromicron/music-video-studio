# Waiting geometry-only v2/v3 seam review — 2026-11-07

**FAIL the S019→S020 sequence join at master f2273 / 94.708333 s.** Matching the canvas fixes the border/scale error but does not fix the residual same-composition face and drawing reset. The accepted S019 source interval remains valid. This independent outside review follows the retained Be Ambitious review requirement and leaves the [earlier report](r1-quiet-sequence-review.md) frozen.

| Frozen export in `exports/` | Frames | SHA-256 |
|---|---:|---|
| `Join_Me_in_Life_Waiting_Correction_Context_Proof_v2.mp4` | 415, S018–S020 | `aa2fe01cec22d7c9d918f397f27e96f67c0395d6be16ba178067e5c61fb38d7a` |
| `Join_Me_in_Life_Waiting_Correction_Context_Proof_v3.mp4` | 649, S018–S022 | `c432ad864108a1f1700c84b5b7a61f16353b0b2d250eb080d3eeff062ba959a6` |

Config hashes: v2 `56a57a73fa35b3933453175733acd2c0afeffb947d3319cd92858d8b53a299d8`; v3 `135eca71a85720b8d87ad45e21014519724089f792a8bbb7c6206d5584310e8c`. Both use editor 1.6.2, 960×540, 24 fps. Indices are zero-based; the contexts begin at master f1994 / 83.083333 s.

The 279 frames of S018/S019 are pixel-identical to the original context. V3's first 415 decoded frames are pixel-identical to v2, so the reviewed S019→S020 defect is identical in both. V2 corrects S020 only; v3 applies the same guide canvas to S021 and extends coverage through S022. Neither changes the accepted motion interval or shot boundaries.

| Exact join | Result |
|---|---|
| S019→S020, local f278→279 / master f2272→2273 | **FAIL residual image reset; PASS canvas correction.** Both sides now retain 8-pixel side padding. Her eyelids abruptly open/change shape; her jaw, hair and shoulder contours shift. His jaw/neck/coat contours and hair detail switch abruptly to the original drawing. Crisper linework and changed shading amplify this reset. The image remains recognizably the same two people, but the near-identical framing presents a visible continuity jump. |
| S020→S021 in v3, local f414→415 / master f2408→2409 (100.375 s) | **PASS.** The same source artwork, stationary composition and padding continue. Mean absolute RGB difference is only 0.10554/255 across the adjacent encoded frames. V2 alone did not contain this outgoing cut; v3 closes that scope. |
| S021→S022 in v3, local f552→553 / master f2546→2547 (106.125 s) | **PASS.** A deliberate change to the wider seated composition makes the scene change legible. It does not repeat the same-composition scale defect. |

[Native adjacent-frame evidence](r1-waiting-seam-v2-review/v3-joins-native.jpg) shows all three joins. Original S020 eye exposure phases were inspected; the short eyelid overlays remain registered after canvas fitting. The failure is at the incoming cut, not an assertion that the entire eye sequence fails.

**Required next correction:** replace the same-composition reset with either a drawing matched to the actual generated endpoint pose/detail or a deliberate, sufficiently distinct composition at S020. Another padding/scale adjustment alone will not resolve it. The author's proposed tighter stationary S020 view of his anxious face is a new candidate: its crown, facial framing, shoulder edges, eye treatment, incoming cut and return to S021 need their own review. No new hold or source crop is authorized by this report.

V3 actually played from beginning to end, unseeked, at **1×** in sandboxed Chromium 154.0.8037.57, with audio enabled/unmuted at volume 1. Duration: 27.041667 s media / 27.1466 s wall; 649 video frames, 648 frame callbacks, zero dropped/corrupt frames, no errors, waiting or stalled events. Native frames and actual [before](r1-waiting-seam-v2-review/waiting-v3-playback-11.40.jpg)/[after](r1-waiting-seam-v2-review/waiting-v3-playback-11.80.jpg) playback captures were inspected. This is instrumented real-time playback plus frame inspection, **not continuous human viewing or subjective listening**. The author manifest's audio correlation is 0.9997643014 at zero offset; that is technical alignment evidence only.

[Checks](r1-waiting-seam-v2-review/checks.json), [playback summary](r1-waiting-seam-v2-review/playback-summary.json), compressed complete callbacks, frozen export manifests, reproduction scripts and [SHA-256 inventory](r1-waiting-seam-v2-review/evidence-sha256.json) are retained in the adjacent folder. Raw evidence is in ignored `build/r1-waiting-seam-v2-review/`. No source/config/provider changes were made by the reviewer. S032→S033 remains **open**, awaiting the actual replacement footage and its own seam review.
