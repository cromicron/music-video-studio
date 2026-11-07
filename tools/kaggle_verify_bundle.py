#!/usr/bin/env python3
"""Verify freshly retrieved private Kaggle inputs against a frozen local bundle.

Read-only toward Kaggle: download metadata, notebook and dataset first. This tool
never submits a job. It does not claim that local checks executed on a GPU mount.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def cell_sources(path):
    return [(cell['cell_type'], ''.join(cell['source']) if isinstance(cell['source'], list)
             else cell['source']) for cell in read(path)['cells']]


def verify(bundle, evidence, expected_lock, version):
    bundle, evidence = bundle.resolve(), evidence.resolve()
    inputs = evidence / 'inputs'
    local_kernel = bundle.with_name(bundle.name + '-kernel')
    expected_meta = read(local_kernel / 'kernel-metadata.json')
    remote_meta = read(evidence / 'kernel-metadata.json')
    dataset = read(evidence / 'dataset-metadata.json')['info']
    dataset_id = dataset['ownerUser'] + '/' + dataset['datasetSlug']
    assert dataset['isPrivate'] is True, 'Actual dataset must be private'
    assert remote_meta['is_private'] is True, 'Actual notebook must be private'
    assert dataset_id == read(bundle / 'dataset-metadata.json')['id']
    for key in ('id', 'enable_gpu', 'enable_internet', 'machine_shape', 'docker_image',
                'dataset_sources', 'kernel_sources', 'competition_sources', 'model_sources'):
        assert remote_meta[key] == expected_meta[key], ('Remote notebook setting differs', key)
    assert remote_meta['dataset_sources'] == [dataset_id]
    assert digest(inputs / 'package-lock.json') == digest(bundle / 'package-lock.json') == expected_lock
    lock = read(inputs / 'package-lock.json')
    for name, expected in lock['files'].items():
        path = (inputs / name).resolve()
        assert path.is_relative_to(inputs) and path.is_file(), name
        assert digest(path) == expected, ('Retrieved file differs', name)
    archive = base64.b64decode((inputs / 'vendor/wangp-source.zip.b64').read_bytes(), validate=True)
    archive_sha = hashlib.sha256(archive).hexdigest()
    assert archive_sha == read(inputs / 'source-lock.json')['archive_sha256']
    assert cell_sources(evidence / remote_meta['code_file']) == cell_sources(local_kernel / expected_meta['code_file'])
    queue = inputs / 'queue.json'
    manifests = read(queue)['manifests'] if queue.exists() else ['pilot.json']
    for name in manifests:
        result = subprocess.run([sys.executable, str(inputs / 'run.py'), '--manifest',
                                 str(inputs / name), '--validate-only'], capture_output=True, text=True)
        (evidence / (Path(name).stem + '-validation.log')).write_text(result.stdout + result.stderr)
        assert result.returncode == 0, ('Retrieved manifest validation failed', name)
    report = {
        'private_dataset': True, 'private_notebook': True,
        'accelerator': remote_meta['machine_shape'], 'attached_dataset': [dataset_id],
        'exact_locked_files_verified': len(lock['files']), 'package_lock_sha256': expected_lock,
        'source_archive_base64_present_and_exact': True, 'decoded_source_archive_sha256': archive_sha,
        'notebook_source_text_exact': True,
        'retrieved_dataset_inputs_and_all_manifests_validation_passed': True,
        'verification_scope': 'Freshly retrieved private dataset files validated locally without consumed metadata; GPU bootstrap independently checks its mount before inference.',
        'notebook': remote_meta['id'], 'no_run_version': version, 'generation_submitted': False,
        'validated_manifests': manifests,
    }
    (evidence / 'verified.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--expected-lock', required=True)
    parser.add_argument('--notebook-version', type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.bundle, args.evidence, args.expected_lock, args.notebook_version), indent=2))
