# Original-song performance pilot V2PERFA

**Operations saved and verified private no-run version 1. No inference has run yet.** The [deployment record](../../research/performance-a-v1-deployment.json) owns current provider state and scheduling. Root authorized execution when a real slot frees after the already scheduled warm experiment; operations owns submission. Do not repeat dataset creation or the no-run save. The eventual A2V shots are V2-21, V2-22, V2-36 and V2-38; this pilot tests only V2-36 and V2-21, in that order. Other shots remain I2V.

[Plan](plan-v1.json), [staging record](staging-v1.json), [local validation](local-validation-v1.json), [test log](offline-tests.log) and [download-verifier self-check](download-verifier-self-check.json) distinguish completed local checks from untested hardware and creative results.

## Frozen package

| Item | Value |
| --- | --- |
| Bundle | `build/jml-story-v2-performance-a-private-v1` |
| Notebook directory | `build/jml-story-v2-performance-a-private-v1-kernel` |
| Archive | `build/jml-story-v2-performance-a-private-v1.zip` |
| Package-lock SHA-256 | `71db95c5228bc827bcd7159e43ab44bf7a43a272b2442a66a973dc9796d7d2fe` |
| Archive SHA-256 | `ccec074caf9b54dcd0c94ca6340e52d66ddad4614f9638574ee411e5a73d58ea` |
| Locked files | 32 |
| Private dataset | `darionalis/jml-story-v2-performance-a-inputs` |
| Actual private notebook | `darionalis/join-me-in-life-v2-private-song-performance-tests` |
| Verified no-run version | 1 |
| Originally requested notebook ID, not created under this ID | `darionalis/jml-story-v2-performance-a` |
| Fixed generation | Two fresh serial children, one seed-49 take each, 896×512 at 24 fps, eight steps |
| Caps | Provider 5,400 seconds; bootstrap 5,390 seconds; zero automatic retries |
| New cash spent | €0 |

The exact neural runtime, backend archive, model pins, patches and dependency requirements are unchanged from `full-film/tools/kaggle-performance23`. The existing `kaggle-performance23` and `kaggle-a2v` directories are untouched. This adapter freezes two new manifests, adds their source/audio validation, permits their exact codec frame counts and isolates output/cache paths. It retains the proven sequential Gemma release, full-audio conditioning math and fresh-child execution. No warm-cache optimization is adopted here.

Kaggle derived the actual notebook slug from its title. Operations preserved that notebook and reconciled only the separate local notebook directory's `kernel-metadata.json` ID. The 32-file bundle, archive, package lock, manifests and notebook code are unchanged. The requested ID in the historical plan is not the current deployment target.

## Exact reviewed start images and source audio

Paths below are relative to `productions/join-me-in-life/full-film/revision-2`. Both 828×464 input PNGs are byte-identical copies of the independently inspected native crops, not regenerated or enlarged substitutes. The existing runtime fits them to 896×512 with preserved aspect ratio. Review JSONs and exact selected panel records travel in the locked bundle.

| Take | Start PNG | SHA-256 | Independent review |
| --- | --- | --- | --- |
| V2-36 | `assets/scene-inputs/animatic-v2/V2-36-before-GUIDE-18-v1.png` | `34c94fd9bdc4194911559a7de03823ad08f36ed44e0f41cd8b2fe46f15017996` | `review/guide-18-v1-static-review.json`, bottom-left panel, selected V2-36 pair |
| V2-21 | `assets/scene-inputs/animatic-v2/V2-21-before-guide-11-v2.png` | `c162c49c81f840ef55179bd27930b94a96811bde2994ec5eeb8f8c96fb6384bf` | `review/guide-11-v2-static-review.json`, top-left panel, selected V2-21 pair |

Both verdicts are `PASS_STATIC_SOURCE_FOR_BOUNDED_MOTION_TEST`; they do not approve animation. A2V receives the first image only. There is no last-image or intermediate-image input in this wrapper, so the planned after pose is not asserted as enforced.

The independent [production-input adoption](../../review/pilot-performance-production-input-adoption-v1.json) additionally binds these exact production PNG bytes to the inspected native crops. It is a separate deployment gate and does not alter the frozen package or approve motion.

Original audio is `productions/join-me-in-life/full-song/track-49.mp3`, SHA-256 `0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb`. Decode once to native 48 kHz stereo PCM16 and take the exact sample intervals below. Each picture frame covers 2,000 source samples. Intervals are zero-based, end-exclusive; six head frames place the first edited frame at the intended song position.

| Take | Raw frames | Edited timeline frames | Keeper in raw take | Head/tail | Original source frame / time | Source samples | Sample count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V2-36 | 97 | [4989, 5070) | [6, 87) | 6 / 10 | 4983 / 207.625 s | [9,966,000, 10,160,000) | 194,000 |
| V2-21 | 121 | [2838, 2940) | [6, 108) | 6 / 13 | 2832 / 118.000 s | [5,664,000, 5,906,000) | 242,000 |

No retiming, invented silence, amplitude change or padding is permitted. The proven model's internal stereo-to-mono mean remains unchanged; the review MKV carries the exact original stereo PCM. Model-produced audio is discarded. The final film must use the original master, with the planned keeper intervals.

The 121-frame take exceeds the previous actual A2V proof of 105 frames. Its encoder must produce at least **126 audio latent frames**, at strength 1.0 with full coverage. V2-36 requires **101**. Local tests execute the real coverage guard with CPU tensors; they cannot prove the real encoder output or GPU memory fit. Hardware must retain the exact 121 frames and complete samples, finish within the shared cap, release Gemma before video components, and preserve two-GPU memory evidence. Any short encode, OOM or timeout is a failed test, not permission to shorten, pad, change gain or retry.

## Completed local validation

Ten offline tests passed. They verify exact source samples and reviewed image bytes; reject altered manifests, handles and extra image conditioning; compare the engine byte-for-byte and process functions by AST; exercise the actual 97/121-frame audio guard; check runtime argument forwarding; encode and fully decode both lengths with lossless original PCM; run two real serial fixture children with a preserved first-child failure and no retry; verify every archive member; and demonstrate CPU preflight failure before weight download.

The download verifier was separately checked against retained actual S046 GPU output and temporary corrupted copies. It does not use that older take as proof of either new performance.

Reproduce locally from the repository root, without adding bytecode to the frozen upload directory:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv-ltx-cpu/bin/python -m unittest discover \
  -s productions/join-me-in-life/full-film/revision-2/tools/performance \
  -p 'test_*.py' -v
```

## Operations runbook: preserve the verified deployment, then run once

Private dataset creation, no-run save and actual remote readback are complete. Evidence is retained in `build/jml-story-v2-performance-a-remote-evidence-v1`. Readback verified actual dataset/notebook privacy, all 32 locked files, decoded source archive, normalized notebook cells, only the expected attached dataset, pinned container and dual-T4 settings. A no-run `COMPLETE` status means saved, not generated. Recheck the retained readback locally with:

```sh
python3 -B tools/kaggle_verify_bundle.py \
  --bundle build/jml-story-v2-performance-a-private-v1 \
  --evidence build/jml-story-v2-performance-a-remote-evidence-v1 \
  --expected-lock 71db95c5228bc827bcd7159e43ab44bf7a43a272b2442a66a973dc9796d7d2fe \
  --notebook-version 1
```

Keep existing jobs intact and count unrelated work against the provider's two-session limit. Read the deployment record before any remote action. Do not create another dataset or notebook for this candidate. If new remote readback is needed, pull `darionalis/join-me-in-life-v2-private-song-performance-tests/1` into a fresh evidence directory and preserve the original evidence.

Future local reconstruction must also read `kernel_id` and `no_run_version` from the deployment record. `prepare_bundle.py` and the immutable historical plan reproduce the originally requested ID; do not use that ID to deploy again. When reconstructing missing notebook transport metadata, reconcile its `id` to the actual deployment ID before verification or submission, preserving code and all frozen bundle bytes. Future unrelated candidates should choose matching notebook titles and IDs from the start.

Root has authorized this pilot after warm, when a real slot frees. Operations must first confirm the reconciled local `kernel-metadata.json` targets `darionalis/join-me-in-life-v2-private-song-performance-tests` and that no execution was already submitted. Then the only execution command is:

```sh
/workspace/.tools/jml-kaggle/bin/kaggle kernels push \
  -p build/jml-story-v2-performance-a-private-v1-kernel \
  --accelerator NvidiaTeslaT4 -t 5400
```

The provider cap is **90 minutes**, not the older pilots' 5,700-second value. The inner 5,390 seconds include setup, downloads and both takes. Each take runs in a fresh process; only installed dependencies and disk weights are shared. An ordinary first-child failure remains separate and permits the distinct second take within the same deadline. A timeout stops the child process group and marks remaining work not started. No automatic retries or resubmissions are allowed. A CLI exit code 0 accompanied by `Maximum batch GPU session count of 2 reached` is an admission failure, not a queued run. Record the actual submitted version and verify its cells/settings again.

## Downloaded evidence and acceptance

Expected GPU output root: **`/kaggle/working/jml-v2-performance-a-results`**. Local retrieval must preserve this root as the `--results` directory, containing `job.json` and the two take directories directly. Runtime cache is `/tmp/jml-v2-performance-a-runtime`.

```text
jml-v2-performance-a-results/
  job.json
  bootstrap.log
  V2-36/
    runner.log
    render.json
    environment.json
    patches-applied.json
    model-lock.json
    input-fitted.png
    video-silent.mp4
    review-original-audio.mkv
  V2-21/
    (same evidence when reached and completed)
```

Failed takes preserve `failure.json`, `runner.log` and any available `render.json`; early failures may not have later-stage files. Retrieve all evidence into a fresh local directory. Then run:

```sh
python3 -B productions/join-me-in-life/full-film/revision-2/tools/performance/verify_download.py \
  --bundle build/jml-story-v2-performance-a-private-v1 \
  --results build/jml-story-v2-performance-a-output-v1/jml-v2-performance-a-results \
  --expected-lock 71db95c5228bc827bcd7159e43ab44bf7a43a272b2442a66a973dc9796d7d2fe \
  --report build/jml-story-v2-performance-a-output-v1/technical-verification.json
```

The verifier binds returned manifests, fitted guide pixels, model pins, actual full-audio coverage and memory/residency records. It fully decodes both video containers at exact frame counts and proves review PCM equals supplied original stereo samples. A full technical pass still requires independent normal-speed performance and cut review.

For V2-36, hear the actual first scream onset with the six-frame offset: it must start full force, carry frightened pleading, and preserve coherent jaw/neck, right hand, microphone and cable. For V2-21, inspect the playful mouthing and reciprocal reaction, stable shared earbud ownership, hands and seated body grounding. Judge both the entire raw take and planned keeper at song speed; check the neighboring cut before acceptance. Do not treat exact PCM or distinct frames as proof of believable movement or phoneme alignment. These two shots alone do not establish the rehearsed-final-part setup, all four pleas or complete-film acceptance.
