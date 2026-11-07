#!/usr/bin/env python3
"""Create one local private upload bundle and notebook; never upload or execute."""
import argparse
import base64
import json
from pathlib import Path
import shutil
import zipfile

from common import sha256, validate_manifest, save_json

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
    shutil.copy2(FILM.parent / 'current/assets/M02_Summer_Start.png', destination / 'summer_start.png')
    shutil.copy2(FILM / 'assets/summer_identity_end_v2_candidate.png', destination / 'summer_end.png')
    manifest = json.loads((HERE / 'pilot-template.json').read_text())
    save_json(destination / 'pilot.json', manifest)
    validate_manifest(manifest, destination)
    save_json(destination / 'dataset-metadata.json', {
        'title': 'Join Me in Life private I2V23 inputs',
        'id': 'darionalis/jml-ltx-i2v23-private-inputs', 'licenses': [{'name': 'other'}],
        'description': 'Private owned start/end artwork, bounded one-take summer I2V source. No audio upload or public sharing.'})
    # Kaggle consumes dataset-metadata.json as transport configuration and does not upload it.
    # Runtime integrity covers the actual mounted source, dependencies and inputs only.
    files = {str(path.relative_to(destination)): sha256(path) for path in sorted(destination.rglob('*'))
             if path.is_file() and path != destination / 'dataset-metadata.json'}
    save_json(destination / 'package-lock.json', {'schema': 'jml-private-i2v23-bundle/v1', 'files': files})
    kernel.mkdir()
    for name in ['private-diagnostic.ipynb', 'kernel-metadata.json']:
        shutil.copy2(HERE / name, kernel / name)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                package.write(path, str(path.relative_to(destination)))
    result = {'bundle': str(destination), 'kernel': str(kernel), 'zip': str(archive),
              'zip_sha256': sha256(archive), 'package_lock_sha256': sha256(destination / 'package-lock.json'),
              'state': 'local_preparation_only', 'remote_calls': 0, 'inference_jobs': 0, 'takes': 1,
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
