"""Retain compact viewing aids and exact telemetry from the independently decoded film."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,gzip
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BUILD=ROOT/'build/final-full-film-review'
for name in ['checks.json','audio-check.json','playback-summary.json','playback-full.json.gz']:
    shutil.copy2(BUILD/name,HERE/name)
with gzip.open(HERE/'full-video.framemd5.gz','wb') as f:f.write((BUILD/'full-video.framemd5').read_bytes())
for pattern in ['chronology-*.jpg','embrace-0*.jpg','pleas-0*.jpg','branding-01.jpg','final-fade-01.jpg']:
    for path in sorted(BUILD.glob(pattern)):
        im=Image.open(path);im.thumbnail((1080,1000));im.save(HERE/path.name,quality=83)
for name in ['embrace-contact-native-02.jpg','held-contact-native-05.jpg','dawn-faces-native-05.jpg','cut-S020.jpg','cut-S021.jpg','cut-S033.jpg','cut-S042.jpg','cut-S052.jpg']:
    shutil.copy2(BUILD/name,HERE/name)
for begin in [0,12]:
    files=sorted(BUILD.glob('playback-*.jpg'))[begin:begin+12]
    im=Image.new('RGB',(1440,292*((len(files)+2)//3)),'#181818');draw=ImageDraw.Draw(im)
    for i,p in enumerate(files):
        tile=Image.open(p);tile.thumbnail((480,270));x=i%3*480;y=i//3*292
        im.paste(tile,(x,y+22));draw.text((x+4,y+4),p.name,fill='white')
    im.save(HERE/f'playback-captures-{begin//12+1:02d}.jpg',quality=88)
ids=[2747,2748,3494,3495,4989,5030,5069,5183,5224,5264]
for begin in [0,4,8]:
    chosen=ids[begin:begin+4];im=Image.new('RGB',(1560,422*((len(chosen)+1)//2)),'#181818');draw=ImageDraw.Draw(im)
    for i,n in enumerate(chosen):
        tile=Image.open(BUILD/f'native-{n:06d}.jpg').crop((160,20,940,420));x=i%2*780;y=i//2*422
        im.paste(tile,(x,y+22));draw.text((x+4,y+4),f'Native crop | f{n} | {n/24:.6f}s',fill='white')
    im.save(HERE/f'performance-native-{begin//4+1:02d}.jpg',quality=94)
print(sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()))
