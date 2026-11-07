# Hospital and summer — separate next-pilot preparation

Prepared 7 November 2026. **This preparation submitted neither take and generated no motion.** These inputs preserve the [Short-to-full continuity findings](../../../review/short-to-full-continuity.md). Root owns provider/account work and has selected hospital as the next bounded capability comparison after the bridge rejection; summer remains prepared. The live [production status](../../../../STATUS.md) owns any later execution result. No batch or accepted-motion record is created here.

| One-take manifest | Native source(s) | Frames / 30 fps | First-to-last span | Encoded duration | Prompt tokens |
| --- | --- | --- | --- | --- | --- |
| [Hospital embrace](hospital-embrace.json) | Original M01 start + end | 241 | 8.000 s | 8.033333 s | 125 |
| [Summer exchange](summer-exchange.json) | Original M02 start only | 185 | 6.133333 s | 6.166667 s | 125 |

Each take uses seed 49 and 864×480. These are the smallest valid `8n+1` frame counts providing at least eight/six seconds at 30 fps. Output duration includes the final frame's exposure. No motion is shortened, slowed, repeated or reversed to meet the old cap. The hospital pilot does not cover all 12.125 s of S028; summer does not cover all 8.5 s of S025–S026.

## Source integrity and creative scope

All three original PNGs are **1916×1080**, copied unchanged into their separate staging directory. The existing runner fits them to 852×480 inside an 864×480 canvas, leaving six black pixels on each side. It does not crop hands or stretch faces. Actual generated frame-edge behaviour still requires review.

| Native file | Exact SHA-256 |
| --- | --- |
| M01_Embrace_Start.png | `259124c27ba71ae4785927457fda743f20a954e38b86ce19ce655866e408b64f` |
| M01_Embrace_End.png | `466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10` |
| M02_Summer_Start.png | `5177ac4a2ea53edebd977976ac3ceefbad77118bc9d5f3e33a723f7fcde4900e` |

Hospital retains his frightened concern for her, one right-arm reach, clear hand contact on her outer upper arm **before** one gentle torso pull, then held unresolved closeness. Her hands stay passive in her lap, gaze down-left/away, and both heads stay self-supported. The complete rejection list still covers high hand arcs, blurred/fused digits, detached ownership, penetration/sliding, cuts/resets, repeated reach/pull and emotional role reversal. Later hospital returns must preserve contact or motivate a change; this preparation does not edit those returns.

Summer starts with the original small smiles, then his brief playful mouthing/glance, her attention and laugh, his response and shared settling. Preserve identity, face proportions, summer wardrobe, rings, bracelets, shared earbud wires, hand positions and seated contact. His hand by his ear is intentional in the source. The old M02 end is expressly excluded because its facial drift is unapproved. Her playful memory response does not make her the lead singer or certify lyric synchronization.

Both prompts are **125 T5 tokens including EOS**, with no truncation. The locally cached tokenizer's four files match the official pinned model-lock hashes. Exact token IDs, source dimensions/hashes, staged-file hashes and runner checks are in [local validation](local-validation.json). Each manifest's `preparation` object records what the shorter prompt states explicitly, what it abbreviates, and the full binding review requirements. Timing guides are acting intentions, not model keyframe controls.

## Separate runner policy

The frozen v3 runner caps pilots at 153 frames; it correctly refuses these longer actions. [prepare.py](prepare.py) therefore copies the pinned existing runner into each new staging folder and changes **only `validate_manifest`**. The staged policy requires one shot, one explicit seed, exactly 864×480/30 fps, and exactly 241 frames for hospital or 185 for summer. Hospital requires an end image; summer forbids one. Batch mode, additional takes, other shot IDs and other durations fail. All original source-hash/privacy/path checks remain.

The copied bootstrap, inference, model lock, dependencies, scheduler, quantization, two-device preflight, process cleanup and deadlines remain unchanged. The frozen v3 directory/ZIP, original runner and current notebook are not modified. No dataset/notebook metadata, ZIP upload or deployment is created here. Staging is preparation, not authorization to replace the existing provider inputs.

The completed bridge run proves the actual Python 3.13/CUDA 13/two-T4 setup can load this model and render 121 frames. It does not prove the larger takes fit. Hospital uses 31 base temporal latents instead of 16, and summer uses 24; attention/activation memory cannot be inferred safely by multiplying the observed peak. Record actual runtime, GPU memory and quota for any later remote attempt. Keep the existing 90-minute process and 95-minute provider caps and stop on failure; do not silently shorten or retry.

## Reproduce and check locally

From the repository root, choose a **new** output path; the preparer refuses to overwrite existing staging:

```bash
PYTHONPATH=build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle/next-pilots/prepare.py --output build/jml-kaggle-next-pilots-20261107 --tokenizer build/ltx-cpu/config/tokenizer
PYTHONPATH=build/ltx-kaggle-check-packages .venv-ltx-cpu/bin/python productions/join-me-in-life/full-film/tools/kaggle/next-pilots/test_preparation.py
python3 build/jml-kaggle-next-pilots-20261107/hospital-embrace/ltx_kaggle.py --manifest build/jml-kaggle-next-pilots-20261107/hospital-embrace/pilot.json --validate-only
python3 build/jml-kaggle-next-pilots-20261107/summer-exchange/ltx_kaggle.py --manifest build/jml-kaggle-next-pilots-20261107/summer-exchange/pilot.json --validate-only
```

Existing staged inputs are in `build/jml-kaggle-next-pilots-20261107/hospital-embrace/` and `build/jml-kaggle-next-pilots-20261107/summer-exchange/`. Each contains its own `pilot.json`, exact native PNG(s), runtime source and license. Build artifacts are local/ignored; the committed templates and preparer recreate them from retained originals. A missing tokenizer/cache is a concrete prerequisite; this tool does not download one or any model weights.

**Nine focused tests pass**, and both actual runner `--validate-only` commands return one shot/one take. Checks cover frame/seed/batch limits, end-image selection, private/hash/path enforcement, fitting without modifying originals, refusal to overwrite staging, and an AST comparison proving that inference outside the validator is unchanged. [Exact test log](local-tests.log). Studio structure, original source review and whitespace checks also pass. No GPU inference or audiovisual review was performed by this preparation.

## Technical check of the completed bridge evidence

The separate [bridge render record](../../../assets/motion/ltx13b-bridge-pilot/render.json) has the expected runner/model/dependency hashes, seven deterministic steps and 121 fully decoded frames. Actual generation took 146.681 s; complete bootstrap/job took 815.988 s. Peak allocated memory was 11,512,751,104 bytes on GPU0 and 4,196,614,144 on GPU1; this is allocated memory, not a guarantee of future headroom. Root reports quota 30.00→29.76 hours.

The saved logs show no OOM, non-finite tensor or weight-hash failure. They do show deprecated API notices, a tiny NF4 smoke matrix lacking optimized dimensions, CUBLAS workspace clipped to the configured deterministic allocation, and pip conflicts involving unrelated managed environment packages. The tiny-matrix and workspace notices concern execution/performance; they do not establish the cause of reported hand/ring instability. No unquantized or alternative-conditioning comparison isolates model/quantization effects. The separate [independent bridge review](../../../review/ltx13b-bridge-pilot-review.md) rejects this tested take for finger/ring discontinuity and unmotivated mouth morphing/endpoint ghosting: **zero accepted seconds**. Recognizable identity and stable stage geometry do not override those failures. Hospital tests a different action with original paired sources; it is not an accepted model choice or production batch.

## What is still unfinished

The complete 277.776-second film remains an animatic. Full hospital contact/pull/aftermath, responsive summer exchange and screamed bridge movement must each pass independent identity/anatomy/contact/acting review at normal speed with the song, followed by exact usable intervals. The completed bridge is technically valid but rejected for production; zero generated acting seconds are accepted at this preparation handoff.

Next come the longer single-take execution/memory test, those motion reviews, final three-tool route selection, higher-resolution source review for the remaining small panels, full-song lyric/section listening checks, continuous aftermath edits and full-film animation/assembly/export review. The dawn ending remains a proposal. Merged-main memory recovery is already complete; automatic first-turn loading in a newly provisioned Cloud task remains a separate unproven check. No sign-in or phone-verification redo is needed.
