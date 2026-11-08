#!/usr/bin/env python3
"""Exact6-frame temporal windows around actual joined movie cuts, not approval."""
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
CONFIG=[('recognition','Recognition_C26_C32.mp4','742a29a52ff3144d5087db00ca25dff57db0c50cecabe1250327e6e03eb9da2a',4598,[('C26_C27',130),('C27_O03',258),('O03_C29',391),('C29_C30',472),('C30_C31',584),('C31_C32',667)]),('ending','Private_Ending_C37_O04.mp4','2e96ea7a43ac8c758003e628fe7e26f1a7f4b145da614a5b4b461126904785b9',6223,[('C37_C38',64),('C38_O04',254)])]
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def main():
 out=HERE/'boundary-index-v1.json';assert not out.exists();rows=[]
 for name,filename,digest,globalstart,joins in CONFIG:
  source=ROOT/'build/performance-cut-story-context-v1'/filename;assert sha(source)==digest
  for label,j in joins:
   a,b=j-3,j+3;target=HERE/name/(label+'-six-frames.png');assert not target.exists()
   text="drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{eif\\:n+"+str(a)+"\\:d}':x=3:y=2:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.8"
   filters=f'trim=start_frame={a}:end_frame={b},'+text+',scale=960:540,tile=2x3:nb_frames=6:padding=4:margin=4'
   cmd=['ffmpeg','-v','error','-n','-threads','2','-i',str(source),'-vf',filters,'-frames:v','1',str(target)];subprocess.run(cmd,check=True)
   rows.append({'excerpt':name,'label':label,'source':str(source.relative_to(ROOT)),'source_sha256':digest,'local_join_frame':j,'master_join_frame':globalstart+j,'actual_window_local_frames':[a,b],'sheet':str(target.relative_to(ROOT)),'sha256':sha(target),'command':cmd,'scope':'Exact encoded boundary extraction scaled50percent for overall cut/body/prop inspection; not a motion or final-film pass.'})
 out.write_text(json.dumps({'schema':'jml-story-context-boundary-aids/v1','windows':rows},indent=2)+'\n');print('Prepared8 actual boundary windows')
if __name__=='__main__':main()
