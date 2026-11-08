from pathlib import Path
from PIL import Image, ImageDraw
import subprocess,json,hashlib
D=Path(__file__).resolve().parent
P=D.parents[1]
ends=[158,147,174,174,155]
for sid,end in zip(range(21,26),ends):
 shot=f'C{sid}'; src=P/f'assets/motion/middle-c-v2/{shot}/video-silent.mp4'
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 overview=[]; edges=[]; i=0
 while True:
  b=proc.stdout.read(896*512*3)
  if not b:break
  im=Image.frombytes('RGB',(896,512),b)
  if i%4==0 or i in [6,end-1]:
   tile=im.resize((448,256));ImageDraw.Draw(tile).text((6,6),f'{shot} raw {i}',fill='red',stroke_width=1,stroke_fill='white');overview.append(tile)
  if i in list(range(3,10))+list(range(end-5,min(end+3,190))):
   im.save(D/f'{shot}-native-{i:03}.jpg',quality=95);edges.append(i)
  i+=1
 proc.wait()
 for off in range(0,len(overview),12):
  canvas=Image.new('RGB',(448*3,256*4))
  for j,im in enumerate(overview[off:off+12]):canvas.paste(im,((j%3)*448,(j//3)*256))
  canvas.save(D/f'{shot}-overview-{off:03}.jpg',quality=93)
 (D/f'{shot}-inspection-selection.json').write_text(json.dumps({'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'decoded':i,'overview_frames':sorted(set(list(range(0,i,4))+[6,end-1])),'native_edges':edges,'method':'Streamed RGB, at most one native frame and bounded thumbnail sheets in memory; no full RGB dump.'},indent=2)+'\n')
