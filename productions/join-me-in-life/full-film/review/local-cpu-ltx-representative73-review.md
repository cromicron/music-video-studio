# Local CPU LTX 512×288 / 73-frame candidate — independent review

Reviewed 6 November 2026. **Verdict: meaningful local character-motion evidence, but the full-frame shot is not approved for production because the reflection does not follow her head turn.** This is distinct from the coherent, nearly still `corrected49` test and from the rejected initial noisy output. It also precedes, and says nothing about, the separate explicit-action test.

## Exact artifact and review scope

- File: `research/local-cpu-test/representative73/ltx_cpu_2b_73f.mp4`.
- SHA256: `f574aa06a888cde73f1084e593c03f0f5ae45b8e1e11d293434278e2b04d24b3`.
- H.264, 512×288, 24 fps, 73 frames, 3.041667 s. Last frame timestamp 3.000 s. No audio stream.
- Source: `assets/her_window.png`, SHA256 `ad7fea94f2ef90c5151fc81f5cfdaa12ea4e102e869e95a47087e9ea413d6779`.
- Read the adjacent `prompt.txt`: keep the exact three-quarter profile and downward gaze, tiny shoulder breath/loose hair movement, eyelids soften and reopen, reflection follows exactly, locked camera, no dialogue. Its prose says two seconds although the generated duration is three seconds; this review covers the entire actual file.
- Independently decoded all frames, inspected all 73 chronologically at native dimensions on `cpu-representative73-all-frames-1.jpg` through `-4.jpg`, compared the exact source again, and inspected the generator's all-frames sheet. Additional selected native frames are saved as `cpu-representative73-NN.png`.
- **No normal-speed playback, listening, lip-sync or music-timing claim.** No source, generation code, or edit was changed.

## Time-specific findings

| Frames / time | Finding |
| --- | --- |
| 0–8 / 0.000–0.333 s | Recognizable initial source profile; eyelids begin to lower. Hair, pendant, sleeves, chair and room retain their identities. Face detail is already softer than the source. |
| 9–17 / 0.375–0.708 s | A visible eyelid closure/softening followed by reopening is readable. The face begins moving away from the precise original side angle. This is more than encoding noise or a camera move. |
| 18–35 / 0.750–1.458 s | Head turns progressively toward a more frontal bowed angle. Nose silhouette, jaw and hairline change with the turn. The motion proceeds without an obvious one-frame geometric break, but the reflection keeps approximately the original side-facing head, making the discrepancy clear by about 1.000 s. |
| 36–59 / 1.500–2.458 s | Actual face becomes substantially more frontal while staying downcast; reflected face remains side-facing. The changing face becomes smoother and more generic, with reduced freckles and hair/eye detail. Neck still joins the shoulders; I do not observe literal head detachment. |
| 60–72 / 2.500–3.000 s | Ends in a different, nearly frontal lowered-head pose. Reflection still fails to match. No return to the source angle or justified loop is present. |

The woman stays seated and withdrawn. Her lowered gaze does not turn into eye contact with the viewer, a smile, a recovery, or comfort directed at the man. The head turn can be emotionally plausible in isolation, but it violates the requested exact profile and cannot coexist naturally with the static reflected pose. The shot's visible reflection makes this a physical-continuity defect, not merely a preference about acting intensity.

Shoulders and torso are comparatively restrained. Hair changes mostly follow head shape and orientation; a separate loose strand moved by a draft is not clearly demonstrated. A distinct shoulder breathing cycle is not established. Hands are out of frame, so this file does not test fingers, reaching, walking, or two-person contact. Background remains stable enough that the principal subject movement cannot be dismissed as camera motion.

The 16:9 output avoids the pronounced 3:2 horizontal compression identified in `corrected49`. Character identifiers—copper hair, striped sleeves, black shirt and silver pendant—survive, but stable wardrobe is not a substitute for stable facial identity. The later simplified face needs improvement for a final reaction close-up.

## Measurements and practical conclusion

Independent decoded-pixel measurements: mean adjacent-frame absolute difference **1.5489/255**, first-to-last difference **14.1049/255**, and first-to-last RMSE **29.7911/255**. Saved in `cpu-representative73-difference-metrics.json`. These include compression and are not quality scores; the chronological images establish the actual turn and failed reflection.

The generator's saved metrics report **421.13 seconds**, four CPU threads, and **7,758,139,392 bytes peak RSS**. This reviewer did not rerun generation or spend credits.

No production range is approved. The least-changed opening is too brief to solve a useful sustained reaction shot, and cropping out the reflection would create a different, much tighter low-resolution composition requiring its own review. Keep this result as a concrete demonstration that local CPU generation can create continuous character movement. A subsequent test should be judged on its own frames; a shot without a visible face reflection would isolate the model's basic acting capability more cleanly. This single failure is not a conclusion that the entire local route cannot work.
