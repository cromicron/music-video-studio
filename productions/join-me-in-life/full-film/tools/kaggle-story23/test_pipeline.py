"""Offline exact-guide, editorial partition, serial scheduling and codec checks."""
import ast
import base64
import copy
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
        cls.bundles = {}
        cls.reports = {}
        cls.queue_manifests = {}
        cls.manifests = []
        for queue_id in common.QUEUES:
            bundle = cls.root / queue_id
            cls.reports[queue_id] = prepare_bundle.prepare(bundle, queue_id)
            cls.bundles[queue_id] = bundle
            paths = common.validate_queue(json.loads((bundle / 'queue.json').read_text()), bundle)
            cls.queue_manifests[queue_id] = [json.loads(p.read_text()) for p in paths]
            cls.manifests.extend(cls.queue_manifests[queue_id])
        cls.bundle = cls.bundles['Q2']
        cls.paths = [cls.bundle / (take + '.json') for take in common.QUEUES['Q2']['takes']]
        cls.backend = cls.root / 'backend'
        common.prepare_backend(cls.bundle, cls.backend)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def bundle_for(self, manifest):
        return self.bundles[manifest['queue_id']]

    def test_exact_sources_handles_and_aftermath_successive_portions(self):
        common.verify_package(self.bundle)
        self.assertEqual([m['frames'] for m in self.manifests], [121, 113, 209, 105, 209, 225, 137, 201, 97, 153, 169, 145, 201,
                                                              153, 225, 121, 113, 209, 169, 209, 137, 201, 105])
        self.assertEqual([len(list(b.glob('*.png'))) for b in self.bundles.values()], [2, 3, 1, 1, 1, 3, 4])
        self.assertFalse(list(self.bundle.glob('*.wav')))
        for m in self.manifests:
            common.validate_manifest(m, self.bundle_for(m))
            self.assertEqual(m['start_image'], m['end_image'])
            self.assertEqual(m['end_frame_index'], m['frames'] - 1)
            self.assertEqual((m['frames'] - 1) % 8, 0)
            e = m['editorial']; previous = e['head_handle_frames']
            self.assertGreaterEqual(previous, 3)
            self.assertGreaterEqual(e['tail_handle_frames'], 4)
            used = set()
            for segment in e['segments']:
                a, b = segment['source_frames']; c, d = segment['timeline_frames']
                self.assertEqual(a, previous)
                self.assertEqual(b - a, d - c)
                self.assertFalse(used.intersection(range(a, b)))
                used.update(range(a, b)); previous = b
            self.assertEqual(previous + e['tail_handle_frames'], m['frames'])
        longest = next(m for m in self.manifests if m['take_id'] == 'L09')
        self.assertEqual([s['source_frames'] for s in longest['editorial']['segments']], [[3, 116], [116, 215]])
        final = next(m for m in self.manifests if m['take_id'] == 'A07')
        self.assertEqual(final['editorial']['editor_only_fade']['source_frames'], [113, 161])
        self.assertIs(final['editorial']['editor_only_fade']['encoded_in_source'], False)
        self.assertIn('No fade, dimming or transition inside this source clip', final['prompt'])

    def test_corrections_change_prompt_without_inference_or_coverage_changes(self):
        originals = {m['take_id']: m for m in json.loads(
            (common.HERE.with_name('kaggle-quiet23') / 'takes-template.json').read_text())}
        for new_id, old_id, queue_id in [('R1L04', 'L04', 'R1W'), ('R1L05', 'L05', 'R1H')]:
            new = next(m for m in self.manifests if m['take_id'] == new_id)
            old = originals[old_id]
            for key in ['seed', 'width', 'height', 'frames', 'fps', 'start_image_sha256',
                        'end_image_sha256', 'start_frame_index', 'end_frame_index',
                        'editorial', 'conditioning', 'supplied_audio', 'model_audio_output']:
                self.assertEqual(new[key], old[key], (new_id, key))
            self.assertNotEqual(new['prompt'], old['prompt'])
            self.assertEqual(common.QUEUES[queue_id]['takes'], [new_id])

    def test_positive_continuations_preserve_slots_and_balance_without_duplicates(self):
        by_id = {m['take_id']: m for m in self.manifests}
        reference_ids = []
        for queue_id in ['P1', 'P2']:
            selected = common.QUEUES[queue_id]['takes']
            self.assertEqual(len(selected), 5)
            self.assertEqual(sum(by_id[ident]['frames'] for ident in selected), 821)
            for ident in selected:
                original = ident[len(queue_id):]
                reference_ids.append(original)
                new, old = by_id[ident], by_id[original]
                for key in ['seed', 'width', 'height', 'frames', 'fps', 'start_image_sha256',
                            'end_image_sha256', 'start_frame_index', 'end_frame_index',
                            'editorial', 'conditioning', 'supplied_audio', 'model_audio_output']:
                    self.assertEqual(new[key], old[key], (ident, key))
                self.assertNotEqual(new['prompt'], old['prompt'])
        self.assertEqual(len(reference_ids), len(set(reference_ids)))
        self.assertEqual(set(reference_ids), {'L02', 'L03', 'L06', 'L07', 'L08', 'L09', 'L10', 'L11', 'L13', 'A07'})

    def test_changed_scope_end_indices_sources_or_editorial_reuse_rejected(self):
        for m in self.manifests:
            for values in [{'privacy': 'public'}, {'frames': m['frames'] + 8}, {'fps': 30}, {'seed': 50}, {'takes': 2},
                           {'take_id': 'A06'}, {'end_frame_index': m['frames']}, {'end_image': 'other.png'},
                           {'start_image_sha256': '0' * 64}, {'audio': 'song.wav'}, {'supplied_audio': True},
                           {'model_audio_output': True}, {'source_provenance_sha256': '0' * 64}]:
                with self.subTest(take=m['take_id'], values=values), self.assertRaises(ValueError):
                    common.validate_manifest({**m, **values}, self.bundle_for(m))
        changed = copy.deepcopy(next(m for m in self.manifests if m['take_id'] == 'L09'))
        changed['editorial']['segments'][1]['source_frames'] = [3, 99]
        with self.assertRaisesRegex(ValueError, 'Editorial slots'):
            common.validate_manifest(changed, self.bundle_for(changed))
        queue = json.loads((self.bundle / 'queue.json').read_text())
        for values in [{'manifests': ['L02.json'] * 4}, {'automatic_retries': 1}, {'privacy': 'public'}]:
            with self.assertRaises(ValueError):
                common.validate_queue({**queue, **values}, self.bundle)

    def test_metadata_absent_mount_strict_base64_and_source_patches(self):
        mounted = self.root / 'mounted'; shutil.copytree(self.bundle, mounted)
        (mounted / 'dataset-metadata.json').unlink()
        self.assertNotIn('dataset-metadata.json', common.verify_package(mounted)['files'])
        self.assertFalse(list(mounted.rglob('__pycache__')))
        b64 = mounted / 'vendor/wangp-source.zip.b64'
        self.assertEqual(base64.b64decode(b64.read_bytes(), validate=True), (common.HERE / 'vendor/wangp-source.zip').read_bytes())
        self.assertFalse((mounted / 'vendor/wangp-source.zip').exists())
        self.assertEqual(len(common.prepare_backend(mounted, self.root / 'mounted-backend')), 13)
        for m in self.queue_manifests['Q2']:
            result = subprocess.run([sys.executable, str(mounted / 'run.py'), '--manifest', str(mounted / (m['take_id'] + '.json')),
                                     '--validate-only'], check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(result.stdout)['frames'], m['frames'])
        b64.write_bytes(b'bad!!!')
        with self.assertRaisesRegex(ValueError, 'Invalid Base64'):
            common.prepare_backend(mounted, self.root / 'bad-base64')
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
            common.verify_package(mounted)

    def test_proven_loader_residency_preflight_dependencies_and_serial_scheduler(self):
        previous = common.HERE.with_name('kaggle-quiet23')
        for name in ['requirements.txt', 'source-lock.json', 'model-lock.json', 'patches.json', 'runtime.py']:
            self.assertEqual((common.HERE / name).read_bytes(), (previous / name).read_bytes())
        def functions(path):
            return {n.name: ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef)}
        for filename, names in [('runtime.py', ['require_finite', 'patch_transformers', 'install_sequential_text_phase',
                                 'configure_attention', 'smoke_quantization', 'load_model']),
                                ('run.py', ['preflight', 'fit_image']), ('common.py', ['prepare_backend', 'download_weights'])]:
            a, b = functions(common.HERE / filename), functions(previous / filename)
            for name in names:
                self.assertEqual(a[name], b[name], name)
        a, b = functions(common.HERE / 'bootstrap.py'), functions(common.HERE.with_name('kaggle-performance23') / 'bootstrap.py')
        for name in ['run_bounded', 'torch_constraints', 'install_environment', 'run_serial_jobs']:
            self.assertEqual(a[name], b[name], name)

    def test_actual_backend_endpoint_construction_and_both_stages_for_all_takes(self):
        tree = ast.parse((self.backend / 'models/ltx2/ltx2.py').read_text())
        index_function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_to_latent_index')
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'LTX2')
        generate = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'generate')
        def assigned(node, name):
            return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
        first = next(i for i, n in enumerate(generate.body) if assigned(n, 'images'))
        last = next(i for i, n in enumerate(generate.body) if assigned(n, 'tiling_config'))
        code = compile(ast.fix_missing_locations(ast.Module(body=[index_function] + generate.body[first:last], type_ignores=[])), '<actual-entries>', 'exec')
        for m in self.manifests:
            image, fitting = run.fit_image(self.bundle_for(m) / m['start_image'])
            self.assertEqual(fitting['source_dimensions'], m['start_image_dimensions'])
            ns = dict(image_start=image, image_end=image, input_video=None, is_start_image_only=True,
                      prefix_frames_count=0, frames_to_inject=[], frames_relative_positions_list=[],
                      frame_num=m['frames'], latent_stride=8, input_video_strength=1.0)
            exec(code, ns)
            self.assertIs(ns['images'][0][0], image)
            self.assertIs(ns['guiding_images'][0][0], image)
            self.assertEqual(ns['guiding_images'][0][1], m['frames'] - 1)
            module = types.SimpleNamespace(image_conditionings_by_replacing_latent=lambda **kw: [],
                                           image_conditionings_by_adding_guiding_latent=lambda **kw: [])
            pipeline = ast.parse((self.backend / 'models/ltx2/ltx_pipelines/distilled.py').read_text())
            calls = sorted([n for n in ast.walk(pipeline) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                            and n.func.id in vars(module)], key=lambda n: n.lineno)
            self.assertEqual(len(calls), 4)
            ns.update(images_stage2=None, video_encoder=None, dtype='float16', self=types.SimpleNamespace(device='cpu'),
                      tiling_config=None, stage_1_output_shape=types.SimpleNamespace(width=448, height=256),
                      stage_2_output_shape=types.SimpleNamespace(width=896, height=512))
            with runtime.audit_endpoint_guides(module, image, image, m['frames'] - 1) as events:
                ns.update(vars(module))
                for call in calls:
                    eval(compile(ast.Expression(call), '<actual-stage-call>', 'eval'), ns)
            self.assertEqual([(e['guide'], e['stage'], e['frame_index']) for e in events],
                             [('start', 1, 0), ('end', 1, m['frames'] - 1), ('start', 2, 0), ('end', 2, m['frames'] - 1)])
            self.assertEqual(len({e['rgb_sha256'] for e in events}), 1)

    def test_missing_stage_changed_bytes_or_wrong_end_index_fail_and_restore(self):
        from PIL import Image
        source, changed = Image.new('RGB', (896, 512), 'red'), Image.new('RGB', (896, 512), 'blue')
        original = lambda **kw: []
        module = types.SimpleNamespace(image_conditionings_by_replacing_latent=original,
                                       image_conditionings_by_adding_guiding_latent=original)
        for frame_count in sorted(common.ALLOWED_FRAMES):
            with self.assertRaisesRegex(RuntimeError, 'Both exact endpoint guides'):
                with runtime.audit_endpoint_guides(module, source, source, frame_count - 1):
                    pass
            for image, index in [(source, frame_count), (changed, frame_count - 1)]:
                with self.assertRaisesRegex(RuntimeError, 'Changed end guide'):
                    with runtime.audit_endpoint_guides(module, source, source, frame_count - 1):
                        module.image_conditionings_by_adding_guiding_latent(images=[(image, index, 1.0)], width=448, height=256)
            self.assertIs(module.image_conditionings_by_adding_guiding_latent, original)

    def test_wrapper_exact_shapes_no_audio_and_same_guides(self):
        import torch
        names = ['models', 'models.ltx2', 'models.ltx2.ltx_pipelines', 'models.ltx2.ltx_pipelines.distilled']
        modules = {name: types.ModuleType(name) for name in names}
        for parent, child in zip(names, names[1:]):
            setattr(modules[parent], child.rsplit('.', 1)[1], modules[child])
        distilled = modules[names[-1]]
        distilled.image_conditionings_by_replacing_latent = lambda **kw: []
        distilled.image_conditionings_by_adding_guiding_latent = lambda **kw: []
        for m in self.manifests:
            source, _ = run.fit_image(self.bundle_for(m) / m['start_image'])
            captured = {}
            def synthetic(**kwargs):
                captured.update(kwargs)
                for width, height in [(448, 256), (896, 512)]:
                    distilled.image_conditionings_by_replacing_latent(images=[(kwargs['image_start'], 0, 1.0, 'lanczos')], width=width, height=height)
                    distilled.image_conditionings_by_adding_guiding_latent(images=[(kwargs['image_end'], kwargs['frame_num'] - 1, 1.0)], width=width, height=height)
                return {'x': torch.zeros(3, kwargs['frame_num'], 512, 896, dtype=torch.uint8), 'audio': object()}
            model = types.SimpleNamespace(generate=synthetic, text_encoder=types.SimpleNamespace(_jml_text_phase={'complete': True}))
            with patch.dict(sys.modules, modules), patch.object(torch.cuda, 'reset_peak_memory_stats'), patch.object(torch.cuda, 'max_memory_allocated', return_value=0):
                frames, details = runtime.generate(model, m, source, source)
            self.assertEqual(frames.shape, (m['frames'], 512, 896, 3))
            self.assertEqual(str(frames.dtype), 'uint8')
            self.assertIs(captured['image_start'], captured['image_end'])
            self.assertEqual(captured['frame_num'], m['frames'])
            self.assertNotIn('input_waveform', captured)
            self.assertTrue(details['joint_audio_video_generation'])
            self.assertTrue(details['returned_model_audio_discarded'])

    def test_real_codec_all_selected_counts_and_no_audio_stream(self):
        import numpy as np
        for count in sorted(common.ALLOWED_FRAMES):
            frames = np.zeros((count, 512, 896, 3), dtype=np.uint8)
            path = self.root / f'synthetic-{count}.mp4'
            run.encode_video(frames, path, 24, count)
            self.assertEqual(run.check_video(path, count)['duration_seconds'], count / 24)
            with self.assertRaises(RuntimeError):
                run.check_video(path, 97 if count != 97 else 105)
        audio = self.root / 'synthetic-audio.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-shortest', '-c:v', 'copy', '-c:a', 'aac', str(audio)], check=True)
        with self.assertRaisesRegex(RuntimeError, 'Export dimensions/count/fps mismatch'):
            run.check_video(audio, 225)

    def test_hardware_early_failure_and_private_clean_notebook(self):
        import torch
        with patch.object(torch.cuda, 'is_available', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'two CUDA Tesla T4'):
                run.preflight(self.root, self.root, self.backend)
        for path in [Path(self.reports['Q2']['kernel']) / 'kernel-metadata.json', self.bundle / 'dataset-metadata.json']:
            self.assertTrue(6 <= len(json.loads(path.read_text())['title']) <= 50)
        self.assertIs(json.loads((Path(self.reports['Q2']['kernel']) / 'kernel-metadata.json').read_text())['is_private'], True)
        for cell in json.loads((Path(self.reports['Q2']['kernel']) / 'private-diagnostic.ipynb').read_text())['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                compile(''.join(cell['source']), '<private-notebook>', 'exec')

    def test_explicit_queue_selection_private_isolation_and_no_auto_all(self):
        with self.assertRaisesRegex(ValueError, 'Explicitly choose'):
            prepare_bundle.prepare(self.root / 'forbidden-all', 'ALL')
        self.assertFalse((self.root / 'forbidden-all').exists())
        cli = subprocess.run([sys.executable, str(common.HERE / 'prepare_bundle.py'), '--output', str(self.root / 'missing-selection')],
                             text=True, capture_output=True)
        self.assertNotEqual(cli.returncode, 0)
        self.assertFalse((self.root / 'missing-selection').exists())
        for queue_id, bundle in self.bundles.items():
            config = common.QUEUES[queue_id]
            common.verify_package(bundle)
            staged = json.loads((bundle / 'take-specs.json').read_text())
            self.assertEqual(list(staged), config['takes'])
            queue = json.loads((bundle / 'queue.json').read_text())
            self.assertEqual(queue['manifests'], [take + '.json' for take in config['takes']])
            for other in set(common.TAKES) - set(config['takes']):
                self.assertFalse((bundle / (other + '.json')).exists())
                self.assertFalse((bundle / (other + '-provenance.json')).exists())
            metadata = json.loads((Path(self.reports[queue_id]['kernel']) / 'kernel-metadata.json').read_text())
            self.assertEqual(metadata['id'], config['kernel_id'])
            self.assertEqual(metadata['dataset_sources'], [config['dataset_id']])
            self.assertTrue(metadata['is_private'])
            self.assertTrue(6 <= len(metadata['title']) <= 50)
            notebook = json.loads((Path(self.reports[queue_id]['kernel']) / 'private-diagnostic.ipynb').read_text())
            self.assertNotIn('__DATASET_SLUG__', json.dumps(notebook))
            self.assertNotIn('__QUEUE__', json.dumps(notebook))
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    self.assertEqual(cell['outputs'], [])
                    compile(''.join(cell['source']), '<selected-private-notebook>', 'exec')
            wrong = dict(queue, queue_id='Q3' if queue_id != 'Q3' else 'Q2')
            with self.assertRaises(ValueError):
                common.validate_queue(wrong, bundle)


    def test_serial_children_share_cache_but_failures_are_separate_without_retry(self):
        fixture = self.root / 'serial-fixture'; fixture.mkdir()
        (fixture / 'run.py').write_text('''import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--output');p.add_argument('--cache');a=p.parse_args()
out=Path(a.output);out.mkdir(exist_ok=True);cache=Path(a.cache);cache.mkdir(exist_ok=True)
record={'shot':Path(a.manifest).stem,'cache':str(cache),'had_shared_marker':(cache/'marker').exists()}
(cache/'marker').write_text('cached');(out/'render.json').write_text(json.dumps(record))
sys.exit(7 if record['shot']=='L02' else 0)
''')
        out = self.root / 'serial-results'; out.mkdir()
        state = {}; state_path = out / 'job.json'
        complete = bootstrap.run_serial_jobs(sys.executable, fixture, self.paths,
            out, self.root / 'shared-cache', deadline=time.monotonic() + 10, env=os.environ.copy(), state=state, state_path=state_path)
        self.assertFalse(complete)
        self.assertEqual([x['status'] for x in state['shots']], ['failed'] + ['child_complete_unreviewed'] * 3)
        self.assertEqual([x['attempts'] for x in state['shots']], [1, 1, 1, 1])
        self.assertTrue((out / 'L02/failure.json').is_file())
        self.assertFalse((out / 'L03/failure.json').exists())
        self.assertTrue(json.loads((out / 'L03/render.json').read_text())['had_shared_marker'])

    def test_serial_deadline_stops_child_and_does_not_start_next(self):
        fixture = self.root / 'timeout-fixture'; fixture.mkdir()
        (fixture / 'run.py').write_text('import time;time.sleep(30)\n')
        out = self.root / 'timeout-results'; out.mkdir()
        state = {}
        with self.assertRaises(TimeoutError):
            bootstrap.run_serial_jobs(sys.executable, fixture, self.paths,
                out, self.root / 'timeout-cache', deadline=time.monotonic() + 0.2, env=os.environ.copy(), state=state, state_path=out / 'job.json')
        self.assertEqual([x['status'] for x in state['shots']], ['failed'] + ['not_started_deadline'] * 3)
        self.assertEqual(state['shots'][1]['attempts'], 0)
        self.assertFalse((out / 'L03').exists())

if __name__ == '__main__':
    unittest.main(verbosity=2)
