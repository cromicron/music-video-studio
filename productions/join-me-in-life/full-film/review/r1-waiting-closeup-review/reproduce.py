"""Frozen V4 closeup evidence; no production writes or provider calls."""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film'
OUT=ROOT/'build/r1-waiting-closeup-review'; OUT.mkdir(parents=True,exist_ok=True)
CONFIG='ff0a2d0e310c558d5c3105a7c62165ea483ce14e610ec233e59fa44ba21d24ce'
SPECS=[('v4',BASE/'exports/Join_Me_in_Life_Waiting_Correction_Context_Proof_v4.mp4',
        'bddab2a000823c2298679bb698be43c80daa36cee8ab8316ad5578dcbfbf7a10',960,540,649),
       ('1080',ROOT/'build/r1-waiting-closeup-1080.mp4',
        'd0c3a6963324d53a6581b3ef137858968773fd821fdab01071062fb40c177704',1920,1080,136)]
def selected(p, ids, w, h):
    filt='select='+'+'.join(f'eq(n\\,{n})' for n in ids)
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf',filt,'-fps_mode','passthrough',
                                 '-f','rawvideo','-pix_fmt','rgb24','-'])
    f=np.frombuffer(raw,np.uint8).reshape(-1,h,w,3)
    assert len(f)==len(ids)
    return dict(zip(ids,f))
checks={'config_sha256':CONFIG}
for label,p,digest,w,h,n in SPECS:
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    m=json.loads(p.with_suffix('.manifest.json').read_text())
    assert m['output_sha256']==digest and m['edit_config']['sha256']==CONFIG
    md5=subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-f','framemd5','-'],text=True)
    hashes=[s.split(',')[-1].strip() for s in md5.splitlines() if not s.startswith('#')]
    assert len(hashes)==n
    (OUT/f'{label}.framemd5').write_text(md5)
    checks[label]={'path':str(p.relative_to(ROOT)),'sha256':digest,'frames':n,'full_picture_decode':'passed',
                   'manifest_sha256':hashlib.sha256(p.with_suffix('.manifest.json').read_bytes()).hexdigest()}
    if label=='v4':
        prev=ROOT/'build/r1-waiting-seam-v2-review/v3.framemd5'
        if not prev.is_file():
            prior=BASE/'exports/Join_Me_in_Life_Waiting_Correction_Context_Proof_v3.mp4'
            assert hashlib.sha256(prior.read_bytes()).hexdigest()=='c432ad864108a1f1700c84b5b7a61f16353b0b2d250eb080d3eeff062ba959a6'
            old=subprocess.check_output(['ffmpeg','-v','error','-i',str(prior),'-map','0:v:0','-f','framemd5','-'],text=True)
        else:
            old=prev.read_text()
        old=[s.split(',')[-1].strip() for s in old.splitlines() if not s.startswith('#')]
        checks[label]['S018_S019_all_279_frames_identical_to_v3']=hashes[:279]==old[:279]
        checks[label]['S022_all_96_frames_identical_to_v3']=hashes[553:]==old[553:]
        assert checks[label]['S018_S019_all_279_frames_identical_to_v3'] and checks[label]['S022_all_96_frames_identical_to_v3']
        ids=[278,279,414,415,552,553]
        data=selected(p,ids,w,h)
        sheet=Image.new('RGB',(1920,3*566),'#171717');draw=ImageDraw.Draw(sheet)
        for row,pair in enumerate([(278,279),(414,415),(552,553)]):
            for col,index in enumerate(pair):
                x,y=col*960,row*566;draw.text((x+5,y+6),f'V4 local f{index} / master f{1994+index}',fill='white')
                sheet.paste(Image.fromarray(data[index]),(x,y+26))
        sheet.save(OUT/'v4-joins-native.jpg',quality=95)
    else:
        ids=[0]+list(range(64,73))+[135]
        data=selected(p,ids,w,h)
        for index in [0,68,135]: Image.fromarray(data[index]).save(OUT/f'1080-native-{index:03}.jpg',quality=96)
        Image.fromarray(data[0][:290,200:1450]).save(OUT/'1080-native-crown.jpg',quality=98)
        sheet=Image.new('RGB',(1590,3*226),'#171717');draw=ImageDraw.Draw(sheet)
        for j,index in enumerate(range(64,73)):
            x,y=j%3*530,j//3*226;draw.text((x+5,y+5),f'S020 f{index} / master f{2273+index}',fill='white')
            sheet.paste(Image.fromarray(data[index]).crop((520,520,1050,720)),(x,y+26))
        sheet.save(OUT/'1080-eye-phases-native.jpg',quality=96)
        checks[label]['first_last_mean_abs_RGB_difference']=float(np.abs(data[0].astype(np.int16)-data[135].astype(np.int16)).mean())
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
