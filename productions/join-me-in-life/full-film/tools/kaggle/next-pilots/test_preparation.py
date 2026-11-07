"""Local next-pilot policy checks; no network, GPU inference or model downloads."""
import ast
import copy
import json
from pathlib import Path
import tempfile
import unittest

import prepare


class NextPilots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name) / 'staged'
        cls.report = prepare.stage(cls.root, prepare.REPOSITORY / 'build/ltx-cpu/config/tokenizer')
        cls.runners = {name: prepare.load_runner(cls.root / name / 'ltx_kaggle.py') for name in prepare.NAMES}
        cls.manifests = {name: json.loads((cls.root / name / 'pilot.json').read_text()) for name in prepare.NAMES}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def assert_rejected(self, name, mutation):
        manifest = copy.deepcopy(self.manifests[name])
        mutation(manifest)
        with self.assertRaises(ValueError):
            self.runners[name].validate_manifest(manifest, self.root / name)

    def test_exact_local_inputs_prompts_and_frames(self):
        for name, frames in [('hospital-embrace', 241), ('summer-exchange', 185)]:
            item = self.report['pilots'][name]
            self.assertEqual(item['frames'], frames)
            self.assertEqual((frames - 1) % 8, 0)
            self.assertEqual(item['token_count_including_eos'], 125)
            self.assertEqual(item['takes'], 1)
            self.assertTrue(all(source['native_dimensions'] == [1916, 1080]
                                for source in item['sources'].values()))

    def test_batches_multiple_shots_and_multiple_seeds_fail(self):
        for name in prepare.NAMES:
            for mutation in [lambda m: m.update(mode='batch'),
                             lambda m: m['shots'].append(copy.deepcopy(m['shots'][0])),
                             lambda m: m['shots'][0].update(seeds=[49, 73])]:
                with self.subTest(name=name, mutation=mutation):
                    self.assert_rejected(name, mutation)

    def test_longer_shorter_wrong_fps_and_wrong_dimensions_fail(self):
        for name in prepare.NAMES:
            for values in [{'frames': 121}, {'frames': 249}, {'fps': 24}, {'width': 832}, {'height': 512}]:
                with self.subTest(name=name, values=values):
                    self.assert_rejected(name, lambda m: m['shots'][0].update(values))

    def test_endpoint_contract_is_enforced(self):
        self.assert_rejected('hospital-embrace', lambda m: m['shots'][0].pop('end_image'))
        self.assert_rejected('summer-exchange', lambda m: m['shots'][0].update(end_image='M02_Summer_End.png'))

    def test_private_hash_and_path_guards_survive_specialization(self):
        for name in prepare.NAMES:
            for mutation in [lambda m: m.update(privacy='public'),
                             lambda m: m['shots'][0].update(image_sha256='0' * 64),
                             lambda m: m['shots'][0].update(image='../outside.png')]:
                with self.subTest(name=name, mutation=mutation):
                    self.assert_rejected(name, mutation)

    def test_frozen_runner_unchanged_and_refuses_long_pilots(self):
        self.assertEqual(prepare.digest(prepare.RUNNER / 'ltx_kaggle.py'), prepare.BASE_RUNNER_SHA256)
        runner = prepare.load_runner(prepare.RUNNER / 'ltx_kaggle.py')
        for name in prepare.NAMES:
            with self.assertRaisesRegex(ValueError, '153 frames'):
                runner.validate_manifest(self.manifests[name], self.root / name)

    def test_only_manifest_policy_changes(self):
        def without_validator(source):
            tree = ast.parse(source)
            tree.body = [node for node in tree.body
                         if not isinstance(node, ast.FunctionDef) or node.name != 'validate_manifest']
            return ast.dump(tree)
        self.assertEqual(without_validator((prepare.RUNNER / 'ltx_kaggle.py').read_text()),
                         without_validator((self.root / 'hospital-embrace/ltx_kaggle.py').read_text()))
        for name in prepare.NAMES:
            self.assertEqual(prepare.digest(prepare.RUNNER / 'bootstrap.py'),
                             prepare.digest(self.root / name / 'bootstrap.py'))

    def test_existing_runner_fits_sources_without_cropping_or_stretch(self):
        for name in prepare.NAMES:
            shot = self.manifests[name]['shots'][0]
            for field in ('image', 'end_image'):
                if field not in shot:
                    continue
                native = self.root / name / shot[field]
                source_digest = prepare.digest(native)
                output = self.root / name / ('check-' + field + '.png')
                image = self.runners[name].prepared_image(native, (864, 480), output)
                self.assertEqual(image.size, (864, 480))
                self.assertIsNone(image.crop((0, 0, 6, 480)).getbbox())
                self.assertIsNone(image.crop((858, 0, 864, 480)).getbbox())
                self.assertIsNotNone(image.crop((6, 0, 858, 480)).getbbox())
                self.assertEqual(prepare.digest(native), source_digest)

    def test_existing_staging_is_preserved(self):
        with self.assertRaisesRegex(ValueError, 'existing evidence is preserved'):
            prepare.stage(self.root, prepare.REPOSITORY / 'build/ltx-cpu/config/tokenizer')


if __name__ == '__main__':
    unittest.main(verbosity=2)
