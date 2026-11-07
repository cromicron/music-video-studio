"""Offline serial scheduling, exact audio/source/shape and codec checks. No weights."""
import ast
import base64
import hashlib
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
import wave
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
        cls.bundle = cls.root / 'bundle'
        prepare_bundle.prepare(cls.bundle)
        cls.manifests = [json.loads((cls.bundle / (sid + '.json')).read_text()) for sid in ['S014', 'S046']]
        cls.backend = cls.root / 'backend'
        common.prepare_backend(cls.bundle, cls.backend)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_exact_queue_native_inputs_samples_and_handle_coverage(self):
        common.verify_package(self.bundle)
        paths = common.validate_queue(json.loads((self.bundle / 'queue.json').read_text()), self.bundle)
        self.assertEqual([p.stem for p in paths], ['S014', 'S046'])
        for m in self.manifests:
            actual = common.validate_manifest(m, self.bundle)
            self.assertEqual((m['frames'] - 1) % 8, 0)
            self.assertEqual(actual['samples'], m['frames'] * 2000)
            start, end = m['editorial']['timeline_frames']
            self.assertEqual(end - start + 3 + 4, m['frames'])
            self.assertEqual(m['editorial']['source_frames'], [3, m['frames'] - 4])
            self.assertNotIn('end_image', m)

    def test_original_master_pcm_matches_each_excerpt_sample_exactly(self):
        master = common.HERE.parents[2] / 'full-song/track-49.mp3'
        self.assertEqual(common.sha256(master), common.MASTER_SHA256)
        pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(master), '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
        for m in self.manifests:
            prov = json.loads((self.bundle / m['audio_provenance']).read_text())
            with wave.open(str(self.bundle / m['audio']), 'rb') as w:
                actual = w.readframes(w.getnframes())
            start = prov['start_sample'] * 4
            self.assertEqual(actual, pcm[start:start + prov['samples'] * 4])
            self.assertEqual(hashlib.sha256(actual).hexdigest(), prov['pcm_sha256'])

    def test_invalid_scope_dimensions_frames_audio_and_queue_fail(self):
        for m in self.manifests:
            for values in [{'privacy': 'public'}, {'frames': 97}, {'frames': 145}, {'fps': 30}, {'seed': 50},
                           {'takes': 2}, {'width': 864}, {'image_sha256': '0' * 64}, {'shot_id': 'S044'},
                           {'end_image': 'bad.png'}, {'audio_pcm': {**m['audio_pcm'], 'samples': m['audio_pcm']['samples'] - 1}}]:
                with self.subTest(shot=m['shot_id'], values=values), self.assertRaises(ValueError):
                    common.validate_manifest({**m, **values}, self.bundle)
        queue = json.loads((self.bundle / 'queue.json').read_text())
        for values in [{'manifests': ['S014.json', 'S014.json']}, {'manifests': ['S046.json', 'S014.json']},
                       {'automatic_retries': 1}, {'privacy': 'public'}]:
            with self.assertRaises(ValueError):
                common.validate_queue({**queue, **values}, self.bundle)

    def test_metadata_absent_mount_base64_and_full_source_patch_integrity(self):
        mounted = self.root / 'mounted'; shutil.copytree(self.bundle, mounted)
        (mounted / 'dataset-metadata.json').unlink()
        lock = common.verify_package(mounted)
        self.assertNotIn('dataset-metadata.json', lock['files'])
        self.assertFalse(list(mounted.rglob('__pycache__')))
        self.assertFalse((mounted / 'vendor/wangp-source.zip').exists())
        b64 = mounted / 'vendor/wangp-source.zip.b64'
        self.assertEqual(base64.b64decode(b64.read_bytes(), validate=True), (common.HERE / 'vendor/wangp-source.zip').read_bytes())
        self.assertEqual(len(common.prepare_backend(mounted, self.root / 'mounted-backend')), 13)
        for sid in ['S014', 'S046']:
            result = subprocess.run([sys.executable, str(mounted / 'run.py'), '--manifest', str(mounted / (sid + '.json')),
                                     '--validate-only'], check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(result.stdout)['shot_id'], sid)
        b64.write_bytes(b'not-base64!!!')
        with self.assertRaisesRegex(ValueError, 'Invalid Base64'):
            common.prepare_backend(mounted, self.root / 'bad-source')
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
            common.verify_package(mounted)

    def test_proven_loader_residency_precisions_preflight_and_pins_unchanged(self):
        previous = common.HERE.with_name('kaggle-a2v')
        for name in ['requirements.txt', 'source-lock.json', 'model-lock.json', 'patches.json']:
            self.assertEqual((common.HERE / name).read_bytes(), (previous / name).read_bytes())
        def functions(path):
            return {n.name: ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef)}
        a, b = functions(common.HERE / 'runtime.py'), functions(previous / 'runtime.py')
        for name in ['require_finite', 'patch_transformers', 'install_sequential_text_phase', 'configure_attention',
                     'smoke_quantization', 'load_model']:
            self.assertEqual(a[name], b[name], name)
        for filename, names in [('run.py', ['preflight']), ('common.py', ['download_weights', 'prepare_backend']),
                                ('bootstrap.py', ['run_bounded', 'torch_constraints', 'install_environment'])]:
            a, b = functions(common.HERE / filename), functions(previous / filename)
            for name in names:
                self.assertEqual(a[name], b[name], name)

    def test_actual_backend_full_audio_branch_at_both_selected_lengths(self):
        import torch
        tree = ast.parse((self.backend / 'models/ltx2/ltx2.py').read_bytes())
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
        # Execute actual pinned types.py, which has no model loading or downloads.
        shape_namespace = {'__name__': 'isolated_ltx_types'}
        module = types.ModuleType('isolated_ltx_types')
        with patch.dict(sys.modules, {'isolated_ltx_types': module}):
            exec(compile((self.backend / 'models/ltx2/ltx_core/types.py').read_text(), '<actual-ltx-types>', 'exec'), module.__dict__)
        for frames, expected in [(105, 109), (89, 93)]:
            target = module.AudioLatentShape.from_video_pixel_shape(module.VideoPixelShape(batch=1, frames=frames, height=512, width=896, fps=24))
            self.assertEqual(target.frames, expected)
            for count in [expected - 1, expected, expected + 1]:
                ns = {'target_shape': target, 'audio_latent': torch.zeros(1, 8, count, 16),
                      'audio_strength': 1.0, 'self': types.SimpleNamespace(), 'json': json, 'AudioConditionByLatent': Full}
                if count < expected:
                    with self.assertRaisesRegex(ValueError, 'prefix fallback forbidden'):
                        exec(code, ns)
                else:
                    exec(code, ns)
                    self.assertEqual(ns['audio_conditionings'][0].shape, (1, 8, expected, 16))
                    self.assertTrue(ns['self']._jml_audio_coverage['full_coverage'])
        distilled = (self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text()
        self.assertIn('stage_2_audio_conditionings = audio_conditionings if audio_conditionings_stage2 is None', distilled)

    def test_wrapper_exact_frame_shapes_waveforms_and_missing_coverage_failure(self):
        import torch
        import numpy as np
        for m in self.manifests:
            calls = {}
            waveform = np.zeros(m['audio_pcm']['samples'], dtype=np.float32)
            image = object()
            def synthetic(**kwargs):
                calls.update(kwargs)
                return {'x': torch.zeros(3, m['frames'], 512, 896, dtype=torch.uint8)}
            model = types.SimpleNamespace(generate=synthetic, _jml_audio_coverage={'full_coverage': True, 'strength': 1.0},
                                          text_encoder=types.SimpleNamespace(_jml_text_phase={'complete': True}))
            with patch.object(torch.cuda, 'reset_peak_memory_stats'), patch.object(torch.cuda, 'max_memory_allocated', return_value=0):
                frames, details = runtime.generate(model, m, image, waveform, 48000)
                self.assertEqual(frames.shape, (m['frames'], 512, 896, 3))
                self.assertEqual(calls['frame_num'], m['frames'])
                self.assertIs(calls['input_waveform'], waveform)
                self.assertIs(calls['image_start'], image)
                self.assertEqual(calls['audio_scale'], 1.0)
                self.assertEqual(calls['fps'], 24.0)
                model._jml_audio_coverage = None
                with self.assertRaisesRegex(RuntimeError, 'No verified full supplied-audio'):
                    runtime.generate(model, m, image, waveform, 48000)

    def test_real_codecs_and_original_pcm_review_for_both_lengths(self):
        import numpy as np
        for m in self.manifests:
            frames = np.zeros((m['frames'], 512, 896, 3), dtype=np.uint8)
            silent = self.root / (m['shot_id'] + '.mp4')
            run.encode_video(frames, silent, 24, m['frames'])
            self.assertEqual(run.check_video(silent, m['frames'])['frames'], m['frames'])
            with self.assertRaises(RuntimeError):
                run.check_video(silent, 89 if m['frames'] == 105 else 105)
            review = silent.with_suffix('.mkv')
            subprocess.run(['ffmpeg', '-v', 'error', '-i', str(silent), '-i', str(self.bundle / m['audio']),
                            '-c:v', 'copy', '-c:a', 'pcm_s16le', str(review)], check=True)
            with self.assertRaises(RuntimeError):
                run.check_video(review, m['frames'])
            actual = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(review), '-map', '0:a:0', '-f', 's16le', '-'])
            with wave.open(str(self.bundle / m['audio']), 'rb') as w:
                self.assertEqual(actual, w.readframes(w.getnframes()))

    def test_serial_children_share_cache_but_failures_are_separate_without_retry(self):
        fixture = self.root / 'serial-fixture'; fixture.mkdir()
        (fixture / 'run.py').write_text('''import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--output');p.add_argument('--cache');a=p.parse_args()
out=Path(a.output);out.mkdir(exist_ok=True);cache=Path(a.cache);cache.mkdir(exist_ok=True)
record={'shot':Path(a.manifest).stem,'cache':str(cache),'had_shared_marker':(cache/'marker').exists()}
(cache/'marker').write_text('cached');(out/'render.json').write_text(json.dumps(record))
sys.exit(7 if record['shot']=='S014' else 0)
''')
        out = self.root / 'serial-results'; out.mkdir()
        state = {}; state_path = out / 'job.json'
        complete = bootstrap.run_serial_jobs(sys.executable, fixture, [self.bundle / 'S014.json', self.bundle / 'S046.json'],
            out, self.root / 'shared-cache', deadline=time.monotonic() + 10, env=os.environ.copy(), state=state, state_path=state_path)
        self.assertFalse(complete)
        self.assertEqual([x['status'] for x in state['shots']], ['failed', 'child_complete_unreviewed'])
        self.assertEqual([x['attempts'] for x in state['shots']], [1, 1])
        self.assertTrue((out / 'S014/failure.json').is_file())
        self.assertFalse((out / 'S046/failure.json').exists())
        self.assertTrue(json.loads((out / 'S046/render.json').read_text())['had_shared_marker'])

    def test_serial_deadline_stops_child_and_does_not_start_next(self):
        fixture = self.root / 'timeout-fixture'; fixture.mkdir()
        (fixture / 'run.py').write_text('import time;time.sleep(30)\n')
        out = self.root / 'timeout-results'; out.mkdir()
        state = {}
        with self.assertRaises(TimeoutError):
            bootstrap.run_serial_jobs(sys.executable, fixture, [self.bundle / 'S014.json', self.bundle / 'S046.json'],
                out, self.root / 'timeout-cache', deadline=time.monotonic() + 0.2, env=os.environ.copy(), state=state, state_path=out / 'job.json')
        self.assertEqual([x['status'] for x in state['shots']], ['failed', 'not_started_deadline'])
        self.assertEqual(state['shots'][1]['attempts'], 0)
        self.assertFalse((out / 'S046').exists())

    def test_hardware_early_failure_and_private_metadata_notebook(self):
        import torch
        with patch.object(torch.cuda, 'is_available', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'two CUDA Tesla T4'):
                run.preflight(self.root, self.root, self.backend)
        for p in [common.HERE / 'kernel-metadata.json', self.bundle / 'dataset-metadata.json']:
            self.assertTrue(6 <= len(json.loads(p.read_text())['title']) <= 50)
        self.assertTrue(json.loads((common.HERE / 'kernel-metadata.json').read_text())['is_private'])
        for c in json.loads((common.HERE / 'private-diagnostic.ipynb').read_text())['cells']:
            if c['cell_type'] == 'code':
                self.assertEqual(c['outputs'], [])
                compile(''.join(c['source']), '<private-notebook>', 'exec')


if __name__ == '__main__':
    unittest.main(verbosity=2)
