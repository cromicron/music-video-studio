# Experimental fixed-prompt warm batches

**Offline candidate only. No GPU test, new download, job submission or production promotion has occurred.** Existing four action pilots, the [production adapter](../production/README.md), standalone runtime and locked engine are unchanged. This directory is an optional throughput experiment, not a prerequisite for continuing the film.

The executable private H01/C01 experiment was staged locally; root/ops subsequently saved and verified its private no-run version 1. [Deployment record](../../research/warm-ab-v1-deployment.json) owns its current provider state and scheduling gate. [Hardware runbook](hardware-runbook.md) gives the frozen paths, complete verification commands, 90-minute provider cap and expected evidence. [Staging record](staging-v1.json) binds the exact candidate package and historical local preparation. No hardware result or production promotion is implied by the saved notebook.

## Feasibility finding

The pinned engine already caches **final video and audio conditioning tensors** in `TextEncoderCache`. Its distilled pipeline resolves the existing projection/connectors, runs `postprocess_text_embeddings(encode_text(...))`, then calls the cache once with `[prompt]` at the current NAG setting. It has a separate `precomputed_contexts` argument, but the public generation route wires that to HDR. The candidate does **not** enable HDR or fork the denoising engine.

Instead, [warm_batch.py](warm_batch.py) temporarily replaces only the standalone runtime's one-use text-phase installer while one model is loaded. It encodes each of at most **four unique fixed prompts** through the *same existing* raw encoder, projection and connectors, one prompt at a time, storing the final contexts on CPU. Raw Gemma layer tensors are projected and discarded immediately, rather than retaining a large batch of hidden states. It then releases Gemma exactly once, stages the same FP32 video encoder/upsampler on GPU1, and replaces the pipeline's cache with a sealed cache. Subsequent calls still use the exact unchanged `runtime.generate` and public model generation API, with the same seed49, images, source dimensions, frame count and generation settings.

The final CPU cache is bounded at256MiB. Each retrieval returns fresh tensor values so an in-place operation cannot change a later take. A missing/changed prompt, extra negative condition, altered cache key, changed fitted image, modified source binding or interrupted/failed batch stops execution; it cannot reload Gemma or silently fall back. A failed batch is poisoned for further calls. Every cache value's shape, dtype and tensor-byte SHA are recorded. Both CUDA devices are synchronized after each returned CPU frame array, then unreferenced temporaries are collected; video/model parameters are not deliberately unloaded.

At the pinned settings, **no negative-prompt embedding is used**: `NAG_scale=1`, `n_prompt=''`, and the engine requests only `[prompt]`. The adapter rejects guidance changes rather than pretending it has cached an absent negative condition. Audio-conditioned performance generation is outside this candidate; existing A2V production remains separate.

## Exact inspected sources

The repository retains the pinned source archive and all existing patches; [binding-lock.json](binding-lock.json) binds the standalone runtime, model/source/patch locks and the actual prepared bytes of six relevant engine files. Existing complete-package and checkpoint verification remain required. Inspection is against WanGP commit `b8880bd5d292edfbe2384f5c951d95757ad59ea0`:

- [Distilled pipeline](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/models/ltx2/ltx_pipelines/distilled.py): lines165 and282–303 provide the cache; lines226–229 recreate per-call seeded noise generators. Denoising state and conditioning are local to each invocation. These code properties support feasibility, not a proof against all retained-state errors.
- [Text cache](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/shared/utils/text_encoder_cache.py): its encode protocol stores CPU values and returns them to the requested device. The experimental sealed implementation follows that interface but refuses cache misses and protects stored values from later mutation.
- [Gemma helpers](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/models/ltx2/ltx_core/text_encoders/gemma/encoders/base_encoder.py): `encode_text`, `postprocess_text_embeddings` and `resolve_text_connectors` are called unchanged, with the repository's existing counted dtype/device patches.
- [Public generation](https://github.com/deepbeepmeep/WanGP/blob/b8880bd5d292edfbe2384f5c951d95757ad59ea0/models/ltx2/ltx2.py): default NAG1 at line919, all normal generation arguments at1305–1348, and HDR-only precomputed-context routing at1337. The candidate keeps the ordinary branch.
- [Current runtime](../../../tools/kaggle-story23/runtime.py): one-use `install_sequential_text_phase`, dual-T4 device/precision layout, seed49 and exact guide audit remain the reference. [Existing attribution](../../../tools/kaggle-story23/NOTICE.md) is preserved.

## What might be saved

[Measured estimate](throughput-estimate.json) binds ten actual P1/P2 render records. Mean child elapsed time **outside `model.generate` is334.57seconds**, median314.41seconds, range305.63–426.26seconds. That is not an isolated model-loading measurement: it also includes validation, encoding and other per-child work. Gemma prompt encoding already occurs *inside* `generation_seconds`. Every distinct new prompt still needs that computation; moving it into a prefill clock is not a speedup.

If49 otherwise comparable I2V takes were run as13 batches of at most four distinct prompts, there would be36 fewer model initializations. Removing the *entire* measured outside-generate overhead on those36 calls would save3.35 summed job-hours. **That is an optimistic upper bound, not an expected or measured saving.** Per-take output encoding/checks remain, video tensors still follow the same offload policy, the initial model download remains, and performance/A2V takes may use a separate path. Real savings must be measured as complete batch wall time, including load, every prefill, generation, cleanup and export.

## API for a separately scheduled diagnostic

The adapter has no submission path. The separate [experiment driver](experiment_driver.py) is now prepared for the fixed private hardware diagnostic described in the [runbook](hardware-runbook.md). Root/ops must schedule it within the account's two-job capacity, considering unrelated workloads. Existing action pilots proceed unchanged and the chair test has priority.

Prerequisites are the unchanged package verification, each manifest's validation, standard `run.preflight`, original checkpoint download/verification and `run.fit_image`. The candidate receives fitted guide objects plus their original fitting evidence:

```python
from warm_batch import WarmBatch

# Run the existing validation/preflight/download functions first.
# start, start_fitting = run.fit_image(the_validated_start_path)
# end, end_fitting = run.fit_image(the_validated_end_path)
entries = [{
    "manifest": exact_validated_manifest,
    "start_image": start, "start_fitting": start_fitting,
    "end_image": end, "end_fitting": end_fitting,
}]
batch = WarmBatch(runtime, model_dir, bundle_dir, prepared_backend_dir, entries)
frames, details = batch.generate_take(exact_validated_manifest["take_id"])
# Use the unchanged run.encode_video/check_video and separate new output paths.
```

The registry in the staged `common` module must include every frozen take, as in the existing production bundle. This candidate neither changes that registry nor derives new manifests. Preserve returned raw RGB-array SHA before encoding, final video bytes, cache tensor checksums, the complete timings and device-memory events. The nested details label neural equivalence unproven until the experiment below passes.

## Precise neural test and adoption gate

1. After the initial action-pilot motion results, use the two frozen validated takes selected by root: H01 has 169 frames and C01 has 193. Both use their exact existing prompts/endpoints, backend/runtime/weights, seed 49 and generation parameters. New experimental IDs separate their diagnostic outputs from production takes. No new visual direction is introduced to test caching.
2. Run A and B through the unchanged standalone runtime in separate fresh child processes using one already verified shared model cache. A diagnostic wrapper may observe the existing cache's returned context values and the uint8 frame array immediately before the unchanged encoder; it must not modify either. Save raw context and RGB-array hashes, full timings, output and memory measurements. Existing pilot encodes alone do not establish pre-encode array identity.
3. In a **fresh candidate process**, prefill A and B, then generate **A → B → A** through one `WarmBatch`. Give the repeated A distinct diagnostic output directories so nothing is overwritten. This repetition is a state-isolation experiment, never permission to repeat it in the final film. Gemma raw-encode count must remain exactly two; sealed cache requests must total three, one positive prompt per call. Gemma must remain released, both video components FP32 on GPU1, no unexpected new loading or model download.
4. Compare cold versus warm final video/audio context tensors **bit for bit**, each selected raw RGB output against its standalone baseline, and first versus last warm A. Verify full decoded outputs and normal source/cut visual standards. If output equality fails, stop promotion and identify the cause. If a repeated cold control is itself nondeterministic, measure that separately before selecting any looser numerical criterion; do not silently relabel a different result equivalent.
5. Record memory after each call and peak memory for both GPUs. A second/later call must not retain a previous take's latents/output or show accumulating memory. The actual context CPU footprint must remain below256MiB; increasing this bound or prompt count requires a separate explicit candidate.
6. Compare **complete process/batch elapsed time**, counting model load, all prompt encoding, context copying/checksums, cleanup and video encoding. A proposed adoption threshold is at least20% lower per-take batch time after accounting for its one-time load/prefill, with all equivalence/memory checks passed. This20% is an engineering decision target, not a claimed benchmark. Keep the existing runtime if the gain is small or the test fails.

Planning from recorded169–225frame jobs suggests the five-generation cold-A/cold-B/warm-A-B-A experiment could occupy roughly45–75minutes plus initial environment/download variation. This is an estimate, not a quota debit or guaranteed runtime. Root should apply a bounded diagnostic timeout and no automatic retries; current story production takes priority. No test was scheduled by this agent.

## Offline checks and limits

Run `python3 -m unittest discover -s productions/join-me-in-life/full-film/revision-2/tools/warm-batch -p 'test_*.py' -v`.

Fifteen offline tests pass. Ten cover exact manifest/image/seed binding, wrong guide rejection, guidance-change refusal, prompt/cache bounds, sequential exact-helper argument order, cache mutation isolation, no cache-miss/negative-condition fallback, and exact current runtime/engine/patch fingerprints. Five cover the experiment's exact RGB/context gates, zero-byte allocation-growth gate, balanced speed threshold and refusal of automatic promotion even when checks pass. Tensor transport uses test doubles; no PyTorch or CUDA arithmetic is exercised. The tests establish API/control-flow bindings and source compatibility, **not neural equivalence, GPU residency viability, peak memory or actual speed**. The concrete risks to resolve on hardware are projection while Gemma remains resident, reference release, repeated mmgp offload/device state, shape-dependent retained state and actual first-versus-later throughput.
