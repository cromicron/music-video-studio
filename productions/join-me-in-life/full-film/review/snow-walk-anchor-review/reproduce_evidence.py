"""Reproduce static anchor-review JPEGs; original images remain read-only.
Requires Pillow and numpy. Outputs stay under ignored root build/.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'studio.json').is_file())
BASE=ROOT/'productions/join-me-in-life/full-film/assets';OUT=ROOT/'build/snow-walk-anchor-review'
SOURCES=[('snow_journey_refined_candidate.png','58198431a0673f8fabe4f0728d6f53b337542cf6518f132d067e83f032cca0e1'),('snow_journey_end_candidate.png','bf94d17c837ce88cf3833e8498ffd9620e899e27b08f2ab55c7523ddabac9792')]
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);images=[];records=[]
 for filename,expected in SOURCES:
  path=BASE/filename;actual=hashlib.sha256(path.read_bytes()).hexdigest()
  if actual!=expected:raise RuntimeError('Source hash differs')
  im=Image.open(path).convert('RGB');images.append(im);records.append({'file':str(path.relative_to(ROOT)),'sha256':actual,'size':im.size})
 a,b=images
 panels=[('START native legs/contact',a.crop((610,455,815,805))),('END native legs/contact',b.crop((875,460,1045,700))),('END detail 2x nearest',b.crop((895,540,1002,676)).resize((214,272),Image.Resampling.NEAREST))]
 im=Image.new('RGB',(630,390),'#161616');d=ImageDraw.Draw(im);x=0
 for label,pic in panels:d.text((x+5,5),label,fill='white');im.paste(pic,(x,30));x+=pic.width+10
 im.save(OUT/'legs-contact.jpg',quality=95)
 for name,img in [('start',a),('end',b)]:img.resize((960,540),Image.Resampling.LANCZOS).save(OUT/f'{name}-normal.jpg',quality=92)
 rects=[('Right path edge',(1100,570,1540,790)),('Door/building',(1050,300,1400,530)),('Left curb behind start',(400,500,800,710))]
 canvas=Image.new('RGB',(900,760),'#171717');d=ImageDraw.Draw(canvas);y=0
 for label,box in rects:
  d.text((5,y+5),label+' / start',fill='white');d.text((455,y+5),label+' / end',fill='white')
  canvas.paste(a.crop(box),(0,y+25));canvas.paste(b.crop(box),(450,y+25));y+=box[3]-box[1]+35
 canvas.save(OUT/'background-detail.jpg',quality=95)
 diff=np.abs(np.asarray(a).astype(np.int16)-np.asarray(b).astype(np.int16))
 Image.fromarray(np.clip(diff*3,0,255).astype(np.uint8)).resize((960,540)).save(OUT/'difference-3x.jpg',quality=91)
 (OUT/'sources.json').write_text(json.dumps({'scope':'Static eligibility only, no generated gait reviewed','sources':records,'detailCropCoordinates':{'startLegs':[610,455,815,805],'endLegs':[875,460,1045,700],'endFeet2x':[895,540,1002,676]},'approximateManualFigureBounds':{'start':[622,252,788,769],'end':[898,321,1002,662]},'measurementCaveat':'Hand-marked approximate silhouette bounds, not segmentation or physical camera calibration. Footprint artwork is not a timed gait trace.'},indent=2)+'\n')
 print(json.dumps(records,indent=2))
