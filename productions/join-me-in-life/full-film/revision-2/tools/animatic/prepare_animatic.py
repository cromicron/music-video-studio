#!/usr/bin/env python3
"""Build a provenance-bound two-pose storyboard catalog; never approve animation."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
V2 = HERE.parents[1]
FILM = V2.parent
REPO = FILM.parents[2]
POSITIONS = {'top_left': 'tl', 'top_right': 'tr', 'bottom_left': 'bl', 'bottom_right': 'br',
             'left': 'l', 'right': 'r', 'entire_frame': 'full'}


def read(path): return json.loads(Path(path).read_text())
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2) + '\n')
def relative(path): return str(Path(path).resolve().relative_to(REPO))
def checked(path, digest):
    path = Path(path)
    if not path.is_file() or sha(path) != digest:
        raise ValueError('Missing or changed bound source: ' + str(path))
    return path
def dimensions(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height',
                             '-of', 'json', str(path)], check=True, capture_output=True, text=True)
    stream = json.loads(result.stdout)['streams'][0]
    return [stream['width'], stream['height']]
def adopt(source, target, digest):
    checked(source, digest)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists(): checked(target, digest)
    else: shutil.copyfile(source, target)
    checked(target, digest)


def panel_info(panel):
    shot = panel.get('shot_id', panel.get('shot'))
    position = panel.get('position', panel.get('region', panel.get('panel')))
    if isinstance(position, int): position = ['tl', 'tr', 'bl', 'br'][position-1]
    else:
        position = position.lower().replace('-', '_').replace(' ', '_')
        position = POSITIONS.get(position, position)
    phase = 'middle' if panel['phase'] in ('middle_incomplete_rise', 'middle_refusal') else panel['phase']
    if not shot or phase not in ('before', 'middle', 'after') or position not in {'tl', 'tr', 'bl', 'br', 'l', 'r', 'full'}:
        raise ValueError('Unrecognized exact panel_map entry: ' + repr(panel))
    return shot, phase, position


def provisional_box(size, position):
    """Explicit mechanical quadrant estimate, never a visual/source approval."""
    width, height = size
    if position == 'full': return [0, 0, width, height]
    middle_x, middle_y = width//2, height//2
    x, right = (4, middle_x-4) if position in {'tl', 'bl', 'l'} else (middle_x+4, width-4)
    if position in {'l', 'r'}: y, bottom = 4, height-4
    else: y, bottom = (4, middle_y-4) if position in {'tl', 'tr'} else (middle_y+4, height-4)
    return [x, y, right-x, bottom-y]


def extract_sheet(spec, output):
    meta_path = V2/spec['metadata']
    if not meta_path.exists(): return [], [str(spec['metadata'])]
    meta = read(meta_path)
    image = meta_path.with_suffix('.png')
    digest = meta.get('sha256', meta.get('png_sha256'))
    checked(image, digest)
    size = dimensions(image)
    review_path = V2/'review'/(meta_path.stem.lower()+'-static-review.json')
    review = read(review_path) if review_path.exists() else None
    if review:
        checked(REPO/review['source'], review['source_sha256'])
        if review['source_sha256'] != digest: raise ValueError('Review belongs to another source')
    crops = {r['panel']: r for r in (review or {}).get('inspection', {}).get('native_review_crops', [])}
    pairs = (review or {}).get('pairs', [])
    entries = []
    for panel in meta['panel_map']:
        shot, phase, position = panel_info(panel)
        if spec.get('shots') and shot not in spec['shots']: continue
        if spec.get('panels') and position not in spec['panels']: continue
        matching_pairs = [p for p in pairs if p['shot'] == shot and position in p.get('panels', [])]
        if len(matching_pairs) > 1: raise ValueError('Ambiguous independent panel review')
        pair, crop = (matching_pairs[0] if matching_pairs else None), crops.get(position)
        verdict = pair['verdict'] if pair else 'PENDING_INDEPENDENT_STATIC_REVIEW'
        if any(word in verdict for word in ('REJECT', 'FAIL', 'REVISE')):
            raise ValueError('Selected rejected source must be replaced: ' + shot + ' ' + verdict)
        record = {'shot_id': shot, 'phase': phase, 'panel': position,
                  'sheet': relative(image), 'sheet_sha256': digest,
                  'metadata': relative(meta_path), 'metadata_sha256': sha(meta_path),
                  'panel_map_entry': panel, 'creator_status': meta.get('status'),
                  'static_verdict': verdict, 'motion_approved': False,
                  'scope': 'Planning storyboard pose only; no generated motion or final cut acceptance.'}
        target = output/(shot+'-'+phase+'-'+meta_path.stem+'.png')
        if crop:
            source = REPO/crop['scratch_review_crop']
            adopt(source, target, crop['sha256'])
            record.update(extraction='byte_identical_adoption_of_independent_native_review_crop',
                          adopted_from=relative(source), adopted_sha256=crop['sha256'],
                          crop_xywh=crop['crop_xywh'], new_visual_approval_claimed=False)
        elif position == 'full':
            adopt(image, target, digest)
            record.update(extraction='byte_identical_standalone_candidate',
                          adopted_from=relative(image), adopted_sha256=digest,
                          new_visual_approval_claimed=False)
        else:
            box = spec.get('crop_xywh', {}).get(position, provisional_box(size, position))
            extraction_key = hashlib.sha256(json.dumps([digest, box]).encode()).hexdigest()[:10]
            target = output/(shot+'-'+phase+'-'+meta_path.stem+'-provisional-'+extraction_key+'.png')
            if not target.exists():
                subprocess.run(['ffmpeg', '-v', 'error', '-i', str(image), '-vf',
                                'crop='+':'.join(map(str, [box[2], box[3], box[0], box[1]])),
                                '-frames:v', '1', '-threads', '1', str(target)], check=True)
            record.update(extraction='provisional_ffmpeg_mechanical_crop', crop_xywh=box,
                          crop_visual_approval=False,
                          caution='Estimated panel bounds require actual viewing; no approval inferred from extraction.')
        if review:
            record.update(review=relative(review_path), review_sha256=sha(review_path),
                          reviewed_scope=review['scope'], review_pair=pair)
        record.update(path=relative(target), sha256=sha(target), native_dimensions=dimensions(target))
        entries.append(record)
    return entries, []


def direct_entries(output, groups=()):
    result = []
    pilot_path = V2/'review/pilot-handoff-medium-endpoint-review.json'
    pilot = read(pilot_path)
    for endpoint in pilot['endpoints']:
        phase = {'start': 'before', 'end': 'after'}[endpoint['role']]
        result.append(('V2-01', phase, FILM/endpoint['path_from_full_film'], endpoint['sha256'], pilot_path,
                       pilot['verdict'], {'crop_xywh': endpoint['crop_xywh']}))
    door_path = V2/'review/guide-09-v3-top-static-review.json'
    door = read(door_path)
    for phase in ('before', 'after'):
        endpoint = door[phase]
        result.append(('V2-17', phase, REPO/endpoint['file'], endpoint['sha256'], door_path, door['verdict'],
                       {'fit_note': 'Full original is preserved; static render uses contain, never the inspection resize.'}))
    for group in groups:
        review_path = V2/group['review']
        if group.get('review_sha256'): checked(review_path, group['review_sha256'])
        review = read(review_path)
        if review['shot'] != group['shot_id'] or not review['verdict'].startswith('PASS_STATIC'):
            raise ValueError('Direct pose group lacks a matching static pass')
        for phase in group['phases']:
            endpoint = review[phase]
            result.append((group['shot_id'], phase, REPO/endpoint['file'], endpoint['sha256'], review_path,
                           review['verdict'], {'fit_note': 'Exact reviewed pose; complete stationary contain fitting only.',
                                               'review_endpoint': endpoint}))
    records = []
    for shot, phase, source, digest, review, verdict, extra in result:
        target = output/(shot+'-'+phase+'-'+source.stem+'.png')
        adopt(source, target, digest)
        records.append({'shot_id': shot, 'phase': phase, 'path': relative(target), 'sha256': digest,
                        'native_dimensions': dimensions(target), 'extraction': 'byte_identical_adoption_of_reviewed_endpoint',
                        'adopted_from': relative(source), 'adopted_sha256': digest,
                        'review': relative(review), 'review_sha256': sha(review), 'static_verdict': verdict,
                        'new_visual_approval_claimed': False, 'motion_approved': False,
                        'scope': 'Existing static endpoint review adopted; planning fit is not production-motion approval.', **extra})
    return records


def generate(selection, output, catalog_path, config_path):
    if config_path.exists(): raise ValueError('Existing completed configuration is frozen; choose new revision paths')
    plan_path = V2/'story/shot-plan.json'
    plan = read(plan_path)
    checked(FILM/plan['audio']['path'], plan['audio']['sha256'])
    timing_reference = selection.get('timing_reference')
    if timing_reference:
        reference = read(checked(REPO/timing_reference['config'], timing_reference['sha256']))
        old_ranges = {}
        for exposure in reference['shots']:
            ident = exposure['story_shot_id']
            if ident not in old_ranges: old_ranges[ident] = [exposure['start_frame'], exposure['end_frame_exclusive']]
            else: old_ranges[ident][1] = exposure['end_frame_exclusive']
        current_ranges = {shot['id']: [shot['start_frame'], shot['end_frame_exclusive']] for shot in plan['shots']}
        if old_ranges != current_ranges: raise ValueError('Original 49 story-shot boundaries changed')
    profiles = selection.get('shot_exposures', {})
    if any(shot not in {'V2-27', 'V2-31'} or profile != [['before', 0.3], ['middle', 0.25], ['after', 0.45]]
           for shot, profile in profiles.items()):
        raise ValueError('Only the explicitly selected V2-27/V2-31 middle-pose timings are supported')
    entries = direct_entries(output, selection.get('direct_review_groups', []))
    absent_files = []
    for sheet in selection['sheets']:
        added, missing = extract_sheet(sheet, output)
        entries.extend(added); absent_files.extend(missing)
    by_key = {}
    for item in entries:
        key = (item['shot_id'], item['phase'])
        if key in by_key: raise ValueError('Duplicate selected endpoint: '+repr(key))
        by_key[key] = item
    expected = {(s['id'], phase) for s in plan['shots']
                for phase, weight in profiles.get(s['id'], [['before', 0.4], ['after', 0.6]])}
    if set(by_key)-expected: raise ValueError('Unexpected shots in art panel_map')
    missing = [{'shot_id': shot, 'phase': phase} for shot, phase in sorted(expected-set(by_key))]
    catalog = {'schema': 'jml-v2-storyboard-source-catalog/v1',
               'story_revision': selection['story_revision'],
               'status': 'planning_only_missing_sources' if missing else 'planning_only_complete_sources',
               'shot_plan': relative(plan_path), 'shot_plan_sha256': sha(plan_path),
               'unchanged_shot_timing_reference': timing_reference,
               'planning_only': True, 'motion_approval_claimed': False,
               'held_pose_policy': 'Stationary planning poses; default before40/after60. Explicit shot profile overrides recorded below. No animation inferred.',
               'shot_exposures': profiles,
               'missing_endpoints': missing, 'missing_metadata_files': absent_files,
               'static_verdict_counts': dict(Counter(e['static_verdict'] for e in entries)), 'sources': entries}
    save(catalog_path, catalog)
    if missing: return catalog, None
    if selection.get('require_all_selected_static_reviews') and any(
            not source['static_verdict'].startswith('PASS_STATIC') for source in entries):
        catalog['status'] = 'planning_sources_complete_waiting_static_reviews'
        save(catalog_path, catalog)
        return catalog, None
    if selection.get('render_gate') == 'awaiting_independent_reviews_and_root_gate':
        catalog['status'] = 'planning_sources_complete_waiting_root_gate'
        save(catalog_path, catalog)
        return catalog, None
    shots, sources = [], {}
    cursor = 0
    for shot in plan['shots']:
        if shot['start_frame'] != cursor: raise ValueError('Noncontiguous story plan')
        end = shot['end_frame_exclusive']
        profile = profiles.get(shot['id'], [['before', 0.4], ['after', 0.6]])
        exposure_start, fraction = cursor, 0
        for phase, weight in profile:
            fraction += weight
            start, stop = exposure_start, cursor+round((end-cursor)*fraction)
            exposure_start = stop
            key = shot['id']+'-'+phase
            source = by_key[(shot['id'], phase)]
            sources[key] = {'path': str((REPO/source['path']).relative_to(FILM)), 'kind': 'storyboard_panel',
                            'sha256': source['sha256'], 'catalog_source': source}
            shots.append({'id': key, 'story_shot_id': shot['id'], 'phase': phase,
                          'start_frame': start, 'end_frame_exclusive': stop, 'section': shot['section'],
                          'source_key': key, 'camera': {'zoom_start': 1, 'zoom_end': 1,
                          'center_start': [0.5, 0.5], 'center_end': [0.5, 0.5]},
                          'title': False, 'final_fade_seconds': 0})
        cursor = end
    if cursor != 6667 or len(shots) != len(expected): raise ValueError('Expected all 49 shots and explicitly selected poses')
    no_motion = HERE/'planning-no-motion.json'
    save(no_motion, {'schema': 'jml-approved-motion/v1', 'clips': [], 'scope': 'Planning animatic uses no motion clips.'})
    config = {'schema': 'jml-v2-storyboard-animatic-edit/v1', 'status': 'PLANNING ANIMATIC — not final animation',
              'story_revision': selection['story_revision'],
              'fps': 24, 'total_frames': 6667, 'audio': plan['audio']['path'],
              'audio_sha256': plan['audio']['sha256'], 'catalog': relative(catalog_path),
              'catalog_sha256': sha(catalog_path), 'shot_plan_sha256': sha(plan_path),
              'narrative_shots': 49, 'pose_exposures': len(shots), 'shot_exposures': profiles,
              'approved_motion': str(no_motion.relative_to(FILM)),
              'production_tools': ['ChatGPT image generation', 'Owned LTX animation pipeline', 'FFmpeg'],
              'actual_animatic_tools': ['ChatGPT image generation', 'FFmpeg'],
              'sources': sources, 'shots': shots}
    save(config_path, config)
    return catalog, config


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selection', type=Path, default=HERE/'selection-v1.json')
    p.add_argument('--inputs', type=Path, default=V2/'assets/scene-inputs/animatic-v1')
    p.add_argument('--catalog', type=Path, default=HERE/'source-catalog-v1.json')
    p.add_argument('--config', type=Path, default=HERE/'edit-v1.json')
    args = p.parse_args()
    catalog, config = generate(read(args.selection), args.inputs.resolve(), args.catalog.resolve(), args.config.resolve())
    print(json.dumps({'status': catalog['status'], 'endpoint_count': len(catalog['sources']),
                      'missing_endpoints': catalog['missing_endpoints'], 'config_written': config is not None}, indent=2))
    raise SystemExit(0 if config else 2)
