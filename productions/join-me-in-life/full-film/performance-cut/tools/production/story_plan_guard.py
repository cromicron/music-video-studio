"""Local staging guard against stale story hashes and silently shifted edit ranges."""
import hashlib
import json
import re
from pathlib import Path


def validate_story_binding(plan, adopted_path, mode):
    path = Path(adopted_path)
    if not path.is_file():
        raise ValueError('Adopted story plan is missing')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if plan.get('story_plan_sha256') != digest:
        raise ValueError('Missing or stale adopted story plan SHA256')
    story = json.loads(path.read_text())
    if (story.get('schema') != 'jml-story-edit/v2'
            or story.get('production') != 'join-me-in-life-performance-cut'
            or story.get('status') != 'adopted_for_production'
            or story.get('adoption', {}).get('state') != 'adopted_for_production'
            or story.get('fps') != 24 or story.get('total_frames') != 6667):
        raise ValueError('Only the adopted performance-cut story may stage; proposals and old stories are rejected')
    shots = {shot['id']: shot for shot in story['shots']}
    for take in plan['takes']:
        if mode == 'performance':
            sid = take['shot_id']
            timeline = take['timeline_frames']
            keeper = [6, 6 + timeline[1] - timeline[0]]
        else:
            segments = take['editorial']['segments']
            if len(segments) != 1:
                raise ValueError('Performance-cut I2V take must bind one exact adopted shot')
            segment = segments[0]
            sid, timeline, keeper = segment['shot_id'], segment['timeline_frames'], segment['source_frames']
        if not re.fullmatch(r'[BO][A-Z0-9_-]{1,35}', sid):
            raise ValueError('Only new B/O slots may generate; inherited C footage is reuse-only')
        if sid not in shots:
            raise ValueError('Shot absent from adopted story plan: ' + sid)
        shot = shots[sid]
        generation = shot['planned_generation']
        expected_method = 'original_song_A2V' if mode == 'performance' else 'reviewed_endpoints_I2V'
        if (timeline != [shot['start_frame'], shot['end_frame_exclusive']]
                or take['frames'] != generation['model_frames_8n_plus_1']
                or keeper != generation['source_keeper_range']
                or generation['fps'] != 24
                or generation['method'] != expected_method):
            raise ValueError('Take timing, keeper, length or method differs from adopted shot: ' + sid)
        if generation['head_handle_frames'] != 6 or generation['tail_handle_frames'] != take['frames'] - keeper[1]:
            raise ValueError('Adopted shot handles inconsistent: ' + sid)
        if mode == 'performance':
            audio = generation['original_audio']
            start = timeline[0] - 6
            if (audio['sample_rate'] != 48000 or audio['source_frame_start'] != start
                    or audio['source_samples'] != [start * 2000, (start + take['frames']) * 2000]):
                raise ValueError('Adopted original-song sample range inconsistent: ' + sid)
        elif (take['editorial']['head_handle_frames'] != 6
                or take['editorial']['tail_handle_frames'] != generation['tail_handle_frames']):
            raise ValueError('Take editorial handles differ from adopted shot: ' + sid)
    return digest
