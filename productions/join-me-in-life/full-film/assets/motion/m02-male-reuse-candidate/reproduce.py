"""Create only the bounded crop derivative and its provenance; no edit approvals.
Run from any directory with FFmpeg/ffprobe. The original source is read-only.
"""
from pathlib import Path
import hashlib,json,shlex,subprocess
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'productions/join-me-in-life/current/assets/M02_Summer.mp4'
OUTPUT=HERE/'M02_Male_0-2s_16x9.mp4'
EXPECTED='03d6eb4da452db9b21b3087edf97492d21517c215cf1c548bfe5a344d8fd70d3'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

if __name__=='__main__':
 if sha(SOURCE)!=EXPECTED:raise RuntimeError('Original M02 source hash differs')
 command=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(SOURCE.relative_to(ROOT)),
  '-map','0:v:0','-vf','trim=start_frame=0:end_frame=48,crop=800:450:212:0,scale=960:540:flags=lanczos,setsar=1',
  '-frames:v','48','-an','-fps_mode','passthrough','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',
  '-metadata','comment=Original M02 frames 1-48 at native 24 fps; locked crop x212 y0 w800 h450; source unchanged; no audio or generated frames.',str(OUTPUT.relative_to(ROOT))]
 subprocess.run(command,cwd=ROOT,check=True)
 info=probe(OUTPUT);video=next(s for s in info['streams'] if s['codec_type']=='video')
 if len(info['streams'])!=1 or int(video['nb_frames'])!=48 or video['avg_frame_rate']!='24/1' or float(video['duration'])!=2.0:
  raise RuntimeError('Derived source does not match 48 frames / 24 fps / 2 seconds / video only')
 provenance={'schema':'jml-crop-provenance/v1','status':'bounded derivative; creative review is separate, no approval manifest edited',
  'source':str(SOURCE.relative_to(ROOT)),'source_sha256':EXPECTED,
  'source_frame_interval_zero_based_exclusive':[0,48],'source_frame_interval_one_based_inclusive':[1,48],
  'source_time_interval_seconds_exclusive':[0.0,2.0],'source_fps':'24/1','timestamp_policy':'Preserve input PTS and frame duration; source begins at zero. No setpts or fps filter.',
  'crop_native_pixels':{'x':212,'y':0,'width':800,'height':450},'crop_policy':'one fixed axis-aligned 16:9 crop for all 48 frames',
  'resize':{'width':960,'height':540,'filter':'lanczos','scale_factor':1.2},
  'transform_scope':'spatial crop/rescale plus H.264 encoding; no camera animation, retiming, optical flow, interpolation or audio',
  'output':str(OUTPUT.relative_to(ROOT)),'output_sha256':sha(OUTPUT),'output_bytes':OUTPUT.stat().st_size,
  'command_working_directory':'repository root','command_argv':command,'command_shell':shlex.join(command),
  'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
  'output_probe':info}
 (HERE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 print(json.dumps({'file':str(OUTPUT.relative_to(ROOT)),'sha256':provenance['output_sha256'],'bytes':OUTPUT.stat().st_size,'frames':48,'fps':'24/1','seconds':2.0,'audio':False},indent=2))
