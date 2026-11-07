"""Independent L12 source evidence. No production input changes."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;FILM=HERE.parent.parent;ROOT=FILM.parents[2]
RAW=ROOT/'build/ltx23-dawn-L12-review';RAW.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'assets/motion/ltx23-dawn-pilots/L12/video-silent.mp4'
GUIDE=FILM/'assets/dawn_together_refined_v2_candidate.png'
SHA='c09a05840d6da33970a08e889f148679f9055cd18dff7aed5d67b68ab174e1f8'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==SHA
assert hashlib.sha256(GUIDE.read_bytes()).hexdigest()=='452839fce63dfdd7046fdcc07a0bf2af33f7357429042c024a9f0cf11a0b6eb5'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(VIDEO)]))
b=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(VIDEO),'-an','-f','rawvideo','-pix_fmt','rgb24','-'])
rgb=np.frombuffer(b,np.uint8).reshape(-1,512,896,3);assert len(rgb)==97
frames=[Image.fromarray(x) for x in rgb]
for n,im in enumerate(frames):im.save(RAW/f'frame-{n:03}.png')
def sheet(ns,path,cols=4,width=448,crop=None):
 base=frames[0].crop(crop) if crop else frames[0]
 height=round(base.height*width/base.width);rows=(len(ns)+cols-1)//cols
 im=Image.new('RGB',(cols*width,rows*(height+22)),'#181818');d=ImageDraw.Draw(im)
 for i,n in enumerate(ns):
  x,y=(i%cols)*width,(i//cols)*(height+22)
  d.text((x+4,y+4),f'zero-based f{n} / {n/24:.3f}s'+(' KEEP' if 3<=n<92 else ' handle'),fill='white')
  source=frames[n].crop(crop) if crop else frames[n]
  im.paste(source.resize((width,height),Image.Resampling.LANCZOS),(x,y+22))
 im.save(path,quality=90,subsampling=0)
for start in range(0,97,25):
 ns=list(range(start,min(start+25,97)))
 sheet(ns,RAW/f'all-{start:03}.jpg',cols=5)
 sheet(ns,RAW/f'faces-{start:03}.jpg',cols=5,width=490,crop=(270,90,515,215))
 sheet(ns,RAW/f'hands-{start:03}.jpg',cols=5,width=540,crop=(330,345,600,445))
sheet([0,3,12,24,36,48,60,72,84,91,96],HERE/'overview.jpg',cols=3)
sheet([3,12,24,36,48,60,72,84,91],HERE/'face-phases.jpg',cols=3,width=490,crop=(270,90,515,215))
sheet([3,12,24,36,48,60,72,84,91],HERE/'hand-phases.jpg',cols=3,width=540,crop=(330,345,600,445))
sheet([0,8,12,16,18,20,22,24,30,40,44,48,52,56,60],HERE/'arm-gesture.jpg',cols=3,width=450,crop=(150,150,600,430))
sheet(list(range(8,25)),RAW/'arm-onset-all.jpg',cols=4,width=450,crop=(150,150,600,430))
sheet(list(range(42,63)),RAW/'arm-return-all.jpg',cols=4,width=450,crop=(150,150,600,430))
summary={'source_path':str(VIDEO.relative_to(FILM)),'source_sha256':SHA,
 'guide_path':str(GUIDE.relative_to(FILM)),'guide_sha256':hashlib.sha256(GUIDE.read_bytes()).hexdigest(),
 'probe':probe,'decoded_frames':97,'full_decode_passed':True,
 'planned_zero_based_source_interval':[3,92],'planned_source_seconds':[.125,92/24],
 'planned_frames':89,'source_audio_streams':sum(x['codec_type']=='audio' for x in probe['streams']),
 'scope':'Source review only; exact editorial insertion/cuts not approved.'}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='probe'},indent=2))
