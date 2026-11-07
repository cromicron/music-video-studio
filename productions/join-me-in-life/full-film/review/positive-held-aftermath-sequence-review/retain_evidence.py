"""Retain compact evidence only; source/build videos remain outside this folder."""
from pathlib import Path
import gzip, hashlib, json, shutil

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'studio.json').is_file())
RAW = ROOT/'build/positive-held-aftermath-sequence-review'
names = ['encoded-checks.json', 'ffprobe.json', 'pinned-manifest.json', 'playback-summary.json',
    'context-phases.jpg', 'native-241.jpg', 'native-314.jpg']
names += [f'join-{c:03}-native.jpg' for c in [100,196,295,391]]
names += [p.name for p in sorted(RAW.glob('held-aftermath-playback-*.jpg'))]
for name in names:
    shutil.copyfile(RAW/name, HERE/name)
config = ROOT/'build/positive-stage1-config.json'
assert hashlib.sha256(config.read_bytes()).hexdigest() == '8422bf9fb4849e02e1ead09148b4615538c4a3780d13161f4f598e94932f7bb6'
shutil.copyfile(config, HERE/'pinned-config.json')
(HERE/'playback.json.gz').write_bytes(gzip.compress((RAW/'playback.json').read_bytes(), mtime=0))
inventory = [{'path':p.name, 'bytes':p.stat().st_size, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'evidence-sha256.json']
(HERE/'evidence-sha256.json').write_text(json.dumps(inventory, indent=2)+'\n')
print(json.dumps({'files':len(inventory), 'bytes':sum(p['bytes'] for p in inventory),
    'inventory_sha256':hashlib.sha256((HERE/'evidence-sha256.json').read_bytes()).hexdigest()}, indent=2))
