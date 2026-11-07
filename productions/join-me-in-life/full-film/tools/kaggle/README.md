# Unfinished private Kaggle pilot checkpoint

**Paused on 7 November 2026 at Dario's request to consolidate project history before more production. Do not treat this as an executed or production-ready notebook. No remote GPU job was started by this agent.**

## What is saved

- `ltx_kaggle.py`: draft private CLI for the researched LTX-Video 0.9.8 13B distilled route. It validates source hashes and pilot limits, defaults to one new take, stages NF4 text encoding on GPU1, unloads T5, places the NF4 transformer on GPU0, and moves tiled VAE decoding to GPU1. It records shot IDs, seeds, source/model/code hashes, timing, environment and technical validation. It does not auto-accept motion. There is no Gradio/public tunnel, NIM, account API, token lookup, purchase, LoRA or silent frame-count reduction.
- `prepare_bundle.py`: local-only packager for three reviewed-candidate source images, exact prompts, two pilot shots × three seeds, code and license notices. No song/audio is included. The output is intended for a **private** Kaggle input dataset; creating the local archive does not upload or establish remote privacy.
- `requirements.txt`: pinned added packages; intentionally preserves Kaggle's managed CUDA Torch. Proposed core versions: Diffusers 0.37.0, Transformers 4.57.3, Accelerate 1.12.0, bitsandbytes 0.49.1, Hub 0.36.0.
- `model-lock.json`: official ungated model revision `7c64400e1861cc0d7b98d570a1926d5408ec60cd`, 22 required files, **47,629,366,835 bytes**, expected sizes and SHA256s. A naive recursive snapshot also includes duplicated model components under `vae/` and totals approximately 92.8 GB; the draft allowlist excludes that duplicate tree. These are expected official hashes; the 13B weights have **not** been downloaded or verified locally.
- `scheduler-reference.json`, `transformer-reference.json`, `vae-reference.json`: official configs at that pinned revision.
- `NOTICE.md`, `LICENSE.creator.txt`: source attribution, Apache-2.0 creator license, separate model-license link, and differences from the audited creator code.

There is **no `.ipynb`, kernel metadata, environment bootstrap, completed test suite or final deployment handoff yet**. Work was paused before those were implemented. Do not upload the draft as though it were a completed notebook.

## Checks actually completed

1. The initial `ltx_kaggle.py` and `prepare_bundle.py` passed `python -m py_compile`. **Later edits adding the NF4 hardware smoke test, finite-embedding check, failed-attempt preservation and license packaging have not been rechecked.**
2. The initial packager successfully created `build/jml-kaggle-pilot-inputs/` and its approximately 5.6 MB ZIP. The manifest passed the runner's `--validate-only` check: two shots, six explicit seeds, existing input files and matching hashes. This was the positive path only; negative/resume/schema tests were not implemented.
3. Pinned Diffusers 0.37.0 and Transformers 4.57.3 successfully imported the actual LTX pipeline/model classes locally using the existing **CPU** Torch environment and isolated packages under `build/ltx-kaggle-check-packages/`. The tiling signature supports the selected spatial/temporal arguments; there is no built-in transformer feed-forward chunking method in this version. bitsandbytes emitted a warning about its optional missing **CPU** GEMM kernel package; CUDA/NF4 execution was not tested here.
4. Public package metadata was inspected for dependency constraints and Python support. The selected bitsandbytes wheel includes `libbitsandbytes_cuda130.so`. Its presence is **not** proof of working T4/CUDA13 quantization.
5. Read-only official-model inspection established ungated/public access, exact revision/configs, and expected file sizes/hashes. The saved model lock has all 22 hashes. No 13B weight download or GPU inference occurred.

**The existing `build/jml-kaggle-pilot-inputs.zip` is stale:** it predates the last source edits and license-copy fix. Its historical SHA256 is `4b82eaa838ba7e6ddbbb75c4a1f4eb42e71fed71d2f3f235032e3d90ee63479d`. Do not upload it as the current implementation. After resumption and review, regenerate into a new directory so the preserved draft is not overwritten.

## Untested stages and unresolved issues

- Root independently reported a successful private hardware probe: two Tesla T4 cards (~15 GiB each), Python 3.13.16, Torch 2.11.0+cu130, CUDA 13.0, Internet enabled. Root stopped that session. This agent's import checks ran on Python 3.12/CPU Torch and do not establish compatibility with the remote stack.
- A private notebook/bootstrap still needs to preserve the managed Torch build, install the pinned added packages in isolation, and run a tiny NF4 operation on both GPUs **before** the 47.63 GB download. The draft preflight contains this test, but it has not run.
- Actual temporary disk and host RAM capacity remain unmeasured for this workload. The draft requires missing model bytes plus 4 GiB disk reserve and at least 10 GiB available host RAM. Model caches belong under `/tmp`, not in saved `/kaggle/working` outputs. Kaggle's 20 GB saved-output limit still applies.
- Transformer NF4 loading, T5 FP16 stability, explicit device maps, chunked feed-forward equivalence, cross-GPU decode, first/end image conditioning, video export/full decode, OOM behavior and resume integrity need meaningful tests. No GPU performance or usable footage is established.
- The draft manually follows the pinned pipeline's latent denormalization and decode-noise interpolation. The official 13B scheduler is deterministic; the older CPU experiment's stochastic sign correction is deliberately not applied. These choices need numerical/structural checks before rendering.
- The session budget currently checks **between takes**, not a hard watchdog; downloads/loading and a running take can exceed it. No automatic Kaggle session shutdown exists. Root must bound and explicitly stop the remote session.
- The first positive manifest contains a window reflection and a bridge hand pose whose occluded fingers were not fully certified. Those are deliberate demanding tests, with known review risks. Technical completion cannot approve them. Full and slow playback, source comparison and an independent motion verdict remain required before any batch.
- No added cash charge, purchased credits or remote GPU quota was spent by this agent. Model download/loading and all failed takes will consume session time when root actually runs them. The previously researched 30-hour allowance and creator timing are not this implementation's measured cost/yield.

## Source evidence and ownership

Start with `../../research/free-gpu.md` and the independent still review at `../../review/her-window-refined-review.md`. Audited creator: `DamnKuldeep/ltxv-13b-distilled-free-gpu-pipeline`, commit `38f99fa7a1d52191d60a82ea07467e0de170a1f9`; its inspected checkout and extracted code are currently under `/tmp/jml-kaggle-ltx-review/`. The pinned official Diffusers decode source is linked in `NOTICE.md`. These temporary checkouts/packages are caches, not required portable source.

Root owns Kaggle OAuth, uploads, privacy verification, notebook pushes/runs, quota records and the production status/session/access logs. This agent changed only this new source directory plus ignored local build/check artifacts during this resumed subtask. Production is paused; the next action belongs to the continuity consolidation, not another render.
