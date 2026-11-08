from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,hashlib
D=Path(__file__).resolve().parent;P=D.parents[1];R=P.parents[3]
src=Path('/workspace/music-video-studio/build/unfinished-morning-final-v1/Join_Me_in_Life_Unfinished_Morning.mp4')
edit=json.loads((P/'tools/editor/edit-v015.json').read_text());cuts=[s['start_frame'] for s in edit['shots'][1:]];nums=sorted({n for k in cuts for n in [k-1,k]})
def decode_selected(nums,w,h):
 select='+'.join(f'eq(n,{n})' for n in nums)
 proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-vf',f"select='{select}',scale={w}:{h}",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 out={};size=w*h*3
 for n in nums:
  data=proc.stdout.read(size);assert len(data)==size,(n,len(data));out[n]=Image.frombytes('RGB',(w,h),data)
 assert not proc.stdout.read(1);assert proc.wait()==0
 return out
ims=decode_selected(nums,960,540)
for i,k in enumerate(cuts):
 can=Image.new('RGB',(1920,565));dr=ImageDraw.Draw(can)
 for col,n in enumerate([k-1,k]):can.paste(ims[n],(col*960,0));dr.text((col*960,540),f'final master frame {n}',fill='white')
 can.save(D/f'cut-{i+1:02}-{k}.jpg',quality=92)
known=[191,1596,1799,2202,2403,6477,6647,6666]
for n,im in decode_selected(known,1920,1080).items():im.save(D/f'known-fix-final-{n:04}.jpg',quality=96)
(D/'decoded-selection-v1.json').write_text(json.dumps({'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'cut_frames':cuts,'selected_decoded_indices':nums,'known_fix_native_output_frames':known,'fps_mode':'passthrough','scope':'Actual final-frame cut pairs resized960x540 for inspection; eight targeted output-native1920x1080 frames. No production edits or full raw dumps.'},indent=2)+'\n')
print('38 cuts and8 targeted output-native images ready')
