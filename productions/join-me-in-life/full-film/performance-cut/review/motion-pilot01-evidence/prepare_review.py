#!/usr/bin/env python3
"""Produce source-bound pilot inspection aids, not a creative acceptance verdict."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
SETTINGS = {
    'O01': {'raw': 209, 'first': 6, 'last': 198, 'master': [0, 192],
            'regions': {'record-contact': [440, 220, 320, 275]}},
    'B03': {'raw': 137, 'first': 6, 'last': 126, 'master': [1596, 1716],
            'regions': {'keys-contact': [5, 175, 180, 100],
                        'guitar-contact': [160, 180, 190, 155],
                        'singer-arm': [330, 105, 225, 235],
                        'drum-contact': [515, 90, 180, 220],
                        'bass-contact': [685, 160, 205, 185]}},
}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def cmd(args):
    return subprocess.check_output(args, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--take', choices=SETTINGS, required=True)
    ap.add_argument('--video', type=Path, required=True)
    ap.add_argument('--sha256', required=True)
    a = ap.parse_args()
    src = a.video.resolve()
    assert digest(src) == a.sha256, 'Actual source hash differs from supplied verification'
    cfg = SETTINGS[a.take]
    out = HERE / a.take
    out.mkdir(exist_ok=False)
    probe = json.loads(cmd(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(src)]))
    assert len(probe['streams']) == 1
    stream = probe['streams'][0]
    assert (stream['codec_type'], stream['width'], stream['height'], stream['avg_frame_rate']) == ('video', 896, 512, '24/1')
    times = json.loads(cmd(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_frames',
                           '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(src)]))['frames']
    assert len(times) == cfg['raw']
    assert all(abs(float(frame['best_effort_timestamp_time']) - n / 24) < 0.00001 for n, frame in enumerate(times))
    process = subprocess.Popen(['ffmpeg', '-v', 'error', '-xerror', '-i', str(src), '-map', '0:v:0',
                                '-pix_fmt', 'rgb24', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    previous = None
    changes, hashes = [], []
    while data := process.stdout.read(896 * 512 * 3):
        assert len(data) == 896 * 512 * 3
        image = np.frombuffer(data, np.uint8).reshape(512, 896, 3)
        hashes.append(hashlib.sha256(data).hexdigest())
        if previous is not None:
            delta = np.abs(image.astype(np.int16) - previous.astype(np.int16))
            changes.append({'raw_frame': len(hashes) - 1, 'whole_mean_abs_difference': float(delta.mean()),
                            'regions': {name: float(delta[y:y+h, x:x+w].mean())
                                        for name, (x, y, w, h) in cfg['regions'].items()}})
        previous = image.copy()
    assert process.wait() == 0 and len(hashes) == cfg['raw']
    font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    label = f"drawtext=fontfile={font}:text='%{{eif\\:n+{cfg['first']}\\:d}}':x=3:y=2:fontsize=13:fontcolor=white:box=1:boxcolor=black@0.8"
    for name, (x, y, w, h) in cfg['regions'].items():
        filters = (f"trim=start_frame={cfg['first']}:end_frame={cfg['last']},crop={w}:{h}:{x}:{y}," + label +
                   ',tile=4x6:nb_frames=24:padding=4:margin=4')
        subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(src), '-vf', filters,
                        '-fps_mode', 'passthrough', str(out / (name + '-%02d.png'))], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(src), '-vf',
                    f"trim=start_frame={cfg['first']}:end_frame={cfg['last']}," + label +
                    ',scale=448:256,tile=4x6:nb_frames=24:padding=4:margin=4',
                    '-fps_mode', 'passthrough', str(out / 'full-temporal-%02d.png')], check=True)
    count = cfg['last'] - cfg['first']
    start, duration = cfg['master'][0] / 24, count / 24
    review = out / (a.take + '-keeper-original-song.mp4')
    song = ROOT / 'productions/join-me-in-life/full-song/track-49.mp3'
    encode = ['ffmpeg', '-v', 'error', '-n', '-i', str(src), '-i', str(song), '-filter_complex',
              f"[0:v]trim=start_frame={cfg['first']}:end_frame={cfg['last']},setpts=PTS-STARTPTS[v];"
              f'[1:a]atrim=start={start:.9f}:duration={duration:.9f},asetpts=PTS-STARTPTS[a]',
              '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '16',
              '-pix_fmt', 'yuv420p', '-threads', '2', '-c:a', 'aac', '-b:a', '256k',
              '-movflags', '+faststart', '-t', f'{duration:.9f}', str(review)]
    subprocess.run(encode, check=True)
    derivative = json.loads(cmd(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(review)]))
    assert all(float(s['start_time']) == 0 for s in derivative['streams'])
    assert int(derivative['streams'][0]['nb_frames']) == count
    keeper_hashes = hashes[cfg['first']:cfg['last']]
    longest = run = 1
    for previous_hash, present_hash in zip(keeper_hashes, keeper_hashes[1:]):
        run = run + 1 if previous_hash == present_hash else 1
        longest = max(longest, run)
    in_range = [entry for entry in changes if cfg['first'] < entry['raw_frame'] < cfg['last']]
    outliers = {name: sorted(in_range, key=lambda entry: entry['regions'][name], reverse=True)[:10]
                for name in cfg['regions']}
    record = {'scope': 'Technical and temporal inspection aids only; no motion acceptance', 'take': a.take,
              'source': str(src.relative_to(ROOT)), 'sha256': a.sha256, 'raw_frames': cfg['raw'],
              'keeper': [cfg['first'], cfg['last']], 'master': cfg['master'], 'natural_cadence_24fps': True,
              'unique_decoded_rgb_frames': len(set(hashes)), 'frame_hashes': hashes,
              'unique_keeper_decoded_rgb_frames': len(set(keeper_hashes)),
              'longest_identical_keeper_frame_run': longest, 'region_change_outliers': outliers,
              'adjacent_region_change_metrics': changes, 'contact_regions': cfg['regions'],
              'review_file': str(review.relative_to(ROOT)), 'review_sha256': digest(review),
              'original_song_sha256': digest(song), 'audio_excerpt_seconds': [start, start+duration],
              'review_probe': derivative, 'review_command': encode,
              'limits': 'Pixel differences, unique frames and valid playback are not proof of coherent action or musical accuracy.'}
    (out / 'inspection-aids.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'take': a.take, 'raw_frames': len(hashes), 'review_file': str(review), 'review_sha256': record['review_sha256']}))


if __name__ == '__main__':
    main()
