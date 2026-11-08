from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent
phase={'start':0,'mid':1,'end':2}
fs=sorted(D.glob('C??-*-*.jpg'),key=lambda p:(p.name[:3],phase[p.name.split('-')[1]]))
for n in range(0,len(fs),12):
 group=fs[n:n+12]
 if len(group)<12 and len(fs)<117:continue
 out=Image.new('RGB',(1440,4*290),'#222')
 for j,p in enumerate(group):
  im=Image.open(p).resize((480,270));x=(j%3)*480;y=(j//3)*290;out.paste(im,(x,y));ImageDraw.Draw(out).text((x+5,y+272),p.stem,fill='white')
 out.save(D/f'overview-{n//12:02}.jpg',quality=88)
print('captured',len(fs))
