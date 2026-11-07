"""Offline protocol/source tests only. No torch, model weights or CUDA are loaded."""
import ast
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import warm_batch as warm

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2] / "tools/kaggle-story23"
LOCK = json.loads((HERE / "binding-lock.json").read_text())


class Image:
    mode = "RGB"
    size = (896, 512)
    def __init__(self, value): self.value = value
    def copy(self): return copy.deepcopy(self)
    def tobytes(self): return self.value.encode()


class Tensor:
    def __init__(self, value, device="cpu"): self.value, self.device = value, device
    def clone(self): return copy.deepcopy(self)
    def to(self, device): self.device = device; return self


def fixture_entry(take="A", prompt="A hand moves the cup."):
    value = {"manifest": {"take_id": take, "prompt": prompt, "seed": 49, "width": 896,
                         "height": 512, "fps": 24, "frames": 169, "end_frame_index": 168,
                         "supplied_audio": False, "model_audio_output": False},
            "start_image": Image("start"), "end_image": Image("end")}
    for side in ("start", "end"):
        value["manifest"][side+"_image_sha256"] = side+"-original-file-hash"
        value["manifest"][side+"_image_dimensions"] = [1024, 768]
        value[side+"_fitting"] = {"source_sha256": side+"-original-file-hash", "source_dimensions": [1024, 768],
                               "rgb_sha256": warm.image_binding(value[side+"_image"])}
    return value


class WarmBatchTest(unittest.TestCase):
    def cache(self):
        with patch.object(warm, "cpu_pair", side_effect=lambda pair: tuple(t.clone() for t in pair)), \
             patch.object(warm, "tensor_record", side_effect=lambda t: {"bytes": 8, "value": t.value}):
            return warm.SealedContextCache({"a": (Tensor(10), Tensor(20)), "b": (Tensor(30), Tensor(40))},
                                           {"exact_model": "fixture"}, 64)

    def test_exact_batch_prompt_image_seed_binding(self):
        original = fixture_entry()
        frozen, prompts = warm.freeze_entries([original, fixture_entry("B")], LOCK)
        self.assertEqual(prompts, [original["manifest"]["prompt"]])
        original["manifest"]["prompt"] = "changed"
        original["start_image"].value = "changed"
        self.assertEqual(frozen["A"]["manifest"]["prompt"], prompts[0])
        self.assertEqual(frozen["A"]["start_image"].tobytes(), b"start")

    def test_changed_seed_or_negative_guidance_rejected(self):
        for key, value in [("seed", 50), ("NAG_scale", 2.0), ("n_prompt", "new condition")]:
            entry = fixture_entry(); entry["manifest"][key] = value
            with self.assertRaises(ValueError): warm.freeze_entries([entry], LOCK)

    def test_wrong_fitted_guide_is_rejected(self):
        entry = fixture_entry(); entry["start_image"].value = "different image"
        with self.assertRaisesRegex(ValueError, "Fitted guide differs"):
            warm.freeze_entries([entry], LOCK)

    def test_unbounded_prompt_bank_rejected(self):
        with self.assertRaisesRegex(ValueError, "four distinct"):
            warm.freeze_entries([fixture_entry(str(i), str(i)) for i in range(5)], LOCK)

    def test_prefill_uses_exact_helpers_one_prompt_at_a_time(self):
        calls = []
        def encode(encoder, prompts):
            calls.append(("encode", encoder, prompts)); return [prompts[0]+" raw"]
        def post(raw, *connectors):
            calls.append(("post", raw, connectors)); return [(raw[0]+" video", raw[0]+" audio")]
        result = warm.prefill_exact("encoder", ("projection", "video", "audio"), ["a", "b"], encode, post,
                                   snapshot=lambda value: value)
        self.assertEqual([c[0] for c in calls], ["encode", "post", "encode", "post"])
        self.assertEqual(calls[0], ("encode", "encoder", ["a"]))
        self.assertEqual(calls[1][2], ("projection", "video", "audio"))
        self.assertEqual(result["b"], ("b raw video", "b raw audio"))

    def test_cache_hit_preserves_values_and_protects_against_mutation(self):
        cache = self.cache(); cache.active_prompt = "a"
        def forbidden(*args): raise AssertionError("Encoder fallback invoked")
        first = cache.encode(forbidden, ["a"], device="cuda:0", parallel=True)
        self.assertEqual([t.value for t in first[0]], [10, 20])
        first[0][0].value = 999
        second = cache.encode(forbidden, ["a"], device="cuda:0", parallel=True)
        self.assertEqual([t.value for t in second[0]], [10, 20])
        self.assertEqual(cache.calls, 2)

    def test_cache_miss_negative_condition_and_alias_never_fallback(self):
        cache = self.cache()
        def forbidden(*args): raise AssertionError("Encoder fallback invoked")
        cache.active_prompt = "missing"
        with self.assertRaisesRegex(ValueError, "cache miss"):
            cache.encode(forbidden, ["missing"])
        cache.active_prompt = "a"
        with self.assertRaisesRegex(ValueError, "negative condition"):
            cache.encode(forbidden, ["a", "b"])
        with self.assertRaisesRegex(ValueError, "cache key"):
            cache.encode(forbidden, ["a"], cache_keys=["b"])

    def test_cache_byte_limit_is_enforced(self):
        with patch.object(warm, "cpu_pair", side_effect=lambda pair: tuple(t.clone() for t in pair)), \
             patch.object(warm, "tensor_record", return_value={"bytes": 1024}):
            with self.assertRaisesRegex(ValueError, "exceeds explicit bound"):
                warm.SealedContextCache({"a": (Tensor(1), Tensor(2))}, {}, 100)

    def test_exact_pinned_runtime_forward_parameters(self):
        source = (BASE / "runtime.py").read_text()
        self.assertEqual(hashlib.sha256(source.encode()).hexdigest(), LOCK["runtime_sha256"])
        tree = ast.parse(source)
        generate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "generate")
        calls = [n for n in ast.walk(generate) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and isinstance(n.func.value, ast.Name) and n.func.value.id == "model" and n.func.attr == "generate"]
        self.assertEqual(len(calls), 1)
        values = {k.arg: ast.literal_eval(k.value) for k in calls[0].keywords if isinstance(k.value, ast.Constant)}
        for key in ("seed", "height", "width", "fps", "n_prompt", "audio_cfg_scale", "guide_scale", "alt_guide_scale", "sampling_steps", "guide_phases"):
            self.assertEqual(values[key], LOCK["fixed_generation"][key])
        self.assertNotIn("NAG_scale", {k.arg for k in calls[0].keywords})

    def test_prepared_backend_lock_matches_existing_patches(self):
        rules = json.loads((BASE / "patches.json").read_text())
        with ZipFile(BASE / "vendor/wangp-source.zip") as archive:
            for name, expected in LOCK["prepared_backend_files"].items():
                source = archive.read(name).decode()
                for rule in rules:
                    if rule["path"] == name:
                        self.assertEqual(source.count(rule["old"]), rule["expected_count"])
                        if rule["expected_count"]:
                            source = source.replace(rule["old"], rule["new"])
                self.assertEqual(hashlib.sha256(source.encode()).hexdigest(), expected)
            source = archive.read("models/ltx2/ltx2.py").decode()
            cls = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == "LTX2")
            method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "generate")
            defaults = dict(zip([a.arg for a in method.args.args][-len(method.args.defaults):], method.args.defaults))
            self.assertEqual(ast.literal_eval(defaults["NAG_scale"]), 1.0)


if __name__ == "__main__": unittest.main()
