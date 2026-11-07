# A07 dawn final-presence source review — 7 November 2026

**Reject the planned full-length S058 selection `[3,161)`.** The couple's early movement is coherent and emotionally suitable. A newly generated foreground passerby then dominates the image, obscuring the people whose continued presence should carry the ending. This is an editorial staging failure; it is not evidence that the seated protagonists' bodies collapse.

| Range, zero-based and end exclusive | Source time | Judgment |
| --- | --- | --- |
| Planned S058 `[3,161)`, 158 frames | 0.125000–6.708333 s | Reject for the final 6.583333-second slot, master 271.208333–277.791667 s. |
| Conservative shorter candidate `[3,87)`, 84 frames | 0.125000–3.625000 s | Useful early quiet head-lowering performance; insufficient to fill S058. This is not a claim that these are the maximal clean boundaries. |
| Complete source `[0,169)` | 0.000000–7.041667 s | No unobstructed contiguous 158-frame ending can be selected from this take. |

The source is silent and unfaded. No timeline, source or approval manifest was changed. The actual edit, neighbouring cut and editor's final fade have not been reviewed here.

## Acting and the blocking change

She closes her eyes and slowly lowers her head between roughly 1.2 and 2.3 seconds, then remains tired and withdrawn. He makes small eyelid/head changes and stays concerned beside her. Her hands remain passive in her lap; his hands rest over his own knees. Both pelvises remain supported by the bench, and their heads remain supported by their own necks. No new embrace, touch, step or seating change occurs in the visible portions. Feet are outside the frame, so ground contact is not independently verified.

This head lowering is larger than the requested tiny gaze adjustment, but it is an acceptable expression of exhaustion. It does not read as a sudden collapse, recovery or reversal of who needs support. The early performance is more than a different file or a static picture. Hair, shoulders and eyelids change modestly; a precise, naturally uneven breathing rhythm is not clearly established at ordinary size. No grotesque chest inflation appears.

A foreground figure begins entering at approximately one-based f90/3.708 seconds, clearly intruding by f91/3.750 seconds. The crossing continues until approximately f152/6.292 seconds; f153/6.333 seconds is clear again. It partly or almost completely hides the couple, especially around 4.5–5.2 seconds. See [crossing phases](ltx23-dawn-A07-review/crossing-phases.jpg) and [actual S058 playback captures](ltx23-dawn-A07-review/captured-S058-2.jpg).

The crossing reads as a person passing close to the camera: its large scale and occlusion are not, by themselves, impossible anatomy. Nevertheless, the broad trousers and swinging hand become the dominant final-shot subject for about 2.6 seconds. We lose sustained access to the faces and cannot verify hidden body/hand details. This interrupts the ending's quiet focus rather than developing their relationship. The planned editor-only fade starts at source frame 113/4.708333 seconds while the obstruction is already underway; a future fade cannot establish that the source is suitable. Only nine selected frames remain after the foreground completely clears. No fade was rendered as part of this review.

She raises her head and reopens her eyes toward the original distant, away-looking pose near the end. That is a return toward the identical endpoint guide, rather than the requested lasting downward gaze. It remains serious, without a reassuring smile or gaze cure. It is not the principal rejection reason. Visible character movement persists into the selected tail; no source fade, black transition or terminal anatomical breakup appears.

Against the corrected dawn guide and A01 identity reference, the adult faces, auburn hair, his facial hair, clothes and pendants remain recognizable. Native [face phases](ltx23-dawn-A07-review/face-phases.jpg) and [hand phases](ltx23-dawn-A07-review/hand-phases.jpg) show stable ownership and seated support when visible. Fine ring/finger outlines and freckles soften or vary; exact accessory invariance is not established. There is no gross identity substitution or detached hand in the unobstructed passages. Minor background/framing drift is not the decisive problem.

## Verification and limits

Reviewed MP4 SHA-256: `1eb004c3e7306da55b479af550481c0fbbb7cf269913e9db16e2ccdc3fc90582`. All 169 native frames at 896×512/24 fps were inspected chronologically, plus native face/hand crops, source/guide/endpoints and captured ordinary-size playback phases. Error-failing full decode and every frame timestamp passed; there is no audio stream.

Actual sandboxed Chromium 154.0.8037.57 played the complete take and an exact review-only S058 trim at 1×, 672×384, without seeking. The raw take delivered 169 frames/7.041667 seconds in 7.0586 wall seconds; the trim delivered 158 frames/6.583333 seconds in 6.6005 wall seconds. Both completed with zero dropped/corrupt frames and no playback error, stall or wait. [Playback telemetry](ltx23-dawn-A07-review/playback.json) records callback times and screenshot capture bounds. I inspected these captured phases and the sequential native frames; this is not human continuous perception or subjective listening. No supplied audio or phoneme-sync claim applies.

[Checks](ltx23-dawn-A07-review/checks.json) verify the corrected outdoor dawn v2 source SHA-256 `452839fce63dfdd7046fdcc07a0bf2af33f7357429042c024a9f0cf11a0b6eb5`, native 1672×941, identical fitted first/last guide pixels, and matching guide records at both stages. [Guide/endpoints](ltx23-dawn-A07-review/guide-endpoints.jpg) are visually compared. Those facts establish provenance, not preservation of the middle action.

[Reproduction script](ltx23-dawn-A07-review/reproduce.py): run with Python, NumPy, Pillow, FFmpeg, Playwright and `/usr/bin/chromium`. It writes raw frames, review proxy and playback evidence under ignored `build/ltx23-dawn-A07-review/`, with no provider calls. The portable folder retains compact JPEG/JSON evidence. Any shorter reassignment needs a separate exact-range review and actual insertion review; no stretching, looping or replay is recommended to fill this ending.
