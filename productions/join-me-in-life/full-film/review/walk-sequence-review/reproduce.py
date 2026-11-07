"""Independent encoded insertion/cut evidence; never changes production inputs."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
REPO=FILM.parents[2]
RAW=REPO/'build/walk-sequence-review'
RAW.mkdir(parents=True,exist_ok=True)
SOURCES={
 'source':('assets/motion/ltx23-walk-pilot/video-silent.mp4','fd21e3d9d84a6f9b565e67d3bcd6aa142e7c1cefe2d48f68d13e6f5ebc120f21'),
 'standalone':('exports/Join_Me_in_Life_Snow_Walk_Proof.mp4','36fc7ea98c76365333862f3461022bb6bc26ee805fd85466e616cfc84cd81731'),
 'context':('exports/Join_Me_in_Life_Snow_Walk_Context_Proof.mp4','df686da204c4f07f3023680f4f5f24713fe69fdc379e9ea9db37a1ef7119aa7a')}
paths={k:FILM/v[0] for k,v in SOURCES.items()}
for k,p in paths.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==SOURCES[k][1],k
def decode(path,vf,width,height):
 b=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(path),'-map','0:v:0','-an','-vf',vf,'-vsync','0','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(b,np.uint8).reshape(-1,height,width,3)
def framehash(path,vf=None):
 cmd=['ffmpeg','-v','error','-i',str(path),'-map','0:v:0']
 if vf:cmd+=['-vf',vf,'-vsync','0']
 s=subprocess.check_output(cmd+['-f','framemd5','-'],text=True)
 return [x.split(',')[-1].strip() for x in s.splitlines() if not x.startswith('#')]
def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]))['streams']

fill='scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1'
src=decode(paths['source'],fill+',scale=480:270:flags=area',480,270)
out=decode(paths['standalone'],'scale=480:270:flags=area',480,270)
assert len(src)==145 and len(out)==132
# Compare every encoded output against all source frames, within a broad actor
# region, so the stable background cannot conceal a repeated/omitted action frame.
actor=(slice(90,260),slice(105,370))
sr=src[:,actor[0],actor[1]].astype(np.float32)
matches=[];expected_mse=[];next_best=[]
for i,frame in enumerate(out):
 err=np.mean((sr-frame[actor[0],actor[1]].astype(np.float32))**2,axis=(1,2,3))
 matches.append(int(err.argmin()));expected_mse.append(float(err[i+3]))
 next_best.append(float(np.min(np.delete(err,i+3))))
# Near-static neighboring poses can be closer after lossy compression; nearest
# pixels alone are therefore recorded, not asserted as proof of exact cadence.
standalone_hashes=framehash(paths['standalone'])
context_hashes=framehash(paths['context'],'select=between(n\\,113\\,244)')
assert standalone_hashes==context_hashes and len(standalone_hashes)==132
expected=RAW/'independent-frame-trim.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2',
 '-i',str(paths['source']),'-vf','trim=start_frame=3:end_frame=135,setpts=PTS-STARTPTS,'+fill+',format=yuv420p',
 '-an','-frames:v','132','-c:v','libx264','-preset','veryfast','-crf','20','-threads','3',
 '-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p',
 '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv',
 '-movflags','+faststart',str(expected)],check=True)
expected_hashes=framehash(expected)
assert expected_hashes==standalone_hashes,'Independent integer-frame trim differs from delivered sequence'

m=json.loads(paths['context'].with_suffix('.manifest.json').read_text())
assert m['edit_config']['sha256']=='ad8047b88e94267a02ffdd25b3d3d7a16cf2c382e98b89422fc412e8fe6abb10'
origin=m['coverage']['start_frame'];selected=set();rows=[]
for s in m['shots']:
 a,b=s['start_frame']-origin,s['end_frame_exclusive']-origin
 ns=[a,(a+b-1)//2,b-1];selected.update(ns);rows.append((s['id'],ns))
seams=[113,245,348]
for n in seams:selected.update([n-2,n-1,n,n+1])
selected=sorted(selected)
vf='select='+'+'.join(f'eq(n\\,{n})' for n in selected)
rgb=decode(paths['context'],vf,960,540)
frames={n:Image.fromarray(rgb[i]) for i,n in enumerate(selected)}
for n,im in frames.items():im.save(RAW/f'context-{n:04}.png')
sheet=Image.new('RGB',(1440,len(rows)*290),'#181818');d=ImageDraw.Draw(sheet)
for row,(shot,ns) in enumerate(rows):
 for col,n in enumerate(ns):
  x,y=col*480,row*290
  d.text((x+4,y+4),f'{shot} {("first","middle","last")[col]} local {n} full {n+origin}',fill='white')
  sheet.paste(frames[n].resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
sheet.save(HERE/'sequence.jpg',quality=88,subsampling=0)
for seam in seams:
 sheet=Image.new('RGB',(1920,570),'#181818');d=ImageDraw.Draw(sheet)
 for col,n in enumerate([seam-1,seam]):
  d.text((col*960+8,7),f'Context local f{n} / full f{n+origin} / {(n+origin)/24:.6f}s',fill='white')
  sheet.paste(frames[n],(col*960,30))
 sheet.save(HERE/f'cut-{seam}.jpg',quality=90,subsampling=0)
# Source and encoded full views for the actual three retained endpoints.
native=decode(paths['source'],'select=eq(n\\,3)+eq(n\\,68)+eq(n\\,134)',896,512)
sheet=Image.new('RGB',(1856,3*570),'#181818');d=ImageDraw.Draw(sheet)
for row,(sn,cn) in enumerate(zip([3,68,134],[113,178,244])):
 d.text((8,row*570+7),f'Source zero-based f{sn} | 896x512',fill='white')
 d.text((904,row*570+7),f'Encoded context f{cn} | 960x540 fixed fill',fill='white')
 sheet.paste(Image.fromarray(native[row]),(0,row*570+30))
 sheet.paste(frames[cn],(896,row*570+30))
sheet.save(HERE/'source-versus-fill.jpg',quality=89,subsampling=0)
report={'sources':{k:{'path':str(p.relative_to(FILM)),'sha256':SOURCES[k][1],'streams':probe(p)} for k,p in paths.items()},
 'config_sha256':m['edit_config']['sha256'],'full_coverage':[1099,1596],
 'source_frame_mapping':{'method':'Independent integer-frame trim [3,135), fixed fill and same CRF20 encoder; all decoded output frames match proof exactly','source_zero_based':[3,135],'independent_trim_all_decoded_frames_identical':True,'expected_mse_max':max(expected_mse),'lossy_nearest_neighbor_test_note':'Not used as exact cadence proof: near-identical adjacent poses and codec loss make some nearest-frame results ambiguous.','nearest_source_indices':matches},
 'standalone_and_context_decoded_video_frames_identical':True,'compared_frames':132,
 'audio_check_from_author_render_manifest':m['audio'],'audio_check_independently_rerun':False,
 'cuts_context_frames':seams,'scope':'Exact insertion, framing and surrounding cuts; accepted source gait reviewed separately.'}
(HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['config_sha256','standalone_and_context_decoded_video_frames_identical','compared_frames','cuts_context_frames']}))
print('Independent integer-frame trim produces the same 132 decoded frames as both delivered proofs.')
