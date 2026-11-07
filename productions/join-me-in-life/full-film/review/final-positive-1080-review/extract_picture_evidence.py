"""Stream selected actual-final RGB frames only; native crops are never upscaled."""
from pathlib import Path
import json,hashlib,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
HERE=Path(__file__).resolve().parent;OUT=ROOT/'build/final-positive-1080-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=ROOT/'build/Join_Me_in_Life_Full_Music_Video_QC.mp4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)=='ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09'
m=json.loads(VIDEO.with_suffix('.manifest.json').read_text());shots={s['id']:s for s in m['shots']}
indices={'S010':[0,24,48,72,96,112],'S015':[0,24,48,72,100],'S033':[0,21,45,69,95,98],'S034':[0,12,24,48,72,95],'S037':[0,21,45,69,93,122],'S041':[0,24,48,72,95],'S042':[0,24,48,72,97],'S043':[0,24,48,72,80,88,97],'S045':[0,24,48,72,96,112],'S047':[0,12,24,48,72,98],'S050':[0,21,45,69,95],'S051':[0,12,24,36,48,60,72,94],'S056':[0,24,48,72,96,120,145],'S058':[0,24,48,72,96,109,110,122,134,146,157]}
selected=set();cuts=set()
for sid,ids in indices.items():
 s=shots[sid];selected.update(s['start_frame']+i for i in ids)
 cuts.update([s['start_frame'],s['end_frame_exclusive']])
cuts=sorted(c for c in cuts if 0<c<6667)
for c in cuts:selected.update(range(c-2,c+2))
selected=sorted(selected)
def balanced(terms):
 if len(terms)==1:return terms[0]
 mid=len(terms)//2
 return '('+balanced(terms[:mid])+'+'+balanced(terms[mid:])+')'
filt='select='+balanced([f'eq(n\\,{i})' for i in selected])
cmd=['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-vf',filt,'-filter_threads','1','-fps_mode','passthrough','-an','-f','rawvideo','-pix_fmt','rgb24','-']
p=subprocess.Popen(cmd,stdout=subprocess.PIPE);folder=OUT/'selected';folder.mkdir(exist_ok=True)
size=1920*1080*3
for i in selected:
 raw=p.stdout.read(size);assert len(raw)==size,(i,len(raw))
 Image.fromarray(np.frombuffer(raw,np.uint8).reshape(1080,1920,3)).save(folder/f'f{i:04}.jpg',quality=96)
assert not p.stdout.read(1);assert p.wait()==0

def sheet(name,items,cols,cell):
 w,h=cell;im=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+26)),'#171717');d=ImageDraw.Draw(im)
 for j,(label,pic) in enumerate(items):
  x,y=j%cols*w,j//cols*(h+26);d.text((x+4,y+5),label,fill='white');pic=ImageOps.contain(pic,(w,h));im.paste(pic,(x+(w-pic.width)//2,y+26+(h-pic.height)//2))
 im.save(HERE/name,quality=94)
def frame(i):return Image.open(folder/f'f{i:04}.jpg')
for sid,ids in indices.items():
 s=shots[sid];sheet(sid+'-phases.jpg',[(f'{sid} local {i} | master {s["start_frame"]+i}',frame(s['start_frame']+i)) for i in ids],3,(640,360))
 # Two native 1080 frame regions for each major pose phase; coordinates measured from actual final picture.
 if sid in ['S010','S015']:boxes=[('face-crown',(600,0,1500,710))]
 elif sid in ['S050','S051']:boxes=[('faces-crown',(400,0,1450,690)),('hands-support',(370,690,1420,1080))]
 elif sid=='S037':boxes=[('faces',(430,0,1430,650)),('hands',(430,600,1430,1080))]
 elif sid in ['S056','S058']:boxes=[('faces',(500,100,1500,720)),('hands',(500,650,1500,1080))]
 else:boxes=[('faces-crown',(460,0,1360,650)),('contact-lap',(370,525,1410,1080))]
 detailids=[ids[0],ids[len(ids)//2],ids[-1]]
 if sid=='S058':detailids=[0,72,109,134,157]
 if sid=='S051':detailids=[0,24,48,72,94]
 for label,box in boxes:
  w,h=box[2]-box[0],box[3]-box[1]
  sheet(sid+'-native-'+label+'.jpg',[(f'{sid} local {i} | native 1080 crop',frame(s['start_frame']+i).crop(box)) for i in detailids],1,(w,h))
for c in cuts:
 before=next(s['id'] for s in m['shots'] if s['end_frame_exclusive']==c);after=next(s['id'] for s in m['shots'] if s['start_frame']==c)
 sheet(f'cut-{c:04}.jpg',[(f'{before}→{after} | master {i}',frame(i)) for i in range(c-2,c+2)],2,(960,540))
 # Exact adjacent boundary pictures retain a large native actor crop, never a 540 proof.
 box=(350,0,1550,1080)
 if c in [3820,3919,4793,4891,5657]:sheet(f'cut-{c:04}-native.jpg',[(f'{before}→{after} | master {i} | native crop',frame(i).crop(box)) for i in [c-1,c]],2,(1200,1080))
# Source S058 stays moving underneath the fade; sample RGB means only document final visibility.
fade=[]
for i in indices['S058']:
 a=np.asarray(frame(shots['S058']['start_frame']+i))
 fade.append({'local_frame':i,'master_frame':shots['S058']['start_frame']+i,'jpeg_rgb_mean':float(a.mean()),'jpeg_rgb_max':int(a.max())})
(HERE/'picture-samples.json').write_text(json.dumps({'output_sha256':sha(VIDEO),'scope':'Actual final export selected frames and unscaled native crops; no full-film raw dump or playback claim.','selected_global_frames':selected,'shot_local_indices':indices,'cut_boundaries':cuts,'selected_count':len(selected),'S058_final_picture_samples':fade},indent=2)+'\n')
print('Actual final samples:',len(selected),'; cuts:',len(cuts),flush=True)
