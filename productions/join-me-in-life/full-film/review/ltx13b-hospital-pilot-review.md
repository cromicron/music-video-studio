# LTX 13B hospital pilot — independent motion review

Reviewed 2026-11-07 UTC. **Whole intended take: REJECT. Separate later-aftermath use of 6.000–8.033333 s: PASS at the visual source-review gate, with the scope below.** The tail is not rejected merely because the preceding reach failed; no inherent blocking tail defect was found.

Exact video: `assets/motion/ltx13b-hospital-pilot/video.mp4`, SHA-256 **`b59ddfc08ed7499cf8f306517a3cce9fabc0528054b85cc86e9173c037773856`**. H.264, 864×480, 30 fps, 241 frames, 8.033333 seconds, no audio stream. Times are clip-relative. Frames are **zero-based**.

## Review basis

Inspected every decoded frame in chronological sheets, dense native hand crops through the initial lift and later shoulder contact, native face samples throughout, 13 additional native whole-frame tail samples, and the final three frames beside the prepared endpoint. Compared `image.png`/`end_image.png` with the established M01 endpoint direction. `render.json` identifies original start SHA `259124c27ba71ae4785927457fda743f20a954e38b86ce19ce655866e408b64f` and end SHA `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10`. These are constraints, not proof that the generated intervening action is correct.

## What the complete take actually does

| Source interval | Observation | Verdict for the intended complete action |
| --- | --- | --- |
| 0–0.400 s, f000–011 | Her initial withdrawn pose and his concerned attention remain. His right arm begins lifting from his lap. | Useful initial intention; too short and incomplete to establish the action. |
| About 0.400–1.033 s, f012–030 | Hand rises in a high arc across her face and over her head. Finger/hand edges visibly smear and ghost, particularly about 0.400–0.733 s. She turns her eyes/head toward him by about 0.600 s. | Reject: wrong path and gaze, with an uncertifiable moving hand. Blur is recorded as visible blur, not an invented exact extra-finger count. |
| About 1.033–2.833 s, f031–084 | His palm settles on her crown and remains there. She repeatedly looks toward him, with occasional blinks. | Reject: prolonged head-pat/hold replaces the requested direct upper-arm contact. Her active look changes the established withdrawal. |
| About 2.833–4.267 s, f085–127 | Hand lifts away from her head, then travels down behind/around her shoulder. Fingers are simplified/merged during parts of this repositioning. Her gaze lowers again. | Reject as the required single reach. This is a second stage after a different completed touch, not the intended uninterrupted reach to her upper arm. |
| About 4.267–4.400 s, f128–131 | Fingers begin resolving against the outer upper arm; the grip becomes readable. | Contact is actually shown; do not claim it is wholly skipped or teleported. |
| About 4.400–6.000 s, f132–179 | One inward pull/settle becomes readable after contact. The right hand belongs to his arm and stays on her upper arm. Her arms remain low/passive. | Useful contact/pull reference, but it cannot retroactively repair the rejected preceding head contact and gaze. Not separately approved here. |
| **6.000–8.033333 s, f180–240** | Coherent held aftermath with a small continuing settle/composition change, no additional reach or pull. | **PASS only as the separate later-aftermath shot described below.** |

No hard cutaway, return to the separated starting pose, or second torso pull was seen. The unintended crown contact is itself sufficient to reject the requested full action. This is not a finding that she becomes his comforter: her hands never reciprocate the embrace, neither person smiles or displays a cure, and he still looks concerned. The concrete deviation is her turn toward him and his added head-pat/hold.

## Scoped tail pass

**Usable source interval: [6.000000, 8.033333…) seconds = f180–240 inclusive, 61 frames / 2.033333… seconds at 30 fps.** This passes the whole-frame visual check as a later shot of already-established physical closeness, not merely as a hand crop.

His visible gripping hand has a readable thumb plus four fingers, stays associated with his right arm, and maintains contact with her outer upper arm without a conspicuous detached wrist, penetration or sliding grip. Her forearms/hands remain passive toward her lap; no reciprocal consolation occurs. Lower fingers are partly outside the bottom crop in earlier tail frames, so unseen digits are not certified. Both heads remain supported by their own necks. She looks down/away and he remains worried/tired; the result is unresolved presence, not clinical improvement or a romantic recovery cue. No ghosted/doubled face or hand was found at the endpoint, unlike the bridge pilot.

Identity, present-day wardrobe, pendant, illustrated room and seat relationship remain recognizable. Fine facial/hair detail is softer and simpler than the high-resolution originals; this is still an 864×480 source, not a demonstrated high-resolution final master. The composition changes gradually toward the endpoint and room lines show some generated drift; no disruptive tail reset or major furniture collapse was visible. The pass allows this small existing settling movement; it is not a claim of an exactly locked camera.

The remaining constraints for the tail are **editorial use and delivery**, not a discovered inherent tail defect: it must follow an already-established embrace somewhere in the film, retain its unresolved meaning, and be checked in the actual crop/sequence against the soundtrack. Cutting directly from separated people to this tail would omit the central action and would not satisfy S028.

The last frame is visually clean enough to consider in a separate hold test, but **no extra freeze, looping, reverse motion or extension is approved**. The full 8.033333-second pilot is already 4.091667 seconds shorter than the planned 12.125-second S028. The approved 2.033333-second later-shot interval does not cover that scene.

## Playback evidence and limits

Actual local Chromium playback ran the complete file at **1× and 0.5×**, reaching `ended` in 8.05 and 16.08 wall seconds respectively. Both runs reported 241 total frames, **zero dropped frames, no media error and no waiting/stalled event**. See `ltx13b-hospital-independent/playback-telemetry.json`. This is headless player telemetry, not a claim that the reviewer perceptually watched/listened at normal speed. Visual judgments use the decoded chronological frames and native diagnostic images. There is no audio track; no lip-sync, phoneme or soundtrack-alignment claim is made.

Evidence is retained in `review/ltx13b-hospital-independent/`: `all-frames-01.jpg` through `all-frames-11.jpg`; six native hand sheets; three native face sheets; two native tail sheets; `endpoint-native-comparison.jpg`; selected full frames; and `verdict.json`. No sources, original exports, editor data, provider jobs or approval manifest were changed by this reviewer. Root owns the editorial placement decision.
