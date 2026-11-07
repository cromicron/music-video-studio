"""Reproduce local review evidence; outputs only ignored root build/.
Requires Python/Pillow, FFmpeg and ffprobe. No provider calls or media edits.
"""
from pathlib import Path
import hashlib,json,subprocess,math,wave
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageStat
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film'
SOURCE=BASE/'assets/motion/ltx23-a2v-bridge-pilot'
OUT=ROOT/'build/ltx23-a2v-bridge-pilot-review'
EXPECTED='9a1420423a8be5e0401e172376e41255e723b2274a87748b5d6857d381959fe5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sheet(entries,cols,size,name):
 w,h=size; rows=math.ceil(len(entries)/cols)
 canvas=Image.new('RGB',(cols*w,rows*(h+24)),'#171717'); d=ImageDraw.Draw(canvas)
 for j,(label,im) in enumerate(entries):
  x,y=(j%cols)*w,(j//cols)*(h+24)
  im=ImageOps.contain(im,(w,h)); canvas.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
  d.text((x+5,y+5),label,fill='white')
 canvas.save(OUT/name,quality=90)
def decode(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 stride=896*512*3
 if len(raw)%stride:raise ValueError('partial frame')
 return [Image.frombytes('RGB',(896,512),raw[i:i+stride]) for i in range(0,len(raw),stride)]
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 p=SOURCE/'video-silent.mp4'; assert sha(p)==EXPECTED
 frames=decode(p); assert len(frames)==97
 frames[88].resize((672,384)).save(OUT/'frame-089-ordinary-size.jpg',quality=91)
 samples=[0,8,16,24,32,40,48,56,64,72,80,88,96]
 sheet([(f'f{i+1:03} | {i/24:.3f}s',frames[i]) for i in samples],4,(448,256),'overview.jpg')
 for start in range(0,97,9):
  sheet([(f'f{i+1:03} | {i/24:.6f}s',frames[i].crop((75,0,635,500))) for i in range(start,min(start+9,97))],3,(560,500),f'native-sequential-{start+1:03}-{min(start+9,97):03}.jpg')
 for i in range(97):frames[i].save(OUT/f'frame-{i+1:03}.png')
 source=BASE/'assets/bridge_plea_start_candidate.png'; a01=BASE.parent/'art/00_References/A01_Approved_Character_Pair.jpg'
 sheet([('Source artwork',Image.open(source).convert('RGB')),('Actual f001',frames[0]),('Actual f097',frames[-1]),('A01 identity reference',Image.open(a01).convert('RGB'))],2,(896,598),'source-final-identity.jpg')
 picked=[0,12,24,36,44,60,76,80,84,88,92,96]
 sheet([(f'f{i+1:03} | face + mic',frames[i].crop((160,20,460,295))) for i in picked],4,(300,275),'face-contact-detail.jpg')
 sheet([(f'f{i+1:03} | free hand',frames[i].crop((315,0,625,495))) for i in picked],4,(310,495),'gesture-detail.jpg')
 browser=decode(SOURCE/'review-original-audio.mp4')
 same=len(browser)==len(frames) and all(a.tobytes()==b.tobytes() for a,b in zip(frames,browser))
 pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(SOURCE/'review-original-audio.mkv'),'-map','0:a:0','-f','s16le','-acodec','pcm_s16le','-'])
 with wave.open(str(BASE/'assets/audio/bridge-a2v-conditioning.wav')) as w:original_pcm=w.readframes(w.getnframes())
 sources=[p,SOURCE/'review-original-audio.mp4',SOURCE/'review-original-audio.mkv',SOURCE/'render.json',source,a01,BASE/'assets/audio/bridge-a2v-conditioning.wav']
 evidence={'frame_numbering':'1-based; source time=(frame-1)/24; full-song time=207.75+source time','video_frame_count':len(frames),'native_dimensions':[896,512],'fps':24,'frame_duration_seconds':97/24,'browser_mp4_decoded_video_exact_match':same,'mkv_decoded_pcm_equal_to_conditioning_wav':pcm==original_pcm,'pcm_samples_per_channel':len(pcm)//4,'pcm_sha256':hashlib.sha256(pcm).hexdigest(),'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sources},'native_image_dimensions':{str(p.relative_to(ROOT)):list(Image.open(p).size) for p in [source,a01]},'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(SOURCE/'review-original-audio.mp4')])),'limits':'All-frame visual evidence and technical waveform equality; neither establishes lip-sync accuracy or subjective listening.'}
 (OUT/'source-checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
 cadence=[{'frame':i+1,'source_seconds':i/24,'previous_frame_mean_absolute_rgb_difference':round(sum(ImageStat.Stat(ImageChops.difference(frames[i],frames[i-1])).mean)/3,6)} for i in range(1,len(frames))]
 (OUT/'cadence.json').write_text(json.dumps({'purpose':'Describes cadence only; numeric differences do not classify visual quality or phoneme sync. Frames26–49 primarily advance on three-frame groups, with small intra-group changes; no backward-motion claim.','samples':cadence},indent=2)+'\n')
 print(json.dumps({k:v for k,v in evidence.items() if k not in ['probe','source_sha256','native_image_dimensions']},indent=2))
