#!/usr/bin/env python3
"""One private supplied-audio diagnostic. Root alone authorizes remote execution."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

from common import GIB, SHOTS, download_weights, inside, prepare_backend, save_json, sha256, validate_manifest, verify_package


def preflight(cache, output, backend):
    import torch
    import psutil
    if not torch.cuda.is_available() or torch.cuda.device_count() != 2:
        raise RuntimeError('Exactly two CUDA Tesla T4 cards are required before weights')
    devices = []
    for index in range(2):
        device = torch.cuda.get_device_properties(index)
        free, total = torch.cuda.mem_get_info(index)
        if 'T4' not in device.name or torch.cuda.get_device_capability(index) != (7, 5):
            raise RuntimeError('This diagnostic is pinned to two Tesla T4s')
        if total < 14 * GIB or free < 12 * GIB:
            raise RuntimeError('Insufficient free T4 memory before weights')
        devices.append({'index': index, 'name': device.name, 'total_bytes': total, 'free_bytes': free})
    if psutil.virtual_memory().available < 20 * GIB:
        raise RuntimeError('Need at least 20 GiB available host RAM before loading')
    if shutil.disk_usage(output).free < 2 * GIB:
        raise RuntimeError('Insufficient output disk reserve')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('FFmpeg and FFprobe are required before weights')
    # Real selected model/quantization imports and tiny CUDA operations precede the 35 GB download.
    sys.path.insert(0, str(backend))
    import torchaudio
    import torchvision
    from models.ltx2.ltx2 import LTX2
    from models.ltx2.ltx2_handler import family_handler
    from models.ltx2.ltx_core.model.audio_vae import AudioProcessor
    import runtime
    runtime.configure_attention()
    patches = runtime.patch_transformers()
    smoke = runtime.smoke_quantization()
    # Exercise the actual Gemma implementation/attention without a pretrained model.
    from transformers import Gemma3TextConfig, Gemma3ForCausalLM
    config = Gemma3TextConfig(vocab_size=128, hidden_size=128, intermediate_size=256,
                             num_hidden_layers=1, num_attention_heads=4, num_key_value_heads=2,
                             head_dim=32, max_position_embeddings=128, sliding_window=64)
    config._attn_implementation = 'sdpa'
    gemma = Gemma3ForCausalLM(config).to('cuda:1', torch.bfloat16).eval()
    with torch.inference_mode():
        hidden = gemma(torch.ones((1, 8), dtype=torch.long, device='cuda:1'), output_hidden_states=True).hidden_states[-1]
    if hidden.dtype != torch.bfloat16 or not torch.isfinite(hidden).all():
        raise RuntimeError('Actual tiny Gemma BF16/SDPA smoke failed')
    del gemma, hidden
    torch.cuda.empty_cache()
    return {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda,
            'devices': devices, 'host_available_bytes': psutil.virtual_memory().available,
            'packages': {name: importlib.metadata.version(name) for name in
                         ['mmgp', 'optimum-quanto', 'diffusers', 'transformers', 'gguf', 'accelerate']},
            'quantization_smoke': smoke, 'tiny_gemma_bf16_sdpa': True, 'runtime_patches': patches,
            'model_class_imports': ['LTX2', 'family_handler', 'AudioProcessor', 'Gemma3ForCausalLM']}


def encode_video(frames, path, fps, expected_frames):
    """Encode exact uint8 RGB frames; this child stays inside bootstrap's process group."""
    count, height, width, channels = frames.shape
    if (count, height, width, channels) != (expected_frames, 512, 896, 3) or expected_frames not in {89, 105} or fps != 24 or str(frames.dtype) != 'uint8':
        raise ValueError('Refuse unexpected video array')
    command = ['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{width}x{height}',
               '-r', str(fps), '-i', '-', '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
               '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, errors = process.communicate(frames.tobytes())
    if process.returncode:
        raise RuntimeError('Video encoding failed: ' + errors.decode(errors='replace')[-1000:])


def check_video(path, expected_frames):
    metadata = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', 
        '-show_entries', 'stream=codec_type,width,height,nb_read_frames,avg_frame_rate,duration', '-of', 'json', str(path)], text=True))
    streams = metadata['streams']
    if expected_frames not in {89, 105} or len(streams) != 1 or streams[0]['codec_type'] != 'video' or (streams[0]['width'], streams[0]['height'], int(streams[0]['nb_read_frames']),
                            streams[0]['avg_frame_rate']) != (896, 512, expected_frames, '24/1'):
        raise RuntimeError('Export dimensions/count/fps mismatch')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], check=True)
    return {'width': 896, 'height': 512, 'frames': expected_frames, 'fps': 24, 'duration_seconds': expected_frames / 24,
            'full_decode_passed': True, 'sha256': sha256(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path('/kaggle/working/jml-ltx-performance23-results'))
    parser.add_argument('--cache', type=Path, default=Path('/tmp/jml-ltx-performance23-runtime/cache'))
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--preflight-only', action='store_true')
    args = parser.parse_args()
    bundle = args.manifest.resolve().parent
    verify_package(bundle)
    manifest = json.loads(args.manifest.read_text())
    validate_manifest(manifest, bundle)
    if args.validate_only:
        print(json.dumps({'valid': True, 'takes': 1, 'frames': manifest['frames'], 'shot_id': manifest['shot_id'], 'supplied_stereo_audio': True}))
        return
    args.output.mkdir(parents=True, exist_ok=True)
    record = args.output / 'render.json'
    if record.exists():
        raise ValueError('Existing attempt preserved; no automatic overwrite or retry')
    args.cache.mkdir(parents=True, exist_ok=True)
    state = {'status': 'starting', 'acceptance': 'unreviewed', 'manifest': manifest,
             'manifest_sha256': sha256(args.manifest), 'started_unix': time.time()}
    save_json(record, state)
    try:
        for key, value in {'HF_HOME': str(args.cache / 'hf'), 'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1',
                           'HF_XET_CHUNK_CACHE_SIZE_BYTES': '0', 'USE_TF': '0', 'USE_FLAX': '0',
                           'TOKENIZERS_PARALLELISM': 'false', 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION': 'python'}.items():
            os.environ[key] = value
        backend = args.cache / ('backend-' + manifest['shot_id'])
        patches = prepare_backend(bundle, backend)
        save_json(args.output / 'patches-applied.json', patches)
        environment = preflight(args.cache, args.output, backend)
        save_json(args.output / 'environment.json', environment)
        if args.preflight_only:
            state['status'] = 'preflight_complete_no_weights'
            return
        lock = json.loads((bundle / 'model-lock.json').read_text())
        model_dir = download_weights(lock, args.cache / 'models')
        save_json(args.output / 'model-lock.json', lock)
        # All required assets now exist. Fail any subsequent implicit Hub lookup.
        os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
        import huggingface_hub.constants
        huggingface_hub.constants.HF_HUB_OFFLINE = True
        import runtime
        from PIL import Image, ImageOps
        import numpy as np
        import soundfile as sf
        image = ImageOps.contain(Image.open(inside(bundle, manifest['image'])).convert('RGB'), (896, 512), Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', (896, 512), (0, 0, 0))
        canvas.paste(image, ((896 - image.width) // 2, (512 - image.height) // 2))
        canvas.save(args.output / 'input-fitted.png')
        samples, sample_rate = sf.read(inside(bundle, manifest['audio']), dtype='float32', always_2d=True)
        waveform = samples.mean(axis=1).astype(np.float32)
        if not np.isfinite(waveform).all():
            raise ValueError('Non-finite supplied waveform')
        model = runtime.load_model(model_dir)
        frames, details = runtime.generate(model, manifest, canvas, waveform, sample_rate)
        silent = args.output / 'video-silent.mp4'
        encode_video(frames, silent, 24, manifest['frames'])
        state.update(details)
        state['video'] = check_video(silent, manifest['frames'])
        # Retain exact original stereo PCM in a lossless review container, never model audio.
        review = args.output / 'review-original-audio.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(silent), '-i', str(inside(bundle, manifest['audio'])),
                        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(review)], check=True)
        decoded = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(review), '-map', '0:a:0',
                                          '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
        import wave, hashlib
        with wave.open(str(inside(bundle, manifest['audio'])), 'rb') as original:
            pcm = original.readframes(original.getnframes())
        if decoded != pcm:
            raise RuntimeError('Review mux changed the supplied original stereo PCM')
        state['review'] = {'path': review.name, 'sha256': sha256(review), 'original_pcm_sha256': hashlib.sha256(pcm).hexdigest(),
                           'decoded_pcm_equal_to_input': True, 'model_audio_used': False}
        state['status'] = 'complete'
        state['technical_valid'] = True
    except Exception as error:
        state.update(status='failed', error_type=type(error).__name__, error=str(error)[:1000])
        raise
    finally:
        state['elapsed_seconds'] = time.time() - state['started_unix']
        save_json(record, state)


if __name__ == '__main__':
    main()
