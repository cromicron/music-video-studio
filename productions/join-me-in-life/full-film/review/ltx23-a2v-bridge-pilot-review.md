# Supplied-song LTX 2.3 bridge — independent editorial review

**Recommend the proposed source interval `[0.125, 3.500)` seconds for visual use as the first distressed plea. Reject the complete 97-frame take unchanged.** The selected interval is frames **4–84 inclusive**, 81 frames / 3.375 seconds, mapping to master **207.875–211.250 seconds**. This is an editorial recommendation, not root/user approval, verified phoneme sync or permission to batch production. No acceptance manifest was changed.

Reviewed silent-video SHA-256: `9a1420423a8be5e0401e172376e41255e723b2274a87748b5d6857d381959fe5`. Native picture is 896×512, 24 fps. Frame numbers below start at 1; source time is `(frame−1)/24`. The [actual prompt and render record](../assets/motion/ltx23-a2v-bridge-pilot/render.json), [source artwork](../assets/bridge_plea_start_candidate.png), A01 identity and [confirmed four-plea direction](../../notes/Music_Video_Anime_Content_v2_Handoff.md#bridge-performance--confirmed-correction-for-the-full-song) were read before judging the take.

## What works in the proposed edit

His brow, wet-looking eyes, tense mouth and forward reach read as frightened pleading. He retains the brown layered hair, blue-gray eyes, light beard/mustache, drawn treatment and stage clothes. The microphone stays in the same supporting hand, its grip and ring remain readable, and the shoulder/elbow/wrist chain stays connected. Stage geometry and the camera remain sufficiently stable. This is actual mouth/jaw and arm movement, with limited drawn-animation cadence, rather than a still with a camera move.

The free hand turns and rises from the abdomen toward/above his head. That exceeds the prompt's small supported gesture and “without lifting over his face” instruction; fingers eventually leave the top of the picture. It nevertheless reads as an urgent reaching plea in this context, without swagger, reassurance or a reversal of the emotional roles. The higher gesture is a prompt deviation, not an anatomy failure by itself.

The weakest passage is the moving palm/finger linework around **f32–46 / 1.292–1.917 s**: grainy/smeared detail, softened finger divisions and diminished metallic ring definition. At native inspection it is plainly imperfect. At the inspected ordinary 672×384 display size, the hand silhouette, direction and wrist connection remain legible, and it resolves into a readable raised palm. I would **not regenerate the entire plea solely for this brief moving-hand softness**. It does not become a persistent extra limb, detached wrist or fused microphone grip. The reduced ring detail is a continuity caveat, not the decisive defect here. [Native rising-hand evidence](ltx23-a2v-bridge-pilot-review/native-sequential-028-036.jpg) · [raised-hand evidence](ltx23-a2v-bridge-pilot-review/native-sequential-037-045.jpg) · [ordinary-size captured hand](ltx23-a2v-bridge-pilot-review/playback-ordinary-1.30.jpg).

An initial impression of a backward hand step in the montage was withdrawn after inspecting standalone frames: f29–31 hold a pose, then f32–34 advance. The [numeric cadence record](ltx23-a2v-bridge-pilot-review/cadence.json) documents the near-held three-frame groups; it does not prove smoothness or classify acting. Do not carry a backward-step claim forward.

## Why the complete take fails, and where to cut

| Source interval | Editorial judgement |
| --- | --- |
| **0.000–3.541667 s**, f1–85 | Maximum contiguous visually usable range in this review, with the moving-hand caveat above. |
| **0.125–3.500 s**, f4–84 | **Recommended proposed S044 trim.** It preserves the first plea and cuts before the faulty settling. Its timing fit is separate from the visual judgement. |
| **3.541667–4.041667 s**, f86–97 | Exclude. The head/body begin settling and the face, hair and hands break into unstable overlapping/noisy detail, clearest at f89–91 / 3.667–3.792 s. The later endpoint is not a reliable hold. |

The terminal breakup is visible at ordinary size, rather than an isolated enlarged finger imperfection. [Late native sequence](ltx23-a2v-bridge-pilot-review/native-sequential-082-090.jpg) · [endpoint sequence](ltx23-a2v-bridge-pilot-review/native-sequential-091-097.jpg) · [ordinary-size damaged f89](ltx23-a2v-bridge-pilot-review/frame-089-ordinary-size.jpg). Mouth closures earlier in the take are coherent expression/articulation changes; they should not be confused with this actual face/hair breakup.

Use the recommended range once at its native cadence, cutting away while the plea remains raised. No slowed version, loop, extended still, alternative crop or transition into the next shot has been reviewed. Do not freeze the final frame of the full take.

## Sound and verification limits

This is an **audio-conditioned visible performance**, not an accepted lip-sync result. Early mouth closures/openings can be ordinary articulation, and the later open mouth can serve a sustained cry. This review has not established their phoneme correspondence, word boundaries or sung-vowel timing. Original soundtrack continuity, model conditioning and a plausible open mouth do not establish those things.

I inspected all 97 frames in native actor/face/hand crops, critical standalone native frames, the full-frame overview, source/final/A01 comparison and eight screenshots captured during ordinary-size playback. Actual local Chromium **154.0.8037.57**, with sandbox enabled, executed unmuted 1× playback at 896×512 and 672×384: both completed all 97 frames with **0 dropped, 0 corrupted and no media errors/stalls**. The exact proposed interval was also encoded as an ignored review proxy from the original silent frames and original conditioning WAV, and checked separately at 1×: **81 decoded/displayed frames, 0 dropped/corrupted, 3.375 seconds**, no media errors/stalls. [Playback measurements](ltx23-a2v-bridge-pilot-review/playback.json). These are execution/captured-frame observations; no subjective listening or continuous human-equivalent viewing is claimed.

Independent decoding verified that the browser MP4's 97 picture frames equal the silent MP4's frames exactly, and the MKV's 194,000 stereo PCM samples equal the conditioning WAV exactly. This establishes preserved audio/picture provenance, not synchronization of lips. [Exact source hashes, native reference dimensions and decode checks](ltx23-a2v-bridge-pilot-review/source-checks.json) · [machine-readable editorial findings](ltx23-a2v-bridge-pilot-review/editorial-findings.json).

## Reproduce

From the repository root, with Python/Pillow, FFmpeg/ffprobe, Playwright Python and `/usr/bin/chromium` available:

```sh
python productions/join-me-in-life/full-film/review/ltx23-a2v-bridge-pilot-review/reproduce_frames.py
python productions/join-me-in-life/full-film/review/ltx23-a2v-bridge-pilot-review/playback_check.py
```

Outputs go to ignored `build/ltx23-a2v-bridge-pilot-review/`. The retained JPEGs are selected portable evidence; the first script reconstructs every native sequential sheet and raw frame. No provider call, source edit, generated-audio substitution or production approval is involved.
