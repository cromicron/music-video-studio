"""Offline checks for exact original audio, unchanged engine and bounded new lengths."""
import ast
import base64
import hashlib
import importlib
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
import zipfile

import prepare_bundle

HERE = Path(__file__).resolve().parent
REPO = prepare_bundle.REPO
BUNDLE = REPO / 'build/jml-story-v2-performance-a-private-v1'
BASE = prepare_bundle.BASE
sys.path.insert(0, str(BUNDLE))
import common
import bootstrap
import run
import runtime


class Performance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.manifests = [json.loads((BUNDLE / (sid + '.json')).read_text()) for sid in ['V2-36', 'V2-21']]
        cls.backend = cls.root / 'backend'
        common.prepare_backend(BUNDLE, cls.backend)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_original_master_and_every_pcm_sample_match_selected_timeline(self):
        self.assertEqual(common.sha256(prepare_bundle.MASTER), prepare_bundle.MASTER_SHA256)
        full = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(prepare_bundle.MASTER),
                                       '-map', '0:a:0', '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
        for m in self.manifests:
            with wave.open(str(BUNDLE / m['audio']), 'rb') as audio:
                data = audio.readframes(audio.getnframes())
            first = (m['editorial']['timeline_frames'][0] - 6) * 2000
            count = m['frames'] * 2000
            self.assertEqual(data, full[first * 4:(first + count) * 4])
            self.assertEqual(len(data), count * 4)
            self.assertEqual(common.validate_manifest(m, BUNDLE)['samples'], count)
            self.assertEqual(m['editorial']['source_frames'][0], 6)
            self.assertGreaterEqual(m['editorial']['tail_handle_frames'], 7)
        self.assertEqual([m['frames'] for m in self.manifests], [97, 121])

    def test_images_are_exact_independently_viewed_start_crops(self):
        for m in self.manifests:
            prov = json.loads((BUNDLE / m['image_provenance']).read_text())
            source = REPO / prov['image_original']
            self.assertEqual((BUNDLE / m['image']).read_bytes(), source.read_bytes())
            self.assertEqual(common.sha256(source), prov['image_sha256'])
            review = json.loads((BUNDLE / prov['review_bundle_path']).read_text())
            pair = next(p for p in review['pairs'] if p['shot'] == m['shot_id'])
            crop = next(c for c in review['inspection']['native_review_crops'] if c['panel'] == prov['panel'])
            self.assertEqual(pair['verdict'], 'PASS_STATIC_SOURCE_FOR_BOUNDED_MOTION_TEST')
            self.assertTrue(crop['native_pixels_viewed'])
            self.assertEqual(crop['sha256'], m['image_sha256'])
            self.assertNotIn('end_image', m)

    def test_frozen_manifest_handles_and_queue_reject_substitution(self):
        for m in self.manifests:
            for changed in ({'frames': 105}, {'frames': m['frames'] - 8}, {'fps': 25}, {'seed': 50},
                            {'takes': 2}, {'end_image': 'end.png'}, {'supplied_audio': False},
                            {'audio_sha256': '0' * 64}, {'prompt': m['prompt'] + ' change'}):
                with self.subTest(shot=m['shot_id'], changed=list(changed)), self.assertRaises(ValueError):
                    common.validate_manifest({**m, **changed}, BUNDLE)
        q = json.loads((BUNDLE / 'queue.json').read_text())
        self.assertEqual([p.stem for p in common.validate_queue(q, BUNDLE)], ['V2-36', 'V2-21'])
        for changed in ({'automatic_retries': 1}, {'whole_job_seconds': 5401},
                        {'manifests': ['V2-21.json', 'V2-36.json']}, {'manifests': ['V2-36.json'] * 2}):
            with self.assertRaises(ValueError):
                common.validate_queue({**q, **changed}, BUNDLE)

    def test_original_engine_pins_and_proven_process_functions_are_unchanged(self):
        for name in ['runtime.py', 'requirements.txt', 'model-lock.json', 'source-lock.json', 'patches.json']:
            self.assertEqual((BUNDLE / name).read_bytes(), (BASE / name).read_bytes(), name)
        def funcs(path):
            return {n.name: ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef)}
        for name, function_names in [('run.py', ['preflight']),
            ('common.py', ['download_weights', 'prepare_backend', 'verify_package']),
            ('bootstrap.py', ['run_bounded', 'torch_constraints', 'install_environment', 'run_serial_jobs'])]:
            before, after = funcs(BASE / name), funcs(BUNDLE / name)
            for function in function_names:
                self.assertEqual(before[function], after[function], function)
        expected_run = (BASE / 'run.py').read_text().replace('expected_frames not in {89, 105}',
            "expected_frames not in {value['frames'] for value in SHOTS.values()}").replace(
            'jml-ltx-performance23-results', 'jml-v2-performance-a-results').replace(
            'jml-ltx-performance23-runtime', 'jml-v2-performance-a-runtime')
        self.assertEqual((BUNDLE / 'run.py').read_text(), expected_run)

    def test_actual_backend_audio_coverage_guard_at_97_and_121_frames(self):
        import torch
        tree = ast.parse((self.backend / 'models/ltx2/ltx2.py').read_bytes())
        statements = None
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                for index, item in enumerate(node.orelse):
                    if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'target_frames' for t in item.targets):
                        statements = node.orelse[index:]
        self.assertIsNotNone(statements)
        code = compile(ast.fix_missing_locations(ast.Module(body=statements, type_ignores=[])), '<actual-audio-guard>', 'exec')
        class Full:
            def __init__(self, latent, strength):
                self.shape, self.strength = tuple(latent.shape), strength
        module = types.ModuleType('isolated_v2_types')
        with patch.dict(sys.modules, {'isolated_v2_types': module}):
            exec(compile((self.backend / 'models/ltx2/ltx_core/types.py').read_text(), '<actual-audio-shapes>', 'exec'), module.__dict__)
        for frames, expected in [(97, 101), (121, 126)]:
            shape = module.AudioLatentShape.from_video_pixel_shape(module.VideoPixelShape(batch=1, frames=frames, height=512, width=896, fps=24))
            self.assertEqual(shape.frames, expected)
            for count in [expected - 1, expected, expected + 1]:
                ns = {'target_shape': shape, 'audio_latent': torch.zeros(1, 8, count, 16),
                      'audio_strength': 1.0, 'self': types.SimpleNamespace(), 'json': json, 'AudioConditionByLatent': Full}
                if count < expected:
                    with self.assertRaisesRegex(ValueError, 'prefix fallback forbidden'):
                        exec(code, ns)
                else:
                    exec(code, ns)
                    self.assertEqual(ns['audio_conditionings'][0].shape, (1, 8, expected, 16))
                    self.assertTrue(ns['self']._jml_audio_coverage['full_coverage'])

    def test_actual_runtime_forwards_exact_waveform_and_shape_without_end_guide(self):
        import numpy as np
        import torch
        for m in self.manifests:
            calls = {}; image = object(); waveform = np.zeros(m['audio_pcm']['samples'], dtype=np.float32)
            def synthetic(**kwargs):
                calls.update(kwargs)
                return {'x': torch.zeros(3, m['frames'], 512, 896, dtype=torch.uint8)}
            model = types.SimpleNamespace(generate=synthetic, _jml_audio_coverage={'full_coverage': True, 'strength': 1.0},
                text_encoder=types.SimpleNamespace(_jml_text_phase={'complete': True}))
            with patch.object(torch.cuda, 'reset_peak_memory_stats'), patch.object(torch.cuda, 'max_memory_allocated', return_value=0):
                frames, details = runtime.generate(model, m, image, waveform, 48000)
                self.assertEqual(frames.shape, (m['frames'], 512, 896, 3))
                self.assertIs(calls['input_waveform'], waveform)
                self.assertIs(calls['image_start'], image)
                self.assertEqual(calls['frame_num'], m['frames'])
                self.assertEqual(calls['audio_scale'], 1.0)
                self.assertEqual(calls['seed'], 49)
                self.assertNotIn('image_end', calls)
                self.assertTrue(details['returned_model_audio_discarded'])
                model._jml_audio_coverage = None
                with self.assertRaisesRegex(RuntimeError, 'No verified full supplied-audio'):
                    runtime.generate(model, m, image, waveform, 48000)

    def test_real_new_length_codecs_full_decode_and_original_pcm_review(self):
        import numpy as np
        for m in self.manifests:
            frame_values = np.arange(m['frames'], dtype=np.uint8)[:, None, None, None]
            frames = np.broadcast_to(frame_values, (m['frames'], 512, 896, 3)).copy()
            silent = self.root / (m['shot_id'] + '.mp4')
            run.encode_video(frames, silent, 24, m['frames'])
            self.assertEqual(run.check_video(silent, m['frames'])['frames'], m['frames'])
            with self.assertRaises(RuntimeError):
                run.check_video(silent, 121 if m['frames'] == 97 else 97)
            review = silent.with_suffix('.mkv')
            subprocess.run(['ffmpeg', '-v', 'error', '-i', str(silent), '-i', str(BUNDLE / m['audio']),
                            '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(review)], check=True)
            actual = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(review), '-map', '0:a:0', '-f', 's16le', '-'])
            with wave.open(str(BUNDLE / m['audio']), 'rb') as audio:
                self.assertEqual(actual, audio.readframes(audio.getnframes()))

    def test_two_real_serial_children_share_only_cache_and_do_not_retry_failure(self):
        fixture = self.root / 'serial'; fixture.mkdir()
        (fixture / 'run.py').write_text('''import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--output');p.add_argument('--cache');a=p.parse_args()
out=Path(a.output);cache=Path(a.cache);cache.mkdir(exist_ok=True)
r={'shot':Path(a.manifest).stem,'shared_marker_present':(cache/'marker').exists()}
(cache/'marker').write_text('cached');(out/'render.json').write_text(json.dumps(r))
sys.exit(7 if r['shot']=='V2-36' else 0)
''')
        manifests = [fixture / (m['shot_id'] + '.json') for m in self.manifests]
        for p in manifests: p.write_text('{}')
        output = fixture / 'results'; output.mkdir(); state = {}; record = output / 'job.json'
        self.assertFalse(bootstrap.run_serial_jobs(sys.executable, fixture, manifests, output, fixture / 'cache',
            deadline=time.monotonic() + 10, env=os.environ.copy(), state=state, state_path=record))
        self.assertEqual([s['status'] for s in state['shots']], ['failed', 'child_complete_unreviewed'])
        self.assertEqual([s['attempts'] for s in state['shots']], [1, 1])
        self.assertFalse(json.loads((output / 'V2-36/render.json').read_text())['shared_marker_present'])
        self.assertTrue(json.loads((output / 'V2-21/render.json').read_text())['shared_marker_present'])
        self.assertTrue((output / 'V2-36/failure.json').is_file())

    def test_package_archive_mount_and_private_notebook_caps(self):
        lock = common.verify_package(BUNDLE)
        with zipfile.ZipFile(BUNDLE.with_suffix('.zip')) as z:
            for name, expected in lock['files'].items():
                self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(), expected)
        self.assertFalse(list(BUNDLE.rglob('__pycache__')))
        mounted = self.root / 'mount'; shutil.copytree(BUNDLE, mounted)
        (mounted / 'dataset-metadata.json').unlink()
        common.verify_package(mounted)
        for m in self.manifests:
            subprocess.run([sys.executable, '-B', str(mounted / 'run.py'), '--manifest', str(mounted / (m['shot_id'] + '.json')), '--validate-only'],
                check=True, capture_output=True, text=True)
        source = base64.b64decode((BUNDLE / 'vendor/wangp-source.zip.b64').read_bytes(), validate=True)
        self.assertEqual(source, (BASE / 'vendor/wangp-source.zip').read_bytes())
        kernel = BUNDLE.with_name(BUNDLE.name + '-kernel')
        meta = json.loads((kernel / 'kernel-metadata.json').read_text())
        self.assertTrue(meta['is_private']); self.assertEqual(meta['machine_shape'], 'NvidiaTeslaT4')
        code = ''.join(json.loads((kernel / 'private-diagnostic.ipynb').read_text())['cells'][1]['source'])
        self.assertIn('WHOLE_JOB_SECONDS = 5390', code); self.assertIn('timeout=5400', code)
        self.assertNotIn('performance23-private-inputs', code)

    def test_cpu_preflight_fails_before_weights_and_preserves_failure_record(self):
        result = subprocess.run([sys.executable, '-B', str(BUNDLE / 'run.py'), '--manifest', str(BUNDLE / 'V2-36.json'),
            '--preflight-only', '--output', str(self.root / 'cpu-output'), '--cache', str(self.root / 'cpu-cache')],
            capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        record = json.loads((self.root / 'cpu-output/render.json').read_text())
        self.assertEqual(record['status'], 'failed')
        self.assertIn('Exactly two CUDA Tesla T4', record['error'])
        self.assertFalse((self.root / 'cpu-cache/models').exists())


if __name__ == '__main__':
    unittest.main()
