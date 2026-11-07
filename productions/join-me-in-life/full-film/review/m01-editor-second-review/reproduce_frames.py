"""Reproduce this review's JPEG evidence from its exact retained sources.

Requires ffmpeg, ffprobe and Pillow. Run from any directory. Outputs and numeric
checks go to ignored build/m01-editor-second-review-reproduced/; archived review
artifacts and production sources remain unchanged. No generation API is used.
"""
from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageChops, ImageDraw, ImageStat

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'studio.json').is_file())
OUT = ROOT / 'build/m01-editor-second-review-reproduced'
ASSETS = ROOT / 'productions/join-me-in-life/current/assets'
SOURCE = ASSETS / 'M01_Embrace.mp4'
R4 = ROOT / 'productions/join-me-in-life/current/exports/Join_Me_in_Life_Short_Hybrid_Camera.mp4'
HASHES = {
    'M01_Embrace.mp4': 'bb6e21e887c5b86d815c1b2638896f2b2612471238d3dd2ee798b586418d5246',
    'M01_Embrace_Start.png': '259124c27ba71ae4785927457fda743f20a954e38b86ce19ce655866e408b64f',
    'M01_Embrace_End.png': '466bccb17c8862b61c6e84792d46bb6a0730c2222a7aa9d32d5316e90e9c0f10',
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
    details = [36, 40, 44, 48, 52, 56, 60, 66, 72]
    selected = sorted(set(details + [0, 120]))
    selection = '+'.join(f'eq(n\\,{i})' for i in selected)
    native = dict(zip(selected, decode(SOURCE, 1916, 1080, f'select={selection}'), strict=True))
    sheet([(f'f{i+1} {i/24:.6f}s | x0:950, y0:800', native[i].crop((0, 0, 950, 800)))
           for i in details], 3, 3, 570, 480, 26, 'reach-contact-detail.jpg', 94)
    endpoints, metrics = [], []
    for index, label in [(0, 'Start'), (120, 'End')]:
        png = Image.open(ASSETS / f'M01_Embrace_{label}.png').convert('RGB')
        diff = ImageChops.difference(native[index], png)
        metrics.append({'endpoint': label, 'frame': index + 1,
                        'exactRgbEqual': diff.getbbox() is None,
                        'meanAbsoluteRgbDifference': ImageStat.Stat(diff).mean})
        endpoints.extend([(label + ' PNG', png), (f'source f{index+1}', native[index])])
    sheet(endpoints, 2, 2, 960, 541, 27, 'endpoints.jpg', 92)
    joins = [815, 816, 817, 875, 876, 877, 935, 936, 937]
    selection = '+'.join(f'eq(n\\,{i})' for i in joins)
    join_frames = decode(R4, 405, 720, f'select={selection},scale=405:720')
    sheet([(f'R4 f{i+1} | {i/24:.6f}s', frame)
           for i, frame in zip(joins, join_frames, strict=True)],
          3, 3, 405, 720, 24, 'r4-joins.jpg', 92)
    (OUT / 'endpoints.json').write_text(json.dumps(metrics, indent=2) + '\n')
    (OUT / 'source.json').write_text(json.dumps({'sha256': HASHES, 'probe': probe,
        'r4Sha256': hashlib.sha256(R4.read_bytes()).hexdigest(), 'frameCount': len(frames)}, indent=2) + '\n')
    print(f'Reproduced 15 JPEGs and source/endpoint checks in {OUT}')
