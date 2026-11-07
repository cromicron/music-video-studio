"""Retain compact source-review evidence; requires completed reproduce.py cache."""
from pathlib import Path
import hashlib,json,gzip,shutil,math
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
TAKE=HERE.name.split('-')[-2]
RAW=ROOT/'build'/HERE.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frames=np.load(RAW/'frames.npy',mmap_mode='r')
playback=json.loads((RAW/'playback.json').read_text())
checks=json.loads((RAW/'checks.json').read_text())
for path,expected in checks['hashes'].items():assert sha(ROOT/path)==expected
for run in playback['runs']:
 media=ROOT/f'productions/join-me-in-life/full-film/assets/motion/ltx23-positive-continuation/P1/{TAKE}/video-silent.mp4' if run['key']=='raw' else RAW/f"{run['key']}-selected.mp4"
 assert sha(media)==run['source_sha256']
 assert run['telemetry']['ended'] and run['telemetry']['playbackRate']==1
summary={**{k:v for k,v in playback.items() if k!='runs'},'raw_playback_sha256':sha(RAW/'playback.json'),'runs':[{**{k:v for k,v in run.items() if k!='telemetry'},'telemetry':{k:v for k,v in run['telemetry'].items() if k!='frameCallbacks'},'frame_callback_count':len(run['telemetry']['frameCallbacks'])} for run in playback['runs']]}
(HERE/'playback-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(HERE/'playback-full.json.gz').write_bytes(gzip.compress((RAW/'playback.json').read_bytes(),mtime=0))
for name in ['overview.jpg','guide-endpoints.jpg','checks.json']+[p.name for p in RAW.glob('captured-*.jpg')]:shutil.copyfile(RAW/name,HERE/name)
def sheet(name,ids,box,cols=3):
 w,h=box[2]-box[0],box[3]-box[1]
 out=Image.new('RGB',(cols*w,math.ceil(len(ids)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(out)
 for j,i in enumerate(ids):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+4,y+5),f'f{i+1:03} | {i/24:.3f}s | native pixels',fill='white');out.paste(Image.fromarray(frames[i]).crop(box),(x,y+24))
 out.save(HERE/name,quality=95)
if TAKE=='P1L06':
 ids=[0,24,48,72,92,101,102,110,120,144,168,192,197,208]
 sheet('gaze-eyelid-phases.jpg',[0,16,24,48,72,84,92,96,101,108,116,132,168,197,208],(245,10,610,300))
 sheet('her-eyelid-detail.jpg',[0,24,48,72,84,96,108,120,144,168,197,208],(260,135,395,240),4)
else:
 ids=[0,24,48,72,96,115,116,144,156,168,180,192,208,214,224]
 sheet('his-gaze-phases.jpg',[0,12,24,32,48,60,72,96,115,132,168,214],(410,15,620,280),4)
 sheet('her-returned-look.jpg',[136,140,143,144,148,152,156,160,168,180,188,192,200,208,214],(245,105,620,310))
 sheet('her-eyelid-detail.jpg',[0,24,48,72,96,115,143,152,168,188,192,208],(260,135,395,240),4)
sheet('contact-lap-phases.jpg',ids,(175,250,660,512))
print(TAKE,'source/proxy hashes verified; compact evidence retained.')
