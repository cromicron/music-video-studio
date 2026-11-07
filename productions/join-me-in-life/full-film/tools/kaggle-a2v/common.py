"""Small, dependency-free integrity checks shared by staging/bootstrap/runner."""
import base64
import binascii
import hashlib
import io
import json
from pathlib import Path
import shutil
import wave
import zipfile

HERE = Path(__file__).resolve().parent
GIB = 1024 ** 3


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
    if (manifest.get('schema'), manifest.get('privacy'), manifest.get('mode')) != ('jml-ltx-a2v/v1', 'private', 'diagnostic'):
        raise ValueError('Require explicit private single-diagnostic manifest')
    if manifest.get('takes') != 1 or manifest.get('seed') != 49:
        raise ValueError('Exactly one seed49 take; no batches or automatic retries')
    if tuple(manifest.get(x) for x in ('width', 'height', 'frames', 'fps')) != (896, 512, 97, 24):
        raise ValueError('Diagnostic is fixed to 896x512, 97 frames (8n+1), 24 fps')
    if 'end_image' in manifest or not isinstance(manifest.get('prompt'), str) or not manifest['prompt'].strip():
        raise ValueError('First-image-only diagnostic requires its exact non-empty prompt')
    for field in ('image', 'audio', 'audio_provenance'):
        path = inside(root, manifest.get(field))
        if sha256(path) != manifest.get(field + '_sha256'):
            raise ValueError('Input SHA256 mismatch: ' + field)
    with wave.open(str(inside(root, manifest['audio'])), 'rb') as audio:
        actual = {'samples': audio.getnframes(), 'sample_rate': audio.getframerate(),
                  'channels': audio.getnchannels(), 'sample_width_bytes': audio.getsampwidth()}
        if audio.getcomptype() != 'NONE' or actual != manifest.get('audio_pcm'):
            raise ValueError('Exact PCM samples/rate/channels/width must match')
        if actual['sample_rate'] != 48000 or actual['channels'] != 2 or actual['sample_width_bytes'] != 2:
            raise ValueError('Preserve the supplied stereo48k PCM16 excerpt')
        if actual['samples'] * 24 < 97 * actual['sample_rate']:
            raise ValueError('Audio does not cover the entire video; no padding or prefix fallback')
    provenance = json.loads(inside(root, manifest['audio_provenance']).read_text())
    if (provenance['conditioning_sha256'] != manifest['audio_sha256']
            or provenance['start_sample'] != 9972000 or provenance['start_seconds'] != 207.75
            or any(provenance[key] != value for key, value in actual.items())):
        raise ValueError('Audio provenance does not match the exact supplied excerpt')
    return actual


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
