#!/usr/bin/env python3
"""Adapt retained C derivative checks to a full accepted movie or real short proof."""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import re
import struct

FULL_FILM = Path(__file__).resolve().parents[2]
RETAINED = FULL_FILM / 'unfinished-morning/tools/editor/verify_viewing_copy.py'
spec = importlib.util.spec_from_file_location('retained_viewing_verifier', RETAINED)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
run, probe = old.run, old.probe


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--encode-record', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists(), 'Preserve previous verification records'
    rec = json.loads(a.encode_record.read_text())
    master = Path(rec['reference_master']['file'])
    viewing = Path(rec['viewing_copy']['file'])
    frames = rec['expected_frames']
    full = rec['scope'] == 'accepted_full_film_delivery'
    assert (frames == 6667 and rec['full_film_accepted']) if full else (0 < frames < 6667 and not rec['full_film_accepted'])
    for key in ('reference_master', 'viewing_copy'):
        data = rec[key]
        path = Path(data['file'])
        assert path.stat().st_size == data['bytes'] and sha(path) == data['sha256']
    assert viewing.stat().st_size < 100 * 1024 ** 2
    info = probe(viewing, ['-show_streams', '-show_format'])
    streams = info['streams']
    assert len(streams) == 2 and all(Fraction(s['start_time']) == 0 for s in streams)
    v = next(s for s in streams if s['codec_type'] == 'video')
    assert (v['width'], v['height'], v['codec_name'], v['pix_fmt'], v['avg_frame_rate']) == (1920, 1080, 'h264', 'yuv420p', '24/1')
    assert info['format'].get('tags', {}).get('title') == rec['intended_title']
    points = probe(viewing, ['-select_streams', 'v:0', '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time'])['frames']
    pts = [Fraction(f['best_effort_timestamp_time']) for f in points]
    assert len(pts) == frames and all(abs(t - Fraction(i, 24)) <= Fraction(1, 100000) for i, t in enumerate(pts))
    packet_args = ['-select_streams', 'a:0', '-show_packets', '-show_entries',
                   'packet=pts,dts,duration,size,data_hash', '-show_data_hash', 'sha256']
    audio_a, audio_b = probe(master, packet_args)['packets'], probe(viewing, packet_args)['packets']
    assert audio_a == audio_b
    run(['ffmpeg', '-v', 'error', '-xerror', '-threads', '2', '-i', str(viewing), '-f', 'null', '-'])
    command = ['ffmpeg', '-hide_banner', '-threads', '2', '-i', str(master), '-threads', '2',
               '-i', str(viewing), '-filter_complex_threads', '1', '-lavfi', '[0:v][1:v]ssim', '-an', '-f', 'null', '-']
    ssim = [s for s in run(command).stderr.splitlines() if 'SSIM Y:' in s][-1]
    atoms = []
    with viewing.open('rb') as f:
        while f.tell() < viewing.stat().st_size:
            offset = f.tell()
            size, typ = struct.unpack('>I4s', f.read(8))
            if size == 1:
                size = struct.unpack('>Q', f.read(8))[0]
            if size == 0:
                size = viewing.stat().st_size - offset
            assert size >= 8 and offset + size <= viewing.stat().st_size
            atoms.append({'type': typ.decode(), 'offset': offset, 'bytes': size})
            f.seek(offset + size)
    assert next(x['offset'] for x in atoms if x['type'] == 'moov') < next(x['offset'] for x in atoms if x['type'] == 'mdat')
    out = {'schema': 'jml-performance-viewing-technical/v1',
           'state': 'TECHNICAL_FULL_DERIVATIVE_PASS' if full else 'TECHNICAL_EXCERPT_DERIVATIVE_PASS_NOT_FULL_FILM',
           'full_film': full, 'master': rec['reference_master'], 'viewing_copy': rec['viewing_copy'],
           'frames': frames, 'fps': 24, 'cadence_and_zero_origins': True,
           'audio_packets_and_timestamps_identical': True, 'audio_packet_count': len(audio_a),
           'audio_packet_list_sha256': hashlib.sha256(json.dumps(audio_a, sort_keys=True).encode()).hexdigest(),
           'full_decode': True, 'faststart_verified': True, 'mp4_atoms': atoms,
           'ssim': ssim, 'ssim_all': float(re.search(r'All:([0-9.]+)', ssim).group(1)),
           'ssim_command': command, 'below100MiB': True, 'intended_title': rec['intended_title'],
           'encode_record': {'file': str(a.encode_record), 'sha256': sha(a.encode_record)},
           'retained_verifier': {'file': str(RETAINED), 'sha256': sha(RETAINED)},
           'limits': 'Numerical/source checks do not clear compression detail, hosted playback, subjective hearing or musical synchronization; native and actual-browser review remain separate.'}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'state': out['state'], 'frames': frames, 'audio_packets': len(audio_a), 'ssim_all': out['ssim_all']}))


if __name__ == '__main__':
    main()
