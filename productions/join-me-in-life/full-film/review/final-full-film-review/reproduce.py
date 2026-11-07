"""Stream the frozen full film; retain selected pictures, never a full raw dump."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
ROOT=FILM.parents[2]
VIDEO=ROOT/'build/Join_Me_in_Life_Full_Music_Video_QC.mp4'
OUT=ROOT/'build/final-full-film-review'
OUT.mkdir(parents=True,exist_ok=True)
EXPECTED='ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==EXPECTED
assert hashlib.sha256((HERE/'frozen-manifest.json').read_bytes()).hexdigest()=='f1c5acd977edd5324682308654b5988de81975766c0f01bd9960a508b4217110'
assert hashlib.sha256((HERE/'frozen-edit.json').read_bytes()).hexdigest()=='1857d2254ade658a66faeb8419ec5fb1a22c831a2baa0bd958aecb2d3b0a3413'
manifest=json.loads((HERE/'frozen-manifest.json').read_text())
shots=manifest['shots']; by_id={s['id']:s for s in shots}
assert len(shots)==58 and shots[0]['start_frame']==0 and shots[-1]['end_frame_exclusive']==6667
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(shots,shots[1:]))
assert manifest['output_sha256']==EXPECTED
import sys
reuse_decode='--reuse-decode' in sys.argv
md5=(OUT/'full-video.framemd5').read_text() if reuse_decode else subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-map','0:v:0','-an','-f','framemd5','-'],text=True)
(OUT/'full-video.framemd5').write_text(md5)
decoded=[line for line in md5.splitlines() if not line.startswith('#')]
assert len(decoded)==6667
subprocess.run(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-map','0:a:0','-vn','-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(VIDEO)]))
pts_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(VIDEO)]))
pts=[float(f['best_effort_timestamp_time']) for f in pts_probe['frames']]
pts_error=max(abs(t-i/24) for i,t in enumerate(pts)); assert len(pts)==6667 and pts_error<1e-6
print('Full video/audio decode and 6667-frame cadence passed.',flush=True)

overview={s['id']:[s['start_frame'],(s['start_frame']+s['end_frame_exclusive']-1)//2,s['end_frame_exclusive']-1] for s in shots}
key_ids=['S020','S021','S025','S026','S027','S028','S029','S030','S032','S033','S034','S041','S042','S043','S044','S045','S046','S047','S048','S050','S051','S052','S053','S054','S056','S057','S058']
cuts={sid:list(range(by_id[sid]['start_frame']-3,by_id[sid]['start_frame']+3)) for sid in key_ids}
phases={
 'summer':sorted(set([2838,2900,2901,2902,2947,2948,2949,2950,3020]+list(range(2901,3021,8)))),
 'embrace':sorted(set([3133,3223,3224,3225,3226,3344,3345,3346,3347,3423]+list(range(3225,3346,4)))),
 'pleas':list(range(4989,5364,8))+[5069,5070,5182,5183,5264,5265,5363],
 'held':sorted(set(n for sid in ['S030','S032','S033','S034','S041','S042','S043','S045','S047'] for n in range(by_id[sid]['start_frame'],by_id[sid]['end_frame_exclusive'],12))),
 'dawn':sorted(set(n for sid in ['S050','S051','S053','S056','S058'] for n in range(by_id[sid]['start_frame'],by_id[sid]['end_frame_exclusive'],12))),
 'branding':[0,8,18,48,72,99,107,115,116,155],
 'final-fade':[6509,6550,6600,6618,6619,6620,6631,6643,6655,6666]
}
indices=sorted(set(n for group in list(overview.values())+list(cuts.values())+list(phases.values()) for n in group))

def selection(ids):
    ranges=[]
    for n in sorted(set(ids)):
        if ranges and n==ranges[-1][1]+1:ranges[-1][1]=n
        else:ranges.append([n,n])
    def balanced(terms):
        if len(terms)==1:return terms[0]
        k=len(terms)//2;return '('+balanced(terms[:k])+'+'+balanced(terms[k:])+')'
    return 'select='+balanced([f'between(n\\,{a}\\,{b})' for a,b in ranges])

def read_selected(ids,w,h):
    cmd=['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-an','-vf',selection(ids)+f',scale={w}:{h}:flags=lanczos','-fps_mode','passthrough','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE);result={}; count=w*h*3
    for n in ids:
        b=bytearray()
        while len(b)<count:
            block=p.stdout.read(count-len(b))
            if not block:break
            b.extend(block)
        assert len(b)==count,(n,len(b))
        result[n]=Image.frombytes('RGB',(w,h),bytes(b))
    assert p.stdout.read(1)==b'' and p.wait()==0
    return result

small=read_selected(indices,480,270)
def sheet(ids,cols,name,frames=small,crop=None):
    tiles=[]
    for n in ids:
        im=frames[n]
        if crop:im=im.crop(crop)
        tile=Image.new('RGB',(im.width,im.height+22),'#181818');tile.paste(im,(0,22))
        sid=next(s['id'] for s in shots if s['start_frame']<=n<s['end_frame_exclusive'])
        ImageDraw.Draw(tile).text((4,4),f'{sid} | f{n} | {n/24:.3f}s',fill='white');tiles.append(tile)
    w,h=tiles[0].size;out=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),'#181818')
    for i,im in enumerate(tiles):out.paste(im,(i%cols*w,i//cols*h))
    out.save(OUT/name,quality=90)

for i in range(0,58,4):
    sheet([n for s in shots[i:i+4] for n in overview[s['id']]],3,f'chronology-{i//4+1:02d}.jpg')
for sid,ids in cuts.items():sheet(ids,3,f'cut-{sid}.jpg')
for name,ids in phases.items():
    ids=sorted(set(ids))
    for i in range(0,len(ids),12):sheet(ids[i:i+12],3,f'{name}-{i//12+1:02d}.jpg')

native_ids=sorted(set([48,115,307,384,2141,2272,2273,2408,2409,2747,2748,2948,2949,3020,3224,3225,3253,3281,3309,3345,3346,3423,3494,3495,3820,3919,4697,4792,4793,4890,4891,4988,4989,5030,5069,5070,5126,5182,5183,5224,5264,5265,5314,5363,5364,5561,5656,5657,5751,5842,5930,6226,6371,6509,6618,6619,6643,6666]))
native=read_selected(native_ids,1920,1080)
for n,im in native.items():im.save(OUT/f'native-{n:06d}.jpg',quality=94)
for name,ids,crop in [('embrace-contact',[3224,3253,3281,3309,3345,3423],(300,240,1700,1050)),('held-contact',[3820,3919,4697,4793,4891,5070,5126,5265,5314,5363],(300,200,1700,1080)),('dawn-faces',[5561,5656,5657,5751,5842,5930,6226,6371,6509,6618],(300,100,1700,1050))]:
    for i in range(0,len(ids),2):sheet(ids[i:i+2],2,f'{name}-native-{i//2+1:02d}.jpg',frames=native,crop=crop)
checks={'video_sha256':EXPECTED,'manifest_sha256':hashlib.sha256((HERE/'frozen-manifest.json').read_bytes()).hexdigest(),'config_sha256':hashlib.sha256((HERE/'frozen-edit.json').read_bytes()).hexdigest(),'full_video_and_audio_decode':True,'decoded_video_frames':len(decoded),'video_pts_max_error_seconds':pts_error,'shots_contiguous_0_to_6667':True,'streams':probe['streams'],'motion_accounting':manifest['motion_accounting'],'overview_frames':overview,'key_cut_frames':cuts,'phase_frames':phases,'selected_thumbnail_frames':indices,'selected_native_frames':native_ids,'scope':'Whole-film chronology, current cuts, selected native detail, branding and final fade. Does not replace exhaustive source review or human listening.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({'small_frames':len(indices),'native_frames':len(native_ids),'pts_error':pts_error},indent=2),flush=True)
