"""Offline tests: no provider calls, weight download, GPU job, or account access."""
import ast
import copy
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
import zipfile
from unittest.mock import patch

os.environ['USE_TF'] = '0'
os.environ['USE_FLAX'] = '0'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'

import bootstrap
import ltx_kaggle as pipeline


class PrivateInputs(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / 'image.png').write_bytes(b'fixture-image-for-hash-validation')
        self.shot = {'shot_id': 'S044', 'image': 'image.png', 'image_sha256': pipeline.sha256(self.root / 'image.png'),
                     'prompt': 'A single supported hand gesture.', 'width': 864, 'height': 480,
                     'frames': 121, 'fps': 30, 'seeds': [49]}
        self.manifest = {'schema': 'jml-ltx-kaggle/v1', 'privacy': 'private', 'mode': 'pilot', 'shots': [self.shot]}
    def tearDown(self):
        self.temporary.cleanup()
    def test_valid_private_manifest(self):
        self.assertIs(pipeline.validate_manifest(self.manifest, self.root), self.manifest)
    def test_bad_privacy_hash_dimensions_and_frames(self):
        for mutation in ['privacy', 'hash', 'width', 'frames', 'seeds', 'duplicate']:
            with self.subTest(mutation=mutation):
                value = copy.deepcopy(self.manifest)
                if mutation == 'privacy': value['privacy'] = 'public'
                if mutation == 'hash': value['shots'][0]['image_sha256'] = '0' * 64
                if mutation == 'width': value['shots'][0]['width'] = 865
                if mutation == 'frames': value['shots'][0]['frames'] = 120
                if mutation == 'seeds': value['shots'][0]['seeds'] = [49, 49]
                if mutation == 'duplicate': value['shots'].append(copy.deepcopy(value['shots'][0]))
                with self.assertRaises(ValueError): pipeline.validate_manifest(value, self.root)
    def test_path_escape_and_missing_input(self):
        for path in ['../outside.png', '/tmp/image.png', 'https://example.invalid/art.png', 'missing.png']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                pipeline.input_path(self.root, path)
    def test_batch_cannot_bypass_review(self):
        self.manifest['mode'] = 'batch'
        with self.assertRaises(ValueError): pipeline.require_batch_review(self.manifest, None)
        review = self.root / 'review.json'
        review.write_text(json.dumps({'decision': 'accepted', 'model_revision': pipeline.MODEL_LOCK['revision']}))
        with self.assertRaises(ValueError): pipeline.require_batch_review(self.manifest, review)
    def test_resume_integrity_and_seed_list_extension(self):
        request = pipeline.request_record(self.shot, 49)
        changed = {**self.shot, 'seeds': [49, 73]}
        self.assertEqual(pipeline.fingerprint(request), pipeline.fingerprint(pipeline.request_record(changed, 49)))
        directory = self.root / 'take'; directory.mkdir()
        (directory / 'video.mp4').write_bytes(b'complete-video')
        saved = {'request_sha256': pipeline.fingerprint(request), 'status': 'complete', 'technical_valid': True,
                 'video_sha256': pipeline.sha256(directory / 'video.mp4')}
        pipeline.save_json(directory / 'render.json', saved)
        self.assertTrue(pipeline.resume_complete(directory, request))
        (directory / 'video.mp4').write_bytes(b'corrupted')
        with self.assertRaises(ValueError): pipeline.resume_complete(directory, request)
        saved['technical_valid'] = False
        pipeline.save_json(directory / 'render.json', saved)
        with self.assertRaises(ValueError): pipeline.resume_complete(directory, request)
    def test_oom_stops_after_one_attempt_and_saves_failure(self):
        manifest = self.root / 'pilot.json'; manifest.write_text(json.dumps(self.manifest))
        output = self.root / 'out'
        argv = ['ltx_kaggle', '--manifest', str(manifest), '--output', str(output), '--cache', str(self.root / 'cache')]
        with patch.object(sys, 'argv', argv), patch.object(pipeline, 'configure_cache'), \
             patch.object(pipeline, 'preflight', return_value={}), patch.object(pipeline, 'download_model', return_value=self.root), \
             patch.object(pipeline, 'encode_prompts', return_value={}), patch.object(pipeline, 'load_pipeline', return_value=object()), \
             patch.object(pipeline, 'generate', side_effect=RuntimeError('simulated OOM')) as generate:
            with self.assertRaisesRegex(RuntimeError, 'simulated OOM'): pipeline.main()
        self.assertEqual(generate.call_count, 1)
        self.assertEqual(generate.call_args.args[3]['frames'], 121)
        result = json.loads((output / 'S044__seed-49/render.json').read_text())
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['acceptance'], 'unreviewed')
        self.assertFalse((output / 'S044__seed-49/video.mp4').exists())
    def test_completed_resume_loads_no_gpu(self):
        output = self.root / 'out'; directory = output / 'S044__seed-49'; directory.mkdir(parents=True)
        request = pipeline.request_record(self.shot, 49)
        (directory / 'video.mp4').write_bytes(b'complete')
        pipeline.save_json(directory / 'render.json', {'request_sha256': pipeline.fingerprint(request),
            'status': 'complete', 'technical_valid': True, 'video_sha256': pipeline.sha256(directory / 'video.mp4')})
        manifest = self.root / 'pilot.json'; manifest.write_text(json.dumps(self.manifest))
        with patch.object(sys, 'argv', ['ltx_kaggle', '--manifest', str(manifest), '--output', str(output)]), \
             patch.object(pipeline, 'preflight') as preflight:
            pipeline.main()
        preflight.assert_not_called()


class Downloads(unittest.TestCase):
    def test_insufficient_disk_never_calls_hub(self):
        with tempfile.TemporaryDirectory() as name, patch('huggingface_hub.snapshot_download') as download, \
             patch.object(pipeline.shutil, 'disk_usage', return_value=SimpleNamespace(free=1)):
            with self.assertRaisesRegex(RuntimeError, 'reserve'):
                pipeline.download_model(Path(name))
            download.assert_not_called()
    def test_exact_allowlist_anonymous_download_and_bad_hash(self):
        with tempfile.TemporaryDirectory() as name:
            cache = Path(name); payload = b'public-test-weights'
            import hashlib
            lock = {'repository': 'official/model', 'revision': 'a' * 40,
                    'files': [{'path': 'transformer/example.safetensors', 'bytes': len(payload),
                               'sha256': hashlib.sha256(payload).hexdigest()}]}
            def fake_download(*args, **kwargs):
                self.assertIs(kwargs['token'], False)
                self.assertEqual(kwargs['allow_patterns'], ['transformer/example.safetensors'])
                destination = Path(kwargs['local_dir']) / lock['files'][0]['path']
                destination.parent.mkdir(parents=True, exist_ok=True); destination.write_bytes(payload)
            with patch.object(pipeline, 'MODEL_LOCK', lock), patch('huggingface_hub.snapshot_download', side_effect=fake_download):
                self.assertTrue((pipeline.download_model(cache) / lock['files'][0]['path']).is_file())
                lock['files'][0]['sha256'] = '0' * 64
                with self.assertRaisesRegex(RuntimeError, 'SHA256'): pipeline.download_model(cache)
    def test_model_lock_has_no_duplicated_tree(self):
        files = pipeline.MODEL_LOCK['files']
        self.assertEqual(len(files), 22)
        self.assertEqual(sum(f['bytes'] for f in files), 47629366835)
        self.assertTrue(all(len(Path(f['path']).parts) <= 2 for f in files))
        self.assertTrue(all(len(f['sha256']) == 64 for f in files))


class NumericAndCodec(unittest.TestCase):
    def test_chunked_feed_forward_matches_full_sequence(self):
        import torch
        torch.manual_seed(11)
        module = torch.nn.Sequential(torch.nn.Linear(7, 19), torch.nn.GELU(), torch.nn.Linear(19, 7)).eval()
        values = torch.randn(2, 13, 7)
        with torch.inference_mode():
            expected = module(values); actual = pipeline.chunk_feed_forward(module, 5)(values)
        self.assertTrue(torch.allclose(actual, expected, atol=1e-6, rtol=1e-6))
    def test_deterministic_per_token_scheduler_direction_and_conditioning(self):
        import torch
        from diffusers import FlowMatchEulerDiscreteScheduler
        config = json.loads((pipeline.HERE / 'scheduler-reference.json').read_text())
        scheduler = FlowMatchEulerDiscreteScheduler.from_config(config)
        self.assertFalse(scheduler.config.stochastic_sampling)
        scheduler.set_timesteps(timesteps=[725.0, 421.9])
        sample = torch.tensor([[[2.], [3.]]]); velocity = torch.tensor([[[.5], [.8]]])
        actual = scheduler.step(-velocity, torch.tensor(725.), sample,
            per_token_timesteps=torch.tensor([[725., 0.]]), return_dict=False)[0]
        expected = torch.tensor([[[2 - (.725 - .4219) * .5], [3.]]])
        self.assertTrue(torch.allclose(actual, expected, atol=1e-6))
    def test_decode_equation_includes_scale_and_noise(self):
        import torch
        from diffusers import LTXConditionPipeline
        mean = torch.tensor([.2, -.4]); std = torch.tensor([1.5, 2.5])
        vae = SimpleNamespace(latents_mean=mean, latents_std=std, config=SimpleNamespace(scaling_factor=2.))
        pipe = SimpleNamespace(vae=vae, _denormalize_latents=LTXConditionPipeline._denormalize_latents)
        values = torch.arange(16, dtype=torch.float32).reshape(1, 2, 2, 2, 2) / 10
        actual = pipeline.prepare_decode_latents(pipe, values, torch.Generator().manual_seed(17))
        denormalized = (values * std.reshape(1, 2, 1, 1, 1) / 2 + mean.reshape(1, 2, 1, 1, 1)).half()
        noise = torch.randn(values.shape, dtype=torch.float16, generator=torch.Generator().manual_seed(17))
        self.assertTrue(torch.equal(actual, .975 * denormalized + .025 * noise))
    def test_image_fit_preserves_aspect_and_source(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as name:
            root = Path(name); source = root / 'source.png'
            Image.new('RGB', (12, 6), 'white').save(source); before = pipeline.sha256(source)
            prepared = pipeline.prepared_image(source, (32, 32), root / 'prepared.png')
            self.assertEqual(prepared.getbbox(), (0, 8, 32, 24))
            self.assertEqual(pipeline.sha256(source), before)
    def test_real_video_encode_full_decode_and_wrong_count_rejection(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            frames = [Image.new('RGB', (32, 32), (n * 20, 40, 90)) for n in range(9)]
            shot = {'frames': 9, 'width': 32, 'height': 32, 'fps': 24}
            result = pipeline.export_and_check(frames, shot, root)
            self.assertEqual(result['decoded_frames'], 9)
            other = root / 'bad'; other.mkdir()
            with self.assertRaisesRegex(RuntimeError, 'frame count'):
                pipeline.export_and_check(frames, {**shot, 'frames': 17}, other)
            self.assertFalse((other / 'video.mp4').exists())


class BoundedPrivateBootstrap(unittest.TestCase):
    def test_venv_without_pip_accepts_offline_host_pip_install(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name); environment = root / 'venv'
            wheel = root / 'jml_bootstrap_fixture-0.0.1-py3-none-any.whl'
            files = {
                'jml_bootstrap_fixture.py': "VALUE = 'local-offline-test'\n",
                'jml_bootstrap_fixture-0.0.1.dist-info/METADATA':
                    'Metadata-Version: 2.1\nName: jml-bootstrap-fixture\nVersion: 0.0.1\n',
                'jml_bootstrap_fixture-0.0.1.dist-info/WHEEL':
                    'Wheel-Version: 1.0\nGenerator: local-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n',
            }
            record = 'jml_bootstrap_fixture-0.0.1.dist-info/RECORD'
            files[record] = ''.join(path + ',,\n' for path in [*files, record])
            with zipfile.ZipFile(wheel, 'w') as archive:
                for path, value in files.items(): archive.writestr(path, value)
            requirements = root / 'requirements.txt'; requirements.write_text(str(wheel) + '\n')
            constraints = root / 'constraints.txt'; constraints.write_text('jml-bootstrap-fixture==0.0.1\n')
            with patch.dict(os.environ, {'PIP_NO_INDEX': '1', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'}):
                python = bootstrap.install_environment(environment, requirements, constraints,
                    deadline=time.monotonic() + 30, log=root / 'setup.log', host_python=sys._base_executable)
            self.assertFalse((environment / 'bin/pip').exists())
            result = subprocess.check_output([str(python), '-c',
                'import jml_bootstrap_fixture as f; print(f.VALUE); print(f.__file__)'], text=True).splitlines()
            self.assertEqual(result[0], 'local-offline-test')
            self.assertTrue(Path(result[1]).is_relative_to(environment))
            host = subprocess.check_output([sys._base_executable, '-c',
                "import importlib.util; print(importlib.util.find_spec('jml_bootstrap_fixture') is None)"], text=True)
            self.assertEqual(host.strip(), 'True')
    def test_unsupported_host_pip_stops_before_install(self):
        commands = []
        def fake_run(command, **kwargs):
            commands.append(command)
            if '--version' in command:
                raise subprocess.CalledProcessError(2, command)
        with patch.object(bootstrap, 'run_bounded', side_effect=fake_run):
            with self.assertRaises(subprocess.CalledProcessError):
                bootstrap.install_environment(Path('/unused/venv'), Path('/unused/requirements'), Path('/unused/constraints'),
                    deadline=time.monotonic() + 30, log=Path('/unused/log'), host_python='/managed/python')
        self.assertEqual(len(commands), 2)
        self.assertIn('--without-pip', commands[0])
        self.assertEqual(commands[1][:4], ['/managed/python', '-m', 'pip', '--python'])
        self.assertFalse(any('install' in command for command in commands))
    def test_cpu_runtime_refused_before_any_model_download(self):
        import torch
        with tempfile.TemporaryDirectory() as name, patch.object(torch.cuda, 'is_available', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'two-GPU'):
                pipeline.preflight(Path(name), Path(name) / 'output')
    def test_actual_timeout_reaps_child(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name); pidfile = root / 'pid'
            code = f'import os,time,pathlib; pathlib.Path({str(pidfile)!r}).write_text(str(os.getpid())); time.sleep(10)'
            with self.assertRaises(TimeoutError):
                bootstrap.run_bounded([sys.executable, '-c', code], deadline=time.monotonic() + .4, log=root / 'job.log')
            pid = int(pidfile.read_text())
            with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
    def test_expired_deadline_starts_nothing(self):
        with patch.object(bootstrap.subprocess, 'Popen') as popen:
            with self.assertRaises(TimeoutError):
                bootstrap.run_bounded(['unused'], deadline=time.monotonic() - 1, log='unused')
            popen.assert_not_called()
    def test_failed_command_is_not_retried(self):
        with tempfile.TemporaryDirectory() as name:
            with self.assertRaises(subprocess.CalledProcessError) as error:
                bootstrap.run_bounded([sys.executable, '-c', 'raise SystemExit(7)'],
                                      deadline=time.monotonic() + 5, log=Path(name) / 'log')
            self.assertEqual(error.exception.returncode, 7)
    def test_notebook_and_metadata_remain_private_and_one_take(self):
        metadata = json.loads((pipeline.HERE / 'kernel-metadata.json').read_text())
        self.assertIs(metadata['is_private'], True)
        self.assertEqual(metadata['machine_shape'], 'NvidiaTeslaT4')
        self.assertEqual(metadata['dataset_sources'], ['darionalis/jml-ltx-private-pilot-inputs'])
        notebook = json.loads((pipeline.HERE / 'private-pilot.ipynb').read_text())
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                ast.parse(''.join(cell['source']))
        source = (pipeline.HERE / 'bootstrap.py').read_text()
        self.assertIn("'--max-new-renders', '1'", source)
        self.assertIn("'--system-site-packages'", source)
        self.assertIn("'-c', str(constraints)", source)
        self.assertIn("'IMAGEIO_FFMPEG_NO_PREVENT_SIGINT': '1'", source)
    def test_package_contains_exactly_one_default_take_and_current_sources(self):
        with tempfile.TemporaryDirectory() as name:
            destination = Path(name) / 'bundle'
            command = [sys.executable, str(pipeline.HERE / 'prepare_bundle.py'), '--output', str(destination)]
            subprocess.run(command, check=True, capture_output=True)
            manifest = json.loads((destination / 'pilot.json').read_text())
            pipeline.validate_manifest(manifest, destination)
            self.assertEqual(len(manifest['shots']), 1)
            self.assertEqual(manifest['shots'][0]['shot_id'], 'S044_bridge_pilot')
            self.assertEqual(manifest['shots'][0]['seeds'], [49])
            for name in ['ltx_kaggle.py', 'bootstrap.py', 'model-lock.json', 'requirements.txt', 'LICENSE.creator.txt']:
                self.assertEqual(pipeline.sha256(destination / name), pipeline.sha256(pipeline.HERE / name))
            self.assertFalse(any(path.suffix.lower() in {'.mp3', '.wav', '.aac'} for path in destination.iterdir()))
            self.assertTrue((destination.with_name('bundle-kernel') / 'private-pilot.ipynb').exists())
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
