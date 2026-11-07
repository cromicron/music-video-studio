"""Retain compact R1L05 evidence from reproduce.py's completed ignored cache.

No provider call or playback rerun. Verify the source and three played files
before carrying the interrupted review's completed telemetry into the report.
"""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'studio.json').is_file())
RAW = ROOT / 'build/ltx23-correction-R1L05-review'
SOURCE = ROOT / 'productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-corrections/R1H/R1L05/video-silent.mp4'
EXPECTED = '0a8e44b2dbc7c5038ecc0667214aae0375b3f0e2e5320fc7996a1f00ea3be24b'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE) == EXPECTED
playback = json.loads((RAW / 'playback.json').read_text())
files = {'raw': SOURCE, 'S030': RAW / 'S030-selected.mp4', 'S032': RAW / 'S032-selected.mp4'}
for run in playback['runs']:
    assert sha(files[run['key']]) == run['source_sha256']
    assert run['telemetry']['ended'] and run['telemetry']['playbackRate'] == 1
summary = {
    'source_sha256': EXPECTED,
    'browser': playback['browser'],
    'chromium_sandbox': playback['chromium_sandbox'],
    'retained_raw_playback_sha256': sha(RAW / 'playback.json'),
    'scope': 'Recovered completed 1x playback from the interrupted review; source/proxy hashes revalidated. Frame/capture inspection is separate from human continuous perception or listening.',
    'runs': [{**{k: v for k, v in run.items() if k != 'telemetry'},
              'telemetry': {k: v for k, v in run['telemetry'].items() if k != 'frameCallbacks'},
              'frame_callback_count': len(run['telemetry']['frameCallbacks'])}
             for run in playback['runs']],
}
(HERE / 'playback-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
for name in ['checks.json', 'overview.jpg', 'guide-endpoints.jpg', 'contact-phases.jpg',
             'captured-S030-1.jpg', 'captured-S032-1.jpg']:
    shutil.copyfile(RAW / name, HERE / name)
frames = np.load(RAW / 'frames.npy', mmap_mode='r')
assert frames.shape == (201, 512, 896, 3)
for name, ids, box in [
    ('gaze-phases.jpg', [0, 16, 24, 48, 72, 88, 100, 112, 144, 196], (180, 0, 650, 310)),
    ('eyelid-phases.jpg', [80, 84, 88, 92, 96, 100, 104, 108, 112], (250, 130, 390, 230)),
]:
    w, h = box[2] - box[0], box[3] - box[1]
    image = Image.new('RGB', (3 * w, ((len(ids) + 2) // 3) * (h + 24)), '#171717')
    draw = ImageDraw.Draw(image)
    for j, i in enumerate(ids):
        x, y = j % 3 * w, j // 3 * (h + 24)
        draw.text((x + 4, y + 5), f'f{i+1:03} | {i/24:.3f}s', fill='white')
        image.paste(Image.fromarray(frames[i]).crop(box), (x, y + 24))
    image.save(HERE / name, quality=95)
print('R1L05 source/proxy hashes and completed playback verified; compact evidence retained.')
