"""Review the exact S028 encode; produce local JPEGs and numeric cadence evidence.
Requires ffmpeg, ffprobe, Pillow and NumPy. Outputs stay under ignored root build/.
No source, edit configuration or archived review evidence is changed.
"""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/m01-reuse-sequence-review'
SOURCE=ROOT/'productions/join-me-in-life/current/assets/M01_Embrace.mp4'
CANDIDATE=ROOT/'productions/join-me-in-life/full-film/exports/Join_Me_in_Life_S028_Original_Reuse_Candidate.mp4'
EXPECTED='83313d4d45797ec8b2161662e5d7de4a9ca4dba2b667e9bcff70f982adee76d1'

def decode(path,w,h,filters):
 with subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vf',filters,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE) as p:
  while data:=p.stdout.read(w*h*3):
   if len(data)!=w*h*3:raise RuntimeError('Partial frame')
   yield Image.frombytes('RGB',(w,h),data)
  if p.wait():raise RuntimeError('Decode failed')

def sheet(frames,indices,name,cols,width=480,height=270):
 rows=(len(indices)+cols-1)//cols
 canvas=Image.new('RGB',(cols*width,rows*(height+27)),'#171717');d=ImageDraw.Draw(canvas)
 for j,i in enumerate(indices):
  x=j%cols*width;y=j//cols*(height+27)
  local=i/24;full=3133/24+local
  d.text((x+5,y+5),f'f{i+1:03} | local {local:.3f}s | song {full:.3f}s',fill='white')
  canvas.paste(frames[i].resize((width,height)),(x,y+27))
 canvas.save(OUT/name,quality=92)

if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 digest=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
 if digest!=EXPECTED:raise RuntimeError('Candidate hash differs from review target')
 frames=list(decode(CANDIDATE,480,270,'scale=480:270'))
 if len(frames)!=291:raise RuntimeError('Expected 291 candidate frames')
 sheet(frames,[0,24,48,72,92,116,140,152,176,200,212,236,260,290],'overview.jpg',4)
 sheet(frames,[89,90,91,92,93,94,210,211,212,213,214,215],'joins.jpg',3)
 sheet(frames,[120,124,128,132,136,140,144,148,152,156,160,164],'reach-contact.jpg',3)
 sheet(frames,[0,48,91,213,252,290],'hold-endpoints.jpg',3)
 # Match output action images to decoded original source images with identical
 # production scale/crop, then smaller comparison pixels. Compression makes this
 # a similarity check, not byte equality or a subjective playback claim.
 source=np.stack([np.asarray(im,dtype=np.float32) for im in decode(SOURCE,240,135,'scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1,scale=240:135')])
 # Decode directly at comparison size so Pillow does not add a different kernel.
 candidate=np.stack([np.asarray(im,dtype=np.float32) for im in decode(CANDIDATE,240,135,'scale=240:135')])
 comparisons=[]
 for i,im in enumerate(candidate[92:213]):
  errors=np.mean((source-im)**2,axis=(1,2,3));order=np.argsort(errors)
  comparisons.append({'outputFrame1based':i+93,'expectedSourceFrame1based':i+1,'bestSourceFrame1based':int(order[0])+1,'expectedMse':float(errors[i]),'bestMse':float(errors[order[0]])})
 hold_metrics={
  'leadMaxMseFromFirstDecodedOutput':float(np.max(np.mean((candidate[:92]-candidate[0])**2,axis=(1,2,3)))),
  'endpointMaxMseFromLastActionOutput':float(np.max(np.mean((candidate[213:]-candidate[212])**2,axis=(1,2,3)))),
  'nearestSourceMatchesExpected':sum(x['expectedSourceFrame1based']==x['bestSourceFrame1based'] for x in comparisons),
 }
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(CANDIDATE)]))
 pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(CANDIDATE)]))['frames']
 values=[float(x['best_effort_timestamp_time']) for x in pts]
 pts_check={'decodedFrames':len(values),'maxAbsDeviationFromFrameIndexOver24Seconds':max(abs(t-i/24) for i,t in enumerate(values))}
 result={'ptsCheck':pts_check,'sha256':digest,'originalSourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'frameCount':len(frames),'sequence':{'leadFrames':92,'actionFrames':121,'endHoldFrames':78,'fullSongStartSeconds':3133/24,'actionStartSeconds':3225/24},'comparisonMethod':'RGB MSE after production-matched Lanczos scale/crop then 240x135; nearest source search across all 121 frames; lossy encode prevents exact equality.','metrics':hold_metrics,'sourceMatches':comparisons,'probe':probe}
 (OUT/'source-cadence.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(hold_metrics,indent=2))
