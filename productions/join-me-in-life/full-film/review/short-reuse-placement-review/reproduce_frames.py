"""Reproduce bounded placement-review evidence; no production files are changed.
Requires FFmpeg/ffprobe, Pillow, numpy. Outputs remain under ignored root build/.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess,numpy as np
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film'
OUT=ROOT/'build/short-reuse-placement-review'
FILES={
 'male':('Join_Me_in_Life_Male_Summer_Reuse_Proof.mp4','260966e365c3e21dd9242c82f3440477ac93fbdfbdb70de38be8c81aacf4d008',111,118.25),
 'later':('Join_Me_in_Life_Later_Short_Performance_Proof_v2.mp4','eb74629c7d7edd7018a9eddf7455568bd759f8fc5afe74fd7fcde99491e028e0',484,126.75)}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 while True:
  data=proc.stdout.read(960*540*3)
  if not data:break
  if len(data)!=960*540*3:raise RuntimeError('Partial frame')
  yield Image.frombytes('RGB',(960,540),data)
 if proc.wait()!=0:raise RuntimeError('Decode failed')
def sheet(name,entries,size,columns=3):
 w,h=size;rows=(len(entries)+columns-1)//columns
 im=Image.new('RGB',(w*columns,(h+25)*rows),'#181818');d=ImageDraw.Draw(im)
 for i,(label,pic) in enumerate(entries):
  x=i%columns*w;y=i//columns*(h+25)
  d.text((x+5,y+5),label,fill='white');im.paste(pic.resize(size),(x,y+25))
 im.save(OUT/name,quality=91)
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);checks={};male_frames=[];later_frames=[]
 for label,(filename,expected,count,origin) in FILES.items():
  path=BASE/'exports'/filename
  if digest(path)!=expected:raise RuntimeError('Proof hash mismatch')
  frames=list(decode(path))
  if len(frames)!=count:raise RuntimeError('Frame count mismatch')
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_frames','-show_entries','frame=best_effort_timestamp_time,media_type','-of','json',str(path)]))
  pts=[float(f['best_effort_timestamp_time']) for f in info.pop('frames') if f['media_type']=='video']
  checks[label]={'file':str(path.relative_to(ROOT)),'sha256':expected,'frames':len(frames),'masterStartSeconds':origin,'maxPtsDeviationFromIndexOver24':max(abs(t-i/24) for i,t in enumerate(pts)),'probe':info}
  if label=='male':male_frames=frames
  else:later_frames=frames
 # Numbering is zero-based throughout these sequence sheets.
 m=lambda i:(f'male f{i} | master {118.25+i/24:.6f}s',male_frames[i])
 l=lambda i:(f'later f{i} | master {126.75+i/24:.6f}s',later_frames[i])
 sheet('male-hold-join.jpg',[m(i) for i in [0,30,60,61,62,63,64,65,66,67,86,110]],(480,270))
 sheet('later-overview.jpg',[l(i) for i in [0,45,90,91,136,182,183,207,231,255,279,303,304,343,381,382,417,452,453,467,483]],(320,180))
 sheet('later-cut-frames.jpg',[l(i) for i in [88,89,90,91,92,93,379,380,381,382,383,384,450,451,452,453,454,455]],(480,270))
 sheet('later-internal-hold-seams.jpg',[l(i) for i in [180,181,182,183,184,185,301,302,303,304,305,306]],(480,270))
 for label,indices in [('male',[0,62,63,110]),('later',[0,90,91,381,382,452,453,483])]:
  frames=male_frames if label=='male' else later_frames
  for i in indices:frames[i].save(OUT/f'{label}-normal-f{i:03}.jpg',quality=92)
 for name,indices,crop in [('s027',list(range(91)),(300,65,515,240)),('s029-p02',list(range(382,453)),(168,0,340,140)),('s029-p01',list(range(453,484)),(300,65,515,240))]:
  for start in range(0,len(indices),48):
   selected=indices[start:start+48]
   sheet(f'{name}-faces-{start+1:03}-{start+len(selected):03}.jpg',[(f'proof f{i} | {i/24:.3f}s',later_frames[i].crop(crop)) for i in selected],(215,175),8)
 # Compare exact decoded picture frames with the earlier hash-bound S028 proof.
 previous=BASE/'exports/Join_Me_in_Life_S028_Original_Reuse_Candidate.mp4'
 previous_digest=digest(previous)
 if previous_digest!='83313d4d45797ec8b2161662e5d7de4a9ca4dba2b667e9bcff70f982adee76d1':raise RuntimeError('Earlier S028 proof changed')
 diffs=[]
 for i,im in enumerate(decode(previous)):
  a=np.asarray(im).astype(np.int16);b=np.asarray(later_frames[91+i]).astype(np.int16)
  diffs.append({'frame':i,'exactRgbEqual':bool(np.array_equal(a,b)),'meanAbsRgbDifference':float(np.abs(a-b).mean())})
 checks['s028Comparison']={'priorProofSha256':previous_digest,'newProofFramesZeroBasedInclusive':[91,381],'framesCompared':len(diffs),'exactRgbEqualFrames':sum(x['exactRgbEqual'] for x in diffs),'maximumMeanAbsRgbDifference':max(x['meanAbsRgbDifference'] for x in diffs)}
 # Verify the male lead ends on the same pose and source starts without a framing reset.
 checks['maleJoinMeanAbsRgbDifference']=float(np.abs(np.asarray(male_frames[62]).astype(np.int16)-np.asarray(male_frames[63]).astype(np.int16)).mean())
 checks['laterHoldSeamMeanAbsRgbDifference']={str(a)+'-'+str(b):float(np.abs(np.asarray(later_frames[a]).astype(np.int16)-np.asarray(later_frames[b]).astype(np.int16)).mean()) for a,b in [(182,183),(303,304)]}
 (OUT/'encoded-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(json.dumps({k:({x:y for x,y in v.items() if x!='probe'} if isinstance(v,dict) else v) for k,v in checks.items()},indent=2))
