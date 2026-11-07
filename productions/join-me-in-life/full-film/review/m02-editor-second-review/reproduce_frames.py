"""Reproduce this review's JPEG evidence from its exact retained sources.

Requires ffmpeg, ffprobe and Pillow. Run from any directory. Outputs and numeric
checks go to ignored build/m02-editor-second-review/; archived review
artifacts and production sources remain unchanged. No generation API is used.
"""
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageChops, ImageDraw, ImageStat, ImageOps

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
OUT = ROOT / 'build/m02-editor-second-review'
ASSETS = ROOT / 'productions/join-me-in-life/current/assets'
SOURCE = ASSETS / 'M02_Summer.mp4'
R4 = ROOT / 'productions/join-me-in-life/current/exports/Join_Me_in_Life_Short_Hybrid_Camera.mp4'
HASHES = {
    'M02_Summer.mp4': '03d6eb4da452db9b21b3087edf97492d21517c215cf1c548bfe5a344d8fd70d3',
    'M02_Summer_Start.png': '5177ac4a2ea53edebd977976ac3ceefbad77118bc9d5f3e33a723f7fcde4900e',
    'M02_Summer_End.png': 'c7b84b689a90712c9fe10a30e374f2ecf0a78a5a044ef6aee6fb41a6592d4d75',
}


def decode(path, width, height, filters):
    command = ['ffmpeg', '-v', 'error', '-i', str(path), '-vf', filters,
               '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        while data := process.stdout.read(width * height * 3):
            if len(data) != width * height * 3:
                raise RuntimeError('Partial decoded RGB frame')
            yield Image.frombytes('RGB', (width, height), data)
        if process.wait():
            raise RuntimeError('FFmpeg decoding failed')


def sheet(entries, cols, rows, width, height, title_height, name, quality):
    canvas = Image.new('RGB', (cols * width, rows * (height + title_height)), '#161616')
    draw = ImageDraw.Draw(canvas)
    for j, (label, frame) in enumerate(entries):
        x, y = (j % cols) * width, (j // cols) * (height + title_height)
        canvas.paste(frame.resize((width, height)), (x, y + title_height))
        draw.text((x + 5, y + 5), label, fill='white')
    canvas.save(OUT / name, quality=quality)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, expected in HASHES.items():
        actual = hashlib.sha256((ASSETS / filename).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f'Source identity mismatch: {filename}')
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(SOURCE)]))
    frames = list(decode(SOURCE, 640, 360, 'scale=640:360'))
    if len(frames) != 121:
        raise RuntimeError(f'Expected 121 frames, found {len(frames)}')
    sheet([(f'frame {i+1:03} | source {i/24:.6f}s', frames[i]) for i in range(0, 121, 8)],
          4, 4, 640, 360, 28, 'overview.jpg', 90)
    for start in range(0, len(frames), 12):
        entries = [(f'f{i+1:03}  {i/24:.3f}s', frames[i])
                   for i in range(start, min(start + 12, len(frames)))]
        sheet(entries, 3, 4, 480, 270, 22,
              f'sequential-{start+1:03}-{min(start+12,len(frames)):03}.jpg', 92)
    details = [0, 12, 24, 36, 48, 60, 72, 96, 120]
    identity_ids = [0, 16, 18, 20, 24, 60, 72, 102, 120]
    hand_ids = [0, 48, 54, 60, 104, 120]
    selected = sorted(set(details + identity_ids + hand_ids))
    selection = '+'.join(f'eq(n\\,{i})' for i in selected)
    native = dict(zip(selected, decode(SOURCE, 1916, 1080, f'select={selection}'), strict=True))
    sheet([(f'f{i+1} {i/24:.6f}s | faces', native[i].crop((500, 80, 1340, 500)))
           for i in details], 3, 3, 840, 420, 26, 'face-detail.jpg', 94)
    sheet([(f'f{i+1} {i/24:.6f}s | hands/lap', native[i].crop((500, 700, 1330, 1030)))
           for i in hand_ids], 2, 3, 830, 330, 26, 'hand-contact-detail.jpg', 94)
    references = [
        ('A01 identity (expression may differ)', Image.open(ASSETS / 'A01_Approved_Character_Pair.jpg').convert('RGB').crop((870, 65, 1040, 265))),
        ('A02 identity; NOT summer mood', Image.open(ASSETS / 'A02_Approved_Anime_Window.png').convert('RGB').crop((200, 290, 550, 650))),
    ]
    entries = references + [(f'M02 f{i+1} | {i/24:.6f}s', native[i].crop((1010, 80, 1350, 440))) for i in identity_ids]
    comparison = Image.new('RGB', (360 * 4, 390 * 3), '#171717')
    draw = ImageDraw.Draw(comparison)
    for j, (label, frame) in enumerate(entries):
        x, y = (j % 4) * 360, (j // 4) * 390
        draw.text((x + 5, y + 5), label, fill='white')
        frame = ImageOps.contain(frame, (350, 360))
        comparison.paste(frame, (x + (360 - frame.width) // 2, y + 27))
    comparison.save(OUT / 'identity-comparison.jpg', quality=94)
    endpoints, metrics = [], []
    for index, label in [(0, 'Start'), (120, 'End')]:
        png = Image.open(ASSETS / f'M02_Summer_{label}.png').convert('RGB')
        diff = ImageChops.difference(native[index], png)
        metrics.append({'endpoint': label, 'frame': index + 1,
                        'exactRgbEqual': diff.getbbox() is None,
                        'meanAbsoluteRgbDifference': ImageStat.Stat(diff).mean})
        endpoints.extend([(label + ' PNG', png), (f'source f{index+1}', native[index])])
    sheet(endpoints, 2, 2, 960, 541, 27, 'endpoints.jpg', 92)
    joins = [491, 492, 493, 539, 540, 541, 611, 612, 613]
    selection = '+'.join(f'eq(n\\,{i})' for i in joins)
    join_frames = decode(R4, 405, 720, f'select={selection},scale=405:720')
    sheet([(f'R4 f{i+1} | {i/24:.6f}s', frame)
           for i, frame in zip(joins, join_frames, strict=True)],
          3, 3, 405, 720, 24, 'r4-joins.jpg', 92)
    (OUT / 'endpoints.json').write_text(json.dumps(metrics, indent=2) + '\n')
    (OUT / 'source.json').write_text(json.dumps({'sha256': HASHES, 'probe': probe,
        'r4Sha256': hashlib.sha256(R4.read_bytes()).hexdigest(), 'frameCount': len(frames),
        'referenceSha256': {name: hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in ['A01_Approved_Character_Pair.jpg', 'A02_Approved_Anime_Window.png', 'S13_Summer_Relaxed_Smiles.png']}}, indent=2) + '\n')
    print(f'Reproduced 17 JPEGs and source/endpoint checks in {OUT}')
