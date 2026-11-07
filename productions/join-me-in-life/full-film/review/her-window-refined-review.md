# New still candidates — independent review

Reviewed 6 November 2026 against the actual source images and approved A02. These are proposed animation inputs, **not accepted replacements in the current edit**. No source or edit was changed by this reviewer. A still review cannot approve generated movement.

## Refined window reaction

`assets/her_window_refined_candidate.png`: 1672×941, SHA256 `9778c0c714d6a58eda8ed9b09f6acd51ab075aa16cb4578fae8b9099a0230eb7`.

Compared directly with `assets/her_window.png` (546×306, SHA256 `ad7fea94f2ef90c5151fc81f5cfdaa12ea4e102e869e95a47087e9ea413d6779`) and `art/00_References/A02_Approved_Anime_Window.png`.

**Verdict: suitable candidate for a restrained window-reaction close-up, subject to separate movement review.** Her auburn hair, green eye, freckles, hoop earring, silver pendant and black/purple clothing remain consistent. Shoulder, neck and head support read coherently. The inward/downward gaze and tense, quiet mouth preserve her withdrawal; the image does not imply recovery or make her comfort him. The detailed drawn treatment is compatible with A02, although the side profile naturally reads differently from A02's more frontal view.

This is a redraw/refinement, not a pixel-exact upscale: hair strands, facial lines, eye rendering, necklace and background detail change. Treat it as a new source with its own hash. It has no visible hand region, so it proves nothing about hand anatomy.

The crown intersects the top edge in **both** the original `her_window.png` and this candidate. The crop is much tighter than full-figure A02, but calling the cut crown a newly introduced defect would be inaccurate. For a deliberate reaction close-up this crop is usable; it does leave almost no upward camera margin. Additional zoom or upward head movement could make framing cramped. Prefer a locked frame and a small eye/chin action inside the visible bounds rather than enlarging it further. The window reflection will need its own temporal check during any eye/head animation.

## Bridge gesture starting pose

`assets/bridge_plea_start_candidate.png`: 1672×941, SHA256 `2fa46ef059bc3e0327c08b2252df5757140e92e97a1496f5cc5c1d9a4cba2840`.

Intended ending pose: `art/04_Performance/P03_Bridge_Plea.png`, 1672×941, SHA256 `8319935b361b791e790c3f5631c19287b28e715c5fae5a94d4d8d82f7eff07ed`. Native hand comparison: `bridge-keypose-hand-comparison.png` in this directory.

**Verdict: plausible controlled-gesture test input, with an unresolved folded-finger readability risk.** The candidate holds his left hand near his abdomen, palm upward, with a continuous forearm leading to the bent elbow and sleeve. It does not read as a detached hand. Extending that arm toward the ending pose is anatomically plausible. It is a substantial extension and wrist rotation, not a movement proved by these endpoints.

Head angle, worried blue eyes, facial hair, open screaming mouth, right-hand microphone grip/cable, pendant, stage curtain, drum kit and lighting align closely with P03. The shoulder and jacket folds change in ways consistent with the arm being lowered. His distress is already fully present at the start, appropriate to the rule that the first bridge plea is screamed.

Jewelry correction: the original P03 already has **two visible rings on the reaching hand**—a broad ring and a smaller band on one of the curled fingers. The candidate's small band is therefore not, by itself, an invented extra ring. The microphone-hand ring and wristband are also retained.

The end pose shows five readable digits. The start pose has overlapping curled fingers: thumb and two raised finger contours are clear, while the remaining finger contours merge/occlude near the underside of the palm and smaller ring. I cannot certify five independently traceable digits in this starting pose. Occlusion can be legitimate, so I do not assert a definite extra/missing finger from this still. For generation, this is the most important area to inspect frame by frame: digits must separate coherently, retain ring placement and avoid fusing as the palm rotates outward. The two keyframes alone do not establish correct intermediate geometry, hand-to-torso contact, or a natural four-second performance. A successful result must also preserve the head/mic alignment and screaming expression through the gesture, not merely land on the endpoint.
