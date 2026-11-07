#!/usr/bin/env python3
"""Stage two independent next-pilot inputs locally. Never upload or run inference."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent
PRODUCTION = RUNNER.parents[2]
REPOSITORY = PRODUCTION.parents[1]
BASE_RUNNER_SHA256 = 'ec81f6af22c267a013dbd39728ecff945e60a124bf7972e91808a133b64f860a'
NAMES = ('hospital-embrace', 'summer-exchange')


def digest(path):
    with Path(path).open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def load_runner(path):
    spec = importlib.util.spec_from_file_location('staged_ltx', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def specialized_runner():
    """Fail on upstream changes; change only the explicitly bounded pilot policy."""
    path = RUNNER / 'ltx_kaggle.py'
    if digest(path) != BASE_RUNNER_SHA256:
        raise ValueError('Runner changed: review the next-pilot specialization before staging')
    source = path.read_text()
    insertion = '''def validate_manifest(manifest, root):
    # Separate next-pilot staging only: full action durations, one take per run.
    shots = manifest.get('shots')
    if manifest.get('mode') != 'pilot' or not isinstance(shots, list) or len(shots) != 1:
        raise ValueError('Next pilot requires exactly one shot in pilot mode')
    shot = shots[0]
    expected_frames = {'S028_hospital_embrace_pilot': 241, 'S025_summer_exchange_pilot': 185}
    if (shot.get('shot_id') not in expected_frames
            or shot.get('frames') != expected_frames[shot['shot_id']]
            or (shot.get('width'), shot.get('height'), shot.get('fps')) != (864, 480, 30)
            or not isinstance(shot.get('seeds'), list) or len(shot['seeds']) != 1):
        raise ValueError('Next pilot requires its exact frame count, 864x480/30fps and one seed')
    if (shot['shot_id'] == 'S028_hospital_embrace_pilot') != ('end_image' in shot):
        raise ValueError('Hospital needs its endpoint; summer uses first frame only')
'''
    source = source.replace('def validate_manifest(manifest, root):\n', insertion, 1)
    source = source.replace("shot['frames'] > 153", "shot['frames'] > 241", 1)
    source = source.replace('Pilot capped at 153 frames and 864x480 pixels',
                            'Next pilot capped at 241 frames and 864x480 pixels', 1)
    return source


def stage(destination, tokenizer_path):
    if destination.exists():
        raise ValueError('Use a new staging directory; existing evidence is preserved')
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    os.environ['USE_TF'] = '0'
    os.environ['USE_FLAX'] = '0'
    from PIL import Image, ImageOps
    from transformers import T5Tokenizer
    lock = json.loads((RUNNER / 'model-lock.json').read_text())
    tokenizer_files = {}
    for item in lock['files']:
        if item['path'].startswith('tokenizer/'):
            path = tokenizer_path / Path(item['path']).name
            if not path.is_file() or digest(path) != item['sha256']:
                raise ValueError('Cached tokenizer differs from the pinned model: ' + path.name)
            tokenizer_files[path.name] = {'sha256': digest(path), 'bytes': path.stat().st_size}
    tokenizer = T5Tokenizer.from_pretrained(tokenizer_path, local_files_only=True)
    source = specialized_runner()
    destination.mkdir(parents=True)
    result = {'schema': 'jml-next-pilot-preparation/v1', 'state': 'prepared_not_submitted',
              'model_revision': lock['revision'], 'base_runner_sha256': BASE_RUNNER_SHA256,
              'tokenizer_files': tokenizer_files, 'prompts_truncated': False,
              'provider_calls': 0, 'remote_jobs': 0, 'model_downloads': 0, 'pilots': {}}
    for name in NAMES:
        manifest = json.loads((HERE / (name + '.json')).read_text())
        shot = manifest['shots'][0]
        token_ids = tokenizer(shot['prompt']).input_ids
        if len(token_ids) > 128:
            raise ValueError(name + ': prompt exceeds 128 tokens')
        target = destination / name
        target.mkdir()
        for filename in ('bootstrap.py', 'requirements.txt', 'model-lock.json', 'NOTICE.md', 'LICENSE.creator.txt'):
            shutil.copy2(RUNNER / filename, target / filename)
        (target / 'ltx_kaggle.py').write_text(source)
        images = {}
        for field in ('image', 'end_image'):
            if field not in shot:
                continue
            original = PRODUCTION / 'current/assets' / shot[field]
            if digest(original) != shot[field + '_sha256']:
                raise ValueError(name + ': native source changed')
            shutil.copy2(original, target / shot[field])
            with Image.open(original) as image:
                if image.size != (1916, 1080):
                    raise ValueError(name + ': native dimensions changed')
                fitted = ImageOps.contain(ImageOps.exif_transpose(image).convert('RGB'),
                                         (864, 480), Image.Resampling.LANCZOS)
                fitted_size = list(fitted.size)
                offset = [(864 - fitted.width) // 2, (480 - fitted.height) // 2]
            images[field] = {'source_relative_to_repository': str(original.relative_to(REPOSITORY)),
                             'sha256': digest(original), 'bytes': original.stat().st_size,
                             'native_dimensions': [1916, 1080], 'fitted_dimensions': fitted_size,
                             'canvas_dimensions': [864, 480], 'offset_xy': offset,
                             'fit': 'contain; no crop or stretch; original bytes copied unchanged'}
        (target / 'pilot.json').write_text(json.dumps(manifest, indent=2) + '\n')
        runner = load_runner(target / 'ltx_kaggle.py')
        runner.validate_manifest(manifest, target)
        runner.require_batch_review(manifest, None)
        result['pilots'][name] = {
            'staging_directory': str(target.relative_to(REPOSITORY)) if target.is_relative_to(REPOSITORY) else str(target),
            'manifest_sha256': digest(target / 'pilot.json'), 'runner_sha256': digest(target / 'ltx_kaggle.py'),
            'token_count_including_eos': len(token_ids), 'token_ids': token_ids,
            'frames': shot['frames'], 'fps': shot['fps'], 'dimensions': [shot['width'], shot['height']],
            'encoded_duration_seconds': shot['frames'] / shot['fps'],
            'first_to_last_frame_span_seconds': (shot['frames'] - 1) / shot['fps'],
            'takes': len(shot['seeds']), 'sources': images,
            'files': {path.name: {'sha256': digest(path), 'bytes': path.stat().st_size}
                      for path in sorted(target.iterdir()) if path.is_file()},
            'manifest_validation': 'passed with separate bounded runner',
        }
    (destination / 'preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--tokenizer', required=True, type=Path, help='Existing cached tokenizer; no download')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = stage(args.output.resolve(), args.tokenizer.resolve())
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({name: {'frames': item['frames'], 'tokens': item['token_count_including_eos'],
                            'takes': item['takes'], 'directory': item['staging_directory']}
                      for name, item in result['pilots'].items()}, indent=2))


if __name__ == '__main__':
    main()
