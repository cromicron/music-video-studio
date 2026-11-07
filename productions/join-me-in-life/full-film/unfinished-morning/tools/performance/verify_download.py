#!/usr/bin/env python3
"""Verify actual downloaded A2V sources, complete video and original review audio."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import wave

from PIL import Image, ImageOps


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text())


def frames(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0',
                                   '-pix_fmt', 'rgb24', '-f', 'framehash', '-hash', 'sha256', '-'], text=True)
    return [line.rsplit(',', 1)[1].strip() for line in raw.splitlines() if line.strip() and not line.startswith('#')]


def verify_take(bundle, results, manifest_name):
    manifest_path = bundle / manifest_name
    manifest = read(manifest_path); sid = manifest['shot_id']; output = results / sid
    record_path = output / 'render.json'; record = read(record_path)
    require(record['status'] == 'complete' and record['technical_valid'] is True, sid + ': child not complete')
    require(record['manifest'] == manifest and record['manifest_sha256'] == sha(manifest_path), sid + ': returned input manifest changed')
    require(read(output / 'model-lock.json') == read(bundle / 'model-lock.json'), sid + ': model pins changed')
    devices = read(output / 'environment.json')['devices']
    require(len(devices) == 2 and all('T4' in d['name'] for d in devices), sid + ': wrong hardware')
    image_path = bundle / manifest['image']; audio_path = bundle / manifest['audio']
    require(sha(image_path) == manifest['image_sha256'] and sha(audio_path) == manifest['audio_sha256'], sid + ': source bytes changed')
    with Image.open(image_path) as original:
        contained = ImageOps.contain(original.convert('RGB'), (896, 512), Image.Resampling.LANCZOS)
    fitted = Image.new('RGB', (896, 512), (0, 0, 0))
    fitted.paste(contained, ((896 - contained.width) // 2, (512 - contained.height) // 2))
    with Image.open(output / 'input-fitted.png') as actual:
        require(actual.convert('RGB').tobytes() == fitted.tobytes() and actual.size == fitted.size,
                sid + ': actual fitted start guide differs')
    coverage = record['audio_coverage']; expected = {89: 93, 97: 101, 105: 109, 113: 118, 121: 126, 129: 134}[manifest['frames']]
    require(coverage['full_coverage'] is True and coverage['strength'] == 1.0
            and coverage['required_frames'] == expected and coverage['encoded_frames'] >= expected,
            sid + ': complete supplied-audio latent coverage not proven')
    require(record['returned_model_audio_discarded'] is True and record['text_phase']['complete'] is True,
            sid + ': audio/text residency completion flags missing')
    phase = record['text_phase']
    require(phase['use_cache'] is False and [event['phase'] for event in phase['events']] == [
        'before_gemma_video_components_on_cpu', 'gemma_released_contexts_transferred',
        'video_components_staged_after_gemma'], sid + ': sequential text/video residency evidence differs')
    peaks = record['gpu_peak_allocated_bytes']
    totals = [device['total'] for device in phase['events'][-1]['gpu_memory']]
    require(len(peaks) == len(totals) == 2 and all(0 < peak <= total for peak, total in zip(peaks, totals)),
            sid + ': invalid or missing actual GPU memory evidence')
    silent = output / 'video-silent.mp4'; review = output / 'review-original-audio.mkv'
    require(sha(silent) == record['video']['sha256'] and sha(review) == record['review']['sha256'], sid + ': returned video/review hash differs')
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,width,height,avg_frame_rate,nb_frames', '-of', 'json', str(silent)], text=True))
    stream = info['streams']
    require(len(stream) == 1 and (stream[0]['codec_type'], stream[0]['width'], stream[0]['height'], stream[0]['avg_frame_rate'])
            == ('video', 896, 512, '24/1'), sid + ': silent delivery format differs')
    video_hashes = frames(silent)
    require(len(video_hashes) == manifest['frames'], sid + ': full decoded frame count differs')
    require(video_hashes == frames(review), sid + ': review container picture differs from silent delivery')
    with wave.open(str(audio_path), 'rb') as audio:
        pcm = audio.readframes(audio.getnframes())
    review_pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-i', str(review), '-map', '0:a:0',
                                         '-f', 's16le', '-acodec', 'pcm_s16le', '-'])
    require(pcm == review_pcm and hashlib.sha256(pcm).hexdigest() == record['review']['original_pcm_sha256']
            and record['review']['model_audio_used'] is False, sid + ': review no longer contains exact original PCM')
    return {'shot_id': sid, 'technical_verification': 'pass', 'video_sha256': sha(silent),
        'render_sha256': sha(record_path), 'frames': len(video_hashes), 'fps': 24,
        'unique_decoded_rgb_frames': len(set(video_hashes)), 'full_decode_passed': True,
        'fitted_start_pixels_exact': True, 'full_actual_audio_coverage': coverage,
        'sequential_text_video_residency_verified': True, 'gpu_peak_allocated_bytes': peaks,
        'review_video_frames_equal': True, 'review_original_pcm_equal': True,
        'source_frames': manifest['editorial']['source_frames'], 'timeline_frames': manifest['editorial']['timeline_frames'],
        'generation_seconds': record['generation_seconds'], 'child_seconds': record['elapsed_seconds'],
        'movement_and_phoneme_acceptance': 'not established; independent song-paced review required'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--expected-lock', required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    require(not args.report.exists(), 'Preserve earlier verification records')
    require(sha(args.bundle / 'package-lock.json') == args.expected_lock, 'Package lock differs from exact remote deployment')
    lock = read(args.bundle / 'package-lock.json')
    for name, expected in lock['files'].items():
        require(sha(args.bundle / name) == expected, 'Staged input changed: ' + name)
    job = read(args.results / 'job.json'); queue = read(args.bundle / 'queue.json')
    require([s['shot_id'] for s in job['shots']] == [Path(name).stem for name in queue['manifests']],
            'Downloaded job does not contain the exact selected sequence')
    report = {'schema': 'jml-v2-a2v-downloaded-verification/v1', 'observed_utc': datetime.now(timezone.utc).isoformat(),
        'package_lock_sha256': args.expected_lock, 'job_record_sha256': sha(args.results / 'job.json'),
        'job_status': job['status'], 'whole_job_seconds': job.get('elapsed_seconds'), 'takes': [],
        'scope': 'Actual downloaded technical/media provenance only. No motion, lyric-climax, musical-cut or complete-film acceptance.'}
    for name in queue['manifests']:
        try:
            report['takes'].append(verify_take(args.bundle, args.results, name))
        except Exception as error:
            report['takes'].append({'manifest': name, 'technical_verification': 'failed',
                                    'error_type': type(error).__name__, 'error': str(error)})
    report['all_takes_technically_verified'] = all(t['technical_verification'] == 'pass' for t in report['takes'])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(args.report), 'all_takes_technically_verified': report['all_takes_technically_verified']}))
    raise SystemExit(0 if report['all_takes_technically_verified'] else 1)


if __name__ == '__main__':
    main()
