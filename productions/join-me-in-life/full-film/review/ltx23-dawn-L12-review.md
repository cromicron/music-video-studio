# L12 outdoor company — independent source review

**REJECT for S053's planned 89-frame interval.** The generated man lifts his hand from his knee, puts his arm behind her shoulders, and withdraws it. That adds a new contact gesture to a scene intended to remain quietly and separately seated. This is observable action, not a stronger version of breathing. No source, edit or approval manifest was changed. Review date: 7 November 2026.

## Exact scope

- [Silent source](../assets/motion/ltx23-dawn-pilots/L12/video-silent.mp4): SHA-256 `c09a05840d6da33970a08e889f148679f9055cd18dff7aed5d67b68ab174e1f8`; 97 frames, 24 fps, 896×512, 4.041667 seconds, no audio stream.
- Identical first/end [outdoor v2 guide](../assets/dawn_together_refined_v2_candidate.png): SHA-256 `452839fce63dfdd7046fdcc07a0bf2af33f7357429042c024a9f0cf11a0b6eb5`; 1672×941, fitted to 896×504 inside the 896×512 canvas. Its prior [static review](dawn-refined-review.md) does not approve generated motion.
- Requested source interval: zero-based **[3,92)**, 89 frames / 3.708333 seconds; intended S053 timeline **[5842,5931)**. This review covers the source, not the later 16:9 editorial crop or neighboring cuts.

## Visible action and continuity

All 97 decoded frames were inspected chronologically, with consecutive native crops around the gesture. The [overview](ltx23-dawn-L12-review/overview.jpg) and [arm phases](ltx23-dawn-L12-review/arm-gesture.jpg) preserve the finding:

| Source frames, zero-based | Observation |
| --- | --- |
| 0–12 | Both hands initially rest over his own knees. His torso/head begin to straighten. |
| 13–18 / 0.542–0.750 s | His screen-left hand visibly leaves the knee and travels across his torso. |
| 19–44 / 0.792–1.833 s | Hand passes her near shoulder, then appears beyond her outer shoulder against the hair/upper-arm outline; his arm runs behind her shoulders. This reads as an arm-around gesture. Some contact is occluded by hair; it is not a fully visible squeeze or full embrace. |
| 45–58 / 1.875–2.417 s | Arm withdraws across his torso. Wrist/finger outlines become soft and doubled during the return, especially 56–58. |
| 59–96 | Hand rests over his knee again. The camera and seated positions remain stable. |

The pair retain broadly recognizable adult faces, hair, clothing and pendants; he retains light facial hair and concerned brows. Her hands remain passive on her lap. Neither stands, steps, changes seat or visibly supports the other's weight. Both crowns remain inside the native frame with margin; the inherited composition omits their feet. The bench, hospital and snow background stay coherent. Real head/torso movement and a brief eyelid close/reopen are present; this is not a still-camera animation.

Her head turns from the original upward/away direction toward the viewer during the middle, then turns back. That is extra acting, but I do **not** read a grin, reassuring role reversal or established recovery from it. The [face phases](ltx23-dawn-L12-review/face-phases.jpg) retain an unresolved expression. [Hand phases](ltx23-dawn-L12-review/hand-phases.jpg) show her thin rings remaining discernible; his moving hand's ring/wristband detail is not stable enough to certify through the gesture. No claim is made about hidden fingers or constant visibility of every ring.

## Playback, interval decision and reproduction

Actual Chromium 154.0.8037.57 playback ran at **1× and native 896×512** for both the whole source and an independently extracted [3,92) proxy. [Full telemetry](ltx23-dawn-L12-review/playback-summary.json): 97 frames, 4.0548 seconds wall time. [Trim telemetry](ltx23-dawn-L12-review/keeper-playback-summary.json): 89 frames, 3.7246 seconds wall time. Both ended normally with zero dropped/corrupt frames and no recorded playback error, waiting or stall. The [1.25-second trim capture](ltx23-dawn-L12-review/keeper-playback-1.25.jpg) also shows the arm around her. This is actual browser execution plus inspected captures/consecutive frames, **not continuous human-equivalent perception or listening**; the source is silent.

No full 89-frame usable interval exists for this instruction: every possible 89-frame window in a 97-frame source starts at frames 0–8 and therefore contains the gesture. The later settled tail cannot supply 89 frames and is not approved for looping, extending or substitution. Rejection concerns the visible new action; it does not reject restrained animation or require an absolutely motionless pose.

[Checks](ltx23-dawn-L12-review/checks.json), [frame evidence script](ltx23-dawn-L12-review/reproduce.py), and [playback script](ltx23-dawn-L12-review/playback_check.py) pin the exact source. From repository root run the frame script, then playback script once normally and once with `--keeper`. Raw native frames and exhaustive sheets go to ignored `build/ltx23-dawn-L12-review/`; compact evidence stays alongside this report. No provider calls or credits were used.
