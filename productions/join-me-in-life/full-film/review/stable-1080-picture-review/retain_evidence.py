"""Retain compact final-size cache evidence, not raw frame/reconstruction caches."""
from pathlib import Path
import gzip,hashlib,json,shutil
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
SRC=ROOT/'build/stable-1080-picture-review'
shutil.copyfile(ROOT/'build/final-stable-shot-cache-prep.json',HERE/'cache-inventory.json')
for name in ['frozen-plan.json','cache-checks.json','interval-checks.json','resolved-geometry.json',
             'playback-summary.json','playback-retry-summary.json','branding-native.jpg',
             'drawn-mouth-detail-A.jpg','drawn-mouth-detail-B.jpg','drawn-eye-details.jpg']:
    shutil.copyfile(SRC/name,HERE/name)
for name in ['playback','playback-retry']:
    (HERE/f'{name}-full.json.gz').write_bytes(gzip.compress((SRC/f'{name}.json').read_bytes(),mtime=0))
for p in sorted(SRC.glob('overview-*.jpg')):
    with Image.open(p) as im:
        im.resize((960,im.height*960//im.width),Image.Resampling.LANCZOS).save(HERE/p.name,quality=89)
for sid in ['S025','S026','S028','S044','S046','S053']:
    with Image.open(SRC/sid/'phases.jpg') as im:
        im.resize((960,im.height*960//im.width),Image.Resampling.LANCZOS).save(HERE/f'{sid}-phases.jpg',quality=89)
for source,name in [('S003/f077.jpg','S003-native.jpg'),('S030/f049.jpg','held-native.jpg'),
                    ('S014-playback-3.73.jpg','S014-native-playback.jpg'),('S044-playback-1.69.jpg','S044-native-playback.jpg')]:
    shutil.copyfile(SRC/source,HERE/name)
files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='evidence-sha256.json')
(HERE/'evidence-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
