"""Independently rebuild 13 frozen motion intervals at 1080 and compare every frame."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/stable-1080-picture-review';OUT.mkdir(parents=True,exist_ok=True)
HERE=Path(__file__).resolve().parent
if not (OUT/'frozen-plan.json').exists():(OUT/'frozen-plan.json').write_bytes((HERE/'frozen-plan.json').read_bytes())
plan=json.loads((OUT/'frozen-plan.json').read_text())
ip=HERE/'cache-inventory.json'
if not ip.exists():ip=ROOT/'build/final-stable-shot-cache-prep.json'
inventory=json.loads(ip.read_text())
cache={s['id']:s for s in inventory['shots']}
def framehash(p):
    raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(p),'-map','0:v:0','-f','framemd5','-'],text=True)
    return [x.split(',')[-1].strip() for x in raw.splitlines() if not x.startswith('#')]
def check(s):
    sid=s['id'];m=s['motion'];src=Path(m['absolute_path']);digest=hashlib.sha256(src.read_bytes()).hexdigest()
    assert digest==m['source_sha256']
    lo=round(m['in_seconds']*24);hi=lo+m['used_frames'];n=s['frames'];policy=m.get('framing_policy','fill')
    stream=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(src)]))['streams'][0]
    if policy=='contain':
        geometry='scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=4:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black'
    else:geometry='scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080'
    vf=(f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,{geometry},setsar=1,'
        f'tpad=start_mode=clone:start={m["lead_in_frames"]}:stop_mode=clone:stop={m["endpoint_hold_frames"]},trim=end_frame={n},format=yuv420p')
    out=OUT/f'{sid}-independent.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(n),
                    '-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24',
                    '-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709',
                    '-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(out)],check=True)
    p=ROOT/cache[sid]['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==cache[sid]['sha256']
    actual,expected=framehash(p),framehash(out);assert len(actual)==len(expected)==n
    result={'id':sid,'cache_sha256':cache[sid]['sha256'],'source_sha256':digest,'source_dimensions':[stream['width'],stream['height']],
            'source_fps':stream['r_frame_rate'],'source_frames':[lo,hi],'framing_policy':policy,'lead_frames':m['lead_in_frames'],
            'endpoint_hold_frames':m['endpoint_hold_frames'],'total_frames':n,'identical_decoded_frames':sum(a==b for a,b in zip(actual,expected)),
            'all_decoded_frames_identical':actual==expected,'filter':vf}
    print(sid,result['identical_decoded_frames'],'/',n,flush=True)
    return result
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(check,[s for s in plan['shots'] if s.get('motion')]))
p=ROOT/cache['S020']['path'];prior=ROOT/'build/r1-waiting-closeup-1080.mp4'
assert hashlib.sha256(prior.read_bytes()).hexdigest()=='d0c3a6963324d53a6581b3ef137858968773fd821fdab01071062fb40c177704'
closeup={'cache_sha256':cache['S020']['sha256'],'prior_proof_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
         'all_136_frames_identical_to_reviewed_1080_proof':framehash(p)==framehash(prior)}
(OUT/'interval-checks.json').write_text(json.dumps({'motion_shots':results,'S020':closeup},indent=2)+'\n')
