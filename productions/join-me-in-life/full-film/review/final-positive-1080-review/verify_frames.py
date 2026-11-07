"""Independently reconstruct 14 source intervals; stream all final/cache frame hashes.
No full-film raw-frame dumps, source/config/provider changes, or editor imports.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,gzip,subprocess,re,shutil
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
HERE=Path(__file__).resolve().parent
OUT=ROOT/'build/final-positive-1080-review';OUT.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'productions/join-me-in-life/full-film'
VIDEO=ROOT/'build/Join_Me_in_Life_Full_Music_Video_QC.mp4'
MANIFEST=VIDEO.with_suffix('.manifest.json')
EXPECTED='ce666666ad5f81effa5ee47db624c2dff7f7f10a044b8e7c60a6baf1474b9f09'
IDS='S010 S015 S033 S034 S037 S041 S042 S043 S045 S047 S050 S051 S056 S058'.split()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)==EXPECTED
m=json.loads(MANIFEST.read_text());assert m['output_sha256']==EXPECTED and m['frames']==6667
shutil.copyfile(MANIFEST,HERE/'frozen-manifest.json')
config=Path(m['edit_config']['path']);assert sha(config)==m['edit_config']['sha256'];shutil.copyfile(config,HERE/'frozen-edit.json')
shots={s['id']:s for s in m['shots']}
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-show_frames','-show_entries','stream=width,height,r_frame_rate,nb_frames:frame=best_effort_timestamp_time','-of','json',str(VIDEO)]))
v=probe['streams'][0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',6667)
times=[float(f['best_effort_timestamp_time']) for f in probe['frames']];assert len(times)==6667
max_time_error=max(abs(t-i/24) for i,t in enumerate(times));assert max_time_error<1e-5

def framehash(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(p),'-map','0:v:0','-an','-f','framemd5','-'],text=True)
 return [x.split(',')[-1].strip() for x in raw.splitlines() if not x.startswith('#')]
actual=framehash(VIDEO);assert len(actual)==6667
(OUT/'final-framemd5.json.gz').write_bytes(gzip.compress(json.dumps(actual).encode(),mtime=0))
print('Final full decode/hash/timestamps pass',flush=True)
geometry='scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=4:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black'
def check(sid):
 s=shots[sid];motion=s['motion'];src=Path(motion['absolute_path']);assert sha(src)==motion['source_sha256']==motion['reviewed_source_sha256']
 review=BASE/motion['review']['path'];assert sha(review)==motion['review']['sha256']
 lo,hi=motion['reviewed_source_frames_zero_based'];n=hi-lo
 assert round(motion['in_seconds']*24)==lo and n==s['frames']==motion['used_frames']
 assert motion['lead_in_frames']==motion['endpoint_hold_frames']==0 and motion['framing_policy']=='contain'
 srcprobe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(src)]))['streams'][0]
 assert (srcprobe['width'],srcprobe['height'],srcprobe['r_frame_rate'])==(896,512,'24/1')
 vf=f'trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS,fps=24,{geometry},setsar=1'
 fade=s['final_fade_seconds'];assert fade==(2 if sid=='S058' else 0)
 if fade:vf+=f',fade=t=out:st={n/24-fade}:d={fade}'
 vf+=',format=yuv420p'
 out=OUT/f'{sid}-independent.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf',vf,'-an','-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-filter_threads','1','-r','24','-video_track_timescale','24000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(out)],check=True)
 expected=framehash(out);real=actual[s['start_frame']:s['end_frame_exclusive']];assert len(expected)==len(real)==n
 result={'id':sid,'timeline_frames':[s['start_frame'],s['end_frame_exclusive']],'source_frames':[lo,hi],'frames':n,'source_sha256':sha(src),'source_review':motion['review'],'independent_sha256':sha(out),'filter':vf,'lead_hold_frames':0,'endpoint_hold_frames':0,'fps':24,'framing':'contain','resolved_picture':[1892,1080],'side_padding':[14,14],'fade_output_frames':[110,158] if fade else None,'identical_decoded_frames':sum(a==b for a,b in zip(real,expected)),'all_decoded_frames_identical':real==expected,'final_frame_hashes':real,'expected_frame_hashes':expected}
 print(sid,result['identical_decoded_frames'],'/',n,flush=True)
 return result
with ThreadPoolExecutor(max_workers=2) as pool:new=list(pool.map(check,IDS))
invpath=BASE/'review/stable-1080-picture-review/cache-inventory.json';assert sha(invpath)=='06b5081dc8f8bb571cca297d65decc65f2113a1947a3c8f2b5d0bcc4be5c1e32'
inv=json.loads(invpath.read_text())
def stable(e):
 p=ROOT/e['path'];assert sha(p)==e['sha256'];s=shots[e['id']]
 expected=framehash(p);real=actual[s['start_frame']:s['end_frame_exclusive']];assert len(real)==len(expected)==e['frames']
 return {**e,'timeline_frames':[s['start_frame'],s['end_frame_exclusive']],'identical_decoded_frames':sum(a==b for a,b in zip(real,expected)),'all_decoded_frames_identical':real==expected}
with ThreadPoolExecutor(max_workers=2) as pool:old=list(pool.map(stable,inv['shots']))
assert len(new)==14 and sum(r['frames'] for r in new)==1531
assert len(old)==44 and sum(r['frames'] for r in old)==5136
raw={'output_sha256':EXPECTED,'manifest_sha256':sha(MANIFEST),'config_sha256':m['edit_config']['sha256'],'new':new,'stable':old,'final_frame_hashes':actual,'timestamps':times}
(HERE/'full-frame-checks.json.gz').write_bytes(gzip.compress(json.dumps(raw,separators=(',',':')).encode(),mtime=0))
summary={'output_sha256':EXPECTED,'manifest_sha256':sha(MANIFEST),'config_sha256':m['edit_config']['sha256'],'dimensions':[1920,1080],'fps':24,'frames':6667,'all_timestamps_checked':True,'maximum_timestamp_error_seconds':max_time_error,'new_shots':[ {k:v for k,v in r.items() if k not in ['final_frame_hashes','expected_frame_hashes']} for r in new],'stable_inventory_sha256':sha(invpath),'stable_shots':old,'all_new_frames_identical':all(r['all_decoded_frames_identical'] for r in new),'all_stable_frames_identical':all(r['all_decoded_frames_identical'] for r in old),'full_checks_sha256':sha(HERE/'full-frame-checks.json.gz')}
(HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
assert summary['all_new_frames_identical'] and summary['all_stable_frames_identical']
print('PASS all1531 new reconstruction frames and all5136 stable cached frames',flush=True)
