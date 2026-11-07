# Full-song editorial candidate

The current output is a **full-length animatic**, not a finished animated music video. It covers take 49 with 58 planned shots and restrained camera movement over drawn artwork. No rejected generated source is used. With no approved motion clips available, the output contains **zero seconds of generated character/video action**; a completed runtime does not satisfy the finished-animation goal.

## What is implemented

[edit.json](edit.json) is the editable shot list and source registry. Frame intervals are zero-based and end-exclusive, contiguous from 0 to 6,667 at 24 fps. This makes the picture 277.791667 seconds, approximately 16 ms longer than the source recording's reported 277.776 seconds. Sections follow [the audio planning map](analysis/timing.json), whose uncertain boundaries remain uncertain. The cut has no subtitles or fabricated lip-sync.

The visual progression is: winter hospital and interrupted home → her withdrawn calm → his journey and arrival → shared waiting with a drawn performance-world refrain → warm summer memory → a long hospital night → four distinct bridge plea cuts → exhausted presence at dawn. The people remain inside until the later exterior bench sequence. Morning is a proposed continuation, not a cure or an already accepted ending. All joins are hard cuts; night/morning object images are not match-dissolved.

The opening title fades over the picture from 0.7 to 5.2 seconds. It uses plain typography and does not invent or imitate the band's original silver wordmark. There is no black title card. The only picture fade to black is during the final two seconds. No original Revision 4 source or export is modified.

Seven new storyboard crops are roughly 550 × 306 pixels. The replacement night/morning room pair is approximately 1176 × 660, with the night bed corrected and cup handles on the same side. The 960 × 540 review output upscales the seven smaller panels; any 1920 × 1080 export also upscales the room pair. Neither is wholly native high-resolution new artwork. The existing story and stage plates have higher resolution. Room joins remain hard cuts because the pair still differs slightly in geometry.

## Rebuild

Run from the repository root:

```sh
python3 productions/join-me-in-life/full-film/edit.py
python3 productions/join-me-in-life/full-film/edit.py --render
```

The first command validates all sources and the complete timeline and prints the plan summary. The second renders the full 960 × 540 review output to `exports/Join_Me_in_Life_Full_Animatic.mp4`, alongside a detailed `.manifest.json`. It caches individual shots under `work/edit-960x540/`. Each cache record includes the source hash, shot settings and renderer version; a changed source, camera, motion selection or output size rebuilds that shot.

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

## Later approved movement

The intended three-tool production route is ChatGPT image generation → LTX-2.5 → FFmpeg. LTX was tested during this task but **does not appear in the animatic's final picture unless an approved clip is explicitly supplied**. Thus the present animatic does not fulfill the completed three-tool music-video request.

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
      "duration_seconds": 4,
      "status": "approved",
      "review_note": "Actual timestamped review result belongs here.",
      "shot_ids": ["S021"]
    }
  ]
}
```

Only `status: approved` with a review note is eligible. Missing approval means a still-camera fallback and an explicit coverage warning. A clip must be no longer than five selected seconds and within the actual source duration. Each clip is used at most once; optional `shot_ids` controls where. It plays forwards at natural speed, with a held exact endpoint if the editorial shot is longer. The old `M01_Embrace.mp4` and `M02_Summer.mp4` sources are explicitly prohibited.

The delivery report separates generated-video seconds, endpoint holds and camera-only still seconds. Generated-video duration does not imply that every frame contains character motion. Later approved footage changes the label to a hybrid review candidate, never automatically to a finished film. The final quality decision still requires watching every shot with sound and resolving timestamped defects.
