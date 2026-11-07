"""Reproduce L01 review frames and contact sheets in ignored root build only."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/ltx23-quiet-L01-review';OUT.mkdir(parents=True,exist_ok=True)
FILM=ROOT/'productions/join-me-in-life/full-film'
MEDIA=FILM/'assets/motion/ltx23-quiet-pilots/L01/video-silent.mp4'
EXPECTED='e90f0c8b2ed56367fe04399109dc7a95a030aacc56e158964a46bac610ef743a'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest()==EXPECTED
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(MEDIA)]))
assert len(probe['streams'])==1
v=probe['streams'][0];assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames']))==(896,512,'24/1',161)
frames=OUT/'frames';frames.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(MEDIA),'-fps_mode','passthrough',str(frames/'f%03d.png')],check=True)
paths=sorted(frames.glob('f*.png'));assert len(paths)==161
images=[Image.open(p).convert('RGB') for p in paths]
def sheet(indices,crop,cols,filename,resize=None,resample=Image.Resampling.LANCZOS):
 tiles=[]
 for i in indices:
  tile=images[i].crop(crop)
  if resize:tile=tile.resize(resize,resample)
  canvas=Image.new('RGB',(tile.width,tile.height+22),(20,20,20));canvas.paste(tile,(0,22))
  ImageDraw.Draw(canvas).text((5,4),f'f{i+1:03d} | {i/24:.3f}s',fill='white');tiles.append(canvas)
 w,h=tiles[0].size;result=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),(40,40,40))
 for n,tile in enumerate(tiles):result.paste(tile,((n%cols)*w,(n//cols)*h))
 result.save(OUT/filename,quality=91)
sheet(range(0,161,16),(0,0,896,512),3,'overview.jpg',(448,256))
for first in range(0,161,16):
 indices=range(first,min(first+16,161))
 sheet(indices,(88,70,560,300),4,f'faces-{first+1:03d}-{min(first+16,161):03d}.jpg')
 sheet(indices,(0,0,896,512),4,f'full-{first+1:03d}-{min(first+16,161):03d}.jpg',(448,256))
sheet([0,16,24,32,40,48,64,80,88,96,104,112,128,144,156,160],(88,70,560,300),4,'face-reflection-phases.jpg')
sheet([0,32,48,80,112,156],(250,0,770,508),3,'head-torso-phases.jpg')
sheet([0,16,32,48,64,88,112,128],(96,130,271,280),4,'reflection-detail.jpg',(350,300),Image.Resampling.NEAREST)
(OUT/'source-checks.json').write_text(json.dumps({'source_sha256':EXPECTED,'width':896,'height':512,'frames':161,'fps':24,'duration_seconds':161/24,'audio_streams':0,'full_decode_passed':True,'all_frames_extracted':161,'selected_source_frames':[3,157],'selected_source_seconds':[3/24,157/24],'selected_duration_seconds':154/24,'raw_frames_location':'build/ltx23-quiet-L01-review/frames','crop_rectangles':{'faces_and_reflection':[88,70,560,300],'head_and_torso':[250,0,770,508]},'scope':'Technical decoding and extraction, not motion acceptance.'},indent=2)+'\n')
print(json.dumps({'source':str(MEDIA),'frames':len(images),'output':str(OUT)},indent=2))
