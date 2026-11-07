# LTX 13B bridge pilot — independent motion review

Reviewed 2026-11-07 UTC. **Reject this take for the intended bridge plea because of independently visible finger/ring discontinuities and the smeared final mouth frames. Zero full-frame intervals are approved.** It demonstrates substantial generated arm movement while retaining the character and stage, so it is useful evidence that the free GPU pipeline can attempt a gesture. It does **not** pass the natural, clean gesture/acting requirement.

Exact source: `assets/motion/ltx13b-bridge-pilot/video.mp4`, SHA-256 **`32e20fd1388ea390b910541384beb79808b958ea5eccab9ff8f5223f2f3c0a29`**, 864×480, 30 fps, 121 frames, 4.033333 seconds; no audio stream. `render.json` records LTX-Video-0.9.8-13B-distilled, seed 49, and the intended single abdomen-to-extended plea with stable rings and sustained frightened performance. No provider calls, source changes or approval-manifest changes were made by this reviewer.

## Evidence and timing

All 121 decoded frames were inspected chronologically in six labelled sheets. Native-resolution crops cover every hand frame through f060, then every fourth frame through f120; face/microphone crops cover every second frame, supplemented by the complete last five frames. Whole-frame sheets include all intervening frames. Source `image.png` and `end_image.png` were compared with the actual 1672×941 original inputs: `bridge_plea_start_candidate.png` (SHA `2fa46ef059bc3e0327c08b2252df5757140e92e97a1496f5cc5c1d9a4cba2840`) and `P03_Bridge_Plea.png` (SHA `8319935b361b791e790c3f5631c19287b28e715c5fae5a94d4d8d82f7eff07ed`). Both original endpoints depict an open scream.

Times below are clip-relative; frame numbers are **zero-based**, at 30 fps. Intervals use an exclusive end unless individual frames are named.

| Interval | Independent finding | Eligibility |
| --- | --- | --- |
| 0.000–0.100 s, f000–002 | Open mouth and near-abdomen starting pose are present. The initial overview sample was later; the generated first frame is not closed-mouthed. | Only three frames; not a useful continuous performance interval. |
| 0.100–0.567 s, f003–016 | Mouth closes/narrows almost immediately. Hand rises toward his face rather than proceeding directly to the final reach. Rings lose their defined shape; finger contours smear/merge particularly around 0.267–0.533 s. | Reject moving-hand interval. |
| 0.567–0.800 s, f017–023 | Raised palm briefly resolves into five distinguishable digits, but the rings visible in the source have disappeared while the finger bases remain exposed. | Reject jewelry continuity; a readable isolated silhouette does not fix the preceding/following movement. |
| 0.800–1.200 s, f024–035 | Hand rotates and descends outward quickly; several fingers become blurred, merged ribbons/points, especially around 0.967–1.100 s. Wrist/palm shading and width change through the transition. | Reject transition. This is more than simply hidden fingers from a valid viewing angle. |
| 1.200–3.967 s, f036–118 | Final palm, rings, forearm and sleeve settle into a comparatively coherent pose; arm is mostly held. Repeated short open/closed mouth changes continue, including a mostly closed/narrow stretch around 2.667–3.133 s. These conflict with the prompt’s sustained-open instruction; their suitability for the actual sung phonemes is untested. | Potential body/hand reference or repair material only. Full-frame performance acceptance is withheld pending song-aligned mouth review; mouth closure alone does not reject this interval. It is not a clean continuation of the rejected reach. |
| 3.967–4.033 s, f119–120 | Mouth/chin smear and ghost; f120 visibly contains doubled mouth outlines. | Reject end hold. Do not freeze the generated last frame as a clean endpoint. |

## What works and what fails

Hair, eye color, light beard/moustache, jacket, burgundy shirt, pendant and distressed brow remain recognizable. Head-to-neck/torso support stays plausible. Shoulder and elbow remain attached; the arm's broad path is physically possible, rather than an impossible detached limb. The high lift is an unrequested detour, not by itself proof of impossible anatomy. There is one overall lift-and-extension followed by a hold, not four separate pleas. Most displacement finishes by about 1.2 seconds, leaving roughly 2.8 seconds of held arm pose.

Microphone, gripping hand and cable are comparatively stable, without a conspicuous released grip or penetrating finger. The mic stays beside the mouth; the original inputs themselves do not show literal lip-to-grille contact throughout. The generated mouth shape/distance changes, so do not claim the prompt's exact contact constraint has been proved. Stage geometry and lighting remain comparatively steady; no new photographic treatment or cast appears.

The independently sufficient rejection reasons are **finger/ring discontinuity and visible mouth/chin ghosting in f119–120**, not global loss of identity or ordinary mouth closure. The repeated open/closed changes do fail the prompt’s literal sustained-open-mouth instruction, but that instruction is not an adequate rule for natural singing: consonants and phrasing can legitimately close or narrow the mouth. This silent take has not been aligned with the actual song phonemes, so neither audio-sync failure nor correct synchronization is established. Whether the intermediate mouth motion suits the performed line remains unjudged. The last-frame ghosting is a visible image defect independent of phoneme timing and prevents relying on that generated endpoint.

## Playback and conclusion

Actual local headless Chromium ran the file at **1× and 0.25×** through `ended`, with no media error. The 1× run took 4.18 wall seconds, reported 121 total frames and 6 dropped frames, and one brief waiting/resume event near 3.076 s. The quarter-speed run took 16.15 seconds and reported 3 dropped frames, with no waiting event. These are player telemetry under concurrent work, **not subjective normal-speed viewing or listening**. Every decoded source frame was separately available and inspected, including frames missed by the player. Saved evidence: `ltx13b-bridge-independent/playback-telemetry.json`.

Keep this take as a failed production candidate and successful pipeline/large-motion experiment. A further test should change the hand-control hypothesis (a clearer starting hand and a less extreme intermediate arc), preserve facial geometry, and evaluate articulation against the actual performed line. Do not replace the uncertain articulation with a permanently frozen-open singing mouth. Rerunning the same endpoints/prompt is not evidence that the defects are fixed. Any repaired/composited result needs its own review. No existing edit should adopt this file or its final frame based on this report.

Diagnostics: `ltx13b-bridge-independent/all-frames-01.jpg` through `all-frames-06.jpg`; `hand-01.jpg` through `hand-04.jpg`; `face-microphone-01.jpg` through `face-microphone-03.jpg`; `last-five-face-frames.png`; native selected frames; and structured `verdict.json`. Original reviewed exports remain separate and were not modified.

Precision clarification: ordinary mouth closures are not classified here as audio-sync errors. No song/phoneme comparison has been performed. The earlier rejection remains supported independently by finger/ring defects and final mouth ghosting. No additional render or broad test was run for this clarification.
