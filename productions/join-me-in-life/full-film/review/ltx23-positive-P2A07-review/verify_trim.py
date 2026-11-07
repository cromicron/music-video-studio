"""Validate the review-only trim after reproduce.py; writes ignored build evidence."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
TAKE='P2A07';SHOT='S058';LO=3;HI=161
OUT=ROOT/f'build/ltx23-positive-{TAKE}-review';VIDEO=OUT/f'{SHOT}-selected.mp4'
checks=json.loads((OUT/'checks.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(VIDEO)==checks['segments'][0]['proxy_sha256']
frames=np.load(OUT/'frames.npy',mmap_mode='r')[LO:HI]
raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(VIDEO),'-map','0:v:0','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
proxy=np.frombuffer(raw,np.uint8).reshape(-1,512,896,3)
assert len(proxy)==HI-LO
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_frames','-show_entries','frame=best_effort_timestamp_time:stream=codec_type,width,height,r_frame_rate,nb_frames','-of','json',str(VIDEO)]))
assert not any(s['codec_type']=='audio' for s in probe['streams'])
times=[float(f['best_effort_timestamp_time']) for f in probe['frames']]
assert len(times)==HI-LO and max(abs(t-i/24) for i,t in enumerate(times))<1e-5
mae=[float(np.abs(a.astype(np.int16)-b.astype(np.int16)).mean()) for a,b in zip(frames,proxy)]
assert max(mae)<5
result={'shot':SHOT,'source_interval_zero_based_half_open':[LO,HI],'selected_frames':len(proxy),'fps':24,'source_frame_mapping':'proxy frame i corresponds to source frame i+3; trim=start_frame=3:end_frame='+str(HI)+',setpts=N/(24*TB)','proxy_sha256':sha(VIDEO),'all_timestamps_correct':True,'audio_streams':0,'all_frames_decode':True,'lossy_proxy_frame_mae_min':min(mae),'lossy_proxy_frame_mae_max':max(mae),'lossy_proxy_frame_mae_mean':sum(mae)/len(mae),'limitation':'Review-only H.264 proxy has lossy pixel changes; original source independently decoded and all frames inspected. No assembled film or fade is generated here.'}
(OUT/'trim-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
