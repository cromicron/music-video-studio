# L13 outdoor later company — independent source review

Reviewed 7 November 2026 UTC. **Reject the planned S056 selection `[3,149)`; recommend only the earlier source interval `[3,69)` for separate editorial consideration.** The full selection contains a standing man and a second seated copy of him simultaneously. This is a real body/identity and story-continuity failure, not merely a different interpretation of quiet acting. No edit or approval manifest was changed.

Source: [L13 silent video](../assets/motion/ltx23-dawn-pilots/L13/video-silent.mp4), SHA-256 `eebdffb903eb5808313ef7e6bbbac42c337d8ea01e1c666bcde6ddbd23b93400`. Verified 153 frames, 24 fps, 896×512, 6.375 seconds, one video stream and no audio. Both endpoint guides were the corrected outdoor dawn v2 source; its [static review](dawn-refined-review.md) remains a separate, limited approval.

All intervals below are zero-based and half-open. Contact-sheet labels are one-based: f001 is source time 0.

| Scope | Source frames / seconds | Finding |
| --- | --- | --- |
| Intended S056 | `[3,149)`, `[0.125,6.208333)`; 146 frames / 6.083333 s | Reject; the failure is inside the intended trim. Planned timeline `[6226,6372)` remains unfilled by this full take. |
| Conservative usable candidate | `[3,69)`, `[0.125,2.875)`; f004–f069 inclusive; 66 frames / 2.75 s | Coherent seated, unresolved company. Source-only recommendation; placement and seams require separate review. |
| Remaining planned duration | 80 frames / 3.333333 s | Not supplied by the usable prefix. No freeze, loop, retiming or late reset is approved. |

## What the motion actually does

In the prefix she begins with the source's away/slightly upward gaze, then slowly closes her eyes and lowers her chin and shoulders. This is genuine continuous settling compatible with an exhale; no audible breath is claimed. Her mouth stays closed, without a smile or engagement with the viewer. He maintains worried attention with small facial/head adjustments. The longer eye closure is not a quick blink, and a complete male blink is not certified in this retained section. Those differences from the prompt are not themselves story failures. Her downturned settling remains depleted rather than recovered.

Her hands remain passive together on her lap, with traceable forearms and supported wrists; his hands remain over his own knees. Visible silver bands and the studded wristband stay attached and recognizable without a conspicuous pop, release or new gesture. The overlapped digits cannot all be counted independently. Heads, necks, shoulders, torsos and seated hips remain connected and plausibly supported. Adult facial structure, copper hair, light beard/moustache, pendants and black/purple clothes remain stable in this early section. Native wide-shot eyes/freckles have limited detail: there is no obvious new eye-color/face-identity change, but this is not a close-up certification of individual iris or freckle pixels. Feet remain outside the source framing. The bench, hospital windows, snow, trees and lamp remain coherent, with sufficient crown/hand margin.

By f073–084 he begins a larger head/torso change. Around f085–101 (3.5–4.167 s) he leans forward and stands into the foreground; his hair/face drawing also becomes unstable through that transition. Around f103–109 a translucent seated version reappears behind him. By f109–137 the shot plainly contains both the foreground moving body and the seated copy. The foreground body continues toward the right edge, with remnants through approximately f148, while the seated pose reconstitutes. [Failure phases](ltx23-dawn-L13-review/failure-phases.jpg) and the [actual ordinary-size playback capture](ltx23-dawn-L13-review/selected-playback-4.40.jpg) show the simultaneous bodies. Matching the final guide does not repair this impossible transition.

The conservative f069 endpoint precedes the larger head/lean preparation, rather than cutting on its first conspicuous stand frame. See [retained face phases](ltx23-dawn-L13-review/seated-face-phases.jpg) and [retained hands](ltx23-dawn-L13-review/seated-hand-phases.jpg). No late fragment is recommended: the short return follows a visible duplicate/reset and does not supply the missing continuous company.

## Inspection and reproducibility

The exact source hash and stream shape passed a full error-checked decode. All 153 frames were extracted without interpolation and inspected in sequence: full-frame sheets at 448×256 per frame plus native-resolution face and hand crops for every frame. Boundary phases and ordinary-size playback captures were also inspected. Raw native PNGs, all contact sheets, playback proxies and full logs stay in ignored root `build/ltx23-dawn-L13-review/`; compact evidence and reproducible scripts are retained here.

Actual local Chromium `154.0.8037.57` playback ran at `playbackRate=1`: full source at native 896×512 and ordinary 672×384, exact selected interval twice, and exact proposed prefix twice. All six runs ended at the expected 153/146/66 frame durations with **zero dropped or corrupt frames, playback errors, stalls or waiting events**. Full-run wall times were 6.402/6.391 s, selected 6.112/6.108 s, prefix 2.762/2.764 s. The captured runs bracket screenshot times explicitly. This is evidence of real 1× execution plus sequential visual inspection, **not a claim of continuous subjective human viewing**. The source is silent; no listening or lip-sync judgment applies.

Reproduce from the repository root:

```bash
python3 productions/join-me-in-life/full-film/review/ltx23-dawn-L13-review/reproduce_evidence.py
python3 productions/join-me-in-life/full-film/review/ltx23-dawn-L13-review/playback_check.py
python3 productions/join-me-in-life/full-film/review/ltx23-dawn-L13-review/playback_check.py --selected
python3 productions/join-me-in-life/full-film/review/ltx23-dawn-L13-review/playback_check.py --prefix
```

Exact intervals, limits and evidence hashes are in [verdict.json](ltx23-dawn-L13-review/verdict.json); measured playback details are in [playback-summary.json](ltx23-dawn-L13-review/playback-summary.json). This report reviews the source only. Proposed dawn narrative, final-resolution rendering, editorial placement and seam continuity remain separate decisions.
