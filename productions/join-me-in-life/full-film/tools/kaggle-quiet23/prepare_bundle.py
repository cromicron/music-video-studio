#!/usr/bin/env python3
"""Create one local private four-take quiet-motion upload bundle and notebook; never upload or execute."""
import argparse
import base64
import json
from pathlib import Path
import shutil
import zipfile

from common import sha256, validate_manifest, validate_queue, save_json

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]


def prepare(destination):
    destination = Path(destination).resolve()
    kernel = destination.with_name(destination.name + '-kernel')
    archive = destination.with_suffix('.zip')
    if any(path.exists() for path in (destination, kernel, archive)):
        raise ValueError('Use a fresh output name; existing bundles are preserved')
    destination.mkdir(parents=True)
    names = ['common.py', 'bootstrap.py', 'run.py', 'runtime.py', 'requirements.txt', 'source-lock.json',
             'model-lock.json', 'patches.json', 'NOTICE.md']
    for name in names:
        shutil.copy2(HERE / name, destination / name)
    # Repository tracking rules are not runtime inputs and may be omitted by upload clients.
    shutil.copytree(HERE / 'vendor', destination / 'vendor',
                    ignore=shutil.ignore_patterns('.gitignore', 'wangp-source.zip'))
    # Keep canonical repository ZIP unchanged; avoid Kaggle's recursive archive expansion.
    (destination / 'vendor/wangp-source.zip.b64').write_bytes(
        base64.b64encode((HERE / 'vendor/wangp-source.zip').read_bytes()))
    shots = json.loads((HERE / 'takes-template.json').read_text())
    for manifest in shots:
        shutil.copy2(FILM / manifest['source_relative_to_full_film'], destination / manifest['start_image'])
        shutil.copy2(HERE / 'provenance' / manifest['source_provenance'], destination / manifest['source_provenance'])
        save_json(destination / (manifest['take_id'] + '.json'), manifest)
        validate_manifest(manifest, destination)
    queue = {'schema': 'jml-quiet-queue/v1', 'privacy': 'private', 'automatic_retries': 0,
             'manifests': ['L01.json', 'A06.json', 'L04.json', 'L05.json'], 'whole_job_seconds': 5400,
             'execution': 'serial fresh children; shared environment and weight cache; no all-prompt cache'}
    save_json(destination / 'queue.json', queue)
    validate_queue(queue, destination)
    save_json(destination / 'dataset-metadata.json', {
        'title': 'Join Me in Life private quiet inputs',
        'id': 'darionalis/jml-ltx-quiet23-private-inputs', 'licenses': [{'name': 'other'}],
        'description': 'Private reviewed artwork for four bounded quiet-motion diagnostics, same first/end image per take. No song or public sharing.'})
    # Kaggle consumes dataset-metadata.json as transport configuration and does not upload it.
    # Runtime integrity covers the actual mounted source, dependencies and inputs only.
    files = {str(path.relative_to(destination)): sha256(path) for path in sorted(destination.rglob('*'))
             if path.is_file() and path != destination / 'dataset-metadata.json'}
    save_json(destination / 'package-lock.json', {'schema': 'jml-private-quiet-bundle/v1', 'files': files})
    kernel.mkdir()
    for name in ['private-diagnostic.ipynb', 'kernel-metadata.json']:
        shutil.copy2(HERE / name, kernel / name)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                package.write(path, str(path.relative_to(destination)))
    result = {'bundle': str(destination), 'kernel': str(kernel), 'zip': str(archive),
              'zip_sha256': sha256(archive), 'package_lock_sha256': sha256(destination / 'package-lock.json'),
              'state': 'local_preparation_only', 'remote_calls': 0, 'inference_jobs': 0, 'takes': 4, 'takes_per_shot': 1, 'serial': True,
              'audio_included': False, 'model_audio_output': False}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = prepare(args.output)
    if args.report:
        save_json(args.report, result)
    print(json.dumps(result, indent=2))
