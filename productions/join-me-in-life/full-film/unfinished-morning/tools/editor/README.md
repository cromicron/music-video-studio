# C incremental editor

The selected film reuses the [retained strict assembly engine](../../../revision-2/tools/editor/strict_edit.py), with only root-authorized backward-compatible metadata fields: optional plan title and production identity in the new output manifest. Existing default title/production remain revision 2; historical edits and outputs are untouched. All source/review paths in an edit remain relative to `full-film`. The original take 49 audio remains at its original absolute time; excerpts use the matching original-song range.

[build_edit.py](build_edit.py) reads the director's complete C story plan and [motion-bindings.json](motion-bindings.json). The binding ledger is separate from creative planning and starts empty. Add a source only after root adopts an independent motion review naming the exact video SHA, exact accepted half-open frame range, and exact review SHA. Then bind each story shot to its source ID and matching interval. Technical provider completion is not motion acceptance.

The builder validates the full 6,667-frame story and checks every supplied binding with the same strict engine: natural 24 fps, actual decoded extent, reviewed intervals, no overlapping reuse even through source aliases, no still fallback or padding. It writes a new version only, preserving existing files. Missing source shots remain visibly unbound and cannot render. It records current story/ledger/engine hashes.

```sh
python3 productions/join-me-in-life/full-film/unfinished-morning/tools/editor/build_edit.py \
  --story productions/join-me-in-life/full-film/unfinished-morning/story/shot-plan-v1.json \
  --bindings productions/join-me-in-life/full-film/unfinished-morning/tools/editor/motion-bindings.json \
  --output productions/join-me-in-life/full-film/unfinished-morning/tools/editor/edit-v001.json
```

Once actual reviewed adjacent shots exist, run the retained engine with that edit, `--shots FIRST:LAST --render --output NEW.mp4 --work-dir NEW_EMPTY_DIR`. A full render without all sources must fail. Source acceptance does not approve the actual cut, emotional contrast, phrase timing or full film; the independent reviewer owns those checks.

The engine supports one source interval per shot. A legitimately split action can be represented by separately named contiguous subshots in a revised canonical C plan, preserving total timing and exact unique source provenance. Do not concatenate sources invisibly into a derivative to evade overlap or review checks. No renderer extension is currently needed.

[Summer evidence](summer-source-ledger.json) distinguishes the preserved original R4 performance, quieter first-full-film replacement, male-only crop and rejected pilots. Its recommendations are not new source acceptance. Existing artwork/source bytes and their historical verdicts remain unchanged.

## Current edit

[current-edit.json](current-edit.json) points to the newest immutable edit version. `edit-v004.json` binds root-adopted story SHA `e928f3765dbbce2b7fcfef1c1cf2e87e38edcb47bcbad36930fdc3e942c6aa15`. C01 opening `[6,198)`, C16 original summer `[0,120)` and repaired performance-b C29 `[6,87)` are the only accepted motion bindings. The rejected performance-a C29/C30 sources remain absent; 36 shots are unbound.

The eight-second [opening progress proof](../../exports/Unfinished_Morning_Opening_8s_v1.mp4) was rendered through the strict editor with the exact original song. Its [manifest](../../exports/Unfinished_Morning_Opening_8s_v1.manifest.json) records source binding, complete decode and zero-offset waveform check. [Equivalence](../../exports/Unfinished_Morning_Opening_8s_v1.equivalence.json) proves all 192 decoded pictures and all 376 AAC packet hashes/timestamps match the independently reviewed diagnostic. The C02 join and full-film pacing remain unreviewed.

Later acceptance-bound updates create a new numbered edit and update this pointer. Prior edits remain historical. The full edit must continue refusing unbound footage rather than padding it.

The [first-plea proof](../../exports/Unfinished_Morning_First_Plea_v1.mp4) uses repaired C29 with the original 207.875–211.25s song excerpt. Its [manifest](../../exports/Unfinished_Morning_First_Plea_v1.manifest.json) records zero-offset correlation 0.999592. All 81 decoded pictures match the independently reviewed diagnostic; the AAC packet bytes differ because the retained editor uses input seeking rather than the diagnostic's full-decode sample trim. [Equivalence record](../../exports/Unfinished_Morning_First_Plea_v1.equivalence.json) reports that distinction explicitly. It is retained for the combined bridge/four-plea review, not an accepted full sequence.
