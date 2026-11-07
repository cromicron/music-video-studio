# Private Kaggle LTX pilot — ready for one remote test

Updated 7 November 2026. The package and offline checks are complete. **GPU model loading and generated movement remain untested.** Root owns uploads, privacy verification, quota reads and execution; this agent made no provider calls or remote submissions during this implementation pass.

## Default job and boundaries

`private-pilot.ipynb` runs **one** representative bridge gesture: `S044_bridge_pilot`, seed 49, 864×480, 121 frames at 30 fps (4.033 seconds), authored start/end images. It does not run the window shot or a film batch. `pilot-suite.json` separately retains two candidate shots × three seeds for explicit follow-up after review; the notebook reads only the one-take `pilot.json`.

The runner accepts other explicitly hashed image/start-end pairs and shot IDs. A later hospital contact→pull→held sequence can therefore have its own manifest. This is not approval to replace its continuous emotional action with disconnected poses or looped footage.

- Private notebook metadata and private input manifest; no public server, Gradio, NIM, account API, paid endpoint, token lookup, LoRA, automatic retry or silent shortening.
- Official ungated `Lightricks/LTX-Video-0.9.8-13B-distilled`, revision `7c64400e1861cc0d7b98d570a1926d5408ec60cd`. Exactly 22 allowlisted files, **47,629,366,835 bytes**, with official expected SHA256s. The duplicate model tree under `vae/` is excluded.
- NF4 weights with FP16 compute. T5 encodes on GPU1 and unloads; transformer runs on GPU0; the VAE encodes on GPU0 and decodes on GPU1. The cards are separate memory spaces.
- Managed Kaggle CUDA Torch is retained. `bootstrap.py` creates a system-site-packages venv **with `--without-pip`** under `/tmp`, probes the managed host pip’s `--python <target>` support, then installs through that mode. It constrains installed Torch/CUDA packages to their existing versions, and pins the added model packages. No alternate Torch install is requested.
- Before downloading weights, preflight requires **exactly two T4s**, ≥14 GiB total and ≥12 GiB currently free on each, imports the actual LTX/T5 model classes, and runs a real tiny NF4 operation on **both** devices. It requires ≥10 GiB available host RAM and ≥2 GiB output disk headroom.
- Fresh model download requires **47.63 GB plus 4 GiB reserve** (~51.92 GB free), after environment installation. Weights and disabled-size Xet chunk cache remain under `/tmp`; only small results/logs are saved under `/kaggle/working` (Kaggle saves at most 20 GB there).
- Bootstrap enforces **5,400 seconds / 90 minutes total**, including setup, downloads, loading and rendering. It terminates and reaps the child process group on timeout; FFmpeg is kept in that group. The deployment command adds a **5,700-second / 95-minute provider session cap**. This bounds quota exposure; it is not a runtime estimate.
- Errors, OOM, bad hashes or wrong frame counts stop the job. Finished output remains `acceptance: unreviewed`. Re-running the same completed manifest verifies its video hash and skips inference; changed inputs/settings fail instead of replacing evidence. Failed/interrupted records are preserved on explicit retry.

Root previously verified two Tesla T4 cards (~15 GiB each), Python 3.13.16, Torch 2.11.0+cu130 and CUDA 13.0, then stopped the hardware-check session. Actual model load/generation time and accepted footage per GPU hour are not yet measured. Creator timing in the research report is not our benchmark.

## Observed remote failure and v3 repair

Root's actual notebook version 2 failed during environment creation after **1.192 bootstrap seconds**, before dependency installation, NF4 preflight, weights or model generation. `venv` reported its automatic `ensurepip --upgrade --default-pip` subprocess exited with status 1; the inner reason was not exposed. Evidence is preserved at `build/jml-kaggle-private-pilot-results-v2/jml-ltx-results/{bootstrap.log,job.json}` and the parent kernel log. Allocated GPU-session time is a separate quota cost recorded by root; failure before inference does not mean the session consumed no quota.

V3 bypasses only the failed automatic pip seeding. It uses standard `venv --without-pip --system-site-packages`, then the host pip’s supported `--python` mode (available since pip 22.3). A real `--python <target> --version` probe runs before dependency installation, so an absent/unsupported host pip produces a concrete early failure. The same managed-Torch constraints, post-install Torch/CUDA verification, private scope, one-take limit and deadlines remain. The new setup path passes local regression tests; **it has not yet succeeded on Kaggle**. No remote retry was launched by this agent.

## Files

- `ltx_kaggle.py`: bounded runner, manifest/source verification, deterministic distilled schedule, quantized loading, explicit GPU1 decode, provenance and full export validation.
- `bootstrap.py`: managed-Torch preservation, isolated added dependencies, whole-job deadline and process cleanup.
- `private-pilot.ipynb` + `kernel-metadata.json`: no-output private notebook, T4×2 selection, official observed Docker image digest, attached private input dataset.
- `prepare_bundle.py`: creates fresh local dataset directory/ZIP and a separate kernel upload directory. It never uploads anything. Inputs are flat to avoid ambiguous archive unpacking; no song, credentials or browser state is included.
- `requirements.txt`, `model-lock.json`, three `*-reference.json` configs, `NOTICE.md` and `LICENSE.creator.txt`: dependency/model provenance and source attribution.
- `test_pipeline.py`, `local-tests.log`, `local-validation.json`: offline checks and their actual environment/results.

The old `build/jml-kaggle-pilot-inputs.zip` is the frozen **stale** draft (SHA256 `4b82eaa838ba7e6ddbbb75c4a1f4eb42e71fed71d2f3f235032e3d90ee63479d`). Do not use it. Fresh staging for this implementation is `build/jml-kaggle-private-pilot-20261107-v3/` with companion `build/jml-kaggle-private-pilot-20261107-v3-kernel/`; its exact ZIP hash is in `local-validation.json`.

## Checks completed locally

**23 offline tests pass**, without model downloads or provider calls. They cover malformed/private manifests, source hashes and path escapes, blocked batch review bypass, corrupt/mismatched resume state, complete-take skipping before GPU setup, single-attempt failure handling, disk refusal before Hub access, exact anonymous download allowlisting and bad-hash rejection using mocks, CPU-runtime refusal, real timeout cleanup and command-failure propagation, notebook/private metadata, fresh package content, and the no-ensurepip setup path. The added regression test creates a real venv without local pip, installs a locally built wheel through host pip `--python` with indexes disabled, verifies installation is confined to the target environment, and confirms the host is unchanged. Unsupported host pip is separately tested to stop before installation.

Numerical checks compare chunked/full feed-forward output, deterministic per-token scheduler direction and fixed conditioning tokens, and the exact decode equation including latent scale and noise. Actual FFmpeg encoding and full decoding verify every frame's dimensions and timestamp; an intentionally short file is rejected. Image fitting preserves source proportions and bytes. The two prompts tokenize to 98 and 90 tokens using the cached T5 tokenizer, below the explicit 128-token cap.

Tests use the existing Python 3.12 CPU environment, with isolated **Diffusers 0.37.0 / Transformers 4.57.3** imports. They do **not** establish remote Python 3.13/CUDA13 integration or GPU quantization. The local bitsandbytes import emits an optional CPU GEMM-kernel warning; CPU quantized inference is not used in these tests. Exact installed local versions are recorded in `local-validation.json`.

Run the offline checks again from repository root, using the already installed local check packages:

```bash
PYTHONPATH=build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle/test_pipeline.py
```

## Exact root-owned deployment sequence

These commands are prepared instructions, **not actions already performed**. Use the existing authenticated CLI and existing private dataset; do not create another account, token or duplicate dataset. Read current free quota first. Never add `--public`. `--keep-tabular` preserves the JSON manifests/configs instead of converting them.

```bash
/workspace/.tools/jml-kaggle/bin/kaggle quota
/workspace/.tools/jml-kaggle/bin/kaggle datasets version --path build/jml-kaggle-private-pilot-20261107-v3 --message "Fix ensurepip bootstrap via managed host pip" --keep-tabular
/workspace/.tools/jml-kaggle/bin/kaggle kernels push --path build/jml-kaggle-private-pilot-20261107-v3-kernel --accelerator NvidiaTeslaT4 --no-run
```

Wait for dataset processing, then independently verify both the dataset and notebook are **Private**, and verify the intended dataset is attached. `--no-run` stages the notebook without spending GPU time. Do not infer remote visibility from the local manifest alone. V3 versions the same private dataset after the observed v2 bootstrap failure. Keep older versions and their failure logs; do not run the superseded bundle.

After those checks, root can execute the single bounded test and retrieve it:

```bash
/workspace/.tools/jml-kaggle/bin/kaggle kernels push --path build/jml-kaggle-private-pilot-20261107-v3-kernel --accelerator NvidiaTeslaT4 --timeout 5700
/workspace/.tools/jml-kaggle/bin/kaggle kernels status darionalis/join-me-in-life-ltx-private-pilot
/workspace/.tools/jml-kaggle/bin/kaggle kernels output darionalis/join-me-in-life-ltx-private-pilot --path build/jml-kaggle-private-pilot-results-v3
/workspace/.tools/jml-kaggle/bin/kaggle quota
```

The second push **runs** the notebook. Check the returned status/version; on a service error, do not blindly retry. Root must verify the job ended and record actual quota before/after. A committed batch runtime ends with the job; explicitly stop any separate interactive session. This code makes no account-side stop call. `/tmp` is ephemeral; preserve the downloaded working outputs before leaving the runtime. No cache upload or model dataset publication is needed.

The notebook has `PREFLIGHT_ONLY=False`. Setting it to true in a deliberately staged version runs dependency setup plus both-device NF4 validation without downloading weights or generating video. Normal execution already includes that preflight, so a separate preflight job is optional rather than required repeated setup.

Expected outputs: `job.json`, `bootstrap.log`, `runner.log`, `environment.json`, copied manifest/model lock, and `S044_bridge_pilot__seed-49/{render.json,video.mp4,image.png,end_image.png,decode.log}`. Early failure may produce only job/log evidence. No MP4 means no successful take. Model loading, both-device NF4, first/end conditioning and generation must still pass remotely.

## Review and continuation

Inspect full playback at normal speed and slower playback. Check all five fingers, rings, wrist rotation, shoulder support, microphone/mouth contact, distressed performance throughout, and identity/continuity between the source poses. The starting fingers have a documented occlusion risk; endpoints alone cannot prove the intervening motion. Record the exact usable interval, video SHA256 and independent review decision. Technical success is not acceptance.

Only an explicit reviewed pilot record can unlock the runner's `batch` mode. Neither source art nor the first generated take is automatically inserted into the film. The original full-film animatic, all earlier rejected tests and the Short's continuous embrace requirement remain separate evidence.

Source research: `../../research/free-gpu.md`; still review: `../../review/her-window-refined-review.md`; creator source/commit and official decode references: `NOTICE.md`. Root owns status/session/access/usage records and all provider operations.
