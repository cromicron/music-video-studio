#!/usr/bin/env python3
"""Extract exact cells from a generated2x2 atlas using the selected FFmpeg tool."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[5]


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--atlas', required=True, type=Path)
    ap.add_argument('--ids', required=True, nargs=4)
    ap.add_argument('--margin', type=int, default=5)
    ap.add_argument('--version', type=int, default=1)
    args = ap.parse_args()
    atlas = args.atlas.resolve()
    if not 0 <= args.margin <= 12 or len(set(args.ids)) != 4:
        raise ValueError('Require four unique cell IDs and bounded margin')
    with Image.open(atlas) as im:
        width, height = im.size
    outputs = []
    for index, name in enumerate(args.ids):
        if not name.replace('-', '').isalnum():
            raise ValueError('Invalid cell identifier')
        column, row = index % 2, index // 2
        x, y = column * (width // 2) + args.margin, row * (height // 2) + args.margin
        w, h = width // 2 - 2 * args.margin, height // 2 - 2 * args.margin
        target = atlas.parent / f'{name}-v{args.version}.png'
        if target.exists():
            raise ValueError(f'Preserve existing source: {target}')
        subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(atlas), '-vf',
                        f'crop={w}:{h}:{x}:{y}', '-frames:v', '1', str(target)], check=True)
        outputs.append({'file': str(target.relative_to(ROOT)), 'sha256': sha(target), 'source_rect': [x, y, w, h]})
    record = atlas.with_name(atlas.stem + '-extraction.json')
    with record.open('x') as stream:
        json.dump({'atlas': str(atlas.relative_to(ROOT)), 'atlas_sha256': sha(atlas),
                   'method': 'Exact fixed FFmpeg cell extraction; no redrawing or retouch',
                   'outputs': outputs}, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'outputs': len(outputs), 'record': str(record)}))


if __name__ == '__main__':
    main()
