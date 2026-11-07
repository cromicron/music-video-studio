"""Independent encoded R1 insertion/cadence/containment and cut evidence.

Writes only ignored build/r1-quiet-sequence-review. No provider or edit mutation.
"""
from pathlib import Path
import hashlib, json, subprocess, gc
import numpy as np
from PIL import Image, ImageDraw

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE = ROOT/'productions/join-me-in-life/full-film'
OUT = ROOT/'build/r1-quiet-sequence-review'; OUT.mkdir(parents=True, exist_ok=True)
CONFIG = '89b6606ee95ddec4026493e548ea821bebb56886b6e59431063cc5ae1a8ae22b'
SPECS = [
 ('waiting', 'Waiting_Correction', 132, '1fd2f4b81592fdb8702322410840a55d9a4065469224383cbce628d080bbd978'),
 ('waiting-context', 'Waiting_Correction_Context', 415, 'b1f61bd2b17ec7e05596d0add089902a17cb300c14e86dc239c9c83ed577e4f8'),
 ('held30', 'Held_Correction_S030', 98, '41fe5fb16d18732537cb44f55eafd8351c53527810f63eaf489d5cf9b55fbd0c'),
 ('held32', 'Held_Correction_S032', 96, '7a3f1b928cc6a2f44dfa90c21c2712f027bedd990235c7dc2afc885804aa0725'),
 ('held-context', 'Held_Correction_Context', 495, '8fa53bf00a736e054331c54f0cb37fbe91a602f44d2eacacb3013eba2937fdf9'),
]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
 raw = subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(raw, np.uint8).reshape(-1,540,960,3)
def sheet(frames, name, ids, cols=4, size=(480,270)):
 w,h=size; im=Image.new('RGB',(cols*w,((len(ids)+cols-1)//cols)*(h+24)),'#171717');d=ImageDraw.Draw(im)
 for j,i in enumerate(ids):
  x,y=j%cols*w,j//cols*(h+24);d.text((x+4,y+5),f'{name} zero f{i} | {i/24:.3f}s',fill='white')
  im.paste(Image.fromarray(frames[i]).resize(size,Image.Resampling.LANCZOS),(x,y+24))
 im.save(OUT/(name+'.jpg'),quality=91)
checks={'config_sha256':CONFIG,'scope':'Exact encoded picture/cadence checks; audio correlation below is the hash-bound author manifest result, not subjective listening.'}; hashes={}
for label,name,n,expected in SPECS:
 p=BASE/f'exports/Join_Me_in_Life_{name}_Proof.mp4';assert sha(p)==expected
 m=json.loads(p.with_suffix('.manifest.json').read_text());assert m['edit_config']['sha256']==CONFIG and m['output_sha256']==expected
 frames=decode(p);assert len(frames)==n
 hashes[label]=[hashlib.sha256(f.tobytes()).hexdigest() for f in frames]
 checks[label]={'path':str(p.relative_to(ROOT)),'sha256':expected,'frames':n,'source_start_seconds':m['audio']['source_start_seconds'],'author_audio_waveform_check':m['audio']['waveform_check'],'full_decode':'passed','manifest_sha256':sha(p.with_suffix('.manifest.json'))}
 if label.endswith('context'):
  cuts=[147,279] if label=='waiting-context' else [71,102,200,300,396]
  for cut in cuts:
   sheet(frames,f'{label}-cut-{cut:03}',list(range(cut-3,cut+3)),cols=2,size=(960,540))
   for i in [cut-1,cut]:Image.fromarray(frames[i]).save(OUT/f'{label}-native-{i:03}.jpg',quality=95)
  sheet(frames,label+'-overview',sorted(set(list(range(0,n,24))+[n-1]+[i for c in cuts for i in [c-1,c]])))
 else:
  source,lo,hi = ('R1W/R1L04',3,135) if label=='waiting' else ('R1H/R1L05',3,101) if label=='held30' else ('R1H/R1L05',101,197)
  src=BASE/f'assets/motion/ltx23-quiet-corrections/{source}/video-silent.mp4'
  vf=f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
  out=OUT/f'{label}-independent-reconstruction.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(out)],check=True)
  reference=decode(out); assert len(reference)==n
  equal=[np.array_equal(a,b) for a,b in zip(frames,reference)]
  checks[label]['independent_reconstruction']={'source_sha256':sha(src),'source_frames_zero_based':[lo,hi],'filter':vf,'reconstructed_sha256':sha(out),'all_decoded_frames_identical':all(equal),'identical_frames':sum(equal),'max_mean_abs_rgb_error':max(float(np.abs(a.astype(np.int16)-b.astype(np.int16)).mean()) for a,b in zip(frames,reference)),'encoding_crf':18}
  print(label,checks[label]['independent_reconstruction'],flush=True)
  edges=[]
  for f in frames:
   active=np.where(f[20:520].mean(axis=(0,2))>8)[0];edges.append((int(active[0]),int(959-active[-1])))
  checks[label]['mean_column_pad_widths']=sorted(set(edges))
  sheet(frames,label+'-encoded-phases',sorted(set(list(range(0,n,8))+[n-1])))
  for i in [0,n//2,n-1]:Image.fromarray(frames[i]).save(OUT/f'{label}-native-{i:03}.jpg',quality=95)
  del reference
 del frames;gc.collect()
checks['context_correspondence']={'waiting':hashes['waiting']==hashes['waiting-context'][147:279], 'held30':hashes['held30']==hashes['held-context'][102:200], 'held32':hashes['held32']==hashes['held-context'][300:396]}
assert all(checks['context_correspondence'].values())
(OUT/'encoded-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks['context_correspondence'])
