from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
D=Path(__file__).resolve().parent;P=D.parents[1]
def decode(src):
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(src)]))['streams'][0];w,h=meta['width'],meta['height']
 p=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);i=0
 while True:
  b=p.stdout.read(w*h*3)
  if not b:break
  assert len(b)==w*h*3
  yield i,Image.frombytes('RGB',(w,h),b);i+=1
 p.wait()
def sheets(ims,prefix,cols=3,rows=4):
 w,h=ims[0].size
 for off in range(0,len(ims),cols*rows):
  c=Image.new('RGB',(w*cols,h*rows))
  for j,im in enumerate(ims[off:off+cols*rows]):c.paste(im,((j%cols)*w,(j//cols)*h))
  c.save(D/f'{prefix}-{off:03}.jpg',quality=94)
for sid in range(21,26):
 shot=f'C{sid}';d=json.loads((P/f'research/middle-c-v2-{shot}-temporal-triage.json').read_text());sel=set()
 for key in ['ranked_fullframe_changes','ranked_adjacent_changes','ranked_single_frame_reversals']:
  for r in d[key][:4]:
   if 'transition' in r:sel.update(r['transition'])
   else:sel.update([r['middle_frame']-1,r['middle_frame'],r['middle_frame']+1])
 if sid==24:sel.update(range(118,140))
 ims=[]
 for i,im in decode(P/f'assets/motion/middle-c-v2/{shot}/video-silent.mp4'):
  if i in sel:
   if sid==24 and 118<=i<140:im=im.crop((180,80,620,512))
   else:im=im.resize((448,256))
   im=im.resize((448,256));ImageDraw.Draw(im).text((5,5),f'{shot} raw{i}',fill='red',stroke_width=1,stroke_fill='white');ims.append(im)
 sheets(ims,f'{shot}-ranked');(D/f'{shot}-ranked-selection.json').write_text(json.dumps({'frames':sorted(sel),'top_each_metric':4,'additional_C24_consecutive_reveal':[118,140] if sid==24 else []},indent=2)+'\n')
cuts=[196,348,489,657,825,974]
selected={c:set(range(c-3,c+3)) for c in cuts};out={c:[] for c in cuts}
for i,im in decode(P/'exports/C20_C26_Middle_C_Unbound_Diagnostic_v1.mp4'):
 for c,ns in selected.items():
  if i in ns:
   im=im.resize((896,504))
   ImageDraw.Draw(im).text((5,5),f'local{i} master{i+3624}',fill='red',stroke_width=1,stroke_fill='white');out[c].append(im.copy())
for c,ims in out.items():sheets(ims,f'joined-cut-{c}',cols=2,rows=3)
for shot in ['C21','C22','C23','C24','C25','C20-C26']:
 ims=[]
 for f in sorted(D.glob(f'{shot}-playback-*.jpg'),key=lambda x:float(x.stem.split('playback-')[1])):
  im=Image.open(f).resize((480,275));ImageDraw.Draw(im).text((5,5),f.stem,fill='red',stroke_width=1,stroke_fill='white');ims.append(im)
 sheets(ims,f'{shot}-playback-captures',cols=3,rows=3)
