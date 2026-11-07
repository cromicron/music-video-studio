#!/usr/bin/env python3
"""Preserve an exact film in fresh, hash-verified parts below Git's file limit."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--directory', required=True, type=Path)
    args = parser.parse_args()
    source = args.input.resolve()
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError('Input must be an existing, nonempty file')
    # Existing archives, including incomplete attempts, must never be replaced.
    args.directory.mkdir(parents=True, exist_ok=False)
    part_size = 48 * 1024 * 1024
    whole = hashlib.sha256()
    parts = []
    total = 0
    with source.open('rb') as stream:
        while data := stream.read(part_size):
            name = f'{source.name}.part{len(parts) + 1:03d}'
            with (args.directory / name).open('xb') as output:
                output.write(data)
            digest = hashlib.sha256(data).hexdigest()
            with (args.directory / name).open('rb') as saved:
                if hashlib.file_digest(saved, 'sha256').hexdigest() != digest:
                    raise ValueError(f'Written part failed verification: {name}')
            whole.update(data)
            total += len(data)
            parts.append({'name': name, 'bytes': len(data), 'sha256': digest})
    with source.open('rb') as original:
        if (source.stat().st_size != total or
                hashlib.file_digest(original, 'sha256').hexdigest() != whole.hexdigest()):
            raise ValueError('Source changed while archiving; incomplete directory retained')
    index = {
        'schema': 'jml-multipart-delivery/v1', 'filename': source.name,
        'bytes': total, 'sha256': whole.hexdigest(), 'part_size': part_size,
        'parts': parts,
        'purpose': 'Exact binary archive; no recompression or creative edit.'
    }
    with (args.directory / 'index.json').open('x') as output:
        output.write(json.dumps(index, indent=2) + '\n')
    print(json.dumps({'index': str((args.directory / 'index.json').resolve()),
                      'bytes': total, 'sha256': whole.hexdigest(), 'parts': len(parts)}))


if __name__ == '__main__':
    main()
