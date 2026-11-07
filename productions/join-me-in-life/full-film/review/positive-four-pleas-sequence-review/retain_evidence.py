"""Retain compact cut/phase/playback evidence without raw-video dumps."""
from pathlib import Path
import gzip, hashlib, json, shutil
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
RAW=ROOT/'build/positive-four-pleas-sequence-review'
names=['encoded-checks.json','ffprobe.json','playback-summary.json','lead-phases.jpg','four-pleas-phases.jpg','native-715.jpg']
names += [f'join-{c:03}-native.jpg' for c in [99,195,293,391,472,585,667,766]]
names += [f'four-pleas-playback-{t:.2f}.jpg' for t in [7.9,8.35,18.3,22,26,29.6,32.2]]
for name in names:shutil.copyfile(RAW/name,HERE/name)
captures=json.loads((RAW/'playback-summary.json').read_text())['runs'][0]['captures']
im=Image.new('RGB',(1920,((len(captures)+3)//4)*294),'#171717');d=ImageDraw.Draw(im)
for j,c in enumerate(captures):
    x,y=j%4*480,j//4*294
    d.text((x+4,y+4),f"target {c['target']:.2f}s; captured {c['before']['time']:.3f}-{c['after']['time']:.3f}s",fill='white')
    with Image.open(RAW/c['file']) as f:im.paste(f.resize((480,270),Image.Resampling.LANCZOS),(x,y+24))
im.save(HERE/'playback-captures.jpg',quality=92)
(HERE/'playback.json.gz').write_bytes(gzip.compress((RAW/'playback.json').read_bytes(),mtime=0))
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='evidence-sha256.json']
(HERE/'evidence-sha256.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':sum(f['bytes'] for f in files),
    'inventory_sha256':hashlib.sha256((HERE/'evidence-sha256.json').read_bytes()).hexdigest()},indent=2))
