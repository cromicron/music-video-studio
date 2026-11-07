"""Offline integrity/coverage/codec tests; no model download or GPU inference."""
import ast
import base64
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch

os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', USE_TF='0', USE_FLAX='0')
import bootstrap
import common
import prepare_bundle
import run


class Diagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.bundle = cls.root / 'input'
        prepare_bundle.prepare(cls.bundle)
        cls.manifest = json.loads((cls.bundle / 'pilot.json').read_text())
        cls.backend = cls.root / 'backend'
        cls.patches = common.prepare_backend(cls.bundle, cls.backend)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_exact_private_job_and_pcm(self):
        common.verify_package(self.bundle)
        actual = common.validate_manifest(self.manifest, self.bundle)
        self.assertEqual(actual, {'samples': 194000, 'sample_rate': 48000, 'channels': 2, 'sample_width_bytes': 2})
        self.assertEqual((self.manifest['frames'] - 1) % 8, 0)
        self.assertEqual(self.manifest['width'] % 64, 0)
        self.assertEqual(self.manifest['height'] % 64, 0)

    def test_batch_public_bad_hash_and_frame_changes_fail(self):
        changes = [{'takes': 2}, {'privacy': 'public'}, {'frames': 96}, {'frames': 105}, {'fps': 30},
                   {'width': 864}, {'seed': 73}, {'end_image': 'bridge_end.png'},
                   {'image_sha256': '0' * 64}, {'audio': '../escape.wav'},
                   {'audio_pcm': {'samples': 193999, 'sample_rate': 48000, 'channels': 2, 'sample_width_bytes': 2}}]
        for values in changes:
            with self.subTest(values=values), self.assertRaises(ValueError):
                common.validate_manifest({**self.manifest, **values}, self.bundle)

    def test_runtime_dependency_and_source_tampering_fail(self):
        altered = self.root / 'tamper'; shutil.copytree(self.bundle, altered)
        with (altered / 'requirements.txt').open('a') as file:
            file.write('\nunexpected-package\n')
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
            common.verify_package(altered)
        (altered / 'vendor/wangp-source.zip.b64').write_bytes(base64.b64encode(b'changed'))
        with self.assertRaisesRegex(ValueError, 'archive hash'):
            common.prepare_backend(altered, self.root / 'bad-backend')

    def test_all_precision_patches_apply_exactly_or_document_absence(self):
        self.assertEqual(len(self.patches), 13)
        absent = [x for x in self.patches if x['matches'] == 0]
        self.assertEqual([x['id'] for x in absent], ['teamaiq-line2'])
        for path in self.backend.rglob('*.py'):
            compile(path.read_bytes(), str(path), 'exec')
        altered = self.root / 'bad-patch'; shutil.copytree(self.bundle, altered)
        rules = json.loads((altered / 'patches.json').read_text())
        rules[0]['expected_count'] = 2
        common.save_json(altered / 'patches.json', rules)
        with self.assertRaisesRegex(ValueError, 'patch assertion'):
            common.prepare_backend(altered, self.root / 'bad-patched-backend')

    def test_actual_backend_audio_branch_rejects_prefix_and_preserves_full_span(self):
        import torch
        tree = ast.parse((self.backend / 'models/ltx2/ltx2.py').read_bytes())
        # Execute the patched backend statements, not a reimplementation of the condition.
        statements = None
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                for index, item in enumerate(node.orelse):
                    if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'target_frames' for t in item.targets):
                        statements = node.orelse[index:]
        self.assertIsNotNone(statements)
        code = compile(ast.fix_missing_locations(ast.Module(body=statements, type_ignores=[])), '<actual-backend-coverage>', 'exec')
        class Full:
            def __init__(self, latent, strength):
                self.shape, self.strength = tuple(latent.shape), strength
        for count in [100, 101, 102]:
            namespace = {'target_shape': types.SimpleNamespace(frames=101), 'audio_latent': torch.zeros(1, 8, count, 16),
                         'audio_strength': 1.0, 'self': types.SimpleNamespace(), 'json': json, 'AudioConditionByLatent': Full}
            if count < 101:
                with self.assertRaisesRegex(ValueError, 'prefix fallback forbidden'):
                    exec(code, namespace)
            else:
                exec(code, namespace)
                result = namespace['audio_conditionings'][0]
                self.assertEqual(result.shape, (1, 8, 101, 16))
                self.assertEqual(result.strength, 1.0)
        distilled = (self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text()
        self.assertIn('stage_2_audio_conditionings = audio_conditionings if audio_conditionings_stage2 is None', distilled)

    def test_hardware_failure_precedes_any_weight_download(self):
        import torch
        with patch.object(torch.cuda, 'is_available', return_value=False), patch('common.download_weights') as download:
            with self.assertRaisesRegex(RuntimeError, 'two CUDA Tesla T4'):
                run.preflight(self.root, self.root, self.backend)
            download.assert_not_called()

    def test_disk_failure_precedes_hub_download(self):
        import huggingface_hub
        lock = json.loads((self.bundle / 'model-lock.json').read_text())
        self.assertEqual(len(lock['files']), 18)
        self.assertEqual(sum(item['bytes'] for item in lock['files']), 35379235525)
        with patch.object(common.shutil, 'disk_usage', return_value=types.SimpleNamespace(free=1)), \
             patch.object(huggingface_hub, 'hf_hub_download') as download:
            with self.assertRaisesRegex(RuntimeError, 'before download'):
                common.download_weights(lock, self.root / 'weights-never-downloaded')
            download.assert_not_called()

    def test_exact_allowlist_pin_anonymous_and_bad_download_fail(self):
        import hashlib
        import huggingface_hub
        content = b'synthetic-test-not-model-weights'
        lock = {'repository': 'test/no-network', 'revision': 'a' * 40, 'cache_reserve_bytes': 0,
                'files': [{'path': 'fixture.dat', 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}]}
        target = self.root / 'synthetic'
        def fake_download(**kwargs):
            self.assertIs(kwargs['token'], False)
            self.assertEqual(kwargs['revision'], 'a' * 40)
            self.assertEqual(kwargs['filename'], 'fixture.dat')
            (Path(kwargs['local_dir']) / kwargs['filename']).write_bytes(content)
        with patch.object(huggingface_hub, 'hf_hub_download', side_effect=fake_download) as download:
            common.download_weights(lock, target)
            download.assert_called_once()
            (target / 'fixture.dat').write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError, 'size/hash mismatch'):
                common.download_weights(lock, target)

    def test_proven_bootstrap_functions_preserved(self):
        original = common.HERE.parent / 'kaggle/bootstrap.py'
        def functions(path):
            return {node.name: ast.dump(node) for node in ast.parse(path.read_text()).body if isinstance(node, ast.FunctionDef)}
        before, after = functions(original), functions(common.HERE / 'bootstrap.py')
        for name in ['run_bounded', 'torch_constraints', 'install_environment']:
            self.assertEqual(before[name], after[name])
        commands = []
        with patch.object(bootstrap, 'run_bounded', side_effect=lambda cmd, **kw: commands.append(cmd)):
            bootstrap.install_environment(self.root / 'venv', self.root / 'requirements', self.root / 'constraints',
                                          deadline=time.monotonic() + 1, log=self.root / 'install.log')
        self.assertIn('--without-pip', commands[0])
        self.assertIn('--system-site-packages', commands[0])
        self.assertIn('--python', commands[1])
        self.assertIn('-c', commands[2])

    def test_whole_job_timeout_and_command_failures(self):
        started = time.monotonic()
        with self.assertRaises(TimeoutError):
            bootstrap.run_bounded([sys.executable, '-c', 'import time; time.sleep(30)'],
                                  deadline=time.monotonic() + 0.2, log=self.root / 'timeout.log')
        self.assertLess(time.monotonic() - started, 5)
        with self.assertRaises(subprocess.CalledProcessError):
            bootstrap.run_bounded([sys.executable, '-c', 'raise SystemExit(7)'],
                                  deadline=time.monotonic() + 5, log=self.root / 'fail.log')

    def test_notebook_private_outputless_and_no_public_launch(self):
        metadata = json.loads((common.HERE / 'kernel-metadata.json').read_text())
        self.assertIs(metadata['is_private'], True)
        notebook = json.loads((common.HERE / 'private-diagnostic.ipynb').read_text())
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertNotIn('launch(', ''.join(cell['source']))
                compile(''.join(cell['source']), '<notebook>', 'exec')
        self.assertNotIn('import gradio', (common.HERE / 'runtime.py').read_text())

    def test_provider_metadata_titles_meet_six_to_fifty_character_limit(self):
        for path in [self.bundle / 'dataset-metadata.json', common.HERE / 'kernel-metadata.json']:
            with self.subTest(metadata=path.name):
                title = json.loads(path.read_text())['title']
                self.assertIsInstance(title, str)
                self.assertEqual(title, title.strip())
                self.assertGreaterEqual(len(title), 6)
                self.assertLessEqual(len(title), 50)

    def test_simulated_kaggle_mount_without_transport_metadata_validates(self):
        mounted = self.root / 'mounted-without-transport-metadata'
        shutil.copytree(self.bundle, mounted)
        (mounted / 'dataset-metadata.json').unlink()
        lock = common.verify_package(mounted)
        self.assertNotIn('dataset-metadata.json', lock['files'])
        self.assertNotIn('vendor/.gitignore', lock['files'])
        self.assertFalse((mounted / 'vendor/.gitignore').exists())
        self.assertFalse((mounted / 'vendor/wangp-source.zip').exists())
        self.assertTrue((mounted / 'vendor/wangp-source.zip.b64').is_file())
        common.validate_manifest(self.manifest, mounted)
        result = subprocess.run([sys.executable, str(mounted / 'run.py'), '--manifest',
                                 str(mounted / 'pilot.json'), '--validate-only'],
                                capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)['valid'])
        patches = common.prepare_backend(mounted, self.root / 'backend-from-mounted-base64')
        self.assertEqual(len(patches), 13)

    def test_base64_transport_rejects_invalid_data_and_preserves_canonical_archive(self):
        canonical = common.HERE / 'vendor/wangp-source.zip'
        before = common.sha256(canonical)
        transport = (self.bundle / 'vendor/wangp-source.zip.b64').read_bytes()
        self.assertEqual(base64.b64decode(transport, validate=True), canonical.read_bytes())
        self.assertEqual(common.sha256(canonical), before)
        damaged = self.root / 'bad-base64'; shutil.copytree(self.bundle, damaged)
        (damaged / 'vendor/wangp-source.zip.b64').write_bytes(b'!invalid base64!')
        with self.assertRaisesRegex(ValueError, 'Invalid Base64'):
            common.prepare_backend(damaged, self.root / 'backend-from-bad-base64')

    def test_actual_codec_exact_frames_and_original_pcm_mux(self):
        import numpy as np
        import wave
        frames = np.zeros((97, 512, 896, 3), dtype=np.uint8)
        frames[:, 100:140, 200:240, 0] = 200
        silent = self.root / 'synthetic-video.mp4'
        run.encode_video(frames, silent, 24)
        self.assertEqual(run.check_video(silent)['frames'], 97)
        review = self.root / 'synthetic-review.mkv'
        audio = self.bundle / self.manifest['audio']
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(silent), '-i', str(audio),
                        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(review)], check=True)
        decoded = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(review), '-map', '0:a:0',
                                           '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
        with wave.open(str(audio), 'rb') as original:
            self.assertEqual(decoded, original.readframes(original.getnframes()))

    def test_actual_gguf_cpu_quantization_against_numpy_reference(self):
        sys.path.insert(0, str(self.backend))
        import numpy as np
        import torch
        import gguf
        import shared.qtypes.gguf as adapter
        for qtype in [gguf.GGMLQuantizationType.Q4_K, gguf.GGMLQuantizationType.Q6_K]:
            block, size = gguf.GGML_QUANT_SIZES[qtype]
            raw = np.zeros((4, size), dtype=np.uint8)
            if qtype == gguf.GGMLQuantizationType.Q4_K:
                raw[:, :2] = np.frombuffer(np.float16(0.125).tobytes(), np.uint8)
                raw[:, 4:] = 17
            else:
                raw[:, -2:] = np.frombuffer(np.float16(0.125).tobytes(), np.uint8)
                raw[:, :-2] = 17
            reference = torch.from_numpy(gguf.quants.dequantize(raw, qtype)).reshape(4, block).float()
            weight = adapter.GGUFWeightTensor.create(torch.from_numpy(raw), (4, block), (block, 1),
                                                    torch.float32, tensor_type=qtype, tensor_shape=(4, block))
            values = torch.linspace(-0.5, 0.5, block).reshape(1, block)
            self.assertTrue(torch.allclose(weight.linear(values), torch.nn.functional.linear(values, reference), atol=0.01))

    def test_actual_gemma_precision_patch_and_cpu_bf16_forward(self):
        import runtime
        import torch
        from transformers import Gemma3TextConfig, Gemma3ForCausalLM
        self.assertTrue(runtime.patch_transformers()['sdpa_module_and_dispatch_alignment'])
        config = Gemma3TextConfig(vocab_size=128, hidden_size=128, intermediate_size=256, num_hidden_layers=1,
                                 num_attention_heads=4, num_key_value_heads=2, head_dim=32,
                                 max_position_embeddings=128, sliding_window=64)
        config._attn_implementation = 'sdpa'
        model = Gemma3ForCausalLM(config).to(torch.bfloat16).eval()
        with torch.inference_mode():
            hidden = model(torch.ones(1, 8, dtype=torch.long), output_hidden_states=True).hidden_states[-1]
        self.assertEqual(hidden.dtype, torch.bfloat16)
        self.assertTrue(torch.isfinite(hidden).all())

    def test_precision_patch_is_idempotent_and_dispatch_stays_single_wrapped(self):
        import runtime
        import transformers.models.gemma3.modeling_gemma3 as gemma
        import transformers.integrations.sdpa_attention as sdpa
        from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS
        runtime.patch_transformers()
        rope, attention = gemma.apply_rotary_pos_emb, sdpa.sdpa_attention_forward
        runtime.patch_transformers()
        self.assertIs(gemma.apply_rotary_pos_emb, rope)
        self.assertIs(sdpa.sdpa_attention_forward, attention)
        self.assertIs(ALL_ATTENTION_FUNCTIONS['sdpa'], attention)
        self.assertFalse(hasattr(attention._jml_original, '_jml_original'))
        self.assertFalse(hasattr(rope._jml_original, '_jml_original'))
        with patch.object(sdpa, 'sdpa_attention_forward', attention._jml_original):
            with self.assertRaisesRegex(RuntimeError, 'Partial or displaced'):
                runtime.patch_transformers()

    def test_actual_padded_gemma_hidden_states_unchanged_when_cache_disabled_and_model_released(self):
        import collections
        import runtime
        import torch
        import weakref
        from tokenizers import Tokenizer, models, pre_tokenizers
        from transformers import Gemma3TextConfig, Gemma3ForCausalLM, PreTrainedTokenizerFast
        runtime.patch_transformers()
        # Use the actual pinned tokenize_with_weights and encode_raw methods with a tiny local
        # Gemma and synthetic vocabulary: 133 active tokens + all 891 left-pad positions.
        tok_tree = ast.parse((self.backend / 'models/ltx2/ltx_core/text_encoders/gemma/tokenizer.py').read_text())
        enc_tree = ast.parse((self.backend / 'models/ltx2/ltx_core/text_encoders/gemma/encoders/base_encoder.py').read_text())
        tok_class = next(n for n in tok_tree.body if isinstance(n, ast.ClassDef) and n.name == 'LTXVGemmaTokenizer')
        enc_class = next(n for n in enc_tree.body if isinstance(n, ast.ClassDef) and n.name == 'GemmaTextEncoderModelBase')
        raw_fn = next(n for n in enc_class.body if isinstance(n, ast.FunctionDef) and n.name == 'encode_raw')
        raw_type = collections.namedtuple('RawTextEmbeddings', 'hidden_states attention_mask padding_side')
        namespace = {'torch': torch, 'RawTextEmbeddings': raw_type}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[tok_class, raw_fn], type_ignores=[])), '<pinned-encoder>', 'exec'), namespace)
        backend_tokenizer = namespace['LTXVGemmaTokenizer'].__new__(namespace['LTXVGemmaTokenizer'])
        tokenizer = Tokenizer(models.WordLevel({'<pad>': 0, '<unk>': 1, 'token': 2}, unk_token='<unk>'))
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        backend_tokenizer.tokenizer = PreTrainedTokenizerFast(tokenizer_object=tokenizer, pad_token='<pad>', unk_token='<unk>',
                                                             padding_side='left', model_max_length=1024)
        backend_tokenizer.max_length = 1024
        config = Gemma3TextConfig(vocab_size=128, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                                 num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                                 max_position_embeddings=2048, sliding_window=1024,
                                 layer_types=['sliding_attention', 'full_attention'], use_cache=True)
        config._attn_implementation = 'sdpa'
        encoder = types.SimpleNamespace(model=Gemma3ForCausalLM(config).to(torch.bfloat16).eval().requires_grad_(False),
                                        tokenizer=backend_tokenizer)
        encoder.encode_raw = types.MethodType(namespace['encode_raw'], encoder)
        prompt = ' '.join(['token'] * 133)
        with torch.inference_mode():
            original = encoder.encode_raw(prompt)
        components = {'video_encoder': torch.nn.Linear(3, 4).float(), 'spatial_upsampler': torch.nn.Linear(4, 2).float()}
        before = {k: {n: p.clone() for n, p in v.state_dict().items()} for k, v in components.items()}
        reference = weakref.ref(encoder.model)
        state = runtime.install_sequential_text_phase(encoder, components, text_device='cpu', context_device='cpu')
        self.assertFalse(encoder.model.config.use_cache)
        with self.assertRaisesRegex(ValueError, 'truncation forbidden'):
            encoder.encode_raw(' '.join(['token'] * 1025))
        self.assertFalse(state['complete'])
        with torch.inference_mode():
            actual = encoder.encode_raw(prompt)
        self.assertIsNone(reference())
        self.assertIsNone(encoder.model)
        self.assertEqual((state['prompt_tokens'], state['padded_tokens']), (133, 1024))
        self.assertTrue(torch.equal(actual.attention_mask, original.attention_mask))
        self.assertEqual(actual.padding_side, original.padding_side)
        self.assertEqual(len(actual.hidden_states), len(original.hidden_states))
        for a, b in zip(actual.hidden_states, original.hidden_states, strict=True):
            self.assertEqual(a.shape[1], 1024)
            self.assertEqual(a.dtype, torch.bfloat16)
            self.assertTrue(torch.equal(a, b), 'Disabling KV cache changed hidden-state conditioning')
        for key, component in components.items():
            for name, value in component.state_dict().items():
                self.assertTrue(torch.equal(value, before[key][name]))
        self.assertEqual([e['phase'] for e in state['events']], ['before_gemma_video_components_on_cpu',
                         'gemma_released_contexts_transferred', 'video_components_staged_after_gemma'])
        with self.assertRaisesRegex(RuntimeError, 'exactly one text encoding'):
            encoder.encode_raw(prompt)

    def test_pinned_pipeline_finishes_text_before_video_encoder_and_uses_one_prompt(self):
        tree = ast.parse((self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text())
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        text = [n.lineno for n in calls if isinstance(n.func, ast.Name) and n.func.id == 'encode_text']
        video = [n.lineno for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == '_get_model'
                 and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == 'video_encoder']
        connectors = [n.lineno for n in calls if isinstance(n.func, ast.Name) and n.func.id == 'resolve_text_connectors']
        self.assertEqual(len(text), 1)
        self.assertEqual(len(video), 1)
        self.assertLess(connectors[0], text[0])
        self.assertLess(text[0], video[0])
        source = (self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text()
        self.assertIn('NAG_scale: float = 1.0', source)
        self.assertIn('contexts = self.text_encoder_cache.encode(encode_fn, [prompt], device=self.device, parallel=True)', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
