# M02 face repair: bounded implementation contract

7 November 2026. **Do not build or launch a new repair engine now.** The official inpaint graph cannot be added faithfully as a small switch to the current Q4 A2V runner. Its logical GPU roles could be reused, but its model loading, guidance and stage handoff require a separate unvalidated path. Root's A2V v5 is still the active test; its source and all frozen packages remain unchanged. No masks, prototype engine, weights download or provider operation was made for this assessment.

The [independent M02 review](../review/m02-editor-second-review.md) supports retaining the original acting, seated support and hand contact, but finds sustained female blue-eye/rounder-face drift beginning in f13–24 and clearly visible by f21 / 0.833333 s. It persists through closed-mouth pauses and f121. Original source: 1916×1080, 121 frames, 24 fps, silent, SHA-256 `03d6eb4da452db9b21b3087edf97492d21517c215cf1c548bfe5a344d8fd70d3`. M01 now passes separately and needs no repair.

## Why an inpaint adapter alone is insufficient

The exact [official 2.3 graph](https://github.com/Lightricks/ComfyUI-LTXVideo/blob/220e1d45aa0469f518e982102fca4dca92a61862/example_workflows/2.3/LTX-2.3_ICLoRA_Inpaint_Two_Stage_Distilled.json) is pinned by SHA-256 `b4d002e2d15eb716654f234797b464daf8aa4f23261f30137ac16dfffdda42bd`.

| Contract | Official graph | Existing owned Q4 route |
| --- | --- | --- |
| Transformer/adapters | Dev + distilled-1.1 LoRA at **0.5** + in/outpainting-0.9 at **1.0** | Pre-distilled Q4; no active LoRA. It is not the same weighted model. |
| Samplers | `euler_ancestral_cfg_pp`, then `euler_cfg_pp`; 8 + 2 steps | `EulerDiffusionStep`; no CFG++ unconditional prediction path. |
| Intermediate state | Decode stage 1 → masked Laplacian blend → **Lanczos pixel resize ×2 → VAE re-encode** | Latent spatial upsampler; no intermediate decoded composite. |
| Source control | Green-mask source video, guide at reference scale 1, explicit blends | Temporal video guides and latent reinjection exist, but do not implement the graph above. |
| Text lifecycle | CFG++ needs unconditional denoising even at CFG 1 | V5 intentionally releases Gemma after one prompt encoding. A faithful repair controller must finish every needed text context first. |

The [CFG++ implementation](https://github.com/Comfy-Org/ComfyUI/blob/1332fabfcc507aa7c548cd5152071ed494c207e8/comfy/k_diffusion/sampling.py#L1334) explicitly sets `disable_cfg1_optimization=True` and consumes `uncond_denoised`. Replacing it with ordinary Euler would be a declared experiment, not a faithful port. Likewise, blending only after generation misses the first-stage source restoration.

## Exact dependency boundary

Keep WanGP `b8880bd5d292edfbe2384f5c951d95757ad59ea0`, the [existing pinned Python requirements](../tools/kaggle-a2v/requirements.txt), managed Torch/CUDA, and proven bootstrap. Relevant existing packages are mmgp **3.7.6**, optimum-quanto **0.2.7**, Transformers **4.57.1**, GGUF **0.17.1**, Diffusers **0.36.0**, Pillow **11.3.0** and SciPy **1.16.3**. In addition, a faithful port needs:

- Exact `vanish_nodes.py`, `iclora.py` / guide semantics and `pyramid_blending.py` from ComfyUI-LTXVideo **220e1d45aa0469f518e982102fca4dca92a61862**, plus the CFG++/model-sampling semantics from ComfyUI **1332fabfcc507aa7c548cd5152071ed494c207e8**. Preserve their licenses. These are substantial model/conditioning contracts, not standalone drop-in functions.
- **Kornia** for the official pyramid blend; upstream `requirements.txt` leaves its version unpinned. Select and test a specific lock before implementation. HDR-only colour-science/OpenImageIO and a prompt-enhancer model are unnecessary for this SDR repair.
- mmgp LoRA hooks declared for the transformer at offload setup, followed by checked `load_loras_into_model` and explicit multipliers; the current A2V profile declares no LoRA hooks. All keys/shapes and actual quantized LoRA arithmetic must be tested before a full model run.

At the already inspected converted-model revision **1798f80b3340d2f87cffae42f9fa5367d0963d0c**, the required additional/changed assets are:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `ltx-2.3-22b-dev_diffusion_model_quanto_int8.safetensors` | 19,447,662,547 | `5fc8d83656cdabf93b79bfb8799ee1c84c8270c59a49caccd4f8d1a27c77f6ec` |
| `ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | 7,605,507,256 | `f5d4953f3386197a4b4f5abdb17616ff256171e8075c111d6e7d2dfa6e823b3a` |
| `ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors` | 1,308,778,338 | `73dd0841c0d4f0eb26fb1f017781b841b2752021944ac5ecefe57917f6dae6b5` |

That metadata contains **no dev Q4 GGUF**. Dev-int8 is a potential T4 conversion of the correct base, not verified numerical equivalence to the official unquantized graph; its 19.45 GB plus two adapters changes host/offload pressure materially. The unquantized dev transformer is 37,987,776,376 bytes. NVFP4 is not the selected T4 route. Reusing the existing component files gives a potential **50,769,279,634-byte** int8-based asset set, before cache/output reserves. Disk size is not a VRAM estimate. The source-guidance sequence also adds transformer tokens, so A2V memory success would not certify repair memory. No new model is silently added to the diagnostic allowlist.

## Concrete future controller, if justified

Require a hashed 121-frame native source and **reviewed tracked face masks** at identical timing; no mask exists yet. Retain f1–12 and all black-mask pixels exactly. Design masks around the actual identity defects, protecting hair, earphones, his face, bodies, hands and the useful mouth/eyelid motion where possible. Painting the entire face green removes its original facial motion cues; the model cannot then guarantee the same laughter just because body motion remains. Iris recoloring alone leaves the proportion drift. Mask choice is therefore an editorial prerequisite, not an automatic rectangle.

The controller would encode all text contexts, release Gemma, apply the exact two adapters, run full-temporal green-mask conditioning, execute stage 1 with the official sigmas/CFG++ noise semantics, decode and blend, pixel-upscale/re-encode, then refine and blend again. Require exact sequence lengths throughout; disable shortest-input trimming. For this silent source, deliberately omit audio guidance rather than inventing silence. Finish with the generated region composited into native source frames under a finite approved boundary; compare every outside-region RGB pixel before delivery encoding. Preserve source fps, 121-frame chronology and the endpoint timing. Only independent normal-speed review could establish identity and acting inside the repaired region.

## Lower-risk next test already supported by our model

The pinned backend directly supports **first image with no supplied waveform**, using the same 18 weights and existing distilled samplers. In `LTX2.generate`, omit `input_waveform`; `audio_conditionings` remains `None`. This means **no supplied audio conditioning**, not an audio-free network: the normal joint pipeline still produces model audio, which the wrapper should discard while retaining the original music separately. The frozen A2V manifest/coverage guard intentionally rejects missing audio, so use a separate small I2V wrapper/manifest instead of weakening it.

Additional constraints already wired in [`ltx2.py:1079`](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/models/ltx2/ltx2.py#L1079):

- `image_start` replaces the initial latent in both stages.
- `image_end` adds a guiding image at **`frame_num - 1`** in both stages.
- `frames_to_inject` with matching `frames_relative_positions_list` adds intermediate guides in both stages. Despite the parameter name, these values are **integer pixel-frame indices**, not fractional percentages. Require equal lists and in-range, deliberately chosen positions; the backend otherwise silently uses the shorter list.

End/intermediate guides are attention conditioning, not a guarantee of pixel-identical poses or successful identity. They need no additional LoRA or sampler change, but are untested in our current wrapper. The uncorrected M02 endpoint already contains the rejected face and must not become the identity target. A separate first-image summer comparison is the smallest useful next test if A2V output establishes the underlying runtime and image quality. It is fresh generation, not source-preserving repair; compare its acting against original M02 before replacing anything.
