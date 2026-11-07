"""Final-size picture evidence for the frozen 44-shot cache; no production writes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess
import numpy as np
from PIL import Image,ImageDraw

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
OUT=ROOT/'build/stable-1080-picture-review';OUT.mkdir(parents=True,exist_ok=True)
HERE=Path(__file__).resolve().parent
INVENTORY=HERE/'cache-inventory.json'
if not INVENTORY.exists():INVENTORY=ROOT/'build/final-stable-shot-cache-prep.json'
inv=json.loads(INVENTORY.read_text())
if not (OUT/'frozen-plan.json').exists():(OUT/'frozen-plan.json').write_bytes((HERE/'frozen-plan.json').read_bytes())
plan={s['id']:s for s in json.loads((OUT/'frozen-plan.json').read_text())['shots']}
assert inv['config_sha256']=='ff0a2d0e310c558d5c3105a7c62165ea483ce14e610ec233e59fa44ba21d24ce'
KEY={'S001','S003','S011','S013','S014','S019','S020','S025','S026','S028','S030','S032','S044','S046','S053'}
def inspect(entry):
    sid=entry['id'];p=ROOT/entry['path'];n=entry['frames'];s=plan[sid]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],sid
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams']
    assert len(streams)==1 and streams[0]['codec_type']=='video',sid
    v=streams[0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',n),sid
    ids={0,n//2,n-1}
    if sid in KEY:ids.update([n//4,3*n//4])
    if sid=='S001':ids.update([8,9,18,24,99,100,112,115,116])
    if sid=='S025':ids.update([31,62,63,64,86])
    if sid=='S028':ids.update([45,91,92,93,122,152,182,211,212,213,251])
    for part in s.get('drawn_art_segments',[]):
        offset=part['start_frame']-s['start_frame'];ids.update([offset,offset+part['frames']-1])
        for patch in part['patches']:
            if patch.get('opacity_keys'):ids.update(offset+k[0] for k in patch['opacity_keys'])
            if patch.get('runs'):
                a,b=patch['runs'][0];ids.add(offset+(a+b-1)//2)
    ids=sorted(i for i in ids if 0<=i<n)
    filt='select='+'+'.join(f'eq(n\\,{i})' for i in ids)
    raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(p),'-vf',filt,
                                 '-filter_threads','1','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(-1,1080,1920,3);assert len(frames)==len(ids),sid
    data=dict(zip(ids,frames));folder=OUT/sid;folder.mkdir(exist_ok=True)
    for i,frame in data.items():Image.fromarray(frame).save(folder/f'f{i:03}.jpg',quality=95)
    overview=Image.new('RGB',(1440,296),'#171717');d=ImageDraw.Draw(overview)
    for col,i in enumerate([0,n//2,n-1]):
        d.text((col*480+5,5),f'{sid} f{i}/{n} | {s["source_key"]}',fill='white')
        overview.paste(Image.fromarray(data[i]).resize((480,270),Image.Resampling.LANCZOS),(col*480,26))
    overview.save(folder/'first-mid-end.jpg',quality=91)
    if sid in KEY or s.get('drawn_art_segments'):
        sheet=Image.new('RGB',(1440,((len(ids)+2)//3)*296),'#171717');d=ImageDraw.Draw(sheet)
        for j,i in enumerate(ids):
            x,y=j%3*480,j//3*296;d.text((x+5,y+5),f'{sid} f{i} | {i/24:.3f}s',fill='white')
            sheet.paste(Image.fromarray(data[i]).resize((480,270),Image.Resampling.LANCZOS),(x,y+26))
        sheet.save(folder/'phases.jpg',quality=92)
    pads={}
    for i,frame in data.items():
        active=np.where(frame[40:1040].mean(axis=(0,2))>8)[0]
        pads[str(i)]=[int(active[0]),int(1919-active[-1])]
    result={**entry,'dimensions':[1920,1080],'fps':'24/1','audio_streams':0,'selected_frames':ids,
            'decode_to_last_frame':'passed','column_pad_estimates':pads,'classification':s['classification']}
    print(sid,'complete',flush=True)
    return result
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(inspect,inv['shots']))
for start in range(0,len(results),5):
    batch=results[start:start+5];sheet=Image.new('RGB',(1440,len(batch)*296),'#171717')
    for j,s in enumerate(batch):sheet.paste(Image.open(OUT/s['id']/'first-mid-end.jpg'),(0,j*296))
    sheet.save(OUT/f'overview-{start//5+1:02}.jpg',quality=91)
(OUT/'cache-checks.json').write_text(json.dumps({'inventory_sha256':hashlib.sha256(INVENTORY.read_bytes()).hexdigest(),
 'config_sha256':inv['config_sha256'],'scope':'44 frozen silent cached shots; picture framing review, not full-film or soundtrack acceptance',
 'shots':results},indent=2)+'\n')
