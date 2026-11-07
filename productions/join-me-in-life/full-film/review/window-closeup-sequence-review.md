# S003 fixed window insertion — independent sequence review

**PASS / KEEP the exact S003 insertion and its current S002→S003→S004 cuts.** No corrective crop, timing or camera change is needed for these 960×540 proof files. Reviewed 7 November 2026 UTC. This does not approve the full film, later window shots, or the rejected full-width window take.

## Pinned artifacts and frame correspondence

| Artifact | SHA-256 / scope |
| --- | --- |
| [Standalone S003](../exports/Join_Me_in_Life_Window_Closeup_Proof.mp4) | `dd1c70082c7ccd5bcc0f2dd5df147df0aee340e46695cf66a99c8ee322d8a9b6`; 154 frames, 24 fps, master `[307,461)` / 12.791667–19.208333 s |
| [S002–S004 context](../exports/Join_Me_in_Life_Window_Closeup_Context_Proof.mp4) | `3f42a3a6dcda31c121a6263a2883a743d1273d5bf8d6c425f701731552f0c646`; 425 frames, 24 fps, master `[156,581)` / 6.5–24.208333 s |
| Render configuration recorded by both manifests | `e32955750fb6c65dcaf81e4304e5896f8d39b1e9c37ab1d397f69fd4095dcec2` |
| [Frozen source review](ltx23-window-closeup-review.md) | `c4fedc811d96d96911b215af7df6af29ae889c0009c2a9228f6c37b1c06af748`; derivative source `[3,157)` only |
| [Fixed derivative](../assets/motion/ltx23-quiet-window-closeup/video-silent.mp4) | `5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20`; full 672×378 picture |

An independent integer-frame selection `[3,157)` followed only by whole-image Lanczos scaling to 960×540 and the same CRF18 encoder reproduces **all 154 decoded standalone frames exactly**. Those frames also equal context frames `[151,305)` exactly. Thus the editor adds no crop, zoom, replay, reversal, hold or retiming; source cadence is preserved rather than inferred from similar endpoints. All 425 context video timestamps match frame index / 24 within 0.34 microseconds. [Checks and stream details](window-closeup-sequence-review/checks.json), [source versus actual render](window-closeup-sequence-review/source-versus-render.jpg).

## Actual joins and mood

The [first/middle/last sequence](window-closeup-sequence-review/sequence.jpg), [encoded movement phases](window-closeup-sequence-review/encoded-phases.jpg), exact neighboring frames and ordinary-size playback captures were inspected.

- **S002→S003, master frame 307:** the blue, unoccupied bedroom cuts clearly to her downcast hospital close-up. It establishes a separate place and emotional association; it does not pretend to continue one camera view. No stray frame, black flash, added transition or facial pose reset appears at the join. [Native cut pair](window-closeup-sequence-review/cut-151.jpg).
- **Inside S003:** her slow rise/three-quarter turn, lowered gaze, eyelid closures and return remain coherent at 960×540. The neck/shoulder follow the head. I see depleted inward attention, no smile, address to the viewer or sudden recovery. The accepted movement is larger than a single blink; the insertion does not change that source judgment. Faulty reflected eyes/mouth remain excluded. Dim reflected ear/cheek/neck fragments and the original crown boundary remain, without additional loss of the face or neck. Enlargement does not create new native detail.
- **S003→S004, master frame 461:** she has returned toward the lowered pose before the cut back to the empty room. The room's wider restart follows a 6.416667-second cutaway, so it reads as a return to the motif rather than a continuous-camera jump. The cool palette and unresolved mood remain consistent. The small background passersby do not cross this location-changing cut or require a contradictory adjoining hospital position. [Native cut pair](window-closeup-sequence-review/cut-305.jpg).

S002 and S004 are still artwork with camera movement. Passing their cuts does not promote them to completed character animation. This review accepts the inherited tight close-up at the delivered 960×540 size; it does not certify a higher-resolution upscale or removal of every reflection fragment.

## Playback and reproduction

The exact context file actually played once in Chromium 154.0.8037.57 at **1×, 960×540, audio enabled**. It ended at 17.708333 s in 17.8243 wall seconds: 425 total frames, zero dropped/corrupted frames, no playback error or waiting/stalled event. [Playback telemetry](window-closeup-sequence-review/playback-summary.json), [raised-pose capture](window-closeup-sequence-review/playback-8.30.jpg), [settled end capture](window-closeup-sequence-review/playback-12.50.jpg).

This documents browser execution and inspected pictures, not continuous human-equivalent audiovisual perception or subjective listening. The author's manifest reports original-master audio starting at 6.5 s, correlation 0.9999409 and zero measured lag; that waveform test was read, not independently rerun in this review.

Run [reproduce.py](window-closeup-sequence-review/reproduce.py) and [playback_check.py](window-closeup-sequence-review/playback_check.py) from repository root. They preserve the source/exports and write compact evidence here, with raw diagnostics under ignored `build/window-closeup-sequence-review/`. No configuration, source approval, prior source report or provider account was changed.
