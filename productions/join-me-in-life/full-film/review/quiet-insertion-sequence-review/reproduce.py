"""Independent encoded-picture/cut evidence, writes only ignored root build/."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/quiet-insertion-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
PREFIX=ROOT/'productions/join-me-in-life/full-film'
SPECS=[('arrival','Arrival_Contain',149,'8c772116797166ac5a7c1e2d43cc6438f55916c17244bb5733ab5ad3d0fc8fc8'),('arrival-context','Arrival_Chorus_Context',451,'eede37caeb2f083b7decd6fed8297d3228383ed39162c328c5d97ef721efa698'),('held','Held_Contact_S030',98,'daf445b7c5108c0ba718b31a944e7f7806e3d338c17a033130aa04a1b5d41b13'),('held-context','Held_Contact_Context',396,'f3874cfaf2116ae66f8fec4cf5b65881657d591cfb38772e1ab067da4c317230')]
allchecks={};hashes={}
def sheet(frames,name,indices,cols=4,scale=(320,180)):
 w,h=scale;c=Image.new('RGB',(cols*w,((len(indices)+cols-1)//cols)*(h+24)),'#171717');d=ImageDraw.Draw(c)
 for j,f in enumerate(indices):
  x,y=j%cols*w,j//cols*(h+24);c.paste(Image.fromarray(frames[f]).resize(scale,Image.Resampling.LANCZOS),(x,y+24));d.text((x+4,y+5),f'{name} f{f:03d} | {f/24:.3f}s',fill='white')
 c.save(OUT/(name+'.jpg'),quality=86)
for label,name,n,sha in SPECS:
 path=PREFIX/f'exports/Join_Me_in_Life_{name}_Proof.mp4'
 assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-f','rawvideo','-pix_fmt','rgb24','-'])
 frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,540,960,3);assert len(frames)==n
 hashes[label]=[hashlib.sha256(f.tobytes()).hexdigest() for f in frames]
 allchecks[label]={'path':str(path.relative_to(ROOT)),'sha256':sha,'frames':n,'probe':probe}
 if 'context' in label:
  cuts=[103,252,350] if label=='arrival-context' else [71,102,200,300]
  indices=sorted(set([0,n-1]+[f for c in cuts for f in [c-3,c-2,c-1,c,c+1,c+2,c+12]]))
  sheet(frames,label+'-cuts',indices,cols=4,scale=(480,270))
  sheet(frames,label+'-overview',list(range(0,n,18))+[n-1],cols=4,scale=(480,270))
  for f in sorted(set([0,n-1]+[x for c in cuts for x in [c-1,c,c+1]])):
   Image.fromarray(frames[f]).save(OUT/f'{label}-native-{f:03d}.jpg',quality=90)
 else:
  for a in range(0,n,20):sheet(frames,f'{label}-all-{a:03d}-{min(a+19,n-1):03d}',list(range(a,min(a+20,n))))
  for f in ([0,30,70,93,120,148] if label=='arrival' else [0,20,40,58,68,80,97]):
   Image.fromarray(frames[f]).save(OUT/f'{label}-native-{f:03d}.jpg',quality=90)
  # Mean column luminance avoids treating codec ringing as extra picture pixels.
  edges=[]
  for f in frames:
   active=np.where(f[20:520].mean(axis=(0,2))>8)[0];edges.append([int(active[0]),int(959-active[-1])])
  allchecks[label]['meanColumnPadWidths']=sorted(set(tuple(x) for x in edges))
  take,end=('A06',152) if label=='arrival' else ('L05',101)
  source=PREFIX/f'assets/motion/ltx23-quiet-pilots/{take}/video-silent.mp4'
  filt=f'trim=start_frame=3:end_frame={end},setpts=PTS-STARTPTS,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
  expected=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vf',filt,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape(-1,540,960,3)
  assert len(expected)==n
  errors=[float(np.abs(a.astype(np.float32)-b.astype(np.float32)).mean()) for a,b in zip(frames,expected)]
  thumbs=np.stack([np.asarray(Image.fromarray(f).resize((120,68)),dtype=np.float32) for f in expected])
  nearest=[int(np.argmin(((thumbs-np.asarray(Image.fromarray(f).resize((120,68)),dtype=np.float32))**2).mean(axis=(1,2,3)))) for f in frames]
  allchecks[label]['independentSourceComparison']={'path':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'filter':filt,'maxPerFrameMeanAbsoluteRGBError':max(errors),'sameIndexMeanAbsoluteRGBErrorPerFrame':errors,'nearestExpectedThumbnailFramePerEncodedFrame':nearest,'thumbnailNearestMatches':sum(a==b for a,b in enumerate(nearest)),'note':'Thumbnail nearest matching can be ambiguous for almost still adjacent frames after lossy encoding; it is not an exact frame-order certificate. Same-index full-picture error and the author exact encoded reconstruction are separate evidence.'}
  print(label,'same-index max RGB MAE',max(errors),'thumbnail same-index',sum(a==b for a,b in enumerate(nearest)),'/',n,flush=True)
  del expected,thumbs
 del frames,raw
allchecks['contextCorrespondence']={'arrival':hashes['arrival']==hashes['arrival-context'][103:252],'held':hashes['held']==hashes['held-context'][102:200]}
assert all(allchecks['contextCorrespondence'].values())
(OUT/'encoded-checks.json').write_text(json.dumps(allchecks,indent=2)+'\n')
print(json.dumps({k:v for k,v in allchecks.items() if k=='contextCorrespondence'},indent=2))
