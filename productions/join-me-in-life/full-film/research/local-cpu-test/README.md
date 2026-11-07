# Owned CPU LTX experiment — 6 November 2026

This experiment tests a real no-API, no-GPU route, rather than assuming that local video generation cannot work on the available machine. It uses Lightricks' smaller **LTX-Video 2B 0.9.6 distilled** checkpoint. This is not the larger LTX-2.5 model used in the separate free hosted test.

## Outcome and scope

The initial 384×256, 49-frame generation completed in **207.2 seconds**, using at most **6.85 GiB RSS**. However, its picture collapsed into noise and was rejected by two independent reviewers. Investigation found an exact, reproducible scheduler sign mismatch in this combination of Diffusers pipeline and stochastic sampling. A separate VAE round trip reconstructs the input woman correctly (mean absolute error 5.44/255). The checkpoint SHA256 matches the official object. This rejects the first configuration, not CPU inference in general.

A corrected retake is saved separately under `corrected49/`. It completed in **208.7 seconds**, peaking at **6.81 GiB RSS**. All 49 frames are coherent and the full file decodes successfully. However, movement is extremely restrained, close to a still: this is a coherent quiet-insert method test, **not proof of useful narrative acting or a production approval**. All frames differ, but mean consecutive pixel change is only 0.096/255; pixel change alone is not a motion-quality metric. The independent reviewer sees a slight early upper-eyelid/gaze opening and then a hold, without a convincing complete blink, breath, or hair action. They also identified that this prototype directly resized the 546×306 source to 384×256, squeezing its horizontal proportions about 16% relative to its vertical proportions. The next 512×288 sample preserves the source aspect ratio to within its pixel rounding. The initial rejected result remains preserved for comparison. Do not use the first MP4 in production.

The **512×288/73-frame** performance sample in `representative73/` completed in **421.13 seconds** and peaked at **7.23 GiB RSS**. All 73 frames decode; aspect ratio is correct. It shows substantial coherent head movement, turning from profile toward a more frontal lowered gaze. **The independent reviewer rejects this full-frame shot:** the glass reflection stays close to the original side profile while the real head turns, with a clear mismatch by 1–3 seconds; the requested fixed pose is also not held, and facial detail simplifies. Its 3.042 seconds of output establish meaningful local-motion feasibility and practical CPU throughput, not production approval.

The explicit **eye/chin-lift action test** in `action73/` completed in **419.22 seconds**, with a **7.25 GiB** peak. A separately encoded prompt asks her to lift her eyes toward the upper-left window, then raise her chin about five degrees and settle. The output makes a real chin lift and a substantial turn, but turns toward the camera/right rather than the window; the reflection remains downcast and no longer matches. **This full-frame shot is rejected for direction and reflection mismatch.** It passes full decode and the requested 512×288, 73 frames, 24 fps, 3.041667-second checks. This is executable, coherent local motion, but not reliable text-directed acting for this shot. No production batch has started. The next justified experiment is an authored start/end pose pair without a visible face reflection, not more blind prompt retries.

At this measured 512×288 throughput, a hypothetical uninterrupted 277.776 seconds of unique footage would require about **10.7 CPU wall-clock hours per film** for one take, before rejected takes, editing, and any extra text encodes. Ten films would be about **107 hours** for one take each, or about **321 hours** at three takes per accepted segment. This is an arithmetic extrapolation from one shot, not a proven rendering schedule or a promise of suitable quality. Higher resolution will cost more time; upscaling this output does not make it native HD.

## Source and configuration

- Checkpoint: `Lightricks/LTX-Video/ltxv-2b-0.9.6-distilled-04-25.safetensors`, 6,340,744,028 bytes; SHA256 `94891bd4bd08de30d484befbfc54fdcffe6d1596a131baad700b9baa5e1de86b`.
- Model/config Hub revisions are recorded in `model-provenance.json` and pinned in the preparation script.
- [Official distilled configuration](https://github.com/Lightricks/LTX-Video/blob/50f0aef1297574a4b29acbdb874e3a363a6d5f2e/configs/ltxv-2b-0.9.6-distilled.yaml): eight distilled steps, guidance 1, no STG, BF16, stochastic sampling, decode timestep 0.05, decode noise scale 0.025.
- Exact checkpoint schedule: `[1, .9937, .9875, .9812, .975, .9094, .725, .4219]`; no timestep shifting. `scheduler-validation.json` checks the actual installed scheduler sigmas against this schedule.
- [Diffusers LTX documentation](https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/ltx_video.md) supplies the single-file pipeline route. The measured CPU runtime here is our evidence, not a vendor performance promise.
- T5 text encoder and tokenizer come from the official `Lightricks/LTX-Video-0.9.5` Diffusers repository. Its FP32 T5 shards were individually converted to BF16 locally, deleting each temporary original after a successful conversion. The final T5 cache is about 9.53 GB.
- The checkpoint uses the **LTXV Open Weights License**, April 17, 2025. Its royalty-free grant covers entities below $10m annual revenue, subject to the license conditions. Attachment A(e) requires an express, intelligible disclosure of machine-generated content. This is not an Apache-license claim. A local extracted copy is `build/ltx-cpu/LICENSE-LTX-2B-distilled.txt`.

## Scheduler correction, with checks

Diffusers 0.42.1 `LTXConditionPipeline` passes **negative** model velocity to `FlowMatchEulerDiscreteScheduler.step()` with per-token timesteps. The scheduler's deterministic per-token branch has `dt = current_sigma - next_sigma`, so that convention is appropriate there. Its stochastic branch instead computes `x0 = sample - current_sigma * model_output`; using the negated velocity reverses the denoising direction.

The [native Lightricks RF scheduler, lines 363–369](https://github.com/Lightricks/LTX-Video/blob/50f0aef1297574a4b29acbdb874e3a363a6d5f2e/ltx_video/schedulers/rf.py#L363) computes `x0 = sample - sigma * velocity`, then `(1 - next_sigma) * x0 + next_sigma * noise`. Source excerpts and the official configuration are preserved in `official-reference.json`.

Our owned subclass, `tools/ltx_cpu_scheduler.py`, corrects the input sign **only** for the affected stochastic per-token path. It first probes the installed base scheduler: a future already-correct implementation is left alone; unexpected behavior fails explicitly. No installed package is patched.

`scheduler-sign-test.json` records:

- Exact terminal case: sample 2, velocity 0.5, sigma .4219 gives native x0 **1.78905**; unmodified scheduler gives **2.21095**; subclass gives **1.78905**.
- Deterministic per-token behavior remains correct.
- Scalar stochastic behavior remains correct.
- A zero-sigma conditioned token remains unchanged.
- A non-terminal mixed-token stochastic step matches the reference equation with **zero maximum absolute error**, using matched random noise.

`vae-input.png`, `vae-roundtrip.png`, and `vae-roundtrip.json` independently check the image codec and finite prompt embeddings before the retake. The generic Diffusers warning about timesteps without sigmas is not the cause here: shift 1 with dynamic shifting disabled is the identity, and the saved schedule comparison differs only by float32 rounding (under 5×10⁻⁸).

## Hardware, resource controls, and reproducibility

The machine has five logical CPU cores, 17.59 GiB RAM, AVX512 BF16 support, and no GPU. Inference uses four threads, leaving a core available to the user's browser work. Separate text and video processes unload T5 before loading the video model. A watchdog stops a stage if RSS exceeds 13.5 GiB, system available memory drops below 2 GiB, or the stage exceeds its configured time cap (900 seconds by default). Downloads preserve at least 4 GiB disk headroom.

Technical video checks decode every frame and compare the actual dimensions, frame count, frame rate and duration. Visual judgments here come from sequential inspection of all frames and full-size comparison sheets, with a second independent reviewer. They do not claim an additional normal-speed player viewing.

The text stage completed in **21.16 seconds**, peaking at **9.07 GiB RSS**. Package versions are preserved in `requirements-observed.txt` (Python 3.12.14, CPU Torch 2.15.0, Diffusers 0.42.1, Transformers 5.22.2). `protobuf` and `sentencepiece` are needed for the official T5 tokenizer.

From repository root, the isolated environment is `.venv-ltx-cpu`, model cache is `build/ltx-cpu/`, and the reusable code is `productions/join-me-in-life/full-film/tools/ltx_cpu_*.py`. The environment and large cache stay ignored by Git.

```bash
python -m venv .venv-ltx-cpu
.venv-ltx-cpu/bin/pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
.venv-ltx-cpu/bin/pip install diffusers==0.42.1 transformers==5.22.2 accelerate==1.15.0 safetensors==0.8.0 sentencepiece==0.2.3 protobuf==7.36.2 pillow==13.0.0 numpy==2.5.4 imageio==2.38.1 imageio-ffmpeg==0.8.1 psutil==7.2.2
.venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/ltx_cpu_prepare.py
.venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/ltx_cpu_benchmark.py --stage text --output-dir build/ltx-cpu/my-test
.venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/ltx_cpu_benchmark.py --stage video --output-dir build/ltx-cpu/my-test --width 512 --height 288 --frames 73
```

The commands above are recovery instructions for the tested package versions, not a second installation performed during this run. The preparation script pins model revisions and validates the final checkpoint hash. To use another prompt/image, provide `--prompt-file` to the text stage and `--image` to the video stage; keep the same output directory for both stages. Text-stage and video-stage processes must run sequentially, not in parallel. The current wrapper rejects aspect-ratio changes over 1.5% before loading the model. Reproducing the historical distorted 384×256 technical test now requires the explicit `--allow-aspect-change` flag. Dimensions must be multiples of 32, and frame count must be 8n+1.

All corrected runs seed both the initial-latent generator and Torch's global CPU RNG, because this version of the pipeline does not forward its generator to the stochastic scheduler. The first rejected run seeded only the initial latents; its stochastic random noise was not reproducibly seeded. Retake comparisons are therefore not a same-noise A/B test, while the isolated scheduler equation checks are deterministic.

No API token, signup, paid credits, GPU rental, or provider quota is used by this local route. Electricity and whatever hosting cost is already paid still exist; zero additional charge is not a promise of zero resource consumption. Final production suitability depends on the corrected video review and a larger representative benchmark, not on successful completion alone.

## A controlled successor, if motion direction fails

The [official Diffusers LTXConditionPipeline API](https://github.com/huggingface/diffusers/blob/v0.42.1/src/diffusers/pipelines/ltx/pipeline_ltx_condition.py#L95) exposes `LTXVideoCondition(image=..., frame_index=..., strength=...)` and accepts multiple conditions. Therefore an authored start pose and end pose can, in principle, constrain direction within the same three-tool workflow (image generation → LTX → FFmpeg). This capability has **not yet been benchmarked with this distilled checkpoint**; it is a justified next experiment, not a success claim. A source without a visible face reflection would also isolate acting quality from the independently observed reflection failure.
