#!/usr/bin/env python3
"""Bind the new editorial plan through the retained strict frame-exact engine."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

FULL_FILM = Path(__file__).resolve().parents[2]
ENGINE = FULL_FILM / 'revision-2/tools/editor/strict_edit.py'
spec = importlib.util.spec_from_file_location('retained_strict_editor', ENGINE)
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def digest(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def verify_new_take_origin(generation_id, source, provider_plan, provider_digest):
    """Bind actual downloaded bytes/manifest to the frozen generation contract.

    This is provenance validation only. The strict engine separately requires an
    accepted exact-hash motion gate before the source can render.
    """
    origin = source.get('generation', {})
    editor.require(origin.get('shot_id') == generation_id, 'New source generation ID differs')
    editor.require(origin.get('provider_plan_sha256') == provider_digest,
                   'New source has missing/stale provider-plan SHA')
    record = editor.local_file(FULL_FILM, origin.get('render_record', ''))
    editor.require(digest(record) == origin.get('render_record_sha256'), 'New render record SHA changed')
    actual = json.loads(record.read_text())
    manifest, video = actual.get('manifest', {}), actual.get('video', {})
    requested = {s['id']: s for s in provider_plan['shots']}
    editor.require(generation_id in requested, 'New source absent from provider plan')
    shot = requested[generation_id]
    expected = shot['planned_generation']
    editor.require(manifest.get('take_id', manifest.get('shot_id')) == generation_id,
                   'Actual render manifest names a different shot')
    editor.require(video.get('sha256') == source.get('sha256'), 'Actual video SHA differs from render record')
    editor.require(manifest.get('frames') == video.get('frames') == expected['model_frames_8n_plus_1']
                   and manifest.get('fps') == video.get('fps') == 24,
                   'Actual raw extent/cadence differs from provider plan')
    supplied_audio = expected['method'] == 'original_song_A2V'
    editor.require(manifest.get('supplied_audio') is supplied_audio,
                   'Actual conditioning method differs from provider plan')
    editorial = manifest.get('editorial', {})
    if supplied_audio:
        timeline, keeper = editorial.get('timeline_frames'), editorial.get('source_frames')
        pcm = manifest.get('audio_pcm', {})
        editor.require(pcm.get('sample_rate') == 48000 and pcm.get('channels') == 2
                       and pcm.get('samples') == expected['model_frames_8n_plus_1'] * 2000,
                       'Actual conditioning PCM extent differs from the frozen original-song request')
    else:
        segments = editorial.get('segments', [])
        editor.require(len(segments) == 1 and segments[0].get('shot_id') == generation_id,
                       'Actual narrative render has a different editorial binding')
        timeline, keeper = segments[0].get('timeline_frames'), segments[0].get('source_frames')
    editor.require(timeline == [shot['start_frame'], shot['end_frame_exclusive']]
                   and keeper == expected['source_keeper_range'],
                   'Actual render timing/keeper differs from frozen provider plan')
    editor.require(editorial.get('head_handle_frames') == expected['head_handle_frames']
                   and editorial.get('tail_handle_frames') == expected['tail_handle_frames'],
                   'Actual render handles differ from provider plan')


def build(story, bindings, reconciliations=None):
    editor.require(story.get('status') == 'adopted_editorial_reallocation_pending_motion',
                   'Use the adopted editorial plan, not a proposal/provider job plan')
    editor.require(bindings.get('schema') == 'jml-performance-bindings/v1', 'Unknown binding schema')
    plan = copy.deepcopy(story)
    plan['sources'] = copy.deepcopy(bindings['sources'])
    direct = bindings.get('shot_sources', {})
    takes = bindings.get('take_sources', {})
    if takes:
        adoption = story.get('adoption', {})
        provider_path = editor.local_file(editor.REPOSITORY, adoption.get('generation_plan', ''))
        provider_digest = digest(provider_path)
        editor.require(provider_digest == adoption.get('generation_plan_sha256'),
                       'Editorial/provider plan hash differs')
        provider_plan = json.loads(provider_path.read_text())
        for generation_id, source_id in takes.items():
            editor.require(source_id in plan['sources'], 'New take maps to an unknown source')
            verify_new_take_origin(generation_id, plan['sources'][source_id],
                                   provider_plan, provider_digest)
    shot_ids = {s['id'] for s in plan['shots']}
    editor.require(not set(direct) - shot_ids, 'Bindings name an unknown editorial shot')
    for shot in plan['shots']:
        editor.require('source' not in shot, 'Story must not silently bind motion')
        # Provider drafts remain in the immutable source plans, not as instructions
        # to repeat obsolete gold-world acting or regenerate already accepted takes.
        if 'reuse_provenance' in shot:
            for field in ('image_briefs', 'planned_generation', 'source_binding',
                          'pacing_and_camera_direction'):
                shot.pop(field, None)
        recipe = shot.get('planned_source')
        editor.require(not (shot['id'] in direct and recipe and recipe['generation_id'] in takes),
                       'Shot has both direct and generated binding; reconcile explicitly')
        if shot['id'] in direct:
            shot['source'] = copy.deepcopy(direct[shot['id']])
        elif recipe and recipe['generation_id'] in takes:
            shot['source'] = {
                'id': takes[recipe['generation_id']],
                'in_frame': recipe['in_frame'],
                'out_frame_exclusive': recipe['out_frame_exclusive'],
            }
        if reconciliations and shot['id'] in reconciliations.get('shots', {}):
            change = reconciliations['shots'][shot['id']]
            if 'world' in change:
                shot['world'] = change['world']
            if 'story' in change:
                shot['story'].update(copy.deepcopy(change['story']))
            if 'pacing_and_camera_direction' in change:
                shot['pacing_and_camera_direction'] = change['pacing_and_camera_direction']
    editor.validate_story(plan)
    available = [s for s in plan['shots'] if 'source' in s]
    if available:
        editor.bind_sources(plan, available)
    plan['status'] = ('complete_motion_candidate_pending_full_review'
                      if len(available) == len(plan['shots']) else 'partial_motion_workprint_only')
    plan['binding_counts'] = {'total_shots': len(plan['shots']), 'bound': len(available),
                              'missing': len(plan['shots']) - len(available)}
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story', type=Path, required=True)
    parser.add_argument('--bindings', type=Path, required=True)
    parser.add_argument('--reconcile', type=Path)
    parser.add_argument('--title', default='Join Me in Life — Movie and Band',
                        help='Intended MP4 title; metadata only, no opening overlay')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    editor.require(not args.output.exists(), 'Preserve prior edit versions; choose a new output')
    plan = build(json.loads(args.story.read_text()), json.loads(args.bindings.read_text()),
                 json.loads(args.reconcile.read_text()) if args.reconcile else None)
    editor.require(bool(args.title.strip()), 'Title must not be empty')
    plan['title'] = args.title
    plan['inputs'] = {
        'editorial_story': {'path': str(args.story), 'sha256': digest(args.story)},
        'bindings': {'path': str(args.bindings), 'sha256': digest(args.bindings)},
        'strict_engine': {'path': str(ENGINE.relative_to(FULL_FILM)), 'sha256': digest(ENGINE)},
    }
    if args.reconcile:
        plan['inputs']['prose_reconciliation'] = {'path': str(args.reconcile),
                                                 'sha256': digest(args.reconcile)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps(plan['binding_counts']))


if __name__ == '__main__':
    main()
