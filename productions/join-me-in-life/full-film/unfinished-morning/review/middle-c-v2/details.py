from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
D=Path(__file__).resolve().parent;P=D.parents[1]
for shot,start,end,box in [('C21',64,115,(50,210,360,500)),('C22',30,138,(175,105,370,495))]:
 src=P/f'assets/motion/middle-c-v2/{shot}/video-silent.mp4'
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 tiles=[];i=0
 while True:
  b=proc.stdout.read(896*512*3)
  if not b:break
  if start<=i<end:
   im=Image.frombytes('RGB',(896,512),b).crop(box);ImageDraw.Draw(im).text((5,5),f'{shot} raw{i}',fill='red',stroke_width=1,stroke_fill='white');tiles.append(im)
  i+=1
 proc.wait();w,h=tiles[0].size
 for off in range(0,len(tiles),12):
  c=Image.new('RGB',(w*6,h*2))
  for j,im in enumerate(tiles[off:off+12]):c.paste(im,((j%6)*w,(j//6)*h))
  c.save(D/f'{shot}-consecutive-{start+off:03}.jpg',quality=95)
 (D/f'{shot}-consecutive-selection.json').write_text(json.dumps({'raw_frames_half_open':[start,end],'native_crop_xyxy':box,'consecutive':True},indent=2)+'\n')
