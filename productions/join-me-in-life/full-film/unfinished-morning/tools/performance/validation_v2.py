"""Frozen C selections over the unchanged supplied-song engine. Schema compatibility retained; old queues rejected."""
import hashlib
import json
import re
from pathlib import Path
import struct
import wave


MASTER_SHA256 = '0fe0f566e985a0b028e12543679d3b142ee7b1b62425fcb595799b35ba116cbb'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inside(root, relative):
    require(isinstance(relative, str) and not Path(relative).is_absolute(), 'Relative bundle input required')
    path = (Path(root) / relative).resolve()
    require(path.is_relative_to(Path(root).resolve()) and path.is_file(), 'Missing input or path escape')
    return path


def validate_manifest(manifest, root):
    root = Path(root)
    specs = json.loads(inside(root, 'take-specs.json').read_text())
    selected = specs.get(manifest.get('shot_id'))
    require(selected is not None and manifest == selected['manifest'], 'Manifest differs from its frozen selected take')
    require((manifest['schema'], manifest['privacy'], manifest['mode'], manifest['takes']) ==
            ('jml-ltx-performance-v2/v1', 'private', 'diagnostic', 1), 'Private single diagnostic required')
    require(re.fullmatch(r'C[A-Z0-9_-]{1,35}', manifest['shot_id']) is not None, 'C-only take required')
    frames = manifest['frames']
    require((manifest['width'], manifest['height'], manifest['fps'], manifest['seed']) == (896, 512, 24, 49)
            and type(frames) is int and frames in (89, 97, 105, 113, 121, 129) and (frames - 1) % 8 == 0, 'Unselected frame extent or generation setting')
    require(not any(key in manifest for key in ('end_image', 'end_frame_index', 'intermediate_images')),
            'This unchanged A2V engine is first-image-only')
    require(manifest['supplied_audio'] is True and manifest['model_audio_output'] is False,
            'Use supplied original audio and discard generated audio')
    require(isinstance(manifest['prompt'], str) and manifest['prompt'].strip(), 'Missing exact prompt')
    editorial = manifest['editorial']
    first, last = editorial['timeline_frames']
    start, stop = editorial['source_frames']
    require(start == editorial['head_handle_frames'] == 6 and stop - start == last - first
            and frames - stop == editorial['tail_handle_frames'] >= 7, 'Timeline/handles changed')
    for field in ('image', 'audio', 'audio_provenance', 'image_provenance'):
        require(sha(inside(root, manifest[field])) == manifest[field + '_sha256'], 'Input hash mismatch: ' + field)
    header = inside(root, manifest['image']).read_bytes()[:24]
    require(header[:8] == b'\x89PNG\r\n\x1a\n' and list(struct.unpack('>II', header[16:24])) == manifest['image_dimensions'],
            'Exact reviewed source dimensions required')
    image_prov = json.loads(inside(root, manifest['image_provenance']).read_text())
    require(image_prov['image_sha256'] == manifest['image_sha256'] and image_prov['shot_id'] == manifest['shot_id'],
            'Image adoption belongs to another source/shot')
    review = inside(root, image_prov['review_bundle_path'])
    require(sha(review) == image_prov['review_sha256'], 'Independent source review changed')
    review_data = json.loads(review.read_text())
    pairs = [p for p in review_data['pairs'] if p['shot'] == manifest['shot_id']]
    require(len(pairs) == 1 and pairs[0]['verdict'] == 'PASS_STATIC_SOURCE_FOR_BOUNDED_MOTION_TEST'
            and image_prov['panel'] in pairs[0]['panels'], 'No independently passed source pair for this shot')
    crops = [c for c in review_data['inspection']['native_review_crops'] if c['panel'] == image_prov['panel']]
    require(len(crops) == 1 and crops[0]['native_pixels_viewed'] is True
            and crops[0]['sha256'] == manifest['image_sha256'], 'Input is not the exact independently viewed crop')
    with wave.open(str(inside(root, manifest['audio'])), 'rb') as audio:
        actual = {'samples': audio.getnframes(), 'sample_rate': audio.getframerate(),
                  'channels': audio.getnchannels(), 'sample_width_bytes': audio.getsampwidth()}
        require(audio.getcomptype() == 'NONE' and actual == manifest['audio_pcm'], 'PCM format/extent changed')
        pcm = audio.readframes(audio.getnframes())
    require(actual == {'samples': frames * 2000, 'sample_rate': 48000, 'channels': 2, 'sample_width_bytes': 2},
            'Preserve complete exact stereo48k PCM16 extent, without invented samples')
    audio_prov = json.loads(inside(root, manifest['audio_provenance']).read_text())
    require(audio_prov['source_master_sha256'] == MASTER_SHA256
            and audio_prov['conditioning_sha256'] == manifest['audio_sha256']
            and audio_prov['pcm_sha256'] == hashlib.sha256(pcm).hexdigest()
            and audio_prov['start_sample'] == (first - 6) * 2000
            and audio_prov['end_sample_exclusive'] == (first - 6 + frames) * 2000
            and audio_prov['start_seconds'] == (first - 6) / 24
            and audio_prov['target_edit_shot'] == manifest['shot_id']
            and audio_prov['target_edit_frames'] == [first, last]
            and all(audio_prov[key] == value for key, value in actual.items()), 'Original audio provenance/interval changed')
    return actual


def validate_queue(queue, root):
    expected = json.loads(inside(root, 'queue-spec.json').read_text())
    require(queue == expected, 'Queue differs from its frozen C batch selection')
    require(queue['schema'] == 'jml-v2-performance-queue/v1' and queue['privacy'] == 'private'
            and queue['automatic_retries'] == 0 and queue['whole_job_seconds'] == 5390
            and 1 <= len(queue['manifests']) <= 5 and len(set(queue['manifests'])) == len(queue['manifests'])
            and re.fullmatch(r'C[A-Z0-9_-]{1,35}', queue['queue_id']) is not None, 'Only the frozen selected C batch is authorized')
    paths = []
    for name in queue['manifests']:
        path = inside(root, name)
        manifest = json.loads(path.read_text())
        require(manifest['shot_id'] == path.stem, 'Manifest/shot mismatch')
        validate_manifest(manifest, root)
        paths.append(path)
    return paths
