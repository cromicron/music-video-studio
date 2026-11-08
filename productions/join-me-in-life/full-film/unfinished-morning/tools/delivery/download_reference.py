#!/usr/bin/env python3
"""Verify a connector-returned HTTPS file reference without printing its bearer URL.

Pass {"download_url": "..."} on stdin, never as a command-line argument.
Only use a freshly returned authenticated file_uri for the selected Drive file.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--expected-bytes', required=True, type=int)
    ap.add_argument('--expected-sha256', required=True)
    args = ap.parse_args()
    if not 0 < args.expected_bytes <= 500 * 1024 * 1024:
        ap.error('expected bytes must be within 1..500MiB')
    if not re.fullmatch('[0-9a-f]{64}', args.expected_sha256):
        ap.error('expected SHA256 must be lowercase hex')
    output = args.output.resolve()
    partial = output.with_name(output.name + '.part')
    if output.exists() or partial.exists():
        ap.error('output or temporary file already exists; use a new path')
    payload = json.loads(sys.stdin.readline(32768))
    url = payload.get('download_url')
    if not isinstance(url, str):
        raise ValueError('missing authenticated download_url')
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('expected HTTPS file reference without userinfo')
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with partial.open('xb') as stream:
            created = True
            os.chmod(partial, 0o600)
            with urllib.request.urlopen(url, timeout=60) as response:
                if response.status != 200 or urllib.parse.urlsplit(response.url).scheme != 'https':
                    raise ValueError('unexpected response status or protocol')
                hasher = hashlib.sha256()
                size = 0
                while chunk := response.read(1024 * 1024):
                    size += len(chunk)
                    if size > args.expected_bytes:
                        raise ValueError('download exceeds expected size')
                    hasher.update(chunk)
                    stream.write(chunk)
            stream.flush()
            os.fsync(stream.fileno())
        actual = hasher.hexdigest()
        if size != args.expected_bytes or actual != args.expected_sha256:
            raise ValueError('download size or hash mismatch')
        # Atomic publication without replacing an existing destination.
        os.link(partial, output)
        partial.unlink()
        print(json.dumps({'output': str(output), 'bytes': size, 'sha256': actual,
                          'matches_expected': True, 'url_retained': False}))
    finally:
        if created and partial.exists():
            partial.unlink()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Some network exceptions include signed URLs; expose only their class.
        print(json.dumps({'verified': False, 'error_class': type(exc).__name__}), file=sys.stderr)
        sys.exit(1)
