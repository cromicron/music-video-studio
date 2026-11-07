"""Frozen ending review: technical/visual evidence only; writes ignored build files.
Dependencies: FFmpeg, NumPy, Pillow, SciPy. No provider, editor/config or Git writes.
"""
from pathlib import Path
import hashlib,json,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from scipy.signal import correlate,correlation_lags
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').exists())
FILM=ROOT/'productions/join-me-in-life/full-film';OUT=ROOT/'build/positive-final-dawn-sequence-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'exports/Join_Me_in_Life_Positive_Final_Dawn_Context_Proof.mp4';MANIFEST=Path(__file__).parent/'frozen-manifest.json'
CONFIG=Path(__file__).parent/'frozen-edit.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)=='1421f2f36a1150dd42c84314f70e4ea044075ce58220f2348981617e6f8bddb7'
assert sha(CONFIG)=='96aa1e09b20fbda237bca6fa156c5cce3585fe2117fb80db82e2052758327c4f'
m=json.loads(MANIFEST.read_text());assert m['output_sha256']==sha(VIDEO)
def ff(*args):return subprocess.check_output(['ffmpeg','-v','error','-xerror',*args])
def decode(path,raw,flt=None):
 args=['ffmpeg','-v','error','-xerror','-y','-i',str(path),'-map','0:v:0']
 if flt:args+=['-vf',flt]
 subprocess.run(args+['-an','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo',str(raw)],check=True)
 return np.memmap(raw,mode='r',dtype=np.uint8).reshape(-1,540,960,3)
frames=decode(VIDEO,OUT/'context.rgb');assert len(frames)==588
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_frames','-show_entries','frame=media_type,best_effort_timestamp_time:stream=codec_type,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels','-of','json',str(VIDEO)]))
times=[float(f['best_effort_timestamp_time']) for f in probe['frames'] if f['media_type']=='video'];assert len(times)==588 and max(abs(t-i/24) for i,t in enumerate(times))<1e-6
assert sum(s['codec_type']=='audio' for s in probe['streams'])==1
checks={'output_sha256':sha(VIDEO),'manifest_sha256':sha(MANIFEST),'config_sha256':sha(CONFIG),'frames':588,'fps':24,'dimensions':[960,540],'timeline':[6079,6667],'duration_seconds':24.5,'complete_decode':True,'max_timestamp_error_seconds':max(abs(t-i/24) for i,t in enumerate(times)),'streams':probe['streams'],'shot_checks':{}}
contain='scale=960:540:force_original_aspect_ratio=decrease:force_divisible_by=4:flags=lanczos,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,format=yuv420p'
for shot in m['shots']:
 key=shot['id'];lo=shot['start_frame']-6079;hi=shot['end_frame_exclusive']-6079;motion=shot.get('motion')
 if motion:
  source=FILM/motion['path'];a,b=motion['reviewed_source_frames_zero_based'];assert sha(source)==motion['reviewed_source_sha256'];assert b-a==hi-lo
  flt=f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB),'+contain
  unfaded=decode(source,OUT/f'{key}-expected-unfaded.rgb',flt)
  if key=='S058':flt+=',fade=t=out:st=4.583333333333333:d=2'
  expected=decode(source,OUT/f'{key}-expected.rgb',flt)
 else:
  source=FILM/shot['source']['path'];assert sha(source)==shot['source']['sha256']
  flt=json.loads((Path(__file__).parent/'shot-filters.json').read_text())[key]['filter']
  expected=decode(source,OUT/f'{key}-expected.rgb',flt)
 assert len(expected)==hi-lo
 actual=frames[lo:hi];mae=[float(np.abs(a.astype(np.int16)-b.astype(np.int16)).mean()) for a,b in zip(actual,expected)]
 checks['shot_checks'][key]={'context_interval':[lo,hi],'timeline_interval':[lo+6079,hi+6079],'frames':hi-lo,'source_sha256':sha(source),'expected_filter':flt,'expected_to_export_rgb_mae_mean':float(np.mean(mae)),'expected_to_export_rgb_mae_max':max(mae),'per_frame_mae':mae,'unique_decoded_export_frames':len({hashlib.sha256(a.tobytes()).hexdigest() for a in actual})}
 assert max(mae)<6
 if motion:
  checks['shot_checks'][key].update({'source_interval':[a,b],'contain_rectangle':[8,0,944,540],'max_outer_six_pixel_side_padding_rgb':int(max(actual[:,:,:6].max(),actual[:,:,954:].max())),'lead_hold_frames':0,'endpoint_hold_frames':0})
 if key=='S058':
  fade=[]
  for i in range(107,158):
   f=actual[i];u=unfaded[i];fade.append({'shot_frame':i,'source_frame':i+3,'context_frame':lo+i,'timeline_frame':6509+i,'rgb_mean':float(f.mean()),'rgb_max':int(f.max()),'rgb_99_percentile':float(np.percentile(f,99)),'unfaded_rgb_mean':float(u.mean()),'brightness_ratio':float(f.mean()/u.mean())})
  checks['fade']={'planned_source_interval':[113,161],'planned_timeline_interval':[6619,6667],'planned_context_interval':[540,588],'samples':fade,'last_frame_all_rgb_zero':bool(not actual[-1].any()),'last_frame_rgb_min':int(actual[-1].min()),'last_frame_rgb_max':int(actual[-1].max()),'last_frame_rgb_mean':float(actual[-1].mean())}

audio=FILM/'../full-song/track-49.mp3';assert sha(audio)==m['audio']['original_audio_sha256']
def pcm(path,flt=None):
 args=['-i',str(path),'-vn']
 if flt:args+=['-af',flt]
 return np.frombuffer(ff(*args,'-ac','1','-ar','4000','-f','f32le','-'),np.float32)
x_trim=pcm(audio,'atrim=start=253.29166666666666:end=277.7916666666667,asetpts=PTS-STARTPTS');x=np.frombuffer(ff('-ss',str(6079/24),'-i',str(audio),'-t','24.5','-vn','-ac','1','-ar','4000','-f','f32le','-'),np.float32);y=pcm(VIDEO);n=min(len(x),len(y));xx=x[:n];yy=y[:n]
c=correlate(yy,xx,mode='full',method='fft');lags=correlation_lags(len(yy),len(xx),mode='full');mask=np.abs(lags)<=400;lag=int(lags[mask][np.argmax(c[mask])]);corr=float(np.corrcoef(xx,yy)[0,1])
checks['audio']={'source_sha256':sha(audio),'source_excerpt_method':'input seek at exact master frame, matching actual renderer; independently decoded atrim comparison also retained','independent_atrim_zero_lag_correlation':float(np.corrcoef(x_trim[:min(len(x_trim),len(y))],y[:min(len(x_trim),len(y))])[0,1]),'source_start_seconds':6079/24,'sample_rate':4000,'source_samples':len(x),'output_samples':len(y),'alignment_lag_samples':lag,'alignment_lag_seconds':lag/4000,'correlation_at_zero_lag':corr,'output_audio_duration_from_decoded_samples':len(y)/4000,'source_audio_duration_from_decoded_samples':len(x)/4000,'last_half_second_rms':float(np.sqrt(np.mean(y[-2000:]**2))),'last_100ms_rms':float(np.sqrt(np.mean(y[-400:]**2))),'last_10ms_rms':float(np.sqrt(np.mean(y[-40:]**2))),'note':'Decoded signal alignment and tail values; not subjective listening or lyric/phoneme verification.'};assert corr>.999 and lag==0

def sheet(ids,crop,cols,size,name):
 w,h=size;out=Image.new('RGB',(w*cols,math.ceil(len(ids)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(out)
 for j,i in enumerate(ids):
  im=Image.fromarray(frames[i]).crop(crop);im=ImageOps.contain(im,size);x,y=j%cols*w,j//cols*(h+24);d.text((x+4,y+5),f'local {i:03} | master {6079+i} | {i/24:.3f}s',fill='white');out.paste(im,(x+(w-im.width)//2,y+24))
 out.save(OUT/name,quality=94)
sheet([0,73,144,146,147,171,219,267,292,293,361,429,430,454,478,502,526,539,540,552,564,576,587],(0,0,960,540),4,(480,270),'context-phases.jpg')
for join in [147,293,430]:sheet(list(range(join-3,join+4)),(0,0,960,540),2,(960,540),f'join-{join:03}-native.jpg')
for lo,hi,shot in [(147,293,'S056'),(430,588,'S058')]:
 for a in range(lo,hi,16):sheet(list(range(a,min(a+16,hi))),(0,0,960,540),4,(480,270),f'{shot}-all-{a:03}-{min(a+16,hi)-1:03}.jpg')
 ids=[lo,lo+24,lo+48,lo+72,lo+96,min(lo+120,hi-1),hi-1]
 sheet(ids,(220,60,600,300),3,(380,240),f'{shot}-faces-native.jpg')
 sheet(ids,(310,325,670,510),3,(360,185),f'{shot}-hands-native.jpg')
for lo in [540,556,572]:sheet(list(range(lo,min(lo+16,588))),(0,0,960,540),4,(480,270),f'fade-{lo:03}-{min(lo+16,588)-1:03}.jpg')
for i in [146,147,292,293,429,430,539,540,564,576,580,584,585,586,587]:Image.fromarray(frames[i]).save(OUT/f'frame-{i:03}.png')
sheet([576,580,584,585,586,587],(0,0,960,540),2,(960,540),'ending-native.jpg')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({**{k:v for k,v in checks.items() if k not in ['shot_checks','fade']},'shot_checks':{k:{a:b for a,b in v.items() if a!='per_frame_mae'} for k,v in checks['shot_checks'].items()},'fade':{k:v for k,v in checks['fade'].items() if k!='samples'}},indent=2))
