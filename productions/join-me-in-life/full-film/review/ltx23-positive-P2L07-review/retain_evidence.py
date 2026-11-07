"""Retain exact-hash checks, compact native phases and actual playback evidence for both held sources.
Run after reproduce.py for each take. No generation, configuration changes or playback rerun.
"""
from pathlib import Path
import hashlib,json,shutil,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def sheet(items,cols,size,path):
 w,h=size;c=Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(c)
 for j,(label,im) in enumerate(items):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+5,y+5),label,fill='white');im=ImageOps.contain(im,size);c.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
 c.save(path,quality=95)
for take,ids in [('P2L07',[3,12,24,36,48,60,72,84,98,104]),('P2L08',[3,20,36,60,84,100,101,120,144,168,180,198,208])]:
 raw=ROOT/f'build/ltx23-positive-{take}-review';here=BASE/f'review/ltx23-positive-{take}-review';frames=np.load(raw/'frames.npy',mmap_mode='r');asset=BASE/f'assets/motion/ltx23-positive-continuation/P2/{take}';video=asset/'video-silent.mp4'
 checks=json.loads((raw/'checks.json').read_text());assert sha(video)==checks['hashes'][str(video.relative_to(ROOT))]
 render=json.loads((asset/'render.json').read_text());template=BASE/'tools/kaggle-story23/takes-template.json';manifest=next(x for x in json.loads(template.read_text()) if x['take_id']==take)
 assert manifest==render['manifest']
 prov=BASE/'tools/kaggle-story23/provenance'/manifest['source_provenance'];assert sha(prov)==manifest['source_provenance_sha256']
 provenance=json.loads(prov.read_text());assert provenance['source_sha256']==manifest['start_image_sha256'] and provenance['editorial']==manifest['editorial']
 checks['manifest_template_exact_object_match']=True;checks['source_provenance_hash_and_editorial_match']=True
 checks['hashes'][str(template.relative_to(ROOT))]=sha(template);checks['hashes'][str(prov.relative_to(ROOT))]=sha(prov)
 (raw/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
 for filename in ['playback.json','playback-capture-free.json']:
  path=raw/filename
  if not path.exists():continue
  data=json.loads(path.read_text())
  for run in data['runs']:
   media=video if run['key']=='raw' else raw/f"{run['key']}-selected.mp4"
   assert sha(media)==run['source_sha256'] and run['telemetry']['ended'] and run['telemetry']['playbackRate']==1
  data['raw_playback_sha256']=sha(path)
  for run in data['runs']:
   run['frame_callback_count']=len(run['telemetry'].pop('frameCallbacks'))
  (here/filename.replace('.json','-summary.json')).write_text(json.dumps(data,indent=2)+'\n')
 for name in ['checks.json','overview.jpg',*[p.name for p in raw.glob('captured-*.jpg')]]:shutil.copyfile(raw/name,here/name)
 source=BASE.parent/'current/assets/M01_Embrace_End.png'
 sheet([('Original M01 endpoint',Image.open(source)),('Fitted start/end guide',Image.open(asset/'start-fitted.png')),('Actual f001',Image.fromarray(frames[0])),(f'Actual f{len(frames):03}',Image.fromarray(frames[-1]))],2,(896,512),here/'guide-endpoints.jpg')
 for name,box in [('gaze-phases',(250,0,650,290)),('contact-phases',(180,210,300,350)),('lap-phases',(270,405,680,512))]:
  size=(box[2]-box[0],box[3]-box[1]);sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i]).crop(box)) for i in ids],4,size,here/f'{name}.jpg')
 if take=='P2L08':
  ids2=[172,175,178,180,182,184,186,188,190,192]
  sheet([(f'f{i+1:03} | {i/24:.3f}s',Image.fromarray(frames[i]).crop((270,130,400,250))) for i in ids2],5,(130,120),here/'eyelid-phases.jpg')
  a=np.load(ROOT/'build/ltx23-positive-P2L07-review/frames.npy',mmap_mode='r')
  sheet([(f'P2L07 f{i+1:03}',Image.fromarray(a[i])) for i in [96,97,98]]+[(f'P2L08 f{i+1:03}',Image.fromarray(frames[i])) for i in [3,4,5]],3,(896,512),here/'source-boundary.jpg')
  sheet([(f'S042 tail f{i+1:03}',Image.fromarray(frames[i])) for i in [99,100]]+[(f'S043 head f{i+1:03}',Image.fromarray(frames[i])) for i in [101,102]],2,(896,512),here/'continuous-boundary.jpg')
print('Both source hashes, playback hashes and compact evidence retained.')
