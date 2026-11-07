# Original M01 — independent animation-editor review

Reviewed 2026-11-07. **Recommendation: reuse the original five-second action at 24 fps at ordinary music-video size.** The source does not require new acting or a mandatory localized repair. Its brief moving-hand softness is real, but does not overturn the single reach → shoulder contact → inward settling → held aftermath. This judgment comes from the original pictures, not the Short's publication or earlier review verdicts.

[Original source](../../current/assets/M01_Embrace.mp4): 1916×1080, 121 frames at 24 fps, 5.041667 s, no audio stream. Source frame numbers below start at 1; time is `(frame−1)/24`. The R4 action occupies 34.000–39.000 s, with the final source image continuing as the endpoint still.

| Source interval | Visible evidence and editorial judgment |
| --- | --- |
| f1–24, 0.000–0.958 s | He watches her with worried brows and a slightly open mouth; she remains down and away. The quiet preparation reads as hesitation/concern, not a confident rescue. |
| f25–42, 1.000–1.708 s | His elbow lifts and forearm follows one continuous high arc. The arc is broad, but clears her head rather than striking or supporting it. There is no stop at the crown, head pat or second reach. |
| f43–54, 1.750–2.208 s | The moving hand is soft, most conspicuously around f45–52 (1.833–2.125 s). Finger contours are simplified/unstable as the wrist turns and the forearm passes behind hair. This is a localized generated-detail limitation; at the inspected 960-pixel-wide display it reads as a passing blurred hand, not a persistent extra limb or broken contact. Occlusion does not require every finger to remain exposed. Do not turn this interval into a slow-motion hand close-up. |
| f55–66, 2.250–2.708 s | Fingers curl around her outer shoulder/upper arm; the thumb and wrapping fingers become readable as motion slows. The hand remains connected to his arm, settles with the shoulder, and does not float independently. His torso follows the reach. |
| f67–92, 2.750–3.792 s | He closes the distance while the shoulder hold remains continuous. Her upper body yields without a return embrace: hands remain together in her lap, eyes stay down/away, and her neck continues to support her head. The changing pose reads as one settling action, not another pull/reset. The seated framing does not expose feet or establish a full-body biomechanical test. |
| f93–121, 3.833–5.000 s | Stable closeness and a concerned downward gaze; no smile, recovery beat or reciprocal comforting gesture. This is a usable unresolved aftermath. |

The start/end PNGs are **exact RGB matches** to decoded source f1/f121. I also inspected encoded R4 f816–818, f876–878 and f936–938, spanning 34.000, 36.500 and 39.000 s: no pose reset, contact break or source jump is visible. Preserve the continuous source timing and matched endpoint. This review does not approve an arbitrary longer freeze, a different full-film crop, a new soundtrack join, or later shots that reset the embrace.

Evidence: [source overview](m01-editor-second-review/overview.jpg), [reach/contact detail](m01-editor-second-review/reach-contact-detail.jpg), [matched endpoints](m01-editor-second-review/endpoints.jpg), [actual R4 join frames](m01-editor-second-review/r4-joins.jpg). Eleven sequential sheets in the same durable folder cover every source frame; all were inspected, along with captured playback frames at normal display size. The portable [frame reproduction script](m01-editor-second-review/reproduce_frames.py) and [playback check](m01-editor-second-review/playback_check.py) write fresh results under ignored `build/m01-editor-second-review-reproduced/`, leaving the recorded evidence intact. No duplicate video or raw-frame cache is retained here.

Playback was actually exercised in Chromium 154.0.8037.57 at `playbackRate=1`. The original at 960×541 CSS pixels completed all 121 frames in 5.055 s, with zero reported dropped/corrupted frames, errors or waiting events. A secondary 480-wide run dropped 23 frames and had two waits; the 11.916667 s R4 context proxy completed but dropped 17 frames. Those secondary runs are **not evidence of uninterrupted timing**. [Raw player telemetry and sampled frame times](m01-editor-second-review/playback.json) are distinct from the visual judgment above. Available tools provided still images and browser execution; I do not claim human-equivalent continuous audiovisual perception or subjective listening. The original is silent; the context proxy's soundtrack was enabled but not listened to subjectively.

| Input | SHA-256 |
| --- | --- |
| M01_Embrace.mp4 | `bb6e21e887c5b86d815c1b2638896f2b2612471238d3dd2ee798b586418d5246` |
| M01_Embrace_Start.png | `259124c27ba71ae4785927457fda743f20a954e38b86ce19ce655866e408b64f` |
| M01_Embrace_End.png | `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10` |

No source, edit configuration or previous review was changed; no generation provider was called. This is a scoped editorial recommendation, not Dario's creative sign-off or a finished-film motion pass.
