# Free GPU production route for Join Me in Life

**7 November execution update:** The owned Kaggle 13B route now ran on actual dual T4s: a 4.033-second take required 146.681 seconds of generation and 815.988 seconds including cold setup/download/loading; displayed quota moved 30.00→29.76 h. The take was rejected after detailed visual review, so accepted-seconds-per-hour is still zero. This proves runtime access, not a sustainable quality yield or ten-film budget. [Provenance](../assets/motion/ltx13b-bridge-pilot/render.json) · [review](../review/ltx13b-bridge-pilot-review.md). The dated research below retains its original assumptions.

Research date: **2026-11-06 UTC**. Read-only source/code review; no account created, notebook uploaded, GPU session started, or money spent. **Kaggle access and output quality on our shots are not yet verified.** Song duration: 277.776 seconds.

## Recommendation

Make a **private Kaggle T4×2 batch pipeline** the next substantial free-production experiment. It provides far more potential sustained rendering time than a few daily hosted clips. Benchmark one difficult close-up and one hand/body action with **LTX-Video 0.9.8 13B distilled** first; compare the same inputs with **LTX 2.5** before choosing the production model. Keep a pinned, reusable local controller, a shot manifest and per-shot outputs. Use existing storyboard art and FFmpeg for finishing. Do not treat a camera move over a still as evidence of successful character animation.

Choose quality from the actual comparison, not the newest model number. The 13B creator reports substantially faster T4 rendering; newer 2.5 has more promising current capabilities but slower community T4 results. Neither community notebook has saved execution outputs, so their timing claims are **creator reports, not our measurements**.

This can remain a three-tool production workflow: existing image/storyboard tool, one LTX generation pipeline running on Kaggle, and FFmpeg. Kaggle is the compute host; do not add another editing or generation service merely because it is connected.

## What access is actually needed

| Access | Required now? | Precise requirement |
|---|---|---|
| Kaggle free account | Yes, for this route | Sign in; complete **phone verification**; confirm Internet and **GPU T4×2** can actually be selected and inspect remaining quota. Account existence alone does not prove GPU availability. |
| Kaggle automation authorization | Yes, for unattended batches | Official CLI supports browser `kaggle auth login`, or a revocable API token. OAuth currently requests **`resources.admin:*`**, not a narrowly scoped read token. Review normal consent; keep credentials in the credential store, never notebook code or outputs. |
| Hugging Face account/token for 13B | **No mandatory account** | Official model API returned `gated:false`, `private:false`; anonymous `model_index.json` download returned HTTP 200. The reviewed notebook passes `token=None` when no token is present. Auth can improve download limits but is not required by this model's current access gate. |
| Hugging Face account/token for official LTX 2.5 | Yes, if choosing official gated downloads | Official `Lightricks/LTX-2.5` and `LTX-2.5-Diffusers` returned `gated:"auto"`. Accept the displayed access conditions and use a fine-grained token with only necessary read access. This is a **free account**, not PRO. |
| Hugging Face token for converted community 2.5 | Not mechanically required today | Reviewed notebooks use `DeepBeepMeep/LTX-2`, which returned `gated:false`, `private:false`. Their download calls have no token parameter. This does not waive model/encoder license obligations or establish equivalent provenance to an official checkpoint. |
| NVIDIA NIM account/key | **No** | Only an optional prompt enhancer in the 13B notebook. Our own shot prompts eliminate this dependency. Single-chunk generation does not need its planner. |
| Google account/Colab | Backup; useful if already paid | Inspect the existing plan and Colab compute balance. Current Google documentation says eligible **paid Google AI plans include Colab benefits automatically on the same account**; promotional Google One free trials do not. Do not purchase a redundant Colab subscription. |
| Vast/Runpod or any subscription | **No** for the free route | Only a separately authorized paid fallback after the free pilot and a fresh cost estimate. |

Sources: [Kaggle staff: phone verification](https://www.kaggle.com/discussions/product-feedback/268333), [official Kaggle authentication documentation](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md), [official OAuth implementation](https://github.com/Kaggle/kaggle-api/blob/fdc788faffe3f29ae317480325c44080a00a5434/src/kaggle/api/kaggle_api_extended.py#L1977), [HF fine-grained tokens](https://huggingface.co/docs/hub/security-tokens), [official Colab FAQ](https://research.google.com/colaboratory/faq.html).

## Free quota, sessions and storage

- Official Kaggle documentation publishes a **30-hour weekly GPU quota**, sometimes higher with resources/demand. The actual account quota and availability are the authority for scheduling. The T4 announcement explicitly says dual T4 and P100 environments share the same quota without a quota change: do **not** automatically halve the 30 hours because there are two cards.
- Kaggle's staff update increased CPU/GPU sessions from 9 to **12 hours**. A legacy tips page still says 9; use current account controls and conservative batches well below either limit. Plan 4–6-hour batches with resumable shot IDs; do not rely on one session completing an entire film.
- Only up to **20 GB of `/kaggle/working` output** is saved. Keep model weights in temporary storage after checking actual free space; save clips, prompts, seeds, measured timings and QA metadata in working outputs. Download each completed batch. `/tmp` downloads are lost when the runtime is replaced.
- The 13B code calculates approximately **49 GB** for fresh base weights, or 29 GB if its T5 encoder is reused. Its README's approximately 80 GB startup claim includes broader setup/cache use; neither fits in the 20 GB saved-output allowance. Do not assume a model downloaded into `/tmp` will survive the next session.
- A CPU setup session can prepare code/downloads where useful. Turn on the accelerator only when needed. Stop unused sessions explicitly; closing a browser alone can leave an interactive session consuming quota.

Sources: [Kaggle efficient GPU usage](https://www.kaggle.com/docs/efficient-gpu-usage), [T4×2 announcement](https://www.kaggle.com/discussions/product-feedback/361104), [12-hour staff update](https://www.kaggle.com/discussions/product-feedback/302908), [notebook specifications](https://www.kaggle.com/docs/notebooks). The public documents do not guarantee a GPU will be available when requested.

## Actual creator implementations reviewed

### Faster 13B route

Repository: [DamnKuldeep/ltxv-13b-distilled-free-gpu-pipeline](https://github.com/DamnKuldeep/ltxv-13b-distilled-free-gpu-pipeline), inspected commit `38f99fa7a1d52191d60a82ea07467e0de170a1f9`. Read all relevant configuration, loading, generation, OOM, saving and UI code without executing it.

- The implementation uses NF4 quantization, **FP16 compute on T4**, explicit placement across two GPUs, tiled VAE decoding and feed-forward chunking. Two 16 GB cards are not one unified 32 GB allocation. It uses seven distilled timesteps with guidance 1.0, not a costly full diffusion schedule.
- It supports image conditioning, which is necessary to preserve our art. Its creator reports **4–6 minutes per 10-second clip**, with 480p the safer production setting. Do not extrapolate that timing to every prompt or claim a measured benchmark.
- There are ten committed MP4 examples. `ffprobe` verified 832×480, 30 fps, lengths 5.10–14.97 seconds. Contact-sheet inspection of `Character_Walk.mp4` and `Train_window.mp4` shows coherent broad framing over time. This is only a limited visual check: the walking sample hides the feet, has changing facial/lighting details and visible embedded text marks; it cannot establish clean gait or watermark-free final quality. No real-time motion approval was performed.
- The notebook has **zero saved cell outputs**. Pin dependencies and model revisions before the pilot: it currently installs broad minimum versions and patches library internals.
- OOM handling silently reduces requested frame counts in 5% increments down to 70%; its extension logic only fills some large deficits. Therefore a successful return is **not proof of requested duration**. Compare actual decoded duration/frame count with the shot manifest.
- Default Gradio `share=True` creates a public endpoint. Remove that launch for private batch work. The hardcoded third-party Kaggle model cache is optional; prefer traceable official weights or a verified cache. Do not upload the song or storyboard into a public dataset.

### Newer 2.5/2.3 routes

| Candidate | What the inspected code actually does | Confidence and use |
|---|---|---|
| [jigs10/ltx-2.5-kaggle-wan2gp](https://github.com/jigs10/ltx-2.5-kaggle-wan2gp), commit `acb5fb33a9bc515efd07a878bef4895dc24c2e6a` | Clones Wan2GP, downloads a roughly 14 GB NVFP4 2.5 checkpoint and INT8 encoder to `/tmp`, launches `wgp.py --share`. | A real runnable notebook, but no saved execution outputs or committed generated examples. Creator reports about **15 minutes/5 seconds**, 30 minutes/10 seconds at 480p. T4 uses NVFP4 fallback kernels, not optimized native NVFP4. Remove public UI, pin code, benchmark before production. |
| [AIQUEST dual-T4 2.5 notebook](https://github.com/TeamAIQ/Colab-notebooks/blob/main/kaggle_notebooks/ltx-2-5-22b-distilled-video-generator.ipynb), repository commit `04923c1446bc32f01e3649a526e3a8e19c5607a6` | Wan2GP with a roughly 19.5 GB INT8 Convrot checkpoint, separate Gemma encoder/components, FP16 patches for T4, custom dual-device handling and Gradio. Default sample is 640×384/73 frames. | More extensive adaptation, but no saved execution outputs or reproducible timing in the inspected notebook. Many live-source text patches make it fragile. It calls converted third-party weights “official”; retain that provenance distinction. |
| [AIQUEST 2.3 multi-reference notebook](https://github.com/TeamAIQ/Colab-notebooks/blob/main/kaggle_notebooks/ltx-2-3-22b-msr-ref-distilled-1-1-kaggle.ipynb) | Wan2GP, quantization, LiconStudio MSR reference LoRA and component transfers to GPU1; Gradio plus optional public tunnel. | Interesting for character consistency, but additional LoRA licensing and compatibility checks are needed. No saved outputs. Not the shortest path to a reliable first pilot. |

The maintained [WanGP/Wan2GP project](https://github.com/deepbeepmeep/WanGP) supports current LTX 2.3/2.5 and low-memory operation. A model being supported by WanGP does not prove that a particular unpinned notebook, precision conversion or dual-T4 patch works today.

Model access API checks, all anonymous on the research date: [13B](https://huggingface.co/api/models/Lightricks/LTX-Video-0.9.8-13B-distilled), [2.3](https://huggingface.co/api/models/Lightricks/LTX-2.3), [2.5](https://huggingface.co/api/models/Lightricks/LTX-2.5), [2.5 Diffusers](https://huggingface.co/api/models/Lightricks/LTX-2.5-Diffusers), [community conversions](https://huggingface.co/api/models/DeepBeepMeep/LTX-2).

## Sustainable capacity calculation

These are planning scenarios, **not promises of acceptable footage**. Assume a 10-second source take contributes 8 usable seconds after trimming and an average of three takes produces one accepted clip:

| Route | One full 277.776-second film | Ten films | Cash |
|---|---:|---:|---:|
| 13B creator timing, 4–6 min per source take | 35 keepers ×3 takes =105 attempts; **7–10.5 session hours** | 1,050 attempts; **70–105 hours**, about 3–4 weekly 30h allocations before setup/retries | €0 incremental compute |
| 2.5 creator timing, 30 min per 10-second take | **52.5 session hours** | **525 hours**, about 18 weekly allocations before setup/retries | €0 incremental compute |
| 2.5 five-second sources, four-second keepers, 15 min per take | 70×3=210 attempts; **52.5 hours** | 2,100 attempts; **525 hours** | €0 incremental compute |

Add cold-start download/loading time each session and rejected shots beyond the assumed three takes. At 6 minutes/take the 13B full-film estimate nearly fills a 12h session before setup, so split it. The relevant measurement is **accepted source seconds per charged session hour**, not generation speed alone. If every action requires six attempts, those estimates double. Free access is renewable but capacity and completion dates are not guaranteed.

The 13B route is therefore a plausible sustainable way to make ten fully generated films inside the €20 **cash** ceiling over several weeks. It is not yet demonstrated to meet the user's movement-quality requirement. The paid alternatives and their separate cost constraints remain in [paid-budget.md](paid-budget.md); do not add their budgets together.

## Private automation and pilot acceptance

Official [Kaggle kernel documentation](https://github.com/Kaggle/kaggle-api/blob/main/docs/kernels.md) supports `kernels push`, `status`, `output` and `pull`. Push **runs the notebook by default**; `--no-run` saves only. Current docs explicitly map accelerator `NvidiaTeslaT4` to T4×2. [Metadata](https://github.com/Kaggle/kaggle-api/blob/main/docs/kernels_metadata.md) supports `is_private:true`, `enable_gpu:true`, `enable_internet:true`, `machine_shape:"NvidiaTeslaT4"`. Default privacy is true, but set it explicitly and verify it after upload. Attach only private source-art datasets. Keep all API/HF tokens out of code, metadata and printed exceptions; use Kaggle Secrets only when needed.

After access is authorized, the concrete next job is:

1. Read `kaggle quota`, device names, VRAM, RAM and temporary-disk space. Confirm the expected two cards and actual remaining quota.
2. Run **three seeds each** for two demanding storyboard shots at a modest resolution. Save inputs, exact revisions, prompts, frame counts, seed, load/generation time and actual quota before/after. Do not run a full film before these samples exist.
3. Decode every output; inspect full playback and slower playback for eye direction, mouth stability, hands, limb continuity, floor contact, body collisions and intended action. Compare start/middle/end with the source art. Contact sheets alone cannot approve movement.
4. Reject unintended head turns, identity changes or hand morphing even when the file technically succeeds. If 13B fails the difficult shots, benchmark 2.5 on those same inputs and measure its quality gain per hour.
5. Only then expand in short, resumable private batches. Download accepted footage and manifests, stop each session, assemble locally, and watch the whole final 277.776-second film with audio before approving it.

## Licenses and Colab fallback

The 13B notebook code is Apache-2.0, but the model uses Lightricks' [0.X open-weights license](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt). It permits royalty-free use subject to its restrictions; entities at or above $10m annual revenue need a commercial agreement for commercial use. LTX 2.5 has the separate [2.x community license](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x), also with a $10m threshold and further terms. Lightricks claims no general ownership of generated outputs under these licenses. Third-party style LoRAs and Gemma components have their own terms: omit unneeded LoRAs and retain provenance. Do not infer that a repository's Apache code license licenses every downloaded checkpoint or demonstration image.

Colab remains a useful backup or an existing-subscription resource, not a guaranteed free render farm. Its [official FAQ](https://research.google.com/colaboratory/faq.html) says free GPU resources and limits vary, with sessions up to 12 hours depending on availability. Free managed runtimes restrict bypassing the notebook UI to interact mainly through a separate web UI; a public Gradio generation server is therefore a poor fallback. Use direct notebook execution, obey actual account limits, and do not implement keepalive/limit bypasses. Check any included paid Google AI compute first; buying storage-only Google One does not buy GPU capacity.
