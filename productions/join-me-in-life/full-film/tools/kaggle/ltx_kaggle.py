#!/usr/bin/env python3
"""Private, bounded LTX 13B pilot/batch runner. No account or publication API.

Adapted from DamnKuldeep's Apache-2.0 implementation, pinned in model-lock.json.
The model has its own LTX open-weights license. See NOTICE.md.
"""
import argparse
import gc
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
MODEL_LOCK = json.loads((HERE / 'model-lock.json').read_text())
TIMESTEPS = [1000, 993, 987, 981, 975, 909, 725]
GIB = 1024 ** 3


def sha256(path):
    with Path(path).open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def input_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('Inputs must use relative paths inside the private bundle')
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()) or not result.is_file():
        raise ValueError('Input missing or outside private bundle')
    return result


def validate_manifest(manifest, root):
    if manifest.get('schema') != 'jml-ltx-kaggle/v1' or manifest.get('privacy') != 'private':
        raise ValueError('Require the supported manifest schema and explicit private inputs')
    if manifest.get('mode') not in ('pilot', 'batch'):
        raise ValueError('Mode must be pilot or batch')
    shots = manifest.get('shots')
    if not isinstance(shots, list) or not shots:
        raise ValueError('Manifest needs at least one shot')
    ids = set()
    for shot in shots:
        ident = shot.get('shot_id', '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', ident) or ident in ids:
            raise ValueError('Invalid or duplicate shot ID')
        ids.add(ident)
        if not isinstance(shot.get('prompt'), str) or not shot['prompt'].strip():
            raise ValueError('Each shot needs its exact prompt')
        for field in ('width', 'height'):
            if type(shot.get(field)) is not int or shot[field] < 32 or shot[field] % 32:
                raise ValueError('Dimensions must be positive multiples of 32')
        if type(shot.get('frames')) is not int or shot['frames'] < 9 or (shot['frames'] - 1) % 8:
            raise ValueError('Frames must be 8n+1')
        if shot.get('fps') not in (24, 25, 30):
            raise ValueError('Unsupported frame rate')
        seeds = shot.get('seeds')
        if not isinstance(seeds, list) or not seeds or len(set(seeds)) != len(seeds):
            raise ValueError('Each shot needs distinct explicit seeds')
        if any(type(seed) is not int or not 0 <= seed < 2 ** 32 for seed in seeds):
            raise ValueError('Seeds must be uint32 integers')
        if manifest['mode'] == 'pilot' and (shot['frames'] > 153 or shot['width'] * shot['height'] > 864 * 480):
            raise ValueError('Pilot capped at 153 frames and 864x480 pixels')
        for field in ('image', 'end_image'):
            if field not in shot:
                if field == 'image':
                    raise ValueError('An image-to-video source is required')
                continue
            path = input_path(root, shot[field])
            expected = shot.get(field + '_sha256')
            if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected) or sha256(path) != expected:
                raise ValueError(f'{ident}: source hash mismatch for {field}')
    if manifest['mode'] == 'pilot' and sum(len(s['seeds']) for s in shots) > 6:
        raise ValueError('Pilot capped at six explicitly listed takes')
    return manifest


def request_record(shot, seed):
    return {'schema': 'jml-ltx-render/v1', 'shot': shot, 'seed': seed,
            'model_repository': MODEL_LOCK['repository'], 'model_revision': MODEL_LOCK['revision'],
            'runner_sha256': sha256(__file__), 'timesteps': TIMESTEPS,
            'dtype': 'float16', 'quantization': 'NF4', 'guidance_scale': 1.0,
            'decode_timestep': 0.05, 'decode_noise_scale': 0.025,
            'image_cond_noise_scale': 0.025, 'image_fit': 'contain',
            'stochastic_sampling': False, 'max_sequence_length': 128}


def fingerprint(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()


def resume_complete(directory, request):
    metadata = directory / 'render.json'
    if not metadata.exists():
        return False
    saved = json.loads(metadata.read_text())
    if saved.get('request_sha256') != fingerprint(request):
        raise ValueError(f'Existing take has different inputs/settings: {directory.name}; use a new output root')
    video = directory / 'video.mp4'
    if saved.get('status') == 'complete':
        if not video.is_file() or sha256(video) != saved.get('video_sha256'):
            raise ValueError('Completed take is missing or has changed; preserve it and investigate')
        return True
    return False


def require_batch_review(manifest, review_path):
    if manifest['mode'] == 'pilot':
        return
    if not review_path:
        raise ValueError('Batch mode needs an explicit completed pilot review file')
    review = json.loads(Path(review_path).read_text())
    if (review.get('model_revision') != MODEL_LOCK['revision'] or review.get('decision') != 'accepted'
            or review.get('normal_speed_reviewed') is not True or review.get('slow_motion_reviewed') is not True
            or not review.get('reviewer') or not review.get('accepted_takes')):
        raise ValueError('Pilot review must identify the accepted model/takes and completed playback review')
    for take in review['accepted_takes']:
        if not re.fullmatch(r'[0-9a-f]{64}', take.get('video_sha256', '')) or not take.get('usable_interval_seconds'):
            raise ValueError('Each reviewed take must identify its exact video hash and usable interval')


def configure_cache(cache):
    cache.mkdir(parents=True, exist_ok=True)
    os.environ['HF_HOME'] = str(cache / 'hf')
    os.environ['HF_HUB_CACHE'] = str(cache / 'hf/hub')
    os.environ['HF_XET_CACHE'] = str(cache / 'hf/xet')
    os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':16:8'
    os.environ['USE_TF'] = '0'
    os.environ['USE_FLAX'] = '0'


def preflight(cache, output):
    import torch
    import psutil
    import bitsandbytes as bnb
    from packaging.version import Version
    if not Version('2.3') <= Version(torch.__version__.split('+')[0]) < Version('3'):
        raise RuntimeError('Keep a Kaggle CUDA Torch build >=2.3,<3; do not auto-install another Torch')
    if not torch.cuda.is_available() or torch.cuda.device_count() != 2:
        raise RuntimeError('This route requires an actual two-GPU CUDA runtime')
    devices = []
    for i in range(2):
        p = torch.cuda.get_device_properties(i)
        if 'T4' not in p.name or p.total_memory < 14 * GIB:
            raise RuntimeError('This pilot is scoped to two T4 GPUs with at least 14 GiB each')
        devices.append({'index': i, 'name': p.name, 'total_memory_bytes': p.total_memory,
                        'free_memory_bytes': torch.cuda.mem_get_info(i)[0],
                        'compute_capability': list(torch.cuda.get_device_capability(i))})
        # Prove the installed NF4/CUDA build works before downloading 47.6 GB.
        layer = bnb.nn.Linear4bit(16, 16, bias=False, quant_type='nf4', compute_dtype=torch.float16).to(f'cuda:{i}')
        with torch.inference_mode():
            value = layer(torch.ones((1, 16), dtype=torch.float16, device=f'cuda:{i}'))
        if not torch.isfinite(value).all():
            raise RuntimeError('NF4 smoke test returned non-finite values')
        del layer, value
        torch.cuda.empty_cache()
    if psutil.virtual_memory().available < 10 * GIB:
        raise RuntimeError('Need at least 10 GiB available host RAM before loading shards')
    output.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output).free < 2 * GIB:
        raise RuntimeError('Insufficient output disk headroom')
    versions = {name: importlib.metadata.version(name) for name in
                ['torch', 'diffusers', 'transformers', 'accelerate', 'bitsandbytes', 'huggingface-hub']}
    required = {'diffusers': '0.37.0', 'transformers': '4.57.3', 'accelerate': '1.12.0',
                'bitsandbytes': '0.49.1', 'huggingface-hub': '0.36.0'}
    if any(versions[k] != v for k, v in required.items()):
        raise RuntimeError('Install the pinned requirements in a fresh process before inference')
    report = {'python': platform.python_version(), 'packages': versions, 'torch_cuda': torch.version.cuda,
              'devices': devices, 'host_available_bytes': psutil.virtual_memory().available,
              'cache_free_bytes': shutil.disk_usage(cache).free, 'output_free_bytes': shutil.disk_usage(output).free}
    save_json(output / 'environment.json', report)
    print(json.dumps(report), flush=True)
    return report


def download_model(cache):
    from huggingface_hub import snapshot_download
    model = cache / 'model'
    missing = sum(f['bytes'] for f in MODEL_LOCK['files'] if not (model / f['path']).exists())
    if shutil.disk_usage(cache).free < missing + 4 * GIB:
        raise RuntimeError(f'Official allowlisted model needs {missing / 1e9:.2f} GB plus 4 GiB reserve; no alternate weights silently substituted')
    snapshot_download(MODEL_LOCK['repository'], revision=MODEL_LOCK['revision'], token=False,
                      local_dir=str(model), allow_patterns=[f['path'] for f in MODEL_LOCK['files']], max_workers=4)
    for entry in MODEL_LOCK['files']:
        file = model / entry['path']
        if file.stat().st_size != entry['bytes'] or sha256(file) != entry['sha256']:
            raise RuntimeError('Official model file failed size/SHA256 validation: ' + entry['path'])
    save_json(cache / 'verified-model.json', MODEL_LOCK)
    return model


def chunk_feed_forward(module, chunk_size=512):
    """No site-package patch; local wrapper follows the audited creator method."""
    import torch
    class ChunkedFeedForward(torch.nn.Module):
        def __init__(self, original):
            super().__init__()
            self.original = original
        def forward(self, hidden_states, *args, **kwargs):
            if hidden_states.shape[1] <= chunk_size:
                return self.original(hidden_states, *args, **kwargs)
            output = torch.empty_like(hidden_states)
            for start in range(0, hidden_states.shape[1], chunk_size):
                output[:, start:start + chunk_size] = self.original(hidden_states[:, start:start + chunk_size], *args, **kwargs)
            return output
    return ChunkedFeedForward(module)


def encode_prompts(model, shots):
    import torch
    from transformers import T5EncoderModel, T5Tokenizer, BitsAndBytesConfig
    tokenizer = T5Tokenizer.from_pretrained(model / 'tokenizer', local_files_only=True)
    encoder = T5EncoderModel.from_pretrained(model / 'text_encoder', local_files_only=True,
        use_safetensors=True, torch_dtype=torch.float16,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.float16),
        device_map={'': 1}, low_cpu_mem_usage=True).eval()
    embeddings = {}
    for shot in shots:
        if len(tokenizer(shot['prompt']).input_ids) > 128:
            raise ValueError(shot['shot_id'] + ': prompt exceeds the explicit 128-token pilot limit')
        inputs = tokenizer(shot['prompt'], padding='max_length', max_length=128, truncation=False, return_tensors='pt')
        with torch.inference_mode():
            hidden = encoder(inputs.input_ids.to('cuda:1'), attention_mask=inputs.attention_mask.to('cuda:1'))[0]
        if not torch.isfinite(hidden).all():
            raise RuntimeError('Non-finite text embeddings; stop before video generation')
        embeddings[shot['shot_id']] = (hidden.cpu(), inputs.attention_mask.bool().cpu())
    del encoder, tokenizer
    gc.collect()
    torch.cuda.empty_cache()
    return embeddings


def load_pipeline(model):
    import torch
    from diffusers import LTXConditionPipeline, LTXVideoTransformer3DModel, AutoencoderKLLTXVideo, BitsAndBytesConfig
    from diffusers import FlowMatchEulerDiscreteScheduler
    transformer = LTXVideoTransformer3DModel.from_pretrained(model / 'transformer', local_files_only=True,
        use_safetensors=True, torch_dtype=torch.float16,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.float16),
        device_map={'': 0}, low_cpu_mem_usage=True).eval()
    for block in transformer.transformer_blocks:
        block.ff = chunk_feed_forward(block.ff, 512)
    vae = AutoencoderKLLTXVideo.from_pretrained(model / 'vae', local_files_only=True,
        use_safetensors=True, torch_dtype=torch.float16).to('cuda:0').eval()
    vae.enable_tiling(tile_sample_min_height=128, tile_sample_min_width=128, tile_sample_min_num_frames=17,
                      tile_sample_stride_height=64, tile_sample_stride_width=64, tile_sample_stride_num_frames=9)
    scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained(model / 'scheduler', local_files_only=True)
    if scheduler.config.stochastic_sampling or scheduler.config.use_dynamic_shifting or scheduler.config.shift != 1:
        raise RuntimeError('Unexpected scheduler: preserve official deterministic 0.9.8 configuration')
    return LTXConditionPipeline(transformer=transformer, vae=vae, scheduler=scheduler, text_encoder=None, tokenizer=None)


def prepared_image(source, size, target):
    from PIL import Image, ImageOps
    with Image.open(source) as image:
        contained = ImageOps.contain(ImageOps.exif_transpose(image).convert('RGB'), size, Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', size, (0, 0, 0))
    canvas.paste(contained, ((size[0] - contained.width) // 2, (size[1] - contained.height) // 2))
    canvas.save(target)
    return canvas


def generate(pipe, embeddings, root, shot, seed, directory):
    import torch
    from diffusers.pipelines.ltx.pipeline_ltx_condition import LTXVideoCondition
    from diffusers.utils.torch_utils import randn_tensor
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    generator = torch.Generator(device='cuda:0').manual_seed(seed)
    conditions = []
    for field, index in [('image', 0), ('end_image', shot['frames'] - 1)]:
        if field in shot:
            image = prepared_image(input_path(root, shot[field]), (shot['width'], shot['height']), directory / (field + '.png'))
            conditions.append(LTXVideoCondition(image=image, frame_index=index, strength=1.0))
    hidden, mask = embeddings[shot['shot_id']]
    step_times = []
    started = time.monotonic()
    def step_done(pipeline, index, timestep, kwargs):
        torch.cuda.synchronize(0)
        step_times.append({'step': index + 1, 'timestep': float(timestep), 'elapsed_seconds': time.monotonic() - started})
        print(json.dumps({'shot_id': shot['shot_id'], 'seed': seed, **step_times[-1]}), flush=True)
        return kwargs
    for i in range(2):
        torch.cuda.reset_peak_memory_stats(i)
    pipe.vae.to('cuda:0')
    with torch.inference_mode():
        latents = pipe(conditions=conditions, prompt_embeds=hidden.to('cuda:0'), prompt_attention_mask=mask.to('cuda:0'),
            width=shot['width'], height=shot['height'], num_frames=shot['frames'], frame_rate=shot['fps'],
            timesteps=TIMESTEPS, guidance_scale=1.0, image_cond_noise_scale=0.025,
            generator=generator, output_type='latent', max_sequence_length=128, callback_on_step_end=step_done).frames
        # Reproduce pinned Diffusers' decode path, moving only VAE/decode to GPU1.
        latents = pipe._denormalize_latents(latents, pipe.vae.latents_mean, pipe.vae.latents_std, pipe.vae.config.scaling_factor)
        latents = latents.to(torch.float16)
        noise = randn_tensor(latents.shape, generator=generator, device=latents.device, dtype=latents.dtype)
        latents = (1 - 0.025) * latents + 0.025 * noise
        del noise
        pipe.vae.to('cuda:1')
        latents = latents.to('cuda:1')
        timestep = torch.tensor([0.05], dtype=torch.float16, device='cuda:1')
        decoded = pipe.vae.decode(latents, timestep, return_dict=False)[0]
        if not torch.isfinite(decoded).all():
            raise RuntimeError('Non-finite decoded pixels; do not export this take')
        frames = pipe.video_processor.postprocess_video(decoded, output_type='pil')[0]
    torch.cuda.synchronize()
    details = {'generation_seconds': time.monotonic() - started, 'steps': step_times,
               'gpu_peak_allocated_bytes': [torch.cuda.max_memory_allocated(i) for i in range(2)]}
    del decoded, latents
    pipe.vae.to('cuda:0')
    gc.collect()
    torch.cuda.empty_cache()
    if len(frames) != shot['frames']:
        raise RuntimeError('Model returned fewer frames; no silent shortening or automatic extension')
    return frames, details


def export_and_check(frames, shot, directory):
    import imageio.v2 as imageio
    import imageio_ffmpeg
    import numpy as np
    temporary = directory / 'video.partial.mp4'
    with imageio.get_writer(temporary, fps=shot['fps'], codec='libx264', macro_block_size=1,
                            output_params=['-crf', '18', '-pix_fmt', 'yuv420p']) as writer:
        for frame in frames:
            writer.append_data(np.asarray(frame))
    # Stream every decoded RGB frame without holding a second video in RAM.
    reader = imageio_ffmpeg.read_frames(str(temporary), pix_fmt='rgb24')
    metadata = next(reader)
    count = sum(1 for _ in reader)
    if count != shot['frames'] or tuple(metadata['size']) != (shot['width'], shot['height']):
        raise RuntimeError('Export decode/frame count/dimensions failed')
    if abs(metadata['fps'] - shot['fps']) > .001 or abs(metadata['duration'] - count / shot['fps']) > .05:
        raise RuntimeError('Export frame rate/duration failed')
    video = directory / 'video.mp4'
    temporary.replace(video)
    return {'decoded_frames': count, 'width': shot['width'], 'height': shot['height'],
            'fps': metadata['fps'], 'duration_seconds': metadata['duration'], 'video_sha256': sha256(video)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('/kaggle/working/jml-ltx-results'))
    parser.add_argument('--cache', type=Path, default=Path('/tmp/jml-ltx-cache'))
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--max-new-renders', type=int, default=1)
    parser.add_argument('--max-session-hours', type=float, default=4)
    parser.add_argument('--pilot-review', type=Path)
    args = parser.parse_args()
    if not 1 <= args.max_new_renders <= 24 or not 0 < args.max_session_hours <= 6:
        parser.error('Use 1–24 new renders and a session budget of at most six hours')
    root = args.manifest.resolve().parent
    manifest = validate_manifest(json.loads(args.manifest.read_text()), root)
    require_batch_review(manifest, args.pilot_review)
    if args.validate_only:
        print(json.dumps({'valid': True, 'shots': len(manifest['shots']), 'takes': sum(len(s['seeds']) for s in manifest['shots'])}))
        return
    args.output.mkdir(parents=True, exist_ok=True)
    jobs = []
    for shot in manifest['shots']:
        for seed in shot['seeds']:
            directory = args.output / f"{shot['shot_id']}__seed-{seed}"
            request = request_record(shot, seed)
            if not resume_complete(directory, request):
                jobs.append((shot, seed, directory, request))
    if not jobs:
        print('All requested takes already complete; no GPU model loaded.')
        return
    configure_cache(args.cache)
    environment = preflight(args.cache, args.output)
    if args.preflight_only:
        return
    session_started = time.monotonic()
    model = download_model(args.cache)
    selected = jobs[:args.max_new_renders]
    shots = list({shot['shot_id']: shot for shot, _, _, _ in selected}.values())
    embeddings = encode_prompts(model, shots)
    pipe = load_pipeline(model)
    save_json(args.output / 'model-lock.json', MODEL_LOCK)
    save_json(args.output / 'manifest.json', manifest)
    for shot, seed, directory, request in selected:
        if time.monotonic() - session_started >= args.max_session_hours * 3600:
            print('Session budget reached; remaining takes are resumable.'); break
        if shutil.disk_usage(args.output).free < 2 * GIB:
            raise RuntimeError('Output disk reserve reached')
        directory.mkdir(parents=True, exist_ok=True)
        previous = directory / 'render.json'
        if previous.exists():
            # Preserve interrupted/failed evidence on an explicitly resumed run.
            previous.rename(directory / f'render-previous-{time.time_ns()}.json')
        partial = directory / 'video.partial.mp4'
        if partial.exists():
            partial.rename(directory / f'video-previous-{time.time_ns()}.mp4')
        base = {'request': request, 'request_sha256': fingerprint(request), 'started_unix': time.time(),
                'status': 'running', 'acceptance': 'unreviewed', 'environment': environment}
        save_json(directory / 'render.json', base)
        try:
            frames, timing = generate(pipe, embeddings, root, shot, seed, directory)
            technical = export_and_check(frames, shot, directory)
            save_json(directory / 'render.json', {**base, **timing, **technical,
                      'status': 'complete', 'technical_valid': True, 'acceptance': 'unreviewed'})
        except Exception as error:
            save_json(directory / 'render.json', {**base, 'status': 'failed', 'error_type': type(error).__name__,
                      'error': str(error)[:800]})
            raise  # Stop on OOM/failure; never shorten, purchase, or change models.
    print('Requested bounded work finished. Playback/acting review is still required; stop unused Kaggle sessions.')


if __name__ == '__main__':
    main()
