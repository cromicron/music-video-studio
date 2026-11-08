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


def build(story, bindings, reconciliations=None):
    editor.require(story.get('status') == 'adopted_editorial_reallocation_pending_motion',
                   'Use the adopted editorial plan, not a proposal/provider job plan')
    editor.require(bindings.get('schema') == 'jml-performance-bindings/v1', 'Unknown binding schema')
    plan = copy.deepcopy(story)
    plan['sources'] = copy.deepcopy(bindings['sources'])
    direct = bindings.get('shot_sources', {})
    takes = bindings.get('take_sources', {})
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
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    editor.require(not args.output.exists(), 'Preserve prior edit versions; choose a new output')
    plan = build(json.loads(args.story.read_text()), json.loads(args.bindings.read_text()),
                 json.loads(args.reconcile.read_text()) if args.reconcile else None)
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
