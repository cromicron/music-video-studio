"""Supplement the actual-final sample set with native reflection and crop-edge details."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, subprocess, gzip
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
HERE=Path(__file__).resolve().parent
SELECTED=ROOT/'build/final-positive-1080-review/selected'
def make(name, frames, box):
    w,h=box[2]-box[0],box[3]-box[1]
    out=Image.new('RGB',(w,(h+24)*len(frames)),'#171717');d=ImageDraw.Draw(out)
    for j,n in enumerate(frames):
        d.text((4,j*(h+24)+4),f'Actual final frame {n}, native crop {box}',fill='white')
        out.paste(Image.open(SELECTED/f'f{n:04}.jpg').crop(box),(0,j*(h+24)+24))
    out.save(HERE/name,quality=94)
make('window-native-reflections.jpg',[1099,1171,1211,1694,1742,1794],(150,210,980,610))
make('S050-native-crown-edge.jpg',[5561,5582,5606,5630,5656],(900,0,1390,280))
src=ROOT/'productions/join-me-in-life/full-film/assets/motion/ltx23-positive-continuation/P1/P1L02/video-silent.mp4'
cmd=['ffmpeg','-hide_banner','-threads','1','-i',str(src),'-vf','scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=4:flags=lanczos,showinfo','-filter_threads','1','-frames:v','1','-an','-f','null','-']
p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
lines=[s for s in p.stderr.splitlines() if 'showinfo' in s and ' s:' in s]
assert lines and all('s:1892x1080' in s for s in lines)
(HERE/'contain-geometry.json').write_text(json.dumps({'scale_output':'1892x1080','padded_output':'1920x1080','left_and_right_pad_px':14,'input':'896x512','filter':cmd[cmd.index('-vf')+1],'ffmpeg_showinfo':lines},indent=2)+'\n')
data=json.loads(gzip.decompress((HERE/'full-frame-checks.json.gz').read_bytes()))
cadence={'scope':'All new-shot final decoded frame hashes; exact expected-source comparisons in full-frame-checks.json.gz','shots':[]}
for s in data['new']:
    hashes=s['final_frame_hashes']
    cadence['shots'].append({'id':s['id'],'frames':len(hashes),'distinct_decoded_frame_hashes':len(set(hashes)),'adjacent_duplicate_count':sum(a==b for a,b in zip(hashes,hashes[1:]))})
(HERE/'cadence.json').write_text(json.dumps(cadence,indent=2)+'\n')
