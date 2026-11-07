#!/usr/bin/env python3
"""Prepare selected v2 A2V diagnostics locally; never upload or submit."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import wave
import zipfile

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
REPO = FILM.parents[2]
BASE = FILM / 'tools/kaggle-performance23'
MASTER = FILM.parent / 'full-song/track-49.mp3'
MASTER_SHA256 = '0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def bound_source(record):
    p = (REPO / record['path']).resolve()
    if not p.is_relative_to(REPO.resolve()) or not p.is_file() or sha(p) != record['sha256']:
        raise ValueError('Missing or changed independently bound source: ' + record['path'])
    return p


def replace_exact(text, old, new, count):
    if text.count(old) != count:
        raise ValueError('Proven wrapper adaptation count changed: ' + old)
    return text.replace(old, new)


def prepare(destination, plan_path=HERE / 'plan-v1.json'):
    plan = json.loads(Path(plan_path).read_text())
    if plan['schema'] != 'jml-v2-performance-plan/v1' or plan['state'] != 'ready_for_local_staging':
        raise ValueError('Explicit local staging plan required')
    if [t['shot_id'] for t in plan['takes']] != ['V2-36', 'V2-21']:
        raise ValueError('Keep the exact selected order: first plea, then longer summer trial')
    locks = json.loads((HERE / 'base-runtime-lock.json').read_text())
    for name, expected in locks['files'].items():
        if sha(BASE / name) != expected:
            raise ValueError('Proven engine/source changed: ' + name)
    if sha(MASTER) != MASTER_SHA256:
        raise ValueError('Original master changed')
    destination = Path(destination).resolve()
    kernel = destination.with_name(destination.name + '-kernel')
    archive = destination.with_suffix('.zip')
    if any(p.exists() for p in (destination, kernel, archive)):
        raise ValueError('Fresh destination required; preserve existing evidence')
    for take in plan['takes']:
        bound_source(take['image'])
        bound_source(take['source_review'])
    destination.mkdir(parents=True)
    for name in ['common.py', 'bootstrap.py', 'run.py', 'runtime.py', 'requirements.txt',
                 'source-lock.json', 'model-lock.json', 'patches.json', 'NOTICE.md']:
        shutil.copy2(BASE / name, destination / name)
    # The complete neural runtime remains byte-identical. Its existing SHOTS
    # lookup receives the bounded v2 table; validation is frozen independently.
    with (destination / 'common.py').open('a') as stream:
        stream.write('\n# V2 adapts only selected source/audio/queue contracts.\n'
                     'from validation_v2 import validate_manifest, validate_queue\n'
                     'SHOTS = {key: {"frames": value["manifest"]["frames"]} for key, value in '
                     'json.loads((HERE / "take-specs.json").read_text()).items()}\n')
    shutil.copy2(HERE / 'validation_v2.py', destination / 'validation_v2.py')
    run = (destination / 'run.py').read_text()
    run = replace_exact(run, 'expected_frames not in {89, 105}',
                        "expected_frames not in {value['frames'] for value in SHOTS.values()}", 2)
    run = run.replace('jml-ltx-performance23-results', 'jml-v2-performance-a-results').replace(
        'jml-ltx-performance23-runtime', 'jml-v2-performance-a-runtime')
    (destination / 'run.py').write_text(run)
    bootstrap = (destination / 'bootstrap.py').read_text().replace(
        'jml-ltx-performance23-results', 'jml-v2-performance-a-results').replace(
        'jml-ltx-performance23-runtime', 'jml-v2-performance-a-runtime')
    (destination / 'bootstrap.py').write_text(bootstrap)
    shutil.copytree(BASE / 'vendor', destination / 'vendor',
                    ignore=shutil.ignore_patterns('.gitignore', 'wangp-source.zip'))
    (destination / 'vendor/wangp-source.zip.b64').write_bytes(base64.b64encode((BASE / 'vendor/wangp-source.zip').read_bytes()))
    # Decode once without resampling/gain filters. Exact sample slices are the
    # full master reference against which every exported WAV is checked.
    full_pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(MASTER),
                                       '-map', '0:a:0', '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
    specs = {}
    for take in plan['takes']:
        sid, frames = take['shot_id'], take['frames']
        timeline = take['timeline_frames']; start_sample = (timeline[0] - 6) * 2000
        samples = frames * 2000; end_sample = start_sample + samples
        pcm = full_pcm[start_sample * 4:end_sample * 4]
        if len(pcm) != samples * 4:
            raise ValueError('Selected original excerpt exceeds decoded source')
        image_name = f'inputs/{sid}-start.png'
        audio_name = f'inputs/{sid}-conditioning.wav'
        audio_prov_name = f'inputs/{sid}-conditioning.json'
        image_prov_name = f'inputs/{sid}-source.json'
        review_name = f'inputs/{sid}-independent-static-review.json'
        (destination / 'inputs').mkdir(exist_ok=True)
        shutil.copy2(bound_source(take['image']), destination / image_name)
        shutil.copy2(bound_source(take['source_review']), destination / review_name)
        with wave.open(str(destination / audio_name), 'wb') as audio:
            audio.setparams((2, 2, 48000, samples, 'NONE', 'not compressed'))
            audio.writeframes(pcm)
        audio_prov = {'schema': 'jml-v2-original-song-excerpt/v1', 'source_master_sha256': MASTER_SHA256,
            'source_master_path_from_repository': str(MASTER.relative_to(REPO)),
            'conditioning_sha256': sha(destination / audio_name), 'pcm_sha256': hashlib.sha256(pcm).hexdigest(),
            'start_sample': start_sample, 'end_sample_exclusive': end_sample, 'start_seconds': start_sample / 48000,
            'samples': samples, 'sample_rate': 48000, 'channels': 2, 'sample_width_bytes': 2,
            'target_edit_shot': sid, 'target_edit_frames': timeline,
            'derivation': 'Decode entire original master to stereo PCM16 at its native48k; take exact sample slice. No gain/resampling/padding/retiming.',
            'decoded_reference_slice_equal': True, 'subjective_listening_claimed': False}
        save(destination / audio_prov_name, audio_prov)
        header = (destination / image_name).read_bytes()[:24]
        dims = list(struct.unpack('>II', header[16:24]))
        image_prov = {'schema': 'jml-v2-performance-source-adoption/v1', 'shot_id': sid,
            'image_sha256': take['image']['sha256'], 'image_original': take['image']['path'],
            'review_bundle_path': review_name, 'review_sha256': take['source_review']['sha256'],
            'review_original': take['source_review']['path'], 'panel': take['source_review']['panel'],
            'review_scope': 'Exact reviewed native crop copied byte-identically; static suitability only.',
            'catalog_record': take['catalog_record'], 'motion_approval': False}
        save(destination / image_prov_name, image_prov)
        source_end = 6 + timeline[1] - timeline[0]
        manifest = {'schema': 'jml-ltx-performance-v2/v1', 'privacy': 'private', 'mode': 'diagnostic',
            'shot_id': sid, 'queue_id': plan['queue_id'], 'takes': 1, 'seed': 49,
            'width': 896, 'height': 512, 'frames': frames, 'fps': 24,
            'image': image_name, 'image_sha256': sha(destination / image_name), 'image_dimensions': dims,
            'audio': audio_name, 'audio_sha256': sha(destination / audio_name),
            'audio_provenance': audio_prov_name, 'audio_provenance_sha256': sha(destination / audio_prov_name),
            'image_provenance': image_prov_name, 'image_provenance_sha256': sha(destination / image_prov_name),
            'audio_pcm': {key: audio_prov[key] for key in ('samples', 'sample_rate', 'channels', 'sample_width_bytes')},
            'supplied_audio': True, 'model_audio_output': False, 'prompt': take['prompt'],
            'conditioning': {'first_image_only': True, 'end_image_supported_in_this_wrapper': False,
                'full_audio_latent_coverage_required': True, 'audio_scale': 1.0, 'prompt_truncation_allowed': False,
                'review_audio': 'Original stereo PCM preserved; internal mono mean is unchanged proven conditioning.'},
            'editorial': {'timeline_frames': timeline, 'source_frames': [6, source_end], 'fps': 24,
                'head_handle_frames': 6, 'tail_handle_frames': frames - source_end},
            'action_contract': take['action_contract'], 'hardware_limit': take['hardware_limit'],
            'production_gate': 'No automatic acceptance or retry. Independent actual movement/song/cut review required.',
            'state': 'prepared_not_submitted'}
        save(destination / (sid + '.json'), manifest)
        specs[sid] = {'manifest': manifest}
    queue = {'schema': 'jml-v2-performance-queue/v1', 'queue_id': plan['queue_id'],
        'privacy': 'private', 'automatic_retries': 0, 'manifests': ['V2-36.json', 'V2-21.json'],
        'whole_job_seconds': 5390, 'provider_cap_seconds': 5400,
        'execution': 'Two fresh serial children; shared installed dependencies and disk weights; separate failures; no warm cache.'}
    save(destination / 'take-specs.json', specs)
    save(destination / 'queue-spec.json', queue)
    save(destination / 'queue.json', queue)
    save(destination / 'dataset-metadata.json', {'title': plan['dataset_title'], 'id': plan['dataset_id'],
        'licenses': [{'name': 'other'}], 'description': 'Private reviewed v2 performance images and exact original-song excerpts; no full song or public sharing.'})
    files = {str(p.relative_to(destination)): sha(p) for p in sorted(destination.rglob('*'))
             if p.is_file() and p.name != 'dataset-metadata.json'}
    save(destination / 'package-lock.json', {'schema': 'jml-private-performance-v2-bundle/v1',
        'files': files, 'base_runtime': locks, 'adaptation_scope': 'Frozen v2 validators and SHOTS table; codec frame whitelist; isolated output/cache names. Entire neural runtime and backend/model/dependency pins unchanged.'})
    for sid in specs:
        subprocess.run([sys.executable, '-B', str(destination / 'run.py'), '--manifest', str(destination / (sid + '.json')), '--validate-only'],
                       check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, '-B', '-c', 'import json,common;common.validate_queue(json.load(open("queue.json")),".")'],
                   cwd=destination, check=True, capture_output=True, text=True)
    kernel.mkdir()
    metadata = json.loads((BASE / 'kernel-metadata.json').read_text())
    metadata.update(id=plan['kernel_id'], title=plan['kernel_title'], dataset_sources=[plan['dataset_id']])
    save(kernel / 'kernel-metadata.json', metadata)
    notebook = json.loads((BASE / 'private-diagnostic.ipynb').read_text())
    slug = plan['dataset_id'].split('/')[-1]
    notebook['cells'][0]['source'] = ['# Join Me in Life v2 — private original-song performance tests\n',
        'One first full-force plea97-frame take, then one121-frame summer trial. Six head frames, exact original stereo PCM, no retries or accepted motion. The longer A2V length is unproven. Provider cap90minutes; bootstrap5390seconds leaves teardown reserve.\n']
    code = ''.join(notebook['cells'][1]['source']).replace('WHOLE_JOB_SECONDS = 5400', 'WHOLE_JOB_SECONDS = 5390').replace(
        'jml-ltx-performance23-private-inputs', slug).replace('timeout=WHOLE_JOB_SECONDS + 60', 'timeout=5400')
    notebook['cells'][1]['source'] = code.splitlines(keepends=True)
    save(kernel / 'private-diagnostic.ipynb', notebook)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for p in sorted(destination.rglob('*')):
            if p.is_file():
                package.write(p, str(p.relative_to(destination)))
    return {'state': 'local_preparation_only', 'bundle': str(destination), 'kernel': str(kernel), 'archive': str(archive),
        'archive_sha256': sha(archive), 'package_lock_sha256': sha(destination / 'package-lock.json'),
        'plan_sha256': sha(plan_path), 'queue_id': plan['queue_id'], 'takes': list(specs),
        'locked_files': len(files), 'neural_runtime_byte_identical': sha(destination / 'runtime.py') == sha(BASE / 'runtime.py'),
        'remote_calls': 0, 'inference_jobs': 0, 'provider_cap_seconds': 5400, 'bootstrap_seconds': 5390,
        'new_frame_lengths_hardware_tested': False, 'motion_approved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--plan', type=Path, default=HERE / 'plan-v1.json')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = prepare(args.output, args.plan)
    if args.report:
        save(args.report, result)
    print(json.dumps(result, indent=2))
