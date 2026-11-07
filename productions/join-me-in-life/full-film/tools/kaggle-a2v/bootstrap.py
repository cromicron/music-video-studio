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

from common import verify_package, validate_manifest


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=5400)
    parser.add_argument('--preflight-only', action='store_true')
    args = parser.parse_args()
    if not 60 <= args.seconds <= 5400:
        parser.error('Whole-job cap must be 60–5400 seconds')
    if not Path('/kaggle/input').is_dir():
        raise SystemExit('This bootstrap is intended only for the verified private Kaggle runtime')
    started = time.monotonic()
    deadline = started + args.seconds
    bundle = args.bundle.resolve()
    manifest = json.loads((bundle / 'pilot.json').read_text())
    verify_package(bundle)
    validate_manifest(manifest, bundle)
    output = Path('/kaggle/working/jml-ltx-a2v-results')
    output.mkdir(parents=True, exist_ok=True)
    state = {'status': 'starting', 'cap_seconds': args.seconds, 'started_unix': time.time(),
             'remote_privacy': 'Must be verified by owner; a local manifest cannot prove account visibility'}
    state_path = output / 'job.json'
    cache = Path('/tmp/jml-ltx-a2v-runtime')
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
        command = [str(python), str(bundle / 'run.py'), '--manifest', str(bundle / 'pilot.json'),
                   '--output', str(output), '--cache', str(cache / 'cache')]
        if args.preflight_only:
            command.append('--preflight-only')
        run_bounded(command, deadline=deadline, log=output / 'runner.log', env=child_env)
        state['status'] = 'preflight_complete' if args.preflight_only else 'bounded_job_complete'
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
