"""Rebuild native summer review evidence in ignored root build/.
Requires FFmpeg, ffprobe and Pillow. No source/config/provider changes.
"""
from pathlib import Path
import hashlib,json,subprocess,math
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageStat
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film'; ASSET=BASE/'assets/motion/ltx23-summer-pilot';OUT=ROOT/'build/ltx23-summer-pilot-review';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ASSET/'video-silent.mp4';EXPECTED='f0d49f36d944932141aedacd49233fcd49d89e286f1ba239462d82b01cec1f57'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED

def decode(path,width,height,vf=None):
 cmd=['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0']
 if vf:cmd+=['-vf',vf]
 raw=subprocess.check_output(cmd+['-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-']); stride=width*height*3
 assert len(raw)%stride==0
 return [Image.frombytes('RGB',(width,height),raw[i:i+stride]) for i in range(0,len(raw),stride)]
def sheet(entries,cols,size,name):
 w,h=size;rows=math.ceil(len(entries)/cols);canvas=Image.new('RGB',(w*cols,(h+24)*rows),'#171717');d=ImageDraw.Draw(canvas)
 for j,(label,im) in enumerate(entries):
  x,y=(j%cols)*w,(j//cols)*(h+24);im=ImageOps.contain(im,(w,h));canvas.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2));d.text((x+5,y+5),label,fill='white')
 canvas.save(OUT/name,quality=90)
frames=decode(SOURCE,896,512);assert len(frames)==145
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(SOURCE)]));assert not any(s['codec_type']=='audio' for s in probe['streams'])
for i,frame in enumerate(frames):frame.save(OUT/f'frame-{i+1:03}.png')
for start in range(0,145,9):sheet([(f'f{i+1:03} | {i/24:.3f}s',frames[i].crop((125,0,665,512))) for i in range(start,min(start+9,145))],3,(540,512),f'native-sequential-{start+1:03}-{min(start+9,145):03}.jpg')
ids=[0,12,24,36,48,60,72,84,96,108,120,132,144]
sheet([(f'f{i+1:03} | {i/24:.3f}s',frames[i]) for i in ids],4,(448,256),'overview.jpg')
sheet([(f'f{i+1:03} | faces',frames[i].crop((225,30,635,220))) for i in ids],4,(410,190),'face-detail.jpg')
sheet([(f'f{i+1:03} | hands/support',frames[i].crop((225,235,660,500))) for i in [0,24,48,60,72,84,96,108,120,144]],3,(435,265),'hands-support.jpg')
start=BASE.parent/'current/assets/M02_Summer_Start.png';end=BASE/'assets/summer_identity_end_v2_candidate.png';a01=BASE.parent/'art/00_References/A01_Approved_Character_Pair.jpg';a02=BASE.parent/'art/00_References/A02_Approved_Anime_Window.png'
sheet([('Original start',Image.open(start)),('Actual f001',frames[0]),('End guide v2',Image.open(end)),('Actual f145',frames[144])],2,(896,512),'guides-endpoints.jpg')
entries=[('A01 female identity',Image.open(a01).crop((860,65,1040,280))),('A02 female identity',Image.open(a02).crop((250,360,520,635)))]
entries +=[(f'Actual f{i+1:03}',frames[i].crop((477,45,624,202))) for i in [12,24,36,48,60,72,84,96,108,120,144]]
sheet(entries,5,(225,255),'female-identity.jpg')
old=BASE.parent/'current/assets/M02_Summer.mp4'; male=BASE/'assets/motion/m02-male-reuse-candidate/M02_Male_0-2s_16x9.mp4'
original48=decode(old,896,505,'select=eq(n\\,47),scale=896:505')[0]
male48=decode(male,960,540,'select=eq(n\\,47)')[0]
sheet([('Original M02 f48: pose context',original48),('Actual outgoing male crop f48',male48),('New take f001',frames[0]),('New take f049 /2s',frames[48]),('New take f073 /3s',frames[72]),('New take f097 /4s',frames[96])],2,(896,512),'seam-candidates.jpg')
paths=[SOURCE,ASSET/'render.json',start,end,a01,a02,old,male]
evidence={'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'reference_dimensions':{str(p.relative_to(ROOT)):list(Image.open(p).size) for p in [start,end,a01,a02]},'decoded_frames':145,'fps':24,'duration_seconds':145/24,'audio_streams':0,'frame_numbering':'1-based; source timestamp=(frame-1)/24','probe':probe,'scope':'All-frame visual/identity/contact review evidence; no source-preserving repair, exact seam, audio or phoneme-sync claim.'}
(OUT/'source-checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Decoded145frames; no audio. Evidence written to',OUT)
