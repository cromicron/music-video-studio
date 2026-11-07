# Waiting and aftermath camera corrections — focused review

Reviewed **7 November 2026**. **Both camera corrections pass. Use these corrected camera settings in the next workprint.** The frozen [full-workprint-v1 review](full-workprint-v1-review.md) and its original defect evidence remain unchanged. This verdict clears the two framing/join defects, not the still-unfinished character motion or complete film.

| Exact reviewed proof | SHA-256 | Coverage |
| --- | --- | --- |
| [Waiting join](../exports/Join_Me_in_Life_Waiting_Join_Fix_Proof.mp4) | `745b0e6ebec2120afbde1177fb34faadfefececa6c3bdb9d0c85275d5d1fc118` | S019–S020, full frames `[2141,2409)`, 268 frames / 11.166667 s |
| [Aftermath joins](../exports/Join_Me_in_Life_Aftermath_Join_Fix_Proof.mp4) | `cb7981f840ab42c6c19e1c14f705c8c08747634b4f97774c6e7a547ca0628ccf` | S041–S043, full frames `[4697,4989)`, 292 frames / 12.166667 s |

Both manifests pin config SHA-256 `424864992036d0c9b6bbc88cc4543913432da7e18151e2506953a60d7901a3a5`. Frames are zero-based at 24 fps; both proofs are 960×540.

**Waiting:** inspected actual encoded first/middle/last frames of both shots and adjacent frames around full f2272→2273 (94.708333 s). S019 now preserves the visible upper hair silhouette at the same safe 1.0 framing as S020. Face, shoulder, window and door geometry carry across without the former outward scale jump. Compare the [corrected seam](camera-fix-review/waiting-seam-132.jpg) with the [v1 seam](full-workprint-v1/waiting-reset.jpg). Her withdrawn gaze and his concern remain unchanged; the existing S020 blink treatment is retained.

**Aftermath:** actual encoded f4792→4793 (199.708333 s) and f4890→4891 (203.791667 s) now maintain the same 1.0 framing. The small punch-in and return are gone; his arm/hand contact, her passive lap and away gaze, and both faces stay registered. [First corrected seam](camera-fix-review/aftermath-seam-96.jpg) · [second corrected seam](camera-fix-review/aftermath-seam-194.jpg). Compare with the frozen v1 [inward](full-workprint-v1/aftermath-small-punch-in.jpg) and [outward](full-workprint-v1/aftermath-small-pull-out.jpg) jumps. No second reach, contact reset or new edge crop was introduced. These are held drawings awaiting the planned motion, not newly animated acting.

The [first/middle/last sheet](camera-fix-review/first-middle-last.jpg) covers all five shots. Independent decoded frame-hash comparison with workprint v1 confirms **only S019's 132 frames and S042's 98 frames changed**. Every frame of S020, S041 and S043 is unchanged. Shot boundaries, source records and drawn-exposure records match v1. Corrected seam mean absolute RGB differences are approximately 0.074, 0.051 and 0.050 on the 0–255 scale: small encoding differences remain, so pixel identity across separate encoded shot boundaries is not claimed.

The render manifests report original-song excerpt offsets of 89.208333 s and 195.708333 s, waveform correlations of 0.999815580 and 0.999972354, each at zero lag. Those existing audio checks were not independently rerun here. This focused camera review used decoded images and numeric comparisons; no new full-file playback or subjective listening is claimed. The prior workprint playback record remains bound to v1.

[Checks](camera-fix-review/checks.json) and [reproduction script](camera-fix-review/reproduce.py) retain exact hashes and comparisons. Compact JPEG evidence is portable; individual diagnostic frames are under ignored root `build/camera-fix-review/`. No production source/configuration, original review, provider account or credits were changed.
