# Corrected local CPU LTX candidate — independent review

Reviewed 6 November 2026 by the independent audio/story/visual reviewer. This is a separate retake review; `local-cpu-ltx-review.md` continues to describe the rejected first output.

**Verdict: coherent, stable quiet-insert feasibility result; not accepted for the current edit and not evidence of substantial character acting.** The scheduler correction has made a decisive practical difference to this output. The woman remains recognizable across all 49 frames instead of dissolving into noise. Motion is nevertheless very close to a held drawing.

## Artifact and method

- File: `research/local-cpu-test/corrected49/ltx_cpu_2b_49f.mp4`.
- SHA256: `153f112f54dedc939eae3c0483b60c899be6ef53680c091de649d52bf25d95dc`.
- H.264, 384×256, 24 fps, 49 frames, 2.041667 s; final frame timestamp 2.000 s. No audio stream.
- Independently decoded the complete file and inspected every frame chronologically at its native 384×256 size on three contact sheets, plus native frames 0, 12, 24, 36 and 48. Compared against `assets/her_window.png` and approved A02. This is **not a normal-speed playback review**, and it provides no music-sync judgment.
- Evidence: `cpu-corrected49-all-frames-1.jpg` through `-3.jpg`, five `cpu-corrected49-NN.png` files, and `cpu-corrected49-difference-metrics.json` in this directory. The adjacent original `all-49-frames.jpg` was also inspected, but the larger independent sheets control this assessment.

## Temporal findings

| Interval | Observation | Consequence |
| --- | --- | --- |
| 0.000–0.333 s, frames 0–8 | Slight opening/reshaping around the visible eyelid and pupil; small cheek/hair-line changes. | A subdued reaction is plausible. There is no fully closed eyelid to support a claim of a complete blink. |
| 0.333–1.458 s, frames 8–35 | Profile, neck, shoulders, pendant, chair and gaze direction remain almost fixed. | No gross head detachment, abrupt turn, limb invention or narrative reversal is visible. No clear shoulder breath or loose-strand excursion is demonstrated either. |
| 1.500–2.000 s, frames 36–48 | The same withdrawn pose holds, with very small facial/detail variation. | Coherent end to a quiet insert; no completed new action and no justified loop claim. |

The face remains oriented down and toward the window, not toward the viewer. Expression stays subdued. Hands are outside the shot: this cannot certify finger animation or interpersonal contact. The window reflection remains similarly still; the tiny face change is insufficient to certify precise mirrored eye tracking. No obvious reflection jump is apparent at this resolution.

The render is softer and simpler than the original, especially eye/freckle/hair detail. Identification is retained mainly through copper hair, profile, striped sleeves and pendant. These 384-pixel frames do not establish final 960×540 quality.

## Aspect ratio and measured movement

This test has an avoidable aspect-ratio problem. The 546×306 input is approximately 16:9, while the output is 3:2. The installed `LTXConditionPipeline` calls `video_processor.preprocess(condition_image, height, width)` without a resize mode; the installed processor's default PIL branch calls `image.resize((width,height))`. This compresses horizontal proportion by approximately 16% relative to vertical, matching the narrower face/torso in the output. It is a preprocessing issue, not evidence that the model invented a neck deformation. A 512×288 run will closely match the source ratio.

Independent decoded-pixel measurements give mean adjacent-frame absolute change **0.0956/255**, first-to-last change **1.5055/255**, and first-to-last RMSE **4.0438/255**. Differences cluster more around the face than the static background. These values include lossy compression and are not a natural-motion score; they support the visual finding of very small change, not a mathematical proof of acting quality.

The saved generation metrics report **208.70 s**, four CPU threads, and **7,306,973,184 bytes peak RSS**. These are generation-process measurements read from its record, not measurements made by this reviewer. No new generation, API credits or purchases were used for this review.

## Use decision

Retain the complete 0–2.041667 s file as evidence that the corrected local route can produce a coherent quiet portrait. Do not insert this 3:2, low-resolution test into the final cut or use it to claim the 58-shot film is animated. The next useful judge is the correctly proportioned run and a deliberately modest but visible eye/chin action, reviewed across every frame. No approved production range is assigned here. A restrained hold can be artistically valid; it simply does not establish walking, reaching, pleading or embracing capability.
