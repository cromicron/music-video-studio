# A06 quiet arrival — independent source review

Reviewed 7 November 2026 UTC. **Use the planned source `[3,152)` at natural 24 fps: 149 frames / 6.208333 seconds for S013, master 60.291667–66.500000.** The take supplies a believable apprehensive pause while his hand remains on the closed door's bar. No localized repair or replacement acting is required for this framing. This is a source recommendation, not approval of its eventual insertion, neighboring cuts, audio relationship or added camera treatment.

The main qualification is the acting choice: he holds a strained, narrowed/closed-eye expression for roughly four seconds, dips his head and upper chest, then looks back up worried. It is **not a brief single blink**. I find that sustained inward pause compatible with being frightened for her. It does not communicate confident rescue, reassurance or recovery.

## Exact scope

| Input | Identity / timing |
| --- | --- |
| [Native silent source](../assets/motion/ltx23-quiet-pilots/A06/video-silent.mp4) | SHA-256 `579efce153b4875493dcaf9d122feac73b72a40e0a43278cfbe91dd9233d4b73`; H.264, 896×512, 161 frames, 24/1 fps, 6.708333 s |
| [Original arrival guide](../assets/his_arrival_refined_candidate.png) | SHA-256 `76c2c4b42aa4d6c269f0415671e2f95f15136f52692687f628d71a428a119de0`; 1672×941 |
| Fitted first and last guides | Both SHA-256 `589963ecb670f25551bee1bf9061518f40a6d5794d303d3f3c54ebd087de244a`; identical 896×512 guides |
| Recommended selection | Zero-based frames 3–151 inclusive; source time `[0.125000,6.333333)`; no retiming, reversal, cycle or added hold |

I inspected every decoded frame 0–160 in full-frame sequence sheets, native-pixel face and grip detail, and selected complete 896×512 frames. This includes all three excluded head frames and all nine excluded tail frames. [Portable evidence index](ltx23-quiet-A06-review/README.md), [source/PTS evidence](ltx23-quiet-A06-review/source-evidence.json), and the earlier [static arrival limits](arrival-doorway-refined-review.md) retain the distinctions between the guide, generated take and final edit.

## What the pictures show

| Source frames / time | Observed progression and judgment |
| --- | --- |
| 0–25 / 0.000–1.042 s | Worried upward/sideward attention, tense parted lips, lifted inner brows. The opening is quiet, with small settling and snow movement. Selected f3 enters a coherent existing pose. |
| 26–70 / 1.083–2.917 s | Eyelids narrow asymmetrically; the screen-left eye closes more completely while the other remains a slit. Brow and mouth retain tension. This is a sustained pained squint, not a clean quick blink. |
| 71–95 / 2.958–3.958 s | Head turns down and slightly inward; collar, upper chest and pendant descend with it. Mouth closes into a strained line. The coherent change in facial orientation, silhouette and necklace position is visible movement, not codec noise. |
| 96–121 / 4.000–5.042 s | Lowered head and eyes hold briefly. Neck stays connected to jaw/collar; shoulders remain coherent and the bar grip stays planted. The stillness reads as bracing himself. |
| 122–151 / 5.083–6.292 s | Eyes reopen as head/chest rise, lips part and worried attention returns. The transition is continuous; it does not snap to the opening guide. Selected f151 ends after this return has substantially settled. |
| 152–160 / 6.333–6.667 s | Excluded tail continues settling toward the matched guide. No new reach, door action or end-frame collapse was found. |

The [native beginning](ltx23-quiet-A06-review/native-003.jpg), [moving down-look](ltx23-quiet-A06-review/native-080.jpg), [lowered pose](ltx23-quiet-A06-review/native-096.jpg) and [selected end](ltx23-quiet-A06-review/native-151.jpg) show this at ordinary display size. The torso settlement is compatible with an exhale; these pictures do not independently prove a separate, precisely timed chest-breath cycle. The visible head/eye/body performance itself is sufficient quiet motion.

**Face and identity:** Hair silhouette, facial proportions, light beard/moustache, black layers and pendant remain consistent with the arrival guide and the established character. The down-facing pose naturally changes jaw and brow shape. Fine facial hair and linework become softer in the middle; around f71–82, narrowed eyelids show layered light/dark lines. Those are visible generation/softness limitations, not perfectly clean animation. In the full 896×512 picture they continue to read as narrowed eyes, with no persistent extra eye, replaced face or materially different character. Preserve this framing; an enlarged eye/face insert has not been cleared.

**Grip, rings and support:** All 161 native grip crops keep the same four visible curled fingers connected over the near bar. Rings remain associated with the same upper finger region, although highlights and boundaries soften. The thumb/wrist are partly occluded as in the source guide; five exposed digits are neither present nor required. No finger detaches, passes visibly through the bar, releases and regrips, or initiates a fresh reach. The sleeve/hand relationship remains plausible throughout the torso dip. Feet and lower body are outside this portrait, so planted soles cannot be certified; there is no visible forward travel, stepping cue or unsupported body jump.

**Door, background and headroom:** Uprights and paired handles retain their positions and closed relationship; no opening/pull action or camera travel appears. Moving snow/bokeh and small texture changes do not establish door movement. The crown is already clipped/grazing the fitted guide's upper edge at the opening and return. The downward phase gains headroom naturally. There is no new abrupt crown cut, but this is not a full-head composition. Retain the complete source image in the actual insertion and avoid the former S013 push-in; inspect any containment/padding and both cuts separately.

## Playback and technical evidence

Chromium 154.0.8037.57 actually played the exact source through once at **1×, displayed 896×512**. It reached 6.708333 s in 6.7257 wall seconds and reported 161 total frames, zero dropped/corrupted frames, no playback error and no waiting/stalled event. All 161 source PTS values agree with frame index / 24 within one microsecond. There are 161 distinct decoded frames; uniqueness alone is not acting evidence.

[Playback telemetry](ltx23-quiet-A06-review/playback.json), [during-motion capture](ltx23-quiet-A06-review/playback-3.00.jpg), [late capture](ltx23-quiet-A06-review/playback-6.30.jpg), [frame reproduction script](ltx23-quiet-A06-review/reproduce.py), [browser reproduction script](ltx23-quiet-A06-review/playback_check.py).

This was actual player execution with captured pictures, supplemented by dense visual frame inspection. It is not a claim of human-equivalent continuous audiovisual perception. The source is silent; no subjective listening or music-sync judgment is claimed. No production source, provider, edit configuration or approval manifest was changed.
