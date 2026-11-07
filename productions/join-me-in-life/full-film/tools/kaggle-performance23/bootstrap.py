#!/usr/bin/env python3
"""Kaggle-only bootstrap: retain managed Torch; bound and clean child processes."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from common import verify_package, validate_queue, save_json


def run_bounded(command, *, deadline, log, env=None):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('Whole-job time budget exhausted before the next stage')
    with Path(log).open('ab') as output:
        process = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True, env=env)
        try:
            code = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
            raise TimeoutError('Whole-job deadline reached; child process group stopped') from None
    if code:
        raise subprocess.CalledProcessError(code, command)


def torch_constraints():
    """Constrain managed CUDA packages; pip may add SDK packages, not replace Torch."""
    protected = {}
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata['Name'].lower().replace('_', '-')
        if name in {'torch', 'torchvision', 'torchaudio', 'triton'} or name.startswith('nvidia-'):
            protected[name] = distribution.version
    if 'torch' not in protected:
        raise RuntimeError('The Kaggle managed Torch installation is required')
    return protected


def install_environment(environment, requirements, constraints, *, deadline, log, host_python=None):
    """Use managed host pip to populate a venv without invoking ensurepip."""
    host_python = host_python or sys.executable
    run_bounded([host_python, '-m', 'venv', '--without-pip', '--system-site-packages', str(environment)],
                deadline=deadline, log=log)
    python = environment / 'bin/python'
    installer = [host_python, '-m', 'pip', '--python', str(python)]
    # pip >=22.3 can manage an environment that has no pip of its own. Probe
    # actual support on the host; fail before downloads if the option is absent.
    run_bounded(installer + ['--version'], deadline=deadline, log=log)
    run_bounded(installer + ['install', '--disable-pip-version-check',
                '--upgrade-strategy', 'only-if-needed', '-c', str(constraints), '-r', str(requirements)],
                deadline=deadline, log=log)
    return python


def run_serial_jobs(python, bundle, manifests, output, cache, *, deadline, env, state, state_path):
    """Fresh child per selected shot; share only installed dependencies and cached weights."""
    state['shots'] = []
    for path in manifests:
        child_output = output / path.stem
        child_output.mkdir(parents=True, exist_ok=True)
        item = {'shot_id': path.stem, 'status': 'starting', 'attempts': 1,
                'manifest': path.name, 'output': str(child_output)}
        state['shots'].append(item)
        save_json(state_path, state)
        started = time.monotonic()
        try:
            run_bounded([str(python), str(bundle / 'run.py'), '--manifest', str(path),
                         '--output', str(child_output), '--cache', str(cache)],
                        deadline=deadline, log=child_output / 'runner.log', env=env)
            item['status'] = 'child_complete_unreviewed'
        except (subprocess.CalledProcessError, TimeoutError) as error:
            item.update(status='failed', error_type=type(error).__name__, error=str(error)[:600])
            save_json(child_output / 'failure.json', item)
            if isinstance(error, TimeoutError):
                for unstarted in manifests[len(state['shots']):]:
                    state['shots'].append({'shot_id': unstarted.stem, 'status': 'not_started_deadline', 'attempts': 0})
                raise
            # A failed first take is not retried. The distinct second requested take may run.
        finally:
            item['elapsed_seconds'] = time.monotonic() - started
            save_json(state_path, state)
    return all(item['status'] == 'child_complete_unreviewed' for item in state['shots'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=5400)
    args = parser.parse_args()
    if not 60 <= args.seconds <= 5400:
        parser.error('Whole-job cap must be 60–5400 seconds')
    if not Path('/kaggle/input').is_dir():
        raise SystemExit('This bootstrap is intended only for the verified private Kaggle runtime')
    started = time.monotonic()
    deadline = started + args.seconds
    bundle = args.bundle.resolve()
    verify_package(bundle)
    manifests = validate_queue(json.loads((bundle / 'queue.json').read_text()), bundle)
    output = Path('/kaggle/working/jml-ltx-performance23-results')
    output.mkdir(parents=True, exist_ok=True)
    state = {'status': 'starting', 'cap_seconds': args.seconds, 'started_unix': time.time(),
             'remote_privacy': 'Must be verified by owner; a local manifest cannot prove account visibility'}
    state_path = output / 'job.json'
    if state_path.exists():
        raise ValueError('Existing serial attempt preserved; no automatic retry or overwrite')
    cache = Path('/tmp/jml-ltx-performance23-runtime')
    cache.mkdir(parents=True, exist_ok=True)
    try:
        protected = torch_constraints()
        state['managed_packages'] = protected
        state_path.write_text(json.dumps(state, indent=2) + '\n')
        constraints = cache / 'managed-constraints.txt'
        constraints.write_text(''.join(f'{name}=={version}\n' for name, version in sorted(protected.items())))
        environment = cache / 'venv'
        state['installer'] = 'managed host pip --python; venv created without ensurepip'
        python = install_environment(environment, bundle / 'requirements.txt', constraints,
                                     deadline=deadline, log=output / 'bootstrap.log')
        verify = ('import torch; expected=' + repr(protected['torch'])
                  + '; assert torch.__version__ == expected, (torch.__version__,expected); '
                    'assert torch.cuda.is_available(); print(torch.__version__,torch.version.cuda)')
        run_bounded([str(python), '-c', verify], deadline=deadline, log=output / 'bootstrap.log')
        child_env = os.environ.copy()
        child_env.update({'PYTHONUNBUFFERED': '1', 'USE_TF': '0', 'USE_FLAX': '0',
                          'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1', 'IMAGEIO_FFMPEG_NO_PREVENT_SIGINT': '1',
                          'HF_XET_CHUNK_CACHE_SIZE_BYTES': '0', 'HF_HUB_DISABLE_TELEMETRY': '1',
                          'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION': 'python',
                          'TOKENIZERS_PARALLELISM': 'false'})
        complete = run_serial_jobs(python, bundle, manifests, output, cache / 'cache',
                                   deadline=deadline, env=child_env, state=state, state_path=state_path)
        state['status'] = 'bounded_job_complete' if complete else 'completed_with_failed_shot'
        state['acceptance'] = 'unreviewed'
    except Exception as error:
        state['status'] = 'failed'
        state['error_type'] = type(error).__name__
        state['error'] = str(error)[:600]
        raise
    finally:
        state['elapsed_seconds'] = time.monotonic() - started
        state_path.write_text(json.dumps(state, indent=2) + '\n')
        print(json.dumps(state, indent=2), flush=True)


if __name__ == '__main__':
    main()
