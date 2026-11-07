"""Exact comparison policy using synthetic records; no neural work."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from compare_experiment import compare


class ComparisonTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.spec = {'maximum_warm_to_cold_time_ratio': 0.8}
        for name, ident in [('cold-A', 'a'), ('cold-B', 'b'), ('warm/A1', 'a'), ('warm/B', 'b'), ('warm/A2', 'a')]:
            self.save(name+'/raw-rgb.json', {'sha256': ident})
            self.save(name+'/context-observation.json', {'calls': [{'prompt_sha256': ident, 'tensors': [ident, ident]}]})
            self.save(name+'/render.json', {'video': {'full_decode_passed': True}, 'after_export_gpu_allocated': [100, 200]})
        for name in ['cold-A', 'cold-B']:
            self.save(name+'/child.json', {'status': 'complete', 'elapsed_seconds': 300})
        self.save('warm/warm-summary.json', {'status': 'complete', 'first_A_and_B_elapsed_seconds': 400,
            'raw_encode_count': 2, 'cache_requests': 3, 'gemma_released': True, 'context_cpu_bytes': 1024, 'context_cpu_limit': 2048})

    def tearDown(self): self.tmp.cleanup()
    def save(self, name, value):
        p = self.root/name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(value))

    def test_all_exact_checks_still_never_promote_production(self):
        result = compare(self.root, self.spec)
        self.assertTrue(result['experimental_checks_all_pass'])
        self.assertFalse(result['production_promotion'])
        self.assertEqual(result['timing']['warm_to_cold_ratio'], 2/3)

    def test_one_rgb_difference_blocks_fast_result(self):
        self.save('warm/B/raw-rgb.json', {'sha256': 'changed'})
        self.assertFalse(compare(self.root, self.spec)['experimental_checks_all_pass'])

    def test_one_context_difference_blocks_fast_result(self):
        self.save('warm/A2/context-observation.json', {'calls': [{'prompt_sha256': 'a', 'tensors': ['changed']}]})
        self.assertFalse(compare(self.root, self.spec)['checks']['all_exact_context_and_rgb_checks'])

    def test_single_byte_memory_growth_is_not_silently_tolerated(self):
        self.save('warm/A2/render.json', {'video': {'full_decode_passed': True}, 'after_export_gpu_allocated': [101, 200]})
        self.assertFalse(compare(self.root, self.spec)['checks']['no_allocated_memory_growth_on_repeated_A'])

    def test_exact_output_without_measured_gain_is_not_a_speed_pass(self):
        p = self.root/'warm/warm-summary.json'; data = json.loads(p.read_text())
        data['first_A_and_B_elapsed_seconds'] = 590; p.write_text(json.dumps(data))
        result = compare(self.root, self.spec)
        self.assertTrue(result['checks']['all_exact_context_and_rgb_checks'])
        self.assertFalse(result['checks']['balanced_AB_end_to_end_speed_target'])


if __name__ == '__main__': unittest.main()
