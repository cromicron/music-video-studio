"""Hash-bound exact insertion/cut evidence; scratch remains under root build/."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').exists());FILM=ROOT/'productions/join-me-in-life/full-film';OUT=ROOT/'build/dawn-early-company-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
FILES={'shot':('exports/Join_Me_in_Life_Dawn_Early_Company_Proof.mp4','568f194d3e2a4576262730502647748a1845098e917e84ee71fdffe665b65deb',89),'context':('exports/Join_Me_in_Life_Dawn_Early_Company_Context_Proof.mp4','f69402b57c8fd426debf41b9d19a74508562dfe863e4204e6e49f06f78f9e2f3',327),'source':('assets/motion/ltx23-dawn-pilots/A07/video-silent.mp4','1eb004c3e7306da55b479af550481c0fbbb7cf269913e9db16e2ccdc3fc90582',169)}
def ff(*args):return subprocess.check_output(['ffmpeg','-v','error','-xerror',*args])
arrays={};checks={}
for key,(rel,h,count) in FILES.items():
 p=FILM/rel;assert hashlib.sha256(p.read_bytes()).hexdigest()==h
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_frames','-select_streams','v:0','-of','json',str(p)]));s=probe['streams'][0];assert int(s['nb_read_frames'])==count and s['avg_frame_rate']=='24/1'
 pts=np.array([float(f['best_effort_timestamp_time']) for f in probe['frames']]);assert np.max(np.abs(pts-np.arange(count)/24))<.000001
 if key=='source':
  filt='trim=start_frame=0:end_frame=89,scale=960:540:force_original_aspect_ratio=decrease:force_divisible_by=4:flags=lanczos,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,format=yuv420p'
  data=ff('-i',str(p),'-an','-vf',filt,'-pix_fmt','rgb24','-f','rawvideo','-');count=89
 else:data=ff('-i',str(p),'-an','-pix_fmt','rgb24','-f','rawvideo','-')
 arrays[key]=np.frombuffer(data,np.uint8).reshape(count,540,960,3)
 checks[key]={'path':rel,'sha256':h,'decoded_frames':int(s['nb_read_frames']),'dimensions':[s['width'],s['height']],'fps':24,'max_pts_error_seconds':float(np.max(np.abs(pts-np.arange(len(pts))/24)))}
mae=np.abs(arrays['shot'].astype(np.int16)-arrays['source'].astype(np.int16)).mean(axis=(1,2,3));ctx=np.abs(arrays['context'][90:179].astype(np.int16)-arrays['shot'].astype(np.int16)).mean(axis=(1,2,3))
checks['mapping']={'source':[0,89],'context':[90,179],'timeline':[5842,5931],'contain_rectangle':[8,0,944,540],'expected_source_to_shot_rgb_mae_mean':float(mae.mean()),'expected_source_to_shot_rgb_mae_max':float(mae.max()),'shot_to_context_rgb_mae_mean':float(ctx.mean()),'shot_to_context_rgb_mae_max':float(ctx.max()),'per_frame_expected_mae':mae.tolist(),'per_frame_context_mae':ctx.tolist(),'max_side_padding_rgb':int(max(arrays['shot'][:,:,:6].max(),arrays['shot'][:,:,954:].max())),'unique_shot_decoded_frames':len({hashlib.sha256(f.tobytes()).hexdigest() for f in arrays['shot']})}
assert mae.max()<5 and ctx.max()<5
cfg=FILM/'edit-production-candidate.json';checks['config_sha256']=hashlib.sha256(cfg.read_bytes()).hexdigest();assert checks['config_sha256']=='c8470942090e8b10799f135a25710f8947daa3d523fa62fe42fbc396559db832'
approval=FILM/json.loads(cfg.read_text())['approved_motion'];clips=json.loads(approval.read_text())['clips'];a=[c for c in clips if c.get('path')==FILES['source'][0]];assert len(a)==1 and a[0]['shot_ids']==['S053'] and a[0]['reviewed_source_frames_zero_based']==[0,89];checks['only_current_A07_assignment']=['S053']
def sheet(key,indices,crop,cols,name,size=None):
 tiles=[]
 for i in indices:
  im=Image.fromarray(arrays[key][i]).crop(crop)
  if size:im=im.resize(size,Image.Resampling.LANCZOS)
  tile=Image.new('RGB',(im.width,im.height+22),(22,22,22));tile.paste(im,(0,22));ImageDraw.Draw(tile).text((5,4),f'{key} f{i+1:03d} | {i/24:.3f}s',fill='white');tiles.append(tile)
 w,h=tiles[0].size;out=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),(30,30,30))
 for n,t in enumerate(tiles):out.paste(t,((n%cols)*w,(n//cols)*h))
 out.save(OUT/name,quality=91)
for n in range(0,89,16):
 indices=range(n,min(89,n+16));sheet('shot',indices,(0,0,960,540),4,f'all-{n+1:03d}-{min(89,n+16):03d}.jpg',(480,270));sheet('shot',indices,(185,60,610,300),4,f'faces-{n+1:03d}-{min(89,n+16):03d}.jpg');sheet('shot',indices,(285,345,680,530),4,f'hands-{n+1:03d}-{min(89,n+16):03d}.jpg')
sheet('context',list(range(0,327,18))+[326],(0,0,960,540),4,'context-phases.jpg',(480,270))
sheet('context',[87,88,89,90,91,92,176,177,178,179,180,181],(0,0,960,540),3,'exact-cuts.jpg',(480,270))
sheet('shot',[0,12,24,36,48,60,72,88],(0,0,960,540),4,'shot-phases.jpg',(480,270))
Image.fromarray(arrays['shot'][-1]).save(OUT/'last-included.png')
(OUT/'verification.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({k:v for k,v in checks['mapping'].items() if not k.startswith('per_frame')},indent=2))
