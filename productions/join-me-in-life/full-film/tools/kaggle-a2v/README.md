# One private supplied-song bridge diagnostic

Prepared 7 November 2026. **Local preparation is complete; no model inference or provider submission was performed by this implementation.** Root owns remote execution. This separate package implements the [researched pinned TeamAIQ LTX-2.3 Q4 A2V route](../../research/ltx-supplied-audio.md). It does not change the frozen 13B runner or hospital job. A successful diagnostic remains unreviewed and does not select a production model.

The frozen upload directory is `build/jml-kaggle-a2v-private-20261107-v4/`, with companion `-kernel/` and `.zip`. **Do not deploy earlier versions**: v1 predates the UTF-8 BOM correction; v2 has an overlong dataset title and requires upload-only metadata at runtime; Kaggle recursively expanded v3's source ZIP, removing the expected archive path. These remain preserved. V4 ZIP SHA-256 is `ab00a040140f8884f40afceeda7eb942735ba276d0f19288f6ff1ca21de8ce05`; its package-lock SHA-256 is `68a81b1fc3e3bb8b9a37b2a3734921cd4b05909618f7be4ec374c589f333ddbe`. [Exact local validation](local-validation.json) and [test log](local-tests.log).

## Fixed comparison

- Exactly one bridge take, **97 frames / 24 fps / 896×512 / seed 49**, two distilled stages, eight requested sampling steps, audio strength 1.0. No batch, retries, automatic resizing, shortened duration or alternate model.
- Original `bridge_plea_start_candidate.png`, SHA-256 `2fa46ef059bc3e0327c08b2252df5757140e92e97a1496f5cc5c1d9a4cba2840`. Native 1672×941 is contained without stretching or cropping inside the output. **First image only**; this adapted wrapper supplies no last-frame constraint.
- Exact supplied take49 excerpt, SHA-256 `f92120a9630041f5b9c93d0af749fce57344d9a74c5939c6a3cc3bd9cef1ab78`: stereo 48 kHz PCM16, 194,000 samples = 97/24 s, beginning at **207.75 s** / source sample 9,972,000. [Audio provenance](../../assets/audio/bridge-a2v-conditioning.json) records the untouched master hash and the 0.125 s handle before editorial S044.
- No new listening or phoneme verification is claimed. Prior ASR estimates are evidence limits, not lyric authority. The excerpt can include the following plea's onset. No silence padding, vocal separation, gain, retiming or fabricated phrase isolation.
- The model receives a mono mean of the supplied stereo waveform, as in the reference notebook. The review container keeps the **original stereo PCM**, and verifies decoded audio bytes equal the input. Returned model audio is discarded. The full master is not uploaded or changed.

The prompt asks for articulation matching the supplied performance, natural consonant closures/breath and one supported pleading gesture. It does not force a permanently open mouth. Face/chin stability, fingers/rings, grip, shoulder support, energy and actual song alignment still need independent review. Model, fps and first/end conditioning differ from the rejected 13B test, so this single diagnostic cannot isolate the causal contribution of supplied audio.

## Pinned implementation and early gates

[Source lock](source-lock.json) pins TeamAIQ notebook commit `04923c1446bc32f01e3649a526e3a8e19c5607a6` and WanGP backend commit `b8880bd5d292edfbe2384f5c951d95757ad59ea0`. The source-only ZIP contains 260 explicitly hashed source/config/notice files. The original notebook remains attribution/evidence; none of its public Gradio code or shell setup executes. [Licenses and adaptation notice](NOTICE.md).

[Patch specifications](patches.json) assert every target count against the pinned source. Eleven TeamAIQ source patches apply exactly once. Its additional `source.to(...bfloat16)` replacement is **absent at its own pinned backend commit**: this absence is asserted and recorded, not falsely reported as an applied patch. One owned patch replaces the actual `AudioConditionByLatentPrefix` fallback with a hard failure. The actual encoded audio must cover all target latents (approximately 101 here); a short result stops before diffusion. Extra encoded audio frames may be cropped to the exact requested span, as in the backend. Padding is never invented.

Runtime preserves the notebook's FP16/Q4 transformer on GPU0, BF16/Quanto-int8 Gemma on GPU1 with CPU token embeddings, FP32 video encoder/upsampler on GPU1, FP32 decoder and profile-4 offload. Gemma hidden states must remain BF16 to avoid overflowing feature-extractor RMS squares. RoPE and SDPA dtype alignment bind to both the function and actual Transformers dispatch. Missing device/precision patches and non-finite latent stages fail. VAE uses fixed 512-pixel tiles / 64-frame chunks with 64-pixel / 24-frame overlaps; the notebook's automatic OOM retry is removed.

Before large weights, the runner requires exactly two T4s, ≥14 GiB total / ≥12 GiB currently free on each, ≥20 GiB available host RAM, FFmpeg/FFprobe and ≥2 GiB output headroom. It imports the real backend classes and runs tiny **actual CUDA Q4_K/Q6_K, Quanto BF16/int8, and Gemma BF16/SDPA operations**. These GPU checks have been authored but have not run locally. Unsupported kernels, managed Torch/torchaudio mismatch or dependencies stop before the download.

The [weight lock](model-lock.json) pins `DeepBeepMeep/LTX-2` revision `1798f80b3340d2f87cffae42f9fa5367d0963d0c`: **18 files / 35,379,235,525 bytes**. This includes a 12,971,904,032-byte community Q4_K_M transformer and 13,210,647,730-byte converted Gemma, not the official unmodified checkpoint. Every file has an expected SHA-256/size from Hub metadata or retrieved small JSON metadata. Fresh cache needs **39,674,202,821 free bytes** including 4 GiB reserve; output headroom is separate. Weights stay under `/tmp`, not saved notebook output. Only this allowlist downloads, anonymously at the exact revision; subsequent implicit Hub access is disabled. No NIM/chat service, LoRA, new account or token is used.

The bootstrap copies the previously exercised `run_bounded`, `torch_constraints` and `install_environment` functions unchanged. It creates a **pipless system-site-packages venv**, uses managed host pip `--python`, and constrains managed Torch/CUDA packages. Its **90-minute whole-job deadline includes installation, downloads, loading and rendering**, and terminates/reaps the child process group. Root must also set the existing **95-minute provider limit**. A failed or completed attempt is preserved; no automatic overwrite or retry.

## Local validation and reproduction

**17 offline tests pass** on Python 3.12.14 / CPU Torch 2.15.0+cpu. Tests cover the one-private-job/input hashes/frame lattice, complete PCM coverage, exact source and dependency locks, patch target assertions, actual patched backend prefix rejection/full-span acceptance, source compilation, CUDA refusal before weights, disk refusal before Hub access, exact anonymous download allowlisting with synthetic data, preserved bootstrap functions, real timeout/exit handling, private outputless notebook, and actual 97-frame FFmpeg encode/decode plus byte-identical stereo PCM mux. Actual CPU Q4_K/Q6_K operations match the independent NumPy GGUF dequantizer; tiny patched Gemma BF16/SDPA produces finite output. Optional CPU bitsandbytes/GPU-kernel warnings are retained in the log; CPU NF4 inference is not used.

```bash
PYTHONPATH=build/ltx-a2v-check-packages:build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle-a2v/test_pipeline.py
python3 productions/join-me-in-life/full-film/tools/kaggle-a2v/prepare_bundle.py --output build/jml-kaggle-a2v-private-NEW
python3 build/jml-kaggle-a2v-private-20261107-v4/run.py --manifest build/jml-kaggle-a2v-private-20261107-v4/pilot.json --validate-only
```

Use a new staging name; existing bundles are preserved. Root should inspect the exact hashes, read available free quota, version the existing **private** `jml-ltx-a2v-private-inputs` dataset, then update the existing `darionalis/join-me-in-life-private-supplied-song-diagnostic` notebook without running, verify privacy/input/hash/two-T4 settings, and submit this single bounded job. No provider action is performed by these local commands. Keep `vendor/` nested paths intact. No master song or credentials are in the bundle.

**Not yet proven:** Kaggle Python 3.13/CUDA13 dependency integration; actual GPU smoke checks; weight download/hash verification; loading 22B/Gemma within available RAM/VRAM; encoded audio latent coverage from this exact excerpt; two-stage generation and runtime/quota; believable singing/pleading/anatomy. The local tests do not substitute for any of these. If audio coverage fails, root can deliberately select a longer original-song tail from the same offset; do not pad or silently change this input. If CUDA/memory fails, diagnose the actual error while preserving this failed comparison.

Expected saved evidence is `/kaggle/working/jml-ltx-a2v-results/`: job/environment/patch/model/render records, fitted image, silent video and original-PCM review MKV. Record actual quota, cold/generation time, GPU peaks, source/output hashes and independent usable intervals. The complete film and final three-tool production route remain unfinished; this is one diagnostic with no accepted motion.

## V3 transport correction

The dataset title is now 38 characters; both dataset and notebook titles pass the provider’s 6–50-character limit. Kaggle consumes `dataset-metadata.json` without uploading it, so that transport file is excluded from runtime `package-lock.json`. The simulated mounted tree removes it and passes actual `run.py --validate-only`; all runtime source, dependencies and input hashes remain enforced. Repository-only `vendor/.gitignore` is also excluded from the upload bundle.

The exact 870,577-byte `vendor/wangp-source.zip` is intentionally trackable through the narrow local `!wangp-source.zip` exception; Git confirms it is not ignored and has no LFS filter. Its SHA-256 is `6b109a552a97ff5ba60d42084b5c6376c63df9b844e153e2ab050355d93c4f54`. Root still owns commit/push verification. V3's actual upload established that Kaggle recursively expands this archive, even inside a zipped vendor directory. It must not be launched.

## V4 archive transport correction

The staged directory carries only `vendor/wangp-source.zip.b64` (1,160,772 ASCII bytes, SHA-256 `6fc0e576cb46e5ae3eb7b1888c7190095766fde172adc9be570e5e7a8637bea5`). Runtime decodes with `base64.b64decode(..., validate=True)`, verifies the decoded bytes against the **unchanged canonical archive hash**, opens the ZIP in memory, then verifies all 260 source entries and exact patch assertions. Invalid Base64 and hash mismatches fail before extraction. No original vendor ZIP is staged. The simulated mounted tree omits upload metadata and successfully validates the job and prepares the backend; a separate test rejects corrupt transport bytes. V2/v3 frozen ZIP and package-lock hashes still match their records.

The kernel id targets the **existing** `darionalis/join-me-in-life-private-supplied-song-diagnostic` notebook, which Kaggle created from its title. Root must inspect the remote `vendor/wangp-source.zip.b64` path and bytes after versioning, then confirm the actual mounted tree before GPU execution. Local tests do not establish remote upload behavior. No new provider object, GPU job or accepted motion was produced by this correction.
