# Reuse audit: seven small active storyboard sources

7 November 2026. **Reuse the existing refined window candidate first; do not regenerate it.** There is no pixel-exact high-resolution version of the seven panels in the inspected sources. The window has a suitable reviewed redraw; other candidates require an explicit change of angle/action, not a silent resolution replacement. No image, edit, account or provider was changed.

The unchanged edit SHA-256 is `f8d78f4b665ac8ccd51b0fd2e8ac41bfbb2e542501cf15c21db779699a45cc30`. Its seven small sources appear in **23 of 58 shots / 2732 frames / 113.833333 seconds** (24 fps). Their source widths are 546–551 px and heights 306 px. The largest existing camera zoom is 1.075. Rendering them at 1080p cannot recover missing detail. All seven were measured as pixel-exact crops from the original 1672×941 nine-panel board; that larger file is not a higher-resolution individual shot.

## Active files and uses

Paths below are relative to `full-film/assets/`; SHA-256 values and frame-exact uses are in [the measured inventory](small-source-reuse-audit.json).

| File | Native size | Active shots | Screen time |
| --- | --- | --- | ---: |
| `night_hospital.png` | 548×306 | S001, S012, S031, S038 | 20.042 s |
| `her_doorway.png` | 546×306 | S006, S009 | 8.333 s |
| `snow_journey.png` | 548×306 | S011 | 5.500 s |
| `his_arrival.png` | 551×306 | S013 | 6.208 s |
| `her_window.png` | 546×306 | S003, S010, S015, S021, S024, S034, S041, S045 | 37.583 s |
| `corridor.png` | 548×306 | S005, S018, S035, S039 | 19.792 s |
| `dawn_together.png` | 546×306 | S053, S056, S058 | 16.375 s |

## Source matches and deliberate alternatives

**night_hospital:** No same-scene high-resolution match found. B03 is a different courtyard at dawn, without the frontal lit entrance; changing its colour would not restore this scene. Retain composition as the brief for a future high-resolution source. Keep one consistent entrance shared with journey/arrival; do not regenerate four separate plates.

**her_doorway:** A02 preserves approved identity, clothes and hospital withdrawal, but she is seated at the window in a portrait frame, not standing in this doorway. S01/S02 include him and would prematurely establish his presence. If the two shots only need the inward portrait described in edit.json, an explicit restaging to A02 is possible; it is not an exact replacement. Prefer revising/reusing one reviewed portrait over inventing another face, while checking repetition and 16:9 crop detail.

**snow_journey:** No matching high-resolution rear-view walk toward the snowy entrance. Character/angle sheets are isolated pose references, not walking/contact footage or this background. Preserve this specific travel action when a new keyframe is needed; a portrait, camera move or standing cutout cannot replace a believable walk. Reuse the same entrance design as night_hospital.

**his_arrival:** No matching high-resolution door-handle/arrival plate. Existing S01/S02/M01 show him already seated beside her; cropping him from those images changes the action and chronology. Keep as a separate source gap. Use A01 for identity and existing hospital/performance art for light facial hair/clothes; do not replace frightened arrival with an unrelated seated reaction.

**her_window:** Existing refined candidate is the same scene/acting intent and a source-reviewed compatible redraw, not the same pixels or a mathematically exact upscale. A02 is the approved identity source, but a different frontal portrait composition. Reuse the existing refined candidate as the first candidate for these uses; no new artwork needed for the source test. Recheck each crop, reflection and post-embrace context before edit promotion. Do not mechanically copy the existing 1.075 zoom into its already tight crown crop.

**corridor:** B01 is a compatible high-resolution empty hospital waiting-room angle: same blue chairs, left windows and warm doorway. It lacks the deep axial corridor/vanishing point, so it is a scene-angle substitution. Reuse B01 for an explicitly revised empty-hospital pause where corridor travel/distance is not essential, especially S005 before arrival. Later empty views must not imply the couple vanished. Preserve the corridor as a source gap if its axial composition is retained.

**dawn_together:** S06 has the same pair, present clothes, unresolved exhaustion and dawn, but they remain INSIDE. B03 is OUTSIDE but empty and differently composed. Neither is the two-person exterior bench. Do not silently swap in S06 after the established exterior transition; that would reintroduce an indoor/outdoor jump. Either retain the outdoor-bench source gap or explicitly revise the ending to stay indoors. The ending remains a proposal, not approved recovery.

## Existing higher-resolution candidates

These are source candidates, not blanket user-approved shot replacements. Only A01/A02 carry approved identity/style authority; [the art guide](../../art/README.md) distinguishes candidate scene art. All paths in this table are relative to the production root.

| Source | Native size | SHA-256 |
| --- | --- | --- |
| `full-film/assets/her_window_refined_candidate.png` | 1672×941 | `9778c0c714d6a58eda8ed9b09f6acd51ab075aa16cb4578fae8b9099a0230eb7` |
| `art/00_References/A02_Approved_Anime_Window.png` | 941×1672 | `9abac2af3dba99e0efb7461d795d89e7d8c85b53f6f8ec2b0e86b900e7baaedd` |
| `art/05_Backgrounds/B01_Empty_Waiting_Room.png` | 1672×941 | `c68e74c0b5845bfe6c539b1ca70c66a2bc0545e6f186c596cd9f7ec6855205c5` |
| `art/03_Story/S06_Still_Here_At_Dawn.png` | 1672×941 | `09a04d5fdc90152550372722789c1c464239f3f16cae3ad03da63d5fecf74774` |
| `art/05_Backgrounds/B03_Blue_Dawn_Courtyard.png` | 1672×941 | `f024981051483cc0f4a8be2f3f0e24e127542ee68df698a0a17b50c17fe44f83` |
| `reference/blender-pilot/assets/background.png` | 1672×941 | `e00d32de460f391c0d20a5dffd74a32950e31a6db2e2e4f216686e5b6ac52de1` |

The refined window already passed [independent static-source review](../review/her-window-refined-review.md): detailed drawn identity, downward gaze and shoulder support are compatible; it inherits the crown crop and provides no hand evidence. This audit also viewed it, A02, B01, S06, B03 and the full source board. The old Blender reference background is a dusk lake, not the hospital, snowy approach or courtyard; its resolution is irrelevant to these scenes.

The largest immediate saving is **eight window uses / 37.583333 s**. A source promotion would still need framing/movement review and the [post-embrace continuity rules](../review/short-to-full-continuity.md); later solo reactions must not erase established contact. Do not claim those seconds are already animated. A02 is 941×1672 portrait: fitting a wide crop retains only about 941×529 source pixels, so it is not equivalent to the 1672×941 refined wide source.

The corrected room pair is already active and is **not** among the seven: `night_room_v2.png` is 1176×660 and `morning_room_v2.png` is 1176×658. Preserve the made-bed/cup-handle correction; do not revert to the original 551×306 room cells. These sources are still below native 1080p but are a separate, smaller scale-up issue, not evidence that nine tiny panels remain.

## Recovered-source coverage

Fetched heads with `python3 tools/studio.py --refresh` without switching/resetting the shared branch. Current branch includes fetched main; local work was preserved. Compared every PNG/JPG/JPEG/WebP/ZIP blob in the three recovered branch tips against HEAD:

| Recovered branch | Pinned commit | Distinct media blobs absent from HEAD |
| --- | --- | ---: |
| `origin/prep/join-me-in-life-recreation` | `3550b3f4a03c1652ccb8aacd53c4bc9fc1a25c93` | 0 |
| `origin/research/video-generation-approach` | `c2b7d256b631e973d528c79c728dda0a45dd9817` | 0 |
| `origin/codex/hedra-mcp-registration` | `656d80ef865b7ff16bd6f0e8d96a0d0b6ac377aa` | 0 |

Those tips therefore supply no new image version to promote. Duplicate A02 and S01/S02 files in `current/assets/` match their `art/` counterparts by SHA-256, not merely by filename.

The optional v1 release archive is absent locally. Its preserved source map lists identity/cutout sheets plus stage, waiting room, tram reflection and distance/curtain concepts; their pixels were **not** inspected and no claim of visual compatibility is made. It supplies no evidenced high-resolution copy of these newly drawn scenes. This is a bounded audit of actual used sources and accessible recovered tips, not a search of every private historical chat.

Verification: image dimensions/SHA-256 read directly; all seven crop pixels compared to extraction rectangles; exact shot/frame totals computed from edit.json; recovered branch media compared by Git blob; `python3 tools/studio.py --check` and `python3 tools/review.py --source-only` passed. No export, source artwork, camera or story decision was changed.
