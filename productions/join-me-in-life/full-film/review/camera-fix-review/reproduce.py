"""Focused encoded camera/seam checks. No production source/config changes."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
FILM=HERE.parent.parent
REPO=FILM.parents[2]
RAW=REPO/'build/camera-fix-review'
RAW.mkdir(parents=True,exist_ok=True)
WORKPRINT=FILM/'exports/Join_Me_in_Life_Full_Hybrid_Workprint_v1.mp4'
assert hashlib.sha256(WORKPRINT.read_bytes()).hexdigest()=='f5f43c7adfae9a7820c873a69c86564ad0123b2eba86e353c824b4b764dbd5fc'
old_manifest=json.loads(WORKPRINT.with_suffix('.manifest.json').read_text())
config='424864992036d0c9b6bbc88cc4543913432da7e18151e2506953a60d7901a3a5'
items=[('Waiting','745b0e6ebec2120afbde1177fb34faadfefececa6c3bdb9d0c85275d5d1fc118',[132]),
       ('Aftermath','cb7981f840ab42c6c19e1c14f705c8c08747634b4f97774c6e7a547ca0628ccf',[96,194])]
report=[];overview=[]

def framehash(video,start=None,end=None):
    cmd=['ffmpeg','-v','error','-i',str(video),'-map','0:v:0']
    if start is not None:cmd+=['-vf',f'select=between(n\\,{start}\\,{end-1})','-vsync','0']
    text=subprocess.check_output(cmd+['-f','framemd5','-'],text=True)
    return [line.split(',')[-1].strip() for line in text.splitlines() if not line.startswith('#')]

for label,digest,seams in items:
    video=FILM/f'exports/Join_Me_in_Life_{label}_Join_Fix_Proof.mp4'
    assert hashlib.sha256(video.read_bytes()).hexdigest()==digest
    m=json.loads(video.with_suffix('.manifest.json').read_text());assert m['edit_config']['sha256']==config
    origin=m['coverage']['start_frame'];end=m['coverage']['end_frame_exclusive']
    selected=set()
    for s in m['shots']:
        a,b=s['start_frame']-origin,s['end_frame_exclusive']-origin
        selected.update([a,(a+b-1)//2,b-1])
    for n in seams:selected.update([n-2,n-1,n,n+1])
    selected=sorted(selected)
    vf='select='+ '+'.join(f'eq(n\\,{n})' for n in selected)
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-an','-vf',vf,'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'])
    rgb=np.frombuffer(data,np.uint8).reshape(len(selected),540,960,3)
    frames={n:Image.fromarray(rgb[i]) for i,n in enumerate(selected)}
    for n,im in frames.items():im.save(RAW/f'{label.lower()}-{n:04}.jpg',quality=94,subsampling=0)
    deltas=[]
    for seam in seams:
        sheet=Image.new('RGB',(1920,570),'#181818');draw=ImageDraw.Draw(sheet)
        for col,n in enumerate([seam-1,seam]):
            draw.text((col*960+8,7),f'{label} corrected | local f{n} | full f{n+origin} / {(n+origin)/24:.6f}s',fill='white')
            sheet.paste(frames[n],(col*960,30))
        sheet.save(HERE/f'{label.lower()}-seam-{seam}.jpg',quality=89,subsampling=0)
        a=np.asarray(frames[seam-1]).astype(np.int16);b=np.asarray(frames[seam]).astype(np.int16)
        deltas.append({'local_seam_frame':seam,'full_seam_frame':seam+origin,'mean_absolute_rgb_difference':float(np.abs(a-b).mean())})
    for s in m['shots']:
        a,b=s['start_frame']-origin,s['end_frame_exclusive']-origin
        overview.append((s['id'],[(n,frames[n]) for n in [a,(a+b-1)//2,b-1]],origin))
        old=next(x for x in old_manifest['shots'] if x['id']==s['id'])
        for key in ['start_frame','end_frame_exclusive','source','drawn_art_segments']:
            assert s.get(key)==old.get(key),(s['id'],key)
    oldhash=framehash(WORKPRINT,origin,end);newhash=framehash(video)
    assert len(oldhash)==len(newhash)==m['frames']
    changed=[i+origin for i,(a,b) in enumerate(zip(oldhash,newhash)) if a!=b]
    report.append({'label':label,'video_sha256':digest,'config_sha256':config,'frames':m['frames'],
        'full_coverage':[origin,end],'changed_full_frames_vs_workprint_v1':{'count':len(changed),'first':min(changed),'last':max(changed)},
        'shot_timing_source_and_drawing_records_unchanged':True,'seams':deltas,
        'audio_check_from_render_manifest':m['audio']['waveform_check'],'audio_check_independently_rerun':False})

sheet=Image.new('RGB',(1440,len(overview)*290),'#181818');draw=ImageDraw.Draw(sheet)
for row,(shot,frames,origin) in enumerate(overview):
    for col,(n,im) in enumerate(frames):
        x,y=col*480,row*290
        draw.text((x+4,y+4),f'{shot} {("first","middle","last")[col]} full f{n+origin}',fill='white')
        sheet.paste(im.resize((480,270),Image.Resampling.LANCZOS),(x,y+20))
sheet.save(HERE/'first-middle-last.jpg',quality=85,subsampling=0)
(HERE/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
