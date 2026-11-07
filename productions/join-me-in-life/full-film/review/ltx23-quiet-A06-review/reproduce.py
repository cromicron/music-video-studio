"""Rebuild A06 review evidence under ignored root build/. No production mutation."""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
SOURCE = ROOT/'productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-pilots/A06/video-silent.mp4'
EXPECTED = '579efce153b4875493dcaf9d122feac73b72a40e0a43278cfbe91dd9233d4b73'
OUT = ROOT/'build/ltx23-quiet-A06-review'
OUT.mkdir(parents=True, exist_ok=True)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(SOURCE)]))
raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(SOURCE),'-f','rawvideo','-pix_fmt','rgb24','-'])
frames = np.frombuffer(raw,dtype=np.uint8).reshape(-1,512,896,3)
assert len(frames)==161
images = [Image.fromarray(f) for f in frames]
fontcolor = '#ffffff'
def sheet(name, indices, crop=None, cols=4, scale=(448,256)):
    tw,th = scale
    canvas = Image.new('RGB',(cols*tw,((len(indices)+cols-1)//cols)*(th+24)),'#171717')
    draw = ImageDraw.Draw(canvas)
    for n,f in enumerate(indices):
        x,y=(n%cols)*tw,(n//cols)*(th+24)
        image=images[f].crop(crop) if crop else images[f]
        image=image.resize(scale,Image.Resampling.LANCZOS)
        canvas.paste(image,(x,y+24))
        draw.text((x+5,y+5),f'f{f:03d} | {f/24:.3f}s'+(' | selected' if 3<=f<152 else ' | outside trim'),fill=fontcolor)
    canvas.save(OUT/name,quality=82)
for a in range(0,161,16):
    sheet(f'all-frames-{a:03d}-{min(a+15,160):03d}.jpg',list(range(a,min(a+16,161))))
for a in range(0,161,40):
    sheet(f'grip-{a:03d}-{min(a+39,160):03d}.jpg',list(range(a,min(a+40,161))),crop=(510,380,690,495),cols=8,scale=(180,115))
for a in range(0,161,24):
    sheet(f'face-{a:03d}-{min(a+23,160):03d}.jpg',list(range(a,min(a+24,161))),crop=(295,20,510,290),cols=6,scale=(215,270))
sheet('motion-phases.jpg',[3,24,48,72,96,120,144,151],cols=2,scale=(896,512))
sheet('trim-edges.jpg',[0,1,2,3,4,150,151,152,153,154,158,159,160],cols=3,scale=(448,256))
for f in [3,24,48,72,80,96,120,144,151]:
    images[f].save(OUT/f'native-{f:03d}.jpg',quality=92)
guide=ROOT/'productions/join-me-in-life/full-film/assets/motion/ltx23-quiet-pilots/A06/start-fitted.png'
end=guide.with_name('end-fitted.png')
Image.open(guide).convert('RGB').save(OUT/'guide-fitted.jpg',quality=90)
timings=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time','-of','json',str(SOURCE)]))['frames']
pts=[float(f['best_effort_timestamp_time']) for f in timings]
assert len(pts)==161 and all(abs(t-i/24)<1e-6 for i,t in enumerate(pts))
manifest={'source':str(SOURCE.relative_to(ROOT)),'sha256':EXPECTED,'probe':probe,
          'startFittedSha256':hashlib.sha256(guide.read_bytes()).hexdigest(),
          'endFittedSha256':hashlib.sha256(end.read_bytes()).hexdigest(),
          'selection':{'first':3,'endExclusive':152,'frames':149,'seconds':149/24,'masterStart':1447/24,'masterEnd':1596/24},
          'decodedFrames':len(frames),'uniqueDecodedFrames':len({hashlib.sha256(f.tobytes()).digest() for f in frames}),
          'cadence':{'frames':len(pts),'firstPts':pts[0],'lastPts':pts[-1],'allPtsAgreeWithIndexDividedBy24WithinMicrosecond':True},
          'note':'Decoded uniqueness is not evidence of acting. Motion judgment requires visible structural change in the linked frames.'}
(OUT/'source-evidence.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='probe'},indent=2))
