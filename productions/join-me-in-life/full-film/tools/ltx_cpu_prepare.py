#!/usr/bin/env python3
"""Fetch only official LTX2B/T5 weights and stage T5 shards in BF16.

Temporary downloaded FP32 T5 shards are deleted only after their local BF16
counterpart has been written. Never downloads 13B models or full repositories.
"""
import gc
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
CACHE = ROOT / "build/ltx-cpu"
# Keep public-model download caches with this task, before importing Hub/Xet.
os.environ['HF_HOME']=str(CACHE/'hf')
os.environ['HF_HUB_CACHE']=str(CACHE/'hf/hub')
os.environ['HF_XET_CACHE']=str(CACHE/'hf/xet')

import psutil
import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file
from huggingface_hub import hf_hub_download

CONFIG_REPO = "Lightricks/LTX-Video-0.9.5"
MODEL_REPO = "Lightricks/LTX-Video"
MODEL_FILE = "ltxv-2b-0.9.6-distilled-04-25.safetensors"
REVISIONS = {
    MODEL_REPO: "8984fa25007f376c1a299016d0957a37a2f797bb",
    CONFIG_REPO: "e58e28c39631af4d1468ee57a853764e11c1d37e",
}
MODEL_SHA256 = "94891bd4bd08de30d484befbfc54fdcffe6d1596a131baad700b9baa5e1de86b"
GiB = 1024 ** 3


def log(stage, **values):
    print(json.dumps({"stage": stage, "time": time.time(),
                      "available_gib": round(psutil.virtual_memory().available/GiB, 2),
                      "disk_free_gib": round(shutil.disk_usage(CACHE).free/GiB, 2),
                      **values}), flush=True)


def fetch(repo, name, target, expected_size=None):
    target = Path(target)
    if target.exists() and (expected_size is None or target.stat().st_size == expected_size):
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    if expected_size and shutil.disk_usage(CACHE).free - expected_size < 4 * GiB:
        raise RuntimeError("Download would leave less than 4 GiB disk headroom")
    url = f"https://huggingface.co/{repo}/resolve/{REVISIONS[repo]}/{name}"
    temporary = target.with_suffix(target.suffix + ".partial")
    log("download_start", source=repo+"/"+name, expected_bytes=expected_size)
    start=time.monotonic(); total=0; last=start
    if expected_size and expected_size>100*1024*1024:
        # The official Hub client's Xet transfer was measured faster than one
        # sequential urllib stream. Local-dir files move without another copy.
        downloaded=Path(hf_hub_download(repo,name,revision=REVISIONS[repo],
                                       local_dir=CACHE/'sdk-download'))
        if downloaded.stat().st_size!=expected_size:
            raise RuntimeError('Hub download size differs from the official file listing')
        downloaded.replace(target)
        if temporary.exists():temporary.unlink()
        log('download_complete',file=name,bytes=expected_size,
            seconds=round(time.monotonic()-start,2),method='official_hub_client')
        return target
    with urllib.request.urlopen(url, timeout=45) as response, temporary.open("wb") as out:
        while block := response.read(8*1024*1024):
            out.write(block); total+=len(block)
            if time.monotonic()-last>15:
                log("download_progress", file=name, bytes=total,
                    mb_s=round(total/1e6/(time.monotonic()-start),1)); last=time.monotonic()
            if shutil.disk_usage(CACHE).free < 4*GiB:
                raise RuntimeError("Stopped before disk reserve was exhausted")
    if expected_size and total != expected_size:
        raise RuntimeError(f"Incomplete file: {total} != {expected_size}")
    temporary.replace(target)
    log("download_complete", file=name, bytes=total, seconds=round(time.monotonic()-start,2))
    return target


def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(4)
    config=CACHE/"config"
    for name in ["model_index.json", "scheduler/scheduler_config.json",
                 "transformer/config.json", "vae/config.json", "text_encoder/config.json",
                 "text_encoder/model.safetensors.index.json", "tokenizer/added_tokens.json",
                 "tokenizer/special_tokens_map.json", "tokenizer/spiece.model",
                 "tokenizer/tokenizer_config.json"]:
        fetch(CONFIG_REPO,name,config/name)
    index=json.loads((config/"text_encoder/model.safetensors.index.json").read_text())
    tree=json.load(urllib.request.urlopen(
        f"https://huggingface.co/api/models/{CONFIG_REPO}/tree/{REVISIONS[CONFIG_REPO]}?recursive=true",timeout=30))
    sizes={entry["path"]:entry.get("size",0) for entry in tree}
    # The final shard is the first bounded transfer benchmark and may already
    # be locally cached. Converting it first immediately frees disk headroom.
    for name in sorted(set(index["weight_map"].values()),reverse=True):
        dst=config/"text_encoder"/name
        if dst.exists():
            with safe_open(str(dst),framework='pt',device='cpu') as existing:
                if not list(existing.keys()):raise RuntimeError('Empty converted T5 shard')
            continue
        src=fetch(CONFIG_REPO,"text_encoder/"+name,CACHE/"temporary"/name,
                  sizes["text_encoder/"+name])
        log("convert_start",file=name)
        weights=load_file(str(src),device="cpu")
        reduced={key:value.to(torch.bfloat16) for key,value in weights.items()}
        del weights;gc.collect()
        converted=dst.with_suffix('.bf16.partial')
        save_file(reduced,str(converted),metadata={"format":"pt", "local_modification":"FP32 to BF16 for CPU benchmark"})
        converted.replace(dst)
        del reduced;gc.collect()
        src.unlink()
        log("convert_complete",file=name,bytes=dst.stat().st_size)
    index.setdefault("metadata",{})["total_size"]=sum(
        (config/"text_encoder"/name).stat().st_size for name in set(index["weight_map"].values()))
    (config/"text_encoder/model.safetensors.index.json").write_text(json.dumps(index,indent=2))
    model=fetch(MODEL_REPO,MODEL_FILE,CACHE/MODEL_FILE,6340744028)
    with model.open('rb') as file:
        actual_hash=hashlib.file_digest(file,'sha256').hexdigest()
    if actual_hash!=MODEL_SHA256:
        raise RuntimeError('Checkpoint SHA256 differs from the verified official LFS object')
    log("prepared")


if __name__ == "__main__":main()
