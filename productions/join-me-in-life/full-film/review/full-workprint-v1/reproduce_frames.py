"""Hash-bound first/middle/last and join evidence; no production files changed."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
REPO=FILM.parents[2]
VIDEO=FILM/'exports/Join_Me_in_Life_Full_Hybrid_Workprint_v1.mp4'
EXPECTED='f5f43c7adfae9a7820c873a69c86564ad0123b2eba86e353c824b4b764dbd5fc'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==EXPECTED
manifest=json.loads(VIDEO.with_suffix('.manifest.json').read_text())
RAW=REPO/'build/full-workprint-v1-review/frames'
RAW.mkdir(parents=True,exist_ok=True)
shots=manifest['shots'];selected=set()
for s in shots:
    a,b=s['start_frame'],s['end_frame_exclusive']
    selected.update([a,(a+b-1)//2,b-1])
# Internal proven-action joins, original P02->P01 edit, and last visible fade.
selected.update([2899,2900,2901,2947,2948,2949,3224,3225,3345,3346,3494,3495,6618,6619,6631,6655,6666])
selected=sorted(selected)
expressions=[f'eq(n\\,{n})' for n in selected]
while len(expressions)>1:
    expressions=['('+ '+'.join(expressions[i:i+2])+')' for i in range(0,len(expressions),2)]
vf='select='+expressions[0]
p=subprocess.Popen(['ffmpeg','-v','error','-i',str(VIDEO),'-an','-vf',vf,'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
for n in selected:
    data=p.stdout.read(960*540*3)
    assert len(data)==960*540*3
    Image.frombytes('RGB',(960,540),data).save(RAW/f'{n:06}.jpg',quality=94,subsampling=0)
assert not p.stdout.read(1) and p.wait()==0
for start in range(0,len(shots),6):
    group=shots[start:start+6]
    sheet=Image.new('RGB',(1440,len(group)*290),'#181818');draw=ImageDraw.Draw(sheet)
    for row,s in enumerate(group):
        a,b=s['start_frame'],s['end_frame_exclusive']
        for col,(label,n) in enumerate(zip(['first','middle','last'],[a,(a+b-1)//2,b-1])):
            x,y=col*480,row*290
            draw.text((x+4,y+4),f'{s["id"]} {label} f{n} / {n/24:.3f}s',fill='white')
            sheet.paste(Image.open(RAW/f'{n:06}.jpg').resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
    sheet.save(HERE/f'chronology-{start//6+1:02}.jpg',quality=84,subsampling=0)
record={'video_sha256':EXPECTED,'edit_config':manifest['edit_config'],'raw_frames_directory':str(RAW.relative_to(REPO)),
        'selected_frame_count':len(selected),'selected_frames':selected,'frame_numbering':'zero-based at24fps',
        'chronology_sheet_order':'each shot first, floor((first+last)/2), last; six chronological shot rows per sheet',
        'shots':[{'id':s['id'],'start':s['start_frame'],'end_exclusive':s['end_frame_exclusive'],'source':s['source_key']} for s in shots]}
(HERE/'frame-evidence.json').write_text(json.dumps(record,indent=2)+'\n')
for a,b,label,name in [
    (899,900,'Continuous room camera','room-continuous-seam'),
    (2272,2273,'Waiting camera reset','waiting-reset'),
    (4792,4793,'Aftermath small punch in','aftermath-small-punch-in'),
    (4890,4891,'Aftermath small pull out','aftermath-small-pull-out'),
    (5656,5657,'Continuous indoor-dawn camera','dawn-continuous-seam')]:
    sheet=Image.new('RGB',(1920,570),'#181818');draw=ImageDraw.Draw(sheet)
    for col,n in enumerate([a,b]):
        draw.text((col*960+8,7),f'{label} | f{n} / {n/24:.6f}s',fill='white')
        sheet.paste(Image.open(RAW/f'{n:06}.jpg'),(col*960,30))
    sheet.save(HERE/f'{name}.jpg',quality=89,subsampling=0)
for n in [2272,2948,2949,3494,3495,4988,4989,5069,5070,5264,5265,5363,5364,5751,5752,5841,5842]:
    Image.open(RAW/f'{n:06}.jpg').save(HERE/f'frame-{n:06}.jpg',quality=88,subsampling=0)
nums=[2899,2900,2901,3224,3225,3345,3346,6618,6619,6631,6655,6666]
sheet=Image.new('RGB',(1440,4*290),'#181818');draw=ImageDraw.Draw(sheet)
for i,n in enumerate(nums):
    x,y=(i%3)*480,(i//3)*290
    draw.text((x+4,y+4),f'f{n} / {n/24:.6f}s',fill='white')
    sheet.paste(Image.open(RAW/f'{n:06}.jpg').resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
sheet.save(HERE/'internal-joins-and-final-fade.jpg',quality=85,subsampling=0)
print(json.dumps({'selected_frames':len(selected),'sheets':(len(shots)+5)//6,'raw_frames':str(RAW)}))
