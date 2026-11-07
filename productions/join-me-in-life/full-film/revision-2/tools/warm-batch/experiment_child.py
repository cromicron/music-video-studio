#!/usr/bin/env python3
"""Isolated prepare/cold/warm child for the fixed H01/C01 cache experiment."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

from common import download_weights, inside, prepare_backend, save_json, sha256, validate_manifest, verify_package


def raw_record(frames):
    if str(frames.dtype) != 'uint8' or not frames.flags.c_contiguous:
        raise ValueError('Expected unchanged contiguous uint8 RGB array')
    return {'shape': list(frames.shape), 'dtype': str(frames.dtype), 'bytes': int(frames.nbytes),
            'sha256': hashlib.sha256(memoryview(frames).cast('B')).hexdigest()}


def environment(cache):
    os.environ.update(HF_HOME=str(cache / 'hf'), HF_HUB_DISABLE_IMPLICIT_TOKEN='1',
        HF_XET_CHUNK_CACHE_SIZE_BYTES='0', USE_TF='0', USE_FLAX='0', TOKENIZERS_PARALLELISM='false',
        PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python')


def require_existing_models(bundle, cache):
    lock = json.loads((bundle / 'model-lock.json').read_text())
    for item in lock['files']:
        p = cache / 'models' / item['path']
        if not p.is_file() or p.stat().st_size != item['bytes']:
            raise ValueError('Setup did not populate the fixed model cache: ' + item['path'])
    # The unchanged download_weights subsequently hashes every existing file;
    # offline mode makes an unexpected second fetch fail instead of biasing timing.
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')


def prepare(bundle, cache, output, *, tag, weights_may_download):
    import run
    environment(cache)
    if not weights_may_download:
        require_existing_models(bundle, cache)
    backend = cache / ('backend-' + tag)
    patches = prepare_backend(bundle, backend)
    save_json(output / 'patches-applied.json', patches)
    env = run.preflight(cache, output, backend)
    save_json(output / 'environment.json', env)
    lock = json.loads((bundle / 'model-lock.json').read_text())
    model_dir = download_weights(lock, cache / 'models')
    save_json(output / 'model-lock.json', lock)
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    import huggingface_hub.constants
    huggingface_hub.constants.HF_HUB_OFFLINE = True
    return backend, model_dir


def observe_cold(bundle, cache, output, take_id):
    """Call original run.main; observers copy hashes but return original tensors."""
    import run
    import runtime
    import warm_batch
    environment(cache)
    require_existing_models(bundle, cache)
    manifest = json.loads((bundle / (take_id + '.json')).read_text())
    original_load, original_encode = runtime.load_model, run.encode_video
    clock = {'observer_context_seconds': 0.0, 'observer_rgb_seconds': 0.0}

    def load_observed(model_dir):
        began = time.monotonic()
        model = original_load(model_dir)
        clock['model_load_seconds'] = time.monotonic() - began
        cache_object = model.pipeline.text_encoder_cache
        encode = cache_object.encode
        calls = []
        def encode_observed(*args, **kwargs):
            result = encode(*args, **kwargs)
            started = time.monotonic()
            prompts = args[1] if len(args) > 1 else kwargs['prompts']
            if list(prompts) != [manifest['prompt']] or len(result) != 1:
                raise ValueError('Unexpected standalone context request')
            pair = warm_batch.cpu_pair(result[0])
            calls.append({'prompt_sha256': hashlib.sha256(manifest['prompt'].encode()).hexdigest(),
                          'tensors': [warm_batch.tensor_record(t) for t in pair]})
            del pair
            if len(calls) != 1:
                raise ValueError('Standalone expected exactly one positive context request')
            save_json(output / 'context-observation.json', {'calls': calls, 'returned_original_tensor_objects': True})
            clock['observer_context_seconds'] += time.monotonic() - started
            return result
        cache_object.encode = encode_observed
        return model

    def encode_observed(frames, *args, **kwargs):
        began = time.monotonic()
        save_json(output / 'raw-rgb.json', raw_record(frames))
        clock['observer_rgb_seconds'] += time.monotonic() - began
        return original_encode(frames, *args, **kwargs)

    runtime.load_model, run.encode_video = load_observed, encode_observed
    old_argv = sys.argv
    try:
        sys.argv = [str(bundle / 'run.py'), '--manifest', str(bundle / (take_id + '.json')),
                    '--output', str(output), '--cache', str(cache)]
        run.main()
    finally:
        sys.argv = old_argv
        runtime.load_model, run.encode_video = original_load, original_encode
        save_json(output / 'observer-timing.json', clock)


def run_warm(bundle, cache, output, experiment, started):
    import run
    from warm_batch import WarmBatch
    backend, model_dir = prepare(bundle, cache, output, tag='warm-equivalence', weights_may_download=False)
    import runtime
    entries = []
    for ident in experiment['takes']:
        manifest = json.loads((bundle / (ident + '.json')).read_text())
        validate_manifest(manifest, bundle)
        start, start_fit = run.fit_image(inside(bundle, manifest['start_image']))
        end, end_fit = run.fit_image(inside(bundle, manifest['end_image']))
        start.save(output / (ident + '-start-fitted.png'))
        end.save(output / (ident + '-end-fitted.png'))
        entries.append({'manifest': manifest, 'start_image': start, 'start_fitting': start_fit,
                        'end_image': end, 'end_fitting': end_fit})
    batch = WarmBatch(runtime, model_dir, bundle, backend, entries, lock_path=bundle / 'binding-lock.json')
    setup_seconds = time.monotonic() - started
    summary = {'status': 'running', 'setup_seconds': setup_seconds, 'calls': [], 'automatic_retries': 0,
               'performance_clock_includes_context_hashing_and_exports': True}
    save_json(output / 'warm-summary.json', summary)
    for item in experiment['warm_order']:
        ident, label = item['take_id'], item['label']
        target = output / label
        target.mkdir()
        began = time.monotonic()
        manifest = batch.entries[ident]['manifest']
        save_json(target / 'manifest.json', manifest)
        frames, details = batch.generate_take(ident)
        save_json(target / 'raw-rgb.json', raw_record(frames))
        prompt_sha = hashlib.sha256(manifest['prompt'].encode()).hexdigest()
        save_json(target / 'context-observation.json', {'calls': [
            {'prompt_sha256': prompt_sha, 'tensors': batch.cache.records[prompt_sha]}],
            'sealed_cache_hit': True})
        run.encode_video(frames, target / 'video-silent.mp4', 24, manifest['frames'])
        video = run.check_video(target / 'video-silent.mp4', manifest['frames'])
        del frames
        gc.collect()
        import torch
        for index in range(2):
            torch.cuda.synchronize(torch.device(f'cuda:{index}'))
        memory = [torch.cuda.memory_allocated(i) for i in range(2)]
        record = {'status': 'complete', 'acceptance': 'diagnostic_not_production', 'manifest': manifest,
                  'manifest_sha256': sha256(bundle / (ident + '.json')), 'video': video,
                  'elapsed_seconds': time.monotonic() - began, 'after_export_gpu_allocated': memory, **details}
        save_json(target / 'render.json', record)
        summary['calls'].append({'label': label, 'take_id': ident, 'elapsed_seconds': record['elapsed_seconds'],
                                 'after_export_gpu_allocated': memory})
        if len(summary['calls']) == 2:
            summary['first_A_and_B_elapsed_seconds'] = time.monotonic() - started
        save_json(output / 'warm-summary.json', summary)
    summary.update(status='complete', elapsed_seconds=time.monotonic()-started,
                   raw_encode_count=len(batch.phase.state['raw_encodes']), cache_requests=batch.cache.calls,
                   gemma_released=batch.model.text_encoder.model is None,
                   context_cpu_bytes=batch.cache.bytes, context_cpu_limit=batch.lock['maximum_final_context_bytes'],
                   model_load_peak_allocated=batch.model_load_peak_allocated,
                   prefill_peak_allocated=batch.prefill_peak_allocated,
                   complete_text_phase=batch.phase.state)
    save_json(output / 'warm-summary.json', summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True, choices=['prepare', 'cold', 'warm'])
    parser.add_argument('--bundle', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--cache', required=True, type=Path)
    parser.add_argument('--take')
    args = parser.parse_args()
    if not Path('/kaggle/input').is_dir():
        raise RuntimeError('Hardware experiment is Kaggle-only')
    started = time.monotonic()
    bundle, output, cache = args.bundle.resolve(), args.output.resolve(), args.cache.resolve()
    verify_package(bundle)
    experiment = json.loads((bundle / 'experiment.json').read_text())
    for ident in experiment['takes']:
        validate_manifest(json.loads((bundle / (ident + '.json')).read_text()), bundle)
    output.mkdir(parents=True, exist_ok=True); cache.mkdir(parents=True, exist_ok=True)
    if (output / 'child.json').exists():
        raise ValueError('Existing child attempt preserved')
    state = {'status': 'starting', 'mode': args.mode, 'started_unix': time.time(), 'attempts': 1,
             'experiment_sha256': sha256(bundle / 'experiment.json')}
    save_json(output / 'child.json', state)
    try:
        if args.mode == 'prepare':
            prepare(bundle, cache, output, tag='warm-test-cache-setup', weights_may_download=True)
            state['neural_generations'] = 0
        elif args.mode == 'cold':
            if args.take not in experiment['takes']:
                raise ValueError('Unplanned cold take')
            observe_cold(bundle, cache, output, args.take)
            state['neural_generations'] = 1
        else:
            run_warm(bundle, cache, output, experiment, started)
            state['neural_generations'] = 3
        state['status'] = 'complete'
    except Exception as exc:
        state.update(status='failed', error_type=type(exc).__name__, error=str(exc)[:1500])
        raise
    finally:
        state['elapsed_seconds'] = time.monotonic() - started
        save_json(output / 'child.json', state)


if __name__ == '__main__':
    main()
