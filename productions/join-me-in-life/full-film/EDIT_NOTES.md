# Full-song editorial candidate

The current output is a **full-length animatic**, not a finished animated music video. It covers take 49 with 58 planned shots and restrained camera movement over drawn artwork. No rejected generated source is used. With no approved motion clips available, the output contains **zero seconds of generated character/video action**; a completed runtime does not satisfy the finished-animation goal.

## What is implemented

[edit.json](edit.json) is the editable shot list and source registry. Frame intervals are zero-based and end-exclusive, contiguous from 0 to 6,667 at 24 fps. This makes the picture 277.791667 seconds, approximately 16 ms longer than the source recording's reported 277.776 seconds. Sections follow [the audio planning map](analysis/timing.json), whose uncertain boundaries remain uncertain. The cut has no subtitles or fabricated lip-sync.

The visual progression is: winter hospital and interrupted home → her withdrawn calm → his journey and arrival → shared waiting with a drawn performance-world refrain → warm summer memory → a long hospital night → four distinct bridge plea cuts → exhausted presence at dawn. The people remain inside until the later exterior bench sequence. Morning is a proposed continuation, not a cure or an already accepted ending. All joins are hard cuts; night/morning object images are not match-dissolved.

The preserved reviewed animatic still contains the earlier plain-type band credit. **Renderer 1.2 repairs that regression in new candidates:** the opening uses the unmodified original silver `Band_Logo_Original.png`, with the Revision 4 planar-RGB/screen blend at 0.94 opacity. The logo and the serif song title immediately beneath it share one fade, in at 0.35–0.75 s and out at 4.15–4.80 s. The pair sits over the darker upper façade, clear of the hospital entrance and faces. Independent review of the first candidate found that the upper-left snowy branches reduced logo legibility and that its distant, separately fading song title lost R4's grouping; the second candidate corrects both. Branding is allowed only at full-song frame zero and is not repeated at the Short's 100.373 s offset. There is no black title card. The only picture fade to black is during the final two seconds. No original art, Revision 4 source/export, edit.json or reviewed full animatic is modified.

Seven new storyboard crops are roughly 550 × 306 pixels. The replacement night/morning room pair is approximately 1176 × 660, with the night bed corrected and cup handles on the same side. The 960 × 540 review output upscales the seven smaller panels; any 1920 × 1080 export also upscales the room pair. Neither is wholly native high-resolution new artwork. The existing story and stage plates have higher resolution. Room joins remain hard cuts because the pair still differs slightly in geometry.

## Rebuild

Run from the repository root:

```sh
python3 productions/join-me-in-life/full-film/edit.py
python3 productions/join-me-in-life/full-film/edit.py --render
```

The first command validates all sources and the complete timeline and prints the plan summary. The second now renders a separate full 960 × 540 candidate to `exports/Join_Me_in_Life_Full_Candidate.mp4`, alongside a detailed `.manifest.json`. The renderer refuses to overwrite `exports/Join_Me_in_Life_Full_Animatic.mp4`, even when explicitly requested. It caches individual shots under `work/edit-960x540/`. Each cache record includes source/branding hashes, shot settings and renderer version; a changed source, camera, motion selection or output size rebuilds that shot.

For a short contiguous diagnostic excerpt:

```sh
python3 productions/join-me-in-life/full-film/edit.py --render --shots 1:3 \
  --output productions/join-me-in-life/full-film/work/editor-test/opening.mp4 \
  --work-dir productions/join-me-in-life/full-film/work/editor-test
```

For an HD candidate, use `--width 1920 --height 1080` and a separate `--work-dir`. HD is not a reason to change the animatic label. Existing cached intermediates are reused only when their fingerprints match. `--force` explicitly rebuilds them.

The renderer uses FFmpeg zoompan with deterministic bounded camera paths, eased spacing and an oversampled input. It uses no random deformation, optical-flow interpolation, video reversal, repeated character actions, or artificial slow motion. FFmpeg and ffprobe are the only external executables. Python uses only its standard library to orchestrate commands and validation.

Independent frame review found that the original S014 chorus crop clipped the top of his hair and the original S046 bridge crop removed the extended fingers. The repaired edit limits every chorus-performance reuse (S014/S029/S033) to a top-anchored 1.015 maximum zoom. Both bridge-plea shots now preserve the full gesture; S046's maximum zoom is reduced from 1.23 to 1.045 with a lower framing centre. First/last frames of all five affected shots were rendered and visually compared with the original plates before the cached full export was rerun. This is a framing repair, not evidence of character animation or full audiovisual approval.

The same review identified a camera reset between the two summer-memory shots. S026 now begins at S025's exact final zoom/centre, then moves into its closer composition. The two boundary frames were rendered independently and compared before the final rerender, preserving one continuous memory camera move instead of a same-image jump.

## Audio and checks

The default final audio is AAC at 256 kbit/s, encoded once from the complete original MP3 for conventional MP4/mobile playback. The source is not shortened to a vocal-transcription endpoint. The delivery manifest records the original file hash and a decoded 4 kHz mono waveform correlation/offset comparison. AAC output is not falsely described as identical compressed audio. Validation requires correlation of at least 0.995 and offset no more than 30 ms; the actual measured values are recorded after rendering.

`--audio-copy` is an explicit alternative for MP3 packets inside MP4. That route verifies every compressed packet payload hash and waveform alignment, but its player compatibility must be checked for the target device. It is not the default delivery.

Every rendered shot's encoded frame count is checked. The finished output must have exactly 6,667 frames at 24 fps; FFmpeg then decodes the entire picture and audio. The manifest records dimensions, pixel format, source provenance, output hash and motion coverage. These technical checks do not establish natural movement, correct emotion, song-sync by ear, or normal-speed audiovisual review. Those remain independent review tasks, and the manifest initially marks them unperformed.

The separate [second 6.5-second opening proof](exports/Join_Me_in_Life_Opening_Logo_Candidate_v2.mp4) has the original song's opening audio, 156 frames at 960×540/24 fps and a [candidate manifest](exports/Join_Me_in_Life_Opening_Logo_Candidate_v2.manifest.json). [Sequential frames](review/opening-logo-candidate-v2-contact.jpg) show the shared logo/title fade. Its [technical validation](review/opening-logo-candidate-v2-validation.json) records a waveform correlation of 0.997765 with zero measured offset against the song opening. It is an animatic excerpt for independent branding review, not a new completed film or approved motion. Reproduce it with:

```sh
python3 productions/join-me-in-life/full-film/edit.py --render --shots 1:1 \
  --output productions/join-me-in-life/full-film/exports/Join_Me_in_Life_Opening_Logo_Candidate_v2.mp4 \
  --work-dir productions/join-me-in-life/full-film/work/opening-logo-candidate-v2
```

The [first proof](exports/Join_Me_in_Life_Opening_Logo_Candidate.mp4) and the [independent review of both versions](review/opening-logo-candidate-review.md) remain available for comparison. The second proof's SHA-256 is `d25f20318fe517f15257025b4d464aec967d04d313ad3e8c8ce0cc3141e099a8`. Independent native-frame and fade-boundary inspection passed its branding treatment. [Chromium playback telemetry](review/opening-logo-v2-browser-telemetry.json) completed all 156 frames at 1×, unmuted, with zero dropped frames, media errors or stalls. Telemetry and still-image inspection are not subjective listening or acceptance of generated character motion; this pass covers only the separate opening branding excerpt.

The reviewed animatic remains SHA-256 `d3f66f4feebc401438218345d61889650418a65a5d3f6afb014720c8369550cb`; edit.json remains `f8d78f4b665ac8ccd51b0fd2e8ac41bfbb2e542501cf15c21db779699a45cc30`; original logo remains `44be7217a5624970a97841af3d2e2971a04378300bf796068be055f1c99e602f`.

## Later approved movement

The three-tool production route is ChatGPT image generation → one selected, tested animation system → FFmpeg. LTX-2.5 remains the proposed provider in edit.json; Flow and owned LTX are still being compared. **No generated source enters the picture unless an approved clip is explicitly supplied.** The delivery report uses the provider recorded with reviewed footage rather than assuming every clip came from LTX. The present animatic does not fulfill the completed three-tool music-video request.

The optional `review/approved-motion.json` format is:

```json
{
  "schema": "jml-approved-motion/v1",
  "clips": [
    {
      "id": "her_window_take2",
      "source_key": "her_window",
      "path": "assets/motion/her_window_take2/clip.mp4",
      "in_seconds": 0,
      "duration_seconds": 8,
      "status": "approved",
      "provider": "Actual reviewed model/provider",
      "reviewed_source_sha256": "SHA-256 of the exact reviewed source file",
      "review_note": "Actual timestamped review result belongs here.",
      "shot_ids": ["S021"]
    }
  ]
}
```

Only `status: approved` with a nonblank review note and a matching `reviewed_source_sha256` is eligible. The example is documentation, not an approval; no production approval manifest has been created. Missing approval means a still-camera fallback and an explicit coverage warning. A changed file at the same path invalidates its approval. The selected interval must be finite, positive and within the **video stream's** actual duration, even if the container has longer audio. There is no arbitrary five-second cap: an eight-second source can fill the 154-frame/6.416667-second window slot without stretching or a premature hold. Selections are truncated to the target slot at natural speed. Each clip is used at most once; optional `shot_ids` must name existing shots with the matching source key. It plays forwards, without loops/reversal/retiming, and only repeats its exact final selected frame when an explicitly shorter approved interval needs an endpoint hold. The old `M01_Embrace.mp4` and `M02_Summer.mp4` filename guards remain until independent usable-interval review changes that policy.

Renderer tests under `tests/test_full_film_editor.py` reject missing review notes, changed sources, nonfinite/out-of-picture timings, unknown targets and repeated mid-song titles. A real FFmpeg test checks every decoded frame from a longer source against its reviewed interval, then checks that a shorter interval produces only its exact endpoint hold. That test exposed a redundant `setpts` dropping the cadence metadata used by FFmpeg's padding; the repaired filter keeps 24 fps and pads an explicit number of frames. A second render test checks that logo/title form adjacent visible bands and fade together, including fully absent frames before and after the shared envelope. These integration tests are skipped when FFmpeg/ffprobe are unavailable; other selection checks use only the Python standard library.

The delivery report separates generated-video seconds, endpoint holds and camera-only still seconds. Generated-video duration does not imply that every frame contains character motion. Later approved footage changes the label to a hybrid review candidate, never automatically to a finished film. The final quality decision still requires watching every shot with sound and resolving timestamped defects.
