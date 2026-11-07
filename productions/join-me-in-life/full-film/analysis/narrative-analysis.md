# Full-song audio and story evidence

Prepared 6 November 2026. This is a proposed full-film planning map, not a new creative approval or a frame-accurate singing alignment.

## Raw evidence and method

The source is [take 49](../../full-song/track-49.mp3), stereo 48 kHz MP3, container duration **277.776 seconds**. [timing.json](timing.json) records its SHA-256, 15 continuous planning sections, the 14 existing reviewed Short lyric cues translated by the waveform-derived **+100.373 s** offset, and the four bridge scream estimates.

Two unprompted, CPU-only ASR passes used faster-whisper `base.en` and `small.en`, int8, English, beam size 5, word timestamps, no VAD, and no previous-text conditioning. They cost no API credits. Raw results are [base](asr-base-en.json) and [small](asr-small-en.json). They agree on the broad structure and on repeated post-chorus hooks, but mishear several sung words. They are related models and **are not independent listening judges**. The [final lyric sheet](../../full-song/lyrics.txt) controls wording. ASR output must not replace it.

[analyze_audio.py](analyze_audio.py) measures decoded per-second RMS and spectral flux; [audio-energy.json](audio-energy.json) retains the measurements. The strongest broad autocorrelation candidate is about 117.44 BPM, with a 78.32 BPM alternative. This is not a verified beat grid, so do not quantize every cut to it. Phrase boundaries and the original music are more reliable editing guides here.

No normal-speed listening or audiovisual review was performed by this analysis pass. In particular, the first intro word, sung sustains, scream onsets, and the outro need listening before precise caption or lip-sync placement. An ASR timestamp is insufficient proof.

## Usable sequence map

| Approximate full-song range | Section | Useful visual function |
| --- | --- | --- |
| 0:00–0:33.1 | Piano/heartbeat intro, first vocal hook, instrumental entrance | Establish night, absence and winter; show title once, then a concrete sign that something is wrong. |
| 0:33.1–0:50.5 | Verse 1 | Records, clean cups, made bed, her unnatural calm; his worried observation. |
| 0:50.5–1:06.5 | Pre-Chorus 1 | Increase urgency through a journey/arrival and the image of an old story whose ending can change. |
| 1:06.5–1:23.1 | Chorus 1 | First direct performance plea, intercut with the unsettled hospital world. |
| 1:23.1–1:40.4 | Post-Chorus 1 | Both ASR passes detect hooks near 83 and 91 s. Continue the night without resolving it. |
| 1:40.373–2:06.753 | Verse 2 | Existing Short supplies the strongest timing reference; use withdrawal, then warm summer memory. |
| 2:06.753–2:22.653 | Pre-Chorus 2 | His recognition and the waiting-room passage. Keep his fear directed toward her. |
| 2:22.653–2:39.173 | Chorus 2 | The plea repeats; her state does not instantly improve. |
| About 2:39–2:51.4 | Post-Chorus 2 | Two hook entrances around 159 and 167 s. Existing cue endpoint and ASR overlap slightly; resolve by ear if subtitling. |
| About 2:51.4–3:11.6 | Synth solo | Let visual action develop without lip-sync demands: windows, passing light, memory, empty chairs. |
| About 3:11.6–3:27.9 | Quiet bridge lines | Narrow the visual space and slow the cutting; rehearsed endings/old stories as a motif. |
| About 3:27.9–3:43.5 | Four screamed pleas | Four distinct, escalating actions or cuts; first is already a scream. Approximate starts 207.9, 211.2, 215.9, 219.4 s. |
| About 3:43.5–3:59.7 | Final chorus after key change | A restrained expansion into morning. Proposed visual response must not imply romantic cure. |
| About 3:59.7–4:07.1 | Final hook | Return to presence and shared space. |
| About 4:07.1–4:37.776 | Outro/tail | Preserve the full recording. Both ASR passes mishear the final words and disagree on repetitions; avoid invented subtitles or singing here. |

Boundaries outside the Short are **editorial estimates**, usually within roughly a second but occasionally worse. The first intro hook onset differs by more than two seconds between models. The correct lyric is “It gets light”; ASR's “We can't slide/stop” must never enter the film. The song tail remains audible and should not be discarded just because ASR becomes unreliable.

## Preserved Short anchors

- Summer action source appears at **120.873–125.873 s** on the full-song timeline.
- Existing continuous waiting-room camera passage maps to **130.540–142.456 s**.
- Existing embrace source appears at **134.373–139.373 s**.
- Existing held rounded vowel ends at **114.498 s**. These values preserve the earlier edit; they are not directions to repeat its defects.

## Artwork inspection and coverage gaps

The [inspected contact sheet](art-contact-sheet.jpg) contains the approved reference pair, approved drawn window reference, crisis mood reference, five story plates and four performance plates.

The usable existing story vocabulary is strong but narrow: hospital waiting, her lowered gaze, his frightened attention, one summer memory, and a possible dawn. Stage images cover a verse, wider chorus, screamed plea, and her presence in the performance world. A01/A02 preserve identity and drawing style; A03 supplies mood only. He has light facial hair. Her hospital striped sleeves/blue jeans differ from the summer fitted dark jeans/black tee and stage wardrobe. All backgrounds must remain drawn.

**The missing visual material is concentrated in the first 100 seconds.** There are no matching production plates for records being given away, the cups/bed, his snow journey, or arrival. A cohesive new storyboard sheet can solve these gaps more efficiently than independently generating unrelated shots. The most economical useful additions are object/environment inserts: record sleeves on a table, two untouched cups, a carefully made bed, footprints in snow, a coat crossing a doorway, hospital light reflected in a window. Show enough causal detail that the film tells this song's story, rather than simply reusing the waiting-room view for four minutes.

Most existing plates are flattened illustrations. The character cutouts are not jointed puppets, and the expression sheets are not aligned animation strips. They do not support an unprepared head turn, walk, hand grasp, or body rotation. Parallax or a camera push can be valid shot motion, but must not be described as full character animation.

### Motion that can be made credible

- Animate snow, passing light, curtains, reflections, steam, particles and stage lighting as real spatial layers with steady continuity.
- Use short, deliberate character actions with one clear intention per generated shot. Keep identity/wardrobe reference fixed; preserve a clean first and last pose.
- For held shots, use existing aligned eye or mouth drawings only where their registration and audio timing have been checked. Do not warp an entire cheek, shoulder or torso to suggest acting.
- For complex motion that cannot be generated cleanly, cut on a real editorial motivation to an insert/reaction, or use a different shot. Do not hide a failed action behind optical-flow interpolation.
- Her emotional movement should remain small and effortful. He may hesitate, look, reach once, and remain. Avoid confident savior gestures, her consoling him, or an automatic smile at dawn.
- Do not animate her singing in the performance-world image. The reference explicitly says she does not sing there.

## Source-motion findings

[Embrace sequential frames](embrace-motion-contact.jpg) show a visibly smeared/poorly resolved reaching hand around **1.7–2.1 s** into `M01_Embrace.mp4` (roughly **136.1–136.5 s** in the old full-song mapping). The hand travels above her head before landing around her shoulder. The final pose respects the withdrawn gaze and one embrace, but this source does not earn an unqualified “no weird movement” pass. The old handoff already identifies brief hand blur. Review the sequence at normal speed and replace or avoid the failing portion in a new strict-quality cut; do not mark it repaired merely because it decodes.

[Summer sequential frames](summer-motion-contact.jpg) reveal a second concern: her eye/mouth proportions and facial treatment become much broader and more cartoonlike around 2.3–4.5 s than at the beginning and in A01/A02 (especially 3.28 s). His mouth/face also broadens around 1.7 s. Sampled frames do not show a gross missing limb, but identity/style consistency is not established. Prefer a cleaner, quieter memory action if the new film must meet a strict natural-motion standard. A contact sheet is a diagnostic, not proof of normal-speed facial acting or music sync.

## Proposed story finish and pass criteria

A restrained dawn is the most economical proposed conclusion: the night has passed, the cups can remain untidied, and they are still there. This does not assert that she is cured. Keep a visible connection to help and ordinary life. It is a proposal for the new full film, not an already accepted resolution from the Short.

The film should pass a normal-speed review with the original song, followed by a targeted frame review of every generated action and every source join. Check faces, hands, shoulders, planted feet, gaze, wardrobe and background continuity. Reject identity drift, unsupported head positions, duplicated/fused fingers, sliding feet, and reversals/repetitions that contradict the action. Also verify full audio duration, no dropped/black frames, correct aspect ratio, and complete ending. Report review coverage honestly: technical decode and motion metrics cannot establish aesthetic naturalness by themselves.

## Reproduction and local dependencies

The isolated ASR environment is at repository-root `.venv-jml-asr`, and the public model cache is at `build/asr-model-cache`; both are ignored local setup. No existing Python environment was changed. Invoke the scripts with `.venv-jml-asr/bin/python`. Recreate from `requirements-asr.txt` if this local environment is absent. `transcribe.py` runs the base model, and `transcribe-small.py` runs the small model. Install `faster-whisper` into an isolated virtual environment before invoking either. The scripts decode with FFmpeg into float32 audio because the installed PyAV API rejects faster-whisper's legacy `metadata_errors` keyword. That supported fallback was tested successfully. These dependencies support analysis and are not additional creative production tools.
