"""Reproduce hash-bound raw frames and source review sheets in ignored build/."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image, ImageDraw

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
NAME = Path(__file__).resolve().parent.name
TAKE = NAME.split('-')[-2]
SPECS = {
    'P1L02': (121, 116, '24312a9d5272083d1c3f248837d63f0b61b8be1a051b6b99c5de2d092cdad53b'),
    'P1L03': (113, 104, '14753d944afdd0ab41db66401ae694ee45c496f1392eb6913d0bbd4da369f2cc'),
}
count, stop, expected = SPECS[TAKE]
OUT = ROOT / 'build' / NAME
OUT.mkdir(parents=True, exist_ok=True)
FILM = ROOT / 'productions/join-me-in-life/full-film'
MEDIA = FILM / f'assets/motion/ltx23-positive-continuation/P1/{TAKE}/video-silent.mp4'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest() == expected
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-of', 'json', str(MEDIA)]))
assert len(probe['streams']) == 1
v = probe['streams'][0]
assert (v['width'], v['height'], v['avg_frame_rate'], int(v['nb_read_frames'])) == (896, 512, '24/1', count)
frames = OUT / 'frames'
frames.mkdir(exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-y', '-i', str(MEDIA), '-fps_mode', 'passthrough', str(frames / 'f%03d.png')], check=True)
paths = sorted(frames.glob('f*.png'))
assert len(paths) == count
images = [Image.open(p).convert('RGB') for p in paths]

def sheet(indices, crop, cols, filename, resize=None, resample=Image.Resampling.LANCZOS):
    tiles = []
    for i in indices:
        tile = images[i].crop(crop)
        if resize:
            tile = tile.resize(resize, resample)
        canvas = Image.new('RGB', (tile.width, tile.height + 22), (20, 20, 20))
        canvas.paste(tile, (0, 22))
        ImageDraw.Draw(canvas).text((5, 4), f'f{i+1:03d} | {i/24:.3f}s', fill='white')
        tiles.append(canvas)
    w, h = tiles[0].size
    result = Image.new('RGB', (w * cols, h * ((len(tiles) + cols - 1) // cols)), (40, 40, 40))
    for n, tile in enumerate(tiles):
        result.paste(tile, ((n % cols) * w, (n // cols) * h))
    result.save(OUT / filename, **({'quality': 94} if filename.endswith('.jpg') else {}))

sheet(sorted(set(list(range(0, count, 12)) + [count - 1])), (0, 0, 896, 512), 3, 'overview.jpg', (448, 256))
for first in range(0, count, 16):
    ids = range(first, min(first + 16, count))
    sheet(ids, (88, 65, 580, 310), 4, f'faces-{first+1:03d}-{min(first+16,count):03d}.jpg')
    sheet(ids, (0, 0, 896, 512), 4, f'full-{first+1:03d}-{min(first+16,count):03d}.jpg', (448, 256))
phases = sorted(set([3, 16, 24, 32, 48, 60, 68, 72, 88, 100, stop - 1, count - 1]))
sheet(phases, (88, 65, 580, 310), 4, 'face-reflection-phases.jpg')
for part, box, scale in [('eye', (330, 105, 430, 190), 3), ('reflection', (110, 120, 265, 290), 2)]:
    sheet([0, 16, 24, 32, 48, 60, 72, 96, 108], box, 3, part + '-detail.png', ((box[2]-box[0])*scale, (box[3]-box[1])*scale), Image.Resampling.NEAREST)
images[stop - 1].save(OUT / 'selected-end.jpg', quality=96)
hashes = {}
for path in [MEDIA, MEDIA.with_name('render.json'), FILM/'assets/her_window_refined_candidate.png', FILM/f'tools/kaggle-story23/provenance/{TAKE}-provenance.json']:
    hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
for ref in (ROOT/'productions/join-me-in-life/art/00_References').glob('A0[123]_*'):
    hashes[str(ref.relative_to(ROOT))] = hashlib.sha256(ref.read_bytes()).hexdigest()
(OUT / 'source-checks.json').write_text(json.dumps({'source_sha256': expected, 'width': 896, 'height': 512, 'frames': count, 'fps': 24, 'duration_seconds': count/24, 'audio_streams': 0, 'full_decode_passed': True, 'all_frames_extracted': count, 'selected_source_frames_zero_based': [3, stop], 'selected_source_seconds': [3/24, stop/24], 'selected_duration_seconds': (stop-3)/24, 'input_hashes': hashes, 'scope': 'Source identity, decoding and extraction checks only; visual verdict is separate.'}, indent=2) + '\n')
print(json.dumps({'take': TAKE, 'frames': len(images), 'output': str(OUT)}, indent=2))
