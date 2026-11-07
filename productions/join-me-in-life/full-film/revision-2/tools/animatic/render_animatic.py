#!/usr/bin/env python3
"""Reuse the full-film editor with stationary contain framing for this planning-only cut."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
spec = importlib.util.spec_from_file_location('full_film_editor', FILM/'edit.py')
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


def static_contain(shot, width, height, streamed=False):
    c = shot['camera']
    if streamed or c != {'zoom_start': 1, 'zoom_end': 1, 'center_start': [0.5, 0.5], 'center_end': [0.5, 0.5]}:
        raise ValueError('Planning animatic only permits stationary, complete endpoint pictures')
    return (f'scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos,'
            f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
            f'loop=loop={shot["frames"]-1}:size=1:start=0,settb=1/24,setpts=N,fps=24')


original_assemble, original_report = editor.assemble_plan, editor.report
def assemble(edit):
    if edit['schema'] != 'jml-v2-storyboard-animatic-edit/v1': raise ValueError('Wrong planning configuration')
    catalog = FILM.parents[2]/edit['catalog']
    if editor.sha256(catalog) != edit['catalog_sha256']: raise ValueError('Planning catalog changed; make an explicit new revision')
    if editor.sha256(editor.resolve_path(edit['audio'])) != edit['audio_sha256']: raise ValueError('Original song changed')
    for source in edit['sources'].values():
        if editor.sha256(editor.resolve_path(source['path'])) != source['sha256']: raise ValueError('Endpoint changed')
    shots, _ = original_assemble(edit)
    for shot in shots:
        if shot['motion'] or shot.get('title') or shot.get('final_fade_seconds') or shot.get('drawn_art_segments'):
            raise ValueError('No generated clip, branding, fade or added performance in blind planning animatic')
        shot['classification'] = 'held_storyboard_endpoint_planning_only'
    return shots, 'Held storyboard drawings with explicitly selected exposures. No generated motion, camera movement or final-film acceptance.'


def report(edit, shots, note, output=None):
    result = original_report(edit, shots, note, output)
    extent = 'FULL-SONG' if result['coverage']['full_song'] else 'EXCERPT'
    result.update(status=extent+' STORYBOARD PLANNING ANIMATIC — NOT FINAL ANIMATION',
                  story_revision=edit['story_revision'],
                  storyboard_catalog={'path': edit['catalog'], 'sha256': edit['catalog_sha256']},
                  shot_plan_sha256=edit['shot_plan_sha256'],
                  narrative_shots=len({shot['story_shot_id'] for shot in shots}), endpoint_exposures=len(shots),
                  shot_exposures=edit.get('shot_exposures', {}),
                  overlay_captions=False, opening_title=False, camera_motion=False)
    result['motion_accounting']['held_storyboard_pose_seconds'] = result['motion_accounting'].pop('still_camera_seconds')
    return result


if __name__ == '__main__':
    if '--render' in sys.argv:
        if '--output' not in sys.argv: raise ValueError('Explicit new planning output path required')
        if Path(sys.argv[sys.argv.index('--output')+1]).exists(): raise ValueError('Existing export is frozen; choose a new revision')
    editor.VERSION += '-v2-static-storyboard-2'
    editor.still_filter, editor.assemble_plan, editor.report = static_contain, assemble, report
    editor.main()
