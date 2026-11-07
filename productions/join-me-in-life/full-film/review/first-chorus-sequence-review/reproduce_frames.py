"""Bounded S014 placement QA. Read-only sources; fresh output under root build/.
Requires FFmpeg/ffprobe, Pillow and numpy. No provider calls.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess,numpy as np
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
FILM=ROOT/'productions/join-me-in-life/full-film';OUT=ROOT/'build/first-chorus-sequence-review'
SOURCE=FILM/'assets/motion/ltx23-performance-pilots/S014/video-silent.mp4'
SINGLE=FILM/'exports/Join_Me_in_Life_First_Chorus_Contain_Proof_v2.mp4'
CONTEXT=FILM/'exports/Join_Me_in_Life_First_Chorus_Context_Proof_v2.mp4'
CONTAIN='scale=944:540:flags=lanczos,pad=960:540:8:0:color=black,setsar=1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(p,flt,w,h):
 command=['ffmpeg','-v','error','-i',str(p),'-map','0:v:0']
 if flt:command+=['-vf',flt]
 command+=['-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-']
 return np.frombuffer(subprocess.check_output(command),dtype=np.uint8).reshape(-1,h,w,3)
def sheet(name,items,size=(480,270),cols=2):
 w,h=size;im=Image.new('RGB',(cols*w,((len(items)+cols-1)//cols)*(h+25)),'#171717');d=ImageDraw.Draw(im)
 for j,(label,pic) in enumerate(items):
  x=j%cols*w;y=j//cols*(h+25);d.text((x+5,y+5),label,fill='white');im.paste(Image.fromarray(pic).resize(size),(x,y+25))
 im.save(OUT/name,quality=92)
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 expected={SOURCE:'8756ad09d45ecfe47bb2a4cead5f5184d3bd4a4561cbc27e9495cdb6170a0252',SINGLE:'5588132a1628cb760703167e4b2d7a415c30684bd883ec828605b9d7d5fb15e1',CONTEXT:'6bed5d22f2f93929cbb6310848e1836cc3891d3b8b2bb5a46d9fa40ea8906114'}
 for p,digest in expected.items():
  if sha(p)!=digest:raise RuntimeError('Source/proof hash differs')
 indices=[0,75,146,147,148,149,150,151,158,182,220,244,245,246,247,248,249,300,347]
 select='+'.join(fr'eq(n\,{i})' for i in indices)
 context=dict(zip(indices,raw(CONTEXT,'select='+select,960,540)))
 single=raw(SINGLE,'',960,540)
 ideal=raw(SOURCE,'trim=start_frame=3:end_frame=101,'+CONTAIN,960,540)
 if len(single)!=98 or len(ideal)!=98:raise RuntimeError('Wrong selected frame count')
 sheet('context-cuts.jpg',[(f'context f{i} | master {(1447+i)/24:.6f}s',context[i]) for i in [146,147,148,149,150,151,244,245,246,247,248,249]],cols=3,size=(480,270))
 sheet('context-overview.jpg',[(f'context f{i} | master {(1447+i)/24:.6f}s',context[i]) for i in [0,75,148,149,158,182,220,246,247,300,347]],cols=3,size=(320,180))
 sheet('expected-vs-encoded.jpg',[(label,pic) for i in [0,9,33,97] for label,pic in [(f'full source f{i+3} contained reference',ideal[i]),(f'encoded insertion f{i}',single[i])]])
 for i in [0,9,21,33,47,71,97]:Image.fromarray(single[i]).save(OUT/f'normal-insertion-f{i:02}.jpg',quality=93)
 # Nearest images at low resolution identify source order; lossy encoding is not byte equality.
 ref=raw(SOURCE,CONTAIN+',scale=160:90',160,90).astype(np.int16)
 actual=raw(SINGLE,'scale=160:90',160,90).astype(np.int16)
 matches=[]
 for i,pic in enumerate(actual):
  errors=np.abs(ref-pic).mean(axis=(1,2,3));best=int(errors.argmin())
  matches.append({'insertionFrame':i,'expectedSourceFrame':i+3,'nearestSourceFrame':best,'expectedMeanAbsoluteRgbError':float(errors[i+3]),'nearestMeanAbsoluteRgbError':float(errors[best])})
 context_s014=raw(CONTEXT,'trim=start_frame=149:end_frame=247,scale=160:90',160,90).astype(np.int16)
 probes=[]
 for p in [SINGLE,CONTEXT]:
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
  pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(p)]))['frames']
  probes.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p),'videoFrames':len(pts),'maxPtsDeviationFromIndexOver24':max(abs(float(f['best_effort_timestamp_time'])-i/24) for i,f in enumerate(pts)),'probe':info})
 checks={'scope':'Independent picture/cadence checks; not listening or phoneme sync','proofs':probes,'sourceSha256':sha(SOURCE),'sourceFramesZeroBasedEndExclusive':[3,101],'containReferenceFilter':CONTAIN,'nearestExpectedSourceMatches':sum(x['nearestSourceFrame']==x['expectedSourceFrame'] for x in matches),'sourceFrameMapping':matches,'singleVsContainedReferenceMaxMeanAbsRgbError':float(np.abs(single.astype(np.int16)-ideal.astype(np.int16)).mean(axis=(1,2,3)).max()),'contextVsStandaloneMaxMeanAbsRgbErrorAt160x90':float(np.abs(context_s014-actual).mean(axis=(1,2,3)).max()),'contextCutsZeroBased':[149,247],'masterCutSeconds':[66.5,70.58333333333333],'expectedFitPixels':{'image':[944,540],'leftPad':8,'rightPad':8},'audioAlignmentIndependentlyRerun':False}
 colmean=single[:,20:520,:,:].mean(axis=(0,1,3));left=next(i for i,v in enumerate(colmean) if v>8);right=next(i for i,v in enumerate(colmean[::-1]) if v>8)
 checks['observedSidePadding']={'left':left,'right':right,'method':'Mean RGB per column over all98 frames and rows20:520; first picture column exceeds8/255. Compression ringing means padded edge pixels are not all exactly zero.','left12MeanRgb':colmean[:12].tolist(),'right12MeanRgb':colmean[-12:].tolist()}
 def hashes(path,flt=None):
  cmd=['ffmpeg','-v','error','-i',str(path),'-map','0:v:0']
  if flt:cmd+=['-vf',flt]
  cmd+=['-fps_mode','passthrough','-f','framemd5','-']
  return [line.rsplit(',',1)[-1].strip() for line in subprocess.check_output(cmd,text=True).splitlines() if not line.startswith('#')]
 aa=hashes(SINGLE);bb=hashes(CONTEXT,'trim=start_frame=149:end_frame=247')
 checks['contextVsStandaloneDecodedFrameHashes']={'comparedFrames':len(aa),'exactDecodedFrameHashMatches':sum(x==y for x,y in zip(aa,bb)),'allEqual':aa==bb}
 (OUT/'encoded-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(json.dumps({k:v for k,v in checks.items() if k not in ['proofs','sourceFrameMapping']},indent=2))
