# Private LTX-2.3 summer I2V diagnostic

One locally prepared take: original M02 start plus the independently reviewed corrected v2 end, seed 49, 145 frames at natural 24 fps, 896×512. The first and last guides enter both generation stages at pixel indices 0 and 144. The final guide is model conditioning, not a promise of an identical final output frame. This is fresh generation, not a source-preserving repair of M02.

The prompt preserves the responsive summer performance: his brief playful phrase, her short laugh/glance, his warm response, then small settled smiles. It specifies adult face proportions, her green/hazel eyes and freckles, his light facial hair, supported seated bodies, and stable hands, rings, wristband and earbud contact. The original start and corrected v2 endpoint passed [independent static review](../../review/summer-identity-anchor-review.md); the intervening motion remains untested.

No audio is supplied or uploaded. The backend still jointly generates audio and video; generated audio is discarded. The only exported movie must contain one video stream and no audio stream. No sung words or phoneme timing are claimed. The original full master stays separate and unchanged for later editorial muxing.

## Reproduce local preparation

From the repository root, using the existing CPU verification environment:

```sh
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-i2v23/test_pipeline.py
python3 productions/join-me-in-life/full-film/tools/kaggle-i2v23/prepare_bundle.py --output build/jml-kaggle-i2v23-private-20261107-v1 --report build/jml-kaggle-i2v23-private-20261107-v1-report.json
python3 build/jml-kaggle-i2v23-private-20261107-v1/run.py --manifest build/jml-kaggle-i2v23-private-20261107-v1/pilot.json --validate-only
```

Preparation refuses existing destinations. Use a new version for changes; do not modify frozen packages. The generated sibling `-kernel/` folder contains the clean private notebook and provider metadata. Only root submits, inspects remote visibility/files and runs the diagnostic. Neither a local privacy field nor a successful upload proves actual account visibility.

The private dataset is `darionalis/jml-ltx-i2v23-private-inputs`; notebook ID and title agree on `darionalis/join-me-in-life-private-summer-i2v`. Provider metadata titles meet the 6–50 character requirement. Runtime hashes exclude `dataset-metadata.json`, which Kaggle consumes rather than mounts. Canonical source ZIP remains recoverable in Git; the upload folder carries strict ASCII Base64 at `vendor/wangp-source.zip.b64` to prevent Kaggle recursively expanding an archive. Verify that mounted path and the complete runtime package before GPU execution. No `__pycache__`, model weights or audio belongs in the upload.

## Proven runtime reused

The model/source/dependency/patch locks are byte-identical to [A2V v5](../kaggle-a2v/README.md). Backend, model-loading, attention/precision, quantization smoke, sequential text residency and managed-Torch bootstrap functions are checked for AST equality. Frozen A2V source and its full supplied-audio checks remain unchanged. Existing source notices and model terms remain in [NOTICE.md](NOTICE.md) and `vendor/`.

Successful remote A2V v5 evidence is retained at [render.json](../../assets/motion/ltx23-a2v-bridge-pilot/render.json): 97 frames, 24 fps, 896×512, 255.161 s generation, 701.964 s runner, 774.901 s whole job, GPU peaks 11,061,042,688 / 11,524,473,856 bytes. All 1024 text positions were retained; Gemma was released before staging video components. This package copies that schedule, without trimming the prompt or adding another model. Its new prompt token count is measured by the actual pinned tokenizer at runtime; no local count is invented.

The same 18 allowlisted files total 35,379,235,525 bytes. Cache download requires that plus 4 GiB reserve (39,674,202,821 bytes); output requires 2 GiB free. The whole bootstrap, installation, download and inference share a 5400-second deadline with process-group cleanup. Hardware, CUDA/precision and quantization checks run before large weights. No automatic retry, public server, chat/NIM service or token is used.

## Local evidence and remaining limits

[local-validation.json](local-validation.json) records frozen hashes, original and fitted dimensions/hashes, and [11 passing checks](local-tests.log). These exercise the actual pinned source's endpoint construction and four helper calls; both exact fitted images must reach both stages. They also exercise Base64 decoding/corruption, all 260 source-file hashes and 13 patch assertions, a simulated mounted dataset without transport metadata, invalid scopes/inputs, no-CUDA early failure, bounded timeout, and a real 145-frame H.264 encode/full decode. A separate wrapper test uses a synthetic CPU tensor and a stub backend; it is not neural inference.

145-frame memory/time, end-guide behavior, unconstrained joint audio generation and the new prompt are not remotely tested yet. The successful 97-frame A2V job is useful residency evidence, not a guarantee that this larger two-guide job fits. Runtime audits and exact shape/stream checks fail closed; they do not prove acting, anatomy or identity quality. The first remote result needs independent normal-speed and frame review. This preparation accepts no motion and creates no production batch.
