# Four selected quiet-motion diagnostics

This separate private package prepares exactly four distinct takes from the [selected action plan](../../review/action-coverage-plan.md). Each uses its unchanged reviewed source PNG as **both first and last semantic guides**, seed 49, 896×512 at natural 24 fps. Matching guides constrain the pose but do not prove movement, output pixel identity, or editorial acceptance. No other quiet shots or production batches are prepared here.

| Take / placement | Source | Total frames | Used source frames | Head / tail handles |
| --- | --- | ---: | --- | --- |
| L01 / S003 | Refined window reaction | 161 | `[3,157)` =154 | 3 / 4 |
| A06 / S013 | Refined arrival | 161 | `[3,152)` =149 | 3 / 9 |
| L04 / S019 | Original S02 waiting close-up | 145 | `[3,135)` =132 | 3 / 10 |
| L05 / S030 then S032 | Original M01 embrace endpoint | 201 | `[3,101)` =98, then `[101,197)` =96 | 3 / 4 |

Frame intervals are zero-based and end-exclusive. All totals are the next `8n+1` count covering the used frames plus at least three head/four tail frames. The aftermath portions are consecutive and non-overlapping: no replay of its earlier source section in S032. This is 629 intended editorial frames / 26.208333 seconds across 668 generated frames / 27.833333 seconds; none is accepted by preparation.

The two 161-frame clips last 6.708333 s, waiting lasts 6.041667 s, and aftermath lasts 8.375 s. Last-guide pixel indices are 160, 160, 144 and 200. Runtime audits the exact fitted RGB image, index, strength and dimensions at both generation stages. Inputs are aspect-fitted without cropping/stretching; three 1672×941 sources become 896×504 on an 896×512 canvas, while the 1916×1080 embrace endpoint becomes 896×505. Black border offsets and fitted hashes are recorded in [local-validation.json](local-validation.json).

## Intended action and source limits

All four actual PNGs were inspected at native dimensions. [Window static review](../../review/her-window-refined-review.md) supports an inward reaction with limited headroom: one heavy breath and brief blink, with the reflection making corresponding changes at the same time. No upward head lift, new turn or recovery smile. [Arrival static review](../../review/arrival-doorway-refined-review.md) supports worried attention and a restrained breath; the fingers/rings remain on the existing pull bar. No grip release, fresh reach, door mechanism or new step is requested.

The original waiting source keeps him worried and her withdrawn, seated apart **before contact**, with a small breath/blink and no reach toward her. The [reviewed embrace endpoint](../../review/aftermath-edit-candidate.md) starts **after contact**: his visible hand remains on her outer upper arm, her own hands stay passive in her lap, and each head remains self-supported. Small naturally uneven breaths and a tired blink must preserve that geography. No fresh pull, squeeze, stroke, head pat or repeat of the embrace. Prompt wording is a request to the model, not evidence of compliance.

Per-take JSON under `provenance/` records source hash/bytes/dimensions, review location, exact editorial mappings and static-only limits. No source was redrawn, enhanced, cropped or substituted. Existing source crops and legitimate occlusions remain; the generator must not invent missing anatomy. Motion, identity, hands/contact, reflection synchronization and joins still need independent review.

## Proven runtime and new limits

The successful [145-frame summer render](../../assets/motion/ltx23-summer-pilot/render.json) used this same Q4 LTX-2.3 source, precision and sequential Gemma/video residency: 333.190 s generation, 746.989 s runner, 804.044 s whole job; GPU peaks 11,143,011,840 / 11,524,473,856 bytes. All 1024 text positions were retained, Gemma was released before video staging, and both endpoint guides were observed in both stages. That proves technical execution for its 145-frame inputs, not this package's acting or 161/201-frame memory fit. **The 201-frame aftermath is a new measured memory/runtime trial**, with no automatic OOM retry or silent shortening.

Loader, precision/attention patches, quantization smoke, preflight, image fitting and dependency/source/model/patch locks are unchanged from successful I2V. The separate [performance wrapper](../kaggle-performance23/README.md) supplies the identical serial child scheduler and managed-Torch pipless bootstrap. One environment and verified downloaded weight cache are shared; each take gets a fresh child/model load and its own text encoding, CUDA state, backend directory, output folder and failure records. No all-prompt cache is introduced. A failed take is recorded without retry; later distinct takes may run. One 5400-second deadline covers installation, downloads and all four takes; timeout stops the process group and marks remaining takes unstarted. Existing job/render records are preserved.

No audio is supplied, uploaded or exported. The backend **still performs joint audio/video generation**, and returned model audio is discarded. Every output movie must have exactly one video stream and no audio stream. The original master remains separate and unchanged for later editorial mux. All 18 pinned weight files are reused: 35,379,235,525 bytes, plus a 4 GiB cache reserve and 2 GiB output reserve at preflight. Source, CUDA and quantization checks precede downloads. Attribution, canonical source and model terms remain in [NOTICE.md](NOTICE.md) and `vendor/`.

## Reproduce and deploy privately

From the repository root:

```sh
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-quiet23/test_pipeline.py
python3 productions/join-me-in-life/full-film/tools/kaggle-quiet23/prepare_bundle.py --output build/jml-kaggle-quiet23-private-20261107-v1 --report build/jml-kaggle-quiet23-private-20261107-v1-report.json
python3 build/jml-kaggle-quiet23-private-20261107-v1/run.py --manifest build/jml-kaggle-quiet23-private-20261107-v1/L01.json --validate-only
python3 build/jml-kaggle-quiet23-private-20261107-v1/run.py --manifest build/jml-kaggle-quiet23-private-20261107-v1/A06.json --validate-only
python3 build/jml-kaggle-quiet23-private-20261107-v1/run.py --manifest build/jml-kaggle-quiet23-private-20261107-v1/L04.json --validate-only
python3 build/jml-kaggle-quiet23-private-20261107-v1/run.py --manifest build/jml-kaggle-quiet23-private-20261107-v1/L05.json --validate-only
```

Use a fresh version when a destination exists; never alter frozen packages. Root owns provider actions. Private dataset: `darionalis/jml-ltx-quiet23-private-inputs`. Notebook ID/title slug: `darionalis/join-me-in-life-private-quiet-motion`. The generated sibling `-kernel/` contains an output-free notebook and private pinned-T4 metadata. Inspect actual remote privacy and mounted paths before GPU execution. Runtime hash checks exclude `dataset-metadata.json`, which Kaggle consumes; the canonical Git-retained ZIP travels as validated `vendor/wangp-source.zip.b64` to avoid archive expansion. No `__pycache__`, audio, master or weights belongs in the upload.

## Local evidence

[Eleven tests pass](local-tests.log): source/handle/partition invariants; rejection of changed scope or repeated aftermath source; metadata-absent Kaggle mount and Base64/source/patch integrity; unchanged successful runtime functions/pins; actual pinned backend endpoint construction and four stage helper calls for every take; missing/wrong guide rejection; synthetic CPU wrapper shapes for all four inputs; real 145/161/201-frame FFmpeg encode/full decode and audio-track rejection; real four-child scheduling after one failure; deadline cleanup/no later launch; no-CUDA early failure and private notebook checks. The neural backend is stubbed only in the full-wrapper tensor test; actual model inference is not claimed.

No provider calls, model weight downloads, GPU jobs or motion acceptance occurred during preparation. New prompt token counts will be measured by the real pinned tokenizer at runtime, with no truncation and all 1024 padded positions retained. Remote success, meaningful non-repeating motion and independent scene review remain separate gates.
