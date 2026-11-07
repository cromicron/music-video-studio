# Full-song editorial candidate

The preserved full-song output is a **full-length animatic**, not a finished animated music video. It covers take 49 with 58 planned shots and restrained camera movement over drawn artwork, with **zero seconds of generated character/video action**. A separate production candidate now selects the independently re-reviewed original M01 action for scoped reuse; its specific S028 sequence now has a scoped independent visual pass, while musical listening and the full-film join remain separate. Neither a completed runtime nor this source reuse alone satisfies the finished-animation goal.

## What is implemented

[edit.json](edit.json) is the editable shot list and source registry. Frame intervals are zero-based and end-exclusive, contiguous from 0 to 6,667 at 24 fps. This makes the picture 277.791667 seconds, approximately 16 ms longer than the source recording's reported 277.776 seconds. Sections follow [the audio planning map](analysis/timing.json), whose uncertain boundaries remain uncertain. The cut has no subtitles or fabricated lip-sync.

The visual progression is: winter hospital and interrupted home → her withdrawn calm → his journey and arrival → shared waiting with a drawn performance-world refrain → warm summer memory → a long hospital night → four distinct bridge plea cuts → exhausted presence at dawn. The people remain inside until the later exterior bench sequence. Morning is a proposed continuation, not a cure or an already accepted ending. All joins are hard cuts; night/morning object images are not match-dissolved.

The preserved reviewed animatic still contains the earlier plain-type band credit. **Renderer 1.2 repairs that regression in new candidates:** the opening uses the unmodified original silver `Band_Logo_Original.png`, with the Revision 4 planar-RGB/screen blend at 0.94 opacity. The logo and the serif song title immediately beneath it share one fade, in at 0.35–0.75 s and out at 4.15–4.80 s. The pair sits over the darker upper façade, clear of the hospital entrance and faces. Independent review of the first candidate found that the upper-left snowy branches reduced logo legibility and that its distant, separately fading song title lost R4's grouping; the second candidate corrects both. Branding is allowed only at full-song frame zero and is not repeated at the Short's 100.373 s offset. There is no black title card. The only picture fade to black is during the final two seconds. No original art, Revision 4 source/export, edit.json or reviewed full animatic is modified.

Seven new storyboard crops are roughly 550 × 306 pixels. The replacement night/morning room pair is approximately 1176 × 660, with the night bed corrected and cup handles on the same side. The 960 × 540 review output upscales the seven smaller panels; any 1920 × 1080 export also upscales the room pair. Neither is wholly native high-resolution new artwork. The existing story and stage plates have higher resolution. Room joins remain hard cuts because the pair still differs slightly in geometry.

Those dimensions describe the preserved baseline configuration. The separate [art candidate](edit-art-candidate.json) replaces all seven small panels with reviewed 1672×941 redraws across23shots, with11portrait uses held wide to protect framing. Its [opening proof](exports/Join_Me_in_Life_Opening_Refined_Animatic_Proof.mp4) includes the original wordmark/audio. These remain still-art candidates; the dawn's omitted finger rings remain a recorded continuity caveat. Renderer1.3 records actual source dimensions per shot instead of carrying the old dimensions into every candidate.

## Rebuild

Run from the repository root:

```sh
python3 productions/join-me-in-life/full-film/edit.py
python3 productions/join-me-in-life/full-film/edit.py --render
```

The first command validates all sources and the complete timeline and prints the plan summary. The second now renders a separate full 960 × 540 candidate to `exports/Join_Me_in_Life_Full_Candidate.mp4`, alongside a detailed `.manifest.json`. The renderer refuses to overwrite `exports/Join_Me_in_Life_Full_Animatic.mp4`, even when explicitly requested. It caches individual shots under `work/edit-960x540/`. Each cache record includes source/branding hashes, shot settings and renderer version; a changed source, camera, motion selection or output size rebuilds that shot.

Renderer1.3 accepts a named configuration without replacing `edit.json` and records that configuration's SHA-256 in the export manifest. Source paths still resolve from the full-film root. For example, validate the refined-art candidate:

```sh
python3 productions/join-me-in-life/full-film/edit.py \
  --edit productions/join-me-in-life/full-film/edit-art-candidate.json
```

Add `--render` and an appropriate separate `--output`/`--work-dir` to export it. A named configuration does not bypass motion review or the protected baseline export.

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

The three-tool production route is ChatGPT image generation → one selected, tested animation system → FFmpeg. The baseline edit.json retains its earlier LTX-2.5 proposal; live owned-LTX tests and the stopped Flow route are recorded in production STATUS. **No generated source enters the picture unless an approved clip is explicitly supplied.** The delivery report uses the provider recorded with reviewed footage rather than assuming every clip came from LTX. The present animatic does not fulfill the completed three-tool music-video request.

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

Only `status: approved` with a nonblank review note and a matching `reviewed_source_sha256` is eligible. The example is documentation, not an approval. The original/default approval path remains absent; the separate production candidate alone points to [approved-motion-production.json](review/approved-motion-production.json). Missing approval means a still-camera fallback and an explicit coverage warning. A changed file at the same path invalidates its approval. The selected interval must be finite, positive and within the **video stream's** actual duration, even if the container has longer audio. There is no arbitrary five-second cap: an eight-second source can fill the 154-frame/6.416667-second window slot without stretching or a premature hold. Selections are truncated to the target slot after any explicit lead-in, at natural speed. Each clip is used at most once; optional `shot_ids` must name existing shots with the matching source key. It plays forwards, without loops/reversal/retiming. Optional nonnegative integer `lead_in_frames` defaults to zero and holds the exact first selected frame; any remaining time holds the exact last selected frame. Both kinds of hold are separately reported.

## Original M01 reuse in the production candidate

[The independent second source review](review/m01-editor-second-review.md) recommends reusing all **121 original M01 frames at 24 fps and ordinary music-video scale**, with the brief moving-hand softness recorded rather than making a new repair mandatory. This supersedes the previous blanket source rejection only for the exact reviewed source and permitted use. It does not approve a new longer hold, a different crop, the soundtrack join or the entire full-film sequence.

Renderer **1.4** retains the default filename guards for `M01_Embrace.mp4` and `M02_Summer.mp4`. A guarded source is allowed only through explicit `usage: reused_existing_video`, approved status, a nonblank note, its matching exact source SHA-256, and `superseding_review: {path, sha256}`. The review must be an existing file with that exact hash and must identify the source hash in its text. An altered/missing review or altered source invalidates the exception. No blanket ban removal or renamed-file workaround is used; M02 has no approval in the production manifest.

The [production configuration](edit-production-candidate.json) maps S028 to the original start still and the scoped M01 source approval. Its new candidate sequence is:

| Shot-local frames, zero-based and end-exclusive | Content | Full-song placement |
| --- | --- | --- |
| 0–92 | 92 copies of exact source f0 | Begins at frame 3133 / 130.541667 s |
| 92–213 | All 121 source frames f0–f120, once at natural 24 fps | Source f0 at frame 3225 / 134.375 s |
| 213–291 | 78 copies of exact source f120 | Ends at frame 3424 / 142.666667 s |

Total: **291 frames / 12.125 seconds**. The first source frame is naturally also the first frame of its own playback; the added lead-in is counted separately. The final source frame similarly joins its own held endpoint without another action. The source start is 2 ms later than the R4-derived 134.373-second position because the full edit uses the 24 fps frame grid. There is no reverse, loop, speed change, concealment cut or new endpoint camera push. The four later hospital returns continue to use the preserved embraced endpoint, rather than separated poses.

The new **S028 composite is still a candidate** even though source reuse has passed independent review. Its 3.833333-second lead-in and 3.25-second endpoint hold, the soundtrack join and ordinary-size framing need outside sequence inspection. The earlier aftermath-preparation report describes the state before this scoped source reuse; its formerly missing action is now selected, not silently marked as newly generated or as final creative acceptance.

Historical source provider remains **Runway**. Reusing this supplied file makes no Runway call and creates no new LTX footage. The manifest distinguishes `reused_existing_video_seconds` from `new_generated_video_seconds` (also exposed as the compatible `generated_video_seconds` field), `lead_in_hold_seconds`, `endpoint_hold_seconds` and camera-only still time. It lists historical reused-source providers separately from tools used for new production work. ChatGPT → Owned LTX animation → FFmpeg remains the planned three-tool route, not a claim that all three have contributed approved new picture.

Render the independent diagnostic, leaving the original/art configurations and reviewed full export unchanged:

```sh
python3 productions/join-me-in-life/full-film/edit.py \
  --edit productions/join-me-in-life/full-film/edit-production-candidate.json \
  --render --shots 28:28 --width 960 --height 540 --crf 18 \
  --output productions/join-me-in-life/full-film/exports/Join_Me_in_Life_S028_Original_Reuse_Candidate.mp4 \
  --work-dir productions/join-me-in-life/full-film/build/m01-reuse-candidate/render
```

The renderer checks all 291 frames, codec/decode, and the AAC excerpt against the corresponding original-song offset; excerpt waveform checks now use the selected full-song start rather than incorrectly comparing against song zero. Audio correlation is technical alignment, not subjective listening. The diagnostic's output/config hashes and measured values are in its adjacent delivery manifest.

Renderer tests under `tests/test_full_film_editor.py` reject missing review notes, changed sources/reviews, nonfinite/out-of-picture timings, invalid/excessive lead-ins, unknown targets and repeated mid-song titles. A real FFmpeg test checks every decoded frame from a longer source against its reviewed interval, then checks that a shorter interval produces only its exact endpoint hold. Another uses 121 individually changing frames and verifies the complete **92 + 121 + 78** decoded sequence byte for byte, catching dropped, repeated, reversed or retimed action frames and off-by-one hold boundaries. Guard tests require an actual review file/hash naming the exact test source; accounting tests keep historical Runway reuse out of new-generation/tool counts. The original tests for the compact logo/title lockup and shared fade remain. These integration tests are skipped when FFmpeg/ffprobe are unavailable; other selection checks use only the Python standard library.

The delivery report separates new-generated video, reused existing video, first-frame holds, endpoint holds and camera-only still seconds. Video duration does not imply that every frame contains character motion. Selected approved-source footage changes the label to a hybrid review candidate, never automatically to a finished film. The final quality decision still requires watching every shot with sound and resolving material timestamped defects.

## Renderer1.5: preserve supplied Short performance knowledge

The selected production candidate now applies the bounded [action coverage plan](review/action-coverage-plan.md). The original/default and art-only configs are unchanged. [The exact before/after diff](review/production-continuity-diff.json) records source changes, four restored boundaries and every changed shot. Picture remains58shots/6667frames with take49 intact. Held-contact replacements prevent post-embrace geographic resets. One shared camera curve now continues across S007–8 and S050–51 instead of restarting/reversing.

The candidate's `historical_drawn_art` registry hashes the existing P01/P02 mouth variants, S02 blink image, original timing/code and measured song origin. The renderer reads only the literal mouth patterns and timing data, then composites localized feathered patches with FFmpeg. No Blender process, new model generation, whole-face morph or portrait-export stretch is involved. Mouth sequences stay inside the matched Short span; unchanged source hashes and matching source plates are mandatory. Missing/mutated art or code, segment gaps/overlap, and simultaneous motion-plus-drawn selection are rejected. The independent video approval requirements remain in force.

The exact original rounded vowel persists through full frame2747; S024 begins2748 before a closing exposure can appear. S029 includes the original P02→P01 cut at3495. The supplied drawings count as `reused_drawn_exposure_sequence_seconds` and are removed from the still-only total; this is sequence duration, not a claim of constant body motion or phoneme-complete singing. New LTX, historical video, drawn exposures, lead/end holds and still-camera frames remain separately reported.

[Separate original-audio proofs and implementation checks](review/r4-drawing-reuse-review.md) cover S021–24, S027–29, the reviewed first-scream source inserted atS044, and the original male summer derivative atS025. Original-audio correlation/frame checks pass. Seventeen editor tests pass, including all1440 exposure frames against the original function, the protected vowel cutoff, real FFmpeg regional isolation/exact-frame activation and earlier review/motion/branding guards. Studio structure and original-source checks also pass. Actual-song listening and outside sequence acceptance are not inferred from these checks.

Only the production candidate promotes `dawn_together_refined_v2_candidate.png`; it preserves the corrected continuous band rings as a static-source eligibility improvement. S025 uses63lead frames plus48frames of the independently reviewed male-only original M02 derivative. S026 remains the explicitly unfinished female-response slot. S044 uses81natural24fps frames from approved A2V source[0.125,3.5), with no endpoint freeze. The broader109.708s remaining new-action/quiet-motion target is not completed by the exposure recovery.

Outside review then identified a tight S023 crown crop in the first exposure proof. The production candidate now uses1.015→1.035zoom atcentre(.5,.49), retaining all exposure frames and the2748reaction cut. A separately named v2proof preserves the v1evidence. This is a framing correction, not new source art or changed articulation.

The same targeted check found S027clipped at its original1.075start, so its v2preserves the pullback with1.035→1.015 atcentre(.5,.49). S029already had visible crown margin and is unchanged. The separate first/later v2proofs preserve v1evidence and retain identical audio/timings; see the recovery review for exact hashes.

## Continuous new summer exchange

Root adopted the frozen [LTX summer source recommendation](review/ltx23-summer-pilot-review.md), source `[0,5)` at natural 24fps. The active manifest now uses S025 = 63 lead + 48 new source frames and S026 = the next 72 new source frames, with identical fixed wide framing across their boundary. The earlier historical male crop and proof remain an inactive alternate. M01 and the first-scream source/sequence review records are unchanged.

There is no summer endpoint hold. S026→S027 moves from3042/126.750s to3021/125.875s, adding21frames to the existing P01 shot while preserving absolute original mouth timings. All later boundaries,6,667frames/master audio, root’s S019/S042camera repairs and original configurations remain unchanged. [Exact sequence/context proofs and checks](review/continuous-summer-implementation.md) supersede the former split-summer plan and the old statement that S026is an empty response slot. They do not supersede the preserved source reviews.

The new-motion delivery target is115.083333s, with8.375s of active accepted/inserted new intervals and5.041667s of historical video (M01only). Remaining targeted new motion is106.708333s. The newly assembled summer sequence still requires independent exact-export review; technical checks and source acceptance are not musical listening or full-film completion.

## Renderer1.6.1: scoped performance insertions and contain framing

Root adopted S014source[3,101),98frames, and S046source[3,85),82frames. Both play once at natural24fps with original-master audio, no new hold/loop/retiming and no boundary changes. Earlier summer, M01 and first-plea source/sequence approvals remain unchanged.

Per-clip`framing_policy` defaults to`fill`, preserving existing behavior. Opt-in`contain` decreases the whole source into the output and pads it, with4pixel-aligned scaling for symmetric chroma-compatible padding at standard540p/1080p. S014only uses contain:896×512→944×540 with8px side bands. The full available source border survives; the already-tight native crown is not reconstructed. S046uses normal fixed wide fill and retains its disclosed hand exit, moving-detail softness and repeated upward motif. The policy is explicit in the delivery shot and cache record; invalid values are rejected.

[Final proof hashes, context and checks](review/performance-insertion-implementation.md) identify the separate chorusv2 and third-plea/four-plea review outputs. Eighteen tests pass, including actual7:4 border/frame verification; source/structure checks pass. For concurrent exports use distinct`--work-dir` directories: their concat lists are work-directory local. The final adopted new-source total is15.875s of the115.083333s target, leaving99.208333s unfinished. Exact sequence acceptance and musical listening remain separate from source adoption and technical decoding.


## Quiet arrival and bounded held-contact insertion

Under JML-026, S013 selects A06 source `[3,152)` (149 natural 24fps frames) and S030 selects only L05 `[3,101)` (98 frames). Both are hash-bound approved source intervals using the existing opt-in contain policy; no editor-code change. At 960×540 each preserves the full 896×512 picture with symmetric 8px side padding. There is no added camera movement, loop, retiming or first/final-frame hold, and every shot boundary/master-audio position remains unchanged.

A06 retains the door-bar grip while his head dips and returns; sustained inward eye closure is accepted as an anxious pause. L05 retains its generated push-in/pull-back, native crown/lap crops and tired blink; it is not a locked-camera or proven uneven-breathing success. Its later release/point/regrip and all S032 use remain rejected. Neither L04 nor original full-width L01 is selected. Source reviews remain frozen.

New accepted/inserted source totals 31.666667s of the 115.083333s target; 21.375s already has scoped placement review, and these latest 10.291667s require independent exact-sequence review. Another 83.416667s still lacks accepted source. Historical M01, supplied drawn exposures and holds retain separate accounting. Four separate 960×540 proofs use distinct render work directories; the existing 1080p preflight and cache are untouched. [Implementation evidence](review/quiet-insertion-implementation.md) identifies exact exports and technical checks, not final-film acceptance.


## Fixed window close-up insertion

S003 now selects only the independently reviewed672×378 L01 derivative, source `[3,157)` /154 natural24fps frames. The derivative crop is fixed at original x224/y0/w672/h378; the editor scales its complete16:9 image to960×540 without adding crop, zoom, loop, retiming or holds. All timing boundaries and earlier proofs remain unchanged. No editor-code change is required.

The original full-width reflection failure remains rejected. This derivative excludes the faulty reflected eyes and mouth while retaining faint peripheral ear/cheek/neck/hair fragments; it does not repair the original reflection. The larger coherent head rise/turn, lowered gaze, native crown limitation and small distant passersby are accepted source qualifications. Standalone and S002–S004 context exports require independent editorial review. Accepted new source totals38.083333s;21.375s already had scoped placement reviews and16.708333s now awaits them.77s of targeted new picture still lacks accepted source. The 1080p preflight/cache remain untouched.

[Exact window insertion proofs and technical evidence](review/window-insertion-implementation.md) retain the snapshot and outstanding independent sequence-review scope.
