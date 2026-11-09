#!/usr/bin/env python3
"""Adapt retained C streamed selected-frame workflow; compact JPEGs, no raw dumps."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess
D=Path(__file__).resolve().parent
ROOT=next(p for p in D.parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film/performance-cut'
SRC=ROOT/'build/performance-cut-final-v1/Join_Me_in_Life_Movie_and_Band.mp4'
EDIT=BASE/'edit/edit-v009.json'
MASTER_SHA='fabe33c576aaa0473e82c6ed755e884e3b6bc9103f392551138f6527099f2fdb'
EDIT_SHA='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def decode_selected(nums,w,h):
 nums=sorted(set(nums));terms=[f'eq(n,{n})' for n in nums];select='+'.join('('+ '+'.join(terms[i:i+12])+')' for i in range(0,len(terms),12))
 cmd=['ffmpeg','-v','error','-threads','1','-i',str(SRC),'-filter_threads','1','-vf',f"select='{select}',scale={w}:{h}",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-']
 proc=subprocess.Popen(cmd,stdout=subprocess.PIPE);out={};size=w*h*3
 for j,n in enumerate(nums):
  data=proc.stdout.read(size);assert len(data)==size,(n,len(data));out[n]=Image.frombytes('RGB',(w,h),data)
  if j%32==0:print(f'selected {j+1}/{len(nums)} actual encoded frames',flush=True)
 assert not proc.stdout.read(1);assert proc.wait()==0
 return out,cmd

def main():
 out=D/'evidence-index-v1.json';assert not out.exists();assert SRC.stat().st_size==196409309 and sha(SRC)==MASTER_SHA;assert sha(EDIT)==EDIT_SHA
 edit=json.loads(EDIT.read_text());shots=edit['shots'];assert len(shots)==46 and edit['total_frames']==6667
 cuts=[s['start_frame'] for s in shots[1:]];mids=[(s['start_frame']+s['end_frame_exclusive']-1)//2 for s in shots];nums=sorted({0,6666,*mids,*[n for k in cuts for n in [k-1,k]]})
 ims,cmd1=decode_selected(nums,960,540);join_rows=[];shot_rows=[]
 for i,(a,b) in enumerate(zip(shots,shots[1:]),1):
  k=b['start_frame'];name=f'join-{i:02d}-{a["id"]}-{b["id"]}-{k}.jpg';p=D/name;assert not p.exists();can=Image.new('RGB',(1920,565),'#161616');draw=ImageDraw.Draw(can)
  for col,n in enumerate([k-1,k]):can.paste(ims[n],(col*960,0));draw.text((col*960+6,543),f'{a["id"] if col==0 else b["id"]}: actual master frame {n} / {n/24:.6f}s',fill='white')
  can.save(p,quality=88);join_rows.append({'index':i,'left':a['id'],'right':b['id'],'master_frame':k,'seconds':k/24,'actually_extracted_frames':[k-1,k],'file':name,'sha256':sha(p)})
 for s,n in zip(shots,mids):
  name=f'shot-{s["id"]}-mid-{n}.jpg';p=D/name;assert not p.exists();ims[n].save(p,quality=88);shot_rows.append({'id':s['id'],'range':[s['start_frame'],s['end_frame_exclusive']],'mid_frame':n,'file':name,'sha256':sha(p)})
 for offset in range(0,len(shot_rows),12):
  group=shot_rows[offset:offset+12];can=Image.new('RGB',(1440,1160),'#151515');draw=ImageDraw.Draw(can)
  for i,row in enumerate(group):
   x,y=(i%3)*480,(i//3)*290;can.paste(ims[row['mid_frame']].resize((480,270)),(x,y));draw.text((x+6,y+273),f'{row["id"]} / {row["mid_frame"]/24:.3f}s',fill='white')
  p=D/f'overview-{offset//12:02}.jpg';assert not p.exists();can.save(p,quality=88)
 native_targets={'opening':96,'cup-action':890,'keyboard-symbol':690,'vocal-fix':1945,'guitar-crop-first':2042,'drum-first':3660,'keyboard-fix':4197,'band-wide':4520,'first-plea':5030,'drum-late':5870,'guitar-crop-tail':6167,'final-tear':6620,'final-picture':6666}
 native,cmd2=decode_selected(list(native_targets.values()),1920,1080);native_rows=[]
 for label,n in native_targets.items():
  name=f'native-{label}-{n}.jpg';p=D/name;assert not p.exists();native[n].save(p,quality=94);native_rows.append({'label':label,'frame':n,'file':name,'sha256':sha(p)})
 record={'schema':'jml-performance-final-director-evidence/v1','master':{'path':str(SRC.relative_to(ROOT)),'sha256':MASTER_SHA,'bytes':SRC.stat().st_size},'edit':{'path':str(EDIT.relative_to(ROOT)),'sha256':EDIT_SHA},'scope':'Exact actual master cut pairs and chronological mid-shot JPEGs. Cut comparison scaled960x540;13 target output-native1920x1080JPEGs. No production edits/raw disk dumps or creative verdict.','joins':join_rows,'shots':shot_rows,'native_targets':native_rows,'selected_frame_indices':nums,'commands':[cmd1,cmd2],'retained_workflow':{'path':'productions/join-me-in-life/full-film/unfinished-morning/review/full-film-v1/extract.py','sha256':sha(ROOT/'productions/join-me-in-life/full-film/unfinished-morning/review/full-film-v1/extract.py')}}
 out.write_text(json.dumps(record,indent=2)+'\n');print('45 actual join pairs,46 mid-shot JPEGs,4 overviews and13 target-native JPEGs ready',flush=True)
if __name__=='__main__':main()
