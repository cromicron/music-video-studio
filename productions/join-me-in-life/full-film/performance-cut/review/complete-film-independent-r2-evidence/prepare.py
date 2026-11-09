from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,hashlib,datetime
D=Path(__file__).resolve().parent;R=Path('/workspace/music-video-studio');P=R/'productions/join-me-in-life/full-film/performance-cut';F=P.parent
S=R/'build/performance-cut-final-v1/Join_Me_in_Life_Movie_and_Band.mp4';E=P/'edit/edit-v009.json'
expected='fabe33c576aaa0473e82c6ed755e884e3b6bc9103f392551138f6527099f2fdb'
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
assert sha(S)==expected and S.stat().st_size==196409309
assert sha(E)=='7aa3b495ec21db1836427080e9cab23a837f97c7fa737d5fdea9f48176e03d80'
e=json.loads(E.read_text());assert len(e['shots'])==46 and e['total_frames']==6667
cuts=[s['start_frame'] for s in e['shots'][1:]];nums=sorted({n for k in cuts for n in [k-2,k-1,k,k+1]}|{(s['start_frame']+s['end_frame_exclusive'])//2 for s in e['shots']})
commands=[]
def decode(ns,w,h):
 ranges=[]
 for n in ns:
  if ranges and n==ranges[-1][1]+1:ranges[-1][1]=n
  else:ranges.append([n,n])
 terms=[f'eq(n,{a})' if a==z else f'between(n,{a},{z})' for a,z in ranges]
 def balanced(ts):
  if len(ts)==1:return ts[0]
  mid=len(ts)//2;return '('+balanced(ts[:mid])+'+'+balanced(ts[mid:])+')'
 select=balanced(terms)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-threads','2','-i',str(S),'-vf',f"select='{select}',scale={w}:{h}:flags=lanczos",'-fps_mode','passthrough','-threads','1','-f','rawvideo','-pix_fmt','rgb24','-']
 commands.append(cmd);p=subprocess.Popen(cmd,stdout=subprocess.PIPE);out={};size=w*h*3
 for n in ns:
  data=p.stdout.read(size);assert len(data)==size,(n,len(data));out[n]=Image.frombytes('RGB',(w,h),data)
 assert not p.stdout.read(1);assert p.wait()==0
 return out
ims=decode(nums,480,270)
proofs=[]
for start in range(0,45,3):
 can=Image.new('RGB',(1920,870));draw=ImageDraw.Draw(can)
 for row,i in enumerate(range(start,min(start+3,45))):
  k=cuts[i];a=e['shots'][i];b=e['shots'][i+1]
  for col,n in enumerate([k-2,k-1,k,k+1]):can.paste(ims[n],(col*480,row*290));draw.text((col*480,row*290+270),f'cut{i+1:02} {a["id"]}>{b["id"]} frame{n}',fill='white')
 p=D/f'cuts-{start+1:02}-{min(start+3,45):02}.jpg';assert not p.exists();can.save(p,quality=91);proofs.append(p.name)
for start in range(0,46,12):
 ss=e['shots'][start:start+12];can=Image.new('RGB',(1440,1160));draw=ImageDraw.Draw(can)
 for j,s in enumerate(ss):
  n=(s['start_frame']+s['end_frame_exclusive'])//2;x=(j%3)*480;y=(j//3)*290;can.paste(ims[n],(x,y));draw.text((x,y+270),f'{s["id"]} {n}/24={n/24:.2f}s {s["world"]}',fill='white')
 p=D/f'shot-middles-{start+1:02}-{min(start+12,46):02}.jpg';assert not p.exists();can.save(p,quality=91);proofs.append(p.name)
# Targeted output-native frames from actual repaired/critical shots. Retain only seven meaningful frames.
focus={'O01':120,'O02':900,'B04':1750,'B05B':1950,'B06_B':6170,'B10':4200,'O04':6650}
for n,im in decode(sorted(focus.values()),1920,1080).items():
 shot=next(k for k,v in focus.items() if v==n);p=D/f'native-{shot}-{n:04}.jpg';assert not p.exists();im.save(p,quality=96);proofs.append(p.name)
# Read-only source/gate hash chain and all selected range nonoverlap checks.
sources={};reviews={};ranges={}
for s in e['shots']:
 sd=e['sources'][s['source']['id']];p=F/sd['path'];actual=sha(p);assert actual==sd['sha256'];sources[sd['path']]=actual
 rv=sd['review'];rp=F/rv['path'];assert sha(rp)==rv['sha256'];reviews[rv['path']]=rv['sha256']
 a,z=s['source']['in_frame'],s['source']['out_frame_exclusive'];assert z-a==s['end_frame_exclusive']-s['start_frame'];ranges.setdefault(sd['path'],[]).append([a,z,s['id']])
 for aa,zz in rv['accepted_ranges']:
  if aa<=a<z<=zz:break
 else:raise AssertionError(('outside reviewed range',s['id']))
for path,rr in ranges.items():
 rr.sort()
 for a,z in zip(rr,rr[1:]):assert a[1]<=z[0],('reused',path,a,z)
record={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'master':str(S),'master_sha256':expected,'master_bytes':S.stat().st_size,'edit':str(E),'edit_sha256':sha(E),'editorial_v3_sha256':sha(P/'story/editorial-plan-v3.json'),'provider_plan_sha256':sha(P/'story/shot-plan-v1.json'),'all45cut_frames':cuts,'boundary_indices':sorted({n for k in cuts for n in [k-2,k-1,k,k+1]}),'shot_midpoints':[(s['id'],(s['start_frame']+s['end_frame_exclusive'])//2) for s in e['shots']],'native_targets':focus,'source_hashes':sources,'review_gate_hashes':reviews,'no_repeated_source_intervals':True,'all_sources_and_gates_hash_verified':True,'commands':commands,'proof_files':proofs,'scope':'Actual final-master compact exact cut windows/midpoints and7output-native targets; source/gate checks do not replace full-film playback or visual judgments.'}
(D/'preparation-v1.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'proofs':len(proofs),'sources':len(sources),'cuts':len(cuts),'heavy_prep':'complete'}))
