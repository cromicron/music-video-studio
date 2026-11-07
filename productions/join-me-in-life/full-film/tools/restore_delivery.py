#!/usr/bin/env python3
"""Reassemble the exact completed film from its hash-verified Git archive parts."""
import argparse
import hashlib
import json
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'exports/archive'


def chunks(path):
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            yield data


def file_hash(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=ROOT/'exports/Join_Me_in_Life_Full_Music_Video.mp4')
    ap.add_argument('--check', action='store_true', help='Verify all parts and combined hash without writing')
    args = ap.parse_args()
    index = json.loads((ARCHIVE/'index.json').read_text())
    combined, count, paths = hashlib.sha256(), 0, []
    for part in index['parts']:
        path = (ARCHIVE/part['name']).resolve()
        if path.parent != ARCHIVE.resolve():
            raise ValueError('Archive part must stay inside its directory')
        if path.stat().st_size != part['bytes'] or file_hash(path) != part['sha256']:
            raise ValueError(f'Archive part mismatch: {part["name"]}')
        for data in chunks(path):
            combined.update(data)
            count += len(data)
        paths.append(path)
    if count != index['bytes'] or combined.hexdigest() != index['sha256']:
        raise ValueError('Combined film hash/size mismatch')
    if not args.check:
        output = args.output.resolve()
        if output.exists():
            if file_hash(output) != index['sha256']:
                raise ValueError('Existing output differs; preserve it and choose a new --output')
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_name(output.name+'.tmp')
            with temporary.open('xb') as stream:
                for path in paths:
                    for data in chunks(path):
                        stream.write(data)
            if file_hash(temporary) != index['sha256']:
                raise ValueError('Reassembly hash mismatch; output was not replaced')
            os.replace(temporary, output)
    print(json.dumps({'sha256': index['sha256'], 'bytes': count, 'parts': len(paths),
                      'verified': True, 'output': None if args.check else str(args.output.resolve())}))


if __name__ == '__main__':
    main()
