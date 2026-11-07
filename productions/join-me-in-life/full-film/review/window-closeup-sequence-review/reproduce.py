"""Independent fixed-window insertion proof. Writes evidence, never production inputs."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;FILM=HERE.parent.parent;ROOT=FILM.parents[2]
RAW=ROOT/'build/window-closeup-sequence-review';RAW.mkdir(parents=True,exist_ok=True)
FILES={
 'source':('assets/motion/ltx23-quiet-window-closeup/video-silent.mp4','5e61ec0d2b686a750e5c36f73fccc646544939dc10673f606153e3d098f8ec20'),
 'standalone':('exports/Join_Me_in_Life_Window_Closeup_Proof.mp4','dd1c70082c7ccd5bcc0f2dd5df147df0aee340e46695cf66a99c8ee322d8a9b6'),
 'context':('exports/Join_Me_in_Life_Window_Closeup_Context_Proof.mp4','3f42a3a6dcda31c121a6263a2883a743d1273d5bf8d6c425f701731552f0c646')}
paths={k:FILM/v[0] for k,v in FILES.items()}
for k,p in paths.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==FILES[k][1],k
review=FILM/'review/ltx23-window-closeup-review.md'
assert hashlib.sha256(review.read_bytes()).hexdigest()=='c4fedc811d96d96911b215af7df6af29ae889c0009c2a9228f6c37b1c06af748'
def decode(p,vf,w,h):
 b=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(p),'-map','0:v:0','-an','-vf',vf,'-fps_mode','passthrough','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(b,np.uint8).reshape(-1,h,w,3)
def hashes(p,vf=None):
 cmd=['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-an']
 if vf:cmd+=['-vf',vf,'-fps_mode','passthrough']
 s=subprocess.check_output(cmd+['-f','framemd5','-'],text=True)
 return [line.split(',')[-1].strip() for line in s.splitlines() if not line.startswith('#')]
expected=RAW/'independent-integer-trim.mp4'
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-threads','2','-i',str(paths['source']),
 '-vf','trim=start_frame=3:end_frame=157,setpts=PTS-STARTPTS,scale=960:540:flags=lanczos,setsar=1,format=yuv420p',
 '-an','-frames:v','154','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',
 '-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p',
 '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv',
 '-movflags','+faststart',str(expected)],check=True)
standalone=hashes(paths['standalone']);context=hashes(paths['context'],'trim=start_frame=151:end_frame=305,setpts=PTS-STARTPTS');independent=hashes(expected)
assert len(standalone)==154 and standalone==context==independent,'Decoded picture differs from independent whole-image [3,157) scaling'
m=json.loads(paths['context'].with_suffix('.manifest.json').read_text());origin=m['coverage']['start_frame']
assert m['edit_config']['sha256']=='e32955750fb6c65dcaf81e4304e5896f8d39b1e9c37ab1d397f69fd4095dcec2'
assert origin==156 and m['coverage']['end_frame_exclusive']==581
rows=[];selected=set();seams=[151,305]
for s in m['shots']:
 a,b=s['start_frame']-origin,s['end_frame_exclusive']-origin
 ns=[a,(a+b-1)//2,b-1];rows.append((s['id'],ns));selected.update(ns)
phases=list(range(151,305,12))+[304];selected.update(phases)
for seam in seams:selected.update([seam-2,seam-1,seam,seam+1])
selected=sorted(selected);vf='select='+'+'.join(f'eq(n\\,{n})' for n in selected)
rgb=decode(paths['context'],vf,960,540);frames={n:Image.fromarray(rgb[i]) for i,n in enumerate(selected)}
for n,im in frames.items():im.save(RAW/f'context-{n:04}.png')
sheet=Image.new('RGB',(1440,3*290),'#181818');d=ImageDraw.Draw(sheet)
for row,(sid,ns) in enumerate(rows):
 for col,n in enumerate(ns):
  x,y=col*480,row*290;d.text((x+4,y+4),f'{sid} {("first","middle","last")[col]} local {n} / full {n+origin}',fill='white')
  sheet.paste(frames[n].resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
sheet.save(HERE/'sequence.jpg',quality=89,subsampling=0)
for seam in seams:
 sheet=Image.new('RGB',(1920,565),'#181818');d=ImageDraw.Draw(sheet)
 for col,n in enumerate([seam-1,seam]):
  d.text((col*960+5,5),f'Context f{n} / full f{n+origin} / {(n+origin)/24:.6f}s',fill='white');sheet.paste(frames[n],(col*960,25))
 sheet.save(HERE/f'cut-{seam}.jpg',quality=89,subsampling=0)
sheet=Image.new('RGB',(1440,((len(phases)+2)//3)*290),'#181818');d=ImageDraw.Draw(sheet)
for i,n in enumerate(phases):
 x,y=i%3*480,i//3*290;d.text((x+5,y+5),f'S003 source {n-151+3} / context {n}',fill='white');sheet.paste(frames[n].resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
sheet.save(HERE/'encoded-phases.jpg',quality=89,subsampling=0)
native=decode(paths['source'],'select=eq(n\\,3)+eq(n\\,79)+eq(n\\,156)',672,378)
sheet=Image.new('RGB',(1632,3*565),'#181818');d=ImageDraw.Draw(sheet)
for row,(sn,cn) in enumerate(zip([3,79,156],[151,227,304])):
 y=row*565;d.text((5,y+5),f'Full derivative source f{sn} 672x378',fill='white');d.text((677,y+5),f'Encoded context f{cn} 960x540',fill='white')
 sheet.paste(Image.fromarray(native[row]),(0,y+25));sheet.paste(frames[cn],(672,y+25))
sheet.save(HERE/'source-versus-render.jpg',quality=89,subsampling=0)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(paths['context'])]))
pts_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(paths['context'])]))
pts=[float(f['best_effort_timestamp_time']) for f in pts_probe['frames']]
assert len(pts)==425
pts_error=max(abs(t-i/24) for i,t in enumerate(pts));assert pts_error<1e-6
report={'sources':{k:{'path':v[0],'sha256':v[1]} for k,v in FILES.items()},'reviewed_source_report_sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
 'config_sha256':m['edit_config']['sha256'],'full_context_frames':[156,581],'context_frames':425,
 'source_interval_zero_based':[3,157],'context_motion_interval_zero_based':[151,305],
 'independent_reconstruction':'Integer-frame trim [3,157), full 672x378 image uniformly scaled to 960x540, same CRF18 encoder. No crop, zoom, hold, loop or retiming.',
 'independent_and_standalone_and_context_all_decoded_frames_identical':True,'compared_frames':154,
 'context_streams':probe['streams'],'context_video_pts_max_error_from_index_over_24_seconds':pts_error,
 'audio_from_author_manifest':m['audio'],'audio_check_independently_rerun':False,'cuts_context_frames':seams,
 'scope':'Exact S003 insertion and S002/S004 cuts only; source review separately frozen, later windows and whole film unapproved.'}
(HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
