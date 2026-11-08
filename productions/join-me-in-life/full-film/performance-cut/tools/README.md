# Retained strict editor — movie and band reconstruction

The new cut reuses the existing [strict renderer](../../revision-2/tools/editor/strict_edit.py). Its source hashes, review hashes, accepted frame ranges, natural24fps decoding, no-repeat/no-padding rules and original-song checks remain unchanged. [render.py](render.py) is only a portable entrypoint, not another renderer.

The immutable provider [shot plan v1](../story/shot-plan-v1.json) owns generation extents and conditioning. The adopted [editorial plan v2](../story/editorial-plan-v2.json) owns current picture order and the split B06/B09 source selections. Do not submit editorial v2 as a provider job plan or change provider v1 to match later cuts. [Exact current source recipes](../edit/editorial-source-recipes-v2.json) preserve the distinction.

[build_edit.py](build_edit.py) combines editorial v2 with an explicit binding ledger. Existing reviewed source selections are under `shot_sources`; newly accepted provider IDs are added under `take_sources`, with actual source definitions and immutable review gates under `sources`. For example, mapping `take_sources.B06` to one accepted source ID automatically binds both nonoverlapping B06_A/B06_B selections; they are not separate generations. Source/review paths are relative to `productions/join-me-in-life/full-film/`, as required by the retained engine.

The [initial binding ledger](../edit/bindings-v001.json) has26 accepted old selections and no new takes. [Initial partial edit v002](../edit/edit-v002.json) has46shots,26bound/20missing. Those20 selections need18 new provider takes. Root owns later source adoption and binding versions. New gates must name exact actual video SHA, approved ranges and mechanics scope; raw completion is not acceptance.

New source definitions also require `generation.shot_id`, `generation.provider_plan_sha256`, `generation.render_record` and `generation.render_record_sha256`. The builder checks the retained actual render manifest against frozen provider v1: source video hash, shot ID, raw frames/fps, conditioning method, original generation timeline, keeper and handles. A2V also requires the exact stereo48kHz PCM extent. [Actual pilot provenance checks](../research/editor-new-motion-origin-validation-v1.json) exercise O01/B03 and reject stale plan/hash/shot mismatches without inventing motion approval. [Pending pilot source definitions](../edit/pending-pilot01-source-definitions.json) deliberately have unaccepted reviews and cannot enter a render until the critic gate and root adoption exist.

[Prose reconciliation v2](../edit/prose-reconciliations-v2.json) replaces stale gold-world draft descriptions with inspected real-room action. The builder also removes obsolete provider/image/pacing instructions from inherited shots; original source plans remain intact for provenance. Neither operation changes picture source or timing.

From repository root, after saving a new reviewed binding version:

```sh
python3 productions/join-me-in-life/full-film/performance-cut/tools/build_edit.py --story productions/join-me-in-life/full-film/performance-cut/story/editorial-plan-v2.json --bindings productions/join-me-in-life/full-film/performance-cut/edit/bindings-v003.json --reconcile productions/join-me-in-life/full-film/performance-cut/edit/prose-reconciliations-v3.json --output productions/join-me-in-life/full-film/performance-cut/edit/edit-v004.json
python3 productions/join-me-in-life/full-film/performance-cut/tools/render.py productions/join-me-in-life/full-film/performance-cut/edit/edit-v004.json --draft
```

These are command patterns for a later binding version; select fresh versions and preserve every existing reviewed edit. `--draft` validates the story ledger only; without it, missing footage is rejected. An inherited-source-only partial plan cannot render a whole-film fallback.

For a fully bound cut, use the same entrypoint with `--render --output NEW_OUTPUT --work-dir EMPTY_DIRECTORY`. Use `--shots FIRST:LAST` for a contiguous available passage. Output and work paths must be new; the engine preserves prior exports. Final master storage belongs under ignored `build/` until source/cut/full-film acceptance, then a verified archive can preserve it.

[Initial validation](../research/editor-initial-validation-v1.json) records actual checks:26 inherited source hashes/review gates/ranges/cadence pass;46shots cover all6,667 frames; all future source recipes are exact and disjoint; missing O01 rejects before any render. New motion, joins, subjective musical rhythm, instrument playing and completed-film acceptance remain separate.

## Actual first new-source binding

[Current pointer](../edit/current-edit.json) identifies edit-v003, with28bound/18missing. Root adopted O01/B03 through the exact motion/director gates and [root adoption](../review/pilot01-root-adoption-v1.json). [Bindings v002](../edit/bindings-v002.json) adds both actual source definitions, immutable review hashes and retained render-record/provider provenance. [Prose v3](../edit/prose-reconciliations-v3.json) records actual put-away/resting-fingers and wide performance tradeoffs, not the unachieved fully-withdrawn hand draft.

[Actual validation](../research/editor-pilot01-actual-validation-v1.json) proves the two new sources pass the new origin checks and all retained strict source/review/range/cadence guards. Clean1920×1080 isolated O01 eight-second and B03 five-second proofs were rendered under ignored build storage and fully decoded. Both stream origins are zero; original-song waveform offset is zero. Complete opening validation still rejects missing B01 rather than filling it. The exact new-source positive validation is separate from a new joined opening or whole-film approval.
