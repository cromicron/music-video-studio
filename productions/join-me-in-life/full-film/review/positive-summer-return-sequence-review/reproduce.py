"""Hash-bound context proof review. Independent integer trims, not editor calls.

Writes exhaustive sheets, decoded arrays and reconstructed motion to ignored
build/<review-directory>. Compact evidence/checks are retained beside script.
"""
from pathlib import Path
import hashlib,json,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'studio.json').is_file())
FILM=ROOT/'productions/join-me-in-life/full-film'
OUT=ROOT/'build'/HERE.name
OUT.mkdir(parents=True,exist_ok=True)
SUMMER='summer' in HERE.name
TITLE='Summer_Return' if SUMMER else 'Indoor_Dawn'
VIDEO=FILM/f'exports/Join_Me_in_Life_Positive_{TITLE}_Context_Proof.mp4'
EXPECTED='a0eb758d9b68d66a0e2ae75b71516ef9348e9aa3451e2548e6f4e31755fa0ed4' if SUMMER else 'fd5717d9f108e497fa1d8fa0f0fb766d9abd71a1a55a81408cdb8cb9cce6f173'
MANIFEST_SHA='1342cff50c7546de26beb04cd307965694c7642a87fab7de9a4496b8a86e61bb' if SUMMER else '3599444ac0df815570eb1a9073dbc0b3dcc16d0b3286f445ef3e41877a2d1afb'
CONFIG_SHA='96aa1e09b20fbda237bca6fa156c5cce3585fe2117fb80db82e2052758327c4f'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)==EXPECTED
assert sha(HERE/'frozen-manifest.json')==MANIFEST_SHA
assert sha(HERE/'frozen-edit.json')==CONFIG_SHA
manifest=json.loads((HERE/'frozen-manifest.json').read_text())
assert manifest['output_sha256']==EXPECTED and manifest['edit_config']['sha256']==CONFIG_SHA
START,END=(4113,4483) if SUMMER else (5462,5842)
COUNT=END-START
assert manifest['coverage']=={'start_frame':START,'end_frame_exclusive':END,'full_song':False}
assert manifest['frames']==COUNT

subprocess.run(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-map','0','-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(VIDEO)]))
vs=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (vs['width'],vs['height'],vs['avg_frame_rate'],int(vs['nb_frames']))==(960,540,'24/1',COUNT)
audio=[s for s in probe['streams'] if s['codec_type']=='audio']
assert len(audio)==1 and audio[0]['codec_name']=='aac' and int(audio[0]['channels'])==2
pts_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(VIDEO)]))
pts=[float(f['best_effort_timestamp_time']) for f in pts_probe['frames']]
assert len(pts)==COUNT
pts_error=max(abs(t-i/24) for i,t in enumerate(pts))
assert pts_error<1e-6

def md5(path):
    text=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(path),'-map','0:v:0','-an','-fps_mode','passthrough','-pix_fmt','yuv420p','-f','framemd5','-'],text=True)
    return [line.rsplit(',',1)[1].strip() for line in text.splitlines() if not line.startswith('#')]

actual=md5(VIDEO)
assert len(actual)==COUNT
insertions=[]
for shot in manifest['shots']:
    motion=shot['motion']
    if not motion:continue
    src=FILM/motion['path'];assert sha(src)==motion['source_sha256']==motion['reviewed_source_sha256']
    assert sha(FILM/motion['review']['path'])==motion['review']['sha256']
    lo,hi=motion['reviewed_source_frames_zero_based']
    a,b=shot['start_frame']-START,shot['end_frame_exclusive']-START
    assert b-a==hi-lo==motion['used_frames']
    assert motion['lead_in_frames']==motion['endpoint_hold_frames']==0
    assert motion['framing_policy']=='contain'
    assert shot['camera']=={'zoom_start':1.0,'zoom_end':1.0,'center_start':[.5,.5],'center_end':[.5,.5]}
    vf=f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
    independent=OUT/f'{shot["id"]}-independent.mp4'
    cmd=['ffmpeg','-v','error','-xerror','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(hi-lo),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(independent)]
    subprocess.run(cmd,check=True)
    expected=md5(independent)
    assert expected==actual[a:b],(shot['id'],'decoded motion differs from independent integer-frame reconstruction')
    insertions.append({'shot':shot['id'],'source_path':motion['path'],'source_sha256':sha(src),'source_frames_zero_based_end_exclusive':[lo,hi],'context_frames_zero_based_end_exclusive':[a,b],'master_frames_zero_based_end_exclusive':[START+a,START+b],'frames_compared':len(expected),'all_decoded_pictures_identical_to_independent_integer_trim_containment_encode':True,'filter':vf,'contain_rectangle_xywh':[8,0,944,540],'reconstructed_sha256':sha(independent),'unique_decoded_pictures':len(set(expected))})

rgbpath=OUT/'frames.rgb'
subprocess.run(['ffmpeg','-v','error','-xerror','-y','-threads','2','-i',str(VIDEO),'-map','0:v:0','-an','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo',str(rgbpath)],check=True)
assert rgbpath.stat().st_size==COUNT*540*960*3
frames=np.memmap(rgbpath,dtype=np.uint8,mode='r',shape=(COUNT,540,960,3))

def sheet(ids,cols,size,name,box=None,retain=False):
    w,h=size;canvas=Image.new('RGB',(cols*w,math.ceil(len(ids)/cols)*(h+24)),'#171717');d=ImageDraw.Draw(canvas)
    for j,n in enumerate(ids):
        x,y=(j%cols)*w,(j//cols)*(h+24);im=Image.fromarray(frames[n]);im=im.crop(box) if box else im;im=ImageOps.contain(im,size)
        label=f'local f{n:03}' if w<300 else f'local f{n:03} | master f{n+START} | {n/24:.3f}s'
        d.text((x+4,y+4),label,fill='white');canvas.paste(im,(x,y+24))
    canvas.save(OUT/name,quality=94)
    if retain:(HERE/name).write_bytes((OUT/name).read_bytes())

cuts=[s['start_frame']-START for s in manifest['shots'][1:]]
phases=[]
for shot in manifest['shots']:
    a,b=shot['start_frame']-START,shot['end_frame_exclusive']-START;phases.extend([a,(a+b-1)//2,b-1])
sheet(phases,3,(480,270),'context-overview.jpg',retain=True)
for cut in cuts:
    sheet([cut-1,cut],2,(960,540),f'cut-{cut:03}-native.jpg',retain=True)
    sheet(list(range(cut-6,cut+6)),4,(480,270),f'cut-{cut:03}-phases.jpg',retain=True)
for first in range(0,COUNT,24):sheet(list(range(first,min(first+24,COUNT))),6,(240,135),f'all-context-{first:03}.jpg')
actor=(185,10,745,520) if SUMMER else (250,0,840,540)
for ins in insertions:
    a,b=ins['context_frames_zero_based_end_exclusive']
    for first in range(a,b,12):sheet(list(range(first,min(first+12,b))),3,(actor[2]-actor[0],actor[3]-actor[1]),f'{ins["shot"]}-actors-{first:03}.jpg',box=actor)
    selected=sorted(set([a,a+min(12,b-a-1),a+(b-a)//3,a+(b-a)*2//3,b-1]))
    sheet(selected,3,(960,540),f'{ins["shot"]}-full-phases.jpg',retain=True)
    box=(220,25,700,290) if SUMMER else (275,0,710,305)
    sheet(selected,3,(box[2]-box[0],box[3]-box[1]),f'{ins["shot"]}-identity-phases.jpg',box=box,retain=True)
    box=(195,250,720,520) if SUMMER else (255,300,840,540)
    sheet(selected,3,(box[2]-box[0],box[3]-box[1]),f'{ins["shot"]}-hands-support.jpg',box=box,retain=True)
if not SUMMER:
    sheet([120,132,144,156,168,180],3,(260,180),'crown-phases.jpg',box=(460,0,720,180),retain=True)
    sheet(list(range(208,256,4)),6,(130,380),'corridor-phases.jpg',box=(830,80,960,460),retain=True)

audio_source=(FILM/json.loads((HERE/'frozen-edit.json').read_text())['audio']).resolve()
assert sha(audio_source)==manifest['audio']['original_audio_sha256']
def pcm(path,start=None,duration=None):
    cmd=['ffmpeg','-v','error','-xerror','-threads','2']
    if start is not None:cmd+=['-ss',str(start)]
    cmd+=['-i',str(path)]
    if duration is not None:cmd+=['-t',str(duration)]
    raw=subprocess.check_output(cmd+['-vn','-ac','1','-ar','4000','-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4').astype(np.float64)
source_pcm=pcm(audio_source,START/24,COUNT/24);output_pcm=pcm(VIDEO);n=min(len(source_pcm),len(output_pcm))
corr=float(np.corrcoef(source_pcm[:n],output_pcm[:n])[0,1]);assert corr>.995
checks={'context_sha256':EXPECTED,'manifest_sha256':MANIFEST_SHA,'config_sha256':CONFIG_SHA,'context_path':str(VIDEO.relative_to(ROOT)),'master_frames_zero_based_end_exclusive':[START,END],'context_frames':COUNT,'fps':24,'dimensions':[960,540],'all_streams_error_failing_decode':'passed','video_pts_max_error_seconds':pts_error,'insertions':insertions,'actual_join_local_frames':cuts,'actual_join_master_frames':[c+START for c in cuts],'streams':probe['streams'],'audio_source_sha256':sha(audio_source),'independent_audio_check':{'method':'4000-Hz mono float PCM, Pearson correlation at expected source start; no lag search or subjective hearing','source_start_seconds':START/24,'source_samples':len(source_pcm),'output_samples':len(output_pcm),'samples_compared':n,'correlation_at_expected_offset':corr},'source_audio_manifest':manifest['audio'],'scope':'Exact decoded insertion pictures, actual neighboring cuts and local proof; not whole-film acceptance or subjective listening.'}
for folder in [OUT,HERE]:(folder/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({'insertions':insertions,'audio_correlation':corr,'frames':COUNT,'cuts':cuts},indent=2))
