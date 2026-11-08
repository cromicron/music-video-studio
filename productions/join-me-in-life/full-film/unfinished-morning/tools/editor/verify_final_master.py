#!/usr/bin/env python3
"""Verify complete C assembly against pinned reviewed partitions without raw dumps."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('diagnostic_checks', Path(__file__).with_name('make_unbound_diagnostic.py'))
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def frame_hashes(path):
    command = ['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0',
               '-fps_mode', 'passthrough', '-f', 'framehash', '-hash', 'sha256', '-']
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
    return [line.rsplit(',', 1)[-1].strip() for line in result.stdout.splitlines()
            if line and not line.startswith('#')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, required=True)
    parser.add_argument('--edit', type=Path, required=True)
    parser.add_argument('--partitions', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Preserve prior verification records'
    edit = json.loads(args.edit.read_text())
    manifest = json.loads(args.master.with_suffix('.manifest.json').read_text())
    reference_plan = json.loads(args.partitions.read_text())
    assert edit['total_frames'] == 6667 and edit['fps'] == 24
    assert len(edit['shots']) == 39 and all('source' in shot for shot in edit['shots'])
    assert manifest['plan_sha256'] == sha(args.edit)
    assert manifest['frames'] == 6667 and manifest['full_song'] is True
    assert manifest['source_padding_frames'] == manifest['reused_source_interval_frames'] == 0
    assert manifest['output_sha256'] == sha(args.master)
    metadata = checks.ed.legacy.probe(args.master)
    video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in metadata['streams'] if s['codec_type'] == 'audio')
    assert video['width'] == 1920 and video['height'] == 1080
    assert video['codec_name'] == 'h264' and video['pix_fmt'] == 'yuv420p'
    assert float(video['start_time']) == float(audio['start_time']) == 0
    assert metadata['format'].get('tags', {}).get('title') == edit['title']
    timing = checks.ed.source_timing(args.master)
    assert timing['frames'] == 6667
    print('Decoded cadence and zero stream origins verified; hashing all master pictures.', flush=True)
    actual = frame_hashes(args.master)
    assert len(actual) == 6667
    position = 0
    results = []
    for part in reference_plan['partitions']:
        lo, hi = part['master_range']
        start, end = part['reference_range']
        assert lo == position and hi - lo == end - start and hi <= 6667
        source = Path(part['reference_file'])
        review = Path(part['independent_review']['file'])
        assert sha(source) == part['reference_sha256']
        assert sha(review) == part['independent_review']['sha256']
        reference = frame_hashes(source)
        assert 0 <= start < end <= len(reference)
        expected = reference[start:end]
        mismatches = [lo + i for i, (a, b) in enumerate(zip(actual[lo:hi], expected)) if a != b]
        assert not mismatches, f'Picture mismatches in {source}: {mismatches[:20]}'
        results.append({**part, 'decoded_reference_frames': len(reference), 'all_picture_hashes_identical': True})
        position = hi
        print(f'Partition [{lo},{hi}) matches {source.name}.', flush=True)
    assert position == 6667
    song = BASE.parent.parent / 'full-song/track-49.mp3'
    assert sha(song) == checks.ed.SONG_SHA256
    waveform = checks.exact_trim_waveform(song, args.master, 0, 6667 * 2000)
    assert waveform['correlation'] >= .995 and abs(waveform['offset_seconds']) <= .03
    record = {
        'schema': 'jml-c-final-master-technical-verification/v1',
        'state': 'TECHNICAL_PASS_ONLY_FULL_FILM_CREATIVE_REVIEW_SEPARATE',
        'master': {'file': str(args.master), 'sha256': sha(args.master), 'bytes': args.master.stat().st_size},
        'edit': {'file': str(args.edit), 'sha256': sha(args.edit)},
        'partition_plan': {'file': str(args.partitions), 'sha256': sha(args.partitions)},
        'frames': 6667, 'fps': 24, 'shots': 39, 'cadence': timing,
        'all6667_pictures_match_reviewed_partitions': True,
        'partitions': results, 'video_start_seconds': 0, 'audio_start_seconds': 0,
        'original_audio_sha256': checks.ed.SONG_SHA256, 'audio_waveform': waveform,
        'full_decode_pass': True, 'source_padding_frames': 0, 'reused_source_interval_frames': 0,
        'container_metadata': metadata['format'].get('tags', {}),
        'method': 'Explicit passthrough SHA256 frame hashes streamed to small text; no full raw RGB/YUV dump. Waveform compares the original full decode from sample zero through natural EOF.',
        'limitations': 'Decoded-pixel and audio-origin verification does not certify subjective hearing, exact phoneme synchronization, dramatic pacing, all joins or whole-film creative acceptance.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'master_sha256': record['master']['sha256'], 'frames': 6667, 'all_partitions_match': True, 'waveform': waveform}))


if __name__ == '__main__':
    main()
