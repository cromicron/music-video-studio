"""Reproduce L13 review frames and contact sheets in ignored root build only."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/ltx23-dawn-L13-review';OUT.mkdir(parents=True,exist_ok=True)
FILM=ROOT/'productions/join-me-in-life/full-film'
MEDIA=FILM/'assets/motion/ltx23-dawn-pilots/L13/video-silent.mp4'
EXPECTED='eebdffb903eb5808313ef7e6bbbac42c337d8ea01e1c666bcde6ddbd23b93400'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest()==EXPECTED
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(MEDIA)]))
assert len(probe['streams'])==1
v=probe['streams'][0];assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames']))==(896,512,'24/1',153)
frames=OUT/'frames';frames.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(MEDIA),'-fps_mode','passthrough',str(frames/'f%03d.png')],check=True)
paths=sorted(frames.glob('f*.png'));assert len(paths)==153
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
sheet(range(0,153,12),(0,0,896,512),4,'overview.jpg',(448,256))
for first in range(0,153,16):
 indices=range(first,min(first+16,153))
 sheet(indices,(180,70,565,275),4,f'faces-{first+1:03d}-{min(first+16,153):03d}.jpg')
 sheet(indices,(275,340,645,510),4,f'hands-{first+1:03d}-{min(first+16,153):03d}.jpg')
 sheet(indices,(0,0,896,512),4,f'full-{first+1:03d}-{min(first+16,153):03d}.jpg',(448,256))
sheet([3,12,24,36,48,56,64,68],(180,70,565,275),4,'seated-face-phases.jpg')
sheet([3,12,24,36,48,56,64,68],(275,340,645,510),4,'seated-hand-phases.jpg')
sheet([68,76,84,96,104,112,120,128],(0,0,896,512),4,'failure-phases.jpg',(448,256))
(OUT/'source-checks.json').write_text(json.dumps({'source_sha256':EXPECTED,'width':896,'height':512,'frames':153,'fps':24,'duration_seconds':153/24,'audio_streams':0,'full_decode_passed':True,'all_frames_extracted':153,'selected_source_frames':[3,149],'selected_source_seconds':[3/24,149/24],'selected_duration_seconds':146/24,'raw_frames_location':'build/ltx23-dawn-L13-review/frames','crop_rectangles':{'seated_faces':[180,70,565,275],'hands':[275,340,645,510]},'scope':'Technical decoding and extraction, not motion acceptance.'},indent=2)+'\n')
print(json.dumps({'source':str(MEDIA),'frames':len(images),'output':str(OUT)},indent=2))
