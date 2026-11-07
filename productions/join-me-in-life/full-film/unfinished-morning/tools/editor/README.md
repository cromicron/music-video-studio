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

[current-edit.json](current-edit.json) points to the newest immutable edit version. `edit-v011.json` binds root-adopted story SHA `e928f3765dbbce2b7fcfef1c1cf2e87e38edcb47bcbad36930fdc3e942c6aa15`. The nineteen accepted shots are C01–C09, C16 and C26–C34; twenty shots remain unbound. Earlier rejected/held takes remain absent. Current C01 uses `[5,197)` and C09 `[2,206)`. C28's broader smile is accepted only within the reviewed bridge context as private finality; C33→C34 is a visible small time elision.

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

## Extended opening

Root adopted C05–C09 from the [independent range review](../../review/C05-C09-opening-c-v2-motion-review.json). C09 uses corrected raw `[5,209)` to exclude the transient wrist distortion at raw 209; its older diagnostic is retained as held evidence. `edit-v008` preserves corrected C01 `[5,197)` and adds these five sources. The 75-second C01–C09 cut is an internal joined-review candidate, ending within his imagined morning. The passed corrected 33-second opening remains the user progress proof until a suitable longer sequence has passed review.

The first 75-second cut passed [scoped joined review](../../review/opening-75s-v1-joined-review.json). Root then chose a further C09 hand-detail improvement: new source range `[2,206)` replaces `[5,209)` without changing the 204-frame slot. The [new immutable range gate](../../review/C09-opening-c-v2-range-v3-review.json) binds this selection in `edit-v009`; corrected 75-second v2 passed its [focused insertion and cut review](../../review/opening-75s-v2-joined-review.json). Prior passing v1 remains preserved, not silently overwritten.

The [second four-plea diagnostic](../../exports/C29_C32_Four_Pleas_Diagnostic_v2.mp4) substitutes new performance-D C30/C32 between the accepted C29/C31. It has one continuous original-song excerpt and passing exact-sample audio/decode checks, but remains unbound pending independent acting and sequence review. Earlier rejected or held performances remain historical, not current bindings.

Root adopted performance-D C30/C32 using the [corrected source gate](../../review/C30-C32-performance-d-v2-motion-review-v2.json) and [four-plea sequence gate](../../review/four-pleas-diagnostic-v2-joined-review-v2.json). Those gates explicitly correct an earlier browser limitation: DOM `muted=false` did not establish audible browser output because Playwright had launched with `--mute-audio`. The repeat removes that default and verifies actual CDP launch arguments. This establishes unmuted browser execution, not subjective hearing or physical speaker output. All prior records remain historical. `edit-v010` binds the fourteen accepted sources; longer bridge joins remain pending.

The [accepted four-plea proof](../../exports/Unfinished_Morning_Four_Pleas_v1.mp4) uses `edit-v010`. Its [equivalence record](../../exports/Unfinished_Morning_Four_Pleas_v1.equivalence.json) proves all 375 decoded pictures match the independently reviewed diagnostic. AAC packet bytes differ between input-seek and full-decode sample-trim encoding; exact original-sample correlation is 0.999476 at zero lag. No standalone upload is planned; the upcoming bridge context remains a separate review.

## Final delivery preservation

A large accepted master can be preserved byte-for-byte with the shared [archive tool](../../../tools/archive_delivery.py), using a fresh archive directory. It writes verified48MiB parts and an index; it refuses an existing directory and detects a changing source. The shared [restore tool](../../../tools/restore_delivery.py) now accepts `--index` while preserving the first film's defaults. For a custom index, writing requires an explicit `--output`; `--check` verifies all part and combined hashes without writing. This does not recompress the film or create another creative version.

[Actual archive validation](../../research/delivery-archive-validation-v1.json) packed and restored the existing130,358,771-byte film in three parts, confirmed exact identity, refused an existing archive and missing custom output, and rejected one corrupted part. Temporary test copies were removed; original archive/master bytes remain unchanged. The new C master will need its own final archive and hash verification after whole-film approval.

## Accepted bridge context

Root adopted the five bridge sources from the [motion review](../../review/bridge-a-v2-motion-review.json) together with the [C26–C34 joined review](../../review/bridge-C26-C34-diagnostic-v1-joined-review.json). The actual C27 fold rests near the table edge. C28's broader approximately four-second closed-eye smile is context-bound private finality, not recovery or a new summer memory. C33→C34 contains an accepted small time elision, not a seamless action match. These limitations travel with `edit-v011`; the rest of the full film and adjoining ranges remain pending.

The [named accepted 48-second bridge proof](../../exports/Unfinished_Morning_Bridge_48s_v1.mp4) uses `edit-v011`. Its [equivalence record](../../exports/Unfinished_Morning_Bridge_48s_v1.equivalence.json) proves all 1,154 pictures match the reviewed diagnostic and the original song has zero-offset waveform alignment. AAC packet bytes differ because of the retained excerpt encoding methods; packet identity is not claimed. At 32,127,341 bytes with faststart it fits the existing 100 MiB connector limit without further recompression. Root owns private delivery; the editor has not uploaded it.
