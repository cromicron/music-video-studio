"""Review-only evidence for frozen geometry-only v2/v3 waiting contexts.

No production writes or provider calls. Run from any directory. Raw output is
ignored build/r1-waiting-seam-v2-review; retain_evidence.py keeps compact files.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE = ROOT/'productions/join-me-in-life/full-film'
OUT = ROOT/'build/r1-waiting-seam-v2-review'
OUT.mkdir(parents=True, exist_ok=True)
SPECS = {
 'v1': ('Waiting_Correction_Context_Proof', 'b1f61bd2b17ec7e05596d0add089902a17cb300c14e86dc239c9c83ed577e4f8'),
 'v2': ('Waiting_Correction_Context_Proof_v2', 'aa2fe01cec22d7c9d918f397f27e96f67c0395d6be16ba178067e5c61fb38d7a'),
 'v3': ('Waiting_Correction_Context_Proof_v3', 'c432ad864108a1f1700c84b5b7a61f16353b0b2d250eb080d3eeff062ba959a6'),
}
checks, hashes = {}, {}
for version, (name, digest) in SPECS.items():
    p = BASE/f'exports/Join_Me_in_Life_{name}.mp4'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
    m = json.loads(p.with_suffix('.manifest.json').read_text())
    assert m['output_sha256'] == digest
    md5 = subprocess.check_output(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-f','framemd5','-'],text=True)
    hashes[version] = [s.split(',')[-1].strip() for s in md5.splitlines() if not s.startswith('#')]
    (OUT/f'{version}.framemd5').write_text(md5)
    checks[version] = {'sha256':digest, 'config_sha256':m['edit_config']['sha256'],
                       'manifest_sha256':hashlib.sha256(p.with_suffix('.manifest.json').read_bytes()).hexdigest(),
                       'frames':len(hashes[version]), 'full_picture_decode':'passed'}
    if version == 'v1':
        continue
    ids = [276,277,278,279,280,281,414] if version == 'v2' else [278,279,414,415,416,551,552,553,554,648]
    select = '+'.join(f'eq(n\\,{i})' for i in ids)
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf',f'select={select}',
                                  '-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
    frames = np.frombuffer(raw,np.uint8).reshape(-1,540,960,3)
    assert len(frames) == len(ids)
    data = dict(zip(ids, frames))
    checks[version]['pads'] = {}
    for index, frame in data.items():
        Image.fromarray(frame).save(OUT/f'{version}-native-{index:03}.jpg', quality=96)
        active = np.where(frame[20:520].mean(axis=(0,2))>8)[0]
        checks[version]['pads'][str(index)] = [int(active[0]),int(959-active[-1])]
    pairs = [(278,279)] if version=='v2' else [(278,279),(414,415),(552,553)]
    sheet = Image.new('RGB',(1920,len(pairs)*566),'#171717'); draw=ImageDraw.Draw(sheet)
    for row, pair in enumerate(pairs):
        for col, index in enumerate(pair):
            x,y=col*960,row*566
            draw.text((x+5,y+6),f'{version} local f{index} / master f{1994+index}',fill='white')
            sheet.paste(Image.fromarray(data[index]),(x,y+26))
    sheet.save(OUT/f'{version}-joins-native.jpg', quality=95)
    if version=='v3':
        checks[version]['S020_to_S021_mean_abs_RGB_difference'] = float(np.abs(data[414].astype(np.int16)-data[415].astype(np.int16)).mean())
checks['comparisons'] = {
 'v1_v2_S018_S019_all_279_frames_identical': hashes['v1'][:279]==hashes['v2'][:279],
 'v2_v3_first_415_frames_identical': hashes['v2']==hashes['v3'][:415],
}
assert all(checks['comparisons'].values())
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
