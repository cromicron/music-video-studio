#!/usr/bin/env python3
"""Check the actual VAE and prompt embeddings before retesting denoising."""
import json
from pathlib import Path
import time
import numpy as np
import torch
from PIL import Image
from diffusers import LTXConditionPipeline
from safetensors.torch import load_file
from ltx_cpu_scheduler import validate_corrected_step

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'productions/join-me-in-life/full-film/research/local-cpu-test'
CACHE=ROOT/'build/ltx-cpu'
torch.set_num_threads(4)
started=time.monotonic()
pipeline=LTXConditionPipeline.from_single_file(
    str(CACHE/'ltxv-2b-0.9.6-distilled-04-25.safetensors'),config=str(CACHE/'config'),
    text_encoder=None,tokenizer=None,torch_dtype=torch.bfloat16,
    local_files_only=True,low_cpu_mem_usage=True)
image=Image.open(ROOT/'productions/join-me-in-life/full-film/assets/her_window.png').convert('RGB').resize((384,256))
x=torch.from_numpy(np.array(image).copy()).permute(2,0,1).unsqueeze(0).unsqueeze(2).to(torch.bfloat16)/127.5-1
with torch.inference_mode():
    z=pipeline.vae.encode(x).latent_dist.mode()
    y=pipeline.vae.decode(z,temb=torch.tensor([0.05],dtype=torch.bfloat16),return_dict=False)[0]
pixels=y[0,:,0].float().permute(1,2,0).clamp(-1,1).add(1).mul(127.5).round().byte().numpy()
Image.fromarray(pixels).save(OUT/'vae-roundtrip.png')
image.save(OUT/'vae-input.png')
embeds=load_file(str(OUT/'prompt.safetensors'))
result={'seconds':time.monotonic()-started,'latent_shape':list(z.shape),
    'latent_mean':z.float().mean().item(),'latent_std':z.float().std().item(),
    'output_finite':bool(torch.isfinite(y).all()),
    'reconstruction_mae_255':float(np.abs(pixels.astype(float)-np.array(image).astype(float)).mean()),
    'prompt_finite':bool(torch.isfinite(embeds['prompt_embeds']).all()),
    'prompt_mean':embeds['prompt_embeds'].float().mean().item(),
    'prompt_std':embeds['prompt_embeds'].float().std().item()}
(OUT/'vae-roundtrip.json').write_text(json.dumps(result,indent=2))
(OUT/'scheduler-sign-test.json').write_text(json.dumps(validate_corrected_step(),indent=2))
print(json.dumps(result,indent=2))
