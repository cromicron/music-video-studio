"""Small, dependency-free integrity checks shared by staging/bootstrap/runner."""
import base64
import binascii
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import zipfile

HERE = Path(__file__).resolve().parent
GIB = 1024 ** 3
TAKES = json.loads((HERE / 'take-specs.json').read_text())
QUEUES = json.loads((HERE / 'queues.json').read_text())
ALLOWED_FRAMES = frozenset(spec['frames'] for spec in TAKES.values())


def sha256(path):
    with Path(path).open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def inside(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('Only relative bundle inputs are supported')
    path = (Path(root) / relative).resolve()
    if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
        raise ValueError('Missing input or path outside private bundle')
    return path


def validate_manifest(manifest, root):
    if (manifest.get('schema'), manifest.get('privacy'), manifest.get('mode')) != ('jml-ltx-story23/v1', 'private', 'diagnostic'):
        raise ValueError('Require explicit private single-diagnostic manifest')
    if manifest.get('takes') != 1 or manifest.get('seed') != 49:
        raise ValueError('Exactly one seed49 take; no batches or automatic retries')
    selected = TAKES.get(manifest.get('take_id'))
    if not selected:
        raise ValueError('Only explicitly selected story takes are permitted')
    if manifest.get('queue_id') != selected['queue_id']:
        raise ValueError('Take belongs to another selected queue')
    frames = selected['frames']
    if tuple(manifest.get(x) for x in ('width', 'height', 'frames', 'fps')) != (896, 512, frames, 24):
        raise ValueError('Require selected 8n+1 frame count at896x512 and natural24fps')
    if manifest.get('editorial') != selected['editorial']:
        raise ValueError('Editorial slots, source portions or handles changed')
    if manifest.get('start_image') != manifest.get('end_image'):
        raise ValueError('Quiet take must use the SAME reviewed first and last source')
    if not isinstance(manifest.get('prompt'), str) or not manifest['prompt'].strip():
        raise ValueError('Two-image diagnostic requires its exact non-empty prompt')
    if any(k in manifest for k in ('audio', 'audio_pcm', 'input_waveform', 'intermediate_images')):
        raise ValueError('Only the two selected image guides; no supplied audio or extra guides')
    if (manifest.get('start_frame_index'), manifest.get('end_frame_index')) != (0, frames - 1):
        raise ValueError('Require first index0 and last pixel index frames-1')
    if manifest.get('model_audio_output') is not False or manifest.get('supplied_audio') is not False:
        raise ValueError('Explicitly require no supplied audio and no output model audio')
    dimensions = {}
    for field in ('start_image', 'end_image'):
        path = inside(root, manifest.get(field))
        if sha256(path) != manifest.get(field + '_sha256') or manifest.get(field + '_sha256') != selected['sha256']:
            raise ValueError('Input SHA256 mismatch: ' + field)
        header = path.read_bytes()[:24]
        if header[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('The exact original PNG inputs are required')
        dimensions[field] = list(struct.unpack('>II', header[16:24]))
        if dimensions[field] != manifest.get(field + '_dimensions') or dimensions[field] != selected['dimensions']:
            raise ValueError('Source dimensions changed: ' + field)
    provenance_path = inside(root, manifest.get('source_provenance'))
    if sha256(provenance_path) != manifest.get('source_provenance_sha256'):
        raise ValueError('Source provenance hash mismatch')
    provenance = json.loads(provenance_path.read_text())
    if (provenance.get('privacy') != 'private' or provenance.get('take_id') != manifest['take_id']
            or provenance.get('queue_id') != selected['queue_id']
            or provenance.get('source_sha256') != selected['sha256']
            or provenance.get('source_dimensions') != selected['dimensions']
            or provenance.get('editorial_segments') != selected['editorial']['segments']
            or provenance.get('same_original_image_first_and_last') is not True):
        raise ValueError('Source provenance changed')
    return dimensions


def validate_queue(queue, root):
    if (queue.get('schema'), queue.get('privacy'), queue.get('automatic_retries')) != ('jml-story-queue/v1', 'private', 0):
        raise ValueError('Require explicit private serial queue without retries')
    selected = QUEUES.get(queue.get('queue_id'))
    if selected is None or queue.get('whole_job_seconds') != 5400:
        raise ValueError('Choose exactly Q2, Q3 or Q4 under the90-minute whole-job cap')
    expected = [take + '.json' for take in selected['takes']]
    if queue.get('manifests') != expected:
        raise ValueError('Only exact selected queue order; no auto-all, extra takes or repeats')
    if any(take not in TAKES for take in selected['takes']):
        raise ValueError('Selected queue is not present in this frozen package')
    staged = json.loads(inside(root, 'take-specs.json').read_text())
    if staged != {take: TAKES[take] for take in selected['takes']}:
        raise ValueError('Stage only the selected queue specifications')
    manifests = []
    for name in expected:
        path = inside(root, name)
        manifest = json.loads(path.read_text())
        if manifest.get('take_id') != path.stem or manifest.get('queue_id') != queue['queue_id']:
            raise ValueError('Child manifest/take/queue mismatch')
        validate_manifest(manifest, root)
        manifests.append(path)
    return manifests


def verify_package(root):
    root = Path(root)
    lock = json.loads((root / 'package-lock.json').read_text())
    for relative, expected in lock['files'].items():
        if sha256(inside(root, relative)) != expected:
            raise ValueError('Runtime/dependency/input integrity mismatch: ' + relative)
    return lock


def prepare_backend(bundle, destination):
    """Verify the entire source-only archive and apply exact, counted replacements."""
    bundle, destination = Path(bundle), Path(destination)
    lock = json.loads((bundle / 'source-lock.json').read_text())
    # Kaggle recursively expands uploaded ZIPs. Carry this one as strict ASCII Base64.
    transport = bundle / 'vendor/wangp-source.zip.b64'
    try:
        archive = base64.b64decode(transport.read_bytes(), validate=True)
    except binascii.Error as error:
        raise ValueError('Invalid Base64 backend transport') from error
    if hashlib.sha256(archive).hexdigest() != lock['archive_sha256']:
        raise ValueError('Pinned backend archive hash mismatch')
    rules = json.loads((bundle / 'patches.json').read_text())
    if destination.exists():
        raise ValueError('Choose a fresh backend directory; existing evidence is preserved')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(archive)) as source:
        if set(source.namelist()) != set(lock['archive_files']):
            raise ValueError('Backend archive differs from its exact source allowlist')
        for relative, expected in lock['archive_files'].items():
            target = (destination / relative).resolve()
            if not target.is_relative_to(destination.resolve()) or Path(relative).is_absolute():
                raise ValueError('Backend path escape')
            data = source.read(relative)
            if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
                raise ValueError('Pinned source file mismatch: ' + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    results = []
    for rule in rules:
        path = inside(destination, rule['path'])
        source = path.read_text()
        if source.count(rule['old']) != rule['expected_count']:
            raise ValueError('Source patch assertion failed: ' + rule['id'])
        if rule['expected_count']:
            source = source.replace(rule['old'], rule['new'])
            # A pinned source file carries a UTF-8 BOM; compile as Python file bytes.
            compile(source.encode('utf-8'), str(path), 'exec')
            path.write_text(source)
        results.append({'id': rule['id'], 'matches': rule['expected_count'], 'path': rule['path'],
                        'result_sha256': sha256(path), 'reason': rule['reason']})
    save_json(destination / 'jml-patch-report.json', results)
    return results


def download_weights(lock, model_dir):
    """Only called by the root-deployed GPU runner, after hardware/source preflight."""
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    missing = [item for item in lock['files'] if not (model_dir / item['path']).is_file()]
    required = sum(item['bytes'] for item in missing) + lock['cache_reserve_bytes']
    if shutil.disk_usage(model_dir).free < required:
        raise RuntimeError(f'Insufficient cache disk before download: need {required} bytes including reserve')
    from huggingface_hub import hf_hub_download
    for item in lock['files']:
        target = model_dir / item['path']
        if not target.is_file():
            hf_hub_download(repo_id=lock['repository'], revision=lock['revision'], filename=item['path'],
                            local_dir=model_dir, token=False)
        if target.stat().st_size != item['bytes'] or sha256(target) != item['sha256']:
            raise ValueError('Converted model file size/hash mismatch: ' + item['path'])
    return model_dir
