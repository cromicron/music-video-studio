#!/usr/bin/env python3
"""Actual B06 derivation positives and forged-metadata/media rejection checks."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[3]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(output):
    assert not output.exists()
    builder = load('actual_B06_builder', BASE / 'tools/build_edit.py')
    crop = load('actual_B06_crop', BASE / 'tools/lossless_crop.py')
    work = REPO / 'build/performance-cut-B06-guard-check-v1'
    work.mkdir(parents=True, exist_ok=False)
    record_file = BASE / 'assets/motion/derived/B06-crop-v1.derivation.json'
    record = json.loads(record_file.read_text())
    render = BASE / 'assets/motion/instruments-a-v2/B06/render.json'
    source = {'kind': 'video', 'take_id': 'PINSTRUMENTS_A_B06_v2', **record['derived'],
              'generation': {'shot_id': 'B06', 'provider_plan_sha256': crop.PROVIDER_SHA,
                             'queue_id': 'PINSTRUMENTS_A', 'render_record': crop.RENDER,
                             'render_record_sha256': crop.sha(render)},
              'derivation': {'kind': crop.KIND, 'record': str(record_file.relative_to(crop.FULL_FILM)),
                             'record_sha256': crop.sha(record_file)},
              'review': {'status': 'pending', 'accepted_ranges': []}}
    plan = json.loads(crop.local(crop.PROVIDER).read_text())
    checks = []

    def valid(name, fn):
        value = fn()
        checks.append({'check': name, 'result': 'PASS', 'actual_result': value})

    def reject(name, fn, messages):
        try:
            fn()
        except ValueError as e:
            assert any(m in str(e) for m in messages), (name, str(e))
            checks.append({'check': name, 'result': 'REJECTED_AS_REQUIRED', 'actual_error': str(e)})
        else:
            raise AssertionError('Guard accepted invalid actual case: ' + name)

    def verify(s, gid='B06', digest=crop.PROVIDER_SHA):
        return builder.verify_new_take_origin(gid, s, plan, digest)

    def fixture(name, rec, src=None):
        f = work / (name + '.json')
        assert not f.exists()
        f.write_text(json.dumps(rec, indent=2) + '\n')
        s = copy.deepcopy(source if src is None else src)
        s['derivation']['record'] = os.path.relpath(f, crop.FULL_FILM)
        s['derivation']['record_sha256'] = crop.sha(f)
        return s

    old_file = 'productions/join-me-in-life/full-film/performance-cut/tools/build_edit.py'
    old = subprocess.run(['git', 'show', '43a8f9556ce33781f2bbb6409540c2092331a281:' + old_file],
                         capture_output=True, text=True, check=True).stdout
    new = (BASE / 'tools/build_edit.py').read_text()

    def body(text, name):
        n = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)
        return '\n'.join(text.splitlines()[n.body[0].lineno - 1:n.end_lineno])

    original_body, current_body = body(old, 'verify_new_take_origin'), body(new, 'verify_raw_take_origin')
    assert original_body == current_body
    checks.append({'check': 'Original raw validator body byte-identical', 'result': 'PASS',
                   'body_sha256': hashlib.sha256(current_body.encode()).hexdigest()})
    valid('Actual derived225frame/full-YUV recomputation', lambda: verify(source))
    ledger = json.loads((BASE / 'edit/bindings-v005.json').read_text())
    for take in ('O01', 'B05A'):
        src = ledger['sources'][ledger['take_sources'][take]]
        valid('Unchanged raw-origin path ' + take, lambda t=take, s=src: verify(s, t))
    reject('Derived exception cannot apply to another take', lambda: verify(source, 'B02'), ['only the frozen B06'])
    reject('Stale provider digest', lambda: verify(source, digest='0' * 64), ['only the frozen B06'])
    bad = copy.deepcopy(source); bad['derivation']['record_sha256'] = '0' * 64
    reject('Stale immutable derivation record', lambda: verify(bad), ['record SHA changed'])
    bad = copy.deepcopy(source); bad['derivation']['kind'] = 'unreviewed_transform'
    reject('Unknown derivation kind', lambda: verify(bad), ['Unknown crop derivation'])
    bad = copy.deepcopy(record); bad['parent']['sha256'] = '0' * 64
    candidate = fixture('wrong-parent', bad)
    reject('Forged/stale parent', lambda: verify(candidate), ['parent path/SHA'])
    bad = copy.deepcopy(record); bad['crop']['y'] = 22
    candidate = fixture('wrong-rectangle', bad)
    reject('Wrong even crop rectangle', lambda: verify(candidate), ['rectangle differs'])
    bad = copy.deepcopy(record); bad['actual_parent_render']['sha256'] = '0' * 64
    candidate = fixture('wrong-render-record', bad)
    reject('Stale actual render metadata', lambda: verify(candidate), ['parent render metadata changed'])
    bad = copy.deepcopy(source); bad['generation']['shot_id'] = 'B02'
    reject('Unchanged raw validator still rejects wrong generation ID', lambda: verify(bad), ['generation ID differs'])

    # Resign each fixture's metadata so stored hashes alone cannot explain rejection.
    # These own temporary binaries are removed; originals and real crop are untouched.
    active = []
    try:
        for i, (name, vf, expected) in enumerate([
            ('actual-wrong-crop', 'crop=824:468:2:44:exact=1', ['YUV pictures differ']),
            ('actual-reordered', crop.crop_filter() + ',reverse', ['YUV pictures differ']),
            ('actual-short-count', crop.crop_filter() + ',trim=end_frame=224', ['count/origin changed']),
            ('actual-changed-time', crop.crop_filter() + ',setpts=2*PTS', ['timing changed', 'format/rate changed']),
        ], 9001):
            target = crop.DERIVED / ('B06-crop-v' + str(i) + '.mkv')
            assert not target.exists(); active.append(target)
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-threads', '2', '-filter_threads', '1',
                   '-i', str(crop.local(crop.PARENT)), '-map', '0:v:0', '-vf', vf, '-an', '-c:v', 'ffv1',
                   '-level', '3', '-g', '1', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
                   '-enc_time_base', '1/24', '-threads', '2', str(target)]
            subprocess.run(cmd, check=True, capture_output=True)
            rec = copy.deepcopy(record)
            rec['derived'] = {'path': str(target.relative_to(crop.FULL_FILM)),
                              'sha256': crop.sha(target), 'bytes': target.stat().st_size}
            s = copy.deepcopy(source); s.update(rec['derived'])
            candidate = fixture(name, rec, s)
            reject(name + ' with updated declared file SHA', lambda: verify(candidate), expected)
            checks[-1]['fixture_binary'] = rec['derived']
            checks[-1]['command'] = cmd
            target.unlink(); active.remove(target)
    finally:
        for target in active:
            target.unlink(missing_ok=True)
    existing = json.loads((BASE / 'edit/edit-v006.json').read_text())
    shot = copy.deepcopy(next(s for s in existing['shots'] if s['id'] == 'B06_A'))
    existing['sources']['P_B06_DERIVATION_PENDING'] = source
    shot['source'] = {'id': 'P_B06_DERIVATION_PENDING', 'in_frame': 6, 'out_frame_exclusive': 102}
    reject('Technical crop cannot bypass accepted motion source gate',
           lambda: builder.editor.bind_sources(existing, [shot]), ['no accepted interval review'])
    pending = BASE / 'edit/pending-B06-crop-v1-source-definition.json'
    assert not pending.exists(); pending.write_text(json.dumps(source, indent=2) + '\n')
    result = {'schema': 'jml-performance-B06-actual-derivation-guard-check/v1',
              'status': 'ACTUAL_GUARDS_PASS_NOT_MOTION_ACCEPTANCE', 'checks': checks,
              'record': {'file': str(record_file), 'sha256': crop.sha(record_file)},
              'pending_source_definition': {'file': str(pending), 'sha256': crop.sha(pending)},
              'tools': [{'file': str(p), 'sha256': crop.sha(p)} for p in
                        (BASE / 'tools/build_edit.py', BASE / 'tools/lossless_crop.py')],
              'retained_strict_renderer_sha256': crop.sha(builder.ENGINE),
              'temporary_negative_binaries_removed': True,
              'limits': 'Actual technical provenance/crop equivalence and targeted rejection checks only. No B06 motion/root/source acceptance or edit binding; original sources/proofs/retained renderer unchanged.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checks': len(checks), 'status': result['status'], 'report': str(output)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args().output)
