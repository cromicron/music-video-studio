"""Independent quiet waiting source evidence; no production input changes."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;FILM=HERE.parent.parent;ROOT=FILM.parents[2]
RAW=ROOT/'build/ltx23-correction-R1L04-review';RAW.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'assets/motion/ltx23-quiet-corrections/R1W/R1L04/video-silent.mp4'
GUIDE=FILM.parent/'art/03_Story/S02_Waiting_Closeup.png'
SHA='664552573bc9da7d8c4da90bbf9978f80c3eb45435be4d3336ffb03270d51e51'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==SHA
assert hashlib.sha256(GUIDE.read_bytes()).hexdigest()=='cec0dfff1f9f64eaf2dc722c18615125e9d21f581b74301a49a0f5573cbb34df'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(VIDEO)]))
b=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(VIDEO),'-an','-f','rawvideo','-pix_fmt','rgb24','-'])
rgb=np.frombuffer(b,np.uint8).reshape(-1,512,896,3);assert len(rgb)==145
frames=[Image.fromarray(x) for x in rgb]

def sheet(ns,path,cols=4,width=448,crop=None):
 base=frames[0].crop(crop) if crop else frames[0]
 height=round(base.height*width/base.width);rows=(len(ns)+cols-1)//cols
 im=Image.new('RGB',(cols*width,rows*(height+22)),'#181818');d=ImageDraw.Draw(im)
 for i,n in enumerate(ns):
  x,y=(i%cols)*width,(i//cols)*(height+22)
  d.text((x+4,y+4),f'zero-based f{n} / {n/24:.3f}s'+(' KEEP' if 3<=n<135 else ' handle'),fill='white')
  source=frames[n].crop(crop) if crop else frames[n]
  im.paste(source.resize((width,height),Image.Resampling.LANCZOS),(x,y+22))
 im.save(path,quality=88,subsampling=0)
for start in range(0,145,30):
 sheet(list(range(start,min(start+30,145))),RAW/f'all-{start:03}.jpg',cols=5)
sheet(list(range(0,145,6)),HERE/'overview.jpg',cols=5)
sheet([3,12,24,36,48,60,72,84,96,108,120,132,134,144],HERE/'native-phases.jpg',cols=2,width=896)
sheet([3,12,24,36,48,60,72,84,96,108,120,134,144],HERE/'face-phases.jpg',cols=3,width=600,crop=(140,65,740,285))
for start in range(0,145,30):
 sheet(list(range(start,min(start+30,145))),RAW/f'faces-{start:03}.jpg',cols=5,width=600,crop=(140,65,740,285))
 sheet(list(range(start,min(start+30,145))),RAW/f'arms-{start:03}.jpg',cols=5,width=600,crop=(140,280,740,512))
for n,im in enumerate(frames):im.save(RAW/f'frame-{n:03}.png',compress_level=1)
summary={'source_path':str(VIDEO.relative_to(FILM)),'source_sha256':SHA,
 'guide_path':str(GUIDE.relative_to(FILM.parent)),'guide_sha256':hashlib.sha256(GUIDE.read_bytes()).hexdigest(),
 'probe':probe,'decoded_frames':len(frames),'full_decode_passed':True,
 'planned_zero_based_source_interval':[3,135],'planned_source_seconds':[.125,5.625],
 'planned_frames':132,'source_audio_streams':sum(x['codec_type']=='audio' for x in probe['streams']),
 'scope':'Source review only; exact later editorial insertion is not approved.'}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='probe'},indent=2))
