# Selected original-song performance diagnostics

This separate wrapper prepares exactly one S014 and one S046 take, seed 49, 896×512 at natural 24 fps. It reuses the successful A2V v5 model-loading, precision, device residency, full-audio conditioning and managed-Torch installation paths. Frozen A2V and summer I2V packages remain unchanged. Root alone uploads or executes this package; local preparation accepts no motion.

| Shot | Native start image | Original master excerpt | Frames | Intended source use |
| --- | --- | --- | ---: | --- |
| S014 first-chorus appeal | Original P02, 1672×941 | 66.375–70.750 s | 105 | `[3,101)` → master 66.500–70.583333 s |
| S046 third screamed plea | Original P03, 1672×941 | 215.833333–219.541667 s | 89 | `[3,85)` → master 215.958333–219.375 s |

Frame intervals are zero-based and end-exclusive. Both takes have three head-handle frames and four tail-handle frames. Both counts satisfy `8n+1`. Audio is untouched original stereo 48 kHz decoded to PCM16 with exact sample trims: S014 starts at sample 3,186,000 and contains 210,000 samples; S046 starts at 10,360,000 and contains 178,000. No retiming, invented silence, padding, gain adjustment or vocal separation. The original master remains separate and unchanged. The short handles contain the actual adjacent song, not assumed isolated speech. No new listening/phoneme verification is claimed.

The [selected action plan](../../review/action-coverage-plan.md) assigns these performances. Native P02 already has a supported low open palm, and P03 already extends the free palm in a plea. Both were visually inspected; no revised start still is required for these bounded tests. P02 retains planted feet and a small tension/breath change. P03 sustains its existing reach, with a more urgent third screamed plea, without retracting and starting another reach. Neither uses the rejected final frame of S044. The adopted S044 source interval `[0.125,3.5)` remains a separate source decision. Both PNGs are aspect-fitted to 896×512 with no cropping or stretching; fingers/hair/shoes are retained.

## Execution and recovery

One installation and one 5400-second deadline cover setup, downloads and both child processes. Each child loads the model and encodes only its own prompt; Gemma is released before video components move onto GPU1, exactly as in v5. Child process exit frees its CUDA state before the next child starts. Installed dependencies and the verified 35,379,235,525-byte weight cache are shared. This intentionally reloads weights from disk for shot two instead of introducing an all-prompt/model residency cache. Existing cached files are hashed again; no second model download is needed when they remain valid.

Outputs are separate `S014/` and `S046/` directories, each with its own render/environment/patch/log records, silent MP4 and original-PCM review MKV. One failed take gets a separate failure record and is never retried; the distinct second requested shot may still run within the remaining deadline. A whole-job timeout stops the process group and marks the unstarted shot. No more than these two selected manifests is allowed. Existing job/render records are not overwritten.

The backend still jointly generates video/audio. Only supplied source audio is used for conditioning and review; returned model audio is discarded. The unchanged backend guard rejects insufficient encoded audio coverage instead of silently using a prefix. Its pinned shape calculation requires 109 latent frames for S014 and 93 for S046; **actual audio encoder output counts are not yet measured**, and must pass at runtime. The synthetic local branch tests establish rejection behavior, not those encoder counts. Original stereo PCM must survive the review mux byte for byte. Original full-song audio should be used for the final edit after actual motion review.

## Reproduction

From the repository root:

```sh
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-performance23/test_pipeline.py
python3 productions/join-me-in-life/full-film/tools/kaggle-performance23/prepare_bundle.py --output build/jml-kaggle-performance23-private-20261107-v1 --report build/jml-kaggle-performance23-private-20261107-v1-report.json
python3 build/jml-kaggle-performance23-private-20261107-v1/run.py --manifest build/jml-kaggle-performance23-private-20261107-v1/S014.json --validate-only
python3 build/jml-kaggle-performance23-private-20261107-v1/run.py --manifest build/jml-kaggle-performance23-private-20261107-v1/S046.json --validate-only
```

Use a fresh version name if the destination exists. [Audio provenance](inputs/S014-conditioning.json) and [third-plea provenance](inputs/S046-conditioning.json) retain exact FFmpeg commands/master and PCM hashes. [NOTICE.md](NOTICE.md) preserves upstream authorship and licenses. Canonical source ZIP remains recoverable in Git, while private upload staging uses validated Base64 at `vendor/wangp-source.zip.b64` to avoid recursive archive expansion. Transport-only `dataset-metadata.json` is excluded from runtime integrity because Kaggle consumes it. Root must inspect the remote private dataset and mounted file paths before execution. No `__pycache__` or master song belongs in the package.

Private dataset ID: `darionalis/jml-ltx-performance23-private-inputs`. Private notebook ID/title slug: `darionalis/join-me-in-life-private-song-performances`. The notebook has no outputs or public service. It uses the previously proven pinned managed CUDA image and dual T4 selection. Source/CUDA/quantization smokes precede large weights; cache space requires 39,674,202,821 bytes including reserve, and output requires 2 GiB free per preflight.

## Verified and unproven

[Local validation](local-validation.json) and [test log](local-tests.log) record 11 passing tests: exact native inputs/selected frame counts; sample-identical original audio; unchanged successful runtime functions/pins; simulated Kaggle mount without metadata; strict Base64/source/patch integrity; actual pinned coverage branch and target-shape calculation; synthetic CPU wrapper shapes; real codec/full-decode and lossless PCM muxes; real separate child failures/shared cache; whole-job timeout/no second launch; no-CUDA early stop and private notebook metadata.

Those tests are offline and contain no neural inference or provider calls. 105/89-frame remote memory/time, actual audio encoder counts, prompt token counts and output quality remain unproven. The real tokenizer counts each full prompt at runtime with no truncation and retains all 1024 padded positions. No longer quiet-motion batch is proposed here; wait for actual 145-frame summer evidence before making that residency decision. Motion identity, microphone/ring/hand continuity, supported body action, mouth timing and editorial joins require independent review of each resulting take.
