from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
D=Path(__file__).resolve().parent;p=json.loads((D/'playback-v1.json').read_text());caps=p['captures'];out=[]
for start in range(0,len(caps),4):
 can=Image.new('RGB',(1440,900));draw=ImageDraw.Draw(can)
 for j,c in enumerate(caps[start:start+4]):
  f=Path(c['file']);assert hashlib.sha256(f.read_bytes()).hexdigest()==c['sha256'];im=Image.open(f);im.thumbnail((720,425));x=(j%2)*720;y=(j//2)*450;can.paste(im,(x,y));draw.text((x,y+425),f'{c["label"]} actual{c["actual_before_screenshot_seconds"]:.4f}s',fill='white')
 f=D/f'actual-playback-overview-{start//4+1:02}.jpg';assert not f.exists();can.save(f,quality=91);out.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'capture_labels':[c['label'] for c in caps[start:start+4]]})
(D/'montage-v1.json').write_text(json.dumps({'source_playback_sha256':hashlib.sha256((D/'playback-v1.json').read_bytes()).hexdigest(),'method':'Only resized actual browser JPEG screenshots; no production-image alteration. Exact boundary judgment uses separately decoded final indices.','montages':out},indent=2)+'\n')
cb=json.loads((D/'presented-frame-callbacks-v1.json').read_text());gaps=[{'after_media':a[0],'next_media':b[0],'media_gap':b[0]-a[0],'presented_delta':b[1]-a[1]} for a,b in zip(cb,cb[1:]) if b[0]-a[0]>.06]
print('montages',len(out),'callback gaps over60ms',gaps)
