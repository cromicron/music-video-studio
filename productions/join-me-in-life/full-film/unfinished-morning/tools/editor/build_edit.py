#!/usr/bin/env python3
"""Build a C-only incremental edit from the current story and explicit motion bindings."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

FULL_FILM = Path(__file__).resolve().parents[3]
ENGINE = FULL_FILM / 'revision-2/tools/editor/strict_edit.py'
spec = importlib.util.spec_from_file_location('retained_strict_editor', ENGINE)
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(story, bindings):
    editor.require(story['fps'] == 24 and story['total_frames'] == 6667, 'C must cover the original whole song')
    editor.require(bindings['schema'] == 'jml-c-motion-bindings/v1', 'Unknown binding schema')
    shots = copy.deepcopy(story['shots'])
    ids = {s['id'] for s in shots}
    selected = bindings.get('shot_sources', {})
    editor.require(not (set(selected) - ids), 'Bindings name unknown story shots')
    for shot in shots:
        editor.require('source' not in shot, 'Story must not silently supply an unreviewed motion binding')
        if shot['id'] in selected:
            shot['source'] = copy.deepcopy(selected[shot['id']])
    plan = {'schema': editor.SCHEMA, 'fps': 24, 'total_frames': 6667,
            'status': 'partial_motion_workprint_only',
            'title': 'Join Me in Life — Unfinished Morning review candidate',
            'production': 'join-me-in-life-unfinished-morning',
            'audio': {'path': '../full-song/track-49.mp3', 'sha256': editor.SONG_SHA256},
            'sources': copy.deepcopy(bindings.get('sources', {})), 'shots': shots,
            'note': 'Only explicit reviewed bindings may render; no missing-source fallback. Actual cuts/final song review remain separate.'}
    editor.validate_story(plan)
    available = [s for s in shots if 'source' in s]
    if available:
        editor.bind_sources(plan, available)
    return plan


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--story', type=Path, required=True)
    p.add_argument('--bindings', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    editor.require(not a.output.exists(), 'Choose a new edit version; preserve previous reviewed edits')
    plan = build(json.loads(a.story.read_text()), json.loads(a.bindings.read_text()))
    plan['input_bindings'] = {'story': {'path': str(a.story), 'sha256': sha(a.story)},
                              'motion_ledger': {'path': str(a.bindings), 'sha256': sha(a.bindings)},
                              'strict_engine': {'path': str(ENGINE.relative_to(FULL_FILM)), 'sha256': sha(ENGINE)}}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n')
    print(f"Built {len(plan['shots'])} shots; {sum('source' in s for s in plan['shots'])} bound motion intervals. No film/cut approval implied.")


if __name__ == '__main__':
    main()
