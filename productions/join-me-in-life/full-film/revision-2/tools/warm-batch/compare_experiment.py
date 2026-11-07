#!/usr/bin/env python3
"""Compare exact standalone/warm evidence. Never relax a failed equality gate."""
import argparse
import json
from pathlib import Path


def read(path): return json.loads(Path(path).read_text())


def compare(output, spec):
    output = Path(output)
    names = ['cold-A', 'cold-B', 'warm/A1', 'warm/B', 'warm/A2']
    data = {name: {'rgb': read(output/name/'raw-rgb.json'), 'context': read(output/name/'context-observation.json'),
                   'render': read(output/name/'render.json')} for name in names}
    def same_context(a, b):
        return data[a]['context']['calls'] == data[b]['context']['calls']
    pairs = [('cold-A', 'warm/A1'), ('cold-B', 'warm/B'), ('warm/A1', 'warm/A2')]
    equality = {a+'__'+b: {'context_exact': same_context(a, b),
                          'rgb_array_exact': data[a]['rgb'] == data[b]['rgb']}
                for a, b in pairs}
    warm = read(output/'warm/warm-summary.json')
    cold_a, cold_b = read(output/'cold-A/child.json'), read(output/'cold-B/child.json')
    cold_total = cold_a['elapsed_seconds'] + cold_b['elapsed_seconds']
    warm_ab = warm['first_A_and_B_elapsed_seconds']
    memory_a1 = data['warm/A1']['render']['after_export_gpu_allocated']
    memory_a2 = data['warm/A2']['render']['after_export_gpu_allocated']
    memory_growth = [b-a for a, b in zip(memory_a1, memory_a2)]
    checks = {
        'all_exact_context_and_rgb_checks': all(all(v.values()) for v in equality.values()),
        'all_five_decodes_passed': all(v['render']['video']['full_decode_passed'] is True for v in data.values()),
        'cold_children_complete': cold_a['status'] == cold_b['status'] == 'complete',
        'warm_complete': warm['status'] == 'complete',
        'exactly_two_raw_encodes_and_three_cache_requests': warm['raw_encode_count'] == 2 and warm['cache_requests'] == 3,
        'gemma_remains_released': warm['gemma_released'] is True,
        'context_cpu_bound': warm['context_cpu_bytes'] <= warm['context_cpu_limit'],
        'no_allocated_memory_growth_on_repeated_A': len(memory_growth) == 2 and all(v <= 0 for v in memory_growth),
        'balanced_AB_end_to_end_speed_target': warm_ab <= cold_total*spec['maximum_warm_to_cold_time_ratio'],
    }
    return {'schema': 'jml-warm-equivalence-result/v1', 'checks': checks, 'exact_equality': equality,
            'offline_fixture': False, 'experimental_checks_all_pass': all(checks.values()),
            'production_promotion': False, 'automatic_retries': 0,
            'timing': {'cold_A_plus_B_seconds': cold_total, 'warm_setup_plus_A1_plus_B_seconds': warm_ab,
                       'warm_to_cold_ratio': warm_ab/cold_total,
                       'warm_A2_is_state_test_not_counted_in_speed_comparison': True,
                       'initial_common_weight_cache_setup_excluded_from_both_branches': True},
            'memory': {'A1_after_export_bytes': memory_a1, 'A2_after_export_bytes': memory_a2,
                       'growth_bytes': memory_growth, 'permitted_growth_bytes': [0, 0]},
            'interpretation': 'Exact numeric/hash comparison only. Any failure blocks promotion; root must review results and actual motion. No changed equality or memory tolerance is inferred.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--spec', type=Path, required=True)
    args = p.parse_args()
    report = compare(args.output, read(args.spec))
    (args.output/'comparison.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['experimental_checks_all_pass'] else 2)
