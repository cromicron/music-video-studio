"""Independent P2L10/P2L11 source-review evidence. No source or edit mutations.

Writes exhaustive sheets/proxies to ignored build/<review-directory>; compact
evidence/checks beside this script. Frame labels are zero-based throughout.
Dependencies: numpy, Pillow, FFmpeg/ffprobe. Playback is a separate script.
"""
from pathlib import Path
import hashlib, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'studio.json').is_file())
BASE = ROOT / 'productions/join-me-in-life/full-film'
TAKE = HERE.name.split('-')[2]
CONFIG = {
    'P2L10': {'sha': '3ab5bd418d93e38731aa19357b83f00072b6c6365ff0fdc4e16858128955a650', 'count': 137, 'guide': BASE / 'assets/summer_identity_end_v2_candidate.png', 'actor': (170,20,700,500), 'phases': [0,3,24,36,48,60,72,84,96,108,125,136], 'detail': (205,20,660,260), 'hands': (180,240,680,490)},
    'P2L11': {'sha': 'f7a168bcb68d4678fd39aea91b8f6aeadcf6aa14103c32b96175ba7a8015f703', 'count': 201, 'guide': BASE.parent / 'art/03_Story/S06_Still_Here_At_Dawn.png', 'actor': (235,0,790,512), 'phases': [0,3,24,48,72,98,99,120,144,168,193,200], 'detail': (260,0,665,290), 'hands': (240,280,790,512)},
}[TAKE]
ASSET = BASE / f'assets/motion/ltx23-positive-continuation/P2/{TAKE}'
OUT = ROOT / 'build' / HERE.name
OUT.mkdir(parents=True, exist_ok=True)
VIDEO = ASSET / 'video-silent.mp4'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO) == CONFIG['sha']
raw = subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(VIDEO),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
frames = np.frombuffer(raw,np.uint8).reshape(-1,512,896,3)
assert len(frames) == CONFIG['count']
np.save(OUT / 'frames.npy',frames)
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_frames','-show_entries','frame=best_effort_timestamp_time:stream=codec_type,width,height,r_frame_rate,nb_frames','-of','json',str(VIDEO)]))
assert not any(s['codec_type'] == 'audio' for s in probe['streams'])
times = [float(f['best_effort_timestamp_time']) for f in probe['frames']]
assert len(times) == len(frames) and max(abs(t-i/24) for i,t in enumerate(times)) < 1e-5
stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
assert [stream['width'], stream['height'], stream['r_frame_rate']] == [896,512,'24/1']
render = json.loads((ASSET / 'render.json').read_text())
assert render['status'] == 'complete' and render['video']['sha256'] == sha(VIDEO)
assert sha(CONFIG['guide']) == render['manifest']['start_image_sha256'] == render['manifest']['end_image_sha256']
provenance = BASE / f'tools/kaggle-story23/provenance/{TAKE}-provenance.json'
assert sha(provenance) == render['manifest']['source_provenance_sha256']
start = np.asarray(Image.open(ASSET / 'start-fitted.png').convert('RGB'))
end = np.asarray(Image.open(ASSET / 'end-fitted.png').convert('RGB'))
assert np.array_equal(start,end)
rgb_hash = hashlib.sha256(start.tobytes()).hexdigest()
assert rgb_hash == render['input_fitting']['start']['rgb_sha256'] == render['input_fitting']['end']['rgb_sha256']
assert {(x['guide'],x['stage'],x['frame_index']) for x in render['image_guides']} == {('start',1,0),('start',2,0),('end',1,len(frames)-1),('end',2,len(frames)-1)}
assert all(x['rgb_sha256'] == rgb_hash for x in render['image_guides'])

def sheet(items,cols,size,name,compact=False):
    w,h = size
    canvas = Image.new('RGB',(cols*w,math.ceil(len(items)/cols)*(h+24)),'#171717')
    draw = ImageDraw.Draw(canvas)
    for j,(label,im) in enumerate(items):
        x,y = (j%cols)*w,(j//cols)*(h+24)
        draw.text((x+4,y+4),label,fill='white')
        im = ImageOps.contain(im,size)
        canvas.paste(im,(x+(w-im.width)//2,y+24+(h-im.height)//2))
    canvas.save(OUT / name,quality=93)
    if compact: (HERE / name).write_bytes((OUT / name).read_bytes())

for first in range(0,len(frames),24):
    sheet([(f'f{i:03}',Image.fromarray(frames[i])) for i in range(first,min(first+24,len(frames)))],6,(224,128),f'all-full-{first:03}.jpg')
box = CONFIG['actor']
for first in range(0,len(frames),12):
    sheet([(f'f{i:03}',Image.fromarray(frames[i]).crop(box)) for i in range(first,min(first+12,len(frames)))],3,(box[2]-box[0],box[3]-box[1]),f'actors-{first:03}.jpg')
ids = CONFIG['phases']
sheet([(f'f{i:03} | {i/24:.3f}s',Image.fromarray(frames[i])) for i in ids],3,(448,256),'overview.jpg',True)
for key,name in [('detail','identity-phases.jpg'),('hands','hands-support.jpg')]:
    box = CONFIG[key]
    sheet([(f'f{i:03} | native crop',Image.fromarray(frames[i]).crop(box)) for i in ids],3,(box[2]-box[0],box[3]-box[1]),name,True)
sheet([('Original source guide',Image.open(CONFIG['guide'])),('Fitted guide (both ends)',Image.fromarray(start)),('Actual f000',Image.fromarray(frames[0])),(f'Actual f{len(frames)-1:03}',Image.fromarray(frames[-1]))],2,(896,512),'guides-endpoints.jpg',True)
eye_box = (490,80,610,185) if TAKE == 'P2L10' else (290,135,395,215)
eye_ids = [0,24,48,60,96,125,136] if TAKE == 'P2L10' else [0,24,48,98,144,193,200]
eye_size = ((eye_box[2]-eye_box[0])*4,(eye_box[3]-eye_box[1])*4)
eye_items = [('Fitted guide | 4x nearest',Image.fromarray(start).crop(eye_box))] + [(f'f{i:03} | 4x nearest',Image.fromarray(frames[i]).crop(eye_box)) for i in eye_ids]
sheet([(label,im.resize(eye_size,Image.Resampling.NEAREST)) for label,im in eye_items],4,eye_size,'eye-comparison.jpg',True)
if TAKE == 'P2L11':
    sheet([(f'f{i:03} | native crown',Image.fromarray(frames[i]).crop((435,0,665,160))) for i in [0,12,24,36,48,60,72,84,98,99,120,150]],4,(230,160),'crown-phases.jpg',True)
    sheet([(f'f{i:03} | native corridor',Image.fromarray(frames[i]).crop((780,80,896,430))) for i in range(112,169,4)],8,(116,350),'corridor-phases.jpg',True)
    for first in range(112,176,16):
        sheet([(f'f{i:03}',Image.fromarray(frames[i]).crop((780,80,896,430))) for i in range(first,first+16)],8,(116,350),f'corridor-all-{first}.jpg')
segments = []
specs = [(s['shot_id'],*s['source_frames']) for s in render['manifest']['editorial']['segments']]
if TAKE == 'P2L11': specs.append(('continuous-S050-S051',3,194))
for key,lo,hi in specs:
    path = OUT / f'{key}-selected.mp4'
    subprocess.run(['ffmpeg','-v','error','-xerror','-y','-i',str(VIDEO),'-vf',f'trim=start_frame={lo}:end_frame={hi},setpts=N/(24*TB)','-an','-r','24','-fps_mode','cfr','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(path)],check=True)
    p = json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]
    assert int(p['nb_read_frames']) == hi-lo and abs(float(p['duration'])-(hi-lo)/24) < 1e-5
    segments.append({'shot':key,'source_frames_zero_based_end_exclusive':[lo,hi],'source_seconds':[lo/24,hi/24],'frames':hi-lo,'duration_seconds':(hi-lo)/24,'proxy_sha256':sha(path)})
references = [BASE.parent / 'art/00_References/A01_Approved_Character_Pair.jpg',BASE.parent / 'art/00_References/A02_Approved_Anime_Window.png']
checks = {'take':TAKE,'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [VIDEO,ASSET/'render.json',ASSET/'start-fitted.png',ASSET/'end-fitted.png',CONFIG['guide'],provenance,*references]},'manifest_sha256_recorded':render['manifest_sha256'],'frames':len(frames),'fps':24,'dimensions':[896,512],'duration_seconds':len(frames)/24,'audio_streams':0,'full_error_failing_decode':True,'guide_pixels_identical':True,'guide_rgb_sha256':rgb_hash,'four_guide_records_both_stages_verified':True,'source_native_dimensions':list(Image.open(CONFIG['guide']).size),'input_fitting':render['input_fitting'],'max_timestamp_error_seconds':max(abs(t-i/24) for i,t in enumerate(times)),'segments':segments,'labels':'zero-based; intervals end-exclusive','scope':'Technical and provenance checks do not establish identity, motion quality or final-edit approval.'}
for folder in [OUT,HERE]: (folder/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
