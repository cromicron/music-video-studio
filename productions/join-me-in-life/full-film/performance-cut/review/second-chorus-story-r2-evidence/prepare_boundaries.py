#!/usr/bin/env python3
"""Exact6-frame temporal windows around actual joined movie cuts, not approval."""
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
CONFIG=[('second_chorus','C18_C05TAIL_B08B_Trial.mp4','df8ed4f62f986662caa6fd9fb5dee9be7f6eb6c61c83533e4d53655d383a293f',3225,[('C18_C05TAIL',199),('C05TAIL_B08B',299)])]
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def main():
 out=HERE/'boundary-index-v1.json';assert not out.exists();rows=[]
 for name,filename,digest,globalstart,joins in CONFIG:
  source=ROOT/'build/performance-cut-second-chorus-story-trial-v1'/filename;assert sha(source)==digest
  for label,j in joins:
   a,b=j-3,j+3;target=HERE/name/(label+'-six-frames.png');assert not target.exists()
   text="drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{eif\\:n+"+str(a)+"\\:d}':x=3:y=2:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.8"
   filters=f'trim=start_frame={a}:end_frame={b},'+text+',scale=960:540,tile=2x3:nb_frames=6:padding=4:margin=4'
   cmd=['ffmpeg','-v','error','-n','-threads','2','-i',str(source),'-vf',filters,'-frames:v','1',str(target)];subprocess.run(cmd,check=True)
   rows.append({'excerpt':name,'label':label,'source':str(source.relative_to(ROOT)),'source_sha256':digest,'local_join_frame':j,'master_join_frame':globalstart+j,'actual_window_local_frames':[a,b],'sheet':str(target.relative_to(ROOT)),'sha256':sha(target),'command':cmd,'scope':'Exact encoded boundary extraction scaled50percent for overall cut/body/prop inspection; not a motion or final-film pass.'})
 out.write_text(json.dumps({'schema':'jml-story-context-boundary-aids/v1','windows':rows},indent=2)+'\n');print('Prepared2 actual local-trial boundary windows')
if __name__=='__main__':main()
