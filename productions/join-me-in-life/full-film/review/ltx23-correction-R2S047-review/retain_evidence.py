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
 media=ROOT/f'productions/join-me-in-life/full-film/assets/motion/ltx23-positive-corrections/R2S/{TAKE}/video-silent.mp4' if run['key']=='raw' else RAW/f"{run['key']}-selected.mp4"
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
ids=[0,3,12,24,36,48,60,72,84,96,101,112]
sheet('gaze-phases.jpg',ids,(245,15,620,310))
sheet('her-eyelid-detail.jpg',ids,(250,120,395,245),4)
sheet('contact-lap-phases.jpg',ids,(175,250,660,512))
print(TAKE,'source/proxy hashes verified; compact evidence retained.')
