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

[current-edit.json](current-edit.json) points to the newest immutable edit version. `edit-v007.json` binds root-adopted story SHA `e928f3765dbbce2b7fcfef1c1cf2e87e38edcb47bcbad36930fdc3e942c6aa15`. C01–C04 opening, C16 original summer `[0,120)` and repaired performance-b C29 `[6,87)` plus performance-c C31 `[6,89)` are the seven accepted motion bindings. The rejected performance-a C29/C30 sources remain absent; 32 shots are unbound.

The eight-second [opening progress proof](../../exports/Unfinished_Morning_Opening_8s_v1.mp4) was rendered through the strict editor with the exact original song. Its [manifest](../../exports/Unfinished_Morning_Opening_8s_v1.manifest.json) records source binding, complete decode and zero-offset waveform check. [Equivalence](../../exports/Unfinished_Morning_Opening_8s_v1.equivalence.json) proves all 192 decoded pictures and all 376 AAC packet hashes/timestamps match the independently reviewed diagnostic. That historical proof is superseded by the corrected, joined opening v2 described below. Full-film pacing remains unreviewed.

Later acceptance-bound updates create a new numbered edit and update this pointer. Prior edits remain historical. The full edit must continue refusing unbound footage rather than padding it.

The [first-plea proof](../../exports/Unfinished_Morning_First_Plea_v1.mp4) uses repaired C29 with the original 207.875–211.25s song excerpt. Its [manifest](../../exports/Unfinished_Morning_First_Plea_v1.manifest.json) records zero-offset correlation 0.999592. All 81 decoded pictures match the independently reviewed diagnostic; the AAC packet bytes differ because the retained editor uses input seeking rather than the diagnostic's full-decode sample trim. [Equivalence record](../../exports/Unfinished_Morning_First_Plea_v1.equivalence.json) reports that distinction explicitly. It is retained for the combined bridge/four-plea review, not an accepted full sequence.

## Unbound motion diagnostics

[make_unbound_diagnostic.py](make_unbound_diagnostic.py) prepares exact-original-song 1080p clips for the independent reviewer before a motion verdict exists. It checks the declared actual source SHA, decoded natural 24 fps, exact keeper length against the frozen C story slot, original 48 kHz stereo song SHA, full output decode and waveform alignment. It writes a separate explicitly unbound diagnostic and reproducible JSON; it never updates the binding ledger or claims creative acceptance. Existing outputs cannot be overwritten.

Actual opening-b C02/C03/C04 diagnostic executions passed their complete decode and zero-lag audio checks. A bad source hash and an undersized keeper were rejected before creating output in [diagnostic-tool-validation.json](diagnostic-tool-validation.json). The production editor's acceptance requirement remains separate.

The [33.125-second opening candidate](../../exports/Unfinished_Morning_Opening_33s_v1.mp4) joins C01–C04 at their exact original-song ranges. Its [manifest](../../exports/Unfinished_Morning_Opening_33s_v1.manifest.json) and [picture-equivalence record](../../exports/Unfinished_Morning_Opening_33s_v1.equivalence.json) preserve technical proof. Its joined review was held for the C01 endpoint pop; v2 below repairs that issue and passes the scoped joined review.

## Corrected opening range

The joined review caught a one-frame face/pose redraw at raw C01 frame 197, previously retained as master frame 191. Root adopted a new immutable [range review](../../review/C01-opening-a-v2-range-v2-review.json) and changed C01 to raw `[5,197)`, keeping all 192 timeline frames. The earlier eight-second proof and 33-second v1 are preserved but superseded for current source selection.

[Corrected 33-second v2](../../exports/Unfinished_Morning_Opening_33s_v2.mp4) uses `edit-v006`. All 192 C01 source selections move one frame earlier; this is not merely a one-picture substitution. [Repair diff](../../exports/Unfinished_Morning_Opening_33s_v2.repair-diff.json) proves C02–C04’s 603 pictures and all original-audio packets/timestamps are unchanged. The [final repaired joined review](../../review/opening-33s-v2-joined-review.json) passes the exact v2 opening and its three joins; full-film acceptance remains separate.

## Exact audio references for short diagnostics

The C30–C32 diagnostic media passed full decode but initially fell just below the legacy 0.995 correlation threshold when its reference used MP3 input seeking. Comparing the unchanged media against a full decode of the original song, trimmed at the exact 48 kHz sample indices before downsampling, gives zero-lag correlations above 0.9993. Both results remain in each diagnostic JSON. The helper now uses this exact reference for its unchanged 0.995 correlation / 30 ms offset gate and preserves the legacy comparison as supplementary evidence. The retained strict renderer and original audio are unchanged.

[Exact-reference validation](exact-audio-reference-validation.json) records all three actual outputs and a one-frame-shifted negative control that fails the gate. The [four-plea diagnostic](../../exports/C29_C32_Four_Pleas_Diagnostic_v1.mp4) uses one continuous original-song excerpt across all four shots; its passing technical check does not adopt the new performances. C30 is rejected and C32 held by the independent acting review; neither belongs in the current edit.
