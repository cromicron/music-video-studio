#!/usr/bin/env python3
"""One private bounded job: cache setup, fresh cold A/B, warm A-B-A, exact comparison."""
import argparse
import json
import os
from pathlib import Path
import sys
import time

from bootstrap import run_bounded, torch_constraints, install_environment
from common import verify_package, validate_queue, save_json, sha256


def validate(bundle):
    verify_package(bundle)
    queue = json.loads((bundle/'queue.json').read_text())
    manifests = validate_queue(queue, bundle)
    spec = json.loads((bundle/'experiment.json').read_text())
    if (spec['schema'], spec['privacy'], spec['whole_job_seconds'], spec['automatic_retries']) != (
            'jml-warm-hardware-experiment/v1', 'private', 5400, 0):
        raise ValueError('Experimental privacy/cap/retry policy changed')
    if spec['takes'] != ['V2WH01', 'V2WC01'] or [p.stem for p in manifests] != spec['takes']:
        raise ValueError('Only the fixed H01/C01 comparison is allowed')
    for path, expected_frames in zip(manifests, [169, 193]):
        if json.loads(path.read_text())['frames'] != expected_frames:
            raise ValueError('Fixed source length changed')
    if spec['warm_order'] != [{'label': 'A1', 'take_id': 'V2WH01'}, {'label': 'B', 'take_id': 'V2WC01'},
                              {'label': 'A2', 'take_id': 'V2WH01'}]:
        raise ValueError('Warm equivalence order changed')
    if spec['maximum_warm_to_cold_time_ratio'] != 0.8 or spec['equality'] != 'exact_context_and_raw_rgb_hashes':
        raise ValueError('Equality/speed gate changed')
    return spec


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle', required=True, type=Path)
    ap.add_argument('--seconds', type=int, default=5400)
    ap.add_argument('--validate-only', action='store_true')
    args = ap.parse_args()
    bundle = args.bundle.resolve()
    spec = validate(bundle)
    if args.validate_only:
        print(json.dumps({'valid': True, 'mode': 'offline_validation_only', 'planned_generations': 5,
                          'takes': spec['takes'], 'cap_seconds': 5400, 'new_gpu_jobs': 0}))
        return
    if args.seconds != 5400 or not Path('/kaggle/input').is_dir():
        raise ValueError('Only the fixed90-minute private Kaggle experiment may execute')
    started = time.monotonic()
    # Reserve ten seconds for the original run_bounded process-group teardown.
    deadline = started + 5390
    output = Path('/kaggle/working/jml-v2-warm-ab-results')
    output.mkdir(parents=True, exist_ok=True)
    state_path = output/'job.json'
    if state_path.exists():
        raise ValueError('Existing experiment preserved; no retry/overwrite')
    state = {'status': 'starting', 'cap_seconds': 5400, 'active_work_seconds': 5390,
             'automatic_retries': 0, 'started_unix': time.time(), 'stages': [],
             'package_lock_sha256': sha256(bundle/'package-lock.json'),
             'experiment_sha256': sha256(bundle/'experiment.json'), 'production_promotion': False}
    save_json(state_path, state)
    cache_root = Path('/tmp/jml-v2-warm-ab-runtime')
    cache_root.mkdir(parents=True, exist_ok=True)
    try:
        protected = torch_constraints()
        state['managed_packages'] = protected
        constraints = cache_root/'managed-constraints.txt'
        constraints.write_text(''.join(f'{name}=={version}\n' for name, version in sorted(protected.items())))
        python = install_environment(cache_root/'venv', bundle/'requirements.txt', constraints,
                                     deadline=deadline, log=output/'bootstrap.log')
        verify = ('import torch; expected='+repr(protected['torch'])+
                  '; assert torch.__version__ == expected; assert torch.cuda.is_available(); print(torch.__version__,torch.version.cuda)')
        run_bounded([str(python), '-c', verify], deadline=deadline, log=output/'bootstrap.log')
        env = os.environ.copy()
        env.update(PYTHONUNBUFFERED='1', USE_TF='0', USE_FLAX='0', HF_HUB_DISABLE_IMPLICIT_TOKEN='1',
                   HF_HUB_DISABLE_TELEMETRY='1', HF_XET_CHUNK_CACHE_SIZE_BYTES='0', TOKENIZERS_PARALLELISM='false',
                   PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python', IMAGEIO_FFMPEG_NO_PREVENT_SIGINT='1')
        jobs = [('setup', 'prepare', None), ('cold-A', 'cold', 'V2WH01'),
                ('cold-B', 'cold', 'V2WC01'), ('warm', 'warm', None)]
        for label, mode, take in jobs:
            target = output/label; target.mkdir()
            item = {'label': label, 'mode': mode, 'take_id': take, 'status': 'starting', 'attempts': 1}
            state['stages'].append(item); save_json(state_path, state)
            began = time.monotonic()
            command = [str(python), str(bundle/'experiment_child.py'), '--mode', mode, '--bundle', str(bundle),
                       '--output', str(target), '--cache', str(cache_root/'cache')]
            if take:
                command += ['--take', take]
            run_bounded(command, deadline=deadline, log=target/'runner.log', env=env)
            item.update(status='complete', driver_elapsed_seconds=time.monotonic()-began)
            save_json(state_path, state)
        run_bounded([str(python), str(bundle/'compare_experiment.py'), '--output', str(output),
                     '--spec', str(bundle/'experiment.json')], deadline=deadline, log=output/'comparison.log', env=env)
        state['status'] = 'experimental_checks_passed_pending_root_review'
    except Exception as exc:
        state.update(status='stopped_no_retry', error_type=type(exc).__name__, error=str(exc)[:1500])
        if state['stages'] and state['stages'][-1]['status'] == 'starting':
            state['stages'][-1]['status'] = 'failed_or_deadline'
        raise
    finally:
        state['elapsed_seconds'] = time.monotonic()-started
        save_json(state_path, state)
        print(json.dumps(state, indent=2), flush=True)


if __name__ == '__main__':
    main()
