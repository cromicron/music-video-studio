from pathlib import Path
import json, subprocess,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
P=HERE.parents[1]
for shot,n in [('O02',217),('B04',89)]:
 out=HERE/shot/f'boundary-full-native-raw{n:03d}.png'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-i',str(P/'assets/motion/action-fix01-v2'/shot/'video-silent.mp4'),'-vf',f'select=eq(n\\,{n})','-frames:v','1','-threads','1','-n',str(out)],check=True)
process=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(P/'assets/motion/action-fix01-v2/O02/video-silent.mp4'),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'],stdout=subprocess.PIPE)
rows=[];first=None
while data:=process.stdout.read(896*512*3):
 assert len(data)==896*512*3
 rgb=np.frombuffer(data,np.uint8).reshape(512,896,3)
 n=len(rows);gray=rgb.mean(axis=2)
 if first is None:first=gray.copy()
 regs={}
 if 38<=n<=64:
  for name,(x,y,w,h) in {'cabinet':(570,5,256,128),'faucet_rack':(760,180,128,256)}.items():
   a=first[y:y+h,x:x+w];b=gray[y:y+h,x:x+w]
   fa=np.fft.rfft2(a-a.mean());fb=np.fft.rfft2(b-b.mean());cross=fa*np.conj(fb);cross/=np.maximum(abs(cross),1e-9)
   corr=np.fft.irfft2(cross,s=(h,w));py,px=np.unravel_index(np.argmax(corr),corr.shape)
   regs[name]={'shift':[int(px if px<w/2 else px-w),int(py if py<h/2 else py-h)],'peak':float(corr[py,px])}
 r,g,b=rgb[375:485,688:740].transpose(2,0,1)
 mask=(r>125)&(g>90)&(r>g)&(g>b)
 ys,xs=np.where(mask)
 box=[int(xs.min()+688),int(ys.min()+375),int(xs.max()+688+1),int(ys.max()+375+1)] if len(xs) else None
 rows.append({'raw':n,'far_cup_color_core_bbox':box,'static_region_registration_advisory':regs})
assert process.wait()==0
(HERE/'O02-prop-stability-advisory.json').write_text(json.dumps({'scope':'Read-only color/phase registration advisory; masks are not object-tracking or motion acceptance. Native contact and full-frame review decide.','source_sha256':hashlib.sha256((P/'assets/motion/action-fix01-v2/O02/video-silent.mp4').read_bytes()).hexdigest(),'rows':rows},indent=2)+'\n')
for i in range(38,65):print(rows[i])
