#!/usr/bin/env python3
"""Adapt retained C checks to actual ordered Movie and Band render chunks.

No placeholders or raw picture dumps. Excerpt mode verifies only the declared
real subset and is explicitly labelled partial; it never clears the full film.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

FULL_FILM = Path(__file__).resolve().parents[2]
REPO = FULL_FILM.parents[2]
FINAL_TITLE = 'Join Me in Life — Movie and Band'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


retained_path = FULL_FILM / 'unfinished-morning/tools/editor/verify_final_master.py'
retained = load('retained_c_master_checks', retained_path)
builder_path = Path(__file__).with_name('build_edit.py')
builder = load('performance_edit_builder', builder_path)
ed = builder.editor
require = ed.require


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def source_ref(path):
    return {'file': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}


def recorded_path(value):
    candidates = [REPO / value, FULL_FILM / value]
    found = [p.resolve() for p in candidates if p.is_file()]
    require(bool(found), f'Missing recorded input: {value}')
    require(found[0].is_relative_to(REPO), 'Recorded input leaves repository')
    return found[0]


def verify(args):
    require(not args.output.exists(), 'Preserve previous verification records')
    frame_index = args.output.with_suffix('.frame-references.json')
    require(not frame_index.exists(), 'Preserve previous frame-reference indexes')
    plan = json.loads(args.edit.read_text())
    ed.validate_story(plan)
    require(len(plan['shots']) == 46, 'Current adopted edit must contain46 shots')
    selected = plan['shots']
    if args.shots:
        first, last = args.shots.split(':')
        ids = [s['id'] for s in selected]
        lo, hi = ids.index(first), ids.index(last)
        require(lo <= hi, 'Reversed excerpt selection')
        selected = selected[lo:hi + 1]
    start = selected[0]['start_frame']
    frames = sum(s['end_frame_exclusive'] - s['start_frame'] for s in selected)
    full = len(selected) == 46 and start == 0 and frames == 6667
    expected_title = args.expected_title or (FINAL_TITLE if full else plan['title'])
    if full:
        require(all('source' in s for s in plan['shots']), 'Whole film has unbound footage')
    bound = ed.bind_sources(plan, selected)
    # Re-exercise new actual-render/provider provenance, not merely the old gates.
    adoption = plan['adoption']
    provider_file = recorded_path(adoption['generation_plan'])
    provider_digest = sha(provider_file)
    require(provider_digest == adoption['generation_plan_sha256'], 'Provider plan changed')
    provider = json.loads(provider_file.read_text())
    checked_new = set()
    for shot in bound:
        recipe = shot.get('planned_source')
        if recipe and recipe['generation_id'] not in checked_new:
            gid = recipe['generation_id']
            builder.verify_new_take_origin(gid, shot['source'], provider, provider_digest)
            root = shot['source'].get('root_adoption', {})
            root_file = ed.local_file(FULL_FILM, root.get('path', ''))
            require(sha(root_file) == root.get('sha256'), 'Root adoption record changed')
            require(shot['source']['sha256'] in root_file.read_text(),
                    'Root adoption does not name actual new source SHA')
            checked_new.add(gid)
    for value in plan.get('inputs', {}).values():
        require(sha(recorded_path(value['path'])) == value['sha256'], 'Built edit input changed')
    manifest_file = args.master.with_suffix('.manifest.json')
    manifest = json.loads(manifest_file.read_text())
    require(manifest['plan_sha256'] == sha(args.edit), 'Render used another edit')
    require(manifest['frames'] == frames and manifest['start_frame'] == start
            and manifest['full_song'] is full, 'Render extent/full-song flag differs')
    require(manifest['source_padding_frames'] == manifest['reused_source_interval_frames'] == 0,
            'Render declares holds or source reuse')
    require(manifest['output_sha256'] == sha(args.master), 'Master bytes changed')
    require(len(manifest['shots']) == len(bound), 'Render source ledger length differs')
    for actual, wanted in zip(manifest['shots'], bound):
        for key in ('id', 'start_frame', 'end_frame_exclusive'):
            require(actual[key] == wanted[key], 'Render source order/timing differs')
        for key in ('id', 'path', 'sha256', 'in_frame', 'out_frame_exclusive'):
            require(actual['source'][key] == wanted['source'][key], 'Render source selection differs')
        require(actual['source']['review'] == wanted['source']['review'], 'Render gate reference differs')
    metadata = ed.legacy.probe(args.master)
    video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in metadata['streams'] if s['codec_type'] == 'audio')
    require((video['width'], video['height'], video['codec_name'], video['pix_fmt'])
            == (1920, 1080, 'h264', 'yuv420p'), 'Unexpected delivery picture format')
    require(audio['codec_name'] == 'aac' and int(audio['sample_rate']) == 48000
            and int(audio['channels']) == 2, 'Unexpected original-song audio format')
    require(float(video['start_time']) == float(audio['start_time']) == 0, 'Nonzero stream origin')
    tags = metadata['format'].get('tags', {})
    require(tags.get('title') == expected_title == plan['title'], 'Incorrect intended title metadata')
    for key in ('title', 'comment', 'description', 'album', 'show', 'synopsis'):
        require(not re.search(r'\b(hybrid|candidate|unfinished morning|revision[ -]?[24])\b',
                              tags.get(key, ''), re.I), f'Stale production metadata: {key}')
    timing = ed.source_timing(args.master)
    require(timing['frames'] == frames, 'Master cadence/decoded count differs')
    actual_hashes = retained.frame_hashes(args.master)
    require(len(actual_hashes) == frames, 'Master frame-hash count differs')
    position, chunks = 0, []
    for shot in bound:
        chunk = args.parts_dir / (shot['id'] + '.mp4')
        require(chunk.is_file(), f'Missing actual rendered chunk: {shot["id"]}')
        expected = retained.frame_hashes(chunk)
        count = shot['end_frame_exclusive'] - shot['start_frame']
        require(len(expected) == count, 'Chunk has missing/extra pictures')
        require(actual_hashes[position:position + count] == expected,
                f'Master differs from actual ordered chunk: {shot["id"]}')
        chunks.append({'shot': shot['id'], 'master_range': [shot['start_frame'], shot['end_frame_exclusive']],
                       'output_local_range': [position, position + count],
                       'chunk': source_ref(chunk), 'source': {'path': shot['source']['path'],
                           'sha256': shot['source']['sha256'],
                           'keeper': [shot['source']['in_frame'], shot['source']['out_frame_exclusive']],
                           'review': shot['source']['review']},
                       'picture_hashes_sha256': hashlib.sha256('\n'.join(expected).encode()).hexdigest(),
                       'decoded_picture_hashes': expected, 'all_pictures_identical': True})
        position += count
        print(f'{shot["id"]}: all{count} pictures equal ordered render chunk', flush=True)
    require(position == frames, 'Chunk coverage leaves a gap')
    song = FULL_FILM.parent / 'full-song/track-49.mp3'
    require(sha(song) == ed.SONG_SHA256, 'Original take49 bytes changed')
    waveform = retained.checks.exact_trim_waveform(song, args.master,
                                                start * 2000, (start + frames) * 2000)
    require(waveform['correlation'] >= .995 and abs(waveform['offset_seconds']) <= 1 / 4000,
            'Original-song waveform does not align at zero within measurement resolution')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(args.master), '-f', 'null', '-'], check=True)
    indexes = {'schema': 'jml-performance-rendered-frame-references/v1', 'scope': 'full' if full else 'excerpt',
               'master': source_ref(args.master), 'edit': source_ref(args.edit), 'chunks': chunks}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame_index.write_text(json.dumps(indexes, indent=2) + '\n')
    joins = [{'left': a['id'], 'right': b['id'], 'master_frame': b['start_frame'],
              'seconds': b['start_frame'] / 24, 'state': 'requires_actual_join_review'}
             for a, b in zip(selected, selected[1:])]
    adjacent_equal = [start + i for i in range(1, len(actual_hashes))
                      if actual_hashes[i] == actual_hashes[i - 1]]
    result = {'schema': 'jml-performance-master-technical-verification/v1',
              'state': 'TECHNICAL_FULL_PASS_CREATIVE_REVIEW_SEPARATE' if full else 'TECHNICAL_EXCERPT_PASS_NOT_FULL_FILM',
              'full_film': full, 'master': source_ref(args.master), 'edit': source_ref(args.edit),
              'render_manifest': source_ref(manifest_file), 'provider_plan': source_ref(provider_file),
              'frames': frames, 'fps': 24, 'shots': len(selected), 'master_start_frame': start,
              'cadence': timing, 'video_origin_seconds': 0, 'audio_origin_seconds': 0,
              'all_ordered_chunk_pictures_identical': True, 'frame_reference_index': source_ref(frame_index),
              'source_padding_frames': 0, 'reused_source_interval_frames': 0,
              'decoded_adjacent_equal_picture_frames': adjacent_equal,
              'decoded_picture_hash_frequency_max': max(Counter(actual_hashes).values()),
              'audio': {'original_sha256': ed.SONG_SHA256, 'waveform': waveform}, 'full_decode': True,
              'container_metadata': tags, 'joins_required': joins,
              'full_film_join_count_target': 45, 'new_generation_origins_checked': sorted(checked_new),
              'retained_tools': [source_ref(retained_path), source_ref(builder_path),
                                 source_ref(FULL_FILM / 'revision-2/tools/editor/strict_edit.py')],
              'limits': 'Exact rendered-chunk equivalence and source uniqueness prove no assembly insertion/reuse/retiming. Equal decoded pictures are reported, not interpreted as acting quality. New motion, all45 joins, story pacing, subjective hearing and exact musical/phoneme synchronization require separate actual reviews.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'state': result['state'], 'frames': frames, 'shots': len(selected),
                      'waveform': waveform, 'output': str(args.output)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, required=True)
    parser.add_argument('--edit', type=Path, required=True)
    parser.add_argument('--parts-dir', type=Path, required=True)
    parser.add_argument('--shots', help='Contiguous actual excerpt FIRST:LAST; never pads missing footage')
    parser.add_argument('--expected-title', help='Override intended title explicitly; full default is Movie and Band')
    parser.add_argument('--output', type=Path, required=True)
    verify(parser.parse_args())


if __name__ == '__main__':
    main()
