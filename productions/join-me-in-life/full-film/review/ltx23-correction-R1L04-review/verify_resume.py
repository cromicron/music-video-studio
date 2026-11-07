"""Verify recovered correction comparison and already completed playback.

Writes only the two owning review folders. Elapsed generation times naturally
differ; compare the recorded step schedule without those timing measurements.
"""
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
BASE = ROOT / 'productions/join-me-in-life/full-film'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for key, queue in [('L04', 'R1W'), ('L05', 'R1H')]:
    old = BASE / f'assets/motion/ltx23-quiet-pilots/{key}'
    new = BASE / f'assets/motion/ltx23-quiet-corrections/{queue}/R1{key}'
    a = json.loads((old / 'render.json').read_text())
    b = json.loads((new / 'render.json').read_text())
    fields = ['seed', 'width', 'height', 'frames', 'fps', 'start_image_sha256',
              'end_image_sha256', 'start_frame_index', 'end_frame_index',
              'supplied_audio', 'model_audio_output', 'conditioning']
    checks = {f: a['manifest'][f] == b['manifest'][f] for f in fields}
    checks.update({f: a[f] == b[f] for f in ['image_guides', 'input_fitting']})
    schedule = lambda r: [{k: v for k, v in x.items() if k != 'elapsed_seconds'} for x in r['steps']]
    checks['step_schedule_without_elapsed_measurements'] = schedule(a) == schedule(b)
    assert all(checks.values())
    report = {'initial_video_sha256': sha(old / 'video-silent.mp4'),
              'correction_video_sha256': sha(new / 'video-silent.mp4'),
              'equal_fields': checks,
              'positive_prompt_changed': a['manifest']['prompt'] != b['manifest']['prompt'],
              'scope': 'Provenance comparison, not motion acceptance or a statistical generalization.'}
    (BASE / f'review/ltx23-correction-R1{key}-review/comparison-checks.json').write_text(json.dumps(report, indent=2) + '\n')
raw = ROOT / 'build/ltx23-correction-R1L04-review'
runs = []
for name in ['playback.json', 'keeper-playback.json', 'uncaptured-playback.json', 'keeper-uncaptured-playback.json']:
    data = json.loads((raw / name).read_text())
    assert sha(ROOT / data['played_file']) == data['played_file_sha256']
    runs.append({'retained_evidence': name, 'evidence_sha256': sha(raw / name),
                 'played_file': data['played_file'], 'played_file_sha256': data['played_file_sha256'],
                 'source_interval_seconds': data['source_interval_seconds'],
                 'ended_all': all(r['telemetry']['ended'] for r in data['runs'])})
report = {'scope': 'Completed playback recovered from the interrupted review; source/proxy hashes revalidated without rerunning completed execution.', 'runs': runs}
(BASE / 'review/ltx23-correction-R1L04-review/resume-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print('Both comparison records and all four retained R1L04 playback media hashes pass.')
