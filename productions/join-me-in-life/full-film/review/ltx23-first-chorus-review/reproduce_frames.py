"""Reproduce the S014 source review; no source/edit mutations. Requires FFmpeg/Pillow.
Raw frames stay under ignored root build/. No provider calls.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,hashlib,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
PROD=ROOT/'productions/join-me-in-life';BASE=PROD/'full-film/assets/motion/ltx23-performance-pilots/S014';OUT=ROOT/'build/ltx23-first-chorus-review'
EXPECTED='8756ad09d45ecfe47bb2a4cead5f5184d3bd4a4561cbc27e9495cdb6170a0252'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def frame_hashes(p):
 s=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-fps_mode','passthrough','-f','framemd5','-'],text=True)
 return [line.rsplit(',',1)[-1].strip() for line in s.splitlines() if not line.startswith('#')]
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);source=BASE/'video-silent.mp4'
 if sha(source)!=EXPECTED:raise RuntimeError('Source hash differs')
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-']);size=896*512*3
 if len(raw)!=105*size:raise RuntimeError('Expected 105 frames')
 frames=[Image.frombytes('RGB',(896,512),raw[i*size:(i+1)*size]) for i in range(105)]
 for i,im in enumerate(frames):im.save(OUT/f'frame-{i:03}.png')
 for start in range(0,105,12):
  sheet=Image.new('RGB',(1344,1124),'#171717');d=ImageDraw.Draw(sheet)
  for j,im in enumerate(frames[start:start+12]):
   i=start+j;x=j%3*448;y=j//3*281;d.text((x+5,y+4),f'source f{i:03} | {i/24:.6f}s | song {66.375+i/24:.6f}',fill='white');sheet.paste(im.resize((448,256)),(x,y+25))
  sheet.save(OUT/f'sequential-{start:03}-{min(start+11,104):03}.jpg',quality=92)
 points=[(0,232,290,225),(12,290,370,245),(24,335,419,250),(36,358,449,259),(48,382,480,263),(60,405,520,253),(72,425,546,243),(84,446,585,238),(96,465,615,233),(104,477,634,231)]
 canvas=Image.new('RGB',(1000,650),'#161616');d=ImageDraw.Draw(canvas)
 for j,(i,cx,hx,hy) in enumerate(points):
  im=frames[i];x=j%5*200;y=j//5*325;d.text((x+5,y+5),f'f{i} / face and free palm',fill='white')
  canvas.paste(im.crop((cx-55,0,cx+65,140)).resize((168,196)),(x,y+25));canvas.paste(im.crop((hx-45,hy-40,hx+45,hy+40)).resize((144,128)),(x,y+197))
 canvas.save(OUT/'face-hand-detail.jpg',quality=95)
 a=Image.open(PROD/'current/assets/A01_Approved_Character_Pair.jpg');fit=Image.open(BASE/'input-fitted.png')
 rows=[('A01 identity',a.crop((460,0,645,220))),('P02 fitted input',fit.crop((174,0,288,136)))]+[(f'generated f{i}',frames[i].crop((cx-55,0,cx+65,142))) for i,cx in [(0,232),(12,290),(50,385),(100,473)]]
 canvas=Image.new('RGB',(660,570),'#161616');d=ImageDraw.Draw(canvas)
 for j,(label,im) in enumerate(rows):
  x=j%3*220;y=j//3*285;d.text((x+5,y+5),label,fill='white');canvas.paste(im.resize((220,260)),(x,y+25))
 canvas.save(OUT/'identity-comparison.jpg',quality=95)
 im=Image.new('RGB',(896,708),'#111');d=ImageDraw.Draw(im)
 for j,i in enumerate([0,25,50,100]):
  d.text((5,j*177+5),f'source f{i}: native floor/feet/cable',fill='white');im.paste(frames[i].crop((0,360,896,512)),(0,j*177+25))
 im.save(OUT/'floor-contact.jpg',quality=95)
 im=Image.new('RGB',(900,405),'#151515');d=ImageDraw.Draw(im)
 for j,(i,cx) in enumerate([(0,232),(3,248),(12,290),(18,316),(24,335),(30,347),(36,358),(50,385),(100,473)]):
  x=j%3*300;y=j//3*135;d.text((x+3,y+4),f'f{i}, top image boundary at next row',fill='white');im.paste(frames[i].crop((cx-75,0,cx+75,55)).resize((300,110),Image.Resampling.NEAREST),(x,y+25))
 im.save(OUT/'crown-detail.jpg',quality=95)
 for i in [3,25,50,100,104]:frames[i].save(OUT/f'normal-f{i:03}.jpg',quality=93)
 pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','frame=best_effort_timestamp_time','-of','json',str(source)]))['frames']
 original=frame_hashes(source);review=frame_hashes(BASE/'review-original-audio.mp4')
 if original!=review:raise RuntimeError('Review MP4 pictures differ from source')
 files=[source,BASE/'review-original-audio.mp4',BASE/'review-original-audio.mkv',BASE/'input-fitted.png',PROD/'art/04_Performance/P02_Chorus_Performance.png',PROD/'current/assets/A01_Approved_Character_Pair.jpg']
 result={'scope':'Technical checks, not creative acceptance or listening.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in files],'sourceProbe':probe(source),'browserReviewProbe':probe(BASE/'review-original-audio.mp4'),'decodedFrames':105,'browserReviewDecodedPicturesAllIdentical':True,'maxSourcePtsDeviationFromIndexOver24':max(abs(float(f['best_effort_timestamp_time'])-i/24) for i,f in enumerate(pts)),'proposedSelection':{'zeroBasedEndExclusive':[3,101],'seconds':[3/24,101/24],'masterSeconds':[66.5,70.58333333333333],'frames':98},'diagnosticCropNote':'Face/hand locations manually selected for display; not automated identity or joint tracking.'}
 (OUT/'encoded-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','sourceProbe','browserReviewProbe']},indent=2))
