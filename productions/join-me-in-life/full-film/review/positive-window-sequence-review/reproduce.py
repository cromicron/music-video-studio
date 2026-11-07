"""Independent integer-frame containment and unchanged-neighbor checks."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
ROOT=FILM.parents[2]
OUT=ROOT/'build/positive-window-sequence-review'
OUT.mkdir(parents=True,exist_ok=True)
VIDEO=FILM/'exports/Join_Me_in_Life_Positive_Window_Context_Proof.mp4'
SHA='dfece1dd258e0da59a2d58fe468670a76447a3ab17bdd3ab1d9afd5f436791d2'
MANIFEST_SHA='fb30d7dbfb0a1ba8188e887adf4e23bfa313dae53f9f607e4f29c2c46ae1a82e'
CONFIG_SHA='8422bf9fb4849e02e1ead09148b4615538c4a3780d13161f4f598e94932f7bb6'
assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==SHA
assert hashlib.sha256((HERE/'frozen-manifest.json').read_bytes()).hexdigest()==MANIFEST_SHA
assert hashlib.sha256((HERE/'frozen-edit.json').read_bytes()).hexdigest()==CONFIG_SHA
manifest=json.loads((HERE/'frozen-manifest.json').read_text())
assert manifest['edit_config']['sha256']==CONFIG_SHA
assert manifest['frames']==898 and manifest['coverage']=={'start_frame':998,'end_frame_exclusive':1896,'full_song':False}

def hashes(path,vf=None):
    cmd=['ffmpeg','-v','error','-xerror','-threads','2','-i',str(path),'-map','0:v:0','-an']
    if vf:cmd+=['-vf',vf,'-fps_mode','passthrough']
    s=subprocess.check_output(cmd+['-f','framemd5','-'],text=True)
    return [line.split(',')[-1].strip() for line in s.splitlines() if not line.startswith('#')]

all_hashes=hashes(VIDEO)
assert len(all_hashes)==898
comparisons=[]
for sid,take,start,stop,local,sha in [('S010','P1L02',3,116,101,'24312a9d5272083d1c3f248837d63f0b61b8be1a051b6b99c5de2d092cdad53b'),('S015','P1L03',3,104,696,'14753d944afdd0ab41db66401ae694ee45c496f1392eb6913d0bbd4da369f2cc')]:
    src=FILM/f'assets/motion/ltx23-positive-continuation/P1/{take}/video-silent.mp4'
    assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
    shot=next(s for s in manifest['shots'] if s['id']==sid)
    assert shot['motion']['used_frames']==stop-start
    assert shot['motion']['lead_in_frames']==shot['motion']['endpoint_hold_frames']==0
    expected=OUT/f'{sid}-independent.mp4'
    vf=f'trim=start_frame={start}:end_frame={stop},setpts=PTS-STARTPTS,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
    subprocess.run(['ffmpeg','-v','error','-xerror','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(stop-start),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(expected)],check=True)
    independent=hashes(expected)
    actual=all_hashes[local:local+stop-start]
    assert actual==independent,(sid,'integer-frame independent reconstruction differs')
    comparisons.append({'shot':sid,'source_sha256':sha,'source_frames_zero_based':[start,stop],'context_frames_zero_based':[local,local+stop-start],'frames_compared':len(actual),'every_decoded_picture_identical_to_independent_integer_trim_and_944x540_containment':True,'independent_filter':vf})

neighbors=[]
for sid,start,stop,name,sha in [('S011',214,346,'Join_Me_in_Life_Snow_Walk_Proof.mp4','36fc7ea98c76365333862f3461022bb6bc26ee805fd85466e616cfc84cd81731'),('S013',449,598,'Join_Me_in_Life_Arrival_Contain_Proof.mp4','8c772116797166ac5a7c1e2d43cc6438f55916c17244bb5733ab5ad3d0fc8fc8'),('S014',598,696,'Join_Me_in_Life_First_Chorus_Contain_Proof_v2.mp4','5588132a1628cb760703167e4b2d7a415c30684bd883ec828605b9d7d5fb15e1')]:
    old=FILM/'exports'/name
    assert hashlib.sha256(old.read_bytes()).hexdigest()==sha
    old_hashes=hashes(old)
    identical=old_hashes==all_hashes[start:stop]
    old_manifest=json.loads(old.with_suffix('.manifest.json').read_text())
    old_shot=next(s for s in old_manifest['shots'] if s['id']==sid)
    new_shot=next(s for s in manifest['shots'] if s['id']==sid)
    for key in ['source_sha256','in_seconds','used_frames','lead_in_frames','endpoint_hold_frames','framing_policy']:
        assert old_shot['motion'][key]==new_shot['motion'][key],(sid,key)
    def small_rgb(path,vf):
        raw=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(path),'-an','-vf',vf+',scale=240:135:flags=lanczos','-fps_mode','passthrough','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-'])
        return np.frombuffer(raw,np.uint8).reshape(-1,135,240,3)
    current_rgb=small_rgb(VIDEO,f'trim=start_frame={start}:end_frame={stop},setpts=PTS-STARTPTS')
    old_rgb=small_rgb(old,'null')
    assert len(current_rgb)==len(old_rgb)==stop-start
    error=np.abs(current_rgb.astype(float)-old_rgb.astype(float)).mean((1,2,3))
    assert float(error.max())<2.0,(sid,'unexpected changed picture')
    neighbors.append({'shot':sid,'previously_reviewed_export':name,'sha256':sha,'compared_frames':stop-start,'source_hash_interval_holds_and_framing_unchanged':True,'all_decoded_frames_identical':identical,'same_index_comparison_240x135_mean_rgb_absolute_error':float(error.mean()),'same_index_comparison_240x135_max_frame_mean_rgb_absolute_error':float(error.max()),'note':'S011/S014 encodes differ slightly; source selection and framing are identical, and same-index pictures agree within the recorded lossy-image error. S013 is decoded-picture-identical.'})

selected=set(range(101,214))|set(range(696,797))
cuts=[101,214,346,449,598,696,797]
for cut in cuts:selected.update(range(cut-6,cut+6))
for shot in manifest['shots']:
    a,b=shot['start_frame']-998,shot['end_frame_exclusive']-998
    selected.update([a,(a+b-1)//2,b-1])
selected.update([797+43,797+45,797+47,797+49,797+64,797+66,797+68,797+70])
indices=sorted(selected)
ranges=[]
for index in indices:
    if ranges and index==ranges[-1][1]+1:ranges[-1][1]=index
    else:ranges.append([index,index])
vf='select='+'+'.join(f'between(n\\,{a}\\,{b})' for a,b in ranges)
raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(VIDEO),'-map','0:v:0','-an','-vf',vf,'-fps_mode','passthrough','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-'])
rgb=np.frombuffer(raw,np.uint8).reshape(-1,540,960,3)
frames={n:Image.fromarray(rgb[i]) for i,n in enumerate(indices)}
for n,im in frames.items():im.save(OUT/f'f{n:04d}.png')

def sheet(ids,cols,name,crop=None,size=(480,270)):
    tiles=[]
    for n in ids:
        im=frames[n]
        if crop:im=im.crop(crop)
        if size:im=im.resize(size,Image.Resampling.LANCZOS)
        tile=Image.new('RGB',(im.width,im.height+22),'#181818');tile.paste(im,(0,22))
        ImageDraw.Draw(tile).text((4,4),f'local {n} | master {n+998} | {n/24:.3f}s',fill='white');tiles.append(tile)
    w,h=tiles[0].size;canvas=Image.new('RGB',(w*cols,h*((len(tiles)+cols-1)//cols)),'#181818')
    for i,tile in enumerate(tiles):canvas.paste(tile,(i%cols*w,i//cols*h))
    canvas.save(OUT/name,quality=92)

rows=[]
for shot in manifest['shots']:
    a,b=shot['start_frame']-998,shot['end_frame_exclusive']-998;rows.extend([a,(a+b-1)//2,b-1])
sheet(rows,3,'sequence-overview.jpg')
for cut in cuts:
    sheet([cut-1,cut],2,f'cut-{cut:03d}.jpg',size=None)
    sheet(range(cut-6,cut+6),4,f'cut-phases-{cut:03d}.jpg')
for sid,a,b in [('S010',101,214),('S015',696,797)]:
    for first in range(a,b,16):
        ids=range(first,min(first+16,b));sheet(ids,4,f'{sid}-full-{first:03d}.jpg');sheet(ids,4,f'{sid}-faces-{first:03d}.jpg',crop=(100,60,625,340),size=None)
    phases=sorted(set(list(range(a,b,12))+[b-1]));sheet(phases,3,f'{sid}-phases.jpg')
sheet([101,141,161,183,203,213],3,'S010-native-face-phases.jpg',crop=(100,60,625,340),size=None)
sheet([696,736,760,766,780,796],3,'S015-native-face-phases.jpg',crop=(100,60,625,340),size=None)
sheet([797,840,842,844,846,861,863,865,867,897],3,'S016-exposure-phases.jpg')
pts_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(VIDEO)]))
pts=[float(f['best_effort_timestamp_time']) for f in pts_probe['frames']]
assert len(pts)==898
pts_error=max(abs(t-i/24) for i,t in enumerate(pts));assert pts_error<1e-6
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(VIDEO)]))
report={'export_sha256':SHA,'manifest_sha256':MANIFEST_SHA,'config_sha256':CONFIG_SHA,'frames':898,'fps':24,'master_frames_zero_based_half_open':[998,1896],'master_seconds_half_open':[998/24,1896/24],'insertions':comparisons,'unchanged_neighbors':neighbors,'context_video_pts_max_error_from_index_over_24_seconds':pts_error,'streams':probe['streams'],'source_audio_manifest':manifest['audio'],'cuts_context_frames':cuts,'source_frames_extracted_and_inspected_for_each_new_window':'all 113 S010 and all 101 S015 frames','context_selected_frames_extracted':indices,'scope':'Exact contained window insertions and S009–S016 cut context; no whole-film acceptance.'}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'insertions':comparisons,'unchanged_neighbors':neighbors,'pts_error':pts_error,'frames_extracted':len(indices)},indent=2))
