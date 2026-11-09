#!/usr/bin/env python3
"""B06-only lossless crop provenance; every check decodes/recompares all frames."""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess

FULL_FILM = Path(__file__).resolve().parents[2]
REPOSITORY = FULL_FILM.parents[2]
DERIVED = FULL_FILM / 'performance-cut/assets/motion/derived'
PARENT = 'performance-cut/assets/motion/instruments-a-v2/B06/video-silent.mp4'
PARENT_SHA = '2a744d6dada8e79b07a4a92f884edf90606d52c7a6b3901c95deb56dd1357c1e'
RENDER = 'performance-cut/assets/motion/instruments-a-v2/B06/render.json'
PROVIDER = 'performance-cut/story/shot-plan-v1.json'
PROVIDER_SHA = '420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e'
CROP = {'x': 0, 'y': 44, 'width': 824, 'height': 468}
KIND = 'lossless_crop_ffv1_yuv420p'
SCHEMA = 'jml-performance-B06-lossless-crop/v1'


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def local(value):
    require(isinstance(value, str) and value and not Path(value).is_absolute(),
            'Crop references must be relative')
    path = (FULL_FILM / value).resolve()
    require(path.is_relative_to(REPOSITORY) and path.is_file(), 'Missing/outside crop reference')
    return path


def run(command):
    return subprocess.run([str(x) for x in command], check=True, capture_output=True, text=True).stdout


def timing(path, cropped=False):
    data = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_frames',
                          '-show_entries', 'stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,time_base:frame=best_effort_timestamp_time',
                          '-of', 'json', path]))
    streams = data['streams']
    require(len(streams) == 1 and streams[0]['codec_type'] == 'video', 'Crop must be silent video only')
    s = streams[0]
    require(s['pix_fmt'] == 'yuv420p' and Fraction(s['avg_frame_rate']) == 24,
            'Crop pixel format/rate changed')
    size = (CROP['width'], CROP['height']) if cropped else (896, 512)
    require((s['width'], s['height']) == size, 'Crop decoded dimensions changed')
    require(s['codec_name'] == ('ffv1' if cropped else 'h264'), 'Crop codec changed')
    pts = [Fraction(f['best_effort_timestamp_time']) for f in data['frames']]
    tolerance = max(Fraction(1, 100000), min(Fraction(1, 96), Fraction(s['time_base']) * Fraction(101, 100)))
    require(len(pts) == 225 and pts[0] == 0, 'Crop raw count/origin changed')
    require(all(a < b for a, b in zip(pts, pts[1:])) and
            all(abs(t - Fraction(i, 24)) <= tolerance for i, t in enumerate(pts)),
            'Crop natural frame timing changed')
    return {'frames': len(pts), 'fps': 24, 'codec': s['codec_name'], 'pixel_format': s['pix_fmt'],
            'width': s['width'], 'height': s['height'], 'time_base': s['time_base'],
            'pts_seconds': [str(t) for t in pts]}


def crop_filter():
    return 'crop={width}:{height}:{x}:{y}:exact=1'.format(**CROP)


def frame_hashes(path, crop=False):
    command = ['ffmpeg', '-v', 'error', '-threads', '2', '-filter_threads', '1', '-i', path, '-map', '0:v:0']
    if crop:
        command += ['-vf', crop_filter()]
    command += ['-an', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough', '-threads', '2', '-f', 'framehash', '-hash', 'sha256', '-']
    lines = run(command).splitlines()
    hashes = [line.split(',')[-1].strip() for line in lines if line and not line.startswith('#')]
    require(len(hashes) == 225 and all(re.fullmatch('[0-9a-f]{64}', h) for h in hashes),
            'Crop decoded YUV frame count/hash format changed')
    return hashes


def load_contract(generation_id, source, provider_digest):
    require(generation_id == 'B06' and provider_digest == PROVIDER_SHA,
            'Lossless crop exception is only the frozen B06 take')
    d = source.get('derivation', {})
    require(d.get('kind') == KIND, 'Unknown crop derivation kind')
    record_path = local(d.get('record', ''))
    require(sha(record_path) == d.get('record_sha256'), 'Crop derivation record SHA changed')
    record = json.loads(record_path.read_text())
    require(record.get('schema') == SCHEMA and record.get('take_id') == 'B06', 'Wrong crop contract')
    require(record.get('crop') == CROP and all(type(v) is int for v in record['crop'].values()),
            'Crop rectangle differs from reviewed geometry')
    require(record.get('provider_plan') == {'path': PROVIDER, 'sha256': PROVIDER_SHA}
            and sha(local(PROVIDER)) == PROVIDER_SHA, 'Crop provider plan changed')
    parent = record.get('parent', {})
    require(parent.get('path') == PARENT and parent.get('sha256') == PARENT_SHA,
            'Crop parent path/SHA differs from exact B06 raw')
    require(sha(local(PARENT)) == PARENT_SHA, 'Crop parent raw bytes changed')
    origin = source.get('generation', {})
    raw_render = record.get('actual_parent_render', {})
    require(raw_render.get('path') == RENDER == origin.get('render_record') and
            raw_render.get('sha256') == origin.get('render_record_sha256') == sha(local(RENDER)),
            'Crop actual parent render metadata changed')
    derived = record.get('derived', {})
    require(derived.get('path') == source.get('path') and derived.get('sha256') == source.get('sha256'),
            'Crop derived source path/SHA differs from record')
    target = local(derived['path'])
    require(target.parent == DERIVED.resolve() and re.fullmatch(r'B06-crop-v[0-9]+\.mkv', target.name),
            'Crop source must be an owned versioned B06 derivative')
    require(sha(target) == derived['sha256'] and target.stat().st_size == derived.get('bytes'),
            'Crop derived bytes changed')
    parent_source = dict(source, path=PARENT, sha256=PARENT_SHA)
    parent_source.pop('derivation', None)
    return record, parent_source


def verify_equivalence(source, record):
    """Never trust a stored comparison alone: recompute both complete YUV streams."""
    parent, derived = local(PARENT), local(source['path'])
    parent_timing, derived_timing = timing(parent), timing(derived, True)
    require(record.get('timing') == {'parent': parent_timing, 'derived': derived_timing},
            'Crop recorded/actual frame timing differs')
    expected, actual = frame_hashes(parent, True), frame_hashes(derived)
    require(expected == actual, 'Parent exact-crop and derivative YUV pictures differ/order changed')
    eq = record.get('equivalence', {})
    require(eq.get('frames') == 225 and eq.get('pixel_format') == 'yuv420p'
            and eq.get('parent_crop_frame_hashes') == expected and eq.get('derived_frame_hashes') == actual
            and eq.get('all_equal') is True, 'Crop recorded/recomputed pixel equivalence differs')
    return {'frames_recomputed': 225, 'ordered_yuv_pictures_equal': True,
            'natural_24fps': True, 'crop': CROP.copy()}


def create(output, record_path):
    output, record_path = output.resolve(), record_path.resolve()
    require(output.parent == DERIVED.resolve() and re.fullmatch(r'B06-crop-v[0-9]+\.mkv', output.name),
            'Choose an owned versioned B06 derivative path')
    require(record_path == output.with_suffix('.derivation.json'), 'Use matching immutable derivation record')
    require(not output.exists() and not record_path.exists(), 'Preserve existing crop versions/records')
    parent, raw_render, provider = local(PARENT), local(RENDER), local(PROVIDER)
    require(sha(parent) == PARENT_SHA and sha(provider) == PROVIDER_SHA, 'Exact raw/plan changed')
    r = json.loads(raw_render.read_text())
    require(r['video']['sha256'] == PARENT_SHA and r['manifest']['take_id'] == 'B06',
            'Actual B06 render does not name the exact raw source')
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-threads', '2', '-i', str(parent),
               '-map', '0:v:0', '-vf', crop_filter(), '-an', '-map_metadata', '-1', '-c:v', 'ffv1',
               '-level', '3', '-coder', '1', '-context', '1', '-g', '1', '-slicecrc', '1',
               '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough', '-enc_time_base', '1/24',
               '-threads', '2', str(output)]
    run(command)
    pt, dt = timing(parent), timing(output, True)
    expected, actual = frame_hashes(parent, True), frame_hashes(output)
    require(expected == actual, 'Actual lossless crop failed all225 decoded YUV equivalence')
    record = {'schema': SCHEMA, 'take_id': 'B06',
              'status': 'TECHNICAL_CROP_EQUIVALENCE_PASS_NOT_MOTION_ACCEPTANCE',
              'parent': {'path': PARENT, 'sha256': PARENT_SHA},
              'actual_parent_render': {'path': RENDER, 'sha256': sha(raw_render)},
              'provider_plan': {'path': PROVIDER, 'sha256': PROVIDER_SHA}, 'crop': CROP.copy(),
              'derived': {'path': str(output.relative_to(FULL_FILM)), 'sha256': sha(output), 'bytes': output.stat().st_size},
              'timing': {'parent': pt, 'derived': dt},
              'equivalence': {'frames': 225, 'pixel_format': 'yuv420p', 'parent_crop_frame_hashes': expected,
                              'derived_frame_hashes': actual, 'all_equal': True},
              'command': command, 'tool': {'path': str(Path(__file__).relative_to(FULL_FILM)), 'sha256': sha(Path(__file__))},
              'limits': 'Exact lossless framing derivation only. Crown/tuner edges can exit intentional tighter framing. Independent actual crop/keeper/both song-placement review and root adoption remain mandatory.'}
    record_path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'file': str(output), 'sha256': sha(output), 'bytes': output.stat().st_size,
                      'record': str(record_path), 'record_sha256': sha(record_path), 'frames': 225}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--record', type=Path, required=True)
    args = p.parse_args()
    create(args.output, args.record)
