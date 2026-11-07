"""Local staging guard against stale story hashes and silently shifted edit ranges."""
import hashlib
import json
from pathlib import Path


def validate_story_binding(plan, adopted_path, mode):
    path = Path(adopted_path)
    if not path.is_file():
        raise ValueError('Adopted story plan is missing')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if plan.get('story_plan_sha256') != digest:
        raise ValueError('Missing or stale adopted story plan SHA256')
    story = json.loads(path.read_text())
    shots = {shot['id']: shot for shot in story['shots']}
    for take in plan['takes']:
        if mode == 'performance':
            sid = take['shot_id']
            timeline = take['timeline_frames']
            keeper = [6, 6 + timeline[1] - timeline[0]]
        else:
            segments = take['editorial']['segments']
            if len(segments) != 1:
                raise ValueError('C narrative take must bind one exact adopted shot')
            segment = segments[0]
            sid, timeline, keeper = segment['shot_id'], segment['timeline_frames'], segment['source_frames']
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
