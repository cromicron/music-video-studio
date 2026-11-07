"""Minimal private adaptation of the pinned TeamAIQ dual-T4 A2V setup.

No UI, service, token, retry, prompt enhancement or implicit model download.
See NOTICE.md and vendor/teamaiq-a2v.ipynb for attribution and exact source.
"""
import inspect
import json
from pathlib import Path
import time


def require_finite(tensor, label):
    import torch
    if not torch.is_tensor(tensor) or not torch.isfinite(tensor).all():
        raise RuntimeError(label + ': non-finite or missing tensor')
    print(json.dumps({'tensor': label, 'shape': list(tensor.shape), 'dtype': str(tensor.dtype),
                      'device': str(tensor.device), 'absmax': float(tensor.abs().max())}), flush=True)


def patch_transformers():
    import torch
    import transformers.models.gemma3.modeling_gemma3 as gemma
    import transformers.integrations.sdpa_attention as sdpa
    from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS
    original_rope, original_sdpa = gemma.apply_rotary_pos_emb, sdpa.sdpa_attention_forward
    if 'unsqueeze_dim' not in inspect.signature(original_rope).parameters:
        raise RuntimeError('Unexpected pinned Gemma RoPE signature')
    if 'query' not in inspect.signature(original_sdpa).parameters:
        raise RuntimeError('Unexpected pinned SDPA signature')
    def safe_rope(q, k, cos, sin, unsqueeze_dim=1):
        return original_rope(q, k, cos.to(dtype=q.dtype), sin.to(dtype=q.dtype), unsqueeze_dim=unsqueeze_dim)
    def safe_sdpa(module, query, key, value, *args, **kwargs):
        return original_sdpa(module, query, key.to(dtype=query.dtype), value.to(dtype=query.dtype), *args, **kwargs)
    gemma.apply_rotary_pos_emb = safe_rope
    sdpa.sdpa_attention_forward = safe_sdpa
    # Transformers registers the original function separately; patch the actual dispatch too.
    ALL_ATTENTION_FUNCTIONS['sdpa'] = safe_sdpa
    if ALL_ATTENTION_FUNCTIONS['sdpa'] is not safe_sdpa:
        raise RuntimeError('Gemma SDPA dispatch patch did not bind')
    return {'gemma_rope_alignment': True, 'sdpa_module_and_dispatch_alignment': True}


def configure_attention():
    import torch
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_mem_efficient_sdp(True)
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cudnn.benchmark = False


def smoke_quantization():
    """Small actual Q4_K/Q6_K + Quanto-int8 operations; no downloaded weights."""
    import numpy as np
    import torch
    import gguf
    import shared.qtypes.gguf as adapter
    from optimum.quanto import quantize, freeze, qint8
    results = []
    for index in range(2):
        device = f'cuda:{index}'
        for qtype in (gguf.GGMLQuantizationType.Q4_K, gguf.GGMLQuantizationType.Q6_K):
            block, size = gguf.GGML_QUANT_SIZES[qtype]
            # Synthetic quantization blocks: deterministic bytes, finite scale fields.
            raw = np.zeros((4, size), dtype=np.uint8)
            if qtype == gguf.GGMLQuantizationType.Q4_K:
                raw[:, :2] = np.frombuffer(np.float16(0.125).tobytes(), np.uint8)
                raw[:, 4:] = 17
            else:
                raw[:, -2:] = np.frombuffer(np.float16(0.125).tobytes(), np.uint8)
                raw[:, :-2] = 17
            dense = torch.from_numpy(gguf.quants.dequantize(raw, qtype)).reshape(4, block).to(device, torch.float16)
            weight = adapter.GGUFWeightTensor.create(torch.from_numpy(raw).to(device), (4, block),
                     (block, 1), torch.float16, tensor_type=qtype, tensor_shape=(4, block))
            values = torch.linspace(-0.5, 0.5, block, device=device, dtype=torch.float16).reshape(1, block)
            actual = weight.linear(values)
            expected = torch.nn.functional.linear(values, dense)
            if not torch.isfinite(actual).all() or not torch.allclose(actual, expected, atol=0.05, rtol=0.02):
                raise RuntimeError('Actual GGUF quantization smoke failed: ' + str(qtype))
            results.append({'device': index, 'quantization': qtype.name, 'passed': True})
        layer = torch.nn.Sequential(torch.nn.Linear(64, 32, bias=False)).to(device, torch.bfloat16)
        quantize(layer, weights=qint8)
        freeze(layer)
        value = layer(torch.ones(1, 64, device=device, dtype=torch.bfloat16))
        if value.dtype != torch.bfloat16 or not torch.isfinite(value).all():
            raise RuntimeError('Quanto BF16/int8 smoke failed')
        results.append({'device': index, 'quantization': 'Quanto qint8 BF16', 'passed': True})
        del layer, value, weight, dense, values, actual, expected
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    return results


def load_model(model_dir):
    """Same model/components/offload route as notebook, with hard assertions."""
    import torch
    from mmgp import offload, quant_router
    from shared.utils import files_locator as fl
    import shared.qtypes.gguf  # registers the exact pinned extension
    import models.ltx2.ltx2 as backend
    from models.ltx2.ltx2_handler import family_handler
    import models.ltx2.ltx_pipelines.distilled as distilled
    import models.ltx2.ltx_core.model.video_vae.video_vae as vae
    from models.ltx2.ltx_core.model.video_vae.tiling import TilingConfig, SpatialTilingConfig, TemporalTilingConfig

    configure_attention()
    patch_transformers()
    model_dir = Path(model_dir)
    fl.set_checkpoints_paths([str(model_dir)])
    def config_from_checkpoint(path, fallback_config_path=None):
        path = path[0] if isinstance(path, (list, tuple)) else path
        _, metadata = quant_router.load_metadata_state_dict(path)
        config = backend._normalize_config((metadata or {}).get('config'))
        if not config and fallback_config_path:
            config = backend._normalize_config(json.loads(Path(fallback_config_path).read_text()))
        if not config:
            raise ValueError('Neither pinned checkpoint nor pinned fallback contains a model config')
        return config
    backend._load_config_from_checkpoint = config_from_checkpoint
    model_def = {'ltx2_pipeline': 'distilled'}
    model_def.update(family_handler.query_model_def('ltx2_22B', model_def))
    gemma = model_dir / 'gemma-3-12b-it-qat-q4_0-unquantized'
    model, pipe = family_handler.load_model(
        model_filename=str(model_dir / 'ltx-2.3-22b-distilled-Q4_K_M_light.gguf'),
        model_type='ltx2_22B_distilled', base_model_type='ltx2_22B', model_def=model_def,
        dtype=torch.float16, VAE_dtype=torch.float32,
        text_encoder_filename=str(gemma / 'gemma-3-12b-it-qat-q4_0-unquantized_quanto_bf16_int8.safetensors'))
    for key in ('video_decoder', 'video_encoder', 'spatial_upsampler'):
        component = getattr(model, key)
        component.to(torch.float32)
        component._model_dtype = torch.float32
        for module in component.modules():
            module._lock_dtype = torch.float32
    old_encoder, old_decoder = vae.VideoEncoder.forward, vae.VideoDecoder.forward
    def encoder(self, sample, *args, **kwargs):
        dtype, device = sample.dtype, sample.device
        param = next(self.parameters())
        sample = sample.to(device=param.device, dtype=param.dtype)
        with torch.cuda.device(sample.device):
            output = old_encoder(self, sample, *args, **kwargs)
        return output.to(device=device, dtype=dtype)
    def decoder(self, sample, *args, **kwargs):
        param = next(self.parameters())
        return old_decoder(self, sample.to(device=param.device, dtype=param.dtype), *args, **kwargs)
    vae.VideoEncoder.forward, vae.VideoDecoder.forward = encoder, decoder

    # No silent single-GPU fallback: the selected comparison requires the actual dual-T4 layout.
    model.text_encoder.to('cuda:1')
    gemma_model = model.text_encoder.model
    gemma_lm = gemma_model.model if hasattr(gemma_model, 'model') else gemma_model
    if getattr(gemma_model, 'lm_head', None) is not None:
        gemma_model.lm_head = torch.nn.Identity()
    embedding = gemma_lm.embed_tokens.to(device='cpu', dtype=torch.bfloat16)
    old_embed = embedding.forward
    def cpu_embed(input_ids, *args, **kwargs):
        return old_embed(input_ids.to('cpu'), *args, **kwargs).to('cuda:1')
    embedding.forward = cpu_embed
    gemma_model.__class__ = type(gemma_model.__class__.__name__, (gemma_model.__class__,),
                               {'device': property(lambda self: torch.device('cuda:1'))})
    pipe.pop('text_encoder')
    old_raw = model.text_encoder.encode_raw
    def encode_raw(text, padding_side='left'):
        tokenizer = model.text_encoder.tokenizer
        token_count = len(tokenizer.tokenizer(text.strip(), truncation=False).input_ids)
        if token_count > tokenizer.max_length:
            raise ValueError('Gemma prompt exceeds its explicit token capacity; truncation forbidden')
        print(json.dumps({'prompt_tokens': token_count, 'maximum': tokenizer.max_length}), flush=True)
        raw = old_raw(text, padding_side=padding_side)
        if any(h.dtype != torch.bfloat16 for h in raw.hidden_states):
            raise RuntimeError('Gemma hidden states must remain BF16; FP16 RMS squares overflow')
        for index, hidden in enumerate(raw.hidden_states):
            if not torch.isfinite(hidden).all():
                raise RuntimeError(f'Non-finite Gemma hidden state {index}')
        hidden = tuple(h.to(device='cuda:0') for h in raw.hidden_states)
        return raw.__class__(hidden, raw.attention_mask.to('cuda:0'), raw.padding_side)
    model.text_encoder.encode_raw = encode_raw
    for key in ('spatial_upsampler', 'video_encoder'):
        pipe[key].to('cuda:1')
        pipe.pop(key)
        param = next(getattr(model, key).parameters())
        if param.device != torch.device('cuda:1') or param.dtype != torch.float32:
            raise RuntimeError(key + ' did not bind to GPU1/FP32')

    old_up, old_decode = distilled.upsample_video, distilled.vae_decode_video_to_tensor
    def upsample(latent, video_encoder, upsampler):
        require_finite(latent, 'stage1')
        device, dtype = latent.device, latent.dtype
        with torch.cuda.device(1):
            output = old_up(latent=latent.to('cuda:1'), video_encoder=video_encoder, upsampler=upsampler)
        require_finite(output, 'upscaled')
        return output.to(device=device, dtype=dtype)
    def decode(latent, video_decoder, tiling_config=None, *args, **kwargs):
        require_finite(latent[0] if isinstance(latent, list) else latent, 'stage2')
        # Fixed bounded tiling; no notebook's automatic OOM retry or heuristic change.
        config = TilingConfig(spatial_config=SpatialTilingConfig(512, 64),
                              temporal_config=TemporalTilingConfig(64, 24))
        return old_decode(latent, video_decoder, config, *args, **kwargs)
    distilled.upsample_video, distilled.vae_decode_video_to_tensor = upsample, decode
    budgets = {'transformer': 11000, 'vae': 3500, 'audio_encoder': 1000,
               'audio_decoder': 1000, 'vocoder': 500, '*': 1000}
    offload.profile(pipe, profile_no=4, quantizeTransformer=False, convertWeightsFloatTo=torch.float16, budgets=budgets)
    offload.shared_state['_attention'] = 'sdpa'
    if model.dtype != torch.float16:
        raise RuntimeError('Transformer compute precision changed')
    return model


def generate(model, manifest, image, waveform, sample_rate):
    import torch
    began = time.monotonic()
    steps = []
    def callback(step, latent, is_start, **kwargs):
        record = {'step': int(step), 'start': bool(is_start), 'elapsed_seconds': time.monotonic() - began,
                  'pass_no': kwargs.get('pass_no'), 'progress_unit': kwargs.get('progress_unit')}
        steps.append(record)
        print(json.dumps(record), flush=True)
    for index in range(2):
        torch.cuda.reset_peak_memory_stats(index)
    with torch.inference_mode():
        result = model.generate(input_prompt=manifest['prompt'], image_start=image,
            height=512, width=896, frame_num=97, fps=24.0, seed=49, callback=callback,
            VAE_tile_size=512, input_video_strength=1.0, denoising_strength=1.0,
            guide_scale=1.0, audio_cfg_scale=1.0, alt_guide_scale=1.0, sampling_steps=8,
            guide_phases=2, n_prompt='', video_prompt_type='', audio_prompt_type='',
            input_waveform=waveform, input_waveform_sample_rate=sample_rate, audio_scale=1.0)
    coverage = getattr(model, '_jml_audio_coverage', None)
    if not coverage or not coverage['full_coverage'] or coverage['strength'] != 1.0:
        raise RuntimeError('No verified full supplied-audio conditioning record')
    if not isinstance(result, dict) or not torch.is_tensor(result.get('x')):
        raise RuntimeError('Pipeline returned no video tensor')
    video = result['x']
    if tuple(video.shape) != (3, 97, 512, 896) or video.dtype != torch.uint8:
        raise RuntimeError('Unexpected output shape/dtype; do not guess a conversion or trim')
    details = {'generation_seconds': time.monotonic() - began, 'steps': steps, 'audio_coverage': coverage,
               'gpu_peak_allocated_bytes': [torch.cuda.max_memory_allocated(i) for i in range(2)],
               'returned_model_audio_discarded': True}
    return video.permute(1, 2, 3, 0).contiguous().cpu().numpy(), details
