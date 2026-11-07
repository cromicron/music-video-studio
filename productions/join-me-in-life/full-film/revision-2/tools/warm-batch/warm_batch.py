"""EXPERIMENTAL: fixed-prompt warm batches over the unchanged pinned I2V runtime.

No CLI, scheduler, download, fallback or acceptance. Neural equivalence has not
been tested. A root-scheduled job must perform the README's matched experiment.
"""
from __future__ import annotations

import copy
import gc
import hashlib
import json
from pathlib import Path
import time
import weakref


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify_bindings(runtime, bundle, backend, lock):
    """Existing prepare_backend/verify_package remain prerequisites, not replaced."""
    require(sha(runtime.__file__) == lock["runtime_sha256"], "Standalone runtime changed")
    for name, expected in lock["bundle_files"].items():
        require(sha(Path(bundle) / name) == expected, f"Bundle binding changed: {name}")
    for name, expected in lock["prepared_backend_files"].items():
        require(sha(Path(backend) / name) == expected, f"Prepared backend binding changed: {name}")


def image_binding(image):
    require(image.mode == "RGB" and image.size == (896, 512), "Use the unchanged run.fit_image RGB output")
    return hashlib.sha256(image.tobytes()).hexdigest()


def freeze_entries(entries, lock):
    require(isinstance(entries, list) and entries, "Explicit nonempty batch required")
    frozen = {}
    for entry in entries:
        m = copy.deepcopy(entry["manifest"])
        require(m["take_id"] not in frozen, "Duplicate take ID")
        require(isinstance(m.get("prompt"), str) and m["prompt"].strip(), "Missing exact prompt")
        for name in ("seed", "height", "width", "fps"):
            require(m.get(name) == lock["fixed_generation"][name], f"Standalone generation setting changed: {name}")
        require(m.get("supplied_audio") is False and m.get("model_audio_output") is False, "This experiment is I2V only")
        require(m.get("end_frame_index") == m["frames"]-1, "Wrong endpoint index")
        require(m.get("NAG_scale", 1.0) == 1.0 and m.get("n_prompt", "") == "", "No guidance/negative-prompt change permitted")
        images = {side: entry[side].copy() for side in ("start_image", "end_image")}
        for side, image in images.items():
            fitting = entry[side.replace("_image", "_fitting")]
            require(fitting["source_sha256"] == m[side+"_sha256"]
                    and fitting["source_dimensions"] == m[side+"_dimensions"]
                    and fitting["rgb_sha256"] == image_binding(image), "Fitted guide differs from its frozen manifest")
        record = {"manifest_sha256": digest_json(m), **{side+"_rgb_sha256": image_binding(im) for side, im in images.items()}}
        frozen[m["take_id"]] = {"manifest": m, **images, "binding": record}
    prompts = list(dict.fromkeys(e["manifest"]["prompt"] for e in frozen.values()))
    require(len(prompts) <= lock["maximum_unique_prompts"], "Bounded experiment permits at most four distinct prompts")
    return frozen, prompts


def cpu_pair(pair):
    import torch
    require(isinstance(pair, (tuple, list)) and len(pair) == 2 and all(torch.is_tensor(t) for t in pair),
            "Expected exactly the existing video/audio context tensors")
    require(all(torch.isfinite(t).all().item() for t in pair), "Non-finite context")
    return tuple(t.detach().to("cpu").contiguous().clone() for t in pair)


def tensor_record(tensor):
    import torch
    return {"shape": list(tensor.shape), "dtype": str(tensor.dtype),
            "bytes": tensor.numel()*tensor.element_size(),
            "sha256": hashlib.sha256(tensor.contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()}


class SealedContextCache:
    """Same encode interface as pinned TextEncoderCache; a miss is fatal."""
    def __init__(self, contexts, binding, max_bytes):
        self._contexts = {prompt: cpu_pair(value) for prompt, value in contexts.items()}
        self.binding = copy.deepcopy(binding)
        self.records = {hashlib.sha256(p.encode()).hexdigest(): [tensor_record(t) for t in pair]
                        for p, pair in self._contexts.items()}
        self.bytes = sum(t["bytes"] for pair in self.records.values() for t in pair)
        require(self.bytes <= max_bytes, "Final CPU context cache exceeds explicit bound")
        self.active_prompt = None
        self.calls = 0

    def encode(self, encode_fn, prompts, device=None, parallel=False, cache_keys=None):
        prompts = [prompts] if isinstance(prompts, str) else list(prompts)
        require(prompts == [self.active_prompt], "Unexpected prompt sequence, negative condition or unbound call")
        require(cache_keys is None or cache_keys == prompts or cache_keys == prompts[0], "Changed cache key semantics")
        require(prompts[0] in self._contexts, "Prompt cache miss after Gemma release; no fallback")
        # Fresh values prevent downstream in-place operations from altering later takes.
        self.calls += 1
        return [tuple(t.clone().to(device) if device is not None else t.clone()
                      for t in self._contexts[p]) for p in prompts]


class TextPhase:
    """Original token/mask/BF16 checks; delay release until all contexts exist."""
    def __init__(self, encoder, components, prompts, text_device="cuda:1", context_device="cuda:0"):
        import torch
        require(not hasattr(encoder, "_jml_text_phase"), "Text phase was already installed")
        self.encoder, self.components = encoder, components
        self.allowed = set(prompts)
        self.text_device, self.context_device = text_device, context_device
        self.model_reference = weakref.ref(encoder.model)
        self.old_raw = encoder.encode_raw
        self.state = {"complete": False, "mode": "experimental_fixed_prompt_warm_batch", "raw_encodes": [],
                      "events": [], "video_parameter_bytes": {}}
        for name, component in components.items():
            require(all(p.device.type == "cpu" and p.dtype == torch.float32 for p in component.parameters()),
                    name + " must remain CPU/FP32 before text encoding")
            self.state["video_parameter_bytes"][name] = sum(p.numel()*p.element_size() for p in component.parameters())
        for module in (encoder.model, getattr(encoder.model, "model", None)):
            if module is not None:
                module.config.use_cache = False
        encoder._jml_text_phase = self.state
        encoder.encode_raw = self.encode_raw

    def record(self, phase):
        import torch
        self.state["events"].append({"phase": phase, "gpu_memory": [
            {"device": i, "allocated": torch.cuda.memory_allocated(i), "reserved": torch.cuda.memory_reserved(i),
             "free": torch.cuda.mem_get_info(i)[0]} for i in range(torch.cuda.device_count())]})

    def encode_raw(self, text, padding_side="left"):
        import torch
        require(not self.state["complete"] and self.encoder.model is not None, "Gemma was already released")
        require(text in self.allowed and padding_side == "left", "Unplanned text/padding side")
        require(not any(r["prompt_sha256"] == hashlib.sha256(text.encode()).hexdigest() for r in self.state["raw_encodes"]),
                "A prompt was unexpectedly encoded twice during prefill")
        for name, component in self.components.items():
            require(all(p.device.type == "cpu" and p.dtype == torch.float32 for p in component.parameters()),
                    name + " overlapped Gemma video residency")
        require(not self.encoder.model.config.use_cache, "Unexpected Gemma KV cache")
        tokenizer = self.encoder.tokenizer
        count = len(tokenizer.tokenizer(text.strip(), truncation=False).input_ids)
        require(count <= tokenizer.max_length, "Prompt truncation forbidden")
        pairs = tokenizer.tokenize_with_weights(text)["gemma"]
        mask = torch.tensor([[int(pair[1]) for pair in pairs]], device=self.context_device)
        require(len(pairs) == tokenizer.max_length and int(mask.sum()) == count, "Changed padded tokenization")
        began = time.monotonic()
        raw = self.old_raw(text, padding_side=padding_side)
        require(raw.padding_side == padding_side and torch.equal(raw.attention_mask.to(self.context_device), mask), "Changed padding mask")
        require(all(h.dtype == torch.bfloat16 and h.shape[1] == len(pairs) for h in raw.hidden_states), "Changed Gemma hidden precision/extent")
        require(all(torch.isfinite(h).all() for h in raw.hidden_states), "Non-finite Gemma hidden state")
        result = raw.__class__(tuple(h.to(device=self.context_device) for h in raw.hidden_states),
                               raw.attention_mask.to(self.context_device), raw.padding_side)
        self.state["raw_encodes"].append({"prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
                                        "tokens": count, "padded_tokens": len(pairs), "seconds": time.monotonic()-began})
        return result

    def release(self):
        import torch
        require(len(self.state["raw_encodes"]) == len(self.allowed), "Not every planned prompt was encoded")
        self.encoder.model = None
        gc.collect()
        require(self.model_reference() is None, "Gemma still referenced; video residency refused")
        torch.cuda.synchronize(torch.device(self.text_device)); torch.cuda.empty_cache()
        self.record("all_contexts_cpu_gemma_released")
        for name, component in self.components.items():
            component.to(device=self.text_device)
            require(all(p.device == torch.device(self.text_device) and p.dtype == torch.float32 for p in component.parameters()),
                    name + " video staging changed")
        self.state["complete"] = True
        self.record("video_components_staged_once")


def prefill_exact(encoder, connectors, prompts, encode_text, postprocess, snapshot=cpu_pair):
    """Each raw prompt is immediately projected; never retain a batch of raw layers."""
    contexts = {}
    for prompt in prompts:
        require(prompt not in contexts, "Prefill prompts must already be unique")
        result = postprocess(encode_text(encoder, prompts=[prompt]), *connectors)
        require(len(result) == 1, "Unexpected context batch extent")
        contexts[prompt] = snapshot(result[0])
        del result
    return contexts


class WarmBatch:
    """Candidate API after unchanged preflight, package validation, fitting and model download."""
    def __init__(self, runtime, model_dir, bundle, backend, entries, lock_path=None):
        import torch
        lock_path = Path(lock_path or Path(__file__).with_name("binding-lock.json"))
        self.lock = json.loads(lock_path.read_text())
        verify_bindings(runtime, bundle, backend, self.lock)
        self.entries, prompts = freeze_entries(entries, self.lock)
        self.binding = {"lock_sha256": sha(lock_path), "entries": {k: v["binding"] for k, v in self.entries.items()},
                        "adapter_sha256": sha(__file__)}
        self.binding["batch_sha256"] = digest_json(self.binding)
        self.runtime, self.failed, self.completed = runtime, False, []
        phases = []
        old_install = runtime.install_sequential_text_phase
        def install(encoder, components, text_device="cuda:1", context_device="cuda:0"):
            phase = TextPhase(encoder, components, prompts, text_device, context_device)
            phases.append(phase)
            return phase.state
        began = time.monotonic()
        try:
            runtime.install_sequential_text_phase = install
            self.model = runtime.load_model(model_dir)
        finally:
            runtime.install_sequential_text_phase = old_install
        require(len(phases) == 1, "Unexpected text hook installation count")
        self.phase = phases[0]
        self.model_load_seconds = time.monotonic()-began
        for index in range(2):
            torch.cuda.synchronize(torch.device(f"cuda:{index}"))
        self.model_load_peak_allocated = [torch.cuda.max_memory_allocated(i) for i in range(2)]
        for index in range(2):
            torch.cuda.reset_peak_memory_stats(index)
        from models.ltx2.ltx_core.text_encoders.gemma.encoders.base_encoder import (
            encode_text, postprocess_text_embeddings, resolve_text_connectors)
        require(self.model.pipeline.models.text_encoder is self.model.text_encoder
                and self.model.pipeline.models.video_encoder is self.model.video_encoder,
                "Unexpected pipeline component ownership")
        began = time.monotonic()
        with torch.inference_mode():
            self.phase.record("prefill_start_video_components_on_cpu")
            connectors = resolve_text_connectors(self.model.text_encoder, self.model._text_connectors)
            contexts = prefill_exact(self.model.text_encoder, connectors, prompts, encode_text, postprocess_text_embeddings)
            self.cache = SealedContextCache(contexts, self.binding, self.lock["maximum_final_context_bytes"])
            del contexts, connectors
            self.model.pipeline.text_encoder_cache = self.cache
            self.phase.release()
        self.prefill_and_stage_seconds = time.monotonic()-began
        self.prefill_peak_allocated = [torch.cuda.max_memory_allocated(i) for i in range(2)]

    def generate_take(self, take_id):
        import torch
        require(not self.failed, "Batch is poisoned after failure; no automatic retry")
        require(take_id in self.entries, "Unplanned take")
        entry = self.entries[take_id]
        require(digest_json(entry["manifest"]) == entry["binding"]["manifest_sha256"], "Manifest changed after cache binding")
        require(all(image_binding(entry[side]) == entry["binding"][side+"_rgb_sha256"] for side in ("start_image", "end_image")),
                "Endpoint image changed after binding")
        require(not self.model._interrupt, "Model retained an interrupted state")
        require(self.model.pipeline.text_encoder_cache is self.cache and self.model.text_encoder.model is None,
                "Warm model/cache residency changed")
        old_calls, began = self.cache.calls, time.monotonic()
        self.cache.active_prompt = entry["manifest"]["prompt"]
        try:
            frames, details = self.runtime.generate(self.model, entry["manifest"], entry["start_image"], entry["end_image"])
            require(self.cache.calls == old_calls+1, "Expected exactly one positive-context cache request")
            details = copy.deepcopy(details)
            gc.collect()
            for index in range(2):
                torch.cuda.synchronize(torch.device(f"cuda:{index}"))
            torch.cuda.empty_cache()
            details["warm_batch"] = {"binding": self.binding, "cache": self.cache.records,
                "context_cpu_bytes": self.cache.bytes, "model_load_seconds_once": self.model_load_seconds,
                "model_load_peak_allocated": self.model_load_peak_allocated,
                "prefill_and_stage_seconds_once": self.prefill_and_stage_seconds,
                "prefill_peak_allocated": self.prefill_peak_allocated,
                "this_call_seconds": time.monotonic()-began, "call_index": len(self.completed),
                "repeat_for_equivalence_test": take_id in self.completed,
                "after_call_gpu_allocated": [torch.cuda.memory_allocated(i) for i in range(2)],
                "negative_condition": "Not encoded: unchanged pinned NAG_scale=1 and empty n_prompt",
                "neural_equivalence": "unproven; matched baseline and A-B-A comparison required"}
            self.completed.append(take_id)
            return frames, details
        except Exception:
            self.failed = True
            raise
        finally:
            self.cache.active_prompt = None
