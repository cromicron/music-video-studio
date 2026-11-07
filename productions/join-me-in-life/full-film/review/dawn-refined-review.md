# Exterior dawn redraw — independent static-source QC

Reviewed **7 November 2026 UTC** against the actual original, refined candidate and approved A01 character pair. **Eligible as a wide static source for the existing proposed dawn ending, with the wardrobe and framing limits below.** This does not approve the dawn narrative, a cure, movement, a new edit or the full film.

| Source | Dimensions | SHA-256 |
| --- | --- | --- |
| `assets/dawn_together.png` | 546×306 | `beb56c89bd71278fbe12496b58fe0ea5dffe887a015d28daad56a1fc7cb1e1ce` |
| `assets/dawn_together_refined_candidate.png` | 1672×941 | `18e3e54b7d0c013d1997d7a634909a11d765ff05f81f0ba315577fbb6711a459` |
| `../current/assets/A01_Approved_Character_Pair.jpg` | 1536×1024 | `3ad6da23fcfd9f45fa1bf13cfdc67a5ddda15bef133dbc4d60cbcb3df7066e14` |

## Emotional and scene continuity

The exterior hospital bench, snowy vegetation and bare trees, hospital façade, distant skyline, warm bollard light and pink/gold morning sky preserve the original scene. She looks away and slightly upward, with her hands resting on her lap; he watches her with a serious, concerned expression and keeps his hands on his own knees. There is no embrace, comforting role reversal, triumphant gesture or visible smile. Warmer light is a time-of-day change, not evidence that she has recovered. The proposed outdoor ending remains a proposal.

Copper/brown hair, eye coloring, light facial hair, earrings/pendants and black/purple present-day clothing remain compatible with A01. Detailed outlines and shaded fabric remain drawn anime. The redraw strengthens facial and environmental detail, changes strands, bench texture, window divisions and hand contours, and slightly repositions proportions. It is not an exact upscale or a matched animation endpoint.

## Anatomy, hands and support

Both heads connect continuously through their necks into the collars and shoulders. Her lifted chin is supported by a slender neck; his slight turn toward her does not produce a visibly broken jaw/neck or detached shoulder. Their torsos and hips sit plausibly on the bench, with thighs extending forward; no conspicuous floating pelvis or seat passing through a body is visible. Seat/back slats and visible vertical supports form a coherent bench, with reasonable snow/vegetation occlusion. Feet and parts of the lower supports are outside the source frame, so neither foot contact nor the entire bench construction is certified.

His two forearms remain individually traceable from rolled sleeves to the hands resting together over his knees. Visible finger contours separate without an obvious extra finger or fused hand, although overlapping fingers/thumbs do not permit independent counting of every digit. Her forearms converge into overlapping passive lap hands; the visible upper hand follows the thigh, with no evident detached wrist. These occlusions are acceptable for this still, but do not establish correct finger separation during later movement.

**Wardrobe caveat:** the exposed fingers have no clearly drawn rings, while A01 includes finger jewelry. The tiny original does not resolve this detail well enough to establish whether its omission is new. Preserve this as an explicit continuity item for final art/hand close-up approval; do not claim exact jewelry matching or invent hidden rings. The pendants and his visible studded wristband remain present. This caveat does not prevent use as a wide planning source; it does prevent blanket approval of all costume details.

## Existing uses and camera limits

The existing outdoor-dawn uses are S053 (243.416667–247.125 s), S056 (259.416667–265.500000 s), and S058 (271.208333–277.791667 s). Each uses a centered 1.015→1.075 push; S058 alone fades during its final two seconds. Both crowns, faces and visible hands have sufficient margin for these crops. Lower legs/feet remain outside the composition as in the source; do not present the shot as full-body contact validation. Native hand/face detail crops are retained in `build/art-candidate-review/`.

The separate `edit-art-candidate.json` uses this exact source consistently in all three places while preserving shot order, duration and the final fade. Actual FFmpeg first/middle/last frames for this camera path were subsequently inspected in `build/art-candidate-review/camera-09-dawn_together/`: both crowns, faces and visible hands remain safely in frame. The representative S053 sample contains no fade; S058's existing final-two-second fade remains unchanged in the configuration and was not newly rendered as a full ending here. The redraw is 1672×941, so a 1920×1080 export enlarges it; it is not native 1080p art. No source file or original `edit.json` was changed by this review.

## V2 jewelry correction — independent static-source recheck

Reviewed **7 November 2026 UTC**. Source: `assets/dawn_together_refined_v2_candidate.png`, **1672×941 RGB**, SHA-256 **`452839fce63dfdd7046fdcc07a0bf2af33f7357429042c024a9f0cf11a0b6eb5`**. Compared the actual full v1/v2 images, native hand crops and both characters' visible ring references in the exact A01 file listed above. Portable comparison: [v1/v2 hand details](dawn-refined-evidence/v1-v2-hands.jpg).

**Verdict: v2 is suitable to replace v1 as the static planning source for S053/S056/S058 and as an input for a future restrained motion test.** The visible thin silver finger bands now agree with A01's jewelry language and resolve the exposed-finger omission recorded above. The bands follow the visible finger surfaces; they do not read as floating jewelry, an extra digit or a connector fusing the hands. This is a visible-jewelry continuity pass, not certification of hidden rings or an exact count on occluded fingers.

Her upper lap hand remains passive and supported by the thigh; his overlapping hands remain supported over his own knees. Wrist connections, finger outlines, necks, shoulders, seated hips and the visible bench supports show no apparent new anatomical or contact defect. Full-image comparison retains their faces, clothes, seated relationship, camera composition and hospital/snow/dawn environment. She still looks away and slightly upward; he remains concerned rather than relieved. No smile, embrace, comfort reversal or visual claim of recovery was introduced. These are visual observations, not a claim that pixels outside the rings are unchanged.

The prior framing limits still apply: feet remain outside the source, overlapping digits are not all individually visible, and 1080p delivery enlarges 1672×941 art. The v2 full source preserves the visible crown/hand margins used by the existing centered 1.015→1.075 camera; this check did not rerender that camera or change either configuration. The earlier FFmpeg camera evidence belongs to v1. Future generated movement must separately retain the passive lap, supported heads/bodies, worried/away gaze and ring/hand geometry through intermediate frames. **No moving clip, completed edit or proposed dawn story ending is approved by this still review.**
