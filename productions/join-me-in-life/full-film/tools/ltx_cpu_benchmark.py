#!/usr/bin/env python3
"""Bounded, CPU-only LTX-Video2B benchmark with separate text/video stages.

Run with --stage text first. Its process must exit before --stage video so the
large T5 encoder does not compete with video inference for RAM. No API calls.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import threading
import time

ROOT=Path(__file__).resolve().parents[4]
CACHE=ROOT/'build/ltx-cpu'
OUT=ROOT/'productions/join-me-in-life/full-film/research/local-cpu-test'
os.environ.setdefault('HF_HOME',str(CACHE/'hf'))
os.environ.setdefault('TOKENIZERS_PARALLELISM','false')

import psutil
import torch

GiB=1024**3
START=time.monotonic()
PROCESS=psutil.Process()
metrics={'started_at':time.time(),'peak_rss_bytes':0,'stage_times':{}}
args=None


def record(event,**details):
    rss=PROCESS.memory_info().rss
    metrics['peak_rss_bytes']=max(metrics['peak_rss_bytes'],rss)
    item={'event':event,'elapsed_s':round(time.monotonic()-START,3),
          'rss_gib':round(rss/GiB,3),
          'available_gib':round(psutil.virtual_memory().available/GiB,3),**details}
    print(json.dumps(item),flush=True)
    with (OUT/(args.stage+'-events.jsonl')).open('a') as file:file.write(json.dumps(item)+'\n')


def watchdog():
    while True:
        rss=PROCESS.memory_info().rss
        metrics['peak_rss_bytes']=max(metrics['peak_rss_bytes'],rss)
        if rss>13.5*GiB or psutil.virtual_memory().available<2*GiB:
            record('STOP_MEMORY_HEADROOM');os._exit(137)
        if time.monotonic()-START>args.max_seconds:
            record('STOP_TIME_BUDGET',limit_s=args.max_seconds);os._exit(124)
        time.sleep(1)


def text_stage():
    from transformers import T5EncoderModel,T5Tokenizer
    from safetensors.torch import save_file
    record('text_load_begin')
    tokenizer=T5Tokenizer.from_pretrained(CACHE/'config/tokenizer',local_files_only=True)
    encoder=T5EncoderModel.from_pretrained(CACHE/'config/text_encoder',
        dtype=torch.bfloat16,low_cpu_mem_usage=True,local_files_only=True).eval()
    record('text_load_complete')
    prompt=Path(args.prompt_file).read_text().strip()
    inputs=tokenizer([prompt],padding='max_length',max_length=256,truncation=True,
                     add_special_tokens=True,return_tensors='pt')
    with torch.inference_mode():
        embeds=encoder(inputs.input_ids,attention_mask=inputs.attention_mask.bool())[0]
    save_file({'prompt_embeds':embeds.contiguous(),
               'prompt_attention_mask':inputs.attention_mask.bool().contiguous()},
              str(OUT/'prompt.safetensors'),metadata={'prompt':prompt})
    (OUT/'encoded-prompt.txt').write_text(prompt+'\n')
    record('text_encode_complete',shape=list(embeds.shape))


def video_stage():
    import diffusers
    from diffusers import LTXConditionPipeline
    from ltx_cpu_scheduler import LTXPerTokenStochasticScheduler,validate_corrected_step
    from safetensors.torch import load_file
    from safetensors import safe_open
    from PIL import Image
    from diffusers.utils import export_to_video
    if diffusers.__version__!='0.42.1':
        raise RuntimeError('This benchmark validates the Diffusers 0.42.1 pipeline sign convention; recheck it before changing library versions')
    image=Image.open(args.image).convert('RGB')
    aspect_change=(args.width/args.height)/(image.width/image.height)-1
    if abs(aspect_change)>0.015 and not args.allow_aspect_change:
        raise ValueError(f'Output dimensions would distort source aspect by {aspect_change:.1%}; choose matching dimensions or explicitly pass --allow-aspect-change for a technical test')
    metrics['source_dimensions']=list(image.size)
    metrics['relative_aspect_change']=aspect_change
    record('video_load_begin')
    pipeline=LTXConditionPipeline.from_single_file(
        str(CACHE/'ltxv-2b-0.9.6-distilled-04-25.safetensors'),
        config=str(CACHE/'config'),text_encoder=None,tokenizer=None,
        torch_dtype=torch.bfloat16,local_files_only=True,low_cpu_mem_usage=True)
    scheduler_check=validate_corrected_step()
    (OUT/'scheduler-sign-test.json').write_text(json.dumps(scheduler_check,indent=2))
    pipeline.scheduler=LTXPerTokenStochasticScheduler(shift=1.0,use_dynamic_shifting=False,
        num_train_timesteps=1000,stochastic_sampling=True)
    pipeline.to('cpu')
    pipeline.vae.enable_tiling()
    record('video_load_complete')
    embeddings=load_file(str(OUT/'prompt.safetensors'))
    with safe_open(str(OUT/'prompt.safetensors'),framework='pt',device='cpu') as file:
        prompt_metadata=file.metadata() or {}
    metrics['prompt_text']=prompt_metadata.get('prompt')
    metrics['image_sha256']=hashlib.sha256(Path(args.image).read_bytes()).hexdigest()
    metrics['embedding_sha256']=hashlib.sha256((OUT/'prompt.safetensors').read_bytes()).hexdigest()
    begin=time.monotonic();previous=begin
    def step_callback(pipe,index,timestep,callback_kwargs):
        nonlocal previous
        now=time.monotonic()
        record('denoise_step_complete',step=index+1,timestep=float(timestep),
               step_s=round(now-previous,3),inference_s=round(now-begin,3))
        previous=now
        return callback_kwargs
    # Exact 0.9.6 distilled schedule from the official checkpoint metadata.
    timesteps=[1000,993.7,987.5,981.2,975,909.4,725,421.9]
    record('inference_begin',width=args.width,height=args.height,frames=args.frames,
           timesteps=timesteps)
    # LTXConditionPipeline does not forward its generator into the stochastic
    # scheduler. Seed the global CPU RNG as well as the initial-latent generator.
    torch.manual_seed(args.seed)
    with torch.inference_mode():
        frames=pipeline(image=image,prompt_embeds=embeddings['prompt_embeds'],
            prompt_attention_mask=embeddings['prompt_attention_mask'],
            width=args.width,height=args.height,num_frames=args.frames,frame_rate=24,
            timesteps=timesteps,guidance_scale=1.0,decode_timestep=0.05,
            decode_noise_scale=0.025,image_cond_noise_scale=0.0,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            callback_on_step_end=step_callback).frames[0]
    record('inference_complete',seconds=round(time.monotonic()-begin,3),frames=len(frames))
    export_to_video(frames,str(OUT/f'ltx_cpu_2b_{args.frames}f.mp4'),fps=24)
    record('export_complete')


def main():
    global args,OUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['text','video'],required=True)
    parser.add_argument('--prompt-file',default=str(ROOT/'productions/join-me-in-life/full-film/assets/prompts/her_window.txt'))
    parser.add_argument('--image',default=str(ROOT/'productions/join-me-in-life/full-film/assets/her_window.png'))
    parser.add_argument('--width',type=int,default=512)
    parser.add_argument('--height',type=int,default=288)
    parser.add_argument('--frames',type=int,default=73)
    parser.add_argument('--allow-aspect-change',action='store_true',help='Only for reproducing the historical distorted 384x256 technical prototype')
    parser.add_argument('--seed',type=int,default=49)
    parser.add_argument('--threads',type=int,default=4)
    parser.add_argument('--output-dir',default=str(OUT))
    parser.add_argument('--max-seconds',type=int,default=900)
    args=parser.parse_args();OUT=Path(args.output_dir);OUT.mkdir(parents=True,exist_ok=True)
    if args.width<=0 or args.height<=0 or args.width%32 or args.height%32:
        parser.error('Width and height must be positive multiples of 32')
    if args.frames<9 or (args.frames-1)%8:
        parser.error('Frame count must be 8n+1, with n at least 1')
    if (OUT/(args.stage+'-events.jsonl')).exists() or (OUT/(args.stage+'-metrics.json')).exists():
        parser.error('This stage already has saved evidence; choose a new output directory to preserve earlier results')
    torch.set_num_threads(args.threads);torch.set_num_interop_threads(1)
    metrics.update({'stage':args.stage,'torch':torch.__version__,'threads':args.threads,
                    'seed':args.seed,'global_stochastic_rng_seeded':True,
                    'width':args.width,'height':args.height,'frames':args.frames})
    threading.Thread(target=watchdog,daemon=True).start()
    record('start')
    try:
        text_stage() if args.stage=='text' else video_stage()
        metrics['status']='completed'
    except Exception as error:
        metrics['status']='error';metrics['error']=repr(error)
        record('error',error=repr(error));raise
    finally:
        metrics['elapsed_seconds']=time.monotonic()-START
        (OUT/(args.stage+'-metrics.json')).write_text(json.dumps(metrics,indent=2))


if __name__=='__main__':main()
