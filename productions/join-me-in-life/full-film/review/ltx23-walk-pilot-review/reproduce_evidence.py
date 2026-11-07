"""Reproduce raw frames/contact sheets under ignored root build; no source edits."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/ltx23-walk-pilot-review';OUT.mkdir(parents=True,exist_ok=True)
FILM=ROOT/'productions/join-me-in-life/full-film'
MEDIA=FILM/'assets/motion/ltx23-walk-pilot/video-silent.mp4'
EXPECTED='fd21e3d9d84a6f9b565e67d3bcd6aa142e7c1cefe2d48f68d13e6f5ebc120f21'
assert hashlib.sha256(MEDIA.read_bytes()).hexdigest()==EXPECTED
frames=OUT/'frames';frames.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(MEDIA)]))
assert len(probe['streams'])==1
v=probe['streams'][0];assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames']))==(896,512,'24/1',145)
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(MEDIA),'-fps_mode','passthrough',str(frames/'f%03d.png')],check=True)
paths=sorted(frames.glob('f*.png'));assert len(paths)==145
images=[Image.open(p).convert('RGB') for p in paths]
def sheet(indices, crop, cols, filename, resize=None, resample=Image.Resampling.LANCZOS):
 tiles=[]
 for i in indices:
  tile=images[i].crop(crop)
  if resize:tile=tile.resize(resize,resample)
  canvas=Image.new('RGB',(tile.width,tile.height+22),(20,20,20));canvas.paste(tile,(0,22))
  ImageDraw.Draw(canvas).text((5,4),f'f{i+1:03d} | {i/24:.3f}s',fill='white');tiles.append(canvas)
 w,h=tiles[0].size;result=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),(40,40,40))
 for n,tile in enumerate(tiles):result.paste(tile,((n%cols)*w,(n//cols)*h))
 result.save(OUT/filename,quality=92)
indices=list(range(0,145,12));sheet(indices,(0,0,896,512),4,'overview.jpg',(448,256))
for first in range(0,145,15):sheet(range(first,min(first+15,145)),(310,115,565,430),5,f'body-{first+1:03d}-{min(first+15,145):03d}.jpg')
for first in range(0,145,25):sheet(range(first,min(first+25,145)),(320,270,565,430),5,f'feet-{first+1:03d}-{min(first+25,145):03d}.jpg')
sheet([i-1 for i in [1,9,17,26,35,44,53,62,73,83,93,102,113,123,133,145]],(310,115,565,430),4,'gait-phases.jpg')
for name,first,crop in [('early',16,(365,360,435,412)),('middle',52,(408,350,463,397)),('late',130,(482,325,525,376))]:
 sheet(range(first,first+10),crop,5,f'plant-{name}.jpg',((crop[2]-crop[0])*3,(crop[3]-crop[1])*3),Image.Resampling.NEAREST)
for i in [0,3,24,48,72,96,120,134,144]:images[i].save(OUT/f'native-f{i+1:03d}.png')
(OUT/'source-checks.json').write_text(json.dumps({'source_sha256':EXPECTED,'width':896,'height':512,'frames':145,'fps':24,'duration_seconds':145/24,'audio_streams':0,'full_decode_passed':True,'all_frames_extracted':145,'proposed_source_frames':[3,135],'proposed_source_seconds':[3/24,135/24],'raw_frames_location':'build/ltx23-walk-pilot-review/frames','crop_rectangles':{'body':[310,115,565,430],'feet':[320,270,565,430]},'scope':'Technical decoding evidence, not gait acceptance.'},indent=2)+'\n')
print(json.dumps({'source':str(MEDIA),'frames':len(images),'output':str(OUT)},indent=2))
