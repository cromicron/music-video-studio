#!/usr/bin/env python3
"""Retained delivery recipe, gated by exact-master acceptance for a full film."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

FULL_FILM = Path(__file__).resolve().parents[2]
RETAINED = FULL_FILM / 'unfinished-morning/tools/editor/verify_viewing_copy.py'
spec = importlib.util.spec_from_file_location('retained_viewing_checks', RETAINED)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
FINAL_TITLE = 'Join Me in Life — Movie and Band'


def ref(path):
    return {'file': str(path), 'bytes': path.stat().st_size,
            'sha256': hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--master', type=Path, required=True)
    p.add_argument('--acceptance', type=Path, help='Required exact-root acceptance for a full film')
    p.add_argument('--excerpt-proof', action='store_true', help='Actual existing short proof only; not full acceptance')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--record', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists() and not a.record.exists(), 'Preserve prior outputs/records'
    source = ref(a.master)
    info = checks.probe(a.master, ['-show_streams', '-show_format'])
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    frames = int(video['nb_frames'])
    title = info['format'].get('tags', {}).get('title')
    if a.excerpt_proof:
        assert 0 < frames < 6667, 'Excerpt mode cannot stand in for a complete movie'
        acceptance = None
    else:
        assert frames == 6667 and title == FINAL_TITLE
        assert a.acceptance is not None, 'Full delivery encode waits for exact-master root acceptance'
        gate = json.loads(a.acceptance.read_text())
        assert gate.get('status') in ('accepted_for_delivery', 'accepted_for_private_delivery')
        assert gate['master']['sha256'] == source['sha256'] and gate['master']['bytes'] == source['bytes']
        acceptance = ref(a.acceptance)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(a.master),
               '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'medium',
               '-crf', '22', '-maxrate', '2300k', '-bufsize', '4600k', '-pix_fmt', 'yuv420p',
               '-threads', '3', '-c:a', 'copy', '-movflags', '+faststart',
               '-metadata', 'title=' + title, str(a.output)]
    started = time.monotonic()
    subprocess.run(command, check=True)
    assert a.output.stat().st_size < 100 * 1024 ** 2, 'Viewing derivative exceeds connector cap'
    result = {'schema': 'jml-performance-viewing-encode/v1',
              'scope': 'technical_excerpt_proof' if a.excerpt_proof else 'accepted_full_film_delivery',
              'full_film_accepted': not a.excerpt_proof, 'reference_master': source,
              'root_acceptance': acceptance, 'viewing_copy': ref(a.output),
              'expected_frames': frames, 'intended_title': title,
              'encode_seconds': time.monotonic() - started, 'command': command,
              'retained_recipe_source': ref(RETAINED),
              'limits': 'Lossy picture derivative; audio packets copied. Technical/native/browser validation remains separate.'}
    a.record.parent.mkdir(parents=True, exist_ok=True)
    a.record.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'scope': result['scope'], 'viewing': result['viewing_copy']}))


if __name__ == '__main__':
    main()
