"""Build retained native detail sheets and record resolved FFmpeg geometry."""
from pathlib import Path
import json,re,subprocess
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/stable-1080-picture-review'
im=Image.new('RGB',(1460,752),'#171717');d=ImageDraw.Draw(im)
for j,n in enumerate([0,24,112,116]):
    x,y=j%2*730,j//2*376;d.text((x+5,y+5),f'S001 native branding f{n} / {n/24:.3f}s',fill='white')
    im.paste(Image.open(OUT/'S001'/f'f{n:03}.jpg').crop((900,30,1630,380)),(x,y+26))
im.save(OUT/'branding-native.jpg',quality=96)
groups=[('drawn-mouth-detail-A.jpg',[('S023',n,(500,0,1100,600)) for n in [0,5,87]]+[('S027',n,(500,0,1100,600)) for n in [0,20,25]]),
        ('drawn-mouth-detail-B.jpg',[('S029',n,(250,0,850,600)) for n in [0,7,12]]+[('S029',n,(500,0,1100,600)) for n in [76,87,101]])]
for name,rows in groups:
    im=Image.new('RGB',(1800,1252),'#171717');d=ImageDraw.Draw(im)
    for j,(sid,n,box) in enumerate(rows):
        x,y=j%3*600,j//3*626;d.text((x+5,y+6),f'{sid} f{n} native crop',fill='white')
        im.paste(Image.open(OUT/sid/f'f{n:03}.jpg').crop(box),(x,y+26))
    im.save(OUT/name,quality=94)
im=Image.new('RGB',(1000,1578),'#171717');d=ImageDraw.Draw(im)
for row,sid in enumerate(['S016','S021','S024']):
    for col,(n,box) in enumerate([(46,(350,160,850,660)),(67,(950,50,1450,550))]):
        x,y=col*500,row*526;d.text((x+5,y+6),f'{sid} f{n} native eye crop',fill='white')
        im.paste(Image.open(OUT/sid/f'f{n:03}.jpg').crop(box),(x,y+26))
im.save(OUT/'drawn-eye-details.jpg',quality=94)
plan=json.loads((OUT/'frozen-plan.json').read_text())['shots'];geo={}
for sid,mode in [('S003','fill'),('S013','contain'),('S011','fill'),('S028','fill')]:
    s=next(s for s in plan if s['id']==sid);p=s['motion']['absolute_path']
    vf='scale=1920:1080:force_original_aspect_ratio='+('decrease:force_divisible_by=4' if mode=='contain' else 'increase')+':flags=lanczos'
    r=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-i',p,'-vf',vf+',showinfo','-frames:v','1','-f','null','-'],capture_output=True,text=True,check=True)
    line=next(l for l in r.stderr.splitlines() if ' n:' in l and ' s:' in l)
    dims=list(map(int,re.search(r' s:(\d+)x(\d+)',line).groups()))
    geo[sid]={'framing':mode,'scale_filter':vf,'resolved_scaled_dimensions':dims,'output':[1920,1080],'showinfo':line}
(OUT/'resolved-geometry.json').write_text(json.dumps(geo,indent=2)+'\n')
