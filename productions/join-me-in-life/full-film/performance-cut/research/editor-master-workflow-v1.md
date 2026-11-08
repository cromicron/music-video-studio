# Actual complete-master and viewing workflow

This adapts the retained C strict renderer, streamed frame-hash verifier, exact original-song waveform reference, derivative verifier and browser playback method. It does not create another animation/render pipeline or treat two pilot proofs as a completed movie. Frozen provider v1 remains SHA256 `420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e`, 18 takes /128.75 raw seconds. The current partial edit remains 46 shots,28 bound/18 missing at this checkpoint.

## Master and exact pictures

Use the exact edit path/hash from `edit/current-edit.json`. After all footage is reviewed/adopted and bound, the next `build_edit.py` output defaults to intended title **Join Me in Life — Movie and Band**. Historical edit-v003/pilot metadata remains intact. The strict renderer has only trim/timebase/contain/scale/pad/format filters: it adds no opening logo, captions, drawtext or overlays. Do not import the preserved Short's logo/subtitle layers over new organising hands or faces; the default is unobscured story pictures, with the title in metadata.

Render through `tools/render.py` into a fresh ignored `build/performance-cut-final-v1/` master and empty parts directory. Missing footage refuses before rendering. The master must use the whole original take49 once; never concatenate excerpt audio or generated model audio.

Run `tools/verify_master.py --master MASTER --edit PINNED_EDIT --parts-dir ACTUAL_PARTS --output NEW_RECORD`. It rechecks actual source/review/range/cadence and new render/provider/root-adoption provenance, exact plan/render hash and shot order, all46 actual ordered chunks and every6,667 decoded picture, natural24fps, zero audio/video origins, clean intended title metadata, full decoding and the fully decoded original-song waveform at zero offset within4kHz measurement resolution. Hashes stream to small text; no full RGB/YUV dumps. A companion frame-reference index preserves ordered per-frame hashes and source/chunk provenance. Exact equal decoded pictures, if any, are reported without equating pixel identity to acting quality.

`--shots FIRST:LAST` permits only a real existing excerpt; output status explicitly says **not full film**. Both actual pilot proofs passed this route: O01 all192 pictures and B03 all120 pictures match their rendered chunks; exact original-song references correlate0.999992 and0.997253 at zero offset. See the two `editor-*-master-excerpt-verification-v1.json` records. No placeholder full-length master was manufactured.

## All45 joins and whole-film acceptance

The technical record enumerates every current join as `requires_actual_join_review`; it never infers dramatic/cut approval. All45 joins need actual adjacent-frame and natural-speed contextual review, including unchanged source pairings in the new story. Inspect complete1× actual final playback with original music, actual unmuted launch flags and saved buffering/drop/corruption data. [ACCEPTANCE.md](../review/ACCEPTANCE.md) supplies questions, not passing results. Root's exact-master acceptance follows source, joined and whole-film review, with no remaining blocking findings.

## Delivery derivative

`tools/make_viewing.py --master MASTER --acceptance ROOT_ACCEPTANCE --output NEW_MP4 --record NEW_ENCODE_RECORD` requires accepted exact master SHA/bytes for a full film. It retains the tested recipe: libx264 medium, CRF22, maxrate2300k, bufsize4600k, yuv420p, three threads, AACcopy, faststart. The actual result must be below100MiB. The record contains the full executed command. `--excerpt-proof` permits only an actual short file and explicitly does not claim full-film acceptance.

`tools/verify_viewing.py --encode-record RECORD --output NEW_RECORD` reuses the retained C probe/run methods: exact source/output bytes/hashes, all natural frame timestamps, zero origins, unchanged AAC packet hashes/timestamps, full decode, faststart atoms, correct title and whole-file SSIM. Two actual pilot derivatives passed:192/120 frames,376/236 unchanged audio packets, SSIM0.988697/0.983266. Their small sizes do not establish the future full-film file size or final detail quality.

Review compression at native scale on organising record/cup contacts, keyboard cross/keys, guitar and bass hands/headstocks, wide singer palm, A2V mouth/eyes, practiced composure and final tears. SSIM alone does not clear these questions. Keep original896×512 source softness distinct from compression loss.

The adapted `tools/check_viewing_browser.py` keeps the retained preload, actual command-line mute-flag check and event/quality capture. Full defaults now sample organising, band, summer, recognition, pleas, late-band/quiet-guitar and final tears, ending naturally; no stale gold-world target labels. `--segments JSON` allows explicit `[label,start_seconds,duration_seconds]` rows. Short `--excerpt-proof` executes only the real file and cannot stand in for a completed movie. Full-film uninterrupted reviews remain separate from these brief derivative checks.

## Exact archive and private delivery

Only after root whole-film acceptance, use the existing shared `full-film/tools/archive_delivery.py` with the exact master and a **new** `performance-cut/exports/archive/master-v1` directory. Its48MiB parts/index preserve original bytes. Use shared `restore_delivery.py --index NEW_INDEX --output NEW_RESTORE` and compare actual restored size/SHA to the accepted master; retain its record. Never call the old default index, overwrite previous archives or substitute the compressed viewing copy for the master.

Then privately upload the validated viewing copy to Drive, fetch back and verify the actual downloaded hash/bytes and usable download path with retained delivery tools. Keep sources, review gates, plans, provenance and current memory committed/pushed/cold-recovered and integrated into main. No public YouTube publication follows from this workflow.
