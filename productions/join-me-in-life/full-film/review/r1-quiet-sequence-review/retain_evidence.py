"""Retain compact, hash-listed evidence from the completed ignored review run."""
from pathlib import Path
import gzip, hashlib, json, shutil
from PIL import Image, ImageDraw

DEST = Path(__file__).resolve().parent
ROOT = next(p for p in DEST.parents if (p/'studio.json').is_file())
SRC = ROOT/'build/r1-quiet-sequence-review'
for name in ['encoded-checks.json', 'playback-summary.json',
             'waiting-context-overview.jpg', 'held-context-overview.jpg',
             'waiting-encoded-phases.jpg', 'held30-encoded-phases.jpg',
             'held32-encoded-phases.jpg']:
    shutil.copyfile(SRC/name, DEST/name)
(DEST/'playback-full.json.gz').write_bytes(gzip.compress((SRC/'playback.json').read_bytes(), mtime=0))

def pairs(name, entries, width=960):
    height = width*540//960
    canvas = Image.new('RGB', (width*2, len(entries)*(height+26)), '#171717')
    draw = ImageDraw.Draw(canvas)
    for row, pair in enumerate(entries):
        for col, (file, label) in enumerate(pair):
            x, y = col*width, row*(height+26)
            draw.text((x+5,y+6), label, fill='white')
            with Image.open(SRC/file) as im:
                canvas.paste(im.resize((width,height), Image.Resampling.LANCZOS), (x,y+26))
    canvas.save(DEST/name, quality=94)

pairs('outgoing-joins-native.jpg', [
    [('waiting-context-native-278.jpg','S019 last: master f2272 / local f278'),
     ('waiting-context-native-279.jpg','S020 first: master f2273 / local f279')],
    [('held-context-native-395.jpg','S032 last: master f3819 / local f395'),
     ('held-context-native-396.jpg','S033 first: master f3820 / local f396')],
])
pairs('other-joins-and-held-continuity.jpg', [
    [('waiting-context-native-146.jpg','S018 last / waiting local f146'),
     ('waiting-context-native-147.jpg','S019 first / waiting local f147')],
    [('held-context-native-101.jpg','S029 last / held local f101'),
     ('held-context-native-102.jpg','S030 first / held local f102')],
    [('held-context-native-199.jpg','S030 last / held local f199'),
     ('held-context-native-200.jpg','S031 first / held local f200')],
    [('held-context-native-299.jpg','S031 last / held local f299'),
     ('held-context-native-300.jpg','S032 first / held local f300')],
    [('held-context-native-199.jpg','S030 last = source f100'),
     ('held-context-native-300.jpg','S032 first = source f101')],
], width=480)

files = sorted(p for p in DEST.iterdir() if p.is_file() and p.name != 'evidence-sha256.json')
(DEST/'evidence-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, indent=2)+'\n')
