"""Rebuild fixed-crop L01 review evidence under ignored root build/."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
SOURCE=ROOT/'productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-window-closeup/video-silent.mp4'
ORIGINAL=ROOT/'productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-pilots/L01/video-silent.mp4'
OUT=ROOT/'build/ltx23-window-closeup-review';OUT.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20'
assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()=='e90f0c8b2ed56367fe04399109dc7a95a030aacc56e158964a46bac610ef743a'
def decode(path,w,h):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape(-1,h,w,3)
frames=decode(SOURCE,672,378);original=decode(ORIGINAL,896,512)
assert len(frames)==len(original)==161
images=[Image.fromarray(f) for f in frames]
def sheet(name,indices,crop=None,cols=4,scale=(336,189)):
    w,h=scale
    canvas=Image.new('RGB',(cols*w,((len(indices)+cols-1)//cols)*(h+24)),'#171717');draw=ImageDraw.Draw(canvas)
    for i,f in enumerate(indices):
        x,y=(i%cols)*w,(i//cols)*(h+24)
        image=images[f].crop(crop) if crop else images[f]
        canvas.paste(image.resize(scale,Image.Resampling.LANCZOS),(x,y+24))
        label=f'f{f:03d}' if w<200 else f'f{f:03d} | {f/24:.3f}s'+(' | selected' if 3<=f<157 else ' | outside trim')
        draw.text((x+4,y+5),label,fill='white')
    canvas.save(OUT/name,quality=84)
for a in range(0,161,16):
    sheet(f'all-frames-{a:03d}-{min(a+15,160):03d}.jpg',list(range(a,min(a+16,161))))
for a in range(0,161,24):
    sheet(f'face-{a:03d}-{min(a+23,160):03d}.jpg',list(range(a,min(a+24,161))),crop=(64,60,334,350),cols=6,scale=(270,290))
for a in range(0,161,32):
    sheet(f'left-edge-{a:03d}-{min(a+31,160):03d}.jpg',list(range(a,min(a+32,161))),crop=(0,60,80,350),cols=8,scale=(80,290))
for f in [3,49,72,89,100,124,156,160]:
    images[f].save(OUT/f'native-{f:03d}.jpg',quality=92)
    if f in [3,49,89,124,156]:images[f].resize((960,540),Image.Resampling.LANCZOS).save(OUT/f'normal-{f:03d}.jpg',quality=90)
comparison=Image.new('RGB',(896,512*2+24),'#171717');draw=ImageDraw.Draw(comparison)
for j,f in enumerate([3,49]):
    im=Image.fromarray(original[f]);d=ImageDraw.Draw(im);d.rectangle((224,0,895,377),outline='#ffdd00',width=2)
    comparison.paste(im,(0,j*(512+24)));draw.text((4,j*(512+24)+512+4),f'Original f{f}: yellow = fixed retained crop',fill='white')
comparison.save(OUT/'original-crop-boundaries.jpg',quality=88)
timings=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time','-of','json',str(SOURCE)]))['frames']
pts=[float(f['best_effort_timestamp_time']) for f in timings]
assert len(pts)==161 and all(abs(t-i/24)<1e-6 for i,t in enumerate(pts))
errors=[float(np.abs(frames[i].astype(np.float32)-original[i,:378,224:896].astype(np.float32)).mean()) for i in range(161)]
# Low-resolution nearest source-frame check, independently of claimed crop provenance.
thumbs=np.stack([np.asarray(im.resize((168,95)),dtype=np.float32) for im in images])
original_thumbs=np.stack([np.asarray(Image.fromarray(f[:378,224:896]).resize((168,95)),dtype=np.float32) for f in original])
nearest=[int(np.argmin(((original_thumbs-t)**2).mean(axis=(1,2,3)))) for t in thumbs]
manifest={'source':str(SOURCE.relative_to(ROOT)),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'original':str(ORIGINAL.relative_to(ROOT)),'originalSha256':hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
          'cropXYWH':[224,0,672,378],'selection':[3,157],'selectedFrames':154,'selectedSeconds':154/24,
          'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(SOURCE)])),
          'cadence':{'frames':161,'firstPts':pts[0],'lastPts':pts[-1],'allPtsMatchIndexDividedBy24WithinMicrosecond':True},
          'cropComparison':{'meanAbsolutePixelErrorPerFrame':errors,'maxMeanAbsolutePixelError':max(errors),'nearestOriginalFramePerDerivativeFrame':nearest,'allNearestFramesMatchIndex':nearest==list(range(161))},
          'note':'Crop matching/cadence are technical facts. Reflection exclusion, anatomy and editorial usability require visual inspection.'}
(OUT/'source-evidence.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'frames':161,'crop':[224,0,672,378],'maxMeanAbsolutePixelError':max(errors),'allNearestFramesMatchIndex':nearest==list(range(161))},indent=2))
