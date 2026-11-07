# Full-song storyboard planning animatic

This is a story-and-timing planning film: two stationary endpoint drawings per each of the 49 planned shots, with roughly 40% before and 60% after exposure. It is **not final animation**, generated body motion, or motion acceptance. The strict final editor is unchanged. No zoom, pan, captions, title, logo or fade is added to influence the blind story read.

Revisions 1 and 2 are rendered and frozen. Revision 2 adds root's explicit V2-27 and V2-31 exposures: before 30%, middle 25%, after 45%, within the same shot boundaries. V2-27 makes her refusal visible while the earbud is still offered, before his withdrawal. V2-31 makes one attempted rise and return legible without introducing a second attempt. Neither changes the 49-shot timing. Both middle drawings passed independent static review before root authorized the new planning render. This does not enable middle-frame conditioning in the animation engine. Completed configurations and exports are protected against overwrite; use separate revision paths. The selection gate prevents a complete source catalog from silently becoming a renderable configuration before root's go.

[V2 freeze](frozen-v2.json) binds the 100 exact reviewed static poses, configuration, full export, excerpts and technical evidence. Every decoded picture and timestamp passed, full-song AAC packets match V1 exactly, and actual browser seeks/playback passed at all seven sampled positions including the corrected scenes. [Revised source bindings](revised-source-bindings-v2.json), [informed follow-up ranges](followup-review-ranges-v2.json), [audio continuity](audio-continuity-v2.json) and [decoded sample inspection](output-sample-inspection-v2.json) preserve the evidence. These technical results do not grant musical-cut, narrative or generated-motion acceptance.

[Explicit selection](selection-v1.json) identifies each chosen source revision and panel subset. Selection is never inferred from a filename being newest. GUIDE01b and GUIDE25 have alternative rows for the same action; only the selected primary pair is used. V2-01 adopts the reviewed H01 source pair. V2-17 adopts the exact cropped before reference and standalone corrected after, preserving both complete frames with stationary contain fitting. The older V2-35 performer top pair is excluded after the user's lyric-climax correction; V2-36 retains the older GUIDE18 bottom pair.

[prepare_animatic.py](prepare_animatic.py) reads actual artwork `panel_map` metadata, checks image and review hashes, adopts the independent critic's native crop bytes when available, and records their original review scope. Adoption is not a new visual approval. Other FFmpeg crops remain explicitly provisional. A rejected source, duplicate endpoint, missing endpoint, changed bound image or incomplete 6,667-frame story timeline stops config production. Pending candidates may appear in the planning film with that status recorded in the catalog; final motion has separate source, generated-motion and cut review requirements.

[render_animatic.py](render_animatic.py) invokes the existing [full-film editor](../../../edit.py) with only a scoped stationary contain filter and honest planning classification. It retains the original song at time zero, encodes AAC once for playback compatibility, and runs the editor's full decode, frame and waveform checks. Original v1 configs, art and exports are preserved. The manifest binds the exact story revision, shot-plan hash, source catalog and source bytes.

The original v1 commands were the following. Their completed config/export/review paths are now protected; these are reproduction records, not instructions to overwrite the reviewed version:

```sh
python3 productions/join-me-in-life/full-film/revision-2/tools/animatic/prepare_animatic.py
python3 productions/join-me-in-life/full-film/revision-2/tools/animatic/render_animatic.py \
  --edit productions/join-me-in-life/full-film/revision-2/tools/animatic/edit-v1.json \
  --render --width 1920 --height 1080 \
  --output productions/join-me-in-life/full-film/revision-2/exports/Join_Me_in_Life_V2_Storyboard_Animatic_v1.mp4 \
  --work-dir build/v2-storyboard-animatic-v1
python3 productions/join-me-in-life/full-film/revision-2/tools/animatic/check_animatic.py \
  --video productions/join-me-in-life/full-film/revision-2/exports/Join_Me_in_Life_V2_Storyboard_Animatic_v1.mp4 \
  --config productions/join-me-in-life/full-film/revision-2/tools/animatic/edit-v1.json \
  --work-dir build/v2-storyboard-animatic-v1 \
  --report productions/join-me-in-life/full-film/revision-2/exports/Join_Me_in_Life_V2_Storyboard_Animatic_v1.technical-review.json
```

The final check compares every decoded picture's SHA-256 against the 98 rendered source exposures, validates all 6,667 presentation timestamps and durations, confirms fast-start MP4 metadata and original-song waveform alignment, and actually opens/seeks/plays the file at normal speed in Chromium. Decoded picture comparison avoids treating inserted H.264 parameter headers at concatenation boundaries as picture changes. That browser test establishes playback readiness, not a full creative or listening review. Independent review of the complete song-paced story still follows.

Do not rerun into a reviewed export path after selection changes. Create a new selection/catalog/config/input/output revision so the reviewed bytes remain available. Intermediate unselected crop files are not part of the selected catalog or film.

The separate v2 preparation command was the following. Its completed output paths are now frozen too. For a later version choose fresh paths; the generator exits without a renderable config while exact sources or the root gate remain unresolved:

```sh
python3 productions/join-me-in-life/full-film/revision-2/tools/animatic/prepare_animatic.py \
  --selection productions/join-me-in-life/full-film/revision-2/tools/animatic/selection-v2.json \
  --inputs productions/join-me-in-life/full-film/revision-2/assets/scene-inputs/animatic-v2 \
  --catalog productions/join-me-in-life/full-film/revision-2/tools/animatic/source-catalog-v2.json \
  --config productions/join-me-in-life/full-film/revision-2/tools/animatic/edit-v2.json
```

[Frozen v1 record](frozen-v1.json) binds the reviewed export, its configuration/catalog/selection, technical report and all selected source copies. Future changes to the canonical story plan do not alter that historical evidence. V2 explicitly checks its 49 shot ranges against the frozen v1 configuration.
