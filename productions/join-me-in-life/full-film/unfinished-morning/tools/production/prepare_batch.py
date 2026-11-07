#!/usr/bin/env python3
"""Stage a v2 action batch using the pinned engine; never upload or execute it."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
BASE = FILM / 'tools/kaggle-story23'


def sha256(path):
    with Path(path).open('rb') as source_file:
        return hashlib.file_digest(source_file, 'sha256').hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def source(film, record):
    relative = record['path']
    path = (film / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(film.resolve()) or not path.is_file():
        raise ValueError('Missing input or source outside full-film')
    if sha256(path) != record['sha256']:
        raise ValueError('Reviewed source hash changed: ' + relative)
    return path


def prepare(plan_path, destination, film=FILM):
    plan = json.loads(Path(plan_path).read_text())
    if (plan.get('schema'), plan.get('state'), plan.get('privacy')) != (
            'jml-v2-action-batch/v1', 'ready_for_local_staging', 'private'):
        raise ValueError('Replace draft fields and explicitly mark ready_for_local_staging')
    queue_id = plan['queue_id']
    if not re.fullmatch(r'C[A-Z0-9_-]{1,35}', queue_id):
        raise ValueError('Use a distinct C-prefixed queue ID')
    takes = plan['takes']
    ids = [take['take_id'] for take in takes]
    if not 1 <= len(takes) <= 5 or len(set(ids)) != len(ids) or any(not re.fullmatch(r'C[A-Z0-9_-]{1,35}', v) for v in ids):
        raise ValueError('Select one to five distinct C-prefixed takes')
    for key in ('dataset_id', 'kernel_id'):
        if not re.fullmatch(r'darionalis/[a-z0-9]+(?:-[a-z0-9]+)*', plan[key]) or '/jml-c-' not in plan[key]:
            raise ValueError('Use explicit new darionalis private C dataset/kernel slugs')
    locks = json.loads((HERE / 'base-runtime-lock.json').read_text())
    for relative, expected in locks['files'].items():
        if sha256(BASE / relative) != expected:
            raise ValueError('Pinned base changed; review before restaging: ' + relative)
    destination = Path(destination).resolve()
    kernel = destination.with_name(destination.name + '-kernel')
    archive = destination.with_suffix('.zip')
    if any(path.exists() for path in (destination, kernel, archive)):
        raise ValueError('Use a fresh destination; preserve existing evidence')
    # Validate original source bindings before making an uploadable directory.
    for take in takes:
        for field in ('start_image', 'end_image', 'source_review'):
            source(film, take[field])
        if take['source_review'].get('status') != 'pass':
            raise ValueError('Endpoint source review must pass before staging')
    destination.mkdir(parents=True)
    for name in ('common.py', 'bootstrap.py', 'run.py', 'runtime.py', 'requirements.txt',
                 'source-lock.json', 'model-lock.json', 'patches.json', 'NOTICE.md'):
        shutil.copy2(BASE / name, destination / name)
    with (destination / 'common.py').open('a') as f:
        f.write('\n# V2 changes only the frozen endpoint/queue contract.\nfrom validation_v2 import validate_manifest, validate_queue\n')
    shutil.copy2(HERE / 'validation_v2.py', destination / 'validation_v2.py')
    shutil.copytree(BASE / 'vendor', destination / 'vendor',
                    ignore=shutil.ignore_patterns('.gitignore', 'wangp-source.zip'))
    (destination / 'vendor/wangp-source.zip.b64').write_bytes(base64.b64encode((BASE / 'vendor/wangp-source.zip').read_bytes()))
    specs = {}
    for take in takes:
        ident = take['take_id']; frames = take['frames']
        manifest = {'schema': 'jml-ltx-story-v2/v1', 'privacy': 'private', 'mode': 'diagnostic',
                    'take_id': ident, 'queue_id': queue_id, 'takes': 1, 'seed': 49,
                    'width': 896, 'height': 512, 'frames': frames, 'fps': 24,
                    'start_frame_index': 0, 'end_frame_index': frames - 1,
                    'supplied_audio': False, 'model_audio_output': False, 'prompt': take['prompt'],
                    'action_contract': take['action_contract'], 'editorial': take['editorial']}
        provenance = {'privacy': 'private', 'take_id': ident, 'queue_id': queue_id,
                      'action_contract': take['action_contract'], 'source_review': dict(take['source_review'])}
        for field in ('start_image', 'end_image'):
            original = source(film, take[field]); target = f'inputs/{ident}-{field}.png'
            header = original.read_bytes()[:24]
            if header[:8] != b'\x89PNG\r\n\x1a\n':
                raise ValueError('Exact PNG endpoint required')
            dims = list(struct.unpack('>II', header[16:24]))
            (destination / target).parent.mkdir(exist_ok=True)
            shutil.copy2(original, destination / target)
            manifest[field] = target; manifest[field + '_sha256'] = take[field]['sha256'];manifest[field + '_dimensions'] = dims
            provenance[field] = dict(take[field], dimensions=dims)
        review_target = f'inputs/{ident}-source-review' + source(film, take['source_review']).suffix
        shutil.copy2(source(film, take['source_review']), destination / review_target)
        provenance['source_review']['bundle_path'] = review_target
        provenance_target = f'inputs/{ident}-provenance.json'
        save(destination / provenance_target, provenance)
        manifest['source_provenance'] = provenance_target;manifest['source_provenance_sha256'] = sha256(destination / provenance_target)
        save(destination / (ident + '.json'), manifest)
        specs[ident] = {'queue_id': queue_id, 'frames': frames, 'editorial': take['editorial'], 'manifest': manifest}
    queue = {'schema': 'jml-story-v2-queue/v1', 'queue_id': queue_id, 'privacy': 'private',
             'automatic_retries': 0, 'manifests': [take + '.json' for take in ids], 'whole_job_seconds': 5400,
             'execution': 'serial fresh children; shared installed environment and disk weight cache'}
    save(destination / 'take-specs.json', specs)
    save(destination / 'queues.json', {queue_id: {'takes': ids, 'queue': queue}})
    save(destination / 'queue.json', queue)
    save(destination / 'dataset-metadata.json', {'title': plan['dataset_title'], 'id': plan['dataset_id'],
         'licenses': [{'name': 'other'}], 'description': 'Private v2 action endpoints and reviewed source provenance; no song or public sharing.'})
    files = {str(p.relative_to(destination)): sha256(p) for p in sorted(destination.rglob('*'))
             if p.is_file() and p.name != 'dataset-metadata.json'}
    save(destination / 'package-lock.json', {'schema': 'jml-private-story-v2-bundle/v1', 'files': files,
         'base_runtime': locks, 'only_adaptation': 'common.py imports strict independently hashed v2 endpoint/queue validators'})
    # Exercise actual unchanged child validation and exact queue binding in a fresh process.
    for ident in ids:
        subprocess.run([sys.executable, str(destination / 'run.py'), '--manifest', str(destination / (ident + '.json')), '--validate-only'], check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, '-c', 'import json,common;common.validate_queue(json.load(open("queue.json")),".")'],
                   cwd=destination, check=True, capture_output=True, text=True)
    kernel.mkdir()
    metadata = json.loads((BASE / 'kernel-template.json').read_text())
    metadata.update(id=plan['kernel_id'], title=plan['kernel_title'], dataset_sources=[plan['dataset_id']])
    save(kernel / 'kernel-metadata.json', metadata)
    notebook = (BASE / 'private-diagnostic.ipynb').read_text().replace('__QUEUE__', queue_id).replace(
        '__DATASET_SLUG__', plan['dataset_id'].split('/')[-1]).replace('same reviewed source at both endpoints', 'independently reviewed start/end action drawings')
    save(kernel / 'private-diagnostic.ipynb', json.loads(notebook))
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(destination.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                z.write(path, str(path.relative_to(destination)))
    # Avoid transporting bytecode created by local validate-only subprocesses.
    for pycache in destination.rglob('__pycache__'):
        shutil.rmtree(pycache)
    return {'state': 'local_preparation_only', 'bundle': str(destination), 'kernel': str(kernel),
            'zip': str(archive), 'zip_sha256': sha256(archive), 'queue_id': queue_id,
            'takes': ids, 'remote_calls': 0, 'inference_jobs': 0,
            'runtime_sha256': sha256(destination / 'runtime.py'), 'bootstrap_sha256': sha256(destination / 'bootstrap.py'),
            'runner_sha256': sha256(destination / 'run.py'), 'source_guides': 'different, independently hashed PNG endpoints'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = prepare(args.plan, args.output)
    if args.report:
        save(args.report, result)
    print(json.dumps(result, indent=2))
