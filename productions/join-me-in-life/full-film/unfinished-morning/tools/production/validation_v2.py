"""Validate independently reviewed endpoints without changing neural execution."""
import json
import struct


def validate_manifest(manifest, root):
    # Deferred import: common.py retains all pinned helpers and imports us last.
    from common import TAKES, inside, sha256
    selected = TAKES.get(manifest.get('take_id'))
    if selected is None or manifest != selected['manifest']:
        raise ValueError('Manifest differs from the explicitly frozen v2 take')
    if (manifest.get('schema'), manifest.get('privacy'), manifest.get('mode')) != (
            'jml-ltx-story-v2/v1', 'private', 'diagnostic'):
        raise ValueError('Require one private v2 action diagnostic')
    if manifest.get('takes') != 1 or manifest.get('seed') != 49:
        raise ValueError('Exactly one seed49 take; no automatic retries')
    frames = manifest['frames']
    if not isinstance(frames, int) or isinstance(frames, bool) or not 89 <= frames <= 225 or (frames - 1) % 8:
        raise ValueError('Use a bounded 8n+1 frame count between89 and225')
    if tuple(manifest.get(k) for k in ('width', 'height', 'fps', 'start_frame_index', 'end_frame_index')) != (
            896, 512, 24, 0, frames - 1):
        raise ValueError('Pinned dimensions, timing or endpoint index changed')
    if manifest.get('supplied_audio') is not False or manifest.get('model_audio_output') is not False:
        raise ValueError('Narrative I2V exports video only; use separate A2V for singing')
    if any(k in manifest for k in ('audio', 'audio_pcm', 'input_waveform', 'intermediate_images')):
        raise ValueError('Extra guides or audio are not part of this tested runtime')
    if not isinstance(manifest.get('prompt'), str) or not manifest['prompt'].strip():
        raise ValueError('A concrete positive action prompt is required')
    action = manifest.get('action_contract', {})
    if any(not isinstance(action.get(k), str) or not action[k].strip()
           for k in ('story_beat', 'before', 'action', 'after')):
        raise ValueError('Record the story beat and visible before/action/after')
    dimensions = {}
    for field in ('start_image', 'end_image'):
        path = inside(root, manifest[field])
        if sha256(path) != manifest[field + '_sha256']:
            raise ValueError('Endpoint SHA256 mismatch: ' + field)
        header = path.read_bytes()[:24]
        if header[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('Endpoint must be an original PNG')
        dimensions[field] = list(struct.unpack('>II', header[16:24]))
        if dimensions[field] != manifest[field + '_dimensions']:
            raise ValueError('Endpoint dimensions changed: ' + field)
    if manifest['start_image_sha256'] == manifest['end_image_sha256']:
        raise ValueError('V2 action pilot requires distinct endpoint drawings')
    segments = manifest['editorial']['segments']
    if not segments:
        raise ValueError('Declare an intended source interval, including for a pilot')
    used = set()
    for segment in segments:
        start, end = segment['source_frames']
        if any(not isinstance(v, int) or isinstance(v, bool) for v in (start, end)) or not 0 <= start < end <= frames:
            raise ValueError('Invalid natural-speed source interval')
        indices = set(range(start, end))
        if used & indices:
            raise ValueError('Replayed source frames are not allowed')
        used |= indices
        timeline = segment.get('timeline_frames')
        if timeline is not None and (len(timeline) != 2 or timeline[1] - timeline[0] != end - start):
            raise ValueError('Timeline/source lengths must agree without retiming or holds')
    provenance = inside(root, manifest['source_provenance'])
    if sha256(provenance) != manifest['source_provenance_sha256']:
        raise ValueError('Source provenance hash changed')
    evidence = json.loads(provenance.read_text())
    if evidence['take_id'] != manifest['take_id'] or evidence['queue_id'] != manifest['queue_id']:
        raise ValueError('Source provenance belongs to another take')
    for field in ('start_image', 'end_image'):
        if evidence[field]['sha256'] != manifest[field + '_sha256']:
            raise ValueError('Endpoint provenance mismatch')
    review = inside(root, evidence['source_review']['bundle_path'])
    if sha256(review) != evidence['source_review']['sha256'] or evidence['source_review']['status'] != 'pass':
        raise ValueError('Reviewed endpoint evidence changed or is not passed')
    return dimensions


def validate_queue(queue, root):
    from common import QUEUES, TAKES, inside
    selected = QUEUES.get(queue.get('queue_id'))
    if selected is None or queue != selected['queue']:
        raise ValueError('Queue differs from the explicitly selected v2 batch')
    if (queue.get('schema'), queue.get('privacy'), queue.get('automatic_retries'), queue.get('whole_job_seconds')) != (
            'jml-story-v2-queue/v1', 'private', 0, 5400):
        raise ValueError('Private serial queue needs zero retries and a90-minute cap')
    ids = selected['takes']
    if not 1 <= len(ids) <= 5 or len(set(ids)) != len(ids) or set(TAKES) != set(ids):
        raise ValueError('Freeze one to five distinct takes, and no unrelated takes')
    if queue['manifests'] != [take + '.json' for take in ids]:
        raise ValueError('Queue order or child selection changed')
    paths = []
    for take in ids:
        path = inside(root, take + '.json')
        manifest = json.loads(path.read_text())
        if manifest['take_id'] != take or manifest['queue_id'] != queue['queue_id']:
            raise ValueError('Take, file and queue names disagree')
        validate_manifest(manifest, root)
        paths.append(path)
    return paths
