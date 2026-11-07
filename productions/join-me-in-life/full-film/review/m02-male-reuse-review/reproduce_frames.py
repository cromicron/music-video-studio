"""Decode all 48 frames of the bounded male crop into four portable review sheets.
Requires FFmpeg, ffprobe and Pillow. Generated output stays under root build/.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,hashlib
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
SOURCE=ROOT/'productions/join-me-in-life/full-film/assets/motion/m02-male-reuse-candidate/M02_Male_0-2s_16x9.mp4'
OUT=ROOT/'build/m02-male-reuse-review'
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(SOURCE),'-vf','scale=480:270','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
 size=480*270*3
 if len(raw)!=48*size:raise RuntimeError('Expected 48 frames')
 frames=[Image.frombytes('RGB',(480,270),raw[i*size:(i+1)*size]) for i in range(48)]
 for start in range(0,48,12):
  sheet=Image.new('RGB',(1440,1188),'#171717');d=ImageDraw.Draw(sheet)
  for j,im in enumerate(frames[start:start+12]):
   i=start+j;x=j%3*480;y=j//3*297;d.text((x+5,y+5),f'derived/source f{i+1:02} | {i/24:.6f}s',fill='white');sheet.paste(im,(x,y+27))
  sheet.save(OUT/f'sequential-{start+1:02}-{start+12:02}.jpg',quality=92)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(SOURCE)]))
 pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','frame=best_effort_timestamp_time,duration_time','-of','json',str(SOURCE)]))['frames']
 values=[float(x['best_effort_timestamp_time']) for x in pts]
 original=ROOT/'productions/join-me-in-life/current/assets/M02_Summer.mp4'
 original_pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','frame=best_effort_timestamp_time,duration_time','-of','json',str(original)]))['frames'][:48]
 same_times=all(a['best_effort_timestamp_time']==b['best_effort_timestamp_time'] and a['duration_time']==b['duration_time'] for a,b in zip(pts,original_pts))
 if len(pts)!=48 or not same_times:raise RuntimeError('Original frame timing was not preserved')
 result={'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'originalSha256':hashlib.sha256(original.read_bytes()).hexdigest(),'decodedFrames':48,'maxPtsDeviationFromFrameIndexOver24Seconds':max(abs(t-i/24) for i,t in enumerate(values)),'all48OriginalPtsAndDurationsPreserved':same_times,'decodedFrameTiming':pts,'probe':probe}
 (OUT/'encode-check.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['probe','decodedFrameTiming']},indent=2))
