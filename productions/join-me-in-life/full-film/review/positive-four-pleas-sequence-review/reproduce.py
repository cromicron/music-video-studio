"""Independent exact intervals, containment and encoded cuts; writes build only.

Requires the completed export and frozen manifest/settings in this evidence folder.
Full comparisons stream decoded frame MD5; only selected frames enter memory.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'studio.json').is_file())
BASE = ROOT/'productions/join-me-in-life/full-film'
OUT = ROOT/'build/positive-four-pleas-sequence-review'; OUT.mkdir(parents=True, exist_ok=True)
CONTEXT = BASE/'exports/Join_Me_in_Life_Positive_Four_Pleas_Context_Proof.mp4'
CONFIG_SHA = '1857d2254ade658a66faeb8419ec5fb1a22c831a2baa0bd958aecb2d3b0a3413'
OLD = BASE/'exports/Join_Me_in_Life_Four_Pleas_Context_Proof.mp4'
OLD_SHA = '513798b11449a2b6405850f125901cea024bc4feb4f7a84a92b6de37c21c08e5'
SOURCES = {
 'P2L07': ('assets/motion/ltx23-positive-continuation/P2/P2L07/video-silent.mp4','c6b99b860c588e5eb7e1aa7b8dd14d7b02500f7964e1b8548dd7e4d6e66c160b'),
 'P2L08': ('assets/motion/ltx23-positive-continuation/P2/P2L08/video-silent.mp4','2fd984ecef9bb36675d21ab595ec2b5c8f69e4a583131be424820dad0a5d6f17'),
 'P1L09': ('assets/motion/ltx23-positive-continuation/P1/P1L09/video-silent.mp4','94c105fb16c8cfdae7ee7e00793b48d7e6dd36196e0689fb8ab3a46e1e4adbd2'),
 'R2S047': ('assets/motion/ltx23-positive-corrections/R2S/R2S047/video-silent.mp4','ede1c44f5c74f57eee8afdb3852db03df567396e22b565d638618899b3eac688'),
}
SPECS = [('S041','P2L07',3,99,99,195), ('S042','P2L08',3,101,195,293),
    ('S043','P2L08',101,199,293,391), ('S045','P1L09',3,116,472,585),
    ('S047','R2S047',3,102,667,766)]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def md5(path):
    text = subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0',
        '-fps_mode','passthrough','-pix_fmt','yuv420p','-f','framemd5','-'], text=True)
    (OUT/(path.stem+'.framemd5')).write_text(text)
    rows = [line.split(',') for line in text.splitlines() if not line.startswith('#')]
    assert [int(r[2]) for r in rows] == list(range(len(rows)))
    return [r[-1].strip() for r in rows]

manifest_bytes = (HERE/'pinned-manifest.json').read_bytes()
assert CONTEXT.with_suffix('.manifest.json').read_bytes() == manifest_bytes
m = json.loads(manifest_bytes)
assert m['edit_config']['sha256'] == CONFIG_SHA and sha(HERE/'pinned-config.json') == CONFIG_SHA
assert sha(CONTEXT) == m['output_sha256'] and sha(OLD) == OLD_SHA
assert m['coverage'] == {'start_frame':4598, 'end_frame_exclusive':5462, 'full_song':False}
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
    'stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,start_time,duration,nb_frames:format=start_time,duration',
    '-of','json',str(CONTEXT)], text=True))
v = next(s for s in probe['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['avg_frame_rate'],v['nb_frames']) == (960,540,'24/1','864')
(OUT/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
actual = md5(CONTEXT); assert len(actual)==864
checks = {'config_sha256':CONFIG_SHA,'context_sha256':m['output_sha256'],
    'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(), 'context_frames':864,
    'master_range_zero_based':[4598,5462], 'full_video_decode':'passed',
    'video_timestamp_frame_indices':'all consecutive at 24 fps',
    'author_audio_check':m['audio'], 'insertions':{}}
for shot,key,lo,hi,start,end in SPECS:
    rel,digest = SOURCES[key];src=BASE/rel;assert sha(src)==digest
    vf=f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1,format=yuv420p'
    dest=OUT/f'{shot}-independent-reconstruction.mp4'
    cmd=['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(hi-lo),
        '-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24',
        '-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709',
        '-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(dest)]
    if not dest.exists(): subprocess.run(cmd,check=True)
    ref=md5(dest)
    checks['insertions'][shot]={'source':rel,'source_sha256':digest,'source_frames_zero_based':[lo,hi],
        'context_frames_zero_based':[start,end],'filter':vf,'encoding_command':cmd,
        'reconstructed_sha256':sha(dest),'identical_frames':sum(a==b for a,b in zip(ref,actual[start:end])),
        'all_decoded_frames_identical':ref==actual[start:end]}
    assert checks['insertions'][shot]['all_decoded_frames_identical']
old=md5(OLD)
for shot,lo,hi,start,end in [('S044',98,179,391,472),('S046',292,374,585,667)]:
    checks['insertions'][shot]={'previous_reviewed_context_sha256':OLD_SHA,
        'previous_context_frames_zero_based':[lo,hi],'context_frames_zero_based':[start,end],
        'all_decoded_frames_equal_previous_context':old[lo:hi]==actual[start:end]}
    if old[lo:hi] != actual[start:end]:
        motion=next(s['motion'] for s in m['shots'] if s['id']==shot)
        src=BASE/motion['path'];assert sha(src)==motion['source_sha256']
        slo,shi=motion['reviewed_source_frames_zero_based']
        vf=f'trim=start_frame={slo}:end_frame={shi},setpts=PTS-STARTPTS,fps=24,scale=960:540:force_original_aspect_ratio=increase:flags=lanczos,crop=960:540,setsar=1,format=yuv420p'
        dest=OUT/f'{shot}-independent-reconstruction.mp4'
        cmd=['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(shi-slo),
            '-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24',
            '-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709',
            '-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(dest)]
        subprocess.run(cmd,check=True);ref=md5(dest)
        checks['insertions'][shot].update({'source_sha256':motion['source_sha256'],
            'source_frames_zero_based':[slo,shi],'filter':vf,'encoding_command':cmd,
            'reconstructed_sha256':sha(dest),'identical_frames':sum(a==b for a,b in zip(ref,actual[start:end])),
            'all_decoded_frames_identical_to_reconstruction':ref==actual[start:end]})
        assert ref==actual[start:end]

cuts=[99,195,293,391,472,585,667,766]
phases=[0,49,98,99,146,194,195,219,243,267,292,293,325,365,390,391,415,447,471,
    472,496,520,544,568,584,585,609,641,666,667,691,715,739,765,766,815,863]
selected=sorted(set(phases+[i for c in cuts for i in range(c-3,c+3)]))
expr='+'.join(f'eq(n\\,{i})' for i in selected)
raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(CONTEXT),'-vf','select='+expr,
    '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'])
decoded=np.frombuffer(raw,np.uint8).reshape(-1,540,960,3);assert len(decoded)==len(selected)
frames={};edges=[]
for i,rgb in zip(selected,decoded):
    frames[i]=Image.fromarray(rgb);frames[i].save(OUT/f'native-{i:03}.jpg',quality=96)
    if any(lo<=i<hi for *_,lo,hi in SPECS):
        active=np.where(rgb[20:520].mean(axis=(0,2))>8)[0];edges.append([int(active[0]),int(959-active[-1])])
checks['selected_native_frames_zero_based']=selected
checks['sampled_held_motion_mean_column_padding_pixels']=sorted(set(map(tuple,edges)))
for c in cuts:
    im=Image.new('RGB',(1920,566),'#171717');d=ImageDraw.Draw(im)
    for j,i in enumerate([c-1,c]):
        d.text((j*960+5,5),f'Context local f{i} / master f{i+4598}',fill='white');im.paste(frames[i],(j*960,26))
    im.save(OUT/f'join-{c:03}-native.jpg',quality=95)
for name,ids in [('lead',phases[:13]),('four-pleas',phases[12:])]:
    im=Image.new('RGB',(1920,((len(ids)+3)//4)*294),'#171717');d=ImageDraw.Draw(im)
    for j,i in enumerate(ids):
        x,y=j%4*480,j//4*294;d.text((x+4,y+4),f'local f{i} / master f{i+4598}',fill='white')
        im.paste(frames[i].resize((480,270),Image.Resampling.LANCZOS),(x,y+24))
    im.save(OUT/f'{name}-phases.jpg',quality=93)
(OUT/'encoded-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
