"""Offline I2V wrapper/actual-source/codec checks. No downloads or model inference."""
import ast
import base64
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
import runtime


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
        sys.path.insert(0, str(cls.backend))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_private_exact_inputs_lattice_and_no_audio(self):
        common.verify_package(self.bundle)
        actual = common.validate_manifest(self.manifest, self.bundle)
        self.assertEqual(actual, {'start_image': [1916, 1080], 'end_image': [1672, 941]})
        self.assertEqual((self.manifest['frames'] - 1) % 8, 0)
        self.assertEqual(self.manifest['end_frame_index'], 144)
        self.assertFalse(list(self.bundle.glob('*.wav')))
        self.assertFalse(list(self.bundle.glob('*.mp3')))
        self.assertFalse(self.manifest['supplied_audio'])
        self.assertFalse(self.manifest['model_audio_output'])

    def test_changed_scope_hash_dimensions_end_position_and_audio_fail(self):
        for values in [{'privacy': 'public'}, {'takes': 2}, {'frames': 144}, {'frames': 153}, {'fps': 30},
                       {'seed': 50}, {'width': 864}, {'end_frame_index': 145}, {'start_frame_index': 1},
                       {'end_image_sha256': '0' * 64}, {'end_image_dimensions': [1916, 1080]},
                       {'audio': 'made-up.wav'}, {'supplied_audio': True}, {'model_audio_output': True}]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                common.validate_manifest({**self.manifest, **values}, self.bundle)

    def test_base64_mounted_tree_and_corrupt_package_fail(self):
        mounted = self.root / 'mounted'; shutil.copytree(self.bundle, mounted)
        (mounted / 'dataset-metadata.json').unlink()
        lock = common.verify_package(mounted)
        self.assertNotIn('dataset-metadata.json', lock['files'])
        self.assertFalse((mounted / 'vendor/wangp-source.zip').exists())
        transport = mounted / 'vendor/wangp-source.zip.b64'
        self.assertEqual(base64.b64decode(transport.read_bytes(), validate=True),
                         (common.HERE / 'vendor/wangp-source.zip').read_bytes())
        self.assertEqual(len(common.prepare_backend(mounted, self.root / 'mounted-backend')), 13)
        cli = subprocess.run([sys.executable, str(mounted / 'run.py'), '--manifest', str(mounted / 'pilot.json'),
                              '--validate-only'], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(cli.stdout)['frames'], 145)
        transport.write_bytes(b'invalid!!!')
        with self.assertRaisesRegex(ValueError, 'Invalid Base64'):
            common.prepare_backend(mounted, self.root / 'bad-base64')
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
            common.verify_package(mounted)

    def test_shared_successful_residency_source_locks_and_audio_gate_are_preserved(self):
        a2v = common.HERE.with_name('kaggle-a2v')
        for name in ['requirements.txt', 'source-lock.json', 'model-lock.json', 'patches.json']:
            self.assertEqual((common.HERE / name).read_bytes(), (a2v / name).read_bytes())
        def functions(path):
            return {n.name: ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef)}
        ours, previous = functions(common.HERE / 'runtime.py'), functions(a2v / 'runtime.py')
        for name in ['require_finite', 'patch_transformers', 'install_sequential_text_phase',
                     'configure_attention', 'smoke_quantization', 'load_model']:
            self.assertEqual(ours[name], previous[name], name)
        ours, previous = functions(common.HERE / 'bootstrap.py'), functions(a2v / 'bootstrap.py')
        for name in ['run_bounded', 'torch_constraints', 'install_environment']:
            self.assertEqual(ours[name], previous[name])
        self.assertEqual(functions(common.HERE / 'run.py')['preflight'], functions(a2v / 'run.py')['preflight'])
        self.assertIn('No verified full supplied-audio conditioning record', (a2v / 'runtime.py').read_text())
        self.assertIn('Audio does not cover the entire video', (a2v / 'common.py').read_text())

    def test_actual_backend_builds_both_endpoint_entries_and_both_stage_calls_preserve_them(self):
        # Execute the pinned backend's real entry-building block and actual helper-call ASTs.
        from PIL import Image
        start, end = Image.new('RGB', (896, 512), 'red'), Image.new('RGB', (896, 512), 'blue')
        tree = ast.parse((self.backend / 'models/ltx2/ltx2.py').read_text())
        index_function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_to_latent_index')
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'LTX2')
        generate = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'generate')
        def assigned(node, name):
            return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
        first = next(i for i, n in enumerate(generate.body) if assigned(n, 'images'))
        last = next(i for i, n in enumerate(generate.body) if assigned(n, 'tiling_config'))
        ns = dict(image_start=start, image_end=end, input_video=None, is_start_image_only=True,
                  prefix_frames_count=0, frames_to_inject=[], frames_relative_positions_list=[],
                  frame_num=145, latent_stride=8, input_video_strength=1.0)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[index_function] + generate.body[first:last],
                                                          type_ignores=[])), '<actual-endpoint-entries>', 'exec'), ns)
        self.assertIs(ns['images'][0][0], start)
        self.assertIs(ns['guiding_images'][0][0], end)
        self.assertEqual(ns['guiding_images'][0][1], 144)
        module = types.SimpleNamespace(image_conditionings_by_replacing_latent=lambda **kw: [],
                                       image_conditionings_by_adding_guiding_latent=lambda **kw: [])
        pipeline = ast.parse((self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text())
        calls = sorted([n for n in ast.walk(pipeline) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                        and n.func.id in vars(module)], key=lambda n: n.lineno)
        self.assertEqual(len(calls), 4)
        ns.update(images_stage2=None, video_encoder=None, dtype='float16', self=types.SimpleNamespace(device='cpu'),
                  tiling_config=None, stage_1_output_shape=types.SimpleNamespace(width=448, height=256),
                  stage_2_output_shape=types.SimpleNamespace(width=896, height=512))
        with runtime.audit_endpoint_guides(module, start, end) as events:
            ns.update(vars(module))
            for call in calls:
                eval(compile(ast.Expression(call), '<actual-stage-guide-call>', 'eval'), ns)
        self.assertEqual([(x['guide'], x['stage'], x['frame_index']) for x in events],
                         [('start', 1, 0), ('end', 1, 144), ('start', 2, 0), ('end', 2, 144)])
        self.assertEqual(events[0]['rgb_sha256'], events[2]['rgb_sha256'])
        self.assertEqual(events[1]['rgb_sha256'], events[3]['rgb_sha256'])

    def test_missing_stage_or_wrong_end_index_is_rejected_and_hooks_restore(self):
        from PIL import Image
        start, end = Image.new('RGB', (896, 512), 'red'), Image.new('RGB', (896, 512), 'blue')
        original = lambda **kw: []
        module = types.SimpleNamespace(image_conditionings_by_replacing_latent=original,
                                       image_conditionings_by_adding_guiding_latent=original)
        with self.assertRaisesRegex(RuntimeError, 'Both exact endpoint guides'):
            with runtime.audit_endpoint_guides(module, start, end):
                pass
        self.assertIs(module.image_conditionings_by_replacing_latent, original)
        with self.assertRaisesRegex(RuntimeError, 'Changed end guide'):
            with runtime.audit_endpoint_guides(module, start, end):
                module.image_conditionings_by_adding_guiding_latent(images=[(end, 143, 1.0)], width=448, height=256)
        self.assertIs(module.image_conditionings_by_adding_guiding_latent, original)

    def test_input_fitting_does_not_crop_or_stretch_and_records_source_hashes(self):
        for key in ['start_image', 'end_image']:
            image, details = run.fit_image(self.bundle / self.manifest[key])
            self.assertEqual(image.size, (896, 512))
            self.assertEqual(details['source_sha256'], self.manifest[key + '_sha256'])
            self.assertEqual(details['source_dimensions'], self.manifest[key + '_dimensions'])
            self.assertEqual(details['contained'][0], 896)
            self.assertLessEqual(details['contained'][1], 512)

    def test_full_wrapper_accepts_exact_145_frame_tensor_and_discards_model_audio(self):
        import torch
        # Interface smoke only: the real backend entry-building/call ASTs are tested above.
        # Do not import GPU/audio dependencies just to return a synthetic CPU video tensor.
        module_names = ['models', 'models.ltx2', 'models.ltx2.ltx_pipelines',
                        'models.ltx2.ltx_pipelines.distilled']
        modules = {name: types.ModuleType(name) for name in module_names}
        for parent, child in zip(module_names, module_names[1:]):
            setattr(modules[parent], child.rsplit('.', 1)[1], modules[child])
        distilled = modules[module_names[-1]]
        distilled.image_conditionings_by_replacing_latent = lambda **kw: []
        distilled.image_conditionings_by_adding_guiding_latent = lambda **kw: []
        start, _ = run.fit_image(self.bundle / self.manifest['start_image'])
        end, _ = run.fit_image(self.bundle / self.manifest['end_image'])
        captured = {}
        def fake_generate(**kwargs):
            captured.update(kwargs)
            for width, height in [(448, 256), (896, 512)]:
                distilled.image_conditionings_by_replacing_latent(
                    images=[(kwargs['image_start'], 0, 1.0, 'lanczos')], width=width, height=height)
                distilled.image_conditionings_by_adding_guiding_latent(
                    images=[(kwargs['image_end'], 144, 1.0)], width=width, height=height)
            return {'x': torch.zeros(3, 145, 512, 896, dtype=torch.uint8), 'audio': object()}
        model = types.SimpleNamespace(generate=fake_generate,
                                      text_encoder=types.SimpleNamespace(_jml_text_phase={'complete': True}))
        with patch.dict(sys.modules, modules), \
             patch.object(torch.cuda, 'reset_peak_memory_stats'), \
             patch.object(torch.cuda, 'max_memory_allocated', return_value=0):
            frames, details = runtime.generate(model, self.manifest, start, end)
        self.assertEqual(frames.shape, (145, 512, 896, 3))
        self.assertEqual(str(frames.dtype), 'uint8')
        self.assertNotIn('input_waveform', captured)
        self.assertIs(captured['image_start'], start)
        self.assertIs(captured['image_end'], end)
        self.assertEqual(captured['frame_num'], 145)
        self.assertEqual(captured['fps'], 24.0)
        self.assertTrue(details['returned_model_audio_discarded'])
        self.assertTrue(details['joint_audio_video_generation'])
        self.assertFalse(details['supplied_audio'])
        self.assertEqual(len(details['image_guides']), 4)

    def test_real_codec_145_frames_natural_fps_and_rejects_audio_track(self):
        import numpy as np
        frames = np.zeros((145, 512, 896, 3), dtype=np.uint8)
        frames[:, 100:140, 200:240, 0] = 200
        path = self.root / 'synthetic-silent.mp4'
        run.encode_video(frames, path, 24)
        evidence = run.check_video(path)
        self.assertEqual(evidence['frames'], 145)
        self.assertEqual(evidence['duration_seconds'], 145 / 24)
        with_audio = self.root / 'synthetic-audio.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-shortest', '-c:v', 'copy', '-c:a', 'aac', str(with_audio)], check=True)
        with self.assertRaisesRegex(RuntimeError, 'Export dimensions/count/fps mismatch'):
            run.check_video(with_audio)

    def test_no_cuda_failure_and_whole_job_timeout(self):
        import torch
        with patch.object(torch.cuda, 'is_available', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'two CUDA Tesla T4'):
                run.preflight(self.root, self.root, self.backend)
        with self.assertRaises(TimeoutError):
            bootstrap.run_bounded([sys.executable, '-c', 'import time; time.sleep(30)'],
                                  deadline=time.monotonic() + 0.2, log=self.root / 'timeout.log')

    def test_metadata_private_outputless_and_titles_within_provider_limits(self):
        metadata = json.loads((common.HERE / 'kernel-metadata.json').read_text())
        self.assertIs(metadata['is_private'], True)
        for source in [metadata, json.loads((self.bundle / 'dataset-metadata.json').read_text())]:
            self.assertTrue(6 <= len(source['title']) <= 50)
        notebook = json.loads((common.HERE / 'private-diagnostic.ipynb').read_text())
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertNotIn('launch(', ''.join(cell['source']))
                compile(''.join(cell['source']), '<private-notebook>', 'exec')
        self.assertEqual(self.manifest['frames'], 145)
        function = next(n for n in ast.parse((common.HERE / 'runtime.py').read_text()).body
                        if isinstance(n, ast.FunctionDef) and n.name == 'generate')
        call = next(n for n in ast.walk(function) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'generate')
        arguments = {k.arg: k.value for k in call.keywords}
        self.assertNotIn('input_waveform', arguments)
        self.assertNotIn('input_waveform_sample_rate', arguments)
        self.assertEqual(ast.literal_eval(arguments['frame_num']), 145)
        self.assertEqual(ast.literal_eval(arguments['fps']), 24.0)
        self.assertIn('image_start', arguments)
        self.assertIn('image_end', arguments)


if __name__ == '__main__':
    unittest.main(verbosity=2)
